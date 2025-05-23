# RiskVisualization

Risk visualization model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**risk_return_scatter** | [**List[RiskReturnPoint]**](RiskReturnPoint.md) | Risk-return scatter plot data | 
**var_histogram** | [**VarHistogram**](VarHistogram.md) | VaR histogram data | 
**drawdown_chart** | [**List[DrawdownPoint]**](DrawdownPoint.md) | Drawdown chart data | 
**stress_test_comparison** | [**List[StressTestComparisonPoint]**](StressTestComparisonPoint.md) | Stress test comparison chart data | 
**sensitivity_charts** | **Dict[str, List[SensitivityChart]]** | Sensitivity charts data | 
**concentration_chart** | [**List[ConcentrationPoint]**](ConcentrationPoint.md) | Concentration chart data | 

## Example

```python
from equihome_sim_sdk.models.risk_visualization import RiskVisualization

# TODO update the JSON string below
json = "{}"
# create an instance of RiskVisualization from a JSON string
risk_visualization_instance = RiskVisualization.from_json(json)
# print the JSON string representation of the object
print(RiskVisualization.to_json())

# convert the object into a dict
risk_visualization_dict = risk_visualization_instance.to_dict()
# create an instance of RiskVisualization from a dict
risk_visualization_from_dict = RiskVisualization.from_dict(risk_visualization_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


