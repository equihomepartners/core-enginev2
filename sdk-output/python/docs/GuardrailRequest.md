# GuardrailRequest

Guardrail request model.  Attributes:     simulation_id: Simulation ID

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 

## Example

```python
from equihome_sim_sdk.models.guardrail_request import GuardrailRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GuardrailRequest from a JSON string
guardrail_request_instance = GuardrailRequest.from_json(json)
# print the JSON string representation of the object
print(GuardrailRequest.to_json())

# convert the object into a dict
guardrail_request_dict = guardrail_request_instance.to_dict()
# create an instance of GuardrailRequest from a dict
guardrail_request_from_dict = GuardrailRequest.from_dict(guardrail_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


