# LPMetrics

LP metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**irr** | **float** | Internal Rate of Return | 
**moic** | **float** | Multiple on Invested Capital | 
**tvpi** | **float** | Total Value to Paid-In | 
**dpi** | **float** | Distributions to Paid-In | 
**rvpi** | **float** | Residual Value to Paid-In | 
**payback_period** | **float** | Payback period in years | 

## Example

```python
from equihome_sim_sdk.models.lp_metrics import LPMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of LPMetrics from a JSON string
lp_metrics_instance = LPMetrics.from_json(json)
# print the JSON string representation of the object
print(LPMetrics.to_json())

# convert the object into a dict
lp_metrics_dict = lp_metrics_instance.to_dict()
# create an instance of LPMetrics from a dict
lp_metrics_from_dict = LPMetrics.from_dict(lp_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


