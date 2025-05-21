"""
Feature flags module for the EQU IHOME SIM ENGINE v2.

This module provides utilities for checking feature flags.
"""

import os
from typing import Set, Optional

import structlog

logger = structlog.get_logger(__name__)

# Set of enabled features
_enabled_features: Optional[Set[str]] = None


def _load_features() -> Set[str]:
    """
    Load enabled features from the environment.
    
    Returns:
        Set of enabled features
    """
    features_str = os.environ.get("SIM_FEATURES", "")
    features = {feature.strip() for feature in features_str.split(",") if feature.strip()}
    
    logger.info("Loaded features", features=features)
    
    return features


def get_enabled_features() -> Set[str]:
    """
    Get the set of enabled features.
    
    Returns:
        Set of enabled features
    """
    global _enabled_features
    
    if _enabled_features is None:
        _enabled_features = _load_features()
    
    return _enabled_features


def is_feature_enabled(feature: str) -> bool:
    """
    Check if a feature is enabled.
    
    Args:
        feature: Feature name
        
    Returns:
        True if the feature is enabled, False otherwise
    """
    return feature in get_enabled_features()


def enable_feature(feature: str) -> None:
    """
    Enable a feature.
    
    Args:
        feature: Feature name
    """
    global _enabled_features
    
    if _enabled_features is None:
        _enabled_features = _load_features()
    
    _enabled_features.add(feature)
    logger.info("Feature enabled", feature=feature)


def disable_feature(feature: str) -> None:
    """
    Disable a feature.
    
    Args:
        feature: Feature name
    """
    global _enabled_features
    
    if _enabled_features is None:
        _enabled_features = _load_features()
    
    _enabled_features.discard(feature)
    logger.info("Feature disabled", feature=feature)


def reset_features() -> None:
    """Reset features to the values from the environment."""
    global _enabled_features
    _enabled_features = None
    get_enabled_features()  # Reload features


# Define known features
FEATURE_PARALLEL = "ENABLE_PARALLEL"
FEATURE_CACHE = "ENABLE_CACHE"
FEATURE_PROMETHEUS = "ENABLE_PROMETHEUS"
FEATURE_DEBUG_LOGGING = "ENABLE_DEBUG_LOGGING"
FEATURE_ADVANCED_RISK = "ENABLE_ADVANCED_RISK"
