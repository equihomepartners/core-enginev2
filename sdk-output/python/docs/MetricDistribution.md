# MetricDistribution

Metric distribution model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metric_name** | **str** | Metric name | 
**category** | **str** | Metric category | 
**unit** | **str** | Metric unit | 
**min_value** | **float** | Minimum value | 
**max_value** | **float** | Maximum value | 
**mean** | **float** | Mean value | 
**median** | **float** | Median value | 
**std_dev** | **float** | Standard deviation | 
**percentiles** | **Dict[str, float]** | Percentiles (10, 25, 50, 75, 90) | 
**histogram** | **List[object]** | Histogram data | 
**by_zone** | **Dict[str, Dict[str, float]]** | Statistics by zone | 

## Example

```python
from equihome_sim_sdk.models.metric_distribution import MetricDistribution

# TODO update the JSON string below
json = "{}"
# create an instance of MetricDistribution from a JSON string
metric_distribution_instance = MetricDistribution.from_json(json)
# print the JSON string representation of the object
print(MetricDistribution.to_json())

# convert the object into a dict
metric_distribution_dict = metric_distribution_instance.to_dict()
# create an instance of MetricDistribution from a dict
metric_distribution_from_dict = MetricDistribution.from_dict(metric_distribution_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


