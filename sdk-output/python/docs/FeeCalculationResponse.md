# FeeCalculationResponse

Response model for fee calculation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simulation_id** | **str** | Simulation ID | 
**total_fees** | **Dict[str, float]** | Total fees by category | 
**fee_impact** | **Dict[str, float]** | Impact of fees on fund performance | 
**visualization** | [**FeeVisualization**](FeeVisualization.md) | Visualization data | 

## Example

```python
from equihome_sim_sdk.models.fee_calculation_response import FeeCalculationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FeeCalculationResponse from a JSON string
fee_calculation_response_instance = FeeCalculationResponse.from_json(json)
# print the JSON string representation of the object
print(FeeCalculationResponse.to_json())

# convert the object into a dict
fee_calculation_response_dict = fee_calculation_response_instance.to_dict()
# create an instance of FeeCalculationResponse from a dict
fee_calculation_response_from_dict = FeeCalculationResponse.from_dict(fee_calculation_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


