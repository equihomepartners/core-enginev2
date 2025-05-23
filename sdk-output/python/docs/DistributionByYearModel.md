# DistributionByYearModel

Model for distribution by year data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** | Distribution year | 
**lp_return_of_capital** | **float** | LP return of capital | 
**lp_preferred_return** | **float** | LP preferred return | 
**lp_residual** | **float** | LP residual distribution | 
**gp_catch_up** | **float** | GP catch-up | 
**gp_carried_interest** | **float** | GP carried interest | 
**total** | **float** | Total distribution | 

## Example

```python
from equihome_sim_sdk.models.distribution_by_year_model import DistributionByYearModel

# TODO update the JSON string below
json = "{}"
# create an instance of DistributionByYearModel from a JSON string
distribution_by_year_model_instance = DistributionByYearModel.from_json(json)
# print the JSON string representation of the object
print(DistributionByYearModel.to_json())

# convert the object into a dict
distribution_by_year_model_dict = distribution_by_year_model_instance.to_dict()
# create an instance of DistributionByYearModel from a dict
distribution_by_year_model_from_dict = DistributionByYearModel.from_dict(distribution_by_year_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


