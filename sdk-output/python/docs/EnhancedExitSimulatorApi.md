# equihome_sim_sdk.EnhancedExitSimulatorApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_enhanced_exit_statistics_api_v1_simulations_simulation_id_enhanced_exits_statistics_get**](EnhancedExitSimulatorApi.md#get_enhanced_exit_statistics_api_v1_simulations_simulation_id_enhanced_exits_statistics_get) | **GET** /api/v1/simulations/{simulation_id}/enhanced-exits/statistics | Get Enhanced Exit Statistics
[**get_enhanced_exit_visualization_api_v1_simulations_simulation_id_enhanced_exits_visualization_get**](EnhancedExitSimulatorApi.md#get_enhanced_exit_visualization_api_v1_simulations_simulation_id_enhanced_exits_visualization_get) | **GET** /api/v1/simulations/{simulation_id}/enhanced-exits/visualization | Get Enhanced Exit Visualization
[**get_enhanced_exits_api_v1_simulations_simulation_id_enhanced_exits_get**](EnhancedExitSimulatorApi.md#get_enhanced_exits_api_v1_simulations_simulation_id_enhanced_exits_get) | **GET** /api/v1/simulations/{simulation_id}/enhanced-exits | Get Enhanced Exits
[**run_enhanced_exit_scenario_api_v1_simulations_simulation_id_enhanced_exits_scenario_post**](EnhancedExitSimulatorApi.md#run_enhanced_exit_scenario_api_v1_simulations_simulation_id_enhanced_exits_scenario_post) | **POST** /api/v1/simulations/{simulation_id}/enhanced-exits/scenario | Run Enhanced Exit Scenario


# **get_enhanced_exit_statistics_api_v1_simulations_simulation_id_enhanced_exits_statistics_get**
> EnhancedExitStatisticsResponse get_enhanced_exit_statistics_api_v1_simulations_simulation_id_enhanced_exits_statistics_get(simulation_id)

Get Enhanced Exit Statistics

Get enhanced statistics for exits.

Args:
    simulation_id: Simulation ID

Returns:
    Enhanced statistics data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.enhanced_exit_statistics_response import EnhancedExitStatisticsResponse
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
    api_instance = equihome_sim_sdk.EnhancedExitSimulatorApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Enhanced Exit Statistics
        api_response = api_instance.get_enhanced_exit_statistics_api_v1_simulations_simulation_id_enhanced_exits_statistics_get(simulation_id)
        print("The response of EnhancedExitSimulatorApi->get_enhanced_exit_statistics_api_v1_simulations_simulation_id_enhanced_exits_statistics_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EnhancedExitSimulatorApi->get_enhanced_exit_statistics_api_v1_simulations_simulation_id_enhanced_exits_statistics_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**EnhancedExitStatisticsResponse**](EnhancedExitStatisticsResponse.md)

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

# **get_enhanced_exit_visualization_api_v1_simulations_simulation_id_enhanced_exits_visualization_get**
> EnhancedExitVisualizationResponse get_enhanced_exit_visualization_api_v1_simulations_simulation_id_enhanced_exits_visualization_get(simulation_id)

Get Enhanced Exit Visualization

Get enhanced visualization data for exits.

Args:
    simulation_id: Simulation ID

Returns:
    Enhanced visualization data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.enhanced_exit_visualization_response import EnhancedExitVisualizationResponse
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
    api_instance = equihome_sim_sdk.EnhancedExitSimulatorApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Enhanced Exit Visualization
        api_response = api_instance.get_enhanced_exit_visualization_api_v1_simulations_simulation_id_enhanced_exits_visualization_get(simulation_id)
        print("The response of EnhancedExitSimulatorApi->get_enhanced_exit_visualization_api_v1_simulations_simulation_id_enhanced_exits_visualization_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EnhancedExitSimulatorApi->get_enhanced_exit_visualization_api_v1_simulations_simulation_id_enhanced_exits_visualization_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**EnhancedExitVisualizationResponse**](EnhancedExitVisualizationResponse.md)

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

# **get_enhanced_exits_api_v1_simulations_simulation_id_enhanced_exits_get**
> object get_enhanced_exits_api_v1_simulations_simulation_id_enhanced_exits_get(simulation_id)

Get Enhanced Exits

Get enhanced exit simulation results.

Args:
    simulation_id: Simulation ID

Returns:
    Enhanced exit simulation results

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
    api_instance = equihome_sim_sdk.EnhancedExitSimulatorApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Enhanced Exits
        api_response = api_instance.get_enhanced_exits_api_v1_simulations_simulation_id_enhanced_exits_get(simulation_id)
        print("The response of EnhancedExitSimulatorApi->get_enhanced_exits_api_v1_simulations_simulation_id_enhanced_exits_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EnhancedExitSimulatorApi->get_enhanced_exits_api_v1_simulations_simulation_id_enhanced_exits_get: %s\n" % e)
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

# **run_enhanced_exit_scenario_api_v1_simulations_simulation_id_enhanced_exits_scenario_post**
> object run_enhanced_exit_scenario_api_v1_simulations_simulation_id_enhanced_exits_scenario_post(simulation_id, enhanced_exit_scenario_request)

Run Enhanced Exit Scenario

Run an enhanced exit scenario with custom parameters.

Args:
    simulation_id: Simulation ID
    request: Enhanced exit scenario request

Returns:
    Enhanced exit scenario results

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.enhanced_exit_scenario_request import EnhancedExitScenarioRequest
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
    api_instance = equihome_sim_sdk.EnhancedExitSimulatorApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    enhanced_exit_scenario_request = equihome_sim_sdk.EnhancedExitScenarioRequest() # EnhancedExitScenarioRequest | 

    try:
        # Run Enhanced Exit Scenario
        api_response = api_instance.run_enhanced_exit_scenario_api_v1_simulations_simulation_id_enhanced_exits_scenario_post(simulation_id, enhanced_exit_scenario_request)
        print("The response of EnhancedExitSimulatorApi->run_enhanced_exit_scenario_api_v1_simulations_simulation_id_enhanced_exits_scenario_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EnhancedExitSimulatorApi->run_enhanced_exit_scenario_api_v1_simulations_simulation_id_enhanced_exits_scenario_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **enhanced_exit_scenario_request** | [**EnhancedExitScenarioRequest**](EnhancedExitScenarioRequest.md)|  | 

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
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

