"""
Leverage manager module for the EQU IHOME SIM ENGINE v2.

This module is responsible for managing debt facilities, calculating interest,
and enforcing borrowing base tests.
"""

import logging
import copy
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from src.engine.simulation_context import SimulationContext
from src.api.websocket_manager import get_websocket_manager

# Set up logging
logger = logging.getLogger(__name__)


class LeverageFacility:
    """
    Represents a debt facility for the fund.

    This class models different types of debt facilities:
    - NAV line: Secured by the fund's net asset value
    - Subscription line: Secured by LP commitments
    - Repo facility: Repurchase agreement for specific assets
    """

    def __init__(
        self,
        facility_id: str,
        facility_type: str,
        max_amount: float,
        interest_rate: float,
        commitment_fee_bps: float = 0,
        term_years: float = 5.0,
        advance_rate: float = 0.75,
    ):
        """
        Initialize a leverage facility.

        Args:
            facility_id: Unique identifier for the facility
            facility_type: Type of facility (nav_line, subscription_line, repo)
            max_amount: Maximum facility amount
            interest_rate: Annual interest rate (as a decimal)
            commitment_fee_bps: Commitment fee on undrawn balance (basis points)
            term_years: Term of the facility in years
            advance_rate: Maximum advance rate (for NAV lines)
        """
        self.facility_id = facility_id
        self.facility_type = facility_type
        self.max_amount = max_amount
        self.interest_rate = interest_rate
        self.commitment_fee_bps = commitment_fee_bps
        self.term_years = term_years
        self.advance_rate = advance_rate

        # Current state
        self.current_balance = 0.0
        self.available_amount = max_amount
        self.inception_date = None
        self.maturity_date = None
        self.draws = []
        self.repayments = []
        self.interest_payments = []

        logger.info(
            "Leverage facility created",
            facility_id=facility_id,
            facility_type=facility_type,
            max_amount=max_amount,
            interest_rate=interest_rate,
        )

    def draw(self, amount: float, date: datetime) -> float:
        """
        Draw from the facility.

        Args:
            amount: Amount to draw
            date: Date of the draw

        Returns:
            Actual amount drawn (may be less than requested if insufficient availability)
        """
        # Set inception date if this is the first draw
        if self.inception_date is None:
            self.inception_date = date
            self.maturity_date = datetime(
                date.year + int(self.term_years),
                date.month,
                date.day,
            )

        # Check if amount exceeds available amount
        actual_draw = min(amount, self.available_amount)

        if actual_draw < amount:
            logger.warning(
                "Draw amount exceeds available amount",
                facility_id=self.facility_id,
                requested=amount,
                available=self.available_amount,
                actual_draw=actual_draw,
            )

        # Update state
        self.current_balance += actual_draw
        self.available_amount = self.max_amount - self.current_balance

        # Record draw
        self.draws.append({
            "date": date,
            "amount": actual_draw,
        })

        logger.info(
            "Facility draw",
            facility_id=self.facility_id,
            amount=actual_draw,
            current_balance=self.current_balance,
            available_amount=self.available_amount,
        )

        return actual_draw

    def repay(self, amount: float, date: datetime) -> float:
        """
        Repay the facility.

        Args:
            amount: Amount to repay
            date: Date of the repayment

        Returns:
            Actual amount repaid (may be less than requested if insufficient balance)
        """
        # Check if amount exceeds current balance
        actual_repayment = min(amount, self.current_balance)

        if actual_repayment < amount:
            logger.warning(
                "Repayment amount exceeds current balance",
                facility_id=self.facility_id,
                requested=amount,
                current_balance=self.current_balance,
                actual_repayment=actual_repayment,
            )

        # Update state
        self.current_balance -= actual_repayment
        self.available_amount = self.max_amount - self.current_balance

        # Record repayment
        self.repayments.append({
            "date": date,
            "amount": actual_repayment,
        })

        logger.info(
            "Facility repayment",
            facility_id=self.facility_id,
            amount=actual_repayment,
            current_balance=self.current_balance,
            available_amount=self.available_amount,
        )

        return actual_repayment

    def calculate_interest(self, period_start: datetime, period_end: datetime) -> float:
        """
        Calculate interest for a period.

        Args:
            period_start: Start date of the period
            period_end: End date of the period

        Returns:
            Interest amount for the period
        """
        # Calculate days in period
        days_in_period = (period_end - period_start).days

        # Calculate average balance during period
        # This is a simplification; in reality, we would need to calculate
        # the weighted average balance based on draws and repayments
        average_balance = self.current_balance

        # Calculate interest
        interest = average_balance * self.interest_rate * (days_in_period / 365)

        # Record interest payment
        self.interest_payments.append({
            "period_start": period_start,
            "period_end": period_end,
            "days": days_in_period,
            "average_balance": average_balance,
            "interest_rate": self.interest_rate,
            "interest_amount": interest,
        })

        logger.info(
            "Interest calculated",
            facility_id=self.facility_id,
            period_start=period_start,
            period_end=period_end,
            days=days_in_period,
            average_balance=average_balance,
            interest_rate=self.interest_rate,
            interest_amount=interest,
        )

        return interest

    def calculate_commitment_fee(self, period_start: datetime, period_end: datetime) -> float:
        """
        Calculate commitment fee for a period.

        Args:
            period_start: Start date of the period
            period_end: End date of the period

        Returns:
            Commitment fee amount for the period
        """
        # Calculate days in period
        days_in_period = (period_end - period_start).days

        # Calculate average undrawn balance during period
        average_undrawn = self.available_amount

        # Calculate commitment fee (basis points converted to decimal)
        commitment_fee = average_undrawn * (self.commitment_fee_bps / 10000) * (days_in_period / 365)

        logger.info(
            "Commitment fee calculated",
            facility_id=self.facility_id,
            period_start=period_start,
            period_end=period_end,
            days=days_in_period,
            average_undrawn=average_undrawn,
            commitment_fee_bps=self.commitment_fee_bps,
            commitment_fee=commitment_fee,
        )

        return commitment_fee

    def check_borrowing_base(self, nav: float) -> Tuple[bool, float]:
        """
        Check if the facility is within borrowing base limits.

        Args:
            nav: Net asset value of the fund

        Returns:
            Tuple of (is_compliant, max_allowed)
        """
        if self.facility_type == "nav_line":
            # NAV line: Maximum advance rate applied to NAV
            max_allowed = nav * self.advance_rate
            is_compliant = self.current_balance <= max_allowed

            if not is_compliant:
                logger.warning(
                    "Borrowing base violation",
                    facility_id=self.facility_id,
                    facility_type=self.facility_type,
                    current_balance=self.current_balance,
                    nav=nav,
                    advance_rate=self.advance_rate,
                    max_allowed=max_allowed,
                )

            return is_compliant, max_allowed

        # For other facility types, no borrowing base test
        return True, self.max_amount


