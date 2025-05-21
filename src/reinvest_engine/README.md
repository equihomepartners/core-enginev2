# Reinvestment Engine

The Reinvestment Engine is a critical component of the EQU IHOME SIM ENGINE v2 that manages the reinvestment of capital during the fund's reinvestment period. It tracks capital that becomes available for reinvestment when loans exit the portfolio, applies different reinvestment strategies, and coordinates with the Capital Allocator and Loan Generator to create new loans.

## Functionality

The Reinvestment Engine provides the following functionality:

1. **Capital Reinvestment Management**:
   - Tracks and manages capital that becomes available for reinvestment when loans exit the portfolio
   - Ensures reinvestment only occurs during the defined reinvestment period
   - Maintains reinvestment constraints and rules
   - Optionally maintains a cash reserve for future reinvestment

2. **Reinvestment Strategy Implementation**:
   - Applies different reinvestment strategies based on configuration
   - Rebalances the portfolio to maintain target zone allocations
   - Coordinates with the Capital Allocator to determine where to reinvest capital
   - Works with the Loan Generator to create new loans for reinvestment

3. **Tracking and Visualization**:
   - Tracks reinvestment activity over time
   - Provides statistics on reinvestment performance
   - Generates visualization data for reinvestment activity
   - Reports progress through WebSocket for frontend updates

## Reinvestment Strategies

The Reinvestment Engine supports the following strategies:

1. **Maintain Allocation** (`maintain_allocation`):
   - Reinvests capital to maintain the current zone allocation
   - Uses the current portfolio composition as the target allocation
   - Suitable for maintaining the status quo

2. **Rebalance** (`rebalance`):
   - Reinvests capital to rebalance the portfolio toward target allocations
   - Uses the target allocations from the configuration
   - Suitable for correcting allocation drift over time

3. **Opportunistic** (`opportunistic`):
   - Reinvests capital in zones with the highest expected returns
   - Uses recent price appreciation as a proxy for expected returns
   - Suitable for maximizing returns in a changing market

4. **Custom** (`custom`):
   - Applies custom preference multipliers to the target allocations
   - Allows fine-tuning of allocations based on user preferences
   - Suitable for implementing custom investment strategies

## Dynamic Allocation

The Reinvestment Engine can optionally use dynamic allocation, which adjusts the target allocations based on recent performance:

- Tracks the performance of loans in each zone
- Calculates performance-based adjustments to allocations
- Applies these adjustments to the target allocations
- Limits adjustments to a configurable maximum

## Cash Reserve Management

The Reinvestment Engine can optionally maintain a cash reserve:

- Holds a portion of exit proceeds in a cash reserve
- Reinvests from the cash reserve when it exceeds the target
- Maintains the cash reserve within configurable limits
- Provides a buffer for future reinvestment opportunities

## Configuration Parameters

The Reinvestment Engine is controlled by the following parameters in the `reinvestment_engine` section of the simulation configuration:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `reinvestment_strategy` | string | Strategy for reinvesting capital | `"rebalance"` |
| `min_reinvestment_amount` | number | Minimum amount to trigger reinvestment | `100000` |
| `reinvestment_frequency` | string | How often to check for reinvestment opportunities | `"quarterly"` |
| `reinvestment_delay` | number | Time delay in months between exit and reinvestment | `1` |
| `reinvestment_batch_size` | integer | Maximum number of loans to generate in one batch | `50` |
| `zone_preference_multipliers` | object | Multipliers for zone preferences during reinvestment | `{"green": 1.0, "orange": 1.0, "red": 1.0}` |
| `opportunistic_threshold` | number | Appreciation threshold for opportunistic reinvestment | `0.05` |
| `rebalance_threshold` | number | Allocation gap threshold to trigger rebalancing | `0.05` |
| `reinvestment_ltv_adjustment` | number | Adjustment to LTV for reinvestment loans | `0` |
| `reinvestment_size_adjustment` | number | Adjustment to loan size for reinvestment loans | `0` |
| `enable_dynamic_allocation` | boolean | Whether to dynamically adjust allocations based on performance | `false` |
| `performance_lookback_period` | number | Lookback period in months for performance-based allocation | `12` |
| `performance_weight` | number | Weight of performance in dynamic allocation | `0.5` |
| `max_allocation_adjustment` | number | Maximum adjustment to allocation based on performance | `0.2` |
| `reinvestment_tracking_granularity` | string | Granularity for tracking reinvestment activity | `"monthly"` |
| `enable_cash_reserve` | boolean | Whether to maintain a cash reserve | `false` |
| `cash_reserve_target` | number | Target cash reserve as percentage of fund size | `0.05` |
| `cash_reserve_min` | number | Minimum cash reserve as percentage of fund size | `0.02` |
| `cash_reserve_max` | number | Maximum cash reserve as percentage of fund size | `0.1` |

