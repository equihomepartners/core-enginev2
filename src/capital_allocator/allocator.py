"""
Capital allocator module for the EQU IHOME SIM ENGINE v2.

This module is responsible for allocating capital across zones based on policy.
It integrates with the TLS module to get zone data and implements allocation
policy enforcement with error handling, visualization support, and progress reporting.
"""

import asyncio
import time
from typing import Dict, Any, List, Optional, Tuple

import numpy as np
import structlog

from src.engine.simulation_context import SimulationContext
from src.tls_module import get_tls_manager
from src.tls_module.tls_data_provider import get_tls_provider
from src.utils.error_handler import ValidationError, ErrorCode, handle_exception, log_error
from src.api.websocket_manager import get_websocket_manager
from src.utils.metrics import increment_counter, observe_histogram, set_gauge

logger = structlog.get_logger(__name__)


async def allocate_capital(context: SimulationContext, year: float = 0.0) -> None:
    """
    Allocate capital across zones based on policy.

    This function allocates capital across zones based on the allocation policy
    specified in the configuration. It integrates with the TLS module to get
    zone data and implements allocation policy enforcement with error handling,
    visualization support, and progress reporting.

    Args:
        context: Simulation context
        year: Current simulation year (default: 0.0 for initial allocation)

    Raises:
        ValidationError: If the allocation policy is invalid
    """
    start_time = time.time()
    logger.info("Allocating capital")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=0.0,
            message="Starting capital allocation",
        )

        # Send informational message
        await websocket_manager.send_info(
            simulation_id=context.run_id,
            message="Allocating capital across zones based on policy",
            data={
                "fund_size": context.config.fund_size,
                "fund_term": context.config.fund_term,
                "vintage_year": context.config.vintage_year,
            },
        )

        # Get configuration parameters
        config = context.config

        # Get zone allocations from configuration
        # If not specified in the config, use default allocations
        zone_allocations = getattr(config, "zone_allocations", None)
        if zone_allocations:
            zone_allocations = zone_allocations.dict()
        else:
            zone_allocations = {"green": 0.6, "orange": 0.3, "red": 0.1}

        # Validate zone allocations
        validate_zone_allocations(zone_allocations)

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=20.0,
            message="Zone allocations validated",
        )

        # Check for cancellation
        if websocket_manager.is_cancelled(context.run_id):
            logger.info("Capital allocation cancelled", run_id=context.run_id)
            await websocket_manager.send_info(
                simulation_id=context.run_id,
                message="Capital allocation cancelled",
            )
            return

        # Initialize TLS module if not already initialized
        if not hasattr(context, "tls_manager") or context.tls_manager is None:
            # Get TLS manager
            tls_manager = get_tls_manager(use_mock=True)

            # Load TLS data
            await tls_manager.load_data(simulation_id=context.run_id)

            # Store TLS manager in context
            context.tls_manager = tls_manager

            # Store zone distribution in context
            context.zone_distribution = tls_manager.get_zone_distribution()

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=40.0,
            message="TLS data loaded",
        )

        # Store target allocations in context
        context.zone_targets = zone_allocations

        # Calculate capital allocation by zone
        fund_size = config.fund_size
        capital_by_zone = {}
        for zone, allocation in zone_allocations.items():
            capital_by_zone[zone] = fund_size * allocation

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=60.0,
            message="Capital allocation calculated",
        )

        # Check for cancellation
        if websocket_manager.is_cancelled(context.run_id):
            logger.info("Capital allocation cancelled", run_id=context.run_id)
            await websocket_manager.send_info(
                simulation_id=context.run_id,
                message="Capital allocation cancelled",
            )
            return

        # Generate allocation visualization data
        allocation_visualization = generate_allocation_visualization(zone_allocations)

        # Store allocation visualization in context
        context.allocation_visualization = allocation_visualization

        # Calculate allocation statistics
        allocation_stats = calculate_allocation_statistics(
            zone_allocations, context.zone_distribution
        )

        # Store allocation statistics in context
        context.allocation_stats = allocation_stats

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=80.0,
            message="Allocation statistics calculated",
        )

        # Log allocation
        logger.info(
            "Capital allocation calculated",
            fund_size=fund_size,
            zone_allocations=zone_allocations,
            capital_by_zone=capital_by_zone,
            allocation_stats=allocation_stats,
        )

        # Store actual allocations in context (will be updated by loan generator)
        context.zone_actual = {zone: 0.0 for zone in zone_allocations}

        # Store capital by zone in context
        context.capital_by_zone = capital_by_zone

        # Store intermediate results for visualization
        context.capital_allocator_results = {
            "zone_targets": zone_allocations,
            "capital_by_zone": capital_by_zone,
            "allocation_visualization": allocation_visualization,
            "allocation_stats": allocation_stats,
        }

        # Track allocation history
        track_allocation_history(context, year)

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=100.0,
            message="Capital allocation completed",
            data={
                "zone_targets": zone_allocations,
                "capital_by_zone": capital_by_zone,
                "allocation_stats": allocation_stats,
            },
        )

        # Send result message
        await websocket_manager.send_result(
            simulation_id=context.run_id,
            result={
                "module": "capital_allocator",
                "zone_targets": zone_allocations,
                "capital_by_zone": capital_by_zone,
                "allocation_stats": allocation_stats,
                "allocation_visualization": allocation_visualization,
                "execution_time": time.time() - start_time,
            },
        )

        # Update metrics
        increment_counter("capital_allocation_completed_total")
        observe_histogram(
            "capital_allocation_runtime_seconds",
            time.time() - start_time,
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
                "module": "capital_allocator",
            },
        )

        # Re-raise exception
        raise


