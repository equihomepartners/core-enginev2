"""
TLS Module integration with the simulation engine.

This module provides the interface between the TLS data and the simulation engine.
"""

import logging
from typing import Dict, Any, List, Optional, Tuple

from src.engine.simulation_context import SimulationContext
from src.tls_module import get_tls_manager
from src.tls_module.tls_core import SuburbData, PropertyAttributes, MetricCategory
from src.utils.error_handler import ValidationError, ErrorCode

logger = logging.getLogger(__name__)


async def initialize_tls_module(context: SimulationContext) -> None:
    """
    Initialize the TLS module.

    Args:
        context: Simulation context
    """
    logger.info("Initializing TLS module")

    # Get TLS manager with static data
    tls_manager = get_tls_manager(use_mock=True)

    # Load TLS data
    await tls_manager.load_data(simulation_id=context.run_id)

    # Store TLS manager in context
    context.tls_manager = tls_manager

    # Store zone distribution in context
    context.zone_distribution = tls_manager.get_zone_distribution()

    # Store metrics by category in context
    context.metrics_by_category = {}
    for category in ["economic", "real_estate", "demographic", "risk", "location", "supply_demand", "temporal"]:
        category_enum = getattr(MetricCategory, category.upper())
        context.metrics_by_category[category] = tls_manager.get_metrics_by_category(category_enum)

    # Store suburb count and property count in context
    context.suburb_count = len(tls_manager.suburbs)
    context.property_count = sum(len(suburb.properties) for suburb in tls_manager.suburbs.values())

    # Populate context.tls_data with suburb information for price path module
    context.tls_data = {}
    for suburb_id, suburb in tls_manager.suburbs.items():
        context.tls_data[suburb_id] = {
            "suburb_id": suburb_id,
            "name": suburb.name,
            "zone": suburb.zone_category,
            "zone_color": suburb.zone_color,
            "appreciation_score": suburb.appreciation_score,
            "risk_score": suburb.risk_score,
            "liquidity_score": suburb.liquidity_score,
            "overall_score": suburb.overall_score,
            "latitude": suburb.latitude,
            "longitude": suburb.longitude,
            "state": suburb.state,
            "postcode": suburb.postcode,
        }

    logger.info(
        "TLS module initialized",
        zone_distribution=context.zone_distribution,
        suburb_count=context.suburb_count,
        property_count=context.property_count,
        tls_data_populated=len(context.tls_data),
    )


def get_suburbs_by_allocation(
    context: SimulationContext, allocation: Dict[str, float]
) -> Dict[str, List[SuburbData]]:
    """
    Get suburbs by allocation.

    Args:
        context: Simulation context
        allocation: Allocation by zone category

    Returns:
        Dictionary mapping zone categories to lists of suburbs
    """
    # Get TLS manager
    tls_manager = getattr(context, "tls_manager", None)
    if tls_manager is None:
        raise ValidationError(
            "TLS module not initialized",
            code=ErrorCode.INVALID_CONFIGURATION,
        )

    # Get suburbs by zone
    result = {}
    for zone, percentage in allocation.items():
        if zone not in ["green", "orange", "red"]:
            raise ValidationError(
                f"Invalid zone category: {zone}",
                code=ErrorCode.INVALID_PARAMETER,
            )

        if percentage <= 0:
            result[zone] = []
            continue

        # Get suburbs in zone
        suburbs = tls_manager.get_suburbs_by_zone(zone)

        # Sort by overall score (highest first)
        suburbs.sort(key=lambda s: s.overall_score, reverse=True)

        result[zone] = suburbs

    return result


