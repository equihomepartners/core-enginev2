# BreachModel

Breach model.  Attributes:     code: Breach code     severity: Breach severity     message: Breach message     value: Actual value that triggered the breach     threshold: Threshold value that was breached     unit: Unit of measurement     layer: Layer where the breach occurred (Unit, Zone, Portfolio, etc.)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Breach code | 
**severity** | **str** | Breach severity (INFO, WARN, FAIL) | 
**message** | **str** | Breach message | 
**value** | **float** | Actual value that triggered the breach | [optional] 
**threshold** | **float** | Threshold value that was breached | [optional] 
**unit** | **str** | Unit of measurement | [optional] 
**layer** | **str** | Layer where the breach occurred (Unit, Zone, Portfolio, etc.) | [optional] 

## Example

```python
from equihome_sim_sdk.models.breach_model import BreachModel

# TODO update the JSON string below
json = "{}"
# create an instance of BreachModel from a JSON string
breach_model_instance = BreachModel.from_json(json)
# print the JSON string representation of the object
print(BreachModel.to_json())

# convert the object into a dict
breach_model_dict = breach_model_instance.to_dict()
# create an instance of BreachModel from a dict
breach_model_from_dict = BreachModel.from_dict(breach_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


