# WaterfallDistributionModel

Model for waterfall distribution data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**return_of_capital** | **float** | Return of capital amount | 
**preferred_return** | **float** | Preferred return amount | 
**catch_up** | **float** | GP catch-up amount | 
**carried_interest** | **float** | Carried interest amount | 
**residual_to_lp** | **float** | Residual to LP amount | 
**total_to_lp** | **float** | Total to LP amount | 
**total_to_gp** | **float** | Total to GP amount | 
**total_distributed** | **float** | Total distributed amount | 

## Example

```python
from equihome_sim_sdk.models.waterfall_distribution_model import WaterfallDistributionModel

# TODO update the JSON string below
json = "{}"
# create an instance of WaterfallDistributionModel from a JSON string
waterfall_distribution_model_instance = WaterfallDistributionModel.from_json(json)
# print the JSON string representation of the object
print(WaterfallDistributionModel.to_json())

# convert the object into a dict
waterfall_distribution_model_dict = waterfall_distribution_model_instance.to_dict()
# create an instance of WaterfallDistributionModel from a dict
waterfall_distribution_model_from_dict = WaterfallDistributionModel.from_dict(waterfall_distribution_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


