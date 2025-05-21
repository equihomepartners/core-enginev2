"""
Pytest configuration file for the EQU IHOME SIM ENGINE v2.

This module provides fixtures for testing.
"""

import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Generator

import pytest
import numpy as np

from src.config.config_loader import SimulationConfig
from src.monte_carlo.rng_factory import RNGFactory, set_rng_factory


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """
    Get the test data directory.
    
    Returns:
        Path to the test data directory
    """
    return Path(__file__).parent / "data"


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    Create a temporary directory for test files.
    
    Yields:
        Path to the temporary directory
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_config() -> Dict[str, Any]:
    """
    Get a sample simulation configuration.
    
    Returns:
        Sample configuration dictionary
    """
    return {
        "fund_size": 100000000,
        "fund_term": 10,
        "vintage_year": 2023,
        "gp_commitment_percentage": 0.0,
        "hurdle_rate": 0.08,
        "carried_interest_rate": 0.20,
        "waterfall_structure": "european",
        "management_fee_rate": 0.02,
        "management_fee_basis": "committed_capital",
        "catch_up_rate": 0.0,
        "reinvestment_period": 5,
        "avg_loan_size": 250000,
        "loan_size_std_dev": 50000,
        "min_loan_size": 100000,
        "max_loan_size": 500000,
        "avg_loan_term": 5,
        "avg_loan_interest_rate": 0.05,
        "avg_loan_ltv": 0.75,
        "ltv_std_dev": 0.05,
        "min_ltv": 0.5,
        "max_ltv": 0.85,
        "zone_allocations": {
            "green": 0.6,
            "orange": 0.3,
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
        },
        "monte_carlo_enabled": False,
        "num_simulations": 1000
    }


@pytest.fixture
def sample_config_file(temp_dir: Path, sample_config: Dict[str, Any]) -> Path:
    """
    Create a sample configuration file.
    
    Args:
        temp_dir: Temporary directory
        sample_config: Sample configuration dictionary
        
    Returns:
        Path to the sample configuration file
    """
    config_file = temp_dir / "config.json"
    
    with open(config_file, "w") as f:
        json.dump(sample_config, f, indent=2)
    
    return config_file


@pytest.fixture
def sample_config_obj(sample_config: Dict[str, Any]) -> SimulationConfig:
    """
    Get a sample SimulationConfig object.
    
    Args:
        sample_config: Sample configuration dictionary
        
    Returns:
        Sample SimulationConfig object
    """
    return SimulationConfig(**sample_config)


@pytest.fixture(autouse=True)
def deterministic_rng() -> Generator[None, None, None]:
    """
    Set up a deterministic RNG factory for tests.
    
    This fixture is automatically used in all tests to ensure reproducibility.
    """
    # Save the original environment variable
    original_seed = os.environ.get("SIM_SEED")
    
    # Set a fixed seed for tests
    os.environ["SIM_SEED"] = "test_seed"
    
    # Create a new RNG factory with the fixed seed
    set_rng_factory(RNGFactory("test_seed"))
    
    yield
    
    # Restore the original environment variable
    if original_seed is not None:
        os.environ["SIM_SEED"] = original_seed
    else:
        os.environ.pop("SIM_SEED", None)
