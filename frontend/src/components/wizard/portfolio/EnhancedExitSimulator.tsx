import React from 'react';
import { FormGroup, Intent, Switch, Slider } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface EnhancedExitSimulatorProps {
  enhancedExitSimulator: {
    refinance_interest_rate_sensitivity: number;
    sale_appreciation_sensitivity: number;
    life_event_probability: number;
    behavioral_correlation: number;
    recession_default_multiplier: number;
    inflation_refinance_multiplier: number;
    employment_sensitivity: number;
    migration_sensitivity: number;
    regulatory_compliance_cost: number;
    tax_efficiency_factor: number;
    vintage_segmentation: boolean;
    ltv_segmentation: boolean;
    zone_segmentation: boolean;
    var_confidence_level: number;
    stress_test_severity: number;
    tail_risk_threshold: number;
    use_ml_models: boolean;
    feature_importance_threshold: number;
    anomaly_detection_threshold: number;
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const EnhancedExitSimulator: React.FC<EnhancedExitSimulatorProps> = ({
  enhancedExitSimulator,
  onChange,
  onBlur,
  errors
}) => {
  const handleChange = (field: string, value: any) => {
    onChange(`enhanced_exit_simulator.${field}`, value);
  };

  const handleBlur = (field: string) => {
    onBlur(`enhanced_exit_simulator.${field}`);
  };

  return (
    <Card
      title="Enhanced Exit Simulator"
      icon="predictive-analysis"
      subtitle="Advanced behavioral and economic modeling"
    >
      <div className="space-y-6">
        {/* Behavioral Factors */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Behavioral & Life Event Factors</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Life Event Probability"
              intent={errors['enhanced_exit_simulator.life_event_probability'] ? Intent.DANGER : Intent.NONE}
              helperText="Annual probability of life events triggering exits"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={0.2}
                  stepSize={0.005}
                  labelStepSize={0.05}
                  value={enhancedExitSimulator.life_event_probability}
                  onChange={(value) => handleChange('life_event_probability', value)}
                  onRelease={() => handleBlur('life_event_probability')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['enhanced_exit_simulator.life_event_probability'] ? Intent.DANGER : Intent.PRIMARY}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {formatPercentage(enhancedExitSimulator.life_event_probability)}
                </div>
              </div>
            </FormGroup>

            <FormGroup
              label="Behavioral Correlation"
              intent={errors['enhanced_exit_simulator.behavioral_correlation'] ? Intent.DANGER : Intent.NONE}
              helperText="Correlation in exit decisions (herd behavior)"
            >
              <div className="flex items-center space-x-4">
                <Slider
                  min={0}
                  max={1}
                  stepSize={0.05}
                  labelStepSize={0.2}
                  value={enhancedExitSimulator.behavioral_correlation}
                  onChange={(value) => handleChange('behavioral_correlation', value)}
                  onRelease={() => handleBlur('behavioral_correlation')}
                  labelRenderer={value => formatPercentage(value)}
                  intent={errors['enhanced_exit_simulator.behavioral_correlation'] ? Intent.DANGER : Intent.PRIMARY}
                  className="flex-grow"
                />
                <div className="w-16 text-right text-sm">
                  {formatPercentage(enhancedExitSimulator.behavioral_correlation)}
                </div>
              </div>
            </FormGroup>
          </div>
        </div>

        {/* Economic Sensitivity */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Economic Sensitivity Factors</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Refinance Interest Rate Sensitivity"
              intent={errors['enhanced_exit_simulator.refinance_interest_rate_sensitivity'] ? Intent.DANGER : Intent.NONE}
              helperText="How sensitive refinancing is to interest rate changes"
            >
              <SimpleNumericInput
                value={enhancedExitSimulator.refinance_interest_rate_sensitivity}
                onValueChange={(value) => handleChange('refinance_interest_rate_sensitivity', value)}
                onBlur={() => handleBlur('refinance_interest_rate_sensitivity')}
                min={0}
                max={10}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['enhanced_exit_simulator.refinance_interest_rate_sensitivity'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Sale Appreciation Sensitivity"
              intent={errors['enhanced_exit_simulator.sale_appreciation_sensitivity'] ? Intent.DANGER : Intent.NONE}
              helperText="How sensitive sales are to appreciation"
            >
              <SimpleNumericInput
                value={enhancedExitSimulator.sale_appreciation_sensitivity}
                onValueChange={(value) => handleChange('sale_appreciation_sensitivity', value)}
                onBlur={() => handleBlur('sale_appreciation_sensitivity')}
                min={0}
                max={10}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['enhanced_exit_simulator.sale_appreciation_sensitivity'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Recession Default Multiplier"
              intent={errors['enhanced_exit_simulator.recession_default_multiplier'] ? Intent.DANGER : Intent.NONE}
              helperText="How much recessions increase defaults"
            >
              <SimpleNumericInput
                value={enhancedExitSimulator.recession_default_multiplier}
                onValueChange={(value) => handleChange('recession_default_multiplier', value)}
                onBlur={() => handleBlur('recession_default_multiplier')}
                min={0}
                max={10}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['enhanced_exit_simulator.recession_default_multiplier'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Inflation Refinance Multiplier"
              intent={errors['enhanced_exit_simulator.inflation_refinance_multiplier'] ? Intent.DANGER : Intent.NONE}
              helperText="How inflation affects refinancing"
            >
              <SimpleNumericInput
                value={enhancedExitSimulator.inflation_refinance_multiplier}
                onValueChange={(value) => handleChange('inflation_refinance_multiplier', value)}
                onBlur={() => handleBlur('inflation_refinance_multiplier')}
                min={0}
                max={10}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['enhanced_exit_simulator.inflation_refinance_multiplier'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Employment Sensitivity"
              intent={errors['enhanced_exit_simulator.employment_sensitivity'] ? Intent.DANGER : Intent.NONE}
              helperText="How employment affects exits"
            >
              <SimpleNumericInput
                value={enhancedExitSimulator.employment_sensitivity}
                onValueChange={(value) => handleChange('employment_sensitivity', value)}
                onBlur={() => handleBlur('employment_sensitivity')}
                min={0}
                max={10}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['enhanced_exit_simulator.employment_sensitivity'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Migration Sensitivity"
              intent={errors['enhanced_exit_simulator.migration_sensitivity'] ? Intent.DANGER : Intent.NONE}
              helperText="How population migration affects exits"
            >
              <SimpleNumericInput
                value={enhancedExitSimulator.migration_sensitivity}
                onValueChange={(value) => handleChange('migration_sensitivity', value)}
                onBlur={() => handleBlur('migration_sensitivity')}
                min={0}
                max={10}
                step={0.1}
                formatter={value => `${value.toFixed(1)}x`}
                intent={errors['enhanced_exit_simulator.migration_sensitivity'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>
        </div>

        {/* Regulatory & Tax Factors */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Regulatory & Tax Factors</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Regulatory Compliance Cost"
              intent={errors['enhanced_exit_simulator.regulatory_compliance_cost'] ? Intent.DANGER : Intent.NONE}
              helperText="Compliance cost as percentage of loan"
            >
              <SimpleNumericInput
                value={enhancedExitSimulator.regulatory_compliance_cost}
                onValueChange={(value) => handleChange('regulatory_compliance_cost', value)}
                onBlur={() => handleBlur('regulatory_compliance_cost')}
                min={0}
                max={0.1}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['enhanced_exit_simulator.regulatory_compliance_cost'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Tax Efficiency Factor"
              intent={errors['enhanced_exit_simulator.tax_efficiency_factor'] ? Intent.DANGER : Intent.NONE}
              helperText="Tax efficiency factor (1.0 = fully efficient)"
            >
              <SimpleNumericInput
                value={enhancedExitSimulator.tax_efficiency_factor}
                onValueChange={(value) => handleChange('tax_efficiency_factor', value)}
                onBlur={() => handleBlur('tax_efficiency_factor')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['enhanced_exit_simulator.tax_efficiency_factor'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>
        </div>

        {/* Segmentation Options */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Segmentation Options</h4>
          <div className="grid grid-cols-3 gap-4">
            <FormGroup
              label="Vintage Segmentation"
              helperText="Segment by loan vintage"
              inline={true}
            >
              <Switch
                checked={enhancedExitSimulator.vintage_segmentation}
                onChange={(e) => handleChange('vintage_segmentation', e.target.checked)}
                label="Enable"
              />
            </FormGroup>

            <FormGroup
              label="LTV Segmentation"
              helperText="Segment by LTV ratio"
              inline={true}
            >
              <Switch
                checked={enhancedExitSimulator.ltv_segmentation}
                onChange={(e) => handleChange('ltv_segmentation', e.target.checked)}
                label="Enable"
              />
            </FormGroup>

            <FormGroup
              label="Zone Segmentation"
              helperText="Segment by risk zone"
              inline={true}
            >
              <Switch
                checked={enhancedExitSimulator.zone_segmentation}
                onChange={(e) => handleChange('zone_segmentation', e.target.checked)}
                label="Enable"
              />
            </FormGroup>
          </div>
        </div>

        {/* Risk Modeling */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Risk Modeling Parameters</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormGroup
              label="VaR Confidence Level"
              intent={errors['enhanced_exit_simulator.var_confidence_level'] ? Intent.DANGER : Intent.NONE}
              helperText="Confidence level for Value-at-Risk"
            >
              <SimpleNumericInput
                value={enhancedExitSimulator.var_confidence_level}
                onValueChange={(value) => handleChange('var_confidence_level', value)}
                onBlur={() => handleBlur('var_confidence_level')}
                min={0.8}
                max={0.99}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['enhanced_exit_simulator.var_confidence_level'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Stress Test Severity"
              intent={errors['enhanced_exit_simulator.stress_test_severity'] ? Intent.DANGER : Intent.NONE}
              helperText="Severity of stress tests (0-1)"
            >
              <SimpleNumericInput
                value={enhancedExitSimulator.stress_test_severity}
                onValueChange={(value) => handleChange('stress_test_severity', value)}
                onBlur={() => handleBlur('stress_test_severity')}
                min={0}
                max={1}
                step={0.05}
                formatter={formatPercentage}
                intent={errors['enhanced_exit_simulator.stress_test_severity'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Tail Risk Threshold"
              intent={errors['enhanced_exit_simulator.tail_risk_threshold'] ? Intent.DANGER : Intent.NONE}
              helperText="Threshold for tail risk events"
            >
              <SimpleNumericInput
                value={enhancedExitSimulator.tail_risk_threshold}
                onValueChange={(value) => handleChange('tail_risk_threshold', value)}
                onBlur={() => handleBlur('tail_risk_threshold')}
                min={0}
                max={0.2}
                step={0.005}
                formatter={formatPercentage}
                intent={errors['enhanced_exit_simulator.tail_risk_threshold'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>
        </div>

        {/* Machine Learning & Analytics */}
        <div>
          <h4 className="text-sm font-semibold mb-3">Machine Learning & Analytics</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormGroup
              label="Use ML Models"
              helperText="Enable machine learning models"
              inline={true}
            >
              <Switch
                checked={enhancedExitSimulator.use_ml_models}
                onChange={(e) => handleChange('use_ml_models', e.target.checked)}
                label="Enable"
              />
            </FormGroup>

            {enhancedExitSimulator.use_ml_models && (
              <>
                <FormGroup
                  label="Feature Importance Threshold"
                  intent={errors['enhanced_exit_simulator.feature_importance_threshold'] ? Intent.DANGER : Intent.NONE}
                  helperText="Threshold for important features"
                >
                  <SimpleNumericInput
                    value={enhancedExitSimulator.feature_importance_threshold}
                    onValueChange={(value) => handleChange('feature_importance_threshold', value)}
                    onBlur={() => handleBlur('feature_importance_threshold')}
                    min={0}
                    max={1}
                    step={0.01}
                    formatter={formatPercentage}
                    intent={errors['enhanced_exit_simulator.feature_importance_threshold'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>

                <FormGroup
                  label="Anomaly Detection Threshold"
                  intent={errors['enhanced_exit_simulator.anomaly_detection_threshold'] ? Intent.DANGER : Intent.NONE}
                  helperText="Standard deviations for anomaly detection"
                >
                  <SimpleNumericInput
                    value={enhancedExitSimulator.anomaly_detection_threshold}
                    onValueChange={(value) => handleChange('anomaly_detection_threshold', value)}
                    onBlur={() => handleBlur('anomaly_detection_threshold')}
                    min={1}
                    max={5}
                    step={0.1}
                    formatter={value => `${value.toFixed(1)}σ`}
                    intent={errors['enhanced_exit_simulator.anomaly_detection_threshold'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>
              </>
            )}
          </div>
        </div>

        {/* Help Information */}
        <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
          <h4 className="font-semibold mb-2">Enhanced Exit Simulator Information</h4>
          <p>Advanced modeling for more realistic exit behavior:</p>
          <ul className="list-disc pl-5 space-y-1 mt-2">
            <li><strong>Behavioral Factors:</strong> Life events and herd behavior effects</li>
            <li><strong>Economic Sensitivity:</strong> Recession, inflation, employment impacts</li>
            <li><strong>Segmentation:</strong> Different behavior by vintage, LTV, and zone</li>
            <li><strong>ML Models:</strong> Machine learning for pattern recognition and anomaly detection</li>
          </ul>
        </div>
      </div>
    </Card>
  );
};

export default EnhancedExitSimulator;
