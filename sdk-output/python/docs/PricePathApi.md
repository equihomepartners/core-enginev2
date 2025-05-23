# equihome_sim_sdk.PricePathApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_enhanced_property_value_api_v1_simulations_simulation_id_price_paths_enhanced_property_value_post**](PricePathApi.md#get_enhanced_property_value_api_v1_simulations_simulation_id_price_paths_enhanced_property_value_post) | **POST** /api/v1/simulations/{simulation_id}/price-paths/enhanced-property-value | Get Enhanced Property Value
[**get_price_path_statistics_api_v1_simulations_simulation_id_price_paths_statistics_get**](PricePathApi.md#get_price_path_statistics_api_v1_simulations_simulation_id_price_paths_statistics_get) | **GET** /api/v1/simulations/{simulation_id}/price-paths/statistics | Get Price Path Statistics
[**get_price_path_visualization_api_v1_simulations_simulation_id_price_paths_visualization_get**](PricePathApi.md#get_price_path_visualization_api_v1_simulations_simulation_id_price_paths_visualization_get) | **GET** /api/v1/simulations/{simulation_id}/price-paths/visualization | Get Price Path Visualization
[**get_price_paths_api_v1_simulations_simulation_id_price_paths_get**](PricePathApi.md#get_price_paths_api_v1_simulations_simulation_id_price_paths_get) | **GET** /api/v1/simulations/{simulation_id}/price-paths | Get Price Paths
[**get_property_value_api_v1_simulations_simulation_id_price_paths_property_value_post**](PricePathApi.md#get_property_value_api_v1_simulations_simulation_id_price_paths_property_value_post) | **POST** /api/v1/simulations/{simulation_id}/price-paths/property-value | Get Property Value
[**run_enhanced_price_path_scenario_api_v1_simulations_simulation_id_price_paths_enhanced_scenario_post**](PricePathApi.md#run_enhanced_price_path_scenario_api_v1_simulations_simulation_id_price_paths_enhanced_scenario_post) | **POST** /api/v1/simulations/{simulation_id}/price-paths/enhanced-scenario | Run Enhanced Price Path Scenario
[**run_price_path_scenario_api_v1_simulations_simulation_id_price_paths_scenario_post**](PricePathApi.md#run_price_path_scenario_api_v1_simulations_simulation_id_price_paths_scenario_post) | **POST** /api/v1/simulations/{simulation_id}/price-paths/scenario | Run Price Path Scenario


# **get_enhanced_property_value_api_v1_simulations_simulation_id_price_paths_enhanced_property_value_post**
> PropertyValueResponse get_enhanced_property_value_api_v1_simulations_simulation_id_price_paths_enhanced_property_value_post(simulation_id, property_value_request)

Get Enhanced Property Value

Calculate the enhanced property value at a specific month.

Args:
    simulation_id: Simulation ID
    request: Property value request

Returns:
    Property value

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.property_value_request import PropertyValueRequest
from equihome_sim_sdk.models.property_value_response import PropertyValueResponse
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
    api_instance = equihome_sim_sdk.PricePathApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    property_value_request = equihome_sim_sdk.PropertyValueRequest() # PropertyValueRequest | 

    try:
        # Get Enhanced Property Value
        api_response = api_instance.get_enhanced_property_value_api_v1_simulations_simulation_id_price_paths_enhanced_property_value_post(simulation_id, property_value_request)
        print("The response of PricePathApi->get_enhanced_property_value_api_v1_simulations_simulation_id_price_paths_enhanced_property_value_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PricePathApi->get_enhanced_property_value_api_v1_simulations_simulation_id_price_paths_enhanced_property_value_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **property_value_request** | [**PropertyValueRequest**](PropertyValueRequest.md)|  | 

### Return type

[**PropertyValueResponse**](PropertyValueResponse.md)

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

# **get_price_path_statistics_api_v1_simulations_simulation_id_price_paths_statistics_get**
> PricePathStatisticsResponse get_price_path_statistics_api_v1_simulations_simulation_id_price_paths_statistics_get(simulation_id)

Get Price Path Statistics

Get statistics for price paths.

Args:
    simulation_id: Simulation ID

Returns:
    Statistics data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.price_path_statistics_response import PricePathStatisticsResponse
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
    api_instance = equihome_sim_sdk.PricePathApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Price Path Statistics
        api_response = api_instance.get_price_path_statistics_api_v1_simulations_simulation_id_price_paths_statistics_get(simulation_id)
        print("The response of PricePathApi->get_price_path_statistics_api_v1_simulations_simulation_id_price_paths_statistics_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PricePathApi->get_price_path_statistics_api_v1_simulations_simulation_id_price_paths_statistics_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**PricePathStatisticsResponse**](PricePathStatisticsResponse.md)

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

# **get_price_path_visualization_api_v1_simulations_simulation_id_price_paths_visualization_get**
> PricePathVisualizationResponse get_price_path_visualization_api_v1_simulations_simulation_id_price_paths_visualization_get(simulation_id)

Get Price Path Visualization

Get visualization data for price paths.

Args:
    simulation_id: Simulation ID

Returns:
    Visualization data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.price_path_visualization_response import PricePathVisualizationResponse
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
    api_instance = equihome_sim_sdk.PricePathApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Price Path Visualization
        api_response = api_instance.get_price_path_visualization_api_v1_simulations_simulation_id_price_paths_visualization_get(simulation_id)
        print("The response of PricePathApi->get_price_path_visualization_api_v1_simulations_simulation_id_price_paths_visualization_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PricePathApi->get_price_path_visualization_api_v1_simulations_simulation_id_price_paths_visualization_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**PricePathVisualizationResponse**](PricePathVisualizationResponse.md)

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

# **get_price_paths_api_v1_simulations_simulation_id_price_paths_get**
> object get_price_paths_api_v1_simulations_simulation_id_price_paths_get(simulation_id)

Get Price Paths

Get price path data for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    Price path data

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
    api_instance = equihome_sim_sdk.PricePathApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Price Paths
        api_response = api_instance.get_price_paths_api_v1_simulations_simulation_id_price_paths_get(simulation_id)
        print("The response of PricePathApi->get_price_paths_api_v1_simulations_simulation_id_price_paths_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PricePathApi->get_price_paths_api_v1_simulations_simulation_id_price_paths_get: %s\n" % e)
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

# **get_property_value_api_v1_simulations_simulation_id_price_paths_property_value_post**
> PropertyValueResponse get_property_value_api_v1_simulations_simulation_id_price_paths_property_value_post(simulation_id, property_value_request)

Get Property Value

Calculate the property value at a specific month.

Args:
    simulation_id: Simulation ID
    request: Property value request

Returns:
    Property value

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.property_value_request import PropertyValueRequest
from equihome_sim_sdk.models.property_value_response import PropertyValueResponse
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
    api_instance = equihome_sim_sdk.PricePathApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    property_value_request = equihome_sim_sdk.PropertyValueRequest() # PropertyValueRequest | 

    try:
        # Get Property Value
        api_response = api_instance.get_property_value_api_v1_simulations_simulation_id_price_paths_property_value_post(simulation_id, property_value_request)
        print("The response of PricePathApi->get_property_value_api_v1_simulations_simulation_id_price_paths_property_value_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PricePathApi->get_property_value_api_v1_simulations_simulation_id_price_paths_property_value_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **property_value_request** | [**PropertyValueRequest**](PropertyValueRequest.md)|  | 

### Return type

[**PropertyValueResponse**](PropertyValueResponse.md)

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

# **run_enhanced_price_path_scenario_api_v1_simulations_simulation_id_price_paths_enhanced_scenario_post**
> object run_enhanced_price_path_scenario_api_v1_simulations_simulation_id_price_paths_enhanced_scenario_post(simulation_id, enhanced_price_path_scenario_request)

Run Enhanced Price Path Scenario

Run an enhanced price path scenario with custom parameters.

This endpoint uses the enhanced price path simulator that integrates more deeply
with the TLS module to generate realistic price paths based on suburb-specific
data, economic factors, and Sydney property market cycles.

Args:
    simulation_id: Simulation ID
    request: Enhanced price path scenario request

Returns:
    Enhanced price path scenario results

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.enhanced_price_path_scenario_request import EnhancedPricePathScenarioRequest
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
    api_instance = equihome_sim_sdk.PricePathApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    enhanced_price_path_scenario_request = equihome_sim_sdk.EnhancedPricePathScenarioRequest() # EnhancedPricePathScenarioRequest | 

    try:
        # Run Enhanced Price Path Scenario
        api_response = api_instance.run_enhanced_price_path_scenario_api_v1_simulations_simulation_id_price_paths_enhanced_scenario_post(simulation_id, enhanced_price_path_scenario_request)
        print("The response of PricePathApi->run_enhanced_price_path_scenario_api_v1_simulations_simulation_id_price_paths_enhanced_scenario_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PricePathApi->run_enhanced_price_path_scenario_api_v1_simulations_simulation_id_price_paths_enhanced_scenario_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **enhanced_price_path_scenario_request** | [**EnhancedPricePathScenarioRequest**](EnhancedPricePathScenarioRequest.md)|  | 

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

# **run_price_path_scenario_api_v1_simulations_simulation_id_price_paths_scenario_post**
> object run_price_path_scenario_api_v1_simulations_simulation_id_price_paths_scenario_post(simulation_id, price_path_scenario_request)

Run Price Path Scenario

Run a price path scenario with custom parameters.

Args:
    simulation_id: Simulation ID
    request: Price path scenario request

Returns:
    Price path scenario results

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.price_path_scenario_request import PricePathScenarioRequest
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
    api_instance = equihome_sim_sdk.PricePathApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    price_path_scenario_request = equihome_sim_sdk.PricePathScenarioRequest() # PricePathScenarioRequest | 

    try:
        # Run Price Path Scenario
        api_response = api_instance.run_price_path_scenario_api_v1_simulations_simulation_id_price_paths_scenario_post(simulation_id, price_path_scenario_request)
        print("The response of PricePathApi->run_price_path_scenario_api_v1_simulations_simulation_id_price_paths_scenario_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PricePathApi->run_price_path_scenario_api_v1_simulations_simulation_id_price_paths_scenario_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **price_path_scenario_request** | [**PricePathScenarioRequest**](PricePathScenarioRequest.md)|  | 

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

