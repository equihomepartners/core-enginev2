# Cashflow Aggregator Module

## Overview

The Cashflow Aggregator module is responsible for aggregating cashflows from various sources, including loans, exits, fees, and leverage, and providing a comprehensive view of the fund's cashflow over time.

This module is designed to work with the EQU IHOME product, which is a 10-year no-payment home-equity advance with the following key characteristics:
- No monthly payments
- 5% simple interest, capitalized to exit
- 3% origination fee
- Appreciation share pro-rata to LTV

## Key Features

### Core Functionality
- **Loan-Level Cashflow Calculation**: Calculates cashflows for each loan, including origination and exit cashflows.
- **Fund-Level Cashflow Aggregation**: Aggregates loan-level cashflows and adds fund-level cashflows like capital calls, management fees, and distributions.
- **Stakeholder Cashflow Calculation**: Calculates cashflows for different stakeholders (LPs and GPs).
- **Visualization Support**: Generates visualization data for cashflows, including waterfall charts, time series charts, and tables.
- **WebSocket Integration**: Provides real-time progress updates and intermediate results.
- **Error Handling**: Comprehensive error handling with detailed error messages.
- **Cancellation Support**: Supports cancellation of long-running calculations.

### Enhanced Features
- **Parallel Processing**: Improved performance for large loan portfolios using multi-core processing.
- **Daily Cashflow Granularity**: More detailed time-based analysis with daily granularity.
- **Scenario Analysis**: Compare different scenarios and their impact on cashflows.
- **Sensitivity Analysis**: Analyze the impact of parameter variations on key metrics.
- **Cashflow Metrics Calculation**: Comprehensive metrics including IRR, MOIC, TVPI, DPI, RVPI, etc.
- **Waterfall Integration**: Integration with the waterfall engine for distribution calculations.
- **Tax Impact Analysis**: Analyze the impact of taxes on cashflows and returns.
- **Reinvestment Modeling**: Model the impact of reinvesting cashflows.
- **Liquidity Analysis**: Analyze the fund's liquidity position over time.
- **Enhanced Visualization Options**: Additional visualization types including heatmaps and Sankey diagrams.
- **Export Capabilities**: Export cashflow data to various formats.

## Module Structure

- `cashflow_aggregator.py`: Main implementation of the cashflow aggregator.
- `__init__.py`: Module initialization and exports.

## Usage

### Using the Aggregate Function

```python
from src.cashflow_aggregator import aggregate_cashflows
from src.engine.simulation_context import SimulationContext

# Create simulation context
context = SimulationContext(...)

# Aggregate cashflows
await aggregate_cashflows(context)

# Access cashflow results
cashflows = context.cashflows
```

### Using the CashflowAggregator Class

```python
from src.cashflow_aggregator.cashflow_aggregator import CashflowAggregator
from src.engine.simulation_context import SimulationContext

# Create simulation context
context = SimulationContext(...)

# Create cashflow aggregator
aggregator = CashflowAggregator(context)

# Run the cashflow aggregator
aggregator.run()

# Access cashflow results
cashflows = context.cashflows

# Access metrics
metrics = cashflows["metrics"]
fund_level_metrics = metrics["fund_level_metrics"]
irr = fund_level_metrics["irr"]
tvpi = fund_level_metrics["tvpi"]
```

## Cashflow Types

### Loan-Level Cashflows

- **Origination Cashflows**:
  - Loan amount (negative cashflow)
  - Origination fee (positive cashflow)

- **Exit Cashflows**:
  - Principal repayment (positive cashflow)
  - Accrued interest (positive cashflow)
  - Appreciation share (positive cashflow)

### Fund-Level Cashflows

- **Capital Calls**: Capital drawn from investors (negative cashflow)
- **Loan Investments**: Money invested in loans (negative cashflow)
- **Origination Fees**: Fees earned when originating loans (positive cashflow)
- **Principal Repayments**: Loan principal repaid at exit (positive cashflow)
- **Interest Income**: Accrued interest paid at exit (positive cashflow)
- **Appreciation Share**: Share of property appreciation at exit (positive cashflow)
- **Management Fees**: Fees paid to the fund manager (negative cashflow)
- **Fund Expenses**: Operating expenses of the fund (negative cashflow)
- **Leverage Draws/Repayments/Interest**: Cashflows related to leverage facilities
- **Distributions**: Cash distributed to investors (negative cashflow)

### Stakeholder Cashflows

- **LP Cashflows**: Capital calls and distributions for Limited Partners
- **GP Cashflows**: Capital calls, management fees, origination fees, carried interest, and distributions for General Partners

## Visualization Data

