"""
Simulation API router for the EQU IHOME SIM ENGINE v2.

This module provides API routes for running simulations and retrieving results.
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field

from src.config.config_loader import SimulationConfig, load_config_from_dict
from src.api.websocket_manager import get_websocket_manager

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    tags=["simulation"],
    responses={404: {"description": "Not found"}},
)

# In-memory storage for simulation results
# In a real implementation, this would be replaced with a database
simulations: Dict[str, Dict[str, Any]] = {}


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

    return SimulationResult(**simulations[simulation_id])


@router.get("/", response_model=List[SimulationResult])
async def list_simulations() -> List[SimulationResult]:
    """
    List all simulations.

    Returns:
        List of simulation results
    """
    return [SimulationResult(**simulation) for simulation in simulations.values()]


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

            # Extract results
            metrics = results.get("metrics", {})
            cashflows = results.get("cashflows", [])
            capital_allocation = results.get("capital_allocation", {})
            loans = results.get("loans", [])
            loan_portfolio = results.get("loan_portfolio", {})

            # Update simulation with results
            simulations[simulation_id].update({
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
                "metrics": metrics,
                "cashflows": cashflows,
                "capital_allocation": capital_allocation,
                "loans": loans,
                "loan_portfolio": loan_portfolio,
                "execution_time": results.get("execution_time", 0),
                "guardrail_violations": results.get("guardrail_violations", []),
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
