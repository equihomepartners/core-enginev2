# SrcApiRoutersRiskLiquidityMetrics

Liquidity metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**liquidity_score** | **object** | Liquidity score metrics | 
**expected_exit_lag** | **object** | Expected exit lag metrics | 
**wal** | **float** | Weighted Average Life (WAL) | 
**cfar** | **object** | Cash-flow-at-risk (CFaR) metrics | 

## Example

```python
from equihome_sim_sdk.models.src_api_routers_risk_liquidity_metrics import SrcApiRoutersRiskLiquidityMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of SrcApiRoutersRiskLiquidityMetrics from a JSON string
src_api_routers_risk_liquidity_metrics_instance = SrcApiRoutersRiskLiquidityMetrics.from_json(json)
# print the JSON string representation of the object
print(SrcApiRoutersRiskLiquidityMetrics.to_json())

# convert the object into a dict
src_api_routers_risk_liquidity_metrics_dict = src_api_routers_risk_liquidity_metrics_instance.to_dict()
# create an instance of SrcApiRoutersRiskLiquidityMetrics from a dict
src_api_routers_risk_liquidity_metrics_from_dict = SrcApiRoutersRiskLiquidityMetrics.from_dict(src_api_routers_risk_liquidity_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


