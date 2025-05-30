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
 * Loan exit request model.
 * @export
 * @interface LoanExitRequest
 */
export interface LoanExitRequest {
    /**
     * Loan ID
     * @type {string}
     * @memberof LoanExitRequest
     */
    loanId: string;
    /**
     * Property ID
     * @type {string}
     * @memberof LoanExitRequest
     */
    propertyId: string;
    /**
     * Suburb ID (optional)
     * @type {string}
     * @memberof LoanExitRequest
     */
    suburbId?: string;
    /**
     * Zone name
     * @type {string}
     * @memberof LoanExitRequest
     */
    zone: string;
    /**
     * Loan amount
     * @type {number}
     * @memberof LoanExitRequest
     */
    loanAmount: number;
    /**
     * Initial property value
     * @type {number}
     * @memberof LoanExitRequest
     */
    propertyValue: number;
    /**
     * Exit month (0-based)
     * @type {number}
     * @memberof LoanExitRequest
     */
    exitMonth: number;
    /**
     * Exit type (sale, refinance, default, term_completion)
     * @type {string}
     * @memberof LoanExitRequest
     */
    exitType: string;
}

/**
 * Check if a given object implements the LoanExitRequest interface.
 */
export function instanceOfLoanExitRequest(value: object): value is LoanExitRequest {
    if (!('loanId' in value) || value['loanId'] === undefined) return false;
    if (!('propertyId' in value) || value['propertyId'] === undefined) return false;
    if (!('zone' in value) || value['zone'] === undefined) return false;
    if (!('loanAmount' in value) || value['loanAmount'] === undefined) return false;
    if (!('propertyValue' in value) || value['propertyValue'] === undefined) return false;
    if (!('exitMonth' in value) || value['exitMonth'] === undefined) return false;
    if (!('exitType' in value) || value['exitType'] === undefined) return false;
    return true;
}

export function LoanExitRequestFromJSON(json: any): LoanExitRequest {
    return LoanExitRequestFromJSONTyped(json, false);
}

export function LoanExitRequestFromJSONTyped(json: any, ignoreDiscriminator: boolean): LoanExitRequest {
    if (json == null) {
        return json;
    }
    return {
        
        'loanId': json['loan_id'],
        'propertyId': json['property_id'],
        'suburbId': json['suburb_id'] == null ? undefined : json['suburb_id'],
        'zone': json['zone'],
        'loanAmount': json['loan_amount'],
        'propertyValue': json['property_value'],
        'exitMonth': json['exit_month'],
        'exitType': json['exit_type'],
    };
}

export function LoanExitRequestToJSON(json: any): LoanExitRequest {
    return LoanExitRequestToJSONTyped(json, false);
}

export function LoanExitRequestToJSONTyped(value?: LoanExitRequest | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'loan_id': value['loanId'],
        'property_id': value['propertyId'],
        'suburb_id': value['suburbId'],
        'zone': value['zone'],
        'loan_amount': value['loanAmount'],
        'property_value': value['propertyValue'],
        'exit_month': value['exitMonth'],
        'exit_type': value['exitType'],
    };
}

