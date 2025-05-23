"""
Performance Reporter module for the EQU IHOME SIM ENGINE v2.

This module is responsible for generating comprehensive performance reports for the simulation,
including KPI tables, zone allocation reports, cash flow visualizations, risk metric reports,
and export capabilities.
"""

import logging
import math
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime
from enum import Enum
import numpy as np
import pandas as pd
import structlog
from collections import defaultdict
import json
import csv
import io
import os
from pathlib import Path

from src.engine.simulation_context import SimulationContext
from src.api.websocket_manager import get_websocket_manager
from src.utils.error_handler import handle_exception, log_error

# Set up logging
logger = structlog.get_logger(__name__)


class ReportFormat(str, Enum):
    """Report format enum."""

    JSON = "json"
    CSV = "csv"
    EXCEL = "excel"
    MARKDOWN = "markdown"
    HTML = "html"


class PerformanceReporter:
    """
    Performance Reporter for generating comprehensive performance reports.

    This class generates reports for the simulation, including:
    - KPI tables
    - Zone allocation reports
    - Cash flow visualizations
    - Risk metric reports
    - Export capabilities
    """

    def __init__(self, context: SimulationContext):
        """
        Initialize the performance reporter.

        Args:
            context: Simulation context
        """
        self.context = context
        self.config = context.config

        # Get performance reporter configuration with safe attribute access
        report_config_obj = getattr(self.config, "performance_reporter", {})
        if hasattr(report_config_obj, 'dict'):
            self.report_config = report_config_obj.dict()
        elif isinstance(report_config_obj, dict):
            self.report_config = report_config_obj
        else:
            self.report_config = {}

        # Get WebSocket manager
        self.websocket_manager = get_websocket_manager()

        # Initialize report data
        self.report_data = {
            "simulation_id": self.context.run_id,
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "kpi_table": {},
            "zone_allocation": {},
            "cash_flow": {},
            "risk_metrics": {},
            "tranche_performance": {},
            "loan_performance": {},
            "visualization": {},
        }

        # Get report configuration
        self.include_kpi_table = self.report_config.get("include_kpi_table", True)
        self.include_zone_allocation = self.report_config.get("include_zone_allocation", True)
        self.include_cash_flow = self.report_config.get("include_cash_flow", True)
        self.include_risk_metrics = self.report_config.get("include_risk_metrics", True)
        self.include_tranche_performance = self.report_config.get("include_tranche_performance", True)
        self.include_loan_performance = self.report_config.get("include_loan_performance", True)
        self.include_visualization = self.report_config.get("include_visualization", True)

        # Get export configuration
        self.export_format = self.report_config.get("export_format", ReportFormat.JSON)
        self.export_path = self.report_config.get("export_path", "reports")

        logger.info(
            "Performance reporter initialized",
            simulation_id=self.context.run_id,
            include_kpi_table=self.include_kpi_table,
            include_zone_allocation=self.include_zone_allocation,
            include_cash_flow=self.include_cash_flow,
            include_risk_metrics=self.include_risk_metrics,
            include_tranche_performance=self.include_tranche_performance,
            include_loan_performance=self.include_loan_performance,
            include_visualization=self.include_visualization,
            export_format=self.export_format,
            export_path=self.export_path,
        )

    async def generate_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive performance report.

        Returns:
            Dictionary containing the performance report
        """
        logger.info("Generating performance report", simulation_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="performance_reporter",
                progress=0.0,
                message="Starting performance report generation",
            )

        try:
            # Generate summary
            await self._generate_summary()

            # Check for cancellation
            if self.websocket_manager and self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Performance report generation cancelled", simulation_id=self.context.run_id)
                return self.report_data

            # Generate KPI table
            if self.include_kpi_table:
                await self._generate_kpi_table()

            # Check for cancellation
            if self.websocket_manager and self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Performance report generation cancelled", simulation_id=self.context.run_id)
                return self.report_data

            # Generate zone allocation report
            if self.include_zone_allocation:
                await self._generate_zone_allocation_report()

            # Check for cancellation
            if self.websocket_manager and self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Performance report generation cancelled", simulation_id=self.context.run_id)
                return self.report_data

            # Generate cash flow report
            if self.include_cash_flow:
                await self._generate_cash_flow_report()

            # Check for cancellation
            if self.websocket_manager and self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Performance report generation cancelled", simulation_id=self.context.run_id)
                return self.report_data

            # Generate risk metrics report
            if self.include_risk_metrics:
                await self._generate_risk_metrics_report()

            # Check for cancellation
            if self.websocket_manager and self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Performance report generation cancelled", simulation_id=self.context.run_id)
                return self.report_data

            # Generate tranche performance report
            if self.include_tranche_performance:
                await self._generate_tranche_performance_report()

            # Check for cancellation
            if self.websocket_manager and self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Performance report generation cancelled", simulation_id=self.context.run_id)
                return self.report_data

            # Generate loan performance report
            if self.include_loan_performance:
                await self._generate_loan_performance_report()

            # Check for cancellation
            if self.websocket_manager and self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Performance report generation cancelled", simulation_id=self.context.run_id)
                return self.report_data

            # Generate visualization data
            if self.include_visualization:
                await self._generate_visualization_data()

            # Export report
            await self._export_report()

            # Store report in context
            self.context.performance_report = self.report_data

            # Send progress update
            if self.websocket_manager:
                await self.websocket_manager.send_progress(
                    simulation_id=self.context.run_id,
                    module="performance_reporter",
                    progress=100.0,
                    message="Performance report generation completed",
                    data={"report_summary": self.report_data["summary"]},
                )

            logger.info("Performance report generation completed", simulation_id=self.context.run_id)

            return self.report_data

        except Exception as e:
            error_message = f"Error generating performance report: {str(e)}"
            logger.error(error_message, simulation_id=self.context.run_id, exc_info=True)

            # Send error message
            if self.websocket_manager:
                await self.websocket_manager.send_error(
                    simulation_id=self.context.run_id,
                    module="performance_reporter",
                    message=error_message,
                )

            # Handle exception
            handle_exception(e, logger)

            return {"error": error_message}

    async def _generate_summary(self) -> None:
        """Generate summary section of the report."""
        logger.info("Generating summary", simulation_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="performance_reporter",
                progress=10.0,
                message="Generating summary",
            )

        # Get fund parameters with safe attribute access
        fund_size = getattr(self.config, "fund_size", 0.0)
        fund_term = getattr(self.config, "fund_term", 10)
        hurdle_rate = getattr(self.config, "hurdle_rate", 0.08)

        # Get cashflow metrics if available
        cashflow_metrics = {}
        if hasattr(self.context, "cashflows") and self.context.cashflows:
            cashflow_metrics = self.context.cashflows.get("metrics", {})

        # Get fund-level metrics
        fund_level_metrics = cashflow_metrics.get("fund_level_metrics", {})
        irr = fund_level_metrics.get("irr", 0.0)
        moic = fund_level_metrics.get("moic", 0.0)
        tvpi = fund_level_metrics.get("tvpi", 0.0)
        dpi = fund_level_metrics.get("dpi", 0.0)
        rvpi = fund_level_metrics.get("rvpi", 0.0)

        # Get risk metrics if available
        risk_metrics = {}
        if hasattr(self.context, "risk_metrics") and self.context.risk_metrics:
            risk_metrics = self.context.risk_metrics

        # Get key risk metrics
        var_99 = risk_metrics.get("var_99", 0.0)
        sharpe_ratio = risk_metrics.get("sharpe_ratio", 0.0)

        # Get guardrail report if available
        guardrail_report = {}
        if hasattr(self.context, "guardrail_report") and self.context.guardrail_report:
            guardrail_report = self.context.guardrail_report.to_dict() if hasattr(self.context.guardrail_report, "to_dict") else self.context.guardrail_report

        # Get worst guardrail level
        worst_level = guardrail_report.get("worst_level", "INFO")

        # Get portfolio metrics
        num_loans = 0
        total_loan_amount = 0.0
        avg_ltv = 0.0

        if hasattr(self.context, "portfolio") and self.context.portfolio:
            loans = self.context.portfolio.get("loans", [])
            num_loans = len(loans)
            total_loan_amount = sum(loan.get("loan_amount", 0.0) for loan in loans)

            # Calculate average LTV
            if num_loans > 0:
                avg_ltv = sum(loan.get("ltv", 0.0) for loan in loans) / num_loans

        # Create summary
        self.report_data["summary"] = {
            "fund_size": fund_size,
            "fund_term": fund_term,
            "hurdle_rate": hurdle_rate,
            "num_loans": num_loans,
            "total_loan_amount": total_loan_amount,
            "avg_ltv": avg_ltv,
            "irr": irr,
            "moic": moic,
            "tvpi": tvpi,
            "dpi": dpi,
            "rvpi": rvpi,
            "var_99": var_99,
            "sharpe_ratio": sharpe_ratio,
            "worst_guardrail_level": worst_level,
            "simulation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        logger.info("Summary generated", simulation_id=self.context.run_id)

    async def _generate_kpi_table(self) -> None:
        """Generate KPI table section of the report."""
        logger.info("Generating KPI table", simulation_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="performance_reporter",
                progress=20.0,
                message="Generating KPI table",
            )

        # Initialize KPI categories
        kpi_table = {
            "fund_metrics": [],
            "portfolio_metrics": [],
            "risk_metrics": [],
            "liquidity_metrics": [],
            "leverage_metrics": [],
            "stakeholder_metrics": [],
        }

        # Get cashflow metrics if available
        cashflow_metrics = {}
        if hasattr(self.context, "cashflows") and self.context.cashflows:
            cashflow_metrics = self.context.cashflows.get("metrics", {})

        # Get fund-level metrics
        fund_level_metrics = cashflow_metrics.get("fund_level_metrics", {})

        # Add fund metrics
        kpi_table["fund_metrics"] = [
            {"name": "Net IRR", "value": fund_level_metrics.get("irr", 0.0), "format": "percentage", "description": "Internal Rate of Return"},
            {"name": "Gross IRR", "value": fund_level_metrics.get("gross_irr", 0.0), "format": "percentage", "description": "Gross Internal Rate of Return"},
            {"name": "MOIC", "value": fund_level_metrics.get("moic", 0.0), "format": "decimal", "description": "Multiple on Invested Capital"},
            {"name": "TVPI", "value": fund_level_metrics.get("tvpi", 0.0), "format": "decimal", "description": "Total Value to Paid-In"},
            {"name": "DPI", "value": fund_level_metrics.get("dpi", 0.0), "format": "decimal", "description": "Distributions to Paid-In"},
            {"name": "RVPI", "value": fund_level_metrics.get("rvpi", 0.0), "format": "decimal", "description": "Residual Value to Paid-In"},
            {"name": "Payback Period", "value": fund_level_metrics.get("payback_period", 0.0), "format": "years", "description": "Time to recover investment"},
        ]

        # Get portfolio metrics
        portfolio_metrics = {}
        if hasattr(self.context, "portfolio") and self.context.portfolio:
            portfolio = self.context.portfolio
            loans = portfolio.get("loans", [])
            num_loans = len(loans)
            total_loan_amount = sum(loan.get("loan_amount", 0.0) for loan in loans)

            # Calculate average LTV
            avg_ltv = 0.0
            if num_loans > 0:
                avg_ltv = sum(loan.get("ltv", 0.0) for loan in loans) / num_loans

            # Calculate zone distribution
            zone_distribution = defaultdict(float)
            for loan in loans:
                suburb = loan.get("suburb", "")
                loan_amount = loan.get("loan_amount", 0.0)

                # Get suburb zone from TLS data
                suburb_zone = "green"  # Default to green zone

                if hasattr(self.context, "tls_manager") and self.context.tls_manager and suburb:
                    suburb_data = self.context.tls_manager.get_suburb_data(suburb)
                    suburb_zone = suburb_data.get("zone", "green")

                zone_distribution[suburb_zone] += loan_amount

            # Calculate zone percentages
            zone_percentages = {}
            if total_loan_amount > 0:
                for zone, amount in zone_distribution.items():
                    zone_percentages[zone] = amount / total_loan_amount

            portfolio_metrics = {
                "num_loans": num_loans,
                "total_loan_amount": total_loan_amount,
                "avg_ltv": avg_ltv,
                "zone_percentages": zone_percentages,
            }

        # Add portfolio metrics
        kpi_table["portfolio_metrics"] = [
            {"name": "Number of Loans", "value": portfolio_metrics.get("num_loans", 0), "format": "integer", "description": "Total number of loans in the portfolio"},
            {"name": "Total Loan Amount", "value": portfolio_metrics.get("total_loan_amount", 0.0), "format": "currency", "description": "Total amount of loans in the portfolio"},
            {"name": "Average LTV", "value": portfolio_metrics.get("avg_ltv", 0.0), "format": "percentage", "description": "Average Loan-to-Value ratio"},
            {"name": "Green Zone %", "value": portfolio_metrics.get("zone_percentages", {}).get("green", 0.0), "format": "percentage", "description": "Percentage of portfolio in green zones"},
            {"name": "Orange Zone %", "value": portfolio_metrics.get("zone_percentages", {}).get("orange", 0.0), "format": "percentage", "description": "Percentage of portfolio in orange zones"},
            {"name": "Red Zone %", "value": portfolio_metrics.get("zone_percentages", {}).get("red", 0.0), "format": "percentage", "description": "Percentage of portfolio in red zones"},
        ]

        # Get risk metrics if available
        risk_metrics = {}
        if hasattr(self.context, "risk_metrics") and self.context.risk_metrics:
            risk_metrics = self.context.risk_metrics

        # Add risk metrics
        kpi_table["risk_metrics"] = [
            {"name": "VaR (95%)", "value": risk_metrics.get("var_95", 0.0), "format": "percentage", "description": "Value at Risk (95% confidence)"},
            {"name": "VaR (99%)", "value": risk_metrics.get("var_99", 0.0), "format": "percentage", "description": "Value at Risk (99% confidence)"},
            {"name": "Sharpe Ratio", "value": risk_metrics.get("sharpe_ratio", 0.0), "format": "decimal", "description": "Risk-adjusted return"},
            {"name": "Sortino Ratio", "value": risk_metrics.get("sortino_ratio", 0.0), "format": "decimal", "description": "Downside risk-adjusted return"},
            {"name": "Max Drawdown", "value": risk_metrics.get("max_drawdown", 0.0), "format": "percentage", "description": "Maximum peak-to-trough decline"},
            {"name": "Beta", "value": risk_metrics.get("beta", 0.0), "format": "decimal", "description": "Market sensitivity"},
            {"name": "Alpha", "value": risk_metrics.get("alpha", 0.0), "format": "percentage", "description": "Excess return over benchmark"},
        ]

        # Get liquidity metrics
        liquidity_metrics = risk_metrics.get("liquidity_metrics", {})

        # Add liquidity metrics
        kpi_table["liquidity_metrics"] = [
            {"name": "Liquidity Buffer", "value": liquidity_metrics.get("liquidity_buffer", 0.0), "format": "percentage", "description": "Cash + undrawn as % of NAV"},
            {"name": "WAL", "value": liquidity_metrics.get("wal", 0.0), "format": "years", "description": "Weighted Average Life"},
            {"name": "Expected Exit Lag", "value": liquidity_metrics.get("expected_exit_lag", 0.0), "format": "months", "description": "Average time to exit"},
            {"name": "Liquidity Score", "value": liquidity_metrics.get("liquidity_score", 0.0), "format": "decimal", "description": "Overall liquidity score"},
        ]

        # Get leverage metrics
        leverage_metrics = risk_metrics.get("leverage_metrics", {})

        # Add leverage metrics
        kpi_table["leverage_metrics"] = [
            {"name": "NAV Utilisation", "value": leverage_metrics.get("nav_utilisation", 0.0), "format": "percentage", "description": "Debt as % of NAV"},
            {"name": "Interest Coverage", "value": leverage_metrics.get("interest_coverage", 0.0), "format": "decimal", "description": "Income / Interest expense"},
            {"name": "Debt-to-Equity", "value": leverage_metrics.get("debt_to_equity", 0.0), "format": "decimal", "description": "Debt / Equity ratio"},
        ]

        # Get LP and GP metrics
        lp_metrics = cashflow_metrics.get("lp_metrics", {})
        gp_metrics = cashflow_metrics.get("gp_metrics", {})

        # Add stakeholder metrics
        kpi_table["stakeholder_metrics"] = [
            {"name": "LP IRR", "value": lp_metrics.get("irr", 0.0), "format": "percentage", "description": "Limited Partner IRR"},
            {"name": "LP MOIC", "value": lp_metrics.get("moic", 0.0), "format": "decimal", "description": "Limited Partner MOIC"},
            {"name": "GP IRR", "value": gp_metrics.get("irr", 0.0), "format": "percentage", "description": "General Partner IRR"},
            {"name": "GP MOIC", "value": gp_metrics.get("moic", 0.0), "format": "decimal", "description": "General Partner MOIC"},
            {"name": "Carried Interest", "value": gp_metrics.get("carried_interest", 0.0), "format": "currency", "description": "Total carried interest"},
            {"name": "Management Fees", "value": gp_metrics.get("management_fees", 0.0), "format": "currency", "description": "Total management fees"},
        ]

        # Store KPI table
        self.report_data["kpi_table"] = kpi_table

        logger.info("KPI table generated", simulation_id=self.context.run_id)

    async def _generate_zone_allocation_report(self) -> None:
        """Generate zone allocation section of the report."""
        logger.info("Generating zone allocation report", simulation_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="performance_reporter",
                progress=30.0,
                message="Generating zone allocation report",
            )

        # Initialize zone allocation data
        zone_allocation = {
            "by_zone": {},
            "by_suburb": {},
            "by_property_type": {},
            "by_ltv_band": {},
            "by_loan_size_band": {},
            "target_vs_actual": {},
        }

        # Get portfolio data
        if not hasattr(self.context, "portfolio") or not self.context.portfolio:
            logger.warning("No portfolio data found", simulation_id=self.context.run_id)
            self.report_data["zone_allocation"] = zone_allocation
            return

        portfolio = self.context.portfolio
        loans = portfolio.get("loans", [])

        if not loans:
            logger.warning("No loans found in portfolio", simulation_id=self.context.run_id)
            self.report_data["zone_allocation"] = zone_allocation
            return

        # Calculate total loan amount
        total_loan_amount = sum(loan.get("loan_amount", 0.0) for loan in loans)

        if total_loan_amount == 0:
            logger.warning("Total loan amount is zero", simulation_id=self.context.run_id)
            self.report_data["zone_allocation"] = zone_allocation
            return

        # Calculate allocation by zone
        zone_amounts = defaultdict(float)
        for loan in loans:
            suburb = loan.get("suburb", "")
            loan_amount = loan.get("loan_amount", 0.0)

            # Get suburb zone from TLS data
            suburb_zone = "green"  # Default to green zone

            if hasattr(self.context, "tls_manager") and self.context.tls_manager and suburb:
                suburb_data = self.context.tls_manager.get_suburb_data(suburb)
                suburb_zone = suburb_data.get("zone", "green")

            zone_amounts[suburb_zone] += loan_amount

        # Calculate zone percentages
        zone_allocation["by_zone"] = {
            zone: {
                "amount": amount,
                "percentage": amount / total_loan_amount,
            }
            for zone, amount in zone_amounts.items()
        }

        # Calculate allocation by suburb
        suburb_amounts = defaultdict(float)
        for loan in loans:
            suburb = loan.get("suburb", "")
            loan_amount = loan.get("loan_amount", 0.0)

            suburb_amounts[suburb] += loan_amount

        # Calculate suburb percentages and sort by amount
        suburb_allocation = {
            suburb: {
                "amount": amount,
                "percentage": amount / total_loan_amount,
            }
            for suburb, amount in suburb_amounts.items()
        }

        # Sort suburbs by amount (descending) and take top 10
        top_suburbs = sorted(
            suburb_allocation.items(),
            key=lambda x: x[1]["amount"],
            reverse=True,
        )[:10]

        zone_allocation["by_suburb"] = {suburb: data for suburb, data in top_suburbs}

        # Calculate allocation by property type
        property_type_amounts = defaultdict(float)
        for loan in loans:
            property_type = loan.get("property_type", "Unknown")
            loan_amount = loan.get("loan_amount", 0.0)

            property_type_amounts[property_type] += loan_amount

        # Calculate property type percentages
        zone_allocation["by_property_type"] = {
            property_type: {
                "amount": amount,
                "percentage": amount / total_loan_amount,
            }
            for property_type, amount in property_type_amounts.items()
        }

        # Calculate allocation by LTV band
        ltv_bands = {
            "0-50%": (0.0, 0.5),
            "50-60%": (0.5, 0.6),
            "60-70%": (0.6, 0.7),
            "70-80%": (0.7, 0.8),
            "80-90%": (0.8, 0.9),
            "90-100%": (0.9, 1.0),
        }

        ltv_band_amounts = defaultdict(float)
        for loan in loans:
            ltv = loan.get("ltv", 0.0)
            loan_amount = loan.get("loan_amount", 0.0)

            for band_name, (lower, upper) in ltv_bands.items():
                if lower <= ltv < upper:
                    ltv_band_amounts[band_name] += loan_amount
                    break

        # Calculate LTV band percentages
        zone_allocation["by_ltv_band"] = {
            band: {
                "amount": amount,
                "percentage": amount / total_loan_amount,
            }
            for band, amount in ltv_band_amounts.items()
        }

        # Calculate allocation by loan size band
        loan_size_bands = {
            "$0-$100k": (0, 100000),
            "$100k-$200k": (100000, 200000),
            "$200k-$300k": (200000, 300000),
            "$300k-$400k": (300000, 400000),
            "$400k-$500k": (400000, 500000),
            "$500k+": (500000, float("inf")),
        }

        loan_size_band_amounts = defaultdict(float)
        for loan in loans:
            loan_amount = loan.get("loan_amount", 0.0)

            for band_name, (lower, upper) in loan_size_bands.items():
                if lower <= loan_amount < upper:
                    loan_size_band_amounts[band_name] += loan_amount
                    break

        # Calculate loan size band percentages
        zone_allocation["by_loan_size_band"] = {
            band: {
                "amount": amount,
                "percentage": amount / total_loan_amount,
            }
            for band, amount in loan_size_band_amounts.items()
        }

        # Calculate target vs actual allocation with safe attribute access
        target_allocation = getattr(self.config, "target_allocation", {})

        zone_allocation["target_vs_actual"] = {
            zone: {
                "target": target_allocation.get(zone, 0.0),
                "actual": zone_allocation["by_zone"].get(zone, {}).get("percentage", 0.0),
                "difference": zone_allocation["by_zone"].get(zone, {}).get("percentage", 0.0) - target_allocation.get(zone, 0.0),
            }
            for zone in set(list(target_allocation.keys()) + list(zone_allocation["by_zone"].keys()))
        }

        # Store zone allocation data
        self.report_data["zone_allocation"] = zone_allocation

        logger.info("Zone allocation report generated", simulation_id=self.context.run_id)

    async def _generate_cash_flow_report(self) -> None:
        """Generate cash flow section of the report."""
        logger.info("Generating cash flow report", simulation_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="performance_reporter",
                progress=40.0,
                message="Generating cash flow report",
            )

        # Initialize cash flow data
        cash_flow = {
            "fund_level": [],
            "lp_level": [],
            "gp_level": [],
            "by_category": {},
            "cumulative": [],
            "metrics_by_year": [],
        }

        # Get cashflow data
        if not hasattr(self.context, "cashflows") or not self.context.cashflows:
            logger.warning("No cashflow data found", simulation_id=self.context.run_id)
            self.report_data["cash_flow"] = cash_flow
            return

        cashflows = self.context.cashflows

        # Get fund-level cashflows
        fund_level_cashflows = cashflows.get("fund_level_cashflows", [])

        if not fund_level_cashflows:
            logger.warning("No fund-level cashflows found", simulation_id=self.context.run_id)
            self.report_data["cash_flow"] = cash_flow
            return

        # Add fund-level cashflows
        cash_flow["fund_level"] = fund_level_cashflows

        # Get LP cashflows
        lp_cashflows = cashflows.get("lp_cashflows", [])

        # Add LP cashflows
        cash_flow["lp_level"] = lp_cashflows

        # Get GP cashflows
        gp_cashflows = cashflows.get("gp_cashflows", [])

        # Add GP cashflows
        cash_flow["gp_level"] = gp_cashflows

        # Calculate cashflows by category
        categories = [
            "capital_calls",
            "loan_investments",
            "origination_fees",
            "principal_repayments",
            "interest_income",
            "appreciation_share",
            "management_fees",
            "fund_expenses",
            "leverage_draws",
            "leverage_repayments",
            "leverage_interest",
            "distributions",
        ]

        for category in categories:
            cash_flow["by_category"][category] = [
                {
                    "year": cf.get("year", 0),
                    "amount": cf.get(category, 0.0),
                }
                for cf in fund_level_cashflows
            ]

        # Calculate cumulative cashflows
        cumulative_cashflow = 0.0
        cash_flow["cumulative"] = []

        for cf in fund_level_cashflows:
            year = cf.get("year", 0)
            net_cashflow = cf.get("net_cashflow", 0.0)
            cumulative_cashflow += net_cashflow

            cash_flow["cumulative"].append({
                "year": year,
                "net_cashflow": net_cashflow,
                "cumulative_cashflow": cumulative_cashflow,
            })

        # Calculate metrics by year
        metrics_by_year = []

        # Get fund size with safe attribute access
        fund_size = getattr(self.config, "fund_size", 0.0)

        # Calculate metrics for each year
        for i, cf in enumerate(fund_level_cashflows):
            year = cf.get("year", 0)

            # Calculate distributions to date
            distributions_to_date = sum(
                cf.get("distributions", 0.0)
                for cf in fund_level_cashflows[:i+1]
            )

            # Calculate NAV
            nav = cumulative_cashflow

            # Calculate DPI
            dpi = distributions_to_date / fund_size if fund_size > 0 else 0.0

            # Calculate RVPI
            rvpi = nav / fund_size if fund_size > 0 else 0.0

            # Calculate TVPI
            tvpi = dpi + rvpi

            # Calculate IRR
            # This is a simplified calculation; in a real implementation, we would use a proper IRR calculation
            cashflows_to_date = [cf.get("net_cashflow", 0.0) for cf in fund_level_cashflows[:i+1]]
            irr = 0.0  # Placeholder

            # Calculate cash yield
            cash_yield = distributions_to_date / fund_size if fund_size > 0 else 0.0

            metrics_by_year.append({
                "year": year,
                "dpi": dpi,
                "rvpi": rvpi,
                "tvpi": tvpi,
                "irr": irr,
                "cash_yield": cash_yield,
            })

        cash_flow["metrics_by_year"] = metrics_by_year

        # Store cash flow data
        self.report_data["cash_flow"] = cash_flow

        logger.info("Cash flow report generated", simulation_id=self.context.run_id)

    async def _generate_risk_metrics_report(self) -> None:
        """Generate risk metrics section of the report."""
        logger.info("Generating risk metrics report", simulation_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="performance_reporter",
                progress=50.0,
                message="Generating risk metrics report",
            )

        # Initialize risk metrics data
        risk_metrics = {
            "market_price_metrics": {},
            "credit_metrics": {},
            "liquidity_metrics": {},
            "leverage_metrics": {},
            "concentration_metrics": {},
            "performance_metrics": {},
            "stress_test_results": {},
            "sensitivity_analysis": {},
            "visualization": {},
        }

        # Get risk metrics data
        if not hasattr(self.context, "risk_metrics") or not self.context.risk_metrics:
            logger.warning("No risk metrics data found", simulation_id=self.context.run_id)
            self.report_data["risk_metrics"] = risk_metrics
            return

        # Get risk metrics
        context_risk_metrics = self.context.risk_metrics

        # Add market price metrics
        risk_metrics["market_price_metrics"] = context_risk_metrics.get("market_price_metrics", {})

        # Add credit metrics
        risk_metrics["credit_metrics"] = context_risk_metrics.get("credit_metrics", {})

        # Add liquidity metrics
        risk_metrics["liquidity_metrics"] = context_risk_metrics.get("liquidity_metrics", {})

        # Add leverage metrics
        risk_metrics["leverage_metrics"] = context_risk_metrics.get("leverage_metrics", {})

        # Add concentration metrics
        risk_metrics["concentration_metrics"] = context_risk_metrics.get("concentration_metrics", {})

        # Add performance metrics
        risk_metrics["performance_metrics"] = context_risk_metrics.get("performance_metrics", {})

        # Add stress test results
        risk_metrics["stress_test_results"] = context_risk_metrics.get("stress_test_results", {})

        # Add sensitivity analysis
        risk_metrics["sensitivity_analysis"] = context_risk_metrics.get("sensitivity_analysis", {})

        # Add visualization data
        risk_metrics["visualization"] = context_risk_metrics.get("visualization", {})

        # Store risk metrics data
        self.report_data["risk_metrics"] = risk_metrics

        logger.info("Risk metrics report generated", simulation_id=self.context.run_id)

    async def _generate_tranche_performance_report(self) -> None:
        """Generate tranche performance section of the report."""
        logger.info("Generating tranche performance report", simulation_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="performance_reporter",
                progress=60.0,
                message="Generating tranche performance report",
            )

        # Initialize tranche performance data
        tranche_performance = {
            "tranche_summary": [],
            "tranche_cashflows": {},
            "tranche_allocations": {},
            "coverage_tests": {},
            "reserve_account": [],
            "visualization": {},
        }

        # Get tranche data
        if not hasattr(self.context, "tranches") or not self.context.tranches:
            logger.warning("No tranche data found", simulation_id=self.context.run_id)
            self.report_data["tranche_performance"] = tranche_performance
            return

        # Get tranches
        tranches = self.context.tranches

        # Add tranche summary
        tranche_summary = tranches.get("tranche_summary", [])
        tranche_performance["tranche_summary"] = tranche_summary

        # Add tranche cashflows
        tranche_cashflows = tranches.get("tranche_cashflows", {})
        tranche_performance["tranche_cashflows"] = tranche_cashflows

        # Add tranche allocations
        tranche_allocations = tranches.get("tranche_allocations", {})
        tranche_performance["tranche_allocations"] = tranche_allocations

        # Add coverage tests
        coverage_tests = tranches.get("coverage_tests", {})
        tranche_performance["coverage_tests"] = coverage_tests

        # Add reserve account
        reserve_account = tranches.get("reserve_account", [])
        tranche_performance["reserve_account"] = reserve_account

        # Add visualization data
        visualization = tranches.get("visualization", {})
        tranche_performance["visualization"] = visualization

        # Store tranche performance data
        self.report_data["tranche_performance"] = tranche_performance

        logger.info("Tranche performance report generated", simulation_id=self.context.run_id)

    async def _generate_loan_performance_report(self) -> None:
        """Generate loan performance section of the report."""
        logger.info("Generating loan performance report", simulation_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="performance_reporter",
                progress=70.0,
                message="Generating loan performance report",
            )

        # Initialize loan performance data
        loan_performance = {
            "loan_summary": [],
            "loan_cashflows": {},
            "loan_metrics": {},
            "loan_exits": {},
            "loan_defaults": {},
            "visualization": {},
        }

        # Get portfolio data
        if not hasattr(self.context, "portfolio") or not self.context.portfolio:
            logger.warning("No portfolio data found", simulation_id=self.context.run_id)
            self.report_data["loan_performance"] = loan_performance
            return

        # Get loans
        portfolio = self.context.portfolio
        loans = portfolio.get("loans", [])

        if not loans:
            logger.warning("No loans found in portfolio", simulation_id=self.context.run_id)
            self.report_data["loan_performance"] = loan_performance
            return

        # Get exits
        exits = {}
        if hasattr(self.context, "exits") and self.context.exits:
            exits = self.context.exits

        # Get cashflows
        loan_cashflows = {}
        if hasattr(self.context, "cashflows") and self.context.cashflows:
            loan_cashflows = self.context.cashflows.get("loan_level_cashflows", {})

        # Create loan summary
        loan_summary = []

        for loan in loans:
            loan_id = loan.get("loan_id", "")
            suburb = loan.get("suburb", "")
            loan_amount = loan.get("loan_amount", 0.0)
            ltv = loan.get("ltv", 0.0)
            property_type = loan.get("property_type", "Unknown")

            # Get suburb zone from TLS data
            suburb_zone = "green"  # Default to green zone

            if hasattr(self.context, "tls_manager") and self.context.tls_manager and suburb:
                suburb_data = self.context.tls_manager.get_suburb_data(suburb)
                suburb_zone = suburb_data.get("zone", "green")

            # Get exit data
            exit_data = exits.get(loan_id, {})
            exit_month = exit_data.get("exit_month", 0)
            exit_type = exit_data.get("exit_type", "")
            exit_amount = exit_data.get("exit_amount", 0.0)

            # Calculate return
            return_amount = exit_amount - loan_amount
            return_percentage = return_amount / loan_amount if loan_amount > 0 else 0.0

            # Calculate IRR
            # This is a simplified calculation; in a real implementation, we would use a proper IRR calculation
            irr = 0.0  # Placeholder

            loan_summary.append({
                "loan_id": loan_id,
                "suburb": suburb,
                "zone": suburb_zone,
                "loan_amount": loan_amount,
                "ltv": ltv,
                "property_type": property_type,
                "exit_month": exit_month,
                "exit_type": exit_type,
                "exit_amount": exit_amount,
                "return_amount": return_amount,
                "return_percentage": return_percentage,
                "irr": irr,
            })

        loan_performance["loan_summary"] = loan_summary

        # Add loan cashflows
        loan_performance["loan_cashflows"] = loan_cashflows

        # Calculate loan metrics
        loan_metrics = {}

        for loan in loans:
            loan_id = loan.get("loan_id", "")
            loan_amount = loan.get("loan_amount", 0.0)

            # Get exit data
            exit_data = exits.get(loan_id, {})
            exit_month = exit_data.get("exit_month", 0)
            exit_amount = exit_data.get("exit_amount", 0.0)

            # Calculate return
            return_amount = exit_amount - loan_amount
            return_percentage = return_amount / loan_amount if loan_amount > 0 else 0.0

            # Calculate IRR
            # This is a simplified calculation; in a real implementation, we would use a proper IRR calculation
            irr = 0.0  # Placeholder

            loan_metrics[loan_id] = {
                "loan_amount": loan_amount,
                "exit_month": exit_month,
                "exit_amount": exit_amount,
                "return_amount": return_amount,
                "return_percentage": return_percentage,
                "irr": irr,
            }

        loan_performance["loan_metrics"] = loan_metrics

        # Add loan exits
        loan_performance["loan_exits"] = exits

        # Calculate loan defaults
        loan_defaults = {}

        for loan_id, exit_data in exits.items():
            exit_type = exit_data.get("exit_type", "")

            if exit_type == "default":
                loan_defaults[loan_id] = exit_data

        loan_performance["loan_defaults"] = loan_defaults

        # Generate visualization data
        visualization = {
            "loan_size_distribution": self._generate_loan_size_distribution(loans),
            "ltv_distribution": self._generate_ltv_distribution(loans),
            "exit_month_distribution": self._generate_exit_month_distribution(exits),
            "exit_type_distribution": self._generate_exit_type_distribution(exits),
            "return_distribution": self._generate_return_distribution(loan_summary),
        }

        loan_performance["visualization"] = visualization

        # Store loan performance data
        self.report_data["loan_performance"] = loan_performance

        logger.info("Loan performance report generated", simulation_id=self.context.run_id)

    def _generate_loan_size_distribution(self, loans: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate loan size distribution visualization data."""
        # Define loan size bands
        loan_size_bands = {
            "$0-$100k": (0, 100000),
            "$100k-$200k": (100000, 200000),
            "$200k-$300k": (200000, 300000),
            "$300k-$400k": (300000, 400000),
            "$400k-$500k": (400000, 500000),
            "$500k+": (500000, float("inf")),
        }

        # Count loans in each band
        band_counts = defaultdict(int)

        for loan in loans:
            loan_amount = loan.get("loan_amount", 0.0)

            for band_name, (lower, upper) in loan_size_bands.items():
                if lower <= loan_amount < upper:
                    band_counts[band_name] += 1
                    break

        # Create visualization data
        return {
            "bands": list(loan_size_bands.keys()),
            "counts": [band_counts[band] for band in loan_size_bands.keys()],
        }

    def _generate_ltv_distribution(self, loans: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate LTV distribution visualization data."""
        # Define LTV bands
        ltv_bands = {
            "0-50%": (0.0, 0.5),
            "50-60%": (0.5, 0.6),
            "60-70%": (0.6, 0.7),
            "70-80%": (0.7, 0.8),
            "80-90%": (0.8, 0.9),
            "90-100%": (0.9, 1.0),
        }

        # Count loans in each band
        band_counts = defaultdict(int)

        for loan in loans:
            ltv = loan.get("ltv", 0.0)

            for band_name, (lower, upper) in ltv_bands.items():
                if lower <= ltv < upper:
                    band_counts[band_name] += 1
                    break

        # Create visualization data
        return {
            "bands": list(ltv_bands.keys()),
            "counts": [band_counts[band] for band in ltv_bands.keys()],
        }

    def _generate_exit_month_distribution(self, exits: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Generate exit month distribution visualization data."""
        # Define exit month bands
        exit_month_bands = {
            "0-12": (0, 12),
            "13-24": (13, 24),
            "25-36": (25, 36),
            "37-48": (37, 48),
            "49-60": (49, 60),
            "61-72": (61, 72),
            "73-84": (73, 84),
            "85-96": (85, 96),
            "97-108": (97, 108),
            "109-120": (109, 120),
            "120+": (121, float("inf")),
        }

        # Count exits in each band
        band_counts = defaultdict(int)

        for loan_id, exit_data in exits.items():
            exit_month = exit_data.get("exit_month", 0)

            for band_name, (lower, upper) in exit_month_bands.items():
                if lower <= exit_month < upper:
                    band_counts[band_name] += 1
                    break

        # Create visualization data
        return {
            "bands": list(exit_month_bands.keys()),
            "counts": [band_counts[band] for band in exit_month_bands.keys()],
        }

    def _generate_exit_type_distribution(self, exits: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Generate exit type distribution visualization data."""
        # Count exits by type
        exit_type_counts = defaultdict(int)

        for loan_id, exit_data in exits.items():
            exit_type = exit_data.get("exit_type", "")
            exit_type_counts[exit_type] += 1

        # Create visualization data
        return {
            "types": list(exit_type_counts.keys()),
            "counts": list(exit_type_counts.values()),
        }

    def _generate_return_distribution(self, loan_summary: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate return distribution visualization data."""
        # Define return bands
        return_bands = {
            "<0%": (float("-inf"), 0.0),
            "0-5%": (0.0, 0.05),
            "5-10%": (0.05, 0.1),
            "10-15%": (0.1, 0.15),
            "15-20%": (0.15, 0.2),
            "20-25%": (0.2, 0.25),
            "25-30%": (0.25, 0.3),
            "30-35%": (0.3, 0.35),
            "35-40%": (0.35, 0.4),
            "40-45%": (0.4, 0.45),
            "45-50%": (0.45, 0.5),
            "50%+": (0.5, float("inf")),
        }

        # Count loans in each band
        band_counts = defaultdict(int)

        for loan in loan_summary:
            return_percentage = loan.get("return_percentage", 0.0)

            for band_name, (lower, upper) in return_bands.items():
                if lower <= return_percentage < upper:
                    band_counts[band_name] += 1
                    break

        # Create visualization data
        return {
            "bands": list(return_bands.keys()),
            "counts": [band_counts[band] for band in return_bands.keys()],
        }

    async def _generate_visualization_data(self) -> None:
        """Generate visualization data section of the report."""
        logger.info("Generating visualization data", simulation_id=self.context.run_id)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="performance_reporter",
                progress=80.0,
                message="Generating visualization data",
            )

        # Initialize visualization data
        visualization = {
            "kpi_summary": {},
            "zone_allocation": {},
            "cash_flow": {},
            "risk_metrics": {},
            "loan_performance": {},
            "tranche_performance": {},
        }

        # Generate KPI summary visualization
        visualization["kpi_summary"] = self._generate_kpi_summary_visualization()

        # Generate zone allocation visualization
        visualization["zone_allocation"] = self._generate_zone_allocation_visualization()

        # Generate cash flow visualization
        visualization["cash_flow"] = self._generate_cash_flow_visualization()

        # Generate risk metrics visualization
        visualization["risk_metrics"] = self._generate_risk_metrics_visualization()

        # Generate loan performance visualization
        visualization["loan_performance"] = self._generate_loan_performance_visualization()

        # Generate tranche performance visualization
        visualization["tranche_performance"] = self._generate_tranche_performance_visualization()

        # Store visualization data
        self.report_data["visualization"] = visualization

        logger.info("Visualization data generated", simulation_id=self.context.run_id)

    def _generate_kpi_summary_visualization(self) -> Dict[str, Any]:
        """Generate KPI summary visualization data."""
        # Get KPI table
        kpi_table = self.report_data.get("kpi_table", {})

        # Create KPI summary visualization
        return {
            "fund_metrics_chart": {
                "metrics": [metric["name"] for metric in kpi_table.get("fund_metrics", [])],
                "values": [metric["value"] for metric in kpi_table.get("fund_metrics", [])],
            },
            "portfolio_metrics_chart": {
                "metrics": [metric["name"] for metric in kpi_table.get("portfolio_metrics", [])],
                "values": [metric["value"] for metric in kpi_table.get("portfolio_metrics", [])],
            },
            "risk_metrics_chart": {
                "metrics": [metric["name"] for metric in kpi_table.get("risk_metrics", [])],
                "values": [metric["value"] for metric in kpi_table.get("risk_metrics", [])],
            },
        }

    def _generate_zone_allocation_visualization(self) -> Dict[str, Any]:
        """Generate zone allocation visualization data."""
        # Get zone allocation data
        zone_allocation = self.report_data.get("zone_allocation", {})

        # Create zone allocation visualization
        return {
            "by_zone_chart": {
                "zones": list(zone_allocation.get("by_zone", {}).keys()),
                "percentages": [data.get("percentage", 0.0) for data in zone_allocation.get("by_zone", {}).values()],
            },
            "by_suburb_chart": {
                "suburbs": list(zone_allocation.get("by_suburb", {}).keys()),
                "percentages": [data.get("percentage", 0.0) for data in zone_allocation.get("by_suburb", {}).values()],
            },
            "by_property_type_chart": {
                "property_types": list(zone_allocation.get("by_property_type", {}).keys()),
                "percentages": [data.get("percentage", 0.0) for data in zone_allocation.get("by_property_type", {}).values()],
            },
            "target_vs_actual_chart": {
                "zones": list(zone_allocation.get("target_vs_actual", {}).keys()),
                "target": [data.get("target", 0.0) for data in zone_allocation.get("target_vs_actual", {}).values()],
                "actual": [data.get("actual", 0.0) for data in zone_allocation.get("target_vs_actual", {}).values()],
            },
        }

    def _generate_cash_flow_visualization(self) -> Dict[str, Any]:
        """Generate cash flow visualization data."""
        # Get cash flow data
        cash_flow = self.report_data.get("cash_flow", {})

        # Create cash flow visualization
        return {
            "cumulative_chart": {
                "years": [cf.get("year", 0) for cf in cash_flow.get("cumulative", [])],
                "net_cashflow": [cf.get("net_cashflow", 0.0) for cf in cash_flow.get("cumulative", [])],
                "cumulative_cashflow": [cf.get("cumulative_cashflow", 0.0) for cf in cash_flow.get("cumulative", [])],
            },
            "by_category_chart": {
                "years": sorted(set(cf.get("year", 0) for cf in cash_flow.get("fund_level", []))),
                "categories": list(cash_flow.get("by_category", {}).keys()),
                "values": [
                    [cf.get("amount", 0.0) for cf in cash_flow.get("by_category", {}).get(category, [])]
                    for category in cash_flow.get("by_category", {}).keys()
                ],
            },
            "metrics_by_year_chart": {
                "years": [metrics.get("year", 0) for metrics in cash_flow.get("metrics_by_year", [])],
                "dpi": [metrics.get("dpi", 0.0) for metrics in cash_flow.get("metrics_by_year", [])],
                "rvpi": [metrics.get("rvpi", 0.0) for metrics in cash_flow.get("metrics_by_year", [])],
                "tvpi": [metrics.get("tvpi", 0.0) for metrics in cash_flow.get("metrics_by_year", [])],
                "irr": [metrics.get("irr", 0.0) for metrics in cash_flow.get("metrics_by_year", [])],
            },
        }

    def _generate_risk_metrics_visualization(self) -> Dict[str, Any]:
        """Generate risk metrics visualization data."""
        # Get risk metrics data
        risk_metrics = self.report_data.get("risk_metrics", {})

        # Create risk metrics visualization
        return {
            "var_chart": risk_metrics.get("visualization", {}).get("var_chart", {}),
            "concentration_chart": risk_metrics.get("visualization", {}).get("concentration_chart", {}),
            "stress_test_chart": risk_metrics.get("visualization", {}).get("stress_test_chart", {}),
            "sensitivity_chart": risk_metrics.get("visualization", {}).get("sensitivity_chart", {}),
        }

    def _generate_loan_performance_visualization(self) -> Dict[str, Any]:
        """Generate loan performance visualization data."""
        # Get loan performance data
        loan_performance = self.report_data.get("loan_performance", {})

        # Create loan performance visualization
        return {
            "loan_size_distribution": loan_performance.get("visualization", {}).get("loan_size_distribution", {}),
            "ltv_distribution": loan_performance.get("visualization", {}).get("ltv_distribution", {}),
            "exit_month_distribution": loan_performance.get("visualization", {}).get("exit_month_distribution", {}),
            "exit_type_distribution": loan_performance.get("visualization", {}).get("exit_type_distribution", {}),
            "return_distribution": loan_performance.get("visualization", {}).get("return_distribution", {}),
        }

    def _generate_tranche_performance_visualization(self) -> Dict[str, Any]:
        """Generate tranche performance visualization data."""
        # Get tranche performance data
        tranche_performance = self.report_data.get("tranche_performance", {})

        # Create tranche performance visualization
        return tranche_performance.get("visualization", {})

    async def _export_report(self) -> None:
        """Export the report to the specified format."""
        logger.info("Exporting report", simulation_id=self.context.run_id, format=self.export_format)

        # Send progress update
        if self.websocket_manager:
            await self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="performance_reporter",
                progress=90.0,
                message=f"Exporting report to {self.export_format}",
            )

        # Create export directory if it doesn't exist
        os.makedirs(self.export_path, exist_ok=True)

        # Generate export filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{self.context.run_id}_{timestamp}"

        # Export report based on format
        if self.export_format == ReportFormat.JSON:
            await self._export_to_json(filename)
        elif self.export_format == ReportFormat.CSV:
            await self._export_to_csv(filename)
        elif self.export_format == ReportFormat.EXCEL:
            await self._export_to_excel(filename)
        elif self.export_format == ReportFormat.MARKDOWN:
            await self._export_to_markdown(filename)
        elif self.export_format == ReportFormat.HTML:
            await self._export_to_html(filename)
        else:
            logger.warning(
                "Unsupported export format",
                simulation_id=self.context.run_id,
                format=self.export_format,
            )

        logger.info("Report exported", simulation_id=self.context.run_id, format=self.export_format)

    async def _export_to_json(self, filename: str) -> None:
        """Export the report to JSON format."""
        filepath = os.path.join(self.export_path, f"{filename}.json")

        with open(filepath, "w") as f:
            json.dump(self.report_data, f, indent=2)

        logger.info("Report exported to JSON", simulation_id=self.context.run_id, filepath=filepath)

    async def _export_to_csv(self, filename: str) -> None:
        """Export the report to CSV format."""
        # Export KPI table
        kpi_filepath = os.path.join(self.export_path, f"{filename}_kpi.csv")

        with open(kpi_filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Category", "Metric", "Value", "Format", "Description"])

            for category, metrics in self.report_data.get("kpi_table", {}).items():
                for metric in metrics:
                    writer.writerow([
                        category,
                        metric.get("name", ""),
                        metric.get("value", ""),
                        metric.get("format", ""),
                        metric.get("description", ""),
                    ])

        # Export loan summary
        loan_filepath = os.path.join(self.export_path, f"{filename}_loans.csv")

        with open(loan_filepath, "w", newline="") as f:
            writer = csv.writer(f)

            # Get loan summary
            loan_summary = self.report_data.get("loan_performance", {}).get("loan_summary", [])

            if loan_summary:
                # Write header
                writer.writerow(loan_summary[0].keys())

                # Write rows
                for loan in loan_summary:
                    writer.writerow(loan.values())

        logger.info(
            "Report exported to CSV",
            simulation_id=self.context.run_id,
            kpi_filepath=kpi_filepath,
            loan_filepath=loan_filepath,
        )

    async def _export_to_excel(self, filename: str) -> None:
        """Export the report to Excel format."""
        # This is a placeholder; in a real implementation, we would use a library like openpyxl or pandas
        logger.info(
            "Excel export not implemented",
            simulation_id=self.context.run_id,
        )

    async def _export_to_markdown(self, filename: str) -> None:
        """Export the report to Markdown format."""
        filepath = os.path.join(self.export_path, f"{filename}.md")

        with open(filepath, "w") as f:
            # Write title
            f.write(f"# Performance Report: {self.context.run_id}\n\n")
            f.write(f"Generated: {self.report_data.get('summary', {}).get('simulation_date', '')}\n\n")

            # Write summary
            f.write("## Summary\n\n")

            summary = self.report_data.get("summary", {})
            f.write("| Metric | Value |\n")
            f.write("|--------|-------|\n")

            for key, value in summary.items():
                if isinstance(value, float):
                    f.write(f"| {key} | {value:.2f} |\n")
                else:
                    f.write(f"| {key} | {value} |\n")

            f.write("\n")

            # Write KPI table
            f.write("## KPI Table\n\n")

            for category, metrics in self.report_data.get("kpi_table", {}).items():
                f.write(f"### {category.replace('_', ' ').title()}\n\n")
                f.write("| Metric | Value | Description |\n")
                f.write("|--------|-------|-------------|\n")

                for metric in metrics:
                    value = metric.get("value", 0.0)
                    format_type = metric.get("format", "")

                    if format_type == "percentage":
                        formatted_value = f"{value:.2%}"
                    elif format_type == "currency":
                        formatted_value = f"${value:,.2f}"
                    elif format_type == "decimal":
                        formatted_value = f"{value:.2f}"
                    elif format_type == "integer":
                        formatted_value = f"{int(value)}"
                    elif format_type == "years":
                        formatted_value = f"{value:.1f} years"
                    elif format_type == "months":
                        formatted_value = f"{value:.1f} months"
                    else:
                        formatted_value = str(value)

                    f.write(f"| {metric.get('name', '')} | {formatted_value} | {metric.get('description', '')} |\n")

                f.write("\n")

        logger.info("Report exported to Markdown", simulation_id=self.context.run_id, filepath=filepath)

    async def _export_to_html(self, filename: str) -> None:
        """Export the report to HTML format."""
        # This is a placeholder; in a real implementation, we would use a template engine like Jinja2
        logger.info(
            "HTML export not implemented",
            simulation_id=self.context.run_id,
        )
