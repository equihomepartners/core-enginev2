# Exit Simulator Module

## Overview

The Exit Simulator module is responsible for modeling how and when loans exit the portfolio. It simulates various exit events including property sales, refinancing, defaults, and term completions. The module works closely with the Price Path Simulator to determine property values at exit and calculate appreciation sharing amounts based on the EQU IHOME product terms.

## Components

The Exit Simulator consists of two main components:

1. **Base Exit Simulator** (`exit_simulator.py`): Provides core exit simulation functionality
2. **Enhanced Exit Simulator** (`enhanced_exit_simulator.py`): Extends the base simulator with advanced features

## Features

### Base Exit Simulator

- Multiple exit probability models:
  - Time-based model (based on loan age)
  - Price-based model (based on property appreciation)
  - Combined model (weighted combination of multiple factors)
  - Stress test model (for scenario testing)
- Exit type determination:
  - Sale probability based on property appreciation, market conditions, and loan age
  - Refinance probability based on interest rates and borrower equity
  - Default probability based on economic conditions and borrower characteristics
  - Term completion for loans reaching their full term
- Exit value calculation:
  - Property value at exit (using Price Path Simulator)
  - Appreciation sharing calculation based on EQU IHOME terms
  - Recovery value in case of defaults
  - Fund return calculation for each exit type
- Comprehensive visualization and reporting:
  - Exit timing distribution charts
  - Exit type distribution charts
  - Cumulative exits over time
  - Return distribution by exit type
  - Sensitivity analysis to various factors

### Enhanced Exit Simulator

- **Behavioral Models**:
  - Interest rate sensitivity for refinancing
  - Appreciation sensitivity for sales
  - Life event modeling (random life events triggering exits)
  - Herd behavior (correlation in exit decisions)

- **Economic Integration**:
  - Macroeconomic scenario generation (GDP, inflation, employment)
  - Recession impact modeling
  - Local economic factors (migration patterns, suburb desirability)
  - Regulatory and tax considerations

- **Cohort Analysis**:
  - Vintage segmentation (by origination year)
  - LTV segmentation (by loan-to-value ratio)
  - Zone segmentation (by geographic zone)

- **Risk Metrics**:
  - Value-at-Risk (VaR) calculation
  - Conditional VaR / Expected Shortfall
  - Tail risk analysis
  - Stress testing
  - Maximum drawdown

- **Machine Learning Integration**:
  - Cluster analysis to identify exit patterns
  - Predictive models for exit timing and type
  - Feature importance analysis
  - Anomaly detection

- **Advanced Visualizations**:
  - Cohort performance charts
  - Risk metric visualizations
  - Geospatial exit maps
  - Economic scenario charts
  - Comparative visualizations (actual vs. expected)

## Integration

The Exit Simulator integrates with:
- **Price Path Simulator**: To determine property values at exit
- **Loan Generator**: To access loan details
- **Capital Allocator**: To provide exit information for reinvestment
- **WebSocket Manager**: For progress reporting
- **Orchestrator**: For execution sequence

## Configuration Parameters

### Base Exit Simulator Parameters

#### Exit Probability Parameters
- `base_exit_rate`: Base annual exit probability (default: 0.1)
- `time_factor`: Weight for time-based exit probability (default: 0.4)
- `price_factor`: Weight for price-based exit probability (default: 0.6)
- `min_hold_period`: Minimum holding period in years (default: 1)
- `max_hold_period`: Maximum holding period in years (default: 10)

#### Exit Type Parameters
- `sale_weight`: Base weight for sale exits (default: 0.6)
- `refinance_weight`: Base weight for refinance exits (default: 0.3)
- `default_weight`: Base weight for default exits (default: 0.1)
- `appreciation_sale_multiplier`: How much appreciation increases sale probability (default: 2.0)
- `interest_rate_refinance_multiplier`: How much interest rate changes affect refinance probability (default: 3.0)
- `economic_factor_default_multiplier`: How much economic factors affect default probability (default: 2.0)

