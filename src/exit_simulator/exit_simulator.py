"""
Exit simulator module for the EQU IHOME SIM ENGINE v2.

This module simulates how and when loans exit the portfolio, including
property sales, refinancing, defaults, and term completions.
"""

import time
from typing import Dict, Any, List, Optional, Tuple, Union, Callable
from enum import Enum

import numpy as np
import structlog
from scipy import stats

from src.engine.simulation_context import SimulationContext
from src.monte_carlo.rng_factory import get_rng
from src.api.websocket_manager import get_websocket_manager
from src.utils.error_handler import handle_exception, log_error
from src.utils.metrics import increment_counter, observe_histogram, set_gauge
from src.tls_module.tls_core import MetricCategory
from src.tls_module import get_tls_manager
from src.price_path.enhanced_price_path import calculate_enhanced_property_value

logger = structlog.get_logger(__name__)


class ExitType(Enum):
    """Exit type enum."""
    SALE = "sale"
    REFINANCE = "refinance"
    DEFAULT = "default"
    TERM_COMPLETION = "term_completion"


# Default parameters
DEFAULT_BASE_EXIT_RATE = 0.1  # 10% annual exit rate
DEFAULT_TIME_FACTOR = 0.4  # Weight for time-based exit probability
DEFAULT_PRICE_FACTOR = 0.6  # Weight for price-based exit probability
DEFAULT_MIN_HOLD_PERIOD = 1.0  # Minimum holding period in years
DEFAULT_MAX_HOLD_PERIOD = 10.0  # Maximum holding period in years

DEFAULT_SALE_WEIGHT = 0.6  # Base weight for sale exits
DEFAULT_REFINANCE_WEIGHT = 0.3  # Base weight for refinance exits
DEFAULT_DEFAULT_WEIGHT = 0.1  # Base weight for default exits
DEFAULT_APPRECIATION_SALE_MULTIPLIER = 2.0  # How much appreciation increases sale probability
DEFAULT_INTEREST_RATE_REFINANCE_MULTIPLIER = 3.0  # How much interest rate changes affect refinance probability
DEFAULT_ECONOMIC_FACTOR_DEFAULT_MULTIPLIER = 2.0  # How much economic factors affect default probability

DEFAULT_APPRECIATION_SHARE = 0.2  # Fund's share of appreciation
DEFAULT_MIN_APPRECIATION_SHARE = 0.1  # Minimum appreciation share
DEFAULT_MAX_APPRECIATION_SHARE = 0.5  # Maximum appreciation share
DEFAULT_TIERED_APPRECIATION_THRESHOLDS = [0.2, 0.5, 1.0]  # Thresholds for tiered appreciation sharing
DEFAULT_TIERED_APPRECIATION_SHARES = [0.1, 0.2, 0.3, 0.4]  # Shares for tiered appreciation sharing

DEFAULT_BASE_DEFAULT_RATE = 0.01  # 1% annual default rate
DEFAULT_RECOVERY_RATE = 0.8  # 80% recovery rate in case of default
DEFAULT_FORECLOSURE_COST = 0.1  # 10% foreclosure cost
DEFAULT_FORECLOSURE_TIME = 1.0  # 1 year to complete foreclosure


