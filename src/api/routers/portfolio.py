"""
Portfolio API router for the EQU IHOME SIM ENGINE v2.

This module provides API routes for accessing capital allocation and loan generation data.
"""

import logging
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from src.api.routers.simulation import simulations

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/simulations",
    tags=["portfolio"],
    responses={404: {"description": "Not found"}},
)


# Models
class CapitalAllocation(BaseModel):
    """Capital allocation model."""
    zone_targets: Dict[str, float] = Field(..., description="Target zone allocations")
    zone_actual: Dict[str, float] = Field(..., description="Actual zone allocations")
    capital_by_zone: Optional[Dict[str, float]] = Field(None, description="Capital allocated by zone")
    allocation_stats: Optional[Dict[str, Any]] = Field(None, description="Allocation statistics")
    visualization: Optional[Dict[str, Any]] = Field(None, description="Visualization data")


class Loan(BaseModel):
    """Loan model."""
    loan_id: str = Field(..., description="Loan ID")
    loan_size: float = Field(..., description="Loan size")
    ltv: float = Field(..., description="Loan-to-value ratio")
    zone: str = Field(..., description="Zone category")
    term: float = Field(..., description="Loan term in years")
    interest_rate: float = Field(..., description="Interest rate")
    origination_year: int = Field(..., description="Origination year")
    property_value: float = Field(..., description="Property value")
    property_id: str = Field(..., description="Property ID")
    suburb_id: str = Field(..., description="Suburb ID")
    suburb_name: str = Field(..., description="Suburb name")
    property_type: Optional[str] = Field(None, description="Property type")
    bedrooms: Optional[int] = Field(None, description="Number of bedrooms")
    bathrooms: Optional[int] = Field(None, description="Number of bathrooms")
    land_size: Optional[float] = Field(None, description="Land size")
    building_size: Optional[float] = Field(None, description="Building size")
    year_built: Optional[int] = Field(None, description="Year built")


class LoanPortfolio(BaseModel):
    """Loan portfolio model."""
    stats: Optional[Dict[str, Any]] = Field(None, description="Portfolio statistics")
    visualization: Optional[Dict[str, Any]] = Field(None, description="Visualization data")


class LoansResponse(BaseModel):
    """Loans response model."""
    loans: List[Loan] = Field(..., description="List of loans")
    total_count: int = Field(..., description="Total number of loans")
    limit: int = Field(..., description="Maximum number of loans to return")
    offset: int = Field(..., description="Offset for pagination")


class VisualizationResponse(BaseModel):
    """Visualization response model."""
    capital_allocation: Optional[Dict[str, Any]] = Field(None, description="Capital allocation visualization")
    loan_portfolio: Optional[Dict[str, Any]] = Field(None, description="Loan portfolio visualization")
    allocation_history: Optional[Dict[str, Any]] = Field(None, description="Allocation history visualization")
    loan_portfolio_history: Optional[Dict[str, Any]] = Field(None, description="Loan portfolio history visualization")


class ReinvestmentRequest(BaseModel):
    """Reinvestment request model."""
    reinvestment_amount: float = Field(..., description="Amount to reinvest")
    target_zones: Dict[str, float] = Field(..., description="Target allocation by zone for reinvestment")
    year: float = Field(..., description="Current simulation year")


class ReinvestmentResponse(BaseModel):
    """Reinvestment response model."""
    loans: List[Loan] = Field(..., description="Generated reinvestment loans")
    total_loan_amount: float = Field(..., description="Total loan amount")
    num_loans: int = Field(..., description="Number of loans generated")


@router.get("/{simulation_id}/capital-allocation", response_model=CapitalAllocation)
async def get_capital_allocation(simulation_id: str) -> CapitalAllocation:
    """
    Get capital allocation data for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Capital allocation data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has capital allocation data
    if "capital_allocation" not in simulation:
        raise HTTPException(status_code=404, detail="Capital allocation data not found")

    return CapitalAllocation(**simulation["capital_allocation"])


@router.get("/{simulation_id}/loans", response_model=LoansResponse)
async def get_loans(
    simulation_id: str,
    zone: Optional[str] = Query(None, description="Filter by zone (green, orange, red)"),
    limit: int = Query(100, description="Maximum number of loans to return", ge=1, le=1000),
    offset: int = Query(0, description="Offset for pagination", ge=0)
) -> LoansResponse:
    """
    Get loans for a simulation.

    Args:
        simulation_id: Simulation ID
        zone: Filter by zone (green, orange, red)
        limit: Maximum number of loans to return
        offset: Offset for pagination

    Returns:
        Loans data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has loans data
    if "loans" not in simulation:
        raise HTTPException(status_code=404, detail="Loans data not found")

    loans = simulation["loans"]

    # Filter by zone if specified
    if zone:
        loans = [loan for loan in loans if loan.get("zone") == zone]

    # Apply pagination
    total_count = len(loans)
    loans = loans[offset:offset + limit]

    return LoansResponse(
        loans=loans,
        total_count=total_count,
        limit=limit,
        offset=offset,
    )


