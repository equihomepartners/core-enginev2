"""
Loan generator module for the EQU IHOME SIM ENGINE v2.

This module is responsible for generating loan portfolios based on configuration parameters.
It integrates with the Capital Allocator module to get zone allocations and the TLS module
to get property data. It implements loan generation with error handling, visualization support,
and progress reporting.
"""

import asyncio
import time
import uuid
from typing import Dict, Any, List, Optional, Tuple, Union

import numpy as np
import structlog

from src.engine.simulation_context import SimulationContext
from src.utils.metrics import increment_counter, observe_histogram, set_gauge
from src.utils.error_handler import ValidationError, ErrorCode, handle_exception, log_error
from src.api.websocket_manager import get_websocket_manager
from src.capital_allocator import calculate_loan_counts, update_actual_allocation
from src.tls_module import get_tls_manager

logger = structlog.get_logger(__name__)


async def generate_reinvestment_loans(
    context: SimulationContext,
    reinvestment_amount: float,
    target_zones: Dict[str, float],
    year: float
) -> List[Dict[str, Any]]:
    """
    Generate loans for reinvestment.

    This function generates a subset of loans for reinvestment based on the
    reinvestment amount and target zone allocations. It uses the same loan
    generation logic as the main generate_loans function but with specific
    parameters for reinvestment.

    Args:
        context: Simulation context
        reinvestment_amount: Amount to reinvest
        target_zones: Target allocation by zone for reinvestment
        year: Current simulation year

    Returns:
        List of generated loans

    Raises:
        ValidationError: If the loan generation parameters are invalid
    """
    start_time = time.time()
    logger.info("Generating reinvestment loans",
                reinvestment_amount=reinvestment_amount,
                target_zones=target_zones,
                year=year)

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=0.0,
            message="Starting reinvestment loan generation",
            data={
                "reinvestment_amount": reinvestment_amount,
                "target_zones": target_zones,
                "year": year,
            },
        )

        # Send informational message
        await websocket_manager.send_info(
            simulation_id=context.run_id,
            message="Generating reinvestment loans",
            data={
                "reinvestment_amount": reinvestment_amount,
                "target_zones": target_zones,
                "year": year,
                "avg_loan_size": context.config.avg_loan_size,
            },
        )

        # Get configuration
        config = context.config

        # Get RNG
        rng = getattr(context, "rng", np.random.default_rng())

        # Calculate loan counts for reinvestment
        avg_loan_size = config.avg_loan_size
        loan_counts = {}
        for zone, allocation in target_zones.items():
            zone_amount = reinvestment_amount * allocation
            loan_counts[zone] = max(1, int(zone_amount / avg_loan_size))

        # Calculate total number of loans
        num_loans = sum(loan_counts.values())

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=20.0,
            message="Calculated reinvestment loan counts by zone",
            data={
                "loan_counts": loan_counts,
                "total_loans": num_loans,
            },
        )

        # Generate loan sizes
        loan_sizes = generate_loan_sizes(
            num_loans=num_loans,
            avg_loan_size=avg_loan_size,
            loan_size_std_dev=config.loan_size_std_dev,
            min_loan_size=config.min_loan_size,
            max_loan_size=config.max_loan_size,
            rng=rng,
        )

        # Adjust loan sizes to match reinvestment amount
        total_loan_size = sum(loan_sizes)
        if total_loan_size > reinvestment_amount:
            # Scale down loan sizes
            scale_factor = reinvestment_amount / total_loan_size
            loan_sizes = [size * scale_factor for size in loan_sizes]
            total_loan_size = sum(loan_sizes)

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=40.0,
            message="Generated reinvestment loan sizes",
            data={
                "total_loan_size": total_loan_size,
                "reinvestment_amount": reinvestment_amount,
            },
        )

        # Generate LTV ratios
        ltv_ratios = generate_ltv_ratios(
            num_loans=num_loans,
            avg_ltv=config.avg_loan_ltv,
            ltv_std_dev=config.ltv_std_dev,
            min_ltv=config.min_ltv,
            max_ltv=config.max_ltv,
            rng=rng,
        )

        # Assign loans to zones based on loan counts
        zones = assign_loans_to_zones(num_loans, loan_counts)

        # Generate loan terms
        loan_terms = generate_loan_terms(
            num_loans=num_loans,
            avg_loan_term=config.avg_loan_term,
            rng=rng,
        )

        # Generate interest rates
        interest_rates = generate_interest_rates(
            num_loans=num_loans,
            avg_interest_rate=config.avg_loan_interest_rate,
            rng=rng,
        )

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=60.0,
            message="Generated reinvestment loan parameters",
        )

        # Get property data from TLS module
        property_data_by_zone = {}
        for zone in set(zones):
            properties = await get_properties_for_zone(context, zone, num_loans)
            property_data_by_zone[zone] = properties

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=80.0,
            message="Retrieved property data for reinvestment loans",
        )

        # Create loan objects
        loans = []
        for i in range(num_loans):
            loan_id = str(uuid.uuid4())
            zone = zones[i]

            # Get property data for this loan
            property_data = get_property_for_loan(property_data_by_zone, zone, i)

            loan = {
                "loan_id": loan_id,
                "loan_size": loan_sizes[i],
                "ltv": ltv_ratios[i],
                "zone": zone,
                "term": loan_terms[i],
                "interest_rate": interest_rates[i],
                "origination_year": int(year),
                "origination_month": 1,  # Default to January for reinvestment loans
                "property_value": loan_sizes[i] / ltv_ratios[i],
                "property_id": property_data.get("property_id", ""),
                "suburb_id": property_data.get("suburb_id", ""),
                "suburb_name": property_data.get("suburb_name", ""),
                "property_type": property_data.get("property_type", ""),
                "bedrooms": property_data.get("bedrooms", 0),
                "bathrooms": property_data.get("bathrooms", 0),
                "land_size": property_data.get("land_size", 0.0),
                "building_size": property_data.get("building_size", 0.0),
                "year_built": property_data.get("year_built", 0),
                "is_reinvestment": True,
                "reinvestment_year": year,
            }

            loans.append(loan)

            # Update metrics
            increment_counter("reinvestment_loans_generated_total", labels={"zone": zone})

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=100.0,
            message="Reinvestment loan generation completed",
            data={
                "num_loans": num_loans,
                "total_loan_size": total_loan_size,
                "reinvestment_amount": reinvestment_amount,
            },
        )

        # Update metrics
        increment_counter("reinvestment_loan_generation_completed_total")
        observe_histogram(
            "reinvestment_loan_generation_runtime_seconds",
            time.time() - start_time,
        )

        return loans

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
                "module": "loan_generator",
                "context": {
                    "reinvestment_amount": reinvestment_amount,
                    "target_zones": target_zones,
                    "year": year,
                },
            },
        )

        # Re-raise exception
        raise


