/**
 * Preset configurations for quick simulation setup
 */

export interface PresetConfig {
  id: string;
  name: string;
  description: string;
  config: any;
}

/**
 * Comprehensive 100M Fund Preset Configuration
 * Uses the entire schema with realistic institutional values
 */
export const EQUIHOME_100M_FUND_PRESET: PresetConfig = {
  id: 'equihome-100m-fund',
  name: 'Equihome 100M Fund',
  description: 'Comprehensive 100M institutional fund with multi-tranche structure, leverage, and advanced features',
  config: {
    // Fund Basics
    fund_name: 'Equihome Fund I',
    fund_size: 100000000, // $100M
    fund_term: 10,
    vintage_year: 2024,
    management_fee_rate: 0.02, // 2%
    management_fee_basis: 'committed_capital',
    carried_interest_rate: 0.20, // 20%
    hurdle_rate: 0.08, // 8%
    waterfall_structure: 'european',
    gp_commitment_percentage: 0.02, // 2%
    catch_up_rate: 0.10, // 10%
    reinvestment_period: 5,

    // Tranche Manager - Multi-tranche institutional structure
    tranche_manager: {
      enabled: true,
      tranches: [
        {
          name: 'Senior Debt',
          size: 60000000, // $60M - 60%
          target_return: 0.06, // 6%
          priority: 1,
          type: 'senior_debt',
          interest_rate: 0.055, // 5.5%
          payment_frequency: 'quarterly',
          amortization: false,
          amortization_schedule: 'interest_only',
          term_years: 7,
          waterfall_rules: {
            hurdle_rate: 0.06,
            carried_interest_rate: 0.0,
            catch_up_rate: 0.0
          },
          allocation_rules: {
            zone_allocations: {
              green: 0.7,
              orange: 0.25,
              red: 0.05
            },
            ltv_constraints: {
              min_ltv: 0.4,
              max_ltv: 0.65
            }
          }
        },
        {
          name: 'Mezzanine',
          size: 25000000, // $25M - 25%
          target_return: 0.12, // 12%
          priority: 2,
          type: 'mezzanine',
          interest_rate: 0.10, // 10%
          payment_frequency: 'quarterly',
          amortization: false,
          amortization_schedule: 'interest_only',
          term_years: 8,
          waterfall_rules: {
            hurdle_rate: 0.10,
            carried_interest_rate: 0.15,
            catch_up_rate: 0.05
          },
          allocation_rules: {
            zone_allocations: {
              green: 0.6,
              orange: 0.3,
              red: 0.1
            },
            ltv_constraints: {
              min_ltv: 0.5,
              max_ltv: 0.75
            }
          }
        },
        {
          name: 'Equity',
          size: 15000000, // $15M - 15%
          target_return: 0.20, // 20%
          priority: 3,
          type: 'equity',
          interest_rate: 0.0, // No fixed interest
          payment_frequency: 'annual',
          amortization: false,
          amortization_schedule: 'balloon',
          term_years: 10,
          waterfall_rules: {
            hurdle_rate: 0.08,
            carried_interest_rate: 0.20,
            catch_up_rate: 0.10
          },
          allocation_rules: {
            zone_allocations: {
              green: 0.5,
              orange: 0.35,
              red: 0.15
            },
            ltv_constraints: {
              min_ltv: 0.3,
              max_ltv: 0.8
            }
          }
        }
      ],
      reserve_account: {
        enabled: true,
        target_percentage: 0.06, // 6% of senior debt
        initial_funding: 0.04, // 4% initial funding
        replenishment_rate: 0.15 // 15% replenishment rate
      },
      overcollateralization_test: {
        enabled: true,
        threshold: 1.25, // 125% OC ratio
        test_frequency: 'quarterly',
        cure_period_months: 6
      },
      interest_coverage_test: {
        enabled: true,
        threshold: 1.5, // 1.5x interest coverage
        test_frequency: 'quarterly',
        cure_period_months: 3
      }
    },

    // Cashflow Aggregator - Comprehensive settings
    cashflow_aggregator: {
      time_granularity: 'monthly',
      include_loan_level_cashflows: true,
      include_fund_level_cashflows: true,
      include_stakeholder_cashflows: true,
      simple_interest_rate: 0.05, // 5%
      origination_fee_rate: 0.03, // 3%
      appreciation_share_method: 'pro_rata_ltv',
      distribution_frequency: 'quarterly',
      distribution_lag: 2, // 2 months
      enable_parallel_processing: true,
      num_workers: 8,
      enable_scenario_analysis: true,
      scenarios: [
        {
          name: 'Base Case',
          description: 'Standard market conditions',
          parameters: {
            appreciation_multiplier: 1.0,
            default_multiplier: 1.0
          }
        },
        {
          name: 'Stress Case',
          description: 'Economic downturn scenario',
          parameters: {
            appreciation_multiplier: 0.7,
            default_multiplier: 2.0
          }
        }
      ],
      enable_sensitivity_analysis: true,
      sensitivity_parameters: [
        {
          parameter: 'interest_rate',
          min_value: 0.03,
          max_value: 0.08,
          step_size: 0.005
        },
        {
          parameter: 'default_rate',
          min_value: 0.01,
          max_value: 0.05,
          step_size: 0.005
        }
      ],
      enable_cashflow_metrics: true,
      discount_rate: 0.08, // 8%
      enable_tax_impact_analysis: true,
      tax_rates: {
        ordinary_income: 0.37, // 37%
        capital_gains: 0.20 // 20%
      },
      enable_reinvestment_modeling: true,
      reinvestment_rate: 0.90, // 90%
      enable_liquidity_analysis: true,
      minimum_cash_reserve: 0.08, // 8%
      enable_export: true,
      export_formats: ['csv', 'excel', 'pdf', 'json']
    },

    // Portfolio Strategy - Zone allocations and loan parameters
    zone_allocations: {
      green: 0.60, // 60% green zone
      orange: 0.30, // 30% orange zone
      red: 0.10 // 10% red zone
    },

    // LTV Parameters
    avg_loan_ltv: 0.40, // 40% average LTV
    min_ltv: 0.15, // 15% minimum
    max_ltv: 0.65, // 65% maximum
    ltv_std_dev: 0.08, // 8% standard deviation

    // Loan Size Parameters
    avg_loan_size: 400000, // $400K average
    min_loan_size: 50000, // $50K minimum
    max_loan_size: 1000000, // $1M maximum
    loan_size_std_dev: 0.25, // 25% standard deviation

    // Loan Terms
    avg_loan_term: 10, // 10 years average
    avg_loan_interest_rate: 0.05, // 5%

    // Zone-specific rates (from TLS data)
    appreciation_rates: {
      green: 0.075, // 7.5% green zone
      orange: 0.065, // 6.5% orange zone
      red: 0.055 // 5.5% red zone
    },
    default_rates: {
      green: 0.015, // 1.5% green zone
      orange: 0.025, // 2.5% orange zone
      red: 0.035 // 3.5% red zone
    },
    recovery_rates: {
      green: 0.85, // 85% green zone
      orange: 0.80, // 80% orange zone
      red: 0.75 // 75% red zone
    },

    // Leverage Engine - NAV line facility
    leverage_engine: {
      enabled: true,
      green_sleeve: {
        enabled: true,
        max_mult: 1.75, // 1.75x facility size
        spread_bps: 250, // 250 bps spread
        commitment_fee_bps: 50, // 50 bps commitment fee
        advance_rate: 0.80, // 80% advance rate
        min_dscr: 1.30, // 1.3x minimum DSCR
        max_ltv: 0.70 // 70% maximum LTV
      },
      ramp_line: {
        enabled: true,
        limit_pct_commit: 0.20, // 20% of commitments
        spread_bps: 275, // 275 bps spread
        commitment_fee_bps: 50, // 50 bps commitment fee
        draw_period_months: 30, // 30 months draw period
        term_months: 42 // 42 months total term
      },
      interest_rate_model: {
        base_rate_initial: 0.045, // 4.5% initial SOFR
        volatility: 0.015, // 1.5% volatility
        mean_reversion: 0.15, // 15% mean reversion
        long_term_mean: 0.04 // 4% long-term mean
      },
      optimization: {
        enabled: true,
        target_leverage: 0.65, // 65% target leverage
        max_leverage: 0.75, // 75% maximum leverage
        deleveraging_threshold: 0.80, // 80% deleveraging threshold
        min_cash_buffer: 2.0 // 2x debt service buffer
      },
      stress_testing: {
        enabled: true,
        interest_rate_shock: 0.025, // 250 bps shock
        nav_shock: 0.25, // 25% NAV shock
        liquidity_shock: 0.60 // 60% liquidity shock
      }
    },

    // Enhanced Leverage Parameters
    enhanced_leverage: {
      term_years: 7, // 7-year term
      amortization_years: 15, // 15-year amortization
      interest_only_period: 3, // 3 years interest-only
      prepayment_penalty: 0.025, // 2.5% prepayment penalty
      prepayment_lockout: 2 // 2-year lockout
    },

    // Fee Engine - Comprehensive fee structure
    fee_engine: {
      origination_fee_rate: 0.03, // 3%
      annual_fund_expenses: 0.008, // 0.8%
      fixed_annual_expenses: 500000, // $500K
      setup_costs: 1000000, // $1M
      expense_growth_rate: 0.025, // 2.5%
      acquisition_fee_rate: 0.01, // 1%
      disposition_fee_rate: 0.01, // 1%
      management_fee_schedule: [
        { year: 0, rate: 0.02 },
        { year: 1, rate: 0.02 },
        { year: 2, rate: 0.02 },
        { year: 3, rate: 0.02 },
        { year: 4, rate: 0.02 },
        { year: 5, rate: 0.02 }, // No step down - 2% for whole term
        { year: 6, rate: 0.02 },
        { year: 7, rate: 0.02 },
        { year: 8, rate: 0.02 },
        { year: 9, rate: 0.02 }
      ]
    },

    // Reinvestment Engine - Capital allocation strategy
    reinvestment_engine: {
      reinvestment_strategy: 'dynamic_allocation',
      min_reinvestment_amount: 200000, // $200K minimum
      reinvestment_frequency: 'monthly',
      reinvestment_delay: 2, // 2 months delay
      reinvestment_batch_size: 25, // 25 loans per batch
      zone_preference_multipliers: {
        green: 1.2, // 20% preference for green
        orange: 1.0, // Neutral for orange
        red: 0.8 // 20% discount for red
      },
      opportunistic_threshold: 0.15, // 15% threshold
      rebalance_threshold: 0.08, // 8% rebalance threshold
      reinvestment_ltv_adjustment: 0.02, // 2% LTV adjustment
      reinvestment_size_adjustment: 0.05, // 5% size adjustment
      enable_dynamic_allocation: true,
      performance_lookback_period: 18, // 18 months
      performance_weight: 0.40, // 40% performance weight
      max_allocation_adjustment: 0.15, // 15% max adjustment
      enable_cash_reserve: true,
      cash_reserve_target: 0.08, // 8% target
      cash_reserve_min: 0.05, // 5% minimum
      cash_reserve_max: 0.12 // 12% maximum
    },

    // Exit Simulator - Comprehensive exit modeling
    exit_simulator: {
      base_exit_rate: 0.18, // 18% base exit rate
      time_factor: 0.65, // 65% time factor
      price_factor: 0.35, // 35% price factor
      min_hold_period: 2.0, // 2 years minimum
      max_hold_period: 10.0, // 10 years maximum (fund term)
      sale_weight: 0.75, // 75% sale weight
      refinance_weight: 0.20, // 20% refinance weight
      default_weight: 0.05, // 5% default weight
      appreciation_sale_multiplier: 2.5, // 2.5x appreciation multiplier
      interest_rate_refinance_multiplier: 1.8, // 1.8x interest rate multiplier
      economic_factor_default_multiplier: 1.5, // 1.5x economic factor multiplier
      appreciation_share: 0.55, // 55% appreciation share
      min_appreciation_share: 0.35, // 35% minimum
      max_appreciation_share: 0.75, // 75% maximum
      tiered_appreciation_thresholds: [0.10, 0.25, 0.50], // 10%, 25%, 50%
      tiered_appreciation_shares: [0.35, 0.55, 0.75], // 35%, 55%, 75%
      base_default_rate: 0.025, // 2.5% base default rate
      recovery_rate: 0.82, // 82% recovery rate
      foreclosure_cost: 0.08, // 8% foreclosure cost
      foreclosure_time: 1.2 // 1.2 years foreclosure time
    },

    // Enhanced Exit Simulator - Advanced exit modeling
    enhanced_exit_simulator: {
      enabled: true,
      exit_year_mean: 2.5, // 2.5 years mean exit
      exit_year_std_dev: 1.5, // 18 months (1.5 years) standard deviation
      early_exit_penalty: 0.015, // 1.5% early exit penalty
      late_exit_bonus: 0.005, // 0.5% late exit bonus
      market_timing_factor: 0.25, // 25% market timing factor
      borrower_behavior_factor: 0.35, // 35% borrower behavior factor
      fund_strategy_factor: 0.40, // 40% fund strategy factor
      enable_seasonal_effects: true,
      seasonal_multipliers: {
        q1: 0.85, // Q1 multiplier
        q2: 1.15, // Q2 multiplier
        q3: 1.05, // Q3 multiplier
        q4: 0.95 // Q4 multiplier
      },
      enable_economic_cycles: true,
      cycle_length_years: 8.5, // 8.5 year cycle
      cycle_amplitude: 0.20, // 20% amplitude
      recession_probability: 0.15, // 15% recession probability
      recession_exit_multiplier: 0.60 // 60% recession multiplier
    },

    // Price Path - Market dynamics
    price_path: {
      base_appreciation_rate: 0.065, // 6.5% base appreciation
      volatility: 0.12, // 12% volatility
      mean_reversion_speed: 0.25, // 25% mean reversion
      long_term_growth_rate: 0.055, // 5.5% long-term growth
      enable_cycles: true,
      cycle_length: 9.0, // 9 year cycle
      cycle_amplitude: 0.15, // 15% amplitude
      enable_shocks: true,
      shock_probability: 0.08, // 8% shock probability
      shock_magnitude: 0.18, // 18% shock magnitude
      shock_duration: 2.5, // 2.5 years duration
      correlation_with_interest_rates: -0.65, // -65% correlation
      correlation_with_unemployment: -0.45, // -45% correlation
      regional_factor: 1.08 // 8% regional premium
    },

    // Risk Metrics - Comprehensive risk analysis
    risk_metrics: {
      enable_var_calculation: true,
      var_confidence_level: 0.95, // 95% confidence
      var_time_horizon: 252, // 252 days (1 year)
      enable_stress_testing: true,
      stress_scenarios: [
        {
          name: 'Interest Rate Shock',
          description: '300 bps rate increase',
          interest_rate_shock: 0.03,
          property_value_shock: -0.15,
          default_rate_shock: 2.0,
          liquidity_shock: 0.4
        },
        {
          name: 'Property Market Crash',
          description: '30% property value decline',
          interest_rate_shock: 0.01,
          property_value_shock: -0.30,
          default_rate_shock: 3.5,
          liquidity_shock: 0.7
        }
      ],
      monte_carlo_simulations: 0, // Monte Carlo disabled
      tail_risk_threshold: 0.05, // 5% tail risk
      enable_sensitivity_analysis: true,
      sensitivity_parameters: [
        'interest_rate',
        'property_value_growth',
        'default_rate',
        'ltv_ratio',
        'leverage_ratio'
      ]
    },

    // Variation Factors - Statistical modeling
    variation_factors: {
      interest_rate_volatility: 0.015, // 1.5% volatility
      property_value_volatility: 0.12, // 12% volatility
      default_rate_volatility: 0.25, // 25% volatility
      prepayment_rate_volatility: 0.20, // 20% volatility
      correlation_stability: 0.85 // 85% stability
    },

    // Correlation Matrix - Risk factor correlations
    correlation_matrix: {
      interest_rate_property_value: -0.45,
      interest_rate_default_rate: 0.35,
      interest_rate_prepayment_rate: -0.25,
      property_value_default_rate: -0.55,
      property_value_prepayment_rate: 0.40,
      default_rate_prepayment_rate: -0.15,
      price_path_exit_events: 0.65,
      price_path_default_events: -0.40,
      price_path_prepayment_events: 0.30,
      default_events_prepayment_events: -0.20
    },

    // Deterministic Mode
    deterministic_mode: false // Use stochastic modeling
  }
};

/**
 * Get all available presets
 */
export const getAvailablePresets = (): PresetConfig[] => {
  return [EQUIHOME_100M_FUND_PRESET];
};

/**
 * Get preset by ID
 */
export const getPresetById = (id: string): PresetConfig | undefined => {
  return getAvailablePresets().find(preset => preset.id === id);
};
