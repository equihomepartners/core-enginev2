# SensitivityAnalysis

Sensitivity analysis model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parameter_variations** | [**List[ParameterVariation]**](ParameterVariation.md) | Parameter variations | 
**tornado_chart** | [**List[TornadoChartItem]**](TornadoChartItem.md) | Tornado chart data | 

## Example

```python
from equihome_sim_sdk.models.sensitivity_analysis import SensitivityAnalysis

# TODO update the JSON string below
json = "{}"
# create an instance of SensitivityAnalysis from a JSON string
sensitivity_analysis_instance = SensitivityAnalysis.from_json(json)
# print the JSON string representation of the object
print(SensitivityAnalysis.to_json())

# convert the object into a dict
sensitivity_analysis_dict = sensitivity_analysis_instance.to_dict()
# create an instance of SensitivityAnalysis from a dict
sensitivity_analysis_from_dict = SensitivityAnalysis.from_dict(sensitivity_analysis_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


