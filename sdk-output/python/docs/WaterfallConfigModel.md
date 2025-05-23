# WaterfallConfigModel

Model for waterfall configuration.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waterfall_structure** | [**WaterfallStructureEnum**](WaterfallStructureEnum.md) | Waterfall structure type | [optional] 
**hurdle_rate** | **float** | Hurdle rate (preferred return) | [optional] [default to 0.08]
**carried_interest_rate** | **float** | Carried interest rate | [optional] [default to 0.2]
**catch_up_rate** | **float** | GP catch-up rate | [optional] [default to 0.0]
**gp_commitment_percentage** | **float** | GP commitment percentage | [optional] [default to 0.0]
**multi_tier_enabled** | **bool** | Enable multi-tier waterfall | [optional] [default to False]
**enable_clawback** | **bool** | Enable clawback | [optional] [default to True]
**clawback_threshold** | **float** | Clawback threshold | [optional] [default to 0.0]

## Example

```python
from equihome_sim_sdk.models.waterfall_config_model import WaterfallConfigModel

# TODO update the JSON string below
json = "{}"
# create an instance of WaterfallConfigModel from a JSON string
waterfall_config_model_instance = WaterfallConfigModel.from_json(json)
# print the JSON string representation of the object
print(WaterfallConfigModel.to_json())

# convert the object into a dict
waterfall_config_model_dict = waterfall_config_model_instance.to_dict()
# create an instance of WaterfallConfigModel from a dict
waterfall_config_model_from_dict = WaterfallConfigModel.from_dict(waterfall_config_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


