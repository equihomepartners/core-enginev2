# VarHistogram

VaR histogram model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bins** | **List[float]** | Histogram bins | 
**frequencies** | **List[int]** | Frequencies for each bin | 
**var_95** | **float** | VaR (95%) value | 
**var_99** | **float** | VaR (99%) value | 

## Example

```python
from equihome_sim_sdk.models.var_histogram import VarHistogram

# TODO update the JSON string below
json = "{}"
# create an instance of VarHistogram from a JSON string
var_histogram_instance = VarHistogram.from_json(json)
# print the JSON string representation of the object
print(VarHistogram.to_json())

# convert the object into a dict
var_histogram_dict = var_histogram_instance.to_dict()
# create an instance of VarHistogram from a dict
var_histogram_from_dict = VarHistogram.from_dict(var_histogram_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


