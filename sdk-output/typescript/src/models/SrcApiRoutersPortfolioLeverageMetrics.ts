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
 * Leverage metrics model.
 * @export
 * @interface SrcApiRoutersPortfolioLeverageMetrics
 */
export interface SrcApiRoutersPortfolioLeverageMetrics {
    /**
     * Total debt outstanding
     * @type {number}
     * @memberof SrcApiRoutersPortfolioLeverageMetrics
     */
    totalDebt: number;
    /**
     * Total available debt capacity
     * @type {number}
     * @memberof SrcApiRoutersPortfolioLeverageMetrics
     */
    totalAvailable: number;
    /**
     * Total interest paid
     * @type {number}
     * @memberof SrcApiRoutersPortfolioLeverageMetrics
     */
    totalInterestPaid: number;
    /**
     * Total commitment fees paid
     * @type {number}
     * @memberof SrcApiRoutersPortfolioLeverageMetrics
     */
    totalCommitmentFeesPaid: number;
    /**
     * Weighted average interest rate
     * @type {number}
     * @memberof SrcApiRoutersPortfolioLeverageMetrics
     */
    weightedAvgInterestRate: number;
    /**
     * Leverage ratio (debt / NAV)
     * @type {number}
     * @memberof SrcApiRoutersPortfolioLeverageMetrics
     */
    leverageRatio: number;
    /**
     * Debt service coverage ratio
     * @type {number}
     * @memberof SrcApiRoutersPortfolioLeverageMetrics
     */
    debtServiceCoverageRatio: number;
    /**
     * Interest coverage ratio
     * @type {number}
     * @memberof SrcApiRoutersPortfolioLeverageMetrics
     */
    interestCoverageRatio: number;
    /**
     * Loan-to-value ratio
     * @type {number}
     * @memberof SrcApiRoutersPortfolioLeverageMetrics
     */
    loanToValueRatio: number;
}

/**
 * Check if a given object implements the SrcApiRoutersPortfolioLeverageMetrics interface.
 */
export function instanceOfSrcApiRoutersPortfolioLeverageMetrics(value: object): value is SrcApiRoutersPortfolioLeverageMetrics {
    if (!('totalDebt' in value) || value['totalDebt'] === undefined) return false;
    if (!('totalAvailable' in value) || value['totalAvailable'] === undefined) return false;
    if (!('totalInterestPaid' in value) || value['totalInterestPaid'] === undefined) return false;
    if (!('totalCommitmentFeesPaid' in value) || value['totalCommitmentFeesPaid'] === undefined) return false;
    if (!('weightedAvgInterestRate' in value) || value['weightedAvgInterestRate'] === undefined) return false;
    if (!('leverageRatio' in value) || value['leverageRatio'] === undefined) return false;
    if (!('debtServiceCoverageRatio' in value) || value['debtServiceCoverageRatio'] === undefined) return false;
    if (!('interestCoverageRatio' in value) || value['interestCoverageRatio'] === undefined) return false;
    if (!('loanToValueRatio' in value) || value['loanToValueRatio'] === undefined) return false;
    return true;
}

export function SrcApiRoutersPortfolioLeverageMetricsFromJSON(json: any): SrcApiRoutersPortfolioLeverageMetrics {
    return SrcApiRoutersPortfolioLeverageMetricsFromJSONTyped(json, false);
}

export function SrcApiRoutersPortfolioLeverageMetricsFromJSONTyped(json: any, ignoreDiscriminator: boolean): SrcApiRoutersPortfolioLeverageMetrics {
    if (json == null) {
        return json;
    }
    return {
        
        'totalDebt': json['total_debt'],
        'totalAvailable': json['total_available'],
        'totalInterestPaid': json['total_interest_paid'],
        'totalCommitmentFeesPaid': json['total_commitment_fees_paid'],
        'weightedAvgInterestRate': json['weighted_avg_interest_rate'],
        'leverageRatio': json['leverage_ratio'],
        'debtServiceCoverageRatio': json['debt_service_coverage_ratio'],
        'interestCoverageRatio': json['interest_coverage_ratio'],
        'loanToValueRatio': json['loan_to_value_ratio'],
    };
}

export function SrcApiRoutersPortfolioLeverageMetricsToJSON(json: any): SrcApiRoutersPortfolioLeverageMetrics {
    return SrcApiRoutersPortfolioLeverageMetricsToJSONTyped(json, false);
}

export function SrcApiRoutersPortfolioLeverageMetricsToJSONTyped(value?: SrcApiRoutersPortfolioLeverageMetrics | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'total_debt': value['totalDebt'],
        'total_available': value['totalAvailable'],
        'total_interest_paid': value['totalInterestPaid'],
        'total_commitment_fees_paid': value['totalCommitmentFeesPaid'],
        'weighted_avg_interest_rate': value['weightedAvgInterestRate'],
        'leverage_ratio': value['leverageRatio'],
        'debt_service_coverage_ratio': value['debtServiceCoverageRatio'],
        'interest_coverage_ratio': value['interestCoverageRatio'],
        'loan_to_value_ratio': value['loanToValueRatio'],
    };
}

