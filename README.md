# EQU IHOME SIM ENGINE v2

A Monte Carlo simulation engine for home equity investment funds.

## Overview

This engine simulates the performance of home equity investment funds using Monte Carlo methods. It models loan origination, home price appreciation, exits, and calculates fund-level metrics.

## Global Context

- **Product** = 10-year no-payment home-equity advances
  - 3% origination fee (GP revenue)
  - 5% simple interest, capitalised to exit
  - Appreciation share pro-rata to LTV
- **Fund terms**: 2% Mgmt Fee on committed, 20% carry over 8% hurdle
- **Monte-Carlo outer loop** = strategy sweep; inner loop = within-strategy randomness
- **100+ parameters** today → target 200+ (all wizard-driven)
  - See [Parameter Tracking Document](docs/frontend/PARAMETER_TRACKING.md) for comprehensive parameter list
  - See [Simulation Config Schema](docs/Auditapr24/simulation_config_schema.md) for canonical schema definition
- **ZERO mock data, ZERO hard-coded defaults**; everything must flow from JSONConfig

## Directory Structure

```
core-simv2/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   ├── param_registry.py
│   │   └── validation.py
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── loan_generator.py
│   │   ├── price_path.py
│   │   ├── exit_simulator.py
│   │   ├── reinvest_engine.py
│   │   ├── fee_engine.py
│   │   ├── carry_engine.py
│   │   └── cashflow_aggregator.py
│   ├── monte_carlo/
│   │   ├── __init__.py
│   │   ├── rng_factory.py
│   │   ├── monte_carlo_outer.py
│   │   ├── mc_inner_wrapper.py
│   │   └── efficient_frontier.py
│   ├── risk/
│   │   ├── __init__.py
│   │   ├── risk_metrics.py
│   │   ├── guardrail_monitor.py
│   │   └── var_calculator.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── db_manager.py
│   │   ├── s3_manager.py
│   │   └── result_store.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── dependencies.py
│   │   └── server.py
│   ├── sdk/
│   │   ├── __init__.py
│   │   ├── openapi_gen.py
│   │   └── graphql_schema.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── financial.py
│   │   ├── logging_setup.py
│   │   ├── metrics.py
│   │   └── feature_flags.py
│   └── main.py
├── schemas/
│   ├── simulation_config_schema.json  # Generated from canonical schema
│   ├── simulation_result_schema.json
│   └── schema.graphql
├── tests/
│   ├── unit/
│   │   ├── test_config_loader.py
│   │   ├── test_loan_generator.py
│   │   └── ...
│   ├── integration/
│   │   ├── test_monte_carlo.py
│   │   ├── test_api.py
│   │   └── ...
│   └── conftest.py
├── docs/
│   ├── arch_overview.md
│   ├── frontend/
│   │   └── PARAMETER_TRACKING.md  # Comprehensive parameter list
│   ├── Auditapr24/
│   │   └── simulation_config_schema.md  # Canonical schema definition
│   ├── module_contracts/
│   │   ├── config_loader.md
│   │   ├── loan_generator.md
│   │   └── ...
│   └── api_reference.md
├── ci/
│   ├── pr.yml
│   └── release.yml
├── infra/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── prometheus/
│       └── prometheus.yml
├── pyproject.toml
├── poetry.lock
├── .gitignore
├── .dockerignore
├── README.md
├── CHANGELOG.md
├── AGENTS.md
└── .env.example
```

## Module Map

1. **config_loader**: Loads and validates simulation configuration from JSON files
2. **param_registry**: Central registry for all simulation parameters with validation rules
3. **rng_factory**: Creates deterministic random number generators with proper seeding
4. **loan_generator**: Generates loan portfolios based on configuration parameters
5. **price_path**: Simulates home price appreciation paths for different zones
6. **exit_simulator**: Models loan exits (sale, refinance, default) based on market conditions
7. **reinvest_engine**: Handles reinvestment of capital during reinvestment period
8. **fee_engine**: Calculates management fees, origination fees, and other expenses
9. **carry_engine**: Implements waterfall distribution and carried interest calculations
10. **cashflow_aggregator**: Aggregates and summarizes cash flows across the portfolio
11. **monte_carlo_outer**: Orchestrates outer loop Monte Carlo simulations (strategy sweep)
12. **mc_inner_wrapper**: Manages inner loop Monte Carlo simulations (within-strategy randomness)
13. **efficient_frontier**: Calculates efficient frontier for portfolio optimization
14. **risk_metrics**: Computes risk metrics (VaR, Sharpe ratio, max drawdown)
15. **guardrail_monitor**: Enforces risk guardrails and validation rules
16. **persistence**: Handles database and S3 storage for simulation results
17. **api_layer**: FastAPI implementation for simulation API endpoints
18. **sdk_gen**: Generates client SDKs from OpenAPI and GraphQL schemas
19. **logging_setup**: Configures structured logging with trace IDs
20. **observability**: Exports Prometheus metrics for monitoring

## Cross-Cutting Concerns