async def generate_loans(context: SimulationContext, year: float = 0.0) -> None:
    """
    Generate a loan portfolio based on configuration parameters.

    This function generates a loan portfolio based on the configuration parameters
    and the capital allocation. It integrates with the Capital Allocator module to
    get zone allocations and the TLS module to get property data. It implements
    loan generation with error handling, visualization support, and progress reporting.

    Args:
        context: Simulation context
        year: Current simulation year (default: 0.0 for initial allocation)

    Raises:
        ValidationError: If the loan generation parameters are invalid
    """
    start_time = time.time()
    logger.info("Generating loans")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=0.0,
            message="Starting loan generation",
        )

        # Send informational message
        await websocket_manager.send_info(
            simulation_id=context.run_id,
            message="Generating loan portfolio based on configuration parameters",
            data={
                "avg_loan_size": context.config.avg_loan_size,
                "avg_loan_ltv": context.config.avg_loan_ltv,
                "avg_loan_term": context.config.avg_loan_term,
                "avg_loan_interest_rate": context.config.avg_loan_interest_rate,
            },
        )

        # Get configuration parameters
        config = context.config

        # Get random number generator
        if context.rng is None:
            # Import here to avoid circular imports
            from src.monte_carlo.rng_factory import get_rng
            context.rng = get_rng("loan_generation", 0)

        rng = context.rng

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=10.0,
            message="Initialized random number generator",
        )

        # Validate loan generation parameters
        validate_loan_parameters(config)

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=15.0,
            message="Validated loan parameters",
        )

        # Check for cancellation
        if websocket_manager.is_cancelled(context.run_id):
            logger.info("Loan generation cancelled", run_id=context.run_id)
            await websocket_manager.send_info(
                simulation_id=context.run_id,
                message="Loan generation cancelled",
            )
            return

        # Calculate loan counts by zone using the capital allocator
        avg_loan_size = config.avg_loan_size
        loan_counts_by_zone = await calculate_loan_counts(context, avg_loan_size)

        # Calculate total number of loans
        num_loans = sum(loan_counts_by_zone.values())

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=20.0,
            message="Calculated loan counts by zone",
            data={
                "loan_counts_by_zone": loan_counts_by_zone,
                "total_loans": num_loans,
            },
        )

        # Generate loan sizes
        loan_sizes = generate_loan_sizes(
            num_loans=num_loans,
            avg_loan_size=avg_loan_size,
            loan_size_std_dev=config.loan_size_std_dev,
            min_loan_size=config.min_loan_size,
            max_loan_size=config.max_loan_size,
            rng=rng,
        )

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=30.0,
            message="Generated loan sizes",
        )

        # Adjust number of loans to match fund size
        total_loan_size = sum(loan_sizes)
        fund_size = config.fund_size
        original_num_loans = len(loan_sizes)

        if total_loan_size > fund_size:
            # Send warning message
            await websocket_manager.send_warning(
                simulation_id=context.run_id,
                message="Total loan size exceeds fund size, adjusting portfolio",
                data={
                    "total_loan_size": total_loan_size,
                    "fund_size": fund_size,
                    "original_num_loans": original_num_loans,
                },
            )

            # Remove loans until we're under the fund size
            while total_loan_size > fund_size and loan_sizes:
                loan_sizes.pop()
                total_loan_size = sum(loan_sizes)

        num_loans = len(loan_sizes)
        logger.info("Adjusted loan portfolio size", num_loans=num_loans, total_loan_size=total_loan_size)

        # Send info message if loans were removed
        if num_loans < original_num_loans:
            await websocket_manager.send_info(
                simulation_id=context.run_id,
                message="Loan portfolio size adjusted",
                data={
                    "original_num_loans": original_num_loans,
                    "adjusted_num_loans": num_loans,
                    "loans_removed": original_num_loans - num_loans,
                    "total_loan_size": total_loan_size,
                },
            )

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=40.0,
            message="Adjusted loan portfolio size",
            data={
                "num_loans": num_loans,
                "total_loan_size": total_loan_size,
            },
        )

        # Generate LTV ratios
        ltv_ratios = generate_ltv_ratios(
            num_loans=num_loans,
            avg_ltv=config.avg_loan_ltv,
            ltv_std_dev=config.ltv_std_dev,
            min_ltv=config.min_ltv,
            max_ltv=config.max_ltv,
            rng=rng,
        )

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=50.0,
            message="Generated LTV ratios",
        )

        # Check for cancellation
        if websocket_manager.is_cancelled(context.run_id):
            logger.info("Loan generation cancelled", run_id=context.run_id)
            await websocket_manager.send_info(
                simulation_id=context.run_id,
                message="Loan generation cancelled",
            )
            return

        # Assign loans to zones based on loan counts by zone
        zones = assign_loans_to_zones(num_loans, loan_counts_by_zone)

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=60.0,
            message="Assigned loans to zones",
        )

        # Generate loan terms
        loan_terms = generate_loan_terms(
            num_loans=num_loans,
            avg_loan_term=config.avg_loan_term,
            rng=rng,
        )

        # Generate interest rates
        interest_rates = generate_interest_rates(
            num_loans=num_loans,
            avg_interest_rate=config.avg_loan_interest_rate,
            rng=rng,
        )

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=70.0,
            message="Generated loan terms and interest rates",
        )

        # Get property data from TLS module
        property_data_by_zone = {}
        for zone in set(zones):
            properties = await get_properties_for_zone(context, zone, num_loans)
            property_data_by_zone[zone] = properties

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=80.0,
            message="Retrieved property data from TLS module",
        )

        # Create loan objects
        loans = []
        for i in range(num_loans):
            loan_id = str(uuid.uuid4())
            zone = zones[i]

            # Get property data for this loan
            property_data = get_property_for_loan(property_data_by_zone, zone, i)

            loan = {
                "loan_id": loan_id,
                "loan_size": loan_sizes[i],
                "ltv": ltv_ratios[i],
                "zone": zone,
                "term": loan_terms[i],
                "interest_rate": interest_rates[i],
                "origination_year": config.vintage_year,
                "origination_month": 1,  # Default to January for initial loans
                "property_value": loan_sizes[i] / ltv_ratios[i],
                "property_id": property_data.get("property_id", ""),
                "suburb_id": property_data.get("suburb_id", ""),
                "suburb_name": property_data.get("suburb_name", ""),
                "property_type": property_data.get("property_type", ""),
                "bedrooms": property_data.get("bedrooms", 0),
                "bathrooms": property_data.get("bathrooms", 0),
                "land_size": property_data.get("land_size", 0.0),
                "building_size": property_data.get("building_size", 0.0),
                "year_built": property_data.get("year_built", 0),
            }

            loans.append(loan)

            # Update metrics
            increment_counter("loans_generated_total", labels={"zone": zone})

        # Store loans in context
        context.loans = loans

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=90.0,
            message="Created loan objects",
        )

        # Update actual allocation based on generated loans
        await update_actual_allocation(context, year)

        # Generate loan portfolio visualization
        loan_portfolio_visualization = generate_loan_portfolio_visualization(loans)

        # Store loan portfolio visualization in context
        context.loan_portfolio_visualization = loan_portfolio_visualization

        # Calculate loan portfolio statistics
        loan_portfolio_stats = calculate_loan_portfolio_statistics(loans)

        # Store loan portfolio statistics in context
        context.loan_portfolio_stats = loan_portfolio_stats

        # Store intermediate results for visualization
        context.loan_generator_results = {
            "loans": loans,
            "loan_portfolio_visualization": loan_portfolio_visualization,
            "loan_portfolio_stats": loan_portfolio_stats,
        }

        # Track loan portfolio history
        track_loan_portfolio_history(context, year)

        # Log summary
        zone_counts = {zone: zones.count(zone) for zone in set(zones)}
        logger.info(
            "Loan generation completed",
            num_loans=num_loans,
            total_loan_size=total_loan_size,
            zone_counts=zone_counts,
        )

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=100.0,
            message="Loan generation completed",
            data={
                "num_loans": num_loans,
                "total_loan_size": total_loan_size,
                "zone_counts": zone_counts,
                "loan_portfolio_stats": loan_portfolio_stats,
            },
        )

        # Send result message
        await websocket_manager.send_result(
            simulation_id=context.run_id,
            result={
                "module": "loan_generator",
                "num_loans": num_loans,
                "total_loan_size": total_loan_size,
                "zone_counts": zone_counts,
                "loan_portfolio_stats": loan_portfolio_stats,
                "loan_portfolio_visualization": loan_portfolio_visualization,
                "execution_time": time.time() - start_time,
            },
        )

        # Update metrics
        increment_counter("loan_generation_completed_total")
        observe_histogram(
            "loan_generation_runtime_seconds",
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
                "module": "loan_generator",
            },
        )

        # Re-raise exception
        raise


