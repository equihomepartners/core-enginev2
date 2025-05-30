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

import { mapValues } from '../runtime';
/**
 * Price path visualization response model.
 * @export
 * @interface PricePathVisualizationResponse
 */
export interface PricePathVisualizationResponse {
    /**
     * Price charts by zone
     * @type {{ [key: string]: Array<object>; }}
     * @memberof PricePathVisualizationResponse
     */
    zonePriceCharts: { [key: string]: Array<object>; };
    /**
     * Comparison chart for all zones
     * @type {Array<object>}
     * @memberof PricePathVisualizationResponse
     */
    zoneComparisonChart: Array<object>;
    /**
     * Price charts by suburb
     * @type {{ [key: string]: Array<object>; }}
     * @memberof PricePathVisualizationResponse
     */
    suburbPriceCharts: { [key: string]: Array<object>; };
    /**
     * Correlation heatmap data
     * @type {Array<object>}
     * @memberof PricePathVisualizationResponse
     */
    correlationHeatmap: Array<object>;
    /**
     * Distribution of final property values
     * @type {{ [key: string]: Array<object>; }}
     * @memberof PricePathVisualizationResponse
     */
    finalDistribution: { [key: string]: Array<object>; };
    /**
     * Property cycle position over time
     * @type {Array<object>}
     * @memberof PricePathVisualizationResponse
     */
    cyclePositionChart?: Array<object>;
    /**
     * Market regime over time
     * @type {Array<object>}
     * @memberof PricePathVisualizationResponse
     */
    regimeChart?: Array<object>;
}

/**
 * Check if a given object implements the PricePathVisualizationResponse interface.
 */
export function instanceOfPricePathVisualizationResponse(value: object): value is PricePathVisualizationResponse {
    if (!('zonePriceCharts' in value) || value['zonePriceCharts'] === undefined) return false;
    if (!('zoneComparisonChart' in value) || value['zoneComparisonChart'] === undefined) return false;
    if (!('suburbPriceCharts' in value) || value['suburbPriceCharts'] === undefined) return false;
    if (!('correlationHeatmap' in value) || value['correlationHeatmap'] === undefined) return false;
    if (!('finalDistribution' in value) || value['finalDistribution'] === undefined) return false;
    return true;
}

export function PricePathVisualizationResponseFromJSON(json: any): PricePathVisualizationResponse {
    return PricePathVisualizationResponseFromJSONTyped(json, false);
}

export function PricePathVisualizationResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): PricePathVisualizationResponse {
    if (json == null) {
        return json;
    }
    return {
        
        'zonePriceCharts': json['zone_price_charts'],
        'zoneComparisonChart': json['zone_comparison_chart'],
        'suburbPriceCharts': json['suburb_price_charts'],
        'correlationHeatmap': json['correlation_heatmap'],
        'finalDistribution': json['final_distribution'],
        'cyclePositionChart': json['cycle_position_chart'] == null ? undefined : json['cycle_position_chart'],
        'regimeChart': json['regime_chart'] == null ? undefined : json['regime_chart'],
    };
}

export function PricePathVisualizationResponseToJSON(json: any): PricePathVisualizationResponse {
    return PricePathVisualizationResponseToJSONTyped(json, false);
}

export function PricePathVisualizationResponseToJSONTyped(value?: PricePathVisualizationResponse | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'zone_price_charts': value['zonePriceCharts'],
        'zone_comparison_chart': value['zoneComparisonChart'],
        'suburb_price_charts': value['suburbPriceCharts'],
        'correlation_heatmap': value['correlationHeatmap'],
        'final_distribution': value['finalDistribution'],
        'cycle_position_chart': value['cyclePositionChart'],
        'regime_chart': value['regimeChart'],
    };
}