async def simulate_exits(context: SimulationContext) -> None:
    """
    Simulate exits for all loans in the portfolio.

    This function simulates when and how loans exit the portfolio, including
    property sales, refinancing, defaults, and term completions.

    Args:
        context: Simulation context

    Raises:
        ValueError: If the configuration parameters are invalid
    """
    start_time = time.time()
    logger.info("Simulating exits")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="exit_simulator",
            progress=0.0,
            message="Starting exit simulation",
        )

        # Get configuration parameters
        config = context.config

        # Get random number generator
        if context.rng is None:
            context.rng = get_rng("exit_simulator", 0)

        # Get exit simulator configuration
        exit_config = getattr(config, "exit_simulator", {})

        # Get base exit rate
        base_exit_rate = getattr(exit_config, "base_exit_rate", DEFAULT_BASE_EXIT_RATE)

        # Get time factor
        time_factor = getattr(exit_config, "time_factor", DEFAULT_TIME_FACTOR)

        # Get price factor
        price_factor = getattr(exit_config, "price_factor", DEFAULT_PRICE_FACTOR)

        # Get min hold period
        min_hold_period = getattr(exit_config, "min_hold_period", DEFAULT_MIN_HOLD_PERIOD)

        # Get max hold period
        max_hold_period = getattr(exit_config, "max_hold_period", DEFAULT_MAX_HOLD_PERIOD)

        # Get sale weight
        sale_weight = getattr(exit_config, "sale_weight", DEFAULT_SALE_WEIGHT)

        # Get refinance weight
        refinance_weight = getattr(exit_config, "refinance_weight", DEFAULT_REFINANCE_WEIGHT)

        # Get default weight
        default_weight = getattr(exit_config, "default_weight", DEFAULT_DEFAULT_WEIGHT)

        # Get appreciation sale multiplier
        appreciation_sale_multiplier = getattr(
            exit_config, "appreciation_sale_multiplier", DEFAULT_APPRECIATION_SALE_MULTIPLIER
        )

        # Get interest rate refinance multiplier
        interest_rate_refinance_multiplier = getattr(
            exit_config, "interest_rate_refinance_multiplier", DEFAULT_INTEREST_RATE_REFINANCE_MULTIPLIER
        )

        # Get economic factor default multiplier
        economic_factor_default_multiplier = getattr(
            exit_config, "economic_factor_default_multiplier", DEFAULT_ECONOMIC_FACTOR_DEFAULT_MULTIPLIER
        )

        # Get appreciation share
        appreciation_share = getattr(exit_config, "appreciation_share", DEFAULT_APPRECIATION_SHARE)

        # Get min appreciation share
        min_appreciation_share = getattr(exit_config, "min_appreciation_share", DEFAULT_MIN_APPRECIATION_SHARE)

        # Get max appreciation share
        max_appreciation_share = getattr(exit_config, "max_appreciation_share", DEFAULT_MAX_APPRECIATION_SHARE)

        # Get tiered appreciation thresholds
        tiered_appreciation_thresholds = getattr(
            exit_config, "tiered_appreciation_thresholds", DEFAULT_TIERED_APPRECIATION_THRESHOLDS
        )

        # Get tiered appreciation shares
        tiered_appreciation_shares = getattr(
            exit_config, "tiered_appreciation_shares", DEFAULT_TIERED_APPRECIATION_SHARES
        )

        # Get base default rate
        base_default_rate = getattr(exit_config, "base_default_rate", DEFAULT_BASE_DEFAULT_RATE)

        # Get recovery rate
        recovery_rate = getattr(exit_config, "recovery_rate", DEFAULT_RECOVERY_RATE)

        # Get foreclosure cost
        foreclosure_cost = getattr(exit_config, "foreclosure_cost", DEFAULT_FORECLOSURE_COST)

        # Get foreclosure time
        foreclosure_time = getattr(exit_config, "foreclosure_time", DEFAULT_FORECLOSURE_TIME)

        # Get fund term
        fund_term = getattr(config, "fund_term", 10)

        # Get time step
        price_path_config = getattr(config, "price_path", {})
        time_step = getattr(price_path_config, "time_step", "monthly")

        # Determine number of time steps
        if time_step == "monthly":
            num_steps = fund_term * 12
            dt = 1.0 / 12.0
        elif time_step == "quarterly":
            num_steps = fund_term * 4
            dt = 1.0 / 4.0
        else:  # yearly
            num_steps = fund_term
            dt = 1.0

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="exit_simulator",
            progress=10.0,
            message="Preparing exit simulation",
            data={
                "base_exit_rate": base_exit_rate,
                "time_factor": time_factor,
                "price_factor": price_factor,
                "min_hold_period": min_hold_period,
                "max_hold_period": max_hold_period,
                "fund_term": fund_term,
                "num_steps": num_steps,
            },
        )

        # Get loans
        loans = context.loans

        # Get price paths
        price_paths = getattr(context, "price_paths", None)
        if price_paths is None:
            raise ValueError("Price paths not found in context")

        # Get TLS manager
        tls_manager = get_tls_manager()

        # Load TLS data if not already loaded
        if not tls_manager.data_loaded:
            await tls_manager.load_data(simulation_id=context.run_id)

        # Initialize exits
        exits = []

        # Simulate exits for each loan
        for i, loan in enumerate(loans):
            # Get loan details
            loan_id = loan.get("loan_id", "")
            property_id = loan.get("property_id", "")
            suburb_id = loan.get("suburb_id", "")
            zone = loan.get("zone", "green")
            loan_amount = loan.get("loan_size", 0.0)  # Use loan_size from loan generator
            property_value = loan.get("property_value", 0.0)
            ltv = loan.get("ltv", 0.0)
            loan_term = loan.get("term", 10.0)  # Use term from loan generator
            interest_rate = loan.get("interest_rate", 0.05)
            origination_date = loan.get("origination_year", 0)  # Use origination_year from loan generator

            # Skip if loan ID is missing
            if not loan_id:
                continue

            # Simulate exit for this loan
            exit_month, exit_type, exit_value, appreciation_share_amount = simulate_loan_exit(
                loan=loan,
                price_paths=price_paths,
                base_exit_rate=base_exit_rate,
                time_factor=time_factor,
                price_factor=price_factor,
                min_hold_period=min_hold_period,
                max_hold_period=max_hold_period,
                sale_weight=sale_weight,
                refinance_weight=refinance_weight,
                default_weight=default_weight,
                appreciation_sale_multiplier=appreciation_sale_multiplier,
                interest_rate_refinance_multiplier=interest_rate_refinance_multiplier,
                economic_factor_default_multiplier=economic_factor_default_multiplier,
                appreciation_share=appreciation_share,
                min_appreciation_share=min_appreciation_share,
                max_appreciation_share=max_appreciation_share,
                tiered_appreciation_thresholds=tiered_appreciation_thresholds,
                tiered_appreciation_shares=tiered_appreciation_shares,
                base_default_rate=base_default_rate,
                recovery_rate=recovery_rate,
                foreclosure_cost=foreclosure_cost,
                foreclosure_time=foreclosure_time,
                num_steps=num_steps,
                dt=dt,
                rng=context.rng,
                tls_manager=tls_manager,
            )

            # Calculate exit year
            exit_year = exit_month * dt

            # Store exit
            exits.append({
                "loan_id": loan_id,
                "property_id": property_id,
                "suburb_id": suburb_id,
                "zone": zone,
                "loan_amount": loan_amount,
                "property_value": property_value,
                "ltv": ltv,
                "loan_term": loan_term,
                "interest_rate": interest_rate,
                "origination_date": origination_date,
                "exit_month": exit_month,
                "exit_year": exit_year,
                "exit_type": exit_type.value,
                "exit_value": exit_value,
                "appreciation_share_amount": appreciation_share_amount,
                "total_return": exit_value + appreciation_share_amount,
                "roi": (exit_value + appreciation_share_amount - loan_amount) / loan_amount if loan_amount > 0 else 0.0,
                "annualized_roi": ((exit_value + appreciation_share_amount) / loan_amount) ** (1 / exit_year) - 1 if exit_year > 0 and loan_amount > 0 else 0.0,
            })

            # Update the loan object with exit information
            loan["exit_month"] = exit_month
            loan["exit_year"] = exit_year
            loan["exit_type"] = exit_type.value
            loan["exit_value"] = exit_value
            loan["appreciation_share_amount"] = appreciation_share_amount
            loan["total_return"] = exit_value + appreciation_share_amount
            loan["roi"] = (exit_value + appreciation_share_amount - loan_amount) / loan_amount if loan_amount > 0 else 0.0
            loan["annualized_roi"] = ((exit_value + appreciation_share_amount) / loan_amount) ** (1 / exit_year) - 1 if exit_year > 0 and loan_amount > 0 else 0.0

            # Report progress periodically
            if i % 100 == 0 or i == len(loans) - 1:
                await websocket_manager.send_progress(
                    simulation_id=context.run_id,
                    module="exit_simulator",
                    progress=10.0 + (i / len(loans)) * 70.0,
                    message=f"Simulated exit for loan {i+1} of {len(loans)}",
                )

        # Store exits in context as both list and dictionary for compatibility
        context.exits = exits

        # Also store as dictionary keyed by loan_id for cashflow aggregator
        exits_dict = {exit["loan_id"]: exit for exit in exits}
        context.exits_dict = exits_dict

        # Calculate exit statistics
        exit_stats = calculate_exit_statistics(exits, num_steps, dt)

        # Store exit statistics in context
        context.exit_stats = exit_stats

        # Generate exit visualization
        exit_visualization = generate_exit_visualization(exits, exit_stats, num_steps, dt)

        # Store exit visualization in context
        context.exit_visualization = exit_visualization

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="exit_simulator",
            progress=100.0,
            message="Exit simulation completed",
            data={
                "num_exits": len(exits),
                "avg_exit_year": exit_stats["avg_exit_year"],
                "avg_roi": exit_stats["avg_roi"],
                "exit_type_distribution": exit_stats["exit_type_distribution"],
            },
        )

        # Update metrics
        increment_counter("exit_simulations_completed_total")
        observe_histogram(
            "exit_simulation_runtime_seconds",
            time.time() - start_time,
        )

        # Log completion
        logger.info(
            "Exit simulation completed",
            num_exits=len(exits),
            avg_exit_year=exit_stats["avg_exit_year"],
            avg_roi=exit_stats["avg_roi"],
            runtime=time.time() - start_time,
        )

    except Exception as e:
        # Handle exception
        error = handle_exception(e)

        # Log error
        log_error(error)

        # Report error
        await websocket_manager.send_error(
            simulation_id=context.run_id,
            error={
                "message": str(error),
                "code": error.code,
                "module": "exit_simulator",
            },
        )

        # Update metrics
        increment_counter("exit_simulations_failed_total")

        # Re-raise exception
        raise


