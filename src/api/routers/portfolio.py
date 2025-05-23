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


class LeverageFacility(BaseModel):
    """Leverage facility model."""
    facility_id: str = Field(..., description="Facility ID")
    facility_type: str = Field(..., description="Facility type (nav_line, subscription_line)")
    max_amount: float = Field(..., description="Maximum facility amount")
    interest_rate: float = Field(..., description="Annual interest rate (as a decimal)")
    commitment_fee_bps: float = Field(..., description="Commitment fee on undrawn balance (basis points)")
    term_years: float = Field(..., description="Term of the facility in years")
    advance_rate: Optional[float] = Field(None, description="Maximum advance rate (for NAV lines)")
    current_balance: float = Field(..., description="Current outstanding balance")
    available_amount: float = Field(..., description="Available amount to draw")
    inception_date: Optional[str] = Field(None, description="Date when the facility was first drawn")
    maturity_date: Optional[str] = Field(None, description="Date when the facility matures")


class LeverageEvent(BaseModel):
    """Leverage event model."""
    facility_id: str = Field(..., description="Facility ID")
    date: str = Field(..., description="Date of the event")
    amount: float = Field(..., description="Amount of the event")
    year: float = Field(..., description="Simulation year")
    month: int = Field(..., description="Month (1-12)")
    event_type: str = Field(..., description="Event type (draw, repayment, interest, fee)")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")


class LeverageMetrics(BaseModel):
    """Leverage metrics model."""
    total_debt: float = Field(..., description="Total debt outstanding")
    total_available: float = Field(..., description="Total available debt capacity")
    total_interest_paid: float = Field(..., description="Total interest paid")
    total_commitment_fees_paid: float = Field(..., description="Total commitment fees paid")
    weighted_avg_interest_rate: float = Field(..., description="Weighted average interest rate")
    leverage_ratio: float = Field(..., description="Leverage ratio (debt / NAV)")
    debt_service_coverage_ratio: float = Field(..., description="Debt service coverage ratio")
    interest_coverage_ratio: float = Field(..., description="Interest coverage ratio")
    loan_to_value_ratio: float = Field(..., description="Loan-to-value ratio")


class LeverageVisualization(BaseModel):
    """Leverage visualization model."""
    leverage_timeline: List[Dict[str, Any]] = Field(..., description="Timeline of leverage")
    facility_utilization: List[Dict[str, Any]] = Field(..., description="Facility utilization over time")
    interest_expense: List[Dict[str, Any]] = Field(..., description="Interest expense over time")


class StressTestResult(BaseModel):
    """Stress test result model."""
    is_compliant: bool = Field(..., description="Whether the test is compliant")
    details: Dict[str, Any] = Field(..., description="Test details")


class LeverageResponse(BaseModel):
    """Leverage response model."""
    facilities: List[LeverageFacility] = Field(..., description="Debt facilities")
    metrics: LeverageMetrics = Field(..., description="Leverage metrics")
    visualization: LeverageVisualization = Field(..., description="Visualization data")
    stress_test_results: Optional[Dict[str, StressTestResult]] = Field(None, description="Stress test results")


class VisualizationResponse(BaseModel):
    """Visualization response model."""
    capital_allocation: Optional[Dict[str, Any]] = Field(None, description="Capital allocation visualization")
    loan_portfolio: Optional[Dict[str, Any]] = Field(None, description="Loan portfolio visualization")
    allocation_history: Optional[Dict[str, Any]] = Field(None, description="Allocation history visualization")
    loan_portfolio_history: Optional[Dict[str, Any]] = Field(None, description="Loan portfolio history visualization")
    leverage: Optional[Dict[str, Any]] = Field(None, description="Leverage visualization")


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

    # Add leverage visualization if available
    if "leverage" in simulation and "visualization" in simulation["leverage"]:
        visualizations["leverage"] = simulation["leverage"]["visualization"]

    return VisualizationResponse(**visualizations)


