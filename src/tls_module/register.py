"""
Register the TLS module with the orchestrator.
"""

from src.engine.orchestrator import get_orchestrator
from src.engine.simulation_context import SimulationContext
from src.tls_module.tls_module import initialize_tls_module


async def register_tls_module() -> None:
    """Register the TLS module with the orchestrator."""
    # Get orchestrator
    orchestrator = get_orchestrator()
    
    # Register TLS module
    orchestrator.register_module(
        name="tls_module",
        func=initialize_tls_module,
        position=0,  # First module to run
    )
