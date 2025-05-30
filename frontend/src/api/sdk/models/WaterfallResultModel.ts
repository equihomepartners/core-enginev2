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
import type { WaterfallVisualizationModel } from './WaterfallVisualizationModel';
import {
    WaterfallVisualizationModelFromJSON,
    WaterfallVisualizationModelFromJSONTyped,
    WaterfallVisualizationModelToJSON,
    WaterfallVisualizationModelToJSONTyped,
} from './WaterfallVisualizationModel';
import type { WaterfallDistributionModel } from './WaterfallDistributionModel';
import {
    WaterfallDistributionModelFromJSON,
    WaterfallDistributionModelFromJSONTyped,
    WaterfallDistributionModelToJSON,
    WaterfallDistributionModelToJSONTyped,
} from './WaterfallDistributionModel';

/**
 * Model for waterfall result data.
 * @export
 * @interface WaterfallResultModel
 */
export interface WaterfallResultModel {
    /**
     * Waterfall distribution data
     * @type {WaterfallDistributionModel}
     * @memberof WaterfallResultModel
     */
    distributions: WaterfallDistributionModel;
    /**
     * Clawback amount
     * @type {number}
     * @memberof WaterfallResultModel
     */
    clawbackAmount: number;
    /**
     * Waterfall visualization data
     * @type {WaterfallVisualizationModel}
     * @memberof WaterfallResultModel
     */
    visualization: WaterfallVisualizationModel;
}

/**
 * Check if a given object implements the WaterfallResultModel interface.
 */
export function instanceOfWaterfallResultModel(value: object): value is WaterfallResultModel {
    if (!('distributions' in value) || value['distributions'] === undefined) return false;
    if (!('clawbackAmount' in value) || value['clawbackAmount'] === undefined) return false;
    if (!('visualization' in value) || value['visualization'] === undefined) return false;
    return true;
}

export function WaterfallResultModelFromJSON(json: any): WaterfallResultModel {
    return WaterfallResultModelFromJSONTyped(json, false);
}

export function WaterfallResultModelFromJSONTyped(json: any, ignoreDiscriminator: boolean): WaterfallResultModel {
    if (json == null) {
        return json;
    }
    return {
        
        'distributions': WaterfallDistributionModelFromJSON(json['distributions']),
        'clawbackAmount': json['clawback_amount'],
        'visualization': WaterfallVisualizationModelFromJSON(json['visualization']),
    };
}

export function WaterfallResultModelToJSON(json: any): WaterfallResultModel {
    return WaterfallResultModelToJSONTyped(json, false);
}

export function WaterfallResultModelToJSONTyped(value?: WaterfallResultModel | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'distributions': WaterfallDistributionModelToJSON(value['distributions']),
        'clawback_amount': value['clawbackAmount'],
        'visualization': WaterfallVisualizationModelToJSON(value['visualization']),
    };
}

