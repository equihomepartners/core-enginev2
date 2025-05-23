# MetricDefinition

Metric definition model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Metric name | 
**category** | **str** | Metric category | 
**description** | **str** | Metric description | 
**unit** | **str** | Metric unit | 
**min_value** | **float** | Minimum value | 
**max_value** | **float** | Maximum value | 
**is_higher_better** | **bool** | Whether higher values are better | [optional] 

## Example

```python
from equihome_sim_sdk.models.metric_definition import MetricDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of MetricDefinition from a JSON string
metric_definition_instance = MetricDefinition.from_json(json)
# print the JSON string representation of the object
print(MetricDefinition.to_json())

# convert the object into a dict
metric_definition_dict = metric_definition_instance.to_dict()
# create an instance of MetricDefinition from a dict
metric_definition_from_dict = MetricDefinition.from_dict(metric_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


