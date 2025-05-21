# Price Path Simulator Module

## Overview

The Price Path Simulator module is responsible for modeling how property values change over time in different zones. It generates realistic price paths for properties based on stochastic models and integrates with the TLS module to apply these price paths to specific properties.

## Features

### Basic Price Path Simulator
- Multiple stochastic models for price path simulation:
  - Geometric Brownian Motion (GBM)
  - Mean-reverting models
  - Regime-switching models
- Zone-specific appreciation rates and volatility
- Correlation between zone price paths
- Suburb-level and property-level variation
- Comprehensive visualization support
- Progress reporting via WebSocket
- Error handling and validation

### Enhanced Price Path Simulator
- Sydney-specific property market cycle model
- Deep integration with TLS module data:
  - Uses suburb-specific appreciation scores
  - Uses suburb-specific risk scores
  - Uses suburb-specific metrics (school quality, crime rate, etc.)
- Property-specific factors:
  - Property type (house, apartment, townhouse, etc.)
  - Number of bedrooms and bathrooms
  - Land size
  - Property age
- Economic factor integration:
  - Interest rate impact
  - Employment growth impact
  - Population growth impact
  - Income growth impact
  - Supply/demand impact
- Enhanced visualization and statistics:
  - Suburb correlation heatmap
  - Zone and suburb performance charts
  - Zone and suburb allocation recommendations
  - Sydney market cycle visualization
  - Economic factor impact visualization
  - Property type and characteristic modifier visualization

## Integration

The Price Path Simulator integrates with:
- TLS Module: To get property data and apply price paths to specific properties
- Loan Generator: To update property values for generated loans
- Exit Simulator: To provide property values for exit decisions
- Risk Metrics: To provide data for risk analysis

## Configuration Parameters

The module uses the following configuration parameters from the simulation config:

```json
{
  "appreciation_rates": {
    "green": 0.05,
    "orange": 0.03,
    "red": 0.01
  },
  "price_path": {
    "model_type": "gbm",
    "volatility": {
      "green": 0.03,
      "orange": 0.05,
      "red": 0.08
    },
    "correlation_matrix": {
      "green_orange": 0.7,
      "green_red": 0.5,
      "orange_red": 0.8
    },
    "mean_reversion_params": {
      "speed": 0.2,
      "long_term_mean": 0.03
    },
    "regime_switching_params": {
      "bull_market_rate": 0.08,
      "bear_market_rate": -0.03,
      "bull_to_bear_prob": 0.1,
      "bear_to_bull_prob": 0.3
    },
    "time_step": "monthly",
    "suburb_variation": 0.02,
    "property_variation": 0.01,
    "cycle_position": 0.5
  }
}
```

## API Endpoints

The module exposes the following API endpoints:

- `GET /api/v1/simulations/{simulation_id}/price-paths`: Get price path data for a simulation
- `GET /api/v1/simulations/{simulation_id}/price-paths/visualization`: Get visualization data for price paths
- `GET /api/v1/simulations/{simulation_id}/price-paths/statistics`: Get statistics for price paths
- `POST /api/v1/simulations/{simulation_id}/price-paths/scenario`: Run a price path scenario with custom parameters

## Implementation Details

### Stochastic Models

#### Geometric Brownian Motion (GBM)

The GBM model is a standard model for asset prices and is defined by the stochastic differential equation:

```
dS_t = μS_t dt + σS_t dW_t
```

where:
- S_t is the asset price at time t
- μ is the drift (expected return)
- σ is the volatility
- W_t is a Wiener process (Brownian motion)

#### Mean-Reverting Model

The mean-reverting model (Ornstein-Uhlenbeck process) is defined by:

```
dS_t = θ(μ - S_t)dt + σdW_t
```

where:
- θ is the speed of mean reversion
- μ is the long-term mean

#### Regime-Switching Model

The regime-switching model alternates between bull and bear market regimes, each with different parameters:

- Bull market: Higher appreciation rates, lower volatility
- Bear market: Lower or negative appreciation rates, higher volatility
- Transition probabilities between regimes

### Correlation

Correlation between zone price paths is implemented using Cholesky decomposition to generate correlated random variables.

### Visualization

The module provides the following visualizations:

- Price path charts for each zone
- Zone comparison chart
- Correlation heatmap
- Final value distribution
- Property cycle position chart
- Market regime chart (for regime-switching model)

## Usage Example

### Basic Price Path Simulator

```python
from src.price_path.price_path import simulate_price_paths, get_price_path_summary

# Simulate price paths
await simulate_price_paths(context)

# Access price paths
price_paths = context.price_paths
zone_price_paths = price_paths["zone_price_paths"]
suburb_price_paths = price_paths["suburb_price_paths"]
property_price_paths = price_paths["property_price_paths"]

# Get price path statistics
price_path_stats = context.price_path_stats

# Get price path visualization
price_path_visualization = context.price_path_visualization

# Get price path summary
summary = await get_price_path_summary(context)
```

### Enhanced Price Path Simulator

```python
from src.price_path.enhanced_price_path import simulate_enhanced_price_paths, get_enhanced_price_path_summary

# Simulate enhanced price paths
await simulate_enhanced_price_paths(context)

# Access price paths
price_paths = context.price_paths
zone_price_paths = price_paths["zone_price_paths"]
suburb_price_paths = price_paths["suburb_price_paths"]
property_price_paths = price_paths["property_price_paths"]

# Get price path statistics
price_path_stats = context.price_path_stats

# Get price path visualization
price_path_visualization = context.price_path_visualization

# Get enhanced price path summary
summary = await get_enhanced_price_path_summary(context)
```

## API Endpoints

The Price Path Simulator provides the following API endpoints:

### Basic Price Path Endpoints

- `GET /api/v1/simulations/{simulation_id}/price-paths`: Get price path data for a simulation
- `GET /api/v1/simulations/{simulation_id}/price-paths/visualization`: Get visualization data for price paths
- `GET /api/v1/simulations/{simulation_id}/price-paths/statistics`: Get statistics for price paths
- `POST /api/v1/simulations/{simulation_id}/price-paths/property-value`: Calculate the property value at a specific month
- `POST /api/v1/simulations/{simulation_id}/price-paths/scenario`: Run a price path scenario with custom parameters

### Enhanced Price Path Endpoints

- `POST /api/v1/simulations/{simulation_id}/price-paths/enhanced-property-value`: Calculate the enhanced property value at a specific month
- `POST /api/v1/simulations/{simulation_id}/price-paths/enhanced-scenario`: Run an enhanced price path scenario with custom parameters

## Error Handling

The module handles the following error conditions:

- Invalid configuration parameters
- Missing TLS data
- Numerical instability in stochastic models
- Correlation matrix not positive definite

## Performance Considerations

- Price path simulation can be computationally intensive, especially for large portfolios
- The module uses vectorized operations with NumPy for performance
- For Monte Carlo simulations, the module supports parallel computation
