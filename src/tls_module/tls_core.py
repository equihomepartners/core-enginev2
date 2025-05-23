"""
Traffic Light System (TLS) Core Module for the EQU IHOME SIM ENGINE v2.

This module provides a sophisticated classification system for geographic areas (suburbs)
with multi-dimensional scoring, rich metrics, and property-level variation.
"""

import json
import time
import random
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
import numpy as np
from scipy import stats

from src.utils.error_handler import ValidationError, ErrorCode
from src.api.websocket_manager import get_websocket_manager

# Configure logging
import structlog
logger = structlog.get_logger(__name__)


class MetricCategory(str, Enum):
    """Categories for TLS metrics."""

    ECONOMIC = "economic"
    REAL_ESTATE = "real_estate"
    DEMOGRAPHIC = "demographic"
    RISK = "risk"
    LOCATION = "location"
    SUPPLY_DEMAND = "supply_demand"
    TEMPORAL = "temporal"


class ConfidenceLevel(str, Enum):
    """Confidence levels for TLS metrics."""

    VERY_LOW = "very_low"  # 0-20%
    LOW = "low"  # 20-40%
    MEDIUM = "medium"  # 40-60%
    HIGH = "high"  # 60-80%
    VERY_HIGH = "very_high"  # 80-100%


@dataclass
class MetricValue:
    """Value for a TLS metric with confidence information."""

    value: float
    confidence: float  # 0-1
    percentile: Optional[float] = None  # 0-1
    timestamp: Optional[float] = None

    def __post_init__(self):
        """Validate and initialize the metric value."""
        if not 0 <= self.confidence <= 1:
            raise ValidationError(
                f"Confidence must be between 0 and 1, got {self.confidence}",
                code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            )

        if self.percentile is not None and not 0 <= self.percentile <= 1:
            raise ValidationError(
                f"Percentile must be between 0 and 1, got {self.percentile}",
                code=ErrorCode.PARAMETER_OUT_OF_RANGE,
            )

        if self.timestamp is None:
            self.timestamp = time.time()

    @property
    def confidence_level(self) -> ConfidenceLevel:
        """Get the confidence level."""
        if self.confidence < 0.2:
            return ConfidenceLevel.VERY_LOW
        elif self.confidence < 0.4:
            return ConfidenceLevel.LOW
        elif self.confidence < 0.6:
            return ConfidenceLevel.MEDIUM
        elif self.confidence < 0.8:
            return ConfidenceLevel.HIGH
        else:
            return ConfidenceLevel.VERY_HIGH


@dataclass
class Metric:
    """A TLS metric with metadata."""

    name: str
    category: MetricCategory
    description: str
    unit: str
    min_value: float
    max_value: float
    is_higher_better: bool
    values: Dict[str, MetricValue] = field(default_factory=dict)  # suburb_id -> value

    def get_value(self, suburb_id: str) -> Optional[MetricValue]:
        """Get the value for a suburb."""
        return self.values.get(suburb_id)

    def set_value(self, suburb_id: str, value: Union[float, MetricValue]) -> None:
        """Set the value for a suburb."""
        if isinstance(value, float):
            # Create a MetricValue with default confidence
            value = MetricValue(value=value, confidence=0.8)

        self.values[suburb_id] = value

    def get_percentile(self, value: float) -> float:
        """Calculate the percentile of a value within all values."""
        all_values = [v.value for v in self.values.values()]
        if not all_values:
            return 0.5  # Default to median if no values

        return stats.percentileofscore(all_values, value) / 100.0

    def normalize(self, value: float) -> float:
        """Normalize a value to 0-1 range."""
        if self.max_value == self.min_value:
            return 0.5  # Avoid division by zero

        normalized = (value - self.min_value) / (self.max_value - self.min_value)
        normalized = max(0.0, min(1.0, normalized))

        if not self.is_higher_better:
            normalized = 1.0 - normalized

        return normalized


