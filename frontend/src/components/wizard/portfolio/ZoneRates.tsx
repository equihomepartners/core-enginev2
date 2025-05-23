import React from 'react';
import { FormGroup, Intent, HTMLTable } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface ZoneRatesProps {
  appreciationRates: {
    green: number;
    orange: number;
    red: number;
  };
  defaultRates: {
    green: number;
    orange: number;
    red: number;
  };
  recoveryRates: {
    green: number;
    orange: number;
    red: number;
  };
  onChange: (field: string, value: number) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const ZoneRates: React.FC<ZoneRatesProps> = ({
  appreciationRates,
  defaultRates,
  recoveryRates,
  onChange,
  onBlur,
  errors
}) => {
  return (
    <Card
      title="Zone-Specific Rates"
      icon="trending-up"
      subtitle="Configure rates by risk zone"
    >
      <div className="overflow-x-auto">
        <HTMLTable striped={true} bordered={true} className="w-full">
          <thead>
            <tr>
              <th>Zone</th>
              <th>Appreciation Rate</th>
              <th>Default Rate</th>
              <th>Recovery Rate</th>
            </tr>
          </thead>
          <tbody>
            {/* Green Zone */}
            <tr>
              <td className="font-medium">
                <div className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
                  Green
                </div>
              </td>
              <td>
                <SimpleNumericInput
                  value={appreciationRates.green}
                  onValueChange={(value) => onChange('appreciation_rates.green', value)}
                  onBlur={() => onBlur('appreciation_rates.green')}
                  min={0}
                  max={0.2}
                  step={0.005}
                  formatter={formatPercentage}
                  intent={errors['appreciation_rates.green'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </td>
              <td>
                <SimpleNumericInput
                  value={defaultRates.green}
                  onValueChange={(value) => onChange('default_rates.green', value)}
                  onBlur={() => onBlur('default_rates.green')}
                  min={0}
                  max={0.2}
                  step={0.005}
                  formatter={formatPercentage}
                  intent={errors['default_rates.green'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </td>
              <td>
                <SimpleNumericInput
                  value={recoveryRates.green}
                  onValueChange={(value) => onChange('recovery_rates.green', value)}
                  onBlur={() => onBlur('recovery_rates.green')}
                  min={0}
                  max={1}
                  step={0.05}
                  formatter={formatPercentage}
                  intent={errors['recovery_rates.green'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </td>
            </tr>

            {/* Orange Zone */}
            <tr>
              <td className="font-medium">
                <div className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-orange-500 mr-2"></div>
                  Orange
                </div>
              </td>
              <td>
                <SimpleNumericInput
                  value={appreciationRates.orange}
                  onValueChange={(value) => onChange('appreciation_rates.orange', value)}
                  onBlur={() => onBlur('appreciation_rates.orange')}
                  min={0}
                  max={0.2}
                  step={0.005}
                  formatter={formatPercentage}
                  intent={errors['appreciation_rates.orange'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </td>
              <td>
                <SimpleNumericInput
                  value={defaultRates.orange}
                  onValueChange={(value) => onChange('default_rates.orange', value)}
                  onBlur={() => onBlur('default_rates.orange')}
                  min={0}
                  max={0.2}
                  step={0.005}
                  formatter={formatPercentage}
                  intent={errors['default_rates.orange'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </td>
              <td>
                <SimpleNumericInput
                  value={recoveryRates.orange}
                  onValueChange={(value) => onChange('recovery_rates.orange', value)}
                  onBlur={() => onBlur('recovery_rates.orange')}
                  min={0}
                  max={1}
                  step={0.05}
                  formatter={formatPercentage}
                  intent={errors['recovery_rates.orange'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </td>
            </tr>

            {/* Red Zone */}
            <tr>
              <td className="font-medium">
                <div className="flex items-center">
                  <div className="w-3 h-3 rounded-full bg-red-500 mr-2"></div>
                  Red
                </div>
              </td>
              <td>
                <SimpleNumericInput
                  value={appreciationRates.red}
                  onValueChange={(value) => onChange('appreciation_rates.red', value)}
                  onBlur={() => onBlur('appreciation_rates.red')}
                  min={0}
                  max={0.2}
                  step={0.005}
                  formatter={formatPercentage}
                  intent={errors['appreciation_rates.red'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </td>
              <td>
                <SimpleNumericInput
                  value={defaultRates.red}
                  onValueChange={(value) => onChange('default_rates.red', value)}
                  onBlur={() => onBlur('default_rates.red')}
                  min={0}
                  max={0.2}
                  step={0.005}
                  formatter={formatPercentage}
                  intent={errors['default_rates.red'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </td>
              <td>
                <SimpleNumericInput
                  value={recoveryRates.red}
                  onValueChange={(value) => onChange('recovery_rates.red', value)}
                  onBlur={() => onBlur('recovery_rates.red')}
                  min={0}
                  max={1}
                  step={0.05}
                  formatter={formatPercentage}
                  intent={errors['recovery_rates.red'] ? Intent.DANGER : Intent.NONE}
                  fill={true}
                />
              </td>
            </tr>
          </tbody>
        </HTMLTable>
      </div>

      {/* Help Information */}
      <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Zone Rates Information</h4>
        <p>Configure key rates for each risk zone:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Appreciation Rate:</strong> Expected annual property value growth</li>
          <li><strong>Default Rate:</strong> Expected annual loan default probability</li>
          <li><strong>Recovery Rate:</strong> Expected recovery percentage in case of default</li>
        </ul>
        <p className="mt-2 text-xs text-gray-600">Note: Higher risk zones typically have higher appreciation potential but also higher default rates and lower recovery rates</p>
      </div>
    </Card>
  );
};

export default ZoneRates;
