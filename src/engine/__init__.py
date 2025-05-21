"""
Engine module for the EQU IHOME SIM ENGINE v2.

This module contains the core simulation engine components, including the
loan generator, simulation context, and other simulation-related functionality.
"""

from src.engine.loan_generator import (
    generate_loans,
    generate_loan_sizes,
    generate_ltv_ratios,
    generate_loan_terms,
    generate_interest_rates,
    validate_loan_parameters,
    assign_loans_to_zones,
    get_properties_for_zone,
    get_property_for_loan,
    generate_loan_portfolio_visualization,
    calculate_loan_portfolio_statistics,
)
from src.engine.simulation_context import SimulationContext

__all__ = [
    "generate_loans",
    "generate_loan_sizes",
    "generate_ltv_ratios",
    "generate_loan_terms",
    "generate_interest_rates",
    "validate_loan_parameters",
    "assign_loans_to_zones",
    "get_properties_for_zone",
    "get_property_for_loan",
    "generate_loan_portfolio_visualization",
    "calculate_loan_portfolio_statistics",
    "SimulationContext",
]