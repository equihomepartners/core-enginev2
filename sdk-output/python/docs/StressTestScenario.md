# StressTestScenario

Stress test scenario model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Scenario name | 
**description** | **str** | Scenario description | [optional] 
**property_value_shock** | **float** | Property value shock as percentage (-1 to 1) | 
**interest_rate_shock** | **float** | Interest rate shock in percentage points (-0.1 to 0.1) | 
**default_rate_shock** | **float** | Default rate shock as multiplier (0-10) | 
**liquidity_shock** | **float** | Liquidity shock as percentage of expected liquidity (0-1) | 

## Example

```python
from equihome_sim_sdk.models.stress_test_scenario import StressTestScenario

# TODO update the JSON string below
json = "{}"
# create an instance of StressTestScenario from a JSON string
stress_test_scenario_instance = StressTestScenario.from_json(json)
# print the JSON string representation of the object
print(StressTestScenario.to_json())

# convert the object into a dict
stress_test_scenario_dict = stress_test_scenario_instance.to_dict()
# create an instance of StressTestScenario from a dict
stress_test_scenario_from_dict = StressTestScenario.from_dict(stress_test_scenario_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


