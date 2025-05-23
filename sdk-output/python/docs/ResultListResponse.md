# ResultListResponse

Result list response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[ResultResponse]**](ResultResponse.md) | List of results | 
**count** | **int** | Total count | 
**limit** | **int** | Limit | 
**offset** | **int** | Offset | 

## Example

```python
from equihome_sim_sdk.models.result_list_response import ResultListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ResultListResponse from a JSON string
result_list_response_instance = ResultListResponse.from_json(json)
# print the JSON string representation of the object
print(ResultListResponse.to_json())

# convert the object into a dict
result_list_response_dict = result_list_response_instance.to_dict()
# create an instance of ResultListResponse from a dict
result_list_response_from_dict = ResultListResponse.from_dict(result_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


