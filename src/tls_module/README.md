# Traffic Light System (TLS) Module

The Traffic Light System (TLS) module provides a sophisticated classification system for geographic areas (suburbs) with multi-dimensional scoring, rich metrics, and property-level variation.

## Features

- **Multi-dimensional Scoring**: Appreciation, risk, and liquidity scores with overall combined score
- **Confidence Levels**: All metrics include confidence levels to indicate data reliability
- **Rich Metrics**: Comprehensive set of economic, demographic, and real estate metrics
- **Property-Level Variation**: Detailed property attributes with individual metric variations
- **Correlation Analysis**: Analysis of relationships between metrics and suburbs
- **Visualization Support**: Data distributions, correlations, and geographic visualization
- **Zone-Based Classification**: Green, orange, and red zones for investment targeting
- **Static Data**: Consistent data for testing and development

## Architecture

The TLS module consists of the following components:

- **TLSDataManager**: Main class for managing TLS data
- **SuburbData**: Class representing a suburb with metrics and properties
- **PropertyAttributes**: Class representing a property with attributes and metrics
- **Metric**: Class representing a metric with values for different suburbs
- **MetricValue**: Class representing a metric value with confidence and percentile

## Data Structure

### Suburbs

Each suburb has:
- Basic information (ID, name, state, postcode, coordinates)
- Scores (appreciation, risk, liquidity, overall)
- Confidence levels for each score
- Zone category (green, orange, red)
- Collection of properties
- Collection of metrics

### Properties

Each property has:
- Basic information (ID, suburb ID, property type)
- Physical characteristics (bedrooms, bathrooms, parking, size)
- Quality attributes (condition, quality, street quality, view quality)
- Risk and appreciation modifiers
- Base value
- Collection of property-specific metrics

### Metrics

The module includes metrics in the following categories:
- **Economic**: Employment rates, income growth, economic resilience
- **Real Estate**: Appreciation rates, days on market, rental yields
- **Demographic**: Population growth, education levels, age distribution
- **Risk**: Default probabilities, recovery rates, market liquidity
- **Location**: School quality, crime rates, walkability
- **Supply/Demand**: Development pipeline, zoning restrictions
- **Temporal**: Price momentum, seasonal adjustments, cycle position

## API

### Core Functions

- `get_tls_manager(use_mock=True)`: Get the global TLS data manager instance
- `reset_tls_manager()`: Reset the global TLS data manager instance

### TLSDataManager Methods

- `load_data(simulation_id=None)`: Load TLS data
- `get_zone_distribution()`: Get distribution of suburbs by zone category
- `get_suburbs_by_zone(zone_category)`: Get suburbs by zone category
- `get_metric(metric_name)`: Get a metric by name
- `get_suburb(suburb_id)`: Get a suburb by ID
- `get_metrics_by_category(category)`: Get metrics by category
- `get_metric_correlation(metric1, metric2)`: Get correlation between two metrics
- `get_properties_by_criteria(...)`: Get properties by criteria

### Visualization Methods

- `get_property_distribution_by_type()`: Get distribution of properties by type
- `get_property_distribution_by_bedrooms()`: Get distribution of properties by bedrooms
- `get_property_distribution_by_value(num_bins=10)`: Get distribution of properties by value
- `get_property_distribution_by_zone()`: Get distribution of properties by zone
- `get_metric_histogram(metric_name, num_bins=10)`: Get histogram for a metric
- `get_metric_correlation_matrix(metric_names)`: Get correlation matrix for metrics
- `get_strong_metric_correlations(threshold=0.7)`: Get strongly correlated metrics
- `get_similar_suburbs(suburb_id, threshold=0.8, limit=10)`: Get similar suburbs
- `get_zone_map_data()`: Get data for zone map visualization

## REST API

The TLS module provides the following REST API endpoints:

### Zone Information

- `GET /tls/zones/distribution`: Get distribution of suburbs by zone category

### Metrics

- `GET /tls/metrics`: Get all metrics or metrics by category
- `GET /tls/metrics/{metric_name}/distribution`: Get distribution of a metric

### Suburbs

- `GET /tls/suburbs`: Get all suburbs or suburbs by zone
- `GET /tls/suburbs/{suburb_id}`: Get a suburb by ID
- `GET /tls/suburbs/{suburb_id}/properties`: Get properties in a suburb

### Properties

- `GET /tls/suburbs/{suburb_id}/properties/{property_id}`: Get a property by ID
- `GET /tls/properties`: Get properties across all suburbs

### Correlations

- `GET /tls/correlations/metrics`: Get correlation matrix for metrics

### Visualizations

- `GET /tls/visualization/zone_map`: Get data for zone map visualization
- `GET /tls/visualization/property_distribution`: Get property distribution data

## Usage

```python
from src.tls_module import get_tls_manager

# Get TLS manager
tls_manager = get_tls_manager(use_mock=True)

# Load data
await tls_manager.load_data()

# Get zone distribution
zone_distribution = tls_manager.get_zone_distribution()
print(f"Green: {zone_distribution['green']}, Orange: {zone_distribution['orange']}, Red: {zone_distribution['red']}")

# Get suburbs in green zone
green_suburbs = tls_manager.get_suburbs_by_zone("green")
print(f"Found {len(green_suburbs)} suburbs in green zone")

# Get properties by criteria
properties = tls_manager.get_properties_by_criteria(
    min_bedrooms=3,
    max_bedrooms=4,
    min_bathrooms=2,
    property_type="house",
    zone_category="green",
    limit=10,
)
print(f"Found {len(properties)} properties matching criteria")
```

## Integration with Other Modules

The TLS module integrates with:

- **Capital Allocator**: Uses zone distribution for capital allocation
- **Loan Generator**: Uses property data for loan generation
- **Waterfall Engine**: Uses property metrics for performance calculation
- **Scenario Builder**: Uses TLS data for scenario generation
- **Performance Reporter**: Uses TLS metrics for reporting

## Data Sources

The TLS module uses data from:
- Sydney House Prices dataset (2000-2019)
- NSW Housing Data (economic and demographic factors)
- Calculated metrics based on real-world relationships
