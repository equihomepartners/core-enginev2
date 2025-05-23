# ReinvestmentChartsResponse

Reinvestment charts response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reinvestment_timeline** | **List[object]** | Timeline of reinvestment events | 
**reinvestment_by_zone_chart** | **List[object]** | Reinvestment by zone chart | 
**reinvestment_by_year_chart** | **List[object]** | Reinvestment by year chart | 
**reinvestment_by_strategy_chart** | **List[object]** | Reinvestment by strategy chart | 
**reinvestment_by_source_chart** | **List[object]** | Reinvestment by source chart | 
**cash_reserve_chart** | **List[object]** | Cash reserve chart | 
**allocation_comparison_chart** | **List[object]** | Allocation comparison chart | 
**reinvestment_efficiency_chart** | **List[object]** | Reinvestment efficiency chart | 
**reinvestment_performance_chart** | **List[object]** | Reinvestment performance chart | 
**exit_type_distribution_chart** | **List[object]** | Exit type distribution chart | 
**reinvestment_timing_chart** | **List[object]** | Reinvestment timing chart | 
**reinvestment_vs_exits_chart** | **List[object]** | Reinvestment vs exits chart | 
**loan_size_distribution_chart** | **List[object]** | Loan size distribution chart | 

## Example

```python
from equihome_sim_sdk.models.reinvestment_charts_response import ReinvestmentChartsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReinvestmentChartsResponse from a JSON string
reinvestment_charts_response_instance = ReinvestmentChartsResponse.from_json(json)
# print the JSON string representation of the object
print(ReinvestmentChartsResponse.to_json())

# convert the object into a dict
reinvestment_charts_response_dict = reinvestment_charts_response_instance.to_dict()
# create an instance of ReinvestmentChartsResponse from a dict
reinvestment_charts_response_from_dict = ReinvestmentChartsResponse.from_dict(reinvestment_charts_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


