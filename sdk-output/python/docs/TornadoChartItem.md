# TornadoChartItem

Tornado chart item model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parameter** | **str** | Parameter name | 
**low_value** | **float** | Low parameter value | 
**high_value** | **float** | High parameter value | 
**low_metric** | **float** | Metric value at low parameter value | 
**high_metric** | **float** | Metric value at high parameter value | 
**base_metric** | **float** | Metric value at base parameter value | 
**metric_name** | **str** | Metric name | 

## Example

```python
from equihome_sim_sdk.models.tornado_chart_item import TornadoChartItem

# TODO update the JSON string below
json = "{}"
# create an instance of TornadoChartItem from a JSON string
tornado_chart_item_instance = TornadoChartItem.from_json(json)
# print the JSON string representation of the object
print(TornadoChartItem.to_json())

# convert the object into a dict
tornado_chart_item_dict = tornado_chart_item_instance.to_dict()
# create an instance of TornadoChartItem from a dict
tornado_chart_item_from_dict = TornadoChartItem.from_dict(tornado_chart_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


