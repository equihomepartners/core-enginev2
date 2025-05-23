import React from 'react';
import { FormGroup, Intent, Switch, Callout } from '@blueprintjs/core';
import { formatPercentage, formatBasisPoints } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface LeverageParametersProps {
  leverageEngine: {
    enabled: boolean;
    green_sleeve: {
      enabled: boolean;
      max_mult: number;
      spread_bps: number;
      commitment_fee_bps: number;
      advance_rate: number;
      min_dscr: number;
      max_ltv: number;
    };
    optimization: {
      enabled: boolean;
      target_leverage: number;
      max_leverage: number;
      deleveraging_threshold: number;
    };
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const LeverageParameters: React.FC<LeverageParametersProps> = ({
  leverageEngine,
  onChange,
  onBlur,
  errors
}) => {
  // Handle toggle changes
  const handleToggle = (field: string, value: boolean) => {
    onChange(field, value);
  };

  // Handle numeric input changes
  const handleNumericChange = (field: string, value: number) => {
    onChange(field, value);
  };

  return (
    <Card
      title="Leverage Parameters"
      icon="bank-account"
      subtitle="Configure fund leverage options"
    >
      {/* Enable Leverage */}
      <FormGroup
        label="Enable Leverage"
        helperText="Enable or disable leverage for the fund"
      >
        <Switch
          checked={leverageEngine.enabled}
          onChange={(e) => handleToggle('leverage_engine.enabled', e.target.checked)}
          label="Use leverage to enhance returns"
        />
      </FormGroup>

      {leverageEngine.enabled && (
        <>
          <div className="mt-4 mb-4">
            <h4 className="font-semibold mb-2">Green Sleeve (NAV Line Facility)</h4>
            
            {/* Enable Green Sleeve */}
            <FormGroup
              label="Enable Green Sleeve"
              helperText="NAV-based credit facility"
              inline={true}
            >
              <Switch
                checked={leverageEngine.green_sleeve.enabled}
                onChange={(e) => handleToggle('leverage_engine.green_sleeve.enabled', e.target.checked)}
                label="Enable"
              />
            </FormGroup>

            {leverageEngine.green_sleeve.enabled && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2 pl-4 border-l-2 border-gray-200">
                {/* Max Multiplier */}
                <FormGroup
                  label="Maximum Multiplier"
                  intent={errors['leverage_engine.green_sleeve.max_mult'] ? Intent.DANGER : Intent.NONE}
                  helperText={errors['leverage_engine.green_sleeve.max_mult'] || "Maximum facility size as multiple of fund size"}
                >
                  <SimpleNumericInput
                    value={leverageEngine.green_sleeve.max_mult}
                    onValueChange={(value) => handleNumericChange('leverage_engine.green_sleeve.max_mult', value)}
                    onBlur={() => onBlur('leverage_engine.green_sleeve.max_mult')}
                    min={0}
                    max={5}
                    step={0.1}
                    intent={errors['leverage_engine.green_sleeve.max_mult'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>

                {/* Spread BPS */}
                <FormGroup
                  label="Spread (BPS)"
                  intent={errors['leverage_engine.green_sleeve.spread_bps'] ? Intent.DANGER : Intent.NONE}
                  helperText={errors['leverage_engine.green_sleeve.spread_bps'] || "Interest rate spread in basis points"}
                >
                  <SimpleNumericInput
                    value={leverageEngine.green_sleeve.spread_bps}
                    onValueChange={(value) => handleNumericChange('leverage_engine.green_sleeve.spread_bps', value)}
                    onBlur={() => onBlur('leverage_engine.green_sleeve.spread_bps')}
                    min={0}
                    max={1000}
                    step={5}
                    formatter={formatBasisPoints}
                    intent={errors['leverage_engine.green_sleeve.spread_bps'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>

                {/* Commitment Fee BPS */}
                <FormGroup
                  label="Commitment Fee (BPS)"
                  intent={errors['leverage_engine.green_sleeve.commitment_fee_bps'] ? Intent.DANGER : Intent.NONE}
                  helperText={errors['leverage_engine.green_sleeve.commitment_fee_bps'] || "Fee on undrawn balance in basis points"}
                >
                  <SimpleNumericInput
                    value={leverageEngine.green_sleeve.commitment_fee_bps}
                    onValueChange={(value) => handleNumericChange('leverage_engine.green_sleeve.commitment_fee_bps', value)}
                    onBlur={() => onBlur('leverage_engine.green_sleeve.commitment_fee_bps')}
                    min={0}
                    max={100}
                    step={1}
                    formatter={formatBasisPoints}
                    intent={errors['leverage_engine.green_sleeve.commitment_fee_bps'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>

                {/* Advance Rate */}
                <FormGroup
                  label="Advance Rate"
                  intent={errors['leverage_engine.green_sleeve.advance_rate'] ? Intent.DANGER : Intent.NONE}
                  helperText={errors['leverage_engine.green_sleeve.advance_rate'] || "Maximum advance rate against NAV"}
                >
                  <SimpleNumericInput
                    value={leverageEngine.green_sleeve.advance_rate}
                    onValueChange={(value) => handleNumericChange('leverage_engine.green_sleeve.advance_rate', value)}
                    onBlur={() => onBlur('leverage_engine.green_sleeve.advance_rate')}
                    min={0}
                    max={1}
                    step={0.01}
                    formatter={formatPercentage}
                    intent={errors['leverage_engine.green_sleeve.advance_rate'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>
              </div>
            )}
          </div>

          <div className="mt-4 mb-4">
            <h4 className="font-semibold mb-2">Leverage Optimization</h4>
            
            {/* Enable Optimization */}
            <FormGroup
              label="Enable Optimization"
              helperText="Automatically optimize leverage usage"
              inline={true}
            >
              <Switch
                checked={leverageEngine.optimization.enabled}
                onChange={(e) => handleToggle('leverage_engine.optimization.enabled', e.target.checked)}
                label="Enable"
              />
            </FormGroup>

            {leverageEngine.optimization.enabled && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2 pl-4 border-l-2 border-gray-200">
                {/* Target Leverage */}
                <FormGroup
                  label="Target Leverage"
                  intent={errors['leverage_engine.optimization.target_leverage'] ? Intent.DANGER : Intent.NONE}
                  helperText={errors['leverage_engine.optimization.target_leverage'] || "Target leverage ratio"}
                >
                  <SimpleNumericInput
                    value={leverageEngine.optimization.target_leverage}
                    onValueChange={(value) => handleNumericChange('leverage_engine.optimization.target_leverage', value)}
                    onBlur={() => onBlur('leverage_engine.optimization.target_leverage')}
                    min={0}
                    max={leverageEngine.optimization.max_leverage}
                    step={0.05}
                    formatter={value => `${value.toFixed(2)}x`}
                    intent={errors['leverage_engine.optimization.target_leverage'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>

                {/* Max Leverage */}
                <FormGroup
                  label="Maximum Leverage"
                  intent={errors['leverage_engine.optimization.max_leverage'] ? Intent.DANGER : Intent.NONE}
                  helperText={errors['leverage_engine.optimization.max_leverage'] || "Maximum leverage ratio"}
                >
                  <SimpleNumericInput
                    value={leverageEngine.optimization.max_leverage}
                    onValueChange={(value) => handleNumericChange('leverage_engine.optimization.max_leverage', value)}
                    onBlur={() => onBlur('leverage_engine.optimization.max_leverage')}
                    min={leverageEngine.optimization.target_leverage}
                    max={5}
                    step={0.05}
                    formatter={value => `${value.toFixed(2)}x`}
                    intent={errors['leverage_engine.optimization.max_leverage'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>

                {/* Deleveraging Threshold */}
                <FormGroup
                  label="Deleveraging Threshold"
                  intent={errors['leverage_engine.optimization.deleveraging_threshold'] ? Intent.DANGER : Intent.NONE}
                  helperText={errors['leverage_engine.optimization.deleveraging_threshold'] || "Leverage ratio threshold for deleveraging"}
                >
                  <SimpleNumericInput
                    value={leverageEngine.optimization.deleveraging_threshold}
                    onValueChange={(value) => handleNumericChange('leverage_engine.optimization.deleveraging_threshold', value)}
                    onBlur={() => onBlur('leverage_engine.optimization.deleveraging_threshold')}
                    min={leverageEngine.optimization.max_leverage}
                    max={5}
                    step={0.05}
                    formatter={value => `${value.toFixed(2)}x`}
                    intent={errors['leverage_engine.optimization.deleveraging_threshold'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>
              </div>
            )}
          </div>

          {/* Help Information */}
          <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
            <h4 className="font-semibold mb-2">Leverage Information</h4>
            <p>Leverage can enhance returns but also increases risk:</p>
            <ul className="list-disc pl-5 space-y-1 mt-2">
              <li><strong>Green Sleeve:</strong> NAV-based credit facility for the fund</li>
              <li><strong>Optimization:</strong> Controls how leverage is managed over time</li>
            </ul>
            <p className="mt-2 text-xs text-gray-600">Note: Higher leverage increases both potential returns and risks</p>
          </div>
        </>
      )}

      {!leverageEngine.enabled && (
        <Callout
          intent={Intent.WARNING}
          icon="info-sign"
          className="mt-4"
        >
          Leverage is currently disabled. Enable leverage to potentially enhance returns, but be aware that it also increases risk.
        </Callout>
      )}
    </Card>
  );
};

export default LeverageParameters;
