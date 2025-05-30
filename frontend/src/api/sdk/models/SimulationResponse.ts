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
 * Simulation response model.
 * @export
 * @interface SimulationResponse
 */
export interface SimulationResponse {
    /**
     * Simulation ID
     * @type {string}
     * @memberof SimulationResponse
     */
    simulationId: string;
    /**
     * Simulation status
     * @type {string}
     * @memberof SimulationResponse
     */
    status: string;
    /**
     * Creation timestamp
     * @type {string}
     * @memberof SimulationResponse
     */
    createdAt: string;
}

/**
 * Check if a given object implements the SimulationResponse interface.
 */
export function instanceOfSimulationResponse(value: object): value is SimulationResponse {
    if (!('simulationId' in value) || value['simulationId'] === undefined) return false;
    if (!('status' in value) || value['status'] === undefined) return false;
    if (!('createdAt' in value) || value['createdAt'] === undefined) return false;
    return true;
}

export function SimulationResponseFromJSON(json: any): SimulationResponse {
    return SimulationResponseFromJSONTyped(json, false);
}

export function SimulationResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): SimulationResponse {
    if (json == null) {
        return json;
    }
    return {
        
        'simulationId': json['simulation_id'],
        'status': json['status'],
        'createdAt': json['created_at'],
    };
}

export function SimulationResponseToJSON(json: any): SimulationResponse {
    return SimulationResponseToJSONTyped(json, false);
}

export function SimulationResponseToJSONTyped(value?: SimulationResponse | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'simulation_id': value['simulationId'],
        'status': value['status'],
        'created_at': value['createdAt'],
    };
}

