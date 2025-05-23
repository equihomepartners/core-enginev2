"""
Reinvestment engine module for the EQU IHOME SIM ENGINE v2.

This module is responsible for managing the reinvestment of capital during the fund's
reinvestment period. It tracks capital that becomes available for reinvestment when
loans exit the portfolio, applies different reinvestment strategies, and coordinates
with the Capital Allocator and Loan Generator to create new loans.
"""

import asyncio
import time
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple, Union, Set

import numpy as np
import structlog

from src.api.websocket_manager import get_websocket_manager
from src.engine.simulation_context import SimulationContext
from src.utils.error_handler import SimulationError, ErrorCode, handle_exception, log_error
from src.utils.metrics import increment_counter, observe_histogram, set_gauge
from src.engine.loan_generator import generate_reinvestment_loans

# Set up logging
logger = structlog.get_logger(__name__)


class ReinvestmentStrategy(str, Enum):
    """Reinvestment strategy enum."""
    MAINTAIN_ALLOCATION = "maintain_allocation"
    REBALANCE = "rebalance"
    OPPORTUNISTIC = "opportunistic"
    CUSTOM = "custom"


class ReinvestmentSource(str, Enum):
    """Reinvestment source enum."""
    EXIT = "exit"
    CASH_RESERVE = "cash_reserve"
    INITIAL_DEPLOYMENT = "initial_deployment"