def generate_loan_sizes(
    num_loans: int,
    avg_loan_size: float,
    loan_size_std_dev: float,
    min_loan_size: float,
    max_loan_size: float,
    rng: np.random.Generator,
) -> List[float]:
    """
    Generate loan sizes based on a normal distribution.

    Args:
        num_loans: Number of loans to generate
        avg_loan_size: Average loan size
        loan_size_std_dev: Standard deviation of loan sizes
        min_loan_size: Minimum loan size
        max_loan_size: Maximum loan size
        rng: Random number generator

    Returns:
        List of loan sizes
    """
    # Generate loan sizes from a normal distribution
    loan_sizes = rng.normal(avg_loan_size, loan_size_std_dev, num_loans)

    # Clip to min/max values
    loan_sizes = np.clip(loan_sizes, min_loan_size, max_loan_size)

    return loan_sizes.tolist()


def generate_ltv_ratios(
    num_loans: int,
    avg_ltv: float,
    ltv_std_dev: float,
    min_ltv: float,
    max_ltv: float,
    rng: np.random.Generator,
) -> List[float]:
    """
    Generate LTV ratios based on a normal distribution.

    Args:
        num_loans: Number of loans to generate
        avg_ltv: Average LTV ratio
        ltv_std_dev: Standard deviation of LTV ratios
        min_ltv: Minimum LTV ratio
        max_ltv: Maximum LTV ratio
        rng: Random number generator

    Returns:
        List of LTV ratios
    """
    # Generate LTV ratios from a normal distribution
    ltv_ratios = rng.normal(avg_ltv, ltv_std_dev, num_loans)

    # Clip to min/max values
    ltv_ratios = np.clip(ltv_ratios, min_ltv, max_ltv)

    return ltv_ratios.tolist()


