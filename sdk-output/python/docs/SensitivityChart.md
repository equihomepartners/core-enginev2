# SensitivityChart

Sensitivity chart model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parameter** | **str** | Parameter name | 
**values** | **List[float]** | Parameter values | 
**metric_values** | **List[float]** | Metric values | 

## Example

```python
from equihome_sim_sdk.models.sensitivity_chart import SensitivityChart

# TODO update the JSON string below
json = "{}"
# create an instance of SensitivityChart from a JSON string
sensitivity_chart_instance = SensitivityChart.from_json(json)
# print the JSON string representation of the object
print(SensitivityChart.to_json())

# convert the object into a dict
sensitivity_chart_dict = sensitivity_chart_instance.to_dict()
# create an instance of SensitivityChart from a dict
sensitivity_chart_from_dict = SensitivityChart.from_dict(sensitivity_chart_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


