# TrancheCashflowResponse

Tranche cashflow response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **float** | Year | 
**month** | **int** | Month (if applicable) | [optional] 
**quarter** | **int** | Quarter (if applicable) | [optional] 
**principal_payment** | **float** | Principal payment | 
**interest_payment** | **float** | Interest payment | 
**profit_share_payment** | **float** | Profit share payment | 
**total_payment** | **float** | Total payment | 
**remaining_principal** | **float** | Remaining principal | 

## Example

```python
from equihome_sim_sdk.models.tranche_cashflow_response import TrancheCashflowResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TrancheCashflowResponse from a JSON string
tranche_cashflow_response_instance = TrancheCashflowResponse.from_json(json)
# print the JSON string representation of the object
print(TrancheCashflowResponse.to_json())

# convert the object into a dict
tranche_cashflow_response_dict = tranche_cashflow_response_instance.to_dict()
# create an instance of TrancheCashflowResponse from a dict
tranche_cashflow_response_from_dict = TrancheCashflowResponse.from_dict(tranche_cashflow_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


