# SrcApiRoutersFinanceLiquidityMetrics

Liquidity metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**min_cash_reserve** | **float** | Minimum cash reserve | 
**max_cash_reserve** | **float** | Maximum cash reserve | 
**avg_cash_reserve** | **float** | Average cash reserve | 
**num_shortfall_periods** | **int** | Number of periods with shortfall | 
**max_shortfall** | **float** | Maximum shortfall | 

## Example

```python
from equihome_sim_sdk.models.src_api_routers_finance_liquidity_metrics import SrcApiRoutersFinanceLiquidityMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of SrcApiRoutersFinanceLiquidityMetrics from a JSON string
src_api_routers_finance_liquidity_metrics_instance = SrcApiRoutersFinanceLiquidityMetrics.from_json(json)
# print the JSON string representation of the object
print(SrcApiRoutersFinanceLiquidityMetrics.to_json())

# convert the object into a dict
src_api_routers_finance_liquidity_metrics_dict = src_api_routers_finance_liquidity_metrics_instance.to_dict()
# create an instance of SrcApiRoutersFinanceLiquidityMetrics from a dict
src_api_routers_finance_liquidity_metrics_from_dict = SrcApiRoutersFinanceLiquidityMetrics.from_dict(src_api_routers_finance_liquidity_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


