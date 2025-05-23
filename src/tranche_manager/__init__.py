"""
Tranche Manager module for the EQU IHOME SIM ENGINE v2.

This module is responsible for managing tranches in the fund, including:
- Tranche definition and configuration
- Cash flow allocation by tranche
- Tranche-specific metrics calculation
- Tranche waterfall rules
- Coverage tests (overcollateralization, interest coverage)
- Reserve account management
"""

from src.tranche_manager.tranche_manager import (
    TrancheManager, Tranche, TrancheType, PaymentFrequency,
    AmortizationSchedule, TestType
)

__all__ = [
    "TrancheManager", "Tranche", "TrancheType", "PaymentFrequency",
    "AmortizationSchedule", "TestType", "manage_tranches"
]


async def manage_tranches(context):
    """
    Manage tranches for the simulation.

    Args:
        context: Simulation context

    Returns:
        Dictionary containing tranche manager results
    """
    # Create tranche manager
    tranche_manager = TrancheManager(context)

    # Check if tranche management is enabled
    if not tranche_manager.enabled:
        return {}

    # Get loans from context
    loans = getattr(context, "loans", [])

    # Allocate loans to tranches
    tranche_manager.allocate_loans(loans)

    # Get cashflows from context
    cashflows = getattr(context, "cashflows", {}).get("fund_level_cashflows", [])

    # Distribute cashflows to tranches
    tranche_manager.distribute_cashflows(cashflows)

    # Calculate metrics
    tranche_manager.calculate_metrics()

    # Get results
    results = tranche_manager.get_results()

    # Store results in context
    context.tranches = results

    return results