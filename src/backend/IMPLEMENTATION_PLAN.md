# EQU IHOME SIM ENGINE v2 - Backend Implementation Plan

This document outlines the comprehensive implementation plan for the EQU IHOME SIM ENGINE v2 backend. It provides a phased approach with detailed checklists for each component.

## ⚠️ IMPORTANT: Module Implementation Rules ⚠️

To maintain a clean architecture with no redundancy, follow these rules for all module implementations:

### Required Updates for Each Module

1. **Master Schemas (Required)**
   - Update `/schemas/simulation_config_schema.json` for input parameters
   - Update `/schemas/simulation_result_schema.json` for output results
   - These are the SINGLE SOURCE OF TRUTH for all data structures

2. **API Routes (Required)**
   - Create `src/api/routers/your_module.py` (not in routes directory)
   - Define FastAPI endpoints for your module's functionality
   - Define Pydantic models DIRECTLY in this file (not as separate schema files)
   - Group related endpoints by functional area, not by module

3. **WebSocket Integration (Required)**
   - Use the existing WebSocket manager from `src/api/websocket_manager.py`
   - Call `send_progress()` for progress updates (percentage, stage, message)
   - Call `send_message()` for intermediate results (partial data)
   - Call `send_info()` for informational messages
   - Call `send_warning()` for warning messages
   - Call `send_error()` for error reporting
   - Call `send_result()` for final results
   - Add cancellation checks with `check_cancelled()`
   - Use the WebSocket router in `src/api/routers/websocket.py` for client connections

4. **Orchestrator Integration (Required)**
   - Register your module in `src/engine/orchestrator.py`
   - Add your module to the execution sequence

5. **Module Documentation (Required)**
   - Create `src/your_module/README.md`
   - Document functionality, architecture, and API

6. **Implementation Plan (Required)**
   - Check off tasks as they are completed

7. **Module Core Implementation (Required)**
   - Create `src/your_module/your_module_core.py`
   - Include visualization methods DIRECTLY in this file

### API Organization

1. **One master FastAPI app**
   - `src/api/server.py` instantiates a single FastAPI() object
   - All routers are mounted on this app with appropriate prefixes

2. **One router per functional area, not per module**
   - Example: `src/api/routers/simulation.py`, `src/api/routers/risk.py`, `src/api/routers/tls.py`
   - A router groups related paths and mounts them on the master app

3. **No new top-level file for each engine module**
   - If you create a new engine module, extend an existing router or add a sub-router
   - Don't create a new router file for each low-level engine module

4. **Single OpenAPI spec generation**
   - All routers are included in the master app, so one OpenAPI spec is generated
   - This is what the SDK is generated from

5. **WebSocket communication**
   - Use the WebSocket router in `src/api/routers/websocket.py` for all WebSocket endpoints
   - Use the WebSocket manager in `src/api/websocket_manager.py` for all WebSocket communication
   - Follow the standard message format for all WebSocket messages:
     ```json
     {
       "type": "progress|info|warning|error|result|message",
       "simulation_id": "unique-simulation-id",
       "timestamp": "ISO-8601-timestamp",
       "data": { ... }
     }
     ```
   - Support client-initiated cancellation through WebSocket messages

### What NOT to Create (Avoid Redundancy)

1. **DO NOT create separate schema files** (`src/schemas/your_module_schema.py`)
   - Instead, define Pydantic models directly in your router file

2. **DO NOT create separate SDK client files** (`src/sdk/your_module_client.py`)
   - The SDK will be generated from the OpenAPI specification

3. **DO NOT create separate visualization files** (`src/your_module/visualization.py`)
   - Instead, add visualization methods directly to your module's core class

4. **DO NOT create new route files for each module** (`src/api/routes/your_module_routes.py`)
   - Instead, add endpoints to existing functional area routers or create new functional area routers

