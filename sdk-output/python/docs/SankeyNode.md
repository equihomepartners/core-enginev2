# SankeyNode

Sankey diagram node model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Node ID | 
**name** | **str** | Node name | 

## Example

```python
from equihome_sim_sdk.models.sankey_node import SankeyNode

# TODO update the JSON string below
json = "{}"
# create an instance of SankeyNode from a JSON string
sankey_node_instance = SankeyNode.from_json(json)
# print the JSON string representation of the object
print(SankeyNode.to_json())

# convert the object into a dict
sankey_node_dict = sankey_node_instance.to_dict()
# create an instance of SankeyNode from a dict
sankey_node_from_dict = SankeyNode.from_dict(sankey_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


