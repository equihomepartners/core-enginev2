# LoanPortfolio

Loan portfolio model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**stats** | **object** | Portfolio statistics | [optional] 
**visualization** | **object** | Visualization data | [optional] 

## Example

```python
from equihome_sim_sdk.models.loan_portfolio import LoanPortfolio

# TODO update the JSON string below
json = "{}"
# create an instance of LoanPortfolio from a JSON string
loan_portfolio_instance = LoanPortfolio.from_json(json)
# print the JSON string representation of the object
print(LoanPortfolio.to_json())

# convert the object into a dict
loan_portfolio_dict = loan_portfolio_instance.to_dict()
# create an instance of LoanPortfolio from a dict
loan_portfolio_from_dict = LoanPortfolio.from_dict(loan_portfolio_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


