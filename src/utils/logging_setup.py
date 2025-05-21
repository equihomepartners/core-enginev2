"""
Logging setup module for the EQU IHOME SIM ENGINE v2.

This module configures structured logging with JSON format and trace IDs.
"""

import logging
import os
import sys
import uuid
from typing import Dict, Any, Optional

import structlog
from pythonjsonlogger import jsonlogger


def setup_logging(verbose: bool = False, run_id: Optional[str] = None) -> None:
    """
    Set up structured logging with JSON format and trace IDs.
    
    Args:
        verbose: Whether to enable DEBUG level logging
        run_id: Unique identifier for the current run, generated if not provided
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Generate a run_id if not provided
    if run_id is None:
        run_id = str(uuid.uuid4())
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard logging
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
    
    # Create a JSON formatter
    formatter = jsonlogger.JsonFormatter(
        fmt="%(timestamp)s %(level)s %(name)s %(message)s",
        rename_fields={"levelname": "level", "module": "logger"},
    )
    
    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # Create a file handler if enabled
    log_file = os.environ.get("SIM_LOG_FILE")
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        root_logger.addHandler(file_handler)
    
    # Set the run_id in the global processor context
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(run_id=run_id)
    
    # Log the setup
    logger = structlog.get_logger(__name__)
    logger.info(
        "Logging initialized",
        level=logging.getLevelName(log_level),
        run_id=run_id,
        verbose=verbose,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a logger with the given name.
    
    Args:
        name: Logger name
        
    Returns:
        A structlog BoundLogger
    """
    return structlog.get_logger(name)


def with_context(**context: Any) -> Dict[str, Any]:
    """
    Add context to the current logger context.
    
    Args:
        **context: Context key-value pairs
        
    Returns:
        The updated context
    """
    structlog.contextvars.bind_contextvars(**context)
    return context