def validate_zone_allocations(zone_allocations: Dict[str, float]) -> None:
    """
    Validate zone allocations.

    Args:
        zone_allocations: Dictionary of zone allocations (zone -> percentage)

    Raises:
        ValidationError: If the zone allocations are invalid
    """
    # Check if zone allocations are provided
    if not zone_allocations:
        raise ValidationError(
            "Zone allocations not provided",
            code=ErrorCode.MISSING_PARAMETER,
        )

    # Check if zone allocations sum to approximately 1.0
    total_allocation = sum(zone_allocations.values())
    if not 0.99 <= total_allocation <= 1.01:
        raise ValidationError(
            f"Zone allocations must sum to 1.0, got {total_allocation}",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={"zone_allocations": zone_allocations},
        )

    # Check if zone allocations are non-negative
    for zone, allocation in zone_allocations.items():
        if allocation < 0:
            raise ValidationError(
                f"Zone allocation for {zone} must be non-negative, got {allocation}",
                code=ErrorCode.PARAMETER_OUT_OF_RANGE,
                details={"zone": zone, "allocation": allocation},
            )

    # Check if zone allocations are valid zones
    valid_zones = {"green", "orange", "red"}
    for zone in zone_allocations:
        if zone not in valid_zones:
            raise ValidationError(
                f"Invalid zone: {zone}. Valid zones are: {', '.join(valid_zones)}",
                code=ErrorCode.INVALID_PARAMETER,
                details={"zone": zone, "valid_zones": list(valid_zones)},
            )


def generate_allocation_visualization(zone_allocations: Dict[str, float]) -> Dict[str, Any]:
    """
    Generate visualization data for zone allocations.

    Args:
        zone_allocations: Dictionary of zone allocations (zone -> percentage)

    Returns:
        Dictionary containing visualization data
    """
    # Generate pie chart data
    pie_chart_data = [
        {"zone": zone, "allocation": allocation * 100}
        for zone, allocation in zone_allocations.items()
    ]

    # Generate bar chart data
    bar_chart_data = [
        {"zone": zone, "allocation": allocation * 100}
        for zone, allocation in zone_allocations.items()
    ]

    # Generate table data
    table_data = [
        {"zone": zone, "allocation": f"{allocation * 100:.2f}%"}
        for zone, allocation in zone_allocations.items()
    ]

    return {
        "pie_chart": pie_chart_data,
        "bar_chart": bar_chart_data,
        "table": table_data,
    }


def calculate_allocation_statistics(
    zone_allocations: Dict[str, float], zone_distribution: Dict[str, float]
) -> Dict[str, Any]:
    """
    Calculate statistics for zone allocations.

    Args:
        zone_allocations: Dictionary of zone allocations (zone -> percentage)
        zone_distribution: Dictionary of zone distribution (zone -> percentage)

    Returns:
        Dictionary containing allocation statistics
    """
    # Calculate allocation vs. distribution
    allocation_vs_distribution = {}
    for zone in zone_allocations:
        allocation = zone_allocations.get(zone, 0.0)
        distribution = zone_distribution.get(zone, 0.0)

        # Calculate difference
        difference = allocation - distribution

        # Calculate relative difference
        relative_difference = (
            difference / distribution if distribution > 0 else 0.0
        )

        allocation_vs_distribution[zone] = {
            "allocation": allocation,
            "distribution": distribution,
            "difference": difference,
            "relative_difference": relative_difference,
        }

    # Calculate concentration metrics
    concentration = {
        "herfindahl_index": sum(allocation ** 2 for allocation in zone_allocations.values()),
        "max_allocation": max(zone_allocations.values()),
        "min_allocation": min(zone_allocations.values()),
        "range": max(zone_allocations.values()) - min(zone_allocations.values()),
    }

    return {
        "allocation_vs_distribution": allocation_vs_distribution,
        "concentration": concentration,
    }


