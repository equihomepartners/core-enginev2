# GuardrailReportModel

Guardrail report model.  Attributes:     simulation_id: Simulation ID     worst_level: Worst severity level in the report     breaches: List of breaches

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | [optional] 
**worst_level** | **str** | Worst severity level in the report (INFO, WARN, FAIL) | 
**breaches** | [**List[BreachModel]**](BreachModel.md) | List of breaches | [optional] 

## Example

```python
from equihome_sim_sdk.models.guardrail_report_model import GuardrailReportModel

# TODO update the JSON string below
json = "{}"
# create an instance of GuardrailReportModel from a JSON string
guardrail_report_model_instance = GuardrailReportModel.from_json(json)
# print the JSON string representation of the object
print(GuardrailReportModel.to_json())

# convert the object into a dict
guardrail_report_model_dict = guardrail_report_model_instance.to_dict()
# create an instance of GuardrailReportModel from a dict
guardrail_report_model_from_dict = GuardrailReportModel.from_dict(guardrail_report_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