class ReinvestmentFrequency(str, Enum):
    """Reinvestment frequency enum."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    SEMI_ANNUALLY = "semi_annually"
    ANNUALLY = "annually"
    ON_EXIT = "on_exit"


async def reinvest_capital(context: SimulationContext) -> None:
    """
    Reinvest capital during the reinvestment period.

    This function manages the reinvestment of capital during the fund's reinvestment period.
    It tracks capital that becomes available for reinvestment when loans exit the portfolio,
    applies different reinvestment strategies, and coordinates with the Capital Allocator
    and Loan Generator to create new loans.

    Args:
        context: Simulation context

    Raises:
        SimulationError: If there is an error during reinvestment
    """
    start_time = time.time()
    logger.info("Starting reinvestment engine")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="reinvest_engine",
            progress=0.0,
            message="Starting reinvestment engine",
        )

        # Check for cancellation
        if websocket_manager.is_cancelled(context.run_id):
            logger.info("Reinvestment engine cancelled", run_id=context.run_id)
            await websocket_manager.send_info(
                simulation_id=context.run_id,
                message="Reinvestment engine cancelled",
            )
            return

        # Get configuration
        config = context.config
        reinvestment_config = getattr(config, "reinvestment_engine", {})

        # Initialize reinvestment tracking in context if not already present
        if not hasattr(context, "reinvestment_events"):
            context.reinvestment_events = []

        if not hasattr(context, "cash_reserve"):
            context.cash_reserve = 0.0

        if not hasattr(context, "cash_reserve_history"):
            context.cash_reserve_history = []

        if not hasattr(context, "reinvestment_risk_metrics"):
            context.reinvestment_risk_metrics = []

        # Capture portfolio state before reinvestment for risk comparison
        portfolio_before = {
            "num_loans": len(getattr(context, "loans", [])),
            "total_loan_amount": sum(loan.get("loan_size", 0) for loan in getattr(context, "loans", [])),
            "zone_distribution": calculate_zone_distribution(context),
            "avg_ltv": calculate_avg_ltv(context),
            "concentration_risk": calculate_concentration_risk(context),
        }

        # Process exits and reinvest capital
        await process_exits_and_reinvest(context)

        # Capture portfolio state after reinvestment for risk comparison
        portfolio_after = {
            "num_loans": len(getattr(context, "loans", [])),
            "total_loan_amount": sum(loan.get("loan_size", 0) for loan in getattr(context, "loans", [])),
            "zone_distribution": calculate_zone_distribution(context),
            "avg_ltv": calculate_avg_ltv(context),
            "concentration_risk": calculate_concentration_risk(context),
        }

        # Calculate risk impact of reinvestment
        risk_impact = calculate_risk_impact(portfolio_before, portfolio_after)

        # Store risk impact in context
        context.reinvestment_risk_metrics.append({
            "timestamp": time.time(),
            "portfolio_before": portfolio_before,
            "portfolio_after": portfolio_after,
            "risk_impact": risk_impact,
        })

        # Calculate reinvestment statistics
        reinvestment_summary = calculate_reinvestment_statistics(context)
        context.reinvestment_summary = reinvestment_summary

        # Generate visualization data
        visualization = generate_reinvestment_visualization(context)
        context.reinvestment_visualization = visualization

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="reinvest_engine",
            progress=100.0,
            message="Reinvestment engine completed",
            data={
                "total_reinvested": reinvestment_summary.get("total_reinvested", 0),
                "num_reinvestment_events": reinvestment_summary.get("num_reinvestment_events", 0),
                "reinvestment_by_zone": reinvestment_summary.get("reinvestment_by_zone", {}),
                "risk_impact": risk_impact,
            },
        )

        # Send result message
        await websocket_manager.send_result(
            simulation_id=context.run_id,
            result={
                "module": "reinvest_engine",
                "reinvestment_summary": reinvestment_summary,
                "visualization": visualization,
                "risk_metrics": {
                    "portfolio_before": portfolio_before,
                    "portfolio_after": portfolio_after,
                    "risk_impact": risk_impact,
                },
                "execution_time": time.time() - start_time,
            },
        )

        # Update metrics
        increment_counter("reinvestment_engine_completed_total")
        observe_histogram(
            "reinvestment_engine_runtime_seconds",
            time.time() - start_time,
        )

        # Log completion
        logger.info(
            "Reinvestment engine completed",
            total_reinvested=reinvestment_summary.get("total_reinvested", 0),
            num_reinvestment_events=reinvestment_summary.get("num_reinvestment_events", 0),
            risk_impact=risk_impact,
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
                "module": "reinvest_engine",
            },
        )

        # Update metrics
        increment_counter("reinvestment_engine_failed_total")

        # Re-raise exception
        raise


async def process_exits_and_reinvest(context: SimulationContext) -> None:
    """
    Process exits and reinvest capital.

    This function processes exits from the portfolio and reinvests the capital
    according to the configured reinvestment strategy.

    Args:
        context: Simulation context
    """
    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    # Get configuration
    config = context.config
    reinvestment_config = getattr(config, "reinvestment_engine", {})

    # Get reinvestment parameters
    reinvestment_strategy = reinvestment_config.get("reinvestment_strategy", ReinvestmentStrategy.REBALANCE)
    min_reinvestment_amount = reinvestment_config.get("min_reinvestment_amount", 100000)
    reinvestment_frequency = reinvestment_config.get("reinvestment_frequency", ReinvestmentFrequency.QUARTERLY)
    reinvestment_delay = reinvestment_config.get("reinvestment_delay", 1)  # months
    enable_cash_reserve = reinvestment_config.get("enable_cash_reserve", False)
    cash_reserve_target = reinvestment_config.get("cash_reserve_target", 0.05) * config.fund_size
    cash_reserve_min = reinvestment_config.get("cash_reserve_min", 0.02) * config.fund_size
    cash_reserve_max = reinvestment_config.get("cash_reserve_max", 0.1) * config.fund_size

    # Get exits
    exits = getattr(context, "exits", [])

    # Check if we're within the reinvestment period
    fund_term = config.fund_term
    reinvestment_period = config.reinvestment_period

    # Group exits by time period based on reinvestment frequency
    exit_groups = group_exits_by_time_period(exits, reinvestment_frequency)

    # Report progress
    await websocket_manager.send_progress(
        simulation_id=context.run_id,
        module="reinvest_engine",
        progress=20.0,
        message="Grouped exits by time period",
        data={
            "num_exit_groups": len(exit_groups),
            "reinvestment_frequency": reinvestment_frequency,
        },
    )

    # Process each exit group
    for i, (time_key, group_exits) in enumerate(exit_groups.items()):
        # Extract year and month from time key
        year, month = parse_time_key(time_key)

        # Check if we're within the reinvestment period
        if year > reinvestment_period:
            logger.info(
                "Skipping reinvestment - beyond reinvestment period",
                year=year,
                reinvestment_period=reinvestment_period,
            )
            continue

        # Calculate total exit value for this group
        total_exit_value = sum(exit_data.get("exit_value", 0) for exit_data in group_exits)

        # Apply reinvestment delay
        delayed_month = month + reinvestment_delay
        delayed_year = year + (delayed_month - 1) // 12
        delayed_month = ((delayed_month - 1) % 12) + 1

        # Check for cancellation
        if websocket_manager.is_cancelled(context.run_id):
            logger.info("Reinvestment processing cancelled", run_id=context.run_id)
            await websocket_manager.send_info(
                simulation_id=context.run_id,
                message="Reinvestment processing cancelled",
            )
            return

        # Handle cash reserve if enabled
        if enable_cash_reserve:
            # Add exit value to cash reserve
            context.cash_reserve += total_exit_value

            # Record cash reserve history
            context.cash_reserve_history.append({
                "year": year,
                "month": month,
                "cash_reserve": context.cash_reserve,
                "cash_reserve_percentage": context.cash_reserve / config.fund_size,
                "event": "exit",
                "amount": total_exit_value,
            })

            # Determine amount to reinvest from cash reserve
            reinvestment_amount = 0

            if context.cash_reserve > cash_reserve_target:
                # Reinvest excess over target
                reinvestment_amount = context.cash_reserve - cash_reserve_target

                # Ensure we don't go below minimum
                if context.cash_reserve - reinvestment_amount < cash_reserve_min:
                    reinvestment_amount = context.cash_reserve - cash_reserve_min

            # Only reinvest if amount exceeds minimum
            if reinvestment_amount >= min_reinvestment_amount:
                # Update cash reserve
                context.cash_reserve -= reinvestment_amount

                # Record cash reserve history
                context.cash_reserve_history.append({
                    "year": delayed_year,
                    "month": delayed_month,
                    "cash_reserve": context.cash_reserve,
                    "cash_reserve_percentage": context.cash_reserve / config.fund_size,
                    "event": "reinvestment",
                    "amount": -reinvestment_amount,
                })

                # Reinvest the amount
                await reinvest_amount(
                    context=context,
                    amount=reinvestment_amount,
                    year=delayed_year,
                    month=delayed_month,
                    source=ReinvestmentSource.CASH_RESERVE,
                    source_details={
                        "exit_group": time_key,
                        "num_exits": len(group_exits),
                    },
                )
        else:
            # Direct reinvestment without cash reserve
            if total_exit_value >= min_reinvestment_amount:
                await reinvest_amount(
                    context=context,
                    amount=total_exit_value,
                    year=delayed_year,
                    month=delayed_month,
                    source=ReinvestmentSource.EXIT,
                    source_details={
                        "exit_group": time_key,
                        "num_exits": len(group_exits),
                        "exit_ids": [exit_data.get("loan_id") for exit_data in group_exits],
                    },
                )

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="reinvest_engine",
            progress=20.0 + (i + 1) / len(exit_groups) * 60.0,
            message=f"Processed exit group {i+1} of {len(exit_groups)}",
            data={
                "time_key": time_key,
                "year": year,
                "month": month,
                "total_exit_value": total_exit_value,
                "num_exits": len(group_exits),
            },
        )

    # Report completion
    await websocket_manager.send_progress(
        simulation_id=context.run_id,
        module="reinvest_engine",
        progress=80.0,
        message="Completed processing exits and reinvestment",
        data={
            "num_reinvestment_events": len(context.reinvestment_events),
            "total_reinvested": sum(event.get("amount", 0) for event in context.reinvestment_events),
        },
    )


async def reinvest_amount(
    context: SimulationContext,
    amount: float,
    year: float,
    month: int,
    source: ReinvestmentSource,
    source_details: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Reinvest a specific amount of capital.

    This function reinvests a specific amount of capital according to the
    configured reinvestment strategy.

    Args:
        context: Simulation context
        amount: Amount to reinvest
        year: Simulation year
        month: Month (1-12)
        source: Source of the reinvestment capital
        source_details: Details about the source of the reinvestment capital

    Returns:
        Reinvestment event details
    """
    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    # Get configuration
    config = context.config
    reinvestment_config = getattr(config, "reinvestment_engine", {})

    # Get reinvestment parameters
    reinvestment_strategy = reinvestment_config.get("reinvestment_strategy", ReinvestmentStrategy.REBALANCE)
    zone_preference_multipliers = reinvestment_config.get("zone_preference_multipliers", {
        "green": 1.0,
        "orange": 1.0,
        "red": 1.0,
    })
    opportunistic_threshold = reinvestment_config.get("opportunistic_threshold", 0.05)
    rebalance_threshold = reinvestment_config.get("rebalance_threshold", 0.05)
    enable_dynamic_allocation = reinvestment_config.get("enable_dynamic_allocation", False)
    performance_lookback_period = reinvestment_config.get("performance_lookback_period", 12)
    performance_weight = reinvestment_config.get("performance_weight", 0.5)
    max_allocation_adjustment = reinvestment_config.get("max_allocation_adjustment", 0.2)

    # Generate a unique ID for this reinvestment event
    event_id = str(uuid.uuid4())

    # Report progress
    await websocket_manager.send_progress(
        simulation_id=context.run_id,
        module="reinvest_engine",
        progress=85.0,
        message="Determining reinvestment allocations",
        data={
            "event_id": event_id,
            "amount": amount,
            "year": year,
            "month": month,
            "strategy": reinvestment_strategy,
        },
    )

    # Determine target allocations based on strategy
    target_allocations = {}

    if reinvestment_strategy == ReinvestmentStrategy.MAINTAIN_ALLOCATION:
        # Use current portfolio allocations
        target_allocations = get_current_allocations(context)
    elif reinvestment_strategy == ReinvestmentStrategy.REBALANCE:
        # Use target allocations from config
        target_allocations = get_target_allocations(context)
    elif reinvestment_strategy == ReinvestmentStrategy.OPPORTUNISTIC:
        # Allocate based on recent performance
        target_allocations = get_opportunistic_allocations(
            context,
            opportunistic_threshold=opportunistic_threshold
        )
    else:  # CUSTOM or fallback
        # Use target allocations from config with preference multipliers
        base_allocations = get_target_allocations(context)
        target_allocations = apply_preference_multipliers(
            base_allocations,
            zone_preference_multipliers
        )

    # Apply dynamic allocation adjustments if enabled
    if enable_dynamic_allocation:
        performance_adjustments = calculate_performance_adjustments(
            context,
            lookback_period=performance_lookback_period,
            weight=performance_weight,
            max_adjustment=max_allocation_adjustment,
        )

        # Apply adjustments to target allocations
        for zone, adjustment in performance_adjustments.items():
            if zone in target_allocations:
                target_allocations[zone] += adjustment

        # Normalize allocations to ensure they sum to 1
        total = sum(target_allocations.values())
        if total > 0:
            target_allocations = {zone: alloc / total for zone, alloc in target_allocations.items()}

    # Report progress
    await websocket_manager.send_progress(
        simulation_id=context.run_id,
        module="reinvest_engine",
        progress=90.0,
        message="Generating reinvestment loans",
        data={
            "event_id": event_id,
            "target_allocations": target_allocations,
        },
    )

    # Generate loans for reinvestment
    reinvestment_loans = await generate_reinvestment_loans(
        context=context,
        reinvestment_amount=amount,
        target_zones=target_allocations,
        year=year,
    )

    # Calculate actual allocations achieved
    actual_allocations = {}
    zone_amounts = {}

    for loan in reinvestment_loans:
        zone = loan.get("zone")
        loan_size = loan.get("loan_size", 0)

        if zone not in zone_amounts:
            zone_amounts[zone] = 0

        zone_amounts[zone] += loan_size

    total_amount = sum(zone_amounts.values())
    if total_amount > 0:
        actual_allocations = {zone: amount / total_amount for zone, amount in zone_amounts.items()}

    # Create reinvestment event
    reinvestment_event = {
        "event_id": event_id,
        "timestamp": time.time(),
        "year": year,
        "month": month,
        "amount": amount,
        "source": source,
        "source_details": source_details,
        "strategy_used": reinvestment_strategy,
        "target_allocations": target_allocations,
        "actual_allocations": actual_allocations,
        "num_loans_generated": len(reinvestment_loans),
        "loan_ids": [loan.get("loan_id") for loan in reinvestment_loans],
        "performance_adjustments": performance_adjustments if enable_dynamic_allocation else {},
    }

    # Add cash reserve information if available
    if hasattr(context, "cash_reserve"):
        reinvestment_event["cash_reserve_before"] = context.cash_reserve + amount if source == ReinvestmentSource.CASH_RESERVE else context.cash_reserve
        reinvestment_event["cash_reserve_after"] = context.cash_reserve

    # Store reinvestment event in context
    context.reinvestment_events.append(reinvestment_event)

    # Report progress
    await websocket_manager.send_progress(
        simulation_id=context.run_id,
        module="reinvest_engine",
        progress=95.0,
        message="Completed reinvestment",
        data={
            "event_id": event_id,
            "amount": amount,
            "num_loans_generated": len(reinvestment_loans),
            "actual_allocations": actual_allocations,
        },
    )

    return reinvestment_event


