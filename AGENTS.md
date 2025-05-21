# Agent Guidelines for EQU IHOME SIM ENGINE v2

## Environment
- Python 3.11
- Poetry for dependency management
- FastAPI for API layer
- NumPy/Pandas for numerical computations
- Pydantic for data validation

## Setup Commands
- Install dependencies: `poetry install`
- Run tests: `poetry run pytest`
- Run linting: `poetry run ruff check .`
- Run type checking: `poetry run mypy .`
- Run formatting: `poetry run black .`
- Run the simulation: `poetry run python -m src.main --config config.json`
- Start the API server: `poetry run python -m src.api.server`

## Plan-Approval Process
- All significant changes require a plan to be approved before implementation
- Plans should include:
  - Problem statement
  - Proposed solution
  - Files to be modified
  - Tests to be added/modified
  - Potential risks and mitigations

## Guardrails & PR Checklist

### Code Quality
- [ ] Code follows the Google Python Style Guide
- [ ] Maximum 400 lines of code per file
- [ ] Maximum 120 characters per line
- [ ] All functions have Google-style docstrings
- [ ] Complex math functions include doctest examples
- [ ] No global state mutations
- [ ] Deterministic RNG passed via context
- [ ] No hardcoded defaults (everything from config)

### Testing
- [ ] Unit tests cover all new functionality
- [ ] Integration tests for complex interactions
- [ ] Monte Carlo tests marked with @slow decorator
- [ ] Fast tests run in under 2 seconds
- [ ] Test coverage maintained or improved

### Security & Performance
- [ ] No sensitive information in logs or errors
- [ ] Proper error handling and validation
- [ ] Performance considerations documented
- [ ] Resource usage (memory, CPU) reasonable

### Documentation
- [ ] Module contracts updated
- [ ] API documentation updated
- [ ] CHANGELOG.md updated
- [ ] README.md updated if necessary

## Key Principles

### Configuration
- All parameters must be loaded from configuration
- No hardcoded defaults in business logic
- All parameters must be validated
- Configuration schema must be documented

### Randomness
- All random number generation must use the provided RNG factory
- RNG must be seeded deterministically for reproducibility
- RNG instances must be passed via context, not created locally

### Logging
- Use structured logging (JSON format)
- Include trace_id in all logs
- Use appropriate log levels
- Do not log sensitive information

### Error Handling
- Use custom exception types
- Provide detailed error messages
- Log exceptions with context
- Fail fast on invalid inputs

### Testing
- Write unit tests for all components
- Use pytest fixtures for common setup
- Mark slow tests with @slow decorator
- Use parameterized tests for edge cases

### Performance
- Profile code for bottlenecks
- Use vectorized operations where possible
- Minimize memory usage
- Consider parallelization for Monte Carlo simulations

## Module Contracts

Each module should have a clear contract defining:
- Inputs and outputs
- Preconditions and postconditions
- Error conditions
- Performance characteristics
- Thread safety guarantees

## Metrics & Observability

The following metrics should be exported:
- `histogram_mc_runtime_seconds`: Runtime of Monte Carlo simulations
- `counter_loans_generated`: Number of loans generated
- `gauge_active_simulations`: Number of active simulations
- `histogram_irr_distribution`: Distribution of IRR values
- `gauge_memory_usage_bytes`: Memory usage of the simulation
- `counter_guardrail_violations`: Number of guardrail violations

## Feature Flags

Feature flags are controlled via the `SIM_FEATURES` environment variable:
- `ENABLE_PARALLEL`: Enable parallel processing
- `ENABLE_CACHE`: Enable caching of intermediate results
- `ENABLE_PROMETHEUS`: Enable Prometheus metrics export
- `ENABLE_DEBUG_LOGGING`: Enable debug logging
- `ENABLE_ADVANCED_RISK`: Enable advanced risk metrics
