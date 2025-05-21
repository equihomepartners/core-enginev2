"""
Test script for the reinvestment engine.

This script tests the reinvestment engine by running a simulation with
reinvestment enabled and verifying that the reinvestment events are
correctly generated and processed.
"""

import asyncio
import json
import logging
import os
import sys
import time
from typing import Dict, Any

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.config.config_loader import SimulationConfig
from src.engine.orchestrator import get_orchestrator
from src.engine.simulation_context import SimulationContext
from src.reinvest_engine.reinvest_engine import (
    reinvest_capital,
    calculate_reinvestment_statistics,
    generate_reinvestment_visualization,
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_reinvestment_engine() -> None:
    """
    Test the reinvestment engine.

    This function runs a simulation with reinvestment enabled and verifies
    that the reinvestment events are correctly generated and processed.
    """
    logger.info("Starting reinvestment engine test")

    # Create a test configuration
    config = SimulationConfig(
        fund_size=100000000,
        fund_term=10,
        vintage_year=2023,
        reinvestment_period=5,
        avg_loan_size=500000,
        avg_loan_ltv=0.5,
        avg_loan_term=10,
        avg_loan_interest_rate=0.05,
        loan_size_std_dev=100000,
        ltv_std_dev=0.05,
        min_loan_size=100000,
        max_loan_size=1000000,
        min_ltv=0.3,
        max_ltv=0.7,
        zone_allocations={
            "green": 0.6,
            "orange": 0.3,
            "red": 0.1,
        },
        reinvestment_engine={
            "reinvestment_strategy": "rebalance",
            "min_reinvestment_amount": 1000000,
            "reinvestment_frequency": "quarterly",
            "reinvestment_delay": 1,
            "reinvestment_batch_size": 10,
            "zone_preference_multipliers": {
                "green": 1.0,
                "orange": 1.0,
                "red": 1.0,
            },
            "opportunistic_threshold": 0.05,
            "rebalance_threshold": 0.05,
            "enable_dynamic_allocation": False,
            "enable_cash_reserve": True,
            "cash_reserve_target": 0.05,
            "cash_reserve_min": 0.02,
            "cash_reserve_max": 0.1,
        },
    )

    # Create a simulation context
    context = SimulationContext(config)

    # Get the orchestrator
    orchestrator = get_orchestrator()

    # Run the simulation
    logger.info("Running simulation")
    results = await orchestrator.run_simulation(config)

    # Check if reinvestment events were generated
    reinvestment_events = getattr(context, "reinvestment_events", [])
    logger.info(f"Generated {len(reinvestment_events)} reinvestment events")

    # Calculate reinvestment statistics
    reinvestment_summary = calculate_reinvestment_statistics(context)
    logger.info(f"Reinvestment summary: {json.dumps(reinvestment_summary, indent=2)}")

    # Generate visualization data
    visualization = generate_reinvestment_visualization(context)
    logger.info(f"Generated visualization data with {len(visualization)} sections")

    # Verify that the reinvestment events were correctly processed
    if len(reinvestment_events) > 0:
        logger.info("Reinvestment engine test passed")
    else:
        logger.error("Reinvestment engine test failed: No reinvestment events generated")


async def test_manual_reinvestment() -> None:
    """
    Test manual reinvestment.

    This function tests the manual reinvestment functionality by creating
    a simulation context and manually triggering a reinvestment event.
    """
    logger.info("Starting manual reinvestment test")

    # Create a test configuration
    config = SimulationConfig(
        fund_size=100000000,
        fund_term=10,
        vintage_year=2023,
        reinvestment_period=5,
        avg_loan_size=500000,
        avg_loan_ltv=0.5,
        avg_loan_term=10,
        avg_loan_interest_rate=0.05,
        loan_size_std_dev=100000,
        ltv_std_dev=0.05,
        min_loan_size=100000,
        max_loan_size=1000000,
        min_ltv=0.3,
        max_ltv=0.7,
        zone_allocations={
            "green": 0.6,
            "orange": 0.3,
            "red": 0.1,
        },
        reinvestment_engine={
            "reinvestment_strategy": "rebalance",
            "min_reinvestment_amount": 1000000,
            "reinvestment_frequency": "quarterly",
            "reinvestment_delay": 1,
            "reinvestment_batch_size": 10,
            "zone_preference_multipliers": {
                "green": 1.0,
                "orange": 1.0,
                "red": 1.0,
            },
            "opportunistic_threshold": 0.05,
            "rebalance_threshold": 0.05,
            "enable_dynamic_allocation": False,
            "enable_cash_reserve": True,
            "cash_reserve_target": 0.05,
            "cash_reserve_min": 0.02,
            "cash_reserve_max": 0.1,
        },
    )

    # Create a simulation context
    context = SimulationContext(config)

    # Get the orchestrator
    orchestrator = get_orchestrator()

    # Run the initial modules to set up the simulation
    logger.info("Running initial modules")
    await orchestrator._execute_module(context, "tls_module")
    await orchestrator._execute_module(context, "capital_allocator")
    await orchestrator._execute_module(context, "loan_generator")
    await orchestrator._execute_module(context, "price_path")
    await orchestrator._execute_module(context, "exit_simulator")

    # Import the reinvest_amount function
    from src.reinvest_engine.reinvest_engine import reinvest_amount, ReinvestmentSource

    # Manually trigger a reinvestment event
    logger.info("Triggering manual reinvestment")
    reinvestment_event = await reinvest_amount(
        context=context,
        amount=5000000,
        year=2.5,
        month=6,
        source=ReinvestmentSource.EXIT,
        source_details={
            "manual_test": True,
        },
    )

    # Verify that the reinvestment event was correctly processed
    if reinvestment_event:
        logger.info(f"Manual reinvestment event: {json.dumps(reinvestment_event, indent=2)}")
        logger.info("Manual reinvestment test passed")
    else:
        logger.error("Manual reinvestment test failed: No reinvestment event generated")


async def main() -> None:
    """Run the tests."""
    await test_reinvestment_engine()
    await test_manual_reinvestment()


if __name__ == "__main__":
    asyncio.run(main())
