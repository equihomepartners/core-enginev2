# equihome_sim_sdk.PerformanceApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generate_report_performance_generate_post**](PerformanceApi.md#generate_report_performance_generate_post) | **POST** /performance/generate | Generate performance report
[**get_report_performance_simulation_id_get**](PerformanceApi.md#get_report_performance_simulation_id_get) | **GET** /performance/{simulation_id} | Get performance report
[**get_report_summary_performance_simulation_id_summary_get**](PerformanceApi.md#get_report_summary_performance_simulation_id_summary_get) | **GET** /performance/{simulation_id}/summary | Get performance report summary


# **generate_report_performance_generate_post**
> object generate_report_performance_generate_post(performance_report_request, simulation_id=simulation_id)

Generate performance report

Generates a comprehensive performance report for the simulation

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.performance_report_request import PerformanceReportRequest
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
    api_instance = equihome_sim_sdk.PerformanceApi(api_client)
    performance_report_request = equihome_sim_sdk.PerformanceReportRequest() # PerformanceReportRequest | 
    simulation_id = 'simulation_id_example' # str |  (optional)

    try:
        # Generate performance report
        api_response = api_instance.generate_report_performance_generate_post(performance_report_request, simulation_id=simulation_id)
        print("The response of PerformanceApi->generate_report_performance_generate_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PerformanceApi->generate_report_performance_generate_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **performance_report_request** | [**PerformanceReportRequest**](PerformanceReportRequest.md)|  | 
 **simulation_id** | **str**|  | [optional] 

### Return type

**object**

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

# **get_report_performance_simulation_id_get**
> object get_report_performance_simulation_id_get(simulation_id)

Get performance report

Returns the performance report for the simulation

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
    api_instance = equihome_sim_sdk.PerformanceApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get performance report
        api_response = api_instance.get_report_performance_simulation_id_get(simulation_id)
        print("The response of PerformanceApi->get_report_performance_simulation_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PerformanceApi->get_report_performance_simulation_id_get: %s\n" % e)
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
**404** | Not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_report_summary_performance_simulation_id_summary_get**
> PerformanceReportSummary get_report_summary_performance_simulation_id_summary_get(simulation_id)

Get performance report summary

Returns the summary of the performance report for the simulation

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.performance_report_summary import PerformanceReportSummary
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
    api_instance = equihome_sim_sdk.PerformanceApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get performance report summary
        api_response = api_instance.get_report_summary_performance_simulation_id_summary_get(simulation_id)
        print("The response of PerformanceApi->get_report_summary_performance_simulation_id_summary_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PerformanceApi->get_report_summary_performance_simulation_id_summary_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**PerformanceReportSummary**](PerformanceReportSummary.md)

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

