# CashflowByYearItem

Cashflow by year item model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** | Year | 
**inflows** | **float** | Total inflows | 
**outflows** | **float** | Total outflows | 
**net** | **float** | Net cashflow | 

## Example

```python
from equihome_sim_sdk.models.cashflow_by_year_item import CashflowByYearItem

# TODO update the JSON string below
json = "{}"
# create an instance of CashflowByYearItem from a JSON string
cashflow_by_year_item_instance = CashflowByYearItem.from_json(json)
# print the JSON string representation of the object
print(CashflowByYearItem.to_json())

# convert the object into a dict
cashflow_by_year_item_dict = cashflow_by_year_item_instance.to_dict()
# create an instance of CashflowByYearItem from a dict
cashflow_by_year_item_from_dict = CashflowByYearItem.from_dict(cashflow_by_year_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


