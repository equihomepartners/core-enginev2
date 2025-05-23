# ScenarioAnalysis

Scenario analysis model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scenarios** | [**List[ScenarioResult]**](ScenarioResult.md) | Scenario results | 

## Example

```python
from equihome_sim_sdk.models.scenario_analysis import ScenarioAnalysis

# TODO update the JSON string below
json = "{}"
# create an instance of ScenarioAnalysis from a JSON string
scenario_analysis_instance = ScenarioAnalysis.from_json(json)
# print the JSON string representation of the object
print(ScenarioAnalysis.to_json())

# convert the object into a dict
scenario_analysis_dict = scenario_analysis_instance.to_dict()
# create an instance of ScenarioAnalysis from a dict
scenario_analysis_from_dict = ScenarioAnalysis.from_dict(scenario_analysis_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


