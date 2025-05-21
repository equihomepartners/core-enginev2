"""
Price path API router for the EQU IHOME SIM ENGINE v2.

This module provides API endpoints for the price path simulator.
"""

from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from src.engine.simulation_context import SimulationContext
from src.price_path.price_path import (
    simulate_price_paths,
    get_price_path_summary,
    calculate_property_value,
)
from src.price_path.enhanced_price_path import (
    simulate_enhanced_price_paths,
    get_enhanced_price_path_summary,
    calculate_enhanced_property_value,
)

# In-memory storage for simulations
from src.api.routers.portfolio import simulations

router = APIRouter(
    prefix="/api/v1/simulations",
    tags=["price-path"],
)


class PricePathVisualizationResponse(BaseModel):
    """Price path visualization response model."""
    zone_price_charts: Dict[str, List[Dict[str, Any]]] = Field(
        ..., description="Price charts by zone"
    )
    zone_comparison_chart: List[Dict[str, Any]] = Field(
        ..., description="Comparison chart for all zones"
    )
    suburb_price_charts: Dict[str, List[Dict[str, Any]]] = Field(
        ..., description="Price charts by suburb"
    )
    correlation_heatmap: List[Dict[str, Any]] = Field(
        ..., description="Correlation heatmap data"
    )
    final_distribution: Dict[str, List[Dict[str, Any]]] = Field(
        ..., description="Distribution of final property values"
    )
    cycle_position_chart: Optional[List[Dict[str, Any]]] = Field(
        None, description="Property cycle position over time"
    )
    regime_chart: Optional[List[Dict[str, Any]]] = Field(
        None, description="Market regime over time"
    )


class PricePathStatisticsResponse(BaseModel):
    """Price path statistics response model."""
    zone_stats: Dict[str, Dict[str, float]] = Field(
        ..., description="Statistics by zone"
    )
    suburb_stats: Dict[str, Dict[str, float]] = Field(
        ..., description="Statistics by suburb"
    )
    correlation_matrix: Dict[str, Dict[str, float]] = Field(
        ..., description="Correlation matrix between zones"
    )


class PropertyValueRequest(BaseModel):
    """Property value request model."""
    property_id: str = Field(..., description="Property ID")
    zone: str = Field(..., description="Zone name")
    suburb_id: str = Field("", description="Suburb ID (optional)")
    initial_value: float = Field(..., description="Initial property value")
    month: int = Field(..., description="Month index (0-based)")


class PropertyValueResponse(BaseModel):
    """Property value response model."""
    property_id: str = Field(..., description="Property ID")
    initial_value: float = Field(..., description="Initial property value")
    current_value: float = Field(..., description="Current property value")
    appreciation: float = Field(..., description="Appreciation percentage")
    month: int = Field(..., description="Month index (0-based)")
    year: float = Field(..., description="Year")


class PricePathScenarioRequest(BaseModel):
    """Price path scenario request model."""
    model_type: str = Field(
        "gbm", description="Type of stochastic model to use"
    )
    appreciation_rates: Dict[str, float] = Field(
        ..., description="Zone-specific appreciation rates"
    )
    volatility: Dict[str, float] = Field(
        ..., description="Zone-specific volatility parameters"
    )
    correlation_matrix: Dict[str, float] = Field(
        ..., description="Correlation matrix between zones"
    )
    time_step: str = Field(
        "monthly", description="Time step for price path simulation"
    )
    fund_term: int = Field(
        10, description="Fund term in years"
    )


class EnhancedPricePathScenarioRequest(BaseModel):
    """Enhanced price path scenario request model."""
    model_type: str = Field(
        "sydney_cycle", description="Type of stochastic model to use (gbm, mean_reversion, regime_switching, sydney_cycle)"
    )
    appreciation_rates: Dict[str, float] = Field(
        ..., description="Zone-specific appreciation rates"
    )
    volatility: Dict[str, float] = Field(
        ..., description="Zone-specific volatility parameters"
    )
    correlation_matrix: Dict[str, float] = Field(
        ..., description="Correlation matrix between zones"
    )
    time_step: str = Field(
        "monthly", description="Time step for price path simulation"
    )
    fund_term: int = Field(
        10, description="Fund term in years"
    )
    cycle_position: float = Field(
        0.5, description="Initial position in the property cycle (0-1)"
    )
    suburb_variation: float = Field(
        0.02, description="Variation between suburbs within the same zone"
    )
    property_variation: float = Field(
        0.01, description="Variation between properties within the same suburb"
    )
    mean_reversion_params: Dict[str, float] = Field(
        {"speed": 0.2, "long_term_mean": 0.03}, description="Parameters for mean-reverting model"
    )
    regime_switching_params: Dict[str, float] = Field(
        {
            "bull_market_rate": 0.08,
            "bear_market_rate": -0.03,
            "bull_to_bear_prob": 0.1,
            "bear_to_bull_prob": 0.3
        },
        description="Parameters for regime-switching model"
    )


@router.get("/{simulation_id}/price-paths")
async def get_price_paths(simulation_id: str) -> Dict[str, Any]:
    """
    Get price path data for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Price path data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has price path data
    if "price_paths" not in simulation:
        raise HTTPException(status_code=404, detail="Price path data not found")

    return simulation["price_paths"]


@router.get("/{simulation_id}/price-paths/visualization", response_model=PricePathVisualizationResponse)
async def get_price_path_visualization(simulation_id: str) -> PricePathVisualizationResponse:
    """
    Get visualization data for price paths.

    Args:
        simulation_id: Simulation ID

    Returns:
        Visualization data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has price path visualization data
    if "price_paths" not in simulation or "visualization" not in simulation["price_paths"]:
        raise HTTPException(status_code=404, detail="Price path visualization data not found")

    return PricePathVisualizationResponse(**simulation["price_paths"]["visualization"])


