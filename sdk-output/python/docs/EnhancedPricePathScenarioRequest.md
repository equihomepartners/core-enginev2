# EnhancedPricePathScenarioRequest

Enhanced price path scenario request model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_type** | **str** | Type of stochastic model to use (gbm, mean_reversion, regime_switching, sydney_cycle) | [optional] [default to 'sydney_cycle']
**appreciation_rates** | **Dict[str, float]** | Zone-specific appreciation rates | 
**volatility** | **Dict[str, float]** | Zone-specific volatility parameters | 
**correlation_matrix** | **Dict[str, float]** | Correlation matrix between zones | 
**time_step** | **str** | Time step for price path simulation | [optional] [default to 'monthly']
**fund_term** | **int** | Fund term in years | [optional] [default to 10]
**cycle_position** | **float** | Initial position in the property cycle (0-1) | [optional] [default to 0.5]
**suburb_variation** | **float** | Variation between suburbs within the same zone | [optional] [default to 0.02]
**property_variation** | **float** | Variation between properties within the same suburb | [optional] [default to 0.01]
**mean_reversion_params** | **Dict[str, float]** | Parameters for mean-reverting model | [optional] 
**regime_switching_params** | **Dict[str, float]** | Parameters for regime-switching model | [optional] 

## Example

```python
from equihome_sim_sdk.models.enhanced_price_path_scenario_request import EnhancedPricePathScenarioRequest

# TODO update the JSON string below
json = "{}"
# create an instance of EnhancedPricePathScenarioRequest from a JSON string
enhanced_price_path_scenario_request_instance = EnhancedPricePathScenarioRequest.from_json(json)
# print the JSON string representation of the object
print(EnhancedPricePathScenarioRequest.to_json())

# convert the object into a dict
enhanced_price_path_scenario_request_dict = enhanced_price_path_scenario_request_instance.to_dict()
# create an instance of EnhancedPricePathScenarioRequest from a dict
enhanced_price_path_scenario_request_from_dict = EnhancedPricePathScenarioRequest.from_dict(enhanced_price_path_scenario_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


