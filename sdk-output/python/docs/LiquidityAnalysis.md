# LiquidityAnalysis

Liquidity analysis model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cash_reserves** | [**List[CashReserve]**](CashReserve.md) | Cash reserves by year | 
**liquidity_metrics** | [**SrcApiRoutersFinanceLiquidityMetrics**](SrcApiRoutersFinanceLiquidityMetrics.md) | Liquidity metrics | 

## Example

```python
from equihome_sim_sdk.models.liquidity_analysis import LiquidityAnalysis

# TODO update the JSON string below
json = "{}"
# create an instance of LiquidityAnalysis from a JSON string
liquidity_analysis_instance = LiquidityAnalysis.from_json(json)
# print the JSON string representation of the object
print(LiquidityAnalysis.to_json())

# convert the object into a dict
liquidity_analysis_dict = liquidity_analysis_instance.to_dict()
# create an instance of LiquidityAnalysis from a dict
liquidity_analysis_from_dict = LiquidityAnalysis.from_dict(liquidity_analysis_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


