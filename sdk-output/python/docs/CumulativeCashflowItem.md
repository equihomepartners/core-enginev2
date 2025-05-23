# CumulativeCashflowItem

Cumulative cashflow item model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** | Year | 
**cumulative_cashflow** | **float** | Cumulative cashflow | 

## Example

```python
from equihome_sim_sdk.models.cumulative_cashflow_item import CumulativeCashflowItem

# TODO update the JSON string below
json = "{}"
# create an instance of CumulativeCashflowItem from a JSON string
cumulative_cashflow_item_instance = CumulativeCashflowItem.from_json(json)
# print the JSON string representation of the object
print(CumulativeCashflowItem.to_json())

# convert the object into a dict
cumulative_cashflow_item_dict = cumulative_cashflow_item_instance.to_dict()
# create an instance of CumulativeCashflowItem from a dict
cumulative_cashflow_item_from_dict = CumulativeCashflowItem.from_dict(cumulative_cashflow_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


