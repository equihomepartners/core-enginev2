import React, { useState, useEffect, useRef } from 'react';
import {
  FormGroup,
  Slider,
  Intent,
  Callout,
  Tag,
  Tooltip,
  Icon,
  Divider,
  Switch,
  HTMLSelect,
  Button,
  Tabs,
  Tab
} from '@blueprintjs/core';
import Card from '../layout/Card';
import { useSimulationStore } from '../../store';
import { formatCurrency, formatPercentage, formatBasisPoints } from '../../utils/formatters';
import SimpleNumericInput from '../common/SimpleNumericInput';
import { getPortfolioStrategyDefaults, getPortfolioStrategyValidationSchema } from '../../utils/schemaUtils';
import { z } from 'zod';

// Import sub-components
import ZoneAllocations from './portfolio/ZoneAllocations';
import LtvParameters from './portfolio/LtvParameters';
import LoanSizeParameters from './portfolio/LoanSizeParameters';
import LeverageParameters from './portfolio/LeverageParameters';
import ZoneRates from './portfolio/ZoneRates';
import LoanTerms from './portfolio/LoanTerms';
import CapitalAllocationStrategy from './portfolio/CapitalAllocationStrategy';
import ExitTimingDistribution from './portfolio/ExitTimingDistribution';
import EnhancedLeverageParameters from './portfolio/EnhancedLeverageParameters';

// Get validation schema from schemaUtils
const portfolioStrategySchema = getPortfolioStrategyValidationSchema()
  // Add custom refinements for validation
  .refine(data => {
    const sum = data.zone_allocations.green + data.zone_allocations.orange + data.zone_allocations.red;
    return Math.abs(sum - 1) < 0.01; // Allow small rounding errors
  }, {
    message: "Zone allocations must sum to 100%",
    path: ["zone_allocations"]
  })
  .refine(data => data.min_ltv <= data.avg_loan_ltv, {
    message: "Minimum LTV must be less than or equal to average LTV",
    path: ["min_ltv"]
  })
  .refine(data => data.avg_loan_ltv <= data.max_ltv, {
    message: "Average LTV must be less than or equal to maximum LTV",
    path: ["max_ltv"]
  })
  .refine(data => data.min_loan_size <= data.avg_loan_size, {
    message: "Minimum loan size must be less than or equal to average loan size",
    path: ["min_loan_size"]
  })
  .refine(data => data.avg_loan_size <= data.max_loan_size, {
    message: "Average loan size must be less than or equal to maximum loan size",
    path: ["max_loan_size"]
  })
  .refine(data => {
    if (data.leverage_engine?.enabled) {
      if (data.leverage_engine.optimization?.enabled) {
        return data.leverage_engine.optimization.target_leverage <= data.leverage_engine.optimization.max_leverage;
      }
    }
    return true;
  }, {
    message: "Target leverage must be less than or equal to maximum leverage",
    path: ["leverage_engine.optimization.target_leverage"]
  });

interface ValidationErrors {
  [key: string]: string | undefined;
}

