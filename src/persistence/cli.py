"""
CLI utilities for the persistence layer.

This module provides command-line utilities for the persistence layer.
"""

import argparse
import asyncio
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

import structlog

from src.persistence.db_manager import get_db_manager, init_db, query_results
from src.persistence.result_store import get_result_store
from src.persistence.s3_manager import get_s3_manager

logger = structlog.get_logger(__name__)


async def init_database() -> None:
    """Initialize the database."""
    await init_db()
    logger.info("Database initialized")


async def list_results(limit: int = 5) -> None:
    """
    List simulation results.

    Args:
        limit: Maximum number of results to return
    """
    result_store = get_result_store()
    results = await result_store.list_results(limit=limit)
    
    if not results:
        print("No results found")
        return
    
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results):
        simulation_id = result.get("run_id", "")
        status = result.get("status", "completed")
        created_at = result.get("created_at", "")
        metrics = result.get("metrics", {})
        
        print(f"{i+1}. ID: {simulation_id}")
        print(f"   Status: {status}")
        print(f"   Created: {created_at}")
        
        if "irr" in metrics:
            print(f"   IRR: {metrics['irr']:.2%}")
        
        if "equity_multiple" in metrics:
            print(f"   Equity Multiple: {metrics['equity_multiple']:.2f}x")
        
        print()


async def get_result(simulation_id: str) -> None:
    """
    Get a simulation result.

    Args:
        simulation_id: Simulation ID
    """
    result_store = get_result_store()
    result = await result_store.get_result(simulation_id)
    
    if not result:
        print(f"Result not found: {simulation_id}")
        return
    
    print(f"Result for simulation {simulation_id}:")
    print(json.dumps(result, indent=2))


async def delete_result(simulation_id: str) -> None:
    """
    Delete a simulation result.

    Args:
        simulation_id: Simulation ID
    """
    result_store = get_result_store()
    success = await result_store.delete_result(simulation_id)
    
    if success:
        print(f"Result deleted: {simulation_id}")
    else:
        print(f"Result not found: {simulation_id}")


async def test_s3() -> None:
    """Test S3 connection."""
    s3_manager = get_s3_manager()
    
    try:
        await s3_manager.initialize()
        print("S3 connection successful")
        
        # Create test file
        test_file = Path("results/test.json")
        with open(test_file, "w") as f:
            json.dump({"test": "data"}, f)
        
        # Upload test file
        key = await s3_manager.upload_file(test_file)
        print(f"Uploaded test file: {key}")
        
        # List files
        print("Listing files in S3...")
        results = await s3_manager.list_results(limit=5)
        print(f"Found {len(results)} results")
        
    except Exception as e:
        print(f"S3 test failed: {str(e)}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Persistence layer CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Init database command
    init_parser = subparsers.add_parser("init-db", help="Initialize the database")
    
    # List results command
    list_parser = subparsers.add_parser("list", help="List simulation results")
    list_parser.add_argument("--limit", type=int, default=5, help="Maximum number of results to return")
    
    # Get result command
    get_parser = subparsers.add_parser("get", help="Get a simulation result")
    get_parser.add_argument("simulation_id", help="Simulation ID")
    
    # Delete result command
    delete_parser = subparsers.add_parser("delete", help="Delete a simulation result")
    delete_parser.add_argument("simulation_id", help="Simulation ID")
    
    # Test S3 command
    s3_parser = subparsers.add_parser("test-s3", help="Test S3 connection")
    
    args = parser.parse_args()
    
    if args.command == "init-db":
        asyncio.run(init_database())
    elif args.command == "list":
        asyncio.run(list_results(args.limit))
    elif args.command == "get":
        asyncio.run(get_result(args.simulation_id))
    elif args.command == "delete":
        asyncio.run(delete_result(args.simulation_id))
    elif args.command == "test-s3":
        asyncio.run(test_s3())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
