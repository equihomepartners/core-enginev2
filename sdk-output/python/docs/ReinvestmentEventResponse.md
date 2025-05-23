# ReinvestmentEventResponse

Reinvestment event response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_id** | **str** | Unique identifier for the reinvestment event | 
**timestamp** | **float** | Timestamp of the reinvestment event | 
**year** | **float** | Simulation year of the reinvestment event | 
**month** | **int** | Month of the reinvestment event (1-12) | 
**amount** | **float** | Amount reinvested | 
**source** | **str** | Source of the reinvestment capital | 
**source_details** | **object** | Details about the source | 
**strategy_used** | **str** | Reinvestment strategy used | 
**target_allocations** | **Dict[str, float]** | Target zone allocations | 
**actual_allocations** | **Dict[str, float]** | Actual zone allocations | 
**num_loans_generated** | **int** | Number of loans generated | 
**loan_ids** | **List[str]** | IDs of loans generated | 
**performance_adjustments** | **Dict[str, float]** | Performance adjustments | [optional] 
**cash_reserve_before** | **float** | Cash reserve before reinvestment | [optional] 
**cash_reserve_after** | **float** | Cash reserve after reinvestment | [optional] 

## Example

```python
from equihome_sim_sdk.models.reinvestment_event_response import ReinvestmentEventResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReinvestmentEventResponse from a JSON string
reinvestment_event_response_instance = ReinvestmentEventResponse.from_json(json)
# print the JSON string representation of the object
print(ReinvestmentEventResponse.to_json())

# convert the object into a dict
reinvestment_event_response_dict = reinvestment_event_response_instance.to_dict()
# create an instance of ReinvestmentEventResponse from a dict
reinvestment_event_response_from_dict = ReinvestmentEventResponse.from_dict(reinvestment_event_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


