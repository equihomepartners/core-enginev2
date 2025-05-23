# ResultResponse

Result response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**status** | **str** | Simulation status | 
**created_at** | **str** | Creation timestamp | 
**completed_at** | **str** | Completion timestamp | [optional] 
**metrics** | **object** | Simulation metrics | [optional] 
**execution_time** | **float** | Execution time in seconds | [optional] 
**num_loans** | **int** | Number of loans | [optional] 
**guardrail_violations** | **List[str]** | Guardrail violations | [optional] 

## Example

```python
from equihome_sim_sdk.models.result_response import ResultResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ResultResponse from a JSON string
result_response_instance = ResultResponse.from_json(json)
# print the JSON string representation of the object
print(ResultResponse.to_json())

# convert the object into a dict
result_response_dict = result_response_instance.to_dict()
# create an instance of ResultResponse from a dict
result_response_from_dict = ResultResponse.from_dict(result_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


