import React from 'react';
import { FormGroup, Intent, Switch, HTMLSelect } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface LeverageRiskManagementProps {
  leverageRisk: {
    ramp_line: {
      enabled: boolean;
      limit_pct_commit: number;
      spread_bps: number;
      commitment_fee_bps: number;
      draw_period_months: number;
      term_months: number;
    };
    interest_rate_model: {
      base_rate_initial: number;
      volatility: number;
      mean_reversion: number;
      long_term_mean: number;
    };
    stress_testing: {
      enabled: boolean;
      interest_rate_shock: number;
      nav_shock: number;
      liquidity_shock: number;
    };
    optimization: {
      target_leverage: number;
      max_leverage: number;
      deleveraging_threshold: number;
      min_cash_buffer: number;
    };
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const LeverageRiskManagement: React.FC<LeverageRiskManagementProps> = ({
  leverageRisk,
  onChange,
  onBlur,
  errors
}) => {
  const handleChange = (field: string, value: any) => {
    onChange(`leverage_risk.${field}`, value);
  };

  const handleBlur = (field: string) => {
    onBlur(`leverage_risk.${field}`);
  };

  const handleNestedChange = (field: string, value: any) => {
    onChange(`leverage_risk.${field}`, value);
  };

  return (
    <div className="space-y-6">
      {/* Subscription Line (Ramp Line) Risk */}
      <Card
        title="Subscription Line Risk"
        icon="credit-card"
        subtitle="Risk parameters for subscription line facility"
      >
        <div className="space-y-4">
          <FormGroup
            label="Enable Subscription Line Risk Modeling"
            helperText="Model risks associated with subscription line facility"
            inline={true}
          >
            <Switch
              checked={leverageRisk.ramp_line.enabled}
              onChange={(e) => handleNestedChange('ramp_line.enabled', e.target.checked)}
              label="Enable"
            />
          </FormGroup>

          {leverageRisk.ramp_line.enabled && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pl-4 border-l-2 border-gray-200">
              <FormGroup
                label="Limit % of Commitments"
                intent={errors['leverage_risk.ramp_line.limit_pct_commit'] ? Intent.DANGER : Intent.NONE}
                helperText="Maximum facility size as % of commitments"
              >
                <SimpleNumericInput
                  value={leverageRisk.ramp_line.limit_pct_commit}
                  onValueChange={(value) => handleNestedChange('ramp_line.limit_pct_commit', value)}
                  onBlur={() => handleBlur('ramp_line.limit_pct_commit')}
                  min={0}
                  max={1}
                  step={0.01}
                  formatter={formatPercentage}
                  intent={errors['leverage_risk.ramp_line.limit_pct_commit'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Spread (bps)"
                intent={errors['leverage_risk.ramp_line.spread_bps'] ? Intent.DANGER : Intent.NONE}
                helperText="Interest rate spread in basis points"
              >
                <SimpleNumericInput
                  value={leverageRisk.ramp_line.spread_bps}
                  onValueChange={(value) => handleNestedChange('ramp_line.spread_bps', value)}
                  onBlur={() => handleBlur('ramp_line.spread_bps')}
                  min={0}
                  max={1000}
                  step={25}
                  formatter={value => `${value} bps`}
                  intent={errors['leverage_risk.ramp_line.spread_bps'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Commitment Fee (bps)"
                intent={errors['leverage_risk.ramp_line.commitment_fee_bps'] ? Intent.DANGER : Intent.NONE}
                helperText="Fee on undrawn balance"
              >
                <SimpleNumericInput
                  value={leverageRisk.ramp_line.commitment_fee_bps}
                  onValueChange={(value) => handleNestedChange('ramp_line.commitment_fee_bps', value)}
                  onBlur={() => handleBlur('ramp_line.commitment_fee_bps')}
                  min={0}
                  max={100}
                  step={5}
                  formatter={value => `${value} bps`}
                  intent={errors['leverage_risk.ramp_line.commitment_fee_bps'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Draw Period (Months)"
                intent={errors['leverage_risk.ramp_line.draw_period_months'] ? Intent.DANGER : Intent.NONE}
                helperText="Period during which draws are allowed"
              >
                <SimpleNumericInput
                  value={leverageRisk.ramp_line.draw_period_months}
                  onValueChange={(value) => handleNestedChange('ramp_line.draw_period_months', value)}
                  onBlur={() => handleBlur('ramp_line.draw_period_months')}
                  min={0}
                  max={60}
                  step={6}
                  formatter={value => `${value} months`}
                  intent={errors['leverage_risk.ramp_line.draw_period_months'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Term (Months)"
                intent={errors['leverage_risk.ramp_line.term_months'] ? Intent.DANGER : Intent.NONE}
                helperText="Total term of the facility"
              >
                <SimpleNumericInput
                  value={leverageRisk.ramp_line.term_months}
                  onValueChange={(value) => handleNestedChange('ramp_line.term_months', value)}
                  onBlur={() => handleBlur('ramp_line.term_months')}
                  min={0}
                  max={60}
                  step={6}
                  formatter={value => `${value} months`}
                  intent={errors['leverage_risk.ramp_line.term_months'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>
            </div>
          )}

          {/* Subscription Line Risk Summary */}
          {leverageRisk.ramp_line.enabled && (
            <div className="bg-orange-50 p-3 rounded-md text-sm">
              <h5 className="font-medium mb-2">Subscription Line Risk Profile</h5>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-xs">
                <div>
                  <div className="text-gray-600">Facility Limit</div>
                  <div className="font-medium">{formatPercentage(leverageRisk.ramp_line.limit_pct_commit)} of commitments</div>
                </div>
                <div>
                  <div className="text-gray-600">All-in Cost</div>
                  <div className="font-medium">{leverageRisk.ramp_line.spread_bps + leverageRisk.ramp_line.commitment_fee_bps} bps</div>
                </div>
                <div>
                  <div className="text-gray-600">Maturity Risk</div>
                  <div className="font-medium">{leverageRisk.ramp_line.term_months} month term</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </Card>

      {/* Interest Rate Model */}
      <Card
        title="Interest Rate Model"
        icon="timeline-line-chart"
        subtitle="Stochastic modeling of base interest rates"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Base Rate Initial"
              intent={errors['leverage_risk.interest_rate_model.base_rate_initial'] ? Intent.DANGER : Intent.NONE}
              helperText="Initial base rate (e.g., SOFR)"
            >
              <SimpleNumericInput
                value={leverageRisk.interest_rate_model.base_rate_initial}
                onValueChange={(value) => handleNestedChange('interest_rate_model.base_rate_initial', value)}
                onBlur={() => handleBlur('interest_rate_model.base_rate_initial')}
                min={0}
                max={0.2}
                step={0.0001}
                formatter={formatPercentage}
                intent={errors['leverage_risk.interest_rate_model.base_rate_initial'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Volatility"
              intent={errors['leverage_risk.interest_rate_model.volatility'] ? Intent.DANGER : Intent.NONE}
              helperText="Volatility of base rate"
            >
              <SimpleNumericInput
                value={leverageRisk.interest_rate_model.volatility}
                onValueChange={(value) => handleNestedChange('interest_rate_model.volatility', value)}
                onBlur={() => handleBlur('interest_rate_model.volatility')}
                min={0}
                max={0.1}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['leverage_risk.interest_rate_model.volatility'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Mean Reversion Speed"
              intent={errors['leverage_risk.interest_rate_model.mean_reversion'] ? Intent.DANGER : Intent.NONE}
              helperText="Speed of mean reversion"
            >
              <SimpleNumericInput
                value={leverageRisk.interest_rate_model.mean_reversion}
                onValueChange={(value) => handleNestedChange('interest_rate_model.mean_reversion', value)}
                onBlur={() => handleBlur('interest_rate_model.mean_reversion')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['leverage_risk.interest_rate_model.mean_reversion'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Long-Term Mean"
              intent={errors['leverage_risk.interest_rate_model.long_term_mean'] ? Intent.DANGER : Intent.NONE}
              helperText="Long-term mean for base rate"
            >
              <SimpleNumericInput
                value={leverageRisk.interest_rate_model.long_term_mean}
                onValueChange={(value) => handleNestedChange('interest_rate_model.long_term_mean', value)}
                onBlur={() => handleBlur('interest_rate_model.long_term_mean')}
                min={0}
                max={0.2}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['leverage_risk.interest_rate_model.long_term_mean'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>

          {/* Interest Rate Model Summary */}
          <div className="bg-blue-50 p-3 rounded-md text-sm">
            <h5 className="font-medium mb-2">Interest Rate Model Summary</h5>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
              <div>
                <div className="text-gray-600">Current Rate</div>
                <div className="font-medium">{formatPercentage(leverageRisk.interest_rate_model.base_rate_initial)}</div>
              </div>
              <div>
                <div className="text-gray-600">Volatility</div>
                <div className="font-medium">{formatPercentage(leverageRisk.interest_rate_model.volatility)}</div>
              </div>
              <div>
                <div className="text-gray-600">Mean Reversion</div>
                <div className="font-medium">{formatPercentage(leverageRisk.interest_rate_model.mean_reversion)}</div>
              </div>
              <div>
                <div className="text-gray-600">Long-Term Mean</div>
                <div className="font-medium">{formatPercentage(leverageRisk.interest_rate_model.long_term_mean)}</div>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Leverage Stress Testing */}
      <Card
        title="Leverage Stress Testing"
        icon="shield"
        subtitle="Test leverage performance under adverse scenarios"
      >
        <div className="space-y-4">
          <FormGroup
            label="Enable Stress Testing"
            helperText="Test leverage under stress scenarios"
            inline={true}
          >
            <Switch
              checked={leverageRisk.stress_testing.enabled}
              onChange={(e) => handleNestedChange('stress_testing.enabled', e.target.checked)}
              label="Enable"
            />
          </FormGroup>

          {leverageRisk.stress_testing.enabled && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pl-4 border-l-2 border-gray-200">
              <FormGroup
                label="Interest Rate Shock"
                intent={errors['leverage_risk.stress_testing.interest_rate_shock'] ? Intent.DANGER : Intent.NONE}
                helperText="Interest rate shock in percentage points"
              >
                <SimpleNumericInput
                  value={leverageRisk.stress_testing.interest_rate_shock}
                  onValueChange={(value) => handleNestedChange('stress_testing.interest_rate_shock', value)}
                  onBlur={() => handleBlur('stress_testing.interest_rate_shock')}
                  min={0}
                  max={0.1}
                  step={0.001}
                  formatter={value => `${(value * 10000).toFixed(0)}bp`}
                  intent={errors['leverage_risk.stress_testing.interest_rate_shock'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="NAV Shock"
                intent={errors['leverage_risk.stress_testing.nav_shock'] ? Intent.DANGER : Intent.NONE}
                helperText="NAV shock as percentage of NAV"
              >
                <SimpleNumericInput
                  value={leverageRisk.stress_testing.nav_shock}
                  onValueChange={(value) => handleNestedChange('stress_testing.nav_shock', value)}
                  onBlur={() => handleBlur('stress_testing.nav_shock')}
                  min={0}
                  max={1}
                  step={0.01}
                  formatter={formatPercentage}
                  intent={errors['leverage_risk.stress_testing.nav_shock'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Liquidity Shock"
                intent={errors['leverage_risk.stress_testing.liquidity_shock'] ? Intent.DANGER : Intent.NONE}
                helperText="Liquidity shock as % of expected liquidity"
              >
                <SimpleNumericInput
                  value={leverageRisk.stress_testing.liquidity_shock}
                  onValueChange={(value) => handleNestedChange('stress_testing.liquidity_shock', value)}
                  onBlur={() => handleBlur('stress_testing.liquidity_shock')}
                  min={0}
                  max={1}
                  step={0.01}
                  formatter={formatPercentage}
                  intent={errors['leverage_risk.stress_testing.liquidity_shock'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>
            </div>
          )}

          {/* Stress Test Results Preview */}
          {leverageRisk.stress_testing.enabled && (
            <div className="bg-red-50 p-3 rounded-md text-sm">
              <h5 className="font-medium mb-2">Stress Test Impact Preview</h5>
              <div className="grid grid-cols-3 gap-3 text-xs">
                <div>
                  <div className="text-gray-600">Interest Cost Impact</div>
                  <div className="font-medium text-red-600">
                    +{(leverageRisk.stress_testing.interest_rate_shock * 10000).toFixed(0)}bp
                  </div>
                </div>
                <div>
                  <div className="text-gray-600">NAV Impact</div>
                  <div className="font-medium text-red-600">
                    -{formatPercentage(leverageRisk.stress_testing.nav_shock)}
                  </div>
                </div>
                <div>
                  <div className="text-gray-600">Liquidity Impact</div>
                  <div className="font-medium text-red-600">
                    -{formatPercentage(leverageRisk.stress_testing.liquidity_shock)}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </Card>

      {/* Risk Management & Optimization */}
      <Card
        title="Risk Management & Optimization"
        icon="automatic-updates"
        subtitle="Automatic risk management and deleveraging parameters"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Target Leverage"
              intent={errors['leverage_risk.optimization.target_leverage'] ? Intent.DANGER : Intent.NONE}
              helperText="Target leverage ratio for optimization"
            >
              <SimpleNumericInput
                value={leverageRisk.optimization.target_leverage}
                onValueChange={(value) => handleNestedChange('optimization.target_leverage', value)}
                onBlur={() => handleBlur('optimization.target_leverage')}
                min={0}
                max={5}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['leverage_risk.optimization.target_leverage'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Maximum Leverage"
              intent={errors['leverage_risk.optimization.max_leverage'] ? Intent.DANGER : Intent.NONE}
              helperText="Maximum allowable leverage ratio"
            >
              <SimpleNumericInput
                value={leverageRisk.optimization.max_leverage}
                onValueChange={(value) => handleNestedChange('optimization.max_leverage', value)}
                onBlur={() => handleBlur('optimization.max_leverage')}
                min={leverageRisk.optimization.target_leverage}
                max={5}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['leverage_risk.optimization.max_leverage'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Deleveraging Threshold"
              intent={errors['leverage_risk.optimization.deleveraging_threshold'] ? Intent.DANGER : Intent.NONE}
              helperText="Leverage ratio that triggers automatic deleveraging"
            >
              <SimpleNumericInput
                value={leverageRisk.optimization.deleveraging_threshold}
                onValueChange={(value) => handleNestedChange('optimization.deleveraging_threshold', value)}
                onBlur={() => handleBlur('optimization.deleveraging_threshold')}
                min={leverageRisk.optimization.max_leverage}
                max={5}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['leverage_risk.optimization.deleveraging_threshold'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Minimum Cash Buffer"
              intent={errors['leverage_risk.optimization.min_cash_buffer'] ? Intent.DANGER : Intent.NONE}
              helperText="Minimum cash buffer as multiple of monthly expenses"
            >
              <SimpleNumericInput
                value={leverageRisk.optimization.min_cash_buffer}
                onValueChange={(value) => handleNestedChange('optimization.min_cash_buffer', value)}
                onBlur={() => handleBlur('optimization.min_cash_buffer')}
                min={0}
                max={10}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['leverage_risk.optimization.min_cash_buffer'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>

          {/* Risk Management Summary */}
          <div className="bg-yellow-50 p-3 rounded-md text-sm">
            <h5 className="font-medium mb-2">Risk Management Rules</h5>
            <ul className="list-disc pl-5 space-y-1 text-xs">
              <li>
                <strong>Target Leverage:</strong> Optimize around {leverageRisk.optimization.target_leverage.toFixed(1)}x leverage ratio
              </li>
              <li>
                <strong>Maximum Leverage:</strong> Hard limit at {leverageRisk.optimization.max_leverage.toFixed(1)}x leverage ratio
              </li>
              <li>
                <strong>Deleveraging:</strong> Automatic deleveraging triggered at {leverageRisk.optimization.deleveraging_threshold.toFixed(1)}x leverage ratio
              </li>
              <li>
                <strong>Cash Buffer:</strong> Maintain minimum {leverageRisk.optimization.min_cash_buffer.toFixed(1)}x monthly expenses in cash
              </li>
              <li>
                <strong>Stress Testing:</strong> {leverageRisk.stress_testing.enabled ? 'Enabled' : 'Disabled'} - Regular stress testing of leverage positions
              </li>
            </ul>
          </div>
        </div>
      </Card>

      {/* Help Information */}
      <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Leverage Risk Management Information</h4>
        <p>Configure risk management for leverage facilities:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Interest Rate Model:</strong> Stochastic modeling of base rates with mean reversion</li>
          <li><strong>Stress Testing:</strong> Test leverage performance under adverse market conditions</li>
          <li><strong>Risk Management:</strong> Automatic deleveraging and cash buffer requirements</li>
          <li><strong>Optimization:</strong> Dynamic leverage management based on market conditions</li>
        </ul>
      </div>
    </div>
  );
};

export default LeverageRiskManagement;
