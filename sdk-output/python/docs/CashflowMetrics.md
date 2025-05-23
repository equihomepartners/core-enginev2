# CashflowMetrics

Cashflow metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fund_level_metrics** | [**FundLevelMetrics**](FundLevelMetrics.md) | Fund-level metrics | 
**lp_metrics** | [**LPMetrics**](LPMetrics.md) | LP metrics | 
**gp_metrics** | [**GPMetrics**](GPMetrics.md) | GP metrics | 
**metrics_by_year** | [**List[MetricsByYear]**](MetricsByYear.md) | Metrics by year | 

## Example

```python
from equihome_sim_sdk.models.cashflow_metrics import CashflowMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of CashflowMetrics from a JSON string
cashflow_metrics_instance = CashflowMetrics.from_json(json)
# print the JSON string representation of the object
print(CashflowMetrics.to_json())

# convert the object into a dict
cashflow_metrics_dict = cashflow_metrics_instance.to_dict()
# create an instance of CashflowMetrics from a dict
cashflow_metrics_from_dict = CashflowMetrics.from_dict(cashflow_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


