# CashflowCalculationRequest

Request model for cashflow calculation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**time_granularity** | **str** | Time granularity for cashflow aggregation | [optional] 
**include_loan_level_cashflows** | **bool** | Whether to include loan-level cashflows in the results | [optional] 
**include_fund_level_cashflows** | **bool** | Whether to include fund-level cashflows in the results | [optional] 
**include_stakeholder_cashflows** | **bool** | Whether to include stakeholder-level cashflows in the results | [optional] 
**simple_interest_rate** | **float** | Simple interest rate for loans (0-1) | [optional] 
**origination_fee_rate** | **float** | Origination fee rate (0-1) | [optional] 
**appreciation_share_method** | **str** | Method for calculating appreciation share | [optional] 
**distribution_frequency** | **str** | Frequency of distributions to investors | [optional] 
**distribution_lag** | **int** | Lag in months between cashflow receipt and distribution | [optional] 
**enable_parallel_processing** | **bool** | Whether to enable parallel processing for loan-level cashflow calculations | [optional] 
**num_workers** | **int** | Number of worker processes for parallel processing | [optional] 
**enable_scenario_analysis** | **bool** | Whether to enable scenario analysis | [optional] 
**scenarios** | **List[object]** | Scenarios for scenario analysis | [optional] 
**enable_sensitivity_analysis** | **bool** | Whether to enable sensitivity analysis | [optional] 
**sensitivity_parameters** | **List[object]** | Parameters to vary for sensitivity analysis | [optional] 
**enable_cashflow_metrics** | **bool** | Whether to enable cashflow metrics calculation | [optional] 
**discount_rate** | **float** | Discount rate for DCF calculations (0-1) | [optional] 
**enable_tax_impact_analysis** | **bool** | Whether to enable tax impact analysis | [optional] 
**tax_rates** | **Dict[str, float]** | Tax rates for different income types | [optional] 
**enable_reinvestment_modeling** | **bool** | Whether to enable reinvestment modeling | [optional] 
**reinvestment_rate** | **float** | Rate of return on reinvested cashflows (0-1) | [optional] 
**enable_liquidity_analysis** | **bool** | Whether to enable liquidity analysis | [optional] 
**minimum_cash_reserve** | **float** | Minimum cash reserve as percentage of fund size (0-1) | [optional] 
**enable_export** | **bool** | Whether to enable export capabilities | [optional] 
**export_formats** | **List[str]** | Export formats | [optional] 

## Example

```python
from equihome_sim_sdk.models.cashflow_calculation_request import CashflowCalculationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CashflowCalculationRequest from a JSON string
cashflow_calculation_request_instance = CashflowCalculationRequest.from_json(json)
# print the JSON string representation of the object
print(CashflowCalculationRequest.to_json())

# convert the object into a dict
cashflow_calculation_request_dict = cashflow_calculation_request_instance.to_dict()
# create an instance of CashflowCalculationRequest from a dict
cashflow_calculation_request_from_dict = CashflowCalculationRequest.from_dict(cashflow_calculation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


