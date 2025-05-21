"""
Enhanced exit simulator module for the EQU IHOME SIM ENGINE v2.

This module provides advanced exit simulation with enhanced metrics, visualizations,
behavioral models, economic integration, and machine learning capabilities.
"""

import time
from typing import Dict, Any, List, Optional, Tuple, Union, Callable
from enum import Enum
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import structlog
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

from src.engine.simulation_context import SimulationContext
from src.monte_carlo.rng_factory import get_rng
from src.api.websocket_manager import get_websocket_manager
from src.utils.error_handler import handle_exception, log_error
from src.utils.metrics import increment_counter, observe_histogram, set_gauge
from src.tls_module.tls_core import MetricCategory
from src.tls_module import get_tls_manager
from src.price_path.enhanced_price_path import calculate_enhanced_property_value
from src.exit_simulator.exit_simulator import (
    ExitType,
    simulate_exits,
    simulate_loan_exit,
    determine_exit_type,
    calculate_exit_value,
    calculate_exit_statistics,
    generate_exit_visualization,
    get_exit_summary,
)

logger = structlog.get_logger(__name__)


# Enhanced default parameters
ENHANCED_DEFAULT_PARAMS = {
    # Behavioral model parameters
    "refinance_interest_rate_sensitivity": 2.0,  # How sensitive refinancing is to interest rate changes
    "sale_appreciation_sensitivity": 1.5,  # How sensitive sales are to appreciation
    "life_event_probability": 0.05,  # Annual probability of life events triggering exits
    "behavioral_correlation": 0.3,  # Correlation in exit decisions (herd behavior)

    # Economic model parameters
    "recession_default_multiplier": 2.5,  # How much recessions increase defaults
    "inflation_refinance_multiplier": 1.8,  # How inflation affects refinancing
    "employment_sensitivity": 1.2,  # How employment affects exits
    "migration_sensitivity": 0.8,  # How population migration affects exits

    # Regulatory and tax parameters
    "regulatory_compliance_cost": 0.01,  # Compliance cost as percentage of loan
    "tax_efficiency_factor": 0.9,  # Tax efficiency factor (1.0 = fully efficient)

    # Cohort analysis parameters
    "vintage_segmentation": True,  # Whether to segment by vintage
    "ltv_segmentation": True,  # Whether to segment by LTV
    "zone_segmentation": True,  # Whether to segment by zone

    # Risk metrics parameters
    "var_confidence_level": 0.95,  # Confidence level for Value-at-Risk
    "stress_test_severity": 0.3,  # Severity of stress tests (0-1)
    "tail_risk_threshold": 0.05,  # Threshold for tail risk events

    # Machine learning parameters
    "use_ml_models": True,  # Whether to use machine learning models
    "feature_importance_threshold": 0.05,  # Threshold for important features
    "anomaly_detection_threshold": 3.0,  # Standard deviations for anomaly detection
}


async def simulate_enhanced_exits(context: SimulationContext) -> None:
    """
    Simulate enhanced exits for all loans in the portfolio.

    This function extends the base exit simulator with advanced features including
    behavioral models, economic integration, cohort analysis, and machine learning.

    Args:
        context: Simulation context

    Raises:
        ValueError: If the configuration parameters are invalid
    """
    start_time = time.time()
    logger.info("Simulating enhanced exits")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="enhanced_exit_simulator",
            progress=0.0,
            message="Starting enhanced exit simulation",
        )

        # First, run the base exit simulation
        await simulate_exits(context)

        # Get the base exits
        base_exits = getattr(context, "exits", [])

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="enhanced_exit_simulator",
            progress=30.0,
            message="Base exit simulation completed, enhancing with advanced models",
        )

        # Get configuration parameters
        config = context.config

        # Get enhanced exit simulator configuration
        enhanced_exit_config = getattr(config, "enhanced_exit_simulator", {})

        # Merge with default parameters
        for param, default_value in ENHANCED_DEFAULT_PARAMS.items():
            if not hasattr(enhanced_exit_config, param):
                setattr(enhanced_exit_config, param, default_value)

        # Apply behavioral models to adjust exits
        enhanced_exits = apply_behavioral_models(
            exits=base_exits,
            context=context,
            config=enhanced_exit_config,
        )

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="enhanced_exit_simulator",
            progress=50.0,
            message="Applied behavioral models",
        )

        # Apply economic models to further adjust exits
        enhanced_exits = apply_economic_models(
            exits=enhanced_exits,
            context=context,
            config=enhanced_exit_config,
        )

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="enhanced_exit_simulator",
            progress=70.0,
            message="Applied economic models",
        )

        # Apply machine learning models if enabled
        if enhanced_exit_config.use_ml_models:
            enhanced_exits = apply_ml_models(
                exits=enhanced_exits,
                context=context,
                config=enhanced_exit_config,
            )

            # Report progress
            await websocket_manager.send_progress(
                simulation_id=context.run_id,
                module="enhanced_exit_simulator",
                progress=80.0,
                message="Applied machine learning models",
            )

        # Store enhanced exits in context
        context.enhanced_exits = enhanced_exits

        # Calculate enhanced exit statistics
        enhanced_exit_stats = calculate_enhanced_exit_statistics(
            exits=enhanced_exits,
            base_exits=base_exits,
            context=context,
            config=enhanced_exit_config,
        )

        # Store enhanced exit statistics in context
        context.enhanced_exit_stats = enhanced_exit_stats

        # Generate enhanced exit visualization
        enhanced_exit_visualization = generate_enhanced_exit_visualization(
            exits=enhanced_exits,
            exit_stats=enhanced_exit_stats,
            context=context,
            config=enhanced_exit_config,
        )

        # Store enhanced exit visualization in context
        context.enhanced_exit_visualization = enhanced_exit_visualization

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="enhanced_exit_simulator",
            progress=100.0,
            message="Enhanced exit simulation completed",
            data={
                "num_exits": len(enhanced_exits),
                "avg_exit_year": enhanced_exit_stats["avg_exit_year"],
                "avg_roi": enhanced_exit_stats["avg_roi"],
                "exit_type_distribution": enhanced_exit_stats["exit_type_distribution"],
                "risk_metrics": enhanced_exit_stats["risk_metrics"],
                "cohort_analysis": enhanced_exit_stats["cohort_analysis_summary"],
            },
        )

        # Update metrics
        increment_counter("enhanced_exit_simulations_completed_total")
        observe_histogram(
            "enhanced_exit_simulation_runtime_seconds",
            time.time() - start_time,
        )

        # Log completion
        logger.info(
            "Enhanced exit simulation completed",
            num_exits=len(enhanced_exits),
            avg_exit_year=enhanced_exit_stats["avg_exit_year"],
            avg_roi=enhanced_exit_stats["avg_roi"],
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
                "module": "enhanced_exit_simulator",
            },
        )

        # Update metrics
        increment_counter("enhanced_exit_simulations_failed_total")

        # Re-raise exception
        raise


