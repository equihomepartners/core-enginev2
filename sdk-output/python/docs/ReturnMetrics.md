# ReturnMetrics

Return metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**irr** | **float** | Internal Rate of Return | [optional] 
**equity_multiple** | **float** | Equity Multiple | [optional] 
**moic** | **float** | Multiple on Invested Capital | [optional] 
**tvpi** | **float** | Total Value to Paid-In | [optional] 
**dpi** | **float** | Distributions to Paid-In | [optional] 
**rvpi** | **float** | Residual Value to Paid-In | [optional] 
**roi** | **float** | Return on Investment | [optional] 
**payback_period** | **float** | Payback Period in years | [optional] 
**cash_yield** | **float** | Cash Yield | [optional] 
**annualized_return** | **float** | Annualized Return | [optional] 

## Example

```python
from equihome_sim_sdk.models.return_metrics import ReturnMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of ReturnMetrics from a JSON string
return_metrics_instance = ReturnMetrics.from_json(json)
# print the JSON string representation of the object
print(ReturnMetrics.to_json())

# convert the object into a dict
return_metrics_dict = return_metrics_instance.to_dict()
# create an instance of ReturnMetrics from a dict
return_metrics_from_dict = ReturnMetrics.from_dict(return_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


