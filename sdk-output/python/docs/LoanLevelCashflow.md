# LoanLevelCashflow

Loan-level cashflow model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**loan_id** | **str** | Loan ID | 
**origination** | **object** | Origination cashflows | 
**exit** | **object** | Exit cashflows | [optional] 

## Example

```python
from equihome_sim_sdk.models.loan_level_cashflow import LoanLevelCashflow

# TODO update the JSON string below
json = "{}"
# create an instance of LoanLevelCashflow from a JSON string
loan_level_cashflow_instance = LoanLevelCashflow.from_json(json)
# print the JSON string representation of the object
print(LoanLevelCashflow.to_json())

# convert the object into a dict
loan_level_cashflow_dict = loan_level_cashflow_instance.to_dict()
# create an instance of LoanLevelCashflow from a dict
loan_level_cashflow_from_dict = LoanLevelCashflow.from_dict(loan_level_cashflow_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


