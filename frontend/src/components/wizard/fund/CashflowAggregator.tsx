import React from 'react';
import { FormGroup, Intent, Switch, HTMLSelect, Button } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface CashflowAggregatorProps {
  cashflowAggregator: {
    time_granularity: 'daily' | 'monthly' | 'quarterly' | 'yearly';
    include_loan_level_cashflows: boolean;
    include_fund_level_cashflows: boolean;
    include_stakeholder_cashflows: boolean;
    simple_interest_rate: number;
    origination_fee_rate: number;
    appreciation_share_method: 'pro_rata_ltv' | 'tiered' | 'fixed';
    distribution_frequency: 'monthly' | 'quarterly' | 'semi_annual' | 'annual';
    distribution_lag: number;
    enable_parallel_processing: boolean;
    num_workers: number;
    enable_scenario_analysis: boolean;
    scenarios: Array<{
      name: string;
      description: string;
      parameters: Record<string, any>;
    }>;
    enable_sensitivity_analysis: boolean;
    sensitivity_parameters: Array<{
      parameter: string;
      min_value: number;
      max_value: number;
      step_size: number;
    }>;
    enable_cashflow_metrics: boolean;
    discount_rate: number;
    enable_tax_impact_analysis: boolean;
    tax_rates: {
      ordinary_income: number;
      capital_gains: number;
    };
    enable_reinvestment_modeling: boolean;
    reinvestment_rate: number;
    enable_liquidity_analysis: boolean;
    minimum_cash_reserve: number;
    enable_export: boolean;
    export_formats: Array<'csv' | 'excel' | 'pdf' | 'json'>;
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const CashflowAggregator: React.FC<CashflowAggregatorProps> = ({
  cashflowAggregator,
  onChange,
  onBlur,
  errors
}) => {
  const handleChange = (field: string, value: any) => {
    onChange(`cashflow_aggregator.${field}`, value);
  };

  const handleBlur = (field: string) => {
    onBlur(`cashflow_aggregator.${field}`);
  };

  const handleNestedChange = (field: string, value: any) => {
    onChange(`cashflow_aggregator.${field}`, value);
  };

  const addScenario = () => {
    const newScenario = {
      name: `Scenario ${cashflowAggregator.scenarios.length + 1}`,
      description: 'Custom scenario',
      parameters: {}
    };
    handleChange('scenarios', [...cashflowAggregator.scenarios, newScenario]);
  };

  const removeScenario = (index: number) => {
    const newScenarios = [...cashflowAggregator.scenarios];
    newScenarios.splice(index, 1);
    handleChange('scenarios', newScenarios);
  };

  const updateScenario = (index: number, field: string, value: any) => {
    const newScenarios = [...cashflowAggregator.scenarios];
    newScenarios[index] = {
      ...newScenarios[index],
      [field]: value
    };
    handleChange('scenarios', newScenarios);
  };

  const addSensitivityParameter = () => {
    const newParam = {
      parameter: 'interest_rate',
      min_value: 0.03,
      max_value: 0.08,
      step_size: 0.005
    };
    handleChange('sensitivity_parameters', [...cashflowAggregator.sensitivity_parameters, newParam]);
  };

  const removeSensitivityParameter = (index: number) => {
    const newParams = [...cashflowAggregator.sensitivity_parameters];
    newParams.splice(index, 1);
    handleChange('sensitivity_parameters', newParams);
  };

  const updateSensitivityParameter = (index: number, field: string, value: any) => {
    const newParams = [...cashflowAggregator.sensitivity_parameters];
    newParams[index] = {
      ...newParams[index],
      [field]: value
    };
    handleChange('sensitivity_parameters', newParams);
  };

  return (
    <div className="space-y-6">
      {/* Basic Cashflow Settings */}
      <Card
        title="Cashflow Aggregation"
        icon="timeline-events"
        subtitle="Configure how cashflows are calculated and aggregated"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Time Granularity"
              intent={errors['cashflow_aggregator.time_granularity'] ? Intent.DANGER : Intent.NONE}
              helperText="Time granularity for cashflow aggregation"
            >
              <HTMLSelect
                value={cashflowAggregator.time_granularity}
                onChange={(e) => handleChange('time_granularity', e.target.value)}
                onBlur={() => handleBlur('time_granularity')}
                fill={true}
                options={[
                  { value: 'daily', label: 'Daily' },
                  { value: 'monthly', label: 'Monthly' },
                  { value: 'quarterly', label: 'Quarterly' },
                  { value: 'yearly', label: 'Yearly' }
                ]}
              />
            </FormGroup>

            <FormGroup
              label="Distribution Frequency"
              intent={errors['cashflow_aggregator.distribution_frequency'] ? Intent.DANGER : Intent.NONE}
              helperText="Frequency of distributions to investors"
            >
              <HTMLSelect
                value={cashflowAggregator.distribution_frequency}
                onChange={(e) => handleChange('distribution_frequency', e.target.value)}
                onBlur={() => handleBlur('distribution_frequency')}
                fill={true}
                options={[
                  { value: 'monthly', label: 'Monthly' },
                  { value: 'quarterly', label: 'Quarterly' },
                  { value: 'semi_annual', label: 'Semi-Annual' },
                  { value: 'annual', label: 'Annual' }
                ]}
              />
            </FormGroup>

            <FormGroup
              label="Distribution Lag (Months)"
              intent={errors['cashflow_aggregator.distribution_lag'] ? Intent.DANGER : Intent.NONE}
              helperText="Lag between cashflow receipt and distribution"
            >
              <SimpleNumericInput
                value={cashflowAggregator.distribution_lag}
                onValueChange={(value) => handleChange('distribution_lag', value)}
                onBlur={() => handleBlur('distribution_lag')}
                min={0}
                max={12}
                step={1}
                formatter={value => `${value} months`}
                intent={errors['cashflow_aggregator.distribution_lag'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Appreciation Share Method"
              intent={errors['cashflow_aggregator.appreciation_share_method'] ? Intent.DANGER : Intent.NONE}
              helperText="Method for calculating appreciation share"
            >
              <HTMLSelect
                value={cashflowAggregator.appreciation_share_method}
                onChange={(e) => handleChange('appreciation_share_method', e.target.value)}
                onBlur={() => handleBlur('appreciation_share_method')}
                fill={true}
                options={[
                  { value: 'pro_rata_ltv', label: 'Pro Rata LTV' },
                  { value: 'tiered', label: 'Tiered' },
                  { value: 'fixed', label: 'Fixed' }
                ]}
              />
            </FormGroup>
          </div>

          {/* Cashflow Inclusion Options */}
          <div className="bg-gray-50 p-3 rounded-md">
            <h5 className="font-medium mb-3">Cashflow Inclusion</h5>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <FormGroup
                label="Include Loan-Level Cashflows"
                inline={true}
              >
                <Switch
                  checked={cashflowAggregator.include_loan_level_cashflows}
                  onChange={(e) => handleChange('include_loan_level_cashflows', e.target.checked)}
                  label="Include"
                />
              </FormGroup>

              <FormGroup
                label="Include Fund-Level Cashflows"
                inline={true}
              >
                <Switch
                  checked={cashflowAggregator.include_fund_level_cashflows}
                  onChange={(e) => handleChange('include_fund_level_cashflows', e.target.checked)}
                  label="Include"
                />
              </FormGroup>

              <FormGroup
                label="Include Stakeholder Cashflows"
                inline={true}
              >
                <Switch
                  checked={cashflowAggregator.include_stakeholder_cashflows}
                  onChange={(e) => handleChange('include_stakeholder_cashflows', e.target.checked)}
                  label="Include"
                />
              </FormGroup>
            </div>
          </div>

          {/* Interest and Fee Rates */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Simple Interest Rate"
              intent={errors['cashflow_aggregator.simple_interest_rate'] ? Intent.DANGER : Intent.NONE}
              helperText="Simple interest rate for loans"
            >
              <SimpleNumericInput
                value={cashflowAggregator.simple_interest_rate}
                onValueChange={(value) => handleChange('simple_interest_rate', value)}
                onBlur={() => handleBlur('simple_interest_rate')}
                min={0}
                max={1}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['cashflow_aggregator.simple_interest_rate'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Origination Fee Rate"
              intent={errors['cashflow_aggregator.origination_fee_rate'] ? Intent.DANGER : Intent.NONE}
              helperText="Origination fee rate"
            >
              <SimpleNumericInput
                value={cashflowAggregator.origination_fee_rate}
                onValueChange={(value) => handleChange('origination_fee_rate', value)}
                onBlur={() => handleBlur('origination_fee_rate')}
                min={0}
                max={0.1}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['cashflow_aggregator.origination_fee_rate'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>
        </div>
      </Card>

      {/* Processing and Performance */}
      <Card
        title="Processing & Performance"
        icon="cog"
        subtitle="Configure processing and performance settings"
      >
        <div className="space-y-4">
          <FormGroup
            label="Enable Parallel Processing"
            helperText="Enable parallel processing for loan-level cashflow calculations"
            inline={true}
          >
            <Switch
              checked={cashflowAggregator.enable_parallel_processing}
              onChange={(e) => handleChange('enable_parallel_processing', e.target.checked)}
              label="Enable"
            />
          </FormGroup>

          {cashflowAggregator.enable_parallel_processing && (
            <FormGroup
              label="Number of Workers"
              intent={errors['cashflow_aggregator.num_workers'] ? Intent.DANGER : Intent.NONE}
              helperText="Number of worker processes for parallel processing"
            >
              <SimpleNumericInput
                value={cashflowAggregator.num_workers}
                onValueChange={(value) => handleChange('num_workers', value)}
                onBlur={() => handleBlur('num_workers')}
                min={1}
                max={32}
                step={1}
                formatter={value => `${value} workers`}
                intent={errors['cashflow_aggregator.num_workers'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          )}

          <FormGroup
            label="Enable Cashflow Metrics"
            helperText="Enable cashflow metrics calculation"
            inline={true}
          >
            <Switch
              checked={cashflowAggregator.enable_cashflow_metrics}
              onChange={(e) => handleChange('enable_cashflow_metrics', e.target.checked)}
              label="Enable"
            />
          </FormGroup>

          {cashflowAggregator.enable_cashflow_metrics && (
            <FormGroup
              label="Discount Rate"
              intent={errors['cashflow_aggregator.discount_rate'] ? Intent.DANGER : Intent.NONE}
              helperText="Discount rate for DCF calculations"
            >
              <SimpleNumericInput
                value={cashflowAggregator.discount_rate}
                onValueChange={(value) => handleChange('discount_rate', value)}
                onBlur={() => handleBlur('discount_rate')}
                min={0}
                max={1}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['cashflow_aggregator.discount_rate'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          )}
        </div>
      </Card>

      {/* Tax Impact Analysis */}
      <Card
        title="Tax Impact Analysis"
        icon="calculator"
        subtitle="Configure tax impact analysis settings"
      >
        <div className="space-y-4">
          <FormGroup
            label="Enable Tax Impact Analysis"
            helperText="Enable tax impact analysis for different income types"
            inline={true}
          >
            <Switch
              checked={cashflowAggregator.enable_tax_impact_analysis}
              onChange={(e) => handleChange('enable_tax_impact_analysis', e.target.checked)}
              label="Enable"
            />
          </FormGroup>

          {cashflowAggregator.enable_tax_impact_analysis && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pl-4 border-l-2 border-gray-200">
              <FormGroup
                label="Ordinary Income Tax Rate"
                intent={errors['cashflow_aggregator.tax_rates.ordinary_income'] ? Intent.DANGER : Intent.NONE}
                helperText="Tax rate for ordinary income"
              >
                <SimpleNumericInput
                  value={cashflowAggregator.tax_rates.ordinary_income}
                  onValueChange={(value) => handleNestedChange('tax_rates.ordinary_income', value)}
                  onBlur={() => handleBlur('tax_rates.ordinary_income')}
                  min={0}
                  max={1}
                  step={0.01}
                  formatter={formatPercentage}
                  intent={errors['cashflow_aggregator.tax_rates.ordinary_income'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>

              <FormGroup
                label="Capital Gains Tax Rate"
                intent={errors['cashflow_aggregator.tax_rates.capital_gains'] ? Intent.DANGER : Intent.NONE}
                helperText="Tax rate for capital gains"
              >
                <SimpleNumericInput
                  value={cashflowAggregator.tax_rates.capital_gains}
                  onValueChange={(value) => handleNestedChange('tax_rates.capital_gains', value)}
                  onBlur={() => handleBlur('tax_rates.capital_gains')}
                  min={0}
                  max={1}
                  step={0.01}
                  formatter={formatPercentage}
                  intent={errors['cashflow_aggregator.tax_rates.capital_gains'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </FormGroup>
            </div>
          )}
        </div>
      </Card>

      {/* Reinvestment and Liquidity */}
      <Card
        title="Reinvestment & Liquidity"
        icon="flows"
        subtitle="Configure reinvestment modeling and liquidity analysis"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Reinvestment Modeling */}
            <div>
              <FormGroup
                label="Enable Reinvestment Modeling"
                helperText="Enable reinvestment modeling for cashflows"
                inline={true}
              >
                <Switch
                  checked={cashflowAggregator.enable_reinvestment_modeling}
                  onChange={(e) => handleChange('enable_reinvestment_modeling', e.target.checked)}
                  label="Enable"
                />
              </FormGroup>

              {cashflowAggregator.enable_reinvestment_modeling && (
                <FormGroup
                  label="Reinvestment Rate"
                  intent={errors['cashflow_aggregator.reinvestment_rate'] ? Intent.DANGER : Intent.NONE}
                  helperText="Rate of return on reinvested cashflows"
                >
                  <SimpleNumericInput
                    value={cashflowAggregator.reinvestment_rate}
                    onValueChange={(value) => handleChange('reinvestment_rate', value)}
                    onBlur={() => handleBlur('reinvestment_rate')}
                    min={0}
                    max={1}
                    step={0.001}
                    formatter={formatPercentage}
                    intent={errors['cashflow_aggregator.reinvestment_rate'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>
              )}
            </div>

            {/* Liquidity Analysis */}
            <div>
              <FormGroup
                label="Enable Liquidity Analysis"
                helperText="Enable liquidity analysis for the fund"
                inline={true}
              >
                <Switch
                  checked={cashflowAggregator.enable_liquidity_analysis}
                  onChange={(e) => handleChange('enable_liquidity_analysis', e.target.checked)}
                  label="Enable"
                />
              </FormGroup>

              {cashflowAggregator.enable_liquidity_analysis && (
                <FormGroup
                  label="Minimum Cash Reserve"
                  intent={errors['cashflow_aggregator.minimum_cash_reserve'] ? Intent.DANGER : Intent.NONE}
                  helperText="Minimum cash reserve as % of fund size"
                >
                  <SimpleNumericInput
                    value={cashflowAggregator.minimum_cash_reserve}
                    onValueChange={(value) => handleChange('minimum_cash_reserve', value)}
                    onBlur={() => handleBlur('minimum_cash_reserve')}
                    min={0}
                    max={1}
                    step={0.01}
                    formatter={formatPercentage}
                    intent={errors['cashflow_aggregator.minimum_cash_reserve'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>
              )}
            </div>
          </div>
        </div>
      </Card>

      {/* Export Settings */}
      <Card
        title="Export Settings"
        icon="export"
        subtitle="Configure export capabilities and formats"
      >
        <div className="space-y-4">
          <FormGroup
            label="Enable Export"
            helperText="Enable export capabilities for results"
            inline={true}
          >
            <Switch
              checked={cashflowAggregator.enable_export}
              onChange={(e) => handleChange('enable_export', e.target.checked)}
              label="Enable"
            />
          </FormGroup>

          {cashflowAggregator.enable_export && (
            <div className="pl-4 border-l-2 border-gray-200">
              <FormGroup
                label="Export Formats"
                helperText="Select the formats for exporting results"
              >
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {['csv', 'excel', 'pdf', 'json'].map((format) => (
                    <label key={format} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={cashflowAggregator.export_formats.includes(format as any)}
                        onChange={(e) => {
                          const newFormats = e.target.checked
                            ? [...cashflowAggregator.export_formats, format]
                            : cashflowAggregator.export_formats.filter(f => f !== format);
                          handleChange('export_formats', newFormats);
                        }}
                        className="form-checkbox"
                      />
                      <span className="text-sm capitalize">{format}</span>
                    </label>
                  ))}
                </div>
              </FormGroup>
            </div>
          )}
        </div>
      </Card>

      {/* Help Information */}
      <div className="p-4 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Cashflow Aggregator Information</h4>
        <p>Configure how cashflows are calculated, aggregated, and analyzed:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Time Granularity:</strong> How frequently cashflows are calculated and aggregated</li>
          <li><strong>Distribution Settings:</strong> Frequency and timing of investor distributions</li>
          <li><strong>Appreciation Share:</strong> Method for calculating fund's share of property appreciation</li>
          <li><strong>Parallel Processing:</strong> Use multiple workers for faster calculations</li>
          <li><strong>Tax Analysis:</strong> Model tax impact on different types of income</li>
          <li><strong>Reinvestment:</strong> Model returns on reinvested cashflows</li>
          <li><strong>Liquidity Analysis:</strong> Analyze fund liquidity and cash reserves</li>
          <li><strong>Export:</strong> Export results in various formats for analysis</li>
        </ul>
      </div>
    </div>
  );
};

export default CashflowAggregator;
