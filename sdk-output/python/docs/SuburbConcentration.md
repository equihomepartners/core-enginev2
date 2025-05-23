# SuburbConcentration

Suburb concentration model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**top_5_pct** | **float** | Percentage in top 5 suburbs | [optional] 
**top_10_pct** | **float** | Percentage in top 10 suburbs | [optional] 
**hhi** | **float** | Suburb HHI | [optional] 

## Example

```python
from equihome_sim_sdk.models.suburb_concentration import SuburbConcentration

# TODO update the JSON string below
json = "{}"
# create an instance of SuburbConcentration from a JSON string
suburb_concentration_instance = SuburbConcentration.from_json(json)
# print the JSON string representation of the object
print(SuburbConcentration.to_json())

# convert the object into a dict
suburb_concentration_dict = suburb_concentration_instance.to_dict()
# create an instance of SuburbConcentration from a dict
suburb_concentration_from_dict = SuburbConcentration.from_dict(suburb_concentration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


