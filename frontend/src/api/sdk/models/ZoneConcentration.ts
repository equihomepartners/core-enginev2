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
 * Zone concentration model.
 * @export
 * @interface ZoneConcentration
 */
export interface ZoneConcentration {
    /**
     * Concentration in green zone
     * @type {number}
     * @memberof ZoneConcentration
     */
    green?: number;
    /**
     * Concentration in orange zone
     * @type {number}
     * @memberof ZoneConcentration
     */
    orange?: number;
    /**
     * Concentration in red zone
     * @type {number}
     * @memberof ZoneConcentration
     */
    red?: number;
    /**
     * Zone HHI
     * @type {number}
     * @memberof ZoneConcentration
     */
    hhi?: number;
}

/**
 * Check if a given object implements the ZoneConcentration interface.
 */
export function instanceOfZoneConcentration(value: object): value is ZoneConcentration {
    return true;
}

export function ZoneConcentrationFromJSON(json: any): ZoneConcentration {
    return ZoneConcentrationFromJSONTyped(json, false);
}

export function ZoneConcentrationFromJSONTyped(json: any, ignoreDiscriminator: boolean): ZoneConcentration {
    if (json == null) {
        return json;
    }
    return {
        
        'green': json['green'] == null ? undefined : json['green'],
        'orange': json['orange'] == null ? undefined : json['orange'],
        'red': json['red'] == null ? undefined : json['red'],
        'hhi': json['hhi'] == null ? undefined : json['hhi'],
    };
}

export function ZoneConcentrationToJSON(json: any): ZoneConcentration {
    return ZoneConcentrationToJSONTyped(json, false);
}

export function ZoneConcentrationToJSONTyped(value?: ZoneConcentration | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'green': value['green'],
        'orange': value['orange'],
        'red': value['red'],
        'hhi': value['hhi'],
    };
}

