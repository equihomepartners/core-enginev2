# Capital Allocation Module

## Overview

The Capital Allocation module is responsible for allocating capital across different zones (green, orange, red) based on the allocation policy specified in the configuration. It integrates with the TLS module to get zone data and implements allocation policy enforcement with error handling, visualization support, and progress reporting.

## Architecture

The Capital Allocation module consists of the following components:

1. **Core Allocation Logic**: Allocates capital across zones based on policy
2. **Rebalancing Logic**: Adjusts allocations if they drift from targets
3. **Validation**: Validates zone allocations against constraints
4. **Visualization**: Generates visualization data for allocation distribution
5. **Statistics**: Calculates allocation statistics
6. **Progress Reporting**: Reports progress via WebSockets
7. **Error Handling**: Provides detailed error messages with specific error codes

## API

### Core Functions

#### `allocate_capital(context: SimulationContext) -> None`

Allocates capital across zones based on policy.

**Parameters**:
- `context`: Simulation context

**Returns**:
- None

**Raises**:
- `ValidationError`: If the allocation policy is invalid

#### `rebalance_allocation(context: SimulationContext, tolerance: float = 0.05) -> Dict[str, float]`

Rebalances allocation to match target allocations.

**Parameters**:
- `context`: Simulation context
- `tolerance`: Tolerance for allocation mismatch

**Returns**:
- Dictionary of allocation adjustments by zone

#### `calculate_loan_counts(context: SimulationContext, avg_loan_size: float) -> Dict[str, int]`

Calculates the number of loans to generate for each zone.

**Parameters**:
- `context`: Simulation context
- `avg_loan_size`: Average loan size

**Returns**:
- Dictionary of loan counts by zone

#### `update_actual_allocation(context: SimulationContext) -> None`

Updates actual allocation based on generated loans.

**Parameters**:
- `context`: Simulation context

**Returns**:
- None

#### `get_zone_properties(context: SimulationContext, zone: str, limit: int = 100) -> List[Dict[str, Any]]`

Gets properties in a specific zone.

**Parameters**:
- `context`: Simulation context
- `zone`: Zone category (green, orange, red)
- `limit`: Maximum number of properties to return

**Returns**:
- List of properties in the zone

#### `get_allocation_summary(context: SimulationContext) -> Dict[str, Any]`

Gets a summary of the capital allocation.

**Parameters**:
- `context`: Simulation context

**Returns**:
- Dictionary containing allocation summary

### Utility Functions

#### `validate_zone_allocations(zone_allocations: Dict[str, float]) -> None`

Validates zone allocations.

**Parameters**:
- `zone_allocations`: Dictionary of zone allocations (zone -> percentage)

**Returns**:
- None

**Raises**:
- `ValidationError`: If the zone allocations are invalid

#### `generate_allocation_visualization(zone_allocations: Dict[str, float]) -> Dict[str, Any]`

Generates visualization data for zone allocations.

**Parameters**:
- `zone_allocations`: Dictionary of zone allocations (zone -> percentage)

**Returns**:
- Dictionary containing visualization data

#### `calculate_allocation_statistics(zone_allocations: Dict[str, float], zone_distribution: Dict[str, float]) -> Dict[str, Any]`

Calculates statistics for zone allocations.

**Parameters**:
- `zone_allocations`: Dictionary of zone allocations (zone -> percentage)
- `zone_distribution`: Dictionary of zone distribution (zone -> percentage)

**Returns**:
- Dictionary containing allocation statistics

## Integration with Other Modules

### TLS Module

The Capital Allocation module integrates with the TLS module to get zone data:

- Retrieves zone distribution from the TLS module
- Gets properties in each zone for loan generation
- Uses zone metrics for allocation statistics calculation

### Loan Generation Module

The Capital Allocation module provides input to the Loan Generation module:

- Provides zone allocations for loan generation
- Calculates loan counts by zone
- Updates actual allocation based on generated loans

### Orchestrator

The Capital Allocation module is registered with the orchestrator:

- Registered as the second module in the execution sequence (after TLS module)
- Stores intermediate results in the simulation context
- Reports progress via WebSockets

## Visualization Data

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

## Error Handling

The Capital Allocation module uses the centralized error handler to handle exceptions:

- Validates zone allocations against constraints
- Provides detailed error messages with specific error codes
- Includes context in error messages (parameters, state)
- Reports errors via WebSockets

## Progress Reporting

The Capital Allocation module reports progress via WebSockets:

- Reports progress at key stages (0%, 20%, 40%, 60%, 80%, 100%)
- Includes data payloads with intermediate results
- Supports cancellation during long-running operations

## Example Usage

```python
# Create simulation context
context = SimulationContext(config)

# Allocate capital
await allocate_capital(context)

# Get allocation summary
allocation_summary = await get_allocation_summary(context)

# Calculate loan counts
loan_counts = await calculate_loan_counts(context, avg_loan_size=500000)

# Update actual allocation after loan generation
await update_actual_allocation(context)

# Rebalance allocation if needed
adjustments = await rebalance_allocation(context, tolerance=0.05)
```
