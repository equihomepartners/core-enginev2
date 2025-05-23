# EnhancedExitScenarioRequest

Enhanced exit scenario request model.

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
**appreciation_share** | **float** | Fund&#39;s share of appreciation | [optional] [default to 0.2]
**refinance_interest_rate_sensitivity** | **float** | How sensitive refinancing is to interest rate changes | [optional] [default to 2.0]
**sale_appreciation_sensitivity** | **float** | How sensitive sales are to appreciation | [optional] [default to 1.5]
**life_event_probability** | **float** | Annual probability of life events triggering exits | [optional] [default to 0.05]
**behavioral_correlation** | **float** | Correlation in exit decisions (herd behavior) | [optional] [default to 0.3]
**recession_default_multiplier** | **float** | How much recessions increase defaults | [optional] [default to 2.5]
**inflation_refinance_multiplier** | **float** | How inflation affects refinancing | [optional] [default to 1.8]
**employment_sensitivity** | **float** | How employment affects exits | [optional] [default to 1.2]
**migration_sensitivity** | **float** | How population migration affects exits | [optional] [default to 0.8]
**regulatory_compliance_cost** | **float** | Compliance cost as percentage of loan | [optional] [default to 0.01]
**tax_efficiency_factor** | **float** | Tax efficiency factor (1.0 &#x3D; fully efficient) | [optional] [default to 0.9]
**vintage_segmentation** | **bool** | Whether to segment by vintage | [optional] [default to True]
**ltv_segmentation** | **bool** | Whether to segment by LTV | [optional] [default to True]
**zone_segmentation** | **bool** | Whether to segment by zone | [optional] [default to True]
**var_confidence_level** | **float** | Confidence level for Value-at-Risk | [optional] [default to 0.95]
**stress_test_severity** | **float** | Severity of stress tests (0-1) | [optional] [default to 0.3]
**tail_risk_threshold** | **float** | Threshold for tail risk events | [optional] [default to 0.05]
**use_ml_models** | **bool** | Whether to use machine learning models | [optional] [default to True]
**feature_importance_threshold** | **float** | Threshold for important features | [optional] [default to 0.05]
**anomaly_detection_threshold** | **float** | Standard deviations for anomaly detection | [optional] [default to 3.0]

## Example

```python
from equihome_sim_sdk.models.enhanced_exit_scenario_request import EnhancedExitScenarioRequest

# TODO update the JSON string below
json = "{}"
# create an instance of EnhancedExitScenarioRequest from a JSON string
enhanced_exit_scenario_request_instance = EnhancedExitScenarioRequest.from_json(json)
# print the JSON string representation of the object
print(EnhancedExitScenarioRequest.to_json())

# convert the object into a dict
enhanced_exit_scenario_request_dict = enhanced_exit_scenario_request_instance.to_dict()
# create an instance of EnhancedExitScenarioRequest from a dict
enhanced_exit_scenario_request_from_dict = EnhancedExitScenarioRequest.from_dict(enhanced_exit_scenario_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


