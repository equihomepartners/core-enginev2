"""
TLS API router for the EQU IHOME SIM ENGINE v2.

This module provides API routes for accessing TLS data and visualizations.
"""

import logging
from typing import Dict, Any, List, Optional, Tuple

from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import os

from src.engine.simulation_context import SimulationContext
from src.tls_module import get_tls_manager
from src.tls_module.tls_core import SuburbData, PropertyAttributes, MetricCategory
from src.utils.error_handler import ValidationError, ErrorCode


# Models
class ZoneDistribution(BaseModel):
    """Zone distribution model."""
    green: int = Field(..., description="Number of suburbs in green zone")
    orange: int = Field(..., description="Number of suburbs in orange zone")
    red: int = Field(..., description="Number of suburbs in red zone")
    total: int = Field(..., description="Total number of suburbs")
    green_percentage: float = Field(..., description="Percentage of suburbs in green zone")
    orange_percentage: float = Field(..., description="Percentage of suburbs in orange zone")
    red_percentage: float = Field(..., description="Percentage of suburbs in red zone")


class MetricValue(BaseModel):
    """Metric value model."""
    value: float = Field(..., description="Metric value")
    confidence: float = Field(..., description="Confidence level (0-1)")
    percentile: Optional[float] = Field(None, description="Percentile (0-1)")


class MetricDefinition(BaseModel):
    """Metric definition model."""
    name: str = Field(..., description="Metric name")
    category: str = Field(..., description="Metric category")
    description: str = Field(..., description="Metric description")
    unit: str = Field(..., description="Metric unit")
    min_value: float = Field(..., description="Minimum value")
    max_value: float = Field(..., description="Maximum value")
    is_higher_better: Optional[bool] = Field(None, description="Whether higher values are better")


class SuburbSummary(BaseModel):
    """Suburb summary model."""
    suburb_id: str = Field(..., description="Suburb ID")
    name: str = Field(..., description="Suburb name")
    state: str = Field(..., description="State")
    postcode: str = Field(..., description="Postcode")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    zone_category: str = Field(..., description="Zone category (green, orange, red)")
    overall_score: float = Field(..., description="Overall score (0-100)")


class SuburbDetail(SuburbSummary):
    """Suburb detail model."""
    appreciation_score: float = Field(..., description="Appreciation score (0-100)")
    risk_score: float = Field(..., description="Risk score (0-100)")
    liquidity_score: float = Field(..., description="Liquidity score (0-100)")
    appreciation_confidence: float = Field(..., description="Appreciation confidence (0-1)")
    risk_confidence: float = Field(..., description="Risk confidence (0-1)")
    liquidity_confidence: float = Field(..., description="Liquidity confidence (0-1)")
    overall_confidence: float = Field(..., description="Overall confidence (0-1)")
    metrics: Dict[str, MetricValue] = Field(..., description="Metrics")
    property_count: int = Field(..., description="Number of properties")


class PropertySummary(BaseModel):
    """Property summary model."""
    property_id: str = Field(..., description="Property ID")
    suburb_id: str = Field(..., description="Suburb ID")
    property_type: str = Field(..., description="Property type")
    bedrooms: int = Field(..., description="Number of bedrooms")
    bathrooms: int = Field(..., description="Number of bathrooms")
    base_value: float = Field(..., description="Base value")


class PropertyDetail(PropertySummary):
    """Property detail model."""
    parking: int = Field(..., description="Number of parking spaces")
    land_size: float = Field(..., description="Land size (square meters)")
    building_size: float = Field(..., description="Building size (square meters)")
    year_built: int = Field(..., description="Year built")
    condition: float = Field(..., description="Condition (0-1)")
    quality: float = Field(..., description="Quality (0-1)")
    street_quality: float = Field(..., description="Street quality (0-1)")
    view_quality: float = Field(..., description="View quality (0-1)")
    noise_level: float = Field(..., description="Noise level (0-1)")
    appreciation_modifier: float = Field(..., description="Appreciation modifier")
    risk_modifier: float = Field(..., description="Risk modifier")
    metrics: Dict[str, MetricValue] = Field(..., description="Metrics")


