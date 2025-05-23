# WaterfallTierModel

Model for waterfall tier data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tier** | **str** | Tier name | 
**amount** | **float** | Amount allocated to this tier | 
**percentage** | **float** | Percentage of total distribution | 

## Example

```python
from equihome_sim_sdk.models.waterfall_tier_model import WaterfallTierModel

# TODO update the JSON string below
json = "{}"
# create an instance of WaterfallTierModel from a JSON string
waterfall_tier_model_instance = WaterfallTierModel.from_json(json)
# print the JSON string representation of the object
print(WaterfallTierModel.to_json())

# convert the object into a dict
waterfall_tier_model_dict = waterfall_tier_model_instance.to_dict()
# create an instance of WaterfallTierModel from a dict
waterfall_tier_model_from_dict = WaterfallTierModel.from_dict(waterfall_tier_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