def manage_leverage(context: SimulationContext) -> None:
    """
    Manage leverage facilities for the simulation.

    Args:
        context: Simulation context
    """
    logger.info("Managing leverage")

    # Get configuration parameters
    config = context.config

    # Check if leverage is enabled
    leverage_config = getattr(config, "leverage", None)
    if not leverage_config or not getattr(leverage_config, "enabled", False):
        logger.info("Leverage disabled, skipping")
        return

    # Initialize leverage facilities if not already done
    if not context.leverage_facilities:
        _initialize_leverage_facilities(context)

    # Process leverage events (draws, repayments, interest)
    _process_leverage_events(context)

    # Check borrowing base compliance
    _check_borrowing_base_compliance(context)


def _initialize_leverage_facilities(context: SimulationContext) -> None:
    """
    Initialize leverage facilities based on configuration.

    Args:
        context: Simulation context
    """
    config = context.config
    leverage_config = getattr(config, "leverage", {})

    # Initialize NAV line facility if enabled
    nav_line = getattr(leverage_config, "green_sleeve", None)
    if nav_line and getattr(nav_line, "enabled", False):
        facility = LeverageFacility(
            facility_id="nav_line",
            facility_type="nav_line",
            max_amount=config.fund_size * getattr(nav_line, "max_mult", 1.5),
            interest_rate=getattr(nav_line, "spread_bps", 275) / 10000,
            commitment_fee_bps=getattr(nav_line, "commitment_fee_bps", 50),
            advance_rate=0.75,
        )
        context.leverage_facilities["nav_line"] = facility.__dict__

    # Initialize subscription line facility if enabled
    sub_line = getattr(leverage_config, "ramp_line", None)
    if sub_line and getattr(sub_line, "enabled", False):
        facility = LeverageFacility(
            facility_id="subscription_line",
            facility_type="subscription_line",
            max_amount=config.fund_size * getattr(sub_line, "limit_pct_commit", 0.15),
            interest_rate=getattr(sub_line, "spread_bps", 300) / 10000,
            commitment_fee_bps=50,
            term_years=getattr(sub_line, "draw_period_months", 24) / 12,
        )
        context.leverage_facilities["subscription_line"] = facility.__dict__


def _initialize_facilities(context: SimulationContext) -> None:
    """
    Initialize debt facilities based on configuration.

    Args:
        context: Simulation context
    """
    # Get configuration
    config = context.config
    leverage_config = getattr(config, "leverage_engine", {})

    # Initialize facilities
    if leverage_config.get("green_sleeve", {}).get("enabled", False):
        _initialize_nav_line(context)

    if leverage_config.get("ramp_line", {}).get("enabled", False):
        _initialize_subscription_line(context)


def _initialize_nav_line(context: SimulationContext) -> None:
    """
    Initialize NAV line facility.

    Args:
        context: Simulation context
    """
    # Get configuration
    config = context.config
    leverage_config = getattr(config, "leverage_engine", {})
    nav_line_config = leverage_config.get("green_sleeve", {})

    # Calculate facility size
    fund_size = getattr(config, "fund_size", 100000000)
    max_mult = nav_line_config.get("max_mult", 1.5)
    max_amount = fund_size * max_mult

    # Get interest rate
    base_rate = leverage_config.get("interest_rate_model", {}).get("base_rate_initial", 0.0425)
    spread_bps = nav_line_config.get("spread_bps", 275)
    interest_rate = base_rate + (spread_bps / 10000)

    # Get other parameters
    commitment_fee_bps = nav_line_config.get("commitment_fee_bps", 50)
    advance_rate = nav_line_config.get("advance_rate", 0.75)
    term_years = nav_line_config.get("term_years", 5)

    # Create facility
    facility = LeverageFacility(
        facility_id="nav_line",
        facility_type="nav_line",
        max_amount=max_amount,
        interest_rate=interest_rate,
        commitment_fee_bps=commitment_fee_bps,
        term_years=term_years,
        advance_rate=advance_rate,
    )

    # Add to context
    context.leverage_facilities["nav_line"] = facility.__dict__

    logger.info(
        "Initialized NAV line facility",
        max_amount=max_amount,
        interest_rate=interest_rate,
        advance_rate=advance_rate,
    )


def _initialize_subscription_line(context: SimulationContext) -> None:
    """
    Initialize subscription line facility.

    Args:
        context: Simulation context
    """
    # Get configuration
    config = context.config
    leverage_config = getattr(config, "leverage_engine", {})
    sub_line_config = leverage_config.get("ramp_line", {})

    # Calculate facility size
    fund_size = getattr(config, "fund_size", 100000000)
    limit_pct = sub_line_config.get("limit_pct_commit", 0.15)
    max_amount = fund_size * limit_pct

    # Get interest rate
    base_rate = leverage_config.get("interest_rate_model", {}).get("base_rate_initial", 0.0425)
    spread_bps = sub_line_config.get("spread_bps", 300)
    interest_rate = base_rate + (spread_bps / 10000)

    # Get other parameters
    commitment_fee_bps = sub_line_config.get("commitment_fee_bps", 50)
    draw_period_months = sub_line_config.get("draw_period_months", 24)
    term_months = sub_line_config.get("term_months", 36)

    # Create facility
    facility = LeverageFacility(
        facility_id="subscription_line",
        facility_type="subscription_line",
        max_amount=max_amount,
        interest_rate=interest_rate,
        commitment_fee_bps=commitment_fee_bps,
        term_years=term_months / 12,
    )

    # Add to context
    context.leverage_facilities["subscription_line"] = facility.__dict__

    logger.info(
        "Initialized subscription line facility",
        max_amount=max_amount,
        interest_rate=interest_rate,
        draw_period_months=draw_period_months,
    )