def apply_behavioral_models(
    exits: List[Dict[str, Any]],
    context: SimulationContext,
    config: Any,
) -> List[Dict[str, Any]]:
    """
    Apply behavioral models to adjust exits.

    This function applies behavioral models to adjust exit timing and types
    based on borrower behavior, market sentiment, and other behavioral factors.

    Args:
        exits: List of exits
        context: Simulation context
        config: Enhanced exit simulator configuration

    Returns:
        Adjusted list of exits
    """
    logger.info("Applying behavioral models to exits")

    # Get random number generator
    rng = context.rng or get_rng("enhanced_exit_simulator", 0)

    # Get parameters
    refinance_interest_rate_sensitivity = getattr(config, "refinance_interest_rate_sensitivity", 2.0)
    sale_appreciation_sensitivity = getattr(config, "sale_appreciation_sensitivity", 1.5)
    life_event_probability = getattr(config, "life_event_probability", 0.05)
    behavioral_correlation = getattr(config, "behavioral_correlation", 0.3)

    # Get price paths
    price_paths = getattr(context, "price_paths", {})

    # Get loans
    loans = context.loans

    # Create a mapping of loan_id to loan
    loan_map = {loan.get("loan_id", ""): loan for loan in loans}

    # Create a copy of exits to modify
    adjusted_exits = []

    # Generate correlated random variables for herd behavior
    num_exits = len(exits)
    base_random = rng.normal(0, 1, size=num_exits)

    # Track exit adjustments for analysis
    exit_adjustments = {
        "interest_rate_effect": [],
        "appreciation_effect": [],
        "life_event_effect": [],
        "herd_effect": [],
        "total_effect": [],
    }

    # Process each exit
    for i, exit_data in enumerate(exits):
        # Get loan details
        loan_id = exit_data.get("loan_id", "")
        loan = loan_map.get(loan_id, {})

        # Get exit details
        exit_month = exit_data.get("exit_month", 0)
        exit_type = exit_data.get("exit_type", "")
        exit_year = exit_data.get("exit_year", 0.0)

        # Initialize adjustment factors
        interest_rate_effect = 0.0
        appreciation_effect = 0.0
        life_event_effect = 0.0
        herd_effect = 0.0

        # Apply interest rate sensitivity for refinancing
        if exit_type == "refinance":
            # Simulate interest rate changes over time
            # For simplicity, we'll use a random walk
            interest_rate_change = rng.normal(0, 0.005) * exit_month / 12.0

            # Calculate effect on exit timing
            interest_rate_effect = -interest_rate_change * refinance_interest_rate_sensitivity * 12.0

            # More likely to refinance if rates decrease
            if interest_rate_change < 0:
                interest_rate_effect *= 2.0

        # Apply appreciation sensitivity for sales
        if exit_type == "sale":
            # Get property details
            property_id = exit_data.get("property_id", "")
            property_value = exit_data.get("property_value", 0.0)
            zone = exit_data.get("zone", "green")
            suburb_id = exit_data.get("suburb_id", "")

            # Calculate appreciation at exit
            current_value = calculate_enhanced_property_value(
                initial_value=property_value,
                price_paths=price_paths,
                zone=zone,
                suburb_id=suburb_id,
                property_id=property_id,
                month=exit_month,
            )

            appreciation = (current_value / property_value) - 1.0

            # Calculate effect on exit timing
            # Higher appreciation leads to earlier sales
            appreciation_effect = -appreciation * sale_appreciation_sensitivity * 12.0

        # Apply life event probability
        # Life events can cause exits regardless of economic factors
        life_event_months = []
        annual_prob = life_event_probability
        max_months = int(exit_year * 12)

        # Generate potential life event months
        for month in range(max_months):
            if rng.random() < annual_prob / 12.0:
                life_event_months.append(month)

        # If there are life events before the current exit month,
        # adjust the exit month to the earliest life event
        if life_event_months and min(life_event_months) < exit_month:
            life_event_effect = min(life_event_months) - exit_month

        # Apply herd behavior (correlated exits)
        # Use the correlated random variable
        herd_effect = behavioral_correlation * base_random[i] * 12.0

        # Calculate total adjustment to exit month
        total_adjustment = int(interest_rate_effect + appreciation_effect + life_event_effect + herd_effect)

        # Ensure exit month doesn't go below minimum hold period
        min_hold_period_months = int(getattr(config, "min_hold_period", 1.0) * 12)
        adjusted_exit_month = max(min_hold_period_months, exit_month + total_adjustment)

        # Recalculate exit year
        adjusted_exit_year = adjusted_exit_month / 12.0

        # Store adjustment factors for analysis
        exit_adjustments["interest_rate_effect"].append(interest_rate_effect)
        exit_adjustments["appreciation_effect"].append(appreciation_effect)
        exit_adjustments["life_event_effect"].append(life_event_effect)
        exit_adjustments["herd_effect"].append(herd_effect)
        exit_adjustments["total_effect"].append(total_adjustment)

        # Create adjusted exit data
        adjusted_exit = exit_data.copy()
        adjusted_exit["exit_month"] = adjusted_exit_month
        adjusted_exit["exit_year"] = adjusted_exit_year
        adjusted_exit["behavioral_adjustments"] = {
            "interest_rate_effect": interest_rate_effect,
            "appreciation_effect": appreciation_effect,
            "life_event_effect": life_event_effect,
            "herd_effect": herd_effect,
            "total_adjustment": total_adjustment,
        }

        # Recalculate exit value and appreciation share
        # This is necessary because the exit month has changed
        if total_adjustment != 0:
            # Get property details
            property_id = exit_data.get("property_id", "")
            property_value = exit_data.get("property_value", 0.0)
            zone = exit_data.get("zone", "green")
            suburb_id = exit_data.get("suburb_id", "")

            # Create loan dictionary for exit value calculation
            loan_dict = {
                "loan_id": loan_id,
                "property_id": property_id,
                "suburb_id": suburb_id,
                "zone": zone,
                "loan_amount": exit_data.get("loan_amount", 0.0),
                "property_value": property_value,
            }

            # Convert exit type string to enum
            exit_type_enum = ExitType(exit_type)

            # Calculate exit value
            exit_value, appreciation_share_amount = calculate_exit_value(
                loan=loan_dict,
                exit_month=adjusted_exit_month,
                exit_type=exit_type_enum,
                price_paths=price_paths,
                appreciation_share=0.2,  # Default value
                min_appreciation_share=0.1,  # Default value
                max_appreciation_share=0.5,  # Default value
                tiered_appreciation_thresholds=[0.2, 0.5, 1.0],  # Default values
                tiered_appreciation_shares=[0.1, 0.2, 0.3, 0.4],  # Default values
                recovery_rate=0.8,  # Default value
                foreclosure_cost=0.1,  # Default value
            )

            # Update exit value and appreciation share
            adjusted_exit["exit_value"] = exit_value
            adjusted_exit["appreciation_share_amount"] = appreciation_share_amount
            adjusted_exit["total_return"] = exit_value + appreciation_share_amount

            # Recalculate ROI
            loan_amount = exit_data.get("loan_amount", 0.0)
            adjusted_exit["roi"] = (exit_value + appreciation_share_amount - loan_amount) / loan_amount if loan_amount > 0 else 0.0

            # Recalculate annualized ROI
            adjusted_exit["annualized_roi"] = ((exit_value + appreciation_share_amount) / loan_amount) ** (1 / adjusted_exit_year) - 1 if adjusted_exit_year > 0 else 0.0

        # Add to adjusted exits
        adjusted_exits.append(adjusted_exit)

    # Store exit adjustments in context for analysis
    context.behavioral_exit_adjustments = exit_adjustments

    # Log summary of adjustments
    logger.info(
        "Behavioral model adjustments",
        avg_interest_rate_effect=np.mean(exit_adjustments["interest_rate_effect"]),
        avg_appreciation_effect=np.mean(exit_adjustments["appreciation_effect"]),
        avg_life_event_effect=np.mean(exit_adjustments["life_event_effect"]),
        avg_herd_effect=np.mean(exit_adjustments["herd_effect"]),
        avg_total_effect=np.mean(exit_adjustments["total_effect"]),
    )

    return adjusted_exits


