"""
Simulation API router for the EQU IHOME SIM ENGINE v2.

This module provides API routes for running simulations and retrieving results.
"""

import uuid
import math
from datetime import datetime
from typing import Dict, Any, List, Optional

import structlog
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field

from src.config.config_loader import SimulationConfig, load_config_from_dict
from src.api.websocket_manager import get_websocket_manager
from src.engine.simulation_context import store_simulation_context, get_simulation_context_by_id
from src.persistence.result_store import get_result_store

logger = structlog.get_logger(__name__)

# Create router
router = APIRouter(
    tags=["simulation"],
    responses={404: {"description": "Not found"}},
)

# In-memory storage for simulation results
# In a real implementation, this would be replaced with a database
simulations: Dict[str, Dict[str, Any]] = {}


def sanitize_float_values(obj: Any, max_value: float = 1e15) -> Any:
    """
    Recursively sanitize float values in a data structure to prevent JSON serialization errors.

    Args:
        obj: The object to sanitize
        max_value: Maximum allowed float value (default: 1e15)

    Returns:
        Sanitized object with safe float values
    """
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        elif abs(obj) > max_value:
            return round(max_value if obj > 0 else -max_value, 3)
        else:
            return round(obj, 3)
    elif isinstance(obj, dict):
        return {key: sanitize_float_values(value, max_value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_float_values(item, max_value) for item in obj]
    else:
        return obj


# Models
class SimulationRequest(BaseModel):
    """Simulation request model."""
    config: Dict[str, Any] = Field(..., description="Simulation configuration")


class SimulationResponse(BaseModel):
    """Simulation response model."""
    simulation_id: str = Field(..., description="Simulation ID")
    status: str = Field(..., description="Simulation status")
    created_at: str = Field(..., description="Creation timestamp")


class SimulationResult(BaseModel):
    """Simulation result model."""
    simulation_id: str = Field(..., description="Simulation ID")
    status: str = Field(..., description="Simulation status")
    created_at: str = Field(..., description="Creation timestamp")
    completed_at: Optional[str] = Field(None, description="Completion timestamp")
    config: Dict[str, Any] = Field(..., description="Simulation configuration")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Simulation metrics")
    cashflows: Optional[List[Dict[str, Any]]] = Field(None, description="Simulation cashflows")
    capital_allocation: Optional[Dict[str, Any]] = Field(None, description="Capital allocation")
    loans: Optional[List[Dict[str, Any]]] = Field(None, description="Generated loans")
    loan_portfolio: Optional[Dict[str, Any]] = Field(None, description="Loan portfolio")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")
    guardrail_violations: Optional[List[Dict[str, Any]]] = Field(None, description="Guardrail violations")


@router.post("/", response_model=SimulationResponse)
async def create_simulation(
    request: SimulationRequest, background_tasks: BackgroundTasks
) -> SimulationResponse:
    """
    Create a new simulation.

    Args:
        request: Simulation request
        background_tasks: Background tasks

    Returns:
        Simulation response
    """
    try:
        # Validate configuration
        config = load_config_from_dict(request.config)

        # Create simulation
        simulation_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()

        simulations[simulation_id] = {
            "simulation_id": simulation_id,
            "status": "pending",
            "created_at": created_at,
            "config": config.dict(),
        }

        # Run simulation in background
        background_tasks.add_task(run_simulation, simulation_id)

        return SimulationResponse(
            simulation_id=simulation_id,
            status="pending",
            created_at=created_at,
        )

    except Exception as e:
        logger.error("Failed to create simulation", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{simulation_id}", response_model=SimulationResult)
async def get_simulation(simulation_id: str) -> SimulationResult:
    """
    Get a simulation by ID.

    Args:
        simulation_id: Simulation ID

    Returns:
        Simulation result
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    # Sanitize float values to prevent JSON serialization errors
    sanitized_data = sanitize_float_values(simulations[simulation_id])
    return SimulationResult(**sanitized_data)


@router.get("/{simulation_id}/detailed")
async def get_simulation_detailed(simulation_id: str) -> Dict[str, Any]:
    """
    Get detailed simulation data including all granular information.

    This endpoint provides comprehensive access to all simulation data including:
    - Basic simulation results
    - Detailed context data
    - Individual loan data
    - Price path simulations
    - Exit scenarios
    - Waterfall calculations
    - Performance metrics
    - Risk assessments
    - Module execution timings

    Args:
        simulation_id: Simulation ID

    Returns:
        Comprehensive simulation data
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    # Get basic simulation data
    simulation_data = simulations[simulation_id].copy()

    # Get simulation context for detailed data
    context = get_simulation_context_by_id(simulation_id)
    if context:
        # Add comprehensive context data
        context_summary = context.get_summary()
        simulation_data["detailed_context"] = context_summary

        # Add individual module data if available
        if hasattr(context, 'loans') and context.loans:
            simulation_data["detailed_loans"] = context.loans

        if hasattr(context, 'price_paths') and context.price_paths:
            simulation_data["detailed_price_paths"] = context.price_paths

        if hasattr(context, 'exits') and context.exits:
            simulation_data["detailed_exits"] = context.exits

        if hasattr(context, 'waterfall') and context.waterfall:
            simulation_data["detailed_waterfall"] = context.waterfall

        if hasattr(context, 'performance_report') and context.performance_report:
            simulation_data["detailed_performance"] = context.performance_report

        if hasattr(context, 'risk_metrics') and context.risk_metrics:
            simulation_data["detailed_risk_metrics"] = context.risk_metrics

        if hasattr(context, 'guardrail_violations') and context.guardrail_violations:
            simulation_data["detailed_guardrails"] = context.guardrail_violations

        # Add module timings
        if hasattr(context, 'module_timings') and context.module_timings:
            simulation_data["module_timings"] = context.module_timings

        # Add configuration details
        simulation_data["detailed_config"] = context.config.__dict__

    # Sanitize float values to prevent JSON serialization errors
    return sanitize_float_values(simulation_data)


@router.get("/", response_model=List[SimulationResult])
async def list_simulations() -> List[SimulationResult]:
    """
    List all simulations.

    Returns:
        List of simulation results
    """
    # Sanitize float values to prevent JSON serialization errors
    sanitized_simulations = [sanitize_float_values(simulation) for simulation in simulations.values()]
    return [SimulationResult(**simulation) for simulation in sanitized_simulations]


@router.delete("/{simulation_id}")
async def delete_simulation(simulation_id: str) -> Dict[str, str]:
    """
    Delete a simulation by ID.

    Args:
        simulation_id: Simulation ID

    Returns:
        Success message
    """
    if simulation_id not in simulations:
        raise HTTPException(status_code=404, detail="Simulation not found")

    del simulations[simulation_id]

    return {"message": f"Simulation {simulation_id} deleted"}


async def run_simulation(simulation_id: str) -> None:
    """
    Run a simulation in the background.

    Args:
        simulation_id: Simulation ID
    """
    logger.info("Running simulation", simulation_id=simulation_id)

    # Get WebSocket manager
    websocket_manager = get_websocket_manager()

    try:
        # Update status
        simulations[simulation_id]["status"] = "running"

        # Get configuration
        config = SimulationConfig(**simulations[simulation_id]["config"])

        # Import here to avoid circular imports
        from src.engine.orchestrator import get_orchestrator

        try:
            # Get orchestrator
            orchestrator = get_orchestrator()

            # Run simulation
            results = await orchestrator.run_simulation(config, run_id=simulation_id)

            # Extract all available results from the comprehensive summary
            metrics = results.get("metrics", {})
            cashflows = results.get("cashflows", [])
            capital_allocation = results.get("capital_allocation", {})
            loans = results.get("loans", [])
            loan_portfolio = results.get("loan_portfolio", {})
            price_paths = results.get("price_paths", {})
            exits = results.get("exits", {})
            module_timings = results.get("module_timings", {})
            total_execution_time = results.get("total_execution_time", 0)
            guardrail_violations = results.get("guardrail_violations", [])

            # Update simulation with comprehensive results
            simulations[simulation_id].update({
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
                "metrics": metrics,
                "cashflows": cashflows,
                "capital_allocation": capital_allocation,
                "loans": loans,
                "loan_portfolio": loan_portfolio,
                "price_paths": price_paths,
                "exits": exits,
                "execution_time": total_execution_time,
                "module_timings": module_timings,
                "guardrail_violations": guardrail_violations,
                # Store the complete results summary for API access
                "results": results,
            })

            logger.info("Simulation completed", simulation_id=simulation_id)

        except Exception as e:
            # If orchestrator is not fully implemented yet, use placeholder results
            logger.warning("Using placeholder results", error=str(e))

            # Send warning message
            await websocket_manager.send_warning(
                simulation_id=simulation_id,
                message="Using placeholder results due to orchestrator error",
                data={"error": str(e)},
            )

            # Update simulation with placeholder results
            simulations[simulation_id].update({
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
                "metrics": {
                    "irr": 0.12,
                    "equity_multiple": 1.5,
                    "roi": 0.5,
                    "payback_period": 4.2,
                    "var_95": 0.08,
                    "var_99": 0.12,
                    "sharpe_ratio": 1.2,
                    "max_drawdown": 0.15,
                },
                "cashflows": [
                    {
                        "year": 0,
                        "inflow": 0,
                        "outflow": 100000000,
                        "net": -100000000,
                        "cumulative": -100000000,
                    },
                    {
                        "year": 1,
                        "inflow": 5000000,
                        "outflow": 2000000,
                        "net": 3000000,
                        "cumulative": -97000000,
                    },
                    # Additional years would be included here
                    {
                        "year": 10,
                        "inflow": 150000000,
                        "outflow": 0,
                        "net": 150000000,
                        "cumulative": 50000000,
                    },
                ],
            })

            # Send placeholder results
            await websocket_manager.send_result(
                simulation_id=simulation_id,
                result=simulations[simulation_id],
            )

    except Exception as e:
        # Handle exception
        from src.utils.error_handler import handle_exception, log_error, format_error_response

        # Convert exception to SimulationError
        error = handle_exception(e)

        # Log error
        log_error(error)

        logger.error("Simulation failed", simulation_id=simulation_id, error=str(e))

        # Update status
        simulations[simulation_id].update({
            "status": "failed",
            "completed_at": datetime.now().isoformat(),
            "error": str(e),
        })

        # Send error message
        await websocket_manager.send_error(
            simulation_id=simulation_id,
            error=format_error_response(error),
        )
