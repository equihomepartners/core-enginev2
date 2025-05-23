import React, { useState } from 'react';
import { Collapse, Button, Icon, Tag } from '@blueprintjs/core';
import { getFundBasicsDefaults, getPortfolioStrategyDefaults } from '../../../utils/schemaUtils';
import Card from '../../layout/Card';

interface JsonDiffPanelProps {
  currentConfig: any;
}

const JsonDiffPanel: React.FC<JsonDiffPanelProps> = ({ currentConfig }) => {
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    fund_basics: true,
    tranche_manager: false,
    portfolio_strategy: false,
    risk_volatility: false,
    advanced: false,
  });

  const fundBasicsDefaults = getFundBasicsDefaults();
  const portfolioDefaults = getPortfolioStrategyDefaults();
  const defaults = { ...fundBasicsDefaults, ...portfolioDefaults };

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const formatValue = (value: any): string => {
    if (typeof value === 'number') {
      if (value < 1 && value > 0) {
        return `${(value * 100).toFixed(2)}%`;
      }
      return value.toLocaleString();
    }
    if (typeof value === 'boolean') {
      return value ? 'Enabled' : 'Disabled';
    }
    if (typeof value === 'string') {
      return value;
    }
    if (Array.isArray(value)) {
      return `[${value.length} items]`;
    }
    if (typeof value === 'object' && value !== null) {
      return `{${Object.keys(value).length} properties}`;
    }
    return String(value);
  };

  const isChanged = (key: string, currentValue: any, defaultValue: any): boolean => {
    if (typeof currentValue === 'object' && typeof defaultValue === 'object') {
      return JSON.stringify(currentValue) !== JSON.stringify(defaultValue);
    }
    return currentValue !== defaultValue;
  };

  const getChangeType = (currentValue: any, defaultValue: any): 'added' | 'modified' | 'unchanged' => {
    if (defaultValue === undefined) return 'added';
    if (isChanged('', currentValue, defaultValue)) return 'modified';
    return 'unchanged';
  };

  const renderConfigSection = (title: string, sectionKey: string, configData: any, defaultData: any) => {
    const hasChanges = Object.keys(configData || {}).some(key =>
      isChanged(key, configData?.[key], defaultData?.[key])
    );

    return (
      <div key={sectionKey} className="border border-gray-200 rounded-md">
        <div
          className="flex items-center justify-between p-3 bg-gray-50 cursor-pointer hover:bg-gray-100"
          onClick={() => toggleSection(sectionKey)}
        >
          <div className="flex items-center space-x-2">
            <Icon icon={expandedSections[sectionKey] ? "chevron-down" : "chevron-right"} />
            <span className="font-medium">{title}</span>
            {hasChanges && (
              <Tag intent="primary" minimal>
                Modified
              </Tag>
            )}
          </div>
          <div className="text-sm text-gray-500">
            {Object.keys(configData || {}).length} parameters
          </div>
        </div>

        <Collapse isOpen={expandedSections[sectionKey]}>
          <div className="p-3 space-y-2">
            {Object.entries(configData || {}).map(([key, value]) => {
              const defaultValue = defaultData?.[key];
              const changeType = getChangeType(value, defaultValue);

              return (
                <div key={key} className="flex items-center justify-between py-1">
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-mono text-gray-600">{key}</span>
                    {changeType === 'modified' && (
                      <Tag intent="warning" minimal small>
                        Changed
                      </Tag>
                    )}
                    {changeType === 'added' && (
                      <Tag intent="success" minimal small>
                        New
                      </Tag>
                    )}
                  </div>
                  <div className="flex items-center space-x-2 text-sm">
                    {changeType === 'modified' && (
                      <>
                        <span className="text-red-600 line-through">
                          {formatValue(defaultValue)}
                        </span>
                        <span className="text-gray-400">→</span>
                      </>
                    )}
                    <span className={changeType === 'modified' ? 'text-green-600 font-medium' : 'text-gray-700'}>
                      {formatValue(value)}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </Collapse>
      </div>
    );
  };

  const fundBasicsConfig = {
    fund_name: currentConfig.fund_name,
    fund_size: currentConfig.fund_size,
    fund_term: currentConfig.fund_term,
    vintage_year: currentConfig.vintage_year,
    management_fee_rate: currentConfig.management_fee_rate,
    carried_interest_rate: currentConfig.carried_interest_rate,
    hurdle_rate: currentConfig.hurdle_rate,
    waterfall_structure: currentConfig.waterfall_structure,
    gp_commitment_percentage: currentConfig.gp_commitment_percentage,
    catch_up_rate: currentConfig.catch_up_rate,
  };

  const trancheManagerConfig = {
    enabled: currentConfig.tranche_manager?.enabled,
    tranches_count: currentConfig.tranche_manager?.tranches?.length || 0,
    reserve_account_enabled: currentConfig.tranche_manager?.reserve_account?.enabled,
    oc_test_enabled: currentConfig.tranche_manager?.overcollateralization_test?.enabled,
    ic_test_enabled: currentConfig.tranche_manager?.interest_coverage_test?.enabled,
  };

  const portfolioStrategyConfig = {
    zone_allocations: currentConfig.zone_allocations,
    avg_loan_ltv: currentConfig.avg_loan_ltv,
    min_ltv: currentConfig.min_ltv,
    max_ltv: currentConfig.max_ltv,
    avg_loan_size: currentConfig.avg_loan_size,
    min_loan_size: currentConfig.min_loan_size,
    max_loan_size: currentConfig.max_loan_size,
    leverage_enabled: currentConfig.leverage_engine?.enabled,
  };

  const riskVolatilityConfig = {
    appreciation_rates: currentConfig.appreciation_rates,
    default_rates: currentConfig.default_rates,
    recovery_rates: currentConfig.recovery_rates,
    property_value_volatility: currentConfig.variation_factors?.property_value_volatility,
    default_rate_volatility: currentConfig.variation_factors?.default_rate_volatility,
  };

  const advancedConfig = {
    cashflow_aggregator_enabled: currentConfig.cashflow_aggregator?.time_granularity,
    tax_analysis_enabled: currentConfig.cashflow_aggregator?.enable_tax_impact_analysis,
    scenario_analysis_enabled: currentConfig.cashflow_aggregator?.enable_scenario_analysis,
    parallel_processing: currentConfig.cashflow_aggregator?.enable_parallel_processing,
    deterministic_mode: currentConfig.deterministic_mode,
  };

  const totalChanges = [
    fundBasicsConfig,
    trancheManagerConfig,
    portfolioStrategyConfig,
    riskVolatilityConfig,
    advancedConfig
  ].reduce((total, section) => {
    return total + Object.keys(section).filter(key =>
      isChanged(key, section[key], defaults[key])
    ).length;
  }, 0);

  return (
    <Card
      title="Configuration Changes"
      icon="comparison"
      subtitle={`Review your configuration changes (${totalChanges} modifications)`}
    >
      <div className="space-y-4">
        {/* Summary */}
        <div className="bg-blue-50 p-3 rounded-md">
          <h4 className="font-medium text-blue-900 mb-2">Configuration Summary</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
            <div>
              <div className="text-blue-700">Total Changes</div>
              <div className="font-bold text-blue-900">{totalChanges}</div>
            </div>
            <div>
              <div className="text-blue-700">Fund Size</div>
              <div className="font-bold text-blue-900">{formatValue(currentConfig.fund_size)}</div>
            </div>
            <div>
              <div className="text-blue-700">Fund Term</div>
              <div className="font-bold text-blue-900">{currentConfig.fund_term} years</div>
            </div>
            <div>
              <div className="text-blue-700">Tranches</div>
              <div className="font-bold text-blue-900">
                {currentConfig.tranche_manager?.enabled ?
                  `${currentConfig.tranche_manager?.tranches?.length || 0} tranches` :
                  'Single tranche'
                }
              </div>
            </div>
          </div>
        </div>

        {/* Configuration Sections */}
        <div className="space-y-3">
          {renderConfigSection('Fund Basics', 'fund_basics', fundBasicsConfig, defaults)}
          {renderConfigSection('Tranche Manager', 'tranche_manager', trancheManagerConfig, {})}
          {renderConfigSection('Portfolio Strategy', 'portfolio_strategy', portfolioStrategyConfig, defaults)}
          {renderConfigSection('Risk & Volatility', 'risk_volatility', riskVolatilityConfig, defaults)}
          {renderConfigSection('Advanced Settings', 'advanced', advancedConfig, defaults)}
        </div>

        {/* Actions */}
        <div className="flex justify-between items-center pt-4 border-t border-gray-200">
          <Button
            icon="expand-all"
            minimal
            onClick={() => setExpandedSections({
              fund_basics: true,
              tranche_manager: true,
              portfolio_strategy: true,
              risk_volatility: true,
              advanced: true,
            })}
          >
            Expand All
          </Button>
          <Button
            icon="collapse-all"
            minimal
            onClick={() => setExpandedSections({
              fund_basics: false,
              tranche_manager: false,
              portfolio_strategy: false,
              risk_volatility: false,
              advanced: false,
            })}
          >
            Collapse All
          </Button>
        </div>
      </div>
    </Card>
  );
};

export default JsonDiffPanel;
