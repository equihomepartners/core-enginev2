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
import type { ParameterVariation } from './ParameterVariation';
import {
    ParameterVariationFromJSON,
    ParameterVariationFromJSONTyped,
    ParameterVariationToJSON,
    ParameterVariationToJSONTyped,
} from './ParameterVariation';
import type { TornadoChartItem } from './TornadoChartItem';
import {
    TornadoChartItemFromJSON,
    TornadoChartItemFromJSONTyped,
    TornadoChartItemToJSON,
    TornadoChartItemToJSONTyped,
} from './TornadoChartItem';

/**
 * Sensitivity analysis model.
 * @export
 * @interface SensitivityAnalysis
 */
export interface SensitivityAnalysis {
    /**
     * Parameter variations
     * @type {Array<ParameterVariation>}
     * @memberof SensitivityAnalysis
     */
    parameterVariations: Array<ParameterVariation>;
    /**
     * Tornado chart data
     * @type {Array<TornadoChartItem>}
     * @memberof SensitivityAnalysis
     */
    tornadoChart: Array<TornadoChartItem>;
}

/**
 * Check if a given object implements the SensitivityAnalysis interface.
 */
export function instanceOfSensitivityAnalysis(value: object): value is SensitivityAnalysis {
    if (!('parameterVariations' in value) || value['parameterVariations'] === undefined) return false;
    if (!('tornadoChart' in value) || value['tornadoChart'] === undefined) return false;
    return true;
}

export function SensitivityAnalysisFromJSON(json: any): SensitivityAnalysis {
    return SensitivityAnalysisFromJSONTyped(json, false);
}

export function SensitivityAnalysisFromJSONTyped(json: any, ignoreDiscriminator: boolean): SensitivityAnalysis {
    if (json == null) {
        return json;
    }
    return {
        
        'parameterVariations': ((json['parameter_variations'] as Array<any>).map(ParameterVariationFromJSON)),
        'tornadoChart': ((json['tornado_chart'] as Array<any>).map(TornadoChartItemFromJSON)),
    };
}

export function SensitivityAnalysisToJSON(json: any): SensitivityAnalysis {
    return SensitivityAnalysisToJSONTyped(json, false);
}

export function SensitivityAnalysisToJSONTyped(value?: SensitivityAnalysis | null, ignoreDiscriminator: boolean = false): any {
    if (value == null) {
        return value;
    }

    return {
        
        'parameter_variations': ((value['parameterVariations'] as Array<any>).map(ParameterVariationToJSON)),
        'tornado_chart': ((value['tornadoChart'] as Array<any>).map(TornadoChartItemToJSON)),
    };
}

