# ZoneDistribution

Zone distribution model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**green** | **int** | Number of suburbs in green zone | 
**orange** | **int** | Number of suburbs in orange zone | 
**red** | **int** | Number of suburbs in red zone | 
**total** | **int** | Total number of suburbs | 
**green_percentage** | **float** | Percentage of suburbs in green zone | 
**orange_percentage** | **float** | Percentage of suburbs in orange zone | 
**red_percentage** | **float** | Percentage of suburbs in red zone | 

## Example

```python
from equihome_sim_sdk.models.zone_distribution import ZoneDistribution

# TODO update the JSON string below
json = "{}"
# create an instance of ZoneDistribution from a JSON string
zone_distribution_instance = ZoneDistribution.from_json(json)
# print the JSON string representation of the object
print(ZoneDistribution.to_json())

# convert the object into a dict
zone_distribution_dict = zone_distribution_instance.to_dict()
# create an instance of ZoneDistribution from a dict
zone_distribution_from_dict = ZoneDistribution.from_dict(zone_distribution_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


