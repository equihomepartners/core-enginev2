# ReinvestmentRequest

Reinvestment request model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reinvestment_amount** | **float** | Amount to reinvest | 
**target_zones** | **Dict[str, float]** | Target allocation by zone for reinvestment | 
**year** | **float** | Current simulation year | 

## Example

```python
from equihome_sim_sdk.models.reinvestment_request import ReinvestmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReinvestmentRequest from a JSON string
reinvestment_request_instance = ReinvestmentRequest.from_json(json)
# print the JSON string representation of the object
print(ReinvestmentRequest.to_json())

# convert the object into a dict
reinvestment_request_dict = reinvestment_request_instance.to_dict()
# create an instance of ReinvestmentRequest from a dict
reinvestment_request_from_dict = ReinvestmentRequest.from_dict(reinvestment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


