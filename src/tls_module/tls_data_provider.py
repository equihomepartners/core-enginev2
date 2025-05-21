"""
TLS data provider module for the EQU IHOME SIM ENGINE v2.

This module provides access to Traffic Light System (TLS) data for zone classification.
"""

import os
from typing import Dict, Any, Optional, List

import structlog

from src.engine.simulation_context import SimulationContext

logger = structlog.get_logger(__name__)


class TLSDataProvider:
    """
    Provider for Traffic Light System (TLS) data.
    
    This class provides access to TLS data for zone classification. It can operate
    in two modes:
    
    1. Mock mode: Uses mock data for testing and development
    2. Production mode: Connects to the TLS service for real data
    
    The mode is controlled by the TLS_MOCK environment variable.
    """
    
    def __init__(self, use_mock: Optional[bool] = None):
        """
        Initialize the TLS data provider.
        
        Args:
            use_mock: Whether to use mock data (overrides environment variable)
        """
        # Determine whether to use mock data
        if use_mock is None:
            use_mock = os.environ.get("TLS_MOCK", "true").lower() == "true"
        
        self.use_mock = use_mock
        
        # Cache for TLS data
        self._cache: Dict[str, Dict[str, Any]] = {}
        
        logger.info("TLS data provider initialized", use_mock=self.use_mock)
    
    def get_zone_data(self, suburb_id: str) -> Dict[str, Any]:
        """
        Get TLS data for a suburb.
        
        Args:
            suburb_id: Suburb ID
            
        Returns:
            Dictionary containing TLS data for the suburb
        """
        # Check cache
        if suburb_id in self._cache:
            return self._cache[suburb_id]
        
        # Get data
        if self.use_mock:
            data = self._get_mock_data(suburb_id)
        else:
            data = self._get_production_data(suburb_id)
        
        # Cache data
        self._cache[suburb_id] = data
        
        return data
    
    def get_zone(self, suburb_id: str) -> str:
        """
        Get the zone for a suburb.
        
        Args:
            suburb_id: Suburb ID
            
        Returns:
            Zone name (green, orange, red)
        """
        data = self.get_zone_data(suburb_id)
        return data.get("zone", "red")
    
    def get_appreciation_rate(self, suburb_id: str) -> float:
        """
        Get the appreciation rate for a suburb.
        
        Args:
            suburb_id: Suburb ID
            
        Returns:
            Appreciation rate
        """
        data = self.get_zone_data(suburb_id)
        return data.get("appreciation_rate", 0.01)
    
    def get_default_rate(self, suburb_id: str) -> float:
        """
        Get the default rate for a suburb.
        
        Args:
            suburb_id: Suburb ID
            
        Returns:
            Default rate
        """
        data = self.get_zone_data(suburb_id)
        return data.get("default_rate", 0.05)
    
    def get_recovery_rate(self, suburb_id: str) -> float:
        """
        Get the recovery rate for a suburb.
        
        Args:
            suburb_id: Suburb ID
            
        Returns:
            Recovery rate
        """
        data = self.get_zone_data(suburb_id)
        return data.get("recovery_rate", 0.7)
    
    def _get_mock_data(self, suburb_id: str) -> Dict[str, Any]:
        """
        Get mock TLS data for a suburb.
        
        Args:
            suburb_id: Suburb ID
            
        Returns:
            Dictionary containing mock TLS data for the suburb
        """
        # Determine zone based on suburb ID
        # This is a simple deterministic algorithm for testing
        suburb_hash = sum(ord(c) for c in suburb_id)
        
        if suburb_hash % 10 < 6:
            zone = "green"
            appreciation_rate = 0.05
            default_rate = 0.01
            recovery_rate = 0.9
        elif suburb_hash % 10 < 9:
            zone = "orange"
            appreciation_rate = 0.03
            default_rate = 0.03
            recovery_rate = 0.8
        else:
            zone = "red"
            appreciation_rate = 0.01
            default_rate = 0.05
            recovery_rate = 0.7
        
        return {
            "suburb_id": suburb_id,
            "zone": zone,
            "appreciation_rate": appreciation_rate,
            "default_rate": default_rate,
            "recovery_rate": recovery_rate,
            "is_mock": True,
        }
    
    def _get_production_data(self, suburb_id: str) -> Dict[str, Any]:
        """
        Get production TLS data for a suburb.
        
        Args:
            suburb_id: Suburb ID
            
        Returns:
            Dictionary containing production TLS data for the suburb
        """
        # TODO: Implement connection to TLS service
        # For now, just return mock data
        logger.warning("Production TLS data not implemented, using mock data")
        return self._get_mock_data(suburb_id)


# Global TLS data provider instance
_global_tls_provider: Optional[TLSDataProvider] = None


def get_tls_provider() -> TLSDataProvider:
    """
    Get the global TLS data provider instance.
    
    Returns:
        The global TLS data provider instance
    """
    global _global_tls_provider
    
    if _global_tls_provider is None:
        _global_tls_provider = TLSDataProvider()
    
    return _global_tls_provider


def load_zone_data(context: SimulationContext) -> None:
    """
    Load TLS zone data into the simulation context.
    
    Args:
        context: Simulation context
    """
    logger.info("Loading TLS zone data")
    
    # Get TLS data provider
    tls_provider = get_tls_provider()
    
    # Load zone data for all suburbs in the configuration
    # For now, we'll just load data for a few example suburbs
    example_suburbs = ["suburb1", "suburb2", "suburb3", "suburb4", "suburb5"]
    
    for suburb_id in example_suburbs:
        zone_data = tls_provider.get_zone_data(suburb_id)
        context.tls_data[suburb_id] = zone_data
    
    # Log summary
    zone_counts = {}
    for suburb_id, data in context.tls_data.items():
        zone = data.get("zone", "unknown")
        zone_counts[zone] = zone_counts.get(zone, 0) + 1
    
    logger.info(
        "TLS zone data loaded",
        num_suburbs=len(context.tls_data),
        zone_counts=zone_counts,
    )