def group_exits_by_time_period(exits: List[Dict[str, Any]], frequency: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group exits by time period based on frequency.

    Args:
        exits: List of exit events
        frequency: Frequency for grouping (monthly, quarterly, etc.)

    Returns:
        Dictionary of exit groups by time key
    """
    exit_groups = {}

    for exit_data in exits:
        # Get exit year and month
        exit_year = exit_data.get("exit_year", 0)
        exit_month = exit_data.get("exit_month", 0) % 12 + 1  # Convert 0-based to 1-based month

        # Create time key based on frequency
        if frequency == ReinvestmentFrequency.MONTHLY:
            time_key = f"{exit_year:.1f}-{exit_month:02d}"
        elif frequency == ReinvestmentFrequency.QUARTERLY:
            quarter = (exit_month - 1) // 3 + 1
            time_key = f"{exit_year:.1f}-Q{quarter}"
        elif frequency == ReinvestmentFrequency.SEMI_ANNUALLY:
            half = (exit_month - 1) // 6 + 1
            time_key = f"{exit_year:.1f}-H{half}"
        elif frequency == ReinvestmentFrequency.ANNUALLY:
            time_key = f"{exit_year:.1f}"
        else:  # ON_EXIT or fallback
            # Each exit is its own group
            time_key = f"{exit_year:.1f}-{exit_month:02d}-{exit_data.get('loan_id', '')}"

        # Add exit to group
        if time_key not in exit_groups:
            exit_groups[time_key] = []

        exit_groups[time_key].append(exit_data)

    return exit_groups


def parse_time_key(time_key: str) -> Tuple[float, int]:
    """
    Parse a time key into year and month.

    Args:
        time_key: Time key string (e.g., "2.0-01", "2.0-Q1", "2.0-H1", "2.0")

    Returns:
        Tuple of (year, month)
    """
    parts = time_key.split("-")
    year = float(parts[0])

    if len(parts) == 1:
        # Annual format: "2.0"
        month = 1
    elif parts[1].startswith("Q"):
        # Quarterly format: "2.0-Q1"
        quarter = int(parts[1][1:])
        month = (quarter - 1) * 3 + 1
    elif parts[1].startswith("H"):
        # Semi-annual format: "2.0-H1"
        half = int(parts[1][1:])
        month = (half - 1) * 6 + 1
    else:
        # Monthly format: "2.0-01"
        month = int(parts[1])

    return year, month


def get_current_allocations(context: SimulationContext) -> Dict[str, float]:
    """
    Get current portfolio allocations by zone.

    Args:
        context: Simulation context

    Returns:
        Dictionary of zone allocations (0-1)
    """
    # Get loans
    loans = getattr(context, "loans", [])

    # Calculate zone amounts
    zone_amounts = {}

    for loan in loans:
        zone = loan.get("zone")
        loan_size = loan.get("loan_size", 0)

        if zone not in zone_amounts:
            zone_amounts[zone] = 0

        zone_amounts[zone] += loan_size

    # Calculate allocations
    total_amount = sum(zone_amounts.values())
    allocations = {}

    if total_amount > 0:
        allocations = {zone: amount / total_amount for zone, amount in zone_amounts.items()}

    # Ensure all zones have an allocation
    for zone in ["green", "orange", "red"]:
        if zone not in allocations:
            allocations[zone] = 0.0

    return allocations


def get_target_allocations(context: SimulationContext) -> Dict[str, float]:
    """
    Get target zone allocations from config.

    Args:
        context: Simulation context

    Returns:
        Dictionary of target zone allocations (0-1)
    """
    # Get configuration
    config = context.config

    # Get zone allocations from config
    zone_allocations = getattr(config, "zone_allocations", None)

    # Convert ZoneAllocations object to dictionary if needed
    if zone_allocations:
        if hasattr(zone_allocations, 'dict'):
            # It's a Pydantic model, convert to dict
            zone_allocations = zone_allocations.dict()
        elif hasattr(zone_allocations, 'green'):
            # It's an object with attributes, convert to dict
            zone_allocations = {
                "green": zone_allocations.green,
                "orange": zone_allocations.orange,
                "red": zone_allocations.red,
            }
    else:
        # Use default allocations
        zone_allocations = {}

    # Create allocations dictionary with fallback defaults
    allocations = {
        "green": zone_allocations.get("green", 0.6),
        "orange": zone_allocations.get("orange", 0.3),
        "red": zone_allocations.get("red", 0.1),
    }

    # Normalize allocations to ensure they sum to 1
    total = sum(allocations.values())
    if total > 0:
        allocations = {zone: alloc / total for zone, alloc in allocations.items()}

    return allocations


def get_opportunistic_allocations(
    context: SimulationContext,
    opportunistic_threshold: float = 0.05
) -> Dict[str, float]:
    """
    Get opportunistic allocations based on recent performance.

    Args:
        context: Simulation context
        opportunistic_threshold: Appreciation threshold for opportunistic allocation

    Returns:
        Dictionary of opportunistic zone allocations (0-1)
    """
    # Get price paths
    price_paths = getattr(context, "price_paths", {})
    zone_price_paths = price_paths.get("zone_price_paths", {})

    # Calculate recent appreciation rates
    appreciation_rates = {}
    lookback_steps = 12  # 1 year lookback

    for zone, path in zone_price_paths.items():
        if len(path) > lookback_steps:
            # Calculate appreciation over lookback period
            recent_appreciation = path[-1] / path[-lookback_steps] - 1
            appreciation_rates[zone] = recent_appreciation

    # Identify zones with appreciation above threshold
    opportunistic_zones = {}

    for zone, rate in appreciation_rates.items():
        if rate > opportunistic_threshold:
            opportunistic_zones[zone] = rate

    # If no zones meet the threshold, fall back to target allocations
    if not opportunistic_zones:
        return get_target_allocations(context)

    # Allocate based on relative appreciation rates
    total_appreciation = sum(opportunistic_zones.values())
    allocations = {}

    if total_appreciation > 0:
        for zone, rate in opportunistic_zones.items():
            allocations[zone] = rate / total_appreciation

    # Ensure all zones have an allocation
    for zone in ["green", "orange", "red"]:
        if zone not in allocations:
            allocations[zone] = 0.0

    return allocations


def apply_preference_multipliers(
    allocations: Dict[str, float],
    multipliers: Dict[str, float]
) -> Dict[str, float]:
    """
    Apply preference multipliers to allocations.

    Args:
        allocations: Base allocations
        multipliers: Preference multipliers by zone

    Returns:
        Adjusted allocations
    """
    # Apply multipliers
    adjusted_allocations = {}

    for zone, allocation in allocations.items():
        multiplier = multipliers.get(zone, 1.0)
        adjusted_allocations[zone] = allocation * multiplier

    # Normalize allocations to ensure they sum to 1
    total = sum(adjusted_allocations.values())
    if total > 0:
        adjusted_allocations = {zone: alloc / total for zone, alloc in adjusted_allocations.items()}

    return adjusted_allocations


def calculate_performance_adjustments(
    context: SimulationContext,
    lookback_period: int = 12,
    weight: float = 0.5,
    max_adjustment: float = 0.2
) -> Dict[str, float]:
    """
    Calculate performance-based allocation adjustments.

    Args:
        context: Simulation context
        lookback_period: Lookback period in months
        weight: Weight of performance in adjustments (0-1)
        max_adjustment: Maximum adjustment to allocation (0-1)

    Returns:
        Dictionary of allocation adjustments by zone
    """
    # Get exits
    exits = getattr(context, "exits", [])

    # Filter exits within lookback period
    recent_exits = []
    current_year = max([exit_data.get("exit_year", 0) for exit_data in exits], default=0)

    for exit_data in exits:
        exit_year = exit_data.get("exit_year", 0)
        exit_month = exit_data.get("exit_month", 0)

        # Convert to months since start
        exit_months = exit_year * 12 + exit_month
        current_months = current_year * 12

        if current_months - exit_months <= lookback_period:
            recent_exits.append(exit_data)

    # Calculate ROI by zone
    zone_roi = {}
    zone_counts = {}

    for exit_data in recent_exits:
        zone = exit_data.get("zone")
        roi = exit_data.get("roi", 0)

        if zone not in zone_roi:
            zone_roi[zone] = 0
            zone_counts[zone] = 0

        zone_roi[zone] += roi
        zone_counts[zone] += 1

    # Calculate average ROI by zone
    avg_roi = {}

    for zone, total_roi in zone_roi.items():
        count = zone_counts.get(zone, 0)
        if count > 0:
            avg_roi[zone] = total_roi / count

    # If no ROI data, return no adjustments
    if not avg_roi:
        return {zone: 0.0 for zone in ["green", "orange", "red"]}

    # Calculate relative performance
    total_roi = sum(avg_roi.values())
    relative_performance = {}

    if total_roi > 0:
        for zone, roi in avg_roi.items():
            relative_performance[zone] = roi / total_roi

    # Calculate target allocations
    target_allocations = get_target_allocations(context)

    # Calculate adjustments
    adjustments = {}

    for zone in target_allocations:
        target = target_allocations.get(zone, 0)
        performance = relative_performance.get(zone, 0)

        # Calculate raw adjustment
        raw_adjustment = (performance - target) * weight

        # Limit adjustment to max_adjustment
        adjustment = max(min(raw_adjustment, max_adjustment), -max_adjustment)

        adjustments[zone] = adjustment

    return adjustments


def calculate_reinvestment_statistics(context: SimulationContext) -> Dict[str, Any]:
    """
    Calculate reinvestment statistics.

    Args:
        context: Simulation context

    Returns:
        Dictionary of reinvestment statistics
    """
    # Get reinvestment events
    reinvestment_events = getattr(context, "reinvestment_events", [])

    # Get loans
    loans = getattr(context, "loans", [])

    # Get exits
    exits = getattr(context, "exits", [])

    # Calculate total reinvested
    total_reinvested = sum(event.get("amount", 0) for event in reinvestment_events)

    # Calculate average reinvestment amount
    avg_reinvestment_amount = 0
    if reinvestment_events:
        avg_reinvestment_amount = total_reinvested / len(reinvestment_events)

    # Calculate reinvestment by year
    reinvestment_by_year = {}
    for event in reinvestment_events:
        year = event.get("year", 0)
        amount = event.get("amount", 0)

        if year not in reinvestment_by_year:
            reinvestment_by_year[year] = 0

        reinvestment_by_year[year] += amount

    # Calculate reinvestment by zone
    reinvestment_by_zone = {}
    for event in reinvestment_events:
        actual_allocations = event.get("actual_allocations", {})
        amount = event.get("amount", 0)

        for zone, allocation in actual_allocations.items():
            if zone not in reinvestment_by_zone:
                reinvestment_by_zone[zone] = 0

            reinvestment_by_zone[zone] += amount * allocation

    # Calculate reinvestment by strategy
    reinvestment_by_strategy = {}
    for event in reinvestment_events:
        strategy = event.get("strategy_used", "unknown")
        amount = event.get("amount", 0)

        if strategy not in reinvestment_by_strategy:
            reinvestment_by_strategy[strategy] = 0

        reinvestment_by_strategy[strategy] += amount

    # Calculate reinvestment by source
    reinvestment_by_source = {}
    for event in reinvestment_events:
        source = event.get("source", "unknown")
        amount = event.get("amount", 0)

        if source not in reinvestment_by_source:
            reinvestment_by_source[source] = 0

        reinvestment_by_source[source] += amount

    # Calculate reinvestment efficiency metrics
    total_exits_amount = sum(exit_data.get("exit_value", 0) for exit_data in exits)
    reinvestment_ratio = total_reinvested / total_exits_amount if total_exits_amount > 0 else 0

    # Calculate time to reinvest
    time_to_reinvest = []
    for event in reinvestment_events:
        if event.get("source") == ReinvestmentSource.EXIT:
            source_details = event.get("source_details", {})
            exit_ids = source_details.get("exit_ids", [])

            for exit_id in exit_ids:
                # Find the exit
                exit_data = next((e for e in exits if e.get("loan_id") == exit_id), None)
                if exit_data:
                    exit_year = exit_data.get("exit_year", 0)
                    exit_month = exit_data.get("exit_month", 0)
                    reinvest_year = event.get("year", 0)
                    reinvest_month = event.get("month", 0)

                    # Calculate time difference in months
                    exit_time = exit_year * 12 + exit_month
                    reinvest_time = reinvest_year * 12 + reinvest_month
                    time_diff = reinvest_time - exit_time

                    if time_diff >= 0:
                        time_to_reinvest.append(time_diff)

    avg_time_to_reinvest = sum(time_to_reinvest) / len(time_to_reinvest) if time_to_reinvest else 0

    # Calculate reinvestment loan performance
    reinvestment_loans = [loan for loan in loans if loan.get("is_reinvestment", False)]
    reinvestment_loan_exits = [
        exit_data for exit_data in exits
        if exit_data.get("loan_id") in [loan.get("loan_id") for loan in reinvestment_loans]
    ]

    # Calculate ROI for reinvestment loans
    reinvestment_roi = 0
    if reinvestment_loan_exits:
        total_exit_value = sum(exit_data.get("exit_value", 0) for exit_data in reinvestment_loan_exits)
        total_loan_size = sum(exit_data.get("loan_size", 0) for exit_data in reinvestment_loan_exits)
        reinvestment_roi = (total_exit_value / total_loan_size) - 1 if total_loan_size > 0 else 0

    # Calculate average hold period for reinvestment loans
    hold_periods = []
    for exit_data in reinvestment_loan_exits:
        loan_id = exit_data.get("loan_id")
        loan = next((l for l in reinvestment_loans if l.get("loan_id") == loan_id), None)

        if loan:
            origination_year = loan.get("reinvestment_year", 0)
            exit_year = exit_data.get("exit_year", 0)
            hold_period = exit_year - origination_year
            hold_periods.append(hold_period)

    avg_hold_period = sum(hold_periods) / len(hold_periods) if hold_periods else 0

    # Calculate exit type distribution for reinvestment loans
    exit_types = {}
    for exit_data in reinvestment_loan_exits:
        exit_type = exit_data.get("exit_type", "unknown")

        if exit_type not in exit_types:
            exit_types[exit_type] = 0

        exit_types[exit_type] += 1

    # Calculate exit type percentages
    exit_type_distribution = {}
    if reinvestment_loan_exits:
        for exit_type, count in exit_types.items():
            exit_type_distribution[exit_type] = count / len(reinvestment_loan_exits)

    # Calculate reinvestment impact on portfolio
    portfolio_with_reinvestment = len(loans)
    portfolio_without_reinvestment = portfolio_with_reinvestment - len(reinvestment_loans)
    reinvestment_portfolio_impact = len(reinvestment_loans) / portfolio_without_reinvestment if portfolio_without_reinvestment > 0 else 0

    # Calculate reinvestment timing metrics
    reinvestment_timing = {}
    for event in reinvestment_events:
        year = event.get("year", 0)
        year_int = int(year)

        if year_int not in reinvestment_timing:
            reinvestment_timing[year_int] = {
                "q1": 0,
                "q2": 0,
                "q3": 0,
                "q4": 0,
            }

        month = event.get("month", 0)
        amount = event.get("amount", 0)

        if 1 <= month <= 3:
            reinvestment_timing[year_int]["q1"] += amount
        elif 4 <= month <= 6:
            reinvestment_timing[year_int]["q2"] += amount
        elif 7 <= month <= 9:
            reinvestment_timing[year_int]["q3"] += amount
        elif 10 <= month <= 12:
            reinvestment_timing[year_int]["q4"] += amount

    # Calculate cash reserve metrics
    cash_reserve_metrics = {}
    if hasattr(context, "cash_reserve_history") and context.cash_reserve_history:
        cash_reserve_history = context.cash_reserve_history

        # Calculate average cash reserve
        avg_cash_reserve = sum(entry.get("cash_reserve", 0) for entry in cash_reserve_history) / len(cash_reserve_history)

        # Calculate min and max cash reserve
        min_cash_reserve = min(entry.get("cash_reserve", 0) for entry in cash_reserve_history)
        max_cash_reserve = max(entry.get("cash_reserve", 0) for entry in cash_reserve_history)

        # Calculate cash reserve as percentage of fund size
        fund_size = context.config.fund_size
        avg_cash_reserve_pct = avg_cash_reserve / fund_size if fund_size > 0 else 0
        min_cash_reserve_pct = min_cash_reserve / fund_size if fund_size > 0 else 0
        max_cash_reserve_pct = max_cash_reserve / fund_size if fund_size > 0 else 0

        cash_reserve_metrics = {
            "avg_cash_reserve": avg_cash_reserve,
            "min_cash_reserve": min_cash_reserve,
            "max_cash_reserve": max_cash_reserve,
            "avg_cash_reserve_pct": avg_cash_reserve_pct,
            "min_cash_reserve_pct": min_cash_reserve_pct,
            "max_cash_reserve_pct": max_cash_reserve_pct,
        }

    # Create statistics dictionary
    statistics = {
        "total_reinvested": total_reinvested,
        "num_reinvestment_events": len(reinvestment_events),
        "avg_reinvestment_amount": avg_reinvestment_amount,
        "reinvestment_by_year": reinvestment_by_year,
        "reinvestment_by_zone": reinvestment_by_zone,
        "reinvestment_by_strategy": reinvestment_by_strategy,
        "reinvestment_by_source": reinvestment_by_source,
        "reinvestment_efficiency": {
            "reinvestment_ratio": reinvestment_ratio,
            "avg_time_to_reinvest": avg_time_to_reinvest,
            "reinvestment_portfolio_impact": reinvestment_portfolio_impact,
        },
        "reinvestment_performance": {
            "roi": reinvestment_roi,
            "avg_hold_period": avg_hold_period,
            "exit_type_distribution": exit_type_distribution,
        },
        "reinvestment_timing": reinvestment_timing,
    }

    # Add cash reserve history and metrics if available
    if hasattr(context, "cash_reserve_history"):
        statistics["cash_reserve_history"] = context.cash_reserve_history
        statistics["cash_reserve_metrics"] = cash_reserve_metrics

    return statistics


def generate_reinvestment_visualization(context: SimulationContext) -> Dict[str, Any]:
    """
    Generate visualization data for reinvestment activity.

    Args:
        context: Simulation context

    Returns:
        Dictionary of visualization data
    """
    # Get reinvestment events
    reinvestment_events = getattr(context, "reinvestment_events", [])

    # Get reinvestment statistics
    reinvestment_summary = getattr(context, "reinvestment_summary", {})

    # Get loans and exits
    loans = getattr(context, "loans", [])
    exits = getattr(context, "exits", [])

    # Identify reinvestment loans
    reinvestment_loans = [loan for loan in loans if loan.get("is_reinvestment", False)]
    reinvestment_loan_exits = [
        exit_data for exit_data in exits
        if exit_data.get("loan_id") in [loan.get("loan_id") for loan in reinvestment_loans]
    ]

    # Generate reinvestment timeline
    reinvestment_timeline = []
    cumulative_amount = 0

    # Sort events by year and month
    sorted_events = sorted(
        reinvestment_events,
        key=lambda e: (e.get("year", 0), e.get("month", 0))
    )

    for event in sorted_events:
        year = event.get("year", 0)
        month = event.get("month", 0)
        amount = event.get("amount", 0)

        cumulative_amount += amount

        reinvestment_timeline.append({
            "year": year,
            "month": month,
            "amount": amount,
            "cumulative_amount": cumulative_amount,
            "strategy": event.get("strategy_used", ""),
            "num_loans": event.get("num_loans_generated", 0),
        })

    # Generate reinvestment by zone chart
    reinvestment_by_zone = reinvestment_summary.get("reinvestment_by_zone", {})
    reinvestment_by_zone_chart = []

    total_reinvested = reinvestment_summary.get("total_reinvested", 0)

    for zone, amount in reinvestment_by_zone.items():
        percentage = 0
        if total_reinvested > 0:
            percentage = amount / total_reinvested

        reinvestment_by_zone_chart.append({
            "zone": zone,
            "amount": amount,
            "percentage": percentage,
        })

    # Generate reinvestment by year chart
    reinvestment_by_year = reinvestment_summary.get("reinvestment_by_year", {})
    reinvestment_by_year_chart = []

    # Count events by year
    events_by_year = {}
    for event in reinvestment_events:
        year = event.get("year", 0)

        if year not in events_by_year:
            events_by_year[year] = 0

        events_by_year[year] += 1

    for year, amount in sorted(reinvestment_by_year.items()):
        reinvestment_by_year_chart.append({
            "year": year,
            "amount": amount,
            "num_events": events_by_year.get(year, 0),
        })

    # Generate reinvestment by strategy chart
    reinvestment_by_strategy = reinvestment_summary.get("reinvestment_by_strategy", {})
    reinvestment_by_strategy_chart = []

    for strategy, amount in reinvestment_by_strategy.items():
        percentage = 0
        if total_reinvested > 0:
            percentage = amount / total_reinvested

        reinvestment_by_strategy_chart.append({
            "strategy": strategy,
            "amount": amount,
            "percentage": percentage,
        })

    # Generate reinvestment by source chart
    reinvestment_by_source = reinvestment_summary.get("reinvestment_by_source", {})
    reinvestment_by_source_chart = []

    for source, amount in reinvestment_by_source.items():
        percentage = 0
        if total_reinvested > 0:
            percentage = amount / total_reinvested

        reinvestment_by_source_chart.append({
            "source": source,
            "amount": amount,
            "percentage": percentage,
        })

    # Generate cash reserve chart
    cash_reserve_chart = []

    if hasattr(context, "cash_reserve_history"):
        # Get configuration
        config = context.config
        reinvestment_config = getattr(config, "reinvestment_engine", {})

        # Get cash reserve parameters
        cash_reserve_target = reinvestment_config.get("cash_reserve_target", 0.05) * config.fund_size
        cash_reserve_min = reinvestment_config.get("cash_reserve_min", 0.02) * config.fund_size
        cash_reserve_max = reinvestment_config.get("cash_reserve_max", 0.1) * config.fund_size

        for entry in context.cash_reserve_history:
            cash_reserve_chart.append({
                "year": entry.get("year", 0),
                "month": entry.get("month", 0),
                "cash_reserve": entry.get("cash_reserve", 0),
                "target": cash_reserve_target,
                "min": cash_reserve_min,
                "max": cash_reserve_max,
                "event": entry.get("event", ""),
                "amount": entry.get("amount", 0),
            })

    # Generate allocation comparison chart
    allocation_comparison_chart = []

    for event in reinvestment_events:
        event_id = event.get("event_id", "")
        year = event.get("year", 0)
        target_allocations = event.get("target_allocations", {})
        actual_allocations = event.get("actual_allocations", {})

        for zone in set(target_allocations.keys()) | set(actual_allocations.keys()):
            target = target_allocations.get(zone, 0)
            actual = actual_allocations.get(zone, 0)
            gap = actual - target

            allocation_comparison_chart.append({
                "event_id": event_id,
                "year": year,
                "zone": zone,
                "target": target,
                "actual": actual,
                "gap": gap,
            })

    # Generate reinvestment efficiency chart
    reinvestment_efficiency = reinvestment_summary.get("reinvestment_efficiency", {})
    reinvestment_efficiency_chart = [
        {
            "metric": "Reinvestment Ratio",
            "value": reinvestment_efficiency.get("reinvestment_ratio", 0),
            "description": "Ratio of reinvested capital to total exit value",
        },
        {
            "metric": "Avg Time to Reinvest (months)",
            "value": reinvestment_efficiency.get("avg_time_to_reinvest", 0),
            "description": "Average time between exit and reinvestment",
        },
        {
            "metric": "Portfolio Impact",
            "value": reinvestment_efficiency.get("reinvestment_portfolio_impact", 0),
            "description": "Percentage of portfolio from reinvestment",
        },
    ]

    # Generate reinvestment performance chart
    reinvestment_performance = reinvestment_summary.get("reinvestment_performance", {})
    reinvestment_performance_chart = [
        {
            "metric": "ROI",
            "value": reinvestment_performance.get("roi", 0),
            "description": "Return on investment for reinvested capital",
        },
        {
            "metric": "Avg Hold Period (years)",
            "value": reinvestment_performance.get("avg_hold_period", 0),
            "description": "Average hold period for reinvestment loans",
        },
    ]

    # Generate exit type distribution chart
    exit_type_distribution = reinvestment_performance.get("exit_type_distribution", {})
    exit_type_distribution_chart = []

    for exit_type, percentage in exit_type_distribution.items():
        exit_type_distribution_chart.append({
            "exit_type": exit_type,
            "percentage": percentage,
        })

    # Generate reinvestment timing chart
    reinvestment_timing = reinvestment_summary.get("reinvestment_timing", {})
    reinvestment_timing_chart = []

    for year, quarters in sorted(reinvestment_timing.items()):
        for quarter, amount in quarters.items():
            if amount > 0:
                reinvestment_timing_chart.append({
                    "year": year,
                    "quarter": quarter,
                    "amount": amount,
                })

    # Generate reinvestment vs exits chart
    reinvestment_vs_exits_chart = []

    # Group exits by year
    exits_by_year = {}
    for exit_data in exits:
        year = exit_data.get("exit_year", 0)
        exit_value = exit_data.get("exit_value", 0)

        if year not in exits_by_year:
            exits_by_year[year] = 0

        exits_by_year[year] += exit_value

    # Compare exits and reinvestments by year
    all_years = sorted(set(list(reinvestment_by_year.keys()) + list(exits_by_year.keys())))
    for year in all_years:
        reinvestment_vs_exits_chart.append({
            "year": year,
            "exits": exits_by_year.get(year, 0),
            "reinvestments": reinvestment_by_year.get(year, 0),
            "gap": reinvestment_by_year.get(year, 0) - exits_by_year.get(year, 0),
        })

    # Generate reinvestment loan size distribution
    loan_sizes = [loan.get("loan_size", 0) for loan in reinvestment_loans]

    if loan_sizes:
        min_size = min(loan_sizes)
        max_size = max(loan_sizes)

        # Create bins
        num_bins = 10
        bin_width = (max_size - min_size) / num_bins if max_size > min_size else 1

        # Initialize bins
        size_bins = {}
        for i in range(num_bins):
            bin_min = min_size + i * bin_width
            bin_max = min_size + (i + 1) * bin_width
            bin_label = f"{bin_min:.0f}-{bin_max:.0f}"
            size_bins[bin_label] = 0

        # Count loans in each bin
        for size in loan_sizes:
            bin_index = min(num_bins - 1, int((size - min_size) / bin_width))
            bin_min = min_size + bin_index * bin_width
            bin_max = min_size + (bin_index + 1) * bin_width
            bin_label = f"{bin_min:.0f}-{bin_max:.0f}"
            size_bins[bin_label] += 1

        # Convert to chart data
        loan_size_distribution_chart = [
            {"bin": bin_label, "count": count}
            for bin_label, count in size_bins.items()
        ]
    else:
        loan_size_distribution_chart = []

    # Generate reinvestment summary table
    reinvestment_summary_table = []

    for year, amount in sorted(reinvestment_by_year.items()):
        year_events = [e for e in reinvestment_events if e.get("year", 0) == year]
        num_events = len(year_events)

        # Count loans
        num_loans = sum(e.get("num_loans_generated", 0) for e in year_events)

        # Calculate average loan size
        avg_loan_size = 0
        if num_loans > 0:
            avg_loan_size = amount / num_loans

        # Calculate zone distribution
        zone_distribution = {}
        for event in year_events:
            actual_allocations = event.get("actual_allocations", {})
            event_amount = event.get("amount", 0)

            for zone, allocation in actual_allocations.items():
                if zone not in zone_distribution:
                    zone_distribution[zone] = 0

                zone_distribution[zone] += event_amount * allocation

        # Convert to percentages
        if amount > 0:
            zone_distribution = {zone: amt / amount for zone, amt in zone_distribution.items()}

        # Calculate strategy distribution
        strategy_distribution = {}
        for event in year_events:
            strategy = event.get("strategy_used", "unknown")
            event_amount = event.get("amount", 0)

            if strategy not in strategy_distribution:
                strategy_distribution[strategy] = 0

            strategy_distribution[strategy] += event_amount

        # Convert to percentages
        if amount > 0:
            strategy_distribution = {strategy: amt / amount for strategy, amt in strategy_distribution.items()}

        reinvestment_summary_table.append({
            "year": year,
            "amount": amount,
            "num_events": num_events,
            "num_loans": num_loans,
            "avg_loan_size": avg_loan_size,
            "zone_distribution": zone_distribution,
            "strategy_distribution": strategy_distribution,
        })

    # Generate reinvestment events table
    reinvestment_events_table = []

    for event in sorted_events:
        reinvestment_events_table.append({
            "event_id": event.get("event_id", ""),
            "year": event.get("year", 0),
            "month": event.get("month", 0),
            "amount": event.get("amount", 0),
            "strategy": event.get("strategy_used", ""),
            "num_loans": event.get("num_loans_generated", 0),
            "source": event.get("source", ""),
            "target_zones": ", ".join([f"{zone}: {alloc:.1%}" for zone, alloc in event.get("target_allocations", {}).items()]),
            "actual_zones": ", ".join([f"{zone}: {alloc:.1%}" for zone, alloc in event.get("actual_allocations", {}).items()]),
        })

    # Generate reinvestment loans table
    reinvestment_loans_table = []

    for loan in reinvestment_loans:
        # Find the corresponding exit if any
        exit_data = next((e for e in exits if e.get("loan_id") == loan.get("loan_id")), None)

        loan_data = {
            "loan_id": loan.get("loan_id", ""),
            "loan_size": loan.get("loan_size", 0),
            "ltv": loan.get("ltv", 0),
            "zone": loan.get("zone", ""),
            "reinvestment_year": loan.get("reinvestment_year", 0),
            "property_value": loan.get("property_value", 0),
            "suburb_name": loan.get("suburb_name", ""),
        }

        if exit_data:
            loan_data.update({
                "exit_year": exit_data.get("exit_year", 0),
                "exit_value": exit_data.get("exit_value", 0),
                "exit_type": exit_data.get("exit_type", ""),
                "roi": exit_data.get("roi", 0),
                "hold_period": exit_data.get("exit_year", 0) - loan.get("reinvestment_year", 0),
            })

        reinvestment_loans_table.append(loan_data)

    # Generate cash reserve metrics table
    cash_reserve_metrics = reinvestment_summary.get("cash_reserve_metrics", {})
    cash_reserve_metrics_table = []

    if cash_reserve_metrics:
        cash_reserve_metrics_table = [
            {
                "metric": "Average Cash Reserve",
                "value": cash_reserve_metrics.get("avg_cash_reserve", 0),
                "percentage": cash_reserve_metrics.get("avg_cash_reserve_pct", 0) * 100,
            },
            {
                "metric": "Minimum Cash Reserve",
                "value": cash_reserve_metrics.get("min_cash_reserve", 0),
                "percentage": cash_reserve_metrics.get("min_cash_reserve_pct", 0) * 100,
            },
            {
                "metric": "Maximum Cash Reserve",
                "value": cash_reserve_metrics.get("max_cash_reserve", 0),
                "percentage": cash_reserve_metrics.get("max_cash_reserve_pct", 0) * 100,
            },
        ]

    # Create visualization dictionary
    visualization = {
        "charts": {
            "reinvestment_timeline": reinvestment_timeline,
            "reinvestment_by_zone_chart": reinvestment_by_zone_chart,
            "reinvestment_by_year_chart": reinvestment_by_year_chart,
            "reinvestment_by_strategy_chart": reinvestment_by_strategy_chart,
            "reinvestment_by_source_chart": reinvestment_by_source_chart,
            "cash_reserve_chart": cash_reserve_chart,
            "allocation_comparison_chart": allocation_comparison_chart,
            "reinvestment_efficiency_chart": reinvestment_efficiency_chart,
            "reinvestment_performance_chart": reinvestment_performance_chart,
            "exit_type_distribution_chart": exit_type_distribution_chart,
            "reinvestment_timing_chart": reinvestment_timing_chart,
            "reinvestment_vs_exits_chart": reinvestment_vs_exits_chart,
            "loan_size_distribution_chart": loan_size_distribution_chart,
        },
        "tables": {
            "reinvestment_summary_table": reinvestment_summary_table,
            "reinvestment_events_table": reinvestment_events_table,
            "reinvestment_loans_table": reinvestment_loans_table,
            "cash_reserve_metrics_table": cash_reserve_metrics_table,
        },
        "kpis": {
            "total_reinvested": reinvestment_summary.get("total_reinvested", 0),
            "num_reinvestment_events": reinvestment_summary.get("num_reinvestment_events", 0),
            "avg_reinvestment_amount": reinvestment_summary.get("avg_reinvestment_amount", 0),
            "reinvestment_ratio": reinvestment_efficiency.get("reinvestment_ratio", 0),
            "avg_time_to_reinvest": reinvestment_efficiency.get("avg_time_to_reinvest", 0),
            "reinvestment_roi": reinvestment_performance.get("roi", 0),
            "num_reinvestment_loans": len(reinvestment_loans),
            "reinvestment_portfolio_impact": reinvestment_efficiency.get("reinvestment_portfolio_impact", 0),
        },
    }

    return visualization


def calculate_zone_distribution(context: SimulationContext) -> Dict[str, float]:
    """
    Calculate the distribution of loans by zone.

    Args:
        context: Simulation context

    Returns:
        Dictionary of zone distributions (0-1)
    """
    # Get loans
    loans = getattr(context, "loans", [])

    # Calculate zone amounts
    zone_amounts = {}

    for loan in loans:
        zone = loan.get("zone")
        loan_size = loan.get("loan_size", 0)

        if zone not in zone_amounts:
            zone_amounts[zone] = 0

        zone_amounts[zone] += loan_size

    # Calculate allocations
    total_amount = sum(zone_amounts.values())
    zone_distribution = {}

    if total_amount > 0:
        zone_distribution = {zone: amount / total_amount for zone, amount in zone_amounts.items()}

    # Ensure all zones have a value
    for zone in ["green", "orange", "red"]:
        if zone not in zone_distribution:
            zone_distribution[zone] = 0.0

    return zone_distribution


def calculate_avg_ltv(context: SimulationContext) -> float:
    """
    Calculate the average LTV of the portfolio.

    Args:
        context: Simulation context

    Returns:
        Average LTV (0-1)
    """
    # Get loans
    loans = getattr(context, "loans", [])

    if not loans:
        return 0.0

    # Calculate weighted average LTV
    total_loan_size = sum(loan.get("loan_size", 0) for loan in loans)

    if total_loan_size == 0:
        return 0.0

    weighted_ltv_sum = sum(loan.get("loan_size", 0) * loan.get("ltv", 0) for loan in loans)

    return weighted_ltv_sum / total_loan_size


def calculate_concentration_risk(context: SimulationContext) -> Dict[str, float]:
    """
    Calculate concentration risk metrics for the portfolio.

    Args:
        context: Simulation context

    Returns:
        Dictionary of concentration risk metrics
    """
    # Get loans
    loans = getattr(context, "loans", [])

    if not loans:
        return {
            "hhi_zone": 0.0,
            "hhi_suburb": 0.0,
            "top_5_concentration": 0.0,
            "top_10_concentration": 0.0,
        }

    # Calculate Herfindahl-Hirschman Index (HHI) for zone concentration
    zone_amounts = {}
    for loan in loans:
        zone = loan.get("zone")
        loan_size = loan.get("loan_size", 0)

        if zone not in zone_amounts:
            zone_amounts[zone] = 0

        zone_amounts[zone] += loan_size

    total_amount = sum(zone_amounts.values())

    if total_amount == 0:
        return {
            "hhi_zone": 0.0,
            "hhi_suburb": 0.0,
            "top_5_concentration": 0.0,
            "top_10_concentration": 0.0,
        }

    zone_shares = {zone: amount / total_amount for zone, amount in zone_amounts.items()}
    hhi_zone = sum(share ** 2 for share in zone_shares.values())

    # Calculate HHI for suburb concentration
    suburb_amounts = {}
    for loan in loans:
        suburb = loan.get("suburb_name", "unknown")
        loan_size = loan.get("loan_size", 0)

        if suburb not in suburb_amounts:
            suburb_amounts[suburb] = 0

        suburb_amounts[suburb] += loan_size

    suburb_shares = {suburb: amount / total_amount for suburb, amount in suburb_amounts.items()}
    hhi_suburb = sum(share ** 2 for share in suburb_shares.values())

    # Calculate top 5 and top 10 concentration
    sorted_suburbs = sorted(suburb_amounts.items(), key=lambda x: x[1], reverse=True)

    top_5_amount = sum(amount for _, amount in sorted_suburbs[:5])
    top_10_amount = sum(amount for _, amount in sorted_suburbs[:10])

    top_5_concentration = top_5_amount / total_amount
    top_10_concentration = top_10_amount / total_amount

    return {
        "hhi_zone": hhi_zone,
        "hhi_suburb": hhi_suburb,
        "top_5_concentration": top_5_concentration,
        "top_10_concentration": top_10_concentration,
    }


def calculate_risk_impact(portfolio_before: Dict[str, Any], portfolio_after: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the impact of reinvestment on portfolio risk.

    Args:
        portfolio_before: Portfolio state before reinvestment
        portfolio_after: Portfolio state after reinvestment

    Returns:
        Dictionary of risk impact metrics
    """
    # Calculate changes in key metrics
    zone_distribution_before = portfolio_before.get("zone_distribution", {})
    zone_distribution_after = portfolio_after.get("zone_distribution", {})

    zone_distribution_change = {}
    for zone in set(zone_distribution_before.keys()) | set(zone_distribution_after.keys()):
        before = zone_distribution_before.get(zone, 0)
        after = zone_distribution_after.get(zone, 0)
        zone_distribution_change[zone] = after - before

    avg_ltv_before = portfolio_before.get("avg_ltv", 0)
    avg_ltv_after = portfolio_after.get("avg_ltv", 0)
    avg_ltv_change = avg_ltv_after - avg_ltv_before

    concentration_risk_before = portfolio_before.get("concentration_risk", {})
    concentration_risk_after = portfolio_after.get("concentration_risk", {})

    concentration_risk_change = {}
    for metric in set(concentration_risk_before.keys()) | set(concentration_risk_after.keys()):
        before = concentration_risk_before.get(metric, 0)
        after = concentration_risk_after.get(metric, 0)
        concentration_risk_change[metric] = after - before

    # Calculate overall risk score change
    # Higher score means higher risk
    risk_score_before = (
        avg_ltv_before * 0.3 +
        concentration_risk_before.get("hhi_zone", 0) * 0.2 +
        concentration_risk_before.get("hhi_suburb", 0) * 0.2 +
        concentration_risk_before.get("top_5_concentration", 0) * 0.15 +
        concentration_risk_before.get("top_10_concentration", 0) * 0.15
    )

    risk_score_after = (
        avg_ltv_after * 0.3 +
        concentration_risk_after.get("hhi_zone", 0) * 0.2 +
        concentration_risk_after.get("hhi_suburb", 0) * 0.2 +
        concentration_risk_after.get("top_5_concentration", 0) * 0.15 +
        concentration_risk_after.get("top_10_concentration", 0) * 0.15
    )

    risk_score_change = risk_score_after - risk_score_before

    # Calculate diversification impact
    # Positive means more diversified, negative means less diversified
    diversification_impact = (
        -concentration_risk_change.get("hhi_zone", 0) * 0.4 +
        -concentration_risk_change.get("hhi_suburb", 0) * 0.4 +
        -concentration_risk_change.get("top_5_concentration", 0) * 0.1 +
        -concentration_risk_change.get("top_10_concentration", 0) * 0.1
    )

    # Calculate risk-adjusted return impact
    # This is a simplified calculation - in a real system, this would be more complex
    risk_adjusted_return_impact = -risk_score_change

    return {
        "zone_distribution_change": zone_distribution_change,
        "avg_ltv_change": avg_ltv_change,
        "concentration_risk_change": concentration_risk_change,
        "risk_score_before": risk_score_before,
        "risk_score_after": risk_score_after,
        "risk_score_change": risk_score_change,
        "diversification_impact": diversification_impact,
        "risk_adjusted_return_impact": risk_adjusted_return_impact,
    }
