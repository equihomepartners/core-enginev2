import React from 'react';
import { FormGroup, Intent, Slider } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface ExitTimingDistributionProps {
  exitSimulator: {
    base_exit_rate: number;
    time_factor: number;
    price_factor: number;
    min_hold_period: number;
    max_hold_period: number;
    sale_weight: number;
    refinance_weight: number;
    default_weight: number;
    appreciation_sale_multiplier: number;
    interest_rate_refinance_multiplier: number;
    economic_factor_default_multiplier: number;
    appreciation_share: number;
    min_appreciation_share: number;
    max_appreciation_share: number;
    tiered_appreciation_thresholds: number[];
    tiered_appreciation_shares: number[];
    base_default_rate: number;
    recovery_rate: number;
    foreclosure_cost: number;
    foreclosure_time: number;
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const ExitTimingDistribution: React.FC<ExitTimingDistributionProps> = ({
  exitSimulator,
  onChange,
  onBlur,
  errors
}) => {
  const handleChange = (field: string, value: any) => {
    onChange(`exit_simulator.${field}`, value);
  };

  const handleBlur = (field: string) => {
    onBlur(`exit_simulator.${field}`);
  };

  return (
    <Card
      title="Exit Timing & Distribution"
      icon="timeline-events"
      subtitle="Configure loan exit patterns and timing"
    >
      <div className="space-y-6">
        {/* Base Exit Parameters */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Base Exit Parameters</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Base Exit Rate"
              intent={errors['exit_simulator.base_exit_rate'] ? Intent.DANGER : Intent.NONE}
              helperText={errors['exit_simulator.base_exit_rate'] || "Base annual exit probability"}
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={0.5}
                  stepSize={0.01}
                  labelStepSize={0.1}
                  value={exitSimulator.base_exit_rate}
                  onChange={(value) => handleChange('base_exit_rate', value)}
                  onRelease={() => handleBlur('base_exit_rate')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['exit_simulator.base_exit_rate'] ? Intent.DANGER : Intent.PRIMARY}
                  className="flex-grow"
                />
                <div className="w-20 text-right text-sm">
                  {formatPercentage(exitSimulator.base_exit_rate)}
                </div>
              </div>
            </FormGroup>

            <FormGroup
              label="Hold Period Range"
              helperText="Minimum and maximum holding periods"
            >
              <div className="grid grid-cols-2 gap-2">
                <SimpleNumericInput
                  value={exitSimulator.min_hold_period}
                  onValueChange={(value) => handleChange('min_hold_period', value)}
                  onBlur={() => handleBlur('min_hold_period')}
                  min={0}
                  max={exitSimulator.max_hold_period}
                  step={0.5}
                  placeholder="Min years"
                  intent={errors['exit_simulator.min_hold_period'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
                <SimpleNumericInput
                  value={exitSimulator.max_hold_period}
                  onValueChange={(value) => handleChange('max_hold_period', value)}
                  onBlur={() => handleBlur('max_hold_period')}
                  min={exitSimulator.min_hold_period}
                  max={30}
                  step={0.5}
                  placeholder="Max years"
                  intent={errors['exit_simulator.max_hold_period'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </div>
            </FormGroup>
          </div>
        </div>

        {/* Exit Factor Weights */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Exit Factor Weights</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Time Factor Weight"
              intent={errors['exit_simulator.time_factor'] ? Intent.DANGER : Intent.NONE}
              helperText="Weight for time-based exit probability"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={1}
                  stepSize={0.1}
                  labelStepSize={0.2}
                  value={exitSimulator.time_factor}
                  onChange={(value) => handleChange('time_factor', value)}
                  onRelease={() => handleBlur('time_factor')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['exit_simulator.time_factor'] ? Intent.DANGER : Intent.PRIMARY}
                  className="flex-grow"
                />
                <div className="w-20 text-right text-sm">
                  {formatPercentage(exitSimulator.time_factor)}
                </div>
              </div>
            </FormGroup>

            <FormGroup
              label="Price Factor Weight"
              intent={errors['exit_simulator.price_factor'] ? Intent.DANGER : Intent.NONE}
              helperText="Weight for price-based exit probability"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={1}
                  stepSize={0.1}
                  labelStepSize={0.2}
                  value={exitSimulator.price_factor}
                  onChange={(value) => handleChange('price_factor', value)}
                  onRelease={() => handleBlur('price_factor')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['exit_simulator.price_factor'] ? Intent.DANGER : Intent.PRIMARY}
                  className="flex-grow"
                />
                <div className="w-20 text-right text-sm">
                  {formatPercentage(exitSimulator.price_factor)}
                </div>
              </div>
            </FormGroup>
          </div>
        </div>

        {/* Exit Type Distribution */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Exit Type Distribution</h4>
          <div className="grid grid-cols-3 gap-4">
            <FormGroup
              label="Sale Weight"
              intent={errors['exit_simulator.sale_weight'] ? Intent.DANGER : Intent.NONE}
              helperText="Base weight for sale exits"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={1}
                  stepSize={0.05}
                  labelStepSize={0.2}
                  value={exitSimulator.sale_weight}
                  onChange={(value) => handleChange('sale_weight', value)}
                  onRelease={() => handleBlur('sale_weight')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['exit_simulator.sale_weight'] ? Intent.DANGER : Intent.SUCCESS}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {formatPercentage(exitSimulator.sale_weight)}
                </div>
              </div>
            </FormGroup>

            <FormGroup
              label="Refinance Weight"
              intent={errors['exit_simulator.refinance_weight'] ? Intent.DANGER : Intent.NONE}
              helperText="Base weight for refinance exits"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={1}
                  stepSize={0.05}
                  labelStepSize={0.2}
                  value={exitSimulator.refinance_weight}
                  onChange={(value) => handleChange('refinance_weight', value)}
                  onRelease={() => handleBlur('refinance_weight')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['exit_simulator.refinance_weight'] ? Intent.DANGER : Intent.WARNING}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {formatPercentage(exitSimulator.refinance_weight)}
                </div>
              </div>
            </FormGroup>

            <FormGroup
              label="Default Weight"
              intent={errors['exit_simulator.default_weight'] ? Intent.DANGER : Intent.NONE}
              helperText="Base weight for default exits"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={1}
                  stepSize={0.05}
                  labelStepSize={0.2}
                  value={exitSimulator.default_weight}
                  onChange={(value) => handleChange('default_weight', value)}
                  onRelease={() => handleBlur('default_weight')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['exit_simulator.default_weight'] ? Intent.DANGER : Intent.DANGER}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {formatPercentage(exitSimulator.default_weight)}
                </div>
              </div>
            </FormGroup>
          </div>

          {/* Total Weight Display */}
          <div className="mt-2 p-2 bg-gray-100 rounded text-sm">
            <div className="flex justify-between items-center">
              <span>Total Weight:</span>
              <span className={`font-bold ${
                Math.abs((exitSimulator.sale_weight + exitSimulator.refinance_weight + exitSimulator.default_weight) - 1) > 0.01 
                  ? 'text-red-600' : 'text-green-600'
              }`}>
                {formatPercentage(exitSimulator.sale_weight + exitSimulator.refinance_weight + exitSimulator.default_weight)}
              </span>
            </div>
            {Math.abs((exitSimulator.sale_weight + exitSimulator.refinance_weight + exitSimulator.default_weight) - 1) > 0.01 && (
              <div className="text-xs text-red-600 mt-1">
                Warning: Exit weights should sum to 100%
              </div>
            )}
          </div>
        </div>

        {/* Sensitivity Multipliers */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Sensitivity Multipliers</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormGroup
              label="Appreciation → Sale"
              intent={errors['exit_simulator.appreciation_sale_multiplier'] ? Intent.DANGER : Intent.NONE}
              helperText="How appreciation increases sale probability"
            >
              <SimpleNumericInput
                value={exitSimulator.appreciation_sale_multiplier}
                onValueChange={(value) => handleChange('appreciation_sale_multiplier', value)}
                onBlur={() => handleBlur('appreciation_sale_multiplier')}
                min={0}
                max={10}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['exit_simulator.appreciation_sale_multiplier'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Interest Rate → Refinance"
              intent={errors['exit_simulator.interest_rate_refinance_multiplier'] ? Intent.DANGER : Intent.NONE}
              helperText="How interest rates affect refinancing"
            >
              <SimpleNumericInput
                value={exitSimulator.interest_rate_refinance_multiplier}
                onValueChange={(value) => handleChange('interest_rate_refinance_multiplier', value)}
                onBlur={() => handleBlur('interest_rate_refinance_multiplier')}
                min={0}
                max={10}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['exit_simulator.interest_rate_refinance_multiplier'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Economic → Default"
              intent={errors['exit_simulator.economic_factor_default_multiplier'] ? Intent.DANGER : Intent.NONE}
              helperText="How economic factors affect defaults"
            >
              <SimpleNumericInput
                value={exitSimulator.economic_factor_default_multiplier}
                onValueChange={(value) => handleChange('economic_factor_default_multiplier', value)}
                onBlur={() => handleBlur('economic_factor_default_multiplier')}
                min={0}
                max={10}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['exit_simulator.economic_factor_default_multiplier'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>
        </div>

        {/* Appreciation Sharing */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Appreciation Sharing</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormGroup
              label="Appreciation Share"
              intent={errors['exit_simulator.appreciation_share'] ? Intent.DANGER : Intent.NONE}
              helperText="Fund's share of appreciation"
            >
              <SimpleNumericInput
                value={exitSimulator.appreciation_share}
                onValueChange={(value) => handleChange('appreciation_share', value)}
                onBlur={() => handleBlur('appreciation_share')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['exit_simulator.appreciation_share'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Min Share"
              intent={errors['exit_simulator.min_appreciation_share'] ? Intent.DANGER : Intent.NONE}
              helperText="Minimum appreciation share"
            >
              <SimpleNumericInput
                value={exitSimulator.min_appreciation_share}
                onValueChange={(value) => handleChange('min_appreciation_share', value)}
                onBlur={() => handleBlur('min_appreciation_share')}
                min={0}
                max={exitSimulator.appreciation_share}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['exit_simulator.min_appreciation_share'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Max Share"
              intent={errors['exit_simulator.max_appreciation_share'] ? Intent.DANGER : Intent.NONE}
              helperText="Maximum appreciation share"
            >
              <SimpleNumericInput
                value={exitSimulator.max_appreciation_share}
                onValueChange={(value) => handleChange('max_appreciation_share', value)}
                onBlur={() => handleBlur('max_appreciation_share')}
                min={exitSimulator.appreciation_share}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['exit_simulator.max_appreciation_share'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>
        </div>

        {/* Default & Recovery Parameters */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Default & Recovery Parameters</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Base Default Rate"
              intent={errors['exit_simulator.base_default_rate'] ? Intent.DANGER : Intent.NONE}
              helperText="Base annual default probability"
            >
              <SimpleNumericInput
                value={exitSimulator.base_default_rate}
                onValueChange={(value) => handleChange('base_default_rate', value)}
                onBlur={() => handleBlur('base_default_rate')}
                min={0}
                max={1}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['exit_simulator.base_default_rate'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Recovery Rate"
              intent={errors['exit_simulator.recovery_rate'] ? Intent.DANGER : Intent.NONE}
              helperText="Recovery rate in case of default"
            >
              <SimpleNumericInput
                value={exitSimulator.recovery_rate}
                onValueChange={(value) => handleChange('recovery_rate', value)}
                onBlur={() => handleBlur('recovery_rate')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['exit_simulator.recovery_rate'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Foreclosure Cost"
              intent={errors['exit_simulator.foreclosure_cost'] ? Intent.DANGER : Intent.NONE}
              helperText="Cost of foreclosure as % of property value"
            >
              <SimpleNumericInput
                value={exitSimulator.foreclosure_cost}
                onValueChange={(value) => handleChange('foreclosure_cost', value)}
                onBlur={() => handleBlur('foreclosure_cost')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['exit_simulator.foreclosure_cost'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Foreclosure Time (Years)"
              intent={errors['exit_simulator.foreclosure_time'] ? Intent.DANGER : Intent.NONE}
              helperText="Time to complete foreclosure"
            >
              <SimpleNumericInput
                value={exitSimulator.foreclosure_time}
                onValueChange={(value) => handleChange('foreclosure_time', value)}
                onBlur={() => handleBlur('foreclosure_time')}
                min={0}
                max={10}
                step={0.1}
                intent={errors['exit_simulator.foreclosure_time'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>
        </div>

        {/* Help Information */}
        <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
          <h4 className="font-semibold mb-2">Exit Timing & Distribution Information</h4>
          <p>Configure how and when loans exit the portfolio:</p>
          <ul className="list-disc pl-5 space-y-1 mt-2">
            <li><strong>Base Exit Rate:</strong> Annual probability of loan exit</li>
            <li><strong>Time/Price Factors:</strong> How time and appreciation affect exits</li>
            <li><strong>Exit Types:</strong> Distribution between sales, refinancing, and defaults</li>
            <li><strong>Sensitivity:</strong> How market conditions affect exit probabilities</li>
          </ul>
        </div>
      </div>
    </Card>
  );
};

export default ExitTimingDistribution;
