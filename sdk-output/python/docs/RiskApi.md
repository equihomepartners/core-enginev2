# equihome_sim_sdk.RiskApi

All URIs are relative to *http://localhost:8000*

Method | HTTP request | Description
------------- | ------------- | -------------
[**calculate_risk_metrics_risk_metrics_calculate_post**](RiskApi.md#calculate_risk_metrics_risk_metrics_calculate_post) | **POST** /risk/metrics/calculate | Calculate Risk Metrics
[**get_risk_metrics_risk_metrics_simulation_id_get**](RiskApi.md#get_risk_metrics_risk_metrics_simulation_id_get) | **GET** /risk/metrics/{simulation_id} | Get Risk Metrics
[**get_risk_visualization_risk_visualization_simulation_id_get**](RiskApi.md#get_risk_visualization_risk_visualization_simulation_id_get) | **GET** /risk/visualization/{simulation_id} | Get Risk Visualization
[**run_stress_test_risk_stress_test_post**](RiskApi.md#run_stress_test_risk_stress_test_post) | **POST** /risk/stress-test | Run Stress Test


# **calculate_risk_metrics_risk_metrics_calculate_post**
> SrcApiRoutersRiskRiskMetricsResponse calculate_risk_metrics_risk_metrics_calculate_post(risk_metrics_request, simulation_id=simulation_id)

Calculate Risk Metrics

Calculate risk metrics for a simulation.

This endpoint calculates a comprehensive set of risk metrics for a simulation, organized into the following categories:

- **Market/Price Metrics**: Volatility, Alpha, Beta, VaR, CVaR
- **Credit Metrics**: LTV, Stress-LTV, Default probabilities
- **Liquidity Metrics**: Liquidity scores, Exit lag, WAL
- **Leverage Metrics**: NAV utilisation, Interest coverage
- **Concentration Metrics**: Zone exposure, Suburb exposure, Single-loan exposure
- **Performance/Return-Risk Metrics**: IRR, Sharpe ratio, Sortino ratio, etc.
- **Scenario/Stress Metrics**: Price shock, Rate shock, Default shock

Some metrics require Monte Carlo simulation to calculate accurately. When Monte Carlo is disabled or not available,
these metrics will be approximated or marked as "requires MC" in the response.

Args:
    request: Risk metrics calculation request
    context: Simulation context

Returns:
    Risk metrics calculation response with all categories of metrics

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.risk_metrics_request import RiskMetricsRequest
from equihome_sim_sdk.models.src_api_routers_risk_risk_metrics_response import SrcApiRoutersRiskRiskMetricsResponse
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
    api_instance = equihome_sim_sdk.RiskApi(api_client)
    risk_metrics_request = equihome_sim_sdk.RiskMetricsRequest() # RiskMetricsRequest | 
    simulation_id = 'simulation_id_example' # str |  (optional)

    try:
        # Calculate Risk Metrics
        api_response = api_instance.calculate_risk_metrics_risk_metrics_calculate_post(risk_metrics_request, simulation_id=simulation_id)
        print("The response of RiskApi->calculate_risk_metrics_risk_metrics_calculate_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RiskApi->calculate_risk_metrics_risk_metrics_calculate_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **risk_metrics_request** | [**RiskMetricsRequest**](RiskMetricsRequest.md)|  | 
 **simulation_id** | **str**|  | [optional] 

### Return type

[**SrcApiRoutersRiskRiskMetricsResponse**](SrcApiRoutersRiskRiskMetricsResponse.md)

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

# **get_risk_metrics_risk_metrics_simulation_id_get**
> SrcApiRoutersRiskRiskMetricsResponse get_risk_metrics_risk_metrics_simulation_id_get(simulation_id)

Get Risk Metrics

Get risk metrics for a simulation.

This endpoint retrieves previously calculated risk metrics for a simulation, organized into the following categories:

- **Market/Price Metrics**: Volatility, Alpha, Beta, VaR, CVaR
- **Credit Metrics**: LTV, Stress-LTV, Default probabilities
- **Liquidity Metrics**: Liquidity scores, Exit lag, WAL
- **Leverage Metrics**: NAV utilisation, Interest coverage
- **Concentration Metrics**: Zone exposure, Suburb exposure, Single-loan exposure
- **Performance/Return-Risk Metrics**: IRR, Sharpe ratio, Sortino ratio, etc.

Some metrics may be marked as "requires MC" if Monte Carlo simulation was not enabled for this simulation.

Args:
    simulation_id: Simulation ID
    context: Simulation context

Returns:
    Risk metrics response with all categories of metrics

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.src_api_routers_risk_risk_metrics_response import SrcApiRoutersRiskRiskMetricsResponse
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
    api_instance = equihome_sim_sdk.RiskApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Risk Metrics
        api_response = api_instance.get_risk_metrics_risk_metrics_simulation_id_get(simulation_id)
        print("The response of RiskApi->get_risk_metrics_risk_metrics_simulation_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RiskApi->get_risk_metrics_risk_metrics_simulation_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**SrcApiRoutersRiskRiskMetricsResponse**](SrcApiRoutersRiskRiskMetricsResponse.md)

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

# **get_risk_visualization_risk_visualization_simulation_id_get**
> RiskVisualization get_risk_visualization_risk_visualization_simulation_id_get(simulation_id)

Get Risk Visualization

Get risk visualization data for a simulation.

This endpoint retrieves risk visualization data for a simulation, including:

- **Risk-Return Scatter Plot**: Shows the relationship between risk and return for different scenarios
- **VaR Histogram**: Shows the distribution of returns with VaR thresholds
- **Drawdown Chart**: Shows the drawdown over time
- **Stress Test Comparison**: Shows the impact of stress scenarios on key metrics
- **Sensitivity Charts**: Shows how metrics change with parameter variations
- **Concentration Chart**: Shows the concentration of exposure by zone, suburb, etc.

The visualization data is designed to be easily consumed by frontend charting libraries.
When Monte Carlo simulation is enabled, the visualizations will include distribution
information. In deterministic mode, the visualizations will be based on single-path data.

Args:
    simulation_id: Simulation ID
    context: Simulation context

Returns:
    Comprehensive risk visualization data for charts and graphs

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.risk_visualization import RiskVisualization
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
    api_instance = equihome_sim_sdk.RiskApi(api_client)
    simulation_id = 'simulation_id_example' # str | 

    try:
        # Get Risk Visualization
        api_response = api_instance.get_risk_visualization_risk_visualization_simulation_id_get(simulation_id)
        print("The response of RiskApi->get_risk_visualization_risk_visualization_simulation_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RiskApi->get_risk_visualization_risk_visualization_simulation_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **simulation_id** | **str**|  | 

### Return type

[**RiskVisualization**](RiskVisualization.md)

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

# **run_stress_test_risk_stress_test_post**
> SrcApiRoutersRiskRiskMetricsResponse run_stress_test_risk_stress_test_post(stress_test_request, simulation_id=simulation_id)

Run Stress Test

Run stress tests on a simulation.

This endpoint runs stress tests on a simulation, applying shocks to key parameters
and recalculating metrics under stress scenarios. The following types of shocks can be applied:

- **Property Value Shock**: Applies a percentage shock to property values (e.g., -10%, -20%, -30%)
- **Interest Rate Shock**: Applies a percentage point shock to interest rates (e.g., +1%, +2%, +3%)
- **Default Rate Shock**: Applies a multiplier to default rates (e.g., 1.5x, 2x, 3x)
- **Liquidity Shock**: Applies a percentage shock to liquidity (e.g., -30%, -50%, -70%)

The stress test results include recalculated metrics for each scenario, allowing comparison
between base case and stressed scenarios. This helps identify vulnerabilities and assess
the portfolio's resilience to adverse market conditions.

Stress tests work in both deterministic and Monte Carlo modes, but provide more detailed
distribution impacts when Monte Carlo is enabled.

Args:
    request: Stress test request with scenarios to apply
    context: Simulation context

Returns:
    Risk metrics response with comprehensive stress test results

### Example

* Api Key Authentication (apiKey):

```python
import equihome_sim_sdk
from equihome_sim_sdk.models.src_api_routers_risk_risk_metrics_response import SrcApiRoutersRiskRiskMetricsResponse
from equihome_sim_sdk.models.stress_test_request import StressTestRequest
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
    api_instance = equihome_sim_sdk.RiskApi(api_client)
    stress_test_request = equihome_sim_sdk.StressTestRequest() # StressTestRequest | 
    simulation_id = 'simulation_id_example' # str |  (optional)

    try:
        # Run Stress Test
        api_response = api_instance.run_stress_test_risk_stress_test_post(stress_test_request, simulation_id=simulation_id)
        print("The response of RiskApi->run_stress_test_risk_stress_test_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RiskApi->run_stress_test_risk_stress_test_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **stress_test_request** | [**StressTestRequest**](StressTestRequest.md)|  | 
 **simulation_id** | **str**|  | [optional] 

### Return type

[**SrcApiRoutersRiskRiskMetricsResponse**](SrcApiRoutersRiskRiskMetricsResponse.md)

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

