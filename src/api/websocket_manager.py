"""
WebSocket manager module for the EQU IHOME SIM ENGINE v2.

This module provides WebSocket functionality for real-time progress updates.
"""

import asyncio
import json
from enum import Enum
from typing import Dict, Any, Optional, List, Set, Callable, Awaitable

import structlog
from fastapi import WebSocket, WebSocketDisconnect

logger = structlog.get_logger(__name__)


class MessageType(str, Enum):
    """Message types for WebSocket communication."""
    
    PROGRESS = "progress"
    RESULT = "result"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"
    CANCEL = "cancel"


class WebSocketManager:
    """
    Manager for WebSocket connections.
    
    This class manages WebSocket connections and provides methods for sending
    messages to connected clients.
    """
    
    def __init__(self):
        """Initialize the WebSocket manager."""
        # Active connections by simulation ID
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        
        # Cancellation flags by simulation ID
        self.cancellation_flags: Dict[str, bool] = {}
        
        # Message handlers by message type
        self.message_handlers: Dict[str, Callable[[Dict[str, Any]], Awaitable[None]]] = {}
    
    async def connect(self, websocket: WebSocket, simulation_id: str) -> None:
        """
        Connect a WebSocket client.
        
        Args:
            websocket: WebSocket connection
            simulation_id: Simulation ID
        """
        await websocket.accept()
        
        # Initialize connection set for this simulation ID if it doesn't exist
        if simulation_id not in self.active_connections:
            self.active_connections[simulation_id] = set()
            self.cancellation_flags[simulation_id] = False
        
        # Add connection to the set
        self.active_connections[simulation_id].add(websocket)
        
        logger.info(
            "WebSocket client connected",
            simulation_id=simulation_id,
            client_count=len(self.active_connections[simulation_id]),
        )
    
    def disconnect(self, websocket: WebSocket, simulation_id: str) -> None:
        """
        Disconnect a WebSocket client.
        
        Args:
            websocket: WebSocket connection
            simulation_id: Simulation ID
        """
        # Remove connection from the set
        if simulation_id in self.active_connections:
            self.active_connections[simulation_id].discard(websocket)
            
            # Remove simulation ID if no connections left
            if not self.active_connections[simulation_id]:
                del self.active_connections[simulation_id]
                
                # Remove cancellation flag
                if simulation_id in self.cancellation_flags:
                    del self.cancellation_flags[simulation_id]
        
        logger.info(
            "WebSocket client disconnected",
            simulation_id=simulation_id,
            client_count=len(self.active_connections.get(simulation_id, set())),
        )
    
    async def send_message(
        self,
        simulation_id: str,
        message_type: MessageType,
        data: Dict[str, Any],
    ) -> None:
        """
        Send a message to all connected clients for a simulation.
        
        Args:
            simulation_id: Simulation ID
            message_type: Message type
            data: Message data
        """
        if simulation_id not in self.active_connections:
            logger.warning(
                "No WebSocket clients connected for simulation",
                simulation_id=simulation_id,
            )
            return
        
        # Create message
        message = {
            "type": message_type,
            "simulation_id": simulation_id,
            "data": data,
        }
        
        # Convert message to JSON
        message_json = json.dumps(message)
        
        # Send message to all connected clients
        disconnected_clients = set()
        for websocket in self.active_connections[simulation_id]:
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                logger.error(
                    "Error sending WebSocket message",
                    simulation_id=simulation_id,
                    error=str(e),
                )
                disconnected_clients.add(websocket)
        
        # Remove disconnected clients
        for websocket in disconnected_clients:
            self.disconnect(websocket, simulation_id)
    
    async def send_progress(
        self,
        simulation_id: str,
        module: str,
        progress: float,
        message: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Send a progress update to all connected clients for a simulation.
        
        Args:
            simulation_id: Simulation ID
            module: Module name
            progress: Progress percentage (0-100)
            message: Progress message
            data: Additional data
        """
        await self.send_message(
            simulation_id=simulation_id,
            message_type=MessageType.PROGRESS,
            data={
                "module": module,
                "progress": progress,
                "message": message,
                "data": data or {},
            },
        )
    
    async def send_result(
        self,
        simulation_id: str,
        result: Dict[str, Any],
    ) -> None:
        """
        Send a result to all connected clients for a simulation.
        
        Args:
            simulation_id: Simulation ID
            result: Simulation result
        """
        await self.send_message(
            simulation_id=simulation_id,
            message_type=MessageType.RESULT,
            data=result,
        )
    
    async def send_error(
        self,
        simulation_id: str,
        error: Dict[str, Any],
    ) -> None:
        """
        Send an error to all connected clients for a simulation.
        
        Args:
            simulation_id: Simulation ID
            error: Error details
        """
        await self.send_message(
            simulation_id=simulation_id,
            message_type=MessageType.ERROR,
            data=error,
        )
    
    async def send_info(
        self,
        simulation_id: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Send an info message to all connected clients for a simulation.
        
        Args:
            simulation_id: Simulation ID
            message: Info message
            data: Additional data
        """
        await self.send_message(
            simulation_id=simulation_id,
            message_type=MessageType.INFO,
            data={
                "message": message,
                "data": data or {},
            },
        )
    
    async def send_warning(
        self,
        simulation_id: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Send a warning message to all connected clients for a simulation.
        
        Args:
            simulation_id: Simulation ID
            message: Warning message
            data: Additional data
        """
        await self.send_message(
            simulation_id=simulation_id,
            message_type=MessageType.WARNING,
            data={
                "message": message,
                "data": data or {},
            },
        )
    
    def is_cancelled(self, simulation_id: str) -> bool:
        """
        Check if a simulation has been cancelled.
        
        Args:
            simulation_id: Simulation ID
            
        Returns:
            True if the simulation has been cancelled, False otherwise
        """
        return self.cancellation_flags.get(simulation_id, False)
    
    def set_cancelled(self, simulation_id: str, cancelled: bool = True) -> None:
        """
        Set the cancellation flag for a simulation.
        
        Args:
            simulation_id: Simulation ID
            cancelled: Whether the simulation is cancelled
        """
        self.cancellation_flags[simulation_id] = cancelled
        
        logger.info(
            "Simulation cancellation flag set",
            simulation_id=simulation_id,
            cancelled=cancelled,
        )
    
    async def handle_client_message(
        self, websocket: WebSocket, simulation_id: str
    ) -> None:
        """
        Handle messages from a WebSocket client.
        
        Args:
            websocket: WebSocket connection
            simulation_id: Simulation ID
        """
        try:
            # Listen for messages
            while True:
                # Receive message
                message_json = await websocket.receive_text()
                
                try:
                    # Parse message
                    message = json.loads(message_json)
                    
                    # Get message type
                    message_type = message.get("type")
                    
                    # Handle cancellation
                    if message_type == MessageType.CANCEL:
                        self.set_cancelled(simulation_id)
                        logger.info(
                            "Simulation cancellation requested",
                            simulation_id=simulation_id,
                        )
                    
                    # Handle other message types
                    elif message_type in self.message_handlers:
                        await self.message_handlers[message_type](message)
                    
                    else:
                        logger.warning(
                            "Unknown WebSocket message type",
                            simulation_id=simulation_id,
                            message_type=message_type,
                        )
                
                except json.JSONDecodeError:
                    logger.error(
                        "Invalid WebSocket message format",
                        simulation_id=simulation_id,
                    )
        
        except WebSocketDisconnect:
            self.disconnect(websocket, simulation_id)
        
        except Exception as e:
            logger.error(
                "Error handling WebSocket message",
                simulation_id=simulation_id,
                error=str(e),
            )
            self.disconnect(websocket, simulation_id)


# Global WebSocket manager instance
_global_websocket_manager: Optional[WebSocketManager] = None


def get_websocket_manager() -> WebSocketManager:
    """
    Get the global WebSocket manager instance.
    
    Returns:
        The global WebSocket manager instance
    """
    global _global_websocket_manager
    
    if _global_websocket_manager is None:
        _global_websocket_manager = WebSocketManager()
    
    return _global_websocket_manager