@dataclass
class PropertyAttributes:
    """Attributes for a property within a suburb."""

    property_id: str
    suburb_id: str
    property_type: str  # house, apartment, townhouse, etc.
    bedrooms: int
    bathrooms: int
    parking: int
    land_size: float  # square meters
    building_size: float  # square meters
    year_built: int
    condition: float  # 0-1 (poor to excellent)
    quality: float  # 0-1 (low to high)
    street_quality: float  # 0-1 (poor to excellent)
    view_quality: float  # 0-1 (poor to excellent)
    noise_level: float  # 0-1 (quiet to noisy)
    appreciation_modifier: float  # Multiplier for suburb appreciation
    risk_modifier: float  # Multiplier for suburb risk
    base_value: float  # Base property value

    # Missing raw data fields
    zoning_code: str = "R2"  # Residential zoning code (default: R2 - Low Density Residential)
    days_on_market_last_sale: int = 30  # Days on market for last sale
    last_sale_price: float = 0.0  # Last sale price (will default to base_value if not set)
    hist_price_series: List[float] = field(default_factory=list)  # Monthly price index
    hist_rent_series: List[float] = field(default_factory=list)  # Monthly rent values

    # Additional metrics specific to the property
    metrics: Dict[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize default values and validate."""
        # Set last_sale_price to base_value if not provided
        if self.last_sale_price == 0.0:
            self.last_sale_price = self.base_value

        # Initialize empty price series if not provided
        if not self.hist_price_series:
            # Create 60 months (5 years) of price history with slight appreciation
            base = self.base_value * 0.8  # Start at 80% of current value
            monthly_growth = (self.base_value / base) ** (1/60) - 1  # Calculate monthly growth rate

            # Add some random noise to the growth rate
            self.hist_price_series = [
                base * (1 + monthly_growth + random.uniform(-0.005, 0.005)) ** i
                for i in range(60)
            ]

        # Initialize empty rent series if not provided
        if not self.hist_rent_series:
            # Create 60 months (5 years) of rent history
            # Assume 3-5% gross rental yield
            rental_yield = random.uniform(0.03, 0.05)
            monthly_rent = (self.base_value * rental_yield) / 12

            # Add some random noise to the rent
            self.hist_rent_series = [
                monthly_rent * (1 + random.uniform(-0.02, 0.02))
                for _ in range(60)
            ]

    def get_metric(self, metric_name: str) -> Optional[MetricValue]:
        """Get a property-specific metric."""
        return self.metrics.get(metric_name)

    def set_metric(self, metric_name: str, value: Union[float, MetricValue]) -> None:
        """Set a property-specific metric."""
        if isinstance(value, float):
            # Create a MetricValue with default confidence
            value = MetricValue(value=value, confidence=0.8)

        self.metrics[metric_name] = value

    def calculate_value(self, appreciation_factor: float = 1.0) -> float:
        """Calculate the current property value with appreciation."""
        return self.base_value * appreciation_factor * self.appreciation_modifier

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "property_id": self.property_id,
            "suburb_id": self.suburb_id,
            "property_type": self.property_type,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "parking": self.parking,
            "land_size": self.land_size,
            "building_size": self.building_size,
            "year_built": self.year_built,
            "condition": self.condition,
            "quality": self.quality,
            "street_quality": self.street_quality,
            "view_quality": self.view_quality,
            "noise_level": self.noise_level,
            "appreciation_modifier": self.appreciation_modifier,
            "risk_modifier": self.risk_modifier,
            "base_value": self.base_value,
            # New fields
            "zoning_code": self.zoning_code,
            "days_on_market_last_sale": self.days_on_market_last_sale,
            "last_sale_price": self.last_sale_price,
            # Don't include full price/rent series in serialization to keep size manageable
            "hist_price_series_length": len(self.hist_price_series),
            "hist_rent_series_length": len(self.hist_rent_series),
            # Include some summary statistics instead
            "hist_price_min": min(self.hist_price_series) if self.hist_price_series else 0,
            "hist_price_max": max(self.hist_price_series) if self.hist_price_series else 0,
            "hist_price_mean": sum(self.hist_price_series) / len(self.hist_price_series) if self.hist_price_series else 0,
            "hist_rent_min": min(self.hist_rent_series) if self.hist_rent_series else 0,
            "hist_rent_max": max(self.hist_rent_series) if self.hist_rent_series else 0,
            "hist_rent_mean": sum(self.hist_rent_series) / len(self.hist_rent_series) if self.hist_rent_series else 0,
        }


@dataclass
class SuburbData:
    """Data for a suburb in the TLS system."""

    suburb_id: str
    name: str
    state: str
    postcode: str
    latitude: float
    longitude: float

    # Composite scores (0-100)
    appreciation_score: float
    risk_score: float
    liquidity_score: float
    overall_score: float

    # Confidence in scores (0-1)
    appreciation_confidence: float
    risk_confidence: float
    liquidity_confidence: float
    overall_confidence: float

    # Missing raw data fields
    mean_appreciation: float = 0.0  # %/year - Base drift for all props in suburb
    vol_appreciation: float = 0.0  # %/year - Shared σ for factor model
    macroecon_beta: float = 1.0  # Loading to city-wide factor
    zone_beta: float = 1.0  # Loading to region factor (eastern beaches, etc.)

    # Properties in this suburb
    properties: Dict[str, PropertyAttributes] = field(default_factory=dict)

    # Metric values specific to this suburb
    metrics: Dict[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize default values and validate."""
        # Set mean_appreciation based on appreciation_score if not provided
        if self.mean_appreciation == 0.0:
            # Convert 0-100 score to annual appreciation rate (0-10%)
            self.mean_appreciation = (self.appreciation_score / 100.0) * 0.10

        # Set vol_appreciation based on risk_score if not provided
        if self.vol_appreciation == 0.0:
            # Convert 0-100 risk score to volatility (0-15%)
            self.vol_appreciation = (self.risk_score / 100.0) * 0.15

        # Set macroecon_beta based on risk_score and appreciation_score if not provided
        if self.macroecon_beta == 1.0:
            # Higher risk and higher appreciation = higher beta
            risk_factor = self.risk_score / 50.0  # Normalize to 0-2 range
            appreciation_factor = self.appreciation_score / 50.0  # Normalize to 0-2 range
            self.macroecon_beta = (risk_factor + appreciation_factor) / 2.0

        # Set zone_beta based on location and risk_score if not provided
        if self.zone_beta == 1.0:
            # Use longitude as a proxy for east/west location
            # Eastern suburbs (higher longitude) tend to have higher zone_beta
            location_factor = (self.longitude - 150.5) * 2  # Normalize to roughly 0-2 range
            self.zone_beta = (location_factor + (self.risk_score / 50.0)) / 2.0

    def get_metric(self, metric_name: str) -> Optional[MetricValue]:
        """Get a suburb-specific metric."""
        return self.metrics.get(metric_name)

    def set_metric(self, metric_name: str, value: Union[float, MetricValue]) -> None:
        """Set a suburb-specific metric."""
        if isinstance(value, float):
            # Create a MetricValue with default confidence
            value = MetricValue(value=value, confidence=0.8)

        self.metrics[metric_name] = value

    def add_property(self, property_data: PropertyAttributes) -> None:
        """Add a property to the suburb."""
        self.properties[property_data.property_id] = property_data

    def get_property(self, property_id: str) -> Optional[PropertyAttributes]:
        """Get a property by ID."""
        return self.properties.get(property_id)

    def get_properties_by_criteria(
        self,
        min_bedrooms: Optional[int] = None,
        max_bedrooms: Optional[int] = None,
        min_bathrooms: Optional[int] = None,
        max_bathrooms: Optional[int] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        property_type: Optional[str] = None,
    ) -> List[PropertyAttributes]:
        """Get properties that match the given criteria."""
        matching_properties = []

        for prop in self.properties.values():
            if min_bedrooms is not None and prop.bedrooms < min_bedrooms:
                continue
            if max_bedrooms is not None and prop.bedrooms > max_bedrooms:
                continue
            if min_bathrooms is not None and prop.bathrooms < min_bathrooms:
                continue
            if max_bathrooms is not None and prop.bathrooms > max_bathrooms:
                continue

            value = prop.base_value
            if min_value is not None and value < min_value:
                continue
            if max_value is not None and value > max_value:
                continue

            if property_type is not None and prop.property_type != property_type:
                continue

            matching_properties.append(prop)

        return matching_properties

    @property
    def zone_color(self) -> str:
        """Get the zone color based on the overall score."""
        if self.overall_score >= 80:
            return "dark_green"
        elif self.overall_score >= 70:
            return "green"
        elif self.overall_score >= 60:
            return "light_green"
        elif self.overall_score >= 50:
            return "yellow"
        elif self.overall_score >= 40:
            return "orange"
        elif self.overall_score >= 30:
            return "light_red"
        else:
            return "red"

    @property
    def zone_category(self) -> str:
        """Get the zone category (simplified color)."""
        color = self.zone_color
        if "green" in color:
            return "green"
        elif color in ["yellow", "orange"]:
            return "orange"
        else:
            return "red"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "suburb_id": self.suburb_id,
            "name": self.name,
            "state": self.state,
            "postcode": self.postcode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "appreciation_score": self.appreciation_score,
            "risk_score": self.risk_score,
            "liquidity_score": self.liquidity_score,
            "overall_score": self.overall_score,
            "appreciation_confidence": self.appreciation_confidence,
            "risk_confidence": self.risk_confidence,
            "liquidity_confidence": self.liquidity_confidence,
            "overall_confidence": self.overall_confidence,
            "zone_color": self.zone_color,
            "zone_category": self.zone_category,
            "property_count": len(self.properties),
            # New fields
            "mean_appreciation": self.mean_appreciation,
            "vol_appreciation": self.vol_appreciation,
            "macroecon_beta": self.macroecon_beta,
            "zone_beta": self.zone_beta,
        }


