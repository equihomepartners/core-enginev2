# CashflowTableItem

Cashflow table item model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** | Year | 
**capital_calls** | **float** | Capital calls | 
**loan_investments** | **float** | Loan investments | 
**origination_fees** | **float** | Origination fees | 
**principal_repayments** | **float** | Principal repayments | 
**interest_income** | **float** | Interest income | 
**appreciation_share** | **float** | Appreciation share | 
**management_fees** | **float** | Management fees | 
**fund_expenses** | **float** | Fund expenses | 
**distributions** | **float** | Distributions | 
**net_cashflow** | **float** | Net cashflow | 
**cumulative_cashflow** | **float** | Cumulative cashflow | 

## Example

```python
from equihome_sim_sdk.models.cashflow_table_item import CashflowTableItem

# TODO update the JSON string below
json = "{}"
# create an instance of CashflowTableItem from a JSON string
cashflow_table_item_instance = CashflowTableItem.from_json(json)
# print the JSON string representation of the object
print(CashflowTableItem.to_json())

# convert the object into a dict
cashflow_table_item_dict = cashflow_table_item_instance.to_dict()
# create an instance of CashflowTableItem from a dict
cashflow_table_item_from_dict = CashflowTableItem.from_dict(cashflow_table_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


