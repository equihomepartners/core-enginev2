"""
Configuration validation module for the EQU IHOME SIM ENGINE v2.

This module provides utilities for validating simulation configuration.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Tuple

import structlog
from pydantic import BaseModel, ValidationError

from src.config.param_registry import get_registry

logger = structlog.get_logger(__name__)


class ValidationResult:
    """
    Result of a validation operation.
    
    Attributes:
        valid: Whether the validation passed
        errors: List of validation errors
    """
    
    def __init__(self, valid: bool = True, errors: Optional[List[str]] = None) -> None:
        """
        Initialize a validation result.
        
        Args:
            valid: Whether the validation passed
            errors: List of validation errors
        """
        self.valid = valid
        self.errors = errors or []
    
    def __bool__(self) -> bool:
        """
        Convert to boolean.
        
        Returns:
            True if valid, False otherwise
        """
        return self.valid
    
    def add_error(self, error: str) -> None:
        """
        Add a validation error.
        
        Args:
            error: Validation error message
        """
        self.errors.append(error)
        self.valid = False
    
    def merge(self, other: "ValidationResult") -> None:
        """
        Merge with another validation result.
        
        Args:
            other: Other validation result
        """
        if not other.valid:
            self.valid = False
            self.errors.extend(other.errors)


def validate_config(config: Dict[str, Any]) -> ValidationResult:
    """
    Validate a simulation configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Validation result
    """
    result = ValidationResult()
    
    # Validate using parameter registry
    registry = get_registry()
    
    for name, value in config.items():
        if not registry.validate_parameter(name, value):
            result.add_error(f"Invalid parameter: {name}")
    
    # Check required parameters
    for name, parameter in registry.get_parameters().items():
        if parameter.required and name not in config:
            result.add_error(f"Missing required parameter: {name}")
    
    # Validate guardrails
    guardrail_result = validate_guardrails(config)
    result.merge(guardrail_result)
    
    return result


def validate_guardrails(config: Dict[str, Any]) -> ValidationResult:
    """
    Validate guardrails for a simulation configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Validation result
    """
    result = ValidationResult()
    
    # Check LTV guardrail
    if "max_ltv" in config and config["max_ltv"] > 0.85:
        result.add_error(f"Maximum LTV cannot exceed 0.85, got {config['max_ltv']}")
    
    # Check zone allocation guardrail
    if "zone_allocations" in config:
        zone_allocations = config["zone_allocations"]
        for zone, allocation in zone_allocations.items():
            if allocation > 0.6:
                result.add_error(f"Allocation to {zone} zone cannot exceed 0.6, got {allocation}")
    
    # Check WAL guardrail
    if "avg_loan_term" in config and "fund_term" in config:
        avg_loan_term = config["avg_loan_term"]
        fund_term = config["fund_term"]
        if avg_loan_term > 8 and fund_term <= 6:
            logger.warning(
                "Average loan term exceeds 8 years while fund term is 6 years or less",
                avg_loan_term=avg_loan_term,
                fund_term=fund_term,
            )
    
    return result


def validate_config_file(config_path: str) -> ValidationResult:
    """
    Validate a simulation configuration file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Validation result
    """
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        
        return validate_config(config)
    
    except FileNotFoundError:
        result = ValidationResult(valid=False)
        result.add_error(f"Configuration file not found: {config_path}")
        return result
    
    except json.JSONDecodeError as e:
        result = ValidationResult(valid=False)
        result.add_error(f"Invalid JSON in configuration file: {str(e)}")
        return result
    
    except Exception as e:
        result = ValidationResult(valid=False)
        result.add_error(f"Error validating configuration file: {str(e)}")
        return result
