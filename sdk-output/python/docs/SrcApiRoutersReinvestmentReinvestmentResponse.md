# SrcApiRoutersReinvestmentReinvestmentResponse

Reinvestment response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**events** | [**List[ReinvestmentEventResponse]**](ReinvestmentEventResponse.md) | List of reinvestment events | 
**summary** | [**ReinvestmentSummaryResponse**](ReinvestmentSummaryResponse.md) | Summary of reinvestment activity | 
**visualization** | [**ReinvestmentVisualizationResponse**](ReinvestmentVisualizationResponse.md) | Visualization data | 

## Example

```python
from equihome_sim_sdk.models.src_api_routers_reinvestment_reinvestment_response import SrcApiRoutersReinvestmentReinvestmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SrcApiRoutersReinvestmentReinvestmentResponse from a JSON string
src_api_routers_reinvestment_reinvestment_response_instance = SrcApiRoutersReinvestmentReinvestmentResponse.from_json(json)
# print the JSON string representation of the object
print(SrcApiRoutersReinvestmentReinvestmentResponse.to_json())

# convert the object into a dict
src_api_routers_reinvestment_reinvestment_response_dict = src_api_routers_reinvestment_reinvestment_response_instance.to_dict()
# create an instance of SrcApiRoutersReinvestmentReinvestmentResponse from a dict
src_api_routers_reinvestment_reinvestment_response_from_dict = SrcApiRoutersReinvestmentReinvestmentResponse.from_dict(src_api_routers_reinvestment_reinvestment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


