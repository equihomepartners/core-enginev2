import React, { useState, useEffect, useRef } from 'react';
import {
  FormGroup,
  InputGroup,
  HTMLSelect,
  Switch,
  Button,
  Intent,
  Callout,
  Icon,
  Tag,
  Tooltip,
  Card as BPCard,
  Elevation,
  Collapse
} from '@blueprintjs/core';
import { formatCurrency, formatPercentage } from '../../utils/formatters';
import SimpleNumericInput from '../common/SimpleNumericInput';

interface Tranche {
  name: string;
  size: number;
  target_return: number;
  priority: number;
  type: string;
  interest_rate?: number;
  payment_frequency?: string;
  amortization?: boolean;
  amortization_schedule?: string;
  term_years?: number;
  waterfall_rules?: {
    hurdle_rate?: number;
    carried_interest_rate?: number;
    catch_up_rate?: number;
  };
  allocation_rules?: {
    zone_allocations?: {
      green?: number;
      orange?: number;
      red?: number;
    };
    ltv_constraints?: {
      min_ltv?: number;
      max_ltv?: number;
    };
  };
}

interface TrancheManagerConfig {
  enabled: boolean;
  tranches: Tranche[];
  reserve_account?: {
    enabled: boolean;
    target_percentage: number;
    initial_funding: number;
    replenishment_rate: number;
  };
  overcollateralization_test?: {
    enabled: boolean;
    threshold: number;
    test_frequency: string;
    cure_period_months: number;
  };
  interest_coverage_test?: {
    enabled: boolean;
    threshold: number;
    test_frequency: string;
    cure_period_months: number;
  };
}

interface TrancheConfigProps {
  value: TrancheManagerConfig;
  onChange: (value: TrancheManagerConfig) => void;
  fundSize: number;
}

const DEFAULT_TRANCHE: Tranche = {
  name: '',
  size: 0,
  target_return: 0.08,
  priority: 1,
  type: 'senior_debt',
  interest_rate: 0.05,
  payment_frequency: 'quarterly',
  amortization: false,
  amortization_schedule: 'interest_only',
  term_years: 10,
  waterfall_rules: {
    hurdle_rate: 0.08,
    carried_interest_rate: 0.2,
    catch_up_rate: 0
  },
  allocation_rules: {
    zone_allocations: {
      green: 0.6,
      orange: 0.3,
      red: 0.1
    },
    ltv_constraints: {
      min_ltv: 0,
      max_ltv: 0.5
    }
  }
};