## API Endpoints

The Reinvestment Engine exposes the following API endpoints:

### Get Reinvestment Data

```
GET /api/v1/simulations/{simulation_id}/reinvestment
```

Returns reinvestment data for a simulation, including events, summary, and visualization data.

### Manual Reinvestment

```
POST /api/v1/simulations/{simulation_id}/reinvestment
```

Manually triggers a reinvestment event with the specified parameters.

Request body:
```json
{
  "amount": 1000000,
  "year": 2.5,
  "month": 6,
  "strategy": "rebalance",
  "source": "exit",
  "source_details": {},
  "zone_preference_multipliers": {
    "green": 1.2,
    "orange": 1.0,
    "red": 0.8
  },
  "enable_dynamic_allocation": true
}
```

## Visualization

The Reinvestment Engine generates the following visualization data:

1. **Reinvestment Timeline**:
   - Shows the timeline of reinvestment events
   - Includes cumulative reinvestment amount

2. **Reinvestment by Zone Chart**:
   - Shows the distribution of reinvestment by zone
   - Includes percentage of total reinvestment

3. **Reinvestment by Year Chart**:
   - Shows the distribution of reinvestment by year
   - Includes number of reinvestment events

4. **Cash Reserve Chart**:
   - Shows the cash reserve over time
   - Includes target, minimum, and maximum levels

5. **Allocation Comparison Chart**:
   - Compares target and actual allocations
   - Shows the gap between target and actual

6. **Reinvestment Summary Table**:
   - Provides a summary of reinvestment activity by year
   - Includes number of events, loans, and zone distribution

7. **Reinvestment Events Table**:
   - Lists all reinvestment events
   - Includes details such as amount, strategy, and number of loans

## Risk Metrics

The Reinvestment Engine calculates and tracks the impact of reinvestment on portfolio risk:

1. **Portfolio Risk Metrics**:
   - **Zone Distribution**: Tracks the distribution of loans by zone
   - **Average LTV**: Calculates the weighted average LTV of the portfolio
   - **Concentration Risk**: Measures portfolio concentration using HHI and top N metrics
   - **Risk Score**: Combines multiple risk factors into a single score

2. **Risk Impact Metrics**:
   - **Zone Distribution Change**: Measures how reinvestment changes zone allocations
   - **LTV Change**: Tracks the impact of reinvestment on portfolio LTV
   - **Concentration Risk Change**: Measures how reinvestment affects concentration
   - **Risk Score Change**: Quantifies the overall risk impact of reinvestment
   - **Diversification Impact**: Measures how reinvestment affects portfolio diversification
   - **Risk-Adjusted Return Impact**: Estimates the impact on risk-adjusted returns

3. **Risk Visualization**:
   - **Before/After Comparisons**: Shows portfolio metrics before and after reinvestment
   - **Risk Impact Charts**: Visualizes the impact of reinvestment on various risk metrics
   - **Risk Trend Analysis**: Tracks how risk metrics evolve over multiple reinvestment events

## Integration with Other Modules

The Reinvestment Engine integrates with the following modules:

1. **Exit Simulator**:
   - Receives capital from exited loans
   - Uses exit timing to determine reinvestment timing

2. **Capital Allocator**:
   - Uses target allocations to determine zone allocations for reinvestment
   - Applies allocation strategies to reinvestment decisions

3. **Loan Generator**:
   - Creates new loans for reinvestment
   - Applies loan parameters to reinvestment loans

4. **Risk Metrics**:
   - Calculates risk metrics before and after reinvestment
   - Tracks the impact of reinvestment on portfolio risk

5. **Orchestrator**:
   - Registers with the Orchestrator to be included in the simulation sequence
   - Executes after the Exit Simulator and before the Waterfall Engine

## WebSocket Integration

The Reinvestment Engine reports progress through WebSocket for frontend updates:

1. **Progress Updates**:
   - Reports progress at key stages of the reinvestment process
   - Provides percentage completion and status messages

2. **Intermediate Results**:
   - Sends intermediate results for frontend visualization
   - Includes reinvestment events and statistics

3. **Error Reporting**:
   - Reports errors during the reinvestment process
   - Includes error messages and codes

## Example Usage

```python
# Get simulation context
context = simulations[simulation_id].get("context")

# Run reinvestment engine
await reinvest_capital(context)

# Get reinvestment statistics
reinvestment_summary = calculate_reinvestment_statistics(context)

# Generate visualization data
visualization = generate_reinvestment_visualization(context)
```
