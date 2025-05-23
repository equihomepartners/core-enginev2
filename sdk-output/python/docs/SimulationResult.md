# SimulationResult

Simulation result model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**status** | **str** | Simulation status | 
**created_at** | **str** | Creation timestamp | 
**completed_at** | **str** | Completion timestamp | [optional] 
**config** | **object** | Simulation configuration | 
**metrics** | **object** | Simulation metrics | [optional] 
**cashflows** | **List[object]** | Simulation cashflows | [optional] 
**capital_allocation** | **object** | Capital allocation | [optional] 
**loans** | **List[object]** | Generated loans | [optional] 
**loan_portfolio** | **object** | Loan portfolio | [optional] 
**execution_time** | **float** | Execution time in seconds | [optional] 
**guardrail_violations** | **List[object]** | Guardrail violations | [optional] 

## Example

```python
from equihome_sim_sdk.models.simulation_result import SimulationResult

# TODO update the JSON string below
json = "{}"
# create an instance of SimulationResult from a JSON string
simulation_result_instance = SimulationResult.from_json(json)
# print the JSON string representation of the object
print(SimulationResult.to_json())

# convert the object into a dict
simulation_result_dict = simulation_result_instance.to_dict()
# create an instance of SimulationResult from a dict
simulation_result_from_dict = SimulationResult.from_dict(simulation_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