def simulate_loan_exit(
    loan: Dict[str, Any],
    price_paths: Dict[str, Any],
    base_exit_rate: float,
    time_factor: float,
    price_factor: float,
    min_hold_period: float,
    max_hold_period: float,
    sale_weight: float,
    refinance_weight: float,
    default_weight: float,
    appreciation_sale_multiplier: float,
    interest_rate_refinance_multiplier: float,
    economic_factor_default_multiplier: float,
    appreciation_share: float,
    min_appreciation_share: float,
    max_appreciation_share: float,
    tiered_appreciation_thresholds: List[float],
    tiered_appreciation_shares: List[float],
    base_default_rate: float,
    recovery_rate: float,
    foreclosure_cost: float,
    foreclosure_time: float,
    num_steps: int,
    dt: float,
    rng: np.random.Generator,
    tls_manager: Any,
) -> Tuple[int, ExitType, float, float]:
    """
    Simulate exit for a single loan.

    Args:
        loan: Loan details
        price_paths: Price paths
        base_exit_rate: Base annual exit probability
        time_factor: Weight for time-based exit probability
        price_factor: Weight for price-based exit probability
        min_hold_period: Minimum holding period in years
        max_hold_period: Maximum holding period in years
        sale_weight: Base weight for sale exits
        refinance_weight: Base weight for refinance exits
        default_weight: Base weight for default exits
        appreciation_sale_multiplier: How much appreciation increases sale probability
        interest_rate_refinance_multiplier: How much interest rate changes affect refinance probability
        economic_factor_default_multiplier: How much economic factors affect default probability
        appreciation_share: Fund's share of appreciation
        min_appreciation_share: Minimum appreciation share
        max_appreciation_share: Maximum appreciation share
        tiered_appreciation_thresholds: Thresholds for tiered appreciation sharing
        tiered_appreciation_shares: Shares for tiered appreciation sharing
        base_default_rate: Base annual default probability
        recovery_rate: Recovery rate in case of default
        foreclosure_cost: Cost of foreclosure as percentage of property value
        foreclosure_time: Time to complete foreclosure in years
        num_steps: Number of time steps
        dt: Time step size (in years)
        rng: Random number generator
        tls_manager: TLS data manager

    Returns:
        Tuple of (exit_month, exit_type, exit_value, appreciation_share_amount)
    """
    # Get loan details
    loan_id = loan.get("loan_id", "")
    property_id = loan.get("property_id", "")
    suburb_id = loan.get("suburb_id", "")
    zone = loan.get("zone", "green")
    loan_amount = loan.get("loan_size", 0.0)  # Use loan_size from loan generator
    property_value = loan.get("property_value", 0.0)
    ltv = loan.get("ltv", 0.0)
    loan_term = loan.get("term", 10.0)  # Use term from loan generator
    interest_rate = loan.get("interest_rate", 0.05)
    origination_date = loan.get("origination_year", 0)  # Use origination_year from loan generator

    # Convert loan term to months
    loan_term_months = int(loan_term * 12)

    # Convert min and max hold periods to months
    min_hold_period_months = int(min_hold_period * 12)
    max_hold_period_months = int(max_hold_period * 12)

    # Ensure max hold period doesn't exceed loan term
    max_hold_period_months = min(max_hold_period_months, loan_term_months)

    # Ensure max hold period doesn't exceed simulation length
    max_hold_period_months = min(max_hold_period_months, num_steps)

    # Initialize exit month to loan term (default to term completion)
    exit_month = loan_term_months

    # Ensure exit month doesn't exceed simulation length
    exit_month = min(exit_month, num_steps)

    # Initialize exit type to term completion
    exit_type = ExitType.TERM_COMPLETION

    # Get suburb data
    suburb = tls_manager.suburbs.get(suburb_id)

    # Get economic metrics for this suburb
    economic_factor = 1.0
    if suburb:
        economic_metrics = []
        for metric_name, metric_value in suburb.metrics.items():
            metric = tls_manager.metrics.get(metric_name)
            if metric and metric.category == MetricCategory.ECONOMIC:
                economic_metrics.append(metric_value.value)

        if economic_metrics:
            economic_factor = np.mean(economic_metrics)

    # Adjust default rate based on economic factor
    adjusted_default_rate = base_default_rate * (2.0 - economic_factor) * economic_factor_default_multiplier

    # Simulate exit for each month
    for month in range(min_hold_period_months, max_hold_period_months + 1):
        # Skip if month exceeds simulation length
        if month >= num_steps:
            break

        # Calculate time-based exit probability
        time_based_prob = base_exit_rate * dt

        # Calculate price-based exit probability
        price_based_prob = 0.0

        # Get current property value
        current_value = calculate_enhanced_property_value(
            initial_value=property_value,
            price_paths=price_paths,
            zone=zone,
            suburb_id=suburb_id,
            property_id=property_id,
            month=month,
        )

        # Calculate appreciation
        appreciation = (current_value / property_value) - 1.0 if property_value > 0 else 0.0

        # Adjust price-based probability based on appreciation
        if appreciation > 0:
            price_based_prob = base_exit_rate * dt * (1.0 + appreciation * appreciation_sale_multiplier)
        else:
            price_based_prob = base_exit_rate * dt * (1.0 + appreciation)

        # Calculate combined exit probability
        exit_prob = (time_based_prob * time_factor) + (price_based_prob * price_factor)

        # Generate random number
        r = rng.random()

        # Check if exit occurs
        if r < exit_prob:
            # Exit occurs at this month
            exit_month = month

            # Determine exit type
            exit_type = determine_exit_type(
                loan=loan,
                current_value=current_value,
                appreciation=appreciation,
                month=month,
                economic_factor=economic_factor,
                sale_weight=sale_weight,
                refinance_weight=refinance_weight,
                default_weight=default_weight,
                appreciation_sale_multiplier=appreciation_sale_multiplier,
                interest_rate_refinance_multiplier=interest_rate_refinance_multiplier,
                economic_factor_default_multiplier=economic_factor_default_multiplier,
                adjusted_default_rate=adjusted_default_rate,
                rng=rng,
            )

            break

    # Calculate exit value and appreciation share
    exit_value, appreciation_share_amount = calculate_exit_value(
        loan=loan,
        exit_month=exit_month,
        exit_type=exit_type,
        price_paths=price_paths,
        appreciation_share=appreciation_share,
        min_appreciation_share=min_appreciation_share,
        max_appreciation_share=max_appreciation_share,
        tiered_appreciation_thresholds=tiered_appreciation_thresholds,
        tiered_appreciation_shares=tiered_appreciation_shares,
        recovery_rate=recovery_rate,
        foreclosure_cost=foreclosure_cost,
    )

    return exit_month, exit_type, exit_value, appreciation_share_amount


