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
import type { Loan } from './Loan';
import {
    LoanFromJSON,
    LoanFromJSONTyped,
    LoanToJSON,
    LoanToJSONTyped,
} from './Loan';

/**
 * Loans response model.
 * @export
 * @interface LoansResponse
 */
export interface LoansResponse {
    /**
     * List of loans
     * @type {Array<Loan>}
     * @memberof LoansResponse
     */
    loans: Array<Loan>;
    /**
     * Total number of loans
     * @type {number}
     * @memberof LoansResponse
     */
    totalCount: number;
    /**
     * Maximum number of loans to return
     * @type {number}
     * @memberof LoansResponse
     */
    limit: number;
    /**
     * Offset for pagination
     * @type {number}
     * @memberof LoansResponse
     */
    offset: number;
}

/**
 * Check if a given object implements the LoansResponse interface.
 */
export function instanceOfLoansResponse(value: object): value is LoansResponse {
    if (!('loans' in value) || value['loans'] === undefined) return false;
    if (!('totalCount' in value) || value['totalCount'] === undefined) return false;
    if (!('limit' in value) || value['limit'] === undefined) return false;
    if (!('offset' in value) || value['offset'] === undefined) return false;
    return true;
}

export function LoansResponseFromJSON(json: any): LoansResponse {
    return LoansResponseFromJSONTyped(json, false);
}

export function LoansResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): LoansResponse {
    if (json == null) {
        return json;
    }
    return {
        
        'loans': ((json['loans'] as Array<any>).map(LoanFromJSON)),
        'totalCount': json['total_count'],
        'limit': json['limit'],
        'offset': json['offset'],
    };
}

export function LoansResponseToJSON(json: any): LoansResponse {
    return LoansResponseToJSONTyped(json, false);
}

export function LoansResponseToJSONTyped(value?: LoansResponse | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'loans': ((value['loans'] as Array<any>).map(LoanToJSON)),
        'total_count': value['totalCount'],
        'limit': value['limit'],
        'offset': value['offset'],
    };
}

