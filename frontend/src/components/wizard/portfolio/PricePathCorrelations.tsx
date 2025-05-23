import React from 'react';
import { FormGroup, Intent, HTMLSelect, Slider } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface PricePathCorrelationsProps {
  pricePath: {
    model_type: string;
    volatility: {
      green: number;
      orange: number;
      red: number;
    };
    correlation_matrix: {
      green_orange: number;
      green_red: number;
      orange_red: number;
    };
    mean_reversion_params: {
      speed: number;
      long_term_mean: number;
    };
    regime_switching_params: {
      bull_market_rate: number;
      bear_market_rate: number;
      bull_to_bear_prob: number;
      bear_to_bull_prob: number;
    };
    time_step: string;
    suburb_variation: number;
    property_variation: number;
    cycle_position: number;
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const PricePathCorrelations: React.FC<PricePathCorrelationsProps> = ({
  pricePath,
  onChange,
  onBlur,
  errors
}) => {
  const handleChange = (field: string, value: any) => {
    onChange(`price_path.${field}`, value);
  };

  const handleBlur = (field: string) => {
    onBlur(`price_path.${field}`);
  };

  const handleNestedChange = (field: string, value: any) => {
    onChange(`price_path.${field}`, value);
  };

  return (
    <Card
      title="Price Path & Correlations"
      icon="trending-up"
      subtitle="Configure price simulation models and correlations"
    >
      <div className="space-y-6">
        {/* Model Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormGroup
            label="Price Model Type"
            intent={errors['price_path.model_type'] ? Intent.DANGER : Intent.NONE}
            helperText={errors['price_path.model_type'] || "Type of stochastic model to use"}
          >
            <HTMLSelect
              value={pricePath.model_type}
              onChange={(e) => handleChange('model_type', e.target.value)}
              onBlur={() => handleBlur('model_type')}
              fill={true}
            >
              <option value="gbm">Geometric Brownian Motion</option>
              <option value="mean_reversion">Mean Reversion</option>
              <option value="regime_switching">Regime Switching</option>
            </HTMLSelect>
          </FormGroup>

          <FormGroup
            label="Time Step"
            intent={errors['price_path.time_step'] ? Intent.DANGER : Intent.NONE}
            helperText={errors['price_path.time_step'] || "Time step for price simulation"}
          >
            <HTMLSelect
              value={pricePath.time_step}
              onChange={(e) => handleChange('time_step', e.target.value)}
              onBlur={() => handleBlur('time_step')}
              fill={true}
            >
              <option value="monthly">Monthly</option>
              <option value="quarterly">Quarterly</option>
              <option value="yearly">Yearly</option>
            </HTMLSelect>
          </FormGroup>
        </div>

        {/* Zone Volatility */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Zone-Specific Volatility</h4>
          <div className="grid grid-cols-3 gap-4">
            <FormGroup
              label="Green Zone Volatility"
              intent={errors['price_path.volatility.green'] ? Intent.DANGER : Intent.NONE}
              helperText="Price volatility for green zone"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={0.2}
                  stepSize={0.005}
                  labelStepSize={0.05}
                  value={pricePath.volatility.green}
                  onChange={(value) => handleNestedChange('volatility.green', value)}
                  onRelease={() => onBlur('price_path.volatility.green')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['price_path.volatility.green'] ? Intent.DANGER : Intent.SUCCESS}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {formatPercentage(pricePath.volatility.green)}
                </div>
              </div>
            </FormGroup>

            <FormGroup
              label="Orange Zone Volatility"
              intent={errors['price_path.volatility.orange'] ? Intent.DANGER : Intent.NONE}
              helperText="Price volatility for orange zone"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={0.2}
                  stepSize={0.005}
                  labelStepSize={0.05}
                  value={pricePath.volatility.orange}
                  onChange={(value) => handleNestedChange('volatility.orange', value)}
                  onRelease={() => onBlur('price_path.volatility.orange')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['price_path.volatility.orange'] ? Intent.DANGER : Intent.WARNING}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {formatPercentage(pricePath.volatility.orange)}
                </div>
              </div>
            </FormGroup>

            <FormGroup
              label="Red Zone Volatility"
              intent={errors['price_path.volatility.red'] ? Intent.DANGER : Intent.NONE}
              helperText="Price volatility for red zone"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={0.2}
                  stepSize={0.005}
                  labelStepSize={0.05}
                  value={pricePath.volatility.red}
                  onChange={(value) => handleNestedChange('volatility.red', value)}
                  onRelease={() => onBlur('price_path.volatility.red')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['price_path.volatility.red'] ? Intent.DANGER : Intent.DANGER}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {formatPercentage(pricePath.volatility.red)}
                </div>
              </div>
            </FormGroup>
          </div>
        </div>

        {/* Correlation Matrix */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Zone Correlation Matrix</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormGroup
              label="Green ↔ Orange"
              intent={errors['price_path.correlation_matrix.green_orange'] ? Intent.DANGER : Intent.NONE}
              helperText="Correlation between green and orange zones"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={-1}
                  max={1}
                  stepSize={0.05}
                  labelStepSize={0.5}
                  value={pricePath.correlation_matrix.green_orange}
                  onChange={(value) => handleNestedChange('correlation_matrix.green_orange', value)}
                  onRelease={() => onBlur('price_path.correlation_matrix.green_orange')}
                  labelRenderer={value => value.toFixed(2)}
                  intent={errors['price_path.correlation_matrix.green_orange'] ? Intent.DANGER : Intent.PRIMARY}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {pricePath.correlation_matrix.green_orange.toFixed(2)}
                </div>
              </div>
            </FormGroup>

            <FormGroup
              label="Green ↔ Red"
              intent={errors['price_path.correlation_matrix.green_red'] ? Intent.DANGER : Intent.NONE}
              helperText="Correlation between green and red zones"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={-1}
                  max={1}
                  stepSize={0.05}
                  labelStepSize={0.5}
                  value={pricePath.correlation_matrix.green_red}
                  onChange={(value) => handleNestedChange('correlation_matrix.green_red', value)}
                  onRelease={() => onBlur('price_path.correlation_matrix.green_red')}
                  labelRenderer={value => value.toFixed(2)}
                  intent={errors['price_path.correlation_matrix.green_red'] ? Intent.DANGER : Intent.PRIMARY}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {pricePath.correlation_matrix.green_red.toFixed(2)}
                </div>
              </div>
            </FormGroup>

            <FormGroup
              label="Orange ↔ Red"
              intent={errors['price_path.correlation_matrix.orange_red'] ? Intent.DANGER : Intent.NONE}
              helperText="Correlation between orange and red zones"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={-1}
                  max={1}
                  stepSize={0.05}
                  labelStepSize={0.5}
                  value={pricePath.correlation_matrix.orange_red}
                  onChange={(value) => handleNestedChange('correlation_matrix.orange_red', value)}
                  onRelease={() => onBlur('price_path.correlation_matrix.orange_red')}
                  labelRenderer={value => value.toFixed(2)}
                  intent={errors['price_path.correlation_matrix.orange_red'] ? Intent.DANGER : Intent.PRIMARY}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {pricePath.correlation_matrix.orange_red.toFixed(2)}
                </div>
              </div>
            </FormGroup>
          </div>
        </div>

        {/* Model-Specific Parameters */}
        {pricePath.model_type === 'mean_reversion' && (
          <div>
            <h4 className="text-sm font-semibold mb-3">Mean Reversion Parameters</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormGroup
                label="Reversion Speed"
                intent={errors['price_path.mean_reversion_params.speed'] ? Intent.DANGER : Intent.NONE}
                helperText="Speed of mean reversion"
              >
                <SimpleNumericInput
                  value={pricePath.mean_reversion_params.speed}
                  onValueChange={(value) => handleNestedChange('mean_reversion_params.speed', value)}
                  onBlur={() => onBlur('price_path.mean_reversion_params.speed')}
                  min={0}
                  max={1}
                  step={0.01}
                  formatter={formatPercentage}
                  intent={errors['price_path.mean_reversion_params.speed'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Long-Term Mean"
                intent={errors['price_path.mean_reversion_params.long_term_mean'] ? Intent.DANGER : Intent.NONE}
                helperText="Long-term mean to revert to"
              >
                <SimpleNumericInput
                  value={pricePath.mean_reversion_params.long_term_mean}
                  onValueChange={(value) => handleNestedChange('mean_reversion_params.long_term_mean', value)}
                  onBlur={() => onBlur('price_path.mean_reversion_params.long_term_mean')}
                  min={0}
                  max={1}
                  step={0.005}
                  formatter={formatPercentage}
                  intent={errors['price_path.mean_reversion_params.long_term_mean'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>
            </div>
          </div>
        )}

        {pricePath.model_type === 'regime_switching' && (
          <div>
            <h4 className="text-sm font-semibold mb-3">Regime Switching Parameters</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormGroup
                label="Bull Market Rate"
                intent={errors['price_path.regime_switching_params.bull_market_rate'] ? Intent.DANGER : Intent.NONE}
                helperText="Appreciation rate in bull market"
              >
                <SimpleNumericInput
                  value={pricePath.regime_switching_params.bull_market_rate}
                  onValueChange={(value) => handleNestedChange('regime_switching_params.bull_market_rate', value)}
                  onBlur={() => onBlur('price_path.regime_switching_params.bull_market_rate')}
                  min={0}
                  max={1}
                  step={0.005}
                  formatter={formatPercentage}
                  intent={errors['price_path.regime_switching_params.bull_market_rate'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Bear Market Rate"
                intent={errors['price_path.regime_switching_params.bear_market_rate'] ? Intent.DANGER : Intent.NONE}
                helperText="Appreciation rate in bear market"
              >
                <SimpleNumericInput
                  value={pricePath.regime_switching_params.bear_market_rate}
                  onValueChange={(value) => handleNestedChange('regime_switching_params.bear_market_rate', value)}
                  onBlur={() => onBlur('price_path.regime_switching_params.bear_market_rate')}
                  min={-1}
                  max={1}
                  step={0.005}
                  formatter={formatPercentage}
                  intent={errors['price_path.regime_switching_params.bear_market_rate'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Bull → Bear Probability"
                intent={errors['price_path.regime_switching_params.bull_to_bear_prob'] ? Intent.DANGER : Intent.NONE}
                helperText="Probability of switching from bull to bear"
              >
                <SimpleNumericInput
                  value={pricePath.regime_switching_params.bull_to_bear_prob}
                  onValueChange={(value) => handleNestedChange('regime_switching_params.bull_to_bear_prob', value)}
                  onBlur={() => onBlur('price_path.regime_switching_params.bull_to_bear_prob')}
                  min={0}
                  max={1}
                  step={0.01}
                  formatter={formatPercentage}
                  intent={errors['price_path.regime_switching_params.bull_to_bear_prob'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Bear → Bull Probability"
                intent={errors['price_path.regime_switching_params.bear_to_bull_prob'] ? Intent.DANGER : Intent.NONE}
                helperText="Probability of switching from bear to bull"
              >
                <SimpleNumericInput
                  value={pricePath.regime_switching_params.bear_to_bull_prob}
                  onValueChange={(value) => handleNestedChange('regime_switching_params.bear_to_bull_prob', value)}
                  onBlur={() => onBlur('price_path.regime_switching_params.bear_to_bull_prob')}
                  min={0}
                  max={1}
                  step={0.01}
                  formatter={formatPercentage}
                  intent={errors['price_path.regime_switching_params.bear_to_bull_prob'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>
            </div>
          </div>
        )}

        {/* Variation Factors */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Variation Factors</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormGroup
              label="Suburb Variation"
              intent={errors['price_path.suburb_variation'] ? Intent.DANGER : Intent.NONE}
              helperText="Variation factor for suburb-specific paths"
            >
              <SimpleNumericInput
                value={pricePath.suburb_variation}
                onValueChange={(value) => handleChange('suburb_variation', value)}
                onBlur={() => handleBlur('suburb_variation')}
                min={0}
                max={1}
                step={0.005}
                formatter={formatPercentage}
                intent={errors['price_path.suburb_variation'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Property Variation"
              intent={errors['price_path.property_variation'] ? Intent.DANGER : Intent.NONE}
              helperText="Variation factor for property-specific paths"
            >
              <SimpleNumericInput
                value={pricePath.property_variation}
                onValueChange={(value) => handleChange('property_variation', value)}
                onBlur={() => handleBlur('property_variation')}
                min={0}
                max={1}
                step={0.005}
                formatter={formatPercentage}
                intent={errors['price_path.property_variation'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Cycle Position"
              intent={errors['price_path.cycle_position'] ? Intent.DANGER : Intent.NONE}
              helperText="Initial position in property cycle"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={1}
                  stepSize={0.05}
                  labelStepSize={0.25}
                  value={pricePath.cycle_position}
                  onChange={(value) => handleChange('cycle_position', value)}
                  onRelease={() => handleBlur('cycle_position')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['price_path.cycle_position'] ? Intent.DANGER : Intent.PRIMARY}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {formatPercentage(pricePath.cycle_position)}
                </div>
              </div>
            </FormGroup>
          </div>
        </div>

        {/* Help Information */}
        <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
          <h4 className="font-semibold mb-2">Price Path & Correlations Information</h4>
          <p>Configure how property prices evolve over time:</p>
          <ul className="list-disc pl-5 space-y-1 mt-2">
            <li><strong>GBM:</strong> Geometric Brownian Motion - constant drift and volatility</li>
            <li><strong>Mean Reversion:</strong> Prices revert to long-term mean over time</li>
            <li><strong>Regime Switching:</strong> Alternates between bull and bear market regimes</li>
            <li><strong>Correlations:</strong> How price movements are correlated between zones</li>
          </ul>
        </div>
      </div>
    </Card>
  );
};

export default PricePathCorrelations;
