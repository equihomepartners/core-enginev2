# CorrelationMatrix

Correlation matrix model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metrics** | **List[str]** | Metric names | 
**matrix** | **List[List[float]]** | Correlation matrix | 
**strong_correlations** | **List[object]** | Strong correlations | 

## Example

```python
from equihome_sim_sdk.models.correlation_matrix import CorrelationMatrix

# TODO update the JSON string below
json = "{}"
# create an instance of CorrelationMatrix from a JSON string
correlation_matrix_instance = CorrelationMatrix.from_json(json)
# print the JSON string representation of the object
print(CorrelationMatrix.to_json())

# convert the object into a dict
correlation_matrix_dict = correlation_matrix_instance.to_dict()
# create an instance of CorrelationMatrix from a dict
correlation_matrix_from_dict = CorrelationMatrix.from_dict(correlation_matrix_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


