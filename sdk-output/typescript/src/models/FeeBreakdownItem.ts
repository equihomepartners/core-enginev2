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
 * Fee breakdown item model.
 * @export
 * @interface FeeBreakdownItem
 */
export interface FeeBreakdownItem {
    /**
     * Fee category
     * @type {string}
     * @memberof FeeBreakdownItem
     */
    category: string;
    /**
     * Fee amount
     * @type {number}
     * @memberof FeeBreakdownItem
     */
    amount: number;
    /**
     * Percentage of total fees
     * @type {number}
     * @memberof FeeBreakdownItem
     */
    percentage: number;
}

/**
 * Check if a given object implements the FeeBreakdownItem interface.
 */
export function instanceOfFeeBreakdownItem(value: object): value is FeeBreakdownItem {
    if (!('category' in value) || value['category'] === undefined) return false;
    if (!('amount' in value) || value['amount'] === undefined) return false;
    if (!('percentage' in value) || value['percentage'] === undefined) return false;
    return true;
}

export function FeeBreakdownItemFromJSON(json: any): FeeBreakdownItem {
    return FeeBreakdownItemFromJSONTyped(json, false);
}

export function FeeBreakdownItemFromJSONTyped(json: any, ignoreDiscriminator: boolean): FeeBreakdownItem {
    if (json == null) {
        return json;
    }
    return {
        
        'category': json['category'],
        'amount': json['amount'],
        'percentage': json['percentage'],
    };
}

export function FeeBreakdownItemToJSON(json: any): FeeBreakdownItem {
    return FeeBreakdownItemToJSONTyped(json, false);
}

export function FeeBreakdownItemToJSONTyped(value?: FeeBreakdownItem | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'category': value['category'],
        'amount': value['amount'],
        'percentage': value['percentage'],
    };
}