@router.get("/{simulation_id}/loan-portfolio", response_model=LoanPortfolio)
async def get_loan_portfolio(simulation_id: str) -> LoanPortfolio:
    """
    Get loan portfolio statistics and visualization data for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Loan portfolio data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has loan portfolio data
    if "loan_portfolio" not in simulation:
        raise HTTPException(status_code=404, detail="Loan portfolio data not found")

    return LoanPortfolio(**simulation["loan_portfolio"])


@router.get("/{simulation_id}/allocation-history")
async def get_allocation_history(simulation_id: str) -> Dict[str, Any]:
    """
    Get allocation history for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Allocation history data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has allocation history data
    if "capital_allocation" not in simulation or "allocation_history" not in simulation["capital_allocation"]:
        raise HTTPException(status_code=404, detail="Allocation history data not found")

    return {
        "allocation_history": simulation["capital_allocation"]["allocation_history"],
        "allocation_history_visualization": simulation["capital_allocation"].get("allocation_history_visualization", {}),
    }


@router.get("/{simulation_id}/loan-portfolio-history")
async def get_loan_portfolio_history(simulation_id: str) -> Dict[str, Any]:
    """
    Get loan portfolio history for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Loan portfolio history data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has loan portfolio history data
    if "loan_portfolio" not in simulation or "loan_portfolio_history" not in simulation["loan_portfolio"]:
        raise HTTPException(status_code=404, detail="Loan portfolio history data not found")

    return {
        "loan_portfolio_history": simulation["loan_portfolio"]["loan_portfolio_history"],
        "loan_portfolio_history_visualization": simulation["loan_portfolio"].get("loan_portfolio_history_visualization", {}),
    }


@router.post("/{simulation_id}/reinvest", response_model=ReinvestmentResponse)
async def reinvest(simulation_id: str, request: ReinvestmentRequest) -> ReinvestmentResponse:
    """
    Generate reinvestment loans for a simulation.

    Args:
        simulation_id: Simulation ID
        request: Reinvestment request

    Returns:
        Generated reinvestment loans
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has a context
    if "context" not in simulation:
        raise HTTPException(status_code=400, detail="Simulation context not found")

    # Get simulation context
    context = simulation["context"]

    # Import the generate_reinvestment_loans function
    from src.engine.loan_generator import generate_reinvestment_loans

    # Generate reinvestment loans
    try:
        loans = await generate_reinvestment_loans(
            context=context,
            reinvestment_amount=request.reinvestment_amount,
            target_zones=request.target_zones,
            year=request.year,
        )

        # Calculate total loan amount
        total_loan_amount = sum(loan.get("loan_size", 0.0) for loan in loans)

        # Add loans to existing loans
        context.loans.extend(loans)

        # Update actual allocation
        from src.capital_allocator import update_actual_allocation
        await update_actual_allocation(context, request.year)

        # Track loan portfolio history
        from src.engine.loan_generator import track_loan_portfolio_history
        track_loan_portfolio_history(context, request.year)

        # Return response
        return ReinvestmentResponse(
            loans=loans,
            total_loan_amount=total_loan_amount,
            num_loans=len(loans),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{simulation_id}/rebalancing-recommendation")
async def get_rebalancing_recommendation(
    simulation_id: str,
    tolerance: float = Query(0.05, description="Tolerance for allocation mismatch")
) -> Dict[str, Any]:
    """
    Get rebalancing recommendation for a simulation.

    Args:
        simulation_id: Simulation ID
        tolerance: Tolerance for allocation mismatch

    Returns:
        Rebalancing recommendation
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has a context
    if "context" not in simulation:
        raise HTTPException(status_code=400, detail="Simulation context not found")

    # Get simulation context
    context = simulation["context"]

    # Import the rebalance_allocation function
    from src.capital_allocator import rebalance_allocation

    # Get rebalancing recommendation
    try:
        adjustments = await rebalance_allocation(context, tolerance)

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

        # Calculate allocation gaps
        gaps = {zone: targets.get(zone, 0.0) - actual_pct.get(zone, 0.0) for zone in targets}

        # Get rebalancing visualization
        rebalancing_visualization = getattr(context, "rebalancing_visualization", {})

        # Return response
        return {
            "targets": targets,
            "actual": actual_pct,
            "gaps": gaps,
            "adjustments": adjustments,
            "rebalancing_visualization": rebalancing_visualization,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{simulation_id}/visualizations", response_model=VisualizationResponse)
async def get_visualizations(simulation_id: str) -> VisualizationResponse:
    """
    Get visualization data for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Visualization data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Collect visualization data from different modules
    visualizations = {}

    # Add capital allocation visualization if available
    if "capital_allocation" in simulation and "visualization" in simulation["capital_allocation"]:
        visualizations["capital_allocation"] = simulation["capital_allocation"]["visualization"]

    # Add loan portfolio visualization if available
    if "loan_portfolio" in simulation and "visualization" in simulation["loan_portfolio"]:
        visualizations["loan_portfolio"] = simulation["loan_portfolio"]["visualization"]

    # Add allocation history visualization if available
    if "capital_allocation" in simulation and "allocation_history_visualization" in simulation["capital_allocation"]:
        visualizations["allocation_history"] = simulation["capital_allocation"]["allocation_history_visualization"]

    # Add loan portfolio history visualization if available
    if "loan_portfolio" in simulation and "loan_portfolio_history_visualization" in simulation["loan_portfolio"]:
        visualizations["loan_portfolio_history"] = simulation["loan_portfolio"]["loan_portfolio_history_visualization"]

    return VisualizationResponse(**visualizations)
