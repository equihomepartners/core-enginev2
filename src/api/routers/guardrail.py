"""
Guardrail API router for the EQU IHOME SIM ENGINE v2.

This module provides API endpoints for guardrail monitoring.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Path, HTTPException, status
from pydantic import BaseModel, Field

import structlog

from src.engine.simulation_context import SimulationContext, get_simulation_context
from src.risk.guardrail_monitor import GuardrailMonitor, Breach, Severity, GuardrailReport
from src.api.websocket_manager import get_websocket_manager
from src.utils.error_handler import handle_exception

# Set up logging
logger = structlog.get_logger(__name__)

# Create router
router = APIRouter(
    prefix="/guardrail",
    tags=["guardrail"],
)


class BreachModel(BaseModel):
    """
    Breach model.
    
    Attributes:
        code: Breach code
        severity: Breach severity
        message: Breach message
        value: Actual value that triggered the breach
        threshold: Threshold value that was breached
        unit: Unit of measurement
        layer: Layer where the breach occurred (Unit, Zone, Portfolio, etc.)
    """
    
    code: str = Field(..., description="Breach code")
    severity: str = Field(..., description="Breach severity (INFO, WARN, FAIL)")
    message: str = Field(..., description="Breach message")
    value: Optional[float] = Field(None, description="Actual value that triggered the breach")
    threshold: Optional[float] = Field(None, description="Threshold value that was breached")
    unit: Optional[str] = Field(None, description="Unit of measurement")
    layer: Optional[str] = Field(None, description="Layer where the breach occurred (Unit, Zone, Portfolio, etc.)")


class GuardrailReportModel(BaseModel):
    """
    Guardrail report model.
    
    Attributes:
        simulation_id: Simulation ID
        worst_level: Worst severity level in the report
        breaches: List of breaches
    """
    
    simulation_id: Optional[str] = Field(None, description="Simulation ID")
    worst_level: str = Field(..., description="Worst severity level in the report (INFO, WARN, FAIL)")
    breaches: List[BreachModel] = Field(default_factory=list, description="List of breaches")


class GuardrailRequest(BaseModel):
    """
    Guardrail request model.
    
    Attributes:
        simulation_id: Simulation ID
    """
    
    simulation_id: str = Field(..., description="Simulation ID")


@router.post("/evaluate", response_model=GuardrailReportModel)
async def evaluate_guardrails(
    request: GuardrailRequest,
    context: SimulationContext = Depends(get_simulation_context),
) -> Dict[str, Any]:
    """
    Evaluate guardrails for a simulation.
    
    This endpoint evaluates guardrails for a simulation, checking that key risk metrics
    stay within acceptable bounds. It is non-blocking, meaning that it reports violations
    but does not stop the simulation.
    
    The guardrails are organized into the following categories:
    
    - **Property/Loan Level**: Stress LTV, loan size, exit month
    - **Zone Level**: Zone NAV weight, default rate, price volatility
    - **Portfolio Level**: Suburb concentration, loan concentration, NAV utilization,
      interest coverage, liquidity buffer, WAL, VaR, CVaR, IRR P5, hurdle-clear probability
    - **Model/Process**: Schema version, Monte Carlo paths, seed reproducibility
    
    Args:
        request: Guardrail evaluation request
        context: Simulation context
    
    Returns:
        Guardrail report with breaches
    """
    try:
        # Check if simulation ID matches context
        if request.simulation_id != context.run_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Simulation ID {request.simulation_id} does not match context {context.run_id}",
            )
        
        # Create guardrail monitor
        guardrail_monitor = GuardrailMonitor(context)
        
        # Evaluate guardrails
        report = await guardrail_monitor.evaluate_guardrails()
        
        # Convert to response model
        response = report.to_dict()
        
        return response
    except Exception as e:
        handle_exception(e, logger)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{simulation_id}", response_model=GuardrailReportModel)
async def get_guardrail_report(
    simulation_id: str = Path(..., description="Simulation ID"),
    context: SimulationContext = Depends(get_simulation_context),
) -> Dict[str, Any]:
    """
    Get guardrail report for a simulation.
    
    This endpoint retrieves the guardrail report for a simulation.
    
    Args:
        simulation_id: Simulation ID
        context: Simulation context
    
    Returns:
        Guardrail report with breaches
    """
    try:
        # Check if simulation ID matches context
        if simulation_id != context.run_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Simulation ID {simulation_id} does not match context {context.run_id}",
            )
        
        # Check if guardrail report exists
        if not hasattr(context, "guardrail_report"):
            # Create guardrail monitor and evaluate guardrails
            guardrail_monitor = GuardrailMonitor(context)
            report = await guardrail_monitor.evaluate_guardrails()
        else:
            # Use existing report
            report = context.guardrail_report
        
        # Convert to response model
        response = report.to_dict()
        
        return response
    except Exception as e:
        handle_exception(e, logger)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
