# SrcApiRoutersReinvestmentRiskMetricsResponse

Risk metrics response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**zone_distribution_change** | **Dict[str, float]** | Change in zone distribution | 
**avg_ltv_change** | **float** | Change in average LTV | 
**concentration_risk_change** | **Dict[str, float]** | Change in concentration risk metrics | 
**risk_score_before** | **float** | Risk score before reinvestment | 
**risk_score_after** | **float** | Risk score after reinvestment | 
**risk_score_change** | **float** | Change in risk score | 
**diversification_impact** | **float** | Impact on portfolio diversification | 
**risk_adjusted_return_impact** | **float** | Impact on risk-adjusted return | 

## Example

```python
from equihome_sim_sdk.models.src_api_routers_reinvestment_risk_metrics_response import SrcApiRoutersReinvestmentRiskMetricsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SrcApiRoutersReinvestmentRiskMetricsResponse from a JSON string
src_api_routers_reinvestment_risk_metrics_response_instance = SrcApiRoutersReinvestmentRiskMetricsResponse.from_json(json)
# print the JSON string representation of the object
print(SrcApiRoutersReinvestmentRiskMetricsResponse.to_json())

# convert the object into a dict
src_api_routers_reinvestment_risk_metrics_response_dict = src_api_routers_reinvestment_risk_metrics_response_instance.to_dict()
# create an instance of SrcApiRoutersReinvestmentRiskMetricsResponse from a dict
src_api_routers_reinvestment_risk_metrics_response_from_dict = SrcApiRoutersReinvestmentRiskMetricsResponse.from_dict(src_api_routers_reinvestment_risk_metrics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


