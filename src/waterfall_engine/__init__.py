"""
Waterfall Engine module for the EQU IHOME SIM ENGINE v2.

This module is responsible for calculating the distribution waterfall for fund cashflows,
including hurdle rates, carried interest, catch-up provisions, and multi-tier structures.
It supports both European (whole-fund) and American (deal-by-deal) waterfall structures.
"""

from src.waterfall_engine.waterfall_engine import WaterfallEngine, WaterfallTier, WaterfallStructure

__all__ = ["WaterfallEngine", "WaterfallTier", "WaterfallStructure", "calculate_waterfall"]


async def calculate_waterfall(context):
    """
    Calculate waterfall distributions for the simulation.

    Args:
        context: Simulation context

    Returns:
        Dictionary containing waterfall distribution results
    """
    waterfall_engine = WaterfallEngine(context)
    return waterfall_engine.run()