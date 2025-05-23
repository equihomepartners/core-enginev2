# Loan

Loan model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**loan_id** | **str** | Loan ID | 
**loan_size** | **float** | Loan size | 
**ltv** | **float** | Loan-to-value ratio | 
**zone** | **str** | Zone category | 
**term** | **float** | Loan term in years | 
**interest_rate** | **float** | Interest rate | 
**origination_year** | **int** | Origination year | 
**property_value** | **float** | Property value | 
**property_id** | **str** | Property ID | 
**suburb_id** | **str** | Suburb ID | 
**suburb_name** | **str** | Suburb name | 
**property_type** | **str** | Property type | [optional] 
**bedrooms** | **int** | Number of bedrooms | [optional] 
**bathrooms** | **int** | Number of bathrooms | [optional] 
**land_size** | **float** | Land size | [optional] 
**building_size** | **float** | Building size | [optional] 
**year_built** | **int** | Year built | [optional] 

## Example

```python
from equihome_sim_sdk.models.loan import Loan

# TODO update the JSON string below
json = "{}"
# create an instance of Loan from a JSON string
loan_instance = Loan.from_json(json)
# print the JSON string representation of the object
print(Loan.to_json())

# convert the object into a dict
loan_dict = loan_instance.to_dict()
# create an instance of Loan from a dict
loan_from_dict = Loan.from_dict(loan_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