def apply_economic_models(
    exits: List[Dict[str, Any]],
    context: SimulationContext,
    config: Any,
) -> List[Dict[str, Any]]:
    """
    Apply economic models to adjust exits.

    This function applies economic models to adjust exit timing and types
    based on macroeconomic factors, local economic conditions, and regulatory changes.

    Args:
        exits: List of exits
        context: Simulation context
        config: Enhanced exit simulator configuration

    Returns:
        Adjusted list of exits
    """
    logger.info("Applying economic models to exits")

    # Get random number generator
    rng = context.rng or get_rng("enhanced_exit_simulator", 0)

    # Get parameters
    recession_default_multiplier = getattr(config, "recession_default_multiplier", 2.5)
    inflation_refinance_multiplier = getattr(config, "inflation_refinance_multiplier", 1.8)
    employment_sensitivity = getattr(config, "employment_sensitivity", 1.2)
    migration_sensitivity = getattr(config, "migration_sensitivity", 0.8)
    regulatory_compliance_cost = getattr(config, "regulatory_compliance_cost", 0.01)
    tax_efficiency_factor = getattr(config, "tax_efficiency_factor", 0.9)

    # Get price paths
    price_paths = getattr(context, "price_paths", {})

    # Get TLS manager
    tls_manager = get_tls_manager()

    # Create a copy of exits to modify
    adjusted_exits = []

    # Generate economic scenario
    # For simplicity, we'll use a simple economic cycle model
    fund_term = getattr(context.config, "fund_term", 10)
    num_months = fund_term * 12

    # Generate economic indicators
    # GDP growth (annual rate, varies between -3% and 5%)
    gdp_growth = np.zeros(num_months)
    # Start with a random value between 1% and 3%
    gdp_growth[0] = rng.uniform(0.01, 0.03)
    # Use an AR(1) process to generate the rest
    for i in range(1, num_months):
        gdp_growth[i] = 0.8 * gdp_growth[i-1] + 0.2 * rng.normal(0.02, 0.01)

    # Identify recession periods (GDP growth < 0)
    recession_periods = gdp_growth < 0

    # Inflation rate (annual rate, varies between 0% and 8%)
    inflation_rate = np.zeros(num_months)
    # Start with a random value between 1% and 3%
    inflation_rate[0] = rng.uniform(0.01, 0.03)
    # Use an AR(1) process to generate the rest
    for i in range(1, num_months):
        inflation_rate[i] = 0.7 * inflation_rate[i-1] + 0.3 * rng.normal(0.02, 0.015)
        # Ensure inflation is non-negative
        inflation_rate[i] = max(0, inflation_rate[i])

    # Employment growth (annual rate, varies between -2% and 3%)
    employment_growth = np.zeros(num_months)
    # Start with a random value between 0.5% and 1.5%
    employment_growth[0] = rng.uniform(0.005, 0.015)
    # Use an AR(1) process to generate the rest, correlated with GDP
    for i in range(1, num_months):
        employment_growth[i] = 0.6 * employment_growth[i-1] + 0.3 * gdp_growth[i] + 0.1 * rng.normal(0, 0.005)

    # Migration rate (annual rate, varies between -1% and 2%)
    migration_rate = np.zeros(num_months)
    # Start with a random value between 0.2% and 0.8%
    migration_rate[0] = rng.uniform(0.002, 0.008)
    # Use an AR(1) process to generate the rest, correlated with employment
    for i in range(1, num_months):
        migration_rate[i] = 0.5 * migration_rate[i-1] + 0.4 * employment_growth[i] + 0.1 * rng.normal(0, 0.003)

    # Regulatory changes (binary events)
    regulatory_changes = np.zeros(num_months, dtype=bool)
    # Randomly place regulatory changes with 5% annual probability
    for i in range(num_months):
        if rng.random() < 0.05 / 12.0:
            regulatory_changes[i] = True

    # Store economic scenario in context for visualization
    context.economic_scenario = {
        "gdp_growth": gdp_growth.tolist(),
        "recession_periods": recession_periods.tolist(),
        "inflation_rate": inflation_rate.tolist(),
        "employment_growth": employment_growth.tolist(),
        "migration_rate": migration_rate.tolist(),
        "regulatory_changes": regulatory_changes.tolist(),
    }

    # Track exit adjustments for analysis
    exit_adjustments = {
        "recession_effect": [],
        "inflation_effect": [],
        "employment_effect": [],
        "migration_effect": [],
        "regulatory_effect": [],
        "tax_effect": [],
        "total_effect": [],
    }

    # Process each exit
    for exit_data in exits:
        # Get exit details
        exit_month = exit_data.get("exit_month", 0)
        exit_type = exit_data.get("exit_type", "")
        exit_year = exit_data.get("exit_year", 0.0)

        # Ensure exit_month is within bounds
        exit_month = min(exit_month, num_months - 1)

        # Initialize adjustment factors
        recession_effect = 0.0
        inflation_effect = 0.0
        employment_effect = 0.0
        migration_effect = 0.0
        regulatory_effect = 0.0
        tax_effect = 0.0

        # Apply recession effect
        # Recessions increase defaults and delay sales
        if exit_month > 0 and recession_periods[exit_month]:
            if exit_type == "default":
                # Increase probability of default during recessions
                # This is handled by potentially changing the exit type
                recession_effect = 0.0
            elif exit_type == "sale":
                # Delay sales during recessions
                recession_effect = rng.uniform(1, 3) * 12.0
            elif exit_type == "refinance":
                # Delay refinancing during recessions
                recession_effect = rng.uniform(1, 2) * 12.0

        # Apply inflation effect
        # High inflation can accelerate refinancing
        if exit_type == "refinance":
            # Calculate average inflation over the past year
            start_month = max(0, exit_month - 12)
            avg_inflation = np.mean(inflation_rate[start_month:exit_month+1])

            # Higher inflation leads to earlier refinancing
            if avg_inflation > 0.04:  # 4% threshold
                inflation_effect = -avg_inflation * inflation_refinance_multiplier * 12.0

        # Apply employment effect
        # Employment growth affects all exit types
        if exit_month > 0:
            # Calculate average employment growth over the past year
            start_month = max(0, exit_month - 12)
            avg_employment_growth = np.mean(employment_growth[start_month:exit_month+1])

            # Higher employment growth leads to earlier sales and refinancing, fewer defaults
            if exit_type == "sale" or exit_type == "refinance":
                employment_effect = -avg_employment_growth * employment_sensitivity * 12.0
            elif exit_type == "default":
                # Higher employment growth delays defaults
                employment_effect = avg_employment_growth * employment_sensitivity * 24.0

        # Apply migration effect
        # Migration affects property values and exit timing
        if exit_month > 0:
            # Get property details
            suburb_id = exit_data.get("suburb_id", "")

            # Get suburb data
            suburb = tls_manager.suburbs.get(suburb_id)

            if suburb:
                # Calculate average migration rate over the past year
                start_month = max(0, exit_month - 12)
                avg_migration_rate = np.mean(migration_rate[start_month:exit_month+1])

                # Adjust based on suburb desirability
                suburb_factor = suburb.overall_score / 50.0 - 1.0  # -1 to 1 scale

                # Positive migration to desirable suburbs accelerates sales
                if exit_type == "sale" and avg_migration_rate > 0 and suburb_factor > 0:
                    migration_effect = -avg_migration_rate * suburb_factor * migration_sensitivity * 12.0
                # Negative migration from less desirable suburbs delays sales
                elif exit_type == "sale" and avg_migration_rate < 0 and suburb_factor < 0:
                    migration_effect = -avg_migration_rate * suburb_factor * migration_sensitivity * 12.0

        # Apply regulatory effect
        # Regulatory changes can affect exit timing
        if exit_month > 0:
            # Check for regulatory changes in the past year
            start_month = max(0, exit_month - 12)
            recent_regulatory_changes = np.any(regulatory_changes[start_month:exit_month+1])

            if recent_regulatory_changes:
                # Regulatory changes can delay exits due to compliance requirements
                regulatory_effect = rng.uniform(1, 3) * 6.0

        # Apply tax effect
        # Tax considerations can affect exit timing
        # For simplicity, we'll assume tax considerations tend to push exits toward tax year boundaries
        month_in_year = exit_month % 12
        if month_in_year > 0 and month_in_year < 3:
            # Early in tax year, might delay to next tax year
            tax_effect = rng.uniform(0, 1) * (1 - tax_efficiency_factor) * 6.0
        elif month_in_year > 9:
            # Late in tax year, might accelerate to current tax year
            tax_effect = -rng.uniform(0, 1) * (1 - tax_efficiency_factor) * 6.0

        # Calculate total adjustment to exit month
        total_adjustment = int(recession_effect + inflation_effect + employment_effect +
                              migration_effect + regulatory_effect + tax_effect)

        # Ensure exit month doesn't go below minimum hold period
        min_hold_period_months = int(getattr(config, "min_hold_period", 1.0) * 12)
        adjusted_exit_month = max(min_hold_period_months, exit_month + total_adjustment)

        # Recalculate exit year
        adjusted_exit_year = adjusted_exit_month / 12.0

        # Store adjustment factors for analysis
        exit_adjustments["recession_effect"].append(recession_effect)
        exit_adjustments["inflation_effect"].append(inflation_effect)
        exit_adjustments["employment_effect"].append(employment_effect)
        exit_adjustments["migration_effect"].append(migration_effect)
        exit_adjustments["regulatory_effect"].append(regulatory_effect)
        exit_adjustments["tax_effect"].append(tax_effect)
        exit_adjustments["total_effect"].append(total_adjustment)

        # Create adjusted exit data
        adjusted_exit = exit_data.copy()
        adjusted_exit["exit_month"] = adjusted_exit_month
        adjusted_exit["exit_year"] = adjusted_exit_year

        # Add economic adjustments to existing behavioral adjustments
        if "behavioral_adjustments" in adjusted_exit:
            adjusted_exit["behavioral_adjustments"].update({
                "recession_effect": recession_effect,
                "inflation_effect": inflation_effect,
                "employment_effect": employment_effect,
                "migration_effect": migration_effect,
                "regulatory_effect": regulatory_effect,
                "tax_effect": tax_effect,
                "economic_total_adjustment": total_adjustment,
            })
        else:
            adjusted_exit["economic_adjustments"] = {
                "recession_effect": recession_effect,
                "inflation_effect": inflation_effect,
                "employment_effect": employment_effect,
                "migration_effect": migration_effect,
                "regulatory_effect": regulatory_effect,
                "tax_effect": tax_effect,
                "total_adjustment": total_adjustment,
            }

        # Recalculate exit value and appreciation share
        # This is necessary because the exit month has changed
        if total_adjustment != 0:
            # Get property details
            property_id = exit_data.get("property_id", "")
            property_value = exit_data.get("property_value", 0.0)
            zone = exit_data.get("zone", "green")
            suburb_id = exit_data.get("suburb_id", "")
            loan_id = exit_data.get("loan_id", "")

            # Create loan dictionary for exit value calculation
            loan_dict = {
                "loan_id": loan_id,
                "property_id": property_id,
                "suburb_id": suburb_id,
                "zone": zone,
                "loan_amount": exit_data.get("loan_amount", 0.0),
                "property_value": property_value,
            }

            # Convert exit type string to enum
            exit_type_enum = ExitType(exit_type)

            # Calculate exit value
            exit_value, appreciation_share_amount = calculate_exit_value(
                loan=loan_dict,
                exit_month=adjusted_exit_month,
                exit_type=exit_type_enum,
                price_paths=price_paths,
                appreciation_share=0.2,  # Default value
                min_appreciation_share=0.1,  # Default value
                max_appreciation_share=0.5,  # Default value
                tiered_appreciation_thresholds=[0.2, 0.5, 1.0],  # Default values
                tiered_appreciation_shares=[0.1, 0.2, 0.3, 0.4],  # Default values
                recovery_rate=0.8,  # Default value
                foreclosure_cost=0.1,  # Default value
            )

            # Update exit value and appreciation share
            adjusted_exit["exit_value"] = exit_value
            adjusted_exit["appreciation_share_amount"] = appreciation_share_amount
            adjusted_exit["total_return"] = exit_value + appreciation_share_amount

            # Recalculate ROI
            loan_amount = exit_data.get("loan_amount", 0.0)
            adjusted_exit["roi"] = (exit_value + appreciation_share_amount - loan_amount) / loan_amount if loan_amount > 0 else 0.0

            # Recalculate annualized ROI
            adjusted_exit["annualized_roi"] = ((exit_value + appreciation_share_amount) / loan_amount) ** (1 / adjusted_exit_year) - 1 if adjusted_exit_year > 0 else 0.0

        # Add to adjusted exits
        adjusted_exits.append(adjusted_exit)

    # Store exit adjustments in context for analysis
    context.economic_exit_adjustments = exit_adjustments

    # Log summary of adjustments
    logger.info(
        "Economic model adjustments",
        avg_recession_effect=np.mean(exit_adjustments["recession_effect"]),
        avg_inflation_effect=np.mean(exit_adjustments["inflation_effect"]),
        avg_employment_effect=np.mean(exit_adjustments["employment_effect"]),
        avg_migration_effect=np.mean(exit_adjustments["migration_effect"]),
        avg_regulatory_effect=np.mean(exit_adjustments["regulatory_effect"]),
        avg_tax_effect=np.mean(exit_adjustments["tax_effect"]),
        avg_total_effect=np.mean(exit_adjustments["total_effect"]),
    )

    return adjusted_exits


