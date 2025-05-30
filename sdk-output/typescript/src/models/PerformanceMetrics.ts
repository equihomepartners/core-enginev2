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
 * Performance/return-risk metrics model.
 * @export
 * @interface PerformanceMetrics
 */
export interface PerformanceMetrics {
    /**
     * Net-IRR point value
     * @type {number}
     * @memberof PerformanceMetrics
     */
    netIrr?: number;
    /**
     * Sharpe ratio
     * @type {number}
     * @memberof PerformanceMetrics
     */
    sharpeRatio?: number;
    /**
     * Sortino ratio
     * @type {number}
     * @memberof PerformanceMetrics
     */
    sortinoRatio?: number;
    /**
     * Hurdle-clear probability
     * @type {object}
     * @memberof PerformanceMetrics
     */
    hurdleClearProbability: object;
    /**
     * Calmar ratio
     * @type {number}
     * @memberof PerformanceMetrics
     */
    calmarRatio?: number;
    /**
     * Information ratio
     * @type {number}
     * @memberof PerformanceMetrics
     */
    informationRatio?: number;
    /**
     * Treynor ratio
     * @type {number}
     * @memberof PerformanceMetrics
     */
    treynorRatio?: number;
    /**
     * Omega ratio
     * @type {number}
     * @memberof PerformanceMetrics
     */
    omegaRatio?: number;
    /**
     * Kappa ratio
     * @type {number}
     * @memberof PerformanceMetrics
     */
    kappaRatio?: number;
    /**
     * Gain-Loss ratio
     * @type {number}
     * @memberof PerformanceMetrics
     */
    gainLossRatio?: number;
}

/**
 * Check if a given object implements the PerformanceMetrics interface.
 */
export function instanceOfPerformanceMetrics(value: object): value is PerformanceMetrics {
    if (!('hurdleClearProbability' in value) || value['hurdleClearProbability'] === undefined) return false;
    return true;
}

export function PerformanceMetricsFromJSON(json: any): PerformanceMetrics {
    return PerformanceMetricsFromJSONTyped(json, false);
}

export function PerformanceMetricsFromJSONTyped(json: any, ignoreDiscriminator: boolean): PerformanceMetrics {
    if (json == null) {
        return json;
    }
    return {
        
        'netIrr': json['net_irr'] == null ? undefined : json['net_irr'],
        'sharpeRatio': json['sharpe_ratio'] == null ? undefined : json['sharpe_ratio'],
        'sortinoRatio': json['sortino_ratio'] == null ? undefined : json['sortino_ratio'],
        'hurdleClearProbability': json['hurdle_clear_probability'],
        'calmarRatio': json['calmar_ratio'] == null ? undefined : json['calmar_ratio'],
        'informationRatio': json['information_ratio'] == null ? undefined : json['information_ratio'],
        'treynorRatio': json['treynor_ratio'] == null ? undefined : json['treynor_ratio'],
        'omegaRatio': json['omega_ratio'] == null ? undefined : json['omega_ratio'],
        'kappaRatio': json['kappa_ratio'] == null ? undefined : json['kappa_ratio'],
        'gainLossRatio': json['gain_loss_ratio'] == null ? undefined : json['gain_loss_ratio'],
    };
}

export function PerformanceMetricsToJSON(json: any): PerformanceMetrics {
    return PerformanceMetricsToJSONTyped(json, false);
}

export function PerformanceMetricsToJSONTyped(value?: PerformanceMetrics | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'net_irr': value['netIrr'],
        'sharpe_ratio': value['sharpeRatio'],
        'sortino_ratio': value['sortinoRatio'],
        'hurdle_clear_probability': value['hurdleClearProbability'],
        'calmar_ratio': value['calmarRatio'],
        'information_ratio': value['informationRatio'],
        'treynor_ratio': value['treynorRatio'],
        'omega_ratio': value['omegaRatio'],
        'kappa_ratio': value['kappaRatio'],
        'gain_loss_ratio': value['gainLossRatio'],
    };
}

