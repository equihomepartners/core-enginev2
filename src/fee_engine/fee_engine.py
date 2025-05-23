"""
Fee engine module for the EQU IHOME SIM ENGINE v2.

This module is responsible for calculating fees and expenses for the fund,
including management fees, origination fees, and fund expenses.
"""

import logging
import math
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime

import numpy as np
import structlog

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

    def send_message(self, simulation_id: str, message_type: str, data: dict, **kwargs) -> None:
        """
        Safe sync wrapper for send_message.

        Logs the message instead of calling async method from sync context.
        """
        self.logger.info(
            "WebSocket message",
            simulation_id=simulation_id,
            message_type=message_type,
            data=data,
        )

    def send_error(self, simulation_id: str, error: dict, **kwargs) -> None:
        """
        Safe sync wrapper for send_error.

        Logs the error instead of calling async method from sync context.
        """
        self.logger.error(
            "WebSocket error",
            simulation_id=simulation_id,
            error=error,
        )

    def is_cancelled(self, simulation_id: str) -> bool:
        """Safe wrapper for is_cancelled (this method is already sync)."""
        return self.websocket_manager.is_cancelled(simulation_id)

# Set up logging
logger = structlog.get_logger(__name__)


class FeeEngine:
    """
    Fee engine for calculating fees and expenses.

    This class calculates various fees and expenses for the fund, including:
    - Management fees (based on committed capital, invested capital, or NAV)
    - Origination fees for loans
    - Fund expenses (fixed and variable)
    - Acquisition fees
    - Disposition fees
    - Setup costs
    """

    def __init__(self, context: SimulationContext):
        """
        Initialize the fee engine.

        Args:
            context: Simulation context
        """
        self.context = context
        self.config = context.config
        self.fee_config = getattr(self.config, "fee_engine", {})

        # Get WebSocket manager and create safe sync wrapper
        websocket_manager = get_websocket_manager()
        self.websocket_manager = SyncWebSocketWrapper(websocket_manager, context.run_id)

        # Initialize fee tracking
        self.management_fees: List[Dict[str, Any]] = []
        self.origination_fees: List[Dict[str, Any]] = []
        self.fund_expenses: List[Dict[str, Any]] = []
        self.acquisition_fees: List[Dict[str, Any]] = []
        self.disposition_fees: List[Dict[str, Any]] = []
        self.setup_costs = self._get_setup_costs()

        # Initialize visualization data
        self.fee_breakdown_chart: List[Dict[str, Any]] = []
        self.fees_by_year_chart: List[Dict[str, Any]] = []
        self.fee_impact_chart: List[Dict[str, Any]] = []
        self.fee_table: List[Dict[str, Any]] = []

        logger.info(
            "Fee engine initialized",
            management_fee_rate=self.config.management_fee_rate,
            management_fee_basis=self.config.management_fee_basis,
        )

    def _get_setup_costs(self) -> float:
        """
        Get setup costs from configuration.

        Returns:
            Setup costs in dollars
        """
        return getattr(self.fee_config, "setup_costs", 250000)

    def calculate_management_fees(self) -> None:
        """
        Calculate management fees for each year of the fund.

        Management fees can be based on:
        - Committed capital
        - Invested capital
        - Net asset value (NAV)
        """
        logger.info("Calculating management fees")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="fee_engine",
            progress=10.0,
            message="Calculating management fees",
        )

        # Get management fee parameters
        base_rate = self.config.management_fee_rate
        fee_basis = self.config.management_fee_basis
        fund_size = self.config.fund_size
        fund_term = self.config.fund_term

        # Get custom fee schedule if provided
        fee_schedule = getattr(self.fee_config, "management_fee_schedule", [])

        # Calculate management fees for each year
        for year in range(fund_term + 1):
            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return

            # Get fee rate for this year (use custom schedule if provided)
            fee_rate = base_rate
            for schedule_item in fee_schedule:
                if schedule_item.get("year") == year:
                    fee_rate = schedule_item.get("rate", base_rate)
                    break

            # Determine basis amount based on fee basis type
            basis_amount = fund_size  # Default to committed capital

            if fee_basis == "invested_capital":
                # Calculate invested capital based on loans
                invested_capital = sum(loan.get("loan_amount", 0) for loan in self.context.loans
                                     if loan.get("origination_year", 0) <= year)
                basis_amount = invested_capital

            elif fee_basis == "net_asset_value":
                # Calculate NAV based on current property values
                # This is a simplified calculation - in a real implementation,
                # we would need to account for debt, cash, and other assets/liabilities
                nav = 0
                for loan in self.context.loans:
                    loan_id = loan.get("loan_id")
                    property_id = loan.get("property_id")

                    # Skip loans that have already exited
                    if loan_id in self.context.exits and self.context.exits[loan_id].get("exit_year", float("inf")) <= year:
                        continue

                    # Get current property value
                    if property_id in self.context.price_paths:
                        price_path = self.context.price_paths[property_id]
                        if year < len(price_path):
                            current_value = loan.get("property_value", 0) * price_path[year]
                            nav += current_value * loan.get("ltv", 0)

                basis_amount = max(nav, 0)

            # Calculate fee amount
            fee_amount = basis_amount * fee_rate

            # Add to management fees list
            self.management_fees.append({
                "year": year,
                "fee_amount": fee_amount,
                "fee_basis": fee_basis,
                "basis_amount": basis_amount,
                "fee_rate": fee_rate,
            })

            logger.debug(
                "Management fee calculated",
                year=year,
                fee_amount=fee_amount,
                fee_basis=fee_basis,
                basis_amount=basis_amount,
                fee_rate=fee_rate,
            )

        logger.info(
            "Management fees calculated",
            total_fees=sum(fee.get("fee_amount", 0) for fee in self.management_fees),
            num_years=len(self.management_fees),
        )

    def calculate_origination_fees(self) -> None:
        """
        Calculate origination fees for each loan.
        """
        logger.info("Calculating origination fees")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="fee_engine",
            progress=30.0,
            message="Calculating origination fees",
        )

        # Get origination fee rate
        fee_rate = getattr(self.fee_config, "origination_fee_rate", 0.01)

        # Calculate origination fees for each loan
        for loan in self.context.loans:
            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return

            loan_id = loan.get("loan_id")
            loan_amount = loan.get("loan_amount", 0)
            origination_year = loan.get("origination_year", 0)

            # Calculate fee amount
            fee_amount = loan_amount * fee_rate

            # Add to origination fees list
            self.origination_fees.append({
                "loan_id": loan_id,
                "fee_amount": fee_amount,
                "loan_amount": loan_amount,
                "fee_rate": fee_rate,
                "year": origination_year,
            })

            logger.debug(
                "Origination fee calculated",
                loan_id=loan_id,
                fee_amount=fee_amount,
                loan_amount=loan_amount,
                fee_rate=fee_rate,
                year=origination_year,
            )

        logger.info(
            "Origination fees calculated",
            total_fees=sum(fee.get("fee_amount", 0) for fee in self.origination_fees),
            num_loans=len(self.origination_fees),
        )

    def calculate_fund_expenses(self) -> None:
        """
        Calculate fund expenses for each year.

        This includes:
        - Fixed annual expenses
        - Variable expenses based on fund size
        """
        logger.info("Calculating fund expenses")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="fee_engine",
            progress=50.0,
            message="Calculating fund expenses",
        )

        # Get expense parameters
        annual_fund_expenses_rate = getattr(self.fee_config, "annual_fund_expenses", 0.005)
        fixed_annual_expenses = getattr(self.fee_config, "fixed_annual_expenses", 100000)
        expense_growth_rate = getattr(self.fee_config, "expense_growth_rate", 0.02)
        fund_size = self.config.fund_size
        fund_term = self.config.fund_term

        # Calculate expenses for each year
        for year in range(fund_term + 1):
            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return

            # Calculate variable expenses (as percentage of fund size)
            variable_expense = fund_size * annual_fund_expenses_rate * (1 + expense_growth_rate) ** year

            # Calculate fixed expenses with growth
            fixed_expense = fixed_annual_expenses * (1 + expense_growth_rate) ** year

            # Add to fund expenses list
            self.fund_expenses.append({
                "year": year,
                "expense_amount": variable_expense,
                "expense_type": "variable",
            })

            self.fund_expenses.append({
                "year": year,
                "expense_amount": fixed_expense,
                "expense_type": "fixed",
            })

            logger.debug(
                "Fund expenses calculated",
                year=year,
                variable_expense=variable_expense,
                fixed_expense=fixed_expense,
            )

        logger.info(
            "Fund expenses calculated",
            total_expenses=sum(expense.get("expense_amount", 0) for expense in self.fund_expenses),
            num_years=fund_term + 1,
        )

    def calculate_acquisition_fees(self) -> None:
        """
        Calculate acquisition fees for each loan.
        """
        logger.info("Calculating acquisition fees")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="fee_engine",
            progress=70.0,
            message="Calculating acquisition fees",
        )

        # Get acquisition fee rate
        fee_rate = getattr(self.fee_config, "acquisition_fee_rate", 0.0)

        # Skip if fee rate is zero
        if fee_rate == 0:
            logger.info("Acquisition fees skipped (rate is zero)")
            return

        # Calculate acquisition fees for each loan
        for loan in self.context.loans:
            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return

            loan_id = loan.get("loan_id")
            property_value = loan.get("property_value", 0)
            origination_year = loan.get("origination_year", 0)

            # Calculate fee amount
            fee_amount = property_value * fee_rate

            # Add to acquisition fees list
            self.acquisition_fees.append({
                "loan_id": loan_id,
                "fee_amount": fee_amount,
                "property_value": property_value,
                "fee_rate": fee_rate,
                "year": origination_year,
            })

            logger.debug(
                "Acquisition fee calculated",
                loan_id=loan_id,
                fee_amount=fee_amount,
                property_value=property_value,
                fee_rate=fee_rate,
                year=origination_year,
            )

        logger.info(
            "Acquisition fees calculated",
            total_fees=sum(fee.get("fee_amount", 0) for fee in self.acquisition_fees),
            num_loans=len(self.acquisition_fees),
        )

    def calculate_disposition_fees(self) -> None:
        """
        Calculate disposition fees for each loan exit.
        """
        logger.info("Calculating disposition fees")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="fee_engine",
            progress=80.0,
            message="Calculating disposition fees",
        )

        # Get disposition fee rate
        fee_rate = getattr(self.fee_config, "disposition_fee_rate", 0.0)

        # Skip if fee rate is zero
        if fee_rate == 0:
            logger.info("Disposition fees skipped (rate is zero)")
            return

        # Calculate disposition fees for each exit
        for loan_id, exit_info in self.context.exits.items():
            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return

            exit_value = exit_info.get("exit_value", 0)
            exit_year = exit_info.get("exit_year", 0)

            # Calculate fee amount
            fee_amount = exit_value * fee_rate

            # Add to disposition fees list
            self.disposition_fees.append({
                "loan_id": loan_id,
                "fee_amount": fee_amount,
                "exit_value": exit_value,
                "fee_rate": fee_rate,
                "year": exit_year,
            })

            logger.debug(
                "Disposition fee calculated",
                loan_id=loan_id,
                fee_amount=fee_amount,
                exit_value=exit_value,
                fee_rate=fee_rate,
                year=exit_year,
            )

        logger.info(
            "Disposition fees calculated",
            total_fees=sum(fee.get("fee_amount", 0) for fee in self.disposition_fees),
            num_exits=len(self.disposition_fees),
        )

    def calculate_total_fees(self) -> Dict[str, float]:
        """
        Calculate total fees by category.

        Returns:
            Dictionary of total fees by category
        """
        logger.info("Calculating total fees")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="fee_engine",
            progress=85.0,
            message="Calculating total fees",
        )

        # Calculate total fees by category
        total_management_fees = sum(fee.get("fee_amount", 0) for fee in self.management_fees)
        total_origination_fees = sum(fee.get("fee_amount", 0) for fee in self.origination_fees)
        total_fund_expenses = sum(expense.get("expense_amount", 0) for expense in self.fund_expenses)
        total_acquisition_fees = sum(fee.get("fee_amount", 0) for fee in self.acquisition_fees)
        total_disposition_fees = sum(fee.get("fee_amount", 0) for fee in self.disposition_fees)

        # Calculate grand total
        total = (
            total_management_fees
            + total_origination_fees
            + total_fund_expenses
            + total_acquisition_fees
            + total_disposition_fees
            + self.setup_costs
        )

        # Create total fees dictionary
        total_fees = {
            "management_fees": total_management_fees,
            "origination_fees": total_origination_fees,
            "fund_expenses": total_fund_expenses,
            "acquisition_fees": total_acquisition_fees,
            "disposition_fees": total_disposition_fees,
            "setup_costs": self.setup_costs,
            "total": total,
        }

        logger.info(
            "Total fees calculated",
            total_fees=total,
            management_fees=total_management_fees,
            origination_fees=total_origination_fees,
            fund_expenses=total_fund_expenses,
            acquisition_fees=total_acquisition_fees,
            disposition_fees=total_disposition_fees,
            setup_costs=self.setup_costs,
        )

        return total_fees

    def calculate_fee_impact(self) -> Dict[str, float]:
        """
        Calculate the impact of fees on fund performance.

        Returns:
            Dictionary of fee impact metrics
        """
        logger.info("Calculating fee impact")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="fee_engine",
            progress=90.0,
            message="Calculating fee impact",
        )

        # Get total fees
        total_fees = self.calculate_total_fees()

        # Get fund metrics
        irr = self.context.metrics.get("irr", 0)
        equity_multiple = self.context.metrics.get("equity_multiple", 0)

        # Calculate gross metrics (simplified approximation)
        # In a real implementation, we would recalculate IRR and equity multiple
        # based on cash flows without fees
        fund_size = self.config.fund_size
        fee_impact_factor = total_fees["total"] / fund_size

        gross_irr = irr + irr * fee_impact_factor * 0.5  # Simplified approximation
        gross_equity_multiple = equity_multiple + fee_impact_factor

        # Calculate impact
        irr_impact = gross_irr - irr
        equity_multiple_impact = gross_equity_multiple - equity_multiple

        # Create fee impact dictionary
        fee_impact = {
            "gross_irr": gross_irr,
            "net_irr": irr,
            "irr_impact": irr_impact,
            "gross_equity_multiple": gross_equity_multiple,
            "net_equity_multiple": equity_multiple,
            "equity_multiple_impact": equity_multiple_impact,
        }

        logger.info(
            "Fee impact calculated",
            gross_irr=gross_irr,
            net_irr=irr,
            irr_impact=irr_impact,
            gross_equity_multiple=gross_equity_multiple,
            net_equity_multiple=equity_multiple,
            equity_multiple_impact=equity_multiple_impact,
        )

        return fee_impact

    def generate_visualization_data(self) -> None:
        """
        Generate visualization data for fees.
        """
        logger.info("Generating fee visualization data")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="fee_engine",
            progress=95.0,
            message="Generating fee visualization data",
        )

        # Get total fees
        total_fees = self.calculate_total_fees()

        # Generate fee breakdown chart
        self.fee_breakdown_chart = []
        for category, amount in total_fees.items():
            if category != "total" and amount > 0:
                percentage = amount / total_fees["total"] if total_fees["total"] > 0 else 0
                self.fee_breakdown_chart.append({
                    "category": category.replace("_", " ").title(),
                    "amount": amount,
                    "percentage": percentage,
                })

        # Generate fees by year chart
        fund_term = self.config.fund_term
        self.fees_by_year_chart = []

        for year in range(fund_term + 1):
            # Get fees for this year
            management_fees = sum(fee.get("fee_amount", 0) for fee in self.management_fees if fee.get("year") == year)
            origination_fees = sum(fee.get("fee_amount", 0) for fee in self.origination_fees if fee.get("year") == year)
            fund_expenses = sum(expense.get("expense_amount", 0) for expense in self.fund_expenses if expense.get("year") == year)
            acquisition_fees = sum(fee.get("fee_amount", 0) for fee in self.acquisition_fees if fee.get("year") == year)
            disposition_fees = sum(fee.get("fee_amount", 0) for fee in self.disposition_fees if fee.get("year") == year)

            # Add setup costs to year 0
            setup_costs = self.setup_costs if year == 0 else 0

            # Calculate total for this year
            total = (
                management_fees
                + origination_fees
                + fund_expenses
                + acquisition_fees
                + disposition_fees
                + setup_costs
            )

            # Add to chart data
            self.fees_by_year_chart.append({
                "year": year,
                "management_fees": management_fees,
                "origination_fees": origination_fees,
                "fund_expenses": fund_expenses,
                "acquisition_fees": acquisition_fees,
                "disposition_fees": disposition_fees,
                "setup_costs": setup_costs,
                "total": total,
            })

        # Generate fee impact chart
        fee_impact = self.calculate_fee_impact()
        self.fee_impact_chart = [
            {
                "metric": "IRR",
                "gross": fee_impact["gross_irr"],
                "net": fee_impact["net_irr"],
                "impact": fee_impact["irr_impact"],
            },
            {
                "metric": "Equity Multiple",
                "gross": fee_impact["gross_equity_multiple"],
                "net": fee_impact["net_equity_multiple"],
                "impact": fee_impact["equity_multiple_impact"],
            },
        ]

        # Generate fee table (same as fees_by_year_chart but formatted for table display)
        self.fee_table = self.fees_by_year_chart

        logger.info(
            "Fee visualization data generated",
            fee_breakdown_chart_size=len(self.fee_breakdown_chart),
            fees_by_year_chart_size=len(self.fees_by_year_chart),
            fee_impact_chart_size=len(self.fee_impact_chart),
            fee_table_size=len(self.fee_table),
        )

    def calculate_fees(self) -> Dict[str, Any]:
        """
        Calculate all fees and expenses.

        Returns:
            Dictionary containing fee calculation results
        """
        logger.info("Starting fee calculation")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="fee_engine",
            progress=0.0,
            message="Starting fee calculation",
        )

        try:
            # Calculate management fees
            self.calculate_management_fees()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return {}

            # Calculate origination fees
            self.calculate_origination_fees()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return {}

            # Calculate fund expenses
            self.calculate_fund_expenses()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return {}

            # Calculate acquisition fees
            self.calculate_acquisition_fees()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return {}

            # Calculate disposition fees
            self.calculate_disposition_fees()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return {}

            # Calculate total fees
            total_fees = self.calculate_total_fees()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return {}

            # Calculate fee impact
            fee_impact = self.calculate_fee_impact()

            # Check for cancellation
            if self.websocket_manager.is_cancelled(self.context.run_id):
                logger.info("Fee calculation cancelled")
                return {}

            # Generate visualization data
            self.generate_visualization_data()

            # Create results dictionary
            results = {
                "management_fees": self.management_fees,
                "origination_fees": self.origination_fees,
                "fund_expenses": self.fund_expenses,
                "acquisition_fees": self.acquisition_fees,
                "disposition_fees": self.disposition_fees,
                "setup_costs": self.setup_costs,
                "total_fees": total_fees,
                "fee_impact": fee_impact,
                "visualization": {
                    "fee_breakdown_chart": self.fee_breakdown_chart,
                    "fees_by_year_chart": self.fees_by_year_chart,
                    "fee_impact_chart": self.fee_impact_chart,
                    "fee_table": self.fee_table,
                },
            }

            # Send progress update
            self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="fee_engine",
                progress=100.0,
                message="Fee calculation completed",
            )

            # Send intermediate results
            self.websocket_manager.send_message(
                simulation_id=self.context.run_id,
                message_type="intermediate_result",
                data={
                    "module": "fee_engine",
                    "results": results,
                },
            )

            logger.info(
                "Fee calculation completed",
                total_fees=total_fees["total"],
                management_fees=total_fees["management_fees"],
                origination_fees=total_fees["origination_fees"],
                fund_expenses=total_fees["fund_expenses"],
                acquisition_fees=total_fees["acquisition_fees"],
                disposition_fees=total_fees["disposition_fees"],
                setup_costs=total_fees["setup_costs"],
            )

            return results

        except Exception as e:
            logger.error(
                "Error calculating fees",
                error=str(e),
                exc_info=True,
            )

            # Send error message
            self.websocket_manager.send_error(
                simulation_id=self.context.run_id,
                error={
                    "message": f"Error calculating fees: {str(e)}",
                    "module": "fee_engine",
                },
            )

            # Re-raise exception
            raise


async def calculate_fees(context: SimulationContext) -> None:
    """
    Calculate fees and expenses for the fund.

    This function is called by the orchestrator to calculate fees and expenses
    for the fund. It creates a FeeEngine instance and calls the calculate_fees
    method.

    Args:
        context: Simulation context
    """
    logger.info("Starting fee calculation")

    # Create fee engine
    fee_engine = FeeEngine(context)

    # Calculate fees
    results = fee_engine.calculate_fees()

    # Store results in context
    context.fee_results = results

    logger.info("Fee calculation completed")
