"""
Capital allocator module for the EQU IHOME SIM ENGINE v2.

This module is responsible for allocating capital across zones based on policy.
It integrates with the TLS module to get zone data and implements allocation
policy enforcement with error handling, visualization support, and progress reporting.
"""

from src.capital_allocator.allocator import (
    allocate_capital,
    rebalance_allocation,
    calculate_loan_counts,
    update_actual_allocation,
    get_zone_properties,
    get_allocation_summary,
    validate_zone_allocations,
    generate_allocation_visualization,
    calculate_allocation_statistics,
    generate_rebalancing_visualization,
    generate_loan_count_visualization,
    generate_allocation_comparison,
)

__all__ = [
    "allocate_capital",
    "rebalance_allocation",
    "calculate_loan_counts",
    "update_actual_allocation",
    "get_zone_properties",
    "get_allocation_summary",
    "validate_zone_allocations",
    "generate_allocation_visualization",
    "calculate_allocation_statistics",
    "generate_rebalancing_visualization",
    "generate_loan_count_visualization",
    "generate_allocation_comparison",
]