def _process_leverage_events(context: SimulationContext) -> None:
    """
    Process leverage events (draws, repayments, interest).

    Args:
        context: Simulation context
    """
    # Get current simulation time
    current_year = getattr(context, "current_year", 0)
    current_month = getattr(context, "current_month", 0)

    # Get configuration
    config = context.config

    # Initialize tracking lists if not already present
    if not hasattr(context, "leverage_draws"):
        context.leverage_draws = []

    if not hasattr(context, "leverage_repayments"):
        context.leverage_repayments = []

    if not hasattr(context, "leverage_interest_payments"):
        context.leverage_interest_payments = []

    if not hasattr(context, "leverage_commitment_fees"):
        context.leverage_commitment_fees = []

    if not hasattr(context, "leverage_borrowing_base_tests"):
        context.leverage_borrowing_base_tests = []

    # Process facility draws
    _process_facility_draws(context, current_year, current_month)

    # Process facility repayments
    _process_facility_repayments(context, current_year, current_month)

    # Calculate interest and commitment fees
    _calculate_interest_and_fees(context, current_year, current_month)

    # Update leverage metrics
    _update_leverage_metrics(context, current_year, current_month)


def _check_borrowing_base_compliance(context: SimulationContext) -> None:
    """
    Check borrowing base compliance for all facilities.

    Args:
        context: Simulation context
    """
    # Get current simulation time
    current_year = getattr(context, "current_year", 0)
    current_month = getattr(context, "current_month", 0)

    # Calculate NAV
    nav = _calculate_nav(context)

    # Check each facility against its borrowing base
    for facility_id, facility_data in context.leverage_facilities.items():
        # Recreate facility object from dict
        facility = LeverageFacility(**facility_data)

        # Check borrowing base
        is_compliant, max_allowed = facility.check_borrowing_base(nav)

        # Record borrowing base test
        test_result = {
            "facility_id": facility_id,
            "date": datetime.now(),
            "year": current_year,
            "month": current_month,
            "nav": nav,
            "current_balance": facility.current_balance,
            "max_allowed": max_allowed,
            "is_compliant": is_compliant,
            "headroom": max_allowed - facility.current_balance,
        }

        context.leverage_borrowing_base_tests.append(test_result)

        # Log result
        if is_compliant:
            logger.info(
                "Borrowing base test passed",
                facility_id=facility_id,
                current_balance=facility.current_balance,
                max_allowed=max_allowed,
                headroom=max_allowed - facility.current_balance,
            )
        else:
            logger.warning(
                "Borrowing base test failed",
                facility_id=facility_id,
                current_balance=facility.current_balance,
                max_allowed=max_allowed,
                shortfall=facility.current_balance - max_allowed,
            )

            # Trigger deleveraging if needed
            if facility.current_balance > max_allowed:
                _deleverage_facility(context, facility_id, facility.current_balance - max_allowed)


def _process_facility_draws(context: SimulationContext, current_year: float, current_month: int) -> None:
    """
    Process facility draws based on capital needs.

    Args:
        context: Simulation context
        current_year: Current simulation year
        current_month: Current simulation month
    """
    # Check if we need to draw from facilities
    capital_needs = _calculate_capital_needs(context)

    if capital_needs <= 0:
        return

    # Determine which facilities to draw from
    # Preference order: subscription line first, then NAV line
    facilities_to_draw = []

    if "subscription_line" in context.leverage_facilities:
        facilities_to_draw.append("subscription_line")

    if "nav_line" in context.leverage_facilities:
        facilities_to_draw.append("nav_line")

    # Draw from facilities in order
    remaining_need = capital_needs

    for facility_id in facilities_to_draw:
        if remaining_need <= 0:
            break

        # Recreate facility object from dict
        facility_data = context.leverage_facilities[facility_id]
        facility = LeverageFacility(**facility_data)

        # Check if facility has available capacity
        if facility.available_amount > 0:
            # Draw the lesser of remaining need or available amount
            draw_amount = min(remaining_need, facility.available_amount)

            # Draw from facility
            actual_draw = facility.draw(draw_amount, datetime.now())

            # Update remaining need
            remaining_need -= actual_draw

            # Record draw
            draw_event = {
                "facility_id": facility_id,
                "date": datetime.now(),
                "amount": actual_draw,
                "year": current_year,
                "month": current_month,
                "purpose": "capital_needs",
            }

            context.leverage_draws.append(draw_event)

            # Update facility in context
            context.leverage_facilities[facility_id] = facility.__dict__

    # Log if we couldn't meet all capital needs
    if remaining_need > 0:
        logger.warning(
            "Could not meet all capital needs with leverage",
            capital_needs=capital_needs,
            unmet_needs=remaining_need,
        )


def _process_facility_repayments(context: SimulationContext, current_year: float, current_month: int) -> None:
    """
    Process facility repayments based on available cash.

    Args:
        context: Simulation context
        current_year: Current simulation year
        current_month: Current simulation month
    """
    # Check if we have excess cash to repay facilities
    excess_cash = _calculate_excess_cash(context)

    if excess_cash <= 0:
        return

    # Determine which facilities to repay
    # Preference order: NAV line first, then subscription line
    facilities_to_repay = []

    if "nav_line" in context.leverage_facilities:
        facilities_to_repay.append("nav_line")

    if "subscription_line" in context.leverage_facilities:
        facilities_to_repay.append("subscription_line")

    # Repay facilities in order
    remaining_cash = excess_cash

    for facility_id in facilities_to_repay:
        if remaining_cash <= 0:
            break

        # Recreate facility object from dict
        facility_data = context.leverage_facilities[facility_id]
        facility = LeverageFacility(**facility_data)

        # Check if facility has outstanding balance
        if facility.current_balance > 0:
            # Repay the lesser of remaining cash or current balance
            repay_amount = min(remaining_cash, facility.current_balance)

            # Repay facility
            actual_repayment = facility.repay(repay_amount, datetime.now())

            # Update remaining cash
            remaining_cash -= actual_repayment

            # Record repayment
            repayment_event = {
                "facility_id": facility_id,
                "date": datetime.now(),
                "amount": actual_repayment,
                "year": current_year,
                "month": current_month,
                "source": "excess_cash",
            }

            context.leverage_repayments.append(repayment_event)

            # Update facility in context
            context.leverage_facilities[facility_id] = facility.__dict__