class MetricDistribution(BaseModel):
    """Metric distribution model."""
    metric_name: str = Field(..., description="Metric name")
    category: str = Field(..., description="Metric category")
    unit: str = Field(..., description="Metric unit")
    min_value: float = Field(..., description="Minimum value")
    max_value: float = Field(..., description="Maximum value")
    mean: float = Field(..., description="Mean value")
    median: float = Field(..., description="Median value")
    std_dev: float = Field(..., description="Standard deviation")
    percentiles: Dict[str, float] = Field(..., description="Percentiles (10, 25, 50, 75, 90)")
    histogram: List[Dict[str, Any]] = Field(..., description="Histogram data")
    by_zone: Dict[str, Dict[str, float]] = Field(..., description="Statistics by zone")


class CorrelationMatrix(BaseModel):
    """Correlation matrix model."""
    metrics: List[str] = Field(..., description="Metric names")
    matrix: List[List[float]] = Field(..., description="Correlation matrix")
    strong_correlations: List[Dict[str, Any]] = Field(..., description="Strong correlations")


class PropertyDistribution(BaseModel):
    """Property distribution model."""
    total_properties: int = Field(..., description="Total number of properties")
    property_types: Dict[str, int] = Field(..., description="Distribution by property type")
    bedrooms: Dict[str, int] = Field(..., description="Distribution by number of bedrooms")
    bathrooms: Dict[str, int] = Field(..., description="Distribution by number of bathrooms")
    value_distribution: List[Dict[str, Any]] = Field(..., description="Distribution by value")
    zone_distribution: Dict[str, int] = Field(..., description="Distribution by zone")

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    tags=["tls"],
    responses={404: {"description": "Not found"}},
)


# Helper function to get TLS manager
def get_tls_manager_from_context() -> Any:
    """Get TLS manager from context."""
    tls_manager = get_tls_manager(use_mock=True)
    return tls_manager