def validate_loan_parameters(config: Any) -> None:
    """
    Validate loan generation parameters.

    Args:
        config: Simulation configuration

    Raises:
        ValidationError: If the loan generation parameters are invalid
    """
    # Check if loan size parameters are valid
    if not hasattr(config, "avg_loan_size") or config.avg_loan_size <= 0:
        raise ValidationError(
            "Average loan size must be positive",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={"avg_loan_size": getattr(config, "avg_loan_size", None)},
        )

    if not hasattr(config, "loan_size_std_dev") or config.loan_size_std_dev < 0:
        raise ValidationError(
            "Loan size standard deviation must be non-negative",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={"loan_size_std_dev": getattr(config, "loan_size_std_dev", None)},
        )

    if not hasattr(config, "min_loan_size") or config.min_loan_size <= 0:
        raise ValidationError(
            "Minimum loan size must be positive",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={"min_loan_size": getattr(config, "min_loan_size", None)},
        )

    if not hasattr(config, "max_loan_size") or config.max_loan_size <= 0:
        raise ValidationError(
            "Maximum loan size must be positive",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={"max_loan_size": getattr(config, "max_loan_size", None)},
        )

    if config.min_loan_size > config.max_loan_size:
        raise ValidationError(
            "Minimum loan size must be less than or equal to maximum loan size",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={
                "min_loan_size": config.min_loan_size,
                "max_loan_size": config.max_loan_size,
            },
        )

    # Check if LTV parameters are valid
    if not hasattr(config, "avg_loan_ltv") or config.avg_loan_ltv <= 0 or config.avg_loan_ltv > 1:
        raise ValidationError(
            "Average LTV ratio must be between 0 and 1",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={"avg_loan_ltv": getattr(config, "avg_loan_ltv", None)},
        )

    if not hasattr(config, "ltv_std_dev") or config.ltv_std_dev < 0:
        raise ValidationError(
            "LTV standard deviation must be non-negative",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={"ltv_std_dev": getattr(config, "ltv_std_dev", None)},
        )

    if not hasattr(config, "min_ltv") or config.min_ltv <= 0 or config.min_ltv > 1:
        raise ValidationError(
            "Minimum LTV ratio must be between 0 and 1",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={"min_ltv": getattr(config, "min_ltv", None)},
        )

    if not hasattr(config, "max_ltv") or config.max_ltv <= 0 or config.max_ltv > 1:
        raise ValidationError(
            "Maximum LTV ratio must be between 0 and 1",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={"max_ltv": getattr(config, "max_ltv", None)},
        )

    if config.min_ltv > config.max_ltv:
        raise ValidationError(
            "Minimum LTV ratio must be less than or equal to maximum LTV ratio",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={
                "min_ltv": config.min_ltv,
                "max_ltv": config.max_ltv,
            },
        )

    # Check if loan term parameters are valid
    if not hasattr(config, "avg_loan_term") or config.avg_loan_term <= 0:
        raise ValidationError(
            "Average loan term must be positive",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={"avg_loan_term": getattr(config, "avg_loan_term", None)},
        )

    # Check if interest rate parameters are valid
    if not hasattr(config, "avg_loan_interest_rate") or config.avg_loan_interest_rate <= 0:
        raise ValidationError(
            "Average loan interest rate must be positive",
            code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            details={"avg_loan_interest_rate": getattr(config, "avg_loan_interest_rate", None)},
        )

    # Check if zone allocations are valid
    if not hasattr(config, "zone_allocations"):
        raise ValidationError(
            "Zone allocations not provided",
            code=ErrorCode.MISSING_PARAMETER,
        )


