"""
GraphQL schema generator for the EQU IHOME SIM ENGINE v2.

This module generates a GraphQL schema from the FastAPI app.
It also provides utilities for generating GraphQL resolvers.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Callable

import structlog
import strawberry
from fastapi import FastAPI
from pydantic import BaseModel
from strawberry.fastapi import GraphQLRouter

from src.api.server import app

logger = structlog.get_logger(__name__)

# Define Strawberry types for GraphQL schema
@strawberry.type
class SimulationStatus:
    id: str
    status: str
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    error: Optional[str] = None

@strawberry.type
class SimulationMetrics:
    irr: Optional[float] = None
    equity_multiple: Optional[float] = None
    roi: Optional[float] = None
    payback_period: Optional[float] = None
    var_95: Optional[float] = None
    var_99: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None

@strawberry.type
class SimulationResult:
    id: str
    status: str
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    execution_time: Optional[float] = None
    metrics: Optional[SimulationMetrics] = None


def pydantic_model_to_strawberry_type(
    model: type[BaseModel], name: Optional[str] = None
) -> type:
    """
    Convert a Pydantic model to a Strawberry type.

    Args:
        model: Pydantic model
        name: Type name (optional, defaults to model name)

    Returns:
        Strawberry type
    """
    # Get model fields
    fields = {}
    for field_name, field in model.__annotations__.items():
        # Skip private fields
        if field_name.startswith("_"):
            continue

        # Add field to fields dictionary
        fields[field_name] = field

    # Create Strawberry type
    return strawberry.type(
        name or model.__name__,
        fields=fields,
    )


def generate_graphql_schema() -> str:
    """
    Generate a GraphQL schema from the FastAPI app.

    Returns:
        GraphQL schema as a string
    """
    # Define query type
    @strawberry.type
    class Query:
        @strawberry.field
        def hello(self) -> str:
            return "Hello, world!"

        @strawberry.field
        def simulation(self, id: str) -> SimulationResult:
            # This is just a placeholder, the actual implementation would use the result store
            metrics = SimulationMetrics(irr=0.12, equity_multiple=1.5)
            return SimulationResult(
                id=id,
                status="completed",
                metrics=metrics
            )

        @strawberry.field
        def simulations(self, limit: int = 10, offset: int = 0) -> List[SimulationStatus]:
            # This is just a placeholder, the actual implementation would use the result store
            return [
                SimulationStatus(id=f"sim-{i}", status="completed")
                for i in range(limit)
            ]

    # Define input type for simulation config
    @strawberry.input
    class SimulationConfigInput:
        fund_size: float
        fund_term: int
        vintage_year: int
        management_fee_rate: Optional[float] = None
        carried_interest_rate: Optional[float] = None
        hurdle_rate: Optional[float] = None
        target_irr: Optional[float] = None
        target_equity_multiple: Optional[float] = None

    # Define mutation type
    @strawberry.type
    class Mutation:
        @strawberry.mutation
        def create_simulation(self, config: SimulationConfigInput) -> SimulationStatus:
            # This is just a placeholder, the actual implementation would use the orchestrator
            return SimulationStatus(id="sim-123", status="pending")

        @strawberry.mutation
        def cancel_simulation(self, id: str) -> SimulationStatus:
            # This is just a placeholder, the actual implementation would use the orchestrator
            return SimulationStatus(id=id, status="cancelled")

    # Create schema
    schema = strawberry.Schema(query=Query, mutation=Mutation)

    # Get SDL
    return schema.as_str()


def generate_graphql_router() -> GraphQLRouter:
    """
    Generate a GraphQL router for the FastAPI app.

    Returns:
        GraphQL router
    """
    # Define query type with resolvers
    @strawberry.type
    class Query:
        @strawberry.field
        def hello(self) -> str:
            return "Hello, world!"

        @strawberry.field
        async def simulation(self, id: str) -> SimulationResult:
            # Import here to avoid circular imports
            from src.persistence.result_store import get_result_store

            # Get result store
            result_store = get_result_store()

            # Get simulation result
            result = await result_store.get_result(id)
            if not result:
                return SimulationResult(id=id, status="not_found")

            # Convert result to SimulationResult
            metrics = None
            if "metrics" in result:
                metrics = SimulationMetrics(
                    irr=result.get("metrics", {}).get("irr"),
                    equity_multiple=result.get("metrics", {}).get("equity_multiple"),
                    roi=result.get("metrics", {}).get("roi"),
                    payback_period=result.get("metrics", {}).get("payback_period"),
                    var_95=result.get("metrics", {}).get("var_95"),
                    var_99=result.get("metrics", {}).get("var_99"),
                    sharpe_ratio=result.get("metrics", {}).get("sharpe_ratio"),
                    max_drawdown=result.get("metrics", {}).get("max_drawdown"),
                )

            return SimulationResult(
                id=result.get("id", id),
                status=result.get("status", "unknown"),
                created_at=result.get("created_at"),
                completed_at=result.get("completed_at"),
                execution_time=result.get("execution_time"),
                metrics=metrics,
            )

        @strawberry.field
        async def simulations(self, limit: int = 10, offset: int = 0) -> List[SimulationStatus]:
            # Import here to avoid circular imports
            from src.persistence.result_store import get_result_store

            # Get result store
            result_store = get_result_store()

            # Get simulation results
            results = await result_store.list_results(limit=limit, offset=offset)

            # Convert results to SimulationStatus objects
            return [
                SimulationStatus(
                    id=result.get("id", f"sim-{i}"),
                    status=result.get("status", "unknown"),
                    created_at=result.get("created_at"),
                    completed_at=result.get("completed_at"),
                    error=result.get("error"),
                )
                for i, result in enumerate(results)
            ]

    # Define mutation type with resolvers
    @strawberry.type
    class Mutation:
        @strawberry.input
        class SimulationConfigInput:
            fund_size: float
            fund_term: int
            vintage_year: int
            management_fee_rate: Optional[float] = None
            carried_interest_rate: Optional[float] = None
            hurdle_rate: Optional[float] = None
            target_irr: Optional[float] = None
            target_equity_multiple: Optional[float] = None

        @strawberry.mutation
        async def create_simulation(self, config: SimulationConfigInput) -> SimulationStatus:
            # Import here to avoid circular imports
            from src.config.config_loader import load_config_from_dict
            import uuid
            from datetime import datetime

            try:
                # Convert strawberry input to dict
                config_dict = {
                    "fund_size": config.fund_size,
                    "fund_term": config.fund_term,
                    "vintage_year": config.vintage_year,
                }

                # Add optional parameters if provided
                if config.management_fee_rate is not None:
                    config_dict["management_fee_rate"] = config.management_fee_rate
                if config.carried_interest_rate is not None:
                    config_dict["carried_interest_rate"] = config.carried_interest_rate
                if config.hurdle_rate is not None:
                    config_dict["hurdle_rate"] = config.hurdle_rate
                if config.target_irr is not None:
                    config_dict["target_irr"] = config.target_irr
                if config.target_equity_multiple is not None:
                    config_dict["target_equity_multiple"] = config.target_equity_multiple

                # Create simulation ID
                simulation_id = str(uuid.uuid4())
                created_at = datetime.now().isoformat()

                # Run simulation in background
                # Note: In a real implementation, this would be handled by a background task
                # For now, we'll just return a pending status
                return SimulationStatus(
                    id=simulation_id,
                    status="pending",
                    created_at=created_at,
                )
            except Exception as e:
                return SimulationStatus(
                    id="",
                    status="error",
                    error=str(e),
                )

        @strawberry.mutation
        async def cancel_simulation(self, id: str) -> SimulationStatus:
            # Import here to avoid circular imports
            from src.api.websocket_manager import get_websocket_manager

            # Get WebSocket manager
            websocket_manager = get_websocket_manager()

            # Set cancellation flag
            websocket_manager.set_cancelled(id)

            return SimulationStatus(
                id=id,
                status="cancellation_requested"
            )

    # Create schema
    schema = strawberry.Schema(query=Query, mutation=Mutation)

    # Create GraphQL router
    graphql_router = GraphQLRouter(schema)

    return graphql_router


def save_graphql_schema(output_file: str) -> None:
    """
    Save the GraphQL schema to a file.

    Args:
        output_file: Path to the output file
    """
    # Generate schema
    schema = generate_graphql_schema()

    # Create output directory
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write to file
    with open(output_path, "w") as f:
        f.write(schema)

    logger.info("Generated GraphQL schema", output_file=str(output_path))


def mount_graphql_router(app: FastAPI, path: str = "/graphql") -> None:
    """
    Mount the GraphQL router on the FastAPI app.

    Args:
        app: FastAPI app
        path: Path to mount the GraphQL router
    """
    # Generate GraphQL router
    graphql_router = generate_graphql_router()

    # Mount router
    app.include_router(graphql_router, prefix=path)
    logger.info("Mounted GraphQL router", path=path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate GraphQL schema")
    parser.add_argument(
        "--output-file",
        default="schemas/schema.graphql",
        help="Output file for GraphQL schema",
    )

    args = parser.parse_args()

    # Save GraphQL schema
    save_graphql_schema(args.output_file)
