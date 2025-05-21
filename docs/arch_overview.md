# Architecture Overview

## System Components

```
┌─────────────────────────────────────────────────────────────────────┐
│                           API Layer                                 │
│                                                                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ REST API│  │GraphQL  │  │WebSocket│  │ SDK Gen │  │ Swagger │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────▼─────────────────────────────────────┐
│                        Simulation Engine                          │
│                                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Config  │  │  Loan   │  │  Exit   │  │   Fee   │  │  Carry  │ │
│  │ Loader  │  │Generator│  │Simulator│  │ Engine  │  │ Engine  │ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │
│                                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Price   │  │Reinvest │  │Cashflow │  │Parameter│  │   RNG   │ │
│  │  Path   │  │ Engine  │  │Aggregator│ │Registry │  │ Factory │ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │
└───────────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────▼─────────────────────────────────────┐
│                        Monte Carlo Layer                          │
│                                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │   MC    │  │   MC    │  │Efficient│  │  Risk   │  │Guardrail│ │
│  │  Outer  │  │  Inner  │  │Frontier │  │ Metrics │  │Monitor  │ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │
└───────────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────▼─────────────────────────────────────┐
│                      Persistence Layer                            │
│                                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │   DB    │  │   S3    │  │ Result  │  │ Metrics │  │  Logs   │ │
│  │ Manager │  │ Manager │  │  Store  │  │ Exporter│  │ Manager │ │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. Configuration is loaded and validated
2. Loan portfolio is generated based on configuration
3. Price paths are simulated for each zone
4. Exit events are simulated for each loan
5. Cash flows are calculated and aggregated
6. Fees and carried interest are calculated
7. Risk metrics are computed
8. Results are stored and returned

## Key Components

### Config Layer
- **config_loader**: Loads and validates simulation configuration from JSON files
- **param_registry**: Central registry for all simulation parameters with validation rules

### Engine Layer
- **loan_generator**: Generates loan portfolios based on configuration parameters
- **price_path**: Simulates home price appreciation paths for different zones
- **exit_simulator**: Models loan exits (sale, refinance, default) based on market conditions
- **fee_engine**: Calculates management fees, origination fees, and other expenses
- **carry_engine**: Implements waterfall distribution and carried interest calculations
- **cashflow_aggregator**: Aggregates and summarizes cash flows across the portfolio

### Monte Carlo Layer
- **rng_factory**: Creates deterministic random number generators with proper seeding
- **monte_carlo_outer**: Orchestrates outer loop Monte Carlo simulations (strategy sweep)
- **mc_inner_wrapper**: Manages inner loop Monte Carlo simulations (within-strategy randomness)
- **efficient_frontier**: Calculates efficient frontier for portfolio optimization

### Risk Layer
- **risk_metrics**: Computes risk metrics (VaR, Sharpe ratio, max drawdown)
- **guardrail_monitor**: Enforces risk guardrails and validation rules

### Persistence Layer
- **db_manager**: Handles database operations
- **s3_manager**: Manages S3 storage for simulation results
- **result_store**: Stores and retrieves simulation results

### API Layer
- **routes**: Defines API endpoints
- **models**: Defines API request and response models
- **dependencies**: Defines API dependencies
- **server**: Configures and runs the API server

## Cross-Cutting Concerns

### Logging
- Structured logging (JSON format)
- Trace IDs for request tracking
- Configurable log levels

### Metrics
- Prometheus metrics export
- Runtime metrics
- Business metrics

### Feature Flags
- Controlled via environment variables
- Enables/disables features at runtime

### Error Handling
- Custom exception types
- Detailed error messages
- Proper error propagation
