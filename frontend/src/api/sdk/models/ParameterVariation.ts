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
 * Parameter variation model.
 * @export
 * @interface ParameterVariation
 */
export interface ParameterVariation {
    /**
     * Parameter name
     * @type {string}
     * @memberof ParameterVariation
     */
    parameter: string;
    /**
     * Parameter value
     * @type {number}
     * @memberof ParameterVariation
     */
    value: number;
    /**
     * Metrics for this parameter value
     * @type {{ [key: string]: number; }}
     * @memberof ParameterVariation
     */
    metrics: { [key: string]: number; };
}

/**
 * Check if a given object implements the ParameterVariation interface.
 */
export function instanceOfParameterVariation(value: object): value is ParameterVariation {
    if (!('parameter' in value) || value['parameter'] === undefined) return false;
    if (!('value' in value) || value['value'] === undefined) return false;
    if (!('metrics' in value) || value['metrics'] === undefined) return false;
    return true;
}

export function ParameterVariationFromJSON(json: any): ParameterVariation {
    return ParameterVariationFromJSONTyped(json, false);
}

export function ParameterVariationFromJSONTyped(json: any, ignoreDiscriminator: boolean): ParameterVariation {
    if (json == null) {
        return json;
    }
    return {
        
        'parameter': json['parameter'],
        'value': json['value'],
        'metrics': json['metrics'],
    };
}

export function ParameterVariationToJSON(json: any): ParameterVariation {
    return ParameterVariationToJSONTyped(json, false);
}

export function ParameterVariationToJSONTyped(value?: ParameterVariation | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'parameter': value['parameter'],
        'value': value['value'],
        'metrics': value['metrics'],
    };
}

