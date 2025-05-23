# ReinvestmentTablesResponse

Reinvestment tables response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reinvestment_summary_table** | **List[object]** | Reinvestment summary table | 
**reinvestment_events_table** | **List[object]** | Reinvestment events table | 
**reinvestment_loans_table** | **List[object]** | Reinvestment loans table | 
**cash_reserve_metrics_table** | **List[object]** | Cash reserve metrics table | 

## Example

```python
from equihome_sim_sdk.models.reinvestment_tables_response import ReinvestmentTablesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReinvestmentTablesResponse from a JSON string
reinvestment_tables_response_instance = ReinvestmentTablesResponse.from_json(json)
# print the JSON string representation of the object
print(ReinvestmentTablesResponse.to_json())

# convert the object into a dict
reinvestment_tables_response_dict = reinvestment_tables_response_instance.to_dict()
# create an instance of ReinvestmentTablesResponse from a dict
reinvestment_tables_response_from_dict = ReinvestmentTablesResponse.from_dict(reinvestment_tables_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


