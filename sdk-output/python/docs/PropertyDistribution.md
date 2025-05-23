# PropertyDistribution

Property distribution model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_properties** | **int** | Total number of properties | 
**property_types** | **Dict[str, int]** | Distribution by property type | 
**bedrooms** | **Dict[str, int]** | Distribution by number of bedrooms | 
**bathrooms** | **Dict[str, int]** | Distribution by number of bathrooms | 
**value_distribution** | **List[object]** | Distribution by value | 
**zone_distribution** | **Dict[str, int]** | Distribution by zone | 

## Example

```python
from equihome_sim_sdk.models.property_distribution import PropertyDistribution

# TODO update the JSON string below
json = "{}"
# create an instance of PropertyDistribution from a JSON string
property_distribution_instance = PropertyDistribution.from_json(json)
# print the JSON string representation of the object
print(PropertyDistribution.to_json())

# convert the object into a dict
property_distribution_dict = property_distribution_instance.to_dict()
# create an instance of PropertyDistribution from a dict
property_distribution_from_dict = PropertyDistribution.from_dict(property_distribution_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


