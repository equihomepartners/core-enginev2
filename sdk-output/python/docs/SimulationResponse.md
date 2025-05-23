# SimulationResponse

Simulation response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**status** | **str** | Simulation status | 
**created_at** | **str** | Creation timestamp | 

## Example

```python
from equihome_sim_sdk.models.simulation_response import SimulationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SimulationResponse from a JSON string
simulation_response_instance = SimulationResponse.from_json(json)
# print the JSON string representation of the object
print(SimulationResponse.to_json())

# convert the object into a dict
simulation_response_dict = simulation_response_instance.to_dict()
# create an instance of SimulationResponse from a dict
simulation_response_from_dict = SimulationResponse.from_dict(simulation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


