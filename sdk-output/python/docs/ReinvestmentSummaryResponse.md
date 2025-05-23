# ReinvestmentSummaryResponse

Reinvestment summary response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_reinvested** | **float** | Total amount reinvested | 
**num_reinvestment_events** | **int** | Number of reinvestment events | 
**avg_reinvestment_amount** | **float** | Average reinvestment amount | 
**reinvestment_by_year** | **Dict[str, float]** | Reinvestment amounts by year | 
**reinvestment_by_zone** | **Dict[str, float]** | Reinvestment amounts by zone | 
**reinvestment_by_strategy** | **Dict[str, float]** | Reinvestment amounts by strategy | 
**reinvestment_by_source** | **Dict[str, float]** | Reinvestment amounts by source | 
**reinvestment_efficiency** | [**ReinvestmentEfficiencyResponse**](ReinvestmentEfficiencyResponse.md) | Reinvestment efficiency metrics | [optional] 
**reinvestment_performance** | [**ReinvestmentPerformanceResponse**](ReinvestmentPerformanceResponse.md) | Reinvestment performance metrics | [optional] 
**reinvestment_timing** | **Dict[str, Dict[str, float]]** | Reinvestment timing by year and quarter | [optional] 
**cash_reserve_history** | **List[object]** | Cash reserve history | [optional] 
**cash_reserve_metrics** | [**CashReserveMetricsResponse**](CashReserveMetricsResponse.md) | Cash reserve metrics | [optional] 

## Example

```python
from equihome_sim_sdk.models.reinvestment_summary_response import ReinvestmentSummaryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReinvestmentSummaryResponse from a JSON string
reinvestment_summary_response_instance = ReinvestmentSummaryResponse.from_json(json)
# print the JSON string representation of the object
print(ReinvestmentSummaryResponse.to_json())

# convert the object into a dict
reinvestment_summary_response_dict = reinvestment_summary_response_instance.to_dict()
# create an instance of ReinvestmentSummaryResponse from a dict
reinvestment_summary_response_from_dict = ReinvestmentSummaryResponse.from_dict(reinvestment_summary_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


