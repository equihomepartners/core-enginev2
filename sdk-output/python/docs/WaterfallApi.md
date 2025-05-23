# equihome_sim_sdk.WaterfallApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**calculate_waterfall_distribution_simulations_simulation_id_waterfall_calculate_post**](WaterfallApi.md#calculate_waterfall_distribution_simulations_simulation_id_waterfall_calculate_post) | **POST** /simulations/{simulation_id}/waterfall/calculate | Calculate waterfall distribution
[**get_waterfall_distribution_simulations_simulation_id_waterfall_get**](WaterfallApi.md#get_waterfall_distribution_simulations_simulation_id_waterfall_get) | **GET** /simulations/{simulation_id}/waterfall | Get waterfall distribution for a simulation
[**get_waterfall_visualization_simulations_simulation_id_waterfall_visualization_get**](WaterfallApi.md#get_waterfall_visualization_simulations_simulation_id_waterfall_visualization_get) | **GET** /simulations/{simulation_id}/waterfall/visualization | Get waterfall visualization data


# **calculate_waterfall_distribution_simulations_simulation_id_waterfall_calculate_post**
> WaterfallResultModel calculate_waterfall_distribution_simulations_simulation_id_waterfall_calculate_post(simulation_id, waterfall_config_model)

Calculate waterfall distribution

Calculates waterfall distribution based on provided configuration

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.waterfall_config_model import WaterfallConfigModel
from equihome_sim_sdk.models.waterfall_result_model import WaterfallResultModel
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
    api_instance = equihome_sim_sdk.WaterfallApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    waterfall_config_model = equihome_sim_sdk.WaterfallConfigModel() # WaterfallConfigModel | 

    try:
        # Calculate waterfall distribution
        api_response = api_instance.calculate_waterfall_distribution_simulations_simulation_id_waterfall_calculate_post(simulation_id, waterfall_config_model)
        print("The response of WaterfallApi->calculate_waterfall_distribution_simulations_simulation_id_waterfall_calculate_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaterfallApi->calculate_waterfall_distribution_simulations_simulation_id_waterfall_calculate_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **waterfall_config_model** | [**WaterfallConfigModel**](WaterfallConfigModel.md)|  | 

### Return type

[**WaterfallResultModel**](WaterfallResultModel.md)

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

# **get_waterfall_distribution_simulations_simulation_id_waterfall_get**
> WaterfallResultModel get_waterfall_distribution_simulations_simulation_id_waterfall_get(simulation_id)

Get waterfall distribution for a simulation

Returns the waterfall distribution for a simulation

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.waterfall_result_model import WaterfallResultModel
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
    api_instance = equihome_sim_sdk.WaterfallApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get waterfall distribution for a simulation
        api_response = api_instance.get_waterfall_distribution_simulations_simulation_id_waterfall_get(simulation_id)
        print("The response of WaterfallApi->get_waterfall_distribution_simulations_simulation_id_waterfall_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaterfallApi->get_waterfall_distribution_simulations_simulation_id_waterfall_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**WaterfallResultModel**](WaterfallResultModel.md)

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

# **get_waterfall_visualization_simulations_simulation_id_waterfall_visualization_get**
> WaterfallVisualizationModel get_waterfall_visualization_simulations_simulation_id_waterfall_visualization_get(simulation_id)

Get waterfall visualization data

Returns visualization data for waterfall distribution

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.waterfall_visualization_model import WaterfallVisualizationModel
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
    api_instance = equihome_sim_sdk.WaterfallApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get waterfall visualization data
        api_response = api_instance.get_waterfall_visualization_simulations_simulation_id_waterfall_visualization_get(simulation_id)
        print("The response of WaterfallApi->get_waterfall_visualization_simulations_simulation_id_waterfall_visualization_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WaterfallApi->get_waterfall_visualization_simulations_simulation_id_waterfall_visualization_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**WaterfallVisualizationModel**](WaterfallVisualizationModel.md)

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

