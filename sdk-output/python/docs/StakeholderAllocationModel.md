# StakeholderAllocationModel

Model for stakeholder allocation data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**stakeholder** | **str** | Stakeholder name | 
**amount** | **float** | Amount allocated | 
**percentage** | **float** | Percentage of total distribution | 

## Example

```python
from equihome_sim_sdk.models.stakeholder_allocation_model import StakeholderAllocationModel

# TODO update the JSON string below
json = "{}"
# create an instance of StakeholderAllocationModel from a JSON string
stakeholder_allocation_model_instance = StakeholderAllocationModel.from_json(json)
# print the JSON string representation of the object
print(StakeholderAllocationModel.to_json())

# convert the object into a dict
stakeholder_allocation_model_dict = stakeholder_allocation_model_instance.to_dict()
# create an instance of StakeholderAllocationModel from a dict
stakeholder_allocation_model_from_dict = StakeholderAllocationModel.from_dict(stakeholder_allocation_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