#### Appreciation Sharing Parameters
- `appreciation_share`: Fund's share of appreciation (default: 0.2)
- `min_appreciation_share`: Minimum appreciation share (default: 0.1)
- `max_appreciation_share`: Maximum appreciation share (default: 0.5)
- `tiered_appreciation_thresholds`: Thresholds for tiered appreciation sharing (default: [0.2, 0.5, 1.0])
- `tiered_appreciation_shares`: Shares for tiered appreciation sharing (default: [0.1, 0.2, 0.3, 0.4])

#### Default Parameters
- `base_default_rate`: Base annual default probability (default: 0.01)
- `recovery_rate`: Recovery rate in case of default (default: 0.8)
- `foreclosure_cost`: Cost of foreclosure as percentage of property value (default: 0.1)
- `foreclosure_time`: Time to complete foreclosure in years (default: 1)

### Enhanced Exit Simulator Parameters

#### Behavioral Model Parameters
- `refinance_interest_rate_sensitivity`: How sensitive refinancing is to interest rate changes (default: 2.0)
- `sale_appreciation_sensitivity`: How sensitive sales are to appreciation (default: 1.5)
- `life_event_probability`: Annual probability of life events triggering exits (default: 0.05)
- `behavioral_correlation`: Correlation in exit decisions (herd behavior) (default: 0.3)

#### Economic Model Parameters
- `recession_default_multiplier`: How much recessions increase defaults (default: 2.5)
- `inflation_refinance_multiplier`: How inflation affects refinancing (default: 1.8)
- `employment_sensitivity`: How employment affects exits (default: 1.2)
- `migration_sensitivity`: How population migration affects exits (default: 0.8)

#### Regulatory and Tax Parameters
- `regulatory_compliance_cost`: Compliance cost as percentage of loan (default: 0.01)
- `tax_efficiency_factor`: Tax efficiency factor (1.0 = fully efficient) (default: 0.9)

#### Cohort Analysis Parameters
- `vintage_segmentation`: Whether to segment by vintage (default: true)
- `ltv_segmentation`: Whether to segment by LTV (default: true)
- `zone_segmentation`: Whether to segment by zone (default: true)

#### Risk Metrics Parameters
- `var_confidence_level`: Confidence level for Value-at-Risk (default: 0.95)
- `stress_test_severity`: Severity of stress tests (0-1) (default: 0.3)
- `tail_risk_threshold`: Threshold for tail risk events (default: 0.05)

#### Machine Learning Parameters
- `use_ml_models`: Whether to use machine learning models (default: true)
- `feature_importance_threshold`: Threshold for important features (default: 0.05)
- `anomaly_detection_threshold`: Standard deviations for anomaly detection (default: 3.0)

## Usage Example

### Base Exit Simulator

```python
from src.exit_simulator.exit_simulator import simulate_exits, get_exit_summary

# Simulate exits
await simulate_exits(context)

# Access exit simulation results
exits = context.exits
exit_stats = context.exit_stats
exit_visualization = context.exit_visualization

# Get exit summary
summary = await get_exit_summary(context)
```

### Enhanced Exit Simulator

```python
from src.exit_simulator.enhanced_exit_simulator import simulate_enhanced_exits, get_enhanced_exit_summary

# Simulate enhanced exits
await simulate_enhanced_exits(context)

# Access enhanced exit simulation results
enhanced_exits = context.enhanced_exits
enhanced_exit_stats = context.enhanced_exit_stats
enhanced_exit_visualization = context.enhanced_exit_visualization

# Get enhanced exit summary
enhanced_summary = await get_enhanced_exit_summary(context)

# Access cohort analysis
cohort_analysis = enhanced_exit_stats["cohort_analysis"]
vintage_stats = cohort_analysis["vintage"]
ltv_stats = cohort_analysis["ltv"]
zone_stats = cohort_analysis["zone"]

# Access risk metrics
risk_metrics = enhanced_exit_stats["risk_metrics"]
var = risk_metrics["value_at_risk"]
cvar = risk_metrics["conditional_var"]
stress_test_roi = risk_metrics["stress_test_roi"]

# Access machine learning insights
ml_insights = enhanced_exit_stats["ml_insights"]
feature_importances = ml_insights["exit_timing_feature_importances"]
clusters = ml_insights["exit_clusters"]
anomalies = ml_insights["anomalies"]
```

