# CashReserve

Cash reserve model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** | Year | 
**month** | **int** | Month | 
**cash_reserve** | **float** | Cash reserve | 
**minimum_required** | **float** | Minimum required cash reserve | 
**shortfall** | **float** | Shortfall (if any) | 

## Example

```python
from equihome_sim_sdk.models.cash_reserve import CashReserve

# TODO update the JSON string below
json = "{}"
# create an instance of CashReserve from a JSON string
cash_reserve_instance = CashReserve.from_json(json)
# print the JSON string representation of the object
print(CashReserve.to_json())

# convert the object into a dict
cash_reserve_dict = cash_reserve_instance.to_dict()
# create an instance of CashReserve from a dict
cash_reserve_from_dict = CashReserve.from_dict(cash_reserve_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


