"""
Tests for the RNG factory module.
"""

import os
import pytest
import numpy as np

from src.monte_carlo.rng_factory import (
    RNGFactory,
    get_rng_factory,
    set_rng_factory,
    get_rng,
    reset_rng_factory,
)


def test_rng_factory_init() -> None:
    """Test RNG factory initialization."""
    # Test case 1: With integer seed
    factory = RNGFactory(42)
    assert factory.base_seed == 42
    
    # Test case 2: With string seed
    factory = RNGFactory("test_seed")
    assert isinstance(factory.base_seed, int)
    
    # Test case 3: With no seed
    factory = RNGFactory()
    assert isinstance(factory.base_seed, int)


def test_rng_factory_get_rng() -> None:
    """Test getting an RNG from the factory."""
    factory = RNGFactory(42)
    
    # Test case 1: Get RNG for a purpose
    rng1 = factory.get_rng("test")
    assert isinstance(rng1, np.random.Generator)
    
    # Test case 2: Get RNG for the same purpose again (should be cached)
    rng2 = factory.get_rng("test")
    assert rng1 is rng2
    
    # Test case 3: Get RNG for a different purpose
    rng3 = factory.get_rng("other")
    assert rng1 is not rng3
    
    # Test case 4: Get RNG for the same purpose but different instance
    rng4 = factory.get_rng("test", 1)
    assert rng1 is not rng4


def test_rng_factory_reset() -> None:
    """Test resetting the RNG factory."""
    factory = RNGFactory(42)
    
    # Get an RNG
    rng1 = factory.get_rng("test")
    
    # Reset the factory
    factory.reset()
    
    # Get an RNG for the same purpose again (should be a new instance)
    rng2 = factory.get_rng("test")
    assert rng1 is not rng2


def test_rng_factory_deterministic() -> None:
    """Test that the RNG factory produces deterministic results."""
    # Create two factories with the same seed
    factory1 = RNGFactory(42)
    factory2 = RNGFactory(42)
    
    # Get RNGs for the same purpose
    rng1 = factory1.get_rng("test")
    rng2 = factory2.get_rng("test")
    
    # Generate random numbers
    nums1 = rng1.random(10)
    nums2 = rng2.random(10)
    
    # They should be the same
    np.testing.assert_array_equal(nums1, nums2)


def test_get_rng_factory() -> None:
    """Test getting the global RNG factory."""
    # Save the original environment variable
    original_seed = os.environ.get("SIM_SEED")
    
    try:
        # Set the environment variable
        os.environ["SIM_SEED"] = "test_seed"
        
        # Reset the global factory
        reset_rng_factory()
        
        # Get the factory
        factory = get_rng_factory()
        assert isinstance(factory, RNGFactory)
        
        # Get it again (should be the same instance)
        factory2 = get_rng_factory()
        assert factory is factory2
    
    finally:
        # Restore the original environment variable
        if original_seed is not None:
            os.environ["SIM_SEED"] = original_seed
        else:
            os.environ.pop("SIM_SEED", None)


def test_set_rng_factory() -> None:
    """Test setting the global RNG factory."""
    # Create a factory
    factory = RNGFactory(42)
    
    # Set it as the global factory
    set_rng_factory(factory)
    
    # Get the global factory
    factory2 = get_rng_factory()
    assert factory is factory2


def test_get_rng() -> None:
    """Test getting an RNG from the global factory."""
    # Create a factory
    factory = RNGFactory(42)
    
    # Set it as the global factory
    set_rng_factory(factory)
    
    # Get an RNG
    rng = get_rng("test")
    assert isinstance(rng, np.random.Generator)
    
    # Get it again (should be the same instance)
    rng2 = get_rng("test")
    assert rng is rng2


def test_reset_rng_factory() -> None:
    """Test resetting the global RNG factory."""
    # Create a factory
    factory = RNGFactory(42)
    
    # Set it as the global factory
    set_rng_factory(factory)
    
    # Get an RNG
    rng1 = get_rng("test")
    
    # Reset the global factory
    reset_rng_factory()
    
    # Get an RNG for the same purpose again (should be a new instance)
    rng2 = get_rng("test")
    assert rng1 is not rng2
