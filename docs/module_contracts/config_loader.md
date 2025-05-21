# Config Loader Module Contract

## Purpose

The `config_loader` module is responsible for loading, validating, and providing access to simulation configuration parameters. It ensures that all configuration values are properly validated against the schema and converted to appropriate types.

## Interfaces

### Public Functions

```python
def load_config(config_path: str) -> SimulationConfig:
    """
    Load and validate a simulation configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration JSON file
        
    Returns:
        A validated SimulationConfig object
        
    Raises:
        ConfigValidationError: If the configuration is invalid
        FileNotFoundError: If the configuration file does not exist
    """
```

```python
def load_config_from_dict(config_dict: Dict[str, Any]) -> SimulationConfig:
    """
    Load and validate a simulation configuration from a dictionary.
    
    Args:
        config_dict: Dictionary containing configuration parameters
        
    Returns:
        A validated SimulationConfig object
        
    Raises:
        ConfigValidationError: If the configuration is invalid
    """
```

```python
def get_default_config() -> SimulationConfig:
    """
    Get a default simulation configuration with all parameters set to their default values.
    
    Returns:
        A default SimulationConfig object
    """
```

### Data Models

```python
@dataclass
class SimulationConfig:
    """
    Simulation configuration parameters.
    
    Attributes:
        fund_size: Fund size in dollars
        fund_term: Fund term in years
        vintage_year: Fund vintage year
        gp_commitment_percentage: GP commitment percentage (0-1)
        hurdle_rate: Hurdle rate (0-1)
        carried_interest_rate: Carried interest rate (0-1)
        waterfall_structure: Waterfall structure type ("european" or "american")
        management_fee_rate: Management fee rate (0-1)
        management_fee_basis: Basis for management fee calculation
        catch_up_rate: GP catch-up rate (0-1)
        reinvestment_period: Reinvestment period in years
        avg_loan_size: Average loan size in dollars
        loan_size_std_dev: Standard deviation of loan sizes
        min_loan_size: Minimum loan size in dollars
        max_loan_size: Maximum loan size in dollars
        avg_loan_term: Average loan term in years
        avg_loan_interest_rate: Average loan interest rate (0-1)
        avg_loan_ltv: Average loan LTV ratio (0-1)
        ltv_std_dev: Standard deviation of LTV ratios
        min_ltv: Minimum LTV ratio (0-1)
        max_ltv: Maximum LTV ratio (0-1)
        avg_loan_exit_year: Average loan exit year
        exit_year_std_dev: Standard deviation of exit years
        zone_allocations: Target zone allocations
        appreciation_rates: Zone-specific appreciation rates
        default_rates: Zone-specific default rates
        recovery_rates: Zone-specific recovery rates
    """
```

## Dependencies

- `src.config.validation`: For validating configuration parameters
- `src.config.param_registry`: For registering parameters and their validation rules
- `src.utils.logging_setup`: For logging configuration loading events

## Error Handling

- `ConfigValidationError`: Raised when configuration validation fails
- `ConfigLoadError`: Raised when configuration loading fails
- `ConfigSchemaError`: Raised when the configuration schema is invalid

## Performance Characteristics

- Loading and validating a configuration should take less than 100ms
- Memory usage should be proportional to the size of the configuration

## Thread Safety

- This module is thread-safe
- The returned `SimulationConfig` object is immutable

## Example Usage

```python
from src.config.config_loader import load_config

# Load a configuration from a file
config = load_config("config.json")

# Access configuration parameters
fund_size = config.fund_size
fund_term = config.fund_term

# Use the configuration in a simulation
simulation = Simulation(config)
results = simulation.run()
```

## Testing

- Unit tests should cover all validation rules
- Edge cases should be tested (min/max values, invalid values)
- Performance tests should ensure loading time is acceptable
