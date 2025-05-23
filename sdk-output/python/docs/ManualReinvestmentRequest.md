# ManualReinvestmentRequest

Manual reinvestment request model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amount** | **float** | Amount to reinvest | 
**year** | **float** | Simulation year | 
**month** | **int** | Month (1-12) | [optional] [default to 1]
**strategy** | **str** | Reinvestment strategy | [optional] [default to 'rebalance']
**source** | **str** | Source of the reinvestment capital | [optional] [default to 'exit']
**source_details** | **object** | Details about the source | [optional] 
**zone_preference_multipliers** | **Dict[str, float]** | Zone preference multipliers | [optional] 
**enable_dynamic_allocation** | **bool** | Whether to use dynamic allocation | [optional] [default to False]

## Example

```python
from equihome_sim_sdk.models.manual_reinvestment_request import ManualReinvestmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ManualReinvestmentRequest from a JSON string
manual_reinvestment_request_instance = ManualReinvestmentRequest.from_json(json)
# print the JSON string representation of the object
print(ManualReinvestmentRequest.to_json())

# convert the object into a dict
manual_reinvestment_request_dict = manual_reinvestment_request_instance.to_dict()
# create an instance of ManualReinvestmentRequest from a dict
manual_reinvestment_request_from_dict = ManualReinvestmentRequest.from_dict(manual_reinvestment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


