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
import type { FeeVisualization } from './FeeVisualization';
import {
    FeeVisualizationFromJSON,
    FeeVisualizationFromJSONTyped,
    FeeVisualizationToJSON,
    FeeVisualizationToJSONTyped,
} from './FeeVisualization';

/**
 * Response model for fee calculation.
 * @export
 * @interface FeeCalculationResponse
 */
export interface FeeCalculationResponse {
    /**
     * Simulation ID
     * @type {string}
     * @memberof FeeCalculationResponse
     */
    simulationId: string;
    /**
     * Total fees by category
     * @type {{ [key: string]: number; }}
     * @memberof FeeCalculationResponse
     */
    totalFees: { [key: string]: number; };
    /**
     * Impact of fees on fund performance
     * @type {{ [key: string]: number; }}
     * @memberof FeeCalculationResponse
     */
    feeImpact: { [key: string]: number; };
    /**
     * Visualization data
     * @type {FeeVisualization}
     * @memberof FeeCalculationResponse
     */
    visualization: FeeVisualization;
}

/**
 * Check if a given object implements the FeeCalculationResponse interface.
 */
export function instanceOfFeeCalculationResponse(value: object): value is FeeCalculationResponse {
    if (!('simulationId' in value) || value['simulationId'] === undefined) return false;
    if (!('totalFees' in value) || value['totalFees'] === undefined) return false;
    if (!('feeImpact' in value) || value['feeImpact'] === undefined) return false;
    if (!('visualization' in value) || value['visualization'] === undefined) return false;
    return true;
}

export function FeeCalculationResponseFromJSON(json: any): FeeCalculationResponse {
    return FeeCalculationResponseFromJSONTyped(json, false);
}

export function FeeCalculationResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): FeeCalculationResponse {
    if (json == null) {
        return json;
    }
    return {
        
        'simulationId': json['simulation_id'],
        'totalFees': json['total_fees'],
        'feeImpact': json['fee_impact'],
        'visualization': FeeVisualizationFromJSON(json['visualization']),
    };
}

export function FeeCalculationResponseToJSON(json: any): FeeCalculationResponse {
    return FeeCalculationResponseToJSONTyped(json, false);
}

export function FeeCalculationResponseToJSONTyped(value?: FeeCalculationResponse | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'simulation_id': value['simulationId'],
        'total_fees': value['totalFees'],
        'fee_impact': value['feeImpact'],
        'visualization': FeeVisualizationToJSON(value['visualization']),
    };
}