async def rebalance_allocation(
    context: SimulationContext, tolerance: float = 0.05
) -> Dict[str, float]:
    """
    Rebalance allocation to match target allocations.

    Args:
        context: Simulation context
        tolerance: Tolerance for allocation mismatch

    Returns:
        Dictionary of allocation adjustments by zone
    """
    start_time = time.time()
    logger.info("Rebalancing allocation")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=0.0,
            message="Starting allocation rebalancing",
        )

        # Get target and actual allocations
        targets = context.zone_targets
        actual = context.zone_actual

        # Calculate total capital allocated
        total_capital = sum(actual.values())

        # Calculate actual allocation percentages
        actual_pct = {
            zone: amount / total_capital if total_capital > 0 else 0.0
            for zone, amount in actual.items()
        }

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=30.0,
            message="Calculating allocation gaps",
        )

        # Calculate allocation gaps
        gaps = {zone: targets.get(zone, 0.0) - actual_pct.get(zone, 0.0) for zone in targets}

        # Identify zones that need adjustment
        adjustments = {}
        for zone, gap in gaps.items():
            if abs(gap) > tolerance:
                # Calculate adjustment amount
                adjustment = gap * total_capital
                adjustments[zone] = adjustment

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=60.0,
            message="Calculating adjustments",
        )

        # Generate rebalancing visualization
        rebalancing_visualization = generate_rebalancing_visualization(
            targets, actual_pct, gaps, adjustments
        )

        # Store rebalancing visualization in context
        context.rebalancing_visualization = rebalancing_visualization

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=90.0,
            message="Rebalancing visualization generated",
        )

        # Log rebalancing
        if adjustments:
            logger.info(
                "Allocation rebalancing required",
                targets=targets,
                actual=actual_pct,
                gaps=gaps,
                adjustments=adjustments,
            )
        else:
            logger.info(
                "Allocation within tolerance, no rebalancing needed",
                targets=targets,
                actual=actual_pct,
                tolerance=tolerance,
            )

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=100.0,
            message="Allocation rebalancing completed",
            data={
                "targets": targets,
                "actual": actual_pct,
                "gaps": gaps,
                "adjustments": adjustments,
            },
        )

        # Update metrics
        increment_counter("allocation_rebalancing_completed_total")
        observe_histogram(
            "allocation_rebalancing_runtime_seconds",
            time.time() - start_time,
        )

        return adjustments

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
                "module": "capital_allocator",
            },
        )

        # Re-raise exception
        raise


def generate_rebalancing_visualization(
    targets: Dict[str, float],
    actual: Dict[str, float],
    gaps: Dict[str, float],
    adjustments: Dict[str, float],
) -> Dict[str, Any]:
    """
    Generate visualization data for allocation rebalancing.

    Args:
        targets: Dictionary of target allocations (zone -> percentage)
        actual: Dictionary of actual allocations (zone -> percentage)
        gaps: Dictionary of allocation gaps (zone -> percentage)
        adjustments: Dictionary of allocation adjustments (zone -> amount)

    Returns:
        Dictionary containing visualization data
    """
    # Generate comparison chart data
    comparison_chart_data = []
    for zone in targets:
        comparison_chart_data.append({
            "zone": zone,
            "target": targets.get(zone, 0.0) * 100,
            "actual": actual.get(zone, 0.0) * 100,
            "gap": gaps.get(zone, 0.0) * 100,
        })

    # Generate adjustment chart data
    adjustment_chart_data = [
        {"zone": zone, "adjustment": adjustment}
        for zone, adjustment in adjustments.items()
    ]

    # Generate table data
    table_data = []
    for zone in targets:
        table_data.append({
            "zone": zone,
            "target": f"{targets.get(zone, 0.0) * 100:.2f}%",
            "actual": f"{actual.get(zone, 0.0) * 100:.2f}%",
            "gap": f"{gaps.get(zone, 0.0) * 100:.2f}%",
            "adjustment": f"${adjustments.get(zone, 0.0):,.2f}",
        })

    return {
        "comparison_chart": comparison_chart_data,
        "adjustment_chart": adjustment_chart_data,
        "table": table_data,
    }


