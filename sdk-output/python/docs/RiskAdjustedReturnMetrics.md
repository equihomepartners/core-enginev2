# RiskAdjustedReturnMetrics

Risk-adjusted return metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sharpe_ratio** | **float** | Sharpe Ratio | [optional] 
**sortino_ratio** | **float** | Sortino Ratio | [optional] 
**calmar_ratio** | **float** | Calmar Ratio | [optional] 
**information_ratio** | **float** | Information Ratio | [optional] 
**treynor_ratio** | **float** | Treynor Ratio | [optional] 
**omega_ratio** | **float** | Omega Ratio | [optional] 
**kappa_ratio** | **float** | Kappa Ratio | [optional] 
**gain_loss_ratio** | **float** | Gain-Loss Ratio | [optional] 

## Example

```python
from equihome_sim_sdk.models.risk_adjusted_return_metrics import RiskAdjustedReturnMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of RiskAdjustedReturnMetrics from a JSON string
risk_adjusted_return_metrics_instance = RiskAdjustedReturnMetrics.from_json(json)
# print the JSON string representation of the object
print(RiskAdjustedReturnMetrics.to_json())

# convert the object into a dict
risk_adjusted_return_metrics_dict = risk_adjusted_return_metrics_instance.to_dict()
# create an instance of RiskAdjustedReturnMetrics from a dict
risk_adjusted_return_metrics_from_dict = RiskAdjustedReturnMetrics.from_dict(risk_adjusted_return_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


