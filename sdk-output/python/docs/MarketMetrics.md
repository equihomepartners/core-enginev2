# MarketMetrics

Market metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**beta** | **float** | Beta (market sensitivity) | [optional] 
**alpha** | **float** | Alpha (excess return) | [optional] 
**tracking_error** | **float** | Tracking Error | [optional] 
**r_squared** | **float** | R-Squared (correlation with benchmark) | [optional] 
**upside_capture** | **float** | Upside Capture Ratio | [optional] 
**downside_capture** | **float** | Downside Capture Ratio | [optional] 
**upside_potential** | **float** | Upside Potential | [optional] 
**downside_risk** | **float** | Downside Risk | [optional] 

## Example

```python
from equihome_sim_sdk.models.market_metrics import MarketMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of MarketMetrics from a JSON string
market_metrics_instance = MarketMetrics.from_json(json)
# print the JSON string representation of the object
print(MarketMetrics.to_json())

# convert the object into a dict
market_metrics_dict = market_metrics_instance.to_dict()
# create an instance of MarketMetrics from a dict
market_metrics_from_dict = MarketMetrics.from_dict(market_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