def _calculate_interest_and_fees(context: SimulationContext, current_year: float, current_month: int) -> None:
    """
    Calculate interest and commitment fees for all facilities.

    Args:
        context: Simulation context
        current_year: Current simulation year
        current_month: Current simulation month
    """
    # Calculate period start and end dates
    # Assuming monthly interest calculations
    period_start = datetime(int(current_year), current_month, 1)

    # Calculate period end (last day of the month)
    if current_month == 12:
        period_end = datetime(int(current_year) + 1, 1, 1)
    else:
        period_end = datetime(int(current_year), current_month + 1, 1)

    period_end = period_end - datetime.timedelta(days=1)

    # Calculate interest and fees for each facility
    for facility_id, facility_data in context.leverage_facilities.items():
        # Recreate facility object from dict
        facility = LeverageFacility(**facility_data)

        # Calculate interest
        interest = facility.calculate_interest(period_start, period_end)

        # Record interest payment
        if interest > 0:
            interest_payment = {
                "facility_id": facility_id,
                "period_start": period_start,
                "period_end": period_end,
                "amount": interest,
                "year": current_year,
                "month": current_month,
                "interest_rate": facility.interest_rate,
                "average_balance": facility.current_balance,
            }

            context.leverage_interest_payments.append(interest_payment)

        # Calculate commitment fee
        commitment_fee = facility.calculate_commitment_fee(period_start, period_end)

        # Record commitment fee
        if commitment_fee > 0:
            fee_payment = {
                "facility_id": facility_id,
                "period_start": period_start,
                "period_end": period_end,
                "amount": commitment_fee,
                "year": current_year,
                "month": current_month,
                "fee_rate_bps": facility.commitment_fee_bps,
                "average_undrawn": facility.available_amount,
            }

            context.leverage_commitment_fees.append(fee_payment)


def _update_leverage_metrics(context: SimulationContext, current_year: float, current_month: int) -> None:
    """
    Update leverage metrics.

    Args:
        context: Simulation context
        current_year: Current simulation year
        current_month: Current simulation month
    """
    # Calculate NAV
    nav = _calculate_nav(context)

    # Calculate total debt
    total_debt = sum(
        facility_data.get("current_balance", 0)
        for facility_data in context.leverage_facilities.values()
    )

    # Calculate total available
    total_available = sum(
        facility_data.get("available_amount", 0)
        for facility_data in context.leverage_facilities.values()
    )

    # Calculate total interest paid
    total_interest_paid = sum(
        payment.get("amount", 0)
        for payment in context.leverage_interest_payments
    )

    # Calculate total commitment fees paid
    total_commitment_fees_paid = sum(
        fee.get("amount", 0)
        for fee in context.leverage_commitment_fees
    )

    # Calculate weighted average interest rate
    weighted_avg_interest_rate = 0
    if total_debt > 0:
        weighted_avg_interest_rate = sum(
            facility_data.get("current_balance", 0) * facility_data.get("interest_rate", 0)
            for facility_data in context.leverage_facilities.values()
        ) / total_debt

    # Calculate leverage ratio
    leverage_ratio = 0
    if nav > 0:
        leverage_ratio = total_debt / nav

    # Calculate debt service coverage ratio
    # This is a simplification; in reality, we would need to calculate
    # cash flow and debt service more precisely
    cash_flow = _calculate_cash_flow(context)
    debt_service = total_interest_paid + total_commitment_fees_paid

    debt_service_coverage_ratio = 0
    if debt_service > 0:
        debt_service_coverage_ratio = cash_flow / debt_service

    # Calculate interest coverage ratio
    interest_coverage_ratio = 0
    if total_interest_paid > 0:
        interest_coverage_ratio = cash_flow / total_interest_paid

    # Calculate loan-to-value ratio
    portfolio_value = _calculate_portfolio_value(context)

    loan_to_value_ratio = 0
    if portfolio_value > 0:
        loan_to_value_ratio = total_debt / portfolio_value

    # Store metrics in context
    if not hasattr(context, "leverage_metrics"):
        context.leverage_metrics = {}

    context.leverage_metrics = {
        "total_debt": total_debt,
        "total_available": total_available,
        "total_interest_paid": total_interest_paid,
        "total_commitment_fees_paid": total_commitment_fees_paid,
        "weighted_avg_interest_rate": weighted_avg_interest_rate,
        "leverage_ratio": leverage_ratio,
        "debt_service_coverage_ratio": debt_service_coverage_ratio,
        "interest_coverage_ratio": interest_coverage_ratio,
        "loan_to_value_ratio": loan_to_value_ratio,
    }

    # Store timeline data for visualization
    if not hasattr(context, "leverage_timeline"):
        context.leverage_timeline = []

    timeline_entry = {
        "year": current_year,
        "month": current_month,
        "total_debt": total_debt,
        "nav": nav,
        "leverage_ratio": leverage_ratio,
    }

    context.leverage_timeline.append(timeline_entry)

    # Store facility utilization data for visualization
    if not hasattr(context, "facility_utilization"):
        context.facility_utilization = []

    for facility_id, facility_data in context.leverage_facilities.items():
        utilization_entry = {
            "year": current_year,
            "month": current_month,
            "facility_id": facility_id,
            "facility_type": facility_data.get("facility_type", ""),
            "current_balance": facility_data.get("current_balance", 0),
            "available_amount": facility_data.get("available_amount", 0),
            "utilization_percentage": 0,
        }

        max_amount = facility_data.get("max_amount", 0)
        if max_amount > 0:
            utilization_entry["utilization_percentage"] = facility_data.get("current_balance", 0) / max_amount

        context.facility_utilization.append(utilization_entry)


def _calculate_nav(context: SimulationContext) -> float:
    """
    Calculate the Net Asset Value (NAV) of the fund.

    Args:
        context: Simulation context

    Returns:
        Net Asset Value
    """
    # Get loans
    loans = getattr(context, "loans", [])

    # Calculate total loan value
    total_loan_value = sum(loan.get("loan_size", 0) for loan in loans)

    # Get cash
    cash = getattr(context, "cash", 0)

    # Calculate NAV
    nav = total_loan_value + cash

    return nav


