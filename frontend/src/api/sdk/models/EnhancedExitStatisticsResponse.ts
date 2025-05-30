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
 * Enhanced exit statistics response model.
 * @export
 * @interface EnhancedExitStatisticsResponse
 */
export interface EnhancedExitStatisticsResponse {
    /**
     * Average exit year
     * @type {number}
     * @memberof EnhancedExitStatisticsResponse
     */
    avgExitYear: number;
    /**
     * Average ROI
     * @type {number}
     * @memberof EnhancedExitStatisticsResponse
     */
    avgRoi: number;
    /**
     * Average annualized ROI
     * @type {number}
     * @memberof EnhancedExitStatisticsResponse
     */
    avgAnnualizedRoi: number;
    /**
     * Exit type distribution
     * @type {{ [key: string]: number; }}
     * @memberof EnhancedExitStatisticsResponse
     */
    exitTypeDistribution: { [key: string]: number; };
    /**
     * Exit timing distribution
     * @type {{ [key: string]: number; }}
     * @memberof EnhancedExitStatisticsResponse
     */
    exitTimingDistribution: { [key: string]: number; };
    /**
     * Exit ROI distribution
     * @type {{ [key: string]: number; }}
     * @memberof EnhancedExitStatisticsResponse
     */
    exitRoiDistribution: { [key: string]: number; };
    /**
     * Exit type ROI
     * @type {{ [key: string]: object; }}
     * @memberof EnhancedExitStatisticsResponse
     */
    exitTypeRoi: { [key: string]: object; };
    /**
     * Total exit value
     * @type {number}
     * @memberof EnhancedExitStatisticsResponse
     */
    exitValueTotal: number;
    /**
     * Total appreciation share
     * @type {number}
     * @memberof EnhancedExitStatisticsResponse
     */
    appreciationShareTotal: number;
    /**
     * Total return
     * @type {number}
     * @memberof EnhancedExitStatisticsResponse
     */
    totalReturn: number;
    /**
     * Total ROI
     * @type {number}
     * @memberof EnhancedExitStatisticsResponse
     */
    totalRoi: number;
    /**
     * Annualized ROI
     * @type {number}
     * @memberof EnhancedExitStatisticsResponse
     */
    annualizedRoi: number;
    /**
     * Comparison to base exit statistics
     * @type {object}
     * @memberof EnhancedExitStatisticsResponse
     */
    comparisonToBase?: object;
    /**
     * Cohort analysis
     * @type {object}
     * @memberof EnhancedExitStatisticsResponse
     */
    cohortAnalysis?: object;
    /**
     * Cohort analysis summary
     * @type {object}
     * @memberof EnhancedExitStatisticsResponse
     */
    cohortAnalysisSummary?: object;
    /**
     * Risk metrics
     * @type {object}
     * @memberof EnhancedExitStatisticsResponse
     */
    riskMetrics?: object;
    /**
     * Machine learning insights
     * @type {object}
     * @memberof EnhancedExitStatisticsResponse
     */
    mlInsights?: object;
}

/**
 * Check if a given object implements the EnhancedExitStatisticsResponse interface.
 */
export function instanceOfEnhancedExitStatisticsResponse(value: object): value is EnhancedExitStatisticsResponse {
    if (!('avgExitYear' in value) || value['avgExitYear'] === undefined) return false;
    if (!('avgRoi' in value) || value['avgRoi'] === undefined) return false;
    if (!('avgAnnualizedRoi' in value) || value['avgAnnualizedRoi'] === undefined) return false;
    if (!('exitTypeDistribution' in value) || value['exitTypeDistribution'] === undefined) return false;
    if (!('exitTimingDistribution' in value) || value['exitTimingDistribution'] === undefined) return false;
    if (!('exitRoiDistribution' in value) || value['exitRoiDistribution'] === undefined) return false;
    if (!('exitTypeRoi' in value) || value['exitTypeRoi'] === undefined) return false;
    if (!('exitValueTotal' in value) || value['exitValueTotal'] === undefined) return false;
    if (!('appreciationShareTotal' in value) || value['appreciationShareTotal'] === undefined) return false;
    if (!('totalReturn' in value) || value['totalReturn'] === undefined) return false;
    if (!('totalRoi' in value) || value['totalRoi'] === undefined) return false;
    if (!('annualizedRoi' in value) || value['annualizedRoi'] === undefined) return false;
    return true;
}

export function EnhancedExitStatisticsResponseFromJSON(json: any): EnhancedExitStatisticsResponse {
    return EnhancedExitStatisticsResponseFromJSONTyped(json, false);
}

export function EnhancedExitStatisticsResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): EnhancedExitStatisticsResponse {
    if (json == null) {
        return json;
    }
    return {
        
        'avgExitYear': json['avg_exit_year'],
        'avgRoi': json['avg_roi'],
        'avgAnnualizedRoi': json['avg_annualized_roi'],
        'exitTypeDistribution': json['exit_type_distribution'],
        'exitTimingDistribution': json['exit_timing_distribution'],
        'exitRoiDistribution': json['exit_roi_distribution'],
        'exitTypeRoi': json['exit_type_roi'],
        'exitValueTotal': json['exit_value_total'],
        'appreciationShareTotal': json['appreciation_share_total'],
        'totalReturn': json['total_return'],
        'totalRoi': json['total_roi'],
        'annualizedRoi': json['annualized_roi'],
        'comparisonToBase': json['comparison_to_base'] == null ? undefined : json['comparison_to_base'],
        'cohortAnalysis': json['cohort_analysis'] == null ? undefined : json['cohort_analysis'],
        'cohortAnalysisSummary': json['cohort_analysis_summary'] == null ? undefined : json['cohort_analysis_summary'],
        'riskMetrics': json['risk_metrics'] == null ? undefined : json['risk_metrics'],
        'mlInsights': json['ml_insights'] == null ? undefined : json['ml_insights'],
    };
}

export function EnhancedExitStatisticsResponseToJSON(json: any): EnhancedExitStatisticsResponse {
    return EnhancedExitStatisticsResponseToJSONTyped(json, false);
}

export function EnhancedExitStatisticsResponseToJSONTyped(value?: EnhancedExitStatisticsResponse | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'avg_exit_year': value['avgExitYear'],
        'avg_roi': value['avgRoi'],
        'avg_annualized_roi': value['avgAnnualizedRoi'],
        'exit_type_distribution': value['exitTypeDistribution'],
        'exit_timing_distribution': value['exitTimingDistribution'],
        'exit_roi_distribution': value['exitRoiDistribution'],
        'exit_type_roi': value['exitTypeRoi'],
        'exit_value_total': value['exitValueTotal'],
        'appreciation_share_total': value['appreciationShareTotal'],
        'total_return': value['totalReturn'],
        'total_roi': value['totalRoi'],
        'annualized_roi': value['annualizedRoi'],
        'comparison_to_base': value['comparisonToBase'],
        'cohort_analysis': value['cohortAnalysis'],
        'cohort_analysis_summary': value['cohortAnalysisSummary'],
        'risk_metrics': value['riskMetrics'],
        'ml_insights': value['mlInsights'],
    };
}

