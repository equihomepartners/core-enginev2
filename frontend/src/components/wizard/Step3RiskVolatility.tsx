import React, { useState, useEffect } from 'react';
import { Tabs, Tab } from '@blueprintjs/core';
import { useSimulationStore } from '../../store';
import { getPortfolioStrategySchema } from '../../utils/schemaUtils';
// No validation import needed - using simple error state

// Import risk and volatility components
import PricePathCorrelations from './portfolio/PricePathCorrelations';
import EnhancedExitSimulator from './portfolio/EnhancedExitSimulator';
import RiskMetrics from './portfolio/RiskMetrics';
import LeverageRiskManagement from './risk/LeverageRiskManagement';
import VariationFactorsCorrelations from './risk/VariationFactorsCorrelations';
import RiskVolatilityTable from './risk/RiskVolatilityTable';
import RiskSparklines from './risk/RiskSparklines';

interface ValidationErrors {
  [key: string]: string | undefined;
}

interface Step3RiskVolatilityProps {
  onValidationChange?: (isValid: boolean) => void;
}

const Step3RiskVolatility: React.FC<Step3RiskVolatilityProps> = ({ onValidationChange }) => {
  const { config, setConfig } = useSimulationStore();

  // Get schema defaults
  const schema = getPortfolioStrategySchema();
  const defaults = schema.properties;

  // Initialize form data with risk and volatility parameters
  const [formData, setFormData] = useState(() => ({
    // Price path parameters (moved from portfolio strategy)
    price_path: {
      model_type: config.price_path?.model_type || defaults.price_path?.default?.model_type || "gbm",
      volatility: {
        green: config.price_path?.volatility?.green || defaults.price_path?.default?.volatility?.green || 0.08,
        orange: config.price_path?.volatility?.orange || defaults.price_path?.default?.volatility?.orange || 0.091,
        red: config.price_path?.volatility?.red || defaults.price_path?.default?.volatility?.red || 0.103,
      },
      correlation_matrix: {
        green_orange: config.price_path?.correlation_matrix?.green_orange || defaults.price_path?.default?.correlation_matrix?.green_orange || 0.7,
        green_red: config.price_path?.correlation_matrix?.green_red || defaults.price_path?.default?.correlation_matrix?.green_red || 0.5,
        orange_red: config.price_path?.correlation_matrix?.orange_red || defaults.price_path?.default?.correlation_matrix?.orange_red || 0.8,
      },
      mean_reversion_params: {
        speed: config.price_path?.mean_reversion_params?.speed || defaults.price_path?.default?.mean_reversion_params?.speed || 0.1,
        long_term_mean: config.price_path?.mean_reversion_params?.long_term_mean || defaults.price_path?.default?.mean_reversion_params?.long_term_mean || 0.05,
      },
      regime_switching_params: {
        bull_market_rate: config.price_path?.regime_switching_params?.bull_market_rate || defaults.price_path?.default?.regime_switching_params?.bull_market_rate || 0.08,
        bear_market_rate: config.price_path?.regime_switching_params?.bear_market_rate || defaults.price_path?.default?.regime_switching_params?.bear_market_rate || -0.02,
        bull_to_bear_prob: config.price_path?.regime_switching_params?.bull_to_bear_prob || defaults.price_path?.default?.regime_switching_params?.bull_to_bear_prob || 0.1,
        bear_to_bull_prob: config.price_path?.regime_switching_params?.bear_to_bull_prob || defaults.price_path?.default?.regime_switching_params?.bear_to_bull_prob || 0.2,
      },
      time_step: config.price_path?.time_step || defaults.price_path?.default?.time_step || "monthly",
      suburb_variation: config.price_path?.suburb_variation || defaults.price_path?.default?.suburb_variation || 0.02,
      property_variation: config.price_path?.property_variation || defaults.price_path?.default?.property_variation || 0.01,
      cycle_position: config.price_path?.cycle_position || defaults.price_path?.default?.cycle_position || 0.5,
    },

    // Enhanced exit simulator parameters (moved from portfolio strategy)
    enhanced_exit_simulator: {
      refinance_interest_rate_sensitivity: config.enhanced_exit_simulator?.refinance_interest_rate_sensitivity || defaults.enhanced_exit_simulator?.default?.refinance_interest_rate_sensitivity || 2.0,
      sale_appreciation_sensitivity: config.enhanced_exit_simulator?.sale_appreciation_sensitivity || defaults.enhanced_exit_simulator?.default?.sale_appreciation_sensitivity || 1.5,
      life_event_probability: config.enhanced_exit_simulator?.life_event_probability || defaults.enhanced_exit_simulator?.default?.life_event_probability || 0.05,
      behavioral_correlation: config.enhanced_exit_simulator?.behavioral_correlation || defaults.enhanced_exit_simulator?.default?.behavioral_correlation || 0.3,
      recession_default_multiplier: config.enhanced_exit_simulator?.recession_default_multiplier || defaults.enhanced_exit_simulator?.default?.recession_default_multiplier || 2.5,
      inflation_refinance_multiplier: config.enhanced_exit_simulator?.inflation_refinance_multiplier || defaults.enhanced_exit_simulator?.default?.inflation_refinance_multiplier || 1.8,
      employment_sensitivity: config.enhanced_exit_simulator?.employment_sensitivity || defaults.enhanced_exit_simulator?.default?.employment_sensitivity || 1.2,
      migration_sensitivity: config.enhanced_exit_simulator?.migration_sensitivity || defaults.enhanced_exit_simulator?.default?.migration_sensitivity || 0.8,
      regulatory_compliance_cost: config.enhanced_exit_simulator?.regulatory_compliance_cost || defaults.enhanced_exit_simulator?.default?.regulatory_compliance_cost || 0.01,
      tax_efficiency_factor: config.enhanced_exit_simulator?.tax_efficiency_factor || defaults.enhanced_exit_simulator?.default?.tax_efficiency_factor || 0.9,
      vintage_segmentation: config.enhanced_exit_simulator?.vintage_segmentation || defaults.enhanced_exit_simulator?.default?.vintage_segmentation || true,
      ltv_segmentation: config.enhanced_exit_simulator?.ltv_segmentation || defaults.enhanced_exit_simulator?.default?.ltv_segmentation || true,
      zone_segmentation: config.enhanced_exit_simulator?.zone_segmentation || defaults.enhanced_exit_simulator?.default?.zone_segmentation || true,
      var_confidence_level: config.enhanced_exit_simulator?.var_confidence_level || defaults.enhanced_exit_simulator?.default?.var_confidence_level || 0.95,
      stress_test_severity: config.enhanced_exit_simulator?.stress_test_severity || defaults.enhanced_exit_simulator?.default?.stress_test_severity || 0.3,
      tail_risk_threshold: config.enhanced_exit_simulator?.tail_risk_threshold || defaults.enhanced_exit_simulator?.default?.tail_risk_threshold || 0.05,
      use_ml_models: config.enhanced_exit_simulator?.use_ml_models || defaults.enhanced_exit_simulator?.default?.use_ml_models || true,
      feature_importance_threshold: config.enhanced_exit_simulator?.feature_importance_threshold || defaults.enhanced_exit_simulator?.default?.feature_importance_threshold || 0.05,
      anomaly_detection_threshold: config.enhanced_exit_simulator?.anomaly_detection_threshold || defaults.enhanced_exit_simulator?.default?.anomaly_detection_threshold || 3.0,
    },

    // Risk metrics parameters (moved from portfolio strategy)
    risk_metrics: {
      var_confidence_level: config.risk_metrics?.var_confidence_level || defaults.risk_metrics?.default?.var_confidence_level || 0.95,
      risk_free_rate: config.risk_metrics?.risk_free_rate || defaults.risk_metrics?.default?.risk_free_rate || 0.03,
      benchmark_return: config.risk_metrics?.benchmark_return || defaults.risk_metrics?.default?.benchmark_return || 0.07,
      min_acceptable_return: config.risk_metrics?.min_acceptable_return || defaults.risk_metrics?.default?.min_acceptable_return || 0.04,
      stress_test_scenarios: config.risk_metrics?.stress_test_scenarios || defaults.risk_metrics?.default?.stress_test_scenarios || [
        {
          name: 'mild_recession',
          description: 'Mild recession scenario',
          property_value_shock: -0.1,
          interest_rate_shock: 0.01,
          default_rate_shock: 1.5,
          liquidity_shock: 0.3
        },
        {
          name: 'severe_recession',
          description: 'Severe recession scenario',
          property_value_shock: -0.3,
          interest_rate_shock: 0.03,
          default_rate_shock: 3,
          liquidity_shock: 0.7
        },
        {
          name: 'financial_crisis',
          description: 'Financial crisis scenario',
          property_value_shock: -0.5,
          interest_rate_shock: 0.05,
          default_rate_shock: 5,
          liquidity_shock: 0.9
        }
      ],
      monte_carlo_simulations: config.risk_metrics?.monte_carlo_simulations || defaults.risk_metrics?.default?.monte_carlo_simulations || 1000,
      tail_risk_threshold: config.risk_metrics?.tail_risk_threshold || defaults.risk_metrics?.default?.tail_risk_threshold || 0.05,
      enable_sensitivity_analysis: config.risk_metrics?.enable_sensitivity_analysis || defaults.risk_metrics?.default?.enable_sensitivity_analysis || true,
      sensitivity_parameters: config.risk_metrics?.sensitivity_parameters || defaults.risk_metrics?.default?.sensitivity_parameters || ['interest_rate', 'property_value_growth', 'default_rate', 'ltv_ratio'],
    },

    // Leverage risk management parameters (extracted from leverage_engine)
    leverage_risk: {
      ramp_line: {
        enabled: config.leverage_engine?.ramp_line?.enabled || false,
        limit_pct_commit: config.leverage_engine?.ramp_line?.limit_pct_commit || 0.15,
        spread_bps: config.leverage_engine?.ramp_line?.spread_bps || 300,
        commitment_fee_bps: config.leverage_engine?.ramp_line?.commitment_fee_bps || 50,
        draw_period_months: config.leverage_engine?.ramp_line?.draw_period_months || 24,
        term_months: config.leverage_engine?.ramp_line?.term_months || 36,
      },
      interest_rate_model: {
        base_rate_initial: config.leverage_engine?.interest_rate_model?.base_rate_initial || 0.0425,
        volatility: config.leverage_engine?.interest_rate_model?.volatility || 0.01,
        mean_reversion: config.leverage_engine?.interest_rate_model?.mean_reversion || 0.1,
        long_term_mean: config.leverage_engine?.interest_rate_model?.long_term_mean || 0.04,
      },
      stress_testing: {
        enabled: config.leverage_engine?.stress_testing?.enabled || true,
        interest_rate_shock: config.leverage_engine?.stress_testing?.interest_rate_shock || 0.02,
        nav_shock: config.leverage_engine?.stress_testing?.nav_shock || 0.2,
        liquidity_shock: config.leverage_engine?.stress_testing?.liquidity_shock || 0.5,
      },
      optimization: {
        target_leverage: config.leverage_engine?.optimization?.target_leverage || 1.5,
        max_leverage: config.leverage_engine?.optimization?.max_leverage || 2.0,
        deleveraging_threshold: config.leverage_engine?.optimization?.deleveraging_threshold || 2.5,
        min_cash_buffer: config.leverage_engine?.optimization?.min_cash_buffer || 1.5,
      }
    },

    // Variation factors parameters
    variation_factors: {
      price_path: config.variation_factors?.price_path || defaults.variation_factors?.default?.price_path || 0.05,
      default_events: config.variation_factors?.default_events || defaults.variation_factors?.default?.default_events || 0.1,
      prepayment_events: config.variation_factors?.prepayment_events || defaults.variation_factors?.default?.prepayment_events || 0.2,
      appreciation_rates: config.variation_factors?.appreciation_rates || defaults.variation_factors?.default?.appreciation_rates || 0.05,
    },

    // Correlation matrix parameters
    correlation_matrix: {
      price_path_default_events: config.correlation_matrix?.price_path_default_events || defaults.correlation_matrix?.default?.price_path_default_events || -0.7,
      price_path_prepayment_events: config.correlation_matrix?.price_path_prepayment_events || defaults.correlation_matrix?.default?.price_path_prepayment_events || 0.3,
      default_events_prepayment_events: config.correlation_matrix?.default_events_prepayment_events || defaults.correlation_matrix?.default?.default_events_prepayment_events || -0.2,
    },

    // Deterministic mode
    deterministic_mode: config.deterministic_mode || defaults.deterministic_mode?.default || false,

    // Zone-specific rates for risk table
    appreciation_rates: {
      green: config.appreciation_rates?.green || 0.075,
      orange: config.appreciation_rates?.orange || 0.065,
      red: config.appreciation_rates?.red || 0.055,
    },
    default_rates: {
      green: config.default_rates?.green || 0.015,
      orange: config.default_rates?.orange || 0.025,
      red: config.default_rates?.red || 0.035,
    },
    recovery_rates: {
      green: config.recovery_rates?.green || 0.85,
      orange: config.recovery_rates?.orange || 0.80,
      red: config.recovery_rates?.red || 0.75,
    },
  }));

  // Validation state
  const [errors, setErrors] = useState<ValidationErrors>({});

  // Update store when form data changes
  useEffect(() => {
    if (Object.keys(formData).length > 0) {
      setConfig({
        // Price path parameters
        price_path: formData.price_path,

        // Enhanced exit simulator parameters
        enhanced_exit_simulator: formData.enhanced_exit_simulator,

        // Risk metrics parameters
        risk_metrics: formData.risk_metrics,

        // Variation factors parameters
        variation_factors: formData.variation_factors,

        // Correlation matrix parameters
        correlation_matrix: formData.correlation_matrix,

        // Deterministic mode
        deterministic_mode: formData.deterministic_mode,

        // Zone-specific rates
        appreciation_rates: formData.appreciation_rates,
        default_rates: formData.default_rates,
        recovery_rates: formData.recovery_rates,

        // Update leverage engine with risk parameters
        leverage_engine: {
          ...config.leverage_engine,
          ramp_line: formData.leverage_risk.ramp_line,
          interest_rate_model: formData.leverage_risk.interest_rate_model,
          stress_testing: formData.leverage_risk.stress_testing,
          optimization: {
            ...config.leverage_engine?.optimization,
            target_leverage: formData.leverage_risk.optimization.target_leverage,
            max_leverage: formData.leverage_risk.optimization.max_leverage,
            deleveraging_threshold: formData.leverage_risk.optimization.deleveraging_threshold,
            min_cash_buffer: formData.leverage_risk.optimization.min_cash_buffer,
          }
        },
      });
    }
  }, [formData]);

  // Simple validation - can be enhanced later
  useEffect(() => {
    // Basic validation logic can be added here if needed
    setErrors({});
    // Notify parent component that validation is always passing for now
    if (onValidationChange) {
      onValidationChange(true);
    }
  }, [formData, onValidationChange]);

  // Handle form field changes
  const handleChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Handle nested field changes (up to 3 levels deep)
  const handleNestedChange = (field: string, value: any) => {
    const fieldParts = field.split('.');

    setFormData(prev => {
      const newData = { ...prev };
      let current = newData;

      // Navigate to the parent object
      for (let i = 0; i < fieldParts.length - 1; i++) {
        if (!current[fieldParts[i]]) {
          current[fieldParts[i]] = {};
        }
        current = current[fieldParts[i]];
      }

      // Set the final value
      current[fieldParts[fieldParts.length - 1]] = value;

      return newData;
    });
  };

  // Handle field blur for validation
  const handleBlur = (field: string) => {
    // Simple blur handling - validation can be added later
    // For now, just clear any existing errors for the field
    setErrors(prev => ({
      ...prev,
      [field]: undefined
    }));
  };

  return (
    <div className="space-y-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">Risk & Volatility</h2>
        <p className="text-gray-600">
          Configure risk modeling, volatility parameters, and stress testing scenarios for comprehensive risk management.
        </p>
      </div>

      <Tabs id="risk-volatility-tabs" renderActiveTabPanelOnly={false}>
        <Tab
          id="zone-risk"
          title="Zone Risk Parameters"
          panel={
            <div className="mt-4 space-y-6">
              <RiskVolatilityTable
                riskMetrics={{
                  appreciation_rates: formData.appreciation_rates,
                  default_rates: formData.default_rates,
                  recovery_rates: formData.recovery_rates,
                  variation_factors: {
                    interest_rate_volatility: formData.variation_factors.price_path || 0.015,
                    property_value_volatility: formData.price_path.volatility.green || 0.12,
                    default_rate_volatility: formData.variation_factors.default_events || 0.25,
                    prepayment_rate_volatility: formData.variation_factors.prepayment_events || 0.20,
                    correlation_stability: 0.85,
                  }
                }}
                onChange={handleNestedChange}
                onBlur={handleBlur}
                errors={errors}
              />
              <RiskSparklines
                riskMetrics={{
                  appreciation_rates: formData.appreciation_rates,
                  default_rates: formData.default_rates,
                  variation_factors: {
                    property_value_volatility: formData.price_path.volatility.green || 0.12,
                    default_rate_volatility: formData.variation_factors.default_events || 0.25,
                  }
                }}
              />
            </div>
          }
        />
        <Tab
          id="price-volatility"
          title="Price Volatility"
          panel={
            <div className="mt-4">
              <PricePathCorrelations
                pricePath={formData.price_path}
                onChange={handleNestedChange}
                onBlur={handleBlur}
                errors={errors}
              />
            </div>
          }
        />
        <Tab
          id="exit-risk"
          title="Exit Risk Modeling"
          panel={
            <div className="mt-4">
              <EnhancedExitSimulator
                enhancedExitSimulator={formData.enhanced_exit_simulator}
                onChange={handleNestedChange}
                onBlur={handleBlur}
                errors={errors}
              />
            </div>
          }
        />
        <Tab
          id="stress-testing"
          title="Stress Testing"
          panel={
            <div className="mt-4">
              <RiskMetrics
                riskMetrics={formData.risk_metrics}
                onChange={handleNestedChange}
                onBlur={handleBlur}
                errors={errors}
              />
            </div>
          }
        />
        <Tab
          id="leverage-risk"
          title="Leverage Risk"
          panel={
            <div className="mt-4">
              <LeverageRiskManagement
                leverageRisk={formData.leverage_risk}
                onChange={handleNestedChange}
                onBlur={handleBlur}
                errors={errors}
              />
            </div>
          }
        />
        <Tab
          id="variation-correlations"
          title="Variation & Correlations"
          panel={
            <div className="mt-4">
              <VariationFactorsCorrelations
                variationFactors={formData.variation_factors}
                correlationMatrix={formData.correlation_matrix}
                deterministicMode={formData.deterministic_mode}
                onChange={handleNestedChange}
                onBlur={handleBlur}
                errors={errors}
              />
            </div>
          }
        />
      </Tabs>

      {/* Help Information */}
      <div className="p-4 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Risk & Volatility Information</h4>
        <p>Configure comprehensive risk modeling and volatility parameters:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Price Volatility:</strong> Stochastic price models, zone correlations, and market regimes</li>
          <li><strong>Exit Risk Modeling:</strong> Advanced behavioral modeling and economic sensitivity</li>
          <li><strong>Stress Testing:</strong> Scenario analysis, sensitivity testing, and risk metrics</li>
          <li><strong>Leverage Risk:</strong> Subscription line, interest rate modeling, and leverage optimization</li>
          <li><strong>Variation & Correlations:</strong> Random variation factors, cross-correlations, and deterministic mode</li>
        </ul>
        <p className="mt-2 text-xs text-gray-600">
          These parameters control how risks are modeled, measured, and managed throughout the simulation.
        </p>
      </div>
    </div>
  );
};

export default Step3RiskVolatility;
