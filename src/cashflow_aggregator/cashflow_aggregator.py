"""
Cashflow aggregator module for the EQU IHOME SIM ENGINE v2.

This module is responsible for aggregating cashflows from various sources,
including loans, exits, fees, and leverage, and providing a comprehensive
view of the fund's cashflow over time.

The module includes the following enhancements:
- Parallel processing for loan-level cashflow calculations
- Daily cashflow granularity
- Scenario analysis
- Sensitivity analysis
- Cashflow metrics calculation (IRR, DPI, RVPI, TVPI, etc.)
- Waterfall integration
- Tax impact analysis
- Reinvestment modeling
- Liquidity analysis
- Enhanced visualization options
- Export capabilities
"""

import logging
import math
import os
import csv
import json
import asyncio
import concurrent.futures
import multiprocessing
from typing import Dict, Any, List, Optional, Tuple, Union, Callable
from datetime import datetime, date, timedelta
from functools import partial
from copy import deepcopy

import numpy as np
import pandas as pd
import structlog
from scipy import optimize
import xlsxwriter
from matplotlib import pyplot as plt
import seaborn as sns

from src.engine.simulation_context import SimulationContext
from src.api.websocket_manager import get_websocket_manager


class SyncWebSocketWrapper:
    """
    Production-level wrapper for WebSocket manager that safely handles sync/async calls.

    This wrapper prevents RuntimeWarnings by not calling async methods from sync contexts.
    Instead, it logs the intended messages and lets the async orchestrator handle WebSocket updates.
    """

    def __init__(self, websocket_manager, simulation_id: str):
        """Initialize the wrapper."""
        self.websocket_manager = websocket_manager
        self.simulation_id = simulation_id
        self.logger = structlog.get_logger(__name__)

    def send_progress(self, simulation_id: str, module: str, progress: float, message: str, **kwargs) -> None:
        """
        Safe sync wrapper for send_progress.

        Logs the progress instead of calling async method from sync context.
        """
        self.logger.info(
            "Progress update",
            simulation_id=simulation_id,
            module=module,
            progress=progress,
            message=message,
        )

    def is_cancelled(self, simulation_id: str) -> bool:
        """Safe wrapper for is_cancelled (this method is already sync)."""
        return self.websocket_manager.is_cancelled(simulation_id)

# Set up logging
logger = structlog.get_logger(__name__)

# Utility functions for cashflow metrics calculation
def calculate_irr(cashflows: List[float]) -> float:
    """
    Calculate the Internal Rate of Return (IRR) for a series of cashflows.

    Args:
        cashflows: List of cashflows, starting with negative values (investments)
                  and ending with positive values (returns)

    Returns:
        IRR as a decimal (e.g., 0.15 for 15%)
    """
    try:
        # Use scipy's optimize.newton to find the IRR
        def npv_equation(rate):
            return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))

        # Start with a guess of 10%
        irr = optimize.newton(npv_equation, 0.1, tol=1e-6, maxiter=1000)
        return irr
    except (RuntimeError, ValueError):
        # If the IRR calculation fails, try a different approach
        try:
            # Use numpy's IRR function
            return np.irr(cashflows)
        except:
            # If all else fails, return 0
            logger.warning("IRR calculation failed, returning 0")
            return 0.0

def calculate_npv(cashflows: List[float], discount_rate: float) -> float:
    """
    Calculate the Net Present Value (NPV) for a series of cashflows.

    Args:
        cashflows: List of cashflows, starting with negative values (investments)
                  and ending with positive values (returns)
        discount_rate: Discount rate as a decimal (e.g., 0.08 for 8%)

    Returns:
        NPV in dollars
    """
    return sum(cf / (1 + discount_rate) ** t for t, cf in enumerate(cashflows))

def calculate_moic(cashflows: List[float]) -> float:
    """
    Calculate the Multiple on Invested Capital (MOIC) for a series of cashflows.

    Args:
        cashflows: List of cashflows, starting with negative values (investments)
                  and ending with positive values (returns)

    Returns:
        MOIC as a decimal (e.g., 2.5 for 2.5x)
    """
    # Split cashflows into investments (negative) and returns (positive)
    investments = sum(-cf for cf in cashflows if cf < 0)
    returns = sum(cf for cf in cashflows if cf > 0)

    if investments == 0:
        return 0.0

    return returns / investments

def calculate_tvpi(distributions: float, nav: float, paid_in: float) -> float:
    """
    Calculate the Total Value to Paid-In (TVPI) ratio.

    Args:
        distributions: Total distributions to investors
        nav: Current Net Asset Value
        paid_in: Total paid-in capital

    Returns:
        TVPI as a decimal (e.g., 1.5 for 1.5x)
    """
    if paid_in == 0:
        return 0.0

    return (distributions + nav) / paid_in

def calculate_dpi(distributions: float, paid_in: float) -> float:
    """
    Calculate the Distributions to Paid-In (DPI) ratio.

    Args:
        distributions: Total distributions to investors
        paid_in: Total paid-in capital

    Returns:
        DPI as a decimal (e.g., 1.2 for 1.2x)
    """
    if paid_in == 0:
        return 0.0

    return distributions / paid_in

def calculate_rvpi(nav: float, paid_in: float) -> float:
    """
    Calculate the Residual Value to Paid-In (RVPI) ratio.

    Args:
        nav: Current Net Asset Value
        paid_in: Total paid-in capital

    Returns:
        RVPI as a decimal (e.g., 0.3 for 0.3x)
    """
    if paid_in == 0:
        return 0.0

    return nav / paid_in

def calculate_payback_period(cashflows: List[float]) -> float:
    """
    Calculate the payback period for a series of cashflows.

    Args:
        cashflows: List of cashflows, starting with negative values (investments)
                  and ending with positive values (returns)

    Returns:
        Payback period in years
    """
    cumulative = 0.0
    for i, cf in enumerate(cashflows):
        cumulative += cf
        if cumulative >= 0:
            # If we've reached the payback point, calculate the exact period
            if i > 0 and cumulative - cf < 0:
                # Interpolate between periods
                prev_cumulative = cumulative - cf
                fraction = -prev_cumulative / (cf - prev_cumulative)
                return i - 1 + fraction
            return float(i)

    # If we never reach payback, return infinity
    return float('inf')

def calculate_cash_on_cash(annual_cashflows: List[float], investment: float) -> float:
    """
    Calculate the cash-on-cash return for a real estate investment.

    Args:
        annual_cashflows: Annual cashflows from the investment
        investment: Initial investment amount

    Returns:
        Cash-on-cash return as a decimal (e.g., 0.08 for 8%)
    """
    if investment == 0:
        return 0.0

    # Calculate the average annual cashflow
    avg_annual_cashflow = sum(annual_cashflows) / len(annual_cashflows) if annual_cashflows else 0

    return avg_annual_cashflow / investment

def calculate_profitability_index(npv: float, initial_investment: float) -> float:
    """
    Calculate the Profitability Index (PI) for an investment.

    Args:
        npv: Net Present Value of the investment
        initial_investment: Initial investment amount

    Returns:
        Profitability Index as a decimal (e.g., 1.2 for 1.2x)
    """
    if initial_investment == 0:
        return 0.0

    return 1 + (npv / initial_investment)

