# CashflowVisualization

Cashflow visualization model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cashflow_waterfall_chart** | [**List[CashflowWaterfallItem]**](CashflowWaterfallItem.md) | Cashflow waterfall chart data | 
**cashflow_by_year_chart** | [**List[CashflowByYearItem]**](CashflowByYearItem.md) | Cashflow by year chart data | 
**cumulative_cashflow_chart** | [**List[CumulativeCashflowItem]**](CumulativeCashflowItem.md) | Cumulative cashflow chart data | 
**cashflow_table** | [**List[CashflowTableItem]**](CashflowTableItem.md) | Cashflow table data | 
**cashflow_heatmap** | [**List[CashflowHeatmapItem]**](CashflowHeatmapItem.md) | Cashflow heatmap data | [optional] 
**cashflow_sankey** | [**CashflowSankey**](CashflowSankey.md) | Cashflow Sankey diagram data | [optional] 
**scenario_comparison_chart** | [**List[ScenarioComparisonItem]**](ScenarioComparisonItem.md) | Scenario comparison chart data | [optional] 

## Example

```python
from equihome_sim_sdk.models.cashflow_visualization import CashflowVisualization

# TODO update the JSON string below
json = "{}"
# create an instance of CashflowVisualization from a JSON string
cashflow_visualization_instance = CashflowVisualization.from_json(json)
# print the JSON string representation of the object
print(CashflowVisualization.to_json())

# convert the object into a dict
cashflow_visualization_dict = cashflow_visualization_instance.to_dict()
# create an instance of CashflowVisualization from a dict
cashflow_visualization_from_dict = CashflowVisualization.from_dict(cashflow_visualization_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


