"""
Reinvestment API router for the EQU IHOME SIM ENGINE v2.

This module provides API endpoints for the reinvestment engine.
"""

import logging
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Set up logging
logger = logging.getLogger(__name__)

from src.reinvest_engine.reinvest_engine import (
    calculate_reinvestment_statistics,
    generate_reinvestment_visualization,
    ReinvestmentStrategy,
    ReinvestmentSource,
)

# In-memory storage for simulations
from src.api.routers.portfolio import simulations

router = APIRouter(
    prefix="/api/v1/simulations",
    tags=["reinvestment"],
)


class ReinvestmentEventResponse(BaseModel):
    """Reinvestment event response model."""
    event_id: str = Field(..., description="Unique identifier for the reinvestment event")
    timestamp: float = Field(..., description="Timestamp of the reinvestment event")
    year: float = Field(..., description="Simulation year of the reinvestment event")
    month: int = Field(..., description="Month of the reinvestment event (1-12)")
    amount: float = Field(..., description="Amount reinvested")
    source: str = Field(..., description="Source of the reinvestment capital")
    source_details: Dict[str, Any] = Field(..., description="Details about the source")
    strategy_used: str = Field(..., description="Reinvestment strategy used")
    target_allocations: Dict[str, float] = Field(..., description="Target zone allocations")
    actual_allocations: Dict[str, float] = Field(..., description="Actual zone allocations")
    num_loans_generated: int = Field(..., description="Number of loans generated")
    loan_ids: List[str] = Field(..., description="IDs of loans generated")
    performance_adjustments: Optional[Dict[str, float]] = Field(None, description="Performance adjustments")
    cash_reserve_before: Optional[float] = Field(None, description="Cash reserve before reinvestment")
    cash_reserve_after: Optional[float] = Field(None, description="Cash reserve after reinvestment")


class ReinvestmentEfficiencyResponse(BaseModel):
    """Reinvestment efficiency response model."""
    reinvestment_ratio: float = Field(..., description="Ratio of reinvested capital to total exit value")
    avg_time_to_reinvest: float = Field(..., description="Average time between exit and reinvestment in months")
    reinvestment_portfolio_impact: float = Field(..., description="Percentage of portfolio from reinvestment")


class ReinvestmentPerformanceResponse(BaseModel):
    """Reinvestment performance response model."""
    roi: float = Field(..., description="Return on investment for reinvested capital")
    avg_hold_period: float = Field(..., description="Average hold period for reinvestment loans in years")
    exit_type_distribution: Dict[str, float] = Field(..., description="Exit type distribution for reinvestment loans")


class CashReserveMetricsResponse(BaseModel):
    """Cash reserve metrics response model."""
    avg_cash_reserve: float = Field(..., description="Average cash reserve")
    min_cash_reserve: float = Field(..., description="Minimum cash reserve")
    max_cash_reserve: float = Field(..., description="Maximum cash reserve")
    avg_cash_reserve_pct: float = Field(..., description="Average cash reserve as percentage of fund size")
    min_cash_reserve_pct: float = Field(..., description="Minimum cash reserve as percentage of fund size")
    max_cash_reserve_pct: float = Field(..., description="Maximum cash reserve as percentage of fund size")


class ReinvestmentSummaryResponse(BaseModel):
    """Reinvestment summary response model."""
    total_reinvested: float = Field(..., description="Total amount reinvested")
    num_reinvestment_events: int = Field(..., description="Number of reinvestment events")
    avg_reinvestment_amount: float = Field(..., description="Average reinvestment amount")
    reinvestment_by_year: Dict[str, float] = Field(..., description="Reinvestment amounts by year")
    reinvestment_by_zone: Dict[str, float] = Field(..., description="Reinvestment amounts by zone")
    reinvestment_by_strategy: Dict[str, float] = Field(..., description="Reinvestment amounts by strategy")
    reinvestment_by_source: Dict[str, float] = Field(..., description="Reinvestment amounts by source")
    reinvestment_efficiency: Optional[ReinvestmentEfficiencyResponse] = Field(None, description="Reinvestment efficiency metrics")
    reinvestment_performance: Optional[ReinvestmentPerformanceResponse] = Field(None, description="Reinvestment performance metrics")
    reinvestment_timing: Optional[Dict[str, Dict[str, float]]] = Field(None, description="Reinvestment timing by year and quarter")
    cash_reserve_history: Optional[List[Dict[str, Any]]] = Field(None, description="Cash reserve history")
    cash_reserve_metrics: Optional[CashReserveMetricsResponse] = Field(None, description="Cash reserve metrics")


