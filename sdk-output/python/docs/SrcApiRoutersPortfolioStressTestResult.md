# SrcApiRoutersPortfolioStressTestResult

Stress test result model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_compliant** | **bool** | Whether the test is compliant | 
**details** | **object** | Test details | 

## Example

```python
from equihome_sim_sdk.models.src_api_routers_portfolio_stress_test_result import SrcApiRoutersPortfolioStressTestResult

# TODO update the JSON string below
json = "{}"
# create an instance of SrcApiRoutersPortfolioStressTestResult from a JSON string
src_api_routers_portfolio_stress_test_result_instance = SrcApiRoutersPortfolioStressTestResult.from_json(json)
# print the JSON string representation of the object
print(SrcApiRoutersPortfolioStressTestResult.to_json())

# convert the object into a dict
src_api_routers_portfolio_stress_test_result_dict = src_api_routers_portfolio_stress_test_result_instance.to_dict()
# create an instance of SrcApiRoutersPortfolioStressTestResult from a dict
src_api_routers_portfolio_stress_test_result_from_dict = SrcApiRoutersPortfolioStressTestResult.from_dict(src_api_routers_portfolio_stress_test_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


