# LoanExitRequest

Loan exit request model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**loan_id** | **str** | Loan ID | 
**property_id** | **str** | Property ID | 
**suburb_id** | **str** | Suburb ID (optional) | [optional] [default to '']
**zone** | **str** | Zone name | 
**loan_amount** | **float** | Loan amount | 
**property_value** | **float** | Initial property value | 
**exit_month** | **int** | Exit month (0-based) | 
**exit_type** | **str** | Exit type (sale, refinance, default, term_completion) | 

## Example

```python
from equihome_sim_sdk.models.loan_exit_request import LoanExitRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LoanExitRequest from a JSON string
loan_exit_request_instance = LoanExitRequest.from_json(json)
# print the JSON string representation of the object
print(LoanExitRequest.to_json())

# convert the object into a dict
loan_exit_request_dict = loan_exit_request_instance.to_dict()
# create an instance of LoanExitRequest from a dict
loan_exit_request_from_dict = LoanExitRequest.from_dict(loan_exit_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


