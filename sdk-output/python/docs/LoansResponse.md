# LoansResponse

Loans response model.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**loans** | [**List[Loan]**](Loan.md) | List of loans | 
**total_count** | **int** | Total number of loans | 
**limit** | **int** | Maximum number of loans to return | 
**offset** | **int** | Offset for pagination | 

## Example

```python
from equihome_sim_sdk.models.loans_response import LoansResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LoansResponse from a JSON string
loans_response_instance = LoansResponse.from_json(json)
# print the JSON string representation of the object
print(LoansResponse.to_json())

# convert the object into a dict
loans_response_dict = loans_response_instance.to_dict()
# create an instance of LoansResponse from a dict
loans_response_from_dict = LoansResponse.from_dict(loans_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


