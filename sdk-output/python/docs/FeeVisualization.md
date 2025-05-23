# FeeVisualization

Fee visualization model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fee_breakdown_chart** | [**List[FeeBreakdownItem]**](FeeBreakdownItem.md) | Fee breakdown chart data | 
**fees_by_year_chart** | [**List[FeesByYearItem]**](FeesByYearItem.md) | Fees by year chart data | 
**fee_impact_chart** | [**List[FeeImpactItem]**](FeeImpactItem.md) | Fee impact chart data | 
**fee_table** | [**List[FeesByYearItem]**](FeesByYearItem.md) | Fee table data | 

## Example

```python
from equihome_sim_sdk.models.fee_visualization import FeeVisualization

# TODO update the JSON string below
json = "{}"
# create an instance of FeeVisualization from a JSON string
fee_visualization_instance = FeeVisualization.from_json(json)
# print the JSON string representation of the object
print(FeeVisualization.to_json())

# convert the object into a dict
fee_visualization_dict = fee_visualization_instance.to_dict()
# create an instance of FeeVisualization from a dict
fee_visualization_from_dict = FeeVisualization.from_dict(fee_visualization_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


