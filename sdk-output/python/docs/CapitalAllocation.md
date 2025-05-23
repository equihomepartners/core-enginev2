# CapitalAllocation

Capital allocation model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**zone_targets** | **Dict[str, float]** | Target zone allocations | 
**zone_actual** | **Dict[str, float]** | Actual zone allocations | 
**capital_by_zone** | **Dict[str, float]** | Capital allocated by zone | [optional] 
**allocation_stats** | **object** | Allocation statistics | [optional] 
**visualization** | **object** | Visualization data | [optional] 

## Example

```python
from equihome_sim_sdk.models.capital_allocation import CapitalAllocation

# TODO update the JSON string below
json = "{}"
# create an instance of CapitalAllocation from a JSON string
capital_allocation_instance = CapitalAllocation.from_json(json)
# print the JSON string representation of the object
print(CapitalAllocation.to_json())

# convert the object into a dict
capital_allocation_dict = capital_allocation_instance.to_dict()
# create an instance of CapitalAllocation from a dict
capital_allocation_from_dict = CapitalAllocation.from_dict(capital_allocation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


