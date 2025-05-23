# ReinvestmentEfficiencyResponse

Reinvestment efficiency response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**reinvestment_ratio** | **float** | Ratio of reinvested capital to total exit value | 
**avg_time_to_reinvest** | **float** | Average time between exit and reinvestment in months | 
**reinvestment_portfolio_impact** | **float** | Percentage of portfolio from reinvestment | 

## Example

```python
from equihome_sim_sdk.models.reinvestment_efficiency_response import ReinvestmentEfficiencyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReinvestmentEfficiencyResponse from a JSON string
reinvestment_efficiency_response_instance = ReinvestmentEfficiencyResponse.from_json(json)
# print the JSON string representation of the object
print(ReinvestmentEfficiencyResponse.to_json())

# convert the object into a dict
reinvestment_efficiency_response_dict = reinvestment_efficiency_response_instance.to_dict()
# create an instance of ReinvestmentEfficiencyResponse from a dict
reinvestment_efficiency_response_from_dict = ReinvestmentEfficiencyResponse.from_dict(reinvestment_efficiency_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


