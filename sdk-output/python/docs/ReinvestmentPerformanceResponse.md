# ReinvestmentPerformanceResponse

Reinvestment performance response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**roi** | **float** | Return on investment for reinvested capital | 
**avg_hold_period** | **float** | Average hold period for reinvestment loans in years | 
**exit_type_distribution** | **Dict[str, float]** | Exit type distribution for reinvestment loans | 

## Example

```python
from equihome_sim_sdk.models.reinvestment_performance_response import ReinvestmentPerformanceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReinvestmentPerformanceResponse from a JSON string
reinvestment_performance_response_instance = ReinvestmentPerformanceResponse.from_json(json)
# print the JSON string representation of the object
print(ReinvestmentPerformanceResponse.to_json())

# convert the object into a dict
reinvestment_performance_response_dict = reinvestment_performance_response_instance.to_dict()
# create an instance of ReinvestmentPerformanceResponse from a dict
reinvestment_performance_response_from_dict = ReinvestmentPerformanceResponse.from_dict(reinvestment_performance_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


