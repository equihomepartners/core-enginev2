# equihome_sim_sdk.FinanceApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**calculate_cashflows_finance_cashflows_calculate_post**](FinanceApi.md#calculate_cashflows_finance_cashflows_calculate_post) | **POST** /finance/cashflows/calculate | Calculate Cashflows
[**calculate_fees_finance_fees_calculate_post**](FinanceApi.md#calculate_fees_finance_fees_calculate_post) | **POST** /finance/fees/calculate | Calculate Fees
[**get_cashflows_finance_cashflows_simulation_id_get**](FinanceApi.md#get_cashflows_finance_cashflows_simulation_id_get) | **GET** /finance/cashflows/{simulation_id} | Get Cashflows
[**get_fees_finance_fees_simulation_id_get**](FinanceApi.md#get_fees_finance_fees_simulation_id_get) | **GET** /finance/fees/{simulation_id} | Get Fees


# **calculate_cashflows_finance_cashflows_calculate_post**
> CashflowCalculationResponse calculate_cashflows_finance_cashflows_calculate_post(cashflow_calculation_request, simulation_id=simulation_id)

Calculate Cashflows

Calculate cashflows for a simulation.

This endpoint calculates cashflows for a simulation, including loan-level cashflows,
fund-level cashflows, and stakeholder cashflows.

Args:
    request: Cashflow calculation request
    context: Simulation context

Returns:
    Cashflow calculation response

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.cashflow_calculation_request import CashflowCalculationRequest
from equihome_sim_sdk.models.cashflow_calculation_response import CashflowCalculationResponse
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
    api_instance = equihome_sim_sdk.FinanceApi(api_client)
    cashflow_calculation_request = equihome_sim_sdk.CashflowCalculationRequest() # CashflowCalculationRequest | 
    simulation_id = 'simulation_id_example' # str |  (optional)

    try:
        # Calculate Cashflows
        api_response = api_instance.calculate_cashflows_finance_cashflows_calculate_post(cashflow_calculation_request, simulation_id=simulation_id)
        print("The response of FinanceApi->calculate_cashflows_finance_cashflows_calculate_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FinanceApi->calculate_cashflows_finance_cashflows_calculate_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cashflow_calculation_request** | [**CashflowCalculationRequest**](CashflowCalculationRequest.md)|  | 
 **simulation_id** | **str**|  | [optional] 

### Return type

[**CashflowCalculationResponse**](CashflowCalculationResponse.md)

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

# **calculate_fees_finance_fees_calculate_post**
> FeeCalculationResponse calculate_fees_finance_fees_calculate_post(fee_calculation_request, simulation_id=simulation_id)

Calculate Fees

Calculate fees for a simulation.

This endpoint calculates fees for a simulation, including management fees,
origination fees, fund expenses, acquisition fees, and disposition fees.

Args:
    request: Fee calculation request
    context: Simulation context

Returns:
    Fee calculation response

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.fee_calculation_request import FeeCalculationRequest
from equihome_sim_sdk.models.fee_calculation_response import FeeCalculationResponse
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
    api_instance = equihome_sim_sdk.FinanceApi(api_client)
    fee_calculation_request = equihome_sim_sdk.FeeCalculationRequest() # FeeCalculationRequest | 
    simulation_id = 'simulation_id_example' # str |  (optional)

    try:
        # Calculate Fees
        api_response = api_instance.calculate_fees_finance_fees_calculate_post(fee_calculation_request, simulation_id=simulation_id)
        print("The response of FinanceApi->calculate_fees_finance_fees_calculate_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FinanceApi->calculate_fees_finance_fees_calculate_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fee_calculation_request** | [**FeeCalculationRequest**](FeeCalculationRequest.md)|  | 
 **simulation_id** | **str**|  | [optional] 

### Return type

[**FeeCalculationResponse**](FeeCalculationResponse.md)

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

# **get_cashflows_finance_cashflows_simulation_id_get**
> CashflowCalculationResponse get_cashflows_finance_cashflows_simulation_id_get(simulation_id)

Get Cashflows

Get cashflow calculation results for a simulation.

This endpoint retrieves cashflow calculation results for a simulation.

Args:
    simulation_id: Simulation ID
    context: Simulation context

Returns:
    Cashflow calculation response

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.cashflow_calculation_response import CashflowCalculationResponse
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
    api_instance = equihome_sim_sdk.FinanceApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Cashflows
        api_response = api_instance.get_cashflows_finance_cashflows_simulation_id_get(simulation_id)
        print("The response of FinanceApi->get_cashflows_finance_cashflows_simulation_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FinanceApi->get_cashflows_finance_cashflows_simulation_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**CashflowCalculationResponse**](CashflowCalculationResponse.md)

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

# **get_fees_finance_fees_simulation_id_get**
> FeeCalculationResponse get_fees_finance_fees_simulation_id_get(simulation_id)

Get Fees

Get fee calculation results for a simulation.

This endpoint retrieves fee calculation results for a simulation.

Args:
    simulation_id: Simulation ID
    context: Simulation context

Returns:
    Fee calculation response

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.fee_calculation_response import FeeCalculationResponse
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
    api_instance = equihome_sim_sdk.FinanceApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Fees
        api_response = api_instance.get_fees_finance_fees_simulation_id_get(simulation_id)
        print("The response of FinanceApi->get_fees_finance_fees_simulation_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FinanceApi->get_fees_finance_fees_simulation_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**FeeCalculationResponse**](FeeCalculationResponse.md)

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

