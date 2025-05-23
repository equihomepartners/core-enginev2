# DrawdownPoint

Drawdown chart point model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** | Year | 
**month** | **int** | Month | 
**drawdown** | **float** | Drawdown percentage | 

## Example

```python
from equihome_sim_sdk.models.drawdown_point import DrawdownPoint

# TODO update the JSON string below
json = "{}"
# create an instance of DrawdownPoint from a JSON string
drawdown_point_instance = DrawdownPoint.from_json(json)
# print the JSON string representation of the object
print(DrawdownPoint.to_json())

# convert the object into a dict
drawdown_point_dict = drawdown_point_instance.to_dict()
# create an instance of DrawdownPoint from a dict
drawdown_point_from_dict = DrawdownPoint.from_dict(drawdown_point_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


