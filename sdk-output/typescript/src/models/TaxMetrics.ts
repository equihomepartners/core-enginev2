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
 * Tax metrics model.
 * @export
 * @interface TaxMetrics
 */
export interface TaxMetrics {
    /**
     * Pre-tax IRR
     * @type {number}
     * @memberof TaxMetrics
     */
    preTaxIrr: number;
    /**
     * Post-tax IRR
     * @type {number}
     * @memberof TaxMetrics
     */
    postTaxIrr: number;
    /**
     * Pre-tax NPV
     * @type {number}
     * @memberof TaxMetrics
     */
    preTaxNpv: number;
    /**
     * Post-tax NPV
     * @type {number}
     * @memberof TaxMetrics
     */
    postTaxNpv: number;
    /**
     * Total tax amount
     * @type {number}
     * @memberof TaxMetrics
     */
    totalTaxAmount: number;
    /**
     * Effective tax rate
     * @type {number}
     * @memberof TaxMetrics
     */
    effectiveTaxRate: number;
}

/**
 * Check if a given object implements the TaxMetrics interface.
 */
export function instanceOfTaxMetrics(value: object): value is TaxMetrics {
    if (!('preTaxIrr' in value) || value['preTaxIrr'] === undefined) return false;
    if (!('postTaxIrr' in value) || value['postTaxIrr'] === undefined) return false;
    if (!('preTaxNpv' in value) || value['preTaxNpv'] === undefined) return false;
    if (!('postTaxNpv' in value) || value['postTaxNpv'] === undefined) return false;
    if (!('totalTaxAmount' in value) || value['totalTaxAmount'] === undefined) return false;
    if (!('effectiveTaxRate' in value) || value['effectiveTaxRate'] === undefined) return false;
    return true;
}

export function TaxMetricsFromJSON(json: any): TaxMetrics {
    return TaxMetricsFromJSONTyped(json, false);
}

export function TaxMetricsFromJSONTyped(json: any, ignoreDiscriminator: boolean): TaxMetrics {
    if (json == null) {
        return json;
    }
    return {
        
        'preTaxIrr': json['pre_tax_irr'],
        'postTaxIrr': json['post_tax_irr'],
        'preTaxNpv': json['pre_tax_npv'],
        'postTaxNpv': json['post_tax_npv'],
        'totalTaxAmount': json['total_tax_amount'],
        'effectiveTaxRate': json['effective_tax_rate'],
    };
}

export function TaxMetricsToJSON(json: any): TaxMetrics {
    return TaxMetricsToJSONTyped(json, false);
}

export function TaxMetricsToJSONTyped(value?: TaxMetrics | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'pre_tax_irr': value['preTaxIrr'],
        'post_tax_irr': value['postTaxIrr'],
        'pre_tax_npv': value['preTaxNpv'],
        'post_tax_npv': value['postTaxNpv'],
        'total_tax_amount': value['totalTaxAmount'],
        'effective_tax_rate': value['effectiveTaxRate'],
    };
}

