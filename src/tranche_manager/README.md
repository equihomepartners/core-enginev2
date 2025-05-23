# Tranche Manager

The Tranche Manager is a critical component of the EQU IHOME SIM ENGINE v2 that manages tranches in the fund. It handles the allocation of loans to tranches, distribution of cashflows, and calculation of tranche-specific metrics.

## Functionality

The Tranche Manager provides the following functionality:

- **Tranche Definition and Configuration**: Defines and configures tranches with different characteristics (senior debt, mezzanine, preferred equity, equity).
- **Loan Allocation**: Allocates loans to tranches based on tranche type, priority, and allocation rules.
- **Cashflow Distribution**: Distributes cashflows to tranches based on priority and payment rules.
- **Tranche Metrics Calculation**: Calculates performance metrics for each tranche (IRR, MOIC, actual return).
- **Tranche Waterfall Rules**: Implements waterfall rules for equity tranches (hurdle rate, carried interest).
- **Coverage Tests**: Runs overcollateralization and interest coverage tests.
- **Reserve Account Management**: Manages a reserve account for senior debt tranches.
- **Visualization**: Generates comprehensive visualization data for tranches.

## Module Structure

The Tranche Manager consists of the following components:

- `TrancheManager` class: The main class that manages tranches in the fund.
- `Tranche` class: Represents a tranche in the fund.
- `TrancheType` enum: Defines the types of tranches (senior debt, mezzanine, preferred equity, equity).
- `PaymentFrequency` enum: Defines the payment frequencies (monthly, quarterly, semi-annual, annual).
- `AmortizationSchedule` enum: Defines the amortization schedules (straight-line, interest-only, balloon).
- `TestType` enum: Defines the types of coverage tests (overcollateralization, interest coverage).
- `manage_tranches` function: The entry point for the orchestrator.

## Integration Points

The Tranche Manager integrates with the following components:

- **Simulation Context**: Retrieves loan and cashflow data and stores tranche results.
- **WebSocket Manager**: Sends progress updates and intermediate results.
- **Orchestrator**: Registers the module for execution.

## Data Flow

### Inputs

The Tranche Manager takes the following inputs:

- **Tranche Configuration**: Tranche definitions, sizes, priorities, types, etc.
- **Loans**: Loan data for allocation to tranches.
- **Cashflows**: Cashflow data for distribution to tranches.
- **Reserve Account Configuration**: Target percentage, initial funding, replenishment rate.
- **Coverage Test Configuration**: Thresholds, test frequencies, cure periods.

### Outputs

The Tranche Manager produces the following outputs:

- **Tranche Summary**: Summary of each tranche's performance.
- **Tranche Cashflows**: Cashflows for each tranche.
- **Tranche Allocations**: Loan allocations for each tranche.
- **Coverage Tests**: Results of overcollateralization and interest coverage tests.
- **Reserve Account**: History of reserve account balances.
- **Visualization Data**: Data for visualizing tranche performance.

## Visualization

The Tranche Manager generates the following visualization data:

- **Tranche Waterfall Chart**: Breakdown of payments by tranche.
- **Tranche Cashflow Chart**: Cashflows over time for each tranche.
- **Tranche Allocation Chart**: Allocation of loans by zone for each tranche.
- **Tranche Performance Chart**: Performance metrics for each tranche.
- **Coverage Test Chart**: Coverage test results over time.
- **Reserve Account Chart**: Reserve account balance over time.

## Error Handling

The Tranche Manager includes comprehensive error handling:

- Logs errors with detailed information.
- Validates tranche configuration.
- Handles missing or invalid data.
- Sends error messages to the frontend via WebSocket.

## Performance Considerations

- The Tranche Manager is designed to be efficient and scalable.
- It handles large numbers of loans and tranches.
- It processes cashflows efficiently.

## Future Enhancements

Potential future enhancements for the Tranche Manager include:

1. Support for more complex tranche structures.
2. Integration with the waterfall engine for more sophisticated distribution rules.
3. More detailed visualization options.
4. Support for custom tranche rules.
5. Performance optimizations for large portfolios.

## Usage Example

```python
from src.tranche_manager import manage_tranches
from src.engine.simulation_context import SimulationContext

# Create simulation context
context = SimulationContext(...)

# Manage tranches
await manage_tranches(context)

# Access tranche results
tranches = context.tranches
tranche_summary = tranches["tranche_summary"]
tranche_cashflows = tranches["tranche_cashflows"]
tranche_allocations = tranches["tranche_allocations"]
```

## Configuration Example

```json
{
  "tranche_manager": {
    "enabled": true,
    "tranches": [
      {
        "name": "Senior Debt",
        "size": 70000000,
        "priority": 1,
        "type": "senior_debt",
        "interest_rate": 0.05,
        "payment_frequency": "quarterly",
        "amortization": false,
        "allocation_rules": {
          "ltv_constraints": {
            "min_ltv": 0.0,
            "max_ltv": 0.75
          }
        }
      },
      {
        "name": "Mezzanine",
        "size": 20000000,
        "priority": 2,
        "type": "mezzanine",
        "interest_rate": 0.08,
        "payment_frequency": "quarterly",
        "amortization": false,
        "allocation_rules": {
          "ltv_constraints": {
            "min_ltv": 0.75,
            "max_ltv": 0.85
          }
        }
      },
      {
        "name": "Equity",
        "size": 10000000,
        "priority": 3,
        "type": "equity",
        "target_return": 0.15,
        "waterfall_rules": {
          "hurdle_rate": 0.08,
          "carried_interest_rate": 0.20
        }
      }
    ],
    "reserve_account": {
      "enabled": true,
      "target_percentage": 0.05,
      "initial_funding": 0.03,
      "replenishment_rate": 0.01
    },
    "overcollateralization_test": {
      "enabled": true,
      "threshold": 1.2,
      "test_frequency": "quarterly",
      "cure_period_months": 3
    },
    "interest_coverage_test": {
      "enabled": true,
      "threshold": 1.5,
      "test_frequency": "quarterly",
      "cure_period_months": 3
    }
  }
}
```