def _calculate_portfolio_value(context: SimulationContext) -> float:
    """
    Calculate the total value of the loan portfolio.

    Args:
        context: Simulation context

    Returns:
        Portfolio value
    """
    # Get loans
    loans = getattr(context, "loans", [])

    # Calculate total property value
    total_property_value = sum(loan.get("property_value", 0) for loan in loans)

    return total_property_value


def _calculate_cash_flow(context: SimulationContext) -> float:
    """
    Calculate the cash flow for the current period.

    Args:
        context: Simulation context

    Returns:
        Cash flow
    """
    # Get cash flow from context if available
    if hasattr(context, "cash_flow"):
        return context.cash_flow

    # Otherwise, estimate cash flow based on interest income
    # This is a simplification; in reality, cash flow would be calculated
    # based on interest income, principal repayments, and other factors
    loans = getattr(context, "loans", [])

    # Calculate interest income
    interest_income = sum(
        loan.get("loan_size", 0) * loan.get("interest_rate", 0)
        for loan in loans
    )

    return interest_income


def _calculate_capital_needs(context: SimulationContext) -> float:
    """
    Calculate the capital needs for the current period.

    Args:
        context: Simulation context

    Returns:
        Capital needs
    """
    # Get capital needs from context if available
    if hasattr(context, "capital_needs"):
        return context.capital_needs

    # Otherwise, estimate capital needs based on target allocation
    # This is a simplification; in reality, capital needs would be calculated
    # based on the fund's investment strategy, pipeline, etc.
    config = context.config
    fund_size = getattr(config, "fund_size", 0)

    # Get loans
    loans = getattr(context, "loans", [])

    # Calculate total loan value
    total_loan_value = sum(loan.get("loan_size", 0) for loan in loans)

    # Get cash
    cash = getattr(context, "cash", 0)

    # Calculate capital needs
    # Assume we want to be fully invested (fund_size)
    capital_needs = fund_size - (total_loan_value + cash)

    # Only return positive capital needs
    return max(0, capital_needs)


def _calculate_excess_cash(context: SimulationContext) -> float:
    """
    Calculate the excess cash available for repayment.

    Args:
        context: Simulation context

    Returns:
        Excess cash
    """
    # Get cash
    cash = getattr(context, "cash", 0)

    # Get cash reserve target
    config = context.config
    leverage_config = getattr(config, "leverage", {})
    optimization = getattr(leverage_config, "optimization", {})
    min_cash_buffer = getattr(optimization, "min_cash_buffer", 1.5)

    # Calculate debt service
    interest_payments = getattr(context, "leverage_interest_payments", [])
    commitment_fees = getattr(context, "leverage_commitment_fees", [])

    # Calculate total debt service for the current period
    current_year = getattr(context, "current_year", 0)
    current_month = getattr(context, "current_month", 0)

    current_interest = sum(
        payment.get("amount", 0)
        for payment in interest_payments
        if payment.get("year") == current_year and payment.get("month") == current_month
    )

    current_fees = sum(
        fee.get("amount", 0)
        for fee in commitment_fees
        if fee.get("year") == current_year and fee.get("month") == current_month
    )

    debt_service = current_interest + current_fees

    # Calculate cash reserve
    cash_reserve = debt_service * min_cash_buffer

    # Calculate excess cash
    excess_cash = cash - cash_reserve

    # Only return positive excess cash
    return max(0, excess_cash)


def _calculate_available_cash(context: SimulationContext) -> float:
    """
    Calculate the available cash.

    Args:
        context: Simulation context

    Returns:
        Available cash
    """
    # Get cash
    cash = getattr(context, "cash", 0)

    # Get minimum cash reserve
    config = context.config
    leverage_config = getattr(config, "leverage", {})
    optimization = getattr(leverage_config, "optimization", {})
    min_cash_buffer = getattr(optimization, "min_cash_buffer", 1.5)

    # Calculate debt service
    interest_payments = getattr(context, "leverage_interest_payments", [])
    commitment_fees = getattr(context, "leverage_commitment_fees", [])

    # Calculate total debt service for the current period
    current_year = getattr(context, "current_year", 0)
    current_month = getattr(context, "current_month", 0)

    current_interest = sum(
        payment.get("amount", 0)
        for payment in interest_payments
        if payment.get("year") == current_year and payment.get("month") == current_month
    )

    current_fees = sum(
        fee.get("amount", 0)
        for fee in commitment_fees
        if fee.get("year") == current_year and fee.get("month") == current_month
    )

    debt_service = current_interest + current_fees

    # Calculate minimum cash reserve
    min_cash_reserve = debt_service * min_cash_buffer

    # Calculate available cash
    available_cash = cash - min_cash_reserve

    # Only return positive available cash
    return max(0, available_cash)


def _deleverage_facility(context: SimulationContext, facility_id: str, amount: float) -> None:
    """
    Deleverage a facility by the specified amount.

    Args:
        context: Simulation context
        facility_id: Facility ID
        amount: Amount to deleverage
    """
    # Check if we have cash to deleverage
    available_cash = _calculate_available_cash(context)

    if available_cash < amount:
        logger.warning(
            "Insufficient cash to deleverage facility",
            facility_id=facility_id,
            amount=amount,
            available_cash=available_cash,
        )

        # Deleverage as much as possible
        amount = available_cash

    if amount <= 0:
        return

    # Recreate facility object from dict
    facility_data = context.leverage_facilities[facility_id]
    facility = LeverageFacility(**facility_data)

    # Repay facility
    actual_repayment = facility.repay(amount, datetime.now())

    # Record repayment
    repayment_event = {
        "facility_id": facility_id,
        "date": datetime.now(),
        "amount": actual_repayment,
        "year": getattr(context, "current_year", 0),
        "month": getattr(context, "current_month", 0),
        "source": "deleveraging",
    }

    context.leverage_repayments.append(repayment_event)

    # Update facility in context
    context.leverage_facilities[facility_id] = facility.__dict__

    logger.info(
        "Deleveraged facility",
        facility_id=facility_id,
        amount=actual_repayment,
    )


