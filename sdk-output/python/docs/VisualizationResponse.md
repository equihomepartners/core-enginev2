# VisualizationResponse

Visualization response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**capital_allocation** | **object** | Capital allocation visualization | [optional] 
**loan_portfolio** | **object** | Loan portfolio visualization | [optional] 
**allocation_history** | **object** | Allocation history visualization | [optional] 
**loan_portfolio_history** | **object** | Loan portfolio history visualization | [optional] 
**leverage** | **object** | Leverage visualization | [optional] 

## Example

```python
from equihome_sim_sdk.models.visualization_response import VisualizationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of VisualizationResponse from a JSON string
visualization_response_instance = VisualizationResponse.from_json(json)
# print the JSON string representation of the object
print(VisualizationResponse.to_json())

# convert the object into a dict
visualization_response_dict = visualization_response_instance.to_dict()
# create an instance of VisualizationResponse from a dict
visualization_response_from_dict = VisualizationResponse.from_dict(visualization_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