const Step2PortfolioStrategy: React.FC = () => {
  const store = useSimulationStore();
  const config = store?.config || {};

  // Get defaults from schema
  const defaults = getPortfolioStrategyDefaults();

  // Initialize form state with defaults or existing values
  const [formData, setFormData] = useState({
    // Zone allocations
    zone_allocations: {
      green: config.zone_allocations?.green || defaults.zone_allocations.green,
      orange: config.zone_allocations?.orange || defaults.zone_allocations.orange,
      red: config.zone_allocations?.red || defaults.zone_allocations.red,
    },

    // LTV parameters
    avg_loan_ltv: config.avg_loan_ltv || defaults.avg_loan_ltv,
    min_ltv: config.min_ltv || defaults.min_ltv,
    max_ltv: config.max_ltv || defaults.max_ltv,
    ltv_std_dev: config.ltv_std_dev || defaults.ltv_std_dev || 0.05,

    // Loan size parameters
    avg_loan_size: config.avg_loan_size || defaults.avg_loan_size,
    min_loan_size: config.min_loan_size || defaults.min_loan_size,
    max_loan_size: config.max_loan_size || defaults.max_loan_size,
    loan_size_std_dev: config.loan_size_std_dev || defaults.loan_size_std_dev || 50000,

    // Loan term and interest rate
    avg_loan_term: config.avg_loan_term || defaults.avg_loan_term || 5,
    avg_loan_interest_rate: config.avg_loan_interest_rate || defaults.avg_loan_interest_rate || 0.05,

    // Zone-specific rates
    appreciation_rates: {
      green: config.appreciation_rates?.green || defaults.appreciation_rates?.green || 0.05,
      orange: config.appreciation_rates?.orange || defaults.appreciation_rates?.orange || 0.03,
      red: config.appreciation_rates?.red || defaults.appreciation_rates?.red || 0.01,
    },

    default_rates: {
      green: config.default_rates?.green || defaults.default_rates?.green || 0.01,
      orange: config.default_rates?.orange || defaults.default_rates?.orange || 0.03,
      red: config.default_rates?.red || defaults.default_rates?.red || 0.05,
    },

    recovery_rates: {
      green: config.recovery_rates?.green || defaults.recovery_rates?.green || 0.9,
      orange: config.recovery_rates?.orange || defaults.recovery_rates?.orange || 0.8,
      red: config.recovery_rates?.red || defaults.recovery_rates?.red || 0.7,
    },



    // Leverage engine parameters
    leverage_engine: {
      enabled: config.leverage_engine?.enabled || defaults.leverage_engine?.enabled || false,

      // Green sleeve (NAV line facility)
      green_sleeve: {
        enabled: config.leverage_engine?.green_sleeve?.enabled || defaults.leverage_engine?.green_sleeve?.enabled || false,
        max_mult: config.leverage_engine?.green_sleeve?.max_mult || defaults.leverage_engine?.green_sleeve?.max_mult || 1.5,
        spread_bps: config.leverage_engine?.green_sleeve?.spread_bps || defaults.leverage_engine?.green_sleeve?.spread_bps || 275,
        commitment_fee_bps: config.leverage_engine?.green_sleeve?.commitment_fee_bps || defaults.leverage_engine?.green_sleeve?.commitment_fee_bps || 50,
        advance_rate: config.leverage_engine?.green_sleeve?.advance_rate || defaults.leverage_engine?.green_sleeve?.advance_rate || 0.75,
        min_dscr: config.leverage_engine?.green_sleeve?.min_dscr || defaults.leverage_engine?.green_sleeve?.min_dscr || 1.2,
        max_ltv: config.leverage_engine?.green_sleeve?.max_ltv || defaults.leverage_engine?.green_sleeve?.max_ltv || 0.65,
      },

      // Optimization parameters
      optimization: {
        enabled: config.leverage_engine?.optimization?.enabled || defaults.leverage_engine?.optimization?.enabled || true,
        target_leverage: config.leverage_engine?.optimization?.target_leverage || defaults.leverage_engine?.optimization?.target_leverage || 0.5,
        max_leverage: config.leverage_engine?.optimization?.max_leverage || defaults.leverage_engine?.optimization?.max_leverage || 0.65,
        deleveraging_threshold: config.leverage_engine?.optimization?.deleveraging_threshold || defaults.leverage_engine?.optimization?.deleveraging_threshold || 0.7,
      },
    },

    // Enhanced leverage parameters
    enhanced_leverage: {
      term_years: config.enhanced_leverage?.term_years || defaults.enhanced_leverage?.term_years || 5,
      amortization_years: config.enhanced_leverage?.amortization_years || defaults.enhanced_leverage?.amortization_years || 10,
      interest_only_period: config.enhanced_leverage?.interest_only_period || defaults.enhanced_leverage?.interest_only_period || 2,
      prepayment_penalty: config.enhanced_leverage?.prepayment_penalty || defaults.enhanced_leverage?.prepayment_penalty || 0.02,
      prepayment_lockout: config.enhanced_leverage?.prepayment_lockout || defaults.enhanced_leverage?.prepayment_lockout || 1,
    },

    // Reinvestment engine parameters
    reinvestment_engine: {
      reinvestment_strategy: config.reinvestment_engine?.reinvestment_strategy || defaults.reinvestment_engine?.reinvestment_strategy || "maintain_allocation",
      min_reinvestment_amount: config.reinvestment_engine?.min_reinvestment_amount || defaults.reinvestment_engine?.min_reinvestment_amount || 100000,
      reinvestment_frequency: config.reinvestment_engine?.reinvestment_frequency || defaults.reinvestment_engine?.reinvestment_frequency || "quarterly",
      reinvestment_delay: config.reinvestment_engine?.reinvestment_delay || defaults.reinvestment_engine?.reinvestment_delay || 3,
      reinvestment_batch_size: config.reinvestment_engine?.reinvestment_batch_size || defaults.reinvestment_engine?.reinvestment_batch_size || 50,
      zone_preference_multipliers: {
        green: config.reinvestment_engine?.zone_preference_multipliers?.green || defaults.reinvestment_engine?.zone_preference_multipliers?.green || 1.0,
        orange: config.reinvestment_engine?.zone_preference_multipliers?.orange || defaults.reinvestment_engine?.zone_preference_multipliers?.orange || 1.0,
        red: config.reinvestment_engine?.zone_preference_multipliers?.red || defaults.reinvestment_engine?.zone_preference_multipliers?.red || 1.0,
      },
      opportunistic_threshold: config.reinvestment_engine?.opportunistic_threshold || defaults.reinvestment_engine?.opportunistic_threshold || 0.1,
      rebalance_threshold: config.reinvestment_engine?.rebalance_threshold || defaults.reinvestment_engine?.rebalance_threshold || 0.05,
      reinvestment_ltv_adjustment: config.reinvestment_engine?.reinvestment_ltv_adjustment || defaults.reinvestment_engine?.reinvestment_ltv_adjustment || 0.0,
      reinvestment_size_adjustment: config.reinvestment_engine?.reinvestment_size_adjustment || defaults.reinvestment_engine?.reinvestment_size_adjustment || 0.0,
      enable_dynamic_allocation: config.reinvestment_engine?.enable_dynamic_allocation || defaults.reinvestment_engine?.enable_dynamic_allocation || false,
      performance_lookback_period: config.reinvestment_engine?.performance_lookback_period || defaults.reinvestment_engine?.performance_lookback_period || 12,
      performance_weight: config.reinvestment_engine?.performance_weight || defaults.reinvestment_engine?.performance_weight || 0.3,
      max_allocation_adjustment: config.reinvestment_engine?.max_allocation_adjustment || defaults.reinvestment_engine?.max_allocation_adjustment || 0.1,
      enable_cash_reserve: config.reinvestment_engine?.enable_cash_reserve || defaults.reinvestment_engine?.enable_cash_reserve || false,
      cash_reserve_target: config.reinvestment_engine?.cash_reserve_target || defaults.reinvestment_engine?.cash_reserve_target || 0.05,
      cash_reserve_min: config.reinvestment_engine?.cash_reserve_min || defaults.reinvestment_engine?.cash_reserve_min || 0.02,
      cash_reserve_max: config.reinvestment_engine?.cash_reserve_max || defaults.reinvestment_engine?.cash_reserve_max || 0.1,
    },

    // Exit simulator parameters
    exit_simulator: {
      base_exit_rate: config.exit_simulator?.base_exit_rate || defaults.exit_simulator?.base_exit_rate || 0.15,
      time_factor: config.exit_simulator?.time_factor || defaults.exit_simulator?.time_factor || 0.6,
      price_factor: config.exit_simulator?.price_factor || defaults.exit_simulator?.price_factor || 0.4,
      min_hold_period: config.exit_simulator?.min_hold_period || defaults.exit_simulator?.min_hold_period || 1.0,
      max_hold_period: config.exit_simulator?.max_hold_period || defaults.exit_simulator?.max_hold_period || 10.0,
      sale_weight: config.exit_simulator?.sale_weight || defaults.exit_simulator?.sale_weight || 0.7,
      refinance_weight: config.exit_simulator?.refinance_weight || defaults.exit_simulator?.refinance_weight || 0.25,
      default_weight: config.exit_simulator?.default_weight || defaults.exit_simulator?.default_weight || 0.05,
      appreciation_sale_multiplier: config.exit_simulator?.appreciation_sale_multiplier || defaults.exit_simulator?.appreciation_sale_multiplier || 2.0,
      interest_rate_refinance_multiplier: config.exit_simulator?.interest_rate_refinance_multiplier || defaults.exit_simulator?.interest_rate_refinance_multiplier || 1.5,
      economic_factor_default_multiplier: config.exit_simulator?.economic_factor_default_multiplier || defaults.exit_simulator?.economic_factor_default_multiplier || 1.2,
      appreciation_share: config.exit_simulator?.appreciation_share || defaults.exit_simulator?.appreciation_share || 0.5,
      min_appreciation_share: config.exit_simulator?.min_appreciation_share || defaults.exit_simulator?.min_appreciation_share || 0.3,
      max_appreciation_share: config.exit_simulator?.max_appreciation_share || defaults.exit_simulator?.max_appreciation_share || 0.7,
      tiered_appreciation_thresholds: config.exit_simulator?.tiered_appreciation_thresholds || defaults.exit_simulator?.tiered_appreciation_thresholds || [0.1, 0.2, 0.3],
      tiered_appreciation_shares: config.exit_simulator?.tiered_appreciation_shares || defaults.exit_simulator?.tiered_appreciation_shares || [0.3, 0.5, 0.7],
      base_default_rate: config.exit_simulator?.base_default_rate || defaults.exit_simulator?.base_default_rate || 0.02,
      recovery_rate: config.exit_simulator?.recovery_rate || defaults.exit_simulator?.recovery_rate || 0.8,
      foreclosure_cost: config.exit_simulator?.foreclosure_cost || defaults.exit_simulator?.foreclosure_cost || 0.1,
      foreclosure_time: config.exit_simulator?.foreclosure_time || defaults.exit_simulator?.foreclosure_time || 1.5,
    },


  });

  // Validation state
  const [errors, setErrors] = useState<ValidationErrors>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const [showManualRates, setShowManualRates] = useState(false);

  // Update store when form data changes - but only when user has made changes
  // to avoid infinite update loops
  const updateStoreRef = useRef(false);

  useEffect(() => {
    // Skip the first render to avoid infinite loops
    if (!updateStoreRef.current) {
      updateStoreRef.current = true;
      return;
    }

    if (store?.setConfig) {
      store.setConfig({
        // Zone allocations
        zone_allocations: formData.zone_allocations,

        // LTV parameters
        avg_loan_ltv: formData.avg_loan_ltv,
        min_ltv: formData.min_ltv,
        max_ltv: formData.max_ltv,
        ltv_std_dev: formData.ltv_std_dev,

        // Loan size parameters
        avg_loan_size: formData.avg_loan_size,
        min_loan_size: formData.min_loan_size,
        max_loan_size: formData.max_loan_size,
        loan_size_std_dev: formData.loan_size_std_dev,

        // Loan term and interest rate
        avg_loan_term: formData.avg_loan_term,
        avg_loan_interest_rate: formData.avg_loan_interest_rate,

        // Zone-specific rates
        appreciation_rates: formData.appreciation_rates,
        default_rates: formData.default_rates,
        recovery_rates: formData.recovery_rates,

        // Price path parameters
        price_path: formData.price_path,

        // Leverage engine parameters
        leverage_engine: formData.leverage_engine,

        // Enhanced leverage parameters
        enhanced_leverage: formData.enhanced_leverage,

        // Reinvestment engine parameters
        reinvestment_engine: formData.reinvestment_engine,

        // Exit simulator parameters
        exit_simulator: formData.exit_simulator,
      });
    }
  }, [formData]);

  // Validate form data
  useEffect(() => {
    try {
      portfolioStrategySchema.parse(formData);
      setErrors({});
    } catch (error) {
      if (error instanceof z.ZodError) {
        const newErrors: ValidationErrors = {};
        error.errors.forEach((err) => {
          const path = err.path.join('.');
          newErrors[path] = err.message;
        });
        setErrors(newErrors);
      }
    }
  }, [formData]);

  // Handle zone allocation changes
  const handleZoneAllocationChange = (zone: 'green' | 'orange' | 'red', value: number) => {
    // Calculate the adjustment needed for other zones
    const currentTotal = Object.values(formData.zone_allocations).reduce((sum, val) => sum + val, 0);
    const currentZoneValue = formData.zone_allocations[zone];
    const delta = value - currentZoneValue;

    // If increasing this zone, decrease others proportionally
    const newAllocations = { ...formData.zone_allocations, [zone]: value };

    if (delta > 0) {
      // Get other zones
      const otherZones = Object.keys(formData.zone_allocations).filter(z => z !== zone) as Array<'green' | 'orange' | 'red'>;

      // Calculate total of other zones
      const otherZonesTotal = otherZones.reduce((sum, z) => sum + formData.zone_allocations[z], 0);

      if (otherZonesTotal > 0) {
        // Adjust other zones proportionally
        otherZones.forEach(otherZone => {
          const proportion = formData.zone_allocations[otherZone] / otherZonesTotal;
          newAllocations[otherZone] = Math.max(0, formData.zone_allocations[otherZone] - (delta * proportion));
        });
      }
    } else if (delta < 0) {
      // If decreasing this zone, increase others proportionally
      const otherZones = Object.keys(formData.zone_allocations).filter(z => z !== zone) as Array<'green' | 'orange' | 'red'>;

      // Calculate total of other zones
      const otherZonesTotal = otherZones.reduce((sum, z) => sum + formData.zone_allocations[z], 0);

      if (otherZonesTotal > 0) {
        // Adjust other zones proportionally
        otherZones.forEach(otherZone => {
          const proportion = formData.zone_allocations[otherZone] / otherZonesTotal;
          newAllocations[otherZone] = formData.zone_allocations[otherZone] + (Math.abs(delta) * proportion);
        });
      }
    }

    // Normalize to ensure sum is exactly 1
    const newTotal = Object.values(newAllocations).reduce((sum, val) => sum + val, 0);
    if (newTotal !== 1) {
      const factor = 1 / newTotal;
      Object.keys(newAllocations).forEach(z => {
        newAllocations[z as 'green' | 'orange' | 'red'] *= factor;
      });
    }

    setFormData({
      ...formData,
      zone_allocations: newAllocations
    });

    setTouched({
      ...touched,
      [`zone_allocations.${zone}`]: true
    });
  };

  // Handle numeric input changes
  const handleChange = (field: string, value: number) => {
    // Handle nested fields
    if (field.includes('.')) {
      const [parent, child] = field.split('.');
      setFormData({
        ...formData,
        [parent]: {
          ...formData[parent as keyof typeof formData],
          [child]: value
        }
      });
    } else {
      setFormData({
        ...formData,
        [field]: value
      });
    }

    setTouched({
      ...touched,
      [field]: true
    });
  };

  // Handle blur events for validation
  const handleBlur = (field: string) => {
    setTouched({
      ...touched,
      [field]: true
    });
  };

  // Get guardrail status
  const getGuardrailStatus = (field: string): { status: 'success' | 'warning' | 'danger', message: string } => {
    if (errors[field]) {
      return { status: 'danger', message: errors[field] || 'Invalid value' };
    }

    // Add specific guardrail checks
    if (field === 'zone_allocations') {
      const total = Object.values(formData.zone_allocations).reduce((sum, val) => sum + val, 0);
      if (Math.abs(total - 1) > 0.01) {
        return { status: 'danger', message: 'Zone allocations must sum to 100%' };
      }

      if (formData.zone_allocations.red > 0.2) {
        return { status: 'warning', message: 'High allocation to red zone may increase risk' };
      }
    }

    if (field === 'avg_loan_ltv') {
      if (formData.avg_loan_ltv > 0.7) {
        return { status: 'warning', message: 'High average LTV increases default risk' };
      }
    }

    if (field === 'max_ltv') {
      if (formData.max_ltv > 0.8) {
        return { status: 'warning', message: 'Very high maximum LTV increases default risk' };
      }
    }

    return { status: 'success', message: 'Valid' };
  };

  // Sub-components are now imported at the top of the file

  // Handle nested field changes
  const handleNestedChange = (field: string, value: any) => {
    const parts = field.split('.');

    if (parts.length === 1) {
      // Simple field
      handleChange(field, value);
    } else if (parts.length === 2) {
      // Two-level nested field (e.g., zone_allocations.green)
      const [parent, child] = parts;
      setFormData({
        ...formData,
        [parent]: {
          ...formData[parent as keyof typeof formData],
          [child]: value
        }
      });
      setTouched({
        ...touched,
        [field]: true
      });
    } else if (parts.length === 3) {
      // Three-level nested field (e.g., leverage_engine.green_sleeve.enabled)
      const [parent, middle, child] = parts;
      setFormData({
        ...formData,
        [parent]: {
          ...formData[parent as keyof typeof formData],
          [middle]: {
            ...(formData[parent as keyof typeof formData] as any)[middle],
            [child]: value
          }
        }
      });
      setTouched({
        ...touched,
        [field]: true
      });
    }
  };

  return (
    <div className="space-y-6">
      <Tabs id="portfolio-strategy-tabs" renderActiveTabPanelOnly={false}>
        <Tab
          id="data-zones"
          title="Data & Zones"
          panel={
            <div className="space-y-6 mt-4">
              {/* TLS Module Interactive Data Card - Moved to top */}
              <Card
                title="TLS Module Data Explorer"
                icon="map-marker"
                subtitle="Sydney Property Risk Zones"
              >
                    {/* Data Overview */}
                    <div className="bg-gray-50 p-3 rounded-md mb-4">
                      <div className="flex justify-between items-center mb-2">
                        <div className="font-semibold text-gray-800">Sydney Metro Area Dataset</div>
                        <div className="flex items-center space-x-2">
                          <div className="text-sm text-gray-600">104 Suburbs • 7,280 Properties</div>
                          <Button
                            size="small"
                            minimal={true}
                            icon="document"
                            onClick={() => {
                              // Open the TLS data file via API endpoint
                              const dataUrl = 'http://localhost:8000/tls/data';
                              window.open(dataUrl, '_blank');
                            }}
                            title="View full TLS data file"
                          >
                            View Data
                          </Button>
                        </div>
                      </div>
                      <div className="text-xs text-gray-600">
                        Comprehensive property data with 51 metrics per suburb including appreciation rates,
                        default probabilities, recovery rates, beta calculations, and risk factors.
                      </div>
                    </div>

                    {/* Zone Distribution */}
                    <div className="mb-4">
                      <h4 className="text-sm font-semibold mb-2">Zone Distribution</h4>
                      <div className="flex h-6 rounded-md overflow-hidden">
                        <div className="bg-green-500 h-full" style={{ width: '29%' }}>
                          <div className="h-full flex items-center justify-center text-white text-xs font-medium">29%</div>
                        </div>
                        <div className="bg-orange-500 h-full" style={{ width: '60%' }}>
                          <div className="h-full flex items-center justify-center text-white text-xs font-medium">60%</div>
                        </div>
                        <div className="bg-red-500 h-full" style={{ width: '11%' }}>
                          <div className="h-full flex items-center justify-center text-white text-xs font-medium">11%</div>
                        </div>
                      </div>

                      <div className="grid grid-cols-3 gap-2 mt-2">
                        <div className="bg-green-100 p-2 rounded text-center">
                          <div className="text-xs text-gray-600">Green Zone</div>
                          <div className="font-semibold text-green-700">30 Suburbs</div>
                          <div className="text-xs text-gray-600">Score: 60+</div>
                          <div className="text-xs text-gray-500">2,100 Properties</div>
                        </div>
                        <div className="bg-orange-100 p-2 rounded text-center">
                          <div className="text-xs text-gray-600">Orange Zone</div>
                          <div className="font-semibold text-orange-700">63 Suburbs</div>
                          <div className="text-xs text-gray-600">Score: 55-60</div>
                          <div className="text-xs text-gray-500">4,410 Properties</div>
                        </div>
                        <div className="bg-red-100 p-2 rounded text-center">
                          <div className="text-xs text-gray-600">Red Zone</div>
                          <div className="font-semibold text-red-700">11 Suburbs</div>
                          <div className="text-xs text-gray-600">Score: &lt;55</div>
                          <div className="text-xs text-gray-500">770 Properties</div>
                        </div>
                      </div>
                    </div>

                    {/* Zone Comparison */}
                    <div className="mb-4">
                      <h4 className="text-sm font-semibold mb-2">Zone Comparison (Real TLS Data)</h4>
                      <div className="overflow-x-auto">
                        <table className="w-full text-xs">
                          <thead>
                            <tr className="bg-gray-100">
                              <th className="p-1 text-left">Metric</th>
                              <th className="p-1 text-center bg-green-50">Green</th>
                              <th className="p-1 text-center bg-orange-50">Orange</th>
                              <th className="p-1 text-center bg-red-50">Red</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr>
                              <td className="p-1 border-b">Appreciation (5yr)</td>
                              <td className="p-1 text-center border-b bg-green-50">7.2%</td>
                              <td className="p-1 text-center border-b bg-orange-50">7.2%</td>
                              <td className="p-1 text-center border-b bg-red-50">5.9%</td>
                            </tr>
                            <tr>
                              <td className="p-1 border-b">Default Rate</td>
                              <td className="p-1 text-center border-b bg-green-50">2.0%</td>
                              <td className="p-1 text-center border-b bg-orange-50">2.2%</td>
                              <td className="p-1 text-center border-b bg-red-50">2.3%</td>
                            </tr>
                            <tr>
                              <td className="p-1 border-b">Recovery Rate</td>
                              <td className="p-1 text-center border-b bg-green-50">82%</td>
                              <td className="p-1 text-center border-b bg-orange-50">80%</td>
                              <td className="p-1 text-center border-b bg-red-50">79%</td>
                            </tr>
                            <tr>
                              <td className="p-1 border-b">Price Volatility</td>
                              <td className="p-1 text-center border-b bg-green-50">8.0%</td>
                              <td className="p-1 text-center border-b bg-orange-50">9.1%</td>
                              <td className="p-1 text-center border-b bg-red-50">10.3%</td>
                            </tr>
                            <tr>
                              <td className="p-1 border-b">Rental Yield</td>
                              <td className="p-1 text-center border-b bg-green-50">5.2%</td>
                              <td className="p-1 text-center border-b bg-orange-50">4.9%</td>
                              <td className="p-1 text-center border-b bg-red-50">4.7%</td>
                            </tr>
                            <tr>
                              <td className="p-1 border-b">Days on Market</td>
                              <td className="p-1 text-center border-b bg-green-50">70</td>
                              <td className="p-1 text-center border-b bg-orange-50">79</td>
                              <td className="p-1 text-center border-b bg-red-50">81</td>
                            </tr>
                            <tr>
                              <td className="p-1">Beta (vs Market)</td>
                              <td className="p-1 text-center bg-green-50">1.07</td>
                              <td className="p-1 text-center bg-orange-50">1.21</td>
                              <td className="p-1 text-center bg-red-50">1.37</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <div className="text-xs text-gray-600 mt-2">
                        <p><strong>Note:</strong> Beta calculated using price volatility vs market volatility (7.5%).
                        Higher beta indicates higher systematic risk relative to the broader market.</p>
                      </div>
                    </div>

                    {/* Suburb Spotlight */}
                    <div>
                      <h4 className="text-sm font-semibold mb-2">Top Suburbs by Zone</h4>
                      <div className="grid grid-cols-3 gap-2 text-xs">
                        <div className="bg-green-50 p-2 rounded">
                          <div className="font-medium text-green-800">Green Zone (Score: 60+)</div>
                          <ul className="mt-1 space-y-1">
                            <li>• Bondi Junction (65.3)</li>
                            <li>• Narrabeen (64.5)</li>
                            <li>• Newtown (64.3)</li>
                            <li>• Mosman (64.3)</li>
                          </ul>
                        </div>
                        <div className="bg-orange-50 p-2 rounded">
                          <div className="font-medium text-orange-800">Orange Zone (Score: 55-60)</div>
                          <ul className="mt-1 space-y-1">
                            <li>• Collaroy (63.7)</li>
                            <li>• Manly (62.8)</li>
                            <li>• Chatswood (61.5)</li>
                            <li>• Parramatta (58.2)</li>
                          </ul>
                        </div>
                        <div className="bg-red-50 p-2 rounded">
                          <div className="font-medium text-red-800">Red Zone (Score: &lt;55)</div>
                          <ul className="mt-1 space-y-1">
                            <li>• Wentworthville (53.9)</li>
                            <li>• Merrylands (53.8)</li>
                            <li>• Glenfield (52.6)</li>
                            <li>• Penrith (50.3)</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </Card>

              {/* Zone Allocations - Moved below TLS */}
              <ZoneAllocations
                zoneAllocations={formData.zone_allocations}
                onChange={handleZoneAllocationChange}
                onBlur={handleBlur}
                errors={errors}
              />

              {/* Zone Rate Override Control */}
              <div className="flex items-center justify-between p-3 bg-blue-50 rounded-md mb-6">
                <div className="text-sm text-gray-700">
                  <p><strong>Zone Rate Configuration:</strong> Rates are auto-calculated from TLS data or can be manually overridden</p>
                </div>
                <Button
                  size="small"
                  intent={showManualRates ? Intent.PRIMARY : Intent.NONE}
                  onClick={() => setShowManualRates(!showManualRates)}
                  icon={showManualRates ? "eye-open" : "edit"}
                >
                  {showManualRates ? "Using Manual" : "Set Manual"}
                </Button>
              </div>

              {showManualRates && (
                <ZoneRates
                  appreciationRates={formData.appreciation_rates}
                  defaultRates={formData.default_rates}
                  recoveryRates={formData.recovery_rates}
                  onChange={handleNestedChange}
                  onBlur={handleBlur}
                  errors={errors}
                />
              )}


            </div>
          }
        />
        <Tab
          id="loan-parameters"
          title="Loan Parameters"
          panel={
            <div className="space-y-6 mt-4">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <LtvParameters
                  avgLoanLtv={formData.avg_loan_ltv}
                  minLtv={formData.min_ltv}
                  maxLtv={formData.max_ltv}
                  ltvStdDev={formData.ltv_std_dev}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  errors={errors}
                  getGuardrailStatus={getGuardrailStatus}
                />
                <LoanTerms
                  avgLoanTerm={formData.avg_loan_term}
                  avgLoanInterestRate={formData.avg_loan_interest_rate}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  errors={errors}
                />
              </div>

              <LoanSizeParameters
                avgLoanSize={formData.avg_loan_size}
                minLoanSize={formData.min_loan_size}
                maxLoanSize={formData.max_loan_size}
                loanSizeStdDev={formData.loan_size_std_dev}
                onChange={handleChange}
                onBlur={handleBlur}
                errors={errors}
                getGuardrailStatus={getGuardrailStatus}
              />
            </div>
          }
        />
        <Tab
          id="leverage"
          title="Leverage"
          panel={
            <div className="space-y-6 mt-4">
              <LeverageParameters
                leverageEngine={formData.leverage_engine}
                onChange={handleNestedChange}
                onBlur={handleBlur}
                errors={errors}
              />
              <EnhancedLeverageParameters
                enhancedLeverage={formData.enhanced_leverage}
                onChange={handleNestedChange}
                onBlur={handleBlur}
                errors={errors}
              />
            </div>
          }
        />
        <Tab
          id="capital-allocation"
          title="Capital Allocation"
          panel={
            <div className="mt-4">
              <CapitalAllocationStrategy
                reinvestmentEngine={formData.reinvestment_engine}
                onChange={handleNestedChange}
                onBlur={handleBlur}
                errors={errors}
              />
            </div>
          }
        />
        <Tab
          id="exit-timing"
          title="Exit Timing"
          panel={
            <div className="mt-4">
              <ExitTimingDistribution
                exitSimulator={formData.exit_simulator}
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
        <h4 className="font-semibold mb-2">Portfolio Strategy Information</h4>
        <p>The portfolio strategy section defines comprehensive fund strategy across multiple dimensions:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Data & Zones:</strong> TLS data explorer and zone allocation strategy</li>
          <li><strong>Loan Parameters:</strong> LTV, size, and term constraints for individual loans</li>
          <li><strong>Leverage:</strong> Basic NAV line and subscription line facility setup</li>
          <li><strong>Capital Allocation:</strong> Reinvestment strategy and dynamic allocation</li>
          <li><strong>Exit Timing:</strong> Basic exit patterns, timing distributions, and appreciation sharing</li>
        </ul>
        <p className="mt-2 text-xs text-gray-600">
          Each tab contains detailed parameters that control different aspects of the fund's investment strategy and risk profile.
        </p>
      </div>
    </div>
  );
};

export default Step2PortfolioStrategy;
