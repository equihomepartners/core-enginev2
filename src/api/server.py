"""
API server module for the EQU IHOME SIM ENGINE v2.

This module provides a FastAPI server for running simulations and retrieving results.
"""

import os
from typing import Dict

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles

from src.api.routers import (
    simulation_router as simulation,
    tls_router as tls,
    websocket_router as websocket,
    portfolio_router as portfolio,
    price_path_router as price_path,
    exit_simulator_router as exit_simulator,
    enhanced_exit_simulator_router as enhanced_exit_simulator,
    reinvestment_router as reinvestment,
    finance_router as finance,
    waterfall_router as waterfall,
    tranche_router,
    risk_router as risk,
    guardrail_router as guardrail
)
from src.api.routers.performance import router as performance_router
from src.api.routers.persistence import router as persistence_router
from src.utils.logging_setup import setup_logging

# Set up logging
setup_logging(verbose=os.environ.get("SIM_DEBUG", "").lower() == "true")
logger = structlog.get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="EQU IHOME SIM ENGINE API",
    description="API for running home equity investment fund simulations",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(simulation, prefix="/simulations")
app.include_router(portfolio)  # Already has /simulations prefix
app.include_router(price_path)  # Already has /simulations prefix
app.include_router(exit_simulator)  # Already has /simulations prefix
app.include_router(enhanced_exit_simulator)  # Already has /simulations prefix
app.include_router(reinvestment)  # Already has /simulations prefix
app.include_router(waterfall)  # Already has /simulations prefix
app.include_router(tranche_router)  # Uses /tranches prefix
app.include_router(finance)  # Uses /finance prefix
app.include_router(risk)  # Uses /risk prefix
app.include_router(guardrail)  # Uses /guardrail prefix
app.include_router(performance_router)  # Uses /performance prefix
app.include_router(tls, prefix="/tls")
app.include_router(websocket, prefix="/ws")
app.include_router(persistence_router)  # Already has /api/v1/results prefix

# Mount GraphQL router
# Temporarily disabled for SDK generation
# try:
#     from src.sdk.graphql_schema import mount_graphql_router
#     mount_graphql_router(app, "/graphql")
#     logger.info("GraphQL router mounted at /graphql")
# except ImportError:
#     logger.warning("GraphQL router not mounted: strawberry not installed")


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {"message": "Welcome to the EQU IHOME SIM ENGINE API"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI."""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """ReDoc UI."""
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
    )


def start() -> None:
    """Start the API server."""
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=os.environ.get("SIM_RELOAD", "").lower() == "true",
    )


if __name__ == "__main__":
    start()
