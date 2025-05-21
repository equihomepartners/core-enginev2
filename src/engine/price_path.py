"""
Price path simulator module for the EQU IHOME SIM ENGINE v2.

This module is responsible for simulating home price appreciation paths for different zones.
"""

from typing import Dict, Any, List, Optional

import numpy as np
import structlog

from src.engine.simulation_context import SimulationContext
from src.monte_carlo.rng_factory import get_rng

logger = structlog.get_logger(__name__)


def simulate_price_paths(context: SimulationContext) -> None:
    """
    Simulate home price appreciation paths for different zones.
    
    Args:
        context: Simulation context
    """
    logger.info("Simulating price paths")
    
    # Get configuration parameters
    config = context.config
    
    # Get random number generator
    if context.rng is None:
        context.rng = get_rng("price_path", 0)
    
    # Get zone-specific appreciation rates
    appreciation_rates = config.appreciation_rates.dict()
    
    # Get fund term
    fund_term = config.fund_term
    
    # Simulate price paths for each zone
    price_paths = {}
    for zone, base_rate in appreciation_rates.items():
        # Get zone-specific RNG
        zone_rng = get_rng(f"price_path_{zone}", 0)
        
        # Simulate price path
        price_path = simulate_zone_price_path(
            base_rate=base_rate,
            years=fund_term,
            rng=zone_rng,
        )
        
        price_paths[zone] = price_path
    
    # Store price paths in context
    context.price_paths = price_paths
    
    # Log summary
    logger.info(
        "Price path simulation completed",
        zones=list(price_paths.keys()),
        years=fund_term,
    )


def simulate_zone_price_path(
    base_rate: float,
    years: int,
    volatility: float = 0.05,
    rng: Optional[np.random.Generator] = None,
) -> np.ndarray:
    """
    Simulate a price path for a specific zone.
    
    Args:
        base_rate: Base appreciation rate
        years: Number of years to simulate
        volatility: Volatility of the price path
        rng: Random number generator
        
    Returns:
        Array of price indices (starting at 1.0)
    """
    if rng is None:
        rng = get_rng("price_path", 0)
    
    # Number of time steps (monthly)
    num_steps = years * 12
    
    # Convert annual rate to monthly rate
    monthly_rate = (1 + base_rate) ** (1 / 12) - 1
    
    # Convert annual volatility to monthly volatility
    monthly_volatility = volatility / np.sqrt(12)
    
    # Generate random shocks
    shocks = rng.normal(0, monthly_volatility, num_steps)
    
    # Calculate monthly returns
    returns = monthly_rate + shocks
    
    # Calculate cumulative returns
    cumulative_returns = np.cumprod(1 + returns)
    
    # Insert initial value (1.0)
    price_path = np.insert(cumulative_returns, 0, 1.0)
    
    return price_path


def get_annual_price_indices(price_path: np.ndarray) -> np.ndarray:
    """
    Extract annual price indices from a monthly price path.
    
    Args:
        price_path: Monthly price path
        
    Returns:
        Annual price indices
    """
    # Extract values at 12-month intervals
    annual_indices = price_path[::12]
    
    return annual_indices


def calculate_appreciation_rate(
    start_index: float, end_index: float, years: float
) -> float:
    """
    Calculate the annualized appreciation rate between two price indices.
    
    Args:
        start_index: Starting price index
        end_index: Ending price index
        years: Number of years between indices
        
    Returns:
        Annualized appreciation rate
    """
    if start_index <= 0 or years <= 0:
        return 0.0
    
    # Calculate annualized rate
    rate = (end_index / start_index) ** (1 / years) - 1
    
    return rate


def get_price_index(
    price_paths: Dict[str, np.ndarray], zone: str, month: int
) -> float:
    """
    Get the price index for a specific zone and month.
    
    Args:
        price_paths: Dictionary of price paths by zone
        zone: Zone name
        month: Month index (0-based)
        
    Returns:
        Price index
    """
    if zone not in price_paths:
        logger.warning("Zone not found in price paths", zone=zone)
        return 1.0
    
    price_path = price_paths[zone]
    
    if month >= len(price_path):
        logger.warning(
            "Month index out of bounds",
            zone=zone,
            month=month,
            max_month=len(price_path) - 1,
        )
        return price_path[-1]
    
    return price_path[month]


def calculate_property_value(
    initial_value: float,
    price_paths: Dict[str, np.ndarray],
    zone: str,
    month: int,
) -> float:
    """
    Calculate the property value at a specific month.
    
    Args:
        initial_value: Initial property value
        price_paths: Dictionary of price paths by zone
        zone: Zone name
        month: Month index (0-based)
        
    Returns:
        Property value
    """
    price_index = get_price_index(price_paths, zone, month)
    return initial_value * price_index
