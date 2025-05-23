# LeverageResponse

Leverage response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**facilities** | [**List[LeverageFacility]**](LeverageFacility.md) | Debt facilities | 
**metrics** | [**SrcApiRoutersPortfolioLeverageMetrics**](SrcApiRoutersPortfolioLeverageMetrics.md) | Leverage metrics | 
**visualization** | [**LeverageVisualization**](LeverageVisualization.md) | Visualization data | 
**stress_test_results** | [**Dict[str, SrcApiRoutersPortfolioStressTestResult]**](SrcApiRoutersPortfolioStressTestResult.md) | Stress test results | [optional] 

## Example

```python
from equihome_sim_sdk.models.leverage_response import LeverageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LeverageResponse from a JSON string
leverage_response_instance = LeverageResponse.from_json(json)
# print the JSON string representation of the object
print(LeverageResponse.to_json())

# convert the object into a dict
leverage_response_dict = leverage_response_instance.to_dict()
# create an instance of LeverageResponse from a dict
leverage_response_from_dict = LeverageResponse.from_dict(leverage_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


