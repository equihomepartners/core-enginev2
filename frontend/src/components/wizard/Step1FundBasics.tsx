import React, { useState, useEffect, useRef } from 'react';
import {
  FormGroup,
  InputGroup,
  NumericInput,
  HTMLSelect,
  Callout,
  Icon,
  Tooltip,
  Intent,
  Button,
  Divider
} from '@blueprintjs/core';
import Card from '../layout/Card';
import { useSimulationStore } from '../../store';
import { getFundBasicsDefaults, getFundBasicsValidationSchema } from '../../utils/schemaUtils';
import { formatCurrency, formatPercentage } from '../../utils/formatters';
import TrancheConfig from './TrancheConfig';
import FormattedNumericInput from '../common/FormattedNumericInput';
import SimpleNumericInput from '../common/SimpleNumericInput';
import TrancheManager from './fund/TrancheManager';
import CashflowAggregator from './fund/CashflowAggregator';
import AdditionalFundParameters from './fund/AdditionalFundParameters';

interface ValidationErrors {
  [key: string]: string | undefined;
}

const Step1FundBasics: React.FC = () => {
  const store = useSimulationStore();
  const validationSchema = getFundBasicsValidationSchema();

  // Initialize form state with defaults or existing values
  const [formData, setFormData] = useState(() => {
    const defaults = getFundBasicsDefaults();
    const config = store?.config || {};

    // Ensure all numeric values are within constraints
    const ensureValidNumber = (value: any, min: number, max: number, defaultValue: number): number => {
      if (typeof value !== 'number' || isNaN(value) || value < min || value > max) {
        return defaultValue;
      }
      return value;
    };

    return {
      ...defaults,
      ...config,
      // Ensure fund_name exists with a default if not in config
      fund_name: config.fund_name || defaults.fund_name || 'Equihome Fund I',
      // Ensure numeric values are valid
      fund_size: ensureValidNumber(config.fund_size, 1000000, 10000000000, defaults.fund_size || 100000000),
      fund_term: ensureValidNumber(config.fund_term, 1, 30, defaults.fund_term || 10),
      vintage_year: ensureValidNumber(config.vintage_year, 1900, 2100, defaults.vintage_year || new Date().getFullYear()),
      management_fee_rate: ensureValidNumber(config.management_fee_rate, 0, 0.05, defaults.management_fee_rate || 0.02),
      carried_interest_rate: ensureValidNumber(config.carried_interest_rate, 0, 1, defaults.carried_interest_rate || 0.2),
      hurdle_rate: ensureValidNumber(config.hurdle_rate, 0, 1, defaults.hurdle_rate || 0.08),
      gp_commitment_percentage: ensureValidNumber(config.gp_commitment_percentage, 0, 1, defaults.gp_commitment_percentage || 0),
      catch_up_rate: ensureValidNumber(config.catch_up_rate, 0, 1, defaults.catch_up_rate || 0),
      reinvestment_period: ensureValidNumber(config.reinvestment_period, 0, 30, defaults.reinvestment_period || 5),

      // Fee engine parameters
      fee_engine: {
        ...(defaults.fee_engine || {}),
        ...(config.fee_engine || {}),
        origination_fee_rate: ensureValidNumber(
          config.fee_engine?.origination_fee_rate,
          0,
          0.1,
          defaults.fee_engine?.origination_fee_rate || 0.01
        ),
        annual_fund_expenses: ensureValidNumber(
          config.fee_engine?.annual_fund_expenses,
          0,
          0.05,
          defaults.fee_engine?.annual_fund_expenses || 0.005
        ),
        fixed_annual_expenses: ensureValidNumber(
          config.fee_engine?.fixed_annual_expenses,
          0,
          10000000,
          defaults.fee_engine?.fixed_annual_expenses || 100000
        ),
        setup_costs: ensureValidNumber(
          config.fee_engine?.setup_costs,
          0,
          10000000,
          defaults.fee_engine?.setup_costs || 250000
        ),
        expense_growth_rate: ensureValidNumber(
          config.fee_engine?.expense_growth_rate,
          0,
          0.1,
          defaults.fee_engine?.expense_growth_rate || 0.02
        ),
        acquisition_fee_rate: ensureValidNumber(
          config.fee_engine?.acquisition_fee_rate,
          0,
          0.05,
          defaults.fee_engine?.acquisition_fee_rate || 0
        ),
        disposition_fee_rate: ensureValidNumber(
          config.fee_engine?.disposition_fee_rate,
          0,
          0.05,
          defaults.fee_engine?.disposition_fee_rate || 0
        )
      }
    };
  });

  // Validation state
  const [errors, setErrors] = useState<ValidationErrors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  // Validate form data
  const validateForm = () => {
    const result = validationSchema.safeParse(formData);
    if (!result.success) {
      const formattedErrors: ValidationErrors = {};
      const formattedResult = result.error.format();

      // Extract error messages
      Object.entries(formattedResult).forEach(([key, value]) => {
        if (key !== '_errors' && typeof value === 'object' && '_errors' in value) {
          const errorMessages = value._errors;
          if (errorMessages.length > 0) {
            formattedErrors[key] = errorMessages[0];
          }
        }
      });

      setErrors(formattedErrors);
      return false;
    }

    setErrors({});
    return true;
  };

  // Validate on form data change - use a ref to prevent infinite loops
  const isValidatingRef = useRef(false);

  useEffect(() => {
    if (Object.keys(touched).length > 0 && !isValidatingRef.current) {
      isValidatingRef.current = true;
      validateForm();
      // Reset the flag after a short delay
      setTimeout(() => {
        isValidatingRef.current = false;
      }, 0);
    }
  }, [formData]);

  // Update store when form is valid - use a ref to prevent infinite loops
  const isUpdatingStoreRef = useRef(false);

  useEffect(() => {
    if (Object.keys(errors).length === 0 &&
        Object.keys(touched).length > 0 &&
        store?.setConfig &&
        !isUpdatingStoreRef.current) {
      isUpdatingStoreRef.current = true;
      store.setConfig(formData);
      // Reset the flag after a short delay
      setTimeout(() => {
        isUpdatingStoreRef.current = false;
      }, 0);
    }
  }, [errors, formData]);

  // Handle input changes
  const handleChange = (field: string, value: any) => {
    // Ensure numeric values are within constraints
    let validatedValue = value;

    // Check if this is a fee engine field
    if (field.startsWith('fee_engine.')) {
      const feeField = field.split('.')[1];

      // Special handling for management_fee_schedule which is an array
      if (feeField === 'management_fee_schedule') {
        // Validate each entry in the schedule
        if (Array.isArray(value)) {
          const validatedSchedule = value.map(entry => ({
            year: typeof entry.year === 'number' ? Math.max(0, Math.min(30, Math.round(entry.year))) : 0,
            rate: typeof entry.rate === 'number' ? Math.max(0, Math.min(0.05, entry.rate)) : 0.02
          }));

          // Update the nested fee_engine object
          setFormData(prev => ({
            ...prev,
            fee_engine: {
              ...prev.fee_engine,
              management_fee_schedule: validatedSchedule
            }
          }));
        }
      } else if (typeof value === 'number') {
        // Handle numeric fee engine fields
        switch (feeField) {
          case 'origination_fee_rate':
            validatedValue = Math.max(0, Math.min(0.1, value));
            break;
          case 'annual_fund_expenses':
            validatedValue = Math.max(0, Math.min(0.05, value));
            break;
          case 'fixed_annual_expenses':
          case 'setup_costs':
            validatedValue = Math.max(0, Math.min(10000000, value));
            break;
          case 'expense_growth_rate':
            validatedValue = Math.max(0, Math.min(0.1, value));
            break;
          case 'acquisition_fee_rate':
          case 'disposition_fee_rate':
            validatedValue = Math.max(0, Math.min(0.05, value));
            break;
        }

        // Update the nested fee_engine object
        setFormData(prev => ({
          ...prev,
          fee_engine: {
            ...prev.fee_engine,
            [feeField]: validatedValue
          }
        }));
      }

      setTouched(prev => ({
        ...prev,
        [`fee_engine.${feeField}`]: true
      }));

      return;
    }

    // Handle regular fields
    if (typeof value === 'number') {
      switch (field) {
        case 'fund_size':
          validatedValue = Math.max(1000000, Math.min(10000000000, value));
          break;
        case 'fund_term':
          validatedValue = Math.max(1, Math.min(30, Math.round(value)));
          break;
        case 'vintage_year':
          validatedValue = Math.max(1900, Math.min(2100, Math.round(value)));
          break;
        case 'management_fee_rate':
          validatedValue = Math.max(0, Math.min(0.05, value));
          break;
        case 'carried_interest_rate':
        case 'hurdle_rate':
        case 'gp_commitment_percentage':
        case 'catch_up_rate':
          validatedValue = Math.max(0, Math.min(1, value));
          break;
        case 'reinvestment_period':
          validatedValue = Math.max(0, Math.min(30, Math.round(value)));
          break;
      }
    }

    setFormData(prev => ({ ...prev, [field]: validatedValue }));
    setTouched(prev => ({ ...prev, [field]: true }));
  };

  // Handle nested field changes (for complex objects)
  const handleNestedChange = (field: string, value: any) => {
    const fieldParts = field.split('.');

    setFormData(prev => {
      const newData = { ...prev };
      let current = newData;

      // Navigate to the parent object
      for (let i = 0; i < fieldParts.length - 1; i++) {
        const part = fieldParts[i];
        if (!current[part]) {
          current[part] = {};
        }
        current[part] = { ...current[part] };
        current = current[part];
      }

      // Set the final value
      current[fieldParts[fieldParts.length - 1]] = value;

      return newData;
    });

    setTouched(prev => ({ ...prev, [field]: true }));
  };

  // Handle blur events for validation
  const handleBlur = (field: string) => {
    setTouched(prev => ({ ...prev, [field]: true }));
    validateForm();
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <Card
            title="Fund Basics"
            icon="properties"
            subtitle="Configure the basic parameters of your fund"
          >
            {/* Fund Name */}
            <FormGroup
              label="Fund Name"
              labelInfo="(required)"
              intent={errors.fund_name ? Intent.DANGER : Intent.NONE}
              helperText={errors.fund_name || "Enter a name for your fund"}
            >
              <InputGroup
                id="fund-name"
                value={formData.fund_name || ''}
                onChange={(e) => handleChange('fund_name', e.target.value)}
                onBlur={() => handleBlur('fund_name')}
                intent={errors.fund_name ? Intent.DANGER : Intent.NONE}
                placeholder="Equihome Fund I"
                leftIcon="tag"
              />
            </FormGroup>

            {/* Fund Size */}
            <FormGroup
              label="Fund Size"
              labelInfo="(required)"
              intent={errors.fund_size ? Intent.DANGER : Intent.NONE}
              helperText={errors.fund_size || "Total capital committed to the fund"}
            >
              <SimpleNumericInput
                value={formData.fund_size || 0}
                onValueChange={(valueAsNumber) => handleChange('fund_size', valueAsNumber)}
                onBlur={() => handleBlur('fund_size')}
                intent={errors.fund_size ? Intent.DANGER : Intent.NONE}
                min={1000000}
                max={10000000000}
                step={1000000}
                formatter={formatCurrency}
                fill={true}
              />
            </FormGroup>

            {/* Fund Term */}
            <FormGroup
              label="Fund Term"
              labelInfo="(required)"
              intent={errors.fund_term ? Intent.DANGER : Intent.NONE}
              helperText={errors.fund_term || "Duration of the fund in years"}
            >
              <SimpleNumericInput
                value={formData.fund_term || 0}
                onValueChange={(valueAsNumber) => handleChange('fund_term', valueAsNumber)}
                onBlur={() => handleBlur('fund_term')}
                intent={errors.fund_term ? Intent.DANGER : Intent.NONE}
                min={1}
                max={30}
                step={1}
                fill={true}
              />
            </FormGroup>

            {/* Vintage Year */}
            <FormGroup
              label="Vintage Year"
              labelInfo="(required)"
              intent={errors.vintage_year ? Intent.DANGER : Intent.NONE}
              helperText={errors.vintage_year || "Year the fund was established"}
            >
              <SimpleNumericInput
                value={formData.vintage_year || new Date().getFullYear()}
                onValueChange={(valueAsNumber) => handleChange('vintage_year', valueAsNumber)}
                onBlur={() => handleBlur('vintage_year')}
                intent={errors.vintage_year ? Intent.DANGER : Intent.NONE}
                min={1900}
                max={2100}
                step={1}
                fill={true}
              />
            </FormGroup>

            {/* Reinvestment Period */}
            <FormGroup
              label="Reinvestment Period"
              intent={errors.reinvestment_period ? Intent.DANGER : Intent.NONE}
              helperText={errors.reinvestment_period || "Period during which capital can be recycled"}
            >
              <SimpleNumericInput
                value={formData.reinvestment_period || 0}
                onValueChange={(valueAsNumber) => handleChange('reinvestment_period', valueAsNumber)}
                onBlur={() => handleBlur('reinvestment_period')}
                intent={errors.reinvestment_period ? Intent.DANGER : Intent.NONE}
                min={0}
                max={30}
                step={1}
                fill={true}
              />
            </FormGroup>

            {/* Fund Basics Help */}
            <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
              <h4 className="font-semibold mb-2">Fund Basics Information</h4>
              <p>The fund basics section defines the fundamental parameters of your investment fund:</p>
              <ul className="list-disc pl-5 space-y-1 mt-2">
                <li><strong>Fund Size:</strong> Total capital committed to the fund</li>
                <li><strong>Fund Term:</strong> Duration of the fund in years</li>
                <li><strong>Vintage Year:</strong> Year the fund was established</li>
                <li><strong>Reinvestment Period:</strong> Period during which capital can be recycled</li>
              </ul>
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <Card
            title="Economics"
            icon="bank-account"
            subtitle="Configure the economic terms of your fund"
          >
            {/* Management Fee Rate */}
            <FormGroup
              label="Management Fee Rate"
              intent={errors.management_fee_rate ? Intent.DANGER : Intent.NONE}
              helperText={errors.management_fee_rate || "Annual fee charged by the manager"}
            >
              <SimpleNumericInput
                value={formData.management_fee_rate || 0}
                onValueChange={(valueAsNumber) => handleChange('management_fee_rate', valueAsNumber)}
                onBlur={() => handleBlur('management_fee_rate')}
                intent={errors.management_fee_rate ? Intent.DANGER : Intent.NONE}
                min={0}
                max={0.05}
                step={0.0025}
                formatter={formatPercentage}
                fill={true}
              />
            </FormGroup>

            {/* Management Fee Basis */}
            <FormGroup
              label="Management Fee Basis"
              intent={errors.management_fee_basis ? Intent.DANGER : Intent.NONE}
              helperText={errors.management_fee_basis || "Basis for calculating management fees"}
            >
              <HTMLSelect
                id="management-fee-basis"
                value={formData.management_fee_basis || 'committed_capital'}
                onChange={(e) => handleChange('management_fee_basis', e.target.value)}
                onBlur={() => handleBlur('management_fee_basis')}
                fill={true}
                options={[
                  { value: 'committed_capital', label: 'Committed Capital' },
                  { value: 'invested_capital', label: 'Invested Capital' },
                  { value: 'net_asset_value', label: 'Net Asset Value' }
                ]}
              />
            </FormGroup>

            {/* Carried Interest Rate */}
            <FormGroup
              label="Carried Interest Rate"
              intent={errors.carried_interest_rate ? Intent.DANGER : Intent.NONE}
              helperText={errors.carried_interest_rate || "Percentage of profits paid to the manager"}
            >
              <SimpleNumericInput
                value={formData.carried_interest_rate || 0}
                onValueChange={(valueAsNumber) => handleChange('carried_interest_rate', valueAsNumber)}
                onBlur={() => handleBlur('carried_interest_rate')}
                intent={errors.carried_interest_rate ? Intent.DANGER : Intent.NONE}
                min={0}
                max={1}
                step={0.05}
                formatter={formatPercentage}
                fill={true}
              />
            </FormGroup>

            {/* Hurdle Rate */}
            <FormGroup
              label="Hurdle Rate"
              intent={errors.hurdle_rate ? Intent.DANGER : Intent.NONE}
              helperText={errors.hurdle_rate || "Minimum return before carried interest is paid"}
            >
              <SimpleNumericInput
                value={formData.hurdle_rate || 0}
                onValueChange={(valueAsNumber) => handleChange('hurdle_rate', valueAsNumber)}
                onBlur={() => handleBlur('hurdle_rate')}
                intent={errors.hurdle_rate ? Intent.DANGER : Intent.NONE}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                fill={true}
              />
            </FormGroup>

            {/* Waterfall Structure */}
            <FormGroup
              label="Waterfall Structure"
              intent={errors.waterfall_structure ? Intent.DANGER : Intent.NONE}
              helperText={errors.waterfall_structure || "Method for distributing profits"}
            >
              <HTMLSelect
                id="waterfall-structure"
                value={formData.waterfall_structure || 'european'}
                onChange={(e) => handleChange('waterfall_structure', e.target.value)}
                onBlur={() => handleBlur('waterfall_structure')}
                fill={true}
                options={[
                  { value: 'european', label: 'European (Deal-by-Deal)' },
                  { value: 'american', label: 'American (Whole Fund)' }
                ]}
              />
            </FormGroup>

            {/* GP Commitment */}
            <FormGroup
              label="GP Commitment"
              intent={errors.gp_commitment_percentage ? Intent.DANGER : Intent.NONE}
              helperText={errors.gp_commitment_percentage || "Percentage of fund committed by the GP"}
            >
              <SimpleNumericInput
                value={formData.gp_commitment_percentage || 0}
                onValueChange={(valueAsNumber) => handleChange('gp_commitment_percentage', valueAsNumber)}
                onBlur={() => handleBlur('gp_commitment_percentage')}
                intent={errors.gp_commitment_percentage ? Intent.DANGER : Intent.NONE}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                fill={true}
              />
            </FormGroup>

            {/* Catch-up Rate */}
            <FormGroup
              label="Catch-up Rate"
              intent={errors.catch_up_rate ? Intent.DANGER : Intent.NONE}
              helperText={errors.catch_up_rate || "Rate at which GP catches up after hurdle is met"}
            >
              <SimpleNumericInput
                value={formData.catch_up_rate || 0}
                onValueChange={(valueAsNumber) => handleChange('catch_up_rate', valueAsNumber)}
                onBlur={() => handleBlur('catch_up_rate')}
                intent={errors.catch_up_rate ? Intent.DANGER : Intent.NONE}
                min={0}
                max={1}
                step={0.1}
                formatter={formatPercentage}
                fill={true}
              />
            </FormGroup>

            {/* Economics Help */}
            <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
              <h4 className="font-semibold mb-2">Economics Information</h4>
              <p>The economics section defines how profits are distributed between the general partner (GP) and limited partners (LPs):</p>
              <ul className="list-disc pl-5 mt-2 space-y-1">
                <li><strong>Management Fee:</strong> Annual fee charged by the GP</li>
                <li><strong>Carried Interest:</strong> Percentage of profits paid to the GP</li>
                <li><strong>Hurdle Rate:</strong> Minimum return before carried interest is paid</li>
                <li><strong>Waterfall:</strong> Method for distributing profits</li>
                <li><strong>GP Commitment:</strong> Percentage of fund committed by the GP</li>
                <li><strong>Catch-up Rate:</strong> Rate at which GP catches up after hurdle is met</li>
              </ul>
            </div>
          </Card>
        </div>
      </div>

      {/* Fee Engine Configuration */}
      <Card
        title="Fee Structure"
        icon="dollar"
        subtitle="Configure the fee structure of your fund"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Origination Fee Rate */}
          <FormGroup
            label="Origination Fee Rate"
          >
            <SimpleNumericInput
              value={formData.fee_engine?.origination_fee_rate || 0}
              onValueChange={(valueAsNumber) => handleChange('fee_engine.origination_fee_rate', valueAsNumber)}
              onBlur={() => handleBlur('fee_engine.origination_fee_rate')}
              min={0}
              max={0.1}
              step={0.005}
              formatter={formatPercentage}
              fill={true}
            />
          </FormGroup>

          {/* Annual Fund Expenses */}
          <FormGroup
            label="Annual Fund Expenses"
          >
            <SimpleNumericInput
              value={formData.fee_engine?.annual_fund_expenses || 0}
              onValueChange={(valueAsNumber) => handleChange('fee_engine.annual_fund_expenses', valueAsNumber)}
              onBlur={() => handleBlur('fee_engine.annual_fund_expenses')}
              min={0}
              max={0.05}
              step={0.001}
              formatter={formatPercentage}
              fill={true}
            />
          </FormGroup>

          {/* Fixed Annual Expenses */}
          <FormGroup
            label="Fixed Annual Expenses"
          >
            <SimpleNumericInput
              value={formData.fee_engine?.fixed_annual_expenses || 0}
              onValueChange={(valueAsNumber) => handleChange('fee_engine.fixed_annual_expenses', valueAsNumber)}
              onBlur={() => handleBlur('fee_engine.fixed_annual_expenses')}
              min={0}
              max={10000000}
              step={10000}
              formatter={formatCurrency}
              fill={true}
            />
          </FormGroup>

          {/* Setup Costs */}
          <FormGroup
            label="Setup Costs"
          >
            <SimpleNumericInput
              value={formData.fee_engine?.setup_costs || 0}
              onValueChange={(valueAsNumber) => handleChange('fee_engine.setup_costs', valueAsNumber)}
              onBlur={() => handleBlur('fee_engine.setup_costs')}
              min={0}
              max={10000000}
              step={10000}
              formatter={formatCurrency}
              fill={true}
            />
          </FormGroup>

          {/* Expense Growth Rate */}
          <FormGroup
            label="Expense Growth Rate"
          >
            <SimpleNumericInput
              value={formData.fee_engine?.expense_growth_rate || 0}
              onValueChange={(valueAsNumber) => handleChange('fee_engine.expense_growth_rate', valueAsNumber)}
              onBlur={() => handleBlur('fee_engine.expense_growth_rate')}
              min={0}
              max={0.1}
              step={0.005}
              formatter={formatPercentage}
              fill={true}
            />
          </FormGroup>

          {/* Acquisition Fee Rate */}
          <FormGroup
            label="Acquisition Fee Rate"
          >
            <SimpleNumericInput
              value={formData.fee_engine?.acquisition_fee_rate || 0}
              onValueChange={(valueAsNumber) => handleChange('fee_engine.acquisition_fee_rate', valueAsNumber)}
              onBlur={() => handleBlur('fee_engine.acquisition_fee_rate')}
              min={0}
              max={0.05}
              step={0.005}
              formatter={formatPercentage}
              fill={true}
            />
          </FormGroup>

          {/* Disposition Fee Rate */}
          <FormGroup
            label="Disposition Fee Rate"
          >
            <SimpleNumericInput
              value={formData.fee_engine?.disposition_fee_rate || 0}
              onValueChange={(valueAsNumber) => handleChange('fee_engine.disposition_fee_rate', valueAsNumber)}
              onBlur={() => handleBlur('fee_engine.disposition_fee_rate')}
              min={0}
              max={0.05}
              step={0.005}
              formatter={formatPercentage}
              fill={true}
            />
          </FormGroup>
        </div>

        {/* Management Fee Schedule */}
        <div className="mt-4">
          <FormGroup
            label="Management Fee Schedule"
          >
            <div className="mb-2">
              <Button
                icon="plus"
                intent="primary"
                onClick={() => {
                  const currentSchedule = formData.fee_engine?.management_fee_schedule || [];
                  const nextYear = currentSchedule.length > 0
                    ? Math.max(...currentSchedule.map(item => item.year)) + 1
                    : 0;

                  handleChange('fee_engine.management_fee_schedule', [
                    ...currentSchedule,
                    { year: nextYear, rate: 0.02 }
                  ]);
                }}
              >
                Add Fee Schedule Entry
              </Button>
            </div>

            {(formData.fee_engine?.management_fee_schedule || []).length === 0 && (
              <div className="text-gray-500 italic">No management fee schedule entries. The default management fee rate will be used.</div>
            )}

            {(formData.fee_engine?.management_fee_schedule || []).map((entry, index) => (
              <div key={index} className="flex items-center gap-2 mb-2">
                <FormGroup
                  label="Year"
                  inline={true}
                  className="mb-0 flex-1"
                >
                  <SimpleNumericInput
                    value={entry.year}
                    onValueChange={(valueAsNumber) => {
                      const newSchedule = [...(formData.fee_engine?.management_fee_schedule || [])];
                      newSchedule[index] = { ...newSchedule[index], year: Math.max(0, Math.round(valueAsNumber)) };
                      handleChange('fee_engine.management_fee_schedule', newSchedule);
                    }}
                    min={0}
                    max={30}
                    step={1}
                    fill={true}
                  />
                </FormGroup>

                <FormGroup
                  label="Rate"
                  inline={true}
                  className="mb-0 flex-1"
                >
                  <SimpleNumericInput
                    value={entry.rate}
                    onValueChange={(valueAsNumber) => {
                      const newSchedule = [...(formData.fee_engine?.management_fee_schedule || [])];
                      newSchedule[index] = { ...newSchedule[index], rate: Math.max(0, Math.min(0.05, valueAsNumber)) };
                      handleChange('fee_engine.management_fee_schedule', newSchedule);
                    }}
                    min={0}
                    max={0.05}
                    step={0.005}
                    formatter={formatPercentage}
                    fill={true}
                  />
                </FormGroup>

                <Button
                  icon="trash"
                  intent="danger"
                  onClick={() => {
                    const newSchedule = [...(formData.fee_engine?.management_fee_schedule || [])];
                    newSchedule.splice(index, 1);
                    handleChange('fee_engine.management_fee_schedule', newSchedule);
                  }}
                />
              </div>
            ))}
          </FormGroup>
        </div>

        {/* Help Text Section */}
        <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
          <h4 className="font-semibold mb-2">Fee Structure Information</h4>
          <ul className="list-disc pl-5 space-y-1">
            <li><strong>Origination Fee Rate:</strong> Fee charged when a loan is originated (0-10%)</li>
            <li><strong>Annual Fund Expenses:</strong> Annual expenses as percentage of fund size (0-5%)</li>
            <li><strong>Fixed Annual Expenses:</strong> Fixed annual expenses in dollars</li>
            <li><strong>Setup Costs:</strong> One-time setup costs in dollars</li>
            <li><strong>Expense Growth Rate:</strong> Annual growth rate for expenses (0-10%)</li>
            <li><strong>Acquisition Fee Rate:</strong> Fee charged when a property is acquired (0-5%)</li>
            <li><strong>Disposition Fee Rate:</strong> Fee charged when a property is sold (0-5%)</li>
            <li><strong>Management Fee Schedule:</strong> Optional year-by-year management fee rates. If not specified, the default management fee rate will be used.</li>
          </ul>
        </div>
      </Card>

      {/* Tranche Manager */}
      <TrancheManager
        trancheManager={formData.tranche_manager || {
          enabled: false,
          tranches: [],
          reserve_account: {
            enabled: false,
            target_percentage: 0.05,
            initial_funding: 0.03,
            replenishment_rate: 0.1
          },
          overcollateralization_test: {
            enabled: false,
            threshold: 1.2,
            test_frequency: 'quarterly',
            cure_period_months: 3
          },
          interest_coverage_test: {
            enabled: false,
            threshold: 1.5,
            test_frequency: 'quarterly',
            cure_period_months: 3
          }
        }}
        onChange={handleNestedChange}
        onBlur={handleBlur}
        errors={errors}
      />

      {/* Cashflow Aggregator */}
      <CashflowAggregator
        cashflowAggregator={formData.cashflow_aggregator || {
          time_granularity: 'monthly',
          include_loan_level_cashflows: true,
          include_fund_level_cashflows: true,
          include_stakeholder_cashflows: true,
          simple_interest_rate: 0.05,
          origination_fee_rate: 0.01,
          appreciation_share_method: 'pro_rata_ltv',
          distribution_frequency: 'quarterly',
          distribution_lag: 1,
          enable_parallel_processing: false,
          num_workers: 4,
          enable_scenario_analysis: false,
          scenarios: [],
          enable_sensitivity_analysis: false,
          sensitivity_parameters: [],
          enable_cashflow_metrics: true,
          discount_rate: 0.08,
          enable_tax_impact_analysis: false,
          tax_rates: {
            ordinary_income: 0.37,
            capital_gains: 0.20
          },
          enable_reinvestment_modeling: false,
          reinvestment_rate: 0.05,
          enable_liquidity_analysis: false,
          minimum_cash_reserve: 0.05,
          enable_export: true,
          export_formats: ['csv', 'excel']
        }}
        onChange={handleNestedChange}
        onBlur={handleBlur}
        errors={errors}
      />

      {/* Additional Fund Parameters */}
      <AdditionalFundParameters
        additionalParams={{
          reinvestment_period: formData.reinvestment_period || 5,
          loan_size_std_dev: formData.loan_size_std_dev || 0.2,
          ltv_std_dev: formData.ltv_std_dev || 0.1,
        }}
        onChange={handleChange}
        onBlur={handleBlur}
        errors={errors}
      />
    </div>
  );
};

export default Step1FundBasics;
