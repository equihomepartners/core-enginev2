# RiskMetricsRequest

Request model for risk metrics calculation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**var_confidence_level** | **float** | Confidence level for Value at Risk (VaR) calculation (0-1) | [optional] 
**risk_free_rate** | **float** | Risk-free rate for risk-adjusted return calculations (0-1) | [optional] 
**benchmark_return** | **float** | Benchmark return for alpha and information ratio calculations (0-1) | [optional] 
**min_acceptable_return** | **float** | Minimum acceptable return for Sortino ratio calculation (0-1) | [optional] 
**tail_risk_threshold** | **float** | Threshold for tail risk calculation (0-1) | [optional] 
**monte_carlo_simulations** | **int** | Number of Monte Carlo simulations for risk metrics | [optional] 
**enable_sensitivity_analysis** | **bool** | Whether to enable sensitivity analysis | [optional] 
**sensitivity_parameters** | **List[str]** | Parameters to analyze in sensitivity analysis | [optional] 

## Example

```python
from equihome_sim_sdk.models.risk_metrics_request import RiskMetricsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RiskMetricsRequest from a JSON string
risk_metrics_request_instance = RiskMetricsRequest.from_json(json)
# print the JSON string representation of the object
print(RiskMetricsRequest.to_json())

# convert the object into a dict
risk_metrics_request_dict = risk_metrics_request_instance.to_dict()
# create an instance of RiskMetricsRequest from a dict
risk_metrics_request_from_dict = RiskMetricsRequest.from_dict(risk_metrics_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


