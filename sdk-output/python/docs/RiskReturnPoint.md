# RiskReturnPoint

Risk-return scatter plot point model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scenario** | **str** | Scenario name | 
**risk** | **float** | Risk measure (e.g., volatility) | 
**var_return** | **float** | Return measure (e.g., IRR) | 

## Example

```python
from equihome_sim_sdk.models.risk_return_point import RiskReturnPoint

# TODO update the JSON string below
json = "{}"
# create an instance of RiskReturnPoint from a JSON string
risk_return_point_instance = RiskReturnPoint.from_json(json)
# print the JSON string representation of the object
print(RiskReturnPoint.to_json())

# convert the object into a dict
risk_return_point_dict = risk_return_point_instance.to_dict()
# create an instance of RiskReturnPoint from a dict
risk_return_point_from_dict = RiskReturnPoint.from_dict(risk_return_point_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


