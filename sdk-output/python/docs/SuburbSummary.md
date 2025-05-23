# SuburbSummary

Suburb summary model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**suburb_id** | **str** | Suburb ID | 
**name** | **str** | Suburb name | 
**state** | **str** | State | 
**postcode** | **str** | Postcode | 
**latitude** | **float** | Latitude | 
**longitude** | **float** | Longitude | 
**zone_category** | **str** | Zone category (green, orange, red) | 
**overall_score** | **float** | Overall score (0-100) | 

## Example

```python
from equihome_sim_sdk.models.suburb_summary import SuburbSummary

# TODO update the JSON string below
json = "{}"
# create an instance of SuburbSummary from a JSON string
suburb_summary_instance = SuburbSummary.from_json(json)
# print the JSON string representation of the object
print(SuburbSummary.to_json())

# convert the object into a dict
suburb_summary_dict = suburb_summary_instance.to_dict()
# create an instance of SuburbSummary from a dict
suburb_summary_from_dict = SuburbSummary.from_dict(suburb_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


