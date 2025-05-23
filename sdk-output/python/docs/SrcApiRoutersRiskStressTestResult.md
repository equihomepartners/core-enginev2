# SrcApiRoutersRiskStressTestResult

Stress test result model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**irr** | **float** | IRR under stress scenario | [optional] 
**equity_multiple** | **float** | Equity multiple under stress scenario | [optional] 
**roi** | **float** | ROI under stress scenario | [optional] 
**max_drawdown** | **float** | Maximum drawdown under stress scenario | [optional] 
**var_95** | **float** | VaR (95%) under stress scenario | [optional] 
**impact_pct** | **float** | Percentage impact on base case IRR | [optional] 

## Example

```python
from equihome_sim_sdk.models.src_api_routers_risk_stress_test_result import SrcApiRoutersRiskStressTestResult

# TODO update the JSON string below
json = "{}"
# create an instance of SrcApiRoutersRiskStressTestResult from a JSON string
src_api_routers_risk_stress_test_result_instance = SrcApiRoutersRiskStressTestResult.from_json(json)
# print the JSON string representation of the object
print(SrcApiRoutersRiskStressTestResult.to_json())

# convert the object into a dict
src_api_routers_risk_stress_test_result_dict = src_api_routers_risk_stress_test_result_instance.to_dict()
# create an instance of SrcApiRoutersRiskStressTestResult from a dict
src_api_routers_risk_stress_test_result_from_dict = SrcApiRoutersRiskStressTestResult.from_dict(src_api_routers_risk_stress_test_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


