# ReinvestmentKPIsResponse

Reinvestment KPIs response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_reinvested** | **float** | Total amount reinvested | 
**num_reinvestment_events** | **int** | Number of reinvestment events | 
**avg_reinvestment_amount** | **float** | Average reinvestment amount | 
**reinvestment_ratio** | **float** | Ratio of reinvested capital to total exit value | 
**avg_time_to_reinvest** | **float** | Average time between exit and reinvestment in months | 
**reinvestment_roi** | **float** | Return on investment for reinvested capital | 
**num_reinvestment_loans** | **int** | Number of reinvestment loans | 
**reinvestment_portfolio_impact** | **float** | Percentage of portfolio from reinvestment | 
**risk_metrics** | [**SrcApiRoutersReinvestmentRiskMetricsResponse**](SrcApiRoutersReinvestmentRiskMetricsResponse.md) | Risk impact metrics | [optional] 

## Example

```python
from equihome_sim_sdk.models.reinvestment_kpis_response import ReinvestmentKPIsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReinvestmentKPIsResponse from a JSON string
reinvestment_kpis_response_instance = ReinvestmentKPIsResponse.from_json(json)
# print the JSON string representation of the object
print(ReinvestmentKPIsResponse.to_json())

# convert the object into a dict
reinvestment_kpis_response_dict = reinvestment_kpis_response_instance.to_dict()
# create an instance of ReinvestmentKPIsResponse from a dict
reinvestment_kpis_response_from_dict = ReinvestmentKPIsResponse.from_dict(reinvestment_kpis_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


