"""
Error handling module for the EQU IHOME SIM ENGINE v2.

This module provides centralized error handling functionality for the simulation engine.
"""

import sys
import traceback
from enum import Enum
from typing import Dict, Any, Optional, List, Type, Callable

import structlog

logger = structlog.get_logger(__name__)


class ErrorCategory(str, Enum):
    """Error categories for the simulation engine."""
    
    VALIDATION = "validation"
    RUNTIME = "runtime"
    SYSTEM = "system"
    DATA = "data"
    CONFIGURATION = "configuration"
    NETWORK = "network"
    UNKNOWN = "unknown"


class ErrorCode(str, Enum):
    """Error codes for the simulation engine."""
    
    # Validation errors
    INVALID_PARAMETER = "INVALID_PARAMETER"
    MISSING_PARAMETER = "MISSING_PARAMETER"
    PARAMETER_OUT_OF_RANGE = "PARAMETER_OUT_OF_RANGE"
    INVALID_CONFIGURATION = "INVALID_CONFIGURATION"
    
    # Runtime errors
    CALCULATION_ERROR = "CALCULATION_ERROR"
    DIVISION_BY_ZERO = "DIVISION_BY_ZERO"
    OVERFLOW_ERROR = "OVERFLOW_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    
    # System errors
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    MEMORY_ERROR = "MEMORY_ERROR"
    
    # Data errors
    DATA_NOT_FOUND = "DATA_NOT_FOUND"
    DATA_CORRUPTION = "DATA_CORRUPTION"
    DATA_TYPE_ERROR = "DATA_TYPE_ERROR"
    
    # Configuration errors
    CONFIG_NOT_FOUND = "CONFIG_NOT_FOUND"
    CONFIG_PARSE_ERROR = "CONFIG_PARSE_ERROR"
    
    # Network errors
    NETWORK_ERROR = "NETWORK_ERROR"
    API_ERROR = "API_ERROR"
    
    # Unknown errors
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class SimulationError(Exception):
    """Base exception class for simulation errors."""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ):
        """
        Initialize a simulation error.
        
        Args:
            message: Error message
            code: Error code
            category: Error category
            details: Additional error details
            original_exception: Original exception that caused this error
        """
        self.message = message
        self.code = code
        self.category = category
        self.details = details or {}
        self.original_exception = original_exception
        
        # Add module and function information
        frame = sys._getframe(1)
        self.module = frame.f_globals.get("__name__", "unknown")
        self.function = frame.f_code.co_name
        
        # Add traceback
        if original_exception:
            self.traceback = "".join(traceback.format_exception(
                type(original_exception),
                original_exception,
                original_exception.__traceback__,
            ))
        else:
            self.traceback = "".join(traceback.format_stack()[:-1])
        
        # Call parent constructor
        super().__init__(message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the error to a dictionary.
        
        Returns:
            Dictionary representation of the error
        """
        result = {
            "message": self.message,
            "code": self.code,
            "category": self.category,
            "module": self.module,
            "function": self.function,
            "details": self.details,
        }
        
        # Add traceback in development mode
        if "dev" in self.details.get("environment", ""):
            result["traceback"] = self.traceback
        
        return result


class ValidationError(SimulationError):
    """Exception raised for validation errors."""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.INVALID_PARAMETER,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ):
        """
        Initialize a validation error.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            original_exception: Original exception that caused this error
        """
        super().__init__(
            message=message,
            code=code,
            category=ErrorCategory.VALIDATION,
            details=details,
            original_exception=original_exception,
        )


class RuntimeError(SimulationError):
    """Exception raised for runtime errors."""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.CALCULATION_ERROR,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ):
        """
        Initialize a runtime error.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            original_exception: Original exception that caused this error
        """
        super().__init__(
            message=message,
            code=code,
            category=ErrorCategory.RUNTIME,
            details=details,
            original_exception=original_exception,
        )


class SystemError(SimulationError):
    """Exception raised for system errors."""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.UNKNOWN_ERROR,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ):
        """
        Initialize a system error.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            original_exception: Original exception that caused this error
        """
        super().__init__(
            message=message,
            code=code,
            category=ErrorCategory.SYSTEM,
            details=details,
            original_exception=original_exception,
        )


class DataError(SimulationError):
    """Exception raised for data errors."""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.DATA_NOT_FOUND,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ):
        """
        Initialize a data error.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            original_exception: Original exception that caused this error
        """
        super().__init__(
            message=message,
            code=code,
            category=ErrorCategory.DATA,
            details=details,
            original_exception=original_exception,
        )


class ConfigurationError(SimulationError):
    """Exception raised for configuration errors."""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.CONFIG_NOT_FOUND,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ):
        """
        Initialize a configuration error.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            original_exception: Original exception that caused this error
        """
        super().__init__(
            message=message,
            code=code,
            category=ErrorCategory.CONFIGURATION,
            details=details,
            original_exception=original_exception,
        )


class NetworkError(SimulationError):
    """Exception raised for network errors."""
    
    def __init__(
        self,
        message: str,
        code: ErrorCode = ErrorCode.NETWORK_ERROR,
        details: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None,
    ):
        """
        Initialize a network error.
        
        Args:
            message: Error message
            code: Error code
            details: Additional error details
            original_exception: Original exception that caused this error
        """
        super().__init__(
            message=message,
            code=code,
            category=ErrorCategory.NETWORK,
            details=details,
            original_exception=original_exception,
        )


# Exception mapping
EXCEPTION_MAP: Dict[Type[Exception], Callable[[Exception], SimulationError]] = {
    ValueError: lambda e: ValidationError(str(e), original_exception=e),
    TypeError: lambda e: ValidationError(str(e), code=ErrorCode.DATA_TYPE_ERROR, original_exception=e),
    KeyError: lambda e: DataError(f"Key not found: {e}", code=ErrorCode.DATA_NOT_FOUND, original_exception=e),
    FileNotFoundError: lambda e: SystemError(str(e), code=ErrorCode.FILE_NOT_FOUND, original_exception=e),
    PermissionError: lambda e: SystemError(str(e), code=ErrorCode.PERMISSION_DENIED, original_exception=e),
    MemoryError: lambda e: SystemError(str(e), code=ErrorCode.MEMORY_ERROR, original_exception=e),
    ZeroDivisionError: lambda e: RuntimeError(str(e), code=ErrorCode.DIVISION_BY_ZERO, original_exception=e),
    OverflowError: lambda e: RuntimeError(str(e), code=ErrorCode.OVERFLOW_ERROR, original_exception=e),
    TimeoutError: lambda e: RuntimeError(str(e), code=ErrorCode.TIMEOUT_ERROR, original_exception=e),
}


def handle_exception(exception: Exception) -> SimulationError:
    """
    Handle an exception by converting it to a SimulationError.
    
    Args:
        exception: Exception to handle
        
    Returns:
        SimulationError instance
    """
    # If it's already a SimulationError, return it
    if isinstance(exception, SimulationError):
        return exception
    
    # Check if we have a mapping for this exception type
    for exception_type, handler in EXCEPTION_MAP.items():
        if isinstance(exception, exception_type):
            return handler(exception)
    
    # If no mapping found, create a generic SimulationError
    return SimulationError(
        message=str(exception),
        code=ErrorCode.UNKNOWN_ERROR,
        category=ErrorCategory.UNKNOWN,
        original_exception=exception,
    )


def log_error(error: SimulationError) -> None:
    """
    Log an error with appropriate context.
    
    Args:
        error: Error to log
    """
    log_context = {
        "error_code": error.code,
        "error_category": error.category,
        "module": error.module,
        "function": error.function,
    }
    
    # Add details to log context
    log_context.update(error.details)
    
    # Log the error
    logger.error(error.message, **log_context)


def format_error_response(error: SimulationError) -> Dict[str, Any]:
    """
    Format an error for API response.
    
    Args:
        error: Error to format
        
    Returns:
        Formatted error response
    """
    return {
        "error": {
            "message": error.message,
            "code": error.code,
            "category": error.category,
            "details": error.details,
        }
    }