@router.get("/{simulation_id}/price-paths/statistics", response_model=PricePathStatisticsResponse)
async def get_price_path_statistics(simulation_id: str) -> PricePathStatisticsResponse:
    """
    Get statistics for price paths.

    Args:
        simulation_id: Simulation ID

    Returns:
        Statistics data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has price path statistics data
    if "price_paths" not in simulation or "statistics" not in simulation["price_paths"]:
        raise HTTPException(status_code=404, detail="Price path statistics data not found")

    return PricePathStatisticsResponse(**simulation["price_paths"]["statistics"])


@router.post("/{simulation_id}/price-paths/property-value", response_model=PropertyValueResponse)
async def get_property_value(
    simulation_id: str,
    request: PropertyValueRequest
) -> PropertyValueResponse:
    """
    Calculate the property value at a specific month.

    Args:
        simulation_id: Simulation ID
        request: Property value request

    Returns:
        Property value
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has price path data
    if "price_paths" not in simulation:
        raise HTTPException(status_code=404, detail="Price path data not found")

    # Get price paths
    price_paths = simulation["price_paths"]

    # Calculate property value
    current_value = calculate_property_value(
        initial_value=request.initial_value,
        price_paths=price_paths,
        zone=request.zone,
        suburb_id=request.suburb_id if hasattr(request, "suburb_id") else "",
        property_id=request.property_id,
        month=request.month,
    )

    # Calculate appreciation
    appreciation = (current_value / request.initial_value) - 1

    # Calculate year
    year = request.month / 12.0

    return PropertyValueResponse(
        property_id=request.property_id,
        initial_value=request.initial_value,
        current_value=current_value,
        appreciation=appreciation,
        month=request.month,
        year=year,
    )


@router.post("/{simulation_id}/price-paths/scenario")
async def run_price_path_scenario(
    simulation_id: str,
    request: PricePathScenarioRequest
) -> Dict[str, Any]:
    """
    Run a price path scenario with custom parameters.

    Args:
        simulation_id: Simulation ID
        request: Price path scenario request

    Returns:
        Price path scenario results
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has a context
    if "context" not in simulation:
        raise HTTPException(status_code=400, detail="Simulation context not found")

    # Get simulation context
    context = simulation["context"]

    # Update context with scenario parameters
    context.config.appreciation_rates = request.appreciation_rates
    context.config.price_path = {
        "model_type": request.model_type,
        "volatility": request.volatility,
        "correlation_matrix": request.correlation_matrix,
        "time_step": request.time_step,
    }
    context.config.fund_term = request.fund_term

    # Run price path simulation
    try:
        await simulate_price_paths(context)

        # Get price path summary
        summary = await get_price_path_summary(context)

        # Update simulation data
        simulation["price_paths"] = summary

        return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{simulation_id}/price-paths/enhanced-property-value")
async def get_enhanced_property_value(
    simulation_id: str,
    request: PropertyValueRequest
) -> PropertyValueResponse:
    """
    Calculate the enhanced property value at a specific month.

    Args:
        simulation_id: Simulation ID
        request: Property value request

    Returns:
        Property value
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has price path data
    if "price_paths" not in simulation:
        raise HTTPException(status_code=404, detail="Price path data not found")

    # Get price paths
    price_paths = simulation["price_paths"]

    # Calculate property value
    current_value = calculate_enhanced_property_value(
        initial_value=request.initial_value,
        price_paths=price_paths,
        zone=request.zone,
        suburb_id=request.suburb_id if hasattr(request, "suburb_id") else "",
        property_id=request.property_id,
        month=request.month,
    )

    # Calculate appreciation
    appreciation = (current_value / request.initial_value) - 1

    # Calculate year
    year = request.month / 12.0

    return PropertyValueResponse(
        property_id=request.property_id,
        initial_value=request.initial_value,
        current_value=current_value,
        appreciation=appreciation,
        month=request.month,
        year=year,
    )


@router.post("/{simulation_id}/price-paths/enhanced-scenario")
async def run_enhanced_price_path_scenario(
    simulation_id: str,
    request: EnhancedPricePathScenarioRequest
) -> Dict[str, Any]:
    """
    Run an enhanced price path scenario with custom parameters.

    This endpoint uses the enhanced price path simulator that integrates more deeply
    with the TLS module to generate realistic price paths based on suburb-specific
    data, economic factors, and Sydney property market cycles.

    Args:
        simulation_id: Simulation ID
        request: Enhanced price path scenario request

    Returns:
        Enhanced price path scenario results
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has a context
    if "context" not in simulation:
        raise HTTPException(status_code=400, detail="Simulation context not found")

    # Get simulation context
    context = simulation["context"]

    # Update context with scenario parameters
    context.config.appreciation_rates = request.appreciation_rates
    context.config.price_path = {
        "model_type": request.model_type,
        "volatility": request.volatility,
        "correlation_matrix": request.correlation_matrix,
        "time_step": request.time_step,
        "cycle_position": request.cycle_position,
        "suburb_variation": request.suburb_variation,
        "property_variation": request.property_variation,
        "mean_reversion_params": request.mean_reversion_params,
        "regime_switching_params": request.regime_switching_params,
    }
    context.config.fund_term = request.fund_term

    # Run enhanced price path simulation
    try:
        await simulate_enhanced_price_paths(context)

        # Get enhanced price path summary
        summary = await get_enhanced_price_path_summary(context)

        # Update simulation data
        simulation["price_paths"] = summary

        return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
