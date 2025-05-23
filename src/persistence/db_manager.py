"""
Database manager module for the EQU IHOME SIM ENGINE v2.

This module provides functionality for database operations.
It supports both SQLite and PostgreSQL, with environment-based configuration.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

import structlog
from sqlalchemy import (
    create_engine, MetaData, Table, Column, String, 
    Text, DateTime, Integer, Float, Boolean, select, 
    insert, update, delete, func
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy.dialects.postgresql import JSONB

logger = structlog.get_logger(__name__)

# Default to SQLite if no DB_URL is provided
DB_URL = os.getenv("DB_URL", "sqlite:///results/simulation.db")

# Convert SQLite URL to async SQLite URL if needed
if DB_URL.startswith("sqlite:///") and not DB_URL.startswith("sqlite+aiosqlite:///"):
    DB_URL = DB_URL.replace("sqlite:///", "sqlite+aiosqlite:///")

# Convert PostgreSQL URL to async PostgreSQL URL if needed
if DB_URL.startswith("postgresql://") and not DB_URL.startswith("postgresql+asyncpg://"):
    DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create metadata
metadata = MetaData()

# Define simulation_results table
simulation_results = Table(
    "simulation_results",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("status", String(20), nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("completed_at", DateTime, nullable=True),
    Column("config", Text, nullable=False),
    Column("metrics", Text, nullable=True),
    Column("execution_time", Float, nullable=True),
    Column("num_loans", Integer, nullable=True),
    Column("guardrail_violations", Text, nullable=True),
    Column("result_json", Text, nullable=True),
)


class DatabaseManager:
    """
    Manager for database operations.

    This class provides methods for database operations.
    It supports both SQLite and PostgreSQL, with environment-based configuration.
    """

    def __init__(self):
        """Initialize the database manager."""
        self.engine: Optional[AsyncEngine] = None
        self.connection: Optional[AsyncConnection] = None
        self.initialized = False

    async def initialize(self) -> None:
        """Initialize the database connection and create tables if they don't exist."""
        if self.initialized:
            return

        try:
            # Create async engine
            self.engine = create_async_engine(DB_URL, echo=False)

            # Create connection
            self.connection = await self.engine.connect()

            # Create tables if they don't exist
            async with self.engine.begin() as conn:
                await conn.run_sync(metadata.create_all)

            self.initialized = True
            logger.info("Database initialized", db_url=DB_URL)
        except Exception as e:
            logger.error("Failed to initialize database", error=str(e))
            raise

    async def store_result(self, simulation_id: str, result: Dict[str, Any]) -> None:
        """
        Store a simulation result in the database.

        Args:
            simulation_id: Simulation ID
            result: Simulation result
        """
        await self.initialize()

        try:
            # Extract fields from result
            status = result.get("status", "completed")
            created_at = datetime.fromisoformat(result.get("created_at", datetime.now().isoformat()))
            completed_at = datetime.fromisoformat(result.get("completed_at", datetime.now().isoformat())) if result.get("completed_at") else None
            config = json.dumps(result.get("config", {}))
            metrics = json.dumps(result.get("metrics", {}))
            execution_time = result.get("execution_time", 0.0)
            num_loans = result.get("num_loans", 0)
            guardrail_violations = json.dumps(result.get("guardrail_violations", []))
            result_json = json.dumps(result)

            # Check if result already exists
            query = select(simulation_results).where(simulation_results.c.id == simulation_id)
            existing = await self.connection.execute(query)
            existing_result = existing.fetchone()

            if existing_result:
                # Update existing result
                query = (
                    update(simulation_results)
                    .where(simulation_results.c.id == simulation_id)
                    .values(
                        status=status,
                        completed_at=completed_at,
                        metrics=metrics,
                        execution_time=execution_time,
                        num_loans=num_loans,
                        guardrail_violations=guardrail_violations,
                        result_json=result_json,
                    )
                )
                await self.connection.execute(query)
                logger.info("Updated result in database", simulation_id=simulation_id)
            else:
                # Insert new result
                query = insert(simulation_results).values(
                    id=simulation_id,
                    status=status,
                    created_at=created_at,
                    completed_at=completed_at,
                    config=config,
                    metrics=metrics,
                    execution_time=execution_time,
                    num_loans=num_loans,
                    guardrail_violations=guardrail_violations,
                    result_json=result_json,
                )
                await self.connection.execute(query)
                logger.info("Inserted result in database", simulation_id=simulation_id)

            # Commit transaction
            await self.connection.commit()
        except Exception as e:
            logger.error("Failed to store result in database", simulation_id=simulation_id, error=str(e))
            raise

    async def get_result(self, simulation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a simulation result from the database.

        Args:
            simulation_id: Simulation ID

        Returns:
            Simulation result or None if not found
        """
        await self.initialize()

        try:
            # Query result
            query = select(simulation_results).where(simulation_results.c.id == simulation_id)
            result = await self.connection.execute(query)
            row = result.fetchone()

            if not row:
                logger.warning("Result not found in database", simulation_id=simulation_id)
                return None

            # Parse result JSON
            result_json = json.loads(row.result_json)
            logger.info("Retrieved result from database", simulation_id=simulation_id)
            return result_json
        except Exception as e:
            logger.error("Failed to retrieve result from database", simulation_id=simulation_id, error=str(e))
            raise

    async def list_results(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List simulation results from the database.

        Args:
            limit: Maximum number of results to return
            offset: Offset for pagination

        Returns:
            List of simulation results
        """
        await self.initialize()

        try:
            # Query results
            query = (
                select(simulation_results)
                .order_by(simulation_results.c.created_at.desc())
                .limit(limit)
                .offset(offset)
            )
            result = await self.connection.execute(query)
            rows = result.fetchall()

            # Parse result JSONs
            results = []
            for row in rows:
                result_json = json.loads(row.result_json)
                results.append(result_json)

            logger.info("Listed results from database", count=len(results))
            return results
        except Exception as e:
            logger.error("Failed to list results from database", error=str(e))
            raise

    async def delete_result(self, simulation_id: str) -> bool:
        """
        Delete a simulation result from the database.

        Args:
            simulation_id: Simulation ID

        Returns:
            True if deleted, False otherwise
        """
        await self.initialize()

        try:
            # Delete result
            query = delete(simulation_results).where(simulation_results.c.id == simulation_id)
            result = await self.connection.execute(query)
            await self.connection.commit()

            if result.rowcount > 0:
                logger.info("Deleted result from database", simulation_id=simulation_id)
                return True
            else:
                logger.warning("Result not found in database", simulation_id=simulation_id)
                return False
        except Exception as e:
            logger.error("Failed to delete result from database", simulation_id=simulation_id, error=str(e))
            raise

    async def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            await self.connection.close()
        if self.engine:
            await self.engine.dispose()
        self.initialized = False
        logger.info("Database connection closed")


# Global database manager instance
_global_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """
    Get the global database manager instance.

    Returns:
        The global database manager instance
    """
    global _global_db_manager

    if _global_db_manager is None:
        _global_db_manager = DatabaseManager()

    return _global_db_manager


async def init_db() -> None:
    """Initialize the database."""
    db_manager = get_db_manager()
    await db_manager.initialize()


async def query_results(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Query simulation results.

    Args:
        limit: Maximum number of results to return

    Returns:
        List of simulation results
    """
    db_manager = get_db_manager()
    return await db_manager.list_results(limit=limit)
