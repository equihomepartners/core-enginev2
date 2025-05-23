# equihome_sim_sdk.PortfolioApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_allocation_history_simulations_simulation_id_allocation_history_get**](PortfolioApi.md#get_allocation_history_simulations_simulation_id_allocation_history_get) | **GET** /simulations/{simulation_id}/allocation-history | Get Allocation History
[**get_capital_allocation_simulations_simulation_id_capital_allocation_get**](PortfolioApi.md#get_capital_allocation_simulations_simulation_id_capital_allocation_get) | **GET** /simulations/{simulation_id}/capital-allocation | Get Capital Allocation
[**get_leverage_events_simulations_simulation_id_leverage_events_get**](PortfolioApi.md#get_leverage_events_simulations_simulation_id_leverage_events_get) | **GET** /simulations/{simulation_id}/leverage/events | Get Leverage Events
[**get_leverage_facilities_simulations_simulation_id_leverage_facilities_get**](PortfolioApi.md#get_leverage_facilities_simulations_simulation_id_leverage_facilities_get) | **GET** /simulations/{simulation_id}/leverage/facilities | Get Leverage Facilities
[**get_leverage_metrics_simulations_simulation_id_leverage_metrics_get**](PortfolioApi.md#get_leverage_metrics_simulations_simulation_id_leverage_metrics_get) | **GET** /simulations/{simulation_id}/leverage/metrics | Get Leverage Metrics
[**get_leverage_simulations_simulation_id_leverage_get**](PortfolioApi.md#get_leverage_simulations_simulation_id_leverage_get) | **GET** /simulations/{simulation_id}/leverage | Get Leverage
[**get_loan_portfolio_history_simulations_simulation_id_loan_portfolio_history_get**](PortfolioApi.md#get_loan_portfolio_history_simulations_simulation_id_loan_portfolio_history_get) | **GET** /simulations/{simulation_id}/loan-portfolio-history | Get Loan Portfolio History
[**get_loan_portfolio_simulations_simulation_id_loan_portfolio_get**](PortfolioApi.md#get_loan_portfolio_simulations_simulation_id_loan_portfolio_get) | **GET** /simulations/{simulation_id}/loan-portfolio | Get Loan Portfolio
[**get_loans_simulations_simulation_id_loans_get**](PortfolioApi.md#get_loans_simulations_simulation_id_loans_get) | **GET** /simulations/{simulation_id}/loans | Get Loans
[**get_rebalancing_recommendation_simulations_simulation_id_rebalancing_recommendation_get**](PortfolioApi.md#get_rebalancing_recommendation_simulations_simulation_id_rebalancing_recommendation_get) | **GET** /simulations/{simulation_id}/rebalancing-recommendation | Get Rebalancing Recommendation
[**get_visualizations_simulations_simulation_id_visualizations_get**](PortfolioApi.md#get_visualizations_simulations_simulation_id_visualizations_get) | **GET** /simulations/{simulation_id}/visualizations | Get Visualizations
[**reinvest_simulations_simulation_id_reinvest_post**](PortfolioApi.md#reinvest_simulations_simulation_id_reinvest_post) | **POST** /simulations/{simulation_id}/reinvest | Reinvest


# **get_allocation_history_simulations_simulation_id_allocation_history_get**
> object get_allocation_history_simulations_simulation_id_allocation_history_get(simulation_id)

Get Allocation History

Get allocation history for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    Allocation history data

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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Allocation History
        api_response = api_instance.get_allocation_history_simulations_simulation_id_allocation_history_get(simulation_id)
        print("The response of PortfolioApi->get_allocation_history_simulations_simulation_id_allocation_history_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->get_allocation_history_simulations_simulation_id_allocation_history_get: %s\n" % e)
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

# **get_capital_allocation_simulations_simulation_id_capital_allocation_get**
> CapitalAllocation get_capital_allocation_simulations_simulation_id_capital_allocation_get(simulation_id)

Get Capital Allocation

Get capital allocation data for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    Capital allocation data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.capital_allocation import CapitalAllocation
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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Capital Allocation
        api_response = api_instance.get_capital_allocation_simulations_simulation_id_capital_allocation_get(simulation_id)
        print("The response of PortfolioApi->get_capital_allocation_simulations_simulation_id_capital_allocation_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->get_capital_allocation_simulations_simulation_id_capital_allocation_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**CapitalAllocation**](CapitalAllocation.md)

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

# **get_leverage_events_simulations_simulation_id_leverage_events_get**
> List[LeverageEvent] get_leverage_events_simulations_simulation_id_leverage_events_get(simulation_id, event_type=event_type, facility_id=facility_id)

Get Leverage Events

Get leverage events for a simulation.

Args:
    simulation_id: Simulation ID
    event_type: Filter by event type (draw, repayment, interest, fee)
    facility_id: Filter by facility ID

Returns:
    Leverage events

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.leverage_event import LeverageEvent
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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    event_type = 'event_type_example' # str | Filter by event type (draw, repayment, interest, fee) (optional)
    facility_id = 'facility_id_example' # str | Filter by facility ID (optional)

    try:
        # Get Leverage Events
        api_response = api_instance.get_leverage_events_simulations_simulation_id_leverage_events_get(simulation_id, event_type=event_type, facility_id=facility_id)
        print("The response of PortfolioApi->get_leverage_events_simulations_simulation_id_leverage_events_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->get_leverage_events_simulations_simulation_id_leverage_events_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **event_type** | **str**| Filter by event type (draw, repayment, interest, fee) | [optional] 
 **facility_id** | **str**| Filter by facility ID | [optional] 

### Return type

[**List[LeverageEvent]**](LeverageEvent.md)

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

# **get_leverage_facilities_simulations_simulation_id_leverage_facilities_get**
> List[LeverageFacility] get_leverage_facilities_simulations_simulation_id_leverage_facilities_get(simulation_id)

Get Leverage Facilities

Get leverage facilities for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    Leverage facilities

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.leverage_facility import LeverageFacility
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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Leverage Facilities
        api_response = api_instance.get_leverage_facilities_simulations_simulation_id_leverage_facilities_get(simulation_id)
        print("The response of PortfolioApi->get_leverage_facilities_simulations_simulation_id_leverage_facilities_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->get_leverage_facilities_simulations_simulation_id_leverage_facilities_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**List[LeverageFacility]**](LeverageFacility.md)

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

# **get_leverage_metrics_simulations_simulation_id_leverage_metrics_get**
> SrcApiRoutersPortfolioLeverageMetrics get_leverage_metrics_simulations_simulation_id_leverage_metrics_get(simulation_id)

Get Leverage Metrics

Get leverage metrics for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    Leverage metrics

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.src_api_routers_portfolio_leverage_metrics import SrcApiRoutersPortfolioLeverageMetrics
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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Leverage Metrics
        api_response = api_instance.get_leverage_metrics_simulations_simulation_id_leverage_metrics_get(simulation_id)
        print("The response of PortfolioApi->get_leverage_metrics_simulations_simulation_id_leverage_metrics_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->get_leverage_metrics_simulations_simulation_id_leverage_metrics_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**SrcApiRoutersPortfolioLeverageMetrics**](SrcApiRoutersPortfolioLeverageMetrics.md)

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

# **get_leverage_simulations_simulation_id_leverage_get**
> LeverageResponse get_leverage_simulations_simulation_id_leverage_get(simulation_id)

Get Leverage

Get leverage data for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    Leverage data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.leverage_response import LeverageResponse
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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Leverage
        api_response = api_instance.get_leverage_simulations_simulation_id_leverage_get(simulation_id)
        print("The response of PortfolioApi->get_leverage_simulations_simulation_id_leverage_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->get_leverage_simulations_simulation_id_leverage_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**LeverageResponse**](LeverageResponse.md)

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

# **get_loan_portfolio_history_simulations_simulation_id_loan_portfolio_history_get**
> object get_loan_portfolio_history_simulations_simulation_id_loan_portfolio_history_get(simulation_id)

Get Loan Portfolio History

Get loan portfolio history for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    Loan portfolio history data

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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Loan Portfolio History
        api_response = api_instance.get_loan_portfolio_history_simulations_simulation_id_loan_portfolio_history_get(simulation_id)
        print("The response of PortfolioApi->get_loan_portfolio_history_simulations_simulation_id_loan_portfolio_history_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->get_loan_portfolio_history_simulations_simulation_id_loan_portfolio_history_get: %s\n" % e)
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

# **get_loan_portfolio_simulations_simulation_id_loan_portfolio_get**
> LoanPortfolio get_loan_portfolio_simulations_simulation_id_loan_portfolio_get(simulation_id)

Get Loan Portfolio

Get loan portfolio statistics and visualization data for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    Loan portfolio data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.loan_portfolio import LoanPortfolio
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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Loan Portfolio
        api_response = api_instance.get_loan_portfolio_simulations_simulation_id_loan_portfolio_get(simulation_id)
        print("The response of PortfolioApi->get_loan_portfolio_simulations_simulation_id_loan_portfolio_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->get_loan_portfolio_simulations_simulation_id_loan_portfolio_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**LoanPortfolio**](LoanPortfolio.md)

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

# **get_loans_simulations_simulation_id_loans_get**
> LoansResponse get_loans_simulations_simulation_id_loans_get(simulation_id, zone=zone, limit=limit, offset=offset)

Get Loans

Get loans for a simulation.

Args:
    simulation_id: Simulation ID
    zone: Filter by zone (green, orange, red)
    limit: Maximum number of loans to return
    offset: Offset for pagination

Returns:
    Loans data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.loans_response import LoansResponse
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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    zone = 'zone_example' # str | Filter by zone (green, orange, red) (optional)
    limit = 100 # int | Maximum number of loans to return (optional) (default to 100)
    offset = 0 # int | Offset for pagination (optional) (default to 0)

    try:
        # Get Loans
        api_response = api_instance.get_loans_simulations_simulation_id_loans_get(simulation_id, zone=zone, limit=limit, offset=offset)
        print("The response of PortfolioApi->get_loans_simulations_simulation_id_loans_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->get_loans_simulations_simulation_id_loans_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **zone** | **str**| Filter by zone (green, orange, red) | [optional] 
 **limit** | **int**| Maximum number of loans to return | [optional] [default to 100]
 **offset** | **int**| Offset for pagination | [optional] [default to 0]

### Return type

[**LoansResponse**](LoansResponse.md)

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

# **get_rebalancing_recommendation_simulations_simulation_id_rebalancing_recommendation_get**
> object get_rebalancing_recommendation_simulations_simulation_id_rebalancing_recommendation_get(simulation_id, tolerance=tolerance)

Get Rebalancing Recommendation

Get rebalancing recommendation for a simulation.

Args:
    simulation_id: Simulation ID
    tolerance: Tolerance for allocation mismatch

Returns:
    Rebalancing recommendation

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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    tolerance = 0.05 # float | Tolerance for allocation mismatch (optional) (default to 0.05)

    try:
        # Get Rebalancing Recommendation
        api_response = api_instance.get_rebalancing_recommendation_simulations_simulation_id_rebalancing_recommendation_get(simulation_id, tolerance=tolerance)
        print("The response of PortfolioApi->get_rebalancing_recommendation_simulations_simulation_id_rebalancing_recommendation_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->get_rebalancing_recommendation_simulations_simulation_id_rebalancing_recommendation_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **tolerance** | **float**| Tolerance for allocation mismatch | [optional] [default to 0.05]

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

# **get_visualizations_simulations_simulation_id_visualizations_get**
> VisualizationResponse get_visualizations_simulations_simulation_id_visualizations_get(simulation_id)

Get Visualizations

Get visualization data for a simulation.

Args:
    simulation_id: Simulation ID

Returns:
    Visualization data

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.visualization_response import VisualizationResponse
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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Visualizations
        api_response = api_instance.get_visualizations_simulations_simulation_id_visualizations_get(simulation_id)
        print("The response of PortfolioApi->get_visualizations_simulations_simulation_id_visualizations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->get_visualizations_simulations_simulation_id_visualizations_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**VisualizationResponse**](VisualizationResponse.md)

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

# **reinvest_simulations_simulation_id_reinvest_post**
> SrcApiRoutersPortfolioReinvestmentResponse reinvest_simulations_simulation_id_reinvest_post(simulation_id, reinvestment_request)

Reinvest

Generate reinvestment loans for a simulation.

Args:
    simulation_id: Simulation ID
    request: Reinvestment request

Returns:
    Generated reinvestment loans

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.reinvestment_request import ReinvestmentRequest
from equihome_sim_sdk.models.src_api_routers_portfolio_reinvestment_response import SrcApiRoutersPortfolioReinvestmentResponse
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
    api_instance = equihome_sim_sdk.PortfolioApi(api_client)
    simulation_id = 'simulation_id_example' # str | 
    reinvestment_request = equihome_sim_sdk.ReinvestmentRequest() # ReinvestmentRequest | 

    try:
        # Reinvest
        api_response = api_instance.reinvest_simulations_simulation_id_reinvest_post(simulation_id, reinvestment_request)
        print("The response of PortfolioApi->reinvest_simulations_simulation_id_reinvest_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PortfolioApi->reinvest_simulations_simulation_id_reinvest_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 
 **reinvestment_request** | [**ReinvestmentRequest**](ReinvestmentRequest.md)|  | 

### Return type

[**SrcApiRoutersPortfolioReinvestmentResponse**](SrcApiRoutersPortfolioReinvestmentResponse.md)

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

