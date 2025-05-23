# CashReserveMetricsResponse

Cash reserve metrics response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**avg_cash_reserve** | **float** | Average cash reserve | 
**min_cash_reserve** | **float** | Minimum cash reserve | 
**max_cash_reserve** | **float** | Maximum cash reserve | 
**avg_cash_reserve_pct** | **float** | Average cash reserve as percentage of fund size | 
**min_cash_reserve_pct** | **float** | Minimum cash reserve as percentage of fund size | 
**max_cash_reserve_pct** | **float** | Maximum cash reserve as percentage of fund size | 

## Example

```python
from equihome_sim_sdk.models.cash_reserve_metrics_response import CashReserveMetricsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CashReserveMetricsResponse from a JSON string
cash_reserve_metrics_response_instance = CashReserveMetricsResponse.from_json(json)
# print the JSON string representation of the object
print(CashReserveMetricsResponse.to_json())

# convert the object into a dict
cash_reserve_metrics_response_dict = cash_reserve_metrics_response_instance.to_dict()
# create an instance of CashReserveMetricsResponse from a dict
cash_reserve_metrics_response_from_dict = CashReserveMetricsResponse.from_dict(cash_reserve_metrics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


