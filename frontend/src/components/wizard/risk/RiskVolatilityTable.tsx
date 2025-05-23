import React from 'react';
import { FormGroup, Intent, HTMLTable } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface RiskVolatilityTableProps {
  riskMetrics: {
    appreciation_rates: {
      green: number;
      orange: number;
      red: number;
    };
    default_rates: {
      green: number;
      orange: number;
      red: number;
    };
    recovery_rates: {
      green: number;
      orange: number;
      red: number;
    };
    variation_factors: {
      interest_rate_volatility: number;
      property_value_volatility: number;
      default_rate_volatility: number;
      prepayment_rate_volatility: number;
      correlation_stability: number;
    };
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const RiskVolatilityTable: React.FC<RiskVolatilityTableProps> = ({
  riskMetrics,
  onChange,
  onBlur,
  errors
}) => {
  const handleZoneRateChange = (zone: string, rateType: string, value: number) => {
    onChange(`${rateType}.${zone}`, value);
  };

  const handleVariationFactorChange = (factor: string, value: number) => {
    onChange(`variation_factors.${factor}`, value);
  };

  const zones = [
    { key: 'green', name: 'Green Zone', color: 'bg-green-100 text-green-800' },
    { key: 'orange', name: 'Orange Zone', color: 'bg-orange-100 text-orange-800' },
    { key: 'red', name: 'Red Zone', color: 'bg-red-100 text-red-800' }
  ];

  return (
    <div className="space-y-6">
      {/* Zone Risk Parameters Table */}
      <Card
        title="Zone Risk Parameters"
        icon="th"
        subtitle="Configure risk parameters by zone"
      >
        <div className="overflow-x-auto">
          <HTMLTable striped className="w-full">
            <thead>
              <tr>
                <th className="text-left">Zone</th>
                <th className="text-center">Appreciation Rate (σ)</th>
                <th className="text-center">Default Rate (PD)</th>
                <th className="text-center">Recovery Rate</th>
                <th className="text-center">Risk Level</th>
              </tr>
            </thead>
            <tbody>
              {zones.map((zone) => {
                const appreciationRate = riskMetrics.appreciation_rates[zone.key as keyof typeof riskMetrics.appreciation_rates];
                const defaultRate = riskMetrics.default_rates[zone.key as keyof typeof riskMetrics.default_rates];
                const recoveryRate = riskMetrics.recovery_rates[zone.key as keyof typeof riskMetrics.recovery_rates];
                
                // Calculate risk score (higher default rate + lower recovery = higher risk)
                const riskScore = (defaultRate * 100) + ((1 - recoveryRate) * 50);
                const riskLevel = riskScore < 5 ? 'Low' : riskScore < 10 ? 'Medium' : 'High';
                const riskColor = riskScore < 5 ? 'text-green-600' : riskScore < 10 ? 'text-orange-600' : 'text-red-600';

                return (
                  <tr key={zone.key}>
                    <td>
                      <span className={`px-2 py-1 rounded-md text-sm font-medium ${zone.color}`}>
                        {zone.name}
                      </span>
                    </td>
                    <td className="text-center">
                      <SimpleNumericInput
                        value={appreciationRate}
                        onValueChange={(value) => handleZoneRateChange(zone.key, 'appreciation_rates', value)}
                        onBlur={() => onBlur(`appreciation_rates.${zone.key}`)}
                        min={0}
                        max={0.2}
                        step={0.001}
                        formatter={formatPercentage}
                        intent={errors[`appreciation_rates.${zone.key}`] ? Intent.DANGER : Intent.NONE}
                        className="w-24"
                      />
                    </td>
                    <td className="text-center">
                      <SimpleNumericInput
                        value={defaultRate}
                        onValueChange={(value) => handleZoneRateChange(zone.key, 'default_rates', value)}
                        onBlur={() => onBlur(`default_rates.${zone.key}`)}
                        min={0}
                        max={0.1}
                        step={0.001}
                        formatter={formatPercentage}
                        intent={errors[`default_rates.${zone.key}`] ? Intent.DANGER : Intent.NONE}
                        className="w-24"
                      />
                    </td>
                    <td className="text-center">
                      <SimpleNumericInput
                        value={recoveryRate}
                        onValueChange={(value) => handleZoneRateChange(zone.key, 'recovery_rates', value)}
                        onBlur={() => onBlur(`recovery_rates.${zone.key}`)}
                        min={0}
                        max={1}
                        step={0.01}
                        formatter={formatPercentage}
                        intent={errors[`recovery_rates.${zone.key}`] ? Intent.DANGER : Intent.NONE}
                        className="w-24"
                      />
                    </td>
                    <td className={`text-center font-medium ${riskColor}`}>
                      {riskLevel}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </HTMLTable>
        </div>

        {/* Risk Summary */}
        <div className="mt-4 p-3 bg-gray-50 rounded-md text-sm">
          <h5 className="font-medium mb-2">Risk Parameter Summary</h5>
          <div className="grid grid-cols-3 gap-4 text-xs">
            <div>
              <div className="text-gray-600">Avg Appreciation Rate</div>
              <div className="font-medium">
                {formatPercentage((riskMetrics.appreciation_rates.green + riskMetrics.appreciation_rates.orange + riskMetrics.appreciation_rates.red) / 3)}
              </div>
            </div>
            <div>
              <div className="text-gray-600">Avg Default Rate</div>
              <div className="font-medium">
                {formatPercentage((riskMetrics.default_rates.green + riskMetrics.default_rates.orange + riskMetrics.default_rates.red) / 3)}
              </div>
            </div>
            <div>
              <div className="text-gray-600">Avg Recovery Rate</div>
              <div className="font-medium">
                {formatPercentage((riskMetrics.recovery_rates.green + riskMetrics.recovery_rates.orange + riskMetrics.recovery_rates.red) / 3)}
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Volatility Factors */}
      <Card
        title="Volatility Factors"
        icon="variable"
        subtitle="Configure market volatility parameters"
      >
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormGroup
              label="Interest Rate Volatility"
              intent={errors['variation_factors.interest_rate_volatility'] ? Intent.DANGER : Intent.NONE}
              helperText="Volatility of interest rate changes"
            >
              <SimpleNumericInput
                value={riskMetrics.variation_factors.interest_rate_volatility}
                onValueChange={(value) => handleVariationFactorChange('interest_rate_volatility', value)}
                onBlur={() => onBlur('variation_factors.interest_rate_volatility')}
                min={0}
                max={0.1}
                step={0.001}
                formatter={formatPercentage}
                intent={errors['variation_factors.interest_rate_volatility'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Property Value Volatility"
              intent={errors['variation_factors.property_value_volatility'] ? Intent.DANGER : Intent.NONE}
              helperText="Volatility of property value changes"
            >
              <SimpleNumericInput
                value={riskMetrics.variation_factors.property_value_volatility}
                onValueChange={(value) => handleVariationFactorChange('property_value_volatility', value)}
                onBlur={() => onBlur('variation_factors.property_value_volatility')}
                min={0}
                max={0.5}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['variation_factors.property_value_volatility'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Default Rate Volatility"
              intent={errors['variation_factors.default_rate_volatility'] ? Intent.DANGER : Intent.NONE}
              helperText="Volatility of default rate changes"
            >
              <SimpleNumericInput
                value={riskMetrics.variation_factors.default_rate_volatility}
                onValueChange={(value) => handleVariationFactorChange('default_rate_volatility', value)}
                onBlur={() => onBlur('variation_factors.default_rate_volatility')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['variation_factors.default_rate_volatility'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Prepayment Rate Volatility"
              intent={errors['variation_factors.prepayment_rate_volatility'] ? Intent.DANGER : Intent.NONE}
              helperText="Volatility of prepayment rate changes"
            >
              <SimpleNumericInput
                value={riskMetrics.variation_factors.prepayment_rate_volatility}
                onValueChange={(value) => handleVariationFactorChange('prepayment_rate_volatility', value)}
                onBlur={() => onBlur('variation_factors.prepayment_rate_volatility')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['variation_factors.prepayment_rate_volatility'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>

            <FormGroup
              label="Correlation Stability"
              intent={errors['variation_factors.correlation_stability'] ? Intent.DANGER : Intent.NONE}
              helperText="Stability of correlations between factors"
            >
              <SimpleNumericInput
                value={riskMetrics.variation_factors.correlation_stability}
                onValueChange={(value) => handleVariationFactorChange('correlation_stability', value)}
                onBlur={() => onBlur('variation_factors.correlation_stability')}
                min={0}
                max={1}
                step={0.01}
                formatter={formatPercentage}
                intent={errors['variation_factors.correlation_stability'] ? Intent.DANGER : Intent.NONE}
                fill={true}
              />
            </FormGroup>
          </div>

          {/* Volatility Summary */}
          <div className="bg-blue-50 p-3 rounded-md text-sm">
            <h5 className="font-medium mb-2">Volatility Summary</h5>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3 text-xs">
              <div>
                <div className="text-gray-600">Interest Rate</div>
                <div className="font-medium">{formatPercentage(riskMetrics.variation_factors.interest_rate_volatility)}</div>
              </div>
              <div>
                <div className="text-gray-600">Property Value</div>
                <div className="font-medium">{formatPercentage(riskMetrics.variation_factors.property_value_volatility)}</div>
              </div>
              <div>
                <div className="text-gray-600">Default Rate</div>
                <div className="font-medium">{formatPercentage(riskMetrics.variation_factors.default_rate_volatility)}</div>
              </div>
              <div>
                <div className="text-gray-600">Prepayment Rate</div>
                <div className="font-medium">{formatPercentage(riskMetrics.variation_factors.prepayment_rate_volatility)}</div>
              </div>
              <div>
                <div className="text-gray-600">Correlation Stability</div>
                <div className="font-medium">{formatPercentage(riskMetrics.variation_factors.correlation_stability)}</div>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Help Information */}
      <div className="p-4 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Risk & Volatility Information</h4>
        <p>Configure risk parameters and volatility factors for simulation:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Appreciation Rate (σ):</strong> Expected annual property appreciation rate by zone</li>
          <li><strong>Default Rate (PD):</strong> Probability of default for loans in each zone</li>
          <li><strong>Recovery Rate:</strong> Expected recovery percentage in case of default</li>
          <li><strong>Volatility Factors:</strong> Control the variability of key market parameters</li>
          <li><strong>Correlation Stability:</strong> How stable correlations remain over time</li>
        </ul>
      </div>
    </div>
  );
};

export default RiskVolatilityTable;