## API Endpoints

### Base Exit Simulator

The base Exit Simulator provides the following API endpoints:

- `GET /api/v1/simulations/{simulation_id}/exits`: Get exit simulation results
- `GET /api/v1/simulations/{simulation_id}/exits/visualization`: Get visualization data for exits
- `GET /api/v1/simulations/{simulation_id}/exits/statistics`: Get statistics for exits
- `POST /api/v1/simulations/{simulation_id}/exits/loan-exit`: Calculate exit value for a specific loan
- `POST /api/v1/simulations/{simulation_id}/exits/scenario`: Run an exit scenario with custom parameters

### Enhanced Exit Simulator

The Enhanced Exit Simulator provides the following additional API endpoints:

- `GET /api/v1/simulations/{simulation_id}/enhanced-exits`: Get enhanced exit simulation results
- `GET /api/v1/simulations/{simulation_id}/enhanced-exits/visualization`: Get enhanced visualization data
- `GET /api/v1/simulations/{simulation_id}/enhanced-exits/statistics`: Get enhanced statistics
- `POST /api/v1/simulations/{simulation_id}/enhanced-exits/scenario`: Run an enhanced exit scenario

## Exit Types

The Exit Simulator models the following exit types:

### 1. Sale
When a homeowner sells their property. The fund receives:
- Original loan amount
- Appreciation share based on the agreed terms

### 2. Refinance
When a homeowner refinances their loan with another lender. The fund receives:
- Original loan amount
- Appreciation share based on the agreed terms

### 3. Default
When a homeowner is unable to meet their obligations. The fund receives:
- Recovery value after foreclosure costs
- No appreciation share

### 4. Term Completion
When a loan reaches its full term. The fund receives:
- Original loan amount
- Appreciation share based on the agreed terms

## Visualization

### Base Exit Simulator

The base Exit Simulator provides the following visualizations:

1. **Exit Timing Distribution**: Histogram of when exits occur
2. **Exit Type Distribution**: Breakdown of exit types
3. **Cumulative Exits**: Cumulative exits over time
4. **Return Distribution**: Distribution of returns by exit type
5. **Exit Value by Year**: Exit values over time
6. **Exit Count by Year**: Exit counts over time

### Enhanced Exit Simulator

The Enhanced Exit Simulator provides additional visualizations:

1. **Cohort Visualizations**:
   - Vintage ROI Chart: Performance by origination year
   - LTV ROI Chart: Performance by loan-to-value ratio
   - Zone ROI Chart: Performance by geographic zone
   - Exit Type by Cohort: Distribution of exit types by cohort

2. **Risk Visualizations**:
   - ROI Distribution Chart: Detailed distribution of returns
   - VaR Chart: Value-at-Risk visualization
   - Stress Test Chart: Performance under stressed scenarios

3. **Machine Learning Visualizations**:
   - Feature Importance Chart: Importance of different factors
   - Cluster Chart: Visualization of exit clusters
   - Anomaly Chart: Visualization of anomalous exits

4. **Economic Visualizations**:
   - Economic Indicators Chart: GDP, inflation, employment over time
   - Economic Adjustments Chart: Impact of economic factors on exits

5. **Geospatial Visualizations**:
   - Exit Map: Geographic distribution of exits
   - Performance Map: ROI by location

6. **Comparative Visualizations**:
   - Exit Timing Comparison: Actual vs. expected exit timing
   - Performance Comparison: Actual vs. expected returns