## Table of Contents
- [Phase 1: Foundation](#phase-1-foundation)
- [Phase 2: Core Engine](#phase-2-core-engine)
- [Phase 3: Aggregation and Analysis](#phase-3-aggregation-and-analysis)
- [Phase 4: Monte Carlo and Optimization](#phase-4-monte-carlo-and-optimization)
- [Phase 5: Persistence and API](#phase-5-persistence-and-api)
- [Phase 6: Testing and Documentation](#phase-6-testing-and-documentation)
- [Phase 7: Performance Optimization](#phase-7-performance-optimization)

## Phase 1: Foundation

This phase establishes the basic infrastructure and configuration components.

### Directory Structure
- [x] Create basic directory structure
- [x] Set up `__init__.py` files in each directory

### Configuration Module
- [x] Implement `config_loader.py` for loading and validating configuration
- [x] Implement `param_registry.py` for parameter registration and validation
- [x] Implement `validation.py` for schema validation

### Utility Module
- [x] Implement `logging_setup.py` for structured logging
- [x] Implement `metrics.py` for Prometheus metrics
- [x] Implement `feature_flags.py` for feature toggles
- [x] Implement `financial.py` for financial calculations

### Error Handling
- [x] Implement `error_handler.py` for centralized error handling
- [x] Define error categories and error codes
- [x] Implement context-rich error messages
- [x] Add error formatting for API responses

### Real-time Progress Tracking
- [x] Implement `websocket_manager.py` for WebSocket support
- [x] Add progress tracking to orchestrator
- [x] Implement intermediate results during simulation
- [x] Add cancellation support for long-running simulations

### Simulation Context
- [x] Create `simulation_context.py` for shared state between modules
- [x] Implement context initialization and tracking methods
- [x] Add module-specific results storage for intermediate results

### Orchestration
- [x] Create `orchestrator.py` for coordinating module execution
- [x] Implement module registration and execution sequence
- [x] Add progress reporting and WebSocket integration
- [x] Update API server to use orchestrator

### Documentation
- [x] Create backend README.md with architecture overview
- [x] Create implementation plan document

## Phase 2: Core Engine

This phase implements the core simulation engine components.

### Cross-Cutting Requirements for All Modules

Each module in this phase must implement the following:

1. **Error Handling**:
   - Use the centralized error handler for all exceptions
   - Define module-specific error codes and messages
   - Include context in error messages (parameters, state)

2. **Logging**:
   - Log entry and exit of major functions
   - Log parameter values and decisions
   - Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
   - Include structured context in log messages

3. **Progress Reporting**:
   - Store intermediate results in the simulation context
   - Support cancellation checks during long operations
   - Report progress percentage for long-running operations

4. **Visualization Support**:
   - Provide methods to generate visualization data
   - Include statistical summaries of outputs
   - Support exporting data in formats suitable for charts

5. **Testing Support**:
   - Include deterministic mode for reproducible tests
   - Provide methods to validate outputs
   - Support mocking of dependencies

### Random Number Generation
- [x] Implement `rng_factory.py` for deterministic RNG
- [x] Implement correlated RNG generation
- [x] Add RNG state persistence for reproducibility
- [x] Add variation factor control
- [x] Add deterministic mode toggle
- [x] Implement batch generation for performance
- [x] Add distribution visualization support
- [x] Implement custom distribution support
- [x] Add statistical analysis of distributions

### TLS Module
- [x] Implement `tls_module.py` for zone classification
- [x] Add mock zone data provider with 100+ suburbs and 6,900+ properties
- [x] Implement zone attribute lookup with rich metrics
- [x] Add caching for zone data with fallback mechanisms
- [x] Add visualization support for zone distribution
- [x] Implement zone statistics calculation
- [x] Add progress reporting for zone data loading
- [x] Implement error handling for missing/invalid zones
- [x] Add property-level variation with detailed attributes
- [x] Implement correlation analysis between metrics and suburbs
- [x] Add comprehensive REST API endpoints for TLS data
- [x] Create SDK client for TLS module integration
- [x] Add detailed documentation with README and API docs
- [x] Implement unit-level metrics with 50+ metrics across 7 categories

### Capital Allocation
- [x] Implement `capital_allocator.py` for zone allocation
- [x] Add target allocation calculation
- [x] Implement allocation policy enforcement
- [x] Add rebalancing logic
- [x] Add visualization support for allocation distribution
- [x] Implement allocation statistics calculation
- [x] Add progress reporting for allocation calculation
- [x] Implement error handling for allocation constraints

### Loan Generation
- [x] Implement basic `loan_generator.py` for creating loan portfolios
- [x] Add zone-based loan allocation
- [x] Implement loan characteristic distributions
- [x] Add loan ID generation and tracking
- [x] Add visualization support for loan characteristics
- [x] Implement loan statistics calculation
- [x] Add progress reporting for loan generation
- [x] Implement error handling for loan constraints
- [x] Add support for reinvestment loan generation
- [x] Implement loan portfolio history tracking
- [x] Add portfolio turnover visualization
- [x] Implement rebalancing recommendation API

### Price Path Simulation
- [x] Implement `price_path.py` for home price appreciation simulation
- [x] Add zone-specific appreciation rates
- [x] Implement stochastic price path models
- [x] Add correlation between zone price paths
- [x] Add visualization support for price paths
- [x] Add multiple stochastic models (GBM, mean-reversion, regime-switching)
- [x] Implement suburb-level and property-level price paths
- [x] Add comprehensive visualization support
- [x] Implement price path statistics calculation
- [x] Add API endpoints for price path data
- [x] Add progress reporting for price path simulation
- [x] Implement error handling for price path constraints
- [x] Implement enhanced price path simulator with TLS integration
- [x] Add Sydney-specific property market cycle model
- [x] Implement property-specific factors (type, bedrooms, land size, age)
- [x] Add economic factor integration (interest rates, employment, population)
- [x] Implement enhanced visualization and statistics
- [x] Add zone and suburb allocation recommendations

### Exit Simulation
- [x] Implement `exit_simulator.py` for modeling loan exits
- [x] Add sale, refinance, and default exit types
- [x] Implement exit timing distributions
- [x] Add correlation between exits
- [x] Add visualization support for exit distributions
- [x] Implement exit statistics calculation
- [x] Add progress reporting for exit simulation
- [x] Implement error handling for exit constraints
- [x] Implement time-based and price-based exit probability models
- [x] Add economic factor integration for default probability
- [x] Implement tiered appreciation sharing
- [x] Add comprehensive exit statistics calculation
- [x] Implement exit scenario testing
- [x] Add API endpoints for exit simulation
- [x] Implement enhanced exit simulator with behavioral models
- [x] Add economic integration with macroeconomic scenario testing
- [x] Implement cohort analysis (vintage, LTV, zone)
- [x] Add risk metrics (VaR, stress testing, tail risk)
- [x] Implement machine learning integration (clustering, prediction, anomaly detection)
- [x] Add geospatial visualization for exits
- [x] Implement comparative visualizations
- [x] Add enhanced API endpoints for exit simulation

### Reinvestment Engine
- [ ] Implement `reinvest_engine.py` for capital reinvestment
- [ ] Add reinvestment period constraints
- [ ] Implement reinvestment strategies
- [ ] Add reinvestment tracking
- [ ] Add visualization support for reinvestment activity
- [ ] Implement reinvestment statistics calculation
- [ ] Add progress reporting for reinvestment simulation
- [ ] Implement error handling for reinvestment constraints

### Leverage Engine
- [ ] Implement `leverage_engine.py` for debt facility management
- [ ] Add NAV line facility implementation
- [ ] Implement subscription line facility
- [ ] Add borrowing base tests
- [ ] Implement interest calculation
- [ ] Add visualization support for leverage metrics
- [ ] Implement leverage statistics calculation
- [ ] Add progress reporting for leverage simulation
- [ ] Implement error handling for leverage constraints

## Phase 3: Aggregation and Analysis

This phase implements components for aggregating and analyzing simulation results.

### Fee Engine
- [ ] Implement `fee_engine.py` for calculating fees and expenses
- [ ] Add management fee calculation
- [ ] Implement origination fee calculation
- [ ] Add expense calculation

### Cashflow Aggregation
- [ ] Implement `cashflow_aggregator.py` for aggregating cash flows
- [ ] Add loan-level cash flow calculation
- [ ] Implement fund-level cash flow aggregation
- [ ] Add time-based cash flow reporting

### Waterfall Engine
- [ ] Implement `waterfall_engine.py` for waterfall distribution
- [ ] Add hurdle rate calculation
- [ ] Implement carried interest calculation
- [ ] Add catch-up calculation
- [ ] Implement multi-tier waterfall rules
- [ ] Add clawback handling

### Tranche Manager
- [ ] Implement `tranche_manager.py` for tranche management
- [ ] Add tranche definition and configuration
- [ ] Implement cash flow allocation by tranche
- [ ] Add tranche-specific metrics calculation
- [ ] Implement tranche waterfall rules

### Risk Metrics
- [ ] Implement `risk_metrics.py` for calculating risk metrics
- [ ] Add IRR calculation
- [ ] Implement equity multiple calculation
- [ ] Add VaR calculation
- [ ] Implement Sharpe ratio calculation
- [ ] Add max drawdown calculation

### Guardrail Monitoring
- [ ] Implement `guardrail_monitor.py` for enforcing guardrails
- [ ] Add LTV guardrail
- [ ] Implement zone allocation guardrail
- [ ] Add WAL guardrail
- [ ] Implement default rate guardrail
- [ ] Add IRR guardrail
- [ ] Implement leverage utilization guardrail
- [ ] Add tranche shortfall guardrail

### Performance Reporter
- [ ] Implement `performance_reporter.py` for generating reports
- [ ] Add KPI table generation
- [ ] Implement zone allocation reporting
- [ ] Add cash flow visualization
- [ ] Implement risk metric reporting
- [ ] Add export to CSV/Excel/Markdown

## Phase 4: Monte Carlo and Optimization

This phase implements Monte Carlo simulation and optimization components.

### Scenario Builder
- [ ] Implement `scenario_builder.py` for scenario definition
- [ ] Add YAML/JSON scenario parsing
- [ ] Implement parameter override handling
- [ ] Add scenario validation

### Monte Carlo Outer Loop
- [ ] Implement `monte_carlo_outer.py` for strategy sweep
- [ ] Add parameter variation
- [ ] Implement simulation tracking
- [ ] Add result aggregation
- [ ] Implement scenario execution

### Monte Carlo Inner Loop
- [ ] Implement `mc_inner_wrapper.py` for within-strategy randomness
- [ ] Add inner loop parameter variation
- [ ] Implement inner loop result tracking
- [ ] Add inner loop aggregation

### Efficient Frontier
- [ ] Implement `efficient_frontier.py` for portfolio optimization
- [ ] Add risk-return calculation
- [ ] Implement efficient frontier generation
- [ ] Add optimal portfolio selection

### Fund Registry
- [ ] Implement `fund_registry.py` for multi-fund simulation
- [ ] Add fund configuration management
- [ ] Implement fund context creation
- [ ] Add fund result aggregation

## Phase 5: Persistence and API

This phase implements components for storing and retrieving simulation results.

### Result Store
- [ ] Implement `result_store.py` for storing simulation results
- [ ] Add result serialization
- [ ] Implement result retrieval
- [ ] Add result caching

### Database Manager
- [ ] Implement `db_manager.py` for database operations
- [ ] Add database connection management
- [ ] Implement database schema
- [ ] Add CRUD operations

### S3 Manager
- [ ] Implement `s3_manager.py` for S3 storage
- [ ] Add S3 connection management
- [ ] Implement file upload/download
- [ ] Add file listing

### API Layer
- [x] Implement basic `server.py` for FastAPI server
- [x] Organize API by functional area (not by module)
- [x] Create routers for different functional areas
- [x] Define Pydantic models directly in router files
- [x] Add simulation endpoints
- [x] Implement TLS endpoints
- [x] Add WebSocket endpoints
- [x] Add parameter validation
- [x] Implement error handling
- [ ] Add authentication and authorization

### SDK Generation
- [ ] Implement `openapi_gen.py` for OpenAPI specification
- [ ] Add client SDK generation
- [ ] Implement GraphQL schema
- [ ] Add GraphQL resolvers

## Phase 6: Testing and Documentation

This phase implements comprehensive testing and documentation.

### Unit Tests
- [ ] Add tests for config module
- [ ] Implement tests for engine module
- [ ] Add tests for monte_carlo module
- [ ] Implement tests for risk module
- [ ] Add tests for persistence module
- [ ] Implement tests for api module

### Integration Tests
- [ ] Add tests for end-to-end simulation
- [ ] Implement tests for API endpoints
- [ ] Add tests for database operations
- [ ] Implement tests for S3 operations

### Performance Tests
- [ ] Add tests for simulation performance
- [ ] Implement tests for API performance
- [ ] Add tests for database performance
- [ ] Implement tests for S3 performance

### Documentation
- [ ] Add docstrings to all modules
- [ ] Implement API documentation
- [ ] Add architecture documentation
- [ ] Implement user guide
- [ ] Add developer guide

## Phase 7: Performance Optimization

This phase optimizes the performance of the simulation engine.

### Profiling
- [ ] Add profiling for simulation engine
- [ ] Implement profiling for API endpoints
- [ ] Add profiling for database operations
- [ ] Implement profiling for S3 operations

### Optimization
- [ ] Optimize loan generation
- [ ] Implement price path optimization
- [ ] Add exit simulation optimization
- [ ] Implement cashflow aggregation optimization
- [ ] Add risk metric calculation optimization

### Parallelization
- [ ] Add parallel loan generation
- [ ] Implement parallel price path simulation
- [ ] Add parallel exit simulation
- [ ] Implement parallel Monte Carlo simulation

### Caching
- [ ] Add result caching
- [ ] Implement parameter caching
- [ ] Add intermediate result caching
- [ ] Implement API response caching

## Progress Tracking

| Phase | Total Tasks | Completed | Progress |
|-------|-------------|-----------|----------|
| Phase 1: Foundation | 23 | 23 | 100% |
| Phase 2: Core Engine | 99 | 88 | 88.9% |
| Phase 3: Aggregation and Analysis | 30 | 0 | 0% |
| Phase 4: Monte Carlo and Optimization | 17 | 0 | 0% |
| Phase 5: Persistence and API | 20 | 9 | 45% |
| Phase 6: Testing and Documentation | 16 | 0 | 0% |
| Phase 7: Performance Optimization | 16 | 0 | 0% |
| **Total** | **221** | **120** | **54.3%** |

## Next Steps

1. ✅ **Complete the implementation of the TLS Module**:
   - ✅ Implement `tls_module.py` for zone classification
   - ✅ Add mock zone data provider with visualization support
   - ✅ Implement zone attribute lookup with caching
   - ✅ Add error handling for missing/invalid zones
   - ✅ Implement progress reporting for zone data loading
   - ✅ Add property-level variation with detailed attributes
   - ✅ Implement correlation analysis between metrics and suburbs
   - ✅ Add comprehensive REST API endpoints for TLS data
   - ✅ Create SDK client for TLS module integration

2. ✅ **Implement the Capital Allocator**:
   - ✅ Implement `capital_allocator.py` for zone allocation
   - ✅ Add target allocation calculation with visualization support
   - ✅ Implement allocation policy enforcement with error handling
   - ✅ Add rebalancing logic with progress reporting
   - ✅ Implement allocation statistics calculation
   - ✅ Add allocation history tracking with visualization

3. ✅ **Enhance the Loan Generation Module**:
   - ✅ Implement `loan_generator.py` for creating loan portfolios
   - ✅ Add zone-based loan allocation with visualization support
   - ✅ Implement loan characteristic distributions with error handling
   - ✅ Add progress reporting for loan generation
   - ✅ Implement loan statistics calculation
   - ✅ Add support for reinvestment loan generation
   - ✅ Implement loan portfolio history tracking
   - ✅ Add portfolio turnover visualization
   - ✅ Implement rebalancing recommendation API

4. ✅ **Complete the Price Path Simulator**:
   - ✅ Implement `price_path.py` for home price appreciation simulation
   - ✅ Add zone-specific appreciation rates with visualization support
   - ✅ Implement stochastic price path models with error handling
   - ✅ Add correlation between zone price paths
   - ✅ Implement progress reporting for price path simulation
   - ✅ Add multiple stochastic models (GBM, mean-reversion, regime-switching)
   - ✅ Implement suburb-level and property-level price paths
   - ✅ Add comprehensive visualization support
   - ✅ Implement price path statistics calculation
   - ✅ Add API endpoints for price path data
   - ✅ Implement enhanced price path simulator with TLS integration
   - ✅ Add Sydney-specific property market cycle model
   - ✅ Implement property-specific factors (type, bedrooms, land size, age)
   - ✅ Add economic factor integration (interest rates, employment, population)
   - ✅ Implement enhanced visualization and statistics
   - ✅ Add zone and suburb allocation recommendations

5. ✅ **Implement the Exit Simulator**:
   - ✅ Implement `exit_simulator.py` for modeling loan exits
   - ✅ Add sale, refinance, and default exit types with visualization support
   - ✅ Implement exit timing distributions with error handling
   - ✅ Add correlation between exits with progress reporting
   - ✅ Implement exit statistics calculation
   - ✅ Implement time-based and price-based exit probability models
   - ✅ Add economic factor integration for default probability
   - ✅ Implement tiered appreciation sharing
   - ✅ Add comprehensive exit statistics calculation
   - ✅ Implement exit scenario testing
   - ✅ Add API endpoints for exit simulation
   - ✅ Implement enhanced exit simulator with behavioral models
   - ✅ Add economic integration with macroeconomic scenario testing
   - ✅ Implement cohort analysis (vintage, LTV, zone)
   - ✅ Add risk metrics (VaR, stress testing, tail risk)
   - ✅ Implement machine learning integration (clustering, prediction, anomaly detection)
   - ✅ Add geospatial visualization for exits
   - ✅ Implement comparative visualizations
   - ✅ Add enhanced API endpoints for exit simulation

6. **Implement the Reinvestment Engine**:
   - Implement `reinvest_engine.py` for capital reinvestment
   - Add reinvestment period constraints with visualization support
   - Implement reinvestment strategies with error handling
   - Add reinvestment tracking with progress reporting
   - Implement reinvestment statistics calculation

7. **Implement the Leverage Engine**:
   - Implement `leverage_engine.py` for debt facility management
   - Add NAV line and subscription line facilities with visualization support
   - Implement borrowing base tests with error handling
   - Add interest calculation with progress reporting
   - Implement leverage statistics calculation

8. **Begin implementing the aggregation and analysis components**:
   - Implement `fee_engine.py` for fee calculation
   - Implement `cashflow_aggregator.py` for cash flow aggregation
   - Implement `waterfall_engine.py` for waterfall distribution
   - Implement `tranche_manager.py` for tranche management

9. **Ensure cross-cutting requirements are met for all modules**:
   - Verify error handling using the centralized error handler
   - Confirm appropriate logging at all levels
   - Check progress reporting for long-running operations
   - Validate visualization support for all key outputs
   - Test cancellation support for all modules

10. **Write unit tests for completed components**:
   - Test normal operation paths
   - Test error handling paths
   - Test visualization data generation
   - Test progress reporting
   - Test cancellation handling

11. **Update the API server documentation**:
    - Document WebSocket endpoints
    - Provide examples of progress tracking
    - Document error response formats
    - Include visualization data endpoints