def apply_ml_models(
    exits: List[Dict[str, Any]],
    context: SimulationContext,
    config: Any,
) -> List[Dict[str, Any]]:
    """
    Apply machine learning models to adjust exits.

    This function applies machine learning models to predict exit timing and types,
    identify patterns, and detect anomalies.

    Args:
        exits: List of exits
        context: Simulation context
        config: Enhanced exit simulator configuration

    Returns:
        Adjusted list of exits
    """
    logger.info("Applying machine learning models to exits")

    # Get random number generator
    rng = context.rng or get_rng("enhanced_exit_simulator", 0)

    # Get parameters
    feature_importance_threshold = getattr(config, "feature_importance_threshold", 0.05)
    anomaly_detection_threshold = getattr(config, "anomaly_detection_threshold", 3.0)

    # Get loans
    loans = context.loans

    # Create a mapping of loan_id to loan
    loan_map = {loan.get("loan_id", ""): loan for loan in loans}

    # Skip if not enough exits for ML
    if len(exits) < 10:
        logger.warning("Not enough exits for ML models, skipping")
        return exits

    # Prepare data for ML models
    features = []
    targets = []

    for exit_data in exits:
        # Get loan details
        loan_id = exit_data.get("loan_id", "")
        loan = loan_map.get(loan_id, {})

        # Get exit details
        exit_month = exit_data.get("exit_month", 0)
        exit_type = exit_data.get("exit_type", "")
        exit_year = exit_data.get("exit_year", 0.0)
        roi = exit_data.get("roi", 0.0)

        # Get property details
        property_value = exit_data.get("property_value", 0.0)
        loan_amount = exit_data.get("loan_amount", 0.0)
        ltv = loan.get("ltv", loan_amount / property_value if property_value > 0 else 0.0)
        zone = exit_data.get("zone", "green")
        suburb_id = exit_data.get("suburb_id", "")

        # Get behavioral adjustments
        behavioral_adjustments = exit_data.get("behavioral_adjustments", {})
        interest_rate_effect = behavioral_adjustments.get("interest_rate_effect", 0.0)
        appreciation_effect = behavioral_adjustments.get("appreciation_effect", 0.0)
        life_event_effect = behavioral_adjustments.get("life_event_effect", 0.0)
        herd_effect = behavioral_adjustments.get("herd_effect", 0.0)

        # Get economic adjustments
        economic_adjustments = exit_data.get("economic_adjustments", {})
        recession_effect = economic_adjustments.get("recession_effect", 0.0)
        inflation_effect = economic_adjustments.get("inflation_effect", 0.0)
        employment_effect = economic_adjustments.get("employment_effect", 0.0)
        migration_effect = economic_adjustments.get("migration_effect", 0.0)
        regulatory_effect = economic_adjustments.get("regulatory_effect", 0.0)
        tax_effect = economic_adjustments.get("tax_effect", 0.0)

        # Create feature vector
        feature = [
            exit_month,
            property_value,
            loan_amount,
            ltv,
            1.0 if zone == "green" else (0.5 if zone == "orange" else 0.0),  # Zone encoding
            interest_rate_effect,
            appreciation_effect,
            life_event_effect,
            herd_effect,
            recession_effect,
            inflation_effect,
            employment_effect,
            migration_effect,
            regulatory_effect,
            tax_effect,
        ]

        # Create target vector
        target = [
            exit_year,
            1.0 if exit_type == "sale" else 0.0,
            1.0 if exit_type == "refinance" else 0.0,
            1.0 if exit_type == "default" else 0.0,
            1.0 if exit_type == "term_completion" else 0.0,
            roi,
        ]

        features.append(feature)
        targets.append(target)

    # Convert to numpy arrays
    X = np.array(features)
    y = np.array(targets)

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Store feature names for interpretation
    feature_names = [
        "exit_month",
        "property_value",
        "loan_amount",
        "ltv",
        "zone",
        "interest_rate_effect",
        "appreciation_effect",
        "life_event_effect",
        "herd_effect",
        "recession_effect",
        "inflation_effect",
        "employment_effect",
        "migration_effect",
        "regulatory_effect",
        "tax_effect",
    ]

    # Store target names for interpretation
    target_names = [
        "exit_year",
        "is_sale",
        "is_refinance",
        "is_default",
        "is_term_completion",
        "roi",
    ]

    # Perform cluster analysis
    try:
        # Determine optimal number of clusters
        max_clusters = min(10, len(exits) // 5)
        if max_clusters >= 2:
            inertia = []
            for k in range(2, max_clusters + 1):
                kmeans = KMeans(n_clusters=k, random_state=42)
                kmeans.fit(X_scaled)
                inertia.append(kmeans.inertia_)

            # Find elbow point
            optimal_clusters = 2
            if len(inertia) > 1:
                # Simple elbow detection
                diffs = np.diff(inertia)
                optimal_clusters = np.argmin(diffs) + 2

            # Cluster exits
            kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)

            # Calculate cluster statistics
            cluster_stats = {}
            for i in range(optimal_clusters):
                cluster_indices = np.where(clusters == i)[0]
                cluster_exits = [exits[j] for j in cluster_indices]

                # Calculate average statistics
                avg_exit_year = np.mean([exit_data.get("exit_year", 0.0) for exit_data in cluster_exits])
                avg_roi = np.mean([exit_data.get("roi", 0.0) for exit_data in cluster_exits])

                # Calculate exit type distribution
                exit_types = [exit_data.get("exit_type", "") for exit_data in cluster_exits]
                exit_type_counts = {}
                for exit_type in exit_types:
                    if exit_type not in exit_type_counts:
                        exit_type_counts[exit_type] = 0
                    exit_type_counts[exit_type] += 1

                exit_type_distribution = {
                    exit_type: count / len(cluster_exits) for exit_type, count in exit_type_counts.items()
                }

                # Store cluster statistics
                cluster_stats[i] = {
                    "size": len(cluster_exits),
                    "avg_exit_year": avg_exit_year,
                    "avg_roi": avg_roi,
                    "exit_type_distribution": exit_type_distribution,
                }

            # Store cluster information in context
            context.exit_clusters = {
                "num_clusters": optimal_clusters,
                "cluster_assignments": clusters.tolist(),
                "cluster_stats": cluster_stats,
            }

            # Add cluster information to exits
            for i, (exit_data, cluster) in enumerate(zip(exits, clusters)):
                exit_data["cluster"] = int(cluster)
                exit_data["cluster_stats"] = cluster_stats[int(cluster)]

    except Exception as e:
        logger.warning(f"Cluster analysis failed: {str(e)}")

    # Train exit timing prediction model
    try:
        # Use exit_year as target
        y_timing = y[:, 0]

        # Train model
        model = GradientBoostingRegressor(random_state=42)
        model.fit(X_scaled, y_timing)

        # Get feature importances
        importances = model.feature_importances_

        # Store feature importances in context
        context.exit_timing_feature_importances = {
            feature_names[i]: importances[i] for i in range(len(feature_names))
        }

        # Identify important features
        important_features = [
            feature_names[i] for i in range(len(feature_names))
            if importances[i] >= feature_importance_threshold
        ]

        # Store important features in context
        context.exit_timing_important_features = important_features

        # Make predictions
        y_timing_pred = model.predict(X_scaled)

        # Calculate prediction errors
        timing_errors = y_timing - y_timing_pred

        # Detect anomalies
        timing_error_mean = np.mean(timing_errors)
        timing_error_std = np.std(timing_errors)
        timing_anomalies = np.abs(timing_errors - timing_error_mean) > anomaly_detection_threshold * timing_error_std

        # Add predictions and anomaly detection to exits
        for i, (exit_data, pred, error, is_anomaly) in enumerate(zip(exits, y_timing_pred, timing_errors, timing_anomalies)):
            exit_data["ml_predicted_exit_year"] = float(pred)
            exit_data["ml_exit_year_error"] = float(error)
            exit_data["ml_exit_timing_anomaly"] = bool(is_anomaly)

    except Exception as e:
        logger.warning(f"Exit timing prediction failed: {str(e)}")

    # Train exit type prediction model
    try:
        # Use exit type as target (one-hot encoded)
        y_type = y[:, 1:5]

        # Train model
        model = RandomForestClassifier(random_state=42)
        model.fit(X_scaled, np.argmax(y_type, axis=1))

        # Get feature importances
        importances = model.feature_importances_

        # Store feature importances in context
        context.exit_type_feature_importances = {
            feature_names[i]: importances[i] for i in range(len(feature_names))
        }

        # Identify important features
        important_features = [
            feature_names[i] for i in range(len(feature_names))
            if importances[i] >= feature_importance_threshold
        ]

        # Store important features in context
        context.exit_type_important_features = important_features

        # Make predictions
        y_type_pred = model.predict_proba(X_scaled)

        # Add predictions to exits
        exit_type_names = ["sale", "refinance", "default", "term_completion"]
        for i, (exit_data, probs) in enumerate(zip(exits, y_type_pred)):
            exit_data["ml_exit_type_probabilities"] = {
                exit_type_names[j]: float(probs[j]) for j in range(len(exit_type_names))
            }

    except Exception as e:
        logger.warning(f"Exit type prediction failed: {str(e)}")

    # Train ROI prediction model
    try:
        # Use ROI as target
        y_roi = y[:, 5]

        # Train model
        model = GradientBoostingRegressor(random_state=42)
        model.fit(X_scaled, y_roi)

        # Get feature importances
        importances = model.feature_importances_

        # Store feature importances in context
        context.roi_feature_importances = {
            feature_names[i]: importances[i] for i in range(len(feature_names))
        }

        # Identify important features
        important_features = [
            feature_names[i] for i in range(len(feature_names))
            if importances[i] >= feature_importance_threshold
        ]

        # Store important features in context
        context.roi_important_features = important_features

        # Make predictions
        y_roi_pred = model.predict(X_scaled)

        # Calculate prediction errors
        roi_errors = y_roi - y_roi_pred

        # Detect anomalies
        roi_error_mean = np.mean(roi_errors)
        roi_error_std = np.std(roi_errors)
        roi_anomalies = np.abs(roi_errors - roi_error_mean) > anomaly_detection_threshold * roi_error_std

        # Add predictions and anomaly detection to exits
        for i, (exit_data, pred, error, is_anomaly) in enumerate(zip(exits, y_roi_pred, roi_errors, roi_anomalies)):
            exit_data["ml_predicted_roi"] = float(pred)
            exit_data["ml_roi_error"] = float(error)
            exit_data["ml_roi_anomaly"] = bool(is_anomaly)

    except Exception as e:
        logger.warning(f"ROI prediction failed: {str(e)}")

    return exits