class ReinvestmentChartsResponse(BaseModel):
    """Reinvestment charts response model."""
    reinvestment_timeline: List[Dict[str, Any]] = Field(..., description="Timeline of reinvestment events")
    reinvestment_by_zone_chart: List[Dict[str, Any]] = Field(..., description="Reinvestment by zone chart")
    reinvestment_by_year_chart: List[Dict[str, Any]] = Field(..., description="Reinvestment by year chart")
    reinvestment_by_strategy_chart: List[Dict[str, Any]] = Field(..., description="Reinvestment by strategy chart")
    reinvestment_by_source_chart: List[Dict[str, Any]] = Field(..., description="Reinvestment by source chart")
    cash_reserve_chart: List[Dict[str, Any]] = Field(..., description="Cash reserve chart")
    allocation_comparison_chart: List[Dict[str, Any]] = Field(..., description="Allocation comparison chart")
    reinvestment_efficiency_chart: List[Dict[str, Any]] = Field(..., description="Reinvestment efficiency chart")
    reinvestment_performance_chart: List[Dict[str, Any]] = Field(..., description="Reinvestment performance chart")
    exit_type_distribution_chart: List[Dict[str, Any]] = Field(..., description="Exit type distribution chart")
    reinvestment_timing_chart: List[Dict[str, Any]] = Field(..., description="Reinvestment timing chart")
    reinvestment_vs_exits_chart: List[Dict[str, Any]] = Field(..., description="Reinvestment vs exits chart")
    loan_size_distribution_chart: List[Dict[str, Any]] = Field(..., description="Loan size distribution chart")


class ReinvestmentTablesResponse(BaseModel):
    """Reinvestment tables response model."""
    reinvestment_summary_table: List[Dict[str, Any]] = Field(..., description="Reinvestment summary table")
    reinvestment_events_table: List[Dict[str, Any]] = Field(..., description="Reinvestment events table")
    reinvestment_loans_table: List[Dict[str, Any]] = Field(..., description="Reinvestment loans table")
    cash_reserve_metrics_table: List[Dict[str, Any]] = Field(..., description="Cash reserve metrics table")


class RiskMetricsResponse(BaseModel):
    """Risk metrics response model."""
    zone_distribution_change: Dict[str, float] = Field(..., description="Change in zone distribution")
    avg_ltv_change: float = Field(..., description="Change in average LTV")
    concentration_risk_change: Dict[str, float] = Field(..., description="Change in concentration risk metrics")
    risk_score_before: float = Field(..., description="Risk score before reinvestment")
    risk_score_after: float = Field(..., description="Risk score after reinvestment")
    risk_score_change: float = Field(..., description="Change in risk score")
    diversification_impact: float = Field(..., description="Impact on portfolio diversification")
    risk_adjusted_return_impact: float = Field(..., description="Impact on risk-adjusted return")


class ReinvestmentKPIsResponse(BaseModel):
    """Reinvestment KPIs response model."""
    total_reinvested: float = Field(..., description="Total amount reinvested")
    num_reinvestment_events: int = Field(..., description="Number of reinvestment events")
    avg_reinvestment_amount: float = Field(..., description="Average reinvestment amount")
    reinvestment_ratio: float = Field(..., description="Ratio of reinvested capital to total exit value")
    avg_time_to_reinvest: float = Field(..., description="Average time between exit and reinvestment in months")
    reinvestment_roi: float = Field(..., description="Return on investment for reinvested capital")
    num_reinvestment_loans: int = Field(..., description="Number of reinvestment loans")
    reinvestment_portfolio_impact: float = Field(..., description="Percentage of portfolio from reinvestment")
    risk_metrics: Optional[RiskMetricsResponse] = Field(None, description="Risk impact metrics")


class ReinvestmentVisualizationResponse(BaseModel):
    """Reinvestment visualization response model."""
    charts: ReinvestmentChartsResponse = Field(..., description="Chart data for reinvestment")
    tables: ReinvestmentTablesResponse = Field(..., description="Table data for reinvestment")
    kpis: ReinvestmentKPIsResponse = Field(..., description="KPIs for reinvestment")


class ReinvestmentResponse(BaseModel):
    """Reinvestment response model."""
    events: List[ReinvestmentEventResponse] = Field(..., description="List of reinvestment events")
    summary: ReinvestmentSummaryResponse = Field(..., description="Summary of reinvestment activity")
    visualization: ReinvestmentVisualizationResponse = Field(..., description="Visualization data")


class ManualReinvestmentRequest(BaseModel):
    """Manual reinvestment request model."""
    amount: float = Field(..., description="Amount to reinvest")
    year: float = Field(..., description="Simulation year")
    month: int = Field(1, description="Month (1-12)")
    strategy: str = Field(ReinvestmentStrategy.REBALANCE, description="Reinvestment strategy")
    source: str = Field(ReinvestmentSource.EXIT, description="Source of the reinvestment capital")
    source_details: Optional[Dict[str, Any]] = Field({}, description="Details about the source")
    zone_preference_multipliers: Optional[Dict[str, float]] = Field(
        None, description="Zone preference multipliers"
    )
    enable_dynamic_allocation: Optional[bool] = Field(
        False, description="Whether to use dynamic allocation"
    )


