# SimulationRequest

Simulation request model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | **object** | Simulation configuration | 

## Example

```python
from equihome_sim_sdk.models.simulation_request import SimulationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SimulationRequest from a JSON string
simulation_request_instance = SimulationRequest.from_json(json)
# print the JSON string representation of the object
print(SimulationRequest.to_json())

# convert the object into a dict
simulation_request_dict = simulation_request_instance.to_dict()
# create an instance of SimulationRequest from a dict
simulation_request_from_dict = SimulationRequest.from_dict(simulation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