def get_properties_by_criteria(
    context: SimulationContext,
    min_bedrooms: Optional[int] = None,
    max_bedrooms: Optional[int] = None,
    min_bathrooms: Optional[int] = None,
    max_bathrooms: Optional[int] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    property_type: Optional[str] = None,
    suburb_ids: Optional[List[str]] = None,
    zone_category: Optional[str] = None,
    limit: int = 100,
) -> List[Tuple[SuburbData, PropertyAttributes]]:
    """
    Get properties by criteria.

    Args:
        context: Simulation context
        min_bedrooms: Minimum number of bedrooms
        max_bedrooms: Maximum number of bedrooms
        min_bathrooms: Minimum number of bathrooms
        max_bathrooms: Maximum number of bathrooms
        min_value: Minimum property value
        max_value: Maximum property value
        property_type: Property type (house, apartment, townhouse, duplex)
        suburb_ids: List of suburb IDs to search in
        zone_category: Zone category (green, orange, red)
        limit: Maximum number of properties to return

    Returns:
        List of (suburb, property) tuples
    """
    # Get TLS manager
    tls_manager = getattr(context, "tls_manager", None)
    if tls_manager is None:
        raise ValidationError(
            "TLS module not initialized",
            code=ErrorCode.INVALID_CONFIGURATION,
        )

    # Get properties
    return tls_manager.get_properties_by_criteria(
        min_bedrooms=min_bedrooms,
        max_bedrooms=max_bedrooms,
        min_bathrooms=min_bathrooms,
        max_bathrooms=max_bathrooms,
        min_value=min_value,
        max_value=max_value,
        property_type=property_type,
        suburb_ids=suburb_ids,
        zone_category=zone_category,
        limit=limit,
    )


def get_suburb_metrics(context: SimulationContext, suburb_id: str) -> Dict[str, Any]:
    """
    Get metrics for a suburb.

    Args:
        context: Simulation context
        suburb_id: Suburb ID

    Returns:
        Dictionary of metrics
    """
    # Get TLS manager
    tls_manager = getattr(context, "tls_manager", None)
    if tls_manager is None:
        raise ValidationError(
            "TLS module not initialized",
            code=ErrorCode.INVALID_CONFIGURATION,
        )

    # Get suburb
    suburb = tls_manager.get_suburb(suburb_id)
    if suburb is None:
        raise ValidationError(
            f"Suburb {suburb_id} not found",
            code=ErrorCode.DATA_NOT_FOUND,
        )

    # Get metrics
    result = {
        "suburb_id": suburb.suburb_id,
        "name": suburb.name,
        "state": suburb.state,
        "postcode": suburb.postcode,
        "latitude": suburb.latitude,
        "longitude": suburb.longitude,
        "appreciation_score": suburb.appreciation_score,
        "risk_score": suburb.risk_score,
        "liquidity_score": suburb.liquidity_score,
        "overall_score": suburb.overall_score,
        "zone_color": suburb.zone_color,
        "zone_category": suburb.zone_category,
        "metrics": {},
    }

    # Add metrics
    for metric_name, metric_value in suburb.metrics.items():
        result["metrics"][metric_name] = {
            "value": metric_value.value,
            "confidence": metric_value.confidence,
            "percentile": metric_value.percentile,
        }

    return result


def get_property_details(
    context: SimulationContext, suburb_id: str, property_id: str
) -> Dict[str, Any]:
    """
    Get details for a property.

    Args:
        context: Simulation context
        suburb_id: Suburb ID
        property_id: Property ID

    Returns:
        Dictionary of property details
    """
    # Get TLS manager
    tls_manager = getattr(context, "tls_manager", None)
    if tls_manager is None:
        raise ValidationError(
            "TLS module not initialized",
            code=ErrorCode.INVALID_CONFIGURATION,
        )

    # Get suburb
    suburb = tls_manager.get_suburb(suburb_id)
    if suburb is None:
        raise ValidationError(
            f"Suburb {suburb_id} not found",
            code=ErrorCode.DATA_NOT_FOUND,
        )

    # Get property
    property_data = suburb.get_property(property_id)
    if property_data is None:
        raise ValidationError(
            f"Property {property_id} not found in suburb {suburb_id}",
            code=ErrorCode.DATA_NOT_FOUND,
        )

    # Get details
    result = {
        "property_id": property_data.property_id,
        "suburb_id": property_data.suburb_id,
        "property_type": property_data.property_type,
        "bedrooms": property_data.bedrooms,
        "bathrooms": property_data.bathrooms,
        "parking": property_data.parking,
        "land_size": property_data.land_size,
        "building_size": property_data.building_size,
        "year_built": property_data.year_built,
        "condition": property_data.condition,
        "quality": property_data.quality,
        "street_quality": property_data.street_quality,
        "view_quality": property_data.view_quality,
        "noise_level": property_data.noise_level,
        "appreciation_modifier": property_data.appreciation_modifier,
        "risk_modifier": property_data.risk_modifier,
        "base_value": property_data.base_value,
        "metrics": {},
    }

    # Add metrics
    for metric_name, metric_value in property_data.metrics.items():
        result["metrics"][metric_name] = {
            "value": metric_value.value,
            "confidence": metric_value.confidence,
            "percentile": metric_value.percentile,
        }

    return result
