# CoverageTestResponse

Coverage test response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**test_type** | **str** | Test type (e.g., &#39;overcollateralization&#39;, &#39;interest_coverage&#39;) | 
**test_date** | **str** | Date of the test | 
**year** | **float** | Year of the test | 
**month** | **int** | Month of the test | 
**threshold** | **float** | Test threshold | 
**actual_value** | **float** | Actual value | 
**passed** | **bool** | Whether the test passed | 
**cure_deadline** | **str** | Deadline to cure the test failure (if applicable) | [optional] 
**cured** | **bool** | Whether the test failure was cured (if applicable) | [optional] 

## Example

```python
from equihome_sim_sdk.models.coverage_test_response import CoverageTestResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CoverageTestResponse from a JSON string
coverage_test_response_instance = CoverageTestResponse.from_json(json)
# print the JSON string representation of the object
print(CoverageTestResponse.to_json())

# convert the object into a dict
coverage_test_response_dict = coverage_test_response_instance.to_dict()
# create an instance of CoverageTestResponse from a dict
coverage_test_response_from_dict = CoverageTestResponse.from_dict(coverage_test_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