def determine_exit_type(
    loan: Dict[str, Any],
    current_value: float,
    appreciation: float,
    month: int,
    economic_factor: float,
    sale_weight: float,
    refinance_weight: float,
    default_weight: float,
    appreciation_sale_multiplier: float,
    interest_rate_refinance_multiplier: float,
    economic_factor_default_multiplier: float,
    adjusted_default_rate: float,
    rng: np.random.Generator,
) -> ExitType:
    """
    Determine the type of exit.

    Args:
        loan: Loan details
        current_value: Current property value
        appreciation: Property appreciation
        month: Current month
        economic_factor: Economic factor
        sale_weight: Base weight for sale exits
        refinance_weight: Base weight for refinance exits
        default_weight: Base weight for default exits
        appreciation_sale_multiplier: How much appreciation increases sale probability
        interest_rate_refinance_multiplier: How much interest rate changes affect refinance probability
        economic_factor_default_multiplier: How much economic factors affect default probability
        adjusted_default_rate: Adjusted default rate
        rng: Random number generator

    Returns:
        Exit type
    """
    # Get loan details
    loan_amount = loan.get("loan_size", 0.0)  # Use loan_size from loan generator
    property_value = loan.get("property_value", 0.0)
    ltv = loan.get("ltv", 0.0)
    interest_rate = loan.get("interest_rate", 0.05)

    # Calculate current LTV
    current_ltv = loan_amount / current_value if current_value > 0 else 1.0

    # Adjust sale weight based on appreciation
    adjusted_sale_weight = sale_weight
    if appreciation > 0:
        adjusted_sale_weight *= (1.0 + appreciation * appreciation_sale_multiplier)

    # Adjust refinance weight based on interest rate and LTV
    adjusted_refinance_weight = refinance_weight
    if current_ltv < 0.8:  # More likely to refinance if LTV is low
        adjusted_refinance_weight *= (1.0 + (0.8 - current_ltv) * interest_rate_refinance_multiplier)

    # Adjust default weight based on economic factor and LTV
    adjusted_default_weight = default_weight
    if current_ltv > 0.9:  # More likely to default if LTV is high
        adjusted_default_weight *= (1.0 + (current_ltv - 0.9) * 10.0)

    # Check for default first (separate probability)
    default_prob = adjusted_default_rate * (2.0 - economic_factor) * economic_factor_default_multiplier
    if rng.random() < default_prob:
        return ExitType.DEFAULT

    # Calculate total weight
    total_weight = adjusted_sale_weight + adjusted_refinance_weight

    # Generate random number
    r = rng.random() * total_weight

    # Determine exit type
    if r < adjusted_sale_weight:
        return ExitType.SALE
    else:
        return ExitType.REFINANCE


