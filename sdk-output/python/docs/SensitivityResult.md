# SensitivityResult

Sensitivity result model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parameter_value** | **float** | Parameter value | 
**irr** | **float** | IRR at this parameter value | [optional] 
**equity_multiple** | **float** | Equity multiple at this parameter value | [optional] 
**roi** | **float** | ROI at this parameter value | [optional] 

## Example

```python
from equihome_sim_sdk.models.sensitivity_result import SensitivityResult

# TODO update the JSON string below
json = "{}"
# create an instance of SensitivityResult from a JSON string
sensitivity_result_instance = SensitivityResult.from_json(json)
# print the JSON string representation of the object
print(SensitivityResult.to_json())

# convert the object into a dict
sensitivity_result_dict = sensitivity_result_instance.to_dict()
# create an instance of SensitivityResult from a dict
sensitivity_result_from_dict = SensitivityResult.from_dict(sensitivity_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


