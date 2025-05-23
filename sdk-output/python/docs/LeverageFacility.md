# LeverageFacility

Leverage facility model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**facility_id** | **str** | Facility ID | 
**facility_type** | **str** | Facility type (nav_line, subscription_line) | 
**max_amount** | **float** | Maximum facility amount | 
**interest_rate** | **float** | Annual interest rate (as a decimal) | 
**commitment_fee_bps** | **float** | Commitment fee on undrawn balance (basis points) | 
**term_years** | **float** | Term of the facility in years | 
**advance_rate** | **float** | Maximum advance rate (for NAV lines) | [optional] 
**current_balance** | **float** | Current outstanding balance | 
**available_amount** | **float** | Available amount to draw | 
**inception_date** | **str** | Date when the facility was first drawn | [optional] 
**maturity_date** | **str** | Date when the facility matures | [optional] 

## Example

```python
from equihome_sim_sdk.models.leverage_facility import LeverageFacility

# TODO update the JSON string below
json = "{}"
# create an instance of LeverageFacility from a JSON string
leverage_facility_instance = LeverageFacility.from_json(json)
# print the JSON string representation of the object
print(LeverageFacility.to_json())

# convert the object into a dict
leverage_facility_dict = leverage_facility_instance.to_dict()
# create an instance of LeverageFacility from a dict
leverage_facility_from_dict = LeverageFacility.from_dict(leverage_facility_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


