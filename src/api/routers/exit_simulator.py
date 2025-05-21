"""
Exit simulator API router for the EQU IHOME SIM ENGINE v2.

This module provides API endpoints for the exit simulator.
"""

from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from src.engine.simulation_context import SimulationContext
from src.exit_simulator.exit_simulator import (
    simulate_exits,
    get_exit_summary,
    calculate_exit_value,
    ExitType,
)

# In-memory storage for simulations
from src.api.routers.portfolio import simulations

router = APIRouter(
    prefix="/api/v1/simulations",
    tags=["exit-simulator"],
)


class ExitVisualizationResponse(BaseModel):
    """Exit visualization response model."""
    exit_timing_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit timing distribution chart"
    )
    exit_type_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit type distribution chart"
    )
    cumulative_exits_chart: List[Dict[str, Any]] = Field(
        ..., description="Cumulative exits chart"
    )
    exit_roi_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit ROI distribution chart"
    )
    exit_type_roi_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit type ROI chart"
    )
    exit_summary: Dict[str, Any] = Field(
        ..., description="Exit summary"
    )
    exit_value_by_year_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit value by year chart"
    )
    exit_count_by_year_chart: List[Dict[str, Any]] = Field(
        ..., description="Exit count by year chart"
    )


class ExitStatisticsResponse(BaseModel):
    """Exit statistics response model."""
    avg_exit_year: float = Field(
        ..., description="Average exit year"
    )
    avg_roi: float = Field(
        ..., description="Average ROI"
    )
    avg_annualized_roi: float = Field(
        ..., description="Average annualized ROI"
    )
    exit_type_distribution: Dict[str, float] = Field(
        ..., description="Exit type distribution"
    )
    exit_timing_distribution: Dict[str, int] = Field(
        ..., description="Exit timing distribution"
    )
    exit_roi_distribution: Dict[str, int] = Field(
        ..., description="Exit ROI distribution"
    )
    exit_type_roi: Dict[str, Dict[str, Any]] = Field(
        ..., description="Exit type ROI"
    )
    exit_value_total: float = Field(
        ..., description="Total exit value"
    )
    appreciation_share_total: float = Field(
        ..., description="Total appreciation share"
    )
    total_return: float = Field(
        ..., description="Total return"
    )
    total_roi: float = Field(
        ..., description="Total ROI"
    )
    annualized_roi: float = Field(
        ..., description="Annualized ROI"
    )


class LoanExitRequest(BaseModel):
    """Loan exit request model."""
    loan_id: str = Field(..., description="Loan ID")
    property_id: str = Field(..., description="Property ID")
    suburb_id: str = Field("", description="Suburb ID (optional)")
    zone: str = Field(..., description="Zone name")
    loan_amount: float = Field(..., description="Loan amount")
    property_value: float = Field(..., description="Initial property value")
    exit_month: int = Field(..., description="Exit month (0-based)")
    exit_type: str = Field(..., description="Exit type (sale, refinance, default, term_completion)")


class LoanExitResponse(BaseModel):
    """Loan exit response model."""
    loan_id: str = Field(..., description="Loan ID")
    property_id: str = Field(..., description="Property ID")
    loan_amount: float = Field(..., description="Loan amount")
    property_value: float = Field(..., description="Initial property value")
    current_value: float = Field(..., description="Current property value")
    appreciation: float = Field(..., description="Appreciation percentage")
    exit_month: int = Field(..., description="Exit month (0-based)")
    exit_year: float = Field(..., description="Exit year")
    exit_type: str = Field(..., description="Exit type")
    exit_value: float = Field(..., description="Exit value")
    appreciation_share_amount: float = Field(..., description="Appreciation share amount")
    total_return: float = Field(..., description="Total return")
    roi: float = Field(..., description="ROI")
    annualized_roi: float = Field(..., description="Annualized ROI")


