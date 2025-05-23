# GPMetrics

GP metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**irr** | **float** | Internal Rate of Return | 
**moic** | **float** | Multiple on Invested Capital | 
**tvpi** | **float** | Total Value to Paid-In | 
**dpi** | **float** | Distributions to Paid-In | 
**rvpi** | **float** | Residual Value to Paid-In | 
**payback_period** | **float** | Payback period in years | 
**carried_interest** | **float** | Total carried interest | 
**management_fees** | **float** | Total management fees | 
**origination_fees** | **float** | Total origination fees | 

## Example

```python
from equihome_sim_sdk.models.gp_metrics import GPMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of GPMetrics from a JSON string
gp_metrics_instance = GPMetrics.from_json(json)
# print the JSON string representation of the object
print(GPMetrics.to_json())

# convert the object into a dict
gp_metrics_dict = gp_metrics_instance.to_dict()
# create an instance of GPMetrics from a dict
gp_metrics_from_dict = GPMetrics.from_dict(gp_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


