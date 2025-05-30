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
import type { DistributionByYearModel } from './DistributionByYearModel';
import {
    DistributionByYearModelFromJSON,
    DistributionByYearModelFromJSONTyped,
    DistributionByYearModelToJSON,
    DistributionByYearModelToJSONTyped,
} from './DistributionByYearModel';
import type { StakeholderAllocationModel } from './StakeholderAllocationModel';
import {
    StakeholderAllocationModelFromJSON,
    StakeholderAllocationModelFromJSONTyped,
    StakeholderAllocationModelToJSON,
    StakeholderAllocationModelToJSONTyped,
} from './StakeholderAllocationModel';
import type { WaterfallChartModel } from './WaterfallChartModel';
import {
    WaterfallChartModelFromJSON,
    WaterfallChartModelFromJSONTyped,
    WaterfallChartModelToJSON,
    WaterfallChartModelToJSONTyped,
} from './WaterfallChartModel';
import type { WaterfallTierModel } from './WaterfallTierModel';
import {
    WaterfallTierModelFromJSON,
    WaterfallTierModelFromJSONTyped,
    WaterfallTierModelToJSON,
    WaterfallTierModelToJSONTyped,
} from './WaterfallTierModel';

/**
 * Model for waterfall visualization data.
 * @export
 * @interface WaterfallVisualizationModel
 */
export interface WaterfallVisualizationModel {
    /**
     * Waterfall chart data
     * @type {Array<WaterfallChartModel>}
     * @memberof WaterfallVisualizationModel
     */
    waterfallChart: Array<WaterfallChartModel>;
    /**
     * Distribution by year chart data
     * @type {Array<DistributionByYearModel>}
     * @memberof WaterfallVisualizationModel
     */
    distributionByYearChart: Array<DistributionByYearModel>;
    /**
     * Tier allocation chart data
     * @type {Array<WaterfallTierModel>}
     * @memberof WaterfallVisualizationModel
     */
    tierAllocationChart: Array<WaterfallTierModel>;
    /**
     * Stakeholder allocation chart data
     * @type {Array<StakeholderAllocationModel>}
     * @memberof WaterfallVisualizationModel
     */
    stakeholderAllocationChart: Array<StakeholderAllocationModel>;
}

/**
 * Check if a given object implements the WaterfallVisualizationModel interface.
 */
export function instanceOfWaterfallVisualizationModel(value: object): value is WaterfallVisualizationModel {
    if (!('waterfallChart' in value) || value['waterfallChart'] === undefined) return false;
    if (!('distributionByYearChart' in value) || value['distributionByYearChart'] === undefined) return false;
    if (!('tierAllocationChart' in value) || value['tierAllocationChart'] === undefined) return false;
    if (!('stakeholderAllocationChart' in value) || value['stakeholderAllocationChart'] === undefined) return false;
    return true;
}

export function WaterfallVisualizationModelFromJSON(json: any): WaterfallVisualizationModel {
    return WaterfallVisualizationModelFromJSONTyped(json, false);
}

export function WaterfallVisualizationModelFromJSONTyped(json: any, ignoreDiscriminator: boolean): WaterfallVisualizationModel {
    if (json == null) {
        return json;
    }
    return {
        
        'waterfallChart': ((json['waterfall_chart'] as Array<any>).map(WaterfallChartModelFromJSON)),
        'distributionByYearChart': ((json['distribution_by_year_chart'] as Array<any>).map(DistributionByYearModelFromJSON)),
        'tierAllocationChart': ((json['tier_allocation_chart'] as Array<any>).map(WaterfallTierModelFromJSON)),
        'stakeholderAllocationChart': ((json['stakeholder_allocation_chart'] as Array<any>).map(StakeholderAllocationModelFromJSON)),
    };
}

export function WaterfallVisualizationModelToJSON(json: any): WaterfallVisualizationModel {
    return WaterfallVisualizationModelToJSONTyped(json, false);
}

export function WaterfallVisualizationModelToJSONTyped(value?: WaterfallVisualizationModel | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'waterfall_chart': ((value['waterfallChart'] as Array<any>).map(WaterfallChartModelToJSON)),
        'distribution_by_year_chart': ((value['distributionByYearChart'] as Array<any>).map(DistributionByYearModelToJSON)),
        'tier_allocation_chart': ((value['tierAllocationChart'] as Array<any>).map(WaterfallTierModelToJSON)),
        'stakeholder_allocation_chart': ((value['stakeholderAllocationChart'] as Array<any>).map(StakeholderAllocationModelToJSON)),
    };
}