def assign_loans_to_zones(num_loans: int, loan_counts_by_zone: Dict[str, int]) -> List[str]:
    """
    Assign loans to zones based on loan counts by zone.

    Args:
        num_loans: Total number of loans to assign
        loan_counts_by_zone: Dictionary of loan counts by zone

    Returns:
        List of zone assignments
    """
    # Create list of zone assignments
    zone_assignments = []

    # Assign loans to zones based on loan counts
    for zone, count in loan_counts_by_zone.items():
        zone_assignments.extend([zone] * count)

    # If we have more loans than assignments, assign the rest to the first zone
    if len(zone_assignments) < num_loans:
        first_zone = next(iter(loan_counts_by_zone.keys()))
        zone_assignments.extend([first_zone] * (num_loans - len(zone_assignments)))

    # If we have more assignments than loans, truncate the list
    if len(zone_assignments) > num_loans:
        zone_assignments = zone_assignments[:num_loans]

    return zone_assignments


async def get_properties_for_zone(
    context: SimulationContext, zone: str, limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get properties for a specific zone from the TLS module.

    Args:
        context: Simulation context
        zone: Zone category (green, orange, red)
        limit: Maximum number of properties to return

    Returns:
        List of properties in the zone
    """
    # Get TLS manager
    tls_manager = getattr(context, "tls_manager", None)
    if tls_manager is None:
        # Initialize TLS module
        tls_manager = get_tls_manager(use_mock=True)

        # Load TLS data
        await tls_manager.load_data(simulation_id=context.run_id)

        # Store TLS manager in context
        context.tls_manager = tls_manager

    # Get suburbs in the zone
    suburbs = tls_manager.get_suburbs_by_zone(zone)

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

    return properties


def get_property_for_loan(
    property_data_by_zone: Dict[str, List[Dict[str, Any]]], zone: str, index: int
) -> Dict[str, Any]:
    """
    Get property data for a specific loan.

    Args:
        property_data_by_zone: Dictionary of property data by zone
        zone: Zone category (green, orange, red)
        index: Index of the loan in the zone

    Returns:
        Property data for the loan
    """
    # Get properties for the zone
    properties = property_data_by_zone.get(zone, [])

    # If no properties found, return empty property data
    if not properties:
        return {}

    # Get property data for the loan
    property_index = index % len(properties)
    return properties[property_index]


def assign_zones(
    num_loans: int, zone_allocations: Dict[str, float], rng: np.random.Generator
) -> List[str]:
    """
    Assign loans to zones based on zone allocations.

    Args:
        num_loans: Number of loans to assign
        zone_allocations: Dictionary of zone allocations (zone -> percentage)
        rng: Random number generator

    Returns:
        List of zone assignments
    """
    zones = list(zone_allocations.keys())
    probabilities = list(zone_allocations.values())

    # Normalize probabilities to sum to 1
    total_probability = sum(probabilities)
    if total_probability != 1.0:
        probabilities = [p / total_probability for p in probabilities]

    # Assign zones based on probabilities
    zone_assignments = rng.choice(zones, size=num_loans, p=probabilities)

    return zone_assignments.tolist()


def generate_loan_terms(
    num_loans: int, avg_loan_term: float, rng: np.random.Generator
) -> List[float]:
    """
    Generate loan terms based on a normal distribution.

    Args:
        num_loans: Number of loans to generate
        avg_loan_term: Average loan term in years
        rng: Random number generator

    Returns:
        List of loan terms in years
    """
    # Generate loan terms from a normal distribution
    # Standard deviation is set to 20% of the average term
    std_dev = avg_loan_term * 0.2
    loan_terms = rng.normal(avg_loan_term, std_dev, num_loans)

    # Clip to reasonable values (1-30 years)
    loan_terms = np.clip(loan_terms, 1, 30)

    return loan_terms.tolist()


def generate_interest_rates(
    num_loans: int, avg_interest_rate: float, rng: np.random.Generator
) -> List[float]:
    """
    Generate interest rates based on a normal distribution.

    Args:
        num_loans: Number of loans to generate
        avg_interest_rate: Average interest rate
        rng: Random number generator

    Returns:
        List of interest rates
    """
    # Generate interest rates from a normal distribution
    # Standard deviation is set to 10% of the average rate
    std_dev = avg_interest_rate * 0.1
    interest_rates = rng.normal(avg_interest_rate, std_dev, num_loans)

    # Clip to reasonable values (1-15%)
    interest_rates = np.clip(interest_rates, 0.01, 0.15)

    return interest_rates.tolist()


def generate_loan_portfolio_visualization(loans: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate visualization data for the loan portfolio.

    Args:
        loans: List of loan objects

    Returns:
        Dictionary containing visualization data
    """
    # Count loans by zone
    zone_counts = {}
    for loan in loans:
        zone = loan.get("zone", "unknown")
        zone_counts[zone] = zone_counts.get(zone, 0) + 1

    # Calculate total loan amount by zone
    zone_amounts = {}
    for loan in loans:
        zone = loan.get("zone", "unknown")
        loan_size = loan.get("loan_size", 0.0)
        zone_amounts[zone] = zone_amounts.get(zone, 0.0) + loan_size

    # Generate pie chart data for loan counts by zone
    pie_chart_counts = [
        {"zone": zone, "count": count}
        for zone, count in zone_counts.items()
    ]

    # Generate pie chart data for loan amounts by zone
    pie_chart_amounts = [
        {"zone": zone, "amount": amount}
        for zone, amount in zone_amounts.items()
    ]

    # Generate histogram data for loan sizes
    loan_sizes = [loan.get("loan_size", 0.0) for loan in loans]
    loan_size_bins = np.linspace(min(loan_sizes), max(loan_sizes), 10)
    loan_size_hist, loan_size_edges = np.histogram(loan_sizes, bins=loan_size_bins)
    loan_size_histogram = [
        {"bin": f"{loan_size_edges[i]:.2f}-{loan_size_edges[i+1]:.2f}", "count": int(loan_size_hist[i])}
        for i in range(len(loan_size_hist))
    ]

    # Generate histogram data for LTV ratios
    ltv_ratios = [loan.get("ltv", 0.0) for loan in loans]
    ltv_bins = np.linspace(min(ltv_ratios), max(ltv_ratios), 10)
    ltv_hist, ltv_edges = np.histogram(ltv_ratios, bins=ltv_bins)
    ltv_histogram = [
        {"bin": f"{ltv_edges[i]:.2f}-{ltv_edges[i+1]:.2f}", "count": int(ltv_hist[i])}
        for i in range(len(ltv_hist))
    ]

    # Generate histogram data for loan terms
    loan_terms = [loan.get("term", 0.0) for loan in loans]
    term_bins = np.linspace(min(loan_terms), max(loan_terms), 10)
    term_hist, term_edges = np.histogram(loan_terms, bins=term_bins)
    term_histogram = [
        {"bin": f"{term_edges[i]:.2f}-{term_edges[i+1]:.2f}", "count": int(term_hist[i])}
        for i in range(len(term_hist))
    ]

    # Generate histogram data for interest rates
    interest_rates = [loan.get("interest_rate", 0.0) for loan in loans]
    rate_bins = np.linspace(min(interest_rates), max(interest_rates), 10)
    rate_hist, rate_edges = np.histogram(interest_rates, bins=rate_bins)
    rate_histogram = [
        {"bin": f"{rate_edges[i]:.2f}-{rate_edges[i+1]:.2f}", "count": int(rate_hist[i])}
        for i in range(len(rate_hist))
    ]

    # Generate scatter plot data for loan size vs. LTV
    scatter_size_ltv = [
        {"loan_size": loan.get("loan_size", 0.0), "ltv": loan.get("ltv", 0.0), "zone": loan.get("zone", "unknown")}
        for loan in loans
    ]

    # Generate scatter plot data for loan size vs. term
    scatter_size_term = [
        {"loan_size": loan.get("loan_size", 0.0), "term": loan.get("term", 0.0), "zone": loan.get("zone", "unknown")}
        for loan in loans
    ]

    # Generate table data for loans by zone
    table_by_zone = []
    for zone in zone_counts:
        zone_loans = [loan for loan in loans if loan.get("zone") == zone]
        avg_loan_size = sum(loan.get("loan_size", 0.0) for loan in zone_loans) / len(zone_loans) if zone_loans else 0.0
        avg_ltv = sum(loan.get("ltv", 0.0) for loan in zone_loans) / len(zone_loans) if zone_loans else 0.0
        avg_term = sum(loan.get("term", 0.0) for loan in zone_loans) / len(zone_loans) if zone_loans else 0.0
        avg_rate = sum(loan.get("interest_rate", 0.0) for loan in zone_loans) / len(zone_loans) if zone_loans else 0.0

        table_by_zone.append({
            "zone": zone,
            "count": zone_counts.get(zone, 0),
            "total_amount": zone_amounts.get(zone, 0.0),
            "avg_loan_size": avg_loan_size,
            "avg_ltv": avg_ltv,
            "avg_term": avg_term,
            "avg_interest_rate": avg_rate,
        })

    return {
        "pie_charts": {
            "loan_counts_by_zone": pie_chart_counts,
            "loan_amounts_by_zone": pie_chart_amounts,
        },
        "histograms": {
            "loan_sizes": loan_size_histogram,
            "ltv_ratios": ltv_histogram,
            "loan_terms": term_histogram,
            "interest_rates": rate_histogram,
        },
        "scatter_plots": {
            "loan_size_vs_ltv": scatter_size_ltv,
            "loan_size_vs_term": scatter_size_term,
        },
        "tables": {
            "loans_by_zone": table_by_zone,
        },
    }


def track_loan_portfolio_history(context: SimulationContext, year: float) -> None:
    """
    Track loan portfolio history over time.

    Args:
        context: Simulation context
        year: Current simulation year
    """
    # Initialize loan portfolio history if not exists
    if not hasattr(context, "loan_portfolio_history"):
        context.loan_portfolio_history = []

    # Get current loan portfolio
    loans = context.loans

    # Calculate portfolio summary
    num_loans = len(loans)
    total_loan_amount = sum(loan.get("loan_size", 0.0) for loan in loans)
    avg_loan_size = total_loan_amount / num_loans if num_loans > 0 else 0.0
    avg_ltv = sum(loan.get("ltv", 0.0) for loan in loans) / num_loans if num_loans > 0 else 0.0

    # Count loans by zone
    zone_counts = {}
    for loan in loans:
        zone = loan.get("zone", "unknown")
        zone_counts[zone] = zone_counts.get(zone, 0) + 1

    # Calculate total loan amount by zone
    zone_amounts = {}
    for loan in loans:
        zone = loan.get("zone", "unknown")
        loan_size = loan.get("loan_size", 0.0)
        zone_amounts[zone] = zone_amounts.get(zone, 0.0) + loan_size

    # Calculate zone percentages
    zone_percentages = {}
    for zone, count in zone_counts.items():
        zone_percentages[zone] = count / num_loans if num_loans > 0 else 0.0

    # Calculate zone amount percentages
    zone_amount_percentages = {}
    for zone, amount in zone_amounts.items():
        zone_amount_percentages[zone] = amount / total_loan_amount if total_loan_amount > 0 else 0.0

    # Create portfolio snapshot
    portfolio_snapshot = {
        "year": year,
        "num_loans": num_loans,
        "total_loan_amount": total_loan_amount,
        "avg_loan_size": avg_loan_size,
        "avg_ltv": avg_ltv,
        "zone_counts": zone_counts,
        "zone_amounts": zone_amounts,
        "zone_percentages": zone_percentages,
        "zone_amount_percentages": zone_amount_percentages,
        "timestamp": time.time(),
    }

    # Add to history
    context.loan_portfolio_history.append(portfolio_snapshot)

    # Generate loan portfolio history visualization
    if len(context.loan_portfolio_history) > 1:
        context.loan_portfolio_history_visualization = generate_loan_portfolio_history_visualization(
            context.loan_portfolio_history
        )


def generate_loan_portfolio_history_visualization(portfolio_history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate visualization data for loan portfolio history.

    Args:
        portfolio_history: List of portfolio history entries

    Returns:
        Dictionary containing visualization data
    """
    # Extract data for visualization
    years = [entry["year"] for entry in portfolio_history]
    zones = set()
    for entry in portfolio_history:
        zones.update(entry["zone_counts"].keys())

    # Generate loan count history
    loan_count_history = []
    for entry in portfolio_history:
        loan_count_history.append({
            "year": entry["year"],
            "count": entry["num_loans"],
        })

    # Generate loan amount history
    loan_amount_history = []
    for entry in portfolio_history:
        loan_amount_history.append({
            "year": entry["year"],
            "amount": entry["total_loan_amount"],
        })

    # Generate zone count history
    zone_count_history = {zone: [] for zone in zones}
    for entry in portfolio_history:
        for zone in zones:
            zone_count_history[zone].append({
                "year": entry["year"],
                "count": entry["zone_counts"].get(zone, 0),
            })

    # Generate zone amount history
    zone_amount_history = {zone: [] for zone in zones}
    for entry in portfolio_history:
        for zone in zones:
            zone_amount_history[zone].append({
                "year": entry["year"],
                "amount": entry["zone_amounts"].get(zone, 0.0),
            })

    # Generate zone percentage history
    zone_percentage_history = {zone: [] for zone in zones}
    for entry in portfolio_history:
        for zone in zones:
            zone_percentage_history[zone].append({
                "year": entry["year"],
                "percentage": entry["zone_percentages"].get(zone, 0.0) * 100,
            })

    # Generate portfolio turnover visualization
    turnover_data = []
    for i in range(1, len(portfolio_history)):
        prev_entry = portfolio_history[i-1]
        curr_entry = portfolio_history[i]

        # Calculate new loans
        new_loans = max(0, curr_entry["num_loans"] - prev_entry["num_loans"])

        # Calculate turnover percentage
        turnover_percentage = new_loans / prev_entry["num_loans"] if prev_entry["num_loans"] > 0 else 0.0

        turnover_data.append({
            "year": curr_entry["year"],
            "new_loans": new_loans,
            "turnover_percentage": turnover_percentage * 100,
        })

    # Generate table data
    table_data = []
    for entry in portfolio_history:
        row = {
            "year": entry["year"],
            "num_loans": entry["num_loans"],
            "total_loan_amount": f"${entry['total_loan_amount']:,.2f}",
            "avg_loan_size": f"${entry['avg_loan_size']:,.2f}",
            "avg_ltv": f"{entry['avg_ltv'] * 100:.2f}%",
        }
        for zone in zones:
            row[f"{zone}_count"] = entry["zone_counts"].get(zone, 0)
            row[f"{zone}_amount"] = f"${entry['zone_amounts'].get(zone, 0.0):,.2f}"
            row[f"{zone}_percentage"] = f"{entry['zone_percentages'].get(zone, 0.0) * 100:.2f}%"
        table_data.append(row)

    return {
        "loan_count_history": loan_count_history,
        "loan_amount_history": loan_amount_history,
        "zone_count_history": zone_count_history,
        "zone_amount_history": zone_amount_history,
        "zone_percentage_history": zone_percentage_history,
        "turnover_data": turnover_data,
        "table": table_data,
    }


async def get_loan_portfolio_summary(context: SimulationContext) -> Dict[str, Any]:
    """
    Get a summary of the loan portfolio.

    Args:
        context: Simulation context

    Returns:
        Dictionary containing loan portfolio summary
    """
    start_time = time.time()
    logger.info("Getting loan portfolio summary")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=0.0,
            message="Generating loan portfolio summary",
        )

        # Get loans
        loans = getattr(context, "loans", [])

        # Get loan portfolio statistics
        loan_portfolio_stats = getattr(context, "loan_portfolio_stats", {})

        # Get loan portfolio visualization
        loan_portfolio_visualization = getattr(context, "loan_portfolio_visualization", {})

        # Get loan portfolio history
        loan_portfolio_history = getattr(context, "loan_portfolio_history", [])
        loan_portfolio_history_visualization = getattr(context, "loan_portfolio_history_visualization", {})

        # Generate summary
        summary = {
            "num_loans": len(loans),
            "loan_portfolio_stats": loan_portfolio_stats,
            "loan_portfolio_visualization": loan_portfolio_visualization,
            "loan_portfolio_history": loan_portfolio_history,
            "loan_portfolio_history_visualization": loan_portfolio_history_visualization,
        }

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="loan_generator",
            progress=100.0,
            message="Loan portfolio summary generated",
            data=summary,
        )

        # Update metrics
        increment_counter("loan_portfolio_summary_generated_total")
        observe_histogram(
            "loan_portfolio_summary_generation_runtime_seconds",
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
                "module": "loan_generator",
            },
        )

        # Re-raise exception
        raise


def calculate_loan_portfolio_statistics(loans: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate statistics for the loan portfolio.

    Args:
        loans: List of loan objects

    Returns:
        Dictionary containing loan portfolio statistics
    """
    # Calculate overall statistics
    num_loans = len(loans)
    total_loan_amount = sum(loan.get("loan_size", 0.0) for loan in loans)
    avg_loan_size = total_loan_amount / num_loans if num_loans > 0 else 0.0
    avg_ltv = sum(loan.get("ltv", 0.0) for loan in loans) / num_loans if num_loans > 0 else 0.0
    avg_term = sum(loan.get("term", 0.0) for loan in loans) / num_loans if num_loans > 0 else 0.0
    avg_interest_rate = sum(loan.get("interest_rate", 0.0) for loan in loans) / num_loans if num_loans > 0 else 0.0

    # Calculate statistics by zone
    zone_stats = {}
    for loan in loans:
        zone = loan.get("zone", "unknown")
        if zone not in zone_stats:
            zone_stats[zone] = {
                "count": 0,
                "total_amount": 0.0,
                "loan_sizes": [],
                "ltv_ratios": [],
                "loan_terms": [],
                "interest_rates": [],
            }

        zone_stats[zone]["count"] += 1
        zone_stats[zone]["total_amount"] += loan.get("loan_size", 0.0)
        zone_stats[zone]["loan_sizes"].append(loan.get("loan_size", 0.0))
        zone_stats[zone]["ltv_ratios"].append(loan.get("ltv", 0.0))
        zone_stats[zone]["loan_terms"].append(loan.get("term", 0.0))
        zone_stats[zone]["interest_rates"].append(loan.get("interest_rate", 0.0))

    # Calculate summary statistics by zone
    zone_summary = {}
    for zone, stats in zone_stats.items():
        count = stats["count"]
        loan_sizes = stats["loan_sizes"]
        ltv_ratios = stats["ltv_ratios"]
        loan_terms = stats["loan_terms"]
        interest_rates = stats["interest_rates"]

        zone_summary[zone] = {
            "count": count,
            "total_amount": stats["total_amount"],
            "percentage_of_loans": count / num_loans if num_loans > 0 else 0.0,
            "percentage_of_amount": stats["total_amount"] / total_loan_amount if total_loan_amount > 0 else 0.0,
            "avg_loan_size": sum(loan_sizes) / count if count > 0 else 0.0,
            "min_loan_size": min(loan_sizes) if loan_sizes else 0.0,
            "max_loan_size": max(loan_sizes) if loan_sizes else 0.0,
            "std_dev_loan_size": np.std(loan_sizes) if loan_sizes else 0.0,
            "avg_ltv": sum(ltv_ratios) / count if count > 0 else 0.0,
            "min_ltv": min(ltv_ratios) if ltv_ratios else 0.0,
            "max_ltv": max(ltv_ratios) if ltv_ratios else 0.0,
            "std_dev_ltv": np.std(ltv_ratios) if ltv_ratios else 0.0,
            "avg_term": sum(loan_terms) / count if count > 0 else 0.0,
            "min_term": min(loan_terms) if loan_terms else 0.0,
            "max_term": max(loan_terms) if loan_terms else 0.0,
            "std_dev_term": np.std(loan_terms) if loan_terms else 0.0,
            "avg_interest_rate": sum(interest_rates) / count if count > 0 else 0.0,
            "min_interest_rate": min(interest_rates) if interest_rates else 0.0,
            "max_interest_rate": max(interest_rates) if interest_rates else 0.0,
            "std_dev_interest_rate": np.std(interest_rates) if interest_rates else 0.0,
        }

    # Calculate property statistics
    property_types = {}
    bedroom_counts = {}
    bathroom_counts = {}

    for loan in loans:
        property_type = loan.get("property_type", "unknown")
        bedrooms = loan.get("bedrooms", 0)
        bathrooms = loan.get("bathrooms", 0)

        property_types[property_type] = property_types.get(property_type, 0) + 1
        bedroom_counts[bedrooms] = bedroom_counts.get(bedrooms, 0) + 1
        bathroom_counts[bathrooms] = bathroom_counts.get(bathrooms, 0) + 1

    return {
        "overall": {
            "num_loans": num_loans,
            "total_loan_amount": total_loan_amount,
            "avg_loan_size": avg_loan_size,
            "avg_ltv": avg_ltv,
            "avg_term": avg_term,
            "avg_interest_rate": avg_interest_rate,
        },
        "by_zone": zone_summary,
        "property_stats": {
            "property_types": property_types,
            "bedroom_counts": bedroom_counts,
            "bathroom_counts": bathroom_counts,
        },
    }
