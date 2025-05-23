# equihome_sim_sdk.PersistenceApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_result_api_v1_results_simulation_id_delete**](PersistenceApi.md#delete_result_api_v1_results_simulation_id_delete) | **DELETE** /api/v1/results/{simulation_id} | Delete Result
[**export_result_api_v1_results_simulation_id_export_post**](PersistenceApi.md#export_result_api_v1_results_simulation_id_export_post) | **POST** /api/v1/results/{simulation_id}/export | Export Result
[**get_result_api_v1_results_simulation_id_get**](PersistenceApi.md#get_result_api_v1_results_simulation_id_get) | **GET** /api/v1/results/{simulation_id} | Get Result
[**list_results_api_v1_results_get**](PersistenceApi.md#list_results_api_v1_results_get) | **GET** /api/v1/results/ | List Results


# **delete_result_api_v1_results_simulation_id_delete**
> object delete_result_api_v1_results_simulation_id_delete(simulation_id)

Delete Result

Delete a simulation result.

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
    api_instance = equihome_sim_sdk.PersistenceApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Delete Result
        api_response = api_instance.delete_result_api_v1_results_simulation_id_delete(simulation_id)
        print("The response of PersistenceApi->delete_result_api_v1_results_simulation_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersistenceApi->delete_result_api_v1_results_simulation_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

**object**

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

# **export_result_api_v1_results_simulation_id_export_post**
> object export_result_api_v1_results_simulation_id_export_post(simulation_id)

Export Result

Export a simulation result to a file.

Args:
    simulation_id: Simulation ID
    background_tasks: Background tasks

Returns:
    Export status

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
    api_instance = equihome_sim_sdk.PersistenceApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Export Result
        api_response = api_instance.export_result_api_v1_results_simulation_id_export_post(simulation_id)
        print("The response of PersistenceApi->export_result_api_v1_results_simulation_id_export_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersistenceApi->export_result_api_v1_results_simulation_id_export_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

**object**

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

# **get_result_api_v1_results_simulation_id_get**
> ResultResponse get_result_api_v1_results_simulation_id_get(simulation_id)

Get Result

Get a simulation result by ID.

Args:
    simulation_id: Simulation ID

Returns:
    Simulation result

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.result_response import ResultResponse
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
    api_instance = equihome_sim_sdk.PersistenceApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Result
        api_response = api_instance.get_result_api_v1_results_simulation_id_get(simulation_id)
        print("The response of PersistenceApi->get_result_api_v1_results_simulation_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersistenceApi->get_result_api_v1_results_simulation_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**ResultResponse**](ResultResponse.md)

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

# **list_results_api_v1_results_get**
> ResultListResponse list_results_api_v1_results_get(limit=limit, offset=offset)

List Results

List simulation results.

Args:
    limit: Maximum number of results to return
    offset: Offset for pagination

Returns:
    List of simulation results

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.result_list_response import ResultListResponse
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
    api_instance = equihome_sim_sdk.PersistenceApi(api_client)
    limit = 100 # int |  (optional) (default to 100)
    offset = 0 # int |  (optional) (default to 0)

    try:
        # List Results
        api_response = api_instance.list_results_api_v1_results_get(limit=limit, offset=offset)
        print("The response of PersistenceApi->list_results_api_v1_results_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PersistenceApi->list_results_api_v1_results_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**|  | [optional] [default to 100]
 **offset** | **int**|  | [optional] [default to 0]

### Return type

[**ResultListResponse**](ResultListResponse.md)

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