def calculate_exit_value(
    loan: Dict[str, Any],
    exit_month: int,
    exit_type: ExitType,
    price_paths: Dict[str, Any],
    appreciation_share: float,
    min_appreciation_share: float,
    max_appreciation_share: float,
    tiered_appreciation_thresholds: List[float],
    tiered_appreciation_shares: List[float],
    recovery_rate: float,
    foreclosure_cost: float,
) -> Tuple[float, float]:
    """
    Calculate the exit value and appreciation share.

    Args:
        loan: Loan details
        exit_month: Exit month
        exit_type: Exit type
        price_paths: Price paths
        appreciation_share: Fund's share of appreciation
        min_appreciation_share: Minimum appreciation share
        max_appreciation_share: Maximum appreciation share
        tiered_appreciation_thresholds: Thresholds for tiered appreciation sharing
        tiered_appreciation_shares: Shares for tiered appreciation sharing
        recovery_rate: Recovery rate in case of default
        foreclosure_cost: Cost of foreclosure as percentage of property value

    Returns:
        Tuple of (exit_value, appreciation_share_amount)
    """
    # Get loan details
    loan_id = loan.get("loan_id", "")
    property_id = loan.get("property_id", "")
    suburb_id = loan.get("suburb_id", "")
    zone = loan.get("zone", "green")
    loan_amount = loan.get("loan_size", 0.0)  # Use loan_size from loan generator
    property_value = loan.get("property_value", 0.0)

    # Get current property value
    current_value = calculate_enhanced_property_value(
        initial_value=property_value,
        price_paths=price_paths,
        zone=zone,
        suburb_id=suburb_id,
        property_id=property_id,
        month=exit_month,
    )

    # Calculate appreciation
    appreciation = (current_value / property_value) - 1.0 if property_value > 0 else 0.0

    # Initialize exit value and appreciation share amount
    exit_value = loan_amount
    appreciation_share_amount = 0.0

    if exit_type == ExitType.DEFAULT:
        # Calculate recovery value
        recovery_value = current_value * recovery_rate * (1.0 - foreclosure_cost)

        # Exit value is the recovery value, capped at loan amount
        exit_value = min(recovery_value, loan_amount)

        # No appreciation share in case of default
        appreciation_share_amount = 0.0
    else:
        # Exit value is the loan amount
        exit_value = loan_amount

        # Calculate appreciation share amount
        if appreciation > 0:
            # Determine appreciation share based on tiered thresholds
            if tiered_appreciation_thresholds and tiered_appreciation_shares:
                # Find the appropriate tier
                tier_index = 0
                for i, threshold in enumerate(tiered_appreciation_thresholds):
                    if appreciation > threshold:
                        tier_index = i + 1

                # Get appreciation share for this tier
                if tier_index < len(tiered_appreciation_shares):
                    tiered_share = tiered_appreciation_shares[tier_index]

                    # Ensure share is within bounds
                    tiered_share = max(min_appreciation_share, min(max_appreciation_share, tiered_share))

                    # Calculate appreciation share amount
                    appreciation_share_amount = current_value * appreciation * tiered_share
            else:
                # Use flat appreciation share
                appreciation_share_amount = current_value * appreciation * appreciation_share

    return exit_value, appreciation_share_amount


