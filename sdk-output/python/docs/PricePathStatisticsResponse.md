# PricePathStatisticsResponse

Price path statistics response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**zone_stats** | **Dict[str, Dict[str, float]]** | Statistics by zone | 
**suburb_stats** | **Dict[str, Dict[str, float]]** | Statistics by suburb | 
**correlation_matrix** | **Dict[str, Dict[str, float]]** | Correlation matrix between zones | 

## Example

```python
from equihome_sim_sdk.models.price_path_statistics_response import PricePathStatisticsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PricePathStatisticsResponse from a JSON string
price_path_statistics_response_instance = PricePathStatisticsResponse.from_json(json)
# print the JSON string representation of the object
print(PricePathStatisticsResponse.to_json())

# convert the object into a dict
price_path_statistics_response_dict = price_path_statistics_response_instance.to_dict()
# create an instance of PricePathStatisticsResponse from a dict
price_path_statistics_response_from_dict = PricePathStatisticsResponse.from_dict(price_path_statistics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


