# LeverageVisualization

Leverage visualization model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**leverage_timeline** | **List[object]** | Timeline of leverage | 
**facility_utilization** | **List[object]** | Facility utilization over time | 
**interest_expense** | **List[object]** | Interest expense over time | 

## Example

```python
from equihome_sim_sdk.models.leverage_visualization import LeverageVisualization

# TODO update the JSON string below
json = "{}"
# create an instance of LeverageVisualization from a JSON string
leverage_visualization_instance = LeverageVisualization.from_json(json)
# print the JSON string representation of the object
print(LeverageVisualization.to_json())

# convert the object into a dict
leverage_visualization_dict = leverage_visualization_instance.to_dict()
# create an instance of LeverageVisualization from a dict
leverage_visualization_from_dict = LeverageVisualization.from_dict(leverage_visualization_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


