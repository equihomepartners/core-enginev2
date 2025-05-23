# equihome_sim_sdk.ReinvestmentApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_reinvestment_data_api_v1_simulations_simulation_id_reinvestment_get**](ReinvestmentApi.md#get_reinvestment_data_api_v1_simulations_simulation_id_reinvestment_get) | **GET** /api/v1/simulations/{simulation_id}/reinvestment | Get Reinvestment Data
[**get_reinvestment_risk_metrics_api_v1_simulations_simulation_id_reinvestment_risk_get**](ReinvestmentApi.md#get_reinvestment_risk_metrics_api_v1_simulations_simulation_id_reinvestment_risk_get) | **GET** /api/v1/simulations/{simulation_id}/reinvestment/risk | Get Reinvestment Risk Metrics
[**manual_reinvestment_api_v1_simulations_simulation_id_reinvestment_post**](ReinvestmentApi.md#manual_reinvestment_api_v1_simulations_simulation_id_reinvestment_post) | **POST** /api/v1/simulations/{simulation_id}/reinvestment | Manual Reinvestment


# **get_reinvestment_data_api_v1_simulations_simulation_id_reinvestment_get**
> SrcApiRoutersReinvestmentReinvestmentResponse get_reinvestment_data_api_v1_simulations_simulation_id_reinvestment_get(simulation_id)

Get Reinvestment Data

Get reinvestment data for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    Reinvestment data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.src_api_routers_reinvestment_reinvestment_response import SrcApiRoutersReinvestmentReinvestmentResponse
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
    api_instance = equihome_sim_sdk.ReinvestmentApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Reinvestment Data
        api_response = api_instance.get_reinvestment_data_api_v1_simulations_simulation_id_reinvestment_get(simulation_id)
        print("The response of ReinvestmentApi->get_reinvestment_data_api_v1_simulations_simulation_id_reinvestment_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReinvestmentApi->get_reinvestment_data_api_v1_simulations_simulation_id_reinvestment_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**SrcApiRoutersReinvestmentReinvestmentResponse**](SrcApiRoutersReinvestmentReinvestmentResponse.md)

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

# **get_reinvestment_risk_metrics_api_v1_simulations_simulation_id_reinvestment_risk_get**
> List[object] get_reinvestment_risk_metrics_api_v1_simulations_simulation_id_reinvestment_risk_get(simulation_id)

Get Reinvestment Risk Metrics

Get reinvestment risk metrics for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    List of risk metrics for each reinvestment event

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
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
    api_instance = equihome_sim_sdk.ReinvestmentApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Reinvestment Risk Metrics
        api_response = api_instance.get_reinvestment_risk_metrics_api_v1_simulations_simulation_id_reinvestment_risk_get(simulation_id)
        print("The response of ReinvestmentApi->get_reinvestment_risk_metrics_api_v1_simulations_simulation_id_reinvestment_risk_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReinvestmentApi->get_reinvestment_risk_metrics_api_v1_simulations_simulation_id_reinvestment_risk_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

**List[object]**

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

# **manual_reinvestment_api_v1_simulations_simulation_id_reinvestment_post**
> ReinvestmentEventResponse manual_reinvestment_api_v1_simulations_simulation_id_reinvestment_post(simulation_id, manual_reinvestment_request)

Manual Reinvestment

Manually trigger a reinvestment event.

Args:
    simulation_id: Simulation ID
    request: Manual reinvestment request

Returns:
    Reinvestment event details

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.manual_reinvestment_request import ManualReinvestmentRequest
from equihome_sim_sdk.models.reinvestment_event_response import ReinvestmentEventResponse
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
    api_instance = equihome_sim_sdk.ReinvestmentApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    manual_reinvestment_request = equihome_sim_sdk.ManualReinvestmentRequest() # ManualReinvestmentRequest | 

    try:
        # Manual Reinvestment
        api_response = api_instance.manual_reinvestment_api_v1_simulations_simulation_id_reinvestment_post(simulation_id, manual_reinvestment_request)
        print("The response of ReinvestmentApi->manual_reinvestment_api_v1_simulations_simulation_id_reinvestment_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReinvestmentApi->manual_reinvestment_api_v1_simulations_simulation_id_reinvestment_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **manual_reinvestment_request** | [**ManualReinvestmentRequest**](ManualReinvestmentRequest.md)|  | 

### Return type

[**ReinvestmentEventResponse**](ReinvestmentEventResponse.md)

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