async def manage_leverage(context: SimulationContext) -> None:
    """
    Manage leverage for the simulation.

    This function is the main entry point for the leverage engine. It initializes
    debt facilities, processes leverage events, and checks borrowing base compliance.

    Args:
        context: Simulation context
    """
    logger.info("Starting leverage engine")

    # Get configuration
    config = context.config
    leverage_config = getattr(config, "leverage_engine", {})

    # Check if leverage is enabled
    if not leverage_config.get("enabled", False):
        logger.info("Leverage is disabled, skipping leverage engine")
        return

    # Initialize facilities if not already present
    if not hasattr(context, "leverage_facilities"):
        context.leverage_facilities = {}

        # Initialize facilities
        _initialize_facilities(context)

    # Process leverage events
    _process_leverage_events(context)

    # Check borrowing base compliance
    _check_borrowing_base_compliance(context)

    # Optimize leverage if enabled
    optimization_config = leverage_config.get("optimization", {})
    if optimization_config.get("enabled", True):
        _optimize_leverage(context)

    # Run stress tests if enabled
    stress_config = leverage_config.get("stress_testing", {})
    if stress_config.get("enabled", True):
        _run_stress_tests(context)

    # Generate visualization data
    _generate_visualization_data(context)

    # Send progress update via WebSocket
    websocket_manager = get_websocket_manager()
    if websocket_manager and hasattr(context, "run_id"):
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="leverage_engine",
            progress=100.0,
            message="Leverage engine completed",
            data={
                "metrics": getattr(context, "leverage_metrics", {}),
                "stress_test_results": getattr(context, "leverage_stress_test_results", {}),
            },
        )

    logger.info("Leverage engine completed")


def _optimize_leverage(context: SimulationContext) -> None:
    """
    Optimize leverage based on target leverage ratio.

    Args:
        context: Simulation context
    """
    # Get configuration
    config = context.config
    leverage_config = getattr(config, "leverage_engine", {})
    optimization_config = leverage_config.get("optimization", {})

    # Get target leverage ratio
    target_leverage = optimization_config.get("target_leverage", 0.5)
    max_leverage = optimization_config.get("max_leverage", 0.65)
    deleveraging_threshold = optimization_config.get("deleveraging_threshold", 0.7)

    # Calculate NAV
    nav = _calculate_nav(context)

    # Calculate current leverage ratio
    total_debt = sum(
        facility_data.get("current_balance", 0)
        for facility_data in context.leverage_facilities.values()
    )

    current_leverage_ratio = 0
    if nav > 0:
        current_leverage_ratio = total_debt / nav

    # Check if we need to deleverage
    if current_leverage_ratio > deleveraging_threshold:
        logger.info(
            "Deleveraging due to high leverage ratio",
            extra={
                "current_leverage": current_leverage_ratio,
                "threshold": deleveraging_threshold
            }
        )

        # Calculate amount to deleverage
        target_debt = nav * max_leverage
        deleverage_amount = total_debt - target_debt

        # Deleverage facilities
        # Preference order: NAV line first, then subscription line
        facilities_to_deleverage = []

        if "nav_line" in context.leverage_facilities:
            facilities_to_deleverage.append("nav_line")

        if "subscription_line" in context.leverage_facilities:
            facilities_to_deleverage.append("subscription_line")

        # Deleverage facilities in order
        remaining_deleverage = deleverage_amount

        for facility_id in facilities_to_deleverage:
            if remaining_deleverage <= 0:
                break

            # Recreate facility object from dict
            facility_data = context.leverage_facilities[facility_id]
            facility = LeverageFacility(**facility_data)

            # Check if facility has outstanding balance
            if facility.current_balance > 0:
                # Deleverage the lesser of remaining amount or current balance
                deleverage_facility_amount = min(remaining_deleverage, facility.current_balance)

                # Deleverage facility
                _deleverage_facility(context, facility_id, deleverage_facility_amount)

                # Update remaining deleverage amount
                remaining_deleverage -= deleverage_facility_amount

    # Check if we need to increase leverage
    elif current_leverage_ratio < target_leverage:
        logger.info(
            "Increasing leverage to target ratio",
            extra={
                "current_leverage": current_leverage_ratio,
                "target_leverage": target_leverage
            }
        )

        # Calculate amount to draw
        target_debt = nav * target_leverage
        draw_amount = target_debt - total_debt

        # Draw from facilities
        # Preference order: subscription line first, then NAV line
        facilities_to_draw = []

        if "subscription_line" in context.leverage_facilities:
            facilities_to_draw.append("subscription_line")

        if "nav_line" in context.leverage_facilities:
            facilities_to_draw.append("nav_line")

        # Draw from facilities in order
        remaining_draw = draw_amount
        current_year = getattr(context, "current_year", 0)
        current_month = getattr(context, "current_month", 0)

        for facility_id in facilities_to_draw:
            if remaining_draw <= 0:
                break

            # Recreate facility object from dict
            facility_data = context.leverage_facilities[facility_id]
            facility = LeverageFacility(**facility_data)

            # Check if facility has available capacity
            if facility.available_amount > 0:
                # Draw the lesser of remaining need or available amount
                facility_draw_amount = min(remaining_draw, facility.available_amount)

                # Draw from facility
                actual_draw = facility.draw(facility_draw_amount, datetime.now())

                # Update remaining draw
                remaining_draw -= actual_draw

                # Record draw
                draw_event = {
                    "facility_id": facility_id,
                    "date": datetime.now(),
                    "amount": actual_draw,
                    "year": current_year,
                    "month": current_month,
                    "purpose": "leverage_optimization",
                }

                context.leverage_draws.append(draw_event)

                # Update facility in context
                context.leverage_facilities[facility_id] = facility.__dict__


