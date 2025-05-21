# Parameter Tracking Document

This document provides a comprehensive list of all parameters used in the EQU IHOME SIM ENGINE v2. It serves as a reference for both frontend and backend developers to ensure consistency in parameter handling.

## Parameter Categories

Parameters are organized into the following categories:

1. Fund Structure
2. Fees and Expenses
3. Deployment and Capital Calls
4. Reinvestment and Exit
5. Waterfall and Returns
6. Market and Loan Parameters
7. Leverage and Capital Structure
8. Advanced/Analytics

## Parameter Definitions

Each parameter is defined with the following attributes:
- **Name**: The canonical parameter name used in the API
- **Type**: Data type (int, float, str, bool, dict, list)
- **Required**: Whether the parameter is required or optional
- **Default**: Default value if not provided
- **Description**: Detailed description of the parameter
- **Validation Rules**: Constraints on valid values
- **UI Component**: Suggested UI component for the frontend

## 1. Fund Structure

| Name | Type | Required | Default | Description | Validation Rules | UI Component |
|------|------|----------|---------|-------------|------------------|-------------|
| `fund_size` | int | Yes | 100,000,000 | Total fund size in dollars | >= 1,000,000 | NumberInput |
| `fund_term` | int | Yes | 10 | Fund lifetime in years | 1-30 | NumberInput |
| `fund_id` | str | No | null | Unique identifier for the fund | - | TextInput |
| `fund_group` | str | No | null | Group identifier for multi-fund setups | - | TextInput |
| `tranche_id` | str | No | null | Tranche identifier if using tranches | - | TextInput |

## 2. Fees and Expenses

| Name | Type | Required | Default | Description | Validation Rules | UI Component |
|------|------|----------|---------|-------------|------------------|-------------|
| `management_fee_rate` | float | No | 0.02 | Management fee as a decimal | 0-0.05 | PercentageInput |
| `management_fee_basis` | str | No | "committed_capital" | Basis for management fee calculation | One of: "committed_capital", "invested_capital", "net_asset_value", "stepped" | Dropdown |
| `management_fee_step_down` | bool | No | false | Whether to step down fees | - | Toggle |
| `management_fee_step_down_year` | int | No | 5 | Year to begin step-down | >= 0 | NumberInput |
| `management_fee_step_down_rate` | float | No | 0.5 | Step-down rate | 0-1 | PercentageInput |
| `expense_rate` | float | No | 0.005 | Fund expense rate | 0-0.1 | PercentageInput |
| `formation_costs` | float | No | 0 | Initial fund formation costs | >= 0 | NumberInput |

## 3. Deployment and Capital Calls

| Name | Type | Required | Default | Description | Validation Rules | UI Component |
|------|------|----------|---------|-------------|------------------|-------------|
| `deployment_pace` | str | No | "even" | Deployment pace pattern | One of: "even", "front_loaded", "back_loaded", "bell_curve" | Dropdown |
| `deployment_period` | int | No | 3 | Number of years for deployment | >= 1 | NumberInput |
| `deployment_period_unit` | str | No | "years" | Unit for deployment period | One of: "years", "months", "quarters" | Dropdown |
| `deployment_monthly_granularity` | bool | No | false | Use monthly granularity for deployment/exit | - | Toggle |
| `capital_call_schedule` | str | No | "upfront" | Capital call schedule type | One of: "upfront", "equal", "front_loaded", "back_loaded", "custom" | Dropdown |
| `capital_call_years` | int | No | 3 | Number of years for capital calls | >= 1 | NumberInput |
| `custom_capital_call_schedule` | dict | No | {} | Custom schedule by year | Valid JSON | JsonEditor |

## 4. Reinvestment and Exit

| Name | Type | Required | Default | Description | Validation Rules | UI Component |
|------|------|----------|---------|-------------|------------------|-------------|
| `reinvestment_period` | int | No | 5 | Years during which reinvestment is allowed | >= 0 | NumberInput |
| `reinvestment_rate` | float | No | 0.0 | Fraction of exits to reinvest | 0-1 | PercentageInput |
| `reinvestment_reserve_rate` | float | No | 0.8 | Fraction of cash reserved for reinvestment | 0-1 | PercentageInput |
| `avg_loan_exit_year` | float | No | 7 | Average exit year for loans | > 0 | NumberInput |
| `exit_year_std_dev` | float | No | 1.5 | Std dev of exit year | >= 0 | NumberInput |
| `early_exit_probability` | float | No | 0.3 | Probability of early exit | 0-1 | PercentageInput |

## 5. Waterfall and Returns

