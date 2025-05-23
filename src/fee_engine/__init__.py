"""
Fee engine module for the EQU IHOME SIM ENGINE v2.

This module is responsible for calculating fees and expenses for the fund,
including management fees, origination fees, and fund expenses.
"""

from src.fee_engine.fee_engine import FeeEngine, calculate_fees

__all__ = ["FeeEngine", "calculate_fees"]
