# FundLevelMetrics

Fund-level metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**irr** | **float** | Internal Rate of Return | 
**moic** | **float** | Multiple on Invested Capital | 
**tvpi** | **float** | Total Value to Paid-In | 
**dpi** | **float** | Distributions to Paid-In | 
**rvpi** | **float** | Residual Value to Paid-In | 
**payback_period** | **float** | Payback period in years | 
**cash_on_cash** | **float** | Cash-on-cash return | 
**npv** | **float** | Net Present Value | 
**profitability_index** | **float** | Profitability Index | 
**cash_yield** | **float** | Cash yield | 

## Example

```python
from equihome_sim_sdk.models.fund_level_metrics import FundLevelMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of FundLevelMetrics from a JSON string
fund_level_metrics_instance = FundLevelMetrics.from_json(json)
# print the JSON string representation of the object
print(FundLevelMetrics.to_json())

# convert the object into a dict
fund_level_metrics_dict = fund_level_metrics_instance.to_dict()
# create an instance of FundLevelMetrics from a dict
fund_level_metrics_from_dict = FundLevelMetrics.from_dict(fund_level_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