async def calculate_loan_counts(
    context: SimulationContext, avg_loan_size: float
) -> Dict[str, int]:
    """
    Calculate the number of loans to generate for each zone.

    Args:
        context: Simulation context
        avg_loan_size: Average loan size

    Returns:
        Dictionary of loan counts by zone
    """
    start_time = time.time()
    logger.info("Calculating loan counts")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=0.0,
            message="Starting loan count calculation",
        )

        # Get capital allocation by zone
        capital_by_zone = getattr(context, "capital_by_zone", None)
        if not capital_by_zone:
            capital_by_zone = {}
            for zone, allocation in context.zone_targets.items():
                capital_by_zone[zone] = context.config.fund_size * allocation

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=50.0,
            message="Calculating loan counts by zone",
        )

        # Calculate loan counts
        loan_counts = {}
        for zone, capital in capital_by_zone.items():
            loan_counts[zone] = int(capital / avg_loan_size)

        # Generate loan count visualization
        loan_count_visualization = generate_loan_count_visualization(
            loan_counts, capital_by_zone, avg_loan_size
        )

        # Store loan count visualization in context
        context.loan_count_visualization = loan_count_visualization

        # Log loan counts
        logger.info(
            "Loan counts calculated",
            avg_loan_size=avg_loan_size,
            capital_by_zone=capital_by_zone,
            loan_counts=loan_counts,
        )

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=100.0,
            message="Loan count calculation completed",
            data={
                "avg_loan_size": avg_loan_size,
                "capital_by_zone": capital_by_zone,
                "loan_counts": loan_counts,
            },
        )

        # Update metrics
        increment_counter("loan_count_calculation_completed_total")
        observe_histogram(
            "loan_count_calculation_runtime_seconds",
            time.time() - start_time,
        )

        return loan_counts

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
                "module": "capital_allocator",
            },
        )

        # Re-raise exception
        raise


def track_allocation_history(context: SimulationContext, year: float) -> None:
    """
    Track allocation history over time.

    Args:
        context: Simulation context
        year: Current simulation year
    """
    # Initialize allocation history if not exists
    if not hasattr(context, "allocation_history"):
        context.allocation_history = []

    # Get current allocation
    current_allocation = {
        "year": year,
        "targets": context.zone_targets.copy(),
        "actual": context.zone_actual.copy() if hasattr(context, "zone_actual") else {},
        "gap": {
            zone: context.zone_targets.get(zone, 0.0) -
                 (context.zone_actual.get(zone, 0.0) if hasattr(context, "zone_actual") else 0.0)
            for zone in context.zone_targets
        },
        "capital_by_zone": context.capital_by_zone.copy() if hasattr(context, "capital_by_zone") else {},
        "timestamp": time.time(),
    }

    # Add to history
    context.allocation_history.append(current_allocation)

    # Generate allocation history visualization
    if len(context.allocation_history) > 1:
        context.allocation_history_visualization = generate_allocation_history_visualization(
            context.allocation_history
        )