def _run_stress_tests(context: SimulationContext) -> None:
    """
    Run stress tests on leverage.

    Args:
        context: Simulation context
    """
    # Get configuration
    config = context.config
    leverage_config = getattr(config, "leverage_engine", {})
    stress_config = leverage_config.get("stress_testing", {})

    # Get stress test parameters
    interest_rate_shock = stress_config.get("interest_rate_shock", 0.02)
    nav_shock = stress_config.get("nav_shock", 0.2)
    liquidity_shock = stress_config.get("liquidity_shock", 0.5)

    # Create a copy of the context for stress testing
    stress_context = copy.deepcopy(context)

    # Apply interest rate shock
    for facility_id, facility_data in stress_context.leverage_facilities.items():
        facility_data["interest_rate"] += interest_rate_shock

    # Apply NAV shock
    original_nav = _calculate_nav(context)
    stress_context.nav_shock_factor = 1 - nav_shock

    # Apply liquidity shock
    original_cash = getattr(context, "cash", 0)
    stress_context.cash = original_cash * (1 - liquidity_shock)

    # Run stress tests
    stress_test_results = {}

    # Test 1: Interest rate shock impact
    interest_shock_results = _test_interest_rate_shock(stress_context, interest_rate_shock)
    stress_test_results["interest_rate_shock"] = interest_shock_results

    # Test 2: NAV shock impact
    nav_shock_results = _test_nav_shock(stress_context, nav_shock)
    stress_test_results["nav_shock"] = nav_shock_results

    # Test 3: Liquidity shock impact
    liquidity_shock_results = _test_liquidity_shock(stress_context, liquidity_shock)
    stress_test_results["liquidity_shock"] = liquidity_shock_results

    # Test 4: Combined shock impact
    combined_shock_results = _test_combined_shock(stress_context)
    stress_test_results["combined_shock"] = combined_shock_results

    # Store stress test results in context
    context.leverage_stress_test_results = stress_test_results

    # Log stress test results
    logger.info(
        "Leverage stress tests completed",
        extra={
            "interest_shock_compliant": interest_shock_results.get("is_compliant", False),
            "nav_shock_compliant": nav_shock_results.get("is_compliant", False),
            "liquidity_shock_compliant": liquidity_shock_results.get("is_compliant", False),
            "combined_shock_compliant": combined_shock_results.get("is_compliant", False)
        }
    )


def _test_interest_rate_shock(context: SimulationContext, shock_amount: float) -> Dict[str, Any]:
    """
    Test the impact of an interest rate shock.

    Args:
        context: Simulation context
        shock_amount: Interest rate shock amount

    Returns:
        Test results
    """
    # Calculate debt service before shock
    original_debt_service = sum(
        payment.get("amount", 0)
        for payment in context.leverage_interest_payments
    )

    # Calculate debt service after shock
    shocked_debt_service = 0
    for facility_id, facility_data in context.leverage_facilities.items():
        balance = facility_data.get("current_balance", 0)
        original_rate = facility_data.get("interest_rate", 0)
        shocked_rate = original_rate + shock_amount
        shocked_debt_service += balance * shocked_rate / 12  # Monthly interest

    # Calculate cash flow
    cash_flow = _calculate_cash_flow(context)

    # Calculate debt service coverage ratio
    dscr = 0
    if shocked_debt_service > 0:
        dscr = cash_flow / shocked_debt_service

    # Check if DSCR is compliant
    min_dscr = 1.2  # Minimum acceptable DSCR
    is_compliant = dscr >= min_dscr

    # Return results
    return {
        "original_debt_service": original_debt_service,
        "shocked_debt_service": shocked_debt_service,
        "cash_flow": cash_flow,
        "dscr": dscr,
        "min_dscr": min_dscr,
        "is_compliant": is_compliant,
        "shock_amount": shock_amount
    }


def _test_nav_shock(context: SimulationContext, shock_amount: float) -> Dict[str, Any]:
    """
    Test the impact of a NAV shock.

    Args:
        context: Simulation context
        shock_amount: NAV shock amount as percentage

    Returns:
        Test results
    """
    # Calculate original NAV
    original_nav = _calculate_nav(context)

    # Calculate shocked NAV
    shocked_nav = original_nav * (1 - shock_amount)

    # Calculate total debt
    total_debt = sum(
        facility_data.get("current_balance", 0)
        for facility_data in context.leverage_facilities.values()
    )

    # Calculate original leverage ratio
    original_leverage_ratio = 0
    if original_nav > 0:
        original_leverage_ratio = total_debt / original_nav

    # Calculate shocked leverage ratio
    shocked_leverage_ratio = 0
    if shocked_nav > 0:
        shocked_leverage_ratio = total_debt / shocked_nav

    # Check if leverage ratio is compliant
    max_leverage = 0.7  # Maximum acceptable leverage ratio
    is_compliant = shocked_leverage_ratio <= max_leverage

    # Return results
    return {
        "original_nav": original_nav,
        "shocked_nav": shocked_nav,
        "total_debt": total_debt,
        "original_leverage_ratio": original_leverage_ratio,
        "shocked_leverage_ratio": shocked_leverage_ratio,
        "max_leverage": max_leverage,
        "is_compliant": is_compliant,
        "shock_amount": shock_amount
    }


def _test_liquidity_shock(context: SimulationContext, shock_amount: float) -> Dict[str, Any]:
    """
    Test the impact of a liquidity shock.

    Args:
        context: Simulation context
        shock_amount: Liquidity shock amount as percentage

    Returns:
        Test results
    """
    # Get original cash
    original_cash = getattr(context, "cash", 0)

    # Calculate shocked cash
    shocked_cash = original_cash * (1 - shock_amount)

    # Calculate debt service
    debt_service = sum(
        payment.get("amount", 0)
        for payment in context.leverage_interest_payments
    ) + sum(
        fee.get("amount", 0)
        for fee in context.leverage_commitment_fees
    )

    # Calculate liquidity coverage ratio
    original_lcr = 0
    if debt_service > 0:
        original_lcr = original_cash / debt_service

    shocked_lcr = 0
    if debt_service > 0:
        shocked_lcr = shocked_cash / debt_service

    # Check if liquidity coverage ratio is compliant
    min_lcr = 1.0  # Minimum acceptable liquidity coverage ratio
    is_compliant = shocked_lcr >= min_lcr

    # Return results
    return {
        "original_cash": original_cash,
        "shocked_cash": shocked_cash,
        "debt_service": debt_service,
        "original_lcr": original_lcr,
        "shocked_lcr": shocked_lcr,
        "min_lcr": min_lcr,
        "is_compliant": is_compliant,
        "shock_amount": shock_amount
    }


