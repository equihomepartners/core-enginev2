# ReserveAccountResponse

Reserve account response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **float** | Year | 
**month** | **int** | Month | 
**balance** | **float** | Reserve account balance | 
**target_balance** | **float** | Target reserve account balance | 
**deposits** | **float** | Deposits to the reserve account | 
**withdrawals** | **float** | Withdrawals from the reserve account | 

## Example

```python
from equihome_sim_sdk.models.reserve_account_response import ReserveAccountResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReserveAccountResponse from a JSON string
reserve_account_response_instance = ReserveAccountResponse.from_json(json)
# print the JSON string representation of the object
print(ReserveAccountResponse.to_json())

# convert the object into a dict
reserve_account_response_dict = reserve_account_response_instance.to_dict()
# create an instance of ReserveAccountResponse from a dict
reserve_account_response_from_dict = ReserveAccountResponse.from_dict(reserve_account_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


