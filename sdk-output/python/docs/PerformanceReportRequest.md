# PerformanceReportRequest

Performance report request model.  Attributes:     simulation_id: Simulation ID     include_kpi_table: Whether to include KPI table in the report     include_zone_allocation: Whether to include zone allocation in the report     include_cash_flow: Whether to include cash flow in the report     include_risk_metrics: Whether to include risk metrics in the report     include_tranche_performance: Whether to include tranche performance in the report     include_loan_performance: Whether to include loan performance in the report     include_visualization: Whether to include visualization data in the report     export_format: Format to export the report to     export_path: Path to export the report to

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**include_kpi_table** | **bool** | Whether to include KPI table in the report | [optional] [default to True]
**include_zone_allocation** | **bool** | Whether to include zone allocation in the report | [optional] [default to True]
**include_cash_flow** | **bool** | Whether to include cash flow in the report | [optional] [default to True]
**include_risk_metrics** | **bool** | Whether to include risk metrics in the report | [optional] [default to True]
**include_tranche_performance** | **bool** | Whether to include tranche performance in the report | [optional] [default to True]
**include_loan_performance** | **bool** | Whether to include loan performance in the report | [optional] [default to True]
**include_visualization** | **bool** | Whether to include visualization data in the report | [optional] [default to True]
**export_format** | **str** | Format to export the report to (json, csv, excel, markdown, html) | [optional] [default to 'json']
**export_path** | **str** | Path to export the report to | [optional] [default to 'reports']

## Example

```python
from equihome_sim_sdk.models.performance_report_request import PerformanceReportRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PerformanceReportRequest from a JSON string
performance_report_request_instance = PerformanceReportRequest.from_json(json)
# print the JSON string representation of the object
print(PerformanceReportRequest.to_json())

# convert the object into a dict
performance_report_request_dict = performance_report_request_instance.to_dict()
# create an instance of PerformanceReportRequest from a dict
performance_report_request_from_dict = PerformanceReportRequest.from_dict(performance_report_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