def generate_allocation_history_visualization(allocation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate visualization data for allocation history.

    Args:
        allocation_history: List of allocation history entries

    Returns:
        Dictionary containing visualization data
    """
    # Extract data for visualization
    years = [entry["year"] for entry in allocation_history]
    zones = set()
    for entry in allocation_history:
        zones.update(entry["targets"].keys())

    # Generate target allocation history
    target_history = {zone: [] for zone in zones}
    for entry in allocation_history:
        for zone in zones:
            target_history[zone].append({
                "year": entry["year"],
                "allocation": entry["targets"].get(zone, 0.0) * 100,
            })

    # Generate actual allocation history
    actual_history = {zone: [] for zone in zones}
    for entry in allocation_history:
        for zone in zones:
            actual_history[zone].append({
                "year": entry["year"],
                "allocation": entry["actual"].get(zone, 0.0) * 100,
            })

    # Generate gap history
    gap_history = {zone: [] for zone in zones}
    for entry in allocation_history:
        for zone in zones:
            gap_history[zone].append({
                "year": entry["year"],
                "gap": entry["gap"].get(zone, 0.0) * 100,
            })

    # Generate allocation drift chart data
    drift_chart_data = []
    for zone in zones:
        zone_data = []
        for entry in allocation_history:
            zone_data.append({
                "year": entry["year"],
                "target": entry["targets"].get(zone, 0.0) * 100,
                "actual": entry["actual"].get(zone, 0.0) * 100,
                "gap": entry["gap"].get(zone, 0.0) * 100,
            })
        drift_chart_data.append({
            "zone": zone,
            "data": zone_data,
        })

    # Generate table data
    table_data = []
    for entry in allocation_history:
        row = {
            "year": entry["year"],
        }
        for zone in zones:
            row[f"{zone}_target"] = f"{entry['targets'].get(zone, 0.0) * 100:.2f}%"
            row[f"{zone}_actual"] = f"{entry['actual'].get(zone, 0.0) * 100:.2f}%"
            row[f"{zone}_gap"] = f"{entry['gap'].get(zone, 0.0) * 100:.2f}%"
        table_data.append(row)

    return {
        "target_history": target_history,
        "actual_history": actual_history,
        "gap_history": gap_history,
        "drift_chart": drift_chart_data,
        "table": table_data,
    }


def generate_loan_count_visualization(
    loan_counts: Dict[str, int],
    capital_by_zone: Dict[str, float],
    avg_loan_size: float,
) -> Dict[str, Any]:
    """
    Generate visualization data for loan counts.

    Args:
        loan_counts: Dictionary of loan counts by zone
        capital_by_zone: Dictionary of capital allocation by zone
        avg_loan_size: Average loan size

    Returns:
        Dictionary containing visualization data
    """
    # Generate bar chart data
    bar_chart_data = [
        {"zone": zone, "count": count}
        for zone, count in loan_counts.items()
    ]

    # Generate pie chart data
    pie_chart_data = [
        {"zone": zone, "count": count}
        for zone, count in loan_counts.items()
    ]

    # Generate table data
    table_data = []
    for zone in loan_counts:
        table_data.append({
            "zone": zone,
            "capital": f"${capital_by_zone.get(zone, 0.0):,.2f}",
            "loan_count": loan_counts.get(zone, 0),
            "avg_loan_size": f"${avg_loan_size:,.2f}",
        })

    return {
        "bar_chart": bar_chart_data,
        "pie_chart": pie_chart_data,
        "table": table_data,
    }


async def update_actual_allocation(context: SimulationContext, year: float = 0.0) -> None:
    """
    Update actual allocation based on generated loans.

    Args:
        context: Simulation context
        year: Current simulation year (default: 0.0 for initial allocation)
    """
    start_time = time.time()
    logger.info("Updating actual allocation")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=0.0,
            message="Starting actual allocation update",
        )

        # Calculate actual allocation by zone
        zone_totals = {zone: 0.0 for zone in context.zone_targets}

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=30.0,
            message="Calculating zone totals",
        )

        for loan in context.loans:
            zone = loan.get("zone")
            loan_size = loan.get("loan_size", 0.0)

            if zone in zone_totals:
                zone_totals[zone] += loan_size

        # Calculate total loan amount
        total_loan_amount = sum(zone_totals.values())

        # Update actual allocation percentages
        if total_loan_amount > 0:
            context.zone_actual = {
                zone: amount / total_loan_amount for zone, amount in zone_totals.items()
            }

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=60.0,
            message="Generating allocation comparison",
        )

        # Generate allocation comparison visualization
        allocation_comparison = generate_allocation_comparison(
            context.zone_targets, context.zone_actual
        )

        # Store allocation comparison in context
        context.allocation_comparison = allocation_comparison

        # Track allocation history
        track_allocation_history(context, year)

        # Log actual allocation
        logger.info(
            "Actual allocation updated",
            zone_totals=zone_totals,
            total_loan_amount=total_loan_amount,
            actual_allocation=context.zone_actual,
        )

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=100.0,
            message="Actual allocation update completed",
            data={
                "zone_totals": zone_totals,
                "total_loan_amount": total_loan_amount,
                "actual_allocation": context.zone_actual,
            },
        )

        # Update metrics
        increment_counter("actual_allocation_update_completed_total")
        observe_histogram(
            "actual_allocation_update_runtime_seconds",
            time.time() - start_time,
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
                "module": "capital_allocator",
            },
        )

        # Re-raise exception
        raise


def generate_allocation_comparison(
    targets: Dict[str, float], actual: Dict[str, float]
) -> Dict[str, Any]:
    """
    Generate visualization data for allocation comparison.

    Args:
        targets: Dictionary of target allocations (zone -> percentage)
        actual: Dictionary of actual allocations (zone -> percentage)

    Returns:
        Dictionary containing visualization data
    """
    # Generate comparison chart data
    comparison_chart_data = []
    for zone in targets:
        comparison_chart_data.append({
            "zone": zone,
            "target": targets.get(zone, 0.0) * 100,
            "actual": actual.get(zone, 0.0) * 100,
        })

    # Generate table data
    table_data = []
    for zone in targets:
        target = targets.get(zone, 0.0)
        actual_val = actual.get(zone, 0.0)
        difference = actual_val - target

        table_data.append({
            "zone": zone,
            "target": f"{target * 100:.2f}%",
            "actual": f"{actual_val * 100:.2f}%",
            "difference": f"{difference * 100:+.2f}%",
        })

    return {
        "comparison_chart": comparison_chart_data,
        "table": table_data,
    }


async def get_zone_properties(
    context: SimulationContext, zone: str, limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get properties in a specific zone.

    Args:
        context: Simulation context
        zone: Zone category (green, orange, red)
        limit: Maximum number of properties to return

    Returns:
        List of properties in the zone
    """
    start_time = time.time()
    logger.info("Getting zone properties", zone=zone, limit=limit)

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=0.0,
            message=f"Getting properties in {zone} zone",
        )

        # Get TLS manager
        tls_manager = getattr(context, "tls_manager", None)
        if tls_manager is None:
            # Initialize TLS module
            tls_manager = get_tls_manager(use_mock=True)

            # Load TLS data
            await tls_manager.load_data(simulation_id=context.run_id)

            # Store TLS manager in context
            context.tls_manager = tls_manager

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=30.0,
            message="TLS data loaded",
        )

        # Get suburbs in the zone
        suburbs = tls_manager.get_suburbs_by_zone(zone)

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=60.0,
            message=f"Found {len(suburbs)} suburbs in {zone} zone",
        )

        # Get properties in the suburbs
        properties = []
        for suburb in suburbs:
            for property_id, property_data in suburb.properties.items():
                properties.append({
                    "property_id": property_id,
                    "suburb_id": suburb.suburb_id,
                    "suburb_name": suburb.name,
                    "zone": zone,
                    "property_type": property_data.property_type,
                    "bedrooms": property_data.bedrooms,
                    "bathrooms": property_data.bathrooms,
                    "land_size": property_data.land_size,
                    "building_size": property_data.building_size,
                    "year_built": property_data.year_built,
                    "base_value": property_data.base_value,
                })

                if len(properties) >= limit:
                    break

            if len(properties) >= limit:
                break

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=100.0,
            message=f"Found {len(properties)} properties in {zone} zone",
            data={
                "zone": zone,
                "suburb_count": len(suburbs),
                "property_count": len(properties),
            },
        )

        # Update metrics
        increment_counter("zone_properties_retrieved_total", labels={"zone": zone})
        observe_histogram(
            "zone_properties_retrieval_runtime_seconds",
            time.time() - start_time,
            labels={"zone": zone},
        )

        return properties

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
                "module": "capital_allocator",
            },
        )

        # Re-raise exception
        raise


