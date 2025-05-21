# Capital Allocation and Loan Generation Modules

This document provides comprehensive documentation for the Capital Allocation and Loan Generation modules in the EQU IHOME SIM ENGINE v2.

## Table of Contents
- [Overview](#overview)
- [Capital Allocation Module](#capital-allocation-module)
  - [Key Features](#key-features)
  - [Functions](#functions)
  - [Visualization Data](#visualization-data)
  - [Integration with TLS Module](#integration-with-tls-module)
- [Loan Generation Module](#loan-generation-module)
  - [Key Features](#key-features-1)
  - [Functions](#functions-1)
  - [Visualization Data](#visualization-data-1)
  - [Property Integration](#property-integration)
- [API Integration](#api-integration)
- [SDK Usage](#sdk-usage)
- [Examples](#examples)

## Overview

The Capital Allocation and Loan Generation modules work together to create a portfolio of loans based on strategy parameters. The Capital Allocation module determines how capital should be allocated across different zones (green, orange, red), while the Loan Generation module creates individual loans with realistic characteristics based on this allocation.

## Capital Allocation Module

The Capital Allocation module (`src/capital_allocator/allocator.py`) is responsible for allocating capital across zones based on the allocation policy specified in the configuration.

### Key Features

- **Zone-Based Allocation**: Allocates capital across different risk zones (green, orange, red)
- **Allocation Policy Enforcement**: Validates and enforces allocation constraints
- **Rebalancing Logic**: Adjusts allocations if they drift from targets
- **Visualization Support**: Generates comprehensive visualization data
- **Progress Reporting**: Reports progress via WebSockets
- **Error Handling**: Provides detailed error messages with specific error codes
- **TLS Integration**: Integrates with the TLS module to get zone data

### Functions

#### Core Functions

- `allocate_capital(context)`: Allocates capital across zones based on policy
- `rebalance_allocation(context, tolerance)`: Rebalances allocation to match target allocations
- `calculate_loan_counts(context, avg_loan_size)`: Calculates the number of loans to generate for each zone
- `update_actual_allocation(context)`: Updates actual allocation based on generated loans
- `get_zone_properties(context, zone, limit)`: Gets properties in a specific zone
- `get_allocation_summary(context)`: Gets a summary of the capital allocation

#### Utility Functions

- `validate_zone_allocations(zone_allocations)`: Validates zone allocations
- `generate_allocation_visualization(zone_allocations)`: Generates visualization data for zone allocations
- `calculate_allocation_statistics(zone_allocations, zone_distribution)`: Calculates statistics for zone allocations
- `generate_rebalancing_visualization(targets, actual, gaps, adjustments)`: Generates visualization data for allocation rebalancing
- `generate_loan_count_visualization(loan_counts, capital_by_zone, avg_loan_size)`: Generates visualization data for loan counts
- `generate_allocation_comparison(targets, actual)`: Generates visualization data for allocation comparison

### Visualization Data

The Capital Allocation module generates the following visualization data:

1. **Allocation Visualization**:
   - Pie chart data for zone allocations
   - Bar chart data for zone allocations
   - Table data with allocation percentages

2. **Rebalancing Visualization**:
   - Comparison chart data for target vs. actual allocations
   - Adjustment chart data for allocation adjustments
   - Table data with target, actual, gap, and adjustment values

3. **Loan Count Visualization**:
   - Bar chart data for loan counts by zone
   - Pie chart data for loan counts by zone
   - Table data with capital, loan count, and average loan size by zone

4. **Allocation Comparison**:
   - Comparison chart data for target vs. actual allocations
   - Table data with target, actual, and difference values

### Integration with TLS Module

The Capital Allocation module integrates with the TLS module to get zone data:

- Retrieves zone distribution from the TLS module
- Gets properties in each zone for loan generation
- Uses zone metrics for allocation statistics calculation

## Loan Generation Module

The Loan Generation module (`src/engine/loan_generator.py`) is responsible for generating loan portfolios based on configuration parameters and the capital allocation.

### Key Features

- **Zone-Based Loan Allocation**: Assigns loans to zones based on capital allocation
- **Realistic Loan Distributions**: Generates loans with realistic distributions for size, LTV, term, and interest rate
- **Property Integration**: Ties each loan to an actual property from the TLS module
- **Visualization Support**: Generates comprehensive visualization data
- **Progress Reporting**: Reports progress via WebSockets
- **Error Handling**: Provides detailed error messages with specific error codes
- **Capital Allocator Integration**: Integrates with the Capital Allocator module to get zone allocations

### Functions

#### Core Functions

- `generate_loans(context)`: Generates a loan portfolio based on configuration parameters
- `generate_loan_sizes(num_loans, avg_loan_size, loan_size_std_dev, min_loan_size, max_loan_size, rng)`: Generates loan sizes based on a normal distribution
- `generate_ltv_ratios(num_loans, avg_ltv, ltv_std_dev, min_ltv, max_ltv, rng)`: Generates LTV ratios based on a normal distribution
- `generate_loan_terms(num_loans, avg_loan_term, rng)`: Generates loan terms based on a normal distribution
- `generate_interest_rates(num_loans, avg_interest_rate, rng)`: Generates interest rates based on a normal distribution

#### Utility Functions

- `validate_loan_parameters(config)`: Validates loan generation parameters
- `assign_loans_to_zones(num_loans, loan_counts_by_zone)`: Assigns loans to zones based on loan counts by zone
- `get_properties_for_zone(context, zone, limit)`: Gets properties for a specific zone from the TLS module
- `get_property_for_loan(property_data_by_zone, zone, index)`: Gets property data for a specific loan
- `generate_loan_portfolio_visualization(loans)`: Generates visualization data for the loan portfolio
- `calculate_loan_portfolio_statistics(loans)`: Calculates statistics for the loan portfolio

### Visualization Data

The Loan Generation module generates the following visualization data:

1. **Loan Portfolio Visualization**:
   - Pie charts for loan counts and amounts by zone
   - Histograms for loan sizes, LTV ratios, loan terms, and interest rates
   - Scatter plots for loan size vs. LTV and loan size vs. term
   - Tables with loan statistics by zone

2. **Loan Portfolio Statistics**:
   - Overall metrics (total loan amount, average loan size, etc.)
   - Zone-specific metrics (percentage of loans in each zone, average characteristics by zone)
   - Property statistics (distribution of property types, bedroom counts, etc.)

### Property Integration

Each loan is tied to an actual property from the TLS module with the following attributes:

- Property ID and suburb ID
- Suburb name and zone
- Property type (house, apartment, townhouse, etc.)
- Physical characteristics (bedrooms, bathrooms, land size, building size)
- Year built and base value

## API Integration

The Capital Allocation and Loan Generation modules integrate with the API through the following endpoints:

- `POST /api/v1/simulations`: Creates a new simulation with capital allocation and loan generation
- `GET /api/v1/simulations/{simulation_id}`: Gets the results of a simulation, including capital allocation and loan generation results
- `GET /api/v1/simulations/{simulation_id}/capital-allocation`: Gets the capital allocation results for a simulation
- `GET /api/v1/simulations/{simulation_id}/loans`: Gets the generated loans for a simulation
- `GET /api/v1/simulations/{simulation_id}/visualizations`: Gets the visualization data for a simulation

WebSocket endpoints for real-time progress tracking:

- `WS /api/v1/ws/{simulation_id}`: Receives real-time progress updates during simulation

## SDK Usage

The SDK provides the following functions for working with the Capital Allocation and Loan Generation modules:

```python
# Create a new simulation
simulation = client.create_simulation(config)

# Get capital allocation results
capital_allocation = client.get_capital_allocation(simulation_id)

# Get generated loans
loans = client.get_loans(simulation_id)

# Get visualization data
visualizations = client.get_visualizations(simulation_id)

# Subscribe to real-time progress updates
client.subscribe_to_progress(simulation_id, callback)
```

## Examples

### Example 1: Basic Capital Allocation and Loan Generation

```python
from equ_ihome_sim_sdk import SimulationClient

# Initialize client
client = SimulationClient("http://localhost:8000")

# Create simulation configuration
config = {
    "fund_size": 100000000,
    "fund_term": 10,
    "vintage_year": 2023,
    "zone_allocations": {
        "green": 0.6,
        "orange": 0.3,
        "red": 0.1
    },
    "avg_loan_size": 500000,
    "loan_size_std_dev": 100000,
    "min_loan_size": 300000,
    "max_loan_size": 1000000,
    "avg_loan_ltv": 0.5,
    "ltv_std_dev": 0.05,
    "min_ltv": 0.3,
    "max_ltv": 0.7,
    "avg_loan_term": 10,
    "avg_loan_interest_rate": 0.05
}

# Create simulation
simulation = client.create_simulation(config)

# Wait for simulation to complete
client.wait_for_simulation(simulation.id)

# Get capital allocation results
capital_allocation = client.get_capital_allocation(simulation.id)

# Get generated loans
loans = client.get_loans(simulation.id)

# Get visualization data
visualizations = client.get_visualizations(simulation.id)

# Print summary
print(f"Capital Allocation: {capital_allocation['zone_targets']}")
print(f"Number of Loans: {len(loans)}")
print(f"Total Loan Amount: ${sum(loan['loan_size'] for loan in loans):,.2f}")
```
