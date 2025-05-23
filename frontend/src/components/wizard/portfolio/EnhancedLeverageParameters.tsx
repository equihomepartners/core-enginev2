import React from 'react';
import { FormGroup, Intent, Switch } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface EnhancedLeverageParametersProps {
  enhancedLeverage: {
    term_years: number;
    amortization_years: number;
    interest_only_period: number;
    prepayment_penalty: number;
    prepayment_lockout: number;
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const EnhancedLeverageParameters: React.FC<EnhancedLeverageParametersProps> = ({
  enhancedLeverage,
  onChange,
  onBlur,
  errors
}) => {
  const handleChange = (field: string, value: any) => {
    onChange(`enhanced_leverage.${field}`, value);
  };

  const handleBlur = (field: string) => {
    onBlur(`enhanced_leverage.${field}`);
  };

  return (
    <div className="space-y-6">
      {/* Enhanced NAV Line Parameters */}
      <Card
        title="Enhanced NAV Line Parameters"
        icon="timeline-line-chart"
        subtitle="Advanced term structure and prepayment parameters"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Term (Years)"
              intent={errors['enhanced_leverage.term_years'] ? Intent.DANGER : Intent.NONE}
              helperText="Total term of the NAV facility"
            >
              <SimpleNumericInput
                value={enhancedLeverage.term_years}
                onValueChange={(value) => handleChange('term_years', value)}
                onBlur={() => handleBlur('term_years')}
                min={0}
                max={30}
                step={1}
                formatter={value => `${value} years`}
                intent={errors['enhanced_leverage.term_years'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Amortization Period (Years)"
              intent={errors['enhanced_leverage.amortization_years'] ? Intent.DANGER : Intent.NONE}
              helperText="Amortization period for principal repayment"
            >
              <SimpleNumericInput
                value={enhancedLeverage.amortization_years}
                onValueChange={(value) => handleChange('amortization_years', value)}
                onBlur={() => handleBlur('amortization_years')}
                min={0}
                max={30}
                step={1}
                formatter={value => `${value} years`}
                intent={errors['enhanced_leverage.amortization_years'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Interest-Only Period (Years)"
              intent={errors['enhanced_leverage.interest_only_period'] ? Intent.DANGER : Intent.NONE}
              helperText="Period during which only interest is paid"
            >
              <SimpleNumericInput
                value={enhancedLeverage.interest_only_period}
                onValueChange={(value) => handleChange('interest_only_period', value)}
                onBlur={() => handleBlur('interest_only_period')}
                min={0}
                max={enhancedLeverage.term_years}
                step={0.5}
                formatter={value => `${value} years`}
                intent={errors['enhanced_leverage.interest_only_period'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Prepayment Penalty"
              intent={errors['enhanced_leverage.prepayment_penalty'] ? Intent.DANGER : Intent.NONE}
              helperText="Penalty for early prepayment as % of outstanding balance"
            >
              <SimpleNumericInput
                value={enhancedLeverage.prepayment_penalty}
                onValueChange={(value) => handleChange('prepayment_penalty', value)}
                onBlur={() => handleBlur('prepayment_penalty')}
                min={0}
                max={0.1}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['enhanced_leverage.prepayment_penalty'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Prepayment Lockout (Years)"
              intent={errors['enhanced_leverage.prepayment_lockout'] ? Intent.DANGER : Intent.NONE}
              helperText="Period during which prepayment is not allowed"
            >
              <SimpleNumericInput
                value={enhancedLeverage.prepayment_lockout}
                onValueChange={(value) => handleChange('prepayment_lockout', value)}
                onBlur={() => handleBlur('prepayment_lockout')}
                min={0}
                max={enhancedLeverage.term_years}
                step={0.5}
                formatter={value => `${value} years`}
                intent={errors['enhanced_leverage.prepayment_lockout'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>

          {/* Term Structure Summary */}
          <div className="bg-green-50 p-3 rounded-md text-sm">
            <h5 className="font-medium mb-2">Term Structure Summary</h5>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-xs">
              <div>
                <div className="text-gray-600">Total Term</div>
                <div className="font-medium">{enhancedLeverage.term_years} years</div>
              </div>
              <div>
                <div className="text-gray-600">Amortization</div>
                <div className="font-medium">{enhancedLeverage.amortization_years} years</div>
              </div>
              <div>
                <div className="text-gray-600">Interest-Only</div>
                <div className="font-medium">{enhancedLeverage.interest_only_period} years</div>
              </div>
              <div>
                <div className="text-gray-600">Prepay Penalty</div>
                <div className="font-medium">{formatPercentage(enhancedLeverage.prepayment_penalty)}</div>
              </div>
              <div>
                <div className="text-gray-600">Prepay Lockout</div>
                <div className="font-medium">{enhancedLeverage.prepayment_lockout} years</div>
              </div>
            </div>
          </div>

          {/* Payment Schedule Visualization */}
          <div className="bg-gray-50 p-3 rounded-md text-sm">
            <h5 className="font-medium mb-2">Payment Schedule</h5>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between">
                <span>Years 0 - {enhancedLeverage.interest_only_period}:</span>
                <span className="font-medium">Interest-Only Payments</span>
              </div>
              {enhancedLeverage.interest_only_period < enhancedLeverage.term_years && (
                <div className="flex justify-between">
                  <span>Years {enhancedLeverage.interest_only_period} - {enhancedLeverage.term_years}:</span>
                  <span className="font-medium">
                    {enhancedLeverage.amortization_years > enhancedLeverage.term_years 
                      ? 'Balloon Payment at Maturity' 
                      : 'Principal + Interest Payments'}
                  </span>
                </div>
              )}
              <div className="flex justify-between">
                <span>Prepayment Restrictions:</span>
                <span className="font-medium">
                  {enhancedLeverage.prepayment_lockout > 0 
                    ? `Locked out for ${enhancedLeverage.prepayment_lockout} years, then ${formatPercentage(enhancedLeverage.prepayment_penalty)} penalty`
                    : `${formatPercentage(enhancedLeverage.prepayment_penalty)} penalty`}
                </span>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Help Information */}
      <div className="p-4 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Enhanced Leverage Parameters Information</h4>
        <p>Configure advanced term structure and prepayment features:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Term:</strong> Total maturity of the facility</li>
          <li><strong>Amortization:</strong> Period over which principal is repaid (can be longer than term for balloon)</li>
          <li><strong>Interest-Only Period:</strong> Initial period with no principal payments</li>
          <li><strong>Prepayment Penalty:</strong> Cost of early repayment as percentage of outstanding balance</li>
          <li><strong>Prepayment Lockout:</strong> Period during which prepayment is prohibited</li>
        </ul>
        <p className="mt-2 text-xs text-gray-600">
          These parameters control the detailed payment structure and prepayment options for the NAV facility.
        </p>
      </div>
    </div>
  );
};

export default EnhancedLeverageParameters;
