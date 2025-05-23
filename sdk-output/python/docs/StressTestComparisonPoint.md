# StressTestComparisonPoint

Stress test comparison chart point model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scenario** | **str** | Scenario name | 
**metric** | **str** | Metric name | 
**value** | **float** | Metric value | 
**base_value** | **float** | Base case value | 
**pct_change** | **float** | Percentage change from base case | 

## Example

```python
from equihome_sim_sdk.models.stress_test_comparison_point import StressTestComparisonPoint

# TODO update the JSON string below
json = "{}"
# create an instance of StressTestComparisonPoint from a JSON string
stress_test_comparison_point_instance = StressTestComparisonPoint.from_json(json)
# print the JSON string representation of the object
print(StressTestComparisonPoint.to_json())

# convert the object into a dict
stress_test_comparison_point_dict = stress_test_comparison_point_instance.to_dict()
# create an instance of StressTestComparisonPoint from a dict
stress_test_comparison_point_from_dict = StressTestComparisonPoint.from_dict(stress_test_comparison_point_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