def calculate_exit_statistics(
    exits: List[Dict[str, Any]],
    num_steps: int,
    dt: float,
) -> Dict[str, Any]:
    """
    Calculate statistics for exits.

    Args:
        exits: List of exits
        num_steps: Number of time steps
        dt: Time step size (in years)

    Returns:
        Dictionary containing exit statistics
    """
    # Skip if no exits
    if not exits:
        return {
            "avg_exit_year": 0.0,
            "avg_roi": 0.0,
            "avg_annualized_roi": 0.0,
            "exit_type_distribution": {},
            "exit_timing_distribution": {},
            "exit_roi_distribution": {},
            "exit_type_roi": {},
            "cumulative_exits": [],
            "exit_value_total": 0.0,
            "appreciation_share_total": 0.0,
            "total_return": 0.0,
            "total_roi": 0.0,
            "annualized_roi": 0.0,
        }

    # Calculate average exit year
    avg_exit_year = np.mean([exit["exit_year"] for exit in exits])

    # Calculate average ROI
    avg_roi = np.mean([exit["roi"] for exit in exits])

    # Calculate average annualized ROI
    avg_annualized_roi = np.mean([exit["annualized_roi"] for exit in exits])

    # Calculate exit type distribution
    exit_types = [exit["exit_type"] for exit in exits]
    exit_type_counts = {}
    for exit_type in exit_types:
        if exit_type not in exit_type_counts:
            exit_type_counts[exit_type] = 0
        exit_type_counts[exit_type] += 1

    exit_type_distribution = {
        exit_type: count / len(exits) for exit_type, count in exit_type_counts.items()
    }

    # Calculate exit timing distribution
    exit_years = [exit["exit_year"] for exit in exits]
    exit_year_bins = np.linspace(0, num_steps * dt, 20)
    exit_year_hist, _ = np.histogram(exit_years, bins=exit_year_bins)

    exit_timing_distribution = {
        f"{exit_year_bins[i]:.1f}-{exit_year_bins[i+1]:.1f}": int(exit_year_hist[i])
        for i in range(len(exit_year_hist))
    }

    # Calculate exit ROI distribution
    exit_rois = [exit["roi"] for exit in exits]
    exit_roi_bins = np.linspace(min(exit_rois), max(exit_rois), 20)
    exit_roi_hist, _ = np.histogram(exit_rois, bins=exit_roi_bins)

    exit_roi_distribution = {
        f"{exit_roi_bins[i]:.2f}-{exit_roi_bins[i+1]:.2f}": int(exit_roi_hist[i])
        for i in range(len(exit_roi_hist))
    }

    # Calculate exit type ROI
    exit_type_roi = {}
    for exit_type in set(exit_types):
        type_exits = [exit for exit in exits if exit["exit_type"] == exit_type]
        exit_type_roi[exit_type] = {
            "count": len(type_exits),
            "avg_roi": np.mean([exit["roi"] for exit in type_exits]),
            "avg_annualized_roi": np.mean([exit["annualized_roi"] for exit in type_exits]),
            "avg_exit_year": np.mean([exit["exit_year"] for exit in type_exits]),
        }

    # Calculate cumulative exits
    cumulative_exits = []
    for year in np.linspace(0, num_steps * dt, 100):
        count = sum(1 for exit in exits if exit["exit_year"] <= year)
        cumulative_exits.append({
            "year": year,
            "count": count,
            "percentage": count / len(exits),
        })

    # Calculate total exit value
    exit_value_total = sum(exit["exit_value"] for exit in exits)

    # Calculate total appreciation share
    appreciation_share_total = sum(exit["appreciation_share_amount"] for exit in exits)

    # Calculate total return
    total_return = exit_value_total + appreciation_share_total

    # Calculate total ROI
    total_loan_amount = sum(exit["loan_amount"] for exit in exits)
    total_roi = (total_return - total_loan_amount) / total_loan_amount if total_loan_amount > 0 else 0.0

    # Calculate annualized ROI (assuming average exit year)
    annualized_roi = (1 + total_roi) ** (1 / avg_exit_year) - 1 if avg_exit_year > 0 else 0.0

    return {
        "avg_exit_year": avg_exit_year,
        "avg_roi": avg_roi,
        "avg_annualized_roi": avg_annualized_roi,
        "exit_type_distribution": exit_type_distribution,
        "exit_timing_distribution": exit_timing_distribution,
        "exit_roi_distribution": exit_roi_distribution,
        "exit_type_roi": exit_type_roi,
        "cumulative_exits": cumulative_exits,
        "exit_value_total": exit_value_total,
        "appreciation_share_total": appreciation_share_total,
        "total_return": total_return,
        "total_roi": total_roi,
        "annualized_roi": annualized_roi,
    }


