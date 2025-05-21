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

from src.api.routers import simulation, tls, websocket, portfolio, price_path, exit_simulator, enhanced_exit_simulator, reinvestment
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
app.include_router(simulation.router, prefix="/simulations")
app.include_router(portfolio.router)  # Already has /simulations prefix
app.include_router(price_path.router)  # Already has /simulations prefix
app.include_router(exit_simulator.router)  # Already has /simulations prefix
app.include_router(enhanced_exit_simulator.router)  # Already has /simulations prefix
app.include_router(reinvestment.router)  # Already has /simulations prefix
app.include_router(tls.router, prefix="/tls")
app.include_router(websocket.router, prefix="/ws")


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {"message": "Welcome to the EQU IHOME SIM ENGINE API"}


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
