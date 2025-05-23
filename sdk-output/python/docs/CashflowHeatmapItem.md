# CashflowHeatmapItem

Cashflow heatmap item model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** | Year | 
**month** | **int** | Month | 
**category** | **str** | Cashflow category | 
**amount** | **float** | Cashflow amount | 

## Example

```python
from equihome_sim_sdk.models.cashflow_heatmap_item import CashflowHeatmapItem

# TODO update the JSON string below
json = "{}"
# create an instance of CashflowHeatmapItem from a JSON string
cashflow_heatmap_item_instance = CashflowHeatmapItem.from_json(json)
# print the JSON string representation of the object
print(CashflowHeatmapItem.to_json())

# convert the object into a dict
cashflow_heatmap_item_dict = cashflow_heatmap_item_instance.to_dict()
# create an instance of CashflowHeatmapItem from a dict
cashflow_heatmap_item_from_dict = CashflowHeatmapItem.from_dict(cashflow_heatmap_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


