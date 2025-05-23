# ExitVisualizationResponse

Exit visualization response model.

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

## Example

```python
from equihome_sim_sdk.models.exit_visualization_response import ExitVisualizationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExitVisualizationResponse from a JSON string
exit_visualization_response_instance = ExitVisualizationResponse.from_json(json)
# print the JSON string representation of the object
print(ExitVisualizationResponse.to_json())

# convert the object into a dict
exit_visualization_response_dict = exit_visualization_response_instance.to_dict()
# create an instance of ExitVisualizationResponse from a dict
exit_visualization_response_from_dict = ExitVisualizationResponse.from_dict(exit_visualization_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


