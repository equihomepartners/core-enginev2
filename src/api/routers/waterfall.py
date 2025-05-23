"""
API router for waterfall engine functionality.

This module defines FastAPI endpoints for waterfall engine functionality,
including waterfall distribution calculation and visualization.
"""

from typing import Dict, Any, List, Optional
from enum import Enum

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field

from src.config.config_loader import SimulationConfig
from src.engine.simulation_context import SimulationContext, get_simulation_context_by_id
from src.waterfall_engine import WaterfallEngine, WaterfallStructure, calculate_waterfall

router = APIRouter(
    prefix="/simulations",
    tags=["waterfall"],
    responses={404: {"description": "Not found"}},
)


class WaterfallStructureEnum(str, Enum):
    """Enum for waterfall structure types."""
    EUROPEAN = "european"
    AMERICAN = "american"


class WaterfallTierModel(BaseModel):
    """Model for waterfall tier data."""
    tier: str = Field(..., description="Tier name")
    amount: float = Field(..., description="Amount allocated to this tier")
    percentage: float = Field(..., description="Percentage of total distribution")


class WaterfallChartModel(BaseModel):
    """Model for waterfall chart data."""
    category: str = Field(..., description="Distribution category")
    amount: float = Field(..., description="Amount distributed")


class DistributionByYearModel(BaseModel):
    """Model for distribution by year data."""
    year: int = Field(..., description="Distribution year")
    lp_return_of_capital: float = Field(..., description="LP return of capital")
    lp_preferred_return: float = Field(..., description="LP preferred return")
    lp_residual: float = Field(..., description="LP residual distribution")
    gp_catch_up: float = Field(..., description="GP catch-up")
    gp_carried_interest: float = Field(..., description="GP carried interest")
    total: float = Field(..., description="Total distribution")


class StakeholderAllocationModel(BaseModel):
    """Model for stakeholder allocation data."""
    stakeholder: str = Field(..., description="Stakeholder name")
    amount: float = Field(..., description="Amount allocated")
    percentage: float = Field(..., description="Percentage of total distribution")


class WaterfallVisualizationModel(BaseModel):
    """Model for waterfall visualization data."""
    waterfall_chart: List[WaterfallChartModel] = Field(
        ..., description="Waterfall chart data"
    )
    distribution_by_year_chart: List[DistributionByYearModel] = Field(
        ..., description="Distribution by year chart data"
    )
    tier_allocation_chart: List[WaterfallTierModel] = Field(
        ..., description="Tier allocation chart data"
    )
    stakeholder_allocation_chart: List[StakeholderAllocationModel] = Field(
        ..., description="Stakeholder allocation chart data"
    )


class WaterfallDistributionModel(BaseModel):
    """Model for waterfall distribution data."""
    return_of_capital: float = Field(..., description="Return of capital amount")
    preferred_return: float = Field(..., description="Preferred return amount")
    catch_up: float = Field(..., description="GP catch-up amount")
    carried_interest: float = Field(..., description="Carried interest amount")
    residual_to_lp: float = Field(..., description="Residual to LP amount")
    total_to_lp: float = Field(..., description="Total to LP amount")
    total_to_gp: float = Field(..., description="Total to GP amount")
    total_distributed: float = Field(..., description="Total distributed amount")


class WaterfallResultModel(BaseModel):
    """Model for waterfall result data."""
    distributions: WaterfallDistributionModel = Field(
        ..., description="Waterfall distribution data"
    )
    clawback_amount: float = Field(..., description="Clawback amount")
    visualization: WaterfallVisualizationModel = Field(
        ..., description="Waterfall visualization data"
    )


