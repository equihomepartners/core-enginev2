# EnhancedExitStatisticsResponse

Enhanced exit statistics response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**avg_exit_year** | **float** | Average exit year | 
**avg_roi** | **float** | Average ROI | 
**avg_annualized_roi** | **float** | Average annualized ROI | 
**exit_type_distribution** | **Dict[str, float]** | Exit type distribution | 
**exit_timing_distribution** | **Dict[str, int]** | Exit timing distribution | 
**exit_roi_distribution** | **Dict[str, int]** | Exit ROI distribution | 
**exit_type_roi** | **Dict[str, object]** | Exit type ROI | 
**exit_value_total** | **float** | Total exit value | 
**appreciation_share_total** | **float** | Total appreciation share | 
**total_return** | **float** | Total return | 
**total_roi** | **float** | Total ROI | 
**annualized_roi** | **float** | Annualized ROI | 
**comparison_to_base** | **object** | Comparison to base exit statistics | [optional] 
**cohort_analysis** | **object** | Cohort analysis | [optional] 
**cohort_analysis_summary** | **object** | Cohort analysis summary | [optional] 
**risk_metrics** | **object** | Risk metrics | [optional] 
**ml_insights** | **object** | Machine learning insights | [optional] 

## Example

```python
from equihome_sim_sdk.models.enhanced_exit_statistics_response import EnhancedExitStatisticsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of EnhancedExitStatisticsResponse from a JSON string
enhanced_exit_statistics_response_instance = EnhancedExitStatisticsResponse.from_json(json)
# print the JSON string representation of the object
print(EnhancedExitStatisticsResponse.to_json())

# convert the object into a dict
enhanced_exit_statistics_response_dict = enhanced_exit_statistics_response_instance.to_dict()
# create an instance of EnhancedExitStatisticsResponse from a dict
enhanced_exit_statistics_response_from_dict = EnhancedExitStatisticsResponse.from_dict(enhanced_exit_statistics_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