def generate_exit_visualization(
    exits: List[Dict[str, Any]],
    exit_stats: Dict[str, Any],
    num_steps: int,
    dt: float,
) -> Dict[str, Any]:
    """
    Generate visualization data for exits.

    Args:
        exits: List of exits
        exit_stats: Exit statistics
        num_steps: Number of time steps
        dt: Time step size (in years)

    Returns:
        Dictionary containing visualization data
    """
    # Skip if no exits
    if not exits:
        return {
            "exit_timing_chart": [],
            "exit_type_chart": [],
            "cumulative_exits_chart": [],
            "exit_roi_chart": [],
            "exit_type_roi_chart": [],
            "exit_summary": {},
        }

    # Generate exit timing chart
    exit_timing_chart = []
    for bin_range, count in exit_stats["exit_timing_distribution"].items():
        exit_timing_chart.append({
            "bin": bin_range,
            "count": count,
        })

    # Generate exit type chart
    exit_type_chart = []
    for exit_type, percentage in exit_stats["exit_type_distribution"].items():
        exit_type_chart.append({
            "type": exit_type,
            "percentage": percentage,
            "count": int(percentage * len(exits)),
        })

    # Generate cumulative exits chart
    cumulative_exits_chart = exit_stats["cumulative_exits"]

    # Generate exit ROI chart
    exit_roi_chart = []
    for bin_range, count in exit_stats["exit_roi_distribution"].items():
        exit_roi_chart.append({
            "bin": bin_range,
            "count": count,
        })

    # Generate exit type ROI chart
    exit_type_roi_chart = []
    for exit_type, stats in exit_stats["exit_type_roi"].items():
        exit_type_roi_chart.append({
            "type": exit_type,
            "avg_roi": stats["avg_roi"],
            "avg_annualized_roi": stats["avg_annualized_roi"],
            "avg_exit_year": stats["avg_exit_year"],
            "count": stats["count"],
        })

    # Generate exit summary
    exit_summary = {
        "total_exits": len(exits),
        "avg_exit_year": exit_stats["avg_exit_year"],
        "avg_roi": exit_stats["avg_roi"],
        "avg_annualized_roi": exit_stats["avg_annualized_roi"],
        "exit_value_total": exit_stats["exit_value_total"],
        "appreciation_share_total": exit_stats["appreciation_share_total"],
        "total_return": exit_stats["total_return"],
        "total_roi": exit_stats["total_roi"],
        "annualized_roi": exit_stats["annualized_roi"],
    }

    # Generate exit value by year chart
    exit_value_by_year = {}
    for exit in exits:
        year = int(exit["exit_year"])
        if year not in exit_value_by_year:
            exit_value_by_year[year] = {
                "exit_value": 0.0,
                "appreciation_share": 0.0,
                "total": 0.0,
            }
        exit_value_by_year[year]["exit_value"] += exit["exit_value"]
        exit_value_by_year[year]["appreciation_share"] += exit["appreciation_share_amount"]
        exit_value_by_year[year]["total"] += exit["exit_value"] + exit["appreciation_share_amount"]

    exit_value_by_year_chart = []
    for year in range(int(num_steps * dt) + 1):
        if year in exit_value_by_year:
            exit_value_by_year_chart.append({
                "year": year,
                "exit_value": exit_value_by_year[year]["exit_value"],
                "appreciation_share": exit_value_by_year[year]["appreciation_share"],
                "total": exit_value_by_year[year]["total"],
            })
        else:
            exit_value_by_year_chart.append({
                "year": year,
                "exit_value": 0.0,
                "appreciation_share": 0.0,
                "total": 0.0,
            })

    # Generate exit count by year chart
    exit_count_by_year = {}
    for exit in exits:
        year = int(exit["exit_year"])
        if year not in exit_count_by_year:
            exit_count_by_year[year] = {
                "sale": 0,
                "refinance": 0,
                "default": 0,
                "term_completion": 0,
                "total": 0,
            }
        exit_count_by_year[year][exit["exit_type"]] += 1
        exit_count_by_year[year]["total"] += 1

    exit_count_by_year_chart = []
    for year in range(int(num_steps * dt) + 1):
        if year in exit_count_by_year:
            exit_count_by_year_chart.append({
                "year": year,
                "sale": exit_count_by_year[year]["sale"],
                "refinance": exit_count_by_year[year]["refinance"],
                "default": exit_count_by_year[year]["default"],
                "term_completion": exit_count_by_year[year]["term_completion"],
                "total": exit_count_by_year[year]["total"],
            })
        else:
            exit_count_by_year_chart.append({
                "year": year,
                "sale": 0,
                "refinance": 0,
                "default": 0,
                "term_completion": 0,
                "total": 0,
            })

    return {
        "exit_timing_chart": exit_timing_chart,
        "exit_type_chart": exit_type_chart,
        "cumulative_exits_chart": cumulative_exits_chart,
        "exit_roi_chart": exit_roi_chart,
        "exit_type_roi_chart": exit_type_roi_chart,
        "exit_summary": exit_summary,
        "exit_value_by_year_chart": exit_value_by_year_chart,
        "exit_count_by_year_chart": exit_count_by_year_chart,
    }


