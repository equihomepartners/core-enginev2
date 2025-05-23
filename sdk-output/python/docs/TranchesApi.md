# equihome_sim_sdk.TranchesApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_coverage_test_visualization_tranches_visualization_coverage_tests_get**](TranchesApi.md#get_coverage_test_visualization_tranches_visualization_coverage_tests_get) | **GET** /tranches/visualization/coverage-tests | Get Coverage Test Visualization
[**get_coverage_tests_tranches_coverage_tests_get**](TranchesApi.md#get_coverage_tests_tranches_coverage_tests_get) | **GET** /tranches/coverage-tests | Get Coverage Tests
[**get_reserve_account_tranches_reserve_account_get**](TranchesApi.md#get_reserve_account_tranches_reserve_account_get) | **GET** /tranches/reserve-account | Get Reserve Account
[**get_reserve_account_visualization_tranches_visualization_reserve_account_get**](TranchesApi.md#get_reserve_account_visualization_tranches_visualization_reserve_account_get) | **GET** /tranches/visualization/reserve-account | Get Reserve Account Visualization
[**get_tranche_allocation_visualization_tranches_visualization_allocation_get**](TranchesApi.md#get_tranche_allocation_visualization_tranches_visualization_allocation_get) | **GET** /tranches/visualization/allocation | Get Tranche Allocation Visualization
[**get_tranche_allocations_tranches_tranche_name_allocations_get**](TranchesApi.md#get_tranche_allocations_tranches_tranche_name_allocations_get) | **GET** /tranches/{tranche_name}/allocations | Get Tranche Allocations
[**get_tranche_cashflow_visualization_tranches_visualization_cashflow_get**](TranchesApi.md#get_tranche_cashflow_visualization_tranches_visualization_cashflow_get) | **GET** /tranches/visualization/cashflow | Get Tranche Cashflow Visualization
[**get_tranche_cashflows_tranches_tranche_name_cashflows_get**](TranchesApi.md#get_tranche_cashflows_tranches_tranche_name_cashflows_get) | **GET** /tranches/{tranche_name}/cashflows | Get Tranche Cashflows
[**get_tranche_performance_visualization_tranches_visualization_performance_get**](TranchesApi.md#get_tranche_performance_visualization_tranches_visualization_performance_get) | **GET** /tranches/visualization/performance | Get Tranche Performance Visualization
[**get_tranche_waterfall_visualization_tranches_visualization_waterfall_get**](TranchesApi.md#get_tranche_waterfall_visualization_tranches_visualization_waterfall_get) | **GET** /tranches/visualization/waterfall | Get Tranche Waterfall Visualization
[**get_tranches_tranches_get**](TranchesApi.md#get_tranches_tranches_get) | **GET** /tranches/ | Get Tranches


# **get_coverage_test_visualization_tranches_visualization_coverage_tests_get**
> Dict[str, List[object]] get_coverage_test_visualization_tranches_visualization_coverage_tests_get(simulation_id)

Get Coverage Test Visualization

Get coverage test visualization data.

Args:
    simulation_id: Simulation ID

Returns:
    Coverage test visualization data

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
    api_instance = equihome_sim_sdk.TranchesApi(api_client)
    simulation_id = 'simulation_id_example' # str | Simulation ID

    try:
        # Get Coverage Test Visualization
        api_response = api_instance.get_coverage_test_visualization_tranches_visualization_coverage_tests_get(simulation_id)
        print("The response of TranchesApi->get_coverage_test_visualization_tranches_visualization_coverage_tests_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranchesApi->get_coverage_test_visualization_tranches_visualization_coverage_tests_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**| Simulation ID | 

### Return type

**Dict[str, List[object]]**

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

# **get_coverage_tests_tranches_coverage_tests_get**
> List[CoverageTestResponse] get_coverage_tests_tranches_coverage_tests_get(simulation_id, test_type=test_type)

Get Coverage Tests

Get coverage test results.

Args:
    simulation_id: Simulation ID
    test_type: Test type filter

Returns:
    List of coverage test results

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.coverage_test_response import CoverageTestResponse
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
    api_instance = equihome_sim_sdk.TranchesApi(api_client)
    simulation_id = 'simulation_id_example' # str | Simulation ID
    test_type = 'test_type_example' # str | Test type (overcollateralization, interest_coverage) (optional)

    try:
        # Get Coverage Tests
        api_response = api_instance.get_coverage_tests_tranches_coverage_tests_get(simulation_id, test_type=test_type)
        print("The response of TranchesApi->get_coverage_tests_tranches_coverage_tests_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranchesApi->get_coverage_tests_tranches_coverage_tests_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**| Simulation ID | 
 **test_type** | **str**| Test type (overcollateralization, interest_coverage) | [optional] 

### Return type

[**List[CoverageTestResponse]**](CoverageTestResponse.md)

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

# **get_reserve_account_tranches_reserve_account_get**
> List[ReserveAccountResponse] get_reserve_account_tranches_reserve_account_get(simulation_id)

Get Reserve Account

Get reserve account history.

Args:
    simulation_id: Simulation ID

Returns:
    Reserve account history

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.reserve_account_response import ReserveAccountResponse
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
    api_instance = equihome_sim_sdk.TranchesApi(api_client)
    simulation_id = 'simulation_id_example' # str | Simulation ID

    try:
        # Get Reserve Account
        api_response = api_instance.get_reserve_account_tranches_reserve_account_get(simulation_id)
        print("The response of TranchesApi->get_reserve_account_tranches_reserve_account_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranchesApi->get_reserve_account_tranches_reserve_account_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**| Simulation ID | 

### Return type

[**List[ReserveAccountResponse]**](ReserveAccountResponse.md)

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

# **get_reserve_account_visualization_tranches_visualization_reserve_account_get**
> List[object] get_reserve_account_visualization_tranches_visualization_reserve_account_get(simulation_id)

Get Reserve Account Visualization

Get reserve account visualization data.

Args:
    simulation_id: Simulation ID

Returns:
    Reserve account visualization data

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
    api_instance = equihome_sim_sdk.TranchesApi(api_client)
    simulation_id = 'simulation_id_example' # str | Simulation ID

    try:
        # Get Reserve Account Visualization
        api_response = api_instance.get_reserve_account_visualization_tranches_visualization_reserve_account_get(simulation_id)
        print("The response of TranchesApi->get_reserve_account_visualization_tranches_visualization_reserve_account_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranchesApi->get_reserve_account_visualization_tranches_visualization_reserve_account_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**| Simulation ID | 

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
**404** | Not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tranche_allocation_visualization_tranches_visualization_allocation_get**
> List[object] get_tranche_allocation_visualization_tranches_visualization_allocation_get(simulation_id)

Get Tranche Allocation Visualization

Get tranche allocation visualization data.

Args:
    simulation_id: Simulation ID

Returns:
    Tranche allocation visualization data

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
    api_instance = equihome_sim_sdk.TranchesApi(api_client)
    simulation_id = 'simulation_id_example' # str | Simulation ID

    try:
        # Get Tranche Allocation Visualization
        api_response = api_instance.get_tranche_allocation_visualization_tranches_visualization_allocation_get(simulation_id)
        print("The response of TranchesApi->get_tranche_allocation_visualization_tranches_visualization_allocation_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranchesApi->get_tranche_allocation_visualization_tranches_visualization_allocation_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**| Simulation ID | 

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
**404** | Not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tranche_allocations_tranches_tranche_name_allocations_get**
> List[TrancheAllocationResponse] get_tranche_allocations_tranches_tranche_name_allocations_get(tranche_name, simulation_id)

Get Tranche Allocations

Get loan allocations for a tranche.

Args:
    tranche_name: Tranche name
    simulation_id: Simulation ID

Returns:
    List of loan allocations

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.tranche_allocation_response import TrancheAllocationResponse
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
    api_instance = equihome_sim_sdk.TranchesApi(api_client)
    tranche_name = 'tranche_name_example' # str | 
    simulation_id = 'simulation_id_example' # str | Simulation ID

    try:
        # Get Tranche Allocations
        api_response = api_instance.get_tranche_allocations_tranches_tranche_name_allocations_get(tranche_name, simulation_id)
        print("The response of TranchesApi->get_tranche_allocations_tranches_tranche_name_allocations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranchesApi->get_tranche_allocations_tranches_tranche_name_allocations_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tranche_name** | **str**|  | 
 **simulation_id** | **str**| Simulation ID | 

### Return type

[**List[TrancheAllocationResponse]**](TrancheAllocationResponse.md)

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

# **get_tranche_cashflow_visualization_tranches_visualization_cashflow_get**
> Dict[str, List[object]] get_tranche_cashflow_visualization_tranches_visualization_cashflow_get(simulation_id)

Get Tranche Cashflow Visualization

Get tranche cashflow visualization data.

Args:
    simulation_id: Simulation ID

Returns:
    Tranche cashflow visualization data

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
    api_instance = equihome_sim_sdk.TranchesApi(api_client)
    simulation_id = 'simulation_id_example' # str | Simulation ID

    try:
        # Get Tranche Cashflow Visualization
        api_response = api_instance.get_tranche_cashflow_visualization_tranches_visualization_cashflow_get(simulation_id)
        print("The response of TranchesApi->get_tranche_cashflow_visualization_tranches_visualization_cashflow_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranchesApi->get_tranche_cashflow_visualization_tranches_visualization_cashflow_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**| Simulation ID | 

### Return type

**Dict[str, List[object]]**

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

# **get_tranche_cashflows_tranches_tranche_name_cashflows_get**
> List[TrancheCashflowResponse] get_tranche_cashflows_tranches_tranche_name_cashflows_get(tranche_name, simulation_id)

Get Tranche Cashflows

Get cashflows for a tranche.

Args:
    tranche_name: Tranche name
    simulation_id: Simulation ID

Returns:
    List of cashflows

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.tranche_cashflow_response import TrancheCashflowResponse
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
    api_instance = equihome_sim_sdk.TranchesApi(api_client)
    tranche_name = 'tranche_name_example' # str | 
    simulation_id = 'simulation_id_example' # str | Simulation ID

    try:
        # Get Tranche Cashflows
        api_response = api_instance.get_tranche_cashflows_tranches_tranche_name_cashflows_get(tranche_name, simulation_id)
        print("The response of TranchesApi->get_tranche_cashflows_tranches_tranche_name_cashflows_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranchesApi->get_tranche_cashflows_tranches_tranche_name_cashflows_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tranche_name** | **str**|  | 
 **simulation_id** | **str**| Simulation ID | 

### Return type

[**List[TrancheCashflowResponse]**](TrancheCashflowResponse.md)

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

# **get_tranche_performance_visualization_tranches_visualization_performance_get**
> List[object] get_tranche_performance_visualization_tranches_visualization_performance_get(simulation_id)

Get Tranche Performance Visualization

Get tranche performance visualization data.

Args:
    simulation_id: Simulation ID

Returns:
    Tranche performance visualization data

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
    api_instance = equihome_sim_sdk.TranchesApi(api_client)
    simulation_id = 'simulation_id_example' # str | Simulation ID

    try:
        # Get Tranche Performance Visualization
        api_response = api_instance.get_tranche_performance_visualization_tranches_visualization_performance_get(simulation_id)
        print("The response of TranchesApi->get_tranche_performance_visualization_tranches_visualization_performance_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranchesApi->get_tranche_performance_visualization_tranches_visualization_performance_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**| Simulation ID | 

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
**404** | Not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tranche_waterfall_visualization_tranches_visualization_waterfall_get**
> List[object] get_tranche_waterfall_visualization_tranches_visualization_waterfall_get(simulation_id)

Get Tranche Waterfall Visualization

Get tranche waterfall visualization data.

Args:
    simulation_id: Simulation ID

Returns:
    Tranche waterfall visualization data

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
    api_instance = equihome_sim_sdk.TranchesApi(api_client)
    simulation_id = 'simulation_id_example' # str | Simulation ID

    try:
        # Get Tranche Waterfall Visualization
        api_response = api_instance.get_tranche_waterfall_visualization_tranches_visualization_waterfall_get(simulation_id)
        print("The response of TranchesApi->get_tranche_waterfall_visualization_tranches_visualization_waterfall_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranchesApi->get_tranche_waterfall_visualization_tranches_visualization_waterfall_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**| Simulation ID | 

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
**404** | Not found |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tranches_tranches_get**
> List[TrancheResponse] get_tranches_tranches_get(simulation_id)

Get Tranches

Get all tranches for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    List of tranches

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.tranche_response import TrancheResponse
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
    api_instance = equihome_sim_sdk.TranchesApi(api_client)
    simulation_id = 'simulation_id_example' # str | Simulation ID

    try:
        # Get Tranches
        api_response = api_instance.get_tranches_tranches_get(simulation_id)
        print("The response of TranchesApi->get_tranches_tranches_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TranchesApi->get_tranches_tranches_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**| Simulation ID | 

### Return type

[**List[TrancheResponse]**](TrancheResponse.md)

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

