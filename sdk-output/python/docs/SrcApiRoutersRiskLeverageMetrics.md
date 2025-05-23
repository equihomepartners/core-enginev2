# SrcApiRoutersRiskLeverageMetrics

Leverage metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**nav_utilisation** | **float** | NAV utilisation | 
**interest_coverage** | **float** | Interest coverage ratio | 
**var_uplift** | **object** | VaR uplift from leverage | 

## Example

```python
from equihome_sim_sdk.models.src_api_routers_risk_leverage_metrics import SrcApiRoutersRiskLeverageMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of SrcApiRoutersRiskLeverageMetrics from a JSON string
src_api_routers_risk_leverage_metrics_instance = SrcApiRoutersRiskLeverageMetrics.from_json(json)
# print the JSON string representation of the object
print(SrcApiRoutersRiskLeverageMetrics.to_json())

# convert the object into a dict
src_api_routers_risk_leverage_metrics_dict = src_api_routers_risk_leverage_metrics_instance.to_dict()
# create an instance of SrcApiRoutersRiskLeverageMetrics from a dict
src_api_routers_risk_leverage_metrics_from_dict = SrcApiRoutersRiskLeverageMetrics.from_dict(src_api_routers_risk_leverage_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


