# CreditMetrics

Credit metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**current_ltv** | **object** | Current LTV metrics | 
**stress_ltv** | **object** | Stress LTV metrics with -20% price shock | 
**default_probability** | **object** | Default probability metrics | 
**portfolio_default_rate** | **float** | Portfolio default rate (exposure-weighted PD) | 

## Example

```python
from equihome_sim_sdk.models.credit_metrics import CreditMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of CreditMetrics from a JSON string
credit_metrics_instance = CreditMetrics.from_json(json)
# print the JSON string representation of the object
print(CreditMetrics.to_json())

# convert the object into a dict
credit_metrics_dict = credit_metrics_instance.to_dict()
# create an instance of CreditMetrics from a dict
credit_metrics_from_dict = CreditMetrics.from_dict(credit_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


