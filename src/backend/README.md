# EQU IHOME SIM ENGINE v2 - Backend Architecture

This document serves as the master reference for the backend architecture of the EQU IHOME SIM ENGINE v2. It provides a comprehensive guide to the system's components, data flow, and implementation strategy.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Data Flow](#data-flow)
- [Module Dependencies](#module-dependencies)
- [Simulation Context](#simulation-context)
- [Development Sequence](#development-sequence)
- [Testing Strategy](#testing-strategy)
- [Performance Considerations](#performance-considerations)

## Architecture Overview

The backend is structured as a modular pipeline with specialized components that process data in sequence. The system follows a clean architecture pattern with distinct layers:

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
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │Config Layer │  │Engine Layer  │  │Monte Carlo  │  │Risk Layer│ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └──────────┘ │
└───────────────────────────────────────────────────────────────────┘
                               │
┌─────────────────────────────▼─────────────────────────────────────┐
│                      Persistence Layer                            │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│  │Database     │  │S3 Storage   │  │Result Cache │               │
│  └─────────────┘  └─────────────┘  └─────────────┘               │
└───────────────────────────────────────────────────────────────────┘
```

### Key Layers

1. **Config Layer**: Loads, validates, and provides access to simulation parameters
2. **Engine Layer**: Core simulation components that model loans, price paths, and exits
3. **Monte Carlo Layer**: Orchestrates simulations with deterministic random number generation
4. **Risk Layer**: Calculates risk metrics and enforces guardrails
5. **Persistence Layer**: Stores and retrieves simulation results
6. **API Layer**: Exposes functionality through REST and GraphQL endpoints

## Data Flow

The data flows through the system in the following sequence:

1. **Configuration Loading**:
   - JSON configuration is loaded and validated
   - Parameters are registered and accessible to all modules

2. **Capital Allocation**:
   - Target zone allocations are determined
   - TLS module provides zone classification data
   - Capital is allocated across zones based on policy

3. **Loan Generation**:
   - Loan portfolios are created based on allocation targets
   - Loans are assigned characteristics (size, LTV, term)

4. **Price Path Simulation**:
   - Home price appreciation paths are generated for each zone
   - Correlated random walks model price movements over time

5. **Exit Simulation**:
   - Loan exits (sale, refinance, default) are modeled
   - Exit timing and recovery values are calculated

6. **Reinvestment**:
   - Capital from exits is reinvested during reinvestment period
   - New loans are generated with updated parameters

7. **Leverage Management**:
   - Debt facilities are drawn/repaid according to strategy
   - Interest expenses are calculated
   - Borrowing base tests are applied

8. **Fee Calculation**:
   - Management fees are calculated
   - Origination fees are applied
   - Fund expenses are deducted

9. **Cashflow Aggregation**:
   - Cash flows are calculated for each loan
   - Fund-level cash flows are aggregated

10. **Waterfall Distribution**:
    - Cash flows are distributed according to waterfall rules
    - Carried interest is calculated
    - LP/GP splits are applied

11. **Tranche Management**:
    - Cash flows are allocated to different tranches
    - Tranche-specific returns are calculated

12. **Risk Analysis**:
    - Risk metrics are calculated (IRR, equity multiple, VaR, etc.)
    - Guardrails are enforced to prevent excessive risk
    - Performance reports are generated

13. **Result Storage**:
    - Results are stored in the database and/or S3
    - Results are cached for quick retrieval

14. **API Response**:
    - Results are formatted and returned to the client
    - SDKs provide client-side access to results

### Detailed Data Flow Diagram

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Config Layer │────▶│Capital Alloc.│────▶│ TLS Module   │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Price Path   │◀────│Loan Generator│────▶│Exit Simulator │
└──────────────┘     └──────────────┘     └──────────────┘
        │                                         │
        │                                         ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│Leverage Engine│◀────│Reinvest Eng. │◀────│ Fee Engine   │
└──────────────┘     └──────────────┘     └──────────────┘
        │
        ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Cashflow Agg │────▶│Waterfall Eng.│────▶│Tranche Manager│
└──────────────┘     └──────────────┘     └──────────────┘
        │
        ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Risk Metrics │────▶│ Guardrails   │────▶│Perf. Reporter │
└──────────────┘     └──────────────┘     └──────────────┘
        │
        ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│ Result Store │────▶│   API Layer  │────▶│   SDK Gen    │
└──────────────┘     └──────────────┘     └──────────────┘
```

## Module Dependencies

The following diagram shows the dependencies between modules:

```
config_loader ◀─── param_registry ◀─── validation
      │
      ▼
capital_allocator ◀─── tls_module
      │
      ▼
loan_generator ──▶ price_path ──▶ exit_simulator
      │                │               │
      │                │               │
      ▼                ▼               ▼
reinvest_engine ──▶ leverage_engine ──▶ fee_engine
      │                │                  │
      │                │                  │
      ▼                ▼                  ▼
cashflow_aggregator ──▶ waterfall_engine ──▶ tranche_manager
      │
      ▼
risk_metrics ──▶ guardrail_monitor ──▶ performance_reporter
      │
      ▼
monte_carlo_outer ◀─── mc_inner_wrapper ◀─── rng_factory ◀─── scenario_builder
      │
      ▼
result_store ──▶ db_manager/s3_manager
      │
      ▼
   api_layer
```

## Simulation Context

The `SimulationContext` is a shared object that is passed between modules to maintain state and provide access to common functionality. It contains:

```python
class SimulationContext:
    """Shared context for simulation modules."""

    def __init__(self, config: SimulationConfig, run_id: str):
        # Configuration
        self.config = config
        self.run_id = run_id

        # Random number generation
        self.rng = None  # Set by rng_factory

        # Simulation state
        self.loans = []  # Set by loan_generator
        self.price_paths = {}  # Set by price_path
        self.exits = {}  # Set by exit_simulator
        self.cashflows = []  # Set by cashflow_aggregator
        self.metrics = {}  # Set by risk_metrics

        # Performance tracking
        self.start_time = time.time()
        self.module_timings = {}
```

## Development Sequence

The recommended sequence for implementing the backend modules is:

### Phase 1: Foundation
1. **config_loader**: Load and validate configuration
2. **param_registry**: Register parameters with validation rules
3. **logging_setup**: Configure structured logging
4. **metrics**: Set up Prometheus metrics
5. **feature_flags**: Implement feature flag system

### Phase 2: Core Engine
6. **rng_factory**: Create deterministic random number generators
7. **loan_generator**: Generate loan portfolios
8. **price_path**: Simulate home price appreciation
9. **exit_simulator**: Model loan exits
10. **financial**: Implement financial calculations

### Phase 3: Aggregation and Analysis
11. **fee_engine**: Calculate fees and expenses
12. **carry_engine**: Implement waterfall distribution
13. **cashflow_aggregator**: Aggregate cash flows
14. **risk_metrics**: Calculate risk metrics
15. **guardrail_monitor**: Enforce guardrails

### Phase 4: Monte Carlo and Optimization
16. **monte_carlo_outer**: Implement outer loop
17. **mc_inner_wrapper**: Implement inner loop
18. **efficient_frontier**: Calculate efficient frontier

### Phase 5: Persistence and API
19. **result_store**: Store and retrieve results
20. **db_manager**: Implement database operations
21. **s3_manager**: Implement S3 storage
22. **api_layer**: Implement API endpoints

## Testing Strategy

Each module should be tested at multiple levels:

1. **Unit Tests**: Test individual functions and classes in isolation
   - Use pytest fixtures to provide test data
   - Mock dependencies to isolate the module being tested

2. **Integration Tests**: Test interactions between modules
   - Test data flow between connected modules
   - Verify that modules work together correctly

3. **System Tests**: Test the entire simulation pipeline
   - Run end-to-end simulations with realistic configurations
   - Verify that results match expected outcomes

4. **Performance Tests**: Test system performance
   - Measure execution time for different configurations
   - Identify and optimize bottlenecks

## Performance Considerations

To ensure the simulation engine performs efficiently:

1. **Vectorization**: Use NumPy/Pandas for vectorized operations instead of loops
2. **Parallelization**: Use multiprocessing for Monte Carlo simulations
3. **Caching**: Cache intermediate results to avoid redundant calculations
4. **Memory Management**: Use generators and iterators for large datasets
5. **Profiling**: Regularly profile the code to identify bottlenecks
6. **Optimization**: Focus optimization efforts on the most time-consuming operations

Remember that premature optimization is the root of all evil. Focus on correctness first, then optimize based on profiling results.
