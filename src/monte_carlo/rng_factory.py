"""
Random number generator factory module for the EQU IHOME SIM ENGINE v2.

This module provides a factory for creating deterministic random number generators
with support for correlation, variation control, and reproducibility.
"""

import hashlib
import os
import json
from typing import Dict, Optional, Union, Tuple, List, Any, Callable

import numpy as np
import structlog
from scipy import stats

logger = structlog.get_logger(__name__)


class RNGFactory:
    """
    Factory for creating deterministic random number generators.

    This class ensures that all random number generators are created with proper
    seeding for reproducibility, with support for correlation between different
    random variables and control over variation factors.
    """

    def __init__(
        self,
        base_seed: Optional[Union[int, str]] = None,
        deterministic_mode: bool = False,
        correlation_matrix: Optional[Dict[str, Dict[str, float]]] = None,
        variation_factors: Optional[Dict[str, float]] = None,
    ):
        """
        Initialize the RNG factory.

        Args:
            base_seed: Base seed for all random number generators. If None, a random
                seed will be used. If a string, it will be hashed to create a seed.
            deterministic_mode: If True, uses fixed seeds for all randomness.
            correlation_matrix: Dictionary mapping purpose pairs to correlation coefficients.
                Example: {"price_path": {"default_rate": 0.7}} means price_path and default_rate
                have a correlation of 0.7.
            variation_factors: Dictionary mapping purposes to variation factors.
                Higher values mean more randomness, lower values mean more deterministic.
                Example: {"price_path": 0.05, "default_rate": 0.1}
        """
        # Set base seed
        if deterministic_mode:
            # In deterministic mode, always use the same seed
            self.base_seed = 42
            logger.info("Using deterministic mode with fixed seed", base_seed=self.base_seed)
        elif base_seed is None:
            # Use a random seed if none is provided
            self.base_seed = np.random.randint(0, 2**32 - 1)
            logger.info("Using random base seed", base_seed=self.base_seed)
        elif isinstance(base_seed, str):
            # Hash the string to create a seed
            self.base_seed = int(hashlib.sha256(base_seed.encode()).hexdigest(), 16) % (2**32)
            logger.info("Using hashed base seed", original=base_seed, base_seed=self.base_seed)
        else:
            # Use the provided seed
            self.base_seed = base_seed
            logger.info("Using provided base seed", base_seed=self.base_seed)

        # Set deterministic mode
        self.deterministic_mode = deterministic_mode

        # Set correlation matrix
        self.correlation_matrix = correlation_matrix or {}

        # Set variation factors
        self.variation_factors = variation_factors or {}

        # Default variation factor (used if not specified for a purpose)
        self.default_variation_factor = 1.0

        # Cache for RNG instances
        self._rng_cache: Dict[Tuple[str, int], np.random.Generator] = {}

        # Cache for correlated RNG instances
        self._correlated_rng_cache: Dict[Tuple[str, str, int], np.random.Generator] = {}

        # Register known purposes
        self.known_purposes = [
            "loan_generation",
            "price_path",
            "exit_simulator",
            "default_events",
            "prepayment_events",
            "appreciation_rates",
            "monte_carlo_outer",
            "monte_carlo_inner",
        ]

        # Log configuration
        logger.info(
            "RNG factory initialized",
            base_seed=self.base_seed,
            deterministic_mode=self.deterministic_mode,
            correlation_matrix=self.correlation_matrix,
            variation_factors=self.variation_factors,
        )

    def get_rng(self, purpose: str, instance_id: int = 0) -> np.random.Generator:
        """
        Get a random number generator for a specific purpose and instance.

        Args:
            purpose: Purpose of the RNG (e.g., "loan_generation", "price_path")
            instance_id: Instance ID for the RNG (e.g., simulation run number)

        Returns:
            A numpy random number generator
        """
        cache_key = (purpose, instance_id)

        if cache_key in self._rng_cache:
            return self._rng_cache[cache_key]

        # Create a seed based on the base seed, purpose, and instance ID
        if self.deterministic_mode:
            # In deterministic mode, use a fixed seed for each purpose
            purpose_hash = int(hashlib.sha256(purpose.encode()).hexdigest(), 16) % (2**32)
            seed = (self.base_seed + purpose_hash) % (2**32)
        else:
            # Create a unique seed based on all inputs
            seed_str = f"{self.base_seed}_{purpose}_{instance_id}"
            seed = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (2**32)

        # Create a new RNG
        rng = np.random.default_rng(seed)

        # Cache the RNG
        self._rng_cache[cache_key] = rng

        logger.debug(
            "Created RNG",
            purpose=purpose,
            instance_id=instance_id,
            seed=seed,
            base_seed=self.base_seed,
            deterministic_mode=self.deterministic_mode,
        )

        return rng

    def get_correlated_rng(
        self, purpose1: str, purpose2: str, correlation: float, instance_id: int = 0
    ) -> Tuple[np.random.Generator, np.random.Generator]:
        """
        Get a pair of correlated random number generators.

        Args:
            purpose1: First purpose
            purpose2: Second purpose
            correlation: Correlation coefficient between the two RNGs (-1 to 1)
            instance_id: Instance ID for the RNGs

        Returns:
            Tuple of (rng1, rng2) with the specified correlation
        """
        # Check if we already have a correlation defined in the matrix
        if purpose1 in self.correlation_matrix and purpose2 in self.correlation_matrix[purpose1]:
            correlation = self.correlation_matrix[purpose1][purpose2]
        elif purpose2 in self.correlation_matrix and purpose1 in self.correlation_matrix[purpose2]:
            correlation = self.correlation_matrix[purpose2][purpose1]

        # Ensure correlation is valid
        correlation = max(-1.0, min(1.0, correlation))

        # Get base RNGs
        rng1 = self.get_rng(purpose1, instance_id)

        # Check if we already have a correlated RNG in the cache
        cache_key = (purpose1, purpose2, instance_id)
        if cache_key in self._correlated_rng_cache:
            return rng1, self._correlated_rng_cache[cache_key]

        # Create a seed for the second RNG
        if self.deterministic_mode:
            # In deterministic mode, use a fixed seed
            seed2 = (
                self.base_seed
                + int(hashlib.sha256(purpose1.encode()).hexdigest(), 16) % (2**16)
                + int(hashlib.sha256(purpose2.encode()).hexdigest(), 16) % (2**16)
            ) % (2**32)
        else:
            # Create a unique seed
            seed_str = f"{self.base_seed}_{purpose1}_{purpose2}_{instance_id}_{correlation}"
            seed2 = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (2**32)

        # Create the second RNG
        rng2 = np.random.default_rng(seed2)

        # Cache the correlated RNG
        self._correlated_rng_cache[cache_key] = rng2

        logger.debug(
            "Created correlated RNGs",
            purpose1=purpose1,
            purpose2=purpose2,
            correlation=correlation,
            instance_id=instance_id,
        )

        return rng1, rng2

    def get_variation_factor(self, purpose: str) -> float:
        """
        Get the variation factor for a specific purpose.

        Args:
            purpose: Purpose of the RNG

        Returns:
            Variation factor (higher = more randomness, lower = more deterministic)
        """
        # If in deterministic mode, return a very small variation factor
        if self.deterministic_mode:
            return 0.01

        # Return the variation factor for the purpose, or the default if not specified
        return self.variation_factors.get(purpose, self.default_variation_factor)

    def generate_normal(
        self, purpose: str, mean: float = 0.0, std_dev: Optional[float] = None, instance_id: int = 0
    ) -> float:
        """
        Generate a normal random variable with controlled variation.

        Args:
            purpose: Purpose of the random variable
            mean: Mean of the normal distribution
            std_dev: Standard deviation of the normal distribution (if None, uses variation factor)
            instance_id: Instance ID

        Returns:
            Random value from a normal distribution
        """
        # Get the RNG for this purpose
        rng = self.get_rng(purpose, instance_id)

        # If std_dev is not provided, use the variation factor
        if std_dev is None:
            variation_factor = self.get_variation_factor(purpose)
            # Scale the standard deviation based on the mean and variation factor
            # Use absolute value of mean to avoid issues with negative means
            std_dev = abs(mean) * variation_factor if mean != 0 else variation_factor

        # Generate the random value
        return float(rng.normal(mean, std_dev))

    def generate_lognormal(
        self,
        purpose: str,
        mean: float,
        std_dev: Optional[float] = None,
        instance_id: int = 0,
    ) -> float:
        """
        Generate a lognormal random variable with controlled variation.

        Args:
            purpose: Purpose of the random variable
            mean: Mean of the underlying normal distribution
            std_dev: Standard deviation of the underlying normal distribution (if None, uses variation factor)
            instance_id: Instance ID

        Returns:
            Random value from a lognormal distribution
        """
        # Get the RNG for this purpose
        rng = self.get_rng(purpose, instance_id)

        # If std_dev is not provided, use the variation factor
        if std_dev is None:
            variation_factor = self.get_variation_factor(purpose)
            # Scale the standard deviation based on the variation factor
            std_dev = variation_factor

        # Generate the random value
        return float(rng.lognormal(mean, std_dev))

    def generate_uniform(
        self, purpose: str, low: float = 0.0, high: float = 1.0, instance_id: int = 0
    ) -> float:
        """
        Generate a uniform random variable.

        Args:
            purpose: Purpose of the random variable
            low: Lower bound of the uniform distribution
            high: Upper bound of the uniform distribution
            instance_id: Instance ID

        Returns:
            Random value from a uniform distribution
        """
        # Get the RNG for this purpose
        rng = self.get_rng(purpose, instance_id)

        # Generate the random value
        return float(rng.uniform(low, high))

    def generate_correlated_normals(
        self,
        purpose1: str,
        purpose2: str,
        correlation: float,
        mean1: float = 0.0,
        mean2: float = 0.0,
        std_dev1: Optional[float] = None,
        std_dev2: Optional[float] = None,
        instance_id: int = 0,
    ) -> Tuple[float, float]:
        """
        Generate a pair of correlated normal random variables.

        Args:
            purpose1: First purpose
            purpose2: Second purpose
            correlation: Correlation coefficient between the two variables (-1 to 1)
            mean1: Mean of the first normal distribution
            mean2: Mean of the second normal distribution
            std_dev1: Standard deviation of the first normal distribution (if None, uses variation factor)
            std_dev2: Standard deviation of the second normal distribution (if None, uses variation factor)
            instance_id: Instance ID

        Returns:
            Tuple of (value1, value2) with the specified correlation
        """
        # Get the RNGs for these purposes
        rng1, rng2 = self.get_correlated_rng(purpose1, purpose2, correlation, instance_id)

        # If std_dev is not provided, use the variation factor
        if std_dev1 is None:
            variation_factor1 = self.get_variation_factor(purpose1)
            std_dev1 = abs(mean1) * variation_factor1 if mean1 != 0 else variation_factor1

        if std_dev2 is None:
            variation_factor2 = self.get_variation_factor(purpose2)
            std_dev2 = abs(mean2) * variation_factor2 if mean2 != 0 else variation_factor2

        # Generate uncorrelated standard normal values
        z1 = rng1.standard_normal()
        z2 = rng2.standard_normal()

        # Apply correlation
        z2_corr = correlation * z1 + np.sqrt(1 - correlation**2) * z2

        # Transform to desired distributions
        x1 = mean1 + std_dev1 * z1
        x2 = mean2 + std_dev2 * z2_corr

        return float(x1), float(x2)

    def generate_beta(
        self, purpose: str, alpha: float, beta: float, instance_id: int = 0
    ) -> float:
        """
        Generate a beta random variable.

        Args:
            purpose: Purpose of the random variable
            alpha: Alpha parameter of the beta distribution
            beta: Beta parameter of the beta distribution
            instance_id: Instance ID

        Returns:
            Random value from a beta distribution
        """
        # Get the RNG for this purpose
        rng = self.get_rng(purpose, instance_id)

        # Generate the random value
        return float(rng.beta(alpha, beta))

    def generate_choice(
        self,
        purpose: str,
        choices: List[Any],
        probabilities: Optional[List[float]] = None,
        instance_id: int = 0,
    ) -> Any:
        """
        Choose a random element from a list with specified probabilities.

        Args:
            purpose: Purpose of the random variable
            choices: List of choices to select from
            probabilities: List of probabilities for each choice (must sum to 1)
            instance_id: Instance ID

        Returns:
            Randomly selected element from choices
        """
        # Get the RNG for this purpose
        rng = self.get_rng(purpose, instance_id)

        # Generate the random choice
        return rng.choice(choices, p=probabilities)

    def generate_batch_normal(
        self,
        purpose: str,
        size: int,
        mean: float = 0.0,
        std_dev: Optional[float] = None,
        instance_id: int = 0,
    ) -> np.ndarray:
        """
        Generate a batch of normal random variables with controlled variation.

        Args:
            purpose: Purpose of the random variables
            size: Number of random variables to generate
            mean: Mean of the normal distribution
            std_dev: Standard deviation of the normal distribution (if None, uses variation factor)
            instance_id: Instance ID

        Returns:
            Array of random values from a normal distribution
        """
        # Get the RNG for this purpose
        rng = self.get_rng(purpose, instance_id)

        # If std_dev is not provided, use the variation factor
        if std_dev is None:
            variation_factor = self.get_variation_factor(purpose)
            # Scale the standard deviation based on the mean and variation factor
            std_dev = abs(mean) * variation_factor if mean != 0 else variation_factor

        # Generate the random values
        return rng.normal(mean, std_dev, size=size)

    def generate_distribution_samples(
        self,
        purpose: str,
        distribution: str,
        params: Dict[str, Any],
        size: int = 1000,
        instance_id: int = 0,
    ) -> np.ndarray:
        """
        Generate samples from a specified distribution for visualization or analysis.

        Args:
            purpose: Purpose of the random variables
            distribution: Distribution type ('normal', 'lognormal', 'uniform', 'beta', etc.)
            params: Distribution parameters
            size: Number of samples to generate
            instance_id: Instance ID

        Returns:
            Array of samples from the specified distribution
        """
        # Get the RNG for this purpose
        rng = self.get_rng(purpose, instance_id)

        if distribution == "normal":
            mean = params.get("mean", 0.0)
            std_dev = params.get("std_dev")
            if std_dev is None:
                variation_factor = self.get_variation_factor(purpose)
                std_dev = abs(mean) * variation_factor if mean != 0 else variation_factor
            return rng.normal(mean, std_dev, size=size)

        elif distribution == "lognormal":
            mean = params.get("mean", 0.0)
            std_dev = params.get("std_dev")
            if std_dev is None:
                variation_factor = self.get_variation_factor(purpose)
                std_dev = variation_factor
            return rng.lognormal(mean, std_dev, size=size)

        elif distribution == "uniform":
            low = params.get("low", 0.0)
            high = params.get("high", 1.0)
            return rng.uniform(low, high, size=size)

        elif distribution == "beta":
            alpha = params.get("alpha", 1.0)
            beta = params.get("beta", 1.0)
            return rng.beta(alpha, beta, size=size)

        elif distribution == "exponential":
            scale = params.get("scale", 1.0)
            return rng.exponential(scale, size=size)

        elif distribution == "weibull":
            shape = params.get("shape", 1.0)
            scale = params.get("scale", 1.0)
            return rng.weibull(shape, size=size) * scale

        else:
            raise ValueError(f"Unsupported distribution: {distribution}")

    def get_distribution_stats(
        self,
        samples: np.ndarray,
    ) -> Dict[str, float]:
        """
        Calculate statistics for a distribution of samples.

        Args:
            samples: Array of samples

        Returns:
            Dictionary of statistics (mean, median, std_dev, min, max, etc.)
        """
        return {
            "mean": float(np.mean(samples)),
            "median": float(np.median(samples)),
            "std_dev": float(np.std(samples)),
            "min": float(np.min(samples)),
            "max": float(np.max(samples)),
            "q1": float(np.percentile(samples, 25)),
            "q3": float(np.percentile(samples, 75)),
            "skewness": float(stats.skew(samples)),
            "kurtosis": float(stats.kurtosis(samples)),
        }

    def reset(self) -> None:
        """Reset the RNG cache."""
        self._rng_cache.clear()
        self._correlated_rng_cache.clear()
        logger.debug("Reset RNG cache")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the RNG factory configuration to a dictionary.

        Returns:
            Dictionary representation of the RNG factory configuration
        """
        return {
            "base_seed": self.base_seed,
            "deterministic_mode": self.deterministic_mode,
            "correlation_matrix": self.correlation_matrix,
            "variation_factors": self.variation_factors,
            "default_variation_factor": self.default_variation_factor,
        }

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "RNGFactory":
        """
        Create an RNG factory from a dictionary configuration.

        Args:
            config: Dictionary containing RNG factory configuration

        Returns:
            RNG factory instance
        """
        return cls(
            base_seed=config.get("base_seed"),
            deterministic_mode=config.get("deterministic_mode", False),
            correlation_matrix=config.get("correlation_matrix"),
            variation_factors=config.get("variation_factors"),
        )

    def save_state(self, file_path: str) -> None:
        """
        Save the RNG factory state to a file.

        Args:
            file_path: Path to save the state to
        """
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

        logger.info("Saved RNG factory state", file_path=file_path)

    @classmethod
    def load_state(cls, file_path: str) -> "RNGFactory":
        """
        Load the RNG factory state from a file.

        Args:
            file_path: Path to load the state from

        Returns:
            RNG factory instance
        """
        with open(file_path, "r") as f:
            config = json.load(f)

        factory = cls.from_dict(config)
        logger.info("Loaded RNG factory state", file_path=file_path)

        return factory


# Global RNG factory instance
_global_rng_factory: Optional[RNGFactory] = None


def get_rng_factory() -> RNGFactory:
    """
    Get the global RNG factory instance.

    Returns:
        The global RNG factory instance
    """
    global _global_rng_factory

    if _global_rng_factory is None:
        # Get configuration from environment variables
        seed = os.environ.get("SIM_SEED")
        deterministic_mode = os.environ.get("SIM_DETERMINISTIC", "").lower() == "true"

        # Create the RNG factory
        _global_rng_factory = RNGFactory(seed, deterministic_mode)

    return _global_rng_factory


def set_rng_factory(factory: RNGFactory) -> None:
    """
    Set the global RNG factory instance.

    Args:
        factory: The RNG factory to use
    """
    global _global_rng_factory
    _global_rng_factory = factory
    logger.info(
        "Set global RNG factory",
        base_seed=factory.base_seed,
        deterministic_mode=factory.deterministic_mode,
    )


def get_rng(purpose: str, instance_id: int = 0) -> np.random.Generator:
    """
    Get a random number generator for a specific purpose and instance.

    Args:
        purpose: Purpose of the RNG (e.g., "loan_generation", "price_path")
        instance_id: Instance ID for the RNG (e.g., simulation run number)

    Returns:
        A numpy random number generator
    """
    return get_rng_factory().get_rng(purpose, instance_id)


def reset_rng_factory() -> None:
    """Reset the global RNG factory."""
    global _global_rng_factory

    if _global_rng_factory is not None:
        _global_rng_factory.reset()
        logger.info("Reset global RNG factory")


def generate_normal(
    purpose: str, mean: float = 0.0, std_dev: Optional[float] = None, instance_id: int = 0
) -> float:
    """
    Generate a normal random variable with controlled variation.

    Args:
        purpose: Purpose of the random variable
        mean: Mean of the normal distribution
        std_dev: Standard deviation of the normal distribution (if None, uses variation factor)
        instance_id: Instance ID

    Returns:
        Random value from a normal distribution
    """
    return get_rng_factory().generate_normal(purpose, mean, std_dev, instance_id)


def generate_lognormal(
    purpose: str, mean: float, std_dev: Optional[float] = None, instance_id: int = 0
) -> float:
    """
    Generate a lognormal random variable with controlled variation.

    Args:
        purpose: Purpose of the random variable
        mean: Mean of the underlying normal distribution
        std_dev: Standard deviation of the underlying normal distribution (if None, uses variation factor)
        instance_id: Instance ID

    Returns:
        Random value from a lognormal distribution
    """
    return get_rng_factory().generate_lognormal(purpose, mean, std_dev, instance_id)


def generate_uniform(
    purpose: str, low: float = 0.0, high: float = 1.0, instance_id: int = 0
) -> float:
    """
    Generate a uniform random variable.

    Args:
        purpose: Purpose of the random variable
        low: Lower bound of the uniform distribution
        high: Upper bound of the uniform distribution
        instance_id: Instance ID

    Returns:
        Random value from a uniform distribution
    """
    return get_rng_factory().generate_uniform(purpose, low, high, instance_id)


def generate_correlated_normals(
    purpose1: str,
    purpose2: str,
    correlation: float,
    mean1: float = 0.0,
    mean2: float = 0.0,
    std_dev1: Optional[float] = None,
    std_dev2: Optional[float] = None,
    instance_id: int = 0,
) -> Tuple[float, float]:
    """
    Generate a pair of correlated normal random variables.

    Args:
        purpose1: First purpose
        purpose2: Second purpose
        correlation: Correlation coefficient between the two variables (-1 to 1)
        mean1: Mean of the first normal distribution
        mean2: Mean of the second normal distribution
        std_dev1: Standard deviation of the first normal distribution (if None, uses variation factor)
        std_dev2: Standard deviation of the second normal distribution (if None, uses variation factor)
        instance_id: Instance ID

    Returns:
        Tuple of (value1, value2) with the specified correlation
    """
    return get_rng_factory().generate_correlated_normals(
        purpose1, purpose2, correlation, mean1, mean2, std_dev1, std_dev2, instance_id
    )


def set_variation_factors(variation_factors: Dict[str, float]) -> None:
    """
    Set variation factors for the global RNG factory.

    Args:
        variation_factors: Dictionary mapping purposes to variation factors
    """
    factory = get_rng_factory()
    factory.variation_factors = variation_factors
    logger.info("Set variation factors", variation_factors=variation_factors)


def set_correlation_matrix(correlation_matrix: Dict[str, Dict[str, float]]) -> None:
    """
    Set the correlation matrix for the global RNG factory.

    Args:
        correlation_matrix: Dictionary mapping purpose pairs to correlation coefficients
    """
    factory = get_rng_factory()
    factory.correlation_matrix = correlation_matrix
    logger.info("Set correlation matrix", correlation_matrix=correlation_matrix)


def set_deterministic_mode(enabled: bool) -> None:
    """
    Set deterministic mode for the global RNG factory.

    Args:
        enabled: Whether to enable deterministic mode
    """
    global _global_rng_factory

    # If the factory already exists, create a new one with the same seed but different mode
    if _global_rng_factory is not None:
        base_seed = _global_rng_factory.base_seed
        variation_factors = _global_rng_factory.variation_factors
        correlation_matrix = _global_rng_factory.correlation_matrix
        _global_rng_factory = RNGFactory(
            base_seed, enabled, correlation_matrix, variation_factors
        )
    else:
        # Create a new factory with deterministic mode
        _global_rng_factory = RNGFactory(deterministic_mode=enabled)

    logger.info("Set deterministic mode", enabled=enabled)
