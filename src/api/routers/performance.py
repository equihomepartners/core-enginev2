"""
Performance Reporter API router for the EQU IHOME SIM ENGINE v2.

This module provides API endpoints for generating and retrieving performance reports.
"""

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from src.engine.simulation_context import SimulationContext, get_simulation_context_by_id
from src.performance_reporter import generate_performance_report, ReportFormat
from src.utils.error_handler import handle_exception
import structlog

# Set up logging
logger = structlog.get_logger(__name__)

# Create router
router = APIRouter(
    prefix="/performance",
    tags=["performance"],
    responses={404: {"description": "Not found"}},
)


class PerformanceReportRequest(BaseModel):
    """
    Performance report request model.

    Attributes:
        simulation_id: Simulation ID
        include_kpi_table: Whether to include KPI table in the report
        include_zone_allocation: Whether to include zone allocation in the report
        include_cash_flow: Whether to include cash flow in the report
        include_risk_metrics: Whether to include risk metrics in the report
        include_tranche_performance: Whether to include tranche performance in the report
        include_loan_performance: Whether to include loan performance in the report
        include_visualization: Whether to include visualization data in the report
        export_format: Format to export the report to
        export_path: Path to export the report to
    """

    simulation_id: str = Field(..., description="Simulation ID")
    include_kpi_table: bool = Field(True, description="Whether to include KPI table in the report")
    include_zone_allocation: bool = Field(True, description="Whether to include zone allocation in the report")
    include_cash_flow: bool = Field(True, description="Whether to include cash flow in the report")
    include_risk_metrics: bool = Field(True, description="Whether to include risk metrics in the report")
    include_tranche_performance: bool = Field(True, description="Whether to include tranche performance in the report")
    include_loan_performance: bool = Field(True, description="Whether to include loan performance in the report")
    include_visualization: bool = Field(True, description="Whether to include visualization data in the report")
    export_format: str = Field("json", description="Format to export the report to (json, csv, excel, markdown, html)")
    export_path: str = Field("reports", description="Path to export the report to")


class PerformanceReportSummary(BaseModel):
    """
    Performance report summary model.

    Attributes:
        simulation_id: Simulation ID
        simulation_date: Simulation date
        fund_size: Fund size
        fund_term: Fund term
        hurdle_rate: Hurdle rate
        num_loans: Number of loans
        total_loan_amount: Total loan amount
        avg_ltv: Average LTV
        irr: IRR
        moic: MOIC
        tvpi: TVPI
        dpi: DPI
        rvpi: RVPI
        var_99: VaR (99%)
        sharpe_ratio: Sharpe ratio
        worst_guardrail_level: Worst guardrail level
    """

    simulation_id: str = Field(..., description="Simulation ID")
    simulation_date: str = Field(..., description="Simulation date")
    fund_size: float = Field(..., description="Fund size")
    fund_term: int = Field(..., description="Fund term")
    hurdle_rate: float = Field(..., description="Hurdle rate")
    num_loans: int = Field(..., description="Number of loans")
    total_loan_amount: float = Field(..., description="Total loan amount")
    avg_ltv: float = Field(..., description="Average LTV")
    irr: float = Field(..., description="IRR")
    moic: float = Field(..., description="MOIC")
    tvpi: float = Field(..., description="TVPI")
    dpi: float = Field(..., description="DPI")
    rvpi: float = Field(..., description="RVPI")
    var_99: float = Field(..., description="VaR (99%)")
    sharpe_ratio: float = Field(..., description="Sharpe ratio")
    worst_guardrail_level: str = Field(..., description="Worst guardrail level")


@router.post(
    "/generate",
    response_model=Dict[str, Any],
    summary="Generate performance report",
    description="Generates a comprehensive performance report for the simulation",
)
async def generate_report(request: PerformanceReportRequest) -> Dict[str, Any]:
    """
    Generate a performance report for the simulation.

    This endpoint generates a comprehensive performance report for the simulation,
    including KPI tables, zone allocation reports, cash flow visualizations,
    risk metric reports, and export capabilities.

    Args:
        request: Performance report request

    Returns:
        Performance report
    """
    try:
        # Get simulation context
        context = get_simulation_context_by_id(request.simulation_id)
        if not context:
            raise HTTPException(
                status_code=404,
                detail="Simulation context not found"
            )

        # Set report configuration
        context.config.performance_reporter = {
            "include_kpi_table": request.include_kpi_table,
            "include_zone_allocation": request.include_zone_allocation,
            "include_cash_flow": request.include_cash_flow,
            "include_risk_metrics": request.include_risk_metrics,
            "include_tranche_performance": request.include_tranche_performance,
            "include_loan_performance": request.include_loan_performance,
            "include_visualization": request.include_visualization,
            "export_format": request.export_format,
            "export_path": request.export_path,
        }

        # Generate performance report
        report = await generate_performance_report(context)

        return report
    except Exception as e:
        handle_exception(e, logger)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/{simulation_id}",
    response_model=Dict[str, Any],
    summary="Get performance report",
    description="Returns the performance report for the simulation",
)
async def get_report(simulation_id: str) -> Dict[str, Any]:
    """
    Get the performance report for the simulation.

    This endpoint returns the performance report for the simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Performance report
    """
    try:
        # Get simulation context
        context = get_simulation_context_by_id(simulation_id)
        if not context:
            raise HTTPException(
                status_code=404,
                detail="Simulation context not found"
            )

        # Check if performance report exists
        if not hasattr(context, "performance_report") or not context.performance_report:
            # Generate performance report
            report = await generate_performance_report(context)
        else:
            report = context.performance_report

        return report
    except Exception as e:
        handle_exception(e, logger)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get(
    "/{simulation_id}/summary",
    response_model=PerformanceReportSummary,
    summary="Get performance report summary",
    description="Returns the summary of the performance report for the simulation",
)
async def get_report_summary(simulation_id: str) -> PerformanceReportSummary:
    """
    Get the summary of the performance report for the simulation.

    This endpoint returns the summary of the performance report for the simulation.

    Args:
        simulation_id: Simulation ID

    Returns:
        Performance report summary
    """
    try:
        # Get simulation context
        context = get_simulation_context_by_id(simulation_id)
        if not context:
            raise HTTPException(
                status_code=404,
                detail="Simulation context not found"
            )

        # Check if performance report exists
        if not hasattr(context, "performance_report") or not context.performance_report:
            # Generate performance report
            report = await generate_performance_report(context)
        else:
            report = context.performance_report

        # Get summary
        summary = report.get("summary", {})

        # Add simulation ID
        summary["simulation_id"] = context.run_id

        return PerformanceReportSummary(**summary)
    except Exception as e:
        handle_exception(e, logger)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