| Name | Type | Required | Default | Description | Validation Rules | UI Component |
|------|------|----------|---------|-------------|------------------|-------------|
| `waterfall_structure` | str | No | "european" | Waterfall structure type | One of: "european", "american" | Dropdown |
| `hurdle_rate` | float | No | 0.08 | Preferred return rate | 0-1 | PercentageInput |
| `catch_up_rate` | float | No | 0.0 | GP catch-up rate | 0-1 | PercentageInput |
| `catch_up_structure` | str | No | "full" | Catch-up structure | One of: "full", "partial", "none" | Dropdown |
| `carried_interest_rate` | float | No | 0.20 | GP carry | 0-1 | PercentageInput |
| `gp_commitment_percentage` | float | No | 0.05 | GP commitment | 0-1 | PercentageInput |
| `preferred_return_compounding` | str | No | "annual" | Compounding frequency | One of: "annual", "quarterly", "monthly", "continuous" | Dropdown |
| `distribution_frequency` | str | No | "annual" | Distribution frequency | One of: "annual", "quarterly", "semi_annual" | Dropdown |
| `distribution_policy` | str | No | "available_cash" | Distribution policy | One of: "available_cash", "income_only", "return_of_capital", "reinvestment_priority" | Dropdown |
| `clawback_provision` | bool | No | true | Whether GP is subject to clawback | - | Toggle |

## 6. Market and Loan Parameters

| Name | Type | Required | Default | Description | Validation Rules | UI Component |
|------|------|----------|---------|-------------|------------------|-------------|
| `avg_loan_size` | float | No | 250000 | Average loan size | > 0 | NumberInput |
| `loan_size_std_dev` | float | No | 50000 | Std dev of loan size | >= 0 | NumberInput |
| `min_loan_size` | float | No | 100000 | Minimum loan size | > 0 | NumberInput |
| `max_loan_size` | float | No | 500000 | Maximum loan size | > min_loan_size | NumberInput |
| `avg_loan_term` | float | No | 5 | Average loan term | > 0 | NumberInput |
| `avg_loan_interest_rate` | float | No | 0.06 | Average loan interest rate | 0-1 | PercentageInput |
| `avg_loan_ltv` | float | No | 0.75 | Average loan-to-value | 0-1 | PercentageInput |
| `zone_allocations` | dict | No | {"green": 0.6, "orange": 0.3, "red": 0.1} | Zone allocation percentages | Sum to 1 | AllocationSlider |
| `use_tls_zone_growth` | bool | No | false | Use TLS dataset suburb growth values | - | Toggle |

## 7. Leverage and Capital Structure

| Name | Type | Required | Default | Description | Validation Rules | UI Component |
|------|------|----------|---------|-------------|------------------|-------------|
| `leverage.green_sleeve.enabled` | bool | No | true | Toggle the Green NAV facility | - | Toggle |
| `leverage.green_sleeve.max_mult` | float | No | 1.5 | Limit as a multiple of sleeve NAV | > 0 | NumberInput |
| `leverage.green_sleeve.spread_bps` | int | No | 275 | Credit spread over base rate (bps) | >= 0 | NumberInput |
| `leverage.green_sleeve.commitment_fee_bps` | int | No | 50 | Commitment fee on undrawn balance (bps) | >= 0 | NumberInput |
| `leverage.a_plus_overadvance.enabled` | bool | No | false | Enable TLS-grade A+ over-advance | - | Toggle |
| `leverage.a_plus_overadvance.tls_grade` | str | No | "A+" | TLS grade eligible for over-advance | Valid TLS grade | TextInput |
| `leverage.a_plus_overadvance.advance_rate` | float | No | 0.75 | Advance rate on eligible NAV | 0-1 | PercentageInput |

## 8. Advanced/Analytics

| Name | Type | Required | Default | Description | Validation Rules | UI Component |
|------|------|----------|---------|-------------|------------------|-------------|
| `monte_carlo_enabled` | bool | No | false | Enable Monte Carlo simulation | - | Toggle |
| `inner_monte_carlo_enabled` | bool | No | false | Enable nested Monte Carlo simulation | - | Toggle |
| `num_simulations` | int | No | 1000 | Number of Monte Carlo runs | > 0 | NumberInput |
| `num_inner_simulations` | int | No | 1000 | Number of inner simulations per outer run | > 0 | NumberInput |
| `variation_factor` | float | No | 0.1 | Parameter variation for MC | >= 0 | NumberInput |
| `monte_carlo_seed` | int | No | null | Random seed for MC | - | NumberInput |
| `optimization_enabled` | bool | No | false | Enable portfolio optimization | - | Toggle |
| `generate_efficient_frontier` | bool | No | false | Generate efficient frontier | - | Toggle |
| `efficient_frontier_points` | int | No | 50 | Number of points on the efficient frontier | > 0 | NumberInput |
| `stress_testing_enabled` | bool | No | false | Enable stress testing | - | Toggle |

## Implementation Notes

1. All parameters must be validated against the canonical schema defined in `docs/Auditapr24/simulation_config_schema.md`
2. The backend must provide clear error messages for validation failures
3. The frontend should use appropriate UI components based on the parameter type and validation rules
4. Default values should be used when parameters are not provided
5. Parameter names must be consistent across frontend, backend, and API
