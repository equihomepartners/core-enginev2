# EnhancedExitVisualizationResponse

Enhanced exit visualization response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exit_timing_chart** | **List[object]** | Exit timing distribution chart | 
**exit_type_chart** | **List[object]** | Exit type distribution chart | 
**cumulative_exits_chart** | **List[object]** | Cumulative exits chart | 
**exit_roi_chart** | **List[object]** | Exit ROI distribution chart | 
**exit_type_roi_chart** | **List[object]** | Exit type ROI chart | 
**exit_summary** | **object** | Exit summary | 
**exit_value_by_year_chart** | **List[object]** | Exit value by year chart | 
**exit_count_by_year_chart** | **List[object]** | Exit count by year chart | 
**cohort_visualizations** | **object** | Cohort analysis visualizations | [optional] 
**risk_visualizations** | **object** | Risk metrics visualizations | [optional] 
**ml_visualizations** | **object** | Machine learning visualizations | [optional] 
**economic_visualizations** | **object** | Economic scenario visualizations | [optional] 
**geospatial_visualizations** | **object** | Geospatial visualizations | [optional] 
**comparative_visualizations** | **object** | Comparative visualizations | [optional] 

## Example

```python
from equihome_sim_sdk.models.enhanced_exit_visualization_response import EnhancedExitVisualizationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of EnhancedExitVisualizationResponse from a JSON string
enhanced_exit_visualization_response_instance = EnhancedExitVisualizationResponse.from_json(json)
# print the JSON string representation of the object
print(EnhancedExitVisualizationResponse.to_json())

# convert the object into a dict
enhanced_exit_visualization_response_dict = enhanced_exit_visualization_response_instance.to_dict()
# create an instance of EnhancedExitVisualizationResponse from a dict
enhanced_exit_visualization_response_from_dict = EnhancedExitVisualizationResponse.from_dict(enhanced_exit_visualization_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


