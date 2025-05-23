# PropertyValueResponse

Property value response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**property_id** | **str** | Property ID | 
**initial_value** | **float** | Initial property value | 
**current_value** | **float** | Current property value | 
**appreciation** | **float** | Appreciation percentage | 
**month** | **int** | Month index (0-based) | 
**year** | **float** | Year | 

## Example

```python
from equihome_sim_sdk.models.property_value_response import PropertyValueResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PropertyValueResponse from a JSON string
property_value_response_instance = PropertyValueResponse.from_json(json)
# print the JSON string representation of the object
print(PropertyValueResponse.to_json())

# convert the object into a dict
property_value_response_dict = property_value_response_instance.to_dict()
# create an instance of PropertyValueResponse from a dict
property_value_response_from_dict = PropertyValueResponse.from_dict(property_value_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


