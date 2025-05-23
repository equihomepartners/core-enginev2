# PricePathVisualizationResponse

Price path visualization response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**zone_price_charts** | **Dict[str, List[object]]** | Price charts by zone | 
**zone_comparison_chart** | **List[object]** | Comparison chart for all zones | 
**suburb_price_charts** | **Dict[str, List[object]]** | Price charts by suburb | 
**correlation_heatmap** | **List[object]** | Correlation heatmap data | 
**final_distribution** | **Dict[str, List[object]]** | Distribution of final property values | 
**cycle_position_chart** | **List[object]** | Property cycle position over time | [optional] 
**regime_chart** | **List[object]** | Market regime over time | [optional] 

## Example

```python
from equihome_sim_sdk.models.price_path_visualization_response import PricePathVisualizationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PricePathVisualizationResponse from a JSON string
price_path_visualization_response_instance = PricePathVisualizationResponse.from_json(json)
# print the JSON string representation of the object
print(PricePathVisualizationResponse.to_json())

# convert the object into a dict
price_path_visualization_response_dict = price_path_visualization_response_instance.to_dict()
# create an instance of PricePathVisualizationResponse from a dict
price_path_visualization_response_from_dict = PricePathVisualizationResponse.from_dict(price_path_visualization_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


