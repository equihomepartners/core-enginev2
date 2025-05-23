# ConcentrationPoint

Concentration chart point model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **str** | Category (e.g., zone, suburb) | 
**name** | **str** | Name (e.g., &#39;green&#39;, &#39;Bondi&#39;) | 
**value** | **float** | Concentration value | 
**percentage** | **float** | Percentage of total | 

## Example

```python
from equihome_sim_sdk.models.concentration_point import ConcentrationPoint

# TODO update the JSON string below
json = "{}"
# create an instance of ConcentrationPoint from a JSON string
concentration_point_instance = ConcentrationPoint.from_json(json)
# print the JSON string representation of the object
print(ConcentrationPoint.to_json())

# convert the object into a dict
concentration_point_dict = concentration_point_instance.to_dict()
# create an instance of ConcentrationPoint from a dict
concentration_point_from_dict = ConcentrationPoint.from_dict(concentration_point_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


