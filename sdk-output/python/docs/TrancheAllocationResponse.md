# TrancheAllocationResponse

Tranche allocation response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**loan_id** | **str** | Loan ID | 
**allocation_percentage** | **float** | Percentage of the loan allocated to this tranche | 
**allocation_amount** | **float** | Amount of the loan allocated to this tranche | 
**zone** | **str** | Zone of the loan | 
**ltv** | **float** | LTV of the loan | 

## Example

```python
from equihome_sim_sdk.models.tranche_allocation_response import TrancheAllocationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TrancheAllocationResponse from a JSON string
tranche_allocation_response_instance = TrancheAllocationResponse.from_json(json)
# print the JSON string representation of the object
print(TrancheAllocationResponse.to_json())

# convert the object into a dict
tranche_allocation_response_dict = tranche_allocation_response_instance.to_dict()
# create an instance of TrancheAllocationResponse from a dict
tranche_allocation_response_from_dict = TrancheAllocationResponse.from_dict(tranche_allocation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


