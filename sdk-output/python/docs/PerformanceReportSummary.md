# PerformanceReportSummary

Performance report summary model.  Attributes:     simulation_id: Simulation ID     simulation_date: Simulation date     fund_size: Fund size     fund_term: Fund term     hurdle_rate: Hurdle rate     num_loans: Number of loans     total_loan_amount: Total loan amount     avg_ltv: Average LTV     irr: IRR     moic: MOIC     tvpi: TVPI     dpi: DPI     rvpi: RVPI     var_99: VaR (99%)     sharpe_ratio: Sharpe ratio     worst_guardrail_level: Worst guardrail level

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**simulation_date** | **str** | Simulation date | 
**fund_size** | **float** | Fund size | 
**fund_term** | **int** | Fund term | 
**hurdle_rate** | **float** | Hurdle rate | 
**num_loans** | **int** | Number of loans | 
**total_loan_amount** | **float** | Total loan amount | 
**avg_ltv** | **float** | Average LTV | 
**irr** | **float** | IRR | 
**moic** | **float** | MOIC | 
**tvpi** | **float** | TVPI | 
**dpi** | **float** | DPI | 
**rvpi** | **float** | RVPI | 
**var_99** | **float** | VaR (99%) | 
**sharpe_ratio** | **float** | Sharpe ratio | 
**worst_guardrail_level** | **str** | Worst guardrail level | 

## Example

```python
from equihome_sim_sdk.models.performance_report_summary import PerformanceReportSummary

# TODO update the JSON string below
json = "{}"
# create an instance of PerformanceReportSummary from a JSON string
performance_report_summary_instance = PerformanceReportSummary.from_json(json)
# print the JSON string representation of the object
print(PerformanceReportSummary.to_json())

# convert the object into a dict
performance_report_summary_dict = performance_report_summary_instance.to_dict()
# create an instance of PerformanceReportSummary from a dict
performance_report_summary_from_dict = PerformanceReportSummary.from_dict(performance_report_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