class ExitScenarioRequest(BaseModel):
    """Exit scenario request model."""
    base_exit_rate: float = Field(
        0.1, description="Base annual exit probability"
    )
    time_factor: float = Field(
        0.4, description="Weight for time-based exit probability"
    )
    price_factor: float = Field(
        0.6, description="Weight for price-based exit probability"
    )
    min_hold_period: float = Field(
        1.0, description="Minimum holding period in years"
    )
    max_hold_period: float = Field(
        10.0, description="Maximum holding period in years"
    )
    sale_weight: float = Field(
        0.6, description="Base weight for sale exits"
    )
    refinance_weight: float = Field(
        0.3, description="Base weight for refinance exits"
    )
    default_weight: float = Field(
        0.1, description="Base weight for default exits"
    )
    appreciation_sale_multiplier: float = Field(
        2.0, description="How much appreciation increases sale probability"
    )
    interest_rate_refinance_multiplier: float = Field(
        3.0, description="How much interest rate changes affect refinance probability"
    )
    economic_factor_default_multiplier: float = Field(
        2.0, description="How much economic factors affect default probability"
    )
    appreciation_share: float = Field(
        0.2, description="Fund's share of appreciation"
    )
    min_appreciation_share: float = Field(
        0.1, description="Minimum appreciation share"
    )
    max_appreciation_share: float = Field(
        0.5, description="Maximum appreciation share"
    )
    tiered_appreciation_thresholds: List[float] = Field(
        [0.2, 0.5, 1.0], description="Thresholds for tiered appreciation sharing"
    )
    tiered_appreciation_shares: List[float] = Field(
        [0.1, 0.2, 0.3, 0.4], description="Shares for tiered appreciation sharing"
    )
    base_default_rate: float = Field(
        0.01, description="Base annual default probability"
    )
    recovery_rate: float = Field(
        0.8, description="Recovery rate in case of default"
    )
    foreclosure_cost: float = Field(
        0.1, description="Cost of foreclosure as percentage of property value"
    )
    foreclosure_time: float = Field(
        1.0, description="Time to complete foreclosure in years"
    )


@router.get("/{simulation_id}/exits")
async def get_exits(simulation_id: str) -> Dict[str, Any]:
    """
    Get exit simulation results.

    Args:
        simulation_id: Simulation ID

    Returns:
        Exit simulation results
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has exit data
    if "exits" not in simulation:
        raise HTTPException(status_code=404, detail="Exit data not found")

    return simulation["exits"]


@router.get("/{simulation_id}/exits/visualization", response_model=ExitVisualizationResponse)
async def get_exit_visualization(simulation_id: str) -> ExitVisualizationResponse:
    """
    Get visualization data for exits.

    Args:
        simulation_id: Simulation ID

    Returns:
        Visualization data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has exit visualization data
    if "exits" not in simulation or "visualization" not in simulation["exits"]:
        raise HTTPException(status_code=404, detail="Exit visualization data not found")

    return ExitVisualizationResponse(**simulation["exits"]["visualization"])


