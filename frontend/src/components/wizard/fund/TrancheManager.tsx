import React from 'react';
import { FormGroup, Intent, Switch, Button, HTMLSelect, Callout } from '@blueprintjs/core';
import { formatCurrency, formatPercentage } from '../../../utils/formatters';
import Card from '../../layout/Card';
import SimpleNumericInput from '../../common/SimpleNumericInput';

interface Tranche {
  name: string;
  size: number;
  target_return: number;
  priority: number;
  type: 'senior_debt' | 'mezzanine' | 'equity' | 'preferred_equity';
  interest_rate: number;
  payment_frequency: 'monthly' | 'quarterly' | 'semi_annual' | 'annual';
  amortization: boolean;
  amortization_schedule: 'straight_line' | 'interest_only' | 'balloon';
  term_years: number;
  waterfall_rules: {
    hurdle_rate: number;
    carried_interest_rate: number;
    catch_up_rate: number;
  };
  allocation_rules: {
    zone_allocations: {
      green: number;
      orange: number;
      red: number;
    };
    ltv_constraints: {
      min_ltv: number;
      max_ltv: number;
    };
  };
}

interface TrancheManagerProps {
  trancheManager: {
    enabled: boolean;
    tranches: Tranche[];
    reserve_account: {
      enabled: boolean;
      target_percentage: number;
      initial_funding: number;
      replenishment_rate: number;
    };
    overcollateralization_test: {
      enabled: boolean;
      threshold: number;
      test_frequency: 'monthly' | 'quarterly' | 'semi_annual' | 'annual';
      cure_period_months: number;
    };
    interest_coverage_test: {
      enabled: boolean;
      threshold: number;
      test_frequency: 'monthly' | 'quarterly' | 'semi_annual' | 'annual';
      cure_period_months: number;
    };
  };
  onChange: (field: string, value: any) => void;
  onBlur: (field: string) => void;
  errors: Record<string, string | undefined>;
}