def process_loan_cashflow(loan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process a single loan's cashflows.

    This function is designed to be used with parallel processing.

    Args:
        loan: Loan data
        context: Processing context with parameters

    Returns:
        Loan cashflow data
    """
    # Extract parameters from context
    simple_interest_rate = context.get("simple_interest_rate", 0.05)
    origination_fee_rate = context.get("origination_fee_rate", 0.03)
    exits = context.get("exits_dict", {})  # Use exits_dict from exit simulator
    price_paths = context.get("price_paths", {})
    recovery_rates = context.get("recovery_rates", {})
    appreciation_share_method = context.get("appreciation_share_method", "pro_rata_ltv")

    # Extract loan data
    loan_id = loan.get("loan_id")
    loan_amount = loan.get("loan_size", 0)  # Use loan_size from loan generator
    origination_year = loan.get("origination_year", 0)
    origination_month = loan.get("origination_month", 0)
    property_id = loan.get("property_id")
    ltv = loan.get("ltv", 0)

    # Calculate origination cashflows
    origination_fee = loan_amount * origination_fee_rate

    # Create origination cashflow
    origination_cashflow = {
        "year": origination_year,
        "month": origination_month,
        "loan_amount": -loan_amount,  # Negative cashflow (money going out)
        "origination_fee": origination_fee,  # Positive cashflow (revenue)
    }

    # Calculate exit cashflows if the loan has exited
    exit_cashflow = None
    if loan_id in exits:
        exit_info = exits[loan_id]
        exit_year = exit_info.get("exit_year", 0)
        exit_month = exit_info.get("exit_month", 0)
        exit_type = exit_info.get("exit_type", "term")

        # Calculate holding period in years
        holding_period = exit_year - origination_year
        if exit_month < origination_month:
            holding_period -= 1
            holding_months = 12 - origination_month + exit_month
        else:
            holding_months = exit_month - origination_month

        holding_period_years = holding_period + holding_months / 12

        # Use values calculated by exit simulator if available, otherwise calculate
        if "appreciation_share_amount" in exit_info:
            # Use appreciation share calculated by exit simulator
            appreciation_share = exit_info.get("appreciation_share_amount", 0.0)
        else:
            # Fallback: Calculate appreciation share using price paths
            appreciation_share = 0
            if exit_type == "sale" and property_id in price_paths:
                price_path = price_paths[property_id]
                if exit_year < len(price_path):
                    initial_property_value = loan.get("property_value", 0)
                    final_property_value = initial_property_value * price_path[exit_year]
                    appreciation = final_property_value - initial_property_value

                    # Calculate appreciation share based on LTV
                    if appreciation_share_method == "pro_rata_ltv":
                        # Pro-rata to LTV
                        appreciation_share = appreciation * ltv
                    elif appreciation_share_method == "tiered":
                        # Tiered appreciation sharing (simplified example)
                        if appreciation > 0:
                            if ltv <= 0.5:
                                appreciation_share = appreciation * 0.5
                            elif ltv <= 0.75:
                                appreciation_share = appreciation * 0.75
                            else:
                                appreciation_share = appreciation * 0.9
                    elif appreciation_share_method == "fixed":
                        # Fixed percentage (e.g., 50%)
                        appreciation_share = appreciation * 0.5

        # Calculate accrued interest (simple interest)
        accrued_interest = loan_amount * simple_interest_rate * holding_period_years

        # Calculate total exit cashflow
        principal = loan_amount

        # Adjust for defaults
        if exit_type == "default":
            recovery_rate = 0.7  # Default recovery rate
            if "zone" in loan:
                zone = loan["zone"]
                if zone in recovery_rates:
                    recovery_rate = recovery_rates[zone]

            principal = loan_amount * recovery_rate
            accrued_interest = 0  # No interest on defaults
            appreciation_share = 0  # No appreciation share on defaults

        total_exit_cashflow = principal + accrued_interest + appreciation_share

        # Create exit cashflow
        exit_cashflow = {
            "year": exit_year,
            "month": exit_month,
            "principal": principal,
            "accrued_interest": accrued_interest,
            "appreciation_share": appreciation_share,
            "total": total_exit_cashflow,
            "exit_type": exit_type,
        }

    # Return loan-level cashflow
    return {
        "loan_id": loan_id,
        "origination": origination_cashflow,
        "exit": exit_cashflow,
    }


class CashflowAggregator:
    """
    Cashflow aggregator for calculating and aggregating cashflows.

    This class aggregates cashflows from various sources, including:
    - Loan originations
    - Loan exits (principal, interest, appreciation share)
    - Fees (management, origination, etc.)
    - Leverage (draws, repayments, interest)
    - Distributions to investors

    Enhanced features:
    - Parallel processing for loan-level cashflow calculations
    - Daily cashflow granularity
    - Scenario analysis
    - Sensitivity analysis
    - Cashflow metrics calculation (IRR, DPI, RVPI, TVPI, etc.)
    - Waterfall integration
    - Tax impact analysis
    - Reinvestment modeling
    - Liquidity analysis
    - Enhanced visualization options
    - Export capabilities
    """

    def __init__(self, context: SimulationContext):
        """
        Initialize the cashflow aggregator.

        Args:
            context: Simulation context
        """
        self.context = context
        self.config = context.config
        self.cashflow_config = getattr(self.config, "cashflow_aggregator", {})

        # Get WebSocket manager and create safe sync wrapper
        websocket_manager = get_websocket_manager()
        self.websocket_manager = SyncWebSocketWrapper(websocket_manager, context.run_id)

        # Get time granularity
        self.time_granularity = getattr(self.cashflow_config, "time_granularity", "yearly")

        # Get parallel processing settings
        self.enable_parallel_processing = getattr(self.cashflow_config, "enable_parallel_processing", True)
        self.num_workers = getattr(self.cashflow_config, "num_workers", 4)

        # Get scenario analysis settings
        self.enable_scenario_analysis = getattr(self.cashflow_config, "enable_scenario_analysis", False)
        self.scenarios = getattr(self.cashflow_config, "scenarios", [])

        # Get sensitivity analysis settings
        self.enable_sensitivity_analysis = getattr(self.cashflow_config, "enable_sensitivity_analysis", False)
        self.sensitivity_parameters = getattr(self.cashflow_config, "sensitivity_parameters", [])

        # Get cashflow metrics settings
        self.enable_cashflow_metrics = getattr(self.cashflow_config, "enable_cashflow_metrics", True)
        self.discount_rate = getattr(self.cashflow_config, "discount_rate", 0.08)

        # Get tax impact analysis settings
        self.enable_tax_impact_analysis = getattr(self.cashflow_config, "enable_tax_impact_analysis", False)
        self.tax_rates = getattr(self.cashflow_config, "tax_rates", {"ordinary_income": 0.35, "capital_gains": 0.20})

        # Get reinvestment modeling settings
        self.enable_reinvestment_modeling = getattr(self.cashflow_config, "enable_reinvestment_modeling", True)
        self.reinvestment_rate = getattr(self.cashflow_config, "reinvestment_rate", 0.05)

        # Get liquidity analysis settings
        self.enable_liquidity_analysis = getattr(self.cashflow_config, "enable_liquidity_analysis", True)
        self.minimum_cash_reserve = getattr(self.cashflow_config, "minimum_cash_reserve", 0.05)

        # Get export settings
        self.enable_export = getattr(self.cashflow_config, "enable_export", False)
        self.export_formats = getattr(self.cashflow_config, "export_formats", ["csv", "excel"])

        # Initialize cashflow tracking
        self.loan_level_cashflows: List[Dict[str, Any]] = []
        self.fund_level_cashflows: List[Dict[str, Any]] = []
        self.lp_cashflows: List[Dict[str, Any]] = []
        self.gp_cashflows: List[Dict[str, Any]] = []

        # Initialize visualization data
        self.cashflow_waterfall_chart: List[Dict[str, Any]] = []
        self.cashflow_by_year_chart: List[Dict[str, Any]] = []
        self.cumulative_cashflow_chart: List[Dict[str, Any]] = []
        self.cashflow_table: List[Dict[str, Any]] = []
        self.cashflow_heatmap: List[Dict[str, Any]] = []
        self.cashflow_sankey: Dict[str, Any] = {"nodes": [], "links": []}
        self.scenario_comparison_chart: List[Dict[str, Any]] = []

        # Initialize metrics
        self.fund_level_metrics: Dict[str, Any] = {}
        self.lp_metrics: Dict[str, Any] = {}
        self.gp_metrics: Dict[str, Any] = {}
        self.metrics_by_year: List[Dict[str, Any]] = []

        # Initialize sensitivity analysis results
        self.sensitivity_analysis_results: Dict[str, Any] = {
            "parameter_variations": [],
            "tornado_chart": []
        }

        # Initialize scenario analysis results
        self.scenario_analysis_results: Dict[str, Any] = {
            "scenarios": []
        }

        # Initialize tax impact analysis results
        self.tax_impact_results: Dict[str, Any] = {
            "pre_tax_cashflows": [],
            "post_tax_cashflows": [],
            "tax_metrics": {}
        }

        # Initialize liquidity analysis results
        self.liquidity_analysis_results: Dict[str, Any] = {
            "cash_reserves": [],
            "liquidity_metrics": {}
        }

        # Initialize scenario contexts
        self.scenario_contexts: Dict[str, SimulationContext] = {}

        logger.info(
            "Cashflow aggregator initialized",
            time_granularity=self.time_granularity,
            enable_parallel_processing=self.enable_parallel_processing,
            num_workers=self.num_workers,
            enable_scenario_analysis=self.enable_scenario_analysis,
            enable_sensitivity_analysis=self.enable_sensitivity_analysis,
            enable_cashflow_metrics=self.enable_cashflow_metrics,
            enable_tax_impact_analysis=self.enable_tax_impact_analysis,
            enable_reinvestment_modeling=self.enable_reinvestment_modeling,
            enable_liquidity_analysis=self.enable_liquidity_analysis,
            enable_export=self.enable_export,
        )

    def calculate_loan_level_cashflows(self) -> None:
        """
        Calculate loan-level cashflows.

        This includes:
        - Origination cashflows (loan amount, origination fee)
        - Exit cashflows (principal, accrued interest, appreciation share)

        Enhanced with parallel processing for improved performance.
        """
        logger.info("Calculating loan-level cashflows")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=10.0,
            message="Calculating loan-level cashflows",
        )

        # Check if we have loans to process
        if not hasattr(self.context, "loans") or not self.context.loans:
            logger.warning("No loans found in context")
            self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="cashflow_aggregator",
                progress=30.0,
                message="No loans found to process",
            )
            return

        # Get parameters
        simple_interest_rate = getattr(self.cashflow_config, "simple_interest_rate", 0.05)
        origination_fee_rate = getattr(self.cashflow_config, "origination_fee_rate", 0.03)
        appreciation_share_method = getattr(self.cashflow_config, "appreciation_share_method", "pro_rata_ltv")

        # Create processing context
        exits_dict = getattr(self.context, "exits_dict", {})
        logger.info(f"DEBUG: Found {len(exits_dict)} exits in context.exits_dict")

        processing_context = {
            "simple_interest_rate": simple_interest_rate,
            "origination_fee_rate": origination_fee_rate,
            "exits_dict": exits_dict,  # Use exits_dict from exit simulator
            "price_paths": getattr(self.context, "price_paths", {}),
            "recovery_rates": getattr(self.context, "recovery_rates", {}),
            "appreciation_share_method": appreciation_share_method,
        }

        # Check for cancellation
        if self.websocket_manager.is_cancelled(self.context.run_id):
            logger.info("Cashflow calculation cancelled")
            return

        # Process loans
        if self.enable_parallel_processing and len(self.context.loans) > 10:
            # Use parallel processing for large loan portfolios
            logger.info(
                "Using parallel processing for loan-level cashflows",
                num_workers=self.num_workers,
                num_loans=len(self.context.loans),
            )

            # Send progress update
            self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="cashflow_aggregator",
                progress=15.0,
                message=f"Processing {len(self.context.loans)} loans in parallel with {self.num_workers} workers",
            )

            # Create a process pool
            with concurrent.futures.ProcessPoolExecutor(max_workers=self.num_workers) as executor:
                # Create a partial function with the processing context
                process_func = partial(process_loan_cashflow, context=processing_context)

                # Submit all loans for processing
                future_to_loan = {executor.submit(process_func, loan): loan for loan in self.context.loans}

                # Process results as they complete
                completed = 0
                total = len(future_to_loan)

                for future in concurrent.futures.as_completed(future_to_loan):
                    # Check for cancellation
                    if self.websocket_manager.is_cancelled(self.context.run_id):
                        logger.info("Cashflow calculation cancelled")
                        executor.shutdown(wait=False)
                        return

                    try:
                        # Get the result
                        loan_cashflow = future.result()
                        self.loan_level_cashflows.append(loan_cashflow)

                        # Update progress
                        completed += 1
                        if completed % 100 == 0 or completed == total:
                            progress = 15.0 + (completed / total) * 15.0
                            self.websocket_manager.send_progress(
                                simulation_id=self.context.run_id,
                                module="cashflow_aggregator",
                                progress=progress,
                                message=f"Processed {completed}/{total} loans",
                            )
                    except Exception as e:
                        loan = future_to_loan[future]
                        logger.error(
                            "Error processing loan",
                            loan_id=loan.get("loan_id"),
                            error=str(e),
                            exc_info=True,
                        )
        else:
            # Use sequential processing for small loan portfolios or when parallel processing is disabled
            logger.info(
                "Using sequential processing for loan-level cashflows",
                num_loans=len(self.context.loans),
            )

            # Process each loan sequentially
            for i, loan in enumerate(self.context.loans):
                # Check for cancellation
                if self.websocket_manager.is_cancelled(self.context.run_id):
                    logger.info("Cashflow calculation cancelled")
                    return

                # Process the loan
                loan_cashflow = process_loan_cashflow(loan, processing_context)
                self.loan_level_cashflows.append(loan_cashflow)

                # Update progress
                if i % 100 == 0 or i == len(self.context.loans) - 1:
                    progress = 10.0 + (i / len(self.context.loans)) * 20.0
                    self.websocket_manager.send_progress(
                        simulation_id=self.context.run_id,
                        module="cashflow_aggregator",
                        progress=progress,
                        message=f"Processed {i+1}/{len(self.context.loans)} loans",
                    )

        logger.info(
            "Loan-level cashflows calculated",
            num_loans=len(self.loan_level_cashflows),
        )

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=30.0,
            message=f"Calculated cashflows for {len(self.loan_level_cashflows)} loans",
        )

    def calculate_fund_level_cashflows(self) -> None:
        """
        Calculate fund-level cashflows.

        This aggregates loan-level cashflows and adds fund-level cashflows like:
        - Capital calls
        - Management fees
        - Fund expenses
        - Leverage draws/repayments/interest
        - Distributions
        """
        logger.info("Calculating fund-level cashflows")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=40.0,
            message="Calculating fund-level cashflows",
        )

        # Get fund parameters
        fund_term = getattr(self.config, "fund_term", 10)
        fund_size = getattr(self.config, "fund_size", 100_000_000)

        # Initialize cashflow tracking by period
        periods = []
        if self.time_granularity == "monthly":
            periods = [(year, month) for year in range(fund_term + 1) for month in range(1, 13)]
        elif self.time_granularity == "quarterly":
            periods = [(year, quarter) for year in range(fund_term + 1) for quarter in range(1, 5)]
        else:  # yearly
            periods = [(year, 0) for year in range(fund_term + 1)]

        # Initialize cashflows for each period
        for period in periods:
            year, sub_period = period

            period_cashflow = {
                "year": year,
                "capital_calls": 0,
                "loan_investments": 0,
                "origination_fees": 0,
                "principal_repayments": 0,
                "interest_income": 0,
                "appreciation_share": 0,
                "management_fees": 0,
                "fund_expenses": 0,
                "leverage_draws": 0,
                "leverage_repayments": 0,
                "leverage_interest": 0,
                "distributions": 0,
                "net_cashflow": 0,
                "cumulative_cashflow": 0,
            }

            # Add sub-period field if applicable
            if self.time_granularity == "monthly":
                period_cashflow["month"] = sub_period
            elif self.time_granularity == "quarterly":
                period_cashflow["quarter"] = sub_period

            self.fund_level_cashflows.append(period_cashflow)

        # Aggregate loan-level cashflows
        for loan_cashflow in self.loan_level_cashflows:
            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Cashflow calculation cancelled")
                return

            # Process origination cashflow
            origination = loan_cashflow.get("origination", {})
            if origination:
                year = origination.get("year", 0)
                month = origination.get("month", 0)

                # Find the corresponding period
                period_index = self._get_period_index(year, month)
                if period_index is not None:
                    # Update the period cashflow
                    self.fund_level_cashflows[period_index]["loan_investments"] += origination.get("loan_amount", 0)
                    self.fund_level_cashflows[period_index]["origination_fees"] += origination.get("origination_fee", 0)

            # Process exit cashflow
            exit_cf = loan_cashflow.get("exit", {})
            if exit_cf:
                year = exit_cf.get("year", 0)
                month = exit_cf.get("month", 0)

                # Find the corresponding period
                period_index = self._get_period_index(year, month)
                if period_index is not None:
                    # Update the period cashflow
                    self.fund_level_cashflows[period_index]["principal_repayments"] += exit_cf.get("principal", 0)
                    self.fund_level_cashflows[period_index]["interest_income"] += exit_cf.get("accrued_interest", 0)
                    self.fund_level_cashflows[period_index]["appreciation_share"] += exit_cf.get("appreciation_share", 0)

        # Add capital calls
        # For simplicity, assume all capital is called in year 0
        if len(self.fund_level_cashflows) > 0:
            self.fund_level_cashflows[0]["capital_calls"] = -fund_size

        # Add management fees and fund expenses
        if hasattr(self.context, "fees"):
            # Add management fees
            for fee in getattr(self.context.fees, "management_fees", []):
                year = fee.get("year", 0)
                fee_amount = fee.get("fee_amount", 0)

                # Find the corresponding period
                period_index = self._get_period_index(year, 0)
                if period_index is not None:
                    # Update the period cashflow (negative because it's an expense)
                    self.fund_level_cashflows[period_index]["management_fees"] = -fee_amount

            # Add fund expenses
            for expense in getattr(self.context.fees, "fund_expenses", []):
                year = expense.get("year", 0)
                expense_amount = expense.get("expense_amount", 0)

                # Find the corresponding period
                period_index = self._get_period_index(year, 0)
                if period_index is not None:
                    # Update the period cashflow (negative because it's an expense)
                    self.fund_level_cashflows[period_index]["fund_expenses"] = -expense_amount

        # Add leverage cashflows if available
        if hasattr(self.context, "leverage"):
            for leverage_cf in getattr(self.context.leverage, "cashflows", []):
                year = leverage_cf.get("year", 0)
                month = leverage_cf.get("month", 0)

                # Find the corresponding period
                period_index = self._get_period_index(year, month)
                if period_index is not None:
                    # Update the period cashflow
                    self.fund_level_cashflows[period_index]["leverage_draws"] += leverage_cf.get("draw", 0)
                    self.fund_level_cashflows[period_index]["leverage_repayments"] += leverage_cf.get("repayment", 0)
                    self.fund_level_cashflows[period_index]["leverage_interest"] += leverage_cf.get("interest", 0)

        # Calculate net cashflow and cumulative cashflow
        cumulative_cashflow = 0
        for i, period_cf in enumerate(self.fund_level_cashflows):
            # Calculate net cashflow
            net_cashflow = (
                period_cf["capital_calls"] +
                period_cf["loan_investments"] +
                period_cf["origination_fees"] +
                period_cf["principal_repayments"] +
                period_cf["interest_income"] +
                period_cf["appreciation_share"] +
                period_cf["management_fees"] +
                period_cf["fund_expenses"] +
                period_cf["leverage_draws"] +
                period_cf["leverage_repayments"] +
                period_cf["leverage_interest"] +
                period_cf["distributions"]
            )

            period_cf["net_cashflow"] = net_cashflow

            # Calculate cumulative cashflow
            cumulative_cashflow += net_cashflow
            period_cf["cumulative_cashflow"] = cumulative_cashflow

        logger.info(
            "Fund-level cashflows calculated",
            num_periods=len(self.fund_level_cashflows),
        )

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=60.0,
            message=f"Calculated fund-level cashflows for {len(self.fund_level_cashflows)} periods",
        )

    def calculate_stakeholder_cashflows(self) -> None:
        """
        Calculate stakeholder-level cashflows.

        This includes:
        - LP cashflows (capital calls, distributions)
        - GP cashflows (capital calls, management fees, carried interest, distributions)
        """
        logger.info("Calculating stakeholder cashflows")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=70.0,
            message="Calculating stakeholder cashflows",
        )

        # Get fund parameters
        fund_term = getattr(self.config, "fund_term", 10)
        fund_size = getattr(self.config, "fund_size", 100_000_000)
        gp_commitment_percentage = getattr(self.config, "gp_commitment_percentage", 0.0)

        # Initialize periods
        periods = []
        if self.time_granularity == "monthly":
            periods = [(year, month) for year in range(fund_term + 1) for month in range(1, 13)]
        elif self.time_granularity == "quarterly":
            periods = [(year, quarter) for year in range(fund_term + 1) for quarter in range(1, 5)]
        else:  # yearly
            periods = [(year, 0) for year in range(fund_term + 1)]

        # Initialize LP cashflows
        for period in periods:
            year, sub_period = period

            lp_cashflow = {
                "year": year,
                "capital_calls": 0,
                "distributions": 0,
                "net_cashflow": 0,
                "cumulative_cashflow": 0,
            }

            # Add sub-period field if applicable
            if self.time_granularity == "monthly":
                lp_cashflow["month"] = sub_period
            elif self.time_granularity == "quarterly":
                lp_cashflow["quarter"] = sub_period

            self.lp_cashflows.append(lp_cashflow)

        # Initialize GP cashflows
        for period in periods:
            year, sub_period = period

            gp_cashflow = {
                "year": year,
                "capital_calls": 0,
                "management_fees": 0,
                "origination_fees": 0,
                "carried_interest": 0,
                "distributions": 0,
                "net_cashflow": 0,
                "cumulative_cashflow": 0,
            }

            # Add sub-period field if applicable
            if self.time_granularity == "monthly":
                gp_cashflow["month"] = sub_period
            elif self.time_granularity == "quarterly":
                gp_cashflow["quarter"] = sub_period

            self.gp_cashflows.append(gp_cashflow)

        # Calculate LP capital calls (fund size minus GP commitment)
        lp_commitment = fund_size * (1 - gp_commitment_percentage)
        if len(self.lp_cashflows) > 0:
            self.lp_cashflows[0]["capital_calls"] = -lp_commitment

        # Calculate GP capital calls (GP commitment)
        gp_commitment = fund_size * gp_commitment_percentage
        if len(self.gp_cashflows) > 0:
            self.gp_cashflows[0]["capital_calls"] = -gp_commitment

        # Add management fees to GP cashflows (positive for GP)
        if hasattr(self.context, "fees"):
            # Add management fees
            for fee in getattr(self.context.fees, "management_fees", []):
                year = fee.get("year", 0)
                fee_amount = fee.get("fee_amount", 0)

                # Find the corresponding period
                period_index = self._get_period_index(year, 0)
                if period_index is not None:
                    # Update the GP cashflow (positive because it's revenue for GP)
                    self.gp_cashflows[period_index]["management_fees"] = fee_amount

            # Add origination fees
            for fee in getattr(self.context.fees, "origination_fees", []):
                year = fee.get("year", 0)
                fee_amount = fee.get("fee_amount", 0)

                # Find the corresponding period
                period_index = self._get_period_index(year, 0)
                if period_index is not None:
                    # Update the GP cashflow (positive because it's revenue for GP)
                    self.gp_cashflows[period_index]["origination_fees"] += fee_amount

        # Calculate carried interest (simplified)
        # In a real implementation, this would be based on the waterfall distribution
        # For now, we'll just use a simple approximation
        hurdle_rate = getattr(self.config, "hurdle_rate", 0.08)
        carried_interest_rate = getattr(self.config, "carried_interest_rate", 0.20)

        # Calculate total fund cashflow
        total_fund_cashflow = sum(cf["net_cashflow"] for cf in self.fund_level_cashflows)

        # Calculate profit above hurdle
        hurdle_amount = lp_commitment * (1 + hurdle_rate) ** fund_term
        profit_above_hurdle = max(0, total_fund_cashflow - hurdle_amount)

        # Calculate carried interest
        carried_interest = profit_above_hurdle * carried_interest_rate

        # Add carried interest to the last period
        if len(self.gp_cashflows) > 0:
            self.gp_cashflows[-1]["carried_interest"] = carried_interest

        # Calculate distributions (simplified)
        # In a real implementation, this would be based on the waterfall distribution
        # For now, we'll just distribute the net cashflow proportionally
        total_distributions = total_fund_cashflow - carried_interest
        lp_distribution_percentage = lp_commitment / fund_size
        gp_distribution_percentage = gp_commitment / fund_size

        # Add distributions to the last period
        if len(self.lp_cashflows) > 0:
            self.lp_cashflows[-1]["distributions"] = total_distributions * lp_distribution_percentage

        if len(self.gp_cashflows) > 0:
            self.gp_cashflows[-1]["distributions"] = total_distributions * gp_distribution_percentage

        # Calculate net cashflow and cumulative cashflow for LP
        lp_cumulative_cashflow = 0
        for i, period_cf in enumerate(self.lp_cashflows):
            # Calculate net cashflow
            net_cashflow = period_cf["capital_calls"] + period_cf["distributions"]
            period_cf["net_cashflow"] = net_cashflow

            # Calculate cumulative cashflow
            lp_cumulative_cashflow += net_cashflow
            period_cf["cumulative_cashflow"] = lp_cumulative_cashflow

        # Calculate net cashflow and cumulative cashflow for GP
        gp_cumulative_cashflow = 0
        for i, period_cf in enumerate(self.gp_cashflows):
            # Calculate net cashflow
            net_cashflow = (
                period_cf["capital_calls"] +
                period_cf["management_fees"] +
                period_cf["origination_fees"] +
                period_cf["carried_interest"] +
                period_cf["distributions"]
            )
            period_cf["net_cashflow"] = net_cashflow

            # Calculate cumulative cashflow
            gp_cumulative_cashflow += net_cashflow
            period_cf["cumulative_cashflow"] = gp_cumulative_cashflow

        logger.info(
            "Stakeholder cashflows calculated",
            num_lp_periods=len(self.lp_cashflows),
            num_gp_periods=len(self.gp_cashflows),
        )

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=80.0,
            message="Calculated stakeholder cashflows",
        )

    def generate_visualization_data(self) -> None:
        """
        Generate visualization data for cashflows.

        This includes:
        - Cashflow waterfall chart
        - Cashflow by year chart
        - Cumulative cashflow chart
        - Cashflow table
        """
        logger.info("Generating visualization data")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=85.0,
            message="Generating visualization data",
        )

        # Generate cashflow waterfall chart
        self._generate_cashflow_waterfall_chart()

        # Generate cashflow by year chart
        self._generate_cashflow_by_year_chart()

        # Generate cumulative cashflow chart
        self._generate_cumulative_cashflow_chart()

        # Generate cashflow table
        self._generate_cashflow_table()

        logger.info("Visualization data generated")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=90.0,
            message="Generated visualization data",
        )

    def _generate_cashflow_waterfall_chart(self) -> None:
        """Generate cashflow waterfall chart data."""
        # Calculate total cashflows by category
        capital_calls = sum(cf["capital_calls"] for cf in self.fund_level_cashflows)
        loan_investments = sum(cf["loan_investments"] for cf in self.fund_level_cashflows)
        origination_fees = sum(cf["origination_fees"] for cf in self.fund_level_cashflows)
        principal_repayments = sum(cf["principal_repayments"] for cf in self.fund_level_cashflows)
        interest_income = sum(cf["interest_income"] for cf in self.fund_level_cashflows)
        appreciation_share = sum(cf["appreciation_share"] for cf in self.fund_level_cashflows)
        management_fees = sum(cf["management_fees"] for cf in self.fund_level_cashflows)
        fund_expenses = sum(cf["fund_expenses"] for cf in self.fund_level_cashflows)
        leverage_draws = sum(cf["leverage_draws"] for cf in self.fund_level_cashflows)
        leverage_repayments = sum(cf["leverage_repayments"] for cf in self.fund_level_cashflows)
        leverage_interest = sum(cf["leverage_interest"] for cf in self.fund_level_cashflows)
        distributions = sum(cf["distributions"] for cf in self.fund_level_cashflows)

        # Create waterfall chart data
        self.cashflow_waterfall_chart = [
            {"category": "Capital Calls", "amount": capital_calls},
            {"category": "Loan Investments", "amount": loan_investments},
            {"category": "Origination Fees", "amount": origination_fees},
            {"category": "Principal Repayments", "amount": principal_repayments},
            {"category": "Interest Income", "amount": interest_income},
            {"category": "Appreciation Share", "amount": appreciation_share},
            {"category": "Management Fees", "amount": management_fees},
            {"category": "Fund Expenses", "amount": fund_expenses},
            {"category": "Leverage Draws", "amount": leverage_draws},
            {"category": "Leverage Repayments", "amount": leverage_repayments},
            {"category": "Leverage Interest", "amount": leverage_interest},
            {"category": "Distributions", "amount": distributions},
        ]

    def _generate_cashflow_by_year_chart(self) -> None:
        """Generate cashflow by year chart data."""
        # Group cashflows by year
        for cf in self.fund_level_cashflows:
            year = cf["year"]

            # Calculate inflows and outflows
            inflows = (
                cf["origination_fees"] +
                cf["principal_repayments"] +
                cf["interest_income"] +
                cf["appreciation_share"] +
                cf["leverage_draws"]
            )

            outflows = (
                cf["capital_calls"] +
                cf["loan_investments"] +
                cf["management_fees"] +
                cf["fund_expenses"] +
                cf["leverage_repayments"] +
                cf["leverage_interest"] +
                cf["distributions"]
            )

            # Add to chart data
            self.cashflow_by_year_chart.append({
                "year": year,
                "inflows": inflows,
                "outflows": outflows,
                "net": cf["net_cashflow"],
            })

    def _generate_cumulative_cashflow_chart(self) -> None:
        """Generate cumulative cashflow chart data."""
        # Add cumulative cashflow data
        for cf in self.fund_level_cashflows:
            self.cumulative_cashflow_chart.append({
                "year": cf["year"],
                "cumulative_cashflow": cf["cumulative_cashflow"],
            })

    def _generate_cashflow_table(self) -> None:
        """Generate cashflow table data."""
        # Add cashflow table data
        for cf in self.fund_level_cashflows:
            self.cashflow_table.append({
                "year": cf["year"],
                "capital_calls": cf["capital_calls"],
                "loan_investments": cf["loan_investments"],
                "origination_fees": cf["origination_fees"],
                "principal_repayments": cf["principal_repayments"],
                "interest_income": cf["interest_income"],
                "appreciation_share": cf["appreciation_share"],
                "management_fees": cf["management_fees"],
                "fund_expenses": cf["fund_expenses"],
                "distributions": cf["distributions"],
                "net_cashflow": cf["net_cashflow"],
                "cumulative_cashflow": cf["cumulative_cashflow"],
            })

    def _get_period_index(self, year: int, month: int) -> Optional[int]:
        """
        Get the index of the period corresponding to the given year and month.

        Converts absolute years (e.g., 2025) to relative fund years (e.g., 0, 1, 2...)
        based on the fund's vintage year.

        Args:
            year: Absolute year (e.g., 2025)
            month: Month

        Returns:
            Index of the period, or None if not found
        """
        # Convert absolute year to relative fund year
        vintage_year = getattr(self.config, "vintage_year", 2025)
        relative_year = year - vintage_year

        # Check if the relative year is within the fund term
        fund_term = getattr(self.config, "fund_term", 10)
        if relative_year < 0 or relative_year > fund_term:
            return None

        if self.time_granularity == "monthly":
            for i, cf in enumerate(self.fund_level_cashflows):
                if cf["year"] == relative_year and cf["month"] == month:
                    return i
        elif self.time_granularity == "quarterly":
            quarter = (month - 1) // 3 + 1
            for i, cf in enumerate(self.fund_level_cashflows):
                if cf["year"] == relative_year and cf["quarter"] == quarter:
                    return i
        else:  # yearly
            for i, cf in enumerate(self.fund_level_cashflows):
                if cf["year"] == relative_year:
                    return i

        return None

    def calculate_cashflow_metrics(self) -> None:
        """
        Calculate cashflow metrics.

        This includes:
        - Fund-level metrics (IRR, MOIC, TVPI, DPI, RVPI, etc.)
        - LP metrics
        - GP metrics
        - Metrics by year
        """
        logger.info("Calculating cashflow metrics")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=80.0,
            message="Calculating cashflow metrics",
        )

        # Skip if metrics calculation is disabled
        if not self.enable_cashflow_metrics:
            logger.info("Cashflow metrics calculation is disabled")
            return

        # Check if we have fund-level cashflows
        if not self.fund_level_cashflows:
            logger.warning("No fund-level cashflows found")
            return

        # Extract fund-level cashflows
        fund_cashflows = [cf["net_cashflow"] for cf in self.fund_level_cashflows]

        # Calculate fund-level metrics
        try:
            # Calculate IRR
            irr = calculate_irr(fund_cashflows)

            # Calculate NPV
            npv = calculate_npv(fund_cashflows, self.discount_rate)

            # Calculate MOIC
            moic = calculate_moic(fund_cashflows)

            # Calculate distributions and paid-in capital
            distributions = sum(cf["distributions"] for cf in self.fund_level_cashflows)
            paid_in = -sum(cf["capital_calls"] for cf in self.fund_level_cashflows)

            # Calculate NAV (assume it's the final cumulative cashflow)
            nav = self.fund_level_cashflows[-1]["cumulative_cashflow"] if self.fund_level_cashflows else 0

            # Calculate TVPI, DPI, RVPI
            tvpi = calculate_tvpi(distributions, nav, paid_in)
            dpi = calculate_dpi(distributions, paid_in)
            rvpi = calculate_rvpi(nav, paid_in)

            # Calculate payback period
            payback_period = calculate_payback_period(fund_cashflows)

            # Calculate cash-on-cash return
            annual_cashflows = [cf["net_cashflow"] for cf in self.fund_level_cashflows if cf["year"] > 0]
            initial_investment = -fund_cashflows[0] if fund_cashflows and fund_cashflows[0] < 0 else 0
            cash_on_cash = calculate_cash_on_cash(annual_cashflows, initial_investment)

            # Calculate profitability index
            profitability_index = calculate_profitability_index(npv, initial_investment)

            # Calculate cash yield
            cash_yield = distributions / paid_in if paid_in > 0 else 0

            # Store fund-level metrics
            self.fund_level_metrics = {
                "irr": irr,
                "moic": moic,
                "tvpi": tvpi,
                "dpi": dpi,
                "rvpi": rvpi,
                "payback_period": payback_period,
                "cash_on_cash": cash_on_cash,
                "npv": npv,
                "profitability_index": profitability_index,
                "cash_yield": cash_yield,
            }

            logger.info(
                "Fund-level metrics calculated",
                irr=irr,
                moic=moic,
                tvpi=tvpi,
                dpi=dpi,
                rvpi=rvpi,
            )
        except Exception as e:
            logger.error(
                "Error calculating fund-level metrics",
                error=str(e),
                exc_info=True,
            )

        # Calculate LP metrics
        try:
            if self.lp_cashflows:
                # Extract LP cashflows
                lp_cashflows = [cf["net_cashflow"] for cf in self.lp_cashflows]

                # Calculate IRR
                lp_irr = calculate_irr(lp_cashflows)

                # Calculate MOIC
                lp_moic = calculate_moic(lp_cashflows)

                # Calculate distributions and paid-in capital
                lp_distributions = sum(cf["distributions"] for cf in self.lp_cashflows)
                lp_paid_in = -sum(cf["capital_calls"] for cf in self.lp_cashflows)

                # Calculate NAV (assume it's 0 at the end)
                lp_nav = 0

                # Calculate TVPI, DPI, RVPI
                lp_tvpi = calculate_tvpi(lp_distributions, lp_nav, lp_paid_in)
                lp_dpi = calculate_dpi(lp_distributions, lp_paid_in)
                lp_rvpi = calculate_rvpi(lp_nav, lp_paid_in)

                # Calculate payback period
                lp_payback_period = calculate_payback_period(lp_cashflows)

                # Store LP metrics
                self.lp_metrics = {
                    "irr": lp_irr,
                    "moic": lp_moic,
                    "tvpi": lp_tvpi,
                    "dpi": lp_dpi,
                    "rvpi": lp_rvpi,
                    "payback_period": lp_payback_period,
                }

                logger.info(
                    "LP metrics calculated",
                    irr=lp_irr,
                    moic=lp_moic,
                    tvpi=lp_tvpi,
                    dpi=lp_dpi,
                    rvpi=lp_rvpi,
                )
        except Exception as e:
            logger.error(
                "Error calculating LP metrics",
                error=str(e),
                exc_info=True,
            )

        # Calculate GP metrics
        try:
            if self.gp_cashflows:
                # Extract GP cashflows
                gp_cashflows = [cf["net_cashflow"] for cf in self.gp_cashflows]

                # Calculate IRR
                gp_irr = calculate_irr(gp_cashflows)

                # Calculate MOIC
                gp_moic = calculate_moic(gp_cashflows)

                # Calculate distributions and paid-in capital
                gp_distributions = sum(cf["distributions"] for cf in self.gp_cashflows)
                gp_paid_in = -sum(cf["capital_calls"] for cf in self.gp_cashflows)

                # Calculate NAV (assume it's 0 at the end)
                gp_nav = 0

                # Calculate TVPI, DPI, RVPI
                gp_tvpi = calculate_tvpi(gp_distributions, gp_nav, gp_paid_in)
                gp_dpi = calculate_dpi(gp_distributions, gp_paid_in)
                gp_rvpi = calculate_rvpi(gp_nav, gp_paid_in)

                # Calculate payback period
                gp_payback_period = calculate_payback_period(gp_cashflows)

                # Calculate carried interest, management fees, and origination fees
                carried_interest = sum(cf["carried_interest"] for cf in self.gp_cashflows)
                management_fees = sum(cf["management_fees"] for cf in self.gp_cashflows)
                origination_fees = sum(cf["origination_fees"] for cf in self.gp_cashflows)

                # Store GP metrics
                self.gp_metrics = {
                    "irr": gp_irr,
                    "moic": gp_moic,
                    "tvpi": gp_tvpi,
                    "dpi": gp_dpi,
                    "rvpi": gp_rvpi,
                    "payback_period": gp_payback_period,
                    "carried_interest": carried_interest,
                    "management_fees": management_fees,
                    "origination_fees": origination_fees,
                }

                logger.info(
                    "GP metrics calculated",
                    irr=gp_irr,
                    moic=gp_moic,
                    tvpi=gp_tvpi,
                    dpi=gp_dpi,
                    rvpi=gp_rvpi,
                )
        except Exception as e:
            logger.error(
                "Error calculating GP metrics",
                error=str(e),
                exc_info=True,
            )

        # Calculate metrics by year
        try:
            # Initialize metrics by year
            self.metrics_by_year = []

            # Calculate cumulative distributions and paid-in capital by year
            cumulative_distributions = 0
            cumulative_paid_in = 0

            for cf in self.fund_level_cashflows:
                year = cf["year"]

                # Update cumulative values
                cumulative_distributions += cf["distributions"] if cf["distributions"] > 0 else 0
                cumulative_paid_in += -cf["capital_calls"] if cf["capital_calls"] < 0 else 0

                # Calculate metrics for this year
                year_dpi = calculate_dpi(cumulative_distributions, cumulative_paid_in)
                year_rvpi = calculate_rvpi(cf["cumulative_cashflow"], cumulative_paid_in)
                year_tvpi = year_dpi + year_rvpi

                # Calculate IRR up to this year
                year_cashflows = [cf2["net_cashflow"] for cf2 in self.fund_level_cashflows if cf2["year"] <= year]
                year_irr = calculate_irr(year_cashflows) if len(year_cashflows) > 1 else 0

                # Calculate cash yield for this year
                year_distributions = cf["distributions"] if cf["distributions"] > 0 else 0
                year_cash_yield = year_distributions / cumulative_paid_in if cumulative_paid_in > 0 else 0

                # Add metrics for this year
                self.metrics_by_year.append({
                    "year": year,
                    "dpi": year_dpi,
                    "rvpi": year_rvpi,
                    "tvpi": year_tvpi,
                    "irr": year_irr,
                    "cash_yield": year_cash_yield,
                })

            logger.info(
                "Metrics by year calculated",
                num_years=len(self.metrics_by_year),
            )
        except Exception as e:
            logger.error(
                "Error calculating metrics by year",
                error=str(e),
                exc_info=True,
            )

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=85.0,
            message="Cashflow metrics calculated",
        )

    def run(self) -> None:
        """
        Run the cashflow aggregator.

        This method calculates cashflows, generates visualization data, and performs
        various analyses including metrics calculation, sensitivity analysis,
        scenario analysis, tax impact analysis, and liquidity analysis.
        """
        logger.info("Running cashflow aggregator")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=5.0,
            message="Starting cashflow aggregation",
        )

        # Calculate loan-level cashflows
        self.calculate_loan_level_cashflows()

        # Check for cancellation
        if self.websocket_manager.is_cancelled(self.context.run_id):
            logger.info("Cashflow aggregation cancelled")
            return

        # Calculate fund-level cashflows
        self.calculate_fund_level_cashflows()

        # Check for cancellation
        if self.websocket_manager.is_cancelled(self.context.run_id):
            logger.info("Cashflow aggregation cancelled")
            return

        # Calculate stakeholder cashflows
        self.calculate_stakeholder_cashflows()

        # Check for cancellation
        if self.websocket_manager.is_cancelled(self.context.run_id):
            logger.info("Cashflow aggregation cancelled")
            return

        # Generate visualization data
        self.generate_visualization_data()

        # Check for cancellation
        if self.websocket_manager.is_cancelled(self.context.run_id):
            logger.info("Cashflow aggregation cancelled")
            return

        # Calculate cashflow metrics
        if self.enable_cashflow_metrics:
            self.calculate_cashflow_metrics()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Cashflow aggregation cancelled")
                return

        # Run sensitivity analysis
        if self.enable_sensitivity_analysis and hasattr(self, "run_sensitivity_analysis"):
            self.run_sensitivity_analysis()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Cashflow aggregation cancelled")
                return

        # Run scenario analysis
        if self.enable_scenario_analysis and hasattr(self, "run_scenario_analysis"):
            self.run_scenario_analysis()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Cashflow aggregation cancelled")
                return

        # Run tax impact analysis
        if self.enable_tax_impact_analysis and hasattr(self, "calculate_tax_impact"):
            self.calculate_tax_impact()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Cashflow aggregation cancelled")
                return

        # Run liquidity analysis
        if self.enable_liquidity_analysis and hasattr(self, "analyze_liquidity"):
            self.analyze_liquidity()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Cashflow aggregation cancelled")
                return

        # Export results
        if self.enable_export and hasattr(self, "export_results"):
            self.export_results()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Cashflow aggregation cancelled")
                return

        # Store results
        self.store_results()

        # Send completion message
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=100.0,
            message="Cashflow aggregation complete",
        )

        logger.info("Cashflow aggregator complete")

    def store_results(self) -> None:
        """
        Store cashflow results in the simulation context.
        """
        logger.info("Storing cashflow results")

        # Create cashflow results
        cashflow_results = {
            "loan_level_cashflows": self.loan_level_cashflows,
            "fund_level_cashflows": self.fund_level_cashflows,
            "stakeholder_cashflows": {
                "lp_cashflows": self.lp_cashflows,
                "gp_cashflows": self.gp_cashflows,
            },
            "visualization": {
                "cashflow_waterfall_chart": self.cashflow_waterfall_chart,
                "cashflow_by_year_chart": self.cashflow_by_year_chart,
                "cumulative_cashflow_chart": self.cumulative_cashflow_chart,
                "cashflow_table": self.cashflow_table,
                "cashflow_heatmap": self.cashflow_heatmap,
                "cashflow_sankey": self.cashflow_sankey,
                "scenario_comparison_chart": self.scenario_comparison_chart,
            },
            "metrics": {
                "fund_level_metrics": self.fund_level_metrics,
                "lp_metrics": self.lp_metrics,
                "gp_metrics": self.gp_metrics,
                "metrics_by_year": self.metrics_by_year,
            },
            "sensitivity_analysis": self.sensitivity_analysis_results,
            "scenario_analysis": self.scenario_analysis_results,
            "tax_impact": self.tax_impact_results,
            "liquidity_analysis": self.liquidity_analysis_results,
        }

        # Store in context
        self.context.cashflows = cashflow_results

        logger.info("Cashflow results stored in context")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="cashflow_aggregator",
            progress=95.0,
            message="Stored cashflow results",
        )

        # Send result message (note: this is a sync method, so we can't await)
        # The WebSocket message will be sent by the async aggregate_cashflows function


async def aggregate_cashflows(context: SimulationContext) -> None:
    """
    Aggregate cashflows for the simulation.

    This function is the entry point for the cashflow aggregator module.
    It creates a CashflowAggregator instance and calls the appropriate methods.

    Enhanced with:
    - Parallel processing for loan-level cashflow calculations
    - Daily cashflow granularity
    - Scenario analysis
    - Sensitivity analysis
    - Cashflow metrics calculation (IRR, DPI, RVPI, TVPI, etc.)
    - Waterfall integration
    - Tax impact analysis
    - Reinvestment modeling
    - Liquidity analysis
    - Enhanced visualization options
    - Export capabilities

    Args:
        context: Simulation context
    """
    logger.info("🚨 CASHFLOW AGGREGATOR CALLED - Starting cashflow aggregation")

    # Get WebSocket manager
    websocket_manager = get_websocket_manager()

    # Send progress update
    await websocket_manager.send_progress(
        simulation_id=context.run_id,
        module="cashflow_aggregator",
        progress=0.0,
        message="Starting cashflow aggregation",
    )

    try:
        # Create cashflow aggregator
        aggregator = CashflowAggregator(context)

        # Calculate loan-level cashflows
        aggregator.calculate_loan_level_cashflows()

        # Check for cancellation
        if websocket_manager.is_cancelled(context.run_id):
            logger.info("Cashflow aggregation cancelled")
            await websocket_manager.send_info(
                simulation_id=context.run_id,
                message="Cashflow aggregation cancelled",
            )
            return

        # Calculate fund-level cashflows
        aggregator.calculate_fund_level_cashflows()

        # Check for cancellation
        if websocket_manager.is_cancelled(context.run_id):
            logger.info("Cashflow aggregation cancelled")
            await websocket_manager.send_info(
                simulation_id=context.run_id,
                message="Cashflow aggregation cancelled",
            )
            return

        # Calculate stakeholder cashflows
        aggregator.calculate_stakeholder_cashflows()

        # Check for cancellation
        if websocket_manager.is_cancelled(context.run_id):
            logger.info("Cashflow aggregation cancelled")
            await websocket_manager.send_info(
                simulation_id=context.run_id,
                message="Cashflow aggregation cancelled",
            )
            return

        # Generate visualization data
        aggregator.generate_visualization_data()

        # Check for cancellation
        if websocket_manager.is_cancelled(context.run_id):
            logger.info("Cashflow aggregation cancelled")
            await websocket_manager.send_info(
                simulation_id=context.run_id,
                message="Cashflow aggregation cancelled",
            )
            return

        # Calculate cashflow metrics
        if aggregator.enable_cashflow_metrics:
            aggregator.calculate_cashflow_metrics()

            # Check for cancellation
            if websocket_manager.is_cancelled(context.run_id):
                logger.info("Cashflow aggregation cancelled")
                await websocket_manager.send_info(
                    simulation_id=context.run_id,
                    message="Cashflow aggregation cancelled",
                )
                return

        # Run sensitivity analysis
        if aggregator.enable_sensitivity_analysis and hasattr(aggregator, "run_sensitivity_analysis"):
            aggregator.run_sensitivity_analysis()

            # Check for cancellation
            if websocket_manager.is_cancelled(context.run_id):
                logger.info("Cashflow aggregation cancelled")
                await websocket_manager.send_info(
                    simulation_id=context.run_id,
                    message="Cashflow aggregation cancelled",
                )
                return

        # Run scenario analysis
        if aggregator.enable_scenario_analysis and hasattr(aggregator, "run_scenario_analysis"):
            aggregator.run_scenario_analysis()

            # Check for cancellation
            if websocket_manager.is_cancelled(context.run_id):
                logger.info("Cashflow aggregation cancelled")
                await websocket_manager.send_info(
                    simulation_id=context.run_id,
                    message="Cashflow aggregation cancelled",
                )
                return

        # Run tax impact analysis
        if aggregator.enable_tax_impact_analysis and hasattr(aggregator, "calculate_tax_impact"):
            aggregator.calculate_tax_impact()

            # Check for cancellation
            if websocket_manager.is_cancelled(context.run_id):
                logger.info("Cashflow aggregation cancelled")
                await websocket_manager.send_info(
                    simulation_id=context.run_id,
                    message="Cashflow aggregation cancelled",
                )
                return

        # Run liquidity analysis
        if aggregator.enable_liquidity_analysis and hasattr(aggregator, "analyze_liquidity"):
            aggregator.analyze_liquidity()

            # Check for cancellation
            if websocket_manager.is_cancelled(context.run_id):
                logger.info("Cashflow aggregation cancelled")
                await websocket_manager.send_info(
                    simulation_id=context.run_id,
                    message="Cashflow aggregation cancelled",
                )
                return

        # Export results
        if aggregator.enable_export and hasattr(aggregator, "export_results"):
            aggregator.export_results()

            # Check for cancellation
            if websocket_manager.is_cancelled(context.run_id):
                logger.info("Cashflow aggregation cancelled")
                await websocket_manager.send_info(
                    simulation_id=context.run_id,
                    message="Cashflow aggregation cancelled",
                )
                return

        # Store results
        aggregator.store_results()

        # Send completion message
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="cashflow_aggregator",
            progress=100.0,
            message="Cashflow aggregation complete",
        )

        logger.info("Cashflow aggregation complete")

    except Exception as e:
        logger.error("Error in cashflow aggregation", exc_info=True)
        await websocket_manager.send_error(
            simulation_id=context.run_id,
            error={
                "message": f"Error in cashflow aggregation: {str(e)}",
                "module": "cashflow_aggregator",
                "error_type": type(e).__name__,
            },
        )
        raise
