"""
Persistence API router for the EQU IHOME SIM ENGINE v2.

This module provides API endpoints for storing and retrieving simulation results.
"""

from typing import Dict, Any, List, Optional

import structlog
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from pydantic import BaseModel, Field

from src.persistence.result_store import get_result_store

logger = structlog.get_logger(__name__)

router = APIRouter(
    prefix="/api/v1/results",
    tags=["persistence"],
)


class ResultResponse(BaseModel):
    """Result response model."""
    simulation_id: str = Field(..., description="Simulation ID")
    status: str = Field(..., description="Simulation status")
    created_at: str = Field(..., description="Creation timestamp")
    completed_at: Optional[str] = Field(None, description="Completion timestamp")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Simulation metrics")
    execution_time: Optional[float] = Field(None, description="Execution time in seconds")
    num_loans: Optional[int] = Field(None, description="Number of loans")
    guardrail_violations: Optional[List[str]] = Field(None, description="Guardrail violations")


class ResultListResponse(BaseModel):
    """Result list response model."""
    results: List[ResultResponse] = Field(..., description="List of results")
    count: int = Field(..., description="Total count")
    limit: int = Field(..., description="Limit")
    offset: int = Field(..., description="Offset")


@router.get("/{simulation_id}", response_model=ResultResponse)
async def get_result(simulation_id: str) -> ResultResponse:
    """
    Get a simulation result by ID.

    Args:
        simulation_id: Simulation ID

    Returns:
        Simulation result
    """
    result_store = get_result_store()
    result = await result_store.get_result(simulation_id)

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    # Extract fields for response
    response = {
        "simulation_id": result.get("run_id", simulation_id),
        "status": result.get("status", "completed"),
        "created_at": result.get("created_at", ""),
        "completed_at": result.get("completed_at", None),
        "metrics": result.get("metrics", {}),
        "execution_time": result.get("execution_time", 0.0),
        "num_loans": result.get("num_loans", 0),
        "guardrail_violations": result.get("guardrail_violations", []),
    }

    return ResultResponse(**response)


@router.get("/", response_model=ResultListResponse)
async def list_results(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
) -> ResultListResponse:
    """
    List simulation results.

    Args:
        limit: Maximum number of results to return
        offset: Offset for pagination

    Returns:
        List of simulation results
    """
    result_store = get_result_store()
    results = await result_store.list_results(limit, offset)

    # Extract fields for response
    response_results = []
    for result in results:
        simulation_id = result.get("run_id", "")
        response = {
            "simulation_id": simulation_id,
            "status": result.get("status", "completed"),
            "created_at": result.get("created_at", ""),
            "completed_at": result.get("completed_at", None),
            "metrics": result.get("metrics", {}),
            "execution_time": result.get("execution_time", 0.0),
            "num_loans": result.get("num_loans", 0),
            "guardrail_violations": result.get("guardrail_violations", []),
        }
        response_results.append(ResultResponse(**response))

    return ResultListResponse(
        results=response_results,
        count=len(response_results),
        limit=limit,
        offset=offset,
    )


@router.delete("/{simulation_id}")
async def delete_result(simulation_id: str) -> Dict[str, Any]:
    """
    Delete a simulation result.

    Args:
        simulation_id: Simulation ID

    Returns:
        Success message
    """
    result_store = get_result_store()
    success = await result_store.delete_result(simulation_id)

    if not success:
        raise HTTPException(status_code=404, detail="Result not found")

    return {"message": "Result deleted", "simulation_id": simulation_id}


@router.post("/{simulation_id}/export")
async def export_result(
    simulation_id: str,
    background_tasks: BackgroundTasks,
) -> Dict[str, Any]:
    """
    Export a simulation result to a file.

    Args:
        simulation_id: Simulation ID
        background_tasks: Background tasks

    Returns:
        Export status
    """
    result_store = get_result_store()
    result = await result_store.get_result(simulation_id)

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    # Export result in background
    background_tasks.add_task(export_result_task, simulation_id, result)

    return {
        "message": "Export started",
        "simulation_id": simulation_id,
        "status": "pending",
    }


async def export_result_task(simulation_id: str, result: Dict[str, Any]) -> None:
    """
    Export a simulation result to a file.

    Args:
        simulation_id: Simulation ID
        result: Simulation result
    """
    try:
        # Import here to avoid circular imports
        from src.persistence.s3_manager import get_s3_manager
        import json
        from pathlib import Path

        # Create export directory
        export_dir = Path("results/exports")
        export_dir.mkdir(parents=True, exist_ok=True)

        # Create export file
        export_file = export_dir / f"{simulation_id}.json"
        with open(export_file, "w") as f:
            json.dump(result, f, indent=2)

        logger.info("Exported result to file", simulation_id=simulation_id, file_path=str(export_file))

        # Upload to S3 if available
        try:
            s3_manager = get_s3_manager()
            key = await s3_manager.upload_file(export_file, f"exports/{simulation_id}.json")
            logger.info("Uploaded export to S3", simulation_id=simulation_id, key=key)
        except Exception as e:
            logger.warning("Failed to upload export to S3", simulation_id=simulation_id, error=str(e))

    except Exception as e:
        logger.error("Failed to export result", simulation_id=simulation_id, error=str(e))