async def get_allocation_summary(context: SimulationContext) -> Dict[str, Any]:
    """
    Get a summary of the capital allocation.

    Args:
        context: Simulation context

    Returns:
        Dictionary containing allocation summary
    """
    start_time = time.time()
    logger.info("Getting allocation summary")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=0.0,
            message="Generating allocation summary",
        )

        # Get target and actual allocations
        targets = getattr(context, "zone_targets", {})
        actual = getattr(context, "zone_actual", {})

        # Get capital by zone
        capital_by_zone = getattr(context, "capital_by_zone", {})

        # Get allocation statistics
        allocation_stats = getattr(context, "allocation_stats", {})

        # Get allocation history
        allocation_history = getattr(context, "allocation_history", [])
        allocation_history_visualization = getattr(context, "allocation_history_visualization", {})

        # Generate summary
        summary = {
            "fund_size": context.config.fund_size,
            "target_allocation": targets,
            "actual_allocation": actual,
            "capital_by_zone": capital_by_zone,
            "allocation_stats": allocation_stats,
            "allocation_history": allocation_history,
            "allocation_history_visualization": allocation_history_visualization,
        }

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="capital_allocator",
            progress=100.0,
            message="Allocation summary generated",
            data=summary,
        )

        # Update metrics
        increment_counter("allocation_summary_generated_total")
        observe_histogram(
            "allocation_summary_generation_runtime_seconds",
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
                "module": "capital_allocator",
            },
        )

        # Re-raise exception
        raise
