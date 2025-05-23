# TaxMetrics

Tax metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pre_tax_irr** | **float** | Pre-tax IRR | 
**post_tax_irr** | **float** | Post-tax IRR | 
**pre_tax_npv** | **float** | Pre-tax NPV | 
**post_tax_npv** | **float** | Post-tax NPV | 
**total_tax_amount** | **float** | Total tax amount | 
**effective_tax_rate** | **float** | Effective tax rate | 

## Example

```python
from equihome_sim_sdk.models.tax_metrics import TaxMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of TaxMetrics from a JSON string
tax_metrics_instance = TaxMetrics.from_json(json)
# print the JSON string representation of the object
print(TaxMetrics.to_json())

# convert the object into a dict
tax_metrics_dict = tax_metrics_instance.to_dict()
# create an instance of TaxMetrics from a dict
tax_metrics_from_dict = TaxMetrics.from_dict(tax_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


