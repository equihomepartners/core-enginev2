# CashflowWaterfallItem

Cashflow waterfall item model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **str** | Cashflow category | 
**amount** | **float** | Cashflow amount | 

## Example

```python
from equihome_sim_sdk.models.cashflow_waterfall_item import CashflowWaterfallItem

# TODO update the JSON string below
json = "{}"
# create an instance of CashflowWaterfallItem from a JSON string
cashflow_waterfall_item_instance = CashflowWaterfallItem.from_json(json)
# print the JSON string representation of the object
print(CashflowWaterfallItem.to_json())

# convert the object into a dict
cashflow_waterfall_item_dict = cashflow_waterfall_item_instance.to_dict()
# create an instance of CashflowWaterfallItem from a dict
cashflow_waterfall_item_from_dict = CashflowWaterfallItem.from_dict(cashflow_waterfall_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


