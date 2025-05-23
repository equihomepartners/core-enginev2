# ExitScenarioRequest

Exit scenario request model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**base_exit_rate** | **float** | Base annual exit probability | [optional] [default to 0.1]
**time_factor** | **float** | Weight for time-based exit probability | [optional] [default to 0.4]
**price_factor** | **float** | Weight for price-based exit probability | [optional] [default to 0.6]
**min_hold_period** | **float** | Minimum holding period in years | [optional] [default to 1.0]
**max_hold_period** | **float** | Maximum holding period in years | [optional] [default to 10.0]
**sale_weight** | **float** | Base weight for sale exits | [optional] [default to 0.6]
**refinance_weight** | **float** | Base weight for refinance exits | [optional] [default to 0.3]
**default_weight** | **float** | Base weight for default exits | [optional] [default to 0.1]
**appreciation_sale_multiplier** | **float** | How much appreciation increases sale probability | [optional] [default to 2.0]
**interest_rate_refinance_multiplier** | **float** | How much interest rate changes affect refinance probability | [optional] [default to 3.0]
**economic_factor_default_multiplier** | **float** | How much economic factors affect default probability | [optional] [default to 2.0]
**appreciation_share** | **float** | Fund&#39;s share of appreciation | [optional] [default to 0.2]
**min_appreciation_share** | **float** | Minimum appreciation share | [optional] [default to 0.1]
**max_appreciation_share** | **float** | Maximum appreciation share | [optional] [default to 0.5]
**tiered_appreciation_thresholds** | **List[float]** | Thresholds for tiered appreciation sharing | [optional] [default to [0.2, 0.5, 1.0]]
**tiered_appreciation_shares** | **List[float]** | Shares for tiered appreciation sharing | [optional] [default to [0.1, 0.2, 0.3, 0.4]]
**base_default_rate** | **float** | Base annual default probability | [optional] [default to 0.01]
**recovery_rate** | **float** | Recovery rate in case of default | [optional] [default to 0.8]
**foreclosure_cost** | **float** | Cost of foreclosure as percentage of property value | [optional] [default to 0.1]
**foreclosure_time** | **float** | Time to complete foreclosure in years | [optional] [default to 1.0]

## Example

```python
from equihome_sim_sdk.models.exit_scenario_request import ExitScenarioRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExitScenarioRequest from a JSON string
exit_scenario_request_instance = ExitScenarioRequest.from_json(json)
# print the JSON string representation of the object
print(ExitScenarioRequest.to_json())

# convert the object into a dict
exit_scenario_request_dict = exit_scenario_request_instance.to_dict()
# create an instance of ExitScenarioRequest from a dict
exit_scenario_request_from_dict = ExitScenarioRequest.from_dict(exit_scenario_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


