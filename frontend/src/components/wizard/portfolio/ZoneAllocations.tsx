import React from 'react';
import { FormGroup, Slider, Intent, Callout } from '@blueprintjs/core';
import { formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';

interface ZoneAllocationsProps {
  zoneAllocations: {
    green: number;
    orange: number;
    red: number;
  };
  onChange: (zone: 'green' | 'orange' | 'red', value: number) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const ZoneAllocations: React.FC<ZoneAllocationsProps> = ({
  zoneAllocations,
  onChange,
  onBlur,
  errors
}) => {
  // Calculate total allocation
  const totalAllocation = Object.values(zoneAllocations).reduce((sum, val) => sum + val, 0);
  const isValidTotal = Math.abs(totalAllocation - 1) < 0.01;

  return (
    <Card
      title="Zone Allocations"
      icon="map"
      subtitle="Allocate capital across risk zones"
    >
      {/* Green Zone Allocation */}
      <FormGroup
        label={
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-green-500 mr-2"></div>
            <span>Green Zone Allocation</span>
          </div>
        }
        intent={errors['zone_allocations.green'] ? Intent.DANGER : Intent.NONE}
        helperText={errors['zone_allocations.green'] || "Low risk, stable appreciation"}
      >
        <div className="flex items-center space-x-4">
          <Slider
            min={0}
            max={1}
            stepSize={0.01}
            labelStepSize={0.25}
            value={zoneAllocations.green}
            onChange={(value) => onChange('green', value)}
            onRelease={() => onBlur('zone_allocations.green')}
            labelRenderer={value => formatPercentage(value)}
            intent={errors['zone_allocations.green'] ? Intent.DANGER : Intent.PRIMARY}
            className="flex-grow"
          />
          <div className="w-20 text-right">
            {formatPercentage(zoneAllocations.green)}
          </div>
        </div>
      </FormGroup>

      {/* Orange Zone Allocation */}
      <FormGroup
        label={
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-orange-500 mr-2"></div>
            <span>Orange Zone Allocation</span>
          </div>
        }
        intent={errors['zone_allocations.orange'] ? Intent.DANGER : Intent.NONE}
        helperText={errors['zone_allocations.orange'] || "Medium risk, moderate appreciation"}
      >
        <div className="flex items-center space-x-4">
          <Slider
            min={0}
            max={1}
            stepSize={0.01}
            labelStepSize={0.25}
            value={zoneAllocations.orange}
            onChange={(value) => onChange('orange', value)}
            onRelease={() => onBlur('zone_allocations.orange')}
            labelRenderer={value => formatPercentage(value)}
            intent={errors['zone_allocations.orange'] ? Intent.DANGER : Intent.WARNING}
            className="flex-grow"
          />
          <div className="w-20 text-right">
            {formatPercentage(zoneAllocations.orange)}
          </div>
        </div>
      </FormGroup>

      {/* Red Zone Allocation */}
      <FormGroup
        label={
          <div className="flex items-center">
            <div className="w-4 h-4 rounded-full bg-red-500 mr-2"></div>
            <span>Red Zone Allocation</span>
          </div>
        }
        intent={errors['zone_allocations.red'] ? Intent.DANGER : Intent.NONE}
        helperText={errors['zone_allocations.red'] || "High risk, high potential appreciation"}
      >
        <div className="flex items-center space-x-4">
          <Slider
            min={0}
            max={1}
            stepSize={0.01}
            labelStepSize={0.25}
            value={zoneAllocations.red}
            onChange={(value) => onChange('red', value)}
            onRelease={() => onBlur('zone_allocations.red')}
            labelRenderer={value => formatPercentage(value)}
            intent={errors['zone_allocations.red'] ? Intent.DANGER : Intent.DANGER}
            className="flex-grow"
          />
          <div className="w-20 text-right">
            {formatPercentage(zoneAllocations.red)}
          </div>
        </div>
      </FormGroup>

      {/* Total Allocation */}
      <div className="mt-4 p-3 bg-gray-100 rounded-md">
        <div className="flex justify-between items-center">
          <span className="font-medium">Total Allocation:</span>
          <span className={`font-bold ${isValidTotal ? 'text-green-600' : 'text-red-600'}`}>
            {formatPercentage(totalAllocation)}
          </span>
        </div>
        
        {/* Error message */}
        {!isValidTotal && (
          <Callout
            intent={Intent.DANGER}
            icon="warning-sign"
            className="mt-2"
          >
            Zone allocations must sum to 100%
          </Callout>
        )}
      </div>

      {/* Help Information */}
      <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Zone Allocation Information</h4>
        <p>Allocate your fund's capital across three risk zones:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Green Zone:</strong> Low risk areas with stable appreciation</li>
          <li><strong>Orange Zone:</strong> Medium risk areas with moderate appreciation</li>
          <li><strong>Red Zone:</strong> Higher risk areas with potential for higher returns</li>
        </ul>
        <p className="mt-2 text-xs text-gray-600">Note: Allocations must sum to 100%</p>
      </div>
    </Card>
  );
};

export default ZoneAllocations;
