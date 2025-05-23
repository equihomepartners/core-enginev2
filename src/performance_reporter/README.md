# Performance Reporter Module

## Overview

The Performance Reporter module is responsible for generating comprehensive performance reports for the EQU IHOME SIM ENGINE v2. It aggregates data from various modules and presents it in a structured format, including KPI tables, zone allocation reports, cash flow visualizations, risk metric reports, and export capabilities.

This module serves as a centralized reporting solution that leverages metrics and data already calculated by other modules, avoiding redundant calculations while providing a standardized approach to reporting.

## Key Features

### Core Functionality
- **KPI Table Generation**: Creates comprehensive tables of key performance indicators across various categories.
- **Zone Allocation Reporting**: Analyzes and reports on portfolio allocation by zone, suburb, property type, and other dimensions.
- **Cash Flow Visualization**: Generates visualizations of fund-level, LP-level, and GP-level cash flows.
- **Risk Metric Reporting**: Aggregates and presents risk metrics from the Risk Metrics module.
- **Tranche Performance Reporting**: Reports on the performance of different tranches in the fund.
- **Loan Performance Reporting**: Analyzes and reports on the performance of individual loans in the portfolio.
- **Export Capabilities**: Exports reports to various formats (JSON, CSV, Excel, Markdown, HTML).
- **WebSocket Integration**: Provides real-time progress updates during report generation.
- **Error Handling**: Comprehensive error handling with detailed error messages.

## Module Structure

- `performance_reporter.py`: Main implementation of the performance reporter.
- `__init__.py`: Module initialization and exports.

## Usage

### Using the Generate Function

```python
from src.performance_reporter import generate_performance_report
from src.engine.simulation_context import SimulationContext

# Create simulation context
context = SimulationContext(...)

# Generate performance report
report = await generate_performance_report(context)

# Access report data
summary = report["summary"]
kpi_table = report["kpi_table"]
zone_allocation = report["zone_allocation"]
```

### Using the PerformanceReporter Class

```python
from src.performance_reporter import PerformanceReporter, ReportFormat
from src.engine.simulation_context import SimulationContext

# Create simulation context
context = SimulationContext(...)

# Create performance reporter with custom configuration
reporter = PerformanceReporter(context)
reporter.export_format = ReportFormat.MARKDOWN
reporter.export_path = "custom_reports"

# Generate report
report = await reporter.generate_report()

# Access report data
summary = report["summary"]
kpi_table = report["kpi_table"]
zone_allocation = report["zone_allocation"]
```

## Report Structure

The performance report is structured as follows:

### Summary
A high-level summary of the simulation, including fund size, fund term, number of loans, total loan amount, average LTV, IRR, MOIC, TVPI, DPI, RVPI, VaR, Sharpe ratio, and worst guardrail level.

### KPI Table
Detailed tables of key performance indicators across various categories:
- **Fund Metrics**: IRR, MOIC, TVPI, DPI, RVPI, payback period, etc.
- **Portfolio Metrics**: Number of loans, total loan amount, average LTV, zone percentages, etc.
- **Risk Metrics**: VaR, CVaR, Sharpe ratio, Sortino ratio, max drawdown, beta, alpha, etc.
- **Liquidity Metrics**: Liquidity buffer, WAL, expected exit lag, liquidity score, etc.
- **Leverage Metrics**: NAV utilisation, interest coverage, debt-to-equity ratio, etc.
- **Stakeholder Metrics**: LP IRR, LP MOIC, GP IRR, GP MOIC, carried interest, management fees, etc.

### Zone Allocation
Analysis of portfolio allocation by:
- **Zone**: Green, orange, red zones
- **Suburb**: Top suburbs by allocation
- **Property Type**: House, apartment, townhouse, etc.
- **LTV Band**: 0-50%, 50-60%, 60-70%, etc.
- **Loan Size Band**: $0-$100k, $100k-$200k, $200k-$300k, etc.
- **Target vs Actual**: Comparison of target allocation to actual allocation