def calculate_enhanced_exit_statistics(
    exits: List[Dict[str, Any]],
    base_exits: List[Dict[str, Any]],
    context: SimulationContext,
    config: Any,
) -> Dict[str, Any]:
    """
    Calculate enhanced statistics for exits.

    This function extends the base exit statistics with advanced metrics,
    cohort analysis, risk metrics, and machine learning insights.

    Args:
        exits: List of exits
        base_exits: List of base exits (before enhancements)
        context: Simulation context
        config: Enhanced exit simulator configuration

    Returns:
        Dictionary containing enhanced exit statistics
    """
    logger.info("Calculating enhanced exit statistics")

    # Get parameters
    vintage_segmentation = getattr(config, "vintage_segmentation", True)
    ltv_segmentation = getattr(config, "ltv_segmentation", True)
    zone_segmentation = getattr(config, "zone_segmentation", True)
    var_confidence_level = getattr(config, "var_confidence_level", 0.95)
    stress_test_severity = getattr(config, "stress_test_severity", 0.3)
    tail_risk_threshold = getattr(config, "tail_risk_threshold", 0.05)

    # Calculate base statistics
    base_stats = calculate_exit_statistics(
        exits=exits,
        num_steps=int(context.config.fund_term * 12),
        dt=1.0 / 12.0,
    )

    # Initialize enhanced statistics
    enhanced_stats = base_stats.copy()

    # Add comparison to base exits
    if base_exits:
        base_base_stats = calculate_exit_statistics(
            exits=base_exits,
            num_steps=int(context.config.fund_term * 12),
            dt=1.0 / 12.0,
        )

        # Calculate differences
        enhanced_stats["comparison_to_base"] = {
            "avg_exit_year_diff": base_stats["avg_exit_year"] - base_base_stats["avg_exit_year"],
            "avg_roi_diff": base_stats["avg_roi"] - base_base_stats["avg_roi"],
            "avg_annualized_roi_diff": base_stats["avg_annualized_roi"] - base_base_stats["avg_annualized_roi"],
            "exit_type_distribution_diff": {
                exit_type: base_stats["exit_type_distribution"].get(exit_type, 0) -
                           base_base_stats["exit_type_distribution"].get(exit_type, 0)
                for exit_type in set(base_stats["exit_type_distribution"].keys()) |
                                 set(base_base_stats["exit_type_distribution"].keys())
            },
            "total_return_diff": base_stats["total_return"] - base_base_stats["total_return"],
            "total_roi_diff": base_stats["total_roi"] - base_base_stats["total_roi"],
            "annualized_roi_diff": base_stats["annualized_roi"] - base_base_stats["annualized_roi"],
        }

    # Add cohort analysis if enabled
    cohort_analysis = {}

    # Vintage segmentation (by origination year)
    if vintage_segmentation:
        vintage_stats = {}

        # Group exits by origination year
        for exit_data in exits:
            origination_date = exit_data.get("origination_date", 0)
            origination_year = int(origination_date / 12)

            if origination_year not in vintage_stats:
                vintage_stats[origination_year] = []

            vintage_stats[origination_year].append(exit_data)

        # Calculate statistics for each vintage
        vintage_summary = {}
        for vintage, vintage_exits in vintage_stats.items():
            # Calculate average statistics
            avg_exit_year = np.mean([exit_data.get("exit_year", 0.0) for exit_data in vintage_exits])
            avg_roi = np.mean([exit_data.get("roi", 0.0) for exit_data in vintage_exits])
            avg_annualized_roi = np.mean([exit_data.get("annualized_roi", 0.0) for exit_data in vintage_exits])

            # Calculate exit type distribution
            exit_types = [exit_data.get("exit_type", "") for exit_data in vintage_exits]
            exit_type_counts = {}
            for exit_type in exit_types:
                if exit_type not in exit_type_counts:
                    exit_type_counts[exit_type] = 0
                exit_type_counts[exit_type] += 1

            exit_type_distribution = {
                exit_type: count / len(vintage_exits) for exit_type, count in exit_type_counts.items()
            }

            # Store vintage statistics
            vintage_summary[vintage] = {
                "count": len(vintage_exits),
                "avg_exit_year": avg_exit_year,
                "avg_roi": avg_roi,
                "avg_annualized_roi": avg_annualized_roi,
                "exit_type_distribution": exit_type_distribution,
            }

        cohort_analysis["vintage"] = vintage_summary

    # LTV segmentation
    if ltv_segmentation:
        ltv_stats = {}

        # Define LTV buckets
        ltv_buckets = [
            (0.0, 0.5, "0-50%"),
            (0.5, 0.6, "50-60%"),
            (0.6, 0.7, "60-70%"),
            (0.7, 0.8, "70-80%"),
            (0.8, 0.9, "80-90%"),
            (0.9, 1.0, "90-100%"),
        ]

        # Group exits by LTV bucket
        for exit_data in exits:
            ltv = exit_data.get("ltv", 0.0)

            # Find the appropriate bucket
            bucket_name = None
            for low, high, name in ltv_buckets:
                if low <= ltv < high:
                    bucket_name = name
                    break

            if bucket_name is None:
                bucket_name = ">100%"

            if bucket_name not in ltv_stats:
                ltv_stats[bucket_name] = []

            ltv_stats[bucket_name].append(exit_data)

        # Calculate statistics for each LTV bucket
        ltv_summary = {}
        for bucket_name, bucket_exits in ltv_stats.items():
            # Calculate average statistics
            avg_exit_year = np.mean([exit_data.get("exit_year", 0.0) for exit_data in bucket_exits])
            avg_roi = np.mean([exit_data.get("roi", 0.0) for exit_data in bucket_exits])
            avg_annualized_roi = np.mean([exit_data.get("annualized_roi", 0.0) for exit_data in bucket_exits])

            # Calculate exit type distribution
            exit_types = [exit_data.get("exit_type", "") for exit_data in bucket_exits]
            exit_type_counts = {}
            for exit_type in exit_types:
                if exit_type not in exit_type_counts:
                    exit_type_counts[exit_type] = 0
                exit_type_counts[exit_type] += 1

            exit_type_distribution = {
                exit_type: count / len(bucket_exits) for exit_type, count in exit_type_counts.items()
            }

            # Store LTV bucket statistics
            ltv_summary[bucket_name] = {
                "count": len(bucket_exits),
                "avg_exit_year": avg_exit_year,
                "avg_roi": avg_roi,
                "avg_annualized_roi": avg_annualized_roi,
                "exit_type_distribution": exit_type_distribution,
            }

        cohort_analysis["ltv"] = ltv_summary

    # Zone segmentation
    if zone_segmentation:
        zone_stats = {}

        # Group exits by zone
        for exit_data in exits:
            zone = exit_data.get("zone", "green")

            if zone not in zone_stats:
                zone_stats[zone] = []

            zone_stats[zone].append(exit_data)

        # Calculate statistics for each zone
        zone_summary = {}
        for zone, zone_exits in zone_stats.items():
            # Calculate average statistics
            avg_exit_year = np.mean([exit_data.get("exit_year", 0.0) for exit_data in zone_exits])
            avg_roi = np.mean([exit_data.get("roi", 0.0) for exit_data in zone_exits])
            avg_annualized_roi = np.mean([exit_data.get("annualized_roi", 0.0) for exit_data in zone_exits])

            # Calculate exit type distribution
            exit_types = [exit_data.get("exit_type", "") for exit_data in zone_exits]
            exit_type_counts = {}
            for exit_type in exit_types:
                if exit_type not in exit_type_counts:
                    exit_type_counts[exit_type] = 0
                exit_type_counts[exit_type] += 1

            exit_type_distribution = {
                exit_type: count / len(zone_exits) for exit_type, count in exit_type_counts.items()
            }

            # Store zone statistics
            zone_summary[zone] = {
                "count": len(zone_exits),
                "avg_exit_year": avg_exit_year,
                "avg_roi": avg_roi,
                "avg_annualized_roi": avg_annualized_roi,
                "exit_type_distribution": exit_type_distribution,
            }

        cohort_analysis["zone"] = zone_summary

    # Add cohort analysis to enhanced statistics
    enhanced_stats["cohort_analysis"] = cohort_analysis

    # Create a summary of cohort analysis
    cohort_analysis_summary = {}

    if "vintage" in cohort_analysis:
        best_vintage = max(
            cohort_analysis["vintage"].items(),
            key=lambda x: x[1]["avg_annualized_roi"],
        )[0]
        worst_vintage = min(
            cohort_analysis["vintage"].items(),
            key=lambda x: x[1]["avg_annualized_roi"],
        )[0]

        cohort_analysis_summary["vintage"] = {
            "best_vintage": best_vintage,
            "best_vintage_roi": cohort_analysis["vintage"][best_vintage]["avg_annualized_roi"],
            "worst_vintage": worst_vintage,
            "worst_vintage_roi": cohort_analysis["vintage"][worst_vintage]["avg_annualized_roi"],
        }

    if "ltv" in cohort_analysis:
        best_ltv = max(
            cohort_analysis["ltv"].items(),
            key=lambda x: x[1]["avg_annualized_roi"],
        )[0]
        worst_ltv = min(
            cohort_analysis["ltv"].items(),
            key=lambda x: x[1]["avg_annualized_roi"],
        )[0]

        cohort_analysis_summary["ltv"] = {
            "best_ltv": best_ltv,
            "best_ltv_roi": cohort_analysis["ltv"][best_ltv]["avg_annualized_roi"],
            "worst_ltv": worst_ltv,
            "worst_ltv_roi": cohort_analysis["ltv"][worst_ltv]["avg_annualized_roi"],
        }

    if "zone" in cohort_analysis:
        best_zone = max(
            cohort_analysis["zone"].items(),
            key=lambda x: x[1]["avg_annualized_roi"],
        )[0]
        worst_zone = min(
            cohort_analysis["zone"].items(),
            key=lambda x: x[1]["avg_annualized_roi"],
        )[0]

        cohort_analysis_summary["zone"] = {
            "best_zone": best_zone,
            "best_zone_roi": cohort_analysis["zone"][best_zone]["avg_annualized_roi"],
            "worst_zone": worst_zone,
            "worst_zone_roi": cohort_analysis["zone"][worst_zone]["avg_annualized_roi"],
        }

    enhanced_stats["cohort_analysis_summary"] = cohort_analysis_summary

    # Add risk metrics
    risk_metrics = {}

    # Calculate Value-at-Risk (VaR)
    rois = [exit_data.get("roi", 0.0) for exit_data in exits]
    var_index = int((1 - var_confidence_level) * len(rois))
    var_index = max(0, min(var_index, len(rois) - 1))

    # Sort ROIs in ascending order
    sorted_rois = sorted(rois)

    # Calculate VaR
    var = -sorted_rois[var_index]

    # Calculate Conditional VaR (CVaR) / Expected Shortfall
    cvar = -np.mean(sorted_rois[:var_index+1])

    # Calculate tail risk metrics
    tail_threshold = np.quantile(rois, tail_risk_threshold)
    tail_events = [roi for roi in rois if roi <= tail_threshold]
    tail_probability = len(tail_events) / len(rois)
    tail_severity = np.mean(tail_events) if tail_events else 0.0

    # Calculate maximum drawdown
    # For simplicity, we'll use the worst ROI as a proxy
    max_drawdown = -min(rois)

    # Calculate stress test metrics
    # Simulate a stress scenario by reducing all positive ROIs by stress_test_severity
    stress_rois = [
        roi * (1 - stress_test_severity) if roi > 0 else roi * (1 + stress_test_severity)
        for roi in rois
    ]
    stress_avg_roi = np.mean(stress_rois)

    # Store risk metrics
    risk_metrics = {
        "value_at_risk": var,
        "conditional_var": cvar,
        "tail_probability": tail_probability,
        "tail_severity": tail_severity,
        "max_drawdown": max_drawdown,
        "stress_test_roi": stress_avg_roi,
        "roi_volatility": np.std(rois),
    }

    enhanced_stats["risk_metrics"] = risk_metrics

    # Add machine learning insights if available
    ml_insights = {}

    # Add feature importances for exit timing
    if hasattr(context, "exit_timing_feature_importances"):
        ml_insights["exit_timing_feature_importances"] = context.exit_timing_feature_importances

    # Add important features for exit timing
    if hasattr(context, "exit_timing_important_features"):
        ml_insights["exit_timing_important_features"] = context.exit_timing_important_features

    # Add feature importances for exit type
    if hasattr(context, "exit_type_feature_importances"):
        ml_insights["exit_type_feature_importances"] = context.exit_type_feature_importances

    # Add important features for exit type
    if hasattr(context, "exit_type_important_features"):
        ml_insights["exit_type_important_features"] = context.exit_type_important_features

    # Add feature importances for ROI
    if hasattr(context, "roi_feature_importances"):
        ml_insights["roi_feature_importances"] = context.roi_feature_importances

    # Add important features for ROI
    if hasattr(context, "roi_important_features"):
        ml_insights["roi_important_features"] = context.roi_important_features

    # Add cluster information
    if hasattr(context, "exit_clusters"):
        ml_insights["exit_clusters"] = context.exit_clusters

    # Add anomaly detection
    anomalies = []
    for exit_data in exits:
        if exit_data.get("ml_exit_timing_anomaly", False) or exit_data.get("ml_roi_anomaly", False):
            anomalies.append({
                "loan_id": exit_data.get("loan_id", ""),
                "exit_year": exit_data.get("exit_year", 0.0),
                "exit_type": exit_data.get("exit_type", ""),
                "roi": exit_data.get("roi", 0.0),
                "exit_timing_anomaly": exit_data.get("ml_exit_timing_anomaly", False),
                "roi_anomaly": exit_data.get("ml_roi_anomaly", False),
            })

    ml_insights["anomalies"] = anomalies

    enhanced_stats["ml_insights"] = ml_insights

    return enhanced_stats


