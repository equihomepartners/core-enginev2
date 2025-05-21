"""
Tests for the config_loader module.
"""

import json
import pytest
from pathlib import Path
from typing import Dict, Any

from src.config.config_loader import (
    load_config,
    load_config_from_dict,
    get_default_config,
    ConfigValidationError,
    SimulationConfig,
)


def test_load_config(sample_config_file: Path) -> None:
    """Test loading a configuration from a file."""
    config = load_config(str(sample_config_file))
    assert isinstance(config, SimulationConfig)
    assert config.fund_size == 100000000
    assert config.fund_term == 10
    assert config.vintage_year == 2023
    assert config.zone_allocations.green == 0.6
    assert config.zone_allocations.orange == 0.3
    assert config.zone_allocations.red == 0.1


def test_load_config_file_not_found() -> None:
    """Test loading a configuration from a non-existent file."""
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_file.json")


def test_load_config_from_dict(sample_config: Dict[str, Any]) -> None:
    """Test loading a configuration from a dictionary."""
    config = load_config_from_dict(sample_config)
    assert isinstance(config, SimulationConfig)
    assert config.fund_size == 100000000
    assert config.fund_term == 10
    assert config.vintage_year == 2023
    assert config.zone_allocations.green == 0.6
    assert config.zone_allocations.orange == 0.3
    assert config.zone_allocations.red == 0.1


def test_load_config_from_dict_invalid() -> None:
    """Test loading an invalid configuration from a dictionary."""
    invalid_config = {
        "fund_size": -100000000,  # Invalid: negative fund size
        "fund_term": 10,
        "vintage_year": 2023,
    }
    
    with pytest.raises(ConfigValidationError):
        load_config_from_dict(invalid_config)


def test_get_default_config() -> None:
    """Test getting a default configuration."""
    config = get_default_config()
    assert isinstance(config, SimulationConfig)
    assert config.fund_size == 100000000
    assert config.fund_term == 10
    assert config.vintage_year == 2023
    assert config.zone_allocations.green == 0.6
    assert config.zone_allocations.orange == 0.3
    assert config.zone_allocations.red == 0.1


def test_max_ltv_validation() -> None:
    """Test validation of max_ltv."""
    config_dict = {
        "fund_size": 100000000,
        "fund_term": 10,
        "vintage_year": 2023,
        "max_ltv": 0.9,  # Invalid: max_ltv > 0.85
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
    
    with pytest.raises(ConfigValidationError):
        load_config_from_dict(config_dict)


def test_zone_allocation_validation() -> None:
    """Test validation of zone allocations."""
    config_dict = {
        "fund_size": 100000000,
        "fund_term": 10,
        "vintage_year": 2023,
        "zone_allocations": {
            "green": 0.7,  # Invalid: allocation > 0.6
            "orange": 0.2,
            "red": 0.1
        },
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
    
    with pytest.raises(ConfigValidationError):
        load_config_from_dict(config_dict)


def test_loan_size_range_validation() -> None:
    """Test validation of loan size range."""
    config_dict = {
        "fund_size": 100000000,
        "fund_term": 10,
        "vintage_year": 2023,
        "min_loan_size": 200000,
        "max_loan_size": 100000,  # Invalid: max < min
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
    
    with pytest.raises(ConfigValidationError):
        load_config_from_dict(config_dict)


def test_ltv_range_validation() -> None:
    """Test validation of LTV range."""
    config_dict = {
        "fund_size": 100000000,
        "fund_term": 10,
        "vintage_year": 2023,
        "min_ltv": 0.7,
        "max_ltv": 0.6,  # Invalid: max < min
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
    
    with pytest.raises(ConfigValidationError):
        load_config_from_dict(config_dict)
