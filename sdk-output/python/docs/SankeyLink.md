# SankeyLink

Sankey diagram link model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **str** | Source node ID | 
**target** | **str** | Target node ID | 
**value** | **float** | Link value | 

## Example

```python
from equihome_sim_sdk.models.sankey_link import SankeyLink

# TODO update the JSON string below
json = "{}"
# create an instance of SankeyLink from a JSON string
sankey_link_instance = SankeyLink.from_json(json)
# print the JSON string representation of the object
print(SankeyLink.to_json())

# convert the object into a dict
sankey_link_dict = sankey_link_instance.to_dict()
# create an instance of SankeyLink from a dict
sankey_link_from_dict = SankeyLink.from_dict(sankey_link_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


