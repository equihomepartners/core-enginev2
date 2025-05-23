import React from 'react';
import { FormGroup, Slider, Intent, Tag, Tooltip } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface LtvParametersProps {
  avgLoanLtv: number;
  minLtv: number;
  maxLtv: number;
  ltvStdDev: number;
  onChange: (field: string, value: number) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
  getGuardrailStatus: (field: string) => { status: 'success' | 'warning' | 'danger', message: string };
}

const LtvParameters: React.FC<LtvParametersProps> = ({
  avgLoanLtv,
  minLtv,
  maxLtv,
  ltvStdDev,
  onChange,
  onBlur,
  errors,
  getGuardrailStatus
}) => {
  return (
    <Card
      title="LTV Parameters"
      icon="percentage"
      subtitle="Configure loan-to-value parameters"
    >
      {/* Average LTV */}
      <FormGroup
        label="Average LTV"
        intent={errors.avg_loan_ltv ? Intent.DANGER : Intent.NONE}
        helperText={errors.avg_loan_ltv || "Target average loan-to-value ratio"}
      >
        <div className="flex items-center space-x-4">
          <Slider
            min={0.1}
            max={0.9}
            stepSize={0.01}
            labelStepSize={0.2}
            value={avgLoanLtv}
            onChange={(value) => onChange('avg_loan_ltv', value)}
            onRelease={() => onBlur('avg_loan_ltv')}
            labelRenderer={value => formatPercentage(value)}
            intent={errors.avg_loan_ltv ? Intent.DANGER : Intent.PRIMARY}
            className="flex-grow"
          />
          <div className="w-20 text-right">
            {formatPercentage(avgLoanLtv)}
          </div>
        </div>
      </FormGroup>

      {/* Min LTV */}
      <FormGroup
        label="Minimum LTV"
        intent={errors.min_ltv ? Intent.DANGER : Intent.NONE}
        helperText={errors.min_ltv || "Minimum loan-to-value ratio"}
      >
        <SimpleNumericInput
          value={minLtv}
          onValueChange={(value) => onChange('min_ltv', value)}
          onBlur={() => onBlur('min_ltv')}
          min={0}
          max={avgLoanLtv}
          step={0.01}
          formatter={formatPercentage}
          intent={errors.min_ltv ? Intent.DANGER : Intent.NONE}
          fill={true}
        />
      </FormGroup>

      {/* Max LTV */}
      <FormGroup
        label="Maximum LTV"
        intent={errors.max_ltv ? Intent.DANGER : Intent.NONE}
        helperText={errors.max_ltv || "Maximum loan-to-value ratio"}
      >
        <SimpleNumericInput
          value={maxLtv}
          onValueChange={(value) => onChange('max_ltv', value)}
          onBlur={() => onBlur('max_ltv')}
          min={avgLoanLtv}
          max={1}
          step={0.01}
          formatter={formatPercentage}
          intent={errors.max_ltv ? Intent.DANGER : Intent.NONE}
          fill={true}
        />
      </FormGroup>

      {/* LTV Standard Deviation */}
      <FormGroup
        label="LTV Standard Deviation"
        intent={errors.ltv_std_dev ? Intent.DANGER : Intent.NONE}
        helperText={errors.ltv_std_dev || "Standard deviation of LTV ratios"}
      >
        <SimpleNumericInput
          value={ltvStdDev}
          onValueChange={(value) => onChange('ltv_std_dev', value)}
          onBlur={() => onBlur('ltv_std_dev')}
          min={0}
          max={0.5}
          step={0.01}
          formatter={formatPercentage}
          intent={errors.ltv_std_dev ? Intent.DANGER : Intent.NONE}
          fill={true}
        />
      </FormGroup>

      {/* Guardrail Status */}
      <div className="mt-4 flex flex-wrap gap-2">
        <Tooltip content={getGuardrailStatus('avg_loan_ltv').message}>
          <Tag
            intent={getGuardrailStatus('avg_loan_ltv').status === 'success' ? Intent.SUCCESS : 
                   getGuardrailStatus('avg_loan_ltv').status === 'warning' ? Intent.WARNING : Intent.DANGER}
            icon={getGuardrailStatus('avg_loan_ltv').status === 'success' ? 'tick' : 'warning-sign'}
          >
            Avg LTV: {formatPercentage(avgLoanLtv)}
          </Tag>
        </Tooltip>
        
        <Tooltip content={getGuardrailStatus('min_ltv').message}>
          <Tag
            intent={getGuardrailStatus('min_ltv').status === 'success' ? Intent.SUCCESS : 
                   getGuardrailStatus('min_ltv').status === 'warning' ? Intent.WARNING : Intent.DANGER}
            icon={getGuardrailStatus('min_ltv').status === 'success' ? 'tick' : 'warning-sign'}
          >
            Min LTV: {formatPercentage(minLtv)}
          </Tag>
        </Tooltip>
        
        <Tooltip content={getGuardrailStatus('max_ltv').message}>
          <Tag
            intent={getGuardrailStatus('max_ltv').status === 'success' ? Intent.SUCCESS : 
                   getGuardrailStatus('max_ltv').status === 'warning' ? Intent.WARNING : Intent.DANGER}
            icon={getGuardrailStatus('max_ltv').status === 'success' ? 'tick' : 'warning-sign'}
          >
            Max LTV: {formatPercentage(maxLtv)}
          </Tag>
        </Tooltip>
      </div>

      {/* Help Information */}
      <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">LTV Parameter Information</h4>
        <p>Loan-to-Value (LTV) ratio is the loan amount divided by the property value:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Average LTV:</strong> Target average across all loans</li>
          <li><strong>Min/Max LTV:</strong> Boundaries for individual loans</li>
          <li><strong>Standard Deviation:</strong> Controls the spread of LTV values</li>
        </ul>
        <p className="mt-2 text-xs text-gray-600">Note: Higher LTV ratios increase risk but may improve returns</p>
      </div>
    </Card>
  );
};

export default LtvParameters;