class WaterfallConfigModel(BaseModel):
    """Model for waterfall configuration."""
    waterfall_structure: WaterfallStructureEnum = Field(
        WaterfallStructureEnum.EUROPEAN, description="Waterfall structure type"
    )
    hurdle_rate: float = Field(0.08, description="Hurdle rate (preferred return)")
    carried_interest_rate: float = Field(0.20, description="Carried interest rate")
    catch_up_rate: float = Field(0.0, description="GP catch-up rate")
    gp_commitment_percentage: float = Field(0.0, description="GP commitment percentage")
    multi_tier_enabled: bool = Field(False, description="Enable multi-tier waterfall")
    enable_clawback: bool = Field(True, description="Enable clawback")
    clawback_threshold: float = Field(0.0, description="Clawback threshold")


@router.get(
    "/{simulation_id}/waterfall",
    response_model=WaterfallResultModel,
    summary="Get waterfall distribution for a simulation",
    description="Returns the waterfall distribution for a simulation",
)
async def get_waterfall_distribution(simulation_id: str):
    """
    Get waterfall distribution for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Waterfall distribution data
    """
    # Get simulation context
    context = get_simulation_context_by_id(simulation_id)
    if not context:
        raise HTTPException(
            status_code=404,
            detail="Simulation context not found"
        )

    if not hasattr(context, "waterfall") or not context.waterfall:
        # Calculate waterfall if not already calculated
        await calculate_waterfall(context)

    if not hasattr(context, "waterfall") or not context.waterfall:
        raise HTTPException(
            status_code=404,
            detail="Waterfall distribution not found for this simulation",
        )

    return context.waterfall


@router.post(
    "/{simulation_id}/waterfall/calculate",
    response_model=WaterfallResultModel,
    summary="Calculate waterfall distribution",
    description="Calculates waterfall distribution based on provided configuration",
)
async def calculate_waterfall_distribution(
    simulation_id: str,
    config: WaterfallConfigModel,
):
    """
    Calculate waterfall distribution.

    Args:
        simulation_id: Simulation ID
        config: Waterfall configuration

    Returns:
        Waterfall distribution data
    """
    # Get simulation context
    context = get_simulation_context_by_id(simulation_id)
    if not context:
        raise HTTPException(
            status_code=404,
            detail="Simulation context not found"
        )

    # Update context with waterfall configuration
    context.config.waterfall_structure = config.waterfall_structure.value
    context.config.hurdle_rate = config.hurdle_rate
    context.config.carried_interest_rate = config.carried_interest_rate
    context.config.catch_up_rate = config.catch_up_rate
    context.config.gp_commitment_percentage = config.gp_commitment_percentage

    # Update waterfall engine config
    if not hasattr(context.config, "waterfall_engine"):
        context.config.waterfall_engine = {}

    context.config.waterfall_engine["multi_tier_enabled"] = config.multi_tier_enabled
    context.config.waterfall_engine["enable_clawback"] = config.enable_clawback
    context.config.waterfall_engine["clawback_threshold"] = config.clawback_threshold

    # Calculate waterfall
    await calculate_waterfall(context)

    if not hasattr(context, "waterfall") or not context.waterfall:
        raise HTTPException(
            status_code=500,
            detail="Failed to calculate waterfall distribution",
        )

    return context.waterfall


@router.get(
    "/{simulation_id}/waterfall/visualization",
    response_model=WaterfallVisualizationModel,
    summary="Get waterfall visualization data",
    description="Returns visualization data for waterfall distribution",
)
async def get_waterfall_visualization(simulation_id: str):
    """
    Get waterfall visualization data.

    Args:
        simulation_id: Simulation ID

    Returns:
        Waterfall visualization data
    """
    # Get simulation context
    context = get_simulation_context_by_id(simulation_id)
    if not context:
        raise HTTPException(
            status_code=404,
            detail="Simulation context not found"
        )

    if not hasattr(context, "waterfall") or not context.waterfall:
        # Calculate waterfall if not already calculated
        await calculate_waterfall(context)

    if not hasattr(context, "waterfall") or not context.waterfall:
        raise HTTPException(
            status_code=404,
            detail="Waterfall distribution not found for this simulation",
        )

    return context.waterfall.get("visualization", {})
