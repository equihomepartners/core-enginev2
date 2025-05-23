# FundLevelCashflow

Fund-level cashflow model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** | Year | 
**month** | **int** | Month (if applicable) | [optional] 
**quarter** | **int** | Quarter (if applicable) | [optional] 
**capital_calls** | **float** | Capital calls | 
**loan_investments** | **float** | Loan investments | 
**origination_fees** | **float** | Origination fees | 
**principal_repayments** | **float** | Principal repayments | 
**interest_income** | **float** | Interest income | 
**appreciation_share** | **float** | Appreciation share | 
**management_fees** | **float** | Management fees | 
**fund_expenses** | **float** | Fund expenses | 
**leverage_draws** | **float** | Leverage draws | 
**leverage_repayments** | **float** | Leverage repayments | 
**leverage_interest** | **float** | Leverage interest | 
**distributions** | **float** | Distributions | 
**net_cashflow** | **float** | Net cashflow | 
**cumulative_cashflow** | **float** | Cumulative cashflow | 

## Example

```python
from equihome_sim_sdk.models.fund_level_cashflow import FundLevelCashflow

# TODO update the JSON string below
json = "{}"
# create an instance of FundLevelCashflow from a JSON string
fund_level_cashflow_instance = FundLevelCashflow.from_json(json)
# print the JSON string representation of the object
print(FundLevelCashflow.to_json())

# convert the object into a dict
fund_level_cashflow_dict = fund_level_cashflow_instance.to_dict()
# create an instance of FundLevelCashflow from a dict
fund_level_cashflow_from_dict = FundLevelCashflow.from_dict(fund_level_cashflow_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


