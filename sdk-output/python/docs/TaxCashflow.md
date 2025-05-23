# TaxCashflow

Tax cashflow model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** | Year | 
**net_cashflow** | **float** | Net cashflow | 
**tax_amount** | **float** | Tax amount | [optional] 

## Example

```python
from equihome_sim_sdk.models.tax_cashflow import TaxCashflow

# TODO update the JSON string below
json = "{}"
# create an instance of TaxCashflow from a JSON string
tax_cashflow_instance = TaxCashflow.from_json(json)
# print the JSON string representation of the object
print(TaxCashflow.to_json())

# convert the object into a dict
tax_cashflow_dict = tax_cashflow_instance.to_dict()
# create an instance of TaxCashflow from a dict
tax_cashflow_from_dict = TaxCashflow.from_dict(tax_cashflow_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


