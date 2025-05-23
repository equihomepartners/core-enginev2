# CashflowSankey

Cashflow Sankey diagram model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**nodes** | [**List[SankeyNode]**](SankeyNode.md) | Nodes in the Sankey diagram | 
**links** | [**List[SankeyLink]**](SankeyLink.md) | Links in the Sankey diagram | 

## Example

```python
from equihome_sim_sdk.models.cashflow_sankey import CashflowSankey

# TODO update the JSON string below
json = "{}"
# create an instance of CashflowSankey from a JSON string
cashflow_sankey_instance = CashflowSankey.from_json(json)
# print the JSON string representation of the object
print(CashflowSankey.to_json())

# convert the object into a dict
cashflow_sankey_dict = cashflow_sankey_instance.to_dict()
# create an instance of CashflowSankey from a dict
cashflow_sankey_from_dict = CashflowSankey.from_dict(cashflow_sankey_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


