import React from 'react';
import { FormGroup, Intent, HTMLSelect, Switch } from '@blueprintjs/core';
import { formatCurrency, formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface CapitalAllocationStrategyProps {
  reinvestmentEngine: {
    reinvestment_strategy: string;
    min_reinvestment_amount: number;
    reinvestment_frequency: string;
    reinvestment_delay: number;
    reinvestment_batch_size: number;
    zone_preference_multipliers: {
      green: number;
      orange: number;
      red: number;
    };
    opportunistic_threshold: number;
    rebalance_threshold: number;
    reinvestment_ltv_adjustment: number;
    reinvestment_size_adjustment: number;
    enable_dynamic_allocation: boolean;
    performance_lookback_period: number;
    performance_weight: number;
    max_allocation_adjustment: number;
    enable_cash_reserve: boolean;
    cash_reserve_target: number;
    cash_reserve_min: number;
    cash_reserve_max: number;
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const CapitalAllocationStrategy: React.FC<CapitalAllocationStrategyProps> = ({
  reinvestmentEngine,
  onChange,
  onBlur,
  errors
}) => {
  const handleChange = (field: string, value: any) => {
    onChange(`reinvestment_engine.${field}`, value);
  };

  const handleBlur = (field: string) => {
    onBlur(`reinvestment_engine.${field}`);
  };

  const handleNestedChange = (field: string, value: any) => {
    onChange(`reinvestment_engine.${field}`, value);
  };

  return (
    <Card
      title="Capital Allocation Strategy"
      icon="flows"
      subtitle="Configure reinvestment and rebalancing strategy"
    >
      <div className="space-y-4">
        {/* Reinvestment Strategy */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormGroup
            label="Reinvestment Strategy"
            intent={errors['reinvestment_engine.reinvestment_strategy'] ? Intent.DANGER : Intent.NONE}
            helperText={errors['reinvestment_engine.reinvestment_strategy'] || "Strategy for reinvesting capital"}
          >
            <HTMLSelect
              value={reinvestmentEngine.reinvestment_strategy}
              onChange={(e) => handleChange('reinvestment_strategy', e.target.value)}
              onBlur={() => handleBlur('reinvestment_strategy')}
              fill={true}
            >
              <option value="maintain_allocation">Maintain Allocation</option>
              <option value="rebalance">Rebalance</option>
              <option value="opportunistic">Opportunistic</option>
              <option value="custom">Custom</option>
            </HTMLSelect>
          </FormGroup>

          <FormGroup
            label="Reinvestment Frequency"
            intent={errors['reinvestment_engine.reinvestment_frequency'] ? Intent.DANGER : Intent.NONE}
            helperText={errors['reinvestment_engine.reinvestment_frequency'] || "How often to check for reinvestment"}
          >
            <HTMLSelect
              value={reinvestmentEngine.reinvestment_frequency}
              onChange={(e) => handleChange('reinvestment_frequency', e.target.value)}
              onBlur={() => handleBlur('reinvestment_frequency')}
              fill={true}
            >
              <option value="monthly">Monthly</option>
              <option value="quarterly">Quarterly</option>
              <option value="semi_annually">Semi-Annually</option>
              <option value="annually">Annually</option>
              <option value="on_exit">On Exit</option>
            </HTMLSelect>
          </FormGroup>
        </div>

        {/* Reinvestment Parameters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <FormGroup
            label="Min Reinvestment Amount"
            intent={errors['reinvestment_engine.min_reinvestment_amount'] ? Intent.DANGER : Intent.NONE}
            helperText={errors['reinvestment_engine.min_reinvestment_amount'] || "Minimum amount to trigger reinvestment"}
          >
            <SimpleNumericInput
              value={reinvestmentEngine.min_reinvestment_amount}
              onValueChange={(value) => handleChange('min_reinvestment_amount', value)}
              onBlur={() => handleBlur('min_reinvestment_amount')}
              min={0}
              step={10000}
              formatter={formatCurrency}
              intent={errors['reinvestment_engine.min_reinvestment_amount'] ? Intent.DANGER : Intent.NONE}
              fill={true}
            />
          </FormGroup>

          <FormGroup
            label="Reinvestment Delay (Months)"
            intent={errors['reinvestment_engine.reinvestment_delay'] ? Intent.DANGER : Intent.NONE}
            helperText={errors['reinvestment_engine.reinvestment_delay'] || "Delay between exit and reinvestment"}
          >
            <SimpleNumericInput
              value={reinvestmentEngine.reinvestment_delay}
              onValueChange={(value) => handleChange('reinvestment_delay', value)}
              onBlur={() => handleBlur('reinvestment_delay')}
              min={0}
              max={24}
              step={1}
              intent={errors['reinvestment_engine.reinvestment_delay'] ? Intent.DANGER : Intent.NONE}
              fill={true}
            />
          </FormGroup>

          <FormGroup
            label="Batch Size"
            intent={errors['reinvestment_engine.reinvestment_batch_size'] ? Intent.DANGER : Intent.NONE}
            helperText={errors['reinvestment_engine.reinvestment_batch_size'] || "Max loans per batch"}
          >
            <SimpleNumericInput
              value={reinvestmentEngine.reinvestment_batch_size}
              onValueChange={(value) => handleChange('reinvestment_batch_size', value)}
              onBlur={() => handleBlur('reinvestment_batch_size')}
              min={1}
              max={1000}
              step={10}
              intent={errors['reinvestment_engine.reinvestment_batch_size'] ? Intent.DANGER : Intent.NONE}
              fill={true}
            />
          </FormGroup>
        </div>

        {/* Zone Preference Multipliers */}
        <div>
          <h4 className="text-sm font-semibold mb-2">Zone Preference Multipliers</h4>
          <div className="grid grid-cols-3 gap-4">
            <FormGroup
              label="Green Zone Preference"
              intent={errors['reinvestment_engine.zone_preference_multipliers.green'] ? Intent.DANGER : Intent.NONE}
              helperText="Preference multiplier for green zone"
            >
              <SimpleNumericInput
                value={reinvestmentEngine.zone_preference_multipliers.green}
                onValueChange={(value) => handleNestedChange('zone_preference_multipliers.green', value)}
                onBlur={() => onBlur('reinvestment_engine.zone_preference_multipliers.green')}
                min={0}
                max={10}
                step={0.1}
                intent={errors['reinvestment_engine.zone_preference_multipliers.green'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Orange Zone Preference"
              intent={errors['reinvestment_engine.zone_preference_multipliers.orange'] ? Intent.DANGER : Intent.NONE}
              helperText="Preference multiplier for orange zone"
            >
              <SimpleNumericInput
                value={reinvestmentEngine.zone_preference_multipliers.orange}
                onValueChange={(value) => handleNestedChange('zone_preference_multipliers.orange', value)}
                onBlur={() => onBlur('reinvestment_engine.zone_preference_multipliers.orange')}
                min={0}
                max={10}
                step={0.1}
                intent={errors['reinvestment_engine.zone_preference_multipliers.orange'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Red Zone Preference"
              intent={errors['reinvestment_engine.zone_preference_multipliers.red'] ? Intent.DANGER : Intent.NONE}
              helperText="Preference multiplier for red zone"
            >
              <SimpleNumericInput
                value={reinvestmentEngine.zone_preference_multipliers.red}
                onValueChange={(value) => handleNestedChange('zone_preference_multipliers.red', value)}
                onBlur={() => onBlur('reinvestment_engine.zone_preference_multipliers.red')}
                min={0}
                max={10}
                step={0.1}
                intent={errors['reinvestment_engine.zone_preference_multipliers.red'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>
        </div>

        {/* Strategy-Specific Parameters */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormGroup
            label="Opportunistic Threshold"
            intent={errors['reinvestment_engine.opportunistic_threshold'] ? Intent.DANGER : Intent.NONE}
            helperText={errors['reinvestment_engine.opportunistic_threshold'] || "Appreciation threshold for opportunistic strategy"}
          >
            <SimpleNumericInput
              value={reinvestmentEngine.opportunistic_threshold}
              onValueChange={(value) => handleChange('opportunistic_threshold', value)}
              onBlur={() => handleBlur('opportunistic_threshold')}
              min={0}
              max={1}
              step={0.01}
              formatter={formatPercentage}
              intent={errors['reinvestment_engine.opportunistic_threshold'] ? Intent.DANGER : Intent.NONE}
              fill={true}
            />
          </FormGroup>

          <FormGroup
            label="Rebalance Threshold"
            intent={errors['reinvestment_engine.rebalance_threshold'] ? Intent.DANGER : Intent.NONE}
            helperText={errors['reinvestment_engine.rebalance_threshold'] || "Allocation gap to trigger rebalancing"}
          >
            <SimpleNumericInput
              value={reinvestmentEngine.rebalance_threshold}
              onValueChange={(value) => handleChange('rebalance_threshold', value)}
              onBlur={() => handleBlur('rebalance_threshold')}
              min={0}
              max={1}
              step={0.01}
              formatter={formatPercentage}
              intent={errors['reinvestment_engine.rebalance_threshold'] ? Intent.DANGER : Intent.NONE}
              fill={true}
            />
          </FormGroup>
        </div>

        {/* Dynamic Allocation */}
        <div>
          <FormGroup
            label="Enable Dynamic Allocation"
            helperText="Dynamically adjust allocations based on performance"
            inline={true}
          >
            <Switch
              checked={reinvestmentEngine.enable_dynamic_allocation}
              onChange={(e) => handleChange('enable_dynamic_allocation', e.target.checked)}
              label="Enable"
            />
          </FormGroup>

          {reinvestmentEngine.enable_dynamic_allocation && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2 pl-4 border-l-2 border-gray-200">
              <FormGroup
                label="Performance Lookback (Months)"
                intent={errors['reinvestment_engine.performance_lookback_period'] ? Intent.DANGER : Intent.NONE}
                helperText="Lookback period for performance analysis"
              >
                <SimpleNumericInput
                  value={reinvestmentEngine.performance_lookback_period}
                  onValueChange={(value) => handleChange('performance_lookback_period', value)}
                  onBlur={() => handleBlur('performance_lookback_period')}
                  min={1}
                  max={60}
                  step={1}
                  intent={errors['reinvestment_engine.performance_lookback_period'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Performance Weight"
                intent={errors['reinvestment_engine.performance_weight'] ? Intent.DANGER : Intent.NONE}
                helperText="Weight of performance in allocation"
              >
                <SimpleNumericInput
                  value={reinvestmentEngine.performance_weight}
                  onValueChange={(value) => handleChange('performance_weight', value)}
                  onBlur={() => handleBlur('performance_weight')}
                  min={0}
                  max={1}
                  step={0.1}
                  formatter={formatPercentage}
                  intent={errors['reinvestment_engine.performance_weight'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Max Allocation Adjustment"
                intent={errors['reinvestment_engine.max_allocation_adjustment'] ? Intent.DANGER : Intent.NONE}
                helperText="Maximum adjustment to allocation"
              >
                <SimpleNumericInput
                  value={reinvestmentEngine.max_allocation_adjustment}
                  onValueChange={(value) => handleChange('max_allocation_adjustment', value)}
                  onBlur={() => handleBlur('max_allocation_adjustment')}
                  min={0}
                  max={1}
                  step={0.05}
                  formatter={formatPercentage}
                  intent={errors['reinvestment_engine.max_allocation_adjustment'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>
            </div>
          )}
        </div>

        {/* Cash Reserve */}
        <div>
          <FormGroup
            label="Enable Cash Reserve"
            helperText="Maintain cash reserve instead of immediate reinvestment"
            inline={true}
          >
            <Switch
              checked={reinvestmentEngine.enable_cash_reserve}
              onChange={(e) => handleChange('enable_cash_reserve', e.target.checked)}
              label="Enable"
            />
          </FormGroup>

          {reinvestmentEngine.enable_cash_reserve && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2 pl-4 border-l-2 border-gray-200">
              <FormGroup
                label="Target Cash Reserve"
                intent={errors['reinvestment_engine.cash_reserve_target'] ? Intent.DANGER : Intent.NONE}
                helperText="Target cash reserve as % of fund size"
              >
                <SimpleNumericInput
                  value={reinvestmentEngine.cash_reserve_target}
                  onValueChange={(value) => handleChange('cash_reserve_target', value)}
                  onBlur={() => handleBlur('cash_reserve_target')}
                  min={0}
                  max={1}
                  step={0.01}
                  formatter={formatPercentage}
                  intent={errors['reinvestment_engine.cash_reserve_target'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Min Cash Reserve"
                intent={errors['reinvestment_engine.cash_reserve_min'] ? Intent.DANGER : Intent.NONE}
                helperText="Minimum cash reserve as % of fund size"
              >
                <SimpleNumericInput
                  value={reinvestmentEngine.cash_reserve_min}
                  onValueChange={(value) => handleChange('cash_reserve_min', value)}
                  onBlur={() => handleBlur('cash_reserve_min')}
                  min={0}
                  max={reinvestmentEngine.cash_reserve_target}
                  step={0.01}
                  formatter={formatPercentage}
                  intent={errors['reinvestment_engine.cash_reserve_min'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Max Cash Reserve"
                intent={errors['reinvestment_engine.cash_reserve_max'] ? Intent.DANGER : Intent.NONE}
                helperText="Maximum cash reserve as % of fund size"
              >
                <SimpleNumericInput
                  value={reinvestmentEngine.cash_reserve_max}
                  onValueChange={(value) => handleChange('cash_reserve_max', value)}
                  onBlur={() => handleBlur('cash_reserve_max')}
                  min={reinvestmentEngine.cash_reserve_target}
                  max={1}
                  step={0.01}
                  formatter={formatPercentage}
                  intent={errors['reinvestment_engine.cash_reserve_max'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>
            </div>
          )}
        </div>

        {/* Help Information */}
        <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
          <h4 className="font-semibold mb-2">Capital Allocation Strategy Information</h4>
          <p>Configure how capital is reinvested as loans exit:</p>
          <ul className="list-disc pl-5 space-y-1 mt-2">
            <li><strong>Maintain Allocation:</strong> Keep original zone allocations</li>
            <li><strong>Rebalance:</strong> Rebalance to target allocations</li>
            <li><strong>Opportunistic:</strong> Focus on best-performing zones</li>
            <li><strong>Custom:</strong> Use custom allocation rules</li>
          </ul>
        </div>
      </div>
    </Card>
  );
};

export default CapitalAllocationStrategy;
