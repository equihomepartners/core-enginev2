# SuburbDetail

Suburb detail model.

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
**appreciation_score** | **float** | Appreciation score (0-100) | 
**risk_score** | **float** | Risk score (0-100) | 
**liquidity_score** | **float** | Liquidity score (0-100) | 
**appreciation_confidence** | **float** | Appreciation confidence (0-1) | 
**risk_confidence** | **float** | Risk confidence (0-1) | 
**liquidity_confidence** | **float** | Liquidity confidence (0-1) | 
**overall_confidence** | **float** | Overall confidence (0-1) | 
**metrics** | [**Dict[str, MetricValue]**](MetricValue.md) | Metrics | 
**property_count** | **int** | Number of properties | 

## Example

```python
from equihome_sim_sdk.models.suburb_detail import SuburbDetail

# TODO update the JSON string below
json = "{}"
# create an instance of SuburbDetail from a JSON string
suburb_detail_instance = SuburbDetail.from_json(json)
# print the JSON string representation of the object
print(SuburbDetail.to_json())

# convert the object into a dict
suburb_detail_dict = suburb_detail_instance.to_dict()
# create an instance of SuburbDetail from a dict
suburb_detail_from_dict = SuburbDetail.from_dict(suburb_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


