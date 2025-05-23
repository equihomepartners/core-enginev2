# WaterfallVisualizationModel

Model for waterfall visualization data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**waterfall_chart** | [**List[WaterfallChartModel]**](WaterfallChartModel.md) | Waterfall chart data | 
**distribution_by_year_chart** | [**List[DistributionByYearModel]**](DistributionByYearModel.md) | Distribution by year chart data | 
**tier_allocation_chart** | [**List[WaterfallTierModel]**](WaterfallTierModel.md) | Tier allocation chart data | 
**stakeholder_allocation_chart** | [**List[StakeholderAllocationModel]**](StakeholderAllocationModel.md) | Stakeholder allocation chart data | 

## Example

```python
from equihome_sim_sdk.models.waterfall_visualization_model import WaterfallVisualizationModel

# TODO update the JSON string below
json = "{}"
# create an instance of WaterfallVisualizationModel from a JSON string
waterfall_visualization_model_instance = WaterfallVisualizationModel.from_json(json)
# print the JSON string representation of the object
print(WaterfallVisualizationModel.to_json())

# convert the object into a dict
waterfall_visualization_model_dict = waterfall_visualization_model_instance.to_dict()
# create an instance of WaterfallVisualizationModel from a dict
waterfall_visualization_model_from_dict = WaterfallVisualizationModel.from_dict(waterfall_visualization_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


