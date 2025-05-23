import React from 'react';
import { Icon, Tag, ProgressBar } from '@blueprintjs/core';
import Card from '../../layout/Card';

interface RuntimeEstimatorProps {
  config: any;
}

const RuntimeEstimator: React.FC<RuntimeEstimatorProps> = ({ config }) => {
  // Calculate complexity factors
  const calculateComplexity = () => {
    let complexity = 1; // Base complexity
    let factors = [];

    // Fund size factor
    const fundSize = config.fund_size || 0;
    if (fundSize > 500000000) { // > $500M
      complexity += 0.5;
      factors.push('Large fund size');
    } else if (fundSize > 100000000) { // > $100M
      complexity += 0.2;
      factors.push('Medium fund size');
    }

    // Tranche complexity
    if (config.tranche_manager?.enabled) {
      const trancheCount = config.tranche_manager?.tranches?.length || 0;
      complexity += trancheCount * 0.3;
      factors.push(`${trancheCount} tranches`);
      
      if (config.tranche_manager?.reserve_account?.enabled) {
        complexity += 0.2;
        factors.push('Reserve account');
      }
      
      if (config.tranche_manager?.overcollateralization_test?.enabled) {
        complexity += 0.15;
        factors.push('OC tests');
      }
      
      if (config.tranche_manager?.interest_coverage_test?.enabled) {
        complexity += 0.15;
        factors.push('IC tests');
      }
    }

    // Leverage complexity
    if (config.leverage_engine?.enabled) {
      complexity += 0.3;
      factors.push('Leverage facility');
      
      if (config.leverage_engine?.stress_testing?.enabled) {
        complexity += 0.2;
        factors.push('Leverage stress testing');
      }
    }

    // Cashflow aggregator complexity
    if (config.cashflow_aggregator?.enable_parallel_processing) {
      complexity += 0.1;
      factors.push('Parallel processing');
    }
    
    if (config.cashflow_aggregator?.enable_scenario_analysis) {
      const scenarioCount = config.cashflow_aggregator?.scenarios?.length || 0;
      complexity += scenarioCount * 0.1;
      factors.push(`${scenarioCount} scenarios`);
    }
    
    if (config.cashflow_aggregator?.enable_sensitivity_analysis) {
      const paramCount = config.cashflow_aggregator?.sensitivity_parameters?.length || 0;
      complexity += paramCount * 0.05;
      factors.push(`${paramCount} sensitivity params`);
    }

    // Risk analysis complexity
    if (config.risk_metrics?.enable_stress_testing) {
      const stressScenarios = config.risk_metrics?.stress_scenarios?.length || 0;
      complexity += stressScenarios * 0.1;
      factors.push(`${stressScenarios} stress scenarios`);
    }

    // Tax analysis
    if (config.cashflow_aggregator?.enable_tax_impact_analysis) {
      complexity += 0.15;
      factors.push('Tax analysis');
    }

    // Portfolio size estimation
    const avgLoanSize = config.avg_loan_size || 400000;
    const estimatedLoanCount = Math.floor(fundSize / avgLoanSize);
    if (estimatedLoanCount > 1000) {
      complexity += 0.4;
      factors.push('Large portfolio (>1000 loans)');
    } else if (estimatedLoanCount > 500) {
      complexity += 0.2;
      factors.push('Medium portfolio (>500 loans)');
    }

    return { complexity, factors, estimatedLoanCount };
  };

  const { complexity, factors, estimatedLoanCount } = calculateComplexity();

  // Estimate runtime based on complexity
  const baseRuntime = 25; // Base runtime in seconds
  const estimatedRuntime = Math.round(baseRuntime * complexity);

  const getRuntimeCategory = (runtime: number) => {
    if (runtime < 30) return { category: 'Fast', color: 'success', icon: 'flash' };
    if (runtime < 60) return { category: 'Medium', color: 'warning', icon: 'time' };
    return { category: 'Complex', color: 'danger', icon: 'warning-sign' };
  };

  const { category, color, icon } = getRuntimeCategory(estimatedRuntime);

  const formatRuntime = (seconds: number) => {
    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
  };

  return (
    <Card
      title="Runtime Estimation"
      icon="time"
      subtitle="Estimated simulation execution time and complexity analysis"
    >
      <div className="space-y-4">
        {/* Main Runtime Display */}
        <div className="text-center p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
          <div className="flex items-center justify-center space-x-2 mb-2">
            <Icon icon={icon} size={24} intent={color} />
            <span className="text-2xl font-bold text-gray-800">
              {formatRuntime(estimatedRuntime)}
            </span>
          </div>
          <div className="text-sm text-gray-600 mb-3">Estimated Runtime</div>
          <Tag intent={color} large>
            {category} Complexity
          </Tag>
        </div>

        {/* Complexity Breakdown */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-gray-50 p-4 rounded-md">
            <h4 className="font-medium mb-3 text-gray-800">Portfolio Metrics</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Fund Size:</span>
                <span className="font-medium">
                  ${(config.fund_size || 0).toLocaleString()}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Est. Loan Count:</span>
                <span className="font-medium">{estimatedLoanCount.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Fund Term:</span>
                <span className="font-medium">{config.fund_term || 10} years</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Complexity Score:</span>
                <span className="font-medium">{complexity.toFixed(1)}x</span>
              </div>
            </div>
          </div>

          <div className="bg-gray-50 p-4 rounded-md">
            <h4 className="font-medium mb-3 text-gray-800">Complexity Factors</h4>
            <div className="space-y-1">
              {factors.length > 0 ? (
                factors.map((factor, index) => (
                  <div key={index} className="flex items-center space-x-2 text-sm">
                    <Icon icon="dot" size={8} className="text-blue-500" />
                    <span className="text-gray-700">{factor}</span>
                  </div>
                ))
              ) : (
                <div className="text-sm text-gray-500 italic">
                  Basic configuration - minimal complexity
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Performance Tips */}
        <div className="bg-yellow-50 p-4 rounded-md border border-yellow-200">
          <h4 className="font-medium mb-2 text-yellow-800">Performance Tips</h4>
          <ul className="text-sm text-yellow-700 space-y-1">
            {estimatedRuntime > 60 && (
              <li>• Consider enabling parallel processing to reduce runtime</li>
            )}
            {config.cashflow_aggregator?.scenarios?.length > 3 && (
              <li>• Reduce number of scenarios for faster execution</li>
            )}
            {estimatedLoanCount > 1000 && (
              <li>• Large portfolio detected - runtime may vary based on system load</li>
            )}
            {!config.cashflow_aggregator?.enable_parallel_processing && estimatedRuntime > 45 && (
              <li>• Enable parallel processing in Cashflow Aggregator settings</li>
            )}
            <li>• Simulation will show real-time progress updates</li>
          </ul>
        </div>

        {/* Runtime Breakdown */}
        <div className="space-y-3">
          <h4 className="font-medium text-gray-800">Estimated Module Execution Times</h4>
          
          <div className="space-y-2">
            {[
              { name: 'Loan Generation', time: Math.round(estimatedRuntime * 0.15), color: 'primary' },
              { name: 'Price Path Simulation', time: Math.round(estimatedRuntime * 0.25), color: 'primary' },
              { name: 'Exit Event Modeling', time: Math.round(estimatedRuntime * 0.20), color: 'primary' },
              { name: 'Cashflow Calculation', time: Math.round(estimatedRuntime * 0.25), color: 'primary' },
              { name: 'Risk Analysis', time: Math.round(estimatedRuntime * 0.10), color: 'primary' },
              { name: 'Report Generation', time: Math.round(estimatedRuntime * 0.05), color: 'primary' },
            ].map((module, index) => (
              <div key={index} className="flex items-center space-x-3">
                <div className="w-32 text-sm text-gray-600">{module.name}</div>
                <div className="flex-1">
                  <ProgressBar
                    value={module.time / estimatedRuntime}
                    intent={module.color}
                    stripes={false}
                  />
                </div>
                <div className="w-12 text-sm text-gray-500 text-right">
                  {formatRuntime(module.time)}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Disclaimer */}
        <div className="text-xs text-gray-500 italic text-center pt-2 border-t border-gray-200">
          * Runtime estimates are approximate and may vary based on system performance and data complexity
        </div>
      </div>
    </Card>
  );
};

export default RuntimeEstimator;
