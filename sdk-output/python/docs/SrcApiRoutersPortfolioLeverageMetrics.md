# SrcApiRoutersPortfolioLeverageMetrics

Leverage metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_debt** | **float** | Total debt outstanding | 
**total_available** | **float** | Total available debt capacity | 
**total_interest_paid** | **float** | Total interest paid | 
**total_commitment_fees_paid** | **float** | Total commitment fees paid | 
**weighted_avg_interest_rate** | **float** | Weighted average interest rate | 
**leverage_ratio** | **float** | Leverage ratio (debt / NAV) | 
**debt_service_coverage_ratio** | **float** | Debt service coverage ratio | 
**interest_coverage_ratio** | **float** | Interest coverage ratio | 
**loan_to_value_ratio** | **float** | Loan-to-value ratio | 

## Example

```python
from equihome_sim_sdk.models.src_api_routers_portfolio_leverage_metrics import SrcApiRoutersPortfolioLeverageMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of SrcApiRoutersPortfolioLeverageMetrics from a JSON string
src_api_routers_portfolio_leverage_metrics_instance = SrcApiRoutersPortfolioLeverageMetrics.from_json(json)
# print the JSON string representation of the object
print(SrcApiRoutersPortfolioLeverageMetrics.to_json())

# convert the object into a dict
src_api_routers_portfolio_leverage_metrics_dict = src_api_routers_portfolio_leverage_metrics_instance.to_dict()
# create an instance of SrcApiRoutersPortfolioLeverageMetrics from a dict
src_api_routers_portfolio_leverage_metrics_from_dict = SrcApiRoutersPortfolioLeverageMetrics.from_dict(src_api_routers_portfolio_leverage_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


