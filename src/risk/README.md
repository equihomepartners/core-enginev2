# Risk Metrics Module

The Risk Metrics module calculates risk metrics for the EQU IHOME SIM ENGINE v2. It provides a comprehensive set of risk metrics, stress testing, and scenario analysis capabilities.

## Overview

The Risk Metrics module:

1. Collects existing metrics from other modules
2. Calculates additional metrics not covered by other modules
3. Standardizes and normalizes metrics for consistency
4. Provides comprehensive visualization of risk metrics
5. Implements stress testing and scenario analysis

## Key Features

- **Value at Risk (VaR)**: Calculates VaR at different confidence levels (95%, 99%)
- **Conditional Value at Risk (CVaR)**: Calculates CVaR at different confidence levels
- **Risk-Adjusted Return Metrics**: Calculates Sharpe Ratio, Sortino Ratio, Calmar Ratio, etc.
- **Drawdown Analysis**: Calculates Maximum Drawdown and related metrics
- **Market Metrics**: Calculates Beta, Alpha, Information Ratio, etc.
- **Concentration Metrics**: Calculates Herfindahl-Hirschman Index (HHI) and other concentration metrics
- **Stress Testing**: Applies shocks to key parameters and recalculates metrics
- **Scenario Analysis**: Calculates metrics under different scenarios
- **Sensitivity Analysis**: Analyzes sensitivity of metrics to changes in parameters
- **Visualization**: Provides comprehensive visualization of risk metrics

## Monte Carlo Integration

The Risk Metrics module is designed to work with both deterministic (single-path) simulations and Monte Carlo simulations:

### Deterministic Mode

In deterministic mode (when Monte Carlo is disabled or not available):

- Most metrics are calculated using analytic approximations or single-path data
- Metrics that absolutely require Monte Carlo simulation are marked as "requires MC" in the response
- Approximations are used where possible (e.g., analytic VaR formula)
- The simulation will not fail, but some metrics will be missing or approximated

### Monte Carlo Mode

When Monte Carlo simulation is enabled:

- All metrics are calculated using the full distribution of outcomes
- More accurate VaR, CVaR, and other distribution-dependent metrics are provided
- Additional metrics like hurdle-clear probability and MC convergence error become available
- Sensitivity analysis and tornado charts are more comprehensive

The module automatically detects whether Monte Carlo data is available and adapts its calculations accordingly. This ensures that the simulation will always run successfully, even if Monte Carlo is disabled, while providing the most accurate metrics possible given the available data.

## Architecture

The Risk Metrics module consists of the following components:

- **RiskMetricsCalculator**: Main class for calculating risk metrics
- **API Endpoints**: FastAPI endpoints for accessing risk metrics
- **Visualization**: Visualization data for risk metrics

## Integration with Other Modules

The Risk Metrics module integrates with the following modules:

- **Cashflow Aggregator**: Uses cashflow data to calculate return metrics
- **Price Path Simulator**: Uses price path data to calculate volatility metrics
- **Exit Simulator**: Uses exit data to calculate risk metrics
- **Reinvestment Engine**: Uses reinvestment data to calculate concentration metrics
- **Capital Allocator**: Uses allocation data to calculate zone concentration metrics

## API Endpoints

The Risk Metrics module provides the following API endpoints:

- `POST /risk/metrics/calculate`: Calculate risk metrics for a simulation
- `GET /risk/metrics/{simulation_id}`: Get risk metrics for a simulation
- `POST /risk/stress-test`: Run stress tests on a simulation
- `GET /risk/visualization/{simulation_id}`: Get risk visualization data for a simulation

## Configuration

The Risk Metrics module can be configured through the `risk_metrics` section in the simulation configuration:

```json
{
  "risk_metrics": {
    "var_confidence_level": 0.95,
    "risk_free_rate": 0.03,
    "benchmark_return": 0.07,
    "min_acceptable_return": 0.04,
    "tail_risk_threshold": 0.05,
    "monte_carlo_simulations": 1000,
    "enable_sensitivity_analysis": true,
    "sensitivity_parameters": [
      "interest_rate",
      "property_value_growth",
      "default_rate",
      "ltv_ratio"
    ],
    "stress_test_scenarios": [
      {
        "name": "mild_recession",
        "description": "Mild recession scenario",
        "property_value_shock": -0.1,
        "interest_rate_shock": 0.01,
        "default_rate_shock": 1.5,
        "liquidity_shock": 0.3
      },
      {
        "name": "severe_recession",
        "description": "Severe recession scenario",
        "property_value_shock": -0.3,
        "interest_rate_shock": 0.03,
        "default_rate_shock": 3,
        "liquidity_shock": 0.7
      },
      {
        "name": "financial_crisis",
        "description": "Financial crisis scenario",
        "property_value_shock": -0.5,
        "interest_rate_shock": 0.05,
        "default_rate_shock": 5,
        "liquidity_shock": 0.9
      }
    ]
  }
}
```

## Metrics Calculated

The Risk Metrics module calculates a comprehensive set of metrics organized into the following categories:

### Market/Price Metrics

