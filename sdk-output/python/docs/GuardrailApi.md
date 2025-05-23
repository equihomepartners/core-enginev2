# equihome_sim_sdk.GuardrailApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**evaluate_guardrails_guardrail_evaluate_post**](GuardrailApi.md#evaluate_guardrails_guardrail_evaluate_post) | **POST** /guardrail/evaluate | Evaluate Guardrails
[**get_guardrail_report_guardrail_simulation_id_get**](GuardrailApi.md#get_guardrail_report_guardrail_simulation_id_get) | **GET** /guardrail/{simulation_id} | Get Guardrail Report


# **evaluate_guardrails_guardrail_evaluate_post**
> GuardrailReportModel evaluate_guardrails_guardrail_evaluate_post(guardrail_request, simulation_id=simulation_id)

Evaluate Guardrails

Evaluate guardrails for a simulation.

This endpoint evaluates guardrails for a simulation, checking that key risk metrics
stay within acceptable bounds. It is non-blocking, meaning that it reports violations
but does not stop the simulation.

The guardrails are organized into the following categories:

- **Property/Loan Level**: Stress LTV, loan size, exit month
- **Zone Level**: Zone NAV weight, default rate, price volatility
- **Portfolio Level**: Suburb concentration, loan concentration, NAV utilization,
  interest coverage, liquidity buffer, WAL, VaR, CVaR, IRR P5, hurdle-clear probability
- **Model/Process**: Schema version, Monte Carlo paths, seed reproducibility

Args:
    request: Guardrail evaluation request
    context: Simulation context

Returns:
    Guardrail report with breaches

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.guardrail_report_model import GuardrailReportModel
from equihome_sim_sdk.models.guardrail_request import GuardrailRequest
from equihome_sim_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = equihome_sim_sdk.Configuration(
    host = "http://localhost:8000"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with equihome_sim_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = equihome_sim_sdk.GuardrailApi(api_client)
    guardrail_request = equihome_sim_sdk.GuardrailRequest() # GuardrailRequest | 
    simulation_id = 'simulation_id_example' # str |  (optional)

    try:
        # Evaluate Guardrails
        api_response = api_instance.evaluate_guardrails_guardrail_evaluate_post(guardrail_request, simulation_id=simulation_id)
        print("The response of GuardrailApi->evaluate_guardrails_guardrail_evaluate_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GuardrailApi->evaluate_guardrails_guardrail_evaluate_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **guardrail_request** | [**GuardrailRequest**](GuardrailRequest.md)|  | 
 **simulation_id** | **str**|  | [optional] 

### Return type

[**GuardrailReportModel**](GuardrailReportModel.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_guardrail_report_guardrail_simulation_id_get**
> GuardrailReportModel get_guardrail_report_guardrail_simulation_id_get(simulation_id)

Get Guardrail Report

Get guardrail report for a simulation.

This endpoint retrieves the guardrail report for a simulation.

Args:
    simulation_id: Simulation ID
    context: Simulation context

Returns:
    Guardrail report with breaches

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.guardrail_report_model import GuardrailReportModel
from equihome_sim_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8000
# See configuration.py for a list of all supported configuration parameters.
configuration = equihome_sim_sdk.Configuration(
    host = "http://localhost:8000"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with equihome_sim_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = equihome_sim_sdk.GuardrailApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Guardrail Report
        api_response = api_instance.get_guardrail_report_guardrail_simulation_id_get(simulation_id)
        print("The response of GuardrailApi->get_guardrail_report_guardrail_simulation_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GuardrailApi->get_guardrail_report_guardrail_simulation_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**GuardrailReportModel**](GuardrailReportModel.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