def _test_combined_shock(context: SimulationContext) -> Dict[str, Any]:
    """
    Test the impact of combined shocks.

    Args:
        context: Simulation context

    Returns:
        Test results
    """
    # Get configuration
    config = context.config
    leverage_config = getattr(config, "leverage_engine", {})
    stress_config = leverage_config.get("stress_testing", {})

    # Get stress test parameters
    interest_rate_shock = stress_config.get("interest_rate_shock", 0.02)
    nav_shock = stress_config.get("nav_shock", 0.2)
    liquidity_shock = stress_config.get("liquidity_shock", 0.5)

    # Calculate original NAV
    original_nav = _calculate_nav(context)

    # Calculate shocked NAV
    shocked_nav = original_nav * (1 - nav_shock)

    # Calculate total debt
    total_debt = sum(
        facility_data.get("current_balance", 0)
        for facility_data in context.leverage_facilities.values()
    )

    # Calculate shocked leverage ratio
    shocked_leverage_ratio = 0
    if shocked_nav > 0:
        shocked_leverage_ratio = total_debt / shocked_nav

    # Calculate shocked debt service
    shocked_debt_service = 0
    for facility_id, facility_data in context.leverage_facilities.items():
        balance = facility_data.get("current_balance", 0)
        original_rate = facility_data.get("interest_rate", 0)
        shocked_rate = original_rate + interest_rate_shock
        shocked_debt_service += balance * shocked_rate / 12  # Monthly interest

    # Get original cash
    original_cash = getattr(context, "cash", 0)

    # Calculate shocked cash
    shocked_cash = original_cash * (1 - liquidity_shock)

    # Calculate shocked liquidity coverage ratio
    shocked_lcr = 0
    if shocked_debt_service > 0:
        shocked_lcr = shocked_cash / shocked_debt_service

    # Check if combined shock is compliant
    max_leverage = 0.7  # Maximum acceptable leverage ratio
    min_lcr = 1.0  # Minimum acceptable liquidity coverage ratio

    leverage_compliant = shocked_leverage_ratio <= max_leverage
    liquidity_compliant = shocked_lcr >= min_lcr
    is_compliant = leverage_compliant and liquidity_compliant

    # Return results
    return {
        "shocked_nav": shocked_nav,
        "total_debt": total_debt,
        "shocked_leverage_ratio": shocked_leverage_ratio,
        "max_leverage": max_leverage,
        "leverage_compliant": leverage_compliant,
        "shocked_debt_service": shocked_debt_service,
        "shocked_cash": shocked_cash,
        "shocked_lcr": shocked_lcr,
        "min_lcr": min_lcr,
        "liquidity_compliant": liquidity_compliant,
        "is_compliant": is_compliant,
        "interest_rate_shock": interest_rate_shock,
        "nav_shock": nav_shock,
        "liquidity_shock": liquidity_shock
    }


def _generate_visualization_data(context: SimulationContext) -> None:
    """
    Generate visualization data for leverage.

    Args:
        context: Simulation context
    """
    # Ensure visualization data is initialized
    if not hasattr(context, "leverage_visualization"):
        context.leverage_visualization = {}

    # Add timeline data
    context.leverage_visualization["leverage_timeline"] = getattr(context, "leverage_timeline", [])

    # Add facility utilization data
    context.leverage_visualization["facility_utilization"] = getattr(context, "facility_utilization", [])

    # Calculate interest expense over time
    interest_payments = getattr(context, "leverage_interest_payments", [])
    commitment_fees = getattr(context, "leverage_commitment_fees", [])

    # Group by year and month
    interest_by_period = {}
    for payment in interest_payments:
        year = payment.get("year", 0)
        month = payment.get("month", 0)
        key = (year, month)

        if key not in interest_by_period:
            interest_by_period[key] = {
                "year": year,
                "month": month,
                "interest_amount": 0,
                "commitment_fees": 0,
                "total_expense": 0,
            }

        interest_by_period[key]["interest_amount"] += payment.get("amount", 0)
        interest_by_period[key]["total_expense"] += payment.get("amount", 0)

    for fee in commitment_fees:
        year = fee.get("year", 0)
        month = fee.get("month", 0)
        key = (year, month)

        if key not in interest_by_period:
            interest_by_period[key] = {
                "year": year,
                "month": month,
                "interest_amount": 0,
                "commitment_fees": 0,
                "total_expense": 0,
            }

        interest_by_period[key]["commitment_fees"] += fee.get("amount", 0)
        interest_by_period[key]["total_expense"] += fee.get("amount", 0)

    # Convert to list and sort by year and month
    interest_expense = sorted(
        interest_by_period.values(),
        key=lambda x: (x["year"], x["month"])
    )

    context.leverage_visualization["interest_expense"] = interest_expense

    # Add stress test visualization
    if hasattr(context, "leverage_stress_test_results"):
        stress_test_results = context.leverage_stress_test_results

        # Create stress test visualization
        stress_test_visualization = {
            "interest_rate_shock": {
                "original_debt_service": stress_test_results.get("interest_rate_shock", {}).get("original_debt_service", 0),
                "shocked_debt_service": stress_test_results.get("interest_rate_shock", {}).get("shocked_debt_service", 0),
                "dscr": stress_test_results.get("interest_rate_shock", {}).get("dscr", 0),
                "is_compliant": stress_test_results.get("interest_rate_shock", {}).get("is_compliant", False),
            },
            "nav_shock": {
                "original_leverage_ratio": stress_test_results.get("nav_shock", {}).get("original_leverage_ratio", 0),
                "shocked_leverage_ratio": stress_test_results.get("nav_shock", {}).get("shocked_leverage_ratio", 0),
                "is_compliant": stress_test_results.get("nav_shock", {}).get("is_compliant", False),
            },
            "liquidity_shock": {
                "original_lcr": stress_test_results.get("liquidity_shock", {}).get("original_lcr", 0),
                "shocked_lcr": stress_test_results.get("liquidity_shock", {}).get("shocked_lcr", 0),
                "is_compliant": stress_test_results.get("liquidity_shock", {}).get("is_compliant", False),
            },
            "combined_shock": {
                "shocked_leverage_ratio": stress_test_results.get("combined_shock", {}).get("shocked_leverage_ratio", 0),
                "shocked_lcr": stress_test_results.get("combined_shock", {}).get("shocked_lcr", 0),
                "is_compliant": stress_test_results.get("combined_shock", {}).get("is_compliant", False),
            },
        }

        context.leverage_visualization["stress_tests"] = stress_test_visualization