- [ ] Deterministic RNG (np.random.default_rng)
- [ ] Structured logging (logfmt/JSON) with trace-id per run
- [ ] Config → dataclass → Pydantic validation
- [ ] Dependency-injection via `sim_context` object
- [ ] Metrics exported (`histogram_mc_runtime_seconds`, `counter_loans_generated`)
- [ ] Feature flags via `SIM_FEATURES=` env var
- [ ] Dockerfile + `.dockerignore`
- [ ] CI: ruff, black, mypy, pytest (unit & @slow markers)
- [ ] CHANGELOG / SemVer
- [ ] Code owners & module-level OWNERS file

## Milestone Roadmap

### Week 1: Scaffold, CI green, config schema v0.1
- Set up project structure and CI pipeline
- Implement core config loading and validation
- Create parameter registry with validation rules
- Implement logging and metrics infrastructure
- Develop basic unit tests for core components

### Week 2: Deterministic engine (loan→exit) + tests
- Implement loan generator with zone allocation
- Develop price path simulator with zone-specific appreciation
- Create exit simulator with default/refinance/sale logic
- Implement fee and carry engines
- Add comprehensive unit tests for all components

### Week 3: MC outer/inner + risk_metrics; Prometheus scrapes
- Implement Monte Carlo simulation framework
- Develop risk metrics calculation
- Add efficient frontier calculation
- Implement guardrail monitoring
- Set up Prometheus metrics export

### Week 4: API layer + SDK autogen; first Grafana dashboard
- Implement FastAPI endpoints
- Create OpenAPI and GraphQL schemas
- Generate client SDKs
- Set up persistence layer
- Create initial Grafana dashboard

## Logging Specification

- Root logger JSON: {ts, level, run_id, module, msg, extra…}
- DEBUG off by default; toggle via param wizard
- Module logs under `sim.engine.*`, `sim.mc.*`
- Error path raises `SimulationError(code, detail)` and logs `.exc_info=True`
- Log levels:
  - ERROR: Simulation failures, guardrail violations
  - WARNING: Performance issues, non-critical problems
  - INFO: Simulation progress, key metrics
  - DEBUG: Detailed calculation steps, parameter values

## Guardrails (fail fast)

- LTV_any > 85% → ValidationError
- VaR_99 > 15% → GuardrailError
- WAL > 8 yrs when strategy goal ≤ 6 yrs → warn & emit metric
- Allocation to any zone > 60% → ValidationError
- Default rate > 10% → GuardrailError
- Negative IRR → Warning & emit metric
- Equity multiple < 1.0 → Warning & emit metric

## Parameter System

The simulation engine is driven by a comprehensive parameter system with over 100 configurable parameters organized into categories:

1. **Fund Structure**: Fund size, term, vintage year, etc.
2. **Fees and Expenses**: Management fees, expense ratios, formation costs
3. **Deployment and Capital Calls**: Deployment pace, capital call schedule
4. **Reinvestment and Exit**: Reinvestment period, exit probabilities
5. **Waterfall and Returns**: Hurdle rates, carried interest, catch-up
6. **Market and Loan Parameters**: Loan sizes, terms, LTV ratios, zone allocations
7. **Leverage and Capital Structure**: Credit facilities, warehouse lines
8. **Advanced/Analytics**: Monte Carlo settings, optimization, stress testing

All parameters are:
- Strictly validated against the canonical schema
- Documented in the [Parameter Tracking Document](docs/frontend/PARAMETER_TRACKING.md)
- Defined in the [Simulation Config Schema](docs/Auditapr24/simulation_config_schema.md)
- Accessible through the parameter registry
- Configurable via JSON with no hard-coded defaults

## Architecture

```
                                 ┌───────────────┐
                                 │  API Layer    │
                                 └───────┬───────┘
                                         │
                 ┌───────────────┬───────┴───────┬───────────────┐
                 │               │               │               │
        ┌────────▼─────┐ ┌───────▼───────┐ ┌─────▼─────┐ ┌───────▼───────┐
        │ Config Layer │ │ Engine Layer  │ │ Risk Layer│ │ Persistence   │
        └────────┬─────┘ └───────┬───────┘ └─────┬─────┘ └───────────────┘
                 │               │               │
                 │       ┌───────▼───────┐       │
                 └───────► Monte Carlo   ◄───────┘
                         └───────────────┘
```

## Environment & Setup

- Python 3.11
- Poetry for dependency management
- FastAPI for API layer
- NumPy/Pandas for numerical computations
- Pydantic for data validation

### Setup Commands
```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run linting
poetry run ruff check .
poetry run black --check .
poetry run mypy .

# Run the simulation
poetry run python -m src.main --config config.json

# Start the API server
poetry run python -m src.api.server
```

## Coding Style Rules
- Max 400 loc per file, 120 col width
- Google docstrings + doctest example where math shown
- `np.random.Generator` passed via context; no global `seed`
- No local state mutations across threads
- Tests: fast (≤ 2 s) default; Monte-Carlo heavy marked @slow

## Quick Start

1. Clone the repository
2. Install dependencies: `poetry install`
3. Run a simulation: `poetry run python -m src.main --config config.json`
4. View results: `poetry run python -m src.main --results latest`
5. Start the API server: `poetry run python -m src.api.server`
