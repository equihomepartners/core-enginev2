# MetricsByYear

Metrics by year model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** | Year | 
**dpi** | **float** | Distributions to Paid-In | 
**rvpi** | **float** | Residual Value to Paid-In | 
**tvpi** | **float** | Total Value to Paid-In | 
**irr** | **float** | Internal Rate of Return | 
**cash_yield** | **float** | Cash yield | 

## Example

```python
from equihome_sim_sdk.models.metrics_by_year import MetricsByYear

# TODO update the JSON string below
json = "{}"
# create an instance of MetricsByYear from a JSON string
metrics_by_year_instance = MetricsByYear.from_json(json)
# print the JSON string representation of the object
print(MetricsByYear.to_json())

# convert the object into a dict
metrics_by_year_dict = metrics_by_year_instance.to_dict()
# create an instance of MetricsByYear from a dict
metrics_by_year_from_dict = MetricsByYear.from_dict(metrics_by_year_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


