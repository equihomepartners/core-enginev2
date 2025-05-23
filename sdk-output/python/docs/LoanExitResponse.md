# LoanExitResponse

Loan exit response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**loan_id** | **str** | Loan ID | 
**property_id** | **str** | Property ID | 
**loan_amount** | **float** | Loan amount | 
**property_value** | **float** | Initial property value | 
**current_value** | **float** | Current property value | 
**appreciation** | **float** | Appreciation percentage | 
**exit_month** | **int** | Exit month (0-based) | 
**exit_year** | **float** | Exit year | 
**exit_type** | **str** | Exit type | 
**exit_value** | **float** | Exit value | 
**appreciation_share_amount** | **float** | Appreciation share amount | 
**total_return** | **float** | Total return | 
**roi** | **float** | ROI | 
**annualized_roi** | **float** | Annualized ROI | 

## Example

```python
from equihome_sim_sdk.models.loan_exit_response import LoanExitResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LoanExitResponse from a JSON string
loan_exit_response_instance = LoanExitResponse.from_json(json)
# print the JSON string representation of the object
print(LoanExitResponse.to_json())

# convert the object into a dict
loan_exit_response_dict = loan_exit_response_instance.to_dict()
# create an instance of LoanExitResponse from a dict
loan_exit_response_from_dict = LoanExitResponse.from_dict(loan_exit_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


