# PropertyValueRequest

Property value request model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**property_id** | **str** | Property ID | 
**zone** | **str** | Zone name | 
**suburb_id** | **str** | Suburb ID (optional) | [optional] [default to '']
**initial_value** | **float** | Initial property value | 
**month** | **int** | Month index (0-based) | 

## Example

```python
from equihome_sim_sdk.models.property_value_request import PropertyValueRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PropertyValueRequest from a JSON string
property_value_request_instance = PropertyValueRequest.from_json(json)
# print the JSON string representation of the object
print(PropertyValueRequest.to_json())

# convert the object into a dict
property_value_request_dict = property_value_request_instance.to_dict()
# create an instance of PropertyValueRequest from a dict
property_value_request_from_dict = PropertyValueRequest.from_dict(property_value_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


