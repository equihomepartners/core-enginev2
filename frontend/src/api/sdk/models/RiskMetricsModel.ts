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
 * Risk metrics model.
 * @export
 * @interface RiskMetricsModel
 */
export interface RiskMetricsModel {
    /**
     * Value at Risk (95%)
     * @type {number}
     * @memberof RiskMetricsModel
     */
    var95?: number;
    /**
     * Value at Risk (99%)
     * @type {number}
     * @memberof RiskMetricsModel
     */
    var99?: number;
    /**
     * Conditional Value at Risk (95%)
     * @type {number}
     * @memberof RiskMetricsModel
     */
    cvar95?: number;
    /**
     * Conditional Value at Risk (99%)
     * @type {number}
     * @memberof RiskMetricsModel
     */
    cvar99?: number;
    /**
     * Maximum Drawdown
     * @type {number}
     * @memberof RiskMetricsModel
     */
    maxDrawdown?: number;
    /**
     * Volatility (standard deviation of returns)
     * @type {number}
     * @memberof RiskMetricsModel
     */
    volatility?: number;
    /**
     * Downside Deviation
     * @type {number}
     * @memberof RiskMetricsModel
     */
    downsideDeviation?: number;
    /**
     * Tail Risk
     * @type {number}
     * @memberof RiskMetricsModel
     */
    tailRisk?: number;
    /**
     * Tail Probability
     * @type {number}
     * @memberof RiskMetricsModel
     */
    tailProbability?: number;
    /**
     * Tail Severity
     * @type {number}
     * @memberof RiskMetricsModel
     */
    tailSeverity?: number;
}

/**
 * Check if a given object implements the RiskMetricsModel interface.
 */
export function instanceOfRiskMetricsModel(value: object): value is RiskMetricsModel {
    return true;
}

export function RiskMetricsModelFromJSON(json: any): RiskMetricsModel {
    return RiskMetricsModelFromJSONTyped(json, false);
}

export function RiskMetricsModelFromJSONTyped(json: any, ignoreDiscriminator: boolean): RiskMetricsModel {
    if (json == null) {
        return json;
    }
    return {
        
        'var95': json['var_95'] == null ? undefined : json['var_95'],
        'var99': json['var_99'] == null ? undefined : json['var_99'],
        'cvar95': json['cvar_95'] == null ? undefined : json['cvar_95'],
        'cvar99': json['cvar_99'] == null ? undefined : json['cvar_99'],
        'maxDrawdown': json['max_drawdown'] == null ? undefined : json['max_drawdown'],
        'volatility': json['volatility'] == null ? undefined : json['volatility'],
        'downsideDeviation': json['downside_deviation'] == null ? undefined : json['downside_deviation'],
        'tailRisk': json['tail_risk'] == null ? undefined : json['tail_risk'],
        'tailProbability': json['tail_probability'] == null ? undefined : json['tail_probability'],
        'tailSeverity': json['tail_severity'] == null ? undefined : json['tail_severity'],
    };
}

export function RiskMetricsModelToJSON(json: any): RiskMetricsModel {
    return RiskMetricsModelToJSONTyped(json, false);
}

export function RiskMetricsModelToJSONTyped(value?: RiskMetricsModel | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'var_95': value['var95'],
        'var_99': value['var99'],
        'cvar_95': value['cvar95'],
        'cvar_99': value['cvar99'],
        'max_drawdown': value['maxDrawdown'],
        'volatility': value['volatility'],
        'downside_deviation': value['downsideDeviation'],
        'tail_risk': value['tailRisk'],
        'tail_probability': value['tailProbability'],
        'tail_severity': value['tailSeverity'],
    };
}

