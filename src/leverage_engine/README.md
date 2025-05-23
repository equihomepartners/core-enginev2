# Leverage Engine

The Leverage Engine module manages debt facilities for the EQU IHOME SIM ENGINE v2. It models different types of debt facilities, calculates interest and fees, enforces borrowing base tests, and tracks leverage metrics.

## Overview

The Leverage Engine is responsible for:

1. **Debt Facility Management**: Creating and managing different types of debt facilities (NAV lines, subscription lines)
2. **Borrowing Base Tests**: Enforcing borrowing base tests and covenant compliance
3. **Interest Calculation**: Computing interest expenses on borrowed amounts
4. **Leverage Optimization**: Determining optimal debt usage given constraints
5. **Stress Testing**: Modeling impact of interest rate shocks, NAV shocks, and liquidity shocks
6. **Risk Assessment**: Evaluating the impact of combined shocks on fund performance
7. **Visualization**: Generating comprehensive visualization data for leverage metrics and stress test results

## Debt Facility Types

The Leverage Engine supports the following types of debt facilities:

### NAV Line (Green Sleeve)

A NAV line is secured by the fund's net asset value. Key characteristics:

- Advance rate applied to NAV (typically 50-75%)
- Floating interest rate (typically SOFR + spread)
- Commitment fee on undrawn amounts
- Borrowing base tests based on portfolio quality
- Covenants related to portfolio performance

### Subscription Line (Ramp Line)

A subscription line is secured by investor commitments. Key characteristics:

- Limited to a percentage of uncalled commitments
- Short-term in nature (typically 1-2 years)
- Used for bridging capital calls
- Higher interest rate than NAV lines
- Commitment fee on undrawn amounts

## Configuration Parameters

The Leverage Engine is configured through the following parameters in the simulation configuration:

```json
{
  "leverage": {
    "enabled": true,
    "green_sleeve": {
      "enabled": true,
      "max_mult": 1.5,
      "spread_bps": 275,
      "commitment_fee_bps": 50,
      "advance_rate": 0.75,
      "min_dscr": 1.2,
      "max_ltv": 0.65
    },
    "ramp_line": {
      "enabled": true,
      "limit_pct_commit": 0.15,
      "spread_bps": 300,
      "commitment_fee_bps": 50,
      "draw_period_months": 24
    },
    "interest_rate_model": {
      "base_rate_initial": 0.0425,
      "volatility": 0.01,
      "mean_reversion": 0.1,
      "long_term_mean": 0.04
    },
    "optimization": {
      "enabled": true,
      "target_leverage": 0.5,
      "max_leverage": 0.65,
      "deleveraging_threshold": 0.7
    }
  }
}
```

## Key Metrics

The Leverage Engine tracks the following key metrics:

1. **Leverage Ratio**: Total debt / NAV
2. **Debt Service Coverage Ratio (DSCR)**: Cash flow / Debt service
3. **Loan-to-Value Ratio (LTV)**: Debt / Portfolio value
4. **Interest Coverage Ratio**: EBITDA / Interest expense
5. **Weighted Average Cost of Debt**: Weighted average interest rate across facilities
6. **Debt Maturity Profile**: Distribution of debt maturities

## Integration with Other Modules

The Leverage Engine integrates with the following modules:

1. **Capital Allocator**: The leverage engine provides additional capital for deployment
2. **Loan Generator**: Leveraged capital is used to generate more loans
3. **Exit Simulator**: Exits provide cash for debt repayment
4. **Reinvestment Engine**: Reinvestment decisions consider leverage constraints
5. **Cashflow Aggregator**: Debt service payments impact fund cash flows
6. **Waterfall Engine**: Debt is senior to equity in the distribution waterfall
7. **Risk Metrics**: Leverage affects risk calculations like VaR

## Stress Testing

The Leverage Engine includes comprehensive stress testing capabilities to assess the resilience of the fund's leverage structure under adverse conditions:

1. **Interest Rate Shock**: Tests the impact of a sudden increase in interest rates on debt service coverage
2. **NAV Shock**: Tests the impact of a decline in NAV on leverage ratios and covenant compliance
3. **Liquidity Shock**: Tests the impact of reduced liquidity on the fund's ability to service debt
4. **Combined Shock**: Tests the impact of multiple simultaneous shocks on overall fund stability

Stress test parameters are configurable through the `stress_testing` section of the leverage configuration:

```json
"stress_testing": {
  "enabled": true,
  "interest_rate_shock": 0.02,  // 200 basis points
  "nav_shock": 0.2,             // 20% decline
  "liquidity_shock": 0.5        // 50% reduction
}
```

## Leverage Optimization

The Leverage Engine includes an optimization module that dynamically adjusts leverage based on target ratios and market conditions:

1. **Target Leverage**: Maintains leverage at the target level by drawing or repaying debt
2. **Deleveraging**: Automatically deleverages when leverage exceeds threshold levels
3. **Facility Preference**: Optimizes which facilities to draw from or repay based on cost and flexibility
4. **Cash Buffer**: Maintains a minimum cash buffer for debt service

Optimization parameters are configurable through the `optimization` section of the leverage configuration:

```json
"optimization": {
  "enabled": true,
  "target_leverage": 0.5,       // 50% target leverage ratio
  "max_leverage": 0.65,         // 65% maximum leverage ratio
  "deleveraging_threshold": 0.7, // Trigger deleveraging at 70%
  "min_cash_buffer": 1.5        // 1.5x debt service coverage
}
```

## Visualization

The Leverage Engine provides the following visualizations:

1. **Leverage Utilization**: How much of available facilities is being used
2. **Interest Expenses**: Interest costs over time
3. **Covenant Compliance**: Tracking metrics vs. covenant thresholds
4. **Debt Structure**: Breakdown of debt by facility type
5. **Leverage Impact**: How leverage affects fund returns
6. **Stress Test Results**: Visual representation of stress test outcomes
7. **Optimization Activity**: Timeline of optimization actions taken

## API Endpoints

The Leverage Engine exposes the following API endpoints:

1. `GET /simulations/{simulation_id}/leverage`: Get comprehensive leverage data including facilities, metrics, visualization, and stress test results
2. `GET /simulations/{simulation_id}/leverage/facilities`: Get detailed information about debt facilities
3. `GET /simulations/{simulation_id}/leverage/events`: Get leverage events (draws, repayments, interest payments, fees)
4. `GET /simulations/{simulation_id}/leverage/metrics`: Get leverage metrics and ratios

## Implementation Details

The Leverage Engine is implemented in the following files:

1. `src/leverage_engine/leverage_manager.py`: Main implementation with all core functionality
2. `src/api/routers/portfolio.py`: API endpoints for leverage data

Key implementation features:

1. **Comprehensive Stress Testing**: Multiple stress test scenarios with detailed results
2. **Dynamic Optimization**: Intelligent leverage optimization based on configurable parameters
3. **Robust Visualization**: Rich visualization data for frontend display
4. **WebSocket Integration**: Real-time progress updates and intermediate results
5. **Detailed Logging**: Comprehensive logging for debugging and monitoring

The implementation follows the module implementation rules defined in the implementation plan, with no redundant files or schemas.
