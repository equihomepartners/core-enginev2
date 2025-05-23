# ConcentrationMetrics

Concentration metrics model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**herfindahl_index** | **float** | Herfindahl-Hirschman Index (HHI) | [optional] 
**zone_concentration** | [**ZoneConcentration**](ZoneConcentration.md) | Zone concentration metrics | [optional] 
**suburb_concentration** | [**SuburbConcentration**](SuburbConcentration.md) | Suburb concentration metrics | [optional] 

## Example

```python
from equihome_sim_sdk.models.concentration_metrics import ConcentrationMetrics

# TODO update the JSON string below
json = "{}"
# create an instance of ConcentrationMetrics from a JSON string
concentration_metrics_instance = ConcentrationMetrics.from_json(json)
# print the JSON string representation of the object
print(ConcentrationMetrics.to_json())

# convert the object into a dict
concentration_metrics_dict = concentration_metrics_instance.to_dict()
# create an instance of ConcentrationMetrics from a dict
concentration_metrics_from_dict = ConcentrationMetrics.from_dict(concentration_metrics_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