| Metric | Deterministic (1 path) | Needs MC? | Pre-MC stand-in / note |
|--------|------------------------|-----------|-------------------------|
| σ (volatility) unit / zone / port | ✓ | — | Uses input σ or historical price series; no random draw needed |
| α idiosyncratic share | ✓ | — | Comes directly from TLS module data |
| β macro / β zone | ✓ | — | Deterministic factor loadings from TLS module |
| VaR-95 / VaR-99 | ✗ | Yes | Uses analytic log-normal VaR: VaR = N⁻¹(0.99)*σ*√T – μT. Flagged as "approximation" |
| CVaR | ✗ | Yes | Simple approximation provided; full calculation requires MC |

### Credit Metrics

| Metric | Deterministic (1 path) | Needs MC? | Pre-MC stand-in / note |
|--------|------------------------|-----------|-------------------------|
| Current LTV | ✓ | — | Direct calculation: principal / value |
| Stress-LTV | ✓ | — | Applies −20% price shock deterministically |
| Default probability unit / zone | ✓ | — | Comes from credit model inputs or TLS module |
| Portfolio default rate | ✓ | — | Exposure-weighted PD (analytic expectation) |

### Liquidity Metrics

| Metric | Deterministic (1 path) | Needs MC? | Pre-MC stand-in / note |
|--------|------------------------|-----------|-------------------------|
| Liquidity score | ✓ | — | Static parameter from TLS module |
| Expected exit lag | ✓ | — | Mean of Gamma (α, β) from parameters |
| WAL | ✓ | — | Deterministic exit months → WAL |
| CFaR (cash-flow-at-risk) | ✗ | Yes | Omitted until MC; analytic proxy not reliable |

### Leverage Metrics

| Metric | Deterministic (1 path) | Needs MC? | Pre-MC stand-in / note |
|--------|------------------------|-----------|-------------------------|
| NAV utilisation | ✓ | — | Exact from deterministic schedule |
| Interest-coverage | ✓ | — | Deterministic inflow/outflow |
| VaR uplift from leverage | ✗ | Yes | Deferred to MC (needs distribution) |

### Concentration Metrics

| Metric | Deterministic (1 path) | Needs MC? | Pre-MC stand-in / note |
|--------|------------------------|-----------|-------------------------|
| Zone exposure % | ✓ | — | Simple aggregation |
| Suburb exposure cap | ✓ | — | Simple calculation |
| Single-loan exposure | ✓ | — | Simple calculation |
| Herfindahl-Hirschman Index (HHI) | ✓ | — | Calculated for zones and suburbs |

### Performance/Return-Risk Metrics

| Metric | Deterministic (1 path) | Needs MC? | Pre-MC stand-in / note |
|--------|------------------------|-----------|-------------------------|
| Net-IRR point value | ✓ | — | XIRR of single path |
| Sharpe ratio | ✓ | — | Uses analytic σ or historical σ |
| Sortino | ✓ | — | Uses one-path downside calculation (approximation) |
| Hurdle-clear probability | ✗ | Yes | Set null; displays "requires MC" |
| Calmar Ratio | ✓ | — | Calculated from IRR and max drawdown |
| Information Ratio | ✓ | — | Calculated using benchmark return |
| Treynor Ratio | ✓ | — | Calculated using beta |
| Omega Ratio | ✓ | — | Calculated from return distribution |
| Kappa Ratio | ✓ | — | Calculated from return distribution |
| Gain-Loss Ratio | ✓ | — | Calculated from return distribution |

### Scenario/Stress Metrics

| Metric | Deterministic (1 path) | Needs MC? | Pre-MC stand-in / note |
|--------|------------------------|-----------|-------------------------|
| Price −10% impact | ✓ | — | Applies deterministic shock once |
| Rate +200 bp impact | ✓ | — | Re-runs deterministic engine with shifted rate parameter |
| PD +50% stress | ✓ | — | Re-runs deterministically |

### Model/Parameter Uncertainty

| Metric | Deterministic (1 path) | Needs MC? | Pre-MC stand-in / note |
|--------|------------------------|-----------|-------------------------|
| Tornado sensitivity | ✗ | Yes | Deferred until MC or scenario grid available |
| MC convergence error | ✗ | Yes | Not applicable pre-MC |

## Visualization

The Risk Metrics module provides the following visualization data:

- Risk-Return Scatter Plot
- VaR Histogram
- Drawdown Chart
- Stress Test Comparison Chart
- Sensitivity Charts
- Concentration Chart

## Usage

To use the Risk Metrics module, follow these steps:

1. Run a simulation
2. Call the `/risk/metrics/calculate` endpoint to calculate risk metrics
3. Retrieve the risk metrics using the `/risk/metrics/{simulation_id}` endpoint
4. Run stress tests using the `/risk/stress-test` endpoint
5. Retrieve visualization data using the `/risk/visualization/{simulation_id}` endpoint

## Example

```python
# Calculate risk metrics
response = await client.post(
    "/risk/metrics/calculate",
    json={"simulation_id": "sim-123"},
)

# Get risk metrics
metrics = await client.get("/risk/metrics/sim-123")

# Run stress tests
response = await client.post(
    "/risk/stress-test",
    json={
        "simulation_id": "sim-123",
        "scenarios": [
            {
                "name": "recession",
                "property_value_shock": -0.2,
                "interest_rate_shock": 0.02,
                "default_rate_shock": 2.0,
                "liquidity_shock": 0.5,
            }
        ],
    },
)

# Get visualization data
visualization = await client.get("/risk/visualization/sim-123")
```
