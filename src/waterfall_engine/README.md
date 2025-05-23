# Waterfall Engine

The Waterfall Engine is a critical component of the EQU IHOME SIM ENGINE v2 that calculates the distribution waterfall for fund cashflows. It handles the allocation of profits between Limited Partners (LPs) and the General Partner (GP) according to the fund's waterfall structure.

## Functionality

The Waterfall Engine provides the following functionality:

- **European Waterfall**: Calculates distributions based on the whole-fund approach, where all capital must be returned before any carried interest is paid.
- **American Waterfall**: Calculates distributions on a deal-by-deal basis, where carried interest can be paid on profitable deals even if other deals are still outstanding.
- **Hurdle Rate Calculation**: Applies the preferred return (hurdle rate) to LP capital before GP carried interest.
- **Catch-up Provisions**: Implements GP catch-up mechanisms to achieve target profit splits.
- **Carried Interest Calculation**: Calculates the GP's share of profits above the hurdle rate.
- **Clawback Handling**: Ensures that the GP does not receive more carried interest than entitled over the fund's life.
- **Multi-tier Waterfall Support**: Supports complex waterfall structures with multiple hurdle rates and carried interest tiers.
- **Visualization**: Generates comprehensive visualization data for waterfall distributions.

## Module Structure

The Waterfall Engine consists of the following components:

- `WaterfallEngine` class: The main class that calculates waterfall distributions.
- `WaterfallTier` enum: Defines the tiers in the waterfall distribution.
- `WaterfallStructure` enum: Defines the waterfall structure types (European or American).
- `calculate_waterfall` function: The entry point for the orchestrator.

## Integration Points

The Waterfall Engine integrates with the following components:

- **Simulation Context**: Retrieves cashflow data and fund parameters.
- **WebSocket Manager**: Sends progress updates and intermediate results.
- **Orchestrator**: Registers the module for execution.

## Data Flow

### Inputs

The Waterfall Engine takes the following inputs:

- **Fund-level Cashflows**: For European waterfall calculations.
- **Loan-level Cashflows**: For American waterfall calculations.
- **Fund Parameters**: Fund size, term, hurdle rate, carried interest rate, etc.
- **Waterfall Structure**: European or American.
- **Catch-up Rate**: Rate for GP catch-up calculations.
- **Clawback Parameters**: Threshold and enabling flag.

### Outputs

The Waterfall Engine produces the following outputs:

- **Tier Cashflows**: Cashflows for each tier of the waterfall.
- **LP Distributions**: Distributions to Limited Partners.
- **GP Distributions**: Distributions to the General Partner.
- **Clawback Amount**: Amount to be clawed back from the GP, if any.
- **Visualization Data**: Data for visualizing the waterfall distribution.

## Visualization

The Waterfall Engine generates the following visualization data:

- **Waterfall Chart**: Breakdown of distributions by tier.
- **Distribution by Year Chart**: Distributions over time.
- **Tier Allocation Chart**: Allocation of distributions by tier.
- **Stakeholder Allocation Chart**: Allocation between LP and GP.

## Error Handling

The Waterfall Engine includes comprehensive error handling:

- Logs errors with detailed information.
- Sends error messages to the frontend via WebSocket.
- Supports cancellation of waterfall calculation.

## Performance Considerations

- The Waterfall Engine is designed to be efficient and scalable.
- It handles large numbers of loans for American waterfall calculations.
- It checks for cancellation after each major calculation step.

## Future Enhancements

Potential future enhancements for the Waterfall Engine include:

1. Support for more complex waterfall structures with multiple tiers.
2. Integration with the tranche manager for tranche-specific waterfalls.
3. More detailed visualization options.
4. Support for custom waterfall rules.
5. Performance optimizations for large portfolios.

## Usage Example

```python
from src.waterfall_engine import calculate_waterfall
from src.engine.simulation_context import SimulationContext

# Create simulation context
context = SimulationContext(...)

# Calculate waterfall distributions
await calculate_waterfall(context)

# Access waterfall results
waterfall = context.waterfall
distributions = waterfall["distributions"]
lp_distributions = waterfall["lp_distributions"]
gp_distributions = waterfall["gp_distributions"]
```