async def get_exit_summary(context: SimulationContext) -> Dict[str, Any]:
    """
    Get a summary of the exit simulation results.

    Args:
        context: Simulation context

    Returns:
        Dictionary containing exit summary
    """
    start_time = time.time()
    logger.info("Getting exit summary")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="exit_simulator",
            progress=0.0,
            message="Generating exit summary",
        )

        # Get exits
        exits = getattr(context, "exits", [])

        # Get exit statistics
        exit_stats = getattr(context, "exit_stats", {})

        # Get exit visualization
        exit_visualization = getattr(context, "exit_visualization", {})

        # Generate summary
        summary = {
            "exits": exits,
            "statistics": exit_stats,
            "visualization": exit_visualization,
        }

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="exit_simulator",
            progress=100.0,
            message="Exit summary generated",
            data=summary,
        )

        # Update metrics
        increment_counter("exit_summary_generated_total")
        observe_histogram(
            "exit_summary_generation_runtime_seconds",
            time.time() - start_time,
        )

        return summary

    except Exception as e:
        # Handle exception
        error = handle_exception(e)

        # Log error
        log_error(error)

        # Report error
        await websocket_manager.send_error(
            simulation_id=context.run_id,
            error={
                "message": str(error),
                "code": error.code,
                "module": "exit_simulator",
            },
        )

        # Re-raise exception
        raise