def generate_enhanced_exit_visualization(
    exits: List[Dict[str, Any]],
    exit_stats: Dict[str, Any],
    context: SimulationContext,
    config: Any,
) -> Dict[str, Any]:
    """
    Generate enhanced visualization data for exits.

    This function extends the base exit visualization with advanced visualizations,
    including cohort analysis, risk metrics, and machine learning insights.

    Args:
        exits: List of exits
        exit_stats: Exit statistics
        context: Simulation context
        config: Enhanced exit simulator configuration

    Returns:
        Dictionary containing enhanced visualization data
    """
    logger.info("Generating enhanced exit visualization")

    # Generate base visualization
    base_visualization = generate_exit_visualization(
        exits=exits,
        exit_stats=exit_stats,
        num_steps=int(context.config.fund_term * 12),
        dt=1.0 / 12.0,
    )

    # Initialize enhanced visualization
    enhanced_visualization = base_visualization.copy()

    # Add cohort analysis visualizations
    cohort_visualizations = {}

    # Add vintage visualization if available
    if "cohort_analysis" in exit_stats and "vintage" in exit_stats["cohort_analysis"]:
        vintage_data = exit_stats["cohort_analysis"]["vintage"]

        # Create vintage ROI chart
        vintage_roi_chart = []
        for vintage, stats in vintage_data.items():
            vintage_roi_chart.append({
                "vintage": vintage,
                "count": stats["count"],
                "avg_roi": stats["avg_roi"],
                "avg_annualized_roi": stats["avg_annualized_roi"],
            })

        # Sort by vintage
        vintage_roi_chart.sort(key=lambda x: x["vintage"])

        # Create vintage exit type chart
        vintage_exit_type_chart = []
        for vintage, stats in vintage_data.items():
            for exit_type, percentage in stats["exit_type_distribution"].items():
                vintage_exit_type_chart.append({
                    "vintage": vintage,
                    "exit_type": exit_type,
                    "percentage": percentage,
                    "count": int(percentage * stats["count"]),
                })

        cohort_visualizations["vintage"] = {
            "roi_chart": vintage_roi_chart,
            "exit_type_chart": vintage_exit_type_chart,
        }

    # Add LTV visualization if available
    if "cohort_analysis" in exit_stats and "ltv" in exit_stats["cohort_analysis"]:
        ltv_data = exit_stats["cohort_analysis"]["ltv"]

        # Create LTV ROI chart
        ltv_roi_chart = []

        # Define LTV bucket order
        ltv_bucket_order = [
            "0-50%", "50-60%", "60-70%", "70-80%", "80-90%", "90-100%", ">100%"
        ]

        # Add buckets in order
        for bucket in ltv_bucket_order:
            if bucket in ltv_data:
                stats = ltv_data[bucket]
                ltv_roi_chart.append({
                    "ltv_bucket": bucket,
                    "count": stats["count"],
                    "avg_roi": stats["avg_roi"],
                    "avg_annualized_roi": stats["avg_annualized_roi"],
                })

        # Create LTV exit type chart
        ltv_exit_type_chart = []
        for bucket in ltv_bucket_order:
            if bucket in ltv_data:
                stats = ltv_data[bucket]
                for exit_type, percentage in stats["exit_type_distribution"].items():
                    ltv_exit_type_chart.append({
                        "ltv_bucket": bucket,
                        "exit_type": exit_type,
                        "percentage": percentage,
                        "count": int(percentage * stats["count"]),
                    })

        cohort_visualizations["ltv"] = {
            "roi_chart": ltv_roi_chart,
            "exit_type_chart": ltv_exit_type_chart,
        }

    # Add zone visualization if available
    if "cohort_analysis" in exit_stats and "zone" in exit_stats["cohort_analysis"]:
        zone_data = exit_stats["cohort_analysis"]["zone"]

        # Create zone ROI chart
        zone_roi_chart = []
        for zone, stats in zone_data.items():
            zone_roi_chart.append({
                "zone": zone,
                "count": stats["count"],
                "avg_roi": stats["avg_roi"],
                "avg_annualized_roi": stats["avg_annualized_roi"],
            })

        # Create zone exit type chart
        zone_exit_type_chart = []
        for zone, stats in zone_data.items():
            for exit_type, percentage in stats["exit_type_distribution"].items():
                zone_exit_type_chart.append({
                    "zone": zone,
                    "exit_type": exit_type,
                    "percentage": percentage,
                    "count": int(percentage * stats["count"]),
                })

        cohort_visualizations["zone"] = {
            "roi_chart": zone_roi_chart,
            "exit_type_chart": zone_exit_type_chart,
        }

    # Add cohort visualizations to enhanced visualization
    enhanced_visualization["cohort_visualizations"] = cohort_visualizations

    # Add risk metrics visualizations
    risk_visualizations = {}

    # Add ROI distribution chart
    if exits:
        rois = [exit_data.get("roi", 0.0) for exit_data in exits]

        # Calculate histogram
        roi_min = min(rois)
        roi_max = max(rois)
        roi_bins = np.linspace(roi_min, roi_max, 20)
        roi_hist, roi_edges = np.histogram(rois, bins=roi_bins)

        # Create ROI distribution chart
        roi_distribution_chart = []
        for i in range(len(roi_hist)):
            roi_distribution_chart.append({
                "bin_min": float(roi_edges[i]),
                "bin_max": float(roi_edges[i+1]),
                "bin_center": float((roi_edges[i] + roi_edges[i+1]) / 2),
                "count": int(roi_hist[i]),
                "percentage": float(roi_hist[i] / len(rois)),
            })

        risk_visualizations["roi_distribution_chart"] = roi_distribution_chart

    # Add VaR visualization
    if "risk_metrics" in exit_stats:
        risk_metrics = exit_stats["risk_metrics"]

        # Create VaR chart
        var_chart = {
            "value_at_risk": risk_metrics["value_at_risk"],
            "conditional_var": risk_metrics["conditional_var"],
            "tail_probability": risk_metrics["tail_probability"],
            "tail_severity": risk_metrics["tail_severity"],
            "max_drawdown": risk_metrics["max_drawdown"],
        }

        risk_visualizations["var_chart"] = var_chart

    # Add stress test visualization
    if "risk_metrics" in exit_stats:
        risk_metrics = exit_stats["risk_metrics"]

        # Create stress test chart
        stress_test_chart = {
            "base_roi": exit_stats["avg_roi"],
            "stress_roi": risk_metrics["stress_test_roi"],
            "roi_volatility": risk_metrics["roi_volatility"],
        }

        risk_visualizations["stress_test_chart"] = stress_test_chart

    # Add risk visualizations to enhanced visualization
    enhanced_visualization["risk_visualizations"] = risk_visualizations

    # Add machine learning visualizations
    ml_visualizations = {}

    # Add feature importance visualization
    if hasattr(context, "exit_timing_feature_importances"):
        # Create feature importance chart
        feature_importance_chart = []
        for feature, importance in context.exit_timing_feature_importances.items():
            feature_importance_chart.append({
                "feature": feature,
                "importance": importance,
            })

        # Sort by importance
        feature_importance_chart.sort(key=lambda x: x["importance"], reverse=True)

        ml_visualizations["feature_importance_chart"] = feature_importance_chart

    # Add cluster visualization
    if hasattr(context, "exit_clusters"):
        # Create cluster chart
        cluster_chart = []
        for cluster_id, stats in context.exit_clusters["cluster_stats"].items():
            cluster_chart.append({
                "cluster_id": cluster_id,
                "size": stats["size"],
                "avg_exit_year": stats["avg_exit_year"],
                "avg_roi": stats["avg_roi"],
                "exit_type_distribution": stats["exit_type_distribution"],
            })

        ml_visualizations["cluster_chart"] = cluster_chart

    # Add anomaly visualization
    if "ml_insights" in exit_stats and "anomalies" in exit_stats["ml_insights"]:
        # Create anomaly chart
        anomaly_chart = exit_stats["ml_insights"]["anomalies"]

        ml_visualizations["anomaly_chart"] = anomaly_chart

    # Add ML visualizations to enhanced visualization
    enhanced_visualization["ml_visualizations"] = ml_visualizations

    # Add economic scenario visualization
    economic_visualizations = {}

    # Add economic indicators chart
    if hasattr(context, "economic_scenario"):
        economic_scenario = context.economic_scenario

        # Create economic indicators chart
        economic_indicators_chart = []
        num_months = len(economic_scenario["gdp_growth"])

        for i in range(num_months):
            economic_indicators_chart.append({
                "month": i,
                "year": i / 12.0,
                "gdp_growth": economic_scenario["gdp_growth"][i],
                "inflation_rate": economic_scenario["inflation_rate"][i],
                "employment_growth": economic_scenario["employment_growth"][i],
                "migration_rate": economic_scenario["migration_rate"][i],
                "is_recession": economic_scenario["recession_periods"][i],
                "has_regulatory_change": economic_scenario["regulatory_changes"][i],
            })

        economic_visualizations["economic_indicators_chart"] = economic_indicators_chart

    # Add economic adjustment visualization
    if hasattr(context, "economic_exit_adjustments"):
        economic_adjustments = context.economic_exit_adjustments

        # Calculate average adjustments
        avg_adjustments = {
            "recession_effect": np.mean(economic_adjustments["recession_effect"]),
            "inflation_effect": np.mean(economic_adjustments["inflation_effect"]),
            "employment_effect": np.mean(economic_adjustments["employment_effect"]),
            "migration_effect": np.mean(economic_adjustments["migration_effect"]),
            "regulatory_effect": np.mean(economic_adjustments["regulatory_effect"]),
            "tax_effect": np.mean(economic_adjustments["tax_effect"]),
            "total_effect": np.mean(economic_adjustments["total_effect"]),
        }

        economic_visualizations["economic_adjustments_chart"] = avg_adjustments

    # Add economic visualizations to enhanced visualization
    enhanced_visualization["economic_visualizations"] = economic_visualizations

    # Add geospatial visualization
    geospatial_visualizations = {}

    # Add exit map
    if exits:
        # Get TLS manager
        tls_manager = get_tls_manager()

        # Create exit map
        exit_map = []

        # Group exits by suburb
        suburb_exits = {}
        for exit_data in exits:
            suburb_id = exit_data.get("suburb_id", "")

            if suburb_id not in suburb_exits:
                suburb_exits[suburb_id] = []

            suburb_exits[suburb_id].append(exit_data)

        # Calculate statistics for each suburb
        for suburb_id, suburb_exit_list in suburb_exits.items():
            suburb = tls_manager.suburbs.get(suburb_id)

            if suburb:
                # Calculate average statistics
                avg_exit_year = np.mean([exit_data.get("exit_year", 0.0) for exit_data in suburb_exit_list])
                avg_roi = np.mean([exit_data.get("roi", 0.0) for exit_data in suburb_exit_list])

                # Calculate exit type distribution
                exit_types = [exit_data.get("exit_type", "") for exit_data in suburb_exit_list]
                exit_type_counts = {}
                for exit_type in exit_types:
                    if exit_type not in exit_type_counts:
                        exit_type_counts[exit_type] = 0
                    exit_type_counts[exit_type] += 1

                exit_type_distribution = {
                    exit_type: count / len(suburb_exit_list) for exit_type, count in exit_type_counts.items()
                }

                # Add to exit map
                exit_map.append({
                    "suburb_id": suburb_id,
                    "suburb_name": suburb.name,
                    "latitude": suburb.latitude,
                    "longitude": suburb.longitude,
                    "count": len(suburb_exit_list),
                    "avg_exit_year": avg_exit_year,
                    "avg_roi": avg_roi,
                    "exit_type_distribution": exit_type_distribution,
                })

        geospatial_visualizations["exit_map"] = exit_map

    # Add geospatial visualizations to enhanced visualization
    enhanced_visualization["geospatial_visualizations"] = geospatial_visualizations

    # Add comparative visualizations
    comparative_visualizations = {}

    # Add actual vs. expected exit timing
    if exits and hasattr(context, "expected_exits"):
        expected_exits = context.expected_exits

        # Calculate actual exit year distribution
        actual_exit_years = [exit_data.get("exit_year", 0.0) for exit_data in exits]

        # Calculate expected exit year distribution
        expected_exit_years = [exit_data.get("exit_year", 0.0) for exit_data in expected_exits]

        # Create bins
        min_year = min(min(actual_exit_years), min(expected_exit_years))
        max_year = max(max(actual_exit_years), max(expected_exit_years))
        year_bins = np.linspace(min_year, max_year, 20)

        # Calculate histograms
        actual_hist, _ = np.histogram(actual_exit_years, bins=year_bins)
        expected_hist, _ = np.histogram(expected_exit_years, bins=year_bins)

        # Create comparison chart
        exit_timing_comparison_chart = []
        for i in range(len(actual_hist)):
            exit_timing_comparison_chart.append({
                "bin_min": float(year_bins[i]),
                "bin_max": float(year_bins[i+1]),
                "bin_center": float((year_bins[i] + year_bins[i+1]) / 2),
                "actual_count": int(actual_hist[i]),
                "expected_count": int(expected_hist[i]),
                "difference": int(actual_hist[i] - expected_hist[i]),
            })

        comparative_visualizations["exit_timing_comparison_chart"] = exit_timing_comparison_chart

    # Add comparative visualizations to enhanced visualization
    enhanced_visualization["comparative_visualizations"] = comparative_visualizations

    return enhanced_visualization


