# TaxImpactAnalysis

Tax impact analysis model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pre_tax_cashflows** | [**List[TaxCashflow]**](TaxCashflow.md) | Pre-tax cashflows by year | 
**post_tax_cashflows** | [**List[TaxCashflow]**](TaxCashflow.md) | Post-tax cashflows by year | 
**tax_metrics** | [**TaxMetrics**](TaxMetrics.md) | Tax metrics | 

## Example

```python
from equihome_sim_sdk.models.tax_impact_analysis import TaxImpactAnalysis

# TODO update the JSON string below
json = "{}"
# create an instance of TaxImpactAnalysis from a JSON string
tax_impact_analysis_instance = TaxImpactAnalysis.from_json(json)
# print the JSON string representation of the object
print(TaxImpactAnalysis.to_json())

# convert the object into a dict
tax_impact_analysis_dict = tax_impact_analysis_instance.to_dict()
# create an instance of TaxImpactAnalysis from a dict
tax_impact_analysis_from_dict = TaxImpactAnalysis.from_dict(tax_impact_analysis_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


