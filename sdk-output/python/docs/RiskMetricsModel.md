# RiskMetricsModel

Risk metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_95** | **float** | Value at Risk (95%) | [optional] 
**var_99** | **float** | Value at Risk (99%) | [optional] 
**cvar_95** | **float** | Conditional Value at Risk (95%) | [optional] 
**cvar_99** | **float** | Conditional Value at Risk (99%) | [optional] 
**max_drawdown** | **float** | Maximum Drawdown | [optional] 
**volatility** | **float** | Volatility (standard deviation of returns) | [optional] 
**downside_deviation** | **float** | Downside Deviation | [optional] 
**tail_risk** | **float** | Tail Risk | [optional] 
**tail_probability** | **float** | Tail Probability | [optional] 
**tail_severity** | **float** | Tail Severity | [optional] 

## Example

```python
from equihome_sim_sdk.models.risk_metrics_model import RiskMetricsModel

# TODO update the JSON string below
json = "{}"
# create an instance of RiskMetricsModel from a JSON string
risk_metrics_model_instance = RiskMetricsModel.from_json(json)
# print the JSON string representation of the object
print(RiskMetricsModel.to_json())

# convert the object into a dict
risk_metrics_model_dict = risk_metrics_model_instance.to_dict()
# create an instance of RiskMetricsModel from a dict
risk_metrics_model_from_dict = RiskMetricsModel.from_dict(risk_metrics_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


