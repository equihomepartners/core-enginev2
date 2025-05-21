"""
Price path simulator module for the EQU IHOME SIM ENGINE v2.

This module is responsible for simulating home price appreciation paths for different zones.
It implements multiple stochastic models for price path simulation, including Geometric
Brownian Motion (GBM), mean-reverting models, and regime-switching models.
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

logger = structlog.get_logger(__name__)


async def simulate_price_paths(context: SimulationContext) -> None:
    """
    Simulate home price appreciation paths for different zones.

    This function simulates price paths for different zones based on the configuration
    parameters. It supports multiple stochastic models, including Geometric Brownian
    Motion (GBM), mean-reverting models, and regime-switching models. It also
    generates suburb-level and property-level price paths with appropriate variation.

    Args:
        context: Simulation context

    Raises:
        ValueError: If the configuration parameters are invalid
    """
    start_time = time.time()
    logger.info("Simulating price paths")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=0.0,
            message="Starting price path simulation",
        )

        # Get configuration parameters
        config = context.config

        # Get random number generator
        if context.rng is None:
            context.rng = get_rng("price_path", 0)

        # Get zone-specific appreciation rates
        appreciation_rates = getattr(config, "appreciation_rates", {})
        if not appreciation_rates:
            appreciation_rates = {
                "green": 0.05,
                "orange": 0.03,
                "red": 0.01
            }

        # Get price path configuration
        price_path_config = getattr(config, "price_path", {})

        # Get model type
        model_type = getattr(price_path_config, "model_type", "gbm")

        # Get volatility parameters
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

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=10.0,
            message="Preparing price path simulation",
            data={
                "model_type": model_type,
                "time_step": time_step,
                "num_steps": num_steps,
                "fund_term": fund_term,
            },
        )

        # Send informational message
        await websocket_manager.send_info(
            simulation_id=context.run_id,
            message="Simulating price paths",
            data={
                "model_type": model_type,
                "appreciation_rates": appreciation_rates,
                "volatility": volatility,
                "time_step": time_step,
                "num_steps": num_steps,
            },
        )

        # Generate correlated random variables for zones
        zones = ["green", "orange", "red"]
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

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=20.0,
            message="Generated correlated random variables",
        )

        # Simulate price paths for each zone
        zone_price_paths = {}
        for i, zone in enumerate(zones):
            # Get zone-specific parameters
            base_rate = getattr(appreciation_rates, zone, 0.03)
            vol = getattr(volatility, zone, 0.05)

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
                    bull_rate=bull_rate,
                    bear_rate=bear_rate,
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
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=50.0,
            message="Simulated zone price paths",
            data={
                "num_zones": len(zone_price_paths),
            },
        )

        # Generate suburb-level price paths
        suburb_price_paths = {}
        suburb_variation = getattr(price_path_config, "suburb_variation", 0.02)

        # Get TLS data
        tls_data = context.tls_data

        # Generate suburb-level price paths
        for suburb_id, suburb_data in tls_data.items():
            zone = suburb_data.get("zone", "green")

            # Get zone price path
            zone_path = zone_price_paths.get(zone, zone_price_paths.get("green", None))
            if zone_path is None:
                continue

            # Generate suburb-specific variation
            suburb_rng = get_rng(f"price_path_suburb_{suburb_id}", 0)
            suburb_shocks = suburb_rng.normal(0, suburb_variation, size=num_steps)

            # Apply variation to zone path
            suburb_path = zone_path.copy()
            for t in range(1, len(suburb_path)):
                # Apply multiplicative shock
                suburb_path[t] *= (1.0 + suburb_shocks[t-1])

            # Store suburb price path
            suburb_price_paths[suburb_id] = suburb_path

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=70.0,
            message="Generated suburb-level price paths",
            data={
                "num_suburbs": len(suburb_price_paths),
            },
        )

        # Generate property-level price paths
        property_price_paths = {}
        property_variation = getattr(price_path_config, "property_variation", 0.01)

        # Get loans
        loans = context.loans

        # Generate property-level price paths for each loan
        for loan in loans:
            property_id = loan.get("property_id", "")
            suburb_id = loan.get("suburb_id", "")
            zone = loan.get("zone", "green")

            # Skip if property ID is missing
            if not property_id:
                continue

            # Get suburb price path or fall back to zone price path
            base_path = suburb_price_paths.get(suburb_id, zone_price_paths.get(zone, None))
            if base_path is None:
                continue

            # Generate property-specific variation
            property_rng = get_rng(f"price_path_property_{property_id}", 0)
            property_shocks = property_rng.normal(0, property_variation, size=num_steps)

            # Apply variation to base path
            property_path = base_path.copy()
            for t in range(1, len(property_path)):
                # Apply multiplicative shock
                property_path[t] *= (1.0 + property_shocks[t-1])

            # Store property price path
            property_price_paths[property_id] = property_path

        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=90.0,
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
        price_path_stats = calculate_price_path_statistics(
            zone_price_paths=zone_price_paths,
            suburb_price_paths=suburb_price_paths,
            dt=dt,
        )

        # Store statistics in context
        context.price_path_stats = price_path_stats

        # Generate visualization data
        price_path_visualization = generate_price_path_visualization(
            zone_price_paths=zone_price_paths,
            suburb_price_paths=suburb_price_paths,
            property_price_paths=property_price_paths,
            price_path_stats=price_path_stats,
            time_step=time_step,
            market_regimes=getattr(context, "market_regimes", None),
        )

        # Store visualization data in context
        context.price_path_visualization = price_path_visualization

        # Report completion
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=100.0,
            message="Price path simulation completed",
            data={
                "num_zones": len(zone_price_paths),
                "num_suburbs": len(suburb_price_paths),
                "num_properties": len(property_price_paths),
            },
        )

        # Update metrics
        increment_counter("price_path_simulations_completed_total")
        observe_histogram(
            "price_path_simulation_runtime_seconds",
            time.time() - start_time,
        )

        # Log completion
        logger.info(
            "Price path simulation completed",
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
        increment_counter("price_path_simulations_failed_total")

        # Re-raise exception
        raise


def simulate_gbm(
    base_rate: float,
    volatility: float,
    num_steps: int,
    dt: float,
    random_shocks: Optional[np.ndarray] = None,
) -> np.ndarray:
    """
    Simulate a price path using Geometric Brownian Motion (GBM).

    Args:
        base_rate: Base appreciation rate (annual)
        volatility: Volatility (annual standard deviation)
        num_steps: Number of time steps
        dt: Time step size (in years)
        random_shocks: Pre-generated random shocks (for correlation)

    Returns:
        Array of price indices (starting at 1.0)
    """
    # Convert annual rate to time step rate
    mu = base_rate * dt

    # Convert annual volatility to time step volatility
    sigma = volatility * np.sqrt(dt)

    # Generate random shocks if not provided
    if random_shocks is None:
        random_shocks = np.random.normal(0, 1, num_steps)

    # Calculate returns
    returns = mu + sigma * random_shocks

    # Calculate cumulative returns
    cumulative_returns = np.cumprod(1 + returns)

    # Insert initial value (1.0)
    price_path = np.insert(cumulative_returns, 0, 1.0)

    return price_path


def simulate_mean_reversion(
    base_rate: float,
    volatility: float,
    speed: float,
    long_term_mean: float,
    num_steps: int,
    dt: float,
    random_shocks: Optional[np.ndarray] = None,
) -> np.ndarray:
    """
    Simulate a price path using a mean-reverting model (Ornstein-Uhlenbeck process).

    Args:
        base_rate: Initial rate
        volatility: Volatility (annual standard deviation)
        speed: Speed of mean reversion
        long_term_mean: Long-term mean to revert to
        num_steps: Number of time steps
        dt: Time step size (in years)
        random_shocks: Pre-generated random shocks (for correlation)

    Returns:
        Array of price indices (starting at 1.0)
    """
    # Convert annual parameters to time step parameters
    sigma = volatility * np.sqrt(dt)

    # Generate random shocks if not provided
    if random_shocks is None:
        random_shocks = np.random.normal(0, 1, num_steps)

    # Initialize arrays
    rates = np.zeros(num_steps + 1)
    rates[0] = base_rate

    # Simulate mean-reverting process for rates
    for t in range(num_steps):
        # Calculate mean reversion term
        mean_reversion = speed * (long_term_mean - rates[t]) * dt

        # Calculate random shock term
        shock = sigma * random_shocks[t]

        # Update rate
        rates[t+1] = rates[t] + mean_reversion + shock

    # Calculate returns from rates
    returns = rates[1:] * dt

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
        bull_volatility: Volatility in bull market (annual)
        bear_volatility: Volatility in bear market (annual)
        bull_to_bear_prob: Probability of switching from bull to bear market
        bear_to_bull_prob: Probability of switching from bear to bull market
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

    # Adjust transition probabilities for time step
    bull_to_bear = 1 - (1 - bull_to_bear_prob) ** dt
    bear_to_bull = 1 - (1 - bear_to_bull_prob) ** dt

    # Generate random shocks if not provided
    if random_shocks is None:
        random_shocks = np.random.normal(0, 1, num_steps)

    # Get RNG for regime transitions
    if rng is None:
        rng = np.random.default_rng()

    # Initialize arrays
    returns = np.zeros(num_steps)
    regimes = np.zeros(num_steps + 1, dtype=int)  # 0 = bull, 1 = bear

    # Start in bull market
    regimes[0] = 0

    # Simulate regime-switching process
    for t in range(num_steps):
        # Determine current regime
        current_regime = regimes[t]

        # Determine next regime
        if current_regime == 0:  # Bull market
            # Check for transition to bear market
            if rng.random() < bull_to_bear:
                regimes[t+1] = 1
            else:
                regimes[t+1] = 0
        else:  # Bear market
            # Check for transition to bull market
            if rng.random() < bear_to_bull:
                regimes[t+1] = 0
            else:
                regimes[t+1] = 1

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


def calculate_price_path_statistics(
    zone_price_paths: Dict[str, np.ndarray],
    suburb_price_paths: Dict[str, np.ndarray],
    dt: float,
) -> Dict[str, Any]:
    """
    Calculate statistics for price paths.

    Args:
        zone_price_paths: Dictionary of price paths by zone
        suburb_price_paths: Dictionary of price paths by suburb
        dt: Time step size (in years)

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
        # Calculate returns
        returns = np.diff(price_path) / price_path[:-1]

        # Calculate CAGR
        years = len(price_path) * dt
        cagr = (price_path[-1] / price_path[0]) ** (1 / years) - 1

        # Calculate volatility
        volatility = np.std(returns) / np.sqrt(dt)

        # Calculate maximum drawdown
        max_drawdown = calculate_max_drawdown(price_path)

        # Store statistics
        suburb_stats[suburb_id] = {
            "cagr": cagr,
            "volatility": volatility,
            "max_drawdown": max_drawdown,
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

    return {
        "zone_stats": zone_stats,
        "suburb_stats": suburb_stats,
        "correlation_matrix": correlation_matrix,
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


def generate_price_path_visualization(
    zone_price_paths: Dict[str, np.ndarray],
    suburb_price_paths: Dict[str, np.ndarray],
    property_price_paths: Dict[str, np.ndarray],
    price_path_stats: Dict[str, Any],
    time_step: str,
    market_regimes: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """
    Generate visualization data for price paths.

    Args:
        zone_price_paths: Dictionary of price paths by zone
        suburb_price_paths: Dictionary of price paths by suburb
        property_price_paths: Dictionary of price paths by property
        price_path_stats: Dictionary of price path statistics
        time_step: Time step for price path simulation
        market_regimes: Array of market regimes (0 = bull, 1 = bear)

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

    # Generate suburb price charts (sample of suburbs)
    suburb_price_charts = {}
    sample_suburbs = list(suburb_price_paths.keys())[:10]  # Limit to 10 suburbs
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
    if market_regimes is not None:
        for t in range(len(market_regimes)):
            # Calculate cycle position (0 = bear market, 1 = bull market)
            cycle_position = 1.0 - market_regimes[t]

            cycle_position_chart.append({
                "year": t * dt,
                "cycle_position": cycle_position,
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

    return {
        "zone_price_charts": zone_price_charts,
        "zone_comparison_chart": zone_comparison_chart,
        "suburb_price_charts": suburb_price_charts,
        "correlation_heatmap": correlation_heatmap,
        "final_distribution": final_distribution,
        "cycle_position_chart": cycle_position_chart,
        "regime_chart": regime_chart,
    }


def get_price_index(
    price_paths: Dict[str, Dict[str, np.ndarray]],
    zone: str,
    property_id: str,
    month: int,
    suburb_id: str = "",
) -> float:
    """
    Get the price index for a specific property at a specific month.

    Args:
        price_paths: Dictionary of price paths
        zone: Zone name
        property_id: Property ID
        month: Month index (0-based)
        suburb_id: Suburb ID (optional)

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
    if suburb_id:
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


def calculate_property_value(
    initial_value: float,
    price_paths: Dict[str, Dict[str, np.ndarray]],
    zone: str,
    property_id: str,
    month: int,
    suburb_id: str = "",
) -> float:
    """
    Calculate the property value at a specific month.

    Args:
        initial_value: Initial property value
        price_paths: Dictionary of price paths
        zone: Zone name
        property_id: Property ID
        month: Month index (0-based)
        suburb_id: Suburb ID (optional)

    Returns:
        Property value
    """
    price_index = get_price_index(price_paths, zone, property_id, month, suburb_id)
    return initial_value * price_index


async def get_price_path_summary(context: SimulationContext) -> Dict[str, Any]:
    """
    Get a summary of the price path simulation results.

    Args:
        context: Simulation context

    Returns:
        Dictionary containing price path summary
    """
    start_time = time.time()
    logger.info("Getting price path summary")

    # Get WebSocket manager for progress reporting
    websocket_manager = get_websocket_manager()

    try:
        # Report progress
        await websocket_manager.send_progress(
            simulation_id=context.run_id,
            module="price_path",
            progress=0.0,
            message="Generating price path summary",
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
            message="Price path summary generated",
            data=summary,
        )

        # Update metrics
        increment_counter("price_path_summary_generated_total")
        observe_histogram(
            "price_path_summary_generation_runtime_seconds",
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