### Cash Flow
Detailed cash flow analysis, including:
- **Fund-Level Cash Flows**: Capital calls, loan investments, origination fees, principal repayments, interest income, appreciation share, management fees, fund expenses, leverage draws, leverage repayments, leverage interest, distributions, etc.
- **LP-Level Cash Flows**: Capital calls, distributions, etc.
- **GP-Level Cash Flows**: Capital calls, management fees, origination fees, carried interest, distributions, etc.
- **Metrics by Year**: DPI, RVPI, TVPI, IRR, cash yield, etc.

### Risk Metrics
Comprehensive risk metrics, including:
- **Market/Price Metrics**: Volatility, alpha, beta, VaR, CVaR, etc.
- **Credit Metrics**: LTV, stress-LTV, default probabilities, etc.
- **Liquidity Metrics**: Liquidity scores, exit lag, WAL, etc.
- **Leverage Metrics**: NAV utilisation, interest coverage, etc.
- **Concentration Metrics**: Zone exposure, suburb exposure, single-loan exposure, etc.
- **Performance Metrics**: IRR, Sharpe ratio, Sortino ratio, etc.
- **Stress Test Results**: Results of various stress tests
- **Sensitivity Analysis**: Results of sensitivity analysis

### Tranche Performance
Analysis of tranche performance, including:
- **Tranche Summary**: Size, priority, type, interest rate, target return, actual return, etc.
- **Tranche Cash Flows**: Principal payments, interest payments, profit share payments, etc.
- **Tranche Allocations**: Allocation of loans to tranches
- **Coverage Tests**: Results of overcollateralization and interest coverage tests
- **Reserve Account**: History of reserve account balances

### Loan Performance
Detailed analysis of loan performance, including:
- **Loan Summary**: Suburb, zone, loan amount, LTV, property type, exit month, exit type, exit amount, return amount, return percentage, IRR, etc.
- **Loan Cash Flows**: Origination, interest, principal repayments, etc.
- **Loan Metrics**: IRR, return percentage, etc.
- **Loan Exits**: Exit month, exit type, exit amount, etc.
- **Loan Defaults**: Default analysis

### Visualization
Visualization data for various aspects of the report, including:
- **KPI Summary**: Charts for fund metrics, portfolio metrics, risk metrics, etc.
- **Zone Allocation**: Charts for allocation by zone, suburb, property type, etc.
- **Cash Flow**: Charts for cumulative cash flow, cash flow by category, metrics by year, etc.
- **Risk Metrics**: Charts for VaR, concentration, stress tests, sensitivity analysis, etc.
- **Loan Performance**: Charts for loan size distribution, LTV distribution, exit month distribution, exit type distribution, return distribution, etc.
- **Tranche Performance**: Charts for tranche waterfall, tranche cash flow, tranche allocation, etc.

## Integration with Other Modules

The Performance Reporter module integrates with:

- **Risk Metrics**: To get risk metrics data
- **Cashflow Aggregator**: To get cash flow data
- **Tranche Manager**: To get tranche performance data
- **TLS Module**: To get zone and suburb data
- **Loan Generator**: To get loan data
- **Exit Simulator**: To get exit data
- **Waterfall Engine**: To get waterfall distribution data
- **Guardrail Monitor**: To get guardrail report data

## Configuration Parameters

The Performance Reporter module supports the following configuration parameters:

- **include_kpi_table**: Whether to include the KPI table in the report (default: true)
- **include_zone_allocation**: Whether to include zone allocation in the report (default: true)
- **include_cash_flow**: Whether to include cash flow in the report (default: true)
- **include_risk_metrics**: Whether to include risk metrics in the report (default: true)
- **include_tranche_performance**: Whether to include tranche performance in the report (default: true)
- **include_loan_performance**: Whether to include loan performance in the report (default: true)
- **include_visualization**: Whether to include visualization data in the report (default: true)
- **export_format**: Format to export the report to (default: json)
- **export_path**: Path to export the report to (default: reports)
