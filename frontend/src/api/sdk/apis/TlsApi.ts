/* tslint:disable */
/* eslint-disable */
/**
 * EQU IHOME SIM ENGINE API
 * API for running home equity investment fund simulations
 *
 * The version of the OpenAPI document: 0.1.0
 * Contact: info@equihome.com
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import * as runtime from '../runtime';
import type {
  CorrelationMatrix,
  HTTPValidationError,
  MetricDefinition,
  MetricDistribution,
  PropertyDistribution,
  SuburbDetail,
  SuburbSummary,
  ZoneDistribution,
} from '../models/index';
import {
    CorrelationMatrixFromJSON,
    CorrelationMatrixToJSON,
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
    MetricDefinitionFromJSON,
    MetricDefinitionToJSON,
    MetricDistributionFromJSON,
    MetricDistributionToJSON,
    PropertyDistributionFromJSON,
    PropertyDistributionToJSON,
    SuburbDetailFromJSON,
    SuburbDetailToJSON,
    SuburbSummaryFromJSON,
    SuburbSummaryToJSON,
    ZoneDistributionFromJSON,
    ZoneDistributionToJSON,
} from '../models/index';

export interface GetMetricCorrelationsTlsCorrelationsMetricsGetRequest {
    metrics?: Array<string>;
}

export interface GetMetricDistributionTlsMetricsMetricNameDistributionGetRequest {
    metricName: string;
    zone?: string;
}

export interface GetMetricsTlsMetricsGetRequest {
    category?: string;
}

export interface GetSuburbTlsSuburbsSuburbIdGetRequest {
    suburbId: string;
}

export interface GetSuburbsTlsSuburbsGetRequest {
    zone?: string;
    minScore?: number;
    maxScore?: number;
    sortBy?: string;
    sortOrder?: string;
    limit?: number;
    offset?: number;
}

/**
 * TlsApi - interface
 * 
 * @export
 * @interface TlsApiInterface
 */
