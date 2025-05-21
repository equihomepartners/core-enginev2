"""
Enhanced price path simulator module for the EQU IHOME SIM ENGINE v2.

This module provides an enhanced version of the price path simulator that integrates
more deeply with the TLS module to generate realistic price paths based on suburb-specific
data, economic factors, and market cycles.
"""

import time
from typing import Dict, Any, List, Optional, Tuple, Union, Callable

import numpy as np
import structlog
from scipy import stats
from scipy.linalg import cholesky

from src.engine.simulation_context import SimulationContext
from src.monte_carlo.rng_factory import get_rng
from src.api.websocket_manager import get_websocket_manager
from src.utils.error_handler import handle_exception, log_error
from src.utils.metrics import increment_counter, observe_histogram, set_gauge
from src.tls_module.tls_core import MetricCategory, SuburbData, PropertyAttributes
from src.tls_module import get_tls_manager

logger = structlog.get_logger(__name__)


def simulate_gbm(
    base_rate: float,
    volatility: float,
    num_steps: int,
    dt: float,
    random_shocks: Optional[np.ndarray] = None,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """
    Simulate a price path using Geometric Brownian Motion.

    Args:
        base_rate: Base appreciation rate (annual)
        volatility: Volatility (annual standard deviation)
        num_steps: Number of time steps
        dt: Time step size (in years)
        random_shocks: Pre-generated random shocks (for correlation)
        rng: Random number generator

    Returns:
        Array of price indices (starting at 1.0)
    """
    # Convert annual parameters to time step parameters
    mu = base_rate * dt
    sigma = volatility * np.sqrt(dt)

    # Generate random shocks if not provided
    if random_shocks is None:
        if rng is None:
            rng = np.random.default_rng()
        random_shocks = rng.normal(0, 1, num_steps)

    # Calculate returns
    returns = mu + sigma * random_shocks

    # Calculate cumulative returns
    price_path = np.cumprod(1 + returns)

    # Insert initial value (1.0)
    price_path = np.insert(price_path, 0, 1.0)

    return price_path


def simulate_mean_reversion(
    base_rate: float,
    volatility: float,
    speed: float,
    long_term_mean: float,
    num_steps: int,
    dt: float,
    random_shocks: Optional[np.ndarray] = None,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """
    Simulate a price path using a mean-reverting model (Ornstein-Uhlenbeck process).

    Args:
        base_rate: Initial rate (annual)
        volatility: Volatility (annual standard deviation)
        speed: Mean reversion speed
        long_term_mean: Long-term mean rate
        num_steps: Number of time steps
        dt: Time step size (in years)
        random_shocks: Pre-generated random shocks (for correlation)
        rng: Random number generator

    Returns:
        Array of price indices (starting at 1.0)
    """
    # Convert annual parameters to time step parameters
    sigma = volatility * np.sqrt(dt)

    # Generate random shocks if not provided
    if random_shocks is None:
        if rng is None:
            rng = np.random.default_rng()
        random_shocks = rng.normal(0, 1, num_steps)

    # Initialize arrays
    rates = np.zeros(num_steps + 1)
    returns = np.zeros(num_steps)

    # Set initial rate
    rates[0] = base_rate

    # Simulate mean-reverting process
    for t in range(num_steps):
        # Calculate mean reversion
        drift = speed * (long_term_mean - rates[t]) * dt

        # Calculate diffusion
        diffusion = sigma * random_shocks[t]

        # Update rate
        rates[t+1] = rates[t] + drift + diffusion

        # Calculate return
        returns[t] = rates[t] * dt

    # Calculate cumulative returns
    price_path = np.cumprod(1 + returns)

    # Insert initial value (1.0)
    price_path = np.insert(price_path, 0, 1.0)

    return price_path


def simulate_regime_switching(
    bull_rate: float,
    bear_rate: float,
    bull_volatility: float,
    bear_volatility: float,
    bull_to_bear_prob: float,
    bear_to_bull_prob: float,
    num_steps: int,
    dt: float,
    random_shocks: Optional[np.ndarray] = None,
    rng: Optional[np.random.Generator] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulate a price path using a regime-switching model.

    Args:
        bull_rate: Appreciation rate in bull market (annual)
        bear_rate: Appreciation rate in bear market (annual)
        bull_volatility: Volatility in bull market (annual standard deviation)
        bear_volatility: Volatility in bear market (annual standard deviation)
        bull_to_bear_prob: Probability of switching from bull to bear
        bear_to_bull_prob: Probability of switching from bear to bull
        num_steps: Number of time steps
        dt: Time step size (in years)
        random_shocks: Pre-generated random shocks (for correlation)
        rng: Random number generator

    Returns:
        Tuple of (price path, regimes)
    """
    # Convert annual parameters to time step parameters
    bull_mu = bull_rate * dt
    bear_mu = bear_rate * dt
    bull_sigma = bull_volatility * np.sqrt(dt)
    bear_sigma = bear_volatility * np.sqrt(dt)

    # Convert annual transition probabilities to time step probabilities
    bull_to_bear = 1 - (1 - bull_to_bear_prob) ** dt
    bear_to_bull = 1 - (1 - bear_to_bull_prob) ** dt

    # Generate random shocks if not provided
    if random_shocks is None:
        if rng is None:
            rng = np.random.default_rng()
        random_shocks = rng.normal(0, 1, num_steps)

    # Generate regime transitions
    if rng is None:
        rng = np.random.default_rng()
    regime_transitions = rng.random(num_steps)

    # Initialize arrays
    regimes = np.zeros(num_steps + 1, dtype=int)  # 0 = bull, 1 = bear
    returns = np.zeros(num_steps)

    # Set initial regime (start in bull market)
    regimes[0] = 0

    # Simulate regime-switching process
    for t in range(num_steps):
        # Get current regime
        current_regime = regimes[t]

        # Determine next regime
        if current_regime == 0:  # Bull market
            if regime_transitions[t] < bull_to_bear:
                regimes[t+1] = 1  # Switch to bear
            else:
                regimes[t+1] = 0  # Stay in bull
        else:  # Bear market
            if regime_transitions[t] < bear_to_bull:
                regimes[t+1] = 0  # Switch to bull
            else:
                regimes[t+1] = 1  # Stay in bear

        # Calculate return based on current regime
        if current_regime == 0:  # Bull market
            returns[t] = bull_mu + bull_sigma * random_shocks[t]
        else:  # Bear market
            returns[t] = bear_mu + bear_sigma * random_shocks[t]

    # Calculate cumulative returns
    price_path = np.cumprod(1 + returns)

    # Insert initial value (1.0)
    price_path = np.insert(price_path, 0, 1.0)

    return price_path, regimes

# Constants for Sydney property market cycles
SYDNEY_CYCLE_PERIOD_YEARS = 7.0  # Average property cycle length in Sydney
SYDNEY_CYCLE_AMPLITUDE = 0.15  # Amplitude of the cycle (peak-to-trough difference)
SYDNEY_LONG_TERM_GROWTH = 0.045  # Long-term annual growth rate for Sydney

# Economic factor impact coefficients
INTEREST_RATE_IMPACT = -2.0  # Impact of 1% interest rate change on appreciation
EMPLOYMENT_IMPACT = 1.5  # Impact of 1% employment change on appreciation
POPULATION_GROWTH_IMPACT = 2.0  # Impact of 1% population growth on appreciation
INCOME_GROWTH_IMPACT = 1.0  # Impact of 1% income growth on appreciation
SUPPLY_DEMAND_IMPACT = 1.2  # Impact of supply/demand ratio on appreciation

# Property type appreciation modifiers
PROPERTY_TYPE_MODIFIERS = {
    "house": 1.0,
    "apartment": 0.8,
    "townhouse": 0.9,
    "duplex": 0.95,
    "villa": 0.85,
    "land": 1.1,
}

# Property characteristic appreciation modifiers
BEDROOM_MODIFIER = 0.02  # Per bedroom above/below suburb average
BATHROOM_MODIFIER = 0.01  # Per bathroom above/below suburb average
LAND_SIZE_MODIFIER = 0.0001  # Per square meter above/below suburb average
AGE_MODIFIER = -0.002  # Per year of age (negative impact)


async def simulate_enhanced_price_paths(context: SimulationContext) -> None:
    """
    Simulate enhanced price paths using TLS data for more realistic modeling.

    This function generates price paths that are calibrated based on suburb-specific
    data from the TLS module, including economic factors, property characteristics,
    and market cycles specific to the Sydney property market.

    Args:
        context: Simulation context

    Raises:
        ValueError: If the configuration parameters are invalid
    """
    start_time = time.time()
    logger.info("Simulating enhanced price paths")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=0.0,
            message="Starting enhanced price path simulation",
        )

        # Get configuration parameters
        config = context.config

        # Get random number generator
        if context.rng is None:
            context.rng = get_rng("price_path", 0)

        # Get price path configuration
        price_path_config = getattr(config, "price_path", {})

        # Get model type
        model_type = getattr(price_path_config, "model_type", "gbm")

        # Get time step
        time_step = getattr(price_path_config, "time_step", "monthly")

        # Get fund term
        fund_term = config.fund_term

        # Get number of time steps
        if time_step == "monthly":
            num_steps = fund_term * 12
            dt = 1.0 / 12.0
        elif time_step == "quarterly":
            num_steps = fund_term * 4
            dt = 1.0 / 4.0
        else:  # yearly
            num_steps = fund_term
            dt = 1.0

        # Get cycle position
        cycle_position = getattr(price_path_config, "cycle_position", 0.5)

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=10.0,
            message="Preparing enhanced price path simulation",
            data={
                "model_type": model_type,
                "time_step": time_step,
                "num_steps": num_steps,
                "fund_term": fund_term,
                "cycle_position": cycle_position,
            },
        )

        # Send informational message
        await websocket_manager.send_info(
            simulation_id=context.run_id,
            message="Loading TLS data for enhanced price paths",
        )

        # Get TLS manager
        tls_manager = get_tls_manager()

        # Load TLS data if not already loaded
        if not tls_manager.is_data_loaded:
            await tls_manager.load_data(simulation_id=context.run_id)

        # Get suburbs from TLS manager
        suburbs = tls_manager.suburbs

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=20.0,
            message="Loaded TLS data",
            data={
                "num_suburbs": len(suburbs),
            },
        )

        # Generate zone-level price paths
        zone_price_paths = await generate_zone_price_paths(
            context=context,
            tls_manager=tls_manager,
            model_type=model_type,
            num_steps=num_steps,
            dt=dt,
            cycle_position=cycle_position,
            websocket_manager=websocket_manager,
        )

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=40.0,
            message="Generated zone-level price paths",
            data={
                "num_zones": len(zone_price_paths),
            },
        )

        # Generate suburb-level price paths
        suburb_price_paths = await generate_suburb_price_paths(
            context=context,
            tls_manager=tls_manager,
            zone_price_paths=zone_price_paths,
            num_steps=num_steps,
            dt=dt,
            websocket_manager=websocket_manager,
        )

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=60.0,
            message="Generated suburb-level price paths",
            data={
                "num_suburbs": len(suburb_price_paths),
            },
        )

        # Generate property-level price paths
        property_price_paths = await generate_property_price_paths(
            context=context,
            tls_manager=tls_manager,
            suburb_price_paths=suburb_price_paths,
            num_steps=num_steps,
            dt=dt,
            websocket_manager=websocket_manager,
        )

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=80.0,
            message="Generated property-level price paths",
            data={
                "num_properties": len(property_price_paths),
            },
        )

        # Store price paths in context
        context.price_paths = {
            "zone_price_paths": zone_price_paths,
            "suburb_price_paths": suburb_price_paths,
            "property_price_paths": property_price_paths,
        }

        # Calculate price path statistics
        price_path_stats = calculate_enhanced_price_path_statistics(
            zone_price_paths=zone_price_paths,
            suburb_price_paths=suburb_price_paths,
            dt=dt,
            tls_manager=tls_manager,
        )

        # Store statistics in context
        context.price_path_stats = price_path_stats

        # Generate visualization data
        price_path_visualization = generate_enhanced_price_path_visualization(
            zone_price_paths=zone_price_paths,
            suburb_price_paths=suburb_price_paths,
            property_price_paths=property_price_paths,
            price_path_stats=price_path_stats,
            time_step=time_step,
            market_regimes=getattr(context, "market_regimes", None),
            tls_manager=tls_manager,
        )

        # Store visualization data in context
        context.price_path_visualization = price_path_visualization

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=100.0,
            message="Enhanced price path simulation completed",
            data={
                "num_zones": len(zone_price_paths),
                "num_suburbs": len(suburb_price_paths),
                "num_properties": len(property_price_paths),
            },
        )

        # Update metrics
        increment_counter("enhanced_price_path_simulations_completed_total")
        observe_histogram(
            "enhanced_price_path_simulation_runtime_seconds",
            time.time() - start_time,
        )

        # Log completion
        logger.info(
            "Enhanced price path simulation completed",
            zones=list(zone_price_paths.keys()),
            num_suburbs=len(suburb_price_paths),
            num_properties=len(property_price_paths),
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
                "module": "price_path",
            },
        )

        # Update metrics
        increment_counter("enhanced_price_path_simulations_failed_total")

        # Re-raise exception
        raise


async def generate_zone_price_paths(
    context: SimulationContext,
    tls_manager: Any,
    model_type: str,
    num_steps: int,
    dt: float,
    cycle_position: float,
    websocket_manager: Any,
) -> Dict[str, np.ndarray]:
    """
    Generate zone-level price paths using TLS data.

    Args:
        context: Simulation context
        tls_manager: TLS data manager
        model_type: Type of stochastic model to use
        num_steps: Number of time steps
        dt: Time step size (in years)
        cycle_position: Initial position in the property cycle (0-1)
        websocket_manager: WebSocket manager for progress reporting

    Returns:
        Dictionary of price paths by zone
    """
    logger.info("Generating zone-level price paths")

    # Get configuration parameters
    config = context.config

    # Get zone-specific appreciation rates
    appreciation_rates = getattr(config, "appreciation_rates", {})
    if not appreciation_rates:
        appreciation_rates = {
            "green": 0.05,
            "orange": 0.03,
            "red": 0.01
        }

    # Get volatility parameters
    price_path_config = getattr(config, "price_path", {})
    volatility = getattr(price_path_config, "volatility", {})
    if not volatility:
        volatility = {
            "green": 0.03,
            "orange": 0.05,
            "red": 0.08
        }

    # Get correlation matrix
    correlation_matrix = getattr(price_path_config, "correlation_matrix", {})
    if not correlation_matrix:
        correlation_matrix = {
            "green_orange": 0.7,
            "green_red": 0.5,
            "orange_red": 0.8
        }

    # Calculate zone-specific parameters based on TLS data
    zones = ["green", "orange", "red"]
    zone_params = {}

    for zone in zones:
        # Get suburbs in this zone
        zone_suburbs = [s for s in tls_manager.suburbs.values() if getattr(s, "zone_category", None) == zone]

        if not zone_suburbs:
            # Use default parameters if no suburbs in this zone
            zone_params[zone] = {
                "appreciation_rate": getattr(appreciation_rates, zone, 0.03),
                "volatility": getattr(volatility, zone, 0.05),
                "economic_factor": 1.0,
                "supply_demand_factor": 1.0,
                "population_growth": 0.01,
                "income_growth": 0.02,
            }
            continue

        # Calculate average appreciation score
        avg_appreciation_score = np.mean([s.appreciation_score for s in zone_suburbs]) / 100.0

        # Calculate average risk score (inverse relationship with volatility)
        avg_risk_score = 1.0 - np.mean([s.risk_score for s in zone_suburbs]) / 100.0

        # Get economic metrics
        economic_metrics = []
        for suburb in zone_suburbs:
            for metric_name, metric_value in suburb.metrics.items():
                metric = tls_manager.metrics.get(metric_name)
                if metric and metric.category == MetricCategory.ECONOMIC:
                    economic_metrics.append(metric_value.value)

        economic_factor = 1.0
        if economic_metrics:
            economic_factor = np.mean(economic_metrics)

        # Get supply/demand metrics
        supply_demand_metrics = []
        for suburb in zone_suburbs:
            for metric_name, metric_value in suburb.metrics.items():
                metric = tls_manager.metrics.get(metric_name)
                if metric and metric.category == MetricCategory.SUPPLY_DEMAND:
                    supply_demand_metrics.append(metric_value.value)

        supply_demand_factor = 1.0
        if supply_demand_metrics:
            supply_demand_factor = np.mean(supply_demand_metrics)

        # Calculate population growth
        population_growth = 0.01  # Default
        for suburb in zone_suburbs:
            for metric_name, metric_value in suburb.metrics.items():
                if metric_name == "population_growth":
                    population_growth = metric_value.value
                    break

        # Calculate income growth
        income_growth = 0.02  # Default
        for suburb in zone_suburbs:
            for metric_name, metric_value in suburb.metrics.items():
                if metric_name == "income_growth":
                    income_growth = metric_value.value
                    break

        # Calculate adjusted appreciation rate
        base_rate = getattr(appreciation_rates, zone, 0.03)
        adjusted_rate = base_rate * (0.5 + 0.5 * avg_appreciation_score) * economic_factor * supply_demand_factor

        # Calculate adjusted volatility
        base_volatility = getattr(volatility, zone, 0.05)
        adjusted_volatility = base_volatility * (0.5 + 0.5 * avg_risk_score)

        # Store parameters
        zone_params[zone] = {
            "appreciation_rate": adjusted_rate,
            "volatility": adjusted_volatility,
            "economic_factor": economic_factor,
            "supply_demand_factor": supply_demand_factor,
            "population_growth": population_growth,
            "income_growth": income_growth,
        }

    # Generate correlated random variables for zones
    corr_matrix = np.array([
        [1.0, correlation_matrix.get("green_orange", 0.7), correlation_matrix.get("green_red", 0.5)],
        [correlation_matrix.get("green_orange", 0.7), 1.0, correlation_matrix.get("orange_red", 0.8)],
        [correlation_matrix.get("green_red", 0.5), correlation_matrix.get("orange_red", 0.8), 1.0]
    ])

    # Ensure correlation matrix is positive definite
    min_eig = np.min(np.linalg.eigvals(corr_matrix))
    if min_eig < 0:
        # Add a small value to the diagonal to make it positive definite
        corr_matrix += np.eye(len(corr_matrix)) * (abs(min_eig) + 1e-6)

    # Generate correlated random variables
    try:
        L = cholesky(corr_matrix, lower=True)
    except np.linalg.LinAlgError:
        # If Cholesky decomposition fails, use a diagonal matrix
        logger.warning("Cholesky decomposition failed, using diagonal matrix")
        L = np.eye(len(corr_matrix))

    # Generate uncorrelated random variables
    uncorrelated_rvs = np.random.default_rng(context.rng.bit_generator).normal(0, 1, size=(len(zones), num_steps))

    # Apply correlation
    correlated_rvs = L @ uncorrelated_rvs

    # Simulate price paths for each zone
    zone_price_paths = {}
    for i, zone in enumerate(zones):
        # Get zone-specific parameters
        params = zone_params[zone]
        base_rate = params["appreciation_rate"]
        vol = params["volatility"]

        # Simulate price path based on model type
        if model_type == "gbm":
            price_path = simulate_gbm(
                base_rate=base_rate,
                volatility=vol,
                num_steps=num_steps,
                dt=dt,
                random_shocks=correlated_rvs[i],
            )
        elif model_type == "mean_reversion":
            # Get mean reversion parameters
            mean_reversion_params = getattr(price_path_config, "mean_reversion_params", {})
            speed = getattr(mean_reversion_params, "speed", 0.2)
            long_term_mean = getattr(mean_reversion_params, "long_term_mean", 0.03)

            price_path = simulate_mean_reversion(
                base_rate=base_rate,
                volatility=vol,
                speed=speed,
                long_term_mean=long_term_mean,
                num_steps=num_steps,
                dt=dt,
                random_shocks=correlated_rvs[i],
            )
        elif model_type == "regime_switching":
            # Get regime switching parameters
            regime_params = getattr(price_path_config, "regime_switching_params", {})
            bull_rate = getattr(regime_params, "bull_market_rate", 0.08)
            bear_rate = getattr(regime_params, "bear_market_rate", -0.03)
            bull_to_bear = getattr(regime_params, "bull_to_bear_prob", 0.1)
            bear_to_bull = getattr(regime_params, "bear_to_bull_prob", 0.3)

            price_path, regimes = simulate_regime_switching(
                bull_rate=bull_rate * params["economic_factor"],
                bear_rate=bear_rate * params["economic_factor"],
                bull_volatility=vol * 0.8,
                bear_volatility=vol * 1.5,
                bull_to_bear_prob=bull_to_bear,
                bear_to_bull_prob=bear_to_bull,
                num_steps=num_steps,
                dt=dt,
                random_shocks=correlated_rvs[i],
                rng=context.rng,
            )

            # Store regimes for visualization
            if zone == "green":  # Only store once
                context.market_regimes = regimes
        elif model_type == "sydney_cycle":
            # Simulate Sydney-specific property cycle
            price_path, cycle_positions = simulate_sydney_cycle(
                base_rate=base_rate,
                volatility=vol,
                num_steps=num_steps,
                dt=dt,
                cycle_position=cycle_position,
                economic_factor=params["economic_factor"],
                supply_demand_factor=params["supply_demand_factor"],
                population_growth=params["population_growth"],
                income_growth=params["income_growth"],
                random_shocks=correlated_rvs[i],
                rng=context.rng,
            )

            # Store cycle positions for visualization
            if zone == "green":  # Only store once
                context.cycle_positions = cycle_positions
        else:
            # Default to GBM
            price_path = simulate_gbm(
                base_rate=base_rate,
                volatility=vol,
                num_steps=num_steps,
                dt=dt,
                random_shocks=correlated_rvs[i],
            )

        # Store price path
        zone_price_paths[zone] = price_path

        # Report progress
        await websocket_manager.send_info(
            simulation_id=context.run_id,
            message=f"Generated price path for {zone} zone",
            data={
                "zone": zone,
                "appreciation_rate": base_rate,
                "volatility": vol,
                "economic_factor": params["economic_factor"],
                "supply_demand_factor": params["supply_demand_factor"],
            },
        )

    return zone_price_paths


def simulate_sydney_cycle(
    base_rate: float,
    volatility: float,
    num_steps: int,
    dt: float,
    cycle_position: float,
    economic_factor: float,
    supply_demand_factor: float,
    population_growth: float,
    income_growth: float,
    random_shocks: Optional[np.ndarray] = None,
    rng: Optional[np.random.Generator] = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulate a price path using a Sydney-specific property cycle model.

    Args:
        base_rate: Base appreciation rate (annual)
        volatility: Volatility (annual standard deviation)
        num_steps: Number of time steps
        dt: Time step size (in years)
        cycle_position: Initial position in the property cycle (0-1)
        economic_factor: Economic factor multiplier
        supply_demand_factor: Supply/demand factor multiplier
        population_growth: Population growth rate
        income_growth: Income growth rate
        random_shocks: Pre-generated random shocks (for correlation)
        rng: Random number generator

    Returns:
        Tuple of (price path, cycle positions)
    """
    # Convert annual parameters to time step parameters
    mu = base_rate * dt
    sigma = volatility * np.sqrt(dt)

    # Generate random shocks if not provided
    if random_shocks is None:
        if rng is None:
            rng = np.random.default_rng()
        random_shocks = rng.normal(0, 1, num_steps)

    # Initialize arrays
    returns = np.zeros(num_steps)
    cycle_positions = np.zeros(num_steps + 1)

    # Set initial cycle position
    cycle_positions[0] = cycle_position

    # Calculate cycle parameters
    cycle_period_steps = int(SYDNEY_CYCLE_PERIOD_YEARS / dt)
    cycle_amplitude = SYDNEY_CYCLE_AMPLITUDE

    # Calculate economic impact
    economic_impact = (economic_factor - 1.0) * 0.02

    # Calculate supply/demand impact
    supply_demand_impact = (supply_demand_factor - 1.0) * SUPPLY_DEMAND_IMPACT * dt

    # Calculate population growth impact
    population_impact = population_growth * POPULATION_GROWTH_IMPACT * dt

    # Calculate income growth impact
    income_impact = income_growth * INCOME_GROWTH_IMPACT * dt

    # Simulate cycle
    for t in range(num_steps):
        # Update cycle position
        cycle_positions[t+1] = (cycle_positions[t] + dt / SYDNEY_CYCLE_PERIOD_YEARS) % 1.0

        # Calculate cycle effect (sinusoidal)
        cycle_effect = cycle_amplitude * np.sin(2 * np.pi * cycle_positions[t])

        # Calculate combined effect
        combined_effect = (
            mu +  # Base rate
            cycle_effect * dt +  # Cycle effect
            economic_impact +  # Economic impact
            supply_demand_impact +  # Supply/demand impact
            population_impact +  # Population growth impact
            income_impact +  # Income growth impact
            sigma * random_shocks[t]  # Random shock
        )

        # Calculate return
        returns[t] = combined_effect

    # Calculate cumulative returns
    price_path = np.cumprod(1 + returns)

    # Insert initial value (1.0)
    price_path = np.insert(price_path, 0, 1.0)

    return price_path, cycle_positions


async def generate_suburb_price_paths(
    context: SimulationContext,
    tls_manager: Any,
    zone_price_paths: Dict[str, np.ndarray],
    num_steps: int,
    dt: float,
    websocket_manager: Any,
) -> Dict[str, np.ndarray]:
    """
    Generate suburb-level price paths using TLS data.

    Args:
        context: Simulation context
        tls_manager: TLS data manager
        zone_price_paths: Dictionary of zone-level price paths
        num_steps: Number of time steps
        dt: Time step size (in years)
        websocket_manager: WebSocket manager for progress reporting

    Returns:
        Dictionary of price paths by suburb
    """
    logger.info("Generating suburb-level price paths")

    # Get configuration parameters
    config = context.config

    # Get price path configuration
    price_path_config = getattr(config, "price_path", {})

    # Get suburb variation parameter
    suburb_variation = getattr(price_path_config, "suburb_variation", 0.02)

    # Initialize suburb price paths
    suburb_price_paths = {}

    # Get all suburbs
    suburbs = tls_manager.suburbs

    # Process each suburb
    for i, (suburb_id, suburb) in enumerate(suburbs.items()):
        # Get zone for this suburb
        zone = getattr(suburb, "zone_category", "green")

        # Get zone price path
        zone_path = zone_price_paths.get(zone, zone_price_paths.get("green", None))
        if zone_path is None:
            continue

        # Calculate suburb-specific factors

        # Appreciation score factor (0.8-1.2)
        appreciation_factor = 0.8 + (suburb.appreciation_score / 100.0) * 0.4

        # Risk score factor (0.8-1.2 for volatility)
        risk_factor = 0.8 + (suburb.risk_score / 100.0) * 0.4

        # Liquidity score factor (0.9-1.1)
        liquidity_factor = 0.9 + (suburb.liquidity_score / 100.0) * 0.2

        # Get suburb-specific metrics
        school_quality = 0.5  # Default
        crime_rate = 0.5  # Default
        transport_access = 0.5  # Default
        employment_growth = 0.01  # Default

        for metric_name, metric_value in suburb.metrics.items():
            if metric_name == "school_quality":
                school_quality = metric_value.value
            elif metric_name == "crime_rate":
                crime_rate = metric_value.value
            elif metric_name == "transport_access":
                transport_access = metric_value.value
            elif metric_name == "employment_growth":
                employment_growth = metric_value.value

        # Calculate location quality factor (0.9-1.1)
        location_factor = 0.9 + (school_quality * 0.3 + (1 - crime_rate) * 0.3 + transport_access * 0.4) * 0.2

        # Calculate employment factor (0.95-1.05)
        employment_factor = 0.95 + employment_growth * 5.0

        # Calculate combined factor
        combined_factor = appreciation_factor * location_factor * employment_factor

        # Generate suburb-specific variation
        suburb_rng = get_rng(f"price_path_suburb_{suburb_id}", 0)

        # Base variation on risk factor
        suburb_volatility = suburb_variation * risk_factor

        # Generate random shocks
        suburb_shocks = suburb_rng.normal(0, suburb_volatility, size=num_steps)

        # Apply variation to zone path
        suburb_path = zone_path.copy()

        # Apply combined factor to overall growth
        suburb_path = 1.0 + (suburb_path - 1.0) * combined_factor

        # Apply random shocks
        for t in range(1, len(suburb_path)):
            # Apply multiplicative shock
            suburb_path[t] *= (1.0 + suburb_shocks[t-1])

        # Store suburb price path
        suburb_price_paths[suburb_id] = suburb_path

        # Report progress periodically
        if i % 10 == 0:
            await websocket_manager.send_progress(
                simulation_id=context.run_id,
                module="price_path",
                progress=40.0 + (i / len(suburbs)) * 20.0,
                message=f"Generated price path for suburb {suburb_id}",
                data={
                    "suburb_id": suburb_id,
                    "suburb_name": suburb.name,
                    "zone": zone,
                    "appreciation_factor": appreciation_factor,
                    "risk_factor": risk_factor,
                    "location_factor": location_factor,
                },
            )

    return suburb_price_paths


async def generate_property_price_paths(
    context: SimulationContext,
    tls_manager: Any,
    suburb_price_paths: Dict[str, np.ndarray],
    num_steps: int,
    dt: float,
    websocket_manager: Any,
) -> Dict[str, np.ndarray]:
    """
    Generate property-level price paths using TLS data.

    Args:
        context: Simulation context
        tls_manager: TLS data manager
        suburb_price_paths: Dictionary of suburb-level price paths
        num_steps: Number of time steps
        dt: Time step size (in years)
        websocket_manager: WebSocket manager for progress reporting

    Returns:
        Dictionary of price paths by property
    """
    logger.info("Generating property-level price paths")

    # Get configuration parameters
    config = context.config

    # Get price path configuration
    price_path_config = getattr(config, "price_path", {})

    # Get property variation parameter
    property_variation = getattr(price_path_config, "property_variation", 0.01)

    # Initialize property price paths
    property_price_paths = {}

    # Get loans
    loans = context.loans

    # Process each loan
    for i, loan in enumerate(loans):
        property_id = loan.get("property_id", "")
        suburb_id = loan.get("suburb_id", "")
        zone = loan.get("zone", "green")

        # Skip if property ID is missing
        if not property_id:
            continue

        # Get suburb price path or fall back to zone price path
        if suburb_id in suburb_price_paths:
            base_path = suburb_price_paths[suburb_id]
        else:
            # Try to get zone price path from context
            zone_price_paths = getattr(context, "price_paths", {}).get("zone_price_paths", {})
            base_path = zone_price_paths.get(zone, None)

            if base_path is None:
                logger.warning(
                    "No price path found for property",
                    property_id=property_id,
                    suburb_id=suburb_id,
                    zone=zone,
                )
                continue

        # Get property attributes
        property_type = loan.get("property_type", "house")
        bedrooms = loan.get("bedrooms", 3)
        bathrooms = loan.get("bathrooms", 2)
        land_size = loan.get("land_size", 500.0)
        building_size = loan.get("building_size", 200.0)
        year_built = loan.get("year_built", 2000)

        # Calculate property-specific factors

        # Property type factor
        type_factor = PROPERTY_TYPE_MODIFIERS.get(property_type.lower(), 1.0)

        # Get suburb average values
        suburb = tls_manager.suburbs.get(suburb_id)
        if suburb:
            # Calculate average values for this suburb
            avg_bedrooms = 3.0  # Default
            avg_bathrooms = 2.0  # Default
            avg_land_size = 500.0  # Default

            # Calculate averages from properties in this suburb
            if suburb.properties:
                bedroom_values = [p.bedrooms for p in suburb.properties.values()]
                bathroom_values = [p.bathrooms for p in suburb.properties.values()]
                land_size_values = [p.land_size for p in suburb.properties.values()]

                if bedroom_values:
                    avg_bedrooms = np.mean(bedroom_values)
                if bathroom_values:
                    avg_bathrooms = np.mean(bathroom_values)
                if land_size_values:
                    avg_land_size = np.mean(land_size_values)

            # Calculate bedroom factor
            bedroom_factor = 1.0 + (bedrooms - avg_bedrooms) * BEDROOM_MODIFIER

            # Calculate bathroom factor
            bathroom_factor = 1.0 + (bathrooms - avg_bathrooms) * BATHROOM_MODIFIER

            # Calculate land size factor
            land_size_factor = 1.0 + (land_size - avg_land_size) * LAND_SIZE_MODIFIER

            # Calculate age factor
            current_year = 2023  # Default current year
            age = current_year - year_built
            age_factor = 1.0 + age * AGE_MODIFIER
        else:
            # Use default factors
            bedroom_factor = 1.0
            bathroom_factor = 1.0
            land_size_factor = 1.0
            age_factor = 1.0

        # Calculate combined factor
        combined_factor = type_factor * bedroom_factor * bathroom_factor * land_size_factor * age_factor

        # Generate property-specific variation
        property_rng = get_rng(f"price_path_property_{property_id}", 0)
        property_shocks = property_rng.normal(0, property_variation, size=num_steps)

        # Apply variation to base path
        property_path = base_path.copy()

        # Apply combined factor to overall growth
        property_path = 1.0 + (property_path - 1.0) * combined_factor

        # Apply random shocks
        for t in range(1, len(property_path)):
            # Apply multiplicative shock
            property_path[t] *= (1.0 + property_shocks[t-1])

        # Store property price path
        property_price_paths[property_id] = property_path

        # Report progress periodically
        if i % 100 == 0:
            await websocket_manager.send_progress(
                simulation_id=context.run_id,
                module="price_path",
                progress=60.0 + (i / len(loans)) * 20.0,
                message=f"Generated price path for property {property_id}",
                data={
                    "property_id": property_id,
                    "suburb_id": suburb_id,
                    "zone": zone,
                    "type_factor": type_factor,
                    "bedroom_factor": bedroom_factor,
                    "land_size_factor": land_size_factor,
                    "age_factor": age_factor,
                },
            )

    return property_price_paths


def calculate_enhanced_price_path_statistics(
    zone_price_paths: Dict[str, np.ndarray],
    suburb_price_paths: Dict[str, np.ndarray],
    dt: float,
    tls_manager: Any,
) -> Dict[str, Any]:
    """
    Calculate enhanced statistics for price paths.

    Args:
        zone_price_paths: Dictionary of price paths by zone
        suburb_price_paths: Dictionary of price paths by suburb
        dt: Time step size (in years)
        tls_manager: TLS data manager

    Returns:
        Dictionary containing price path statistics
    """
    # Calculate zone statistics
    zone_stats = {}
    for zone, price_path in zone_price_paths.items():
        # Calculate returns
        returns = np.diff(price_path) / price_path[:-1]

        # Calculate CAGR
        years = len(price_path) * dt
        cagr = (price_path[-1] / price_path[0]) ** (1 / years) - 1

        # Calculate volatility
        volatility = np.std(returns) / np.sqrt(dt)

        # Calculate maximum drawdown
        max_drawdown = calculate_max_drawdown(price_path)

        # Calculate Sharpe ratio
        risk_free_rate = 0.02  # Assume 2% risk-free rate
        sharpe_ratio = (cagr - risk_free_rate) / volatility if volatility > 0 else 0

        # Calculate final appreciation
        final_appreciation = price_path[-1] / price_path[0] - 1

        # Store statistics
        zone_stats[zone] = {
            "cagr": cagr,
            "volatility": volatility,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio,
            "final_appreciation": final_appreciation,
        }

    # Calculate suburb statistics
    suburb_stats = {}
    for suburb_id, price_path in suburb_price_paths.items():
        # Get suburb data
        suburb = tls_manager.suburbs.get(suburb_id)
        if not suburb:
            continue

        # Calculate returns
        returns = np.diff(price_path) / price_path[:-1]

        # Calculate CAGR
        years = len(price_path) * dt
        cagr = (price_path[-1] / price_path[0]) ** (1 / years) - 1

        # Calculate volatility
        volatility = np.std(returns) / np.sqrt(dt)

        # Calculate maximum drawdown
        max_drawdown = calculate_max_drawdown(price_path)

        # Calculate Sharpe ratio
        risk_free_rate = 0.02  # Assume 2% risk-free rate
        sharpe_ratio = (cagr - risk_free_rate) / volatility if volatility > 0 else 0

        # Calculate final appreciation
        final_appreciation = price_path[-1] / price_path[0] - 1

        # Store statistics
        suburb_stats[suburb_id] = {
            "name": suburb.name,
            "zone": getattr(suburb, "zone_category", "green"),
            "cagr": cagr,
            "volatility": volatility,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio,
            "final_appreciation": final_appreciation,
            "appreciation_score": suburb.appreciation_score,
            "risk_score": suburb.risk_score,
            "liquidity_score": suburb.liquidity_score,
        }

    # Calculate correlation matrix
    correlation_matrix = {}
    zones = list(zone_price_paths.keys())
    for i, zone1 in enumerate(zones):
        correlation_matrix[zone1] = {}
        for j, zone2 in enumerate(zones):
            # Calculate correlation of returns
            returns1 = np.diff(zone_price_paths[zone1]) / zone_price_paths[zone1][:-1]
            returns2 = np.diff(zone_price_paths[zone2]) / zone_price_paths[zone2][:-1]
            correlation = np.corrcoef(returns1, returns2)[0, 1]
            correlation_matrix[zone1][zone2] = correlation

    # Calculate suburb correlation matrix
    suburb_correlation_matrix = {}
    # Limit to top 20 suburbs by overall score to avoid excessive computation
    top_suburbs = sorted(
        tls_manager.suburbs.values(),
        key=lambda s: s.overall_score,
        reverse=True,
    )[:20]
    top_suburb_ids = [s.suburb_id for s in top_suburbs]

    for i, suburb_id1 in enumerate(top_suburb_ids):
        if suburb_id1 not in suburb_price_paths:
            continue

        suburb_correlation_matrix[suburb_id1] = {}
        for j, suburb_id2 in enumerate(top_suburb_ids):
            if suburb_id2 not in suburb_price_paths:
                continue

            # Calculate correlation of returns
            returns1 = np.diff(suburb_price_paths[suburb_id1]) / suburb_price_paths[suburb_id1][:-1]
            returns2 = np.diff(suburb_price_paths[suburb_id2]) / suburb_price_paths[suburb_id2][:-1]
            correlation = np.corrcoef(returns1, returns2)[0, 1]
            suburb_correlation_matrix[suburb_id1][suburb_id2] = correlation

    # Calculate zone performance ranking
    zone_ranking = sorted(
        [(zone, stats["sharpe_ratio"]) for zone, stats in zone_stats.items()],
        key=lambda x: x[1],
        reverse=True,
    )

    # Calculate suburb performance ranking
    suburb_ranking = sorted(
        [(suburb_id, stats["sharpe_ratio"]) for suburb_id, stats in suburb_stats.items()],
        key=lambda x: x[1],
        reverse=True,
    )

    return {
        "zone_stats": zone_stats,
        "suburb_stats": suburb_stats,
        "correlation_matrix": correlation_matrix,
        "suburb_correlation_matrix": suburb_correlation_matrix,
        "zone_ranking": zone_ranking,
        "suburb_ranking": suburb_ranking,
    }


def calculate_max_drawdown(price_path: np.ndarray) -> float:
    """
    Calculate the maximum drawdown of a price path.

    Args:
        price_path: Array of price indices

    Returns:
        Maximum drawdown (as a positive fraction)
    """
    # Calculate running maximum
    running_max = np.maximum.accumulate(price_path)

    # Calculate drawdown
    drawdown = (running_max - price_path) / running_max

    # Get maximum drawdown
    max_drawdown = np.max(drawdown)

    return max_drawdown


def generate_enhanced_price_path_visualization(
    zone_price_paths: Dict[str, np.ndarray],
    suburb_price_paths: Dict[str, np.ndarray],
    property_price_paths: Dict[str, np.ndarray],
    price_path_stats: Dict[str, Any],
    time_step: str,
    market_regimes: Optional[np.ndarray] = None,
    tls_manager: Any = None,
) -> Dict[str, Any]:
    """
    Generate enhanced visualization data for price paths.

    Args:
        zone_price_paths: Dictionary of price paths by zone
        suburb_price_paths: Dictionary of price paths by suburb
        property_price_paths: Dictionary of price paths by property
        price_path_stats: Dictionary of price path statistics
        time_step: Time step for price path simulation
        market_regimes: Array of market regimes (0 = bull, 1 = bear)
        tls_manager: TLS data manager

    Returns:
        Dictionary containing visualization data
    """
    # Determine time step in years
    if time_step == "monthly":
        dt = 1.0 / 12.0
    elif time_step == "quarterly":
        dt = 1.0 / 4.0
    else:  # yearly
        dt = 1.0

    # Generate zone price charts
    zone_price_charts = {}
    for zone, price_path in zone_price_paths.items():
        chart_data = []
        for t in range(len(price_path)):
            chart_data.append({
                "year": t * dt,
                "price_index": price_path[t],
            })
        zone_price_charts[zone] = chart_data

    # Generate zone comparison chart
    zone_comparison_chart = []
    max_length = max(len(path) for path in zone_price_paths.values())
    for t in range(max_length):
        data_point = {"year": t * dt}
        for zone, price_path in zone_price_paths.items():
            if t < len(price_path):
                data_point[zone] = price_path[t]
        zone_comparison_chart.append(data_point)

    # Generate suburb price charts (top 10 suburbs by overall score)
    suburb_price_charts = {}
    if tls_manager:
        top_suburbs = sorted(
            tls_manager.suburbs.values(),
            key=lambda s: s.overall_score,
            reverse=True,
        )[:10]
        top_suburb_ids = [s.suburb_id for s in top_suburbs]

        for suburb_id in top_suburb_ids:
            if suburb_id not in suburb_price_paths:
                continue

            price_path = suburb_price_paths[suburb_id]
            suburb_name = tls_manager.suburbs[suburb_id].name

            chart_data = []
            for t in range(len(price_path)):
                chart_data.append({
                    "year": t * dt,
                    "price_index": price_path[t],
                })
            suburb_price_charts[f"{suburb_id} - {suburb_name}"] = chart_data
    else:
        # If no TLS manager, just use the first 10 suburbs
        sample_suburbs = list(suburb_price_paths.keys())[:10]
        for suburb_id in sample_suburbs:
            price_path = suburb_price_paths[suburb_id]
            chart_data = []
            for t in range(len(price_path)):
                chart_data.append({
                    "year": t * dt,
                    "price_index": price_path[t],
                })
            suburb_price_charts[suburb_id] = chart_data

    # Generate correlation heatmap
    correlation_heatmap = []
    correlation_matrix = price_path_stats.get("correlation_matrix", {})
    for zone1, correlations in correlation_matrix.items():
        for zone2, correlation in correlations.items():
            correlation_heatmap.append({
                "zone1": zone1,
                "zone2": zone2,
                "correlation": correlation,
            })

    # Generate suburb correlation heatmap
    suburb_correlation_heatmap = []
    suburb_correlation_matrix = price_path_stats.get("suburb_correlation_matrix", {})
    for suburb_id1, correlations in suburb_correlation_matrix.items():
        suburb_name1 = tls_manager.suburbs[suburb_id1].name if tls_manager and suburb_id1 in tls_manager.suburbs else suburb_id1
        for suburb_id2, correlation in correlations.items():
            suburb_name2 = tls_manager.suburbs[suburb_id2].name if tls_manager and suburb_id2 in tls_manager.suburbs else suburb_id2
            suburb_correlation_heatmap.append({
                "suburb1": suburb_name1,
                "suburb2": suburb_name2,
                "correlation": correlation,
            })

    # Generate final distribution
    final_distribution = {}
    for zone, price_path in zone_price_paths.items():
        # Get final values for all properties in this zone
        final_values = []
        for property_id, prop_path in property_price_paths.items():
            # Skip if property path is empty
            if len(prop_path) == 0:
                continue

            # Get property zone
            property_zone = None
            for loan in property_price_paths:
                if loan.get("property_id") == property_id:
                    property_zone = loan.get("zone")
                    break

            # Skip if property is not in current zone
            if property_zone != zone:
                continue

            # Add final value
            final_values.append(prop_path[-1])

        # Skip if no properties in this zone
        if not final_values:
            continue

        # Generate histogram
        hist, bin_edges = np.histogram(final_values, bins=10)

        # Format bin ranges
        bin_ranges = [f"{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}" for i in range(len(bin_edges)-1)]

        # Create histogram data
        histogram_data = []
        for i in range(len(hist)):
            histogram_data.append({
                "bin": bin_ranges[i],
                "count": int(hist[i]),
            })

        final_distribution[zone] = histogram_data

    # Generate cycle position chart
    cycle_position_chart = []
    # Use the cycle positions passed from the simulation context
    if hasattr(SimulationContext, "cycle_positions"):
        cycle_positions = SimulationContext.cycle_positions
        if cycle_positions is not None:
            for t in range(len(cycle_positions)):
                cycle_position_chart.append({
                    "year": t * dt,
                    "cycle_position": cycle_positions[t],
                })

    # Generate regime chart
    regime_chart = []
    if market_regimes is not None:
        for t in range(len(market_regimes)):
            regime = "bull" if market_regimes[t] == 0 else "bear"

            regime_chart.append({
                "year": t * dt,
                "regime": regime,
            })

    # Generate zone performance chart
    zone_performance_chart = []
    zone_stats = price_path_stats.get("zone_stats", {})
    for zone, stats in zone_stats.items():
        zone_performance_chart.append({
            "zone": zone,
            "cagr": stats["cagr"],
            "volatility": stats["volatility"],
            "sharpe_ratio": stats["sharpe_ratio"],
            "max_drawdown": stats["max_drawdown"],
        })

    # Generate suburb performance chart (top 20)
    suburb_performance_chart = []
    suburb_ranking = price_path_stats.get("suburb_ranking", [])
    for i, (suburb_id, sharpe_ratio) in enumerate(suburb_ranking[:20]):
        if suburb_id not in price_path_stats.get("suburb_stats", {}):
            continue

        stats = price_path_stats["suburb_stats"][suburb_id]
        suburb_name = stats.get("name", suburb_id)

        suburb_performance_chart.append({
            "rank": i + 1,
            "suburb_id": suburb_id,
            "suburb_name": suburb_name,
            "zone": stats.get("zone", "unknown"),
            "cagr": stats["cagr"],
            "volatility": stats["volatility"],
            "sharpe_ratio": stats["sharpe_ratio"],
            "max_drawdown": stats["max_drawdown"],
            "appreciation_score": stats.get("appreciation_score", 0),
            "risk_score": stats.get("risk_score", 0),
        })

    # Generate zone allocation recommendation
    zone_allocation_recommendation = []
    zone_ranking = price_path_stats.get("zone_ranking", [])
    total_sharpe = sum(sharpe for _, sharpe in zone_ranking)

    if total_sharpe > 0:
        for zone, sharpe_ratio in zone_ranking:
            # Calculate allocation based on Sharpe ratio
            allocation = sharpe_ratio / total_sharpe

            zone_allocation_recommendation.append({
                "zone": zone,
                "allocation": allocation,
                "sharpe_ratio": sharpe_ratio,
            })

    # Generate suburb allocation recommendation (top 10)
    suburb_allocation_recommendation = []
    suburb_ranking = price_path_stats.get("suburb_ranking", [])
    top_suburbs = suburb_ranking[:10]
    total_sharpe = sum(sharpe for _, sharpe in top_suburbs)

    if total_sharpe > 0:
        for suburb_id, sharpe_ratio in top_suburbs:
            if suburb_id not in price_path_stats.get("suburb_stats", {}):
                continue

            stats = price_path_stats["suburb_stats"][suburb_id]
            suburb_name = stats.get("name", suburb_id)

            # Calculate allocation based on Sharpe ratio
            allocation = sharpe_ratio / total_sharpe

            suburb_allocation_recommendation.append({
                "suburb_id": suburb_id,
                "suburb_name": suburb_name,
                "zone": stats.get("zone", "unknown"),
                "allocation": allocation,
                "sharpe_ratio": sharpe_ratio,
            })

    # Generate Sydney market cycle visualization
    sydney_cycle_visualization = {
        "cycle_period_years": SYDNEY_CYCLE_PERIOD_YEARS,
        "cycle_amplitude": SYDNEY_CYCLE_AMPLITUDE,
        "long_term_growth": SYDNEY_LONG_TERM_GROWTH,
    }

    # Generate economic factor impact visualization
    economic_factor_impact = {
        "interest_rate_impact": INTEREST_RATE_IMPACT,
        "employment_impact": EMPLOYMENT_IMPACT,
        "population_growth_impact": POPULATION_GROWTH_IMPACT,
        "income_growth_impact": INCOME_GROWTH_IMPACT,
        "supply_demand_impact": SUPPLY_DEMAND_IMPACT,
    }

    # Generate property type modifier visualization
    property_type_modifiers = {
        "type": list(PROPERTY_TYPE_MODIFIERS.keys()),
        "modifier": list(PROPERTY_TYPE_MODIFIERS.values()),
    }

    # Generate property characteristic modifier visualization
    property_characteristic_modifiers = {
        "bedroom_modifier": BEDROOM_MODIFIER,
        "bathroom_modifier": BATHROOM_MODIFIER,
        "land_size_modifier": LAND_SIZE_MODIFIER,
        "age_modifier": AGE_MODIFIER,
    }

    return {
        "zone_price_charts": zone_price_charts,
        "zone_comparison_chart": zone_comparison_chart,
        "suburb_price_charts": suburb_price_charts,
        "correlation_heatmap": correlation_heatmap,
        "suburb_correlation_heatmap": suburb_correlation_heatmap,
        "final_distribution": final_distribution,
        "cycle_position_chart": cycle_position_chart,
        "regime_chart": regime_chart,
        "zone_performance_chart": zone_performance_chart,
        "suburb_performance_chart": suburb_performance_chart,
        "zone_allocation_recommendation": zone_allocation_recommendation,
        "suburb_allocation_recommendation": suburb_allocation_recommendation,
        "sydney_cycle_visualization": sydney_cycle_visualization,
        "economic_factor_impact": economic_factor_impact,
        "property_type_modifiers": property_type_modifiers,
        "property_characteristic_modifiers": property_characteristic_modifiers,
    }


def get_enhanced_price_index(
    price_paths: Dict[str, Dict[str, np.ndarray]],
    zone: str,
    suburb_id: str,
    property_id: str,
    month: int,
) -> float:
    """
    Get the enhanced price index for a specific property at a specific month.

    Args:
        price_paths: Dictionary of price paths
        zone: Zone name
        suburb_id: Suburb ID
        property_id: Property ID
        month: Month index (0-based)

    Returns:
        Price index
    """
    # Try to get property-specific price path
    property_price_paths = price_paths.get("property_price_paths", {})
    if property_id in property_price_paths:
        price_path = property_price_paths[property_id]
        if month < len(price_path):
            return price_path[month]

    # Try to get suburb-specific price path
    suburb_price_paths = price_paths.get("suburb_price_paths", {})
    if suburb_id in suburb_price_paths:
        price_path = suburb_price_paths[suburb_id]
        if month < len(price_path):
            return price_path[month]

    # Fall back to zone price path
    zone_price_paths = price_paths.get("zone_price_paths", {})
    if zone in zone_price_paths:
        price_path = zone_price_paths[zone]
        if month < len(price_path):
            return price_path[month]

    # Default to 1.0 (no appreciation)
    return 1.0


def calculate_enhanced_property_value(
    initial_value: float,
    price_paths: Dict[str, Dict[str, np.ndarray]],
    zone: str,
    suburb_id: str,
    property_id: str,
    month: int,
) -> float:
    """
    Calculate the enhanced property value at a specific month.

    Args:
        initial_value: Initial property value
        price_paths: Dictionary of price paths
        zone: Zone name
        suburb_id: Suburb ID
        property_id: Property ID
        month: Month index (0-based)

    Returns:
        Property value
    """
    price_index = get_enhanced_price_index(price_paths, zone, suburb_id, property_id, month)
    return initial_value * price_index


async def get_enhanced_price_path_summary(context: SimulationContext) -> Dict[str, Any]:
    """
    Get a summary of the enhanced price path simulation results.

    Args:
        context: Simulation context

    Returns:
        Dictionary containing price path summary
    """
    start_time = time.time()
    logger.info("Getting enhanced price path summary")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=0.0,
            message="Generating enhanced price path summary",
        )

        # Get price paths
        price_paths = getattr(context, "price_paths", {})

        # Get price path statistics
        price_path_stats = getattr(context, "price_path_stats", {})

        # Get price path visualization
        price_path_visualization = getattr(context, "price_path_visualization", {})

        # Generate summary
        summary = {
            "price_paths": price_paths,
            "statistics": price_path_stats,
            "visualization": price_path_visualization,
        }

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=100.0,
            message="Enhanced price path summary generated",
            data=summary,
        )

        # Update metrics
        increment_counter("enhanced_price_path_summary_generated_total")
        observe_histogram(
            "enhanced_price_path_summary_generation_runtime_seconds",
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
                "module": "price_path",
            },
        )

        # Re-raise exception
        raise
