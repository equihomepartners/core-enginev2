# WaterfallResultModel

Model for waterfall result data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**distributions** | [**WaterfallDistributionModel**](WaterfallDistributionModel.md) | Waterfall distribution data | 
**clawback_amount** | **float** | Clawback amount | 
**visualization** | [**WaterfallVisualizationModel**](WaterfallVisualizationModel.md) | Waterfall visualization data | 

## Example

```python
from equihome_sim_sdk.models.waterfall_result_model import WaterfallResultModel

# TODO update the JSON string below
json = "{}"
# create an instance of WaterfallResultModel from a JSON string
waterfall_result_model_instance = WaterfallResultModel.from_json(json)
# print the JSON string representation of the object
print(WaterfallResultModel.to_json())

# convert the object into a dict
waterfall_result_model_dict = waterfall_result_model_instance.to_dict()
# create an instance of WaterfallResultModel from a dict
waterfall_result_model_from_dict = WaterfallResultModel.from_dict(waterfall_result_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


