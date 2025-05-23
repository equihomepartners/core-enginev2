# equihome_sim_sdk.SimulationApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_simulation_simulations_post**](SimulationApi.md#create_simulation_simulations_post) | **POST** /simulations/ | Create Simulation
[**delete_simulation_simulations_simulation_id_delete**](SimulationApi.md#delete_simulation_simulations_simulation_id_delete) | **DELETE** /simulations/{simulation_id} | Delete Simulation
[**get_simulation_simulations_simulation_id_get**](SimulationApi.md#get_simulation_simulations_simulation_id_get) | **GET** /simulations/{simulation_id} | Get Simulation
[**list_simulations_simulations_get**](SimulationApi.md#list_simulations_simulations_get) | **GET** /simulations/ | List Simulations


# **create_simulation_simulations_post**
> SimulationResponse create_simulation_simulations_post(simulation_request)

Create Simulation

Create a new simulation.

Args:
    request: Simulation request
    background_tasks: Background tasks

Returns:
    Simulation response

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.simulation_request import SimulationRequest
from equihome_sim_sdk.models.simulation_response import SimulationResponse
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
    api_instance = equihome_sim_sdk.SimulationApi(api_client)
    simulation_request = equihome_sim_sdk.SimulationRequest() # SimulationRequest | 

    try:
        # Create Simulation
        api_response = api_instance.create_simulation_simulations_post(simulation_request)
        print("The response of SimulationApi->create_simulation_simulations_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SimulationApi->create_simulation_simulations_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_request** | [**SimulationRequest**](SimulationRequest.md)|  | 

### Return type

[**SimulationResponse**](SimulationResponse.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_simulation_simulations_simulation_id_delete**
> Dict[str, str] delete_simulation_simulations_simulation_id_delete(simulation_id)

Delete Simulation

Delete a simulation by ID.

Args:
    simulation_id: Simulation ID

Returns:
    Success message

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
    api_instance = equihome_sim_sdk.SimulationApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Delete Simulation
        api_response = api_instance.delete_simulation_simulations_simulation_id_delete(simulation_id)
        print("The response of SimulationApi->delete_simulation_simulations_simulation_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SimulationApi->delete_simulation_simulations_simulation_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

**Dict[str, str]**

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_simulation_simulations_simulation_id_get**
> SimulationResult get_simulation_simulations_simulation_id_get(simulation_id)

Get Simulation

Get a simulation by ID.

Args:
    simulation_id: Simulation ID

Returns:
    Simulation result

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.simulation_result import SimulationResult
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
    api_instance = equihome_sim_sdk.SimulationApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Simulation
        api_response = api_instance.get_simulation_simulations_simulation_id_get(simulation_id)
        print("The response of SimulationApi->get_simulation_simulations_simulation_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SimulationApi->get_simulation_simulations_simulation_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**SimulationResult**](SimulationResult.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_simulations_simulations_get**
> List[SimulationResult] list_simulations_simulations_get()

List Simulations

List all simulations.

Returns:
    List of simulation results

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.simulation_result import SimulationResult
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
    api_instance = equihome_sim_sdk.SimulationApi(api_client)

    try:
        # List Simulations
        api_response = api_instance.list_simulations_simulations_get()
        print("The response of SimulationApi->list_simulations_simulations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SimulationApi->list_simulations_simulations_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[SimulationResult]**](SimulationResult.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

