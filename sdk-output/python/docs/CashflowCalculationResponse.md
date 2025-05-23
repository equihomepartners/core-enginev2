# CashflowCalculationResponse

Response model for cashflow calculation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**loan_level_cashflows** | [**List[LoanLevelCashflow]**](LoanLevelCashflow.md) | Loan-level cashflows | [optional] 
**fund_level_cashflows** | [**List[FundLevelCashflow]**](FundLevelCashflow.md) | Fund-level cashflows | 
**stakeholder_cashflows** | **Dict[str, List[object]]** | Stakeholder cashflows | 
**visualization** | [**CashflowVisualization**](CashflowVisualization.md) | Visualization data | 
**metrics** | [**CashflowMetrics**](CashflowMetrics.md) | Cashflow metrics | [optional] 
**sensitivity_analysis** | [**SensitivityAnalysis**](SensitivityAnalysis.md) | Sensitivity analysis results | [optional] 
**scenario_analysis** | [**ScenarioAnalysis**](ScenarioAnalysis.md) | Scenario analysis results | [optional] 
**tax_impact** | [**TaxImpactAnalysis**](TaxImpactAnalysis.md) | Tax impact analysis results | [optional] 
**liquidity_analysis** | [**LiquidityAnalysis**](LiquidityAnalysis.md) | Liquidity analysis results | [optional] 

## Example

```python
from equihome_sim_sdk.models.cashflow_calculation_response import CashflowCalculationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CashflowCalculationResponse from a JSON string
cashflow_calculation_response_instance = CashflowCalculationResponse.from_json(json)
# print the JSON string representation of the object
print(CashflowCalculationResponse.to_json())

# convert the object into a dict
cashflow_calculation_response_dict = cashflow_calculation_response_instance.to_dict()
# create an instance of CashflowCalculationResponse from a dict
cashflow_calculation_response_from_dict = CashflowCalculationResponse.from_dict(cashflow_calculation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


