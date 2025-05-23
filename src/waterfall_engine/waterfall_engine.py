"""
Waterfall Engine module for the EQU IHOME SIM ENGINE v2.

This module is responsible for calculating the distribution waterfall for fund cashflows,
including hurdle rates, carried interest, catch-up provisions, and multi-tier structures.
It supports both European (whole-fund) and American (deal-by-deal) waterfall structures.
"""

import logging
import math
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime
from enum import Enum
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

    def is_cancelled(self, simulation_id: str) -> bool:
        """Safe wrapper for is_cancelled (this method is already sync)."""
        return self.websocket_manager.is_cancelled(simulation_id)

# Set up logging
logger = structlog.get_logger(__name__)


class WaterfallTier(Enum):
    """Enum for waterfall distribution tiers."""
    RETURN_OF_CAPITAL = 1
    PREFERRED_RETURN = 2
    CATCH_UP = 3
    CARRIED_INTEREST = 4
    RESIDUAL = 5


class WaterfallStructure(Enum):
    """Enum for waterfall structure types."""
    EUROPEAN = "european"  # Whole-fund waterfall
    AMERICAN = "american"  # Deal-by-deal waterfall


class WaterfallEngine:
    """
    Waterfall Engine for calculating distribution waterfalls.

    This class calculates the distribution waterfall for fund cashflows, including:
    - Return of capital
    - Preferred return (hurdle rate)
    - GP catch-up
    - Carried interest
    - Residual distributions

    It supports both European (whole-fund) and American (deal-by-deal) waterfall structures,
    as well as multi-tier waterfalls with different hurdle rates and carried interest rates.
    """

    def __init__(self, context: SimulationContext):
        """
        Initialize the waterfall engine.

        Args:
            context: Simulation context
        """
        self.context = context
        self.config = context.config
        self.waterfall_config = getattr(self.config, "waterfall_engine", {})

        # Get WebSocket manager and create safe sync wrapper
        websocket_manager = get_websocket_manager()
        self.websocket_manager = SyncWebSocketWrapper(websocket_manager, context.run_id)

        # Get waterfall structure
        self.waterfall_structure = WaterfallStructure(getattr(self.config, "waterfall_structure", "european"))

        # Get hurdle rate
        self.hurdle_rate = getattr(self.config, "hurdle_rate", 0.08)

        # Get carried interest rate
        self.carried_interest_rate = getattr(self.config, "carried_interest_rate", 0.20)

        # Get catch-up rate
        self.catch_up_rate = getattr(self.config, "catch_up_rate", 0.0)

        # Get GP commitment percentage
        self.gp_commitment_percentage = getattr(self.config, "gp_commitment_percentage", 0.0)

        # Get multi-tier waterfall parameters
        self.multi_tier_enabled = getattr(self.waterfall_config, "multi_tier_enabled", False)
        self.tiers = getattr(self.waterfall_config, "tiers", [])

        # Get clawback parameters
        self.enable_clawback = getattr(self.waterfall_config, "enable_clawback", True)
        self.clawback_threshold = getattr(self.waterfall_config, "clawback_threshold", 0.0)

        # Initialize distribution results
        self.distributions: Dict[str, Any] = {}
        self.tier_cashflows: Dict[WaterfallTier, List[Dict[str, Any]]] = {
            tier: [] for tier in WaterfallTier
        }
        self.lp_distributions: List[Dict[str, Any]] = []
        self.gp_distributions: List[Dict[str, Any]] = []
        self.clawback_amount: float = 0.0

        # Initialize visualization data
        self.waterfall_chart: List[Dict[str, Any]] = []
        self.distribution_by_year_chart: List[Dict[str, Any]] = []
        self.tier_allocation_chart: List[Dict[str, Any]] = []
        self.stakeholder_allocation_chart: List[Dict[str, Any]] = []

        logger.info(
            "Waterfall engine initialized",
            waterfall_structure=self.waterfall_structure.value,
            hurdle_rate=self.hurdle_rate,
            carried_interest_rate=self.carried_interest_rate,
            catch_up_rate=self.catch_up_rate,
            multi_tier_enabled=self.multi_tier_enabled,
        )

    def run(self) -> Dict[str, Any]:
        """
        Run the waterfall engine.

        Returns:
            Dictionary containing waterfall distribution results
        """
        logger.info("Running waterfall engine")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="waterfall_engine",
            progress=0.0,
            message="Starting waterfall distribution calculation",
        )

        # Check if cashflows are available
        if not hasattr(self.context, "cashflows") or not self.context.cashflows:
            logger.warning("No cashflows found in context")
            self.websocket_manager.send_progress(
                simulation_id=self.context.run_id,
                module="waterfall_engine",
                progress=100.0,
                message="No cashflows found to process",
            )
            return {}

        # Calculate waterfall distributions
        if self.waterfall_structure == WaterfallStructure.EUROPEAN:
            self.calculate_european_waterfall()
        else:
            self.calculate_american_waterfall()

        # Check for clawback
        if self.enable_clawback:
            self.calculate_clawback()

        # Generate visualization data
        self.generate_visualization_data()

        # Create results dictionary
        results = {
            "distributions": self.distributions,
            "tier_cashflows": {tier.name: cashflows for tier, cashflows in self.tier_cashflows.items()},
            "lp_distributions": self.lp_distributions,
            "gp_distributions": self.gp_distributions,
            "clawback_amount": self.clawback_amount,
            "visualization": {
                "waterfall_chart": self.waterfall_chart,
                "distribution_by_year_chart": self.distribution_by_year_chart,
                "tier_allocation_chart": self.tier_allocation_chart,
                "stakeholder_allocation_chart": self.stakeholder_allocation_chart,
            },
        }

        # Store results in context
        self.context.waterfall = results

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="waterfall_engine",
            progress=100.0,
            message="Waterfall distribution calculation completed",
        )

        logger.info("Waterfall engine completed")

        return results

    def calculate_european_waterfall(self):
        """
        Calculate European (whole-fund) waterfall distribution.

        In a European waterfall:
        1. Return all capital to LPs
        2. Pay preferred return to LPs
        3. GP catch-up (if applicable)
        4. Split remaining profits according to carried interest
        """
        logger.info("Calculating European waterfall distribution")

        # Get fund-level cashflows
        fund_cashflows = self.context.cashflows.get("fund_level_cashflows", [])
        if not fund_cashflows:
            logger.warning("No fund-level cashflows found")
            return

        # Get fund size and GP commitment
        fund_size = getattr(self.config, "fund_size", 0.0)
        gp_commitment = fund_size * self.gp_commitment_percentage
        lp_commitment = fund_size - gp_commitment

        # Calculate total fund cashflow
        total_inflows = sum(cf.get("principal_repayments", 0.0) +
                           cf.get("interest_income", 0.0) +
                           cf.get("appreciation_share", 0.0) +
                           cf.get("origination_fees", 0.0)
                           for cf in fund_cashflows)

        total_outflows = sum(cf.get("loan_investments", 0.0) +
                            cf.get("management_fees", 0.0) +
                            cf.get("fund_expenses", 0.0)
                            for cf in fund_cashflows)

        # Calculate net cashflow
        net_cashflow = total_inflows - total_outflows

        # Initialize distribution amounts
        return_of_capital = min(lp_commitment, net_cashflow)
        remaining_cashflow = net_cashflow - return_of_capital

        # Calculate preferred return
        fund_term = getattr(self.config, "fund_term", 10)
        preferred_return = lp_commitment * (math.pow(1 + self.hurdle_rate, fund_term) - 1)
        preferred_return_paid = min(preferred_return, remaining_cashflow)
        remaining_cashflow -= preferred_return_paid

        # Calculate catch-up (if applicable)
        catch_up_amount = 0.0
        if self.catch_up_rate > 0 and remaining_cashflow > 0:
            # Calculate total profit
            total_profit = net_cashflow - return_of_capital

            # Calculate catch-up amount
            target_gp_profit = total_profit * self.carried_interest_rate
            current_gp_profit = 0  # GP hasn't received any profit yet
            catch_up_amount = min(remaining_cashflow,
                                 (target_gp_profit - current_gp_profit) / self.catch_up_rate)
            remaining_cashflow -= catch_up_amount

        # Calculate carried interest
        carried_interest = remaining_cashflow * self.carried_interest_rate
        residual_to_lp = remaining_cashflow - carried_interest

        # Store tier cashflows
        self.tier_cashflows[WaterfallTier.RETURN_OF_CAPITAL].append({
            "amount": return_of_capital,
            "description": "Return of LP capital"
        })

        self.tier_cashflows[WaterfallTier.PREFERRED_RETURN].append({
            "amount": preferred_return_paid,
            "description": f"Preferred return at {self.hurdle_rate:.1%}"
        })

        if catch_up_amount > 0:
            self.tier_cashflows[WaterfallTier.CATCH_UP].append({
                "amount": catch_up_amount,
                "description": f"GP catch-up at {self.catch_up_rate:.1%}"
            })

        self.tier_cashflows[WaterfallTier.CARRIED_INTEREST].append({
            "amount": carried_interest,
            "description": f"Carried interest at {self.carried_interest_rate:.1%}"
        })

        self.tier_cashflows[WaterfallTier.RESIDUAL].append({
            "amount": residual_to_lp,
            "description": "Residual to LP"
        })

        # Calculate total distributions to LP and GP
        total_to_lp = return_of_capital + preferred_return_paid + residual_to_lp
        total_to_gp = catch_up_amount + carried_interest

        # Store distributions
        self.distributions = {
            "return_of_capital": return_of_capital,
            "preferred_return": preferred_return_paid,
            "catch_up": catch_up_amount,
            "carried_interest": carried_interest,
            "residual_to_lp": residual_to_lp,
            "total_to_lp": total_to_lp,
            "total_to_gp": total_to_gp,
            "total_distributed": total_to_lp + total_to_gp,
        }

        # Create LP and GP distribution records
        # For simplicity, we'll assume all distributions happen at the end of the fund term
        distribution_year = getattr(self.config, "vintage_year", 2023) + fund_term

        self.lp_distributions.append({
            "year": distribution_year,
            "return_of_capital": return_of_capital,
            "preferred_return": preferred_return_paid,
            "residual": residual_to_lp,
            "total": total_to_lp,
        })

        self.gp_distributions.append({
            "year": distribution_year,
            "catch_up": catch_up_amount,
            "carried_interest": carried_interest,
            "total": total_to_gp,
        })

        logger.info(
            "European waterfall calculated",
            return_of_capital=return_of_capital,
            preferred_return=preferred_return_paid,
            catch_up=catch_up_amount,
            carried_interest=carried_interest,
            residual_to_lp=residual_to_lp,
            total_to_lp=total_to_lp,
            total_to_gp=total_to_gp,
        )

    def calculate_american_waterfall(self):
        """
        Calculate American (deal-by-deal) waterfall distribution.

        In an American waterfall:
        1. Return capital for each deal
        2. Pay preferred return for each deal
        3. GP catch-up for each deal (if applicable)
        4. Split remaining profits according to carried interest for each deal
        """
        logger.info("Calculating American waterfall distribution")

        # Get loan-level cashflows
        loan_cashflows = self.context.cashflows.get("loan_level_cashflows", [])
        if not loan_cashflows:
            logger.warning("No loan-level cashflows found")
            return

        # Get fund size and GP commitment
        fund_size = getattr(self.config, "fund_size", 0.0)
        gp_commitment = fund_size * self.gp_commitment_percentage
        lp_commitment = fund_size - gp_commitment

        # Initialize distribution totals
        total_return_of_capital = 0.0
        total_preferred_return = 0.0
        total_catch_up = 0.0
        total_carried_interest = 0.0
        total_residual_to_lp = 0.0

        # Process each loan as a separate "deal"
        for loan in loan_cashflows:
            loan_id = loan.get("loan_id", "unknown")

            # Get loan origination and exit cashflows
            origination = loan.get("origination", {})
            exit_cf = loan.get("exit", {})

            # Calculate loan-level cashflows
            loan_investment = origination.get("loan_amount", 0.0)
            if loan_investment >= 0:  # Loan amount should be negative (outflow)
                loan_investment = -loan_investment

            origination_fee = origination.get("origination_fee", 0.0)
            principal_repayment = exit_cf.get("principal", 0.0)
            interest_income = exit_cf.get("accrued_interest", 0.0)
            appreciation_share = exit_cf.get("appreciation_share", 0.0)

            # Calculate net cashflow for this loan
            loan_inflows = principal_repayment + interest_income + appreciation_share + origination_fee
            loan_outflows = abs(loan_investment)
            loan_net_cashflow = loan_inflows - loan_outflows

            # Skip if loan has negative or zero net cashflow
            if loan_net_cashflow <= 0:
                continue

            # Calculate loan term in years
            origination_year = origination.get("year", 0)
            origination_month = origination.get("month", 0)
            exit_year = exit_cf.get("year", 0)
            exit_month = exit_cf.get("month", 0)

            loan_term_years = (exit_year - origination_year) + (exit_month - origination_month) / 12.0
            if loan_term_years <= 0:
                loan_term_years = 0.1  # Minimum term to avoid division by zero

            # Calculate return of capital
            return_of_capital = min(loan_outflows, loan_net_cashflow)
            remaining_cashflow = loan_net_cashflow - return_of_capital

            # Calculate preferred return
            preferred_return = loan_outflows * (math.pow(1 + self.hurdle_rate, loan_term_years) - 1)
            preferred_return_paid = min(preferred_return, remaining_cashflow)
            remaining_cashflow -= preferred_return_paid

            # Calculate catch-up (if applicable)
            catch_up_amount = 0.0
            if self.catch_up_rate > 0 and remaining_cashflow > 0:
                # Calculate total profit for this loan
                loan_profit = loan_net_cashflow - return_of_capital

                # Calculate catch-up amount
                target_gp_profit = loan_profit * self.carried_interest_rate
                current_gp_profit = 0  # GP hasn't received any profit yet
                catch_up_amount = min(remaining_cashflow,
                                     (target_gp_profit - current_gp_profit) / self.catch_up_rate)
                remaining_cashflow -= catch_up_amount

            # Calculate carried interest
            carried_interest = remaining_cashflow * self.carried_interest_rate
            residual_to_lp = remaining_cashflow - carried_interest

            # Add to tier cashflows
            self.tier_cashflows[WaterfallTier.RETURN_OF_CAPITAL].append({
                "loan_id": loan_id,
                "amount": return_of_capital,
                "description": f"Return of capital for loan {loan_id}"
            })

            self.tier_cashflows[WaterfallTier.PREFERRED_RETURN].append({
                "loan_id": loan_id,
                "amount": preferred_return_paid,
                "description": f"Preferred return for loan {loan_id} at {self.hurdle_rate:.1%}"
            })

            if catch_up_amount > 0:
                self.tier_cashflows[WaterfallTier.CATCH_UP].append({
                    "loan_id": loan_id,
                    "amount": catch_up_amount,
                    "description": f"GP catch-up for loan {loan_id} at {self.catch_up_rate:.1%}"
                })

            self.tier_cashflows[WaterfallTier.CARRIED_INTEREST].append({
                "loan_id": loan_id,
                "amount": carried_interest,
                "description": f"Carried interest for loan {loan_id} at {self.carried_interest_rate:.1%}"
            })

            self.tier_cashflows[WaterfallTier.RESIDUAL].append({
                "loan_id": loan_id,
                "amount": residual_to_lp,
                "description": f"Residual to LP for loan {loan_id}"
            })

            # Add to distribution totals
            total_return_of_capital += return_of_capital
            total_preferred_return += preferred_return_paid
            total_catch_up += catch_up_amount
            total_carried_interest += carried_interest
            total_residual_to_lp += residual_to_lp

            # Create LP and GP distribution records for this loan
            self.lp_distributions.append({
                "loan_id": loan_id,
                "year": exit_year,
                "month": exit_month,
                "return_of_capital": return_of_capital,
                "preferred_return": preferred_return_paid,
                "residual": residual_to_lp,
                "total": return_of_capital + preferred_return_paid + residual_to_lp,
            })

            self.gp_distributions.append({
                "loan_id": loan_id,
                "year": exit_year,
                "month": exit_month,
                "catch_up": catch_up_amount,
                "carried_interest": carried_interest,
                "total": catch_up_amount + carried_interest,
            })

        # Calculate total distributions to LP and GP
        total_to_lp = total_return_of_capital + total_preferred_return + total_residual_to_lp
        total_to_gp = total_catch_up + total_carried_interest

        # Store distributions
        self.distributions = {
            "return_of_capital": total_return_of_capital,
            "preferred_return": total_preferred_return,
            "catch_up": total_catch_up,
            "carried_interest": total_carried_interest,
            "residual_to_lp": total_residual_to_lp,
            "total_to_lp": total_to_lp,
            "total_to_gp": total_to_gp,
            "total_distributed": total_to_lp + total_to_gp,
        }

        logger.info(
            "American waterfall calculated",
            return_of_capital=total_return_of_capital,
            preferred_return=total_preferred_return,
            catch_up=total_catch_up,
            carried_interest=total_carried_interest,
            residual_to_lp=total_residual_to_lp,
            total_to_lp=total_to_lp,
            total_to_gp=total_to_gp,
        )

    def calculate_clawback(self):
        """
        Calculate clawback amount if GP has received more carried interest than entitled.

        Clawback is typically calculated at the end of the fund's life to ensure
        that the GP has not received more carried interest than they are entitled to
        based on the fund's overall performance.
        """
        logger.info("Calculating clawback")

        # Get total distributions
        total_to_lp = self.distributions.get("total_to_lp", 0.0)
        total_to_gp = self.distributions.get("total_to_gp", 0.0)
        carried_interest = self.distributions.get("carried_interest", 0.0)

        # Get fund size and GP commitment
        fund_size = getattr(self.config, "fund_size", 0.0)
        gp_commitment = fund_size * self.gp_commitment_percentage
        lp_commitment = fund_size - gp_commitment

        # Calculate total profit
        total_profit = total_to_lp + total_to_gp - lp_commitment

        # Calculate entitled carried interest
        if total_profit <= 0:
            entitled_carried_interest = 0.0
        else:
            # Calculate preferred return
            fund_term = getattr(self.config, "fund_term", 10)
            preferred_return = lp_commitment * (math.pow(1 + self.hurdle_rate, fund_term) - 1)

            # Calculate profit after preferred return
            profit_after_preferred = max(0, total_profit - preferred_return)

            # Calculate entitled carried interest
            entitled_carried_interest = profit_after_preferred * self.carried_interest_rate

        # Calculate clawback amount
        self.clawback_amount = max(0, carried_interest - entitled_carried_interest)

        # Apply clawback threshold
        if self.clawback_amount <= self.clawback_threshold:
            self.clawback_amount = 0.0

        # Adjust distributions if clawback is applied
        if self.clawback_amount > 0:
            # Adjust GP distributions
            self.distributions["carried_interest"] -= self.clawback_amount
            self.distributions["total_to_gp"] -= self.clawback_amount

            # Adjust LP distributions
            self.distributions["residual_to_lp"] += self.clawback_amount
            self.distributions["total_to_lp"] += self.clawback_amount

            logger.info(
                "Clawback applied",
                clawback_amount=self.clawback_amount,
                adjusted_carried_interest=self.distributions["carried_interest"],
                adjusted_total_to_gp=self.distributions["total_to_gp"],
                adjusted_residual_to_lp=self.distributions["residual_to_lp"],
                adjusted_total_to_lp=self.distributions["total_to_lp"],
            )
        else:
            logger.info("No clawback required")

    def generate_visualization_data(self):
        """Generate visualization data for waterfall distributions."""
        logger.info("Generating visualization data")

        # Generate waterfall chart
        self.generate_waterfall_chart()

        # Generate distribution by year chart
        self.generate_distribution_by_year_chart()

        # Generate tier allocation chart
        self.generate_tier_allocation_chart()

        # Generate stakeholder allocation chart
        self.generate_stakeholder_allocation_chart()

    def generate_waterfall_chart(self):
        """Generate waterfall chart data."""
        # Create waterfall chart data
        self.waterfall_chart = [
            {"category": "Return of Capital", "amount": self.distributions.get("return_of_capital", 0.0)},
            {"category": "Preferred Return", "amount": self.distributions.get("preferred_return", 0.0)},
            {"category": "GP Catch-up", "amount": self.distributions.get("catch_up", 0.0)},
            {"category": "Carried Interest", "amount": self.distributions.get("carried_interest", 0.0)},
            {"category": "Residual to LP", "amount": self.distributions.get("residual_to_lp", 0.0)},
        ]

    def generate_distribution_by_year_chart(self):
        """Generate distribution by year chart data."""
        # Create a dictionary to track distributions by year
        distributions_by_year = {}

        # Process LP distributions
        for dist in self.lp_distributions:
            year = dist.get("year", 0)
            if year not in distributions_by_year:
                distributions_by_year[year] = {
                    "year": year,
                    "lp_return_of_capital": 0.0,
                    "lp_preferred_return": 0.0,
                    "lp_residual": 0.0,
                    "gp_catch_up": 0.0,
                    "gp_carried_interest": 0.0,
                }

            distributions_by_year[year]["lp_return_of_capital"] += dist.get("return_of_capital", 0.0)
            distributions_by_year[year]["lp_preferred_return"] += dist.get("preferred_return", 0.0)
            distributions_by_year[year]["lp_residual"] += dist.get("residual", 0.0)

        # Process GP distributions
        for dist in self.gp_distributions:
            year = dist.get("year", 0)
            if year not in distributions_by_year:
                distributions_by_year[year] = {
                    "year": year,
                    "lp_return_of_capital": 0.0,
                    "lp_preferred_return": 0.0,
                    "lp_residual": 0.0,
                    "gp_catch_up": 0.0,
                    "gp_carried_interest": 0.0,
                }

            distributions_by_year[year]["gp_catch_up"] += dist.get("catch_up", 0.0)
            distributions_by_year[year]["gp_carried_interest"] += dist.get("carried_interest", 0.0)

        # Convert to list and sort by year
        self.distribution_by_year_chart = sorted(
            [
                {
                    "year": year,
                    "lp_return_of_capital": data["lp_return_of_capital"],
                    "lp_preferred_return": data["lp_preferred_return"],
                    "lp_residual": data["lp_residual"],
                    "gp_catch_up": data["gp_catch_up"],
                    "gp_carried_interest": data["gp_carried_interest"],
                    "total": (
                        data["lp_return_of_capital"] +
                        data["lp_preferred_return"] +
                        data["lp_residual"] +
                        data["gp_catch_up"] +
                        data["gp_carried_interest"]
                    ),
                }
                for year, data in distributions_by_year.items()
            ],
            key=lambda x: x["year"]
        )

    def generate_tier_allocation_chart(self):
        """Generate tier allocation chart data."""
        # Calculate total amount distributed
        total_distributed = self.distributions.get("total_distributed", 0.0)
        if total_distributed == 0:
            return

        # Calculate amount for each tier
        return_of_capital = self.distributions.get("return_of_capital", 0.0)
        preferred_return = self.distributions.get("preferred_return", 0.0)
        catch_up = self.distributions.get("catch_up", 0.0)
        carried_interest = self.distributions.get("carried_interest", 0.0)
        residual_to_lp = self.distributions.get("residual_to_lp", 0.0)

        # Create tier allocation chart data
        self.tier_allocation_chart = [
            {
                "tier": "Return of Capital",
                "amount": return_of_capital,
                "percentage": return_of_capital / total_distributed if total_distributed > 0 else 0.0,
            },
            {
                "tier": "Preferred Return",
                "amount": preferred_return,
                "percentage": preferred_return / total_distributed if total_distributed > 0 else 0.0,
            },
            {
                "tier": "GP Catch-up",
                "amount": catch_up,
                "percentage": catch_up / total_distributed if total_distributed > 0 else 0.0,
            },
            {
                "tier": "Carried Interest",
                "amount": carried_interest,
                "percentage": carried_interest / total_distributed if total_distributed > 0 else 0.0,
            },
            {
                "tier": "Residual to LP",
                "amount": residual_to_lp,
                "percentage": residual_to_lp / total_distributed if total_distributed > 0 else 0.0,
            },
        ]

    def generate_stakeholder_allocation_chart(self):
        """Generate stakeholder allocation chart data."""
        # Get total distributions to LP and GP
        total_to_lp = self.distributions.get("total_to_lp", 0.0)
        total_to_gp = self.distributions.get("total_to_gp", 0.0)
        total_distributed = total_to_lp + total_to_gp

        # Create stakeholder allocation chart data
        self.stakeholder_allocation_chart = [
            {
                "stakeholder": "Limited Partners",
                "amount": total_to_lp,
                "percentage": total_to_lp / total_distributed if total_distributed > 0 else 0.0,
            },
            {
                "stakeholder": "General Partner",
                "amount": total_to_gp,
                "percentage": total_to_gp / total_distributed if total_distributed > 0 else 0.0,
            },
        ]
