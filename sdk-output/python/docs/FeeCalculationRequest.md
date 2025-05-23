# FeeCalculationRequest

Request model for fee calculation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**management_fee_rate** | **float** | Management fee rate (0-1) | [optional] 
**management_fee_basis** | **str** | Basis for management fee calculation | [optional] 
**origination_fee_rate** | **float** | Origination fee rate (0-1) | [optional] 
**annual_fund_expenses** | **float** | Annual fund expenses as percentage of fund size (0-1) | [optional] 
**fixed_annual_expenses** | **float** | Fixed annual expenses in dollars | [optional] 
**expense_growth_rate** | **float** | Annual growth rate for expenses (0-1) | [optional] 
**acquisition_fee_rate** | **float** | Acquisition fee rate (0-1) | [optional] 
**disposition_fee_rate** | **float** | Disposition fee rate (0-1) | [optional] 
**setup_costs** | **float** | One-time setup costs in dollars | [optional] 

## Example

```python
from equihome_sim_sdk.models.fee_calculation_request import FeeCalculationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FeeCalculationRequest from a JSON string
fee_calculation_request_instance = FeeCalculationRequest.from_json(json)
# print the JSON string representation of the object
print(FeeCalculationRequest.to_json())

# convert the object into a dict
fee_calculation_request_dict = fee_calculation_request_instance.to_dict()
# create an instance of FeeCalculationRequest from a dict
fee_calculation_request_from_dict = FeeCalculationRequest.from_dict(fee_calculation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


