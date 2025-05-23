# equihome_sim_sdk.ExitSimulatorApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**calculate_loan_exit_api_v1_simulations_simulation_id_exits_loan_exit_post**](ExitSimulatorApi.md#calculate_loan_exit_api_v1_simulations_simulation_id_exits_loan_exit_post) | **POST** /api/v1/simulations/{simulation_id}/exits/loan-exit | Calculate Loan Exit
[**get_exit_statistics_api_v1_simulations_simulation_id_exits_statistics_get**](ExitSimulatorApi.md#get_exit_statistics_api_v1_simulations_simulation_id_exits_statistics_get) | **GET** /api/v1/simulations/{simulation_id}/exits/statistics | Get Exit Statistics
[**get_exit_visualization_api_v1_simulations_simulation_id_exits_visualization_get**](ExitSimulatorApi.md#get_exit_visualization_api_v1_simulations_simulation_id_exits_visualization_get) | **GET** /api/v1/simulations/{simulation_id}/exits/visualization | Get Exit Visualization
[**get_exits_api_v1_simulations_simulation_id_exits_get**](ExitSimulatorApi.md#get_exits_api_v1_simulations_simulation_id_exits_get) | **GET** /api/v1/simulations/{simulation_id}/exits | Get Exits
[**run_exit_scenario_api_v1_simulations_simulation_id_exits_scenario_post**](ExitSimulatorApi.md#run_exit_scenario_api_v1_simulations_simulation_id_exits_scenario_post) | **POST** /api/v1/simulations/{simulation_id}/exits/scenario | Run Exit Scenario


# **calculate_loan_exit_api_v1_simulations_simulation_id_exits_loan_exit_post**
> LoanExitResponse calculate_loan_exit_api_v1_simulations_simulation_id_exits_loan_exit_post(simulation_id, loan_exit_request)

Calculate Loan Exit

Calculate exit value for a specific loan.

Args:
    simulation_id: Simulation ID
    request: Loan exit request

Returns:
    Loan exit value

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.loan_exit_request import LoanExitRequest
from equihome_sim_sdk.models.loan_exit_response import LoanExitResponse
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
    api_instance = equihome_sim_sdk.ExitSimulatorApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    loan_exit_request = equihome_sim_sdk.LoanExitRequest() # LoanExitRequest | 

    try:
        # Calculate Loan Exit
        api_response = api_instance.calculate_loan_exit_api_v1_simulations_simulation_id_exits_loan_exit_post(simulation_id, loan_exit_request)
        print("The response of ExitSimulatorApi->calculate_loan_exit_api_v1_simulations_simulation_id_exits_loan_exit_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExitSimulatorApi->calculate_loan_exit_api_v1_simulations_simulation_id_exits_loan_exit_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **loan_exit_request** | [**LoanExitRequest**](LoanExitRequest.md)|  | 

### Return type

[**LoanExitResponse**](LoanExitResponse.md)

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

# **get_exit_statistics_api_v1_simulations_simulation_id_exits_statistics_get**
> ExitStatisticsResponse get_exit_statistics_api_v1_simulations_simulation_id_exits_statistics_get(simulation_id)

Get Exit Statistics

Get statistics for exits.

Args:
    simulation_id: Simulation ID

Returns:
    Statistics data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.exit_statistics_response import ExitStatisticsResponse
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
    api_instance = equihome_sim_sdk.ExitSimulatorApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Exit Statistics
        api_response = api_instance.get_exit_statistics_api_v1_simulations_simulation_id_exits_statistics_get(simulation_id)
        print("The response of ExitSimulatorApi->get_exit_statistics_api_v1_simulations_simulation_id_exits_statistics_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExitSimulatorApi->get_exit_statistics_api_v1_simulations_simulation_id_exits_statistics_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**ExitStatisticsResponse**](ExitStatisticsResponse.md)

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

# **get_exit_visualization_api_v1_simulations_simulation_id_exits_visualization_get**
> ExitVisualizationResponse get_exit_visualization_api_v1_simulations_simulation_id_exits_visualization_get(simulation_id)

Get Exit Visualization

Get visualization data for exits.

Args:
    simulation_id: Simulation ID

Returns:
    Visualization data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.exit_visualization_response import ExitVisualizationResponse
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
    api_instance = equihome_sim_sdk.ExitSimulatorApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Exit Visualization
        api_response = api_instance.get_exit_visualization_api_v1_simulations_simulation_id_exits_visualization_get(simulation_id)
        print("The response of ExitSimulatorApi->get_exit_visualization_api_v1_simulations_simulation_id_exits_visualization_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExitSimulatorApi->get_exit_visualization_api_v1_simulations_simulation_id_exits_visualization_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**ExitVisualizationResponse**](ExitVisualizationResponse.md)

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

# **get_exits_api_v1_simulations_simulation_id_exits_get**
> object get_exits_api_v1_simulations_simulation_id_exits_get(simulation_id)

Get Exits

Get exit simulation results.

Args:
    simulation_id: Simulation ID

Returns:
    Exit simulation results

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
    api_instance = equihome_sim_sdk.ExitSimulatorApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Exits
        api_response = api_instance.get_exits_api_v1_simulations_simulation_id_exits_get(simulation_id)
        print("The response of ExitSimulatorApi->get_exits_api_v1_simulations_simulation_id_exits_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExitSimulatorApi->get_exits_api_v1_simulations_simulation_id_exits_get: %s\n" % e)
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

# **run_exit_scenario_api_v1_simulations_simulation_id_exits_scenario_post**
> object run_exit_scenario_api_v1_simulations_simulation_id_exits_scenario_post(simulation_id, exit_scenario_request)

Run Exit Scenario

Run an exit scenario with custom parameters.

Args:
    simulation_id: Simulation ID
    request: Exit scenario request

Returns:
    Exit scenario results

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.exit_scenario_request import ExitScenarioRequest
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
    api_instance = equihome_sim_sdk.ExitSimulatorApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    exit_scenario_request = equihome_sim_sdk.ExitScenarioRequest() # ExitScenarioRequest | 

    try:
        # Run Exit Scenario
        api_response = api_instance.run_exit_scenario_api_v1_simulations_simulation_id_exits_scenario_post(simulation_id, exit_scenario_request)
        print("The response of ExitSimulatorApi->run_exit_scenario_api_v1_simulations_simulation_id_exits_scenario_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExitSimulatorApi->run_exit_scenario_api_v1_simulations_simulation_id_exits_scenario_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **exit_scenario_request** | [**ExitScenarioRequest**](ExitScenarioRequest.md)|  | 

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