const TrancheManager: React.FC<TrancheManagerProps> = ({
  trancheManager,
  onChange,
  onBlur,
  errors
}) => {
  const handleChange = (field: string, value: any) => {
    onChange(`tranche_manager.${field}`, value);
  };

  const handleBlur = (field: string) => {
    onBlur(`tranche_manager.${field}`);
  };

  const handleNestedChange = (field: string, value: any) => {
    onChange(`tranche_manager.${field}`, value);
  };

  // Ensure tranches is always an array
  const tranches = Array.isArray(trancheManager.tranches) ? trancheManager.tranches : [];

  const addTranche = () => {
    const newTranche: Tranche = {
      name: `Tranche ${tranches.length + 1}`,
      size: 10000000,
      target_return: 0.08,
      priority: tranches.length + 1,
      type: 'senior_debt',
      interest_rate: 0.06,
      payment_frequency: 'quarterly',
      amortization: false,
      amortization_schedule: 'interest_only',
      term_years: 5,
      waterfall_rules: {
        hurdle_rate: 0.08,
        carried_interest_rate: 0.2,
        catch_up_rate: 0.0
      },
      allocation_rules: {
        zone_allocations: {
          green: 0.6,
          orange: 0.3,
          red: 0.1
        },
        ltv_constraints: {
          min_ltv: 0.5,
          max_ltv: 0.8
        }
      }
    };

    handleChange('tranches', [...tranches, newTranche]);
  };

  const removeTranche = (index: number) => {
    const newTranches = [...tranches];
    newTranches.splice(index, 1);
    // Reorder priorities
    newTranches.forEach((tranche, i) => {
      tranche.priority = i + 1;
    });
    handleChange('tranches', newTranches);
  };

  const updateTranche = (index: number, field: string, value: any) => {
    const newTranches = [...tranches];
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      newTranches[index] = {
        ...newTranches[index],
        [parent]: {
          ...newTranches[index][parent as keyof Tranche],
          [child]: value
        }
      };
    } else {
      newTranches[index] = {
        ...newTranches[index],
        [field]: value
      };
    }
    handleChange('tranches', newTranches);
  };

  const totalTrancheSize = tranches.reduce((sum, tranche) => sum + tranche.size, 0);

  return (
    <div className="space-y-6">
      {/* Enable Tranche Management */}
      <Card
        title="Tranche Management"
        icon="layers"
        subtitle="Configure multi-tranche capital structure"
      >
        <div className="space-y-4">
          <FormGroup
            label="Enable Tranche Management"
            helperText="Enable multi-tranche capital structure with different risk/return profiles"
            inline={true}
          >
            <Switch
              checked={trancheManager.enabled}
              onChange={(e) => handleChange('enabled', e.target.checked)}
              label="Enable"
            />
          </FormGroup>

          {trancheManager.enabled && (
            <div className="space-y-4 pl-4 border-l-2 border-gray-200">
              {/* Tranches Summary */}
              <div className="bg-blue-50 p-3 rounded-md">
                <h5 className="font-medium mb-2">Capital Structure Summary</h5>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                  <div>
                    <div className="text-gray-600">Total Tranches</div>
                    <div className="font-medium">{tranches.length}</div>
                  </div>
                  <div>
                    <div className="text-gray-600">Total Size</div>
                    <div className="font-medium">{formatCurrency(totalTrancheSize)}</div>
                  </div>
                  <div>
                    <div className="text-gray-600">Senior Debt</div>
                    <div className="font-medium">
                      {tranches.filter(t => t.type === 'senior_debt').length}
                    </div>
                  </div>
                  <div>
                    <div className="text-gray-600">Equity</div>
                    <div className="font-medium">
                      {tranches.filter(t => t.type === 'equity').length}
                    </div>
                  </div>
                </div>
              </div>

              {/* Add Tranche Button */}
              <div className="flex justify-between items-center">
                <h4 className="text-sm font-semibold">Tranches</h4>
                <Button
                  icon="plus"
                  intent="primary"
                  onClick={addTranche}
                  small={true}
                >
                  Add Tranche
                </Button>
              </div>

              {/* Tranches List */}
              {tranches.length === 0 && (
                <div className="text-gray-500 italic text-center py-4">
                  No tranches configured. Click "Add Tranche" to create your first tranche.
                </div>
              )}

              {tranches.map((tranche, index) => (
                <div key={index} className="border border-gray-200 rounded-md p-4 space-y-3">
                  <div className="flex justify-between items-center">
                    <h5 className="font-medium">
                      {tranche.name} (Priority {tranche.priority})
                    </h5>
                    <Button
                      icon="trash"
                      intent="danger"
                      minimal={true}
                      onClick={() => removeTranche(index)}
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {/* Basic Tranche Info */}
                    <FormGroup label="Name" className="mb-0">
                      <input
                        type="text"
                        className="bp4-input bp4-fill"
                        value={tranche.name}
                        onChange={(e) => updateTranche(index, 'name', e.target.value)}
                        placeholder="Tranche name"
                      />
                    </FormGroup>

                    <FormGroup label="Size" className="mb-0">
                      <SimpleNumericInput
                        value={tranche.size}
                        onValueChange={(value) => updateTranche(index, 'size', value)}
                        min={0}
                        step={1000000}
                        formatter={formatCurrency}
                        fill={true}
                      />
                    </FormGroup>

                    <FormGroup label="Type" className="mb-0">
                      <HTMLSelect
                        value={tranche.type}
                        onChange={(e) => updateTranche(index, 'type', e.target.value)}
                        fill={true}
                        options={[
                          { value: 'senior_debt', label: 'Senior Debt' },
                          { value: 'mezzanine', label: 'Mezzanine' },
                          { value: 'preferred_equity', label: 'Preferred Equity' },
                          { value: 'equity', label: 'Equity' }
                        ]}
                      />
                    </FormGroup>

                    <FormGroup label="Target Return" className="mb-0">
                      <SimpleNumericInput
                        value={tranche.target_return}
                        onValueChange={(value) => updateTranche(index, 'target_return', value)}
                        min={0}
                        max={1}
                        step={0.01}
                        formatter={formatPercentage}
                        fill={true}
                      />
                    </FormGroup>

                    <FormGroup label="Interest Rate" className="mb-0">
                      <SimpleNumericInput
                        value={tranche.interest_rate}
                        onValueChange={(value) => updateTranche(index, 'interest_rate', value)}
                        min={0}
                        max={1}
                        step={0.001}
                        formatter={formatPercentage}
                        fill={true}
                      />
                    </FormGroup>

                    <FormGroup label="Term (Years)" className="mb-0">
                      <SimpleNumericInput
                        value={tranche.term_years}
                        onValueChange={(value) => updateTranche(index, 'term_years', value)}
                        min={0}
                        max={30}
                        step={1}
                        fill={true}
                      />
                    </FormGroup>
                  </div>

                  {/* Waterfall Rules */}
                  <div className="bg-gray-50 p-3 rounded-md">
                    <h6 className="font-medium mb-2">Waterfall Rules</h6>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      <FormGroup label="Hurdle Rate" className="mb-0">
                        <SimpleNumericInput
                          value={tranche.waterfall_rules.hurdle_rate}
                          onValueChange={(value) => updateTranche(index, 'waterfall_rules.hurdle_rate', value)}
                          min={0}
                          max={1}
                          step={0.01}
                          formatter={formatPercentage}
                          fill={true}
                        />
                      </FormGroup>

                      <FormGroup label="Carried Interest" className="mb-0">
                        <SimpleNumericInput
                          value={tranche.waterfall_rules.carried_interest_rate}
                          onValueChange={(value) => updateTranche(index, 'waterfall_rules.carried_interest_rate', value)}
                          min={0}
                          max={1}
                          step={0.01}
                          formatter={formatPercentage}
                          fill={true}
                        />
                      </FormGroup>

                      <FormGroup label="Catch-up Rate" className="mb-0">
                        <SimpleNumericInput
                          value={tranche.waterfall_rules.catch_up_rate}
                          onValueChange={(value) => updateTranche(index, 'waterfall_rules.catch_up_rate', value)}
                          min={0}
                          max={1}
                          step={0.01}
                          formatter={formatPercentage}
                          fill={true}
                        />
                      </FormGroup>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </Card>

      {/* Reserve Account */}
      {trancheManager.enabled && (
        <Card
          title="Reserve Account"
          icon="bank-account"
          subtitle="Cash reserve to ensure debt service payments"
        >
          <div className="space-y-4">
            <FormGroup
              label="Enable Reserve Account"
              helperText="Maintain a cash reserve to ensure debt service payments"
              inline={true}
            >
              <Switch
                checked={trancheManager.reserve_account.enabled}
                onChange={(e) => handleNestedChange('reserve_account.enabled', e.target.checked)}
                label="Enable"
              />
            </FormGroup>

            {trancheManager.reserve_account.enabled && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pl-4 border-l-2 border-gray-200">
                <FormGroup
                  label="Target Percentage"
                  intent={errors['tranche_manager.reserve_account.target_percentage'] ? Intent.DANGER : Intent.NONE}
                  helperText="Target reserve as % of senior debt"
                >
                  <SimpleNumericInput
                    value={trancheManager.reserve_account.target_percentage}
                    onValueChange={(value) => handleNestedChange('reserve_account.target_percentage', value)}
                    onBlur={() => handleBlur('reserve_account.target_percentage')}
                    min={0}
                    max={1}
                    step={0.01}
                    formatter={formatPercentage}
                    intent={errors['tranche_manager.reserve_account.target_percentage'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>

                <FormGroup
                  label="Initial Funding"
                  intent={errors['tranche_manager.reserve_account.initial_funding'] ? Intent.DANGER : Intent.NONE}
                  helperText="Initial funding as % of senior debt"
                >
                  <SimpleNumericInput
                    value={trancheManager.reserve_account.initial_funding}
                    onValueChange={(value) => handleNestedChange('reserve_account.initial_funding', value)}
                    onBlur={() => handleBlur('reserve_account.initial_funding')}
                    min={0}
                    max={1}
                    step={0.01}
                    formatter={formatPercentage}
                    intent={errors['tranche_manager.reserve_account.initial_funding'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>

                <FormGroup
                  label="Replenishment Rate"
                  intent={errors['tranche_manager.reserve_account.replenishment_rate'] ? Intent.DANGER : Intent.NONE}
                  helperText="Rate at which reserve is replenished"
                >
                  <SimpleNumericInput
                    value={trancheManager.reserve_account.replenishment_rate}
                    onValueChange={(value) => handleNestedChange('reserve_account.replenishment_rate', value)}
                    onBlur={() => handleBlur('reserve_account.replenishment_rate')}
                    min={0}
                    max={1}
                    step={0.01}
                    formatter={formatPercentage}
                    intent={errors['tranche_manager.reserve_account.replenishment_rate'] ? Intent.DANGER : Intent.NONE}
                    fill={true}
                  />
                </FormGroup>
              </div>
            )}
          </div>
        </Card>
      )}

      {/* Coverage Tests */}
      {trancheManager.enabled && (
        <Card
          title="Coverage Tests"
          icon="shield"
          subtitle="Tests to ensure adequate collateral and income"
        >
          <div className="space-y-6">
            {/* Overcollateralization Test */}
            <div>
              <FormGroup
                label="Enable Overcollateralization Test"
                helperText="Test to ensure adequate collateral coverage"
                inline={true}
              >
                <Switch
                  checked={trancheManager.overcollateralization_test.enabled}
                  onChange={(e) => handleNestedChange('overcollateralization_test.enabled', e.target.checked)}
                  label="Enable"
                />
              </FormGroup>

              {trancheManager.overcollateralization_test.enabled && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pl-4 border-l-2 border-gray-200">
                  <FormGroup
                    label="OC Threshold"
                    intent={errors['tranche_manager.overcollateralization_test.threshold'] ? Intent.DANGER : Intent.NONE}
                    helperText="Minimum overcollateralization ratio"
                  >
                    <SimpleNumericInput
                      value={trancheManager.overcollateralization_test.threshold}
                      onValueChange={(value) => handleNestedChange('overcollateralization_test.threshold', value)}
                      onBlur={() => handleBlur('overcollateralization_test.threshold')}
                      min={1}
                      max={5}
                      step={0.1}
                      formatter={value => `${value.toFixed(1)}x`}
                      intent={errors['tranche_manager.overcollateralization_test.threshold'] ? Intent.DANGER : Intent.NONE}
                      fill={true}
                    />
                  </FormGroup>

                  <FormGroup
                    label="Test Frequency"
                    intent={errors['tranche_manager.overcollateralization_test.test_frequency'] ? Intent.DANGER : Intent.NONE}
                    helperText="How often to perform the test"
                  >
                    <HTMLSelect
                      value={trancheManager.overcollateralization_test.test_frequency}
                      onChange={(e) => handleNestedChange('overcollateralization_test.test_frequency', e.target.value)}
                      onBlur={() => handleBlur('overcollateralization_test.test_frequency')}
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
                    label="Cure Period (Months)"
                    intent={errors['tranche_manager.overcollateralization_test.cure_period_months'] ? Intent.DANGER : Intent.NONE}
                    helperText="Time allowed to cure test failure"
                  >
                    <SimpleNumericInput
                      value={trancheManager.overcollateralization_test.cure_period_months}
                      onValueChange={(value) => handleNestedChange('overcollateralization_test.cure_period_months', value)}
                      onBlur={() => handleBlur('overcollateralization_test.cure_period_months')}
                      min={0}
                      max={12}
                      step={1}
                      formatter={value => `${value} months`}
                      intent={errors['tranche_manager.overcollateralization_test.cure_period_months'] ? Intent.DANGER : Intent.NONE}
                      fill={true}
                    />
                  </FormGroup>
                </div>
              )}
            </div>

            {/* Interest Coverage Test */}
            <div>
              <FormGroup
                label="Enable Interest Coverage Test"
                helperText="Test to ensure adequate income to service debt"
                inline={true}
              >
                <Switch
                  checked={trancheManager.interest_coverage_test.enabled}
                  onChange={(e) => handleNestedChange('interest_coverage_test.enabled', e.target.checked)}
                  label="Enable"
                />
              </FormGroup>

              {trancheManager.interest_coverage_test.enabled && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pl-4 border-l-2 border-gray-200">
                  <FormGroup
                    label="IC Threshold"
                    intent={errors['tranche_manager.interest_coverage_test.threshold'] ? Intent.DANGER : Intent.NONE}
                    helperText="Minimum interest coverage ratio"
                  >
                    <SimpleNumericInput
                      value={trancheManager.interest_coverage_test.threshold}
                      onValueChange={(value) => handleNestedChange('interest_coverage_test.threshold', value)}
                      onBlur={() => handleBlur('interest_coverage_test.threshold')}
                      min={1}
                      max={10}
                      step={0.1}
                      formatter={value => `${value.toFixed(1)}x`}
                      intent={errors['tranche_manager.interest_coverage_test.threshold'] ? Intent.DANGER : Intent.NONE}
                      fill={true}
                    />
                  </FormGroup>

                  <FormGroup
                    label="Test Frequency"
                    intent={errors['tranche_manager.interest_coverage_test.test_frequency'] ? Intent.DANGER : Intent.NONE}
                    helperText="How often to perform the test"
                  >
                    <HTMLSelect
                      value={trancheManager.interest_coverage_test.test_frequency}
                      onChange={(e) => handleNestedChange('interest_coverage_test.test_frequency', e.target.value)}
                      onBlur={() => handleBlur('interest_coverage_test.test_frequency')}
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
                    label="Cure Period (Months)"
                    intent={errors['tranche_manager.interest_coverage_test.cure_period_months'] ? Intent.DANGER : Intent.NONE}
                    helperText="Time allowed to cure test failure"
                  >
                    <SimpleNumericInput
                      value={trancheManager.interest_coverage_test.cure_period_months}
                      onValueChange={(value) => handleNestedChange('interest_coverage_test.cure_period_months', value)}
                      onBlur={() => handleBlur('interest_coverage_test.cure_period_months')}
                      min={0}
                      max={12}
                      step={1}
                      formatter={value => `${value} months`}
                      intent={errors['tranche_manager.interest_coverage_test.cure_period_months'] ? Intent.DANGER : Intent.NONE}
                      fill={true}
                    />
                  </FormGroup>
                </div>
              )}
            </div>
          </div>
        </Card>
      )}

      {/* Help Information */}
      {trancheManager.enabled && (
        <div className="p-4 bg-gray-100 rounded-md text-sm">
          <h4 className="font-semibold mb-2">Tranche Management Information</h4>
          <p>Configure multi-tranche capital structure with institutional-grade features:</p>
          <ul className="list-disc pl-5 space-y-1 mt-2">
            <li><strong>Tranches:</strong> Different classes of capital with varying risk/return profiles</li>
            <li><strong>Priority:</strong> Payment order (1 = highest priority, paid first)</li>
            <li><strong>Waterfall Rules:</strong> Hurdle rates, carried interest, and catch-up provisions</li>
            <li><strong>Reserve Account:</strong> Cash reserve to ensure debt service payments</li>
            <li><strong>Coverage Tests:</strong> Overcollateralization and interest coverage tests</li>
            <li><strong>Allocation Rules:</strong> Zone allocations and LTV constraints per tranche</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default TrancheManager;
