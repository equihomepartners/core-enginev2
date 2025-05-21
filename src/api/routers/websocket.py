"""
WebSocket API router for the EQU IHOME SIM ENGINE v2.

This module provides WebSocket endpoints for real-time updates.
"""

import logging
from typing import Dict, Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.api.websocket_manager import get_websocket_manager

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    tags=["websocket"],
    responses={404: {"description": "Not found"}},
)


@router.websocket("/simulations/{simulation_id}")
async def simulation_websocket(websocket: WebSocket, simulation_id: str):
    """
    WebSocket endpoint for real-time simulation updates.

    Args:
        websocket: WebSocket connection
        simulation_id: Simulation ID
    """
    # Get WebSocket manager
    websocket_manager = get_websocket_manager()

    # Connect WebSocket
    await websocket_manager.connect(websocket, simulation_id)

    try:
        # Send welcome message
        await websocket_manager.send_info(
            simulation_id=simulation_id,
            message=f"Connected to simulation {simulation_id}",
            data={},
        )

        # Handle client messages
        await websocket_manager.handle_client_message(websocket, simulation_id)

    except WebSocketDisconnect:
        # Disconnect WebSocket
        websocket_manager.disconnect(websocket, simulation_id)

    except Exception as e:
        # Log error
        logger.error(
            "WebSocket error",
            simulation_id=simulation_id,
            error=str(e),
        )

        # Disconnect WebSocket
        websocket_manager.disconnect(websocket, simulation_id)
