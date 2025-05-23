# PerformanceMetrics

Performance/return-risk metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**net_irr** | **float** | Net-IRR point value | [optional] 
**sharpe_ratio** | **float** | Sharpe ratio | [optional] 
**sortino_ratio** | **float** | Sortino ratio | [optional] 
**hurdle_clear_probability** | **object** | Hurdle-clear probability | 
**calmar_ratio** | **float** | Calmar ratio | [optional] 
**information_ratio** | **float** | Information ratio | [optional] 
**treynor_ratio** | **float** | Treynor ratio | [optional] 
**omega_ratio** | **float** | Omega ratio | [optional] 
**kappa_ratio** | **float** | Kappa ratio | [optional] 
**gain_loss_ratio** | **float** | Gain-Loss ratio | [optional] 

## Example

```python
from equihome_sim_sdk.models.performance_metrics import PerformanceMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of PerformanceMetrics from a JSON string
performance_metrics_instance = PerformanceMetrics.from_json(json)
# print the JSON string representation of the object
print(PerformanceMetrics.to_json())

# convert the object into a dict
performance_metrics_dict = performance_metrics_instance.to_dict()
# create an instance of PerformanceMetrics from a dict
performance_metrics_from_dict = PerformanceMetrics.from_dict(performance_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


