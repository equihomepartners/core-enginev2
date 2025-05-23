import React from 'react';
import { FormGroup, Intent, Switch, HTMLSelect } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface RiskMetricsProps {
  riskMetrics: {
    var_confidence_level: number;
    risk_free_rate: number;
    benchmark_return: number;
    min_acceptable_return: number;
    stress_test_scenarios: Array<{
      name: string;
      description: string;
      property_value_shock: number;
      interest_rate_shock: number;
      default_rate_shock: number;
      liquidity_shock: number;
    }>;
    monte_carlo_simulations: number;
    tail_risk_threshold: number;
    enable_sensitivity_analysis: boolean;
    sensitivity_parameters: string[];
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const RiskMetrics: React.FC<RiskMetricsProps> = ({
  riskMetrics,
  onChange,
  onBlur,
  errors
}) => {
  const handleChange = (field: string, value: any) => {
    onChange(`risk_metrics.${field}`, value);
  };

  const handleBlur = (field: string) => {
    onBlur(`risk_metrics.${field}`);
  };

  const handleNestedChange = (field: string, value: any) => {
    onChange(`risk_metrics.${field}`, value);
  };

  const availableSensitivityParams = [
    'interest_rate',
    'property_value_growth',
    'default_rate',
    'prepayment_rate',
    'ltv_ratio',
    'leverage_ratio',
    'management_fee_rate',
    'carried_interest_rate',
    'hurdle_rate'
  ];

  const handleSensitivityParamToggle = (param: string, checked: boolean) => {
    const currentParams = riskMetrics.sensitivity_parameters || [];
    let newParams;
    
    if (checked) {
      newParams = [...currentParams, param];
    } else {
      newParams = currentParams.filter(p => p !== param);
    }
    
    handleChange('sensitivity_parameters', newParams);
  };

  return (
    <Card
      title="Risk Metrics & Stress Testing"
      icon="shield"
      subtitle="Configure risk measurement and stress testing parameters"
    >
      <div className="space-y-6">
        {/* Risk-Adjusted Return Parameters */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Risk-Adjusted Return Parameters</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="VaR Confidence Level"
              intent={errors['risk_metrics.var_confidence_level'] ? Intent.DANGER : Intent.NONE}
              helperText="Confidence level for Value at Risk calculation"
            >
              <SimpleNumericInput
                value={riskMetrics.var_confidence_level}
                onValueChange={(value) => handleChange('var_confidence_level', value)}
                onBlur={() => handleBlur('var_confidence_level')}
                min={0.8}
                max={0.99}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['risk_metrics.var_confidence_level'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Risk-Free Rate"
              intent={errors['risk_metrics.risk_free_rate'] ? Intent.DANGER : Intent.NONE}
              helperText="Risk-free rate for risk-adjusted return calculations"
            >
              <SimpleNumericInput
                value={riskMetrics.risk_free_rate}
                onValueChange={(value) => handleChange('risk_free_rate', value)}
                onBlur={() => handleBlur('risk_free_rate')}
                min={0}
                max={0.1}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['risk_metrics.risk_free_rate'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Benchmark Return"
              intent={errors['risk_metrics.benchmark_return'] ? Intent.DANGER : Intent.NONE}
              helperText="Benchmark return for alpha and information ratio calculations"
            >
              <SimpleNumericInput
                value={riskMetrics.benchmark_return}
                onValueChange={(value) => handleChange('benchmark_return', value)}
                onBlur={() => handleBlur('benchmark_return')}
                min={0}
                max={0.2}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['risk_metrics.benchmark_return'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Minimum Acceptable Return"
              intent={errors['risk_metrics.min_acceptable_return'] ? Intent.DANGER : Intent.NONE}
              helperText="Minimum acceptable return for Sortino ratio calculation"
            >
              <SimpleNumericInput
                value={riskMetrics.min_acceptable_return}
                onValueChange={(value) => handleChange('min_acceptable_return', value)}
                onBlur={() => handleBlur('min_acceptable_return')}
                min={0}
                max={0.1}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['risk_metrics.min_acceptable_return'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>
        </div>

        {/* Monte Carlo & Tail Risk */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Monte Carlo & Tail Risk</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Monte Carlo Simulations"
              intent={errors['risk_metrics.monte_carlo_simulations'] ? Intent.DANGER : Intent.NONE}
              helperText="Number of Monte Carlo simulations for risk metrics"
            >
              <SimpleNumericInput
                value={riskMetrics.monte_carlo_simulations}
                onValueChange={(value) => handleChange('monte_carlo_simulations', value)}
                onBlur={() => handleBlur('monte_carlo_simulations')}
                min={100}
                max={10000}
                step={100}
                formatter={value => value.toLocaleString()}
                intent={errors['risk_metrics.monte_carlo_simulations'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Tail Risk Threshold"
              intent={errors['risk_metrics.tail_risk_threshold'] ? Intent.DANGER : Intent.NONE}
              helperText="Threshold for tail risk calculation"
            >
              <SimpleNumericInput
                value={riskMetrics.tail_risk_threshold}
                onValueChange={(value) => handleChange('tail_risk_threshold', value)}
                onBlur={() => handleBlur('tail_risk_threshold')}
                min={0}
                max={0.5}
                step={0.005}
                formatter={formatPercentage}
                intent={errors['risk_metrics.tail_risk_threshold'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>
        </div>

        {/* Stress Test Scenarios */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Stress Test Scenarios</h4>
          <div className="space-y-4">
            {riskMetrics.stress_test_scenarios.map((scenario, index) => (
              <div key={index} className="border rounded-md p-4 bg-gray-50">
                <div className="flex justify-between items-center mb-3">
                  <div>
                    <h5 className="font-medium text-sm">{scenario.name.replace('_', ' ').toUpperCase()}</h5>
                    <p className="text-xs text-gray-600">{scenario.description}</p>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                  <div>
                    <label className="block text-gray-600 mb-1">Property Value Shock</label>
                    <SimpleNumericInput
                      value={scenario.property_value_shock}
                      onValueChange={(value) => handleNestedChange(`stress_test_scenarios.${index}.property_value_shock`, value)}
                      onBlur={() => onBlur(`risk_metrics.stress_test_scenarios.${index}.property_value_shock`)}
                      min={-1}
                      max={1}
                      step={0.01}
                      formatter={formatPercentage}
                      size="small"
                      fill={true}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-gray-600 mb-1">Interest Rate Shock</label>
                    <SimpleNumericInput
                      value={scenario.interest_rate_shock}
                      onValueChange={(value) => handleNestedChange(`stress_test_scenarios.${index}.interest_rate_shock`, value)}
                      onBlur={() => onBlur(`risk_metrics.stress_test_scenarios.${index}.interest_rate_shock`)}
                      min={-0.1}
                      max={0.1}
                      step={0.001}
                      formatter={value => `${(value * 100).toFixed(1)}bp`}
                      size="small"
                      fill={true}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-gray-600 mb-1">Default Rate Shock</label>
                    <SimpleNumericInput
                      value={scenario.default_rate_shock}
                      onValueChange={(value) => handleNestedChange(`stress_test_scenarios.${index}.default_rate_shock`, value)}
                      onBlur={() => onBlur(`risk_metrics.stress_test_scenarios.${index}.default_rate_shock`)}
                      min={0}
                      max={10}
                      step={0.1}
                      formatter={value => `${value.toFixed(1)}x`}
                      size="small"
                      fill={true}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-gray-600 mb-1">Liquidity Shock</label>
                    <SimpleNumericInput
                      value={scenario.liquidity_shock}
                      onValueChange={(value) => handleNestedChange(`stress_test_scenarios.${index}.liquidity_shock`, value)}
                      onBlur={() => onBlur(`risk_metrics.stress_test_scenarios.${index}.liquidity_shock`)}
                      min={0}
                      max={1}
                      step={0.01}
                      formatter={formatPercentage}
                      size="small"
                      fill={true}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Sensitivity Analysis */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Sensitivity Analysis</h4>
          
          <FormGroup
            label="Enable Sensitivity Analysis"
            helperText="Whether to enable sensitivity analysis"
            inline={true}
          >
            <Switch
              checked={riskMetrics.enable_sensitivity_analysis}
              onChange={(e) => handleChange('enable_sensitivity_analysis', e.target.checked)}
              label="Enable"
            />
          </FormGroup>

          {riskMetrics.enable_sensitivity_analysis && (
            <div className="mt-4">
              <h5 className="text-sm font-medium mb-2">Parameters to Analyze</h5>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                {availableSensitivityParams.map(param => (
                  <FormGroup
                    key={param}
                    inline={true}
                    className="mb-2"
                  >
                    <Switch
                      checked={riskMetrics.sensitivity_parameters?.includes(param) || false}
                      onChange={(e) => handleSensitivityParamToggle(param, e.target.checked)}
                      label={param.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      className="text-xs"
                    />
                  </FormGroup>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Risk Metrics Summary */}
        <div className="bg-blue-50 p-4 rounded-md">
          <h4 className="text-sm font-semibold mb-2">Risk Metrics Summary</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
            <div>
              <div className="text-gray-600">VaR Confidence</div>
              <div className="font-medium">{formatPercentage(riskMetrics.var_confidence_level)}</div>
            </div>
            <div>
              <div className="text-gray-600">Monte Carlo Runs</div>
              <div className="font-medium">{riskMetrics.monte_carlo_simulations.toLocaleString()}</div>
            </div>
            <div>
              <div className="text-gray-600">Stress Scenarios</div>
              <div className="font-medium">{riskMetrics.stress_test_scenarios.length}</div>
            </div>
            <div>
              <div className="text-gray-600">Sensitivity Params</div>
              <div className="font-medium">{riskMetrics.sensitivity_parameters?.length || 0}</div>
            </div>
          </div>
        </div>

        {/* Help Information */}
        <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
          <h4 className="font-semibold mb-2">Risk Metrics Information</h4>
          <p>Configure comprehensive risk measurement and stress testing:</p>
          <ul className="list-disc pl-5 space-y-1 mt-2">
            <li><strong>VaR:</strong> Value at Risk calculation with configurable confidence levels</li>
            <li><strong>Risk-Adjusted Returns:</strong> Sharpe, Sortino, and Information ratios</li>
            <li><strong>Stress Testing:</strong> Multiple economic scenarios with customizable shocks</li>
            <li><strong>Sensitivity Analysis:</strong> Parameter sensitivity across key risk factors</li>
            <li><strong>Monte Carlo:</strong> Stochastic simulation for tail risk analysis</li>
          </ul>
        </div>
      </div>
    </Card>
  );
};

export default RiskMetrics;
