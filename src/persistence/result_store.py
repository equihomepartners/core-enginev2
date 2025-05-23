"""
Result store module for the EQU IHOME SIM ENGINE v2.

This module provides functionality for storing and retrieving simulation results.
It supports both local file storage and database storage, with environment-based configuration.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

import structlog

from src.engine.simulation_context import SimulationContext

logger = structlog.get_logger(__name__)

# Default to local storage if no DB_URL is provided
DB_URL = os.getenv("DB_URL", "sqlite:///results/simulation.db")

# Default to local file storage if no S3 configuration
USE_S3 = os.getenv("USE_S3", "false").lower() == "true"

# Results directory
RESULTS_DIR = os.getenv("RESULTS_DIR", "results")

# Create results directory if it doesn't exist
Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)

# In-memory cache for simulation results
_result_cache: Dict[str, Dict[str, Any]] = {}


class ResultStore:
    """
    Store for simulation results.

    This class provides methods for storing and retrieving simulation results.
    It supports both local file storage and database storage, with environment-based configuration.
    """

    def __init__(self, simulation_id: Optional[str] = None):
        """
        Initialize the result store.

        Args:
            simulation_id: Simulation ID (optional)
        """
        self.simulation_id = simulation_id
        self.db_manager = None
        self.s3_manager = None

        # Import here to avoid circular imports
        if "sqlite" in DB_URL or "postgresql" in DB_URL:
            try:
                from src.persistence.db_manager import get_db_manager
                self.db_manager = get_db_manager()
                logger.info("Database manager initialized", db_url=DB_URL)
            except ImportError:
                logger.warning("Database manager not available, using local file storage")

        if USE_S3:
            try:
                from src.persistence.s3_manager import get_s3_manager
                self.s3_manager = get_s3_manager()
                logger.info("S3 manager initialized")
            except ImportError:
                logger.warning("S3 manager not available, using local file storage")

    async def store_result(self, context: SimulationContext) -> str:
        """
        Store a simulation result.

        Args:
            context: Simulation context

        Returns:
            Simulation ID
        """
        # Get simulation summary
        summary = context.get_summary()
        simulation_id = context.run_id

        # Add timestamp
        summary["stored_at"] = datetime.now().isoformat()

        # Store in cache
        _result_cache[simulation_id] = summary

        # Store in database if available
        if self.db_manager:
            try:
                await self.db_manager.store_result(simulation_id, summary)
                logger.info("Stored result in database", simulation_id=simulation_id)
            except Exception as e:
                logger.error("Failed to store result in database", simulation_id=simulation_id, error=str(e))

        # Store in S3 if available
        if self.s3_manager:
            try:
                await self.s3_manager.upload_result(simulation_id, summary)
                logger.info("Stored result in S3", simulation_id=simulation_id)
            except Exception as e:
                logger.error("Failed to store result in S3", simulation_id=simulation_id, error=str(e))

        # Always store locally as fallback
        self._store_local(simulation_id, summary)

        return simulation_id

    def _store_local(self, simulation_id: str, result: Dict[str, Any]) -> None:
        """
        Store a simulation result locally.

        Args:
            simulation_id: Simulation ID
            result: Simulation result
        """
        # Create file path
        file_path = Path(RESULTS_DIR) / f"{simulation_id}.json"

        # Write to file
        with open(file_path, "w") as f:
            json.dump(result, f, indent=2)

        logger.info("Stored result locally", simulation_id=simulation_id, file_path=str(file_path))

    async def get_result(self, simulation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a simulation result.

        Args:
            simulation_id: Simulation ID

        Returns:
            Simulation result or None if not found
        """
        # Check cache first
        if simulation_id in _result_cache:
            logger.debug("Retrieved result from cache", simulation_id=simulation_id)
            return _result_cache[simulation_id]

        # Try database if available
        if self.db_manager:
            try:
                result = await self.db_manager.get_result(simulation_id)
                if result:
                    # Update cache
                    _result_cache[simulation_id] = result
                    logger.info("Retrieved result from database", simulation_id=simulation_id)
                    return result
            except Exception as e:
                logger.error("Failed to retrieve result from database", simulation_id=simulation_id, error=str(e))

        # Try S3 if available
        if self.s3_manager:
            try:
                result = await self.s3_manager.download_result(simulation_id)
                if result:
                    # Update cache
                    _result_cache[simulation_id] = result
                    logger.info("Retrieved result from S3", simulation_id=simulation_id)
                    return result
            except Exception as e:
                logger.error("Failed to retrieve result from S3", simulation_id=simulation_id, error=str(e))

        # Try local file as fallback
        return self._get_local(simulation_id)

    def _get_local(self, simulation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a simulation result from local storage.

        Args:
            simulation_id: Simulation ID

        Returns:
            Simulation result or None if not found
        """
        # Create file path
        file_path = Path(RESULTS_DIR) / f"{simulation_id}.json"

        # Check if file exists
        if not file_path.exists():
            logger.warning("Result not found locally", simulation_id=simulation_id)
            return None

        # Read from file
        try:
            with open(file_path, "r") as f:
                result = json.load(f)

            logger.info("Retrieved result from local file", simulation_id=simulation_id)
            return result
        except Exception as e:
            logger.error("Failed to read result from local file", simulation_id=simulation_id, error=str(e))
            return None

    async def list_results(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List simulation results.

        Args:
            limit: Maximum number of results to return
            offset: Offset for pagination

        Returns:
            List of simulation results
        """
        # Try database if available
        if self.db_manager:
            try:
                results = await self.db_manager.list_results(limit, offset)
                if results:
                    logger.info("Listed results from database", count=len(results))
                    return results
            except Exception as e:
                logger.error("Failed to list results from database", error=str(e))

        # Try S3 if available
        if self.s3_manager:
            try:
                results = await self.s3_manager.list_results(limit, offset)
                if results:
                    logger.info("Listed results from S3", count=len(results))
                    return results
            except Exception as e:
                logger.error("Failed to list results from S3", error=str(e))

        # Fall back to local files
        return self._list_local(limit, offset)

    def _list_local(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List simulation results from local storage.

        Args:
            limit: Maximum number of results to return
            offset: Offset for pagination

        Returns:
            List of simulation results
        """
        # Get all JSON files in results directory
        result_files = list(Path(RESULTS_DIR).glob("*.json"))

        # Sort by modification time (newest first)
        result_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        # Apply pagination
        result_files = result_files[offset:offset + limit]

        # Load results
        results = []
        for file_path in result_files:
            try:
                with open(file_path, "r") as f:
                    result = json.load(f)
                    results.append(result)
            except Exception as e:
                logger.error("Failed to read result from local file", file_path=str(file_path), error=str(e))

        logger.info("Listed results from local files", count=len(results))
        return results

    async def delete_result(self, simulation_id: str) -> bool:
        """
        Delete a simulation result.

        Args:
            simulation_id: Simulation ID

        Returns:
            True if deleted, False otherwise
        """
        success = False

        # Remove from cache
        if simulation_id in _result_cache:
            del _result_cache[simulation_id]
            success = True

        # Delete from database if available
        if self.db_manager:
            try:
                db_success = await self.db_manager.delete_result(simulation_id)
                success = success or db_success
                if db_success:
                    logger.info("Deleted result from database", simulation_id=simulation_id)
            except Exception as e:
                logger.error("Failed to delete result from database", simulation_id=simulation_id, error=str(e))

        # Delete from S3 if available
        if self.s3_manager:
            try:
                s3_success = await self.s3_manager.delete_result(simulation_id)
                success = success or s3_success
                if s3_success:
                    logger.info("Deleted result from S3", simulation_id=simulation_id)
            except Exception as e:
                logger.error("Failed to delete result from S3", simulation_id=simulation_id, error=str(e))

        # Delete local file
        local_success = self._delete_local(simulation_id)
        success = success or local_success

        return success

    def _delete_local(self, simulation_id: str) -> bool:
        """
        Delete a simulation result from local storage.

        Args:
            simulation_id: Simulation ID

        Returns:
            True if deleted, False otherwise
        """
        # Create file path
        file_path = Path(RESULTS_DIR) / f"{simulation_id}.json"

        # Check if file exists
        if not file_path.exists():
            logger.warning("Result not found locally", simulation_id=simulation_id)
            return False

        # Delete file
        try:
            file_path.unlink()
            logger.info("Deleted result from local file", simulation_id=simulation_id)
            return True
        except Exception as e:
            logger.error("Failed to delete result from local file", simulation_id=simulation_id, error=str(e))
            return False


# Global result store instance
_global_result_store: Optional[ResultStore] = None


def get_result_store(simulation_id: Optional[str] = None) -> ResultStore:
    """
    Get the global result store instance.

    Args:
        simulation_id: Simulation ID (optional)

    Returns:
        The global result store instance
    """
    global _global_result_store

    if _global_result_store is None or simulation_id is not None:
        _global_result_store = ResultStore(simulation_id)

    return _global_result_store