export interface TlsApiInterface {
    /**
     * Get correlation matrix for metrics.  Args:     metrics: List of metric names to include (if not provided, uses top 20 metrics)  Returns:     Correlation matrix
     * @summary Get Metric Correlations
     * @param {Array<string>} [metrics] 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof TlsApiInterface
     */
    getMetricCorrelationsTlsCorrelationsMetricsGetRaw(requestParameters: GetMetricCorrelationsTlsCorrelationsMetricsGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<CorrelationMatrix>>;

    /**
     * Get correlation matrix for metrics.  Args:     metrics: List of metric names to include (if not provided, uses top 20 metrics)  Returns:     Correlation matrix
     * Get Metric Correlations
     */
    getMetricCorrelationsTlsCorrelationsMetricsGet(requestParameters: GetMetricCorrelationsTlsCorrelationsMetricsGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<CorrelationMatrix>;

    /**
     * Get distribution of a metric across all suburbs.  Args:     metric_name: Metric name     zone: Zone category (green, orange, red) to filter by  Returns:     Metric distribution statistics
     * @summary Get Metric Distribution
     * @param {string} metricName 
     * @param {string} [zone] 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof TlsApiInterface
     */
    getMetricDistributionTlsMetricsMetricNameDistributionGetRaw(requestParameters: GetMetricDistributionTlsMetricsMetricNameDistributionGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<MetricDistribution>>;

    /**
     * Get distribution of a metric across all suburbs.  Args:     metric_name: Metric name     zone: Zone category (green, orange, red) to filter by  Returns:     Metric distribution statistics
     * Get Metric Distribution
     */
    getMetricDistributionTlsMetricsMetricNameDistributionGet(requestParameters: GetMetricDistributionTlsMetricsMetricNameDistributionGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<MetricDistribution>;

    /**
     * Get all metrics or metrics by category.  Args:     category: Metric category (economic, real_estate, demographic, risk, location, supply_demand, temporal)  Returns:     List of metric definitions
     * @summary Get Metrics
     * @param {string} [category] 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof TlsApiInterface
     */
    getMetricsTlsMetricsGetRaw(requestParameters: GetMetricsTlsMetricsGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<MetricDefinition>>>;

    /**
     * Get all metrics or metrics by category.  Args:     category: Metric category (economic, real_estate, demographic, risk, location, supply_demand, temporal)  Returns:     List of metric definitions
     * Get Metrics
     */
    getMetricsTlsMetricsGet(requestParameters: GetMetricsTlsMetricsGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<MetricDefinition>>;

    /**
     * Get property distribution data for visualization.  Returns:     Property distribution data
     * @summary Get Property Distribution
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof TlsApiInterface
     */
    getPropertyDistributionTlsVisualizationPropertyDistributionGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<PropertyDistribution>>;

    /**
     * Get property distribution data for visualization.  Returns:     Property distribution data
     * Get Property Distribution
     */
    getPropertyDistributionTlsVisualizationPropertyDistributionGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<PropertyDistribution>;

    /**
     * Get a suburb by ID.  Args:     suburb_id: Suburb ID  Returns:     Suburb details
     * @summary Get Suburb
     * @param {string} suburbId 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof TlsApiInterface
     */
    getSuburbTlsSuburbsSuburbIdGetRaw(requestParameters: GetSuburbTlsSuburbsSuburbIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<SuburbDetail>>;

    /**
     * Get a suburb by ID.  Args:     suburb_id: Suburb ID  Returns:     Suburb details
     * Get Suburb
     */
    getSuburbTlsSuburbsSuburbIdGet(requestParameters: GetSuburbTlsSuburbsSuburbIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<SuburbDetail>;

    /**
     * Get all suburbs or suburbs by zone.  Args:     zone: Zone category (green, orange, red) to filter by     min_score: Minimum overall score (0-100)     max_score: Maximum overall score (0-100)     sort_by: Field to sort by (overall_score, appreciation_score, risk_score, liquidity_score, name)     sort_order: Sort order (asc, desc)     limit: Maximum number of suburbs to return     offset: Number of suburbs to skip  Returns:     List of suburb summaries
     * @summary Get Suburbs
     * @param {string} [zone] 
     * @param {number} [minScore] 
     * @param {number} [maxScore] 
     * @param {string} [sortBy] 
     * @param {string} [sortOrder] 
     * @param {number} [limit] 
     * @param {number} [offset] 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof TlsApiInterface
     */
    getSuburbsTlsSuburbsGetRaw(requestParameters: GetSuburbsTlsSuburbsGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<SuburbSummary>>>;

    /**
     * Get all suburbs or suburbs by zone.  Args:     zone: Zone category (green, orange, red) to filter by     min_score: Minimum overall score (0-100)     max_score: Maximum overall score (0-100)     sort_by: Field to sort by (overall_score, appreciation_score, risk_score, liquidity_score, name)     sort_order: Sort order (asc, desc)     limit: Maximum number of suburbs to return     offset: Number of suburbs to skip  Returns:     List of suburb summaries
     * Get Suburbs
     */
    getSuburbsTlsSuburbsGet(requestParameters: GetSuburbsTlsSuburbsGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<SuburbSummary>>;

    /**
     * Get distribution of suburbs by zone category.  Returns:     Zone distribution statistics
     * @summary Get Zone Distribution
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof TlsApiInterface
     */
    getZoneDistributionTlsZonesDistributionGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<ZoneDistribution>>;

    /**
     * Get distribution of suburbs by zone category.  Returns:     Zone distribution statistics
     * Get Zone Distribution
     */
    getZoneDistributionTlsZonesDistributionGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<ZoneDistribution>;

    /**
     * Get data for zone map visualization.  Returns:     Zone map data
     * @summary Get Zone Map
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof TlsApiInterface
     */
    getZoneMapTlsVisualizationZoneMapGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<object>>;

    /**
     * Get data for zone map visualization.  Returns:     Zone map data
     * Get Zone Map
     */
    getZoneMapTlsVisualizationZoneMapGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<object>;

}

/**
 * 
 */
export class TlsApi extends runtime.BaseAPI implements TlsApiInterface {

    /**
     * Get correlation matrix for metrics.  Args:     metrics: List of metric names to include (if not provided, uses top 20 metrics)  Returns:     Correlation matrix
     * Get Metric Correlations
     */
    async getMetricCorrelationsTlsCorrelationsMetricsGetRaw(requestParameters: GetMetricCorrelationsTlsCorrelationsMetricsGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<CorrelationMatrix>> {
        const queryParameters: any = {};

        if (requestParameters['metrics'] != null) {
            queryParameters['metrics'] = requestParameters['metrics'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["X-API-Key"] = await this.configuration.apiKey("X-API-Key"); // apiKey authentication
        }

        const response = await this.request({
            path: `/tls/correlations/metrics`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => CorrelationMatrixFromJSON(jsonValue));
    }

    /**
     * Get correlation matrix for metrics.  Args:     metrics: List of metric names to include (if not provided, uses top 20 metrics)  Returns:     Correlation matrix
     * Get Metric Correlations
     */
    async getMetricCorrelationsTlsCorrelationsMetricsGet(requestParameters: GetMetricCorrelationsTlsCorrelationsMetricsGetRequest = {}, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<CorrelationMatrix> {
        const response = await this.getMetricCorrelationsTlsCorrelationsMetricsGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get distribution of a metric across all suburbs.  Args:     metric_name: Metric name     zone: Zone category (green, orange, red) to filter by  Returns:     Metric distribution statistics
     * Get Metric Distribution
     */
    async getMetricDistributionTlsMetricsMetricNameDistributionGetRaw(requestParameters: GetMetricDistributionTlsMetricsMetricNameDistributionGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<MetricDistribution>> {
        if (requestParameters['metricName'] == null) {
            throw new runtime.RequiredError(
                'metricName',
                'Required parameter "metricName" was null or undefined when calling getMetricDistributionTlsMetricsMetricNameDistributionGet().'
            );
        }

        const queryParameters: any = {};

        if (requestParameters['zone'] != null) {
            queryParameters['zone'] = requestParameters['zone'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["X-API-Key"] = await this.configuration.apiKey("X-API-Key"); // apiKey authentication
        }

        const response = await this.request({
            path: `/tls/metrics/{metric_name}/distribution`.replace(`{${"metric_name"}}`, encodeURIComponent(String(requestParameters['metricName']))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => MetricDistributionFromJSON(jsonValue));
    }

    /**
     * Get distribution of a metric across all suburbs.  Args:     metric_name: Metric name     zone: Zone category (green, orange, red) to filter by  Returns:     Metric distribution statistics
     * Get Metric Distribution
     */
    async getMetricDistributionTlsMetricsMetricNameDistributionGet(requestParameters: GetMetricDistributionTlsMetricsMetricNameDistributionGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<MetricDistribution> {
        const response = await this.getMetricDistributionTlsMetricsMetricNameDistributionGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get all metrics or metrics by category.  Args:     category: Metric category (economic, real_estate, demographic, risk, location, supply_demand, temporal)  Returns:     List of metric definitions
     * Get Metrics
     */
    async getMetricsTlsMetricsGetRaw(requestParameters: GetMetricsTlsMetricsGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<MetricDefinition>>> {
        const queryParameters: any = {};

        if (requestParameters['category'] != null) {
            queryParameters['category'] = requestParameters['category'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["X-API-Key"] = await this.configuration.apiKey("X-API-Key"); // apiKey authentication
        }

        const response = await this.request({
            path: `/tls/metrics`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(MetricDefinitionFromJSON));
    }

    /**
     * Get all metrics or metrics by category.  Args:     category: Metric category (economic, real_estate, demographic, risk, location, supply_demand, temporal)  Returns:     List of metric definitions
     * Get Metrics
     */
    async getMetricsTlsMetricsGet(requestParameters: GetMetricsTlsMetricsGetRequest = {}, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<MetricDefinition>> {
        const response = await this.getMetricsTlsMetricsGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get property distribution data for visualization.  Returns:     Property distribution data
     * Get Property Distribution
     */
    async getPropertyDistributionTlsVisualizationPropertyDistributionGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<PropertyDistribution>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["X-API-Key"] = await this.configuration.apiKey("X-API-Key"); // apiKey authentication
        }

        const response = await this.request({
            path: `/tls/visualization/property_distribution`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => PropertyDistributionFromJSON(jsonValue));
    }

    /**
     * Get property distribution data for visualization.  Returns:     Property distribution data
     * Get Property Distribution
     */
    async getPropertyDistributionTlsVisualizationPropertyDistributionGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<PropertyDistribution> {
        const response = await this.getPropertyDistributionTlsVisualizationPropertyDistributionGetRaw(initOverrides);
        return await response.value();
    }

    /**
     * Get a suburb by ID.  Args:     suburb_id: Suburb ID  Returns:     Suburb details
     * Get Suburb
     */
    async getSuburbTlsSuburbsSuburbIdGetRaw(requestParameters: GetSuburbTlsSuburbsSuburbIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<SuburbDetail>> {
        if (requestParameters['suburbId'] == null) {
            throw new runtime.RequiredError(
                'suburbId',
                'Required parameter "suburbId" was null or undefined when calling getSuburbTlsSuburbsSuburbIdGet().'
            );
        }

        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["X-API-Key"] = await this.configuration.apiKey("X-API-Key"); // apiKey authentication
        }

        const response = await this.request({
            path: `/tls/suburbs/{suburb_id}`.replace(`{${"suburb_id"}}`, encodeURIComponent(String(requestParameters['suburbId']))),
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => SuburbDetailFromJSON(jsonValue));
    }

    /**
     * Get a suburb by ID.  Args:     suburb_id: Suburb ID  Returns:     Suburb details
     * Get Suburb
     */
    async getSuburbTlsSuburbsSuburbIdGet(requestParameters: GetSuburbTlsSuburbsSuburbIdGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<SuburbDetail> {
        const response = await this.getSuburbTlsSuburbsSuburbIdGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get all suburbs or suburbs by zone.  Args:     zone: Zone category (green, orange, red) to filter by     min_score: Minimum overall score (0-100)     max_score: Maximum overall score (0-100)     sort_by: Field to sort by (overall_score, appreciation_score, risk_score, liquidity_score, name)     sort_order: Sort order (asc, desc)     limit: Maximum number of suburbs to return     offset: Number of suburbs to skip  Returns:     List of suburb summaries
     * Get Suburbs
     */
    async getSuburbsTlsSuburbsGetRaw(requestParameters: GetSuburbsTlsSuburbsGetRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<Array<SuburbSummary>>> {
        const queryParameters: any = {};

        if (requestParameters['zone'] != null) {
            queryParameters['zone'] = requestParameters['zone'];
        }

        if (requestParameters['minScore'] != null) {
            queryParameters['min_score'] = requestParameters['minScore'];
        }

        if (requestParameters['maxScore'] != null) {
            queryParameters['max_score'] = requestParameters['maxScore'];
        }

        if (requestParameters['sortBy'] != null) {
            queryParameters['sort_by'] = requestParameters['sortBy'];
        }

        if (requestParameters['sortOrder'] != null) {
            queryParameters['sort_order'] = requestParameters['sortOrder'];
        }

        if (requestParameters['limit'] != null) {
            queryParameters['limit'] = requestParameters['limit'];
        }

        if (requestParameters['offset'] != null) {
            queryParameters['offset'] = requestParameters['offset'];
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["X-API-Key"] = await this.configuration.apiKey("X-API-Key"); // apiKey authentication
        }

        const response = await this.request({
            path: `/tls/suburbs`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => jsonValue.map(SuburbSummaryFromJSON));
    }

    /**
     * Get all suburbs or suburbs by zone.  Args:     zone: Zone category (green, orange, red) to filter by     min_score: Minimum overall score (0-100)     max_score: Maximum overall score (0-100)     sort_by: Field to sort by (overall_score, appreciation_score, risk_score, liquidity_score, name)     sort_order: Sort order (asc, desc)     limit: Maximum number of suburbs to return     offset: Number of suburbs to skip  Returns:     List of suburb summaries
     * Get Suburbs
     */
    async getSuburbsTlsSuburbsGet(requestParameters: GetSuburbsTlsSuburbsGetRequest = {}, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<Array<SuburbSummary>> {
        const response = await this.getSuburbsTlsSuburbsGetRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Get distribution of suburbs by zone category.  Returns:     Zone distribution statistics
     * Get Zone Distribution
     */
    async getZoneDistributionTlsZonesDistributionGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<ZoneDistribution>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["X-API-Key"] = await this.configuration.apiKey("X-API-Key"); // apiKey authentication
        }

        const response = await this.request({
            path: `/tls/zones/distribution`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => ZoneDistributionFromJSON(jsonValue));
    }

    /**
     * Get distribution of suburbs by zone category.  Returns:     Zone distribution statistics
     * Get Zone Distribution
     */
    async getZoneDistributionTlsZonesDistributionGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<ZoneDistribution> {
        const response = await this.getZoneDistributionTlsZonesDistributionGetRaw(initOverrides);
        return await response.value();
    }

    /**
     * Get data for zone map visualization.  Returns:     Zone map data
     * Get Zone Map
     */
    async getZoneMapTlsVisualizationZoneMapGetRaw(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<object>> {
        const queryParameters: any = {};

        const headerParameters: runtime.HTTPHeaders = {};

        if (this.configuration && this.configuration.apiKey) {
            headerParameters["X-API-Key"] = await this.configuration.apiKey("X-API-Key"); // apiKey authentication
        }

        const response = await this.request({
            path: `/tls/visualization/zone_map`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse<any>(response);
    }

    /**
     * Get data for zone map visualization.  Returns:     Zone map data
     * Get Zone Map
     */
    async getZoneMapTlsVisualizationZoneMapGet(initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<object> {
        const response = await this.getZoneMapTlsVisualizationZoneMapGetRaw(initOverrides);
        return await response.value();
    }

}
