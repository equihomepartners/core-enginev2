# ScenarioResult

Scenario result model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Scenario name | 
**description** | **str** | Scenario description | 
**metrics** | **Dict[str, float]** | Metrics for this scenario | 
**cashflows** | **List[Dict[str, float]]** | Cashflows for this scenario | 

## Example

```python
from equihome_sim_sdk.models.scenario_result import ScenarioResult

# TODO update the JSON string below
json = "{}"
# create an instance of ScenarioResult from a JSON string
scenario_result_instance = ScenarioResult.from_json(json)
# print the JSON string representation of the object
print(ScenarioResult.to_json())

# convert the object into a dict
scenario_result_dict = scenario_result_instance.to_dict()
# create an instance of ScenarioResult from a dict
scenario_result_from_dict = ScenarioResult.from_dict(scenario_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