class TLSDataManager:
    """Manager for TLS data."""

    def __init__(self, use_mock: bool = True):
        """
        Initialize the TLS data manager.

        Args:
            use_mock: Whether to use mock data
        """
        self.use_mock = use_mock

        # Suburbs by ID
        self.suburbs: Dict[str, SuburbData] = {}

        # Metrics by name
        self.metrics: Dict[str, Metric] = {}

        # Correlation matrix for metrics
        self.metric_correlations: Dict[str, Dict[str, float]] = {}

        # Suburb correlations
        self.suburb_correlations: Dict[str, Dict[str, float]] = {}

        # Data loaded flag
        self.data_loaded = False

        logger.info("TLS data manager initialized", use_mock=use_mock)

    async def load_data(self, simulation_id: Optional[str] = None) -> None:
        """
        Load TLS data.

        Args:
            simulation_id: Simulation ID for progress reporting
        """
        if self.data_loaded:
            logger.info("TLS data already loaded")
            return

        logger.info("Loading TLS data", use_mock=self.use_mock)

        # Get WebSocket manager for progress reporting
        websocket_manager = get_websocket_manager()

        try:
            # Report progress
            if simulation_id:
                await websocket_manager.send_progress(
                    simulation_id=simulation_id,
                    module="tls_module",
                    progress=0.0,
                    message="Loading TLS data",
                )

            if self.use_mock:
                # Load mock data
                await self._load_mock_data(simulation_id)
            else:
                # Load production data
                await self._load_production_data(simulation_id)

            # Calculate derived data
            await self._calculate_derived_data(simulation_id)

            self.data_loaded = True

            # Report completion
            if simulation_id:
                await websocket_manager.send_progress(
                    simulation_id=simulation_id,
                    module="tls_module",
                    progress=100.0,
                    message="TLS data loaded",
                    data={
                        "suburb_count": len(self.suburbs),
                        "metric_count": len(self.metrics),
                        "property_count": sum(len(s.properties) for s in self.suburbs.values()),
                    },
                )

            logger.info(
                "TLS data loaded",
                suburb_count=len(self.suburbs),
                metric_count=len(self.metrics),
                property_count=sum(len(s.properties) for s in self.suburbs.values()),
            )

        except Exception as e:
            logger.error("Error loading TLS data", error=str(e), exc_info=True)

            # Report error
            if simulation_id:
                await websocket_manager.send_error(
                    simulation_id=simulation_id,
                    error={
                        "message": f"Error loading TLS data: {str(e)}",
                        "code": "TLS_DATA_LOAD_ERROR",
                    },
                )

            raise

    async def _load_mock_data(self, simulation_id: Optional[str] = None) -> None:
        """
        Load mock TLS data from static file.

        Args:
            simulation_id: Simulation ID for progress reporting
        """
        logger.info("Loading mock TLS data from static file")

        # Get WebSocket manager for progress reporting
        websocket_manager = get_websocket_manager()

        # Report progress
        if simulation_id:
            await websocket_manager.send_progress(
                simulation_id=simulation_id,
                module="tls_module",
                progress=10.0,
                message="Loading TLS data from static file",
            )

        # Load data from static file
        data_file = "src/tls_module/data/sydney_suburbs_data.json"

        try:
            with open(data_file, "r") as f:
                data = json.load(f)

            # Report progress
            if simulation_id:
                await websocket_manager.send_progress(
                    simulation_id=simulation_id,
                    module="tls_module",
                    progress=30.0,
                    message="Processing suburbs",
                )

            # Process suburbs
            for i, (suburb_id, suburb_data) in enumerate(data["suburbs"].items()):
                # Create suburb
                suburb = SuburbData(
                    suburb_id=suburb_id,
                    name=suburb_data["name"],
                    state=suburb_data["state"],
                    postcode=suburb_data["postcode"],
                    latitude=suburb_data["latitude"],
                    longitude=suburb_data["longitude"],
                    appreciation_score=suburb_data["appreciation_score"],
                    risk_score=suburb_data["risk_score"],
                    liquidity_score=suburb_data["liquidity_score"],
                    overall_score=suburb_data["overall_score"],
                    appreciation_confidence=suburb_data["appreciation_confidence"],
                    risk_confidence=suburb_data["risk_confidence"],
                    liquidity_confidence=suburb_data["liquidity_confidence"],
                    overall_confidence=suburb_data["overall_confidence"],
                    # New fields - use defaults if not in the data
                    mean_appreciation=suburb_data.get("mean_appreciation", 0.0),
                    vol_appreciation=suburb_data.get("vol_appreciation", 0.0),
                    macroecon_beta=suburb_data.get("macroecon_beta", 1.0),
                    zone_beta=suburb_data.get("zone_beta", 1.0),
                )

                # Add metrics
                for metric_name, metric_data in suburb_data["metrics"].items():
                    suburb.set_metric(
                        metric_name,
                        MetricValue(
                            value=metric_data["value"],
                            confidence=metric_data["confidence"],
                            percentile=metric_data["percentile"],
                        ),
                    )

                # Add properties
                for property_data in suburb_data["properties"]:
                    # Create property
                    property_obj = PropertyAttributes(
                        property_id=property_data["property_id"],
                        suburb_id=property_data["suburb_id"],
                        property_type=property_data["property_type"],
                        bedrooms=property_data["bedrooms"],
                        bathrooms=property_data["bathrooms"],
                        parking=property_data["parking"],
                        land_size=property_data["land_size"],
                        building_size=property_data["building_size"],
                        year_built=property_data["year_built"],
                        condition=property_data["condition"],
                        quality=property_data["quality"],
                        street_quality=property_data["street_quality"],
                        view_quality=property_data["view_quality"],
                        noise_level=property_data["noise_level"],
                        appreciation_modifier=property_data["appreciation_modifier"],
                        risk_modifier=property_data["risk_modifier"],
                        base_value=property_data["base_value"],
                        # New fields - use defaults if not in the data
                        zoning_code=property_data.get("zoning_code", "R2"),
                        days_on_market_last_sale=property_data.get("days_on_market_last_sale", 30),
                        last_sale_price=property_data.get("last_sale_price", property_data["base_value"]),
                        hist_price_series=property_data.get("hist_price_series", []),
                        hist_rent_series=property_data.get("hist_rent_series", []),
                    )

                    # Add metrics
                    for metric_name, metric_data in property_data["metrics"].items():
                        property_obj.set_metric(
                            metric_name,
                            MetricValue(
                                value=metric_data["value"],
                                confidence=metric_data["confidence"],
                            ),
                        )

                    # Add property to suburb
                    suburb.add_property(property_obj)

                # Add suburb to dictionary
                self.suburbs[suburb_id] = suburb

                # Report progress periodically
                if simulation_id and i % 10 == 0:
                    await websocket_manager.send_progress(
                        simulation_id=simulation_id,
                        module="tls_module",
                        progress=30.0 + (i / len(data["suburbs"])) * 20.0,
                        message=f"Processed suburb {suburb.name}",
                    )

            # Report progress
            if simulation_id:
                await websocket_manager.send_progress(
                    simulation_id=simulation_id,
                    module="tls_module",
                    progress=50.0,
                    message="Processing metrics",
                )

            # Process metrics
            for i, (metric_name, metric_data) in enumerate(data["metrics"].items()):
                # Map static file categories to enum values
                category_mapping = {
                    "real": "REAL_ESTATE",
                    "supply": "SUPPLY_DEMAND",
                    "economic": "ECONOMIC",
                    "demographic": "DEMOGRAPHIC",
                    "risk": "RISK",
                    "location": "LOCATION",
                    "temporal": "TEMPORAL"
                }

                # Get the correct category
                file_category = metric_data["category"].lower()
                enum_category = category_mapping.get(file_category, file_category.upper())

                # Debug logging
                logger.debug(
                    f"Processing metric {metric_name}: file_category='{file_category}', enum_category='{enum_category}'"
                )

                # Create metric
                try:
                    metric = Metric(
                        name=metric_name,
                        category=getattr(MetricCategory, enum_category),
                        description=metric_data["description"],
                        unit=metric_data["unit"],
                        min_value=metric_data["min_value"],
                        max_value=metric_data["max_value"],
                        is_higher_better=metric_data["is_higher_better"],
                    )
                except AttributeError as ae:
                    logger.error(
                        f"Invalid category for metric {metric_name}: '{enum_category}' not found in MetricCategory enum",
                        file_category=file_category,
                        enum_category=enum_category,
                        available_categories=[e.value for e in MetricCategory],
                    )
                    raise

                # Add values from suburbs
                for suburb_id, suburb in self.suburbs.items():
                    if metric_name in suburb.metrics:
                        metric.set_value(suburb_id, suburb.metrics[metric_name])

                # Add metric to dictionary
                self.metrics[metric_name] = metric

                # Report progress periodically
                if simulation_id and i % 10 == 0:
                    await websocket_manager.send_progress(
                        simulation_id=simulation_id,
                        module="tls_module",
                        progress=50.0 + (i / len(data["metrics"])) * 20.0,
                        message=f"Processed metric {metric_name}",
                    )

            # Report progress
            if simulation_id:
                await websocket_manager.send_progress(
                    simulation_id=simulation_id,
                    module="tls_module",
                    progress=70.0,
                    message="Processing correlations",
                )

            # Process correlations
            self.metric_correlations = data["correlations"]["metrics"]
            self.suburb_correlations = data["correlations"]["suburbs"]

            # Report progress
            if simulation_id:
                await websocket_manager.send_progress(
                    simulation_id=simulation_id,
                    module="tls_module",
                    progress=90.0,
                    message="TLS data loaded",
                )

            logger.info(
                "Mock TLS data loaded from static file",
                suburb_count=len(self.suburbs),
                metric_count=len(self.metrics),
                property_count=sum(len(suburb.properties) for suburb in self.suburbs.values()),
            )

        except Exception as e:
            logger.error(
                "Error loading TLS data from static file",
                error=str(e),
                exc_info=True,
            )

            # NO FALLBACK - MUST USE STATIC FILE ONLY
            raise RuntimeError(f"Failed to load static TLS data file: {e}") from e

    async def _generate_mock_data(self, simulation_id: Optional[str] = None) -> None:
        """
        Generate mock TLS data.

        Args:
            simulation_id: Simulation ID for progress reporting
        """
        logger.info("Generating mock TLS data")

        # Get WebSocket manager for progress reporting
        websocket_manager = get_websocket_manager()

        # Define Sydney suburbs (30 representative suburbs)
        sydney_suburbs = [
            ("SYD001", "Bondi", "NSW", "2026", -33.8914, 151.2743),
            ("SYD002", "Manly", "NSW", "2095", -33.7971, 151.2857),
            ("SYD003", "Mosman", "NSW", "2088", -33.8288, 151.2428),
            ("SYD004", "Double Bay", "NSW", "2028", -33.8785, 151.2428),
            ("SYD005", "Paddington", "NSW", "2021", -33.8845, 151.2271),
            ("SYD006", "Surry Hills", "NSW", "2010", -33.8845, 151.2119),
            ("SYD007", "Newtown", "NSW", "2042", -33.8988, 151.1785),
            ("SYD008", "Parramatta", "NSW", "2150", -33.8148, 151.0011),
            ("SYD009", "Chatswood", "NSW", "2067", -33.7971, 151.1828),
            ("SYD010", "Cronulla", "NSW", "2230", -34.0581, 151.1543),
        ]

        # Report progress
        if simulation_id:
            await websocket_manager.send_progress(
                simulation_id=simulation_id,
                module="tls_module",
                progress=10.0,
                message="Creating suburbs",
            )

        # Create suburbs
        for i, (suburb_id, name, state, postcode, latitude, longitude) in enumerate(sydney_suburbs):
            # Generate scores with some correlation to location
            # Eastern/Northern suburbs tend to have higher scores
            base_score = 50.0

            # Location factor (east/north is higher)
            location_factor = (longitude - 150.5) * 20 + (33.9 - latitude) * 10

            # Add some randomness
            random_factor = random.uniform(-10, 10)

            # Calculate scores
            appreciation_score = min(100, max(0, base_score + location_factor + random_factor))
            risk_score = min(100, max(0, base_score - location_factor + random_factor))
            liquidity_score = min(100, max(0, base_score + location_factor * 0.5 + random_factor))
            overall_score = (appreciation_score * 0.4 + (100 - risk_score) * 0.3 + liquidity_score * 0.3)

            # Calculate confidences (higher for well-known suburbs)
            confidence_base = 0.7
            confidence_factor = random.uniform(-0.2, 0.2)
            appreciation_confidence = min(1.0, max(0.3, confidence_base + confidence_factor))
            risk_confidence = min(1.0, max(0.3, confidence_base + confidence_factor))
            liquidity_confidence = min(1.0, max(0.3, confidence_base + confidence_factor))
            overall_confidence = (appreciation_confidence + risk_confidence + liquidity_confidence) / 3

            # Create suburb
            suburb = SuburbData(
                suburb_id=suburb_id,
                name=name,
                state=state,
                postcode=postcode,
                latitude=latitude,
                longitude=longitude,
                appreciation_score=appreciation_score,
                risk_score=risk_score,
                liquidity_score=liquidity_score,
                overall_score=overall_score,
                appreciation_confidence=appreciation_confidence,
                risk_confidence=risk_confidence,
                liquidity_confidence=liquidity_confidence,
                overall_confidence=overall_confidence,
            )

            self.suburbs[suburb_id] = suburb

            # Report progress periodically
            if simulation_id and i % 5 == 0:
                await websocket_manager.send_progress(
                    simulation_id=simulation_id,
                    module="tls_module",
                    progress=10.0 + (i / len(sydney_suburbs)) * 20.0,
                    message=f"Created suburb {name}",
                )

        # Report progress
        if simulation_id:
            await websocket_manager.send_progress(
                simulation_id=simulation_id,
                module="tls_module",
                progress=30.0,
                message="Creating metrics",
            )

        # Create metrics
        await self._create_mock_metrics(simulation_id)

        # Report progress
        if simulation_id:
            await websocket_manager.send_progress(
                simulation_id=simulation_id,
                module="tls_module",
                progress=50.0,
                message="Creating properties",
            )

        # Create properties for each suburb
        await self._create_mock_properties(simulation_id)

        # Report progress
        if simulation_id:
            await websocket_manager.send_progress(
                simulation_id=simulation_id,
                module="tls_module",
                progress=70.0,
                message="Creating correlations",
            )

        # Create correlations
        await self._create_mock_correlations(simulation_id)

        logger.info(
            "Mock TLS data generated",
            suburb_count=len(self.suburbs),
            metric_count=len(self.metrics),
        )

    async def _create_mock_metrics(self, simulation_id: Optional[str] = None) -> None:
        """
        Create mock metrics for all suburbs.

        Args:
            simulation_id: Simulation ID for progress reporting
        """
        # Import metrics definitions
        from src.tls_module.tls_metrics import get_all_metrics

        # Get WebSocket manager for progress reporting
        websocket_manager = get_websocket_manager()

        # Get all metric definitions
        metric_definitions = get_all_metrics()

        # Create metrics
        for i, (metric_name, metric_def) in enumerate(metric_definitions):
            # Create metric
            metric = Metric(
                name=metric_name,
                category=metric_def["category"],
                description=metric_def["description"],
                unit=metric_def["unit"],
                min_value=metric_def["min_value"],
                max_value=metric_def["max_value"],
                is_higher_better=metric_def["is_higher_better"],
            )

            # Add to metrics dictionary
            self.metrics[metric_name] = metric

            # Generate values for each suburb
            for suburb_id, suburb in self.suburbs.items():
                # Base value depends on suburb scores
                if metric.is_higher_better is True:
                    # For positive metrics, higher suburb score means higher metric value
                    base_value = suburb.overall_score / 100.0
                elif metric.is_higher_better is False:
                    # For negative metrics, higher suburb score means lower metric value
                    base_value = 1.0 - (suburb.overall_score / 100.0)
                else:
                    # For neutral metrics, use middle value
                    base_value = 0.5

                # Scale to metric range
                value_range = metric.max_value - metric.min_value
                scaled_value = metric.min_value + (base_value * value_range)

                # Add randomness (more for lower confidence suburbs)
                randomness_factor = (1.0 - suburb.overall_confidence) * 0.5
                random_adjustment = random.uniform(-randomness_factor, randomness_factor) * value_range

                # Final value with constraints
                final_value = min(metric.max_value, max(metric.min_value, scaled_value + random_adjustment))

                # Create metric value with confidence
                metric_value = MetricValue(
                    value=final_value,
                    confidence=suburb.overall_confidence,
                )

                # Set value for suburb
                metric.set_value(suburb_id, metric_value)

                # Also store in suburb metrics for easy access
                suburb.set_metric(metric_name, metric_value)

            # Report progress periodically
            if simulation_id and i % 10 == 0:
                await websocket_manager.send_progress(
                    simulation_id=simulation_id,
                    module="tls_module",
                    progress=30.0 + (i / len(metric_definitions)) * 20.0,
                    message=f"Created metric {metric_name}",
                )

        logger.info("Created mock metrics", metric_count=len(self.metrics))

    async def _create_mock_properties(self, simulation_id: Optional[str] = None) -> None:
        """
        Create mock properties for all suburbs.

        Args:
            simulation_id: Simulation ID for progress reporting
        """
        # Get WebSocket manager for progress reporting
        websocket_manager = get_websocket_manager()

        # Property types with probabilities
        property_types = [
            ("house", 0.5),
            ("apartment", 0.3),
            ("townhouse", 0.15),
            ("duplex", 0.05),
        ]

        # Create properties for each suburb
        for i, (suburb_id, suburb) in enumerate(self.suburbs.items()):
            # Number of properties depends on suburb score (more for higher scores)
            # Between 20 and 100 properties per suburb
            num_properties = int(20 + (suburb.overall_score / 100.0) * 80)

            # Base property value from median_property_value metric
            base_property_value = 1000000.0  # Default if metric not available
            if "median_property_value" in suburb.metrics:
                base_property_value = suburb.metrics["median_property_value"].value

            # Create properties
            for j in range(num_properties):
                # Generate property ID
                property_id = f"{suburb_id}_P{j+1:04d}"

                # Select property type based on probabilities
                property_type = random.choices(
                    [pt[0] for pt in property_types],
                    weights=[pt[1] for pt in property_types],
                    k=1,
                )[0]

                # Generate bedrooms (1-5)
                if property_type == "apartment":
                    bedrooms = random.choices([1, 2, 3, 4], weights=[0.3, 0.4, 0.25, 0.05], k=1)[0]
                else:
                    bedrooms = random.choices([2, 3, 4, 5], weights=[0.2, 0.4, 0.3, 0.1], k=1)[0]

                # Generate bathrooms (usually bedrooms - 1 or equal)
                bathrooms = max(1, random.choices(
                    [bedrooms - 1, bedrooms, bedrooms + 1],
                    weights=[0.4, 0.5, 0.1],
                    k=1,
                )[0])

                # Generate parking (0-3)
                if property_type == "apartment":
                    parking = random.choices([0, 1, 2], weights=[0.2, 0.7, 0.1], k=1)[0]
                else:
                    parking = random.choices([1, 2, 3], weights=[0.3, 0.6, 0.1], k=1)[0]

                # Generate land size (square meters)
                if property_type == "house":
                    land_size = random.uniform(300, 1000)
                elif property_type == "townhouse":
                    land_size = random.uniform(150, 300)
                elif property_type == "duplex":
                    land_size = random.uniform(200, 400)
                else:  # apartment
                    land_size = 0.0

                # Generate building size (square meters)
                if property_type == "house":
                    building_size = random.uniform(120, 350)
                elif property_type == "townhouse":
                    building_size = random.uniform(100, 200)
                elif property_type == "duplex":
                    building_size = random.uniform(100, 250)
                else:  # apartment
                    building_size = random.uniform(50, 150)

                # Generate year built (1900-2023)
                # Higher score suburbs tend to have newer properties
                min_year = 1900
                max_year = 2023
                year_range = max_year - min_year
                year_built = min_year + int((suburb.overall_score / 100.0) * 0.5 * year_range + random.uniform(0, 0.5 * year_range))

                # Generate condition (0-1)
                # Newer properties tend to be in better condition
                age_factor = 1.0 - ((max_year - year_built) / year_range)
                condition = min(1.0, max(0.0, age_factor * 0.7 + random.uniform(0, 0.3)))

                # Generate quality (0-1)
                # Higher score suburbs tend to have higher quality properties
                quality = min(1.0, max(0.0, (suburb.overall_score / 100.0) * 0.8 + random.uniform(0, 0.2)))

                # Generate street quality (0-1)
                street_quality = min(1.0, max(0.0, (suburb.overall_score / 100.0) * 0.7 + random.uniform(-0.2, 0.3)))

                # Generate view quality (0-1)
                view_quality = min(1.0, max(0.0, random.uniform(0, 1.0)))

                # Generate noise level (0-1)
                noise_level = min(1.0, max(0.0, 1.0 - (suburb.overall_score / 100.0) * 0.6 + random.uniform(-0.2, 0.4)))

                # Generate appreciation modifier (0.8-1.2)
                appreciation_modifier = min(1.2, max(0.8, 1.0 + random.uniform(-0.2, 0.2)))

                # Generate risk modifier (0.8-1.2)
                risk_modifier = min(1.2, max(0.8, 1.0 + random.uniform(-0.2, 0.2)))

                # Calculate property value
                # Base value adjusted for property characteristics
                value_adjustments = {
                    "bedrooms": (bedrooms - 3) * 0.1,  # +/- 10% per bedroom difference from 3
                    "bathrooms": (bathrooms - 2) * 0.05,  # +/- 5% per bathroom difference from 2
                    "parking": parking * 0.03,  # +3% per parking space
                    "land_size": (land_size - 500) / 500 * 0.1 if land_size > 0 else 0,  # +/- 10% per 500sqm
                    "building_size": (building_size - 150) / 150 * 0.1,  # +/- 10% per 150sqm
                    "condition": (condition - 0.5) * 0.2,  # +/- 20% from average condition
                    "quality": (quality - 0.5) * 0.3,  # +/- 30% from average quality
                    "street_quality": (street_quality - 0.5) * 0.1,  # +/- 10% from average street
                    "view_quality": view_quality * 0.2,  # Up to +20% for great views
                    "noise_level": -noise_level * 0.1,  # Up to -10% for noisy locations
                }

                # Apply adjustments
                adjustment_factor = 1.0
                for adjustment in value_adjustments.values():
                    adjustment_factor += adjustment

                # Final property value
                property_value = base_property_value * adjustment_factor

                # Create property
                property_data = PropertyAttributes(
                    property_id=property_id,
                    suburb_id=suburb_id,
                    property_type=property_type,
                    bedrooms=bedrooms,
                    bathrooms=bathrooms,
                    parking=parking,
                    land_size=land_size,
                    building_size=building_size,
                    year_built=year_built,
                    condition=condition,
                    quality=quality,
                    street_quality=street_quality,
                    view_quality=view_quality,
                    noise_level=noise_level,
                    appreciation_modifier=appreciation_modifier,
                    risk_modifier=risk_modifier,
                    base_value=property_value,
                )

                # Add property to suburb
                suburb.add_property(property_data)

            # Report progress periodically
            if simulation_id and i % 5 == 0:
                await websocket_manager.send_progress(
                    simulation_id=simulation_id,
                    module="tls_module",
                    progress=50.0 + (i / len(self.suburbs)) * 20.0,
                    message=f"Created properties for {suburb.name}",
                    data={"property_count": num_properties},
                )

        # Count total properties
        total_properties = sum(len(suburb.properties) for suburb in self.suburbs.values())

        logger.info(
            "Created mock properties",
            suburb_count=len(self.suburbs),
            property_count=total_properties,
        )

    async def _create_mock_correlations(self, simulation_id: Optional[str] = None) -> None:
        """
        Create mock correlations between metrics and suburbs.

        Args:
            simulation_id: Simulation ID for progress reporting
        """
        # Create metric correlations
        await self._create_metric_correlations(simulation_id)

        # Create suburb correlations
        await self._create_suburb_correlations(simulation_id)

        logger.info(
            "Created mock correlations",
            metric_correlation_count=sum(len(corrs) for corrs in self.metric_correlations.values()),
            suburb_correlation_count=sum(len(corrs) for corrs in self.suburb_correlations.values()),
        )

    async def _create_metric_correlations(self, simulation_id: Optional[str] = None) -> None:
        """
        Create mock correlations between metrics.

        Args:
            simulation_id: Simulation ID for progress reporting
        """
        # Get WebSocket manager for progress reporting
        websocket_manager = get_websocket_manager()

        # Define strongly correlated metric pairs
        strong_correlations = [
            # Economic correlations
            ("employment_rate", "unemployment_rate", -0.9),  # Negatively correlated
            ("employment_rate", "median_household_income", 0.7),
            ("income_growth", "economic_resilience", 0.6),

            # Real estate correlations
            ("appreciation_1yr", "appreciation_3yr", 0.8),
            ("appreciation_3yr", "appreciation_5yr", 0.7),
            ("appreciation_5yr", "appreciation_10yr", 0.6),
            ("days_on_market", "auction_clearance_rate", -0.7),  # Negatively correlated
            ("rental_yield_gross", "median_property_value", -0.5),  # Negatively correlated
            ("vacancy_rate", "rental_yield_gross", -0.6),  # Negatively correlated

            # Risk correlations
            ("default_probability", "recovery_rate", -0.7),  # Negatively correlated
            ("market_liquidity", "days_on_market", -0.8),  # Negatively correlated

            # Location correlations
            ("school_quality", "median_household_income", 0.6),
            ("crime_rate", "property_value", -0.7),  # Negatively correlated

            # Supply/demand correlations
            ("demand_pressure", "days_on_market", -0.7),  # Negatively correlated
            ("development_pipeline", "appreciation_1yr", -0.4),  # Negatively correlated

            # Cross-category correlations
            ("employment_rate", "default_probability", -0.6),  # Negatively correlated
            ("median_household_income", "price_to_income_ratio", -0.5),  # Negatively correlated
            ("school_quality", "median_property_value", 0.7),
            ("crime_rate", "default_probability", 0.5),
        ]

        # Initialize correlation matrix
        for metric_name in self.metrics:
            self.metric_correlations[metric_name] = {}

        # Set self-correlations to 1.0
        for metric_name in self.metrics:
            self.metric_correlations[metric_name][metric_name] = 1.0

        # Set strong correlations
        for metric1, metric2, correlation in strong_correlations:
            if metric1 in self.metrics and metric2 in self.metrics:
                self.metric_correlations[metric1][metric2] = correlation
                self.metric_correlations[metric2][metric1] = correlation

        # Fill in remaining correlations with weak random values
        for i, metric1 in enumerate(self.metrics):
            for metric2 in self.metrics:
                if metric2 not in self.metric_correlations[metric1]:
                    # Random weak correlation (-0.3 to 0.3)
                    correlation = random.uniform(-0.3, 0.3)
                    self.metric_correlations[metric1][metric2] = correlation
                    self.metric_correlations[metric2][metric1] = correlation

            # Report progress periodically
            if simulation_id and i % 10 == 0:
                await websocket_manager.send_progress(
                    simulation_id=simulation_id,
                    module="tls_module",
                    progress=70.0 + (i / len(self.metrics)) * 10.0,
                    message=f"Created metric correlations for {metric1}",
                )

    async def _create_suburb_correlations(self, simulation_id: Optional[str] = None) -> None:
        """
        Create mock correlations between suburbs.

        Args:
            simulation_id: Simulation ID for progress reporting
        """
        # Get WebSocket manager for progress reporting
        websocket_manager = get_websocket_manager()

        # Initialize correlation matrix
        for suburb_id in self.suburbs:
            self.suburb_correlations[suburb_id] = {}

        # Set self-correlations to 1.0
        for suburb_id in self.suburbs:
            self.suburb_correlations[suburb_id][suburb_id] = 1.0

        # Calculate correlations based on geographic proximity and similarity
        for i, (suburb_id1, suburb1) in enumerate(self.suburbs.items()):
            for suburb_id2, suburb2 in self.suburbs.items():
                if suburb_id2 not in self.suburb_correlations[suburb_id1]:
                    # Calculate geographic distance
                    distance = ((suburb1.latitude - suburb2.latitude) ** 2 + (suburb1.longitude - suburb2.longitude) ** 2) ** 0.5

                    # Normalize distance (0-1)
                    max_distance = 0.5  # Maximum distance in Sydney
                    normalized_distance = min(1.0, distance / max_distance)

                    # Calculate score similarity
                    score_diff = abs(suburb1.overall_score - suburb2.overall_score) / 100.0

                    # Calculate correlation
                    # Closer and more similar suburbs have higher correlation
                    correlation = 1.0 - (normalized_distance * 0.7 + score_diff * 0.3)

                    # Add some randomness
                    correlation = min(0.95, max(0.0, correlation + random.uniform(-0.1, 0.1)))

                    # Set correlation
                    self.suburb_correlations[suburb_id1][suburb_id2] = correlation
                    self.suburb_correlations[suburb_id2][suburb_id1] = correlation

            # Report progress periodically
            if simulation_id and i % 5 == 0:
                await websocket_manager.send_progress(
                    simulation_id=simulation_id,
                    module="tls_module",
                    progress=80.0 + (i / len(self.suburbs)) * 10.0,
                    message=f"Created suburb correlations for {suburb1.name}",
                )

    async def _load_production_data(self, simulation_id: Optional[str] = None) -> None:
        """
        Load production TLS data.

        Args:
            simulation_id: Simulation ID for progress reporting
        """
        # This would load data from a database or API
        # For now, just use mock data
        logger.warning("Production data not implemented, using mock data instead")
        await self._load_mock_data(simulation_id)

    async def _calculate_derived_data(self, simulation_id: Optional[str] = None) -> None:
        """
        Calculate derived data from loaded data.

        Args:
            simulation_id: Simulation ID for progress reporting
        """
        # Get WebSocket manager for progress reporting
        websocket_manager = get_websocket_manager()

        # Calculate percentiles for all metrics
        for metric_name, metric in self.metrics.items():
            # Calculate percentiles
            for suburb_id, value in metric.values.items():
                percentile = metric.get_percentile(value.value)
                metric.values[suburb_id].percentile = percentile

        # Report progress
        if simulation_id:
            await websocket_manager.send_progress(
                simulation_id=simulation_id,
                module="tls_module",
                progress=90.0,
                message="Calculated derived data",
            )

        logger.info("Calculated derived data")

    # Public methods

    def get_suburb(self, suburb_id: str) -> Optional[SuburbData]:
        """
        Get a suburb by ID.

        Args:
            suburb_id: Suburb ID

        Returns:
            Suburb data or None if not found
        """
        return self.suburbs.get(suburb_id)

    def get_suburb_by_name(self, name: str) -> Optional[SuburbData]:
        """
        Get a suburb by name.

        Args:
            name: Suburb name

        Returns:
            Suburb data or None if not found
        """
        for suburb in self.suburbs.values():
            if suburb.name.lower() == name.lower():
                return suburb
        return None

    def get_suburbs_by_zone(self, zone_category: str) -> List[SuburbData]:
        """
        Get suburbs by zone category.

        Args:
            zone_category: Zone category (green, orange, red)

        Returns:
            List of suburbs in the zone
        """
        return [
            suburb for suburb in self.suburbs.values()
            if suburb.zone_category == zone_category
        ]

    def get_suburbs_by_score_range(
        self,
        min_score: Optional[float] = None,
        max_score: Optional[float] = None,
    ) -> List[SuburbData]:
        """
        Get suburbs by overall score range.

        Args:
            min_score: Minimum overall score (0-100)
            max_score: Maximum overall score (0-100)

        Returns:
            List of suburbs in the score range
        """
        min_score = min_score if min_score is not None else 0.0
        max_score = max_score if max_score is not None else 100.0

        return [
            suburb for suburb in self.suburbs.values()
            if min_score <= suburb.overall_score <= max_score
        ]

    def get_suburbs_by_metric_range(
        self,
        metric_name: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ) -> List[SuburbData]:
        """
        Get suburbs by metric value range.

        Args:
            metric_name: Metric name
            min_value: Minimum metric value
            max_value: Maximum metric value

        Returns:
            List of suburbs in the metric value range
        """
        if metric_name not in self.metrics:
            raise ValidationError(
                f"Metric {metric_name} not found",
                code=ErrorCode.DATA_NOT_FOUND,
            )

        metric = self.metrics[metric_name]
        min_value = min_value if min_value is not None else metric.min_value
        max_value = max_value if max_value is not None else metric.max_value

        result = []
        for suburb_id, suburb in self.suburbs.items():
            metric_value = suburb.get_metric(metric_name)
            if metric_value and min_value <= metric_value.value <= max_value:
                result.append(suburb)

        return result

    def get_suburbs_by_percentile(
        self,
        metric_name: str,
        min_percentile: float = 0.0,
        max_percentile: float = 1.0,
    ) -> List[SuburbData]:
        """
        Get suburbs by metric percentile range.

        Args:
            metric_name: Metric name
            min_percentile: Minimum percentile (0-1)
            max_percentile: Maximum percentile (0-1)

        Returns:
            List of suburbs in the percentile range
        """
        if metric_name not in self.metrics:
            raise ValidationError(
                f"Metric {metric_name} not found",
                code=ErrorCode.DATA_NOT_FOUND,
            )

        result = []
        for suburb_id, suburb in self.suburbs.items():
            metric_value = suburb.get_metric(metric_name)
            if metric_value and metric_value.percentile is not None:
                if min_percentile <= metric_value.percentile <= max_percentile:
                    result.append(suburb)

        return result

    def get_metric(self, metric_name: str) -> Optional[Metric]:
        """
        Get a metric by name.

        Args:
            metric_name: Metric name

        Returns:
            Metric or None if not found
        """
        return self.metrics.get(metric_name)

    def get_metrics_by_category(self, category: MetricCategory) -> List[Metric]:
        """
        Get metrics by category.

        Args:
            category: Metric category

        Returns:
            List of metrics in the category
        """
        return [
            metric for metric in self.metrics.values()
            if metric.category == category
        ]

    def get_metric_correlation(self, metric1: str, metric2: str) -> float:
        """
        Get correlation between two metrics.

        Args:
            metric1: First metric name
            metric2: Second metric name

        Returns:
            Correlation coefficient (-1 to 1)
        """
        if metric1 not in self.metrics:
            raise ValidationError(
                f"Metric {metric1} not found",
                code=ErrorCode.DATA_NOT_FOUND,
            )

        if metric2 not in self.metrics:
            raise ValidationError(
                f"Metric {metric2} not found",
                code=ErrorCode.DATA_NOT_FOUND,
            )

        return self.metric_correlations.get(metric1, {}).get(metric2, 0.0)

    def get_suburb_correlation(self, suburb_id1: str, suburb_id2: str) -> float:
        """
        Get correlation between two suburbs.

        Args:
            suburb_id1: First suburb ID
            suburb_id2: Second suburb ID

        Returns:
            Correlation coefficient (0 to 1)
        """
        if suburb_id1 not in self.suburbs:
            raise ValidationError(
                f"Suburb {suburb_id1} not found",
                code=ErrorCode.DATA_NOT_FOUND,
            )

        if suburb_id2 not in self.suburbs:
            raise ValidationError(
                f"Suburb {suburb_id2} not found",
                code=ErrorCode.DATA_NOT_FOUND,
            )

        return self.suburb_correlations.get(suburb_id1, {}).get(suburb_id2, 0.0)

    def get_properties_by_criteria(
        self,
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
        result = []

        # Filter suburbs
        if suburb_ids:
            suburbs = [self.suburbs[sid] for sid in suburb_ids if sid in self.suburbs]
        elif zone_category:
            suburbs = self.get_suburbs_by_zone(zone_category)
        else:
            suburbs = list(self.suburbs.values())

        # Get properties from each suburb
        for suburb in suburbs:
            matching_properties = suburb.get_properties_by_criteria(
                min_bedrooms=min_bedrooms,
                max_bedrooms=max_bedrooms,
                min_bathrooms=min_bathrooms,
                max_bathrooms=max_bathrooms,
                min_value=min_value,
                max_value=max_value,
                property_type=property_type,
            )

            for prop in matching_properties:
                result.append((suburb, prop))

                if len(result) >= limit:
                    break

            if len(result) >= limit:
                break

        return result

    def get_zone_distribution(self) -> Dict[str, int]:
        """
        Get distribution of suburbs by zone category.

        Returns:
            Dictionary mapping zone categories to counts
        """
        distribution = {"green": 0, "orange": 0, "red": 0}

        for suburb in self.suburbs.values():
            distribution[suburb.zone_category] += 1

        return distribution

    def get_metric_statistics(self, metric_name: str) -> Dict[str, float]:
        """
        Get statistics for a metric across all suburbs.

        Args:
            metric_name: Metric name

        Returns:
            Dictionary of statistics
        """
        if metric_name not in self.metrics:
            raise ValidationError(
                f"Metric {metric_name} not found",
                code=ErrorCode.DATA_NOT_FOUND,
            )

        metric = self.metrics[metric_name]
        values = [v.value for v in metric.values.values()]

        if not values:
            return {
                "mean": 0.0,
                "median": 0.0,
                "std_dev": 0.0,
                "min": 0.0,
                "max": 0.0,
                "count": 0,
            }

        return {
            "mean": float(np.mean(values)),
            "median": float(np.median(values)),
            "std_dev": float(np.std(values)),
            "min": float(np.min(values)),
            "max": float(np.max(values)),
            "count": len(values),
        }

    def get_metric_distribution_by_zone(
        self, metric_name: str
    ) -> Dict[str, Dict[str, float]]:
        """
        Get distribution of a metric by zone category.

        Args:
            metric_name: Metric name

        Returns:
            Dictionary mapping zone categories to metric statistics
        """
        if metric_name not in self.metrics:
            raise ValidationError(
                f"Metric {metric_name} not found",
                code=ErrorCode.DATA_NOT_FOUND,
            )

        # Group values by zone
        zone_values = {"green": [], "orange": [], "red": []}

        for suburb_id, suburb in self.suburbs.items():
            metric_value = suburb.get_metric(metric_name)
            if metric_value:
                zone_values[suburb.zone_category].append(metric_value.value)

        # Calculate statistics for each zone
        result = {}
        for zone, values in zone_values.items():
            if not values:
                result[zone] = {
                    "mean": 0.0,
                    "median": 0.0,
                    "std_dev": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "count": 0,
                }
            else:
                result[zone] = {
                    "mean": float(np.mean(values)),
                    "median": float(np.median(values)),
                    "std_dev": float(np.std(values)),
                    "min": float(np.min(values)),
                    "max": float(np.max(values)),
                    "count": len(values),
                }

        return result

    # Enhanced visualization and unit-level metrics methods

    def get_property_distribution_by_type(self) -> Dict[str, int]:
        """
        Get distribution of properties by type.

        Returns:
            Dictionary mapping property types to counts
        """
        distribution = {}

        for suburb in self.suburbs.values():
            for prop in suburb.properties:
                property_type = prop.property_type
                if property_type not in distribution:
                    distribution[property_type] = 0
                distribution[property_type] += 1

        return distribution

    def get_property_distribution_by_bedrooms(self) -> Dict[int, int]:
        """
        Get distribution of properties by number of bedrooms.

        Returns:
            Dictionary mapping bedroom counts to property counts
        """
        distribution = {}

        for suburb in self.suburbs.values():
            for prop in suburb.properties:
                bedrooms = prop.bedrooms
                if bedrooms not in distribution:
                    distribution[bedrooms] = 0
                distribution[bedrooms] += 1

        return distribution

    def get_property_distribution_by_value(self, num_bins: int = 10) -> List[Dict[str, Any]]:
        """
        Get distribution of properties by value.

        Args:
            num_bins: Number of bins for the histogram

        Returns:
            List of dictionaries with bin information
        """
        # Get all property values
        values = []
        for suburb in self.suburbs.values():
            for prop in suburb.properties:
                values.append(prop.base_value)

        if not values:
            return []

        # Create histogram
        hist, bin_edges = np.histogram(values, bins=num_bins)

        # Format result
        result = []
        for i in range(len(hist)):
            result.append({
                "bin_start": float(bin_edges[i]),
                "bin_end": float(bin_edges[i + 1]),
                "count": int(hist[i]),
                "percentage": float(hist[i] / len(values) * 100),
            })

        return result

    def get_property_distribution_by_zone(self) -> Dict[str, int]:
        """
        Get distribution of properties by zone category.

        Returns:
            Dictionary mapping zone categories to property counts
        """
        distribution = {"green": 0, "orange": 0, "red": 0}

        for suburb in self.suburbs.values():
            for _ in suburb.properties:
                distribution[suburb.zone_category] += 1

        return distribution

    def get_metric_histogram(self, metric_name: str, num_bins: int = 10) -> List[Dict[str, Any]]:
        """
        Get histogram for a metric across all suburbs.

        Args:
            metric_name: Metric name
            num_bins: Number of bins for the histogram

        Returns:
            List of dictionaries with bin information
        """
        if metric_name not in self.metrics:
            raise ValidationError(
                f"Metric {metric_name} not found",
                code=ErrorCode.DATA_NOT_FOUND,
            )

        # Get all values
        values = []
        for suburb_id, suburb in self.suburbs.items():
            metric_value = suburb.get_metric(metric_name)
            if metric_value:
                values.append(metric_value.value)

        if not values:
            return []

        # Create histogram
        hist, bin_edges = np.histogram(values, bins=num_bins)

        # Format result
        result = []
        for i in range(len(hist)):
            result.append({
                "bin_start": float(bin_edges[i]),
                "bin_end": float(bin_edges[i + 1]),
                "count": int(hist[i]),
                "percentage": float(hist[i] / len(values) * 100),
            })

        return result

    def get_strong_metric_correlations(self, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Get strongly correlated metrics.

        Args:
            threshold: Correlation threshold (absolute value)

        Returns:
            List of dictionaries with correlation information
        """
        result = []

        # Check all metric pairs
        metric_names = list(self.metrics.keys())
        for i, metric1 in enumerate(metric_names):
            for j, metric2 in enumerate(metric_names):
                if i < j:  # Only include each pair once
                    correlation = self.get_metric_correlation(metric1, metric2)
                    if abs(correlation) >= threshold:
                        result.append({
                            "metric1": metric1,
                            "metric2": metric2,
                            "correlation": float(correlation),
                            "is_positive": correlation > 0,
                        })

        # Sort by absolute correlation (highest first)
        result.sort(key=lambda c: abs(c["correlation"]), reverse=True)

        return result

    def get_similar_suburbs(self, suburb_id: str, threshold: float = 0.8, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get suburbs similar to a given suburb.

        Args:
            suburb_id: Suburb ID
            threshold: Similarity threshold (0-1)
            limit: Maximum number of similar suburbs to return

        Returns:
            List of dictionaries with similarity information
        """
        if suburb_id not in self.suburbs:
            raise ValidationError(
                f"Suburb {suburb_id} not found",
                code=ErrorCode.DATA_NOT_FOUND,
            )

        # Get correlations for this suburb
        correlations = self.suburb_correlations.get(suburb_id, {})

        # Filter by threshold and exclude the suburb itself
        similar_suburbs = []
        for other_id, correlation in correlations.items():
            if other_id != suburb_id and correlation >= threshold:
                similar_suburbs.append({
                    "suburb_id": other_id,
                    "name": self.suburbs[other_id].name,
                    "similarity": float(correlation),
                })

        # Sort by similarity (highest first)
        similar_suburbs.sort(key=lambda s: s["similarity"], reverse=True)

        # Apply limit
        return similar_suburbs[:limit]

    def get_zone_map_data(self) -> Dict[str, Any]:
        """
        Get data for zone map visualization.

        Returns:
            GeoJSON-like data structure
        """
        features = []

        for suburb in self.suburbs.values():
            features.append({
                "type": "Feature",
                "properties": {
                    "suburb_id": suburb.suburb_id,
                    "name": suburb.name,
                    "state": suburb.state,
                    "postcode": suburb.postcode,
                    "zone_category": suburb.zone_category,
                    "overall_score": suburb.overall_score,
                    "appreciation_score": suburb.appreciation_score,
                    "risk_score": suburb.risk_score,
                    "liquidity_score": suburb.liquidity_score,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [suburb.longitude, suburb.latitude],
                },
            })

        return {
            "type": "FeatureCollection",
            "features": features,
        }
