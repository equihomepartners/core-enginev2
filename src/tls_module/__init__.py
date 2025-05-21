"""
Traffic Light System (TLS) Module for the EQU IHOME SIM ENGINE v2.

This module provides a sophisticated classification system for geographic areas (suburbs)
with multi-dimensional scoring, rich metrics, and property-level variation.

Features:
- Multi-dimensional scoring (appreciation, risk, liquidity)
- Confidence levels for all metrics
- Rich set of economic, demographic, and real estate metrics
- Property-level variation with detailed attributes
- Correlation analysis between metrics and suburbs
- Visualization support for various data distributions
- Zone-based classification (green, orange, red)
- Static data for consistent testing
"""

from typing import Optional

from src.tls_module.tls_core import TLSDataManager


# Global TLS data manager instance
_global_tls_manager: Optional[TLSDataManager] = None


def get_tls_manager(use_mock: bool = True) -> TLSDataManager:
    """
    Get the global TLS data manager instance.

    Args:
        use_mock: Whether to use mock data

    Returns:
        The global TLS data manager instance
    """
    global _global_tls_manager

    if _global_tls_manager is None:
        _global_tls_manager = TLSDataManager(use_mock=use_mock)

    return _global_tls_manager


def reset_tls_manager() -> None:
    """Reset the global TLS data manager instance."""
    global _global_tls_manager
    _global_tls_manager = None