# FeesByYearItem

Fees by year item model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** | Year | 
**management_fees** | **float** | Management fees | 
**origination_fees** | **float** | Origination fees | 
**fund_expenses** | **float** | Fund expenses | 
**acquisition_fees** | **float** | Acquisition fees | 
**disposition_fees** | **float** | Disposition fees | 
**setup_costs** | **float** | Setup costs | 
**total** | **float** | Total fees | 

## Example

```python
from equihome_sim_sdk.models.fees_by_year_item import FeesByYearItem

# TODO update the JSON string below
json = "{}"
# create an instance of FeesByYearItem from a JSON string
fees_by_year_item_instance = FeesByYearItem.from_json(json)
# print the JSON string representation of the object
print(FeesByYearItem.to_json())

# convert the object into a dict
fees_by_year_item_dict = fees_by_year_item_instance.to_dict()
# create an instance of FeesByYearItem from a dict
fees_by_year_item_from_dict = FeesByYearItem.from_dict(fees_by_year_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


