# FeeBreakdownItem

Fee breakdown item model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **str** | Fee category | 
**amount** | **float** | Fee amount | 
**percentage** | **float** | Percentage of total fees | 

## Example

```python
from equihome_sim_sdk.models.fee_breakdown_item import FeeBreakdownItem

# TODO update the JSON string below
json = "{}"
# create an instance of FeeBreakdownItem from a JSON string
fee_breakdown_item_instance = FeeBreakdownItem.from_json(json)
# print the JSON string representation of the object
print(FeeBreakdownItem.to_json())

# convert the object into a dict
fee_breakdown_item_dict = fee_breakdown_item_instance.to_dict()
# create an instance of FeeBreakdownItem from a dict
fee_breakdown_item_from_dict = FeeBreakdownItem.from_dict(fee_breakdown_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