# Routes
@router.get("/zones/distribution", response_model=ZoneDistribution)
async def get_zone_distribution(
    tls_manager: Any = Depends(get_tls_manager_from_context),
) -> Dict[str, Any]:
    """
    Get distribution of suburbs by zone category.

    Returns:
        Zone distribution statistics
    """
    try:
        # Load data if not already loaded
        if not tls_manager.data_loaded:
            await tls_manager.load_data()

        # Get zone distribution
        distribution = tls_manager.get_zone_distribution()

        # Calculate total and percentages
        total = sum(distribution.values())

        return {
            "green": distribution.get("green", 0),
            "orange": distribution.get("orange", 0),
            "red": distribution.get("red", 0),
            "total": total,
            "green_percentage": (distribution.get("green", 0) / total * 100) if total > 0 else 0,
            "orange_percentage": (distribution.get("orange", 0) / total * 100) if total > 0 else 0,
            "red_percentage": (distribution.get("red", 0) / total * 100) if total > 0 else 0,
        }

    except Exception as e:
        logger.error("Failed to get zone distribution", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics", response_model=List[MetricDefinition])
async def get_metrics(
    category: Optional[str] = None,
    tls_manager: Any = Depends(get_tls_manager_from_context),
) -> List[Dict[str, Any]]:
    """
    Get all metrics or metrics by category.

    Args:
        category: Metric category (economic, real_estate, demographic, risk, location, supply_demand, temporal)

    Returns:
        List of metric definitions
    """
    try:
        # Load data if not already loaded
        if not tls_manager.data_loaded:
            await tls_manager.load_data()

        # Get metrics
        if category:
            try:
                category_enum = getattr(MetricCategory, category.upper())
                metrics = tls_manager.get_metrics_by_category(category_enum)
            except (AttributeError, ValueError):
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid category: {category}. Valid categories are: economic, real_estate, demographic, risk, location, supply_demand, temporal",
                )
        else:
            metrics = list(tls_manager.metrics.values())

        # Format metrics
        result = []
        for metric in metrics:
            result.append({
                "name": metric.name,
                "category": metric.category.value.lower(),
                "description": metric.description,
                "unit": metric.unit,
                "min_value": metric.min_value,
                "max_value": metric.max_value,
                "is_higher_better": metric.is_higher_better,
            })

        return result

    except Exception as e:
        logger.error("Failed to get metrics", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/{metric_name}/distribution", response_model=MetricDistribution)
async def get_metric_distribution(
    metric_name: str,
    zone: Optional[str] = None,
    tls_manager: Any = Depends(get_tls_manager_from_context),
) -> Dict[str, Any]:
    """
    Get distribution of a metric across all suburbs.

    Args:
        metric_name: Metric name
        zone: Zone category (green, orange, red) to filter by

    Returns:
        Metric distribution statistics
    """
    try:
        # Load data if not already loaded
        if not tls_manager.data_loaded:
            await tls_manager.load_data()

        # Get metric
        metric = tls_manager.get_metric(metric_name)
        if not metric:
            raise HTTPException(
                status_code=404,
                detail=f"Metric {metric_name} not found",
            )

        # Get suburbs
        if zone:
            if zone not in ["green", "orange", "red"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid zone: {zone}. Valid zones are: green, orange, red",
                )
            suburbs = tls_manager.get_suburbs_by_zone(zone)
        else:
            suburbs = list(tls_manager.suburbs.values())

        # Get values
        values = []
        for suburb in suburbs:
            metric_value = suburb.get_metric(metric_name)
            if metric_value:
                values.append(metric_value.value)

        if not values:
            raise HTTPException(
                status_code=404,
                detail=f"No values found for metric {metric_name}",
            )

        # Calculate statistics
        import numpy as np

        mean = float(np.mean(values))
        median = float(np.median(values))
        std_dev = float(np.std(values))

        # Calculate percentiles
        percentiles = {
            "10": float(np.percentile(values, 10)),
            "25": float(np.percentile(values, 25)),
            "50": float(np.percentile(values, 50)),
            "75": float(np.percentile(values, 75)),
            "90": float(np.percentile(values, 90)),
        }

        # Create histogram
        hist, bin_edges = np.histogram(values, bins=10)
        histogram = []
        for i in range(len(hist)):
            histogram.append({
                "bin_start": float(bin_edges[i]),
                "bin_end": float(bin_edges[i + 1]),
                "count": int(hist[i]),
                "percentage": float(hist[i] / len(values) * 100),
            })

        # Calculate statistics by zone
        by_zone = {}
        for zone_category in ["green", "orange", "red"]:
            zone_suburbs = tls_manager.get_suburbs_by_zone(zone_category)
            zone_values = []
            for suburb in zone_suburbs:
                metric_value = suburb.get_metric(metric_name)
                if metric_value:
                    zone_values.append(metric_value.value)

            if zone_values:
                by_zone[zone_category] = {
                    "count": len(zone_values),
                    "mean": float(np.mean(zone_values)),
                    "median": float(np.median(zone_values)),
                    "min": float(np.min(zone_values)),
                    "max": float(np.max(zone_values)),
                    "std_dev": float(np.std(zone_values)),
                }
            else:
                by_zone[zone_category] = {
                    "count": 0,
                    "mean": 0.0,
                    "median": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "std_dev": 0.0,
                }

        return {
            "metric_name": metric_name,
            "category": metric.category.value.lower(),
            "unit": metric.unit,
            "min_value": float(min(values)),
            "max_value": float(max(values)),
            "mean": mean,
            "median": median,
            "std_dev": std_dev,
            "percentiles": percentiles,
            "histogram": histogram,
            "by_zone": by_zone,
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error("Failed to get metric distribution", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suburbs", response_model=List[SuburbSummary])
async def get_suburbs(
    zone: Optional[str] = None,
    min_score: Optional[float] = None,
    max_score: Optional[float] = None,
    sort_by: Optional[str] = "overall_score",
    sort_order: Optional[str] = "desc",
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    tls_manager: Any = Depends(get_tls_manager_from_context),
) -> List[Dict[str, Any]]:
    """
    Get all suburbs or suburbs by zone.

    Args:
        zone: Zone category (green, orange, red) to filter by
        min_score: Minimum overall score (0-100)
        max_score: Maximum overall score (0-100)
        sort_by: Field to sort by (overall_score, appreciation_score, risk_score, liquidity_score, name)
        sort_order: Sort order (asc, desc)
        limit: Maximum number of suburbs to return
        offset: Number of suburbs to skip

    Returns:
        List of suburb summaries
    """
    try:
        # Load data if not already loaded
        if not tls_manager.data_loaded:
            await tls_manager.load_data()

        # Get suburbs
        if zone:
            if zone not in ["green", "orange", "red"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid zone: {zone}. Valid zones are: green, orange, red",
                )
            suburbs = tls_manager.get_suburbs_by_zone(zone)
        else:
            suburbs = list(tls_manager.suburbs.values())

        # Filter by score
        if min_score is not None or max_score is not None:
            min_score = min_score if min_score is not None else 0.0
            max_score = max_score if max_score is not None else 100.0
            suburbs = [s for s in suburbs if min_score <= s.overall_score <= max_score]

        # Sort suburbs
        if sort_by not in ["overall_score", "appreciation_score", "risk_score", "liquidity_score", "name"]:
            sort_by = "overall_score"

        reverse = sort_order.lower() == "desc"

        if sort_by == "name":
            suburbs.sort(key=lambda s: s.name, reverse=reverse)
        else:
            suburbs.sort(key=lambda s: getattr(s, sort_by), reverse=reverse)

        # Apply pagination
        suburbs = suburbs[offset:offset + limit]

        # Format suburbs
        result = []
        for suburb in suburbs:
            result.append({
                "suburb_id": suburb.suburb_id,
                "name": suburb.name,
                "state": suburb.state,
                "postcode": suburb.postcode,
                "latitude": suburb.latitude,
                "longitude": suburb.longitude,
                "zone_category": suburb.zone_category,
                "overall_score": suburb.overall_score,
            })

        return result

    except Exception as e:
        logger.error("Failed to get suburbs", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/suburbs/{suburb_id}", response_model=SuburbDetail)
async def get_suburb(
    suburb_id: str,
    tls_manager: Any = Depends(get_tls_manager_from_context),
) -> Dict[str, Any]:
    """
    Get a suburb by ID.

    Args:
        suburb_id: Suburb ID

    Returns:
        Suburb details
    """
    try:
        # Load data if not already loaded
        if not tls_manager.data_loaded:
            await tls_manager.load_data()

        # Get suburb
        suburb = tls_manager.get_suburb(suburb_id)
        if not suburb:
            raise HTTPException(
                status_code=404,
                detail=f"Suburb {suburb_id} not found",
            )

        # Format metrics
        metrics = {}
        for metric_name, metric_value in suburb.metrics.items():
            metrics[metric_name] = {
                "value": metric_value.value,
                "confidence": metric_value.confidence,
                "percentile": metric_value.percentile,
            }

        return {
            "suburb_id": suburb.suburb_id,
            "name": suburb.name,
            "state": suburb.state,
            "postcode": suburb.postcode,
            "latitude": suburb.latitude,
            "longitude": suburb.longitude,
            "zone_category": suburb.zone_category,
            "overall_score": suburb.overall_score,
            "appreciation_score": suburb.appreciation_score,
            "risk_score": suburb.risk_score,
            "liquidity_score": suburb.liquidity_score,
            "appreciation_confidence": suburb.appreciation_confidence,
            "risk_confidence": suburb.risk_confidence,
            "liquidity_confidence": suburb.liquidity_confidence,
            "overall_confidence": suburb.overall_confidence,
            "metrics": metrics,
            "property_count": len(suburb.properties),
        }

    except Exception as e:
        logger.error("Failed to get suburb", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/visualization/property_distribution", response_model=PropertyDistribution)
async def get_property_distribution(
    tls_manager: Any = Depends(get_tls_manager_from_context),
) -> Dict[str, Any]:
    """
    Get property distribution data for visualization.

    Returns:
        Property distribution data
    """
    try:
        # Load data if not already loaded
        if not tls_manager.data_loaded:
            await tls_manager.load_data()

        # Get property type distribution
        property_types = tls_manager.get_property_distribution_by_type()

        # Get bedroom distribution
        bedrooms = tls_manager.get_property_distribution_by_bedrooms()

        # Convert int keys to strings for JSON serialization
        bedrooms_str = {str(k): v for k, v in bedrooms.items()}

        # Get bathroom distribution
        bathroom_distribution = {}
        for suburb in tls_manager.suburbs.values():
            for prop in suburb.properties:
                bathroom_count = prop.bathrooms
                if bathroom_count not in bathroom_distribution:
                    bathroom_distribution[bathroom_count] = 0
                bathroom_distribution[bathroom_count] += 1

        # Convert int keys to strings for JSON serialization
        bathrooms_str = {str(k): v for k, v in bathroom_distribution.items()}

        # Get value distribution
        value_distribution = tls_manager.get_property_distribution_by_value(num_bins=10)

        # Get zone distribution
        zone_distribution = tls_manager.get_property_distribution_by_zone()

        # Calculate total properties
        total_properties = sum(property_types.values())

        return {
            "total_properties": total_properties,
            "property_types": property_types,
            "bedrooms": bedrooms_str,
            "bathrooms": bathrooms_str,
            "value_distribution": value_distribution,
            "zone_distribution": zone_distribution,
        }

    except Exception as e:
        logger.error("Failed to get property distribution data", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/visualization/zone_map")
async def get_zone_map(
    tls_manager: Any = Depends(get_tls_manager_from_context),
) -> Dict[str, Any]:
    """
    Get data for zone map visualization.

    Returns:
        Zone map data
    """
    try:
        # Load data if not already loaded
        if not tls_manager.data_loaded:
            await tls_manager.load_data()

        # Get zone map data
        return tls_manager.get_zone_map_data()

    except Exception as e:
        logger.error("Failed to get zone map data", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/correlations/metrics", response_model=CorrelationMatrix)
async def get_metric_correlations(
    metrics: Optional[List[str]] = Query(None),
    tls_manager: Any = Depends(get_tls_manager_from_context),
) -> Dict[str, Any]:
    """
    Get correlation matrix for metrics.

    Args:
        metrics: List of metric names to include (if not provided, uses top 20 metrics)

    Returns:
        Correlation matrix
    """
    try:
        # Load data if not already loaded
        if not tls_manager.data_loaded:
            await tls_manager.load_data()

        # Get metrics
        if metrics:
            # Validate metrics
            for metric_name in metrics:
                if not tls_manager.get_metric(metric_name):
                    raise HTTPException(
                        status_code=404,
                        detail=f"Metric {metric_name} not found",
                    )
        else:
            # Use top 20 metrics by coverage
            metrics = [m.name for m in list(tls_manager.metrics.values())[:20]]

        # Get correlation matrix
        matrix = []
        for i, metric1 in enumerate(metrics):
            row = []
            for j, metric2 in enumerate(metrics):
                if i == j:
                    row.append(1.0)  # Correlation with self is 1.0
                else:
                    row.append(float(tls_manager.get_metric_correlation(metric1, metric2)))
            matrix.append(row)

        # Get strong correlations
        strong_correlations = tls_manager.get_strong_metric_correlations(threshold=0.7)

        return {
            "metrics": metrics,
            "matrix": matrix,
            "strong_correlations": strong_correlations,
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.error("Failed to get metric correlations", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/data")
async def get_raw_data():
    """
    Serve the raw TLS data file.

    Returns:
        Raw TLS data file as JSON
    """
    try:
        # Path to the TLS data file
        data_file_path = os.path.join(os.getcwd(), "src", "tls_module", "data", "sydney_suburbs_data.json")

        # Check if file exists
        if not os.path.exists(data_file_path):
            raise HTTPException(
                status_code=404,
                detail="TLS data file not found"
            )

        # Return the file
        return FileResponse(
            path=data_file_path,
            media_type="application/json",
            filename="sydney_suburbs_data.json"
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error("Failed to serve TLS data file", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
