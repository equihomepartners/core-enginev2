import React from 'react';
import { FormGroup, Intent, Tag, Tooltip } from '@blueprintjs/core';
import { formatCurrency } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface LoanSizeParametersProps {
  avgLoanSize: number;
  minLoanSize: number;
  maxLoanSize: number;
  loanSizeStdDev: number;
  onChange: (field: string, value: number) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
  getGuardrailStatus: (field: string) => { status: 'success' | 'warning' | 'danger', message: string };
}

const LoanSizeParameters: React.FC<LoanSizeParametersProps> = ({
  avgLoanSize,
  minLoanSize,
  maxLoanSize,
  loanSizeStdDev,
  onChange,
  onBlur,
  errors,
  getGuardrailStatus
}) => {
  return (
    <Card
      title="Loan Size Parameters"
      icon="dollar"
      subtitle="Configure loan size parameters"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Average Loan Size */}
        <FormGroup
          label="Average Loan Size"
          intent={errors.avg_loan_size ? Intent.DANGER : Intent.NONE}
          helperText={errors.avg_loan_size || "Target average loan size"}
        >
          <SimpleNumericInput
            value={avgLoanSize}
            onValueChange={(value) => onChange('avg_loan_size', value)}
            onBlur={() => onBlur('avg_loan_size')}
            min={10000}
            max={1000000}
            step={10000}
            formatter={formatCurrency}
            intent={errors.avg_loan_size ? Intent.DANGER : Intent.NONE}
            fill={true}
          />
        </FormGroup>

        {/* Loan Size Standard Deviation */}
        <FormGroup
          label="Loan Size Standard Deviation"
          intent={errors.loan_size_std_dev ? Intent.DANGER : Intent.NONE}
          helperText={errors.loan_size_std_dev || "Standard deviation of loan sizes"}
        >
          <SimpleNumericInput
            value={loanSizeStdDev}
            onValueChange={(value) => onChange('loan_size_std_dev', value)}
            onBlur={() => onBlur('loan_size_std_dev')}
            min={0}
            max={500000}
            step={5000}
            formatter={formatCurrency}
            intent={errors.loan_size_std_dev ? Intent.DANGER : Intent.NONE}
            fill={true}
          />
        </FormGroup>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
        {/* Min Loan Size */}
        <FormGroup
          label="Minimum Loan Size"
          intent={errors.min_loan_size ? Intent.DANGER : Intent.NONE}
          helperText={errors.min_loan_size || "Minimum loan size"}
        >
          <SimpleNumericInput
            value={minLoanSize}
            onValueChange={(value) => onChange('min_loan_size', value)}
            onBlur={() => onBlur('min_loan_size')}
            min={1000}
            max={avgLoanSize}
            step={10000}
            formatter={formatCurrency}
            intent={errors.min_loan_size ? Intent.DANGER : Intent.NONE}
            fill={true}
          />
        </FormGroup>

        {/* Max Loan Size */}
        <FormGroup
          label="Maximum Loan Size"
          intent={errors.max_loan_size ? Intent.DANGER : Intent.NONE}
          helperText={errors.max_loan_size || "Maximum loan size"}
        >
          <SimpleNumericInput
            value={maxLoanSize}
            onValueChange={(value) => onChange('max_loan_size', value)}
            onBlur={() => onBlur('max_loan_size')}
            min={avgLoanSize}
            max={10000000}
            step={10000}
            formatter={formatCurrency}
            intent={errors.max_loan_size ? Intent.DANGER : Intent.NONE}
            fill={true}
          />
        </FormGroup>
      </div>

      {/* Guardrail Status */}
      <div className="mt-4 flex flex-wrap gap-2">
        <Tooltip content={getGuardrailStatus('avg_loan_size').message}>
          <Tag
            intent={getGuardrailStatus('avg_loan_size').status === 'success' ? Intent.SUCCESS : 
                   getGuardrailStatus('avg_loan_size').status === 'warning' ? Intent.WARNING : Intent.DANGER}
            icon={getGuardrailStatus('avg_loan_size').status === 'success' ? 'tick' : 'warning-sign'}
          >
            Avg Size: {formatCurrency(avgLoanSize)}
          </Tag>
        </Tooltip>
        
        <Tooltip content={getGuardrailStatus('min_loan_size').message}>
          <Tag
            intent={getGuardrailStatus('min_loan_size').status === 'success' ? Intent.SUCCESS : 
                   getGuardrailStatus('min_loan_size').status === 'warning' ? Intent.WARNING : Intent.DANGER}
            icon={getGuardrailStatus('min_loan_size').status === 'success' ? 'tick' : 'warning-sign'}
          >
            Min Size: {formatCurrency(minLoanSize)}
          </Tag>
        </Tooltip>
        
        <Tooltip content={getGuardrailStatus('max_loan_size').message}>
          <Tag
            intent={getGuardrailStatus('max_loan_size').status === 'success' ? Intent.SUCCESS : 
                   getGuardrailStatus('max_loan_size').status === 'warning' ? Intent.WARNING : Intent.DANGER}
            icon={getGuardrailStatus('max_loan_size').status === 'success' ? 'tick' : 'warning-sign'}
          >
            Max Size: {formatCurrency(maxLoanSize)}
          </Tag>
        </Tooltip>
      </div>

      {/* Help Information */}
      <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Loan Size Information</h4>
        <p>Configure the size distribution of loans in your portfolio:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Average Loan Size:</strong> Target average across all loans</li>
          <li><strong>Min/Max Loan Size:</strong> Boundaries for individual loans</li>
          <li><strong>Standard Deviation:</strong> Controls the spread of loan sizes</li>
        </ul>
        <p className="mt-2 text-xs text-gray-600">Note: Smaller loans may diversify risk but increase operational overhead</p>
      </div>
    </Card>
  );
};

export default LoanSizeParameters;
