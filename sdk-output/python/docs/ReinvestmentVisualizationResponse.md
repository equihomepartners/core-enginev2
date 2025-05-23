# ReinvestmentVisualizationResponse

Reinvestment visualization response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**charts** | [**ReinvestmentChartsResponse**](ReinvestmentChartsResponse.md) | Chart data for reinvestment | 
**tables** | [**ReinvestmentTablesResponse**](ReinvestmentTablesResponse.md) | Table data for reinvestment | 
**kpis** | [**ReinvestmentKPIsResponse**](ReinvestmentKPIsResponse.md) | KPIs for reinvestment | 

## Example

```python
from equihome_sim_sdk.models.reinvestment_visualization_response import ReinvestmentVisualizationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReinvestmentVisualizationResponse from a JSON string
reinvestment_visualization_response_instance = ReinvestmentVisualizationResponse.from_json(json)
# print the JSON string representation of the object
print(ReinvestmentVisualizationResponse.to_json())

# convert the object into a dict
reinvestment_visualization_response_dict = reinvestment_visualization_response_instance.to_dict()
# create an instance of ReinvestmentVisualizationResponse from a dict
reinvestment_visualization_response_from_dict = ReinvestmentVisualizationResponse.from_dict(reinvestment_visualization_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


