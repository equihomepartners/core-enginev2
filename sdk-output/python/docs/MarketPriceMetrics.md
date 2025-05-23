# MarketPriceMetrics

Market/price metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**volatility** | **object** | Volatility metrics at portfolio, zone, and unit levels | 
**alpha_idiosyncratic_share** | **float** | Alpha idiosyncratic share | [optional] 
**beta** | **object** | Beta metrics at macro and zone levels | 
**var** | **object** | Value at Risk (VaR) metrics | 
**cvar** | **object** | Conditional Value at Risk (CVaR) metrics | 

## Example

```python
from equihome_sim_sdk.models.market_price_metrics import MarketPriceMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of MarketPriceMetrics from a JSON string
market_price_metrics_instance = MarketPriceMetrics.from_json(json)
# print the JSON string representation of the object
print(MarketPriceMetrics.to_json())

# convert the object into a dict
market_price_metrics_dict = market_price_metrics_instance.to_dict()
# create an instance of MarketPriceMetrics from a dict
market_price_metrics_from_dict = MarketPriceMetrics.from_dict(market_price_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


