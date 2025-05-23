# TrancheResponse

Tranche response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Tranche name | 
**type** | **str** | Tranche type | 
**size** | **float** | Tranche size in dollars | 
**priority** | **int** | Payment priority | 
**interest_rate** | **float** | Interest rate for debt tranches | [optional] 
**target_return** | **float** | Target return for the tranche | [optional] 
**actual_return** | **float** | Actual return achieved | [optional] 
**irr** | **float** | Internal rate of return | [optional] 
**moic** | **float** | Multiple on invested capital | [optional] 
**total_payments** | **float** | Total payments made to the tranche | 
**principal_payments** | **float** | Principal payments made to the tranche | 
**interest_payments** | **float** | Interest payments made to the tranche | 
**profit_share_payments** | **float** | Profit share payments made to the tranche | 
**shortfall** | **float** | Shortfall amount (if any) | 
**status** | **str** | Tranche status (e.g., &#39;paid&#39;, &#39;defaulted&#39;, &#39;active&#39;) | 

## Example

```python
from equihome_sim_sdk.models.tranche_response import TrancheResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TrancheResponse from a JSON string
tranche_response_instance = TrancheResponse.from_json(json)
# print the JSON string representation of the object
print(TrancheResponse.to_json())

# convert the object into a dict
tranche_response_dict = tranche_response_instance.to_dict()
# create an instance of TrancheResponse from a dict
tranche_response_from_dict = TrancheResponse.from_dict(tranche_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


