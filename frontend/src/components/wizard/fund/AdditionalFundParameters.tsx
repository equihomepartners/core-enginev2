import React from 'react';
import { FormGroup, Intent } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface AdditionalFundParametersProps {
  additionalParams: {
    reinvestment_period: number;
    loan_size_std_dev: number;
    ltv_std_dev: number;
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const AdditionalFundParameters: React.FC<AdditionalFundParametersProps> = ({
  additionalParams,
  onChange,
  onBlur,
  errors
}) => {
  const handleChange = (field: string, value: any) => {
    onChange(field, value);
  };

  const handleBlur = (field: string) => {
    onBlur(field);
  };

  return (
    <div className="space-y-6">
      {/* Statistical Parameters */}
      <Card
        title="Statistical Parameters"
        icon="variable"
        subtitle="Configure statistical distributions for loan parameters"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <FormGroup
              label="Reinvestment Period (Years)"
              intent={errors['reinvestment_period'] ? Intent.DANGER : Intent.NONE}
              helperText="Period during which capital can be reinvested"
            >
              <SimpleNumericInput
                value={additionalParams.reinvestment_period}
                onValueChange={(value) => handleChange('reinvestment_period', value)}
                onBlur={() => handleBlur('reinvestment_period')}
                min={0}
                max={20}
                step={0.5}
                formatter={value => `${value} years`}
                intent={errors['reinvestment_period'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Loan Size Standard Deviation"
              intent={errors['loan_size_std_dev'] ? Intent.DANGER : Intent.NONE}
              helperText="Standard deviation of loan sizes"
            >
              <SimpleNumericInput
                value={additionalParams.loan_size_std_dev}
                onValueChange={(value) => handleChange('loan_size_std_dev', value)}
                onBlur={() => handleBlur('loan_size_std_dev')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['loan_size_std_dev'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="LTV Standard Deviation"
              intent={errors['ltv_std_dev'] ? Intent.DANGER : Intent.NONE}
              helperText="Standard deviation of LTV ratios"
            >
              <SimpleNumericInput
                value={additionalParams.ltv_std_dev}
                onValueChange={(value) => handleChange('ltv_std_dev', value)}
                onBlur={() => handleBlur('ltv_std_dev')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['ltv_std_dev'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>

          {/* Statistical Summary */}
          <div className="bg-blue-50 p-3 rounded-md text-sm">
            <h5 className="font-medium mb-2">Statistical Distribution Summary</h5>
            <div className="grid grid-cols-3 gap-3 text-xs">
              <div>
                <div className="text-gray-600">Reinvestment Period</div>
                <div className="font-medium">{additionalParams.reinvestment_period} years</div>
              </div>
              <div>
                <div className="text-gray-600">Loan Size Variation</div>
                <div className="font-medium">{formatPercentage(additionalParams.loan_size_std_dev)} std dev</div>
              </div>
              <div>
                <div className="text-gray-600">LTV Variation</div>
                <div className="font-medium">{formatPercentage(additionalParams.ltv_std_dev)} std dev</div>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Help Information */}
      <div className="p-4 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Additional Fund Parameters Information</h4>
        <p>Configure additional statistical and operational parameters:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Reinvestment Period:</strong> Time period during which capital can be reinvested in new loans</li>
          <li><strong>Loan Size Std Dev:</strong> Controls variation in individual loan sizes around the average</li>
          <li><strong>LTV Std Dev:</strong> Controls variation in LTV ratios around the average</li>
        </ul>
        <p className="mt-2 text-xs text-gray-600">
          These parameters control the statistical distributions used in loan generation and portfolio modeling.
        </p>
      </div>
    </div>
  );
};

export default AdditionalFundParameters;
