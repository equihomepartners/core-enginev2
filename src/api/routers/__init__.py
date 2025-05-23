"""
API routers for the EQU IHOME SIM ENGINE v2.

This package provides FastAPI routers for different functional areas of the API.
"""

from src.api.routers.finance import router as finance_router
from src.api.routers.portfolio import router as portfolio_router
from src.api.routers.price_path import router as price_path_router
from src.api.routers.exit_simulator import router as exit_simulator_router
from src.api.routers.enhanced_exit_simulator import router as enhanced_exit_simulator_router
from src.api.routers.reinvestment import router as reinvestment_router
from src.api.routers.simulation import router as simulation_router
from src.api.routers.tls import router as tls_router
from src.api.routers.tranche_router import router as tranche_router
from src.api.routers.waterfall import router as waterfall_router
from src.api.routers.websocket import router as websocket_router
from src.api.routers.risk import router as risk_router
from src.api.routers.guardrail import router as guardrail_router

__all__ = [
    "finance_router",
    "portfolio_router",
    "price_path_router",
    "exit_simulator_router",
    "enhanced_exit_simulator_router",
    "reinvestment_router",
    "simulation_router",
    "tls_router",
    "tranche_router",
    "waterfall_router",
    "websocket_router",
    "risk_router",
    "guardrail_router",
]