@router.get("/{simulation_id}/reinvestment", response_model=ReinvestmentResponse)
async def get_reinvestment_data(simulation_id: str) -> ReinvestmentResponse:
    """
    Get reinvestment data for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Reinvestment data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    # Get simulation context
    context = simulations[simulation_id].get("context")
    if not context:
        raise HTTPException(status_code=404, detail="Simulation context not found")

    # Get reinvestment events
    reinvestment_events = getattr(context, "reinvestment_events", [])

    # Get reinvestment summary
    reinvestment_summary = getattr(context, "reinvestment_summary", None)
    if not reinvestment_summary:
        reinvestment_summary = calculate_reinvestment_statistics(context)

    # Get reinvestment visualization
    reinvestment_visualization = getattr(context, "reinvestment_visualization", None)
    if not reinvestment_visualization:
        reinvestment_visualization = generate_reinvestment_visualization(context)

    # Get risk metrics
    risk_metrics = None
    if hasattr(context, "reinvestment_risk_metrics") and context.reinvestment_risk_metrics:
        # Get the most recent risk metrics
        latest_risk_metrics = context.reinvestment_risk_metrics[-1]
        risk_metrics = latest_risk_metrics.get("risk_impact", {})

        # Add risk metrics to KPIs
        if "kpis" in reinvestment_visualization:
            reinvestment_visualization["kpis"]["risk_metrics"] = risk_metrics

    return ReinvestmentResponse(
        events=reinvestment_events,
        summary=reinvestment_summary,
        visualization=reinvestment_visualization,
    )


@router.get("/{simulation_id}/reinvestment/risk", response_model=List[Dict[str, Any]])
async def get_reinvestment_risk_metrics(simulation_id: str) -> List[Dict[str, Any]]:
    """
    Get reinvestment risk metrics for a simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        List of risk metrics for each reinvestment event
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    # Get simulation context
    context = simulations[simulation_id].get("context")
    if not context:
        raise HTTPException(status_code=404, detail="Simulation context not found")

    # Get risk metrics
    risk_metrics = getattr(context, "reinvestment_risk_metrics", [])

    return risk_metrics


@router.post("/{simulation_id}/reinvestment", response_model=ReinvestmentEventResponse)
async def manual_reinvestment(
    simulation_id: str, request: ManualReinvestmentRequest
) -> ReinvestmentEventResponse:
    """
    Manually trigger a reinvestment event.

    Args:
        simulation_id: Simulation ID
        request: Manual reinvestment request

    Returns:
        Reinvestment event details
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    # Get simulation context
    context = simulations[simulation_id].get("context")
    if not context:
        raise HTTPException(status_code=404, detail="Simulation context not found")

    # Check if amount is valid
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Reinvestment amount must be positive")

    # Check if year is valid
    if request.year < 0 or request.year > context.config.fund_term:
        raise HTTPException(
            status_code=400,
            detail=f"Year must be between 0 and {context.config.fund_term}",
        )

    # Check if month is valid
    if request.month < 1 or request.month > 12:
        raise HTTPException(status_code=400, detail="Month must be between 1 and 12")

    # Check if strategy is valid
    if request.strategy not in [s.value for s in ReinvestmentStrategy]:
        raise HTTPException(
            status_code=400,
            detail=f"Strategy must be one of {[s.value for s in ReinvestmentStrategy]}",
        )

    # Check if source is valid
    if request.source not in [s.value for s in ReinvestmentSource]:
        raise HTTPException(
            status_code=400,
            detail=f"Source must be one of {[s.value for s in ReinvestmentSource]}",
        )

    # Import the reinvest_amount function
    from src.reinvest_engine.reinvest_engine import reinvest_amount

    try:
        # Create source details
        source_details = request.source_details or {}

        # Apply zone preference multipliers if provided
        if request.zone_preference_multipliers:
            # Set zone preference multipliers in config
            context.config.reinvestment_engine = context.config.reinvestment_engine or {}
            context.config.reinvestment_engine["zone_preference_multipliers"] = request.zone_preference_multipliers

        # Apply dynamic allocation if requested
        if request.enable_dynamic_allocation:
            context.config.reinvestment_engine = context.config.reinvestment_engine or {}
            context.config.reinvestment_engine["enable_dynamic_allocation"] = True

        # Perform reinvestment
        reinvestment_event = await reinvest_amount(
            context=context,
            amount=request.amount,
            year=request.year,
            month=request.month,
            source=request.source,
            source_details=source_details,
        )

        # Return the reinvestment event
        return reinvestment_event

    except Exception as e:
        # Log the error
        logger.error("Manual reinvestment failed", error=str(e))

        # Raise HTTP exception
        raise HTTPException(
            status_code=500,
            detail=f"Manual reinvestment failed: {str(e)}",
        )
