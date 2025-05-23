import React from 'react';
import { FormGroup, Intent, Slider } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface LoanTermsProps {
  avgLoanTerm: number;
  avgLoanInterestRate: number;
  onChange: (field: string, value: number) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const LoanTerms: React.FC<LoanTermsProps> = ({
  avgLoanTerm,
  avgLoanInterestRate,
  onChange,
  onBlur,
  errors
}) => {
  return (
    <Card
      title="Loan Terms"
      icon="time"
      subtitle="Configure loan term and interest rate"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Average Loan Term */}
        <FormGroup
          label="Average Loan Term (Years)"
          intent={errors.avg_loan_term ? Intent.DANGER : Intent.NONE}
          helperText={errors.avg_loan_term || "Average loan term in years"}
        >
          <div className="flex items-center space-x-4">
            <Slider
              min={0.5}
              max={10}
              stepSize={0.5}
              labelStepSize={2}
              value={avgLoanTerm}
              onChange={(value) => onChange('avg_loan_term', value)}
              onRelease={() => onBlur('avg_loan_term')}
              labelRenderer={value => `${value}y`}
              intent={errors.avg_loan_term ? Intent.DANGER : Intent.PRIMARY}
              className="flex-grow"
            />
            <div className="w-20 text-right">
              {avgLoanTerm.toFixed(1)} years
            </div>
          </div>
        </FormGroup>

        {/* Average Loan Interest Rate */}
        <FormGroup
          label="Average Loan Interest Rate"
          intent={errors.avg_loan_interest_rate ? Intent.DANGER : Intent.NONE}
          helperText={errors.avg_loan_interest_rate || "Average loan interest rate"}
        >
          <div className="flex items-center space-x-4">
            <Slider
              min={0.01}
              max={0.15}
              stepSize={0.005}
              labelStepSize={0.05}
              value={avgLoanInterestRate}
              onChange={(value) => onChange('avg_loan_interest_rate', value)}
              onRelease={() => onBlur('avg_loan_interest_rate')}
              labelRenderer={value => formatPercentage(value)}
              intent={errors.avg_loan_interest_rate ? Intent.DANGER : Intent.PRIMARY}
              className="flex-grow"
            />
            <div className="w-20 text-right">
              {formatPercentage(avgLoanInterestRate)}
            </div>
          </div>
        </FormGroup>
      </div>

      {/* Help Information */}
      <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Loan Terms Information</h4>
        <p>Configure the basic loan terms for your portfolio:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Average Loan Term:</strong> The average duration of loans in years</li>
          <li><strong>Average Interest Rate:</strong> The average interest rate charged on loans</li>
        </ul>
        <p className="mt-2 text-xs text-gray-600">Note: Longer terms may reduce monthly payments but increase interest costs over the life of the loan</p>
      </div>
    </Card>
  );
};

export default LoanTerms;
