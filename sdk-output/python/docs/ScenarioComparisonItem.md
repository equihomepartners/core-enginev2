# ScenarioComparisonItem

Scenario comparison item model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scenario** | **str** | Scenario name | 
**metric** | **str** | Metric name | 
**value** | **float** | Metric value | 

## Example

```python
from equihome_sim_sdk.models.scenario_comparison_item import ScenarioComparisonItem

# TODO update the JSON string below
json = "{}"
# create an instance of ScenarioComparisonItem from a JSON string
scenario_comparison_item_instance = ScenarioComparisonItem.from_json(json)
# print the JSON string representation of the object
print(ScenarioComparisonItem.to_json())

# convert the object into a dict
scenario_comparison_item_dict = scenario_comparison_item_instance.to_dict()
# create an instance of ScenarioComparisonItem from a dict
scenario_comparison_item_from_dict = ScenarioComparisonItem.from_dict(scenario_comparison_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