async def get_enhanced_exit_summary(context: SimulationContext) -> Dict[str, Any]:
    """
    Get a summary of the enhanced exit simulation results.

    Args:
        context: Simulation context

    Returns:
        Dictionary containing enhanced exit summary
    """
    start_time = time.time()
    logger.info("Getting enhanced exit summary")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="enhanced_exit_simulator",
            progress=0.0,
            message="Generating enhanced exit summary",
        )

        # Get enhanced exits
        enhanced_exits = getattr(context, "enhanced_exits", [])

        # Get enhanced exit statistics
        enhanced_exit_stats = getattr(context, "enhanced_exit_stats", {})

        # Get enhanced exit visualization
        enhanced_exit_visualization = getattr(context, "enhanced_exit_visualization", {})

        # Generate summary
        summary = {
            "exits": enhanced_exits,
            "statistics": enhanced_exit_stats,
            "visualization": enhanced_exit_visualization,
        }

        # Add comparison to base exits if available
        if hasattr(context, "exits") and hasattr(context, "exit_stats") and hasattr(context, "exit_visualization"):
            summary["base_summary"] = {
                "exits": context.exits,
                "statistics": context.exit_stats,
                "visualization": context.exit_visualization,
            }

        # Add economic scenario if available
        if hasattr(context, "economic_scenario"):
            summary["economic_scenario"] = context.economic_scenario

        # Add behavioral adjustments if available
        if hasattr(context, "behavioral_exit_adjustments"):
            summary["behavioral_adjustments"] = context.behavioral_exit_adjustments

        # Add economic adjustments if available
        if hasattr(context, "economic_exit_adjustments"):
            summary["economic_adjustments"] = context.economic_exit_adjustments

        # Add machine learning insights if available
        ml_insights = {}

        # Add feature importances
        if hasattr(context, "exit_timing_feature_importances"):
            ml_insights["exit_timing_feature_importances"] = context.exit_timing_feature_importances

        if hasattr(context, "exit_type_feature_importances"):
            ml_insights["exit_type_feature_importances"] = context.exit_type_feature_importances

        if hasattr(context, "roi_feature_importances"):
            ml_insights["roi_feature_importances"] = context.roi_feature_importances

        # Add important features
        if hasattr(context, "exit_timing_important_features"):
            ml_insights["exit_timing_important_features"] = context.exit_timing_important_features

        if hasattr(context, "exit_type_important_features"):
            ml_insights["exit_type_important_features"] = context.exit_type_important_features

        if hasattr(context, "roi_important_features"):
            ml_insights["roi_important_features"] = context.roi_important_features

        # Add cluster information
        if hasattr(context, "exit_clusters"):
            ml_insights["exit_clusters"] = context.exit_clusters

        # Add ML insights to summary
        if ml_insights:
            summary["ml_insights"] = ml_insights

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="enhanced_exit_simulator",
            progress=100.0,
            message="Enhanced exit summary generated",
            data=summary,
        )

        # Update metrics
        increment_counter("enhanced_exit_summary_generated_total")
        observe_histogram(
            "enhanced_exit_summary_generation_runtime_seconds",
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
                "module": "enhanced_exit_simulator",
            },
        )

        # Re-raise exception
        raise