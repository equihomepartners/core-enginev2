# ParameterVariation

Parameter variation model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parameter** | **str** | Parameter name | 
**value** | **float** | Parameter value | 
**metrics** | **Dict[str, float]** | Metrics for this parameter value | 

## Example

```python
from equihome_sim_sdk.models.parameter_variation import ParameterVariation

# TODO update the JSON string below
json = "{}"
# create an instance of ParameterVariation from a JSON string
parameter_variation_instance = ParameterVariation.from_json(json)
# print the JSON string representation of the object
print(ParameterVariation.to_json())

# convert the object into a dict
parameter_variation_dict = parameter_variation_instance.to_dict()
# create an instance of ParameterVariation from a dict
parameter_variation_from_dict = ParameterVariation.from_dict(parameter_variation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


