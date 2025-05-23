# PricePathScenarioRequest

Price path scenario request model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_type** | **str** | Type of stochastic model to use | [optional] [default to 'gbm']
**appreciation_rates** | **Dict[str, float]** | Zone-specific appreciation rates | 
**volatility** | **Dict[str, float]** | Zone-specific volatility parameters | 
**correlation_matrix** | **Dict[str, float]** | Correlation matrix between zones | 
**time_step** | **str** | Time step for price path simulation | [optional] [default to 'monthly']
**fund_term** | **int** | Fund term in years | [optional] [default to 10]

## Example

```python
from equihome_sim_sdk.models.price_path_scenario_request import PricePathScenarioRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PricePathScenarioRequest from a JSON string
price_path_scenario_request_instance = PricePathScenarioRequest.from_json(json)
# print the JSON string representation of the object
print(PricePathScenarioRequest.to_json())

# convert the object into a dict
price_path_scenario_request_dict = price_path_scenario_request_instance.to_dict()
# create an instance of PricePathScenarioRequest from a dict
price_path_scenario_request_from_dict = PricePathScenarioRequest.from_dict(price_path_scenario_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


