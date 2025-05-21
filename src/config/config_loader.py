"""
Configuration loader module for the EQU IHOME SIM ENGINE v2.

This module is responsible for loading, validating, and providing access to
simulation configuration parameters.
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional, Union, List

import structlog
from pydantic import BaseModel, Field, validator

logger = structlog.get_logger(__name__)


class ConfigValidationError(Exception):
    """Raised when configuration validation fails."""
    pass


class ConfigLoadError(Exception):
    """Raised when configuration loading fails."""
    pass


class ZoneAllocations(BaseModel):
    """Zone allocations configuration."""
    green: float = Field(0.6, ge=0, le=1, description="Green zone allocation (0-1)")
    orange: float = Field(0.3, ge=0, le=1, description="Orange zone allocation (0-1)")
    red: float = Field(0.1, ge=0, le=1, description="Red zone allocation (0-1)")
    
    @validator("green", "orange", "red")
    def validate_allocation(cls, v: float) -> float:
        """Validate that allocations are between 0 and 1."""
        if v < 0 or v > 1:
            raise ValueError(f"Allocation must be between 0 and 1, got {v}")
        return v
    
    @validator("red")
    def validate_total(cls, v: float, values: Dict[str, float]) -> float:
        """Validate that allocations sum to 1."""
        total = v
        if "green" in values:
            total += values["green"]
        if "orange" in values:
            total += values["orange"]
        
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"Allocations must sum to 1, got {total}")
        
        return v


class ZoneRates(BaseModel):
    """Zone-specific rates configuration."""
    green: float = Field(..., ge=0, le=1, description="Green zone rate (0-1)")
    orange: float = Field(..., ge=0, le=1, description="Orange zone rate (0-1)")
    red: float = Field(..., ge=0, le=1, description="Red zone rate (0-1)")


class SimulationConfig(BaseModel):
    """Simulation configuration parameters."""
    fund_size: float = Field(100000000, ge=1000000, description="Fund size in dollars")
    fund_term: int = Field(10, ge=1, le=30, description="Fund term in years")
    vintage_year: int = Field(2023, ge=1900, le=2100, description="Fund vintage year")
    gp_commitment_percentage: float = Field(0.0, ge=0, le=1, description="GP commitment percentage (0-1)")
    hurdle_rate: float = Field(0.08, ge=0, le=1, description="Hurdle rate (0-1)")
    carried_interest_rate: float = Field(0.20, ge=0, le=1, description="Carried interest rate (0-1)")
    waterfall_structure: str = Field("european", description="Waterfall structure type")
    management_fee_rate: float = Field(0.02, ge=0, le=0.05, description="Management fee rate (0-1)")
    management_fee_basis: str = Field("committed_capital", description="Basis for management fee calculation")
    catch_up_rate: float = Field(0.0, ge=0, le=1, description="GP catch-up rate (0-1)")
    reinvestment_period: int = Field(5, ge=0, le=30, description="Reinvestment period in years")
    avg_loan_size: float = Field(250000, ge=10000, description="Average loan size in dollars")
    loan_size_std_dev: float = Field(50000, ge=0, description="Standard deviation of loan sizes")
    min_loan_size: float = Field(100000, ge=1000, description="Minimum loan size in dollars")
    max_loan_size: float = Field(500000, ge=10000, description="Maximum loan size in dollars")
    avg_loan_term: float = Field(5, ge=0.1, description="Average loan term in years")
    avg_loan_interest_rate: float = Field(0.05, ge=0, le=1, description="Average loan interest rate (0-1)")
    avg_loan_ltv: float = Field(0.75, ge=0, le=1, description="Average loan LTV ratio (0-1)")
    ltv_std_dev: float = Field(0.05, ge=0, le=0.5, description="Standard deviation of LTV ratios")
    min_ltv: float = Field(0.5, ge=0, le=1, description="Minimum LTV ratio (0-1)")
    max_ltv: float = Field(0.85, ge=0, le=1, description="Maximum LTV ratio (0-1)")
    zone_allocations: ZoneAllocations = Field(default_factory=ZoneAllocations, description="Target zone allocations")
    appreciation_rates: ZoneRates = Field(..., description="Zone-specific appreciation rates")
    default_rates: ZoneRates = Field(..., description="Zone-specific default rates")
    recovery_rates: ZoneRates = Field(..., description="Zone-specific recovery rates")
    monte_carlo_enabled: bool = Field(False, description="Whether to run Monte Carlo simulation")
    num_simulations: int = Field(1000, ge=1, le=10000, description="Number of Monte Carlo simulations")
    
    @validator("max_ltv")
    def validate_max_ltv(cls, v: float) -> float:
        """Validate that max_ltv is not greater than 0.85."""
        if v > 0.85:
            raise ValueError(f"Maximum LTV cannot exceed 0.85, got {v}")
        return v
    
    @validator("min_loan_size", "max_loan_size")
    def validate_loan_size_range(cls, v: float, values: Dict[str, Any], field: Field) -> float:
        """Validate that min_loan_size <= max_loan_size."""
        if field.name == "max_loan_size" and "min_loan_size" in values:
            if v < values["min_loan_size"]:
                raise ValueError(f"Maximum loan size ({v}) cannot be less than minimum loan size ({values['min_loan_size']})")
        return v
    
    @validator("min_ltv", "max_ltv")
    def validate_ltv_range(cls, v: float, values: Dict[str, Any], field: Field) -> float:
        """Validate that min_ltv <= max_ltv."""
        if field.name == "max_ltv" and "min_ltv" in values:
            if v < values["min_ltv"]:
                raise ValueError(f"Maximum LTV ({v}) cannot be less than minimum LTV ({values['min_ltv']})")
        return v
    
    class Config:
        """Pydantic configuration."""
        extra = "allow"


def load_config(config_path: str) -> SimulationConfig:
    """
    Load and validate a simulation configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration JSON file
        
    Returns:
        A validated SimulationConfig object
        
    Raises:
        ConfigValidationError: If the configuration is invalid
        FileNotFoundError: If the configuration file does not exist
    """
    logger.info("Loading configuration", path=config_path)
    
    try:
        with open(config_path, "r") as f:
            config_dict = json.load(f)
        
        return load_config_from_dict(config_dict)
    
    except FileNotFoundError:
        logger.error("Configuration file not found", path=config_path)
        raise
    
    except json.JSONDecodeError as e:
        logger.error("Invalid JSON in configuration file", path=config_path, error=str(e))
        raise ConfigLoadError(f"Invalid JSON in configuration file: {str(e)}")


def load_config_from_dict(config_dict: Dict[str, Any]) -> SimulationConfig:
    """
    Load and validate a simulation configuration from a dictionary.
    
    Args:
        config_dict: Dictionary containing configuration parameters
        
    Returns:
        A validated SimulationConfig object
        
    Raises:
        ConfigValidationError: If the configuration is invalid
    """
    logger.debug("Validating configuration")
    
    try:
        # Set default values for required nested objects if not provided
        if "appreciation_rates" not in config_dict:
            config_dict["appreciation_rates"] = {
                "green": 0.05,
                "orange": 0.03,
                "red": 0.01
            }
        
        if "default_rates" not in config_dict:
            config_dict["default_rates"] = {
                "green": 0.01,
                "orange": 0.03,
                "red": 0.05
            }
        
        if "recovery_rates" not in config_dict:
            config_dict["recovery_rates"] = {
                "green": 0.9,
                "orange": 0.8,
                "red": 0.7
            }
        
        config = SimulationConfig(**config_dict)
        
        # Additional validation
        validate_guardrails(config)
        
        return config
    
    except Exception as e:
        logger.error("Configuration validation failed", error=str(e))
        raise ConfigValidationError(f"Configuration validation failed: {str(e)}")


def get_default_config() -> SimulationConfig:
    """
    Get a default simulation configuration with all parameters set to their default values.
    
    Returns:
        A default SimulationConfig object
    """
    logger.debug("Creating default configuration")
    
    config_dict = {
        "appreciation_rates": {
            "green": 0.05,
            "orange": 0.03,
            "red": 0.01
        },
        "default_rates": {
            "green": 0.01,
            "orange": 0.03,
            "red": 0.05
        },
        "recovery_rates": {
            "green": 0.9,
            "orange": 0.8,
            "red": 0.7
        }
    }
    
    return SimulationConfig(**config_dict)


def validate_guardrails(config: SimulationConfig) -> None:
    """
    Validate that the configuration meets all guardrail requirements.
    
    Args:
        config: The configuration to validate
        
    Raises:
        ConfigValidationError: If the configuration violates any guardrails
    """
    # Check LTV guardrail
    if config.max_ltv > 0.85:
        raise ConfigValidationError(f"Maximum LTV cannot exceed 0.85, got {config.max_ltv}")
    
    # Check zone allocation guardrail
    for zone, allocation in config.zone_allocations.dict().items():
        if allocation > 0.6:
            raise ConfigValidationError(f"Allocation to {zone} zone cannot exceed 0.6, got {allocation}")
    
    # Check WAL guardrail
    # This would require a more complex calculation in a real implementation
    # For now, we'll just use the average loan term as a proxy
    if config.avg_loan_term > 8 and config.fund_term <= 6:
        logger.warning(
            "Average loan term exceeds 8 years while fund term is 6 years or less",
            avg_loan_term=config.avg_loan_term,
            fund_term=config.fund_term
        )