@router.get("/{simulation_id}/leverage", response_model=LeverageResponse)
async def get_leverage(simulation_id: str) -> LeverageResponse:
    """
    Get leverage data for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Leverage data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has leverage data
    if "context" not in simulation:
        raise HTTPException(status_code=404, detail="Simulation context not found")

    context = simulation["context"]

    # Check if leverage is enabled
    if not hasattr(context, "leverage_facilities"):
        raise HTTPException(status_code=404, detail="Leverage not enabled for this simulation")

    # Get facilities
    facilities = []
    for facility_id, facility_data in context.leverage_facilities.items():
        facilities.append({
            "facility_id": facility_id,
            **facility_data,
        })

    # Get metrics
    metrics = getattr(context, "leverage_metrics", {})

    # Get visualization data
    visualization = {}

    # Check if leverage visualization is available
    if hasattr(context, "leverage_visualization"):
        visualization = context.leverage_visualization
    else:
        # Calculate visualization data manually
        visualization = {
            "leverage_timeline": getattr(context, "leverage_timeline", []),
            "facility_utilization": getattr(context, "facility_utilization", []),
            "interest_expense": [],
        }

        # Calculate interest expense over time
        interest_payments = getattr(context, "leverage_interest_payments", [])
        commitment_fees = getattr(context, "leverage_commitment_fees", [])

        # Group by year and month
        interest_by_period = {}
        for payment in interest_payments:
            year = payment.get("year", 0)
            month = payment.get("month", 0)
            key = (year, month)

            if key not in interest_by_period:
                interest_by_period[key] = {
                    "year": year,
                    "month": month,
                    "interest_amount": 0,
                    "commitment_fees": 0,
                    "total_expense": 0,
                }

            interest_by_period[key]["interest_amount"] += payment.get("amount", 0)
            interest_by_period[key]["total_expense"] += payment.get("amount", 0)

        for fee in commitment_fees:
            year = fee.get("year", 0)
            month = fee.get("month", 0)
            key = (year, month)

            if key not in interest_by_period:
                interest_by_period[key] = {
                    "year": year,
                    "month": month,
                    "interest_amount": 0,
                    "commitment_fees": 0,
                    "total_expense": 0,
                }

            interest_by_period[key]["commitment_fees"] += fee.get("amount", 0)
            interest_by_period[key]["total_expense"] += fee.get("amount", 0)

        # Convert to list and sort by year and month
        interest_expense = sorted(
            interest_by_period.values(),
            key=lambda x: (x["year"], x["month"])
        )

        visualization["interest_expense"] = interest_expense

    # Get stress test results
    stress_test_results = None
    if hasattr(context, "leverage_stress_test_results"):
        raw_results = context.leverage_stress_test_results
        stress_test_results = {}

        # Convert raw results to API model
        for test_name, test_data in raw_results.items():
            is_compliant = test_data.get("is_compliant", False)
            details = {k: v for k, v in test_data.items() if k != "is_compliant"}
            stress_test_results[test_name] = {
                "is_compliant": is_compliant,
                "details": details
            }

    return LeverageResponse(
        facilities=facilities,
        metrics=metrics,
        visualization=visualization,
        stress_test_results=stress_test_results,
    )


@router.get("/{simulation_id}/leverage/facilities", response_model=List[LeverageFacility])
async def get_leverage_facilities(simulation_id: str) -> List[LeverageFacility]:
    """
    Get leverage facilities for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Leverage facilities
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has leverage data
    if "context" not in simulation:
        raise HTTPException(status_code=404, detail="Simulation context not found")

    context = simulation["context"]

    # Check if leverage is enabled
    if not hasattr(context, "leverage_facilities"):
        raise HTTPException(status_code=404, detail="Leverage not enabled for this simulation")

    # Get facilities
    facilities = []
    for facility_id, facility_data in context.leverage_facilities.items():
        facilities.append({
            "facility_id": facility_id,
            **facility_data,
        })

    return facilities


@router.get("/{simulation_id}/leverage/events", response_model=List[LeverageEvent])
async def get_leverage_events(
    simulation_id: str,
    event_type: Optional[str] = Query(None, description="Filter by event type (draw, repayment, interest, fee)"),
    facility_id: Optional[str] = Query(None, description="Filter by facility ID"),
) -> List[LeverageEvent]:
    """
    Get leverage events for a simulation.

    Args:
        simulation_id: Simulation ID
        event_type: Filter by event type (draw, repayment, interest, fee)
        facility_id: Filter by facility ID

    Returns:
        Leverage events
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has leverage data
    if "context" not in simulation:
        raise HTTPException(status_code=404, detail="Simulation context not found")

    context = simulation["context"]

    # Check if leverage is enabled
    if not hasattr(context, "leverage_facilities"):
        raise HTTPException(status_code=404, detail="Leverage not enabled for this simulation")

    # Get events
    events = []

    # Add draws
    draws = getattr(context, "leverage_draws", [])
    for draw in draws:
        if facility_id and draw.get("facility_id") != facility_id:
            continue

        if event_type and event_type != "draw":
            continue

        events.append({
            **draw,
            "event_type": "draw",
            "details": {
                "purpose": draw.get("purpose", ""),
            },
        })

    # Add repayments
    repayments = getattr(context, "leverage_repayments", [])
    for repayment in repayments:
        if facility_id and repayment.get("facility_id") != facility_id:
            continue

        if event_type and event_type != "repayment":
            continue

        events.append({
            **repayment,
            "event_type": "repayment",
            "details": {
                "source": repayment.get("source", ""),
            },
        })

    # Add interest payments
    interest_payments = getattr(context, "leverage_interest_payments", [])
    for payment in interest_payments:
        if facility_id and payment.get("facility_id") != facility_id:
            continue

        if event_type and event_type != "interest":
            continue

        events.append({
            **payment,
            "event_type": "interest",
            "details": {
                "interest_rate": payment.get("interest_rate", 0),
                "average_balance": payment.get("average_balance", 0),
                "period_start": payment.get("period_start", ""),
                "period_end": payment.get("period_end", ""),
            },
        })

    # Add commitment fees
    commitment_fees = getattr(context, "leverage_commitment_fees", [])
    for fee in commitment_fees:
        if facility_id and fee.get("facility_id") != facility_id:
            continue

        if event_type and event_type != "fee":
            continue

        events.append({
            **fee,
            "event_type": "fee",
            "details": {
                "fee_rate_bps": fee.get("fee_rate_bps", 0),
                "average_undrawn": fee.get("average_undrawn", 0),
                "period_start": fee.get("period_start", ""),
                "period_end": fee.get("period_end", ""),
            },
        })

    # Sort events by year and month
    events.sort(key=lambda x: (x["year"], x["month"]))

    return events


@router.get("/{simulation_id}/leverage/metrics", response_model=LeverageMetrics)
async def get_leverage_metrics(simulation_id: str) -> LeverageMetrics:
    """
    Get leverage metrics for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Leverage metrics
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    simulation = simulations[simulation_id]

    # Check if simulation has leverage data
    if "context" not in simulation:
        raise HTTPException(status_code=404, detail="Simulation context not found")

    context = simulation["context"]

    # Check if leverage is enabled
    if not hasattr(context, "leverage_metrics"):
        raise HTTPException(status_code=404, detail="Leverage not enabled for this simulation")

    # Get metrics
    metrics = getattr(context, "leverage_metrics", {})

    return LeverageMetrics(**metrics)
