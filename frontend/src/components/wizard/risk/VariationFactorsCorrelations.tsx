import React from 'react';
import { FormGroup, Intent, Switch, Callout } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface VariationFactorsCorrelationsProps {
  variationFactors: {
    price_path: number;
    default_events: number;
    prepayment_events: number;
    appreciation_rates: number;
  };
  correlationMatrix: {
    price_path_default_events: number;
    price_path_prepayment_events: number;
    default_events_prepayment_events: number;
  };
  deterministicMode: boolean;
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const VariationFactorsCorrelations: React.FC<VariationFactorsCorrelationsProps> = ({
  variationFactors,
  correlationMatrix,
  deterministicMode,
  onChange,
  onBlur,
  errors
}) => {
  const handleChange = (field: string, value: any) => {
    onChange(field, value);
  };

  const handleBlur = (field: string) => {
    onBlur(field);
  };

  return (
    <div className="space-y-6">
      {/* Deterministic Mode Control */}
      <Card
        title="Simulation Mode"
        icon="predictive-analysis"
        subtitle="Control randomness and reproducibility"
      >
        <div className="space-y-4">
          <FormGroup
            label="Deterministic Mode"
            helperText="Enable for reproducible results with fixed random seed"
            inline={true}
          >
            <Switch
              checked={deterministicMode}
              onChange={(e) => handleChange('deterministic_mode', e.target.checked)}
              label="Use deterministic mode"
            />
          </FormGroup>

          {deterministicMode && (
            <Callout intent={Intent.PRIMARY} icon="info-sign">
              <strong>Deterministic Mode Enabled:</strong> All random variations will use a fixed seed for reproducible results. 
              This is useful for testing and comparing scenarios.
            </Callout>
          )}

          {!deterministicMode && (
            <Callout intent={Intent.WARNING} icon="random">
              <strong>Stochastic Mode:</strong> Random variations will be applied to all risk factors. 
              Results will vary between simulation runs.
            </Callout>
          )}
        </div>
      </Card>

      {/* Variation Factors */}
      <Card
        title="Variation Factors"
        icon="variable"
        subtitle="Control the amount of random variation for different risk factors"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Price Path Variation"
              intent={errors['variation_factors.price_path'] ? Intent.DANGER : Intent.NONE}
              helperText="Random variation in property price paths"
            >
              <SimpleNumericInput
                value={variationFactors.price_path}
                onValueChange={(value) => handleChange('variation_factors.price_path', value)}
                onBlur={() => handleBlur('variation_factors.price_path')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['variation_factors.price_path'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Default Events Variation"
              intent={errors['variation_factors.default_events'] ? Intent.DANGER : Intent.NONE}
              helperText="Random variation in default event timing"
            >
              <SimpleNumericInput
                value={variationFactors.default_events}
                onValueChange={(value) => handleChange('variation_factors.default_events', value)}
                onBlur={() => handleBlur('variation_factors.default_events')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['variation_factors.default_events'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Prepayment Events Variation"
              intent={errors['variation_factors.prepayment_events'] ? Intent.DANGER : Intent.NONE}
              helperText="Random variation in prepayment event timing"
            >
              <SimpleNumericInput
                value={variationFactors.prepayment_events}
                onValueChange={(value) => handleChange('variation_factors.prepayment_events', value)}
                onBlur={() => handleBlur('variation_factors.prepayment_events')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['variation_factors.prepayment_events'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Appreciation Rates Variation"
              intent={errors['variation_factors.appreciation_rates'] ? Intent.DANGER : Intent.NONE}
              helperText="Random variation in appreciation rates"
            >
              <SimpleNumericInput
                value={variationFactors.appreciation_rates}
                onValueChange={(value) => handleChange('variation_factors.appreciation_rates', value)}
                onBlur={() => handleBlur('variation_factors.appreciation_rates')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['variation_factors.appreciation_rates'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>

          {/* Variation Factors Summary */}
          <div className="bg-blue-50 p-3 rounded-md text-sm">
            <h5 className="font-medium mb-2">Variation Impact Summary</h5>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
              <div>
                <div className="text-gray-600">Price Paths</div>
                <div className="font-medium">{formatPercentage(variationFactors.price_path)} variation</div>
              </div>
              <div>
                <div className="text-gray-600">Default Events</div>
                <div className="font-medium">{formatPercentage(variationFactors.default_events)} variation</div>
              </div>
              <div>
                <div className="text-gray-600">Prepayments</div>
                <div className="font-medium">{formatPercentage(variationFactors.prepayment_events)} variation</div>
              </div>
              <div>
                <div className="text-gray-600">Appreciation</div>
                <div className="font-medium">{formatPercentage(variationFactors.appreciation_rates)} variation</div>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Correlation Matrix */}
      <Card
        title="Global Correlation Matrix"
        icon="graph"
        subtitle="Cross-correlations between major risk factors"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormGroup
              label="Price Path ↔ Default Events"
              intent={errors['correlation_matrix.price_path_default_events'] ? Intent.DANGER : Intent.NONE}
              helperText="Correlation between price changes and defaults (typically negative)"
            >
              <SimpleNumericInput
                value={correlationMatrix.price_path_default_events}
                onValueChange={(value) => handleChange('correlation_matrix.price_path_default_events', value)}
                onBlur={() => handleBlur('correlation_matrix.price_path_default_events')}
                min={-1}
                max={1}
                step={0.01}
                formatter={value => `${(value >= 0 ? '+' : '')}${(value * 100).toFixed(0)}%`}
                intent={errors['correlation_matrix.price_path_default_events'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Price Path ↔ Prepayments"
              intent={errors['correlation_matrix.price_path_prepayment_events'] ? Intent.DANGER : Intent.NONE}
              helperText="Correlation between price changes and prepayments (typically positive)"
            >
              <SimpleNumericInput
                value={correlationMatrix.price_path_prepayment_events}
                onValueChange={(value) => handleChange('correlation_matrix.price_path_prepayment_events', value)}
                onBlur={() => handleBlur('correlation_matrix.price_path_prepayment_events')}
                min={-1}
                max={1}
                step={0.01}
                formatter={value => `${(value >= 0 ? '+' : '')}${(value * 100).toFixed(0)}%`}
                intent={errors['correlation_matrix.price_path_prepayment_events'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Defaults ↔ Prepayments"
              intent={errors['correlation_matrix.default_events_prepayment_events'] ? Intent.DANGER : Intent.NONE}
              helperText="Correlation between defaults and prepayments (typically negative)"
            >
              <SimpleNumericInput
                value={correlationMatrix.default_events_prepayment_events}
                onValueChange={(value) => handleChange('correlation_matrix.default_events_prepayment_events', value)}
                onBlur={() => handleBlur('correlation_matrix.default_events_prepayment_events')}
                min={-1}
                max={1}
                step={0.01}
                formatter={value => `${(value >= 0 ? '+' : '')}${(value * 100).toFixed(0)}%`}
                intent={errors['correlation_matrix.default_events_prepayment_events'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>

          {/* Correlation Matrix Visualization */}
          <div className="bg-gray-50 p-3 rounded-md text-sm">
            <h5 className="font-medium mb-2">Correlation Matrix</h5>
            <div className="grid grid-cols-3 gap-2 text-xs">
              <div className="text-center font-medium">Price ↔ Defaults</div>
              <div className="text-center font-medium">Price ↔ Prepayments</div>
              <div className="text-center font-medium">Defaults ↔ Prepayments</div>
              
              <div className={`text-center p-2 rounded ${correlationMatrix.price_path_default_events < 0 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                {(correlationMatrix.price_path_default_events >= 0 ? '+' : '')}{(correlationMatrix.price_path_default_events * 100).toFixed(0)}%
              </div>
              <div className={`text-center p-2 rounded ${correlationMatrix.price_path_prepayment_events < 0 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                {(correlationMatrix.price_path_prepayment_events >= 0 ? '+' : '')}{(correlationMatrix.price_path_prepayment_events * 100).toFixed(0)}%
              </div>
              <div className={`text-center p-2 rounded ${correlationMatrix.default_events_prepayment_events < 0 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                {(correlationMatrix.default_events_prepayment_events >= 0 ? '+' : '')}{(correlationMatrix.default_events_prepayment_events * 100).toFixed(0)}%
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Help Information */}
      <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Variation & Correlation Information</h4>
        <p>Configure randomness and cross-correlations in the simulation:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Deterministic Mode:</strong> Use fixed random seed for reproducible results</li>
          <li><strong>Variation Factors:</strong> Control how much randomness is applied to each risk factor</li>
          <li><strong>Correlation Matrix:</strong> Define how different risk factors move together</li>
          <li><strong>Typical Correlations:</strong> Price↔Defaults (negative), Price↔Prepayments (positive)</li>
        </ul>
      </div>
    </div>
  );
};

export default VariationFactorsCorrelations;
