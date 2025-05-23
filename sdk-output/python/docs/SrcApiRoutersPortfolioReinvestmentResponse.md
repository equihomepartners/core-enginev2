# SrcApiRoutersPortfolioReinvestmentResponse

Reinvestment response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**loans** | [**List[Loan]**](Loan.md) | Generated reinvestment loans | 
**total_loan_amount** | **float** | Total loan amount | 
**num_loans** | **int** | Number of loans generated | 

## Example

```python
from equihome_sim_sdk.models.src_api_routers_portfolio_reinvestment_response import SrcApiRoutersPortfolioReinvestmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SrcApiRoutersPortfolioReinvestmentResponse from a JSON string
src_api_routers_portfolio_reinvestment_response_instance = SrcApiRoutersPortfolioReinvestmentResponse.from_json(json)
# print the JSON string representation of the object
print(SrcApiRoutersPortfolioReinvestmentResponse.to_json())

# convert the object into a dict
src_api_routers_portfolio_reinvestment_response_dict = src_api_routers_portfolio_reinvestment_response_instance.to_dict()
# create an instance of SrcApiRoutersPortfolioReinvestmentResponse from a dict
src_api_routers_portfolio_reinvestment_response_from_dict = SrcApiRoutersPortfolioReinvestmentResponse.from_dict(src_api_routers_portfolio_reinvestment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


