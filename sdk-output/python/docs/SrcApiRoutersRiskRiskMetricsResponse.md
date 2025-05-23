# SrcApiRoutersRiskRiskMetricsResponse

Response model for risk metrics calculation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**market_price_metrics** | [**MarketPriceMetrics**](MarketPriceMetrics.md) | Market/price metrics | 
**credit_metrics** | [**CreditMetrics**](CreditMetrics.md) | Credit metrics | 
**liquidity_metrics** | [**SrcApiRoutersRiskLiquidityMetrics**](SrcApiRoutersRiskLiquidityMetrics.md) | Liquidity metrics | 
**leverage_metrics** | [**SrcApiRoutersRiskLeverageMetrics**](SrcApiRoutersRiskLeverageMetrics.md) | Leverage metrics | 
**concentration_metrics** | [**ConcentrationMetrics**](ConcentrationMetrics.md) | Concentration metrics | 
**performance_metrics** | [**PerformanceMetrics**](PerformanceMetrics.md) | Performance/return-risk metrics | 
**return_metrics** | [**ReturnMetrics**](ReturnMetrics.md) | Return metrics | 
**risk_metrics** | [**RiskMetricsModel**](RiskMetricsModel.md) | Risk metrics | 
**risk_adjusted_return_metrics** | [**RiskAdjustedReturnMetrics**](RiskAdjustedReturnMetrics.md) | Risk-adjusted return metrics | 
**market_metrics** | [**MarketMetrics**](MarketMetrics.md) | Market metrics | 
**stress_test_results** | [**Dict[str, SrcApiRoutersRiskStressTestResult]**](SrcApiRoutersRiskStressTestResult.md) | Stress test results | 
**sensitivity_analysis** | **Dict[str, List[SensitivityResult]]** | Sensitivity analysis results | 
**visualization** | [**RiskVisualization**](RiskVisualization.md) | Visualization data | 

## Example

```python
from equihome_sim_sdk.models.src_api_routers_risk_risk_metrics_response import SrcApiRoutersRiskRiskMetricsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SrcApiRoutersRiskRiskMetricsResponse from a JSON string
src_api_routers_risk_risk_metrics_response_instance = SrcApiRoutersRiskRiskMetricsResponse.from_json(json)
# print the JSON string representation of the object
print(SrcApiRoutersRiskRiskMetricsResponse.to_json())

# convert the object into a dict
src_api_routers_risk_risk_metrics_response_dict = src_api_routers_risk_risk_metrics_response_instance.to_dict()
# create an instance of SrcApiRoutersRiskRiskMetricsResponse from a dict
src_api_routers_risk_risk_metrics_response_from_dict = SrcApiRoutersRiskRiskMetricsResponse.from_dict(src_api_routers_risk_risk_metrics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


