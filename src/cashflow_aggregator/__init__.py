"""
Cashflow aggregator module for the EQU IHOME SIM ENGINE v2.

This module is responsible for aggregating cashflows from various sources,
including loans, exits, fees, and leverage, and providing a comprehensive
view of the fund's cashflow over time.
"""

from src.cashflow_aggregator.cashflow_aggregator import aggregate_cashflows

__all__ = ["aggregate_cashflows"]
