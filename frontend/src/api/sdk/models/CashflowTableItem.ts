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
 * Cashflow table item model.
 * @export
 * @interface CashflowTableItem
 */
export interface CashflowTableItem {
    /**
     * Year
     * @type {number}
     * @memberof CashflowTableItem
     */
    year: number;
    /**
     * Capital calls
     * @type {number}
     * @memberof CashflowTableItem
     */
    capitalCalls: number;
    /**
     * Loan investments
     * @type {number}
     * @memberof CashflowTableItem
     */
    loanInvestments: number;
    /**
     * Origination fees
     * @type {number}
     * @memberof CashflowTableItem
     */
    originationFees: number;
    /**
     * Principal repayments
     * @type {number}
     * @memberof CashflowTableItem
     */
    principalRepayments: number;
    /**
     * Interest income
     * @type {number}
     * @memberof CashflowTableItem
     */
    interestIncome: number;
    /**
     * Appreciation share
     * @type {number}
     * @memberof CashflowTableItem
     */
    appreciationShare: number;
    /**
     * Management fees
     * @type {number}
     * @memberof CashflowTableItem
     */
    managementFees: number;
    /**
     * Fund expenses
     * @type {number}
     * @memberof CashflowTableItem
     */
    fundExpenses: number;
    /**
     * Distributions
     * @type {number}
     * @memberof CashflowTableItem
     */
    distributions: number;
    /**
     * Net cashflow
     * @type {number}
     * @memberof CashflowTableItem
     */
    netCashflow: number;
    /**
     * Cumulative cashflow
     * @type {number}
     * @memberof CashflowTableItem
     */
    cumulativeCashflow: number;
}

/**
 * Check if a given object implements the CashflowTableItem interface.
 */
export function instanceOfCashflowTableItem(value: object): value is CashflowTableItem {
    if (!('year' in value) || value['year'] === undefined) return false;
    if (!('capitalCalls' in value) || value['capitalCalls'] === undefined) return false;
    if (!('loanInvestments' in value) || value['loanInvestments'] === undefined) return false;
    if (!('originationFees' in value) || value['originationFees'] === undefined) return false;
    if (!('principalRepayments' in value) || value['principalRepayments'] === undefined) return false;
    if (!('interestIncome' in value) || value['interestIncome'] === undefined) return false;
    if (!('appreciationShare' in value) || value['appreciationShare'] === undefined) return false;
    if (!('managementFees' in value) || value['managementFees'] === undefined) return false;
    if (!('fundExpenses' in value) || value['fundExpenses'] === undefined) return false;
    if (!('distributions' in value) || value['distributions'] === undefined) return false;
    if (!('netCashflow' in value) || value['netCashflow'] === undefined) return false;
    if (!('cumulativeCashflow' in value) || value['cumulativeCashflow'] === undefined) return false;
    return true;
}

export function CashflowTableItemFromJSON(json: any): CashflowTableItem {
    return CashflowTableItemFromJSONTyped(json, false);
}

export function CashflowTableItemFromJSONTyped(json: any, ignoreDiscriminator: boolean): CashflowTableItem {
    if (json == null) {
        return json;
    }
    return {
        
        'year': json['year'],
        'capitalCalls': json['capital_calls'],
        'loanInvestments': json['loan_investments'],
        'originationFees': json['origination_fees'],
        'principalRepayments': json['principal_repayments'],
        'interestIncome': json['interest_income'],
        'appreciationShare': json['appreciation_share'],
        'managementFees': json['management_fees'],
        'fundExpenses': json['fund_expenses'],
        'distributions': json['distributions'],
        'netCashflow': json['net_cashflow'],
        'cumulativeCashflow': json['cumulative_cashflow'],
    };
}

export function CashflowTableItemToJSON(json: any): CashflowTableItem {
    return CashflowTableItemToJSONTyped(json, false);
}

export function CashflowTableItemToJSONTyped(value?: CashflowTableItem | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'year': value['year'],
        'capital_calls': value['capitalCalls'],
        'loan_investments': value['loanInvestments'],
        'origination_fees': value['originationFees'],
        'principal_repayments': value['principalRepayments'],
        'interest_income': value['interestIncome'],
        'appreciation_share': value['appreciationShare'],
        'management_fees': value['managementFees'],
        'fund_expenses': value['fundExpenses'],
        'distributions': value['distributions'],
        'net_cashflow': value['netCashflow'],
        'cumulative_cashflow': value['cumulativeCashflow'],
    };
}