const DEFAULT_CONFIG: TrancheManagerConfig = {
  enabled: false,
  tranches: [],
  reserve_account: {
    enabled: false,
    target_percentage: 0.05,
    initial_funding: 0.03,
    replenishment_rate: 0.01
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
};

const TrancheConfig: React.FC<TrancheConfigProps> = ({ value = DEFAULT_CONFIG, onChange, fundSize }) => {
  // Don't use local state for the config - use the value prop directly
  // This eliminates the two-way binding that can cause infinite loops
  const [expandedTrancheIndex, setExpandedTrancheIndex] = useState<number | null>(null);
  const [showAdvancedSettings, setShowAdvancedSettings] = useState(false);

  // Use a ref to track if we're in the middle of an update
  const isUpdatingRef = useRef(false);

  // Calculate remaining fund size
  const allocatedSize = value.tranches.reduce((sum, tranche) => sum + tranche.size, 0);
  const remainingSize = fundSize - allocatedSize;

  // Create a safe update function that prevents infinite loops
  const safeUpdate = (updater: (prev: TrancheManagerConfig) => TrancheManagerConfig) => {
    if (isUpdatingRef.current) return;

    isUpdatingRef.current = true;
    try {
      const newConfig = updater(value);
      // Only call onChange if the config has actually changed
      if (JSON.stringify(newConfig) !== JSON.stringify(value)) {
        onChange(newConfig);
      }
    } finally {
      // Reset the updating flag after a short delay to ensure React has time to process the update
      setTimeout(() => {
        isUpdatingRef.current = false;
      }, 0);
    }
  };

  // Handle toggle tranche manager
  const handleToggleTrancheManager = (enabled: boolean) => {
    safeUpdate(prev => ({
      ...prev,
      enabled
    }));
  };

  // Handle add tranche
  const handleAddTranche = () => {
    const newTranche: Tranche = {
      ...DEFAULT_TRANCHE,
      name: `Tranche ${value.tranches.length + 1}`,
      priority: value.tranches.length + 1,
      size: remainingSize > 0 ? remainingSize : 0
    };

    safeUpdate(prev => ({
      ...prev,
      tranches: [...prev.tranches, newTranche]
    }));

    // Expand the newly added tranche
    setExpandedTrancheIndex(value.tranches.length);
  };

  // Handle remove tranche
  const handleRemoveTranche = (index: number) => {
    safeUpdate(prev => ({
      ...prev,
      tranches: prev.tranches.filter((_, i) => i !== index)
    }));

    // Reset expanded index if the removed tranche was expanded
    if (expandedTrancheIndex === index) {
      setExpandedTrancheIndex(null);
    } else if (expandedTrancheIndex !== null && expandedTrancheIndex > index) {
      setExpandedTrancheIndex(expandedTrancheIndex - 1);
    }
  };

  // Handle update tranche
  const handleUpdateTranche = (index: number, updates: Partial<Tranche>) => {
    safeUpdate(prev => ({
      ...prev,
      tranches: prev.tranches.map((tranche, i) =>
        i === index ? { ...tranche, ...updates } : tranche
      )
    }));
  };

  // Handle toggle reserve account
  const handleToggleReserveAccount = (enabled: boolean) => {
    safeUpdate(prev => ({
      ...prev,
      reserve_account: {
        ...prev.reserve_account!,
        enabled
      }
    }));
  };

  // Handle update reserve account
  const handleUpdateReserveAccount = (updates: Partial<TrancheManagerConfig['reserve_account']>) => {
    safeUpdate(prev => ({
      ...prev,
      reserve_account: {
        ...prev.reserve_account!,
        ...updates
      }
    }));
  };

  // Handle toggle tests
  const handleToggleOvercollateralizationTest = (enabled: boolean) => {
    safeUpdate(prev => ({
      ...prev,
      overcollateralization_test: {
        ...prev.overcollateralization_test!,
        enabled
      }
    }));
  };

  const handleToggleInterestCoverageTest = (enabled: boolean) => {
    safeUpdate(prev => ({
      ...prev,
      interest_coverage_test: {
        ...prev.interest_coverage_test!,
        enabled
      }
    }));
  };

  // Handle update tests
  const handleUpdateOvercollateralizationTest = (updates: Partial<TrancheManagerConfig['overcollateralization_test']>) => {
    safeUpdate(prev => ({
      ...prev,
      overcollateralization_test: {
        ...prev.overcollateralization_test!,
        ...updates
      }
    }));
  };

  const handleUpdateInterestCoverageTest = (updates: Partial<TrancheManagerConfig['interest_coverage_test']>) => {
    safeUpdate(prev => ({
      ...prev,
      interest_coverage_test: {
        ...prev.interest_coverage_test!,
        ...updates
      }
    }));
  };

  // Get tranche type tag
  const getTrancheTypeTag = (type: string) => {
    switch (type) {
      case 'senior_debt':
        return <Tag intent={Intent.PRIMARY} minimal>Senior Debt</Tag>;
      case 'mezzanine':
        return <Tag intent={Intent.WARNING} minimal>Mezzanine</Tag>;
      case 'equity':
        return <Tag intent={Intent.SUCCESS} minimal>Equity</Tag>;
      case 'preferred_equity':
        return <Tag intent={Intent.SUCCESS} minimal>Preferred Equity</Tag>;
      default:
        return <Tag minimal>{type}</Tag>;
    }
  };

  return (
    <div className="space-y-4">
      <FormGroup
        label="Enable Tranche Management"
        helperText="Configure multiple tranches with different risk/return profiles"
      >
        <Switch
          checked={value.enabled}
          onChange={(e) => handleToggleTrancheManager(e.target.checked)}
          large
        />
      </FormGroup>

      {value.enabled && (
        <>
          {/* Tranches */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-medium">Tranches</h3>
              <div className="flex items-center space-x-2">
                <div className="text-sm text-neutral-500">
                  Allocated: {formatCurrency(allocatedSize)} / {formatCurrency(fundSize)}
                </div>
                <Button
                  icon="add"
                  intent={Intent.PRIMARY}
                  text="Add Tranche"
                  onClick={handleAddTranche}
                  disabled={remainingSize <= 0 && value.tranches.length > 0}
                />
              </div>
            </div>

            {value.tranches.length === 0 ? (
              <Callout
                icon="info-sign"
                title="No Tranches Configured"
                intent={Intent.PRIMARY}
              >
                <p>Add a tranche to configure the capital structure of your fund.</p>
                <Button
                  icon="add"
                  intent={Intent.PRIMARY}
                  text="Add Tranche"
                  onClick={handleAddTranche}
                  className="mt-2"
                />
              </Callout>
            ) : (
              <div className="space-y-4">
                {value.tranches.map((tranche, index) => (
                  <BPCard key={index} elevation={Elevation.ONE} className="relative">
                    <div className="flex justify-between items-center">
                      <div className="flex items-center space-x-2">
                        <span className="font-medium">{tranche.name}</span>
                        {getTrancheTypeTag(tranche.type)}
                        <span className="text-sm text-neutral-500">
                          Priority: {tranche.priority}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="font-medium">{formatCurrency(tranche.size)}</span>
                        <span className="text-sm text-neutral-500">
                          ({((tranche.size / fundSize) * 100).toFixed(1)}%)
                        </span>
                        <Button
                          icon={expandedTrancheIndex === index ? "chevron-up" : "chevron-down"}
                          minimal
                          onClick={() => setExpandedTrancheIndex(expandedTrancheIndex === index ? null : index)}
                        />
                        <Button
                          icon="trash"
                          intent={Intent.DANGER}
                          minimal
                          onClick={() => handleRemoveTranche(index)}
                        />
                      </div>
                    </div>

                    <Collapse isOpen={expandedTrancheIndex === index}>
                      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                        {/* Basic tranche properties */}
                        <div className="space-y-3">
                          <FormGroup
                            label="Tranche Name"
                            labelInfo="(required)"
                          >
                            <InputGroup
                              value={tranche.name}
                              onChange={(e) => handleUpdateTranche(index, { name: e.target.value })}
                              placeholder="Enter tranche name"
                            />
                          </FormGroup>

                          <FormGroup
                            label="Tranche Size"
                            labelInfo="(required)"
                            helperText={`Maximum: ${formatCurrency(fundSize - allocatedSize + tranche.size)}`}
                          >
                            <SimpleNumericInput
                              value={tranche.size}
                              onValueChange={(value) => handleUpdateTranche(index, { size: value })}
                              min={0}
                              max={fundSize - allocatedSize + tranche.size}
                              step={1000000}
                              formatter={formatCurrency}
                              fill
                            />
                          </FormGroup>

                          <FormGroup
                            label="Tranche Type"
                            labelInfo="(required)"
                          >
                            <HTMLSelect
                              value={tranche.type}
                              onChange={(e) => handleUpdateTranche(index, { type: e.target.value })}
                              options={[
                                { label: "Senior Debt", value: "senior_debt" },
                                { label: "Mezzanine", value: "mezzanine" },
                                { label: "Preferred Equity", value: "preferred_equity" },
                                { label: "Equity", value: "equity" }
                              ]}
                              fill
                            />
                          </FormGroup>

                          <FormGroup
                            label="Payment Priority"
                            labelInfo="(required)"
                            helperText="Lower numbers get paid first"
                          >
                            <SimpleNumericInput
                              value={tranche.priority}
                              onValueChange={(value) => handleUpdateTranche(index, { priority: value })}
                              min={1}
                              step={1}
                              fill
                            />
                          </FormGroup>
                        </div>

                        {/* Additional tranche properties */}
                        <div className="space-y-3">
                          <FormGroup
                            label="Target Return"
                            helperText="Annual target return for this tranche"
                          >
                            <SimpleNumericInput
                              value={tranche.target_return}
                              onValueChange={(value) => handleUpdateTranche(index, { target_return: value })}
                              min={0}
                              max={1}
                              step={0.01}
                              formatter={formatPercentage}
                              fill
                            />
                          </FormGroup>

                          {(tranche.type === 'senior_debt' || tranche.type === 'mezzanine') && (
                            <FormGroup
                              label="Interest Rate"
                              helperText="Annual interest rate for debt tranches"
                            >
                              <SimpleNumericInput
                                value={tranche.interest_rate || 0}
                                onValueChange={(value) => handleUpdateTranche(index, { interest_rate: value })}
                                min={0}
                                max={1}
                                step={0.005}
                                formatter={formatPercentage}
                                fill
                              />
                            </FormGroup>
                          )}

                          <FormGroup
                            label="Term (Years)"
                            helperText="Duration of this tranche"
                          >
                            <SimpleNumericInput
                              value={tranche.term_years || 0}
                              onValueChange={(value) => handleUpdateTranche(index, { term_years: value })}
                              min={0}
                              max={30}
                              step={1}
                              fill
                            />
                          </FormGroup>

                          <FormGroup
                            label="Payment Frequency"
                          >
                            <HTMLSelect
                              value={tranche.payment_frequency || 'quarterly'}
                              onChange={(e) => handleUpdateTranche(index, { payment_frequency: e.target.value })}
                              options={[
                                { label: "Monthly", value: "monthly" },
                                { label: "Quarterly", value: "quarterly" },
                                { label: "Semi-Annual", value: "semi_annual" },
                                { label: "Annual", value: "annual" }
                              ]}
                              fill
                            />
                          </FormGroup>
                        </div>
                      </div>
                    </Collapse>
                  </BPCard>
                ))}
              </div>
            )}
          </div>

          {/* Advanced Settings */}
          <div className="mt-6">
            <Button
              icon={showAdvancedSettings ? "chevron-up" : "chevron-down"}
              text={`${showAdvancedSettings ? 'Hide' : 'Show'} Advanced Settings`}
              minimal
              onClick={() => setShowAdvancedSettings(!showAdvancedSettings)}
            />

            <Collapse isOpen={showAdvancedSettings}>
              <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Reserve Account */}
                <BPCard elevation={Elevation.ONE}>
                  <h3 className="text-lg font-medium mb-4">Reserve Account</h3>

                  <FormGroup
                    label="Enable Reserve Account"
                    helperText="Set aside funds to cover potential shortfalls"
                  >
                    <Switch
                      checked={value.reserve_account?.enabled || false}
                      onChange={(e) => handleToggleReserveAccount(e.target.checked)}
                    />
                  </FormGroup>

                  {value.reserve_account?.enabled && (
                    <div className="space-y-3 mt-3">
                      <FormGroup
                        label="Target Percentage"
                        helperText="Target reserve as percentage of senior debt"
                      >
                        <SimpleNumericInput
                          value={value.reserve_account?.target_percentage || 0.05}
                          onValueChange={(val) => handleUpdateReserveAccount({ target_percentage: val })}
                          min={0}
                          max={1}
                          step={0.01}
                          formatter={formatPercentage}
                          fill
                        />
                      </FormGroup>

                      <FormGroup
                        label="Initial Funding"
                        helperText="Initial funding as percentage of senior debt"
                      >
                        <SimpleNumericInput
                          value={value.reserve_account?.initial_funding || 0.03}
                          onValueChange={(val) => handleUpdateReserveAccount({ initial_funding: val })}
                          min={0}
                          max={1}
                          step={0.01}
                          formatter={formatPercentage}
                          fill
                        />
                      </FormGroup>

                      <FormGroup
                        label="Replenishment Rate"
                        helperText="Rate at which reserve is replenished"
                      >
                        <SimpleNumericInput
                          value={value.reserve_account?.replenishment_rate || 0.01}
                          onValueChange={(val) => handleUpdateReserveAccount({ replenishment_rate: val })}
                          min={0}
                          max={1}
                          step={0.01}
                          formatter={formatPercentage}
                          fill
                        />
                      </FormGroup>
                    </div>
                  )}
                </BPCard>

                {/* Coverage Tests */}
                <BPCard elevation={Elevation.ONE}>
                  <h3 className="text-lg font-medium mb-4">Coverage Tests</h3>

                  <FormGroup
                    label="Enable Overcollateralization Test"
                    helperText="Test that assets exceed liabilities by a specified margin"
                  >
                    <Switch
                      checked={value.overcollateralization_test?.enabled || false}
                      onChange={(e) => handleToggleOvercollateralizationTest(e.target.checked)}
                    />
                  </FormGroup>

                  {value.overcollateralization_test?.enabled && (
                    <div className="space-y-3 mt-3">
                      <FormGroup
                        label="OC Threshold"
                        helperText="Minimum ratio of assets to liabilities"
                      >
                        <SimpleNumericInput
                          value={value.overcollateralization_test?.threshold || 1.2}
                          onValueChange={(val) => handleUpdateOvercollateralizationTest({ threshold: val })}
                          min={1}
                          max={2}
                          step={0.05}
                          fill
                        />
                      </FormGroup>
                    </div>
                  )}

                  <div className="mt-4">
                    <FormGroup
                      label="Enable Interest Coverage Test"
                      helperText="Test that interest income exceeds interest expense by a specified margin"
                    >
                      <Switch
                        checked={value.interest_coverage_test?.enabled || false}
                        onChange={(e) => handleToggleInterestCoverageTest(e.target.checked)}
                      />
                    </FormGroup>

                    {value.interest_coverage_test?.enabled && (
                      <div className="space-y-3 mt-3">
                        <FormGroup
                          label="IC Threshold"
                          helperText="Minimum ratio of interest income to interest expense"
                        >
                          <SimpleNumericInput
                            value={value.interest_coverage_test?.threshold || 1.5}
                            onValueChange={(val) => handleUpdateInterestCoverageTest({ threshold: val })}
                            min={1}
                            max={3}
                            step={0.1}
                            fill
                          />
                        </FormGroup>
                      </div>
                    )}
                  </div>
                </BPCard>
              </div>
            </Collapse>
          </div>
        </>
      )}
    </div>
  );
};

export default TrancheConfig;
