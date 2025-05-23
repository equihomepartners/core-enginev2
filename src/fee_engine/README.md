# Fee Engine Module

The Fee Engine module is responsible for calculating various fees and expenses associated with the fund, including management fees, origination fees, fund expenses, acquisition fees, disposition fees, and setup costs.

## Overview

The Fee Engine calculates the following types of fees:

1. **Management Fees**: Calculated based on committed capital, invested capital, or net asset value (NAV).
2. **Origination Fees**: Charged when a loan is originated.
3. **Fund Expenses**: Both fixed and variable expenses that grow over time.
4. **Acquisition Fees**: Charged when a property is acquired.
5. **Disposition Fees**: Charged when a property is sold.
6. **Setup Costs**: One-time costs for setting up the fund.

## Architecture

The Fee Engine consists of the following components:

- `FeeEngine` class: The main class that calculates fees and expenses.
- `calculate_fees` function: The entry point for the orchestrator.

## Integration Points

The Fee Engine integrates with the following components:

- **Simulation Context**: Retrieves loan data, exits, and price paths.
- **WebSocket Manager**: Sends progress updates and intermediate results.
- **Orchestrator**: Registers the module for execution.

## Data Flow

1. The Fee Engine receives the simulation context from the orchestrator.
2. It calculates various fees based on the loans, exits, and fund parameters.
3. It generates visualization data for the frontend.
4. It returns the fee calculation results to the orchestrator.
5. The results are stored in the simulation context for use by downstream modules.

## Configuration Parameters

The Fee Engine uses the following configuration parameters:

- `management_fee_rate`: Management fee rate (0-1).
- `management_fee_basis`: Basis for management fee calculation (committed_capital, invested_capital, net_asset_value).
- `fee_engine.origination_fee_rate`: Origination fee rate (0-1).
- `fee_engine.annual_fund_expenses`: Annual fund expenses as percentage of fund size (0-1).
- `fee_engine.fixed_annual_expenses`: Fixed annual expenses in dollars.
- `fee_engine.management_fee_schedule`: Schedule of management fee rates by year.
- `fee_engine.expense_growth_rate`: Annual growth rate for expenses (0-1).
- `fee_engine.acquisition_fee_rate`: Acquisition fee rate (0-1).
- `fee_engine.disposition_fee_rate`: Disposition fee rate (0-1).
- `fee_engine.setup_costs`: One-time setup costs in dollars.

## Output

The Fee Engine produces the following outputs:

- `management_fees`: Management fees by year.
- `origination_fees`: Origination fees by loan.
- `fund_expenses`: Fund expenses by year.
- `acquisition_fees`: Acquisition fees by loan.
- `disposition_fees`: Disposition fees by loan exit.
- `setup_costs`: One-time setup costs.
- `total_fees`: Total fees by category.
- `fee_impact`: Impact of fees on fund performance.
- `visualization`: Visualization data for the frontend.

## Visualization

The Fee Engine generates the following visualization data:

- `fee_breakdown_chart`: Breakdown of fees by category.
- `fees_by_year_chart`: Fees by year.
- `fee_impact_chart`: Impact of fees on fund performance.
- `fee_table`: Tabular data of fees by year.

## Error Handling

The Fee Engine includes comprehensive error handling:

- Logs errors with detailed information.
- Sends error messages to the frontend via WebSocket.
- Supports cancellation of fee calculation.

## Performance Considerations

- The Fee Engine is designed to be efficient and scalable.
- It uses vectorized operations where possible.
- It checks for cancellation after each major calculation step.

## Future Enhancements

Potential future enhancements for the Fee Engine include:

1. Support for more complex fee structures.
2. Integration with the waterfall engine for carried interest calculations.
3. More detailed fee impact analysis.
4. Support for custom fee schedules.