@router.get("/{simulation_id}/exits/statistics", response_model=ExitStatisticsResponse)
async def get_exit_statistics(simulation_id: str) -> ExitStatisticsResponse:
    """
    Get statistics for exits.

    Args:
        simulation_id: Simulation ID

    Returns:
        Statistics data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has exit statistics data
    if "exits" not in simulation or "statistics" not in simulation["exits"]:
        raise HTTPException(status_code=404, detail="Exit statistics data not found")

    return ExitStatisticsResponse(**simulation["exits"]["statistics"])


@router.post("/{simulation_id}/exits/loan-exit", response_model=LoanExitResponse)
async def calculate_loan_exit(
    simulation_id: str,
    request: LoanExitRequest
) -> LoanExitResponse:
    """
    Calculate exit value for a specific loan.

    Args:
        simulation_id: Simulation ID
        request: Loan exit request

    Returns:
        Loan exit value
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has price path data
    if "price_paths" not in simulation:
        raise HTTPException(status_code=404, detail="Price path data not found")

    # Get price paths
    price_paths = simulation["price_paths"]

    # Convert exit type string to enum
    try:
        exit_type = ExitType(request.exit_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid exit type: {request.exit_type}")

    # Create loan dictionary
    loan = {
        "loan_id": request.loan_id,
        "property_id": request.property_id,
        "suburb_id": request.suburb_id,
        "zone": request.zone,
        "loan_amount": request.loan_amount,
        "property_value": request.property_value,
    }

    # Calculate exit value
    exit_value, appreciation_share_amount = calculate_exit_value(
        loan=loan,
        exit_month=request.exit_month,
        exit_type=exit_type,
        price_paths=price_paths,
        appreciation_share=0.2,  # Default value
        min_appreciation_share=0.1,  # Default value
        max_appreciation_share=0.5,  # Default value
        tiered_appreciation_thresholds=[0.2, 0.5, 1.0],  # Default values
        tiered_appreciation_shares=[0.1, 0.2, 0.3, 0.4],  # Default values
        recovery_rate=0.8,  # Default value
        foreclosure_cost=0.1,  # Default value
    )

    # Get current property value
    from src.price_path.enhanced_price_path import calculate_enhanced_property_value
    current_value = calculate_enhanced_property_value(
        initial_value=request.property_value,
        price_paths=price_paths,
        zone=request.zone,
        suburb_id=request.suburb_id,
        property_id=request.property_id,
        month=request.exit_month,
    )

    # Calculate appreciation
    appreciation = (current_value / request.property_value) - 1.0

    # Calculate exit year
    exit_year = request.exit_month / 12.0

    # Calculate ROI
    roi = (exit_value + appreciation_share_amount - request.loan_amount) / request.loan_amount

    # Calculate annualized ROI
    annualized_roi = ((exit_value + appreciation_share_amount) / request.loan_amount) ** (1 / exit_year) - 1 if exit_year > 0 else 0

    return LoanExitResponse(
        loan_id=request.loan_id,
        property_id=request.property_id,
        loan_amount=request.loan_amount,
        property_value=request.property_value,
        current_value=current_value,
        appreciation=appreciation,
        exit_month=request.exit_month,
        exit_year=exit_year,
        exit_type=request.exit_type,
        exit_value=exit_value,
        appreciation_share_amount=appreciation_share_amount,
        total_return=exit_value + appreciation_share_amount,
        roi=roi,
        annualized_roi=annualized_roi,
    )


@router.post("/{simulation_id}/exits/scenario")
async def run_exit_scenario(
    simulation_id: str,
    request: ExitScenarioRequest
) -> Dict[str, Any]:
    """
    Run an exit scenario with custom parameters.

    Args:
        simulation_id: Simulation ID
        request: Exit scenario request

    Returns:
        Exit scenario results
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
    context.config.exit_simulator = {
        "base_exit_rate": request.base_exit_rate,
        "time_factor": request.time_factor,
        "price_factor": request.price_factor,
        "min_hold_period": request.min_hold_period,
        "max_hold_period": request.max_hold_period,
        "sale_weight": request.sale_weight,
        "refinance_weight": request.refinance_weight,
        "default_weight": request.default_weight,
        "appreciation_sale_multiplier": request.appreciation_sale_multiplier,
        "interest_rate_refinance_multiplier": request.interest_rate_refinance_multiplier,
        "economic_factor_default_multiplier": request.economic_factor_default_multiplier,
        "appreciation_share": request.appreciation_share,
        "min_appreciation_share": request.min_appreciation_share,
        "max_appreciation_share": request.max_appreciation_share,
        "tiered_appreciation_thresholds": request.tiered_appreciation_thresholds,
        "tiered_appreciation_shares": request.tiered_appreciation_shares,
        "base_default_rate": request.base_default_rate,
        "recovery_rate": request.recovery_rate,
        "foreclosure_cost": request.foreclosure_cost,
        "foreclosure_time": request.foreclosure_time,
    }

    # Run exit simulation
    try:
        await simulate_exits(context)

        # Get exit summary
        summary = await get_exit_summary(context)

        # Update simulation data
        simulation["exits"] = summary

        return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
