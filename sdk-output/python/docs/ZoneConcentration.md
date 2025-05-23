# ZoneConcentration

Zone concentration model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**green** | **float** | Concentration in green zone | [optional] 
**orange** | **float** | Concentration in orange zone | [optional] 
**red** | **float** | Concentration in red zone | [optional] 
**hhi** | **float** | Zone HHI | [optional] 

## Example

```python
from equihome_sim_sdk.models.zone_concentration import ZoneConcentration

# TODO update the JSON string below
json = "{}"
# create an instance of ZoneConcentration from a JSON string
zone_concentration_instance = ZoneConcentration.from_json(json)
# print the JSON string representation of the object
print(ZoneConcentration.to_json())

# convert the object into a dict
zone_concentration_dict = zone_concentration_instance.to_dict()
# create an instance of ZoneConcentration from a dict
zone_concentration_from_dict = ZoneConcentration.from_dict(zone_concentration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


