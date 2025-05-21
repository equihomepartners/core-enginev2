"""
Leverage manager module for the EQU IHOME SIM ENGINE v2.

This module is responsible for managing debt facilities, calculating interest,
and enforcing borrowing base tests.
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

import structlog

from src.engine.simulation_context import SimulationContext

logger = structlog.get_logger(__name__)


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


def _process_leverage_events(context: SimulationContext) -> None:
    """
    Process leverage events (draws, repayments, interest).
    
    Args:
        context: Simulation context
    """
    # TODO: Implement leverage event processing
    # This would involve:
    # 1. Determining when to draw from facilities
    # 2. Calculating interest payments
    # 3. Determining when to repay facilities
    pass


def _check_borrowing_base_compliance(context: SimulationContext) -> None:
    """
    Check borrowing base compliance for all facilities.
    
    Args:
        context: Simulation context
    """
    # TODO: Implement borrowing base compliance checks
    # This would involve:
    # 1. Calculating NAV
    # 2. Checking each facility against its borrowing base
    pass
