# StressTestRequest

Request model for stress testing.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**scenarios** | [**List[StressTestScenario]**](StressTestScenario.md) | Stress test scenarios | 

## Example

```python
from equihome_sim_sdk.models.stress_test_request import StressTestRequest

# TODO update the JSON string below
json = "{}"
# create an instance of StressTestRequest from a JSON string
stress_test_request_instance = StressTestRequest.from_json(json)
# print the JSON string representation of the object
print(StressTestRequest.to_json())

# convert the object into a dict
stress_test_request_dict = stress_test_request_instance.to_dict()
# create an instance of StressTestRequest from a dict
stress_test_request_from_dict = StressTestRequest.from_dict(stress_test_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


