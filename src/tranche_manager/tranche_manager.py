"""
Tranche Manager module for the EQU IHOME SIM ENGINE v2.

This module is responsible for managing tranches in the fund, including:
- Tranche definition and configuration
- Cash flow allocation by tranche
- Tranche-specific metrics calculation
- Tranche waterfall rules
- Coverage tests (overcollateralization, interest coverage)
- Reserve account management
"""

import logging
import math
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime
from enum import Enum
import numpy as np
import structlog
from collections import defaultdict

from src.engine.simulation_context import SimulationContext
from src.api.websocket_manager import get_websocket_manager

# Set up logging
logger = structlog.get_logger(__name__)


class TrancheType(Enum):
    """Enum for tranche types."""
    SENIOR_DEBT = "senior_debt"
    MEZZANINE = "mezzanine"
    PREFERRED_EQUITY = "preferred_equity"
    EQUITY = "equity"


class PaymentFrequency(Enum):
    """Enum for payment frequencies."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUAL = "semi_annual"
    ANNUAL = "annual"


class AmortizationSchedule(Enum):
    """Enum for amortization schedules."""
    STRAIGHT_LINE = "straight_line"
    INTEREST_ONLY = "interest_only"
    BALLOON = "balloon"


class TestType(Enum):
    """Enum for coverage test types."""
    OVERCOLLATERALIZATION = "overcollateralization"
    INTEREST_COVERAGE = "interest_coverage"


class Tranche:
    """
    Class representing a tranche in the fund.

    A tranche is a portion of the fund with specific characteristics, such as
    priority, interest rate, and payment terms.
    """

    def __init__(
        self,
        name: str,
        size: float,
        priority: int,
        tranche_type: TrancheType,
        interest_rate: Optional[float] = None,
        target_return: Optional[float] = None,
        payment_frequency: PaymentFrequency = PaymentFrequency.QUARTERLY,
        amortization: bool = False,
        amortization_schedule: AmortizationSchedule = AmortizationSchedule.INTEREST_ONLY,
        term_years: Optional[float] = None,
        waterfall_rules: Optional[Dict[str, Any]] = None,
        allocation_rules: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a tranche.

        Args:
            name: Tranche name
            size: Tranche size in dollars
            priority: Payment priority (lower numbers get paid first)
            tranche_type: Tranche type
            interest_rate: Interest rate for debt tranches (0-1)
            target_return: Target return for the tranche (0-1)
            payment_frequency: Payment frequency for the tranche
            amortization: Whether the tranche amortizes
            amortization_schedule: Amortization schedule type
            term_years: Term in years
            waterfall_rules: Waterfall rules for the tranche
            allocation_rules: Allocation rules for the tranche
        """
        self.name = name
        self.size = size
        self.priority = priority
        self.tranche_type = tranche_type
        self.interest_rate = interest_rate
        self.target_return = target_return
        self.payment_frequency = payment_frequency
        self.amortization = amortization
        self.amortization_schedule = amortization_schedule
        self.term_years = term_years
        self.waterfall_rules = waterfall_rules or {}
        self.allocation_rules = allocation_rules or {}

        # Initialize tracking variables
        self.remaining_principal = size
        self.accrued_interest = 0.0
        self.total_payments = 0.0
        self.principal_payments = 0.0
        self.interest_payments = 0.0
        self.profit_share_payments = 0.0
        self.shortfall = 0.0
        self.status = "active"

        # Initialize cashflow tracking
        self.cashflows = []

        # Initialize loan allocations
        self.loan_allocations = []

        # Initialize metrics
        self.irr = None
        self.moic = None
        self.actual_return = None

        logger.info(
            "Tranche initialized",
            name=name,
            size=size,
            priority=priority,
            tranche_type=tranche_type.value,
            interest_rate=interest_rate,
            target_return=target_return,
        )

    def allocate_loan(
        self,
        loan_id: str,
        allocation_percentage: float,
        allocation_amount: float,
        zone: str,
        ltv: float,
    ) -> None:
        """
        Allocate a loan to this tranche.

        Args:
            loan_id: Loan ID
            allocation_percentage: Percentage of the loan allocated to this tranche
            allocation_amount: Amount of the loan allocated to this tranche
            zone: Zone of the loan
            ltv: LTV of the loan
        """
        self.loan_allocations.append({
            "loan_id": loan_id,
            "allocation_percentage": allocation_percentage,
            "allocation_amount": allocation_amount,
            "zone": zone,
            "ltv": ltv,
        })

        logger.debug(
            "Loan allocated to tranche",
            tranche=self.name,
            loan_id=loan_id,
            allocation_percentage=allocation_percentage,
            allocation_amount=allocation_amount,
        )

    def record_payment(
        self,
        year: float,
        month: int,
        quarter: Optional[int] = None,
        principal_payment: float = 0.0,
        interest_payment: float = 0.0,
        profit_share_payment: float = 0.0,
    ) -> None:
        """
        Record a payment to this tranche.

        Args:
            year: Year
            month: Month
            quarter: Quarter (if applicable)
            principal_payment: Principal payment
            interest_payment: Interest payment
            profit_share_payment: Profit share payment
        """
        total_payment = principal_payment + interest_payment + profit_share_payment

        # Update tracking variables
        self.remaining_principal -= principal_payment
        self.total_payments += total_payment
        self.principal_payments += principal_payment
        self.interest_payments += interest_payment
        self.profit_share_payments += profit_share_payment

        # Record cashflow
        self.cashflows.append({
            "year": year,
            "month": month,
            "quarter": quarter,
            "principal_payment": principal_payment,
            "interest_payment": interest_payment,
            "profit_share_payment": profit_share_payment,
            "total_payment": total_payment,
            "remaining_principal": self.remaining_principal,
        })

        logger.debug(
            "Payment recorded for tranche",
            tranche=self.name,
            year=year,
            month=month,
            principal_payment=principal_payment,
            interest_payment=interest_payment,
            profit_share_payment=profit_share_payment,
            total_payment=total_payment,
            remaining_principal=self.remaining_principal,
        )

        # Update status if fully paid
        if self.remaining_principal <= 0 and self.tranche_type in [
            TrancheType.SENIOR_DEBT, TrancheType.MEZZANINE
        ]:
            self.status = "paid"
            logger.info(
                "Tranche fully paid",
                tranche=self.name,
                total_payments=self.total_payments,
            )

    def calculate_metrics(self) -> None:
        """Calculate performance metrics for this tranche."""
        # Calculate MOIC
        if self.size > 0:
            self.moic = self.total_payments / self.size
        else:
            self.moic = 0.0

        # Calculate actual return
        if self.tranche_type in [TrancheType.SENIOR_DEBT, TrancheType.MEZZANINE]:
            self.actual_return = self.interest_rate
        else:
            # For equity tranches, calculate annualized return
            # This is a simplified calculation; IRR would be more accurate
            if self.size > 0 and self.term_years and self.term_years > 0:
                self.actual_return = ((self.total_payments / self.size) ** (1 / self.term_years)) - 1
            else:
                self.actual_return = 0.0

        # Calculate IRR (simplified)
        # In a real implementation, this would use a proper IRR calculation
        self.irr = self.actual_return

        logger.info(
            "Tranche metrics calculated",
            tranche=self.name,
            moic=self.moic,
            actual_return=self.actual_return,
            irr=self.irr,
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert tranche to dictionary.

        Returns:
            Dictionary representation of the tranche
        """
        return {
            "name": self.name,
            "type": self.tranche_type.value,
            "size": self.size,
            "priority": self.priority,
            "interest_rate": self.interest_rate,
            "target_return": self.target_return,
            "actual_return": self.actual_return,
            "irr": self.irr,
            "moic": self.moic,
            "total_payments": self.total_payments,
            "principal_payments": self.principal_payments,
            "interest_payments": self.interest_payments,
            "profit_share_payments": self.profit_share_payments,
            "shortfall": self.shortfall,
            "status": self.status,
        }


class TrancheManager:
    """
    Tranche Manager for managing tranches in the fund.

    This class is responsible for:
    - Tranche definition and configuration
    - Cash flow allocation by tranche
    - Tranche-specific metrics calculation
    - Tranche waterfall rules
    - Coverage tests (overcollateralization, interest coverage)
    - Reserve account management
    """

    def __init__(self, context: SimulationContext):
        """
        Initialize the tranche manager.

        Args:
            context: Simulation context
        """
        self.context = context
        self.config = context.config
        self.tranche_config = getattr(self.config, "tranche_manager", {})

        # Get WebSocket manager
        self.websocket_manager = get_websocket_manager()

        # Check if tranche management is enabled
        self.enabled = getattr(self.tranche_config, "enabled", False)
        if not self.enabled:
            logger.info("Tranche management disabled")
            return

        # Initialize tranches
        self.tranches: List[Tranche] = []
        self._initialize_tranches()

        # Initialize reserve account
        self.reserve_account = {
            "enabled": getattr(self.tranche_config.get("reserve_account", {}), "enabled", False),
            "target_percentage": getattr(self.tranche_config.get("reserve_account", {}), "target_percentage", 0.05),
            "initial_funding": getattr(self.tranche_config.get("reserve_account", {}), "initial_funding", 0.03),
            "replenishment_rate": getattr(self.tranche_config.get("reserve_account", {}), "replenishment_rate", 0.01),
            "balance": 0.0,
            "target_balance": 0.0,
            "history": [],
        }

        # Initialize coverage tests
        self.overcollateralization_test = {
            "enabled": getattr(self.tranche_config.get("overcollateralization_test", {}), "enabled", False),
            "threshold": getattr(self.tranche_config.get("overcollateralization_test", {}), "threshold", 1.2),
            "test_frequency": getattr(self.tranche_config.get("overcollateralization_test", {}), "test_frequency", "quarterly"),
            "cure_period_months": getattr(self.tranche_config.get("overcollateralization_test", {}), "cure_period_months", 3),
            "results": [],
        }

        self.interest_coverage_test = {
            "enabled": getattr(self.tranche_config.get("interest_coverage_test", {}), "enabled", False),
            "threshold": getattr(self.tranche_config.get("interest_coverage_test", {}), "threshold", 1.5),
            "test_frequency": getattr(self.tranche_config.get("interest_coverage_test", {}), "test_frequency", "quarterly"),
            "cure_period_months": getattr(self.tranche_config.get("interest_coverage_test", {}), "cure_period_months", 3),
            "results": [],
        }

        # Initialize visualization data
        self.visualization = {
            "tranche_waterfall_chart": [],
            "tranche_cashflow_chart": {},
            "tranche_allocation_chart": [],
            "tranche_performance_chart": [],
            "coverage_test_chart": {},
            "reserve_account_chart": [],
        }

        logger.info(
            "Tranche manager initialized",
            num_tranches=len(self.tranches),
            reserve_account_enabled=self.reserve_account["enabled"],
            oc_test_enabled=self.overcollateralization_test["enabled"],
            ic_test_enabled=self.interest_coverage_test["enabled"],
        )

    def _initialize_tranches(self) -> None:
        """Initialize tranches from configuration."""
        tranche_configs = getattr(self.tranche_config, "tranches", [])
        if not tranche_configs:
            logger.warning("No tranches defined in configuration")
            return

        for tranche_config in tranche_configs:
            name = tranche_config.get("name")
            size = tranche_config.get("size")
            priority = tranche_config.get("priority")
            tranche_type_str = tranche_config.get("type")

            if not all([name, size, priority, tranche_type_str]):
                logger.warning(
                    "Skipping tranche with missing required fields",
                    name=name,
                    size=size,
                    priority=priority,
                    tranche_type=tranche_type_str,
                )
                continue

            try:
                tranche_type = TrancheType(tranche_type_str)
            except ValueError:
                logger.warning(
                    "Invalid tranche type",
                    tranche_type=tranche_type_str,
                    valid_types=[t.value for t in TrancheType],
                )
                continue

            # Get optional parameters
            interest_rate = tranche_config.get("interest_rate")
            target_return = tranche_config.get("target_return")
            payment_frequency_str = tranche_config.get("payment_frequency", "quarterly")
            amortization = tranche_config.get("amortization", False)
            amortization_schedule_str = tranche_config.get("amortization_schedule", "interest_only")
            term_years = tranche_config.get("term_years")
            waterfall_rules = tranche_config.get("waterfall_rules", {})
            allocation_rules = tranche_config.get("allocation_rules", {})

            try:
                payment_frequency = PaymentFrequency(payment_frequency_str)
            except ValueError:
                logger.warning(
                    "Invalid payment frequency, using quarterly",
                    payment_frequency=payment_frequency_str,
                    valid_frequencies=[f.value for f in PaymentFrequency],
                )
                payment_frequency = PaymentFrequency.QUARTERLY

            try:
                amortization_schedule = AmortizationSchedule(amortization_schedule_str)
            except ValueError:
                logger.warning(
                    "Invalid amortization schedule, using interest-only",
                    amortization_schedule=amortization_schedule_str,
                    valid_schedules=[s.value for s in AmortizationSchedule],
                )
                amortization_schedule = AmortizationSchedule.INTEREST_ONLY

            # Create tranche
            tranche = Tranche(
                name=name,
                size=size,
                priority=priority,
                tranche_type=tranche_type,
                interest_rate=interest_rate,
                target_return=target_return,
                payment_frequency=payment_frequency,
                amortization=amortization,
                amortization_schedule=amortization_schedule,
                term_years=term_years,
                waterfall_rules=waterfall_rules,
                allocation_rules=allocation_rules,
            )

            self.tranches.append(tranche)

        # Sort tranches by priority
        self.tranches.sort(key=lambda t: t.priority)

        logger.info(
            "Tranches initialized",
            num_tranches=len(self.tranches),
            tranches=[t.name for t in self.tranches],
        )

        # Initialize reserve account target balance
        if self.reserve_account["enabled"]:
            senior_debt_size = sum(t.size for t in self.tranches if t.tranche_type == TrancheType.SENIOR_DEBT)
            self.reserve_account["target_balance"] = senior_debt_size * self.reserve_account["target_percentage"]
            self.reserve_account["balance"] = senior_debt_size * self.reserve_account["initial_funding"]

            logger.info(
                "Reserve account initialized",
                target_balance=self.reserve_account["target_balance"],
                initial_balance=self.reserve_account["balance"],
            )

    def allocate_loans(self, loans: List[Dict[str, Any]]) -> None:
        """
        Allocate loans to tranches.

        Args:
            loans: List of loans to allocate
        """
        if not self.enabled or not self.tranches:
            return

        logger.info("Allocating loans to tranches")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="tranche_manager",
            progress=10.0,
            message="Allocating loans to tranches",
        )

        # Group tranches by type
        tranches_by_type = defaultdict(list)
        for tranche in self.tranches:
            tranches_by_type[tranche.tranche_type].append(tranche)

        # Allocate loans based on tranche type and allocation rules
        for loan in loans:
            loan_id = loan.get("loan_id", "unknown")
            loan_amount = loan.get("loan_amount", 0.0)
            zone = loan.get("zone", "unknown")
            ltv = loan.get("ltv", 0.0)

            # Allocate to senior debt first
            remaining_amount = loan_amount
            for tranche_type in [TrancheType.SENIOR_DEBT, TrancheType.MEZZANINE, TrancheType.PREFERRED_EQUITY, TrancheType.EQUITY]:
                if remaining_amount <= 0:
                    break

                tranches = tranches_by_type[tranche_type]
                if not tranches:
                    continue

                # Determine allocation percentage for this tranche type
                if tranche_type == TrancheType.SENIOR_DEBT:
                    # Senior debt gets allocated based on LTV constraints
                    for tranche in tranches:
                        ltv_constraints = tranche.allocation_rules.get("ltv_constraints", {})
                        min_ltv = ltv_constraints.get("min_ltv", 0.0)
                        max_ltv = ltv_constraints.get("max_ltv", 0.75)  # Default max LTV for senior debt

                        if min_ltv <= ltv <= max_ltv:
                            # Allocate up to max_ltv
                            allocation_percentage = max_ltv / ltv if ltv > 0 else 0.0
                            allocation_amount = min(remaining_amount, loan_amount * allocation_percentage)

                            tranche.allocate_loan(
                                loan_id=loan_id,
                                allocation_percentage=allocation_amount / loan_amount if loan_amount > 0 else 0.0,
                                allocation_amount=allocation_amount,
                                zone=zone,
                                ltv=ltv,
                            )

                            remaining_amount -= allocation_amount

                elif tranche_type == TrancheType.MEZZANINE:
                    # Mezzanine gets allocated based on LTV constraints
                    for tranche in tranches:
                        ltv_constraints = tranche.allocation_rules.get("ltv_constraints", {})
                        min_ltv = ltv_constraints.get("min_ltv", 0.75)
                        max_ltv = ltv_constraints.get("max_ltv", 0.85)  # Default max LTV for mezzanine

                        if min_ltv <= ltv <= max_ltv:
                            # Allocate up to max_ltv
                            allocation_percentage = (max_ltv - min_ltv) / ltv if ltv > 0 else 0.0
                            allocation_amount = min(remaining_amount, loan_amount * allocation_percentage)

                            tranche.allocate_loan(
                                loan_id=loan_id,
                                allocation_percentage=allocation_amount / loan_amount if loan_amount > 0 else 0.0,
                                allocation_amount=allocation_amount,
                                zone=zone,
                                ltv=ltv,
                            )

                            remaining_amount -= allocation_amount

                else:
                    # Equity tranches get the remainder
                    total_equity_size = sum(t.size for t in tranches)
                    if total_equity_size > 0:
                        for tranche in tranches:
                            allocation_percentage = tranche.size / total_equity_size
                            allocation_amount = min(remaining_amount, allocation_percentage * remaining_amount)

                            tranche.allocate_loan(
                                loan_id=loan_id,
                                allocation_percentage=allocation_amount / loan_amount if loan_amount > 0 else 0.0,
                                allocation_amount=allocation_amount,
                                zone=zone,
                                ltv=ltv,
                            )

                            remaining_amount -= allocation_amount

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="tranche_manager",
            progress=30.0,
            message="Loans allocated to tranches",
        )

        logger.info("Loans allocated to tranches")

    def distribute_cashflows(self, cashflows: List[Dict[str, Any]]) -> None:
        """
        Distribute cashflows to tranches.

        Args:
            cashflows: List of cashflows to distribute
        """
        if not self.enabled or not self.tranches:
            return

        logger.info("Distributing cashflows to tranches")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="tranche_manager",
            progress=40.0,
            message="Distributing cashflows to tranches",
        )

        # Process cashflows by period
        for cashflow in cashflows:
            year = cashflow.get("year", 0)
            month = cashflow.get("month", 0)
            quarter = cashflow.get("quarter", 0)

            # Calculate total available cashflow for distribution
            available_cashflow = cashflow.get("net_cashflow", 0.0)
            if available_cashflow <= 0:
                continue

            # Replenish reserve account if needed
            if self.reserve_account["enabled"]:
                if self.reserve_account["balance"] < self.reserve_account["target_balance"]:
                    replenishment_amount = min(
                        available_cashflow,
                        (self.reserve_account["target_balance"] - self.reserve_account["balance"]) * self.reserve_account["replenishment_rate"]
                    )

                    self.reserve_account["balance"] += replenishment_amount
                    available_cashflow -= replenishment_amount

                    # Record reserve account history
                    self.reserve_account["history"].append({
                        "year": year,
                        "month": month,
                        "balance": self.reserve_account["balance"],
                        "target_balance": self.reserve_account["target_balance"],
                        "deposits": replenishment_amount,
                        "withdrawals": 0.0,
                    })

                    logger.debug(
                        "Reserve account replenished",
                        year=year,
                        month=month,
                        replenishment_amount=replenishment_amount,
                        new_balance=self.reserve_account["balance"],
                    )

            # Distribute to tranches in priority order
            for tranche in self.tranches:
                if available_cashflow <= 0:
                    break

                # Calculate interest due
                interest_due = 0.0
                if tranche.tranche_type in [TrancheType.SENIOR_DEBT, TrancheType.MEZZANINE] and tranche.interest_rate:
                    # Calculate interest based on payment frequency
                    if tranche.payment_frequency == PaymentFrequency.MONTHLY:
                        interest_due = tranche.remaining_principal * tranche.interest_rate / 12
                    elif tranche.payment_frequency == PaymentFrequency.QUARTERLY:
                        interest_due = tranche.remaining_principal * tranche.interest_rate / 4
                    elif tranche.payment_frequency == PaymentFrequency.SEMI_ANNUAL:
                        interest_due = tranche.remaining_principal * tranche.interest_rate / 2
                    else:  # Annual
                        interest_due = tranche.remaining_principal * tranche.interest_rate

                # Calculate principal due
                principal_due = 0.0
                if tranche.amortization and tranche.remaining_principal > 0:
                    if tranche.amortization_schedule == AmortizationSchedule.STRAIGHT_LINE:
                        # Simple straight-line amortization
                        if tranche.term_years and tranche.term_years > 0:
                            if tranche.payment_frequency == PaymentFrequency.MONTHLY:
                                principal_due = tranche.size / (tranche.term_years * 12)
                            elif tranche.payment_frequency == PaymentFrequency.QUARTERLY:
                                principal_due = tranche.size / (tranche.term_years * 4)
                            elif tranche.payment_frequency == PaymentFrequency.SEMI_ANNUAL:
                                principal_due = tranche.size / (tranche.term_years * 2)
                            else:  # Annual
                                principal_due = tranche.size / tranche.term_years

                    # Cap principal due to remaining principal
                    principal_due = min(principal_due, tranche.remaining_principal)

                # Calculate total due
                total_due = interest_due + principal_due

                # Calculate payment amounts
                interest_payment = min(available_cashflow, interest_due)
                available_cashflow -= interest_payment

                principal_payment = min(available_cashflow, principal_due)
                available_cashflow -= principal_payment

                # For equity tranches, distribute remaining cashflow as profit share
                profit_share_payment = 0.0
                if tranche.tranche_type in [TrancheType.PREFERRED_EQUITY, TrancheType.EQUITY]:
                    # Distribute based on waterfall rules
                    if tranche.waterfall_rules:
                        hurdle_rate = tranche.waterfall_rules.get("hurdle_rate")
                        carried_interest_rate = tranche.waterfall_rules.get("carried_interest_rate")

                        if hurdle_rate:
                            # Calculate hurdle amount
                            hurdle_amount = tranche.size * hurdle_rate

                            # Pay up to hurdle amount
                            hurdle_payment = min(available_cashflow, hurdle_amount)
                            profit_share_payment += hurdle_payment
                            available_cashflow -= hurdle_payment

                            # If carried interest is defined, calculate carried interest
                            if carried_interest_rate and available_cashflow > 0:
                                carried_interest = available_cashflow * carried_interest_rate
                                profit_share_payment += carried_interest
                                available_cashflow -= carried_interest
                    else:
                        # Simple profit share based on tranche size
                        profit_share_payment = available_cashflow
                        available_cashflow = 0.0

                # Record payment
                if interest_payment > 0 or principal_payment > 0 or profit_share_payment > 0:
                    tranche.record_payment(
                        year=year,
                        month=month,
                        quarter=quarter,
                        principal_payment=principal_payment,
                        interest_payment=interest_payment,
                        profit_share_payment=profit_share_payment,
                    )

            # Run coverage tests if applicable
            self._run_coverage_tests(year, month, quarter)

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="tranche_manager",
            progress=70.0,
            message="Cashflows distributed to tranches",
        )

        logger.info("Cashflows distributed to tranches")

    def _run_coverage_tests(self, year: float, month: int, quarter: Optional[int] = None) -> None:
        """
        Run coverage tests.

        Args:
            year: Year
            month: Month
            quarter: Quarter (if applicable)
        """
        # Check if tests are enabled
        if not self.overcollateralization_test["enabled"] and not self.interest_coverage_test["enabled"]:
            return

        # Check if it's time to run tests based on frequency
        should_run_oc_test = False
        should_run_ic_test = False

        if self.overcollateralization_test["enabled"]:
            test_frequency = self.overcollateralization_test["test_frequency"]
            if (test_frequency == "monthly" or
                (test_frequency == "quarterly" and month in [3, 6, 9, 12]) or
                (test_frequency == "semi_annual" and month in [6, 12]) or
                (test_frequency == "annual" and month == 12)):
                should_run_oc_test = True

        if self.interest_coverage_test["enabled"]:
            test_frequency = self.interest_coverage_test["test_frequency"]
            if (test_frequency == "monthly" or
                (test_frequency == "quarterly" and month in [3, 6, 9, 12]) or
                (test_frequency == "semi_annual" and month in [6, 12]) or
                (test_frequency == "annual" and month == 12)):
                should_run_ic_test = True

        # Run overcollateralization test
        if should_run_oc_test:
            # Calculate total loan value
            total_loan_value = sum(
                sum(allocation["allocation_amount"] for allocation in tranche.loan_allocations)
                for tranche in self.tranches
            )

            # Calculate total senior debt
            total_senior_debt = sum(
                tranche.remaining_principal
                for tranche in self.tranches
                if tranche.tranche_type == TrancheType.SENIOR_DEBT
            )

            # Calculate OC ratio
            oc_ratio = total_loan_value / total_senior_debt if total_senior_debt > 0 else float('inf')

            # Check if test passed
            threshold = self.overcollateralization_test["threshold"]
            passed = oc_ratio >= threshold

            # Record test result
            test_date = datetime.now().isoformat()
            cure_deadline = None
            if not passed:
                # Calculate cure deadline
                cure_period_months = self.overcollateralization_test["cure_period_months"]
                # Simple calculation - in a real implementation, this would use proper date arithmetic
                cure_deadline = datetime(int(year), month, 1).replace(month=month + cure_period_months).isoformat()

            self.overcollateralization_test["results"].append({
                "test_type": TestType.OVERCOLLATERALIZATION.value,
                "test_date": test_date,
                "year": year,
                "month": month,
                "threshold": threshold,
                "actual_value": oc_ratio,
                "passed": passed,
                "cure_deadline": cure_deadline,
                "cured": None,
            })

            # Update visualization data
            if "overcollateralization" not in self.visualization["coverage_test_chart"]:
                self.visualization["coverage_test_chart"]["overcollateralization"] = []

            self.visualization["coverage_test_chart"]["overcollateralization"].append({
                "year": year,
                "month": month,
                "actual_value": oc_ratio,
                "threshold": threshold,
            })

            logger.info(
                "Overcollateralization test run",
                year=year,
                month=month,
                oc_ratio=oc_ratio,
                threshold=threshold,
                passed=passed,
            )

        # Run interest coverage test
        if should_run_ic_test:
            # Calculate total interest income
            # In a real implementation, this would use actual interest income from cashflows
            total_interest_income = 1000000  # Placeholder value

            # Calculate total interest expense
            total_interest_expense = sum(
                tranche.interest_rate * tranche.remaining_principal / 4  # Assuming quarterly payments
                for tranche in self.tranches
                if tranche.tranche_type in [TrancheType.SENIOR_DEBT, TrancheType.MEZZANINE] and tranche.interest_rate
            )

            # Calculate IC ratio
            ic_ratio = total_interest_income / total_interest_expense if total_interest_expense > 0 else float('inf')

            # Check if test passed
            threshold = self.interest_coverage_test["threshold"]
            passed = ic_ratio >= threshold

            # Record test result
            test_date = datetime.now().isoformat()
            cure_deadline = None
            if not passed:
                # Calculate cure deadline
                cure_period_months = self.interest_coverage_test["cure_period_months"]
                # Simple calculation - in a real implementation, this would use proper date arithmetic
                cure_deadline = datetime(int(year), month, 1).replace(month=month + cure_period_months).isoformat()

            self.interest_coverage_test["results"].append({
                "test_type": TestType.INTEREST_COVERAGE.value,
                "test_date": test_date,
                "year": year,
                "month": month,
                "threshold": threshold,
                "actual_value": ic_ratio,
                "passed": passed,
                "cure_deadline": cure_deadline,
                "cured": None,
            })

            # Update visualization data
            if "interest_coverage" not in self.visualization["coverage_test_chart"]:
                self.visualization["coverage_test_chart"]["interest_coverage"] = []

            self.visualization["coverage_test_chart"]["interest_coverage"].append({
                "year": year,
                "month": month,
                "actual_value": ic_ratio,
                "threshold": threshold,
            })

            logger.info(
                "Interest coverage test run",
                year=year,
                month=month,
                ic_ratio=ic_ratio,
                threshold=threshold,
                passed=passed,
            )

    def calculate_metrics(self) -> None:
        """Calculate metrics for all tranches."""
        if not self.enabled or not self.tranches:
            return

        logger.info("Calculating tranche metrics")

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="tranche_manager",
            progress=80.0,
            message="Calculating tranche metrics",
        )

        # Calculate metrics for each tranche
        for tranche in self.tranches:
            tranche.calculate_metrics()

        # Generate visualization data
        self._generate_visualization_data()

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="tranche_manager",
            progress=90.0,
            message="Tranche metrics calculated",
        )

        logger.info("Tranche metrics calculated")

    def _generate_visualization_data(self) -> None:
        """Generate visualization data for tranches."""
        # Generate tranche waterfall chart
        self.visualization["tranche_waterfall_chart"] = [
            {
                "tranche": tranche.name,
                "principal": tranche.principal_payments,
                "interest": tranche.interest_payments,
                "profit_share": tranche.profit_share_payments,
                "total": tranche.total_payments,
            }
            for tranche in self.tranches
        ]

        # Generate tranche cashflow chart
        for tranche in self.tranches:
            self.visualization["tranche_cashflow_chart"][tranche.name] = [
                {
                    "year": cf["year"],
                    "quarter": cf.get("quarter"),
                    "payment": cf["total_payment"],
                }
                for cf in tranche.cashflows
            ]

        # Generate tranche allocation chart
        zone_allocations = defaultdict(lambda: defaultdict(float))
        for tranche in self.tranches:
            for allocation in tranche.loan_allocations:
                zone = allocation["zone"]
                amount = allocation["allocation_amount"]
                zone_allocations[tranche.name][zone] += amount

        self.visualization["tranche_allocation_chart"] = [
            {
                "tranche": tranche_name,
                "green": allocations.get("green", 0.0),
                "orange": allocations.get("orange", 0.0),
                "red": allocations.get("red", 0.0),
            }
            for tranche_name, allocations in zone_allocations.items()
        ]

        # Generate tranche performance chart
        self.visualization["tranche_performance_chart"] = [
            {
                "tranche": tranche.name,
                "target_return": tranche.target_return or 0.0,
                "actual_return": tranche.actual_return or 0.0,
                "irr": tranche.irr or 0.0,
                "moic": tranche.moic or 0.0,
            }
            for tranche in self.tranches
        ]

        # Generate reserve account chart
        self.visualization["reserve_account_chart"] = [
            {
                "year": entry["year"],
                "month": entry["month"],
                "balance": entry["balance"],
                "target": entry["target_balance"],
            }
            for entry in self.reserve_account["history"]
        ]

        logger.debug("Visualization data generated")

    def get_results(self) -> Dict[str, Any]:
        """
        Get tranche manager results.

        Returns:
            Dictionary containing tranche manager results
        """
        if not self.enabled:
            return {}

        # Send progress update
        self.websocket_manager.send_progress(
            simulation_id=self.context.run_id,
            module="tranche_manager",
            progress=100.0,
            message="Tranche manager completed",
        )

        # Create tranche summary
        tranche_summary = [tranche.to_dict() for tranche in self.tranches]

        # Create tranche cashflows
        tranche_cashflows = {
            tranche.name: tranche.cashflows
            for tranche in self.tranches
        }

        # Create tranche allocations
        tranche_allocations = {
            tranche.name: tranche.loan_allocations
            for tranche in self.tranches
        }

        # Create coverage tests
        coverage_tests = (
            self.overcollateralization_test["results"] +
            self.interest_coverage_test["results"]
        )

        # Create reserve account
        reserve_account = self.reserve_account["history"]

        # Create results dictionary
        results = {
            "tranche_summary": tranche_summary,
            "tranche_cashflows": tranche_cashflows,
            "tranche_allocations": tranche_allocations,
            "coverage_tests": coverage_tests,
            "reserve_account": reserve_account,
            "visualization": self.visualization,
        }

        logger.info("Tranche manager results generated")

        return results