### Basic Visualizations
- **Cashflow Waterfall Chart**: Shows the contribution of each cashflow category to the total cashflow.
- **Cashflow by Year Chart**: Shows inflows, outflows, and net cashflow by year.
- **Cumulative Cashflow Chart**: Shows the cumulative cashflow over time.
- **Cashflow Table**: Detailed table of all cashflow categories by year.

### Enhanced Visualizations
- **Cashflow Heatmap**: Shows cashflows by year and month with color intensity representing amount.
- **Cashflow Sankey Diagram**: Shows the flow of cashflows between different categories.
- **Scenario Comparison Chart**: Compares key metrics across different scenarios.

## Metrics

The cashflow aggregator calculates the following metrics:

### Fund-Level Metrics
- **IRR (Internal Rate of Return)**: The annualized effective compounded return rate.
- **MOIC (Multiple on Invested Capital)**: The ratio of total returns to total investments.
- **TVPI (Total Value to Paid-In)**: The ratio of total value (distributions + NAV) to paid-in capital.
- **DPI (Distributions to Paid-In)**: The ratio of distributions to paid-in capital.
- **RVPI (Residual Value to Paid-In)**: The ratio of NAV to paid-in capital.
- **Payback Period**: The time required to recover the initial investment.
- **Cash-on-Cash Return**: The ratio of annual cashflow to initial investment.
- **NPV (Net Present Value)**: The present value of future cashflows minus the initial investment.
- **Profitability Index**: The ratio of NPV to initial investment.
- **Cash Yield**: The ratio of distributions to paid-in capital.

### LP Metrics
- IRR, MOIC, TVPI, DPI, RVPI, Payback Period

### GP Metrics
- IRR, MOIC, TVPI, DPI, RVPI, Payback Period
- Carried Interest, Management Fees, Origination Fees

### Metrics by Year
- DPI, RVPI, TVPI, IRR, Cash Yield

## Integration with Other Modules

The Cashflow Aggregator module integrates with:

- **Loan Generator**: To get loan origination data
- **Exit Simulator**: To get exit timing and values
- **Fee Engine**: To get fee amounts and timing
- **Leverage Engine**: To get leverage draws, repayments, and interest
- **Waterfall Engine**: To provide cashflows for distribution calculations and receive distribution results
- **Risk Metrics**: To provide cashflows for IRR and other calculations
- **Scenario Builder**: To get scenario definitions for scenario analysis
- **Tax Engine**: To calculate tax impacts on cashflows
- **Reinvestment Module**: To model reinvestment of cashflows
- **Liquidity Manager**: To analyze and manage fund liquidity
- **Export Module**: To export cashflow data to various formats

## Configuration Parameters

The module supports the following configuration parameters:

### Basic Parameters
- `time_granularity`: Time granularity for cashflow aggregation (daily, monthly, quarterly, yearly)
- `include_loan_level_cashflows`: Whether to include loan-level cashflows in the results
- `include_fund_level_cashflows`: Whether to include fund-level cashflows in the results
- `include_stakeholder_cashflows`: Whether to include stakeholder-level cashflows in the results
- `simple_interest_rate`: Simple interest rate for loans (default: 5%)
- `origination_fee_rate`: Origination fee rate (default: 3%)
- `appreciation_share_method`: Method for calculating appreciation share (pro_rata_ltv, tiered, fixed)
- `distribution_frequency`: Frequency of distributions to investors
- `distribution_lag`: Lag in months between cashflow receipt and distribution

### Parallel Processing Parameters
- `enable_parallel_processing`: Whether to enable parallel processing for loan-level cashflow calculations
- `num_workers`: Number of worker processes for parallel processing

### Scenario Analysis Parameters
- `enable_scenario_analysis`: Whether to enable scenario analysis
- `scenarios`: List of scenarios to analyze

### Sensitivity Analysis Parameters
- `enable_sensitivity_analysis`: Whether to enable sensitivity analysis
- `sensitivity_parameters`: List of parameters to vary for sensitivity analysis

### Cashflow Metrics Parameters
- `enable_cashflow_metrics`: Whether to enable cashflow metrics calculation
- `discount_rate`: Discount rate for DCF calculations

### Tax Impact Analysis Parameters
- `enable_tax_impact_analysis`: Whether to enable tax impact analysis
- `tax_rates`: Tax rates for different income types

### Reinvestment Modeling Parameters
- `enable_reinvestment_modeling`: Whether to enable reinvestment modeling
- `reinvestment_rate`: Rate of return on reinvested cashflows

### Liquidity Analysis Parameters
- `enable_liquidity_analysis`: Whether to enable liquidity analysis
- `minimum_cash_reserve`: Minimum cash reserve as percentage of fund size

### Export Parameters
- `enable_export`: Whether to enable export capabilities
- `export_formats`: Export formats (csv, excel, etc.)
