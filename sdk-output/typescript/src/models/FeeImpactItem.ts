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
 * Fee impact item model.
 * @export
 * @interface FeeImpactItem
 */
export interface FeeImpactItem {
    /**
     * Performance metric
     * @type {string}
     * @memberof FeeImpactItem
     */
    metric: string;
    /**
     * Gross value (before fees)
     * @type {number}
     * @memberof FeeImpactItem
     */
    gross: number;
    /**
     * Net value (after fees)
     * @type {number}
     * @memberof FeeImpactItem
     */
    net: number;
    /**
     * Impact of fees
     * @type {number}
     * @memberof FeeImpactItem
     */
    impact: number;
}

/**
 * Check if a given object implements the FeeImpactItem interface.
 */
export function instanceOfFeeImpactItem(value: object): value is FeeImpactItem {
    if (!('metric' in value) || value['metric'] === undefined) return false;
    if (!('gross' in value) || value['gross'] === undefined) return false;
    if (!('net' in value) || value['net'] === undefined) return false;
    if (!('impact' in value) || value['impact'] === undefined) return false;
    return true;
}

export function FeeImpactItemFromJSON(json: any): FeeImpactItem {
    return FeeImpactItemFromJSONTyped(json, false);
}

export function FeeImpactItemFromJSONTyped(json: any, ignoreDiscriminator: boolean): FeeImpactItem {
    if (json == null) {
        return json;
    }
    return {
        
        'metric': json['metric'],
        'gross': json['gross'],
        'net': json['net'],
        'impact': json['impact'],
    };
}

export function FeeImpactItemToJSON(json: any): FeeImpactItem {
    return FeeImpactItemToJSONTyped(json, false);
}

export function FeeImpactItemToJSONTyped(value?: FeeImpactItem | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'metric': value['metric'],
        'gross': value['gross'],
        'net': value['net'],
        'impact': value['impact'],
    };
}

