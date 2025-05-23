# equihome_sim_sdk.TlsApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_metric_correlations_tls_correlations_metrics_get**](TlsApi.md#get_metric_correlations_tls_correlations_metrics_get) | **GET** /tls/correlations/metrics | Get Metric Correlations
[**get_metric_distribution_tls_metrics_metric_name_distribution_get**](TlsApi.md#get_metric_distribution_tls_metrics_metric_name_distribution_get) | **GET** /tls/metrics/{metric_name}/distribution | Get Metric Distribution
[**get_metrics_tls_metrics_get**](TlsApi.md#get_metrics_tls_metrics_get) | **GET** /tls/metrics | Get Metrics
[**get_property_distribution_tls_visualization_property_distribution_get**](TlsApi.md#get_property_distribution_tls_visualization_property_distribution_get) | **GET** /tls/visualization/property_distribution | Get Property Distribution
[**get_suburb_tls_suburbs_suburb_id_get**](TlsApi.md#get_suburb_tls_suburbs_suburb_id_get) | **GET** /tls/suburbs/{suburb_id} | Get Suburb
[**get_suburbs_tls_suburbs_get**](TlsApi.md#get_suburbs_tls_suburbs_get) | **GET** /tls/suburbs | Get Suburbs
[**get_zone_distribution_tls_zones_distribution_get**](TlsApi.md#get_zone_distribution_tls_zones_distribution_get) | **GET** /tls/zones/distribution | Get Zone Distribution
[**get_zone_map_tls_visualization_zone_map_get**](TlsApi.md#get_zone_map_tls_visualization_zone_map_get) | **GET** /tls/visualization/zone_map | Get Zone Map


# **get_metric_correlations_tls_correlations_metrics_get**
> CorrelationMatrix get_metric_correlations_tls_correlations_metrics_get(metrics=metrics)

Get Metric Correlations

Get correlation matrix for metrics.

Args:
    metrics: List of metric names to include (if not provided, uses top 20 metrics)

Returns:
    Correlation matrix

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.correlation_matrix import CorrelationMatrix
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
    api_instance = equihome_sim_sdk.TlsApi(api_client)
    metrics = ['metrics_example'] # List[str] |  (optional)

    try:
        # Get Metric Correlations
        api_response = api_instance.get_metric_correlations_tls_correlations_metrics_get(metrics=metrics)
        print("The response of TlsApi->get_metric_correlations_tls_correlations_metrics_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TlsApi->get_metric_correlations_tls_correlations_metrics_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **metrics** | [**List[str]**](str.md)|  | [optional] 

### Return type

[**CorrelationMatrix**](CorrelationMatrix.md)

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

# **get_metric_distribution_tls_metrics_metric_name_distribution_get**
> MetricDistribution get_metric_distribution_tls_metrics_metric_name_distribution_get(metric_name, zone=zone)

Get Metric Distribution

Get distribution of a metric across all suburbs.

Args:
    metric_name: Metric name
    zone: Zone category (green, orange, red) to filter by

Returns:
    Metric distribution statistics

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.metric_distribution import MetricDistribution
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
    api_instance = equihome_sim_sdk.TlsApi(api_client)
    metric_name = 'metric_name_example' # str | 
    zone = 'zone_example' # str |  (optional)

    try:
        # Get Metric Distribution
        api_response = api_instance.get_metric_distribution_tls_metrics_metric_name_distribution_get(metric_name, zone=zone)
        print("The response of TlsApi->get_metric_distribution_tls_metrics_metric_name_distribution_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TlsApi->get_metric_distribution_tls_metrics_metric_name_distribution_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **metric_name** | **str**|  | 
 **zone** | **str**|  | [optional] 

### Return type

[**MetricDistribution**](MetricDistribution.md)

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

# **get_metrics_tls_metrics_get**
> List[MetricDefinition] get_metrics_tls_metrics_get(category=category)

Get Metrics

Get all metrics or metrics by category.

Args:
    category: Metric category (economic, real_estate, demographic, risk, location, supply_demand, temporal)

Returns:
    List of metric definitions

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.metric_definition import MetricDefinition
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
    api_instance = equihome_sim_sdk.TlsApi(api_client)
    category = 'category_example' # str |  (optional)

    try:
        # Get Metrics
        api_response = api_instance.get_metrics_tls_metrics_get(category=category)
        print("The response of TlsApi->get_metrics_tls_metrics_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TlsApi->get_metrics_tls_metrics_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category** | **str**|  | [optional] 

### Return type

[**List[MetricDefinition]**](MetricDefinition.md)

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

# **get_property_distribution_tls_visualization_property_distribution_get**
> PropertyDistribution get_property_distribution_tls_visualization_property_distribution_get()

Get Property Distribution

Get property distribution data for visualization.

Returns:
    Property distribution data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.property_distribution import PropertyDistribution
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
    api_instance = equihome_sim_sdk.TlsApi(api_client)

    try:
        # Get Property Distribution
        api_response = api_instance.get_property_distribution_tls_visualization_property_distribution_get()
        print("The response of TlsApi->get_property_distribution_tls_visualization_property_distribution_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TlsApi->get_property_distribution_tls_visualization_property_distribution_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**PropertyDistribution**](PropertyDistribution.md)

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

# **get_suburb_tls_suburbs_suburb_id_get**
> SuburbDetail get_suburb_tls_suburbs_suburb_id_get(suburb_id)

Get Suburb

Get a suburb by ID.

Args:
    suburb_id: Suburb ID

Returns:
    Suburb details

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.suburb_detail import SuburbDetail
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
    api_instance = equihome_sim_sdk.TlsApi(api_client)
    suburb_id = 'suburb_id_example' # str | 

    try:
        # Get Suburb
        api_response = api_instance.get_suburb_tls_suburbs_suburb_id_get(suburb_id)
        print("The response of TlsApi->get_suburb_tls_suburbs_suburb_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TlsApi->get_suburb_tls_suburbs_suburb_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **suburb_id** | **str**|  | 

### Return type

[**SuburbDetail**](SuburbDetail.md)

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

# **get_suburbs_tls_suburbs_get**
> List[SuburbSummary] get_suburbs_tls_suburbs_get(zone=zone, min_score=min_score, max_score=max_score, sort_by=sort_by, sort_order=sort_order, limit=limit, offset=offset)

Get Suburbs

Get all suburbs or suburbs by zone.

Args:
    zone: Zone category (green, orange, red) to filter by
    min_score: Minimum overall score (0-100)
    max_score: Maximum overall score (0-100)
    sort_by: Field to sort by (overall_score, appreciation_score, risk_score, liquidity_score, name)
    sort_order: Sort order (asc, desc)
    limit: Maximum number of suburbs to return
    offset: Number of suburbs to skip

Returns:
    List of suburb summaries

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.suburb_summary import SuburbSummary
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
    api_instance = equihome_sim_sdk.TlsApi(api_client)
    zone = 'zone_example' # str |  (optional)
    min_score = 3.4 # float |  (optional)
    max_score = 3.4 # float |  (optional)
    sort_by = 'overall_score' # str |  (optional) (default to 'overall_score')
    sort_order = 'desc' # str |  (optional) (default to 'desc')
    limit = 100 # int |  (optional) (default to 100)
    offset = 0 # int |  (optional) (default to 0)

    try:
        # Get Suburbs
        api_response = api_instance.get_suburbs_tls_suburbs_get(zone=zone, min_score=min_score, max_score=max_score, sort_by=sort_by, sort_order=sort_order, limit=limit, offset=offset)
        print("The response of TlsApi->get_suburbs_tls_suburbs_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TlsApi->get_suburbs_tls_suburbs_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **zone** | **str**|  | [optional] 
 **min_score** | **float**|  | [optional] 
 **max_score** | **float**|  | [optional] 
 **sort_by** | **str**|  | [optional] [default to &#39;overall_score&#39;]
 **sort_order** | **str**|  | [optional] [default to &#39;desc&#39;]
 **limit** | **int**|  | [optional] [default to 100]
 **offset** | **int**|  | [optional] [default to 0]

### Return type

[**List[SuburbSummary]**](SuburbSummary.md)

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

# **get_zone_distribution_tls_zones_distribution_get**
> ZoneDistribution get_zone_distribution_tls_zones_distribution_get()

Get Zone Distribution

Get distribution of suburbs by zone category.

Returns:
    Zone distribution statistics

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.zone_distribution import ZoneDistribution
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
    api_instance = equihome_sim_sdk.TlsApi(api_client)

    try:
        # Get Zone Distribution
        api_response = api_instance.get_zone_distribution_tls_zones_distribution_get()
        print("The response of TlsApi->get_zone_distribution_tls_zones_distribution_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TlsApi->get_zone_distribution_tls_zones_distribution_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ZoneDistribution**](ZoneDistribution.md)

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

# **get_zone_map_tls_visualization_zone_map_get**
> object get_zone_map_tls_visualization_zone_map_get()

Get Zone Map

Get data for zone map visualization.

Returns:
    Zone map data

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
    api_instance = equihome_sim_sdk.TlsApi(api_client)

    try:
        # Get Zone Map
        api_response = api_instance.get_zone_map_tls_visualization_zone_map_get()
        print("The response of TlsApi->get_zone_map_tls_visualization_zone_map_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TlsApi->get_zone_map_tls_visualization_zone_map_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

