# FeeImpactItem

Fee impact item model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metric** | **str** | Performance metric | 
**gross** | **float** | Gross value (before fees) | 
**net** | **float** | Net value (after fees) | 
**impact** | **float** | Impact of fees | 

## Example

```python
from equihome_sim_sdk.models.fee_impact_item import FeeImpactItem

# TODO update the JSON string below
json = "{}"
# create an instance of FeeImpactItem from a JSON string
fee_impact_item_instance = FeeImpactItem.from_json(json)
# print the JSON string representation of the object
print(FeeImpactItem.to_json())

# convert the object into a dict
fee_impact_item_dict = fee_impact_item_instance.to_dict()
# create an instance of FeeImpactItem from a dict
fee_impact_item_from_dict = FeeImpactItem.from_dict(fee_impact_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


