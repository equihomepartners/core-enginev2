# LeverageEvent

Leverage event model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**facility_id** | **str** | Facility ID | 
**var_date** | **str** | Date of the event | 
**amount** | **float** | Amount of the event | 
**year** | **float** | Simulation year | 
**month** | **int** | Month (1-12) | 
**event_type** | **str** | Event type (draw, repayment, interest, fee) | 
**details** | **object** | Additional details | [optional] 

## Example

```python
from equihome_sim_sdk.models.leverage_event import LeverageEvent

# TODO update the JSON string below
json = "{}"
# create an instance of LeverageEvent from a JSON string
leverage_event_instance = LeverageEvent.from_json(json)
# print the JSON string representation of the object
print(LeverageEvent.to_json())

# convert the object into a dict
leverage_event_dict = leverage_event_instance.to_dict()
# create an instance of LeverageEvent from a dict
leverage_event_from_dict = LeverageEvent.from_dict(leverage_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


