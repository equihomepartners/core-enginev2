import { z } from 'zod';
import simulationConfigSchemaJson from '../../../schemas/simulation_config_schema.json';

// Use the actual schema from the schemas directory
const simulationConfigSchema = simulationConfigSchemaJson;

/**
 * Extract default values from a JSON schema
 * @param schema JSON schema object
 * @returns Object with default values
 */
export function extractDefaultValues(schema: any): Record<string, any> {
  const defaults: Record<string, any> = {};

  if (!schema || typeof schema !== 'object') {
    return defaults;
  }

  // Handle direct default value
  if ('default' in schema) {
    return schema.default;
  }

  // Handle object properties
  if (schema.type === 'object' && schema.properties) {
    Object.entries(schema.properties).forEach(([key, propSchema]: [string, any]) => {
      defaults[key] = extractDefaultValues(propSchema);
    });
  }

  return defaults;
}

/**
 * Create a Zod schema from a JSON schema property
 * @param schema JSON schema property
 * @returns Zod schema
 */
export function createZodSchema(schema: any): z.ZodTypeAny {
  if (!schema || typeof schema !== 'object') {
    return z.any();
  }

  // Handle different types
  switch (schema.type) {
    case 'string':
      let stringSchema = z.string();

      if (schema.enum) {
        return z.enum(schema.enum as [string, ...string[]]);
      }

      if (schema.minLength) {
        stringSchema = stringSchema.min(schema.minLength);
      }

      if (schema.maxLength) {
        stringSchema = stringSchema.max(schema.maxLength);
      }

      if (schema.pattern) {
        stringSchema = stringSchema.regex(new RegExp(schema.pattern));
      }

      return stringSchema;

    case 'number':
    case 'integer':
      let numberSchema = schema.type === 'integer' ? z.number().int() : z.number();

      if (schema.minimum !== undefined) {
        numberSchema = numberSchema.min(schema.minimum);
      }

      if (schema.maximum !== undefined) {
        numberSchema = numberSchema.max(schema.maximum);
      }

      return numberSchema;

    case 'boolean':
      return z.boolean();

    case 'object':
      if (!schema.properties) {
        return z.record(z.any());
      }

      const shape: Record<string, z.ZodTypeAny> = {};

      Object.entries(schema.properties).forEach(([key, propSchema]: [string, any]) => {
        shape[key] = createZodSchema(propSchema);
      });

      let objectSchema = z.object(shape);

      // Handle required properties
      if (schema.required && Array.isArray(schema.required)) {
        const required = schema.required as string[];
        objectSchema = objectSchema.refine(
          (data) => required.every(key => key in data && data[key] !== undefined),
          {
            message: `Required properties: ${required.join(', ')}`,
            path: required,
          }
        );
      }

      return objectSchema;

    case 'array':
      if (!schema.items) {
        return z.array(z.any());
      }

      const itemSchema = createZodSchema(schema.items);
      let arraySchema = z.array(itemSchema);

      if (schema.minItems) {
        arraySchema = arraySchema.min(schema.minItems);
      }

      if (schema.maxItems) {
        arraySchema = arraySchema.max(schema.maxItems);
      }

      return arraySchema;

    case 'null':
      return z.null();

    default:
      if (Array.isArray(schema.type)) {
        // Handle union types
        const unionSchemas = schema.type.map((type: string) => {
          return createZodSchema({ ...schema, type });
        });
        return z.union(unionSchemas);
      }

      return z.any();
  }
}

/**
 * Get fund basics schema
 * @returns Fund basics schema
 */
export function getFundBasicsSchema() {
  // Extract the relevant properties for fund basics
  const fundBasicsProperties = {
    fund_name: {
      type: 'string',
      description: 'Fund name',
      default: 'Equihome Fund I'
    },
    fund_size: simulationConfigSchema.properties.fund_size,
    fund_term: simulationConfigSchema.properties.fund_term,
    vintage_year: simulationConfigSchema.properties.vintage_year,
    hurdle_rate: simulationConfigSchema.properties.hurdle_rate,
    carried_interest_rate: simulationConfigSchema.properties.carried_interest_rate,
    management_fee_rate: simulationConfigSchema.properties.management_fee_rate,
    management_fee_basis: simulationConfigSchema.properties.management_fee_basis,
    waterfall_structure: simulationConfigSchema.properties.waterfall_structure,
    gp_commitment_percentage: simulationConfigSchema.properties.gp_commitment_percentage,
    catch_up_rate: simulationConfigSchema.properties.catch_up_rate,
    reinvestment_period: {
      type: 'number',
      description: 'Reinvestment period in years',
      minimum: 0,
      maximum: 20,
      default: 5
    },
    loan_size_std_dev: {
      type: 'number',
      description: 'Standard deviation of loan sizes',
      minimum: 0,
      maximum: 1,
      default: 0.2
    },
    ltv_std_dev: {
      type: 'number',
      description: 'Standard deviation of LTV ratios',
      minimum: 0,
      maximum: 1,
      default: 0.1
    },
    tranche_manager: simulationConfigSchema.properties.tranche_manager,
    cashflow_aggregator: {
      type: 'object',
      description: 'Cashflow aggregator parameters',
      properties: {
        time_granularity: {
          type: 'string',
          enum: ['daily', 'monthly', 'quarterly', 'yearly'],
          default: 'monthly'
        },
        include_loan_level_cashflows: { type: 'boolean', default: true },
        include_fund_level_cashflows: { type: 'boolean', default: true },
        include_stakeholder_cashflows: { type: 'boolean', default: true },
        simple_interest_rate: { type: 'number', minimum: 0, maximum: 1, default: 0.05 },
        origination_fee_rate: { type: 'number', minimum: 0, maximum: 0.1, default: 0.01 },
        appreciation_share_method: {
          type: 'string',
          enum: ['pro_rata_ltv', 'tiered', 'fixed'],
          default: 'pro_rata_ltv'
        },
        distribution_frequency: {
          type: 'string',
          enum: ['monthly', 'quarterly', 'semi_annual', 'annual'],
          default: 'quarterly'
        },
        distribution_lag: { type: 'number', minimum: 0, maximum: 12, default: 1 },
        enable_parallel_processing: { type: 'boolean', default: false },
        num_workers: { type: 'integer', minimum: 1, maximum: 32, default: 4 },
        enable_scenario_analysis: { type: 'boolean', default: false },
        scenarios: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              description: { type: 'string' },
              parameters: { type: 'object' }
            }
          },
          default: []
        },
        enable_sensitivity_analysis: { type: 'boolean', default: false },
        sensitivity_parameters: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              parameter: { type: 'string' },
              min_value: { type: 'number' },
              max_value: { type: 'number' },
              step_size: { type: 'number' }
            }
          },
          default: []
        },
        enable_cashflow_metrics: { type: 'boolean', default: true },
        discount_rate: { type: 'number', minimum: 0, maximum: 1, default: 0.08 },
        enable_tax_impact_analysis: { type: 'boolean', default: false },
        tax_rates: {
          type: 'object',
          properties: {
            ordinary_income: { type: 'number', minimum: 0, maximum: 1, default: 0.37 },
            capital_gains: { type: 'number', minimum: 0, maximum: 1, default: 0.20 }
          },
          default: {
            ordinary_income: 0.37,
            capital_gains: 0.20
          }
        },
        enable_reinvestment_modeling: { type: 'boolean', default: false },
        reinvestment_rate: { type: 'number', minimum: 0, maximum: 1, default: 0.05 },
        enable_liquidity_analysis: { type: 'boolean', default: false },
        minimum_cash_reserve: { type: 'number', minimum: 0, maximum: 1, default: 0.05 },
        enable_export: { type: 'boolean', default: true },
        export_formats: {
          type: 'array',
          items: {
            type: 'string',
            enum: ['csv', 'excel', 'pdf', 'json']
          },
          default: ['csv', 'excel']
        }
      },
      default: {
        time_granularity: 'monthly',
        include_loan_level_cashflows: true,
        include_fund_level_cashflows: true,
        include_stakeholder_cashflows: true,
        simple_interest_rate: 0.05,
        origination_fee_rate: 0.01,
        appreciation_share_method: 'pro_rata_ltv',
        distribution_frequency: 'quarterly',
        distribution_lag: 1,
        enable_parallel_processing: false,
        num_workers: 4,
        enable_scenario_analysis: false,
        scenarios: [],
        enable_sensitivity_analysis: false,
        sensitivity_parameters: [],
        enable_cashflow_metrics: true,
        discount_rate: 0.08,
        enable_tax_impact_analysis: false,
        tax_rates: {
          ordinary_income: 0.37,
          capital_gains: 0.20
        },
        enable_reinvestment_modeling: false,
        reinvestment_rate: 0.05,
        enable_liquidity_analysis: false,
        minimum_cash_reserve: 0.05,
        enable_export: true,
        export_formats: ['csv', 'excel']
      }
    },
    fee_engine: simulationConfigSchema.properties.fee_engine
  };

  return {
    type: 'object',
    properties: fundBasicsProperties,
    required: ['fund_name', 'fund_size', 'fund_term', 'vintage_year']
  };
}

/**
 * Get fund basics default values
 * @returns Fund basics default values
 */
export function getFundBasicsDefaults() {
  const schema = getFundBasicsSchema();
  return extractDefaultValues(schema);
}

/**
 * Get fund basics Zod validation schema
 * @returns Zod validation schema for fund basics
 */
export function getFundBasicsValidationSchema() {
  const schema = getFundBasicsSchema();
  return createZodSchema(schema);
}

/**
 * Get portfolio strategy schema
 * @returns Portfolio strategy schema
 */
export function getPortfolioStrategySchema() {
  // Extract the relevant properties for portfolio strategy
  const portfolioStrategyProperties = {
    zone_allocations: {
      type: 'object',
      description: 'Target zone allocations',
      properties: {
        green: {
          type: 'number',
          description: 'Green zone allocation (0-1)',
          minimum: 0,
          maximum: 1,
          default: 0.6
        },
        orange: {
          type: 'number',
          description: 'Orange zone allocation (0-1)',
          minimum: 0,
          maximum: 1,
          default: 0.3
        },
        red: {
          type: 'number',
          description: 'Red zone allocation (0-1)',
          minimum: 0,
          maximum: 1,
          default: 0.1
        }
      },
      additionalProperties: false
    },
    avg_loan_ltv: {
      type: 'number',
      description: 'Average loan LTV ratio (0-1)',
      minimum: 0,
      maximum: 1,
      default: 0.5
    },
    min_ltv: {
      type: 'number',
      description: 'Minimum LTV ratio (0-1)',
      minimum: 0,
      maximum: 1,
      default: 0.3
    },
    max_ltv: {
      type: 'number',
      description: 'Maximum LTV ratio (0-1)',
      minimum: 0,
      maximum: 1,
      default: 0.7
    },
    avg_loan_size: {
      type: 'number',
      description: 'Average loan size in dollars',
      minimum: 10000,
      default: 250000
    },
    min_loan_size: {
      type: 'number',
      description: 'Minimum loan size in dollars',
      minimum: 1000,
      default: 100000
    },
    max_loan_size: {
      type: 'number',
      description: 'Maximum loan size in dollars',
      minimum: 10000,
      default: 500000
    },
    ltv_std_dev: {
      type: 'number',
      description: 'LTV standard deviation',
      minimum: 0,
      maximum: 1,
      default: 0.05
    },
    loan_size_std_dev: {
      type: 'number',
      description: 'Loan size standard deviation',
      minimum: 0,
      default: 50000
    },
    avg_loan_term: {
      type: 'number',
      description: 'Average loan term in years',
      minimum: 0.5,
      maximum: 30,
      default: 5
    },
    avg_loan_interest_rate: {
      type: 'number',
      description: 'Average loan interest rate',
      minimum: 0,
      maximum: 1,
      default: 0.05
    },
    appreciation_rates: {
      type: 'object',
      description: 'Zone-specific appreciation rates',
      properties: {
        green: { type: 'number', minimum: 0, maximum: 1, default: 0.072 },
        orange: { type: 'number', minimum: 0, maximum: 1, default: 0.072 },
        red: { type: 'number', minimum: 0, maximum: 1, default: 0.059 }
      },
      default: { green: 0.072, orange: 0.072, red: 0.059 }
    },
    default_rates: {
      type: 'object',
      description: 'Zone-specific default rates',
      properties: {
        green: { type: 'number', minimum: 0, maximum: 1, default: 0.02 },
        orange: { type: 'number', minimum: 0, maximum: 1, default: 0.022 },
        red: { type: 'number', minimum: 0, maximum: 1, default: 0.023 }
      },
      default: { green: 0.02, orange: 0.022, red: 0.023 }
    },
    recovery_rates: {
      type: 'object',
      description: 'Zone-specific recovery rates',
      properties: {
        green: { type: 'number', minimum: 0, maximum: 1, default: 0.82 },
        orange: { type: 'number', minimum: 0, maximum: 1, default: 0.80 },
        red: { type: 'number', minimum: 0, maximum: 1, default: 0.79 }
      },
      default: { green: 0.82, orange: 0.80, red: 0.79 }
    },
    leverage_engine: {
      type: 'object',
      description: 'Leverage engine parameters',
      properties: {
        enabled: { type: 'boolean', default: false },
        green_sleeve: {
          type: 'object',
          properties: {
            enabled: { type: 'boolean', default: false },
            max_mult: { type: 'number', minimum: 0, maximum: 5, default: 2.0 },
            spread_bps: { type: 'number', minimum: 0, maximum: 1000, default: 200 },
            commitment_fee_bps: { type: 'number', minimum: 0, maximum: 100, default: 25 },
            advance_rate: { type: 'number', minimum: 0, maximum: 1, default: 0.75 },
            min_dscr: { type: 'number', minimum: 0, default: 1.25 },
            max_ltv: { type: 'number', minimum: 0, maximum: 1, default: 0.65 }
          },
          default: {
            enabled: false,
            max_mult: 2.0,
            spread_bps: 200,
            commitment_fee_bps: 25,
            advance_rate: 0.75,
            min_dscr: 1.25,
            max_ltv: 0.65
          }
        },
        ramp_line: {
          type: 'object',
          properties: {
            enabled: { type: 'boolean', default: false },
            limit_pct_commit: { type: 'number', minimum: 0, maximum: 1, default: 0.15 },
            spread_bps: { type: 'number', minimum: 0, maximum: 1000, default: 300 },
            commitment_fee_bps: { type: 'number', minimum: 0, maximum: 100, default: 50 },
            draw_period_months: { type: 'number', minimum: 0, maximum: 60, default: 24 },
            term_months: { type: 'number', minimum: 0, maximum: 60, default: 36 }
          },
          default: {
            enabled: false,
            limit_pct_commit: 0.15,
            spread_bps: 300,
            commitment_fee_bps: 50,
            draw_period_months: 24,
            term_months: 36
          }
        },
        interest_rate_model: {
          type: 'object',
          properties: {
            base_rate_initial: { type: 'number', minimum: 0, maximum: 0.2, default: 0.0425 },
            volatility: { type: 'number', minimum: 0, maximum: 0.1, default: 0.01 },
            mean_reversion: { type: 'number', minimum: 0, maximum: 1, default: 0.1 },
            long_term_mean: { type: 'number', minimum: 0, maximum: 0.2, default: 0.04 }
          },
          default: {
            base_rate_initial: 0.0425,
            volatility: 0.01,
            mean_reversion: 0.1,
            long_term_mean: 0.04
          }
        },
        optimization: {
          type: 'object',
          properties: {
            enabled: { type: 'boolean', default: false },
            target_leverage: { type: 'number', minimum: 0, maximum: 5, default: 1.5 },
            max_leverage: { type: 'number', minimum: 0, maximum: 5, default: 2.0 },
            deleveraging_threshold: { type: 'number', minimum: 0, maximum: 5, default: 2.5 },
            min_cash_buffer: { type: 'number', minimum: 0, maximum: 5, default: 1.5 }
          },
          default: {
            enabled: false,
            target_leverage: 1.5,
            max_leverage: 2.0,
            deleveraging_threshold: 2.5,
            min_cash_buffer: 1.5
          }
        },
        stress_testing: {
          type: 'object',
          properties: {
            enabled: { type: 'boolean', default: true },
            interest_rate_shock: { type: 'number', minimum: 0, maximum: 0.1, default: 0.02 },
            nav_shock: { type: 'number', minimum: 0, maximum: 1, default: 0.2 },
            liquidity_shock: { type: 'number', minimum: 0, maximum: 1, default: 0.5 }
          },
          default: {
            enabled: true,
            interest_rate_shock: 0.02,
            nav_shock: 0.2,
            liquidity_shock: 0.5
          }
        }
      },
      default: {
        enabled: false,
        green_sleeve: {
          enabled: false,
          max_mult: 2.0,
          spread_bps: 200,
          commitment_fee_bps: 25,
          advance_rate: 0.75,
          min_dscr: 1.25,
          max_ltv: 0.65
        },
        optimization: {
          enabled: false,
          target_leverage: 1.5,
          max_leverage: 2.0,
          deleveraging_threshold: 2.5
        }
      }
    },
    enhanced_leverage: {
      type: 'object',
      description: 'Enhanced leverage parameters',
      properties: {
        term_years: { type: 'number', minimum: 0, maximum: 30, default: 5 },
        amortization_years: { type: 'number', minimum: 0, maximum: 30, default: 10 },
        interest_only_period: { type: 'number', minimum: 0, maximum: 30, default: 2 },
        prepayment_penalty: { type: 'number', minimum: 0, maximum: 0.1, default: 0.02 },
        prepayment_lockout: { type: 'number', minimum: 0, maximum: 30, default: 1 }
      },
      default: {
        term_years: 5,
        amortization_years: 10,
        interest_only_period: 2,
        prepayment_penalty: 0.02,
        prepayment_lockout: 1
      }
    },
    reinvestment_engine: {
      type: 'object',
      description: 'Reinvestment engine parameters',
      properties: {
        reinvestment_strategy: { type: 'string', enum: ['maintain_allocation', 'rebalance', 'opportunistic', 'custom'], default: 'maintain_allocation' },
        min_reinvestment_amount: { type: 'number', minimum: 0, default: 100000 },
        reinvestment_frequency: { type: 'string', enum: ['monthly', 'quarterly', 'semi_annually', 'annually', 'on_exit'], default: 'quarterly' },
        reinvestment_delay: { type: 'number', minimum: 0, maximum: 24, default: 3 },
        reinvestment_batch_size: { type: 'number', minimum: 1, maximum: 1000, default: 50 },
        zone_preference_multipliers: {
          type: 'object',
          properties: {
            green: { type: 'number', minimum: 0, maximum: 10, default: 1.0 },
            orange: { type: 'number', minimum: 0, maximum: 10, default: 1.0 },
            red: { type: 'number', minimum: 0, maximum: 10, default: 1.0 }
          },
          default: { green: 1.0, orange: 1.0, red: 1.0 }
        },
        opportunistic_threshold: { type: 'number', minimum: 0, maximum: 1, default: 0.1 },
        rebalance_threshold: { type: 'number', minimum: 0, maximum: 1, default: 0.05 },
        reinvestment_ltv_adjustment: { type: 'number', minimum: -1, maximum: 1, default: 0.0 },
        reinvestment_size_adjustment: { type: 'number', minimum: -1, maximum: 1, default: 0.0 },
        enable_dynamic_allocation: { type: 'boolean', default: false },
        performance_lookback_period: { type: 'number', minimum: 1, maximum: 60, default: 12 },
        performance_weight: { type: 'number', minimum: 0, maximum: 1, default: 0.3 },
        max_allocation_adjustment: { type: 'number', minimum: 0, maximum: 1, default: 0.1 },
        enable_cash_reserve: { type: 'boolean', default: false },
        cash_reserve_target: { type: 'number', minimum: 0, maximum: 1, default: 0.05 },
        cash_reserve_min: { type: 'number', minimum: 0, maximum: 1, default: 0.02 },
        cash_reserve_max: { type: 'number', minimum: 0, maximum: 1, default: 0.1 }
      },
      default: {
        reinvestment_strategy: 'maintain_allocation',
        min_reinvestment_amount: 100000,
        reinvestment_frequency: 'quarterly',
        reinvestment_delay: 3,
        reinvestment_batch_size: 50,
        zone_preference_multipliers: { green: 1.0, orange: 1.0, red: 1.0 },
        opportunistic_threshold: 0.1,
        rebalance_threshold: 0.05,
        reinvestment_ltv_adjustment: 0.0,
        reinvestment_size_adjustment: 0.0,
        enable_dynamic_allocation: false,
        performance_lookback_period: 12,
        performance_weight: 0.3,
        max_allocation_adjustment: 0.1,
        enable_cash_reserve: false,
        cash_reserve_target: 0.05,
        cash_reserve_min: 0.02,
        cash_reserve_max: 0.1
      }
    },
    exit_simulator: {
      type: 'object',
      description: 'Exit simulator parameters',
      properties: {
        base_exit_rate: { type: 'number', minimum: 0, maximum: 0.5, default: 0.15 },
        time_factor: { type: 'number', minimum: 0, maximum: 1, default: 0.6 },
        price_factor: { type: 'number', minimum: 0, maximum: 1, default: 0.4 },
        min_hold_period: { type: 'number', minimum: 0, maximum: 30, default: 1.0 },
        max_hold_period: { type: 'number', minimum: 0, maximum: 30, default: 10.0 },
        sale_weight: { type: 'number', minimum: 0, maximum: 1, default: 0.7 },
        refinance_weight: { type: 'number', minimum: 0, maximum: 1, default: 0.25 },
        default_weight: { type: 'number', minimum: 0, maximum: 1, default: 0.05 },
        appreciation_sale_multiplier: { type: 'number', minimum: 0, maximum: 10, default: 2.0 },
        interest_rate_refinance_multiplier: { type: 'number', minimum: 0, maximum: 10, default: 1.5 },
        economic_factor_default_multiplier: { type: 'number', minimum: 0, maximum: 10, default: 1.2 },
        appreciation_share: { type: 'number', minimum: 0, maximum: 1, default: 0.5 },
        min_appreciation_share: { type: 'number', minimum: 0, maximum: 1, default: 0.3 },
        max_appreciation_share: { type: 'number', minimum: 0, maximum: 1, default: 0.7 },
        tiered_appreciation_thresholds: { type: 'array', items: { type: 'number' }, default: [0.1, 0.2, 0.3] },
        tiered_appreciation_shares: { type: 'array', items: { type: 'number' }, default: [0.3, 0.5, 0.7] },
        base_default_rate: { type: 'number', minimum: 0, maximum: 1, default: 0.02 },
        recovery_rate: { type: 'number', minimum: 0, maximum: 1, default: 0.8 },
        foreclosure_cost: { type: 'number', minimum: 0, maximum: 1, default: 0.1 },
        foreclosure_time: { type: 'number', minimum: 0, maximum: 10, default: 1.5 }
      },
      default: {
        base_exit_rate: 0.15,
        time_factor: 0.6,
        price_factor: 0.4,
        min_hold_period: 1.0,
        max_hold_period: 10.0,
        sale_weight: 0.7,
        refinance_weight: 0.25,
        default_weight: 0.05,
        appreciation_sale_multiplier: 2.0,
        interest_rate_refinance_multiplier: 1.5,
        economic_factor_default_multiplier: 1.2,
        appreciation_share: 0.5,
        min_appreciation_share: 0.3,
        max_appreciation_share: 0.7,
        tiered_appreciation_thresholds: [0.1, 0.2, 0.3],
        tiered_appreciation_shares: [0.3, 0.5, 0.7],
        base_default_rate: 0.02,
        recovery_rate: 0.8,
        foreclosure_cost: 0.1,
        foreclosure_time: 1.5
      }
    },
    price_path: {
      type: 'object',
      description: 'Price path parameters',
      properties: {
        model_type: { type: 'string', enum: ['gbm', 'mean_reversion', 'regime_switching'], default: 'gbm' },
        volatility: {
          type: 'object',
          properties: {
            green: { type: 'number', minimum: 0, maximum: 0.2, default: 0.08 },
            orange: { type: 'number', minimum: 0, maximum: 0.2, default: 0.091 },
            red: { type: 'number', minimum: 0, maximum: 0.2, default: 0.103 }
          },
          default: { green: 0.08, orange: 0.091, red: 0.103 }
        },
        correlation_matrix: {
          type: 'object',
          properties: {
            green_orange: { type: 'number', minimum: -1, maximum: 1, default: 0.7 },
            green_red: { type: 'number', minimum: -1, maximum: 1, default: 0.5 },
            orange_red: { type: 'number', minimum: -1, maximum: 1, default: 0.8 }
          },
          default: { green_orange: 0.7, green_red: 0.5, orange_red: 0.8 }
        },
        mean_reversion_params: {
          type: 'object',
          properties: {
            speed: { type: 'number', minimum: 0, maximum: 1, default: 0.1 },
            long_term_mean: { type: 'number', minimum: 0, maximum: 1, default: 0.05 }
          },
          default: { speed: 0.1, long_term_mean: 0.05 }
        },
        regime_switching_params: {
          type: 'object',
          properties: {
            bull_market_rate: { type: 'number', minimum: 0, maximum: 1, default: 0.08 },
            bear_market_rate: { type: 'number', minimum: -1, maximum: 1, default: -0.02 },
            bull_to_bear_prob: { type: 'number', minimum: 0, maximum: 1, default: 0.1 },
            bear_to_bull_prob: { type: 'number', minimum: 0, maximum: 1, default: 0.2 }
          },
          default: { bull_market_rate: 0.08, bear_market_rate: -0.02, bull_to_bear_prob: 0.1, bear_to_bull_prob: 0.2 }
        },
        time_step: { type: 'string', enum: ['monthly', 'quarterly', 'yearly'], default: 'monthly' },
        suburb_variation: { type: 'number', minimum: 0, maximum: 1, default: 0.02 },
        property_variation: { type: 'number', minimum: 0, maximum: 1, default: 0.01 },
        cycle_position: { type: 'number', minimum: 0, maximum: 1, default: 0.5 }
      },
      default: {
        model_type: 'gbm',
        volatility: { green: 0.08, orange: 0.091, red: 0.103 },
        correlation_matrix: { green_orange: 0.7, green_red: 0.5, orange_red: 0.8 },
        mean_reversion_params: { speed: 0.1, long_term_mean: 0.05 },
        regime_switching_params: { bull_market_rate: 0.08, bear_market_rate: -0.02, bull_to_bear_prob: 0.1, bear_to_bull_prob: 0.2 },
        time_step: 'monthly',
        suburb_variation: 0.02,
        property_variation: 0.01,
        cycle_position: 0.5
      }
    },
    enhanced_exit_simulator: {
      type: 'object',
      description: 'Enhanced exit simulator parameters',
      properties: {
        refinance_interest_rate_sensitivity: { type: 'number', minimum: 0, maximum: 10, default: 2.0 },
        sale_appreciation_sensitivity: { type: 'number', minimum: 0, maximum: 10, default: 1.5 },
        life_event_probability: { type: 'number', minimum: 0, maximum: 1, default: 0.05 },
        behavioral_correlation: { type: 'number', minimum: 0, maximum: 1, default: 0.3 },
        recession_default_multiplier: { type: 'number', minimum: 0, maximum: 10, default: 2.5 },
        inflation_refinance_multiplier: { type: 'number', minimum: 0, maximum: 10, default: 1.8 },
        employment_sensitivity: { type: 'number', minimum: 0, maximum: 10, default: 1.2 },
        migration_sensitivity: { type: 'number', minimum: 0, maximum: 10, default: 0.8 },
        regulatory_compliance_cost: { type: 'number', minimum: 0, maximum: 1, default: 0.01 },
        tax_efficiency_factor: { type: 'number', minimum: 0, maximum: 1, default: 0.9 },
        vintage_segmentation: { type: 'boolean', default: true },
        ltv_segmentation: { type: 'boolean', default: true },
        zone_segmentation: { type: 'boolean', default: true },
        var_confidence_level: { type: 'number', minimum: 0, maximum: 1, default: 0.95 },
        stress_test_severity: { type: 'number', minimum: 0, maximum: 1, default: 0.3 },
        tail_risk_threshold: { type: 'number', minimum: 0, maximum: 1, default: 0.05 },
        use_ml_models: { type: 'boolean', default: true },
        feature_importance_threshold: { type: 'number', minimum: 0, maximum: 1, default: 0.05 },
        anomaly_detection_threshold: { type: 'number', minimum: 0, maximum: 10, default: 3.0 }
      },
      default: {
        refinance_interest_rate_sensitivity: 2.0,
        sale_appreciation_sensitivity: 1.5,
        life_event_probability: 0.05,
        behavioral_correlation: 0.3,
        recession_default_multiplier: 2.5,
        inflation_refinance_multiplier: 1.8,
        employment_sensitivity: 1.2,
        migration_sensitivity: 0.8,
        regulatory_compliance_cost: 0.01,
        tax_efficiency_factor: 0.9,
        vintage_segmentation: true,
        ltv_segmentation: true,
        zone_segmentation: true,
        var_confidence_level: 0.95,
        stress_test_severity: 0.3,
        tail_risk_threshold: 0.05,
        use_ml_models: true,
        feature_importance_threshold: 0.05,
        anomaly_detection_threshold: 3.0
      }
    },
    risk_metrics: {
      type: 'object',
      description: 'Risk metrics parameters',
      properties: {
        var_confidence_level: { type: 'number', minimum: 0.8, maximum: 0.99, default: 0.95 },
        risk_free_rate: { type: 'number', minimum: 0, maximum: 0.1, default: 0.03 },
        benchmark_return: { type: 'number', minimum: 0, maximum: 0.2, default: 0.07 },
        min_acceptable_return: { type: 'number', minimum: 0, maximum: 0.1, default: 0.04 },
        stress_test_scenarios: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              description: { type: 'string' },
              property_value_shock: { type: 'number', minimum: -1, maximum: 1 },
              interest_rate_shock: { type: 'number', minimum: -0.1, maximum: 0.1 },
              default_rate_shock: { type: 'number', minimum: 0, maximum: 10 },
              liquidity_shock: { type: 'number', minimum: 0, maximum: 1 }
            }
          },
          default: [
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
          ]
        },
        monte_carlo_simulations: { type: 'integer', minimum: 0, maximum: 10000, default: 0 },
        tail_risk_threshold: { type: 'number', minimum: 0, maximum: 0.5, default: 0.05 },
        enable_sensitivity_analysis: { type: 'boolean', default: true },
        sensitivity_parameters: {
          type: 'array',
          items: { type: 'string' },
          default: ['interest_rate', 'property_value_growth', 'default_rate', 'ltv_ratio']
        }
      },
      default: {
        var_confidence_level: 0.95,
        risk_free_rate: 0.03,
        benchmark_return: 0.07,
        min_acceptable_return: 0.04,
        stress_test_scenarios: [
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
        monte_carlo_simulations: 0,
        tail_risk_threshold: 0.05,
        enable_sensitivity_analysis: true,
        sensitivity_parameters: ['interest_rate', 'property_value_growth', 'default_rate', 'ltv_ratio']
      }
    },
    variation_factors: {
      type: 'object',
      description: 'Factors controlling the amount of random variation for different aspects',
      properties: {
        price_path: { type: 'number', minimum: 0, maximum: 1, default: 0.05 },
        default_events: { type: 'number', minimum: 0, maximum: 1, default: 0.1 },
        prepayment_events: { type: 'number', minimum: 0, maximum: 1, default: 0.2 },
        appreciation_rates: { type: 'number', minimum: 0, maximum: 1, default: 0.05 }
      },
      default: {
        price_path: 0.05,
        default_events: 0.1,
        prepayment_events: 0.2,
        appreciation_rates: 0.05
      }
    },
    correlation_matrix: {
      type: 'object',
      description: 'Matrix of correlations between different random variables',
      properties: {
        price_path_default_events: { type: 'number', minimum: -1, maximum: 1, default: -0.7 },
        price_path_prepayment_events: { type: 'number', minimum: -1, maximum: 1, default: 0.3 },
        default_events_prepayment_events: { type: 'number', minimum: -1, maximum: 1, default: -0.2 }
      },
      default: {
        price_path_default_events: -0.7,
        price_path_prepayment_events: 0.3,
        default_events_prepayment_events: -0.2
      }
    },
    deterministic_mode: {
      type: 'boolean',
      description: 'Whether to use deterministic mode for reproducible results',
      default: false
    },
    reinvestment_period: {
      type: 'number',
      description: 'Reinvestment period in years',
      minimum: 0,
      maximum: 20,
      default: 5
    }

  };

  return {
    type: 'object',
    properties: portfolioStrategyProperties,
    required: [
      'zone_allocations',
      'avg_loan_ltv',
      'min_ltv',
      'max_ltv',
      'avg_loan_size',
      'min_loan_size',
      'max_loan_size',
      'ltv_std_dev',
      'loan_size_std_dev',
      'appreciation_rates',
      'default_rates',
      'recovery_rates',
      'leverage_engine',
      'enhanced_leverage',
      'reinvestment_engine',
      'exit_simulator',
      'price_path',
      'enhanced_exit_simulator',
      'risk_metrics',
      'variation_factors',
      'correlation_matrix',
      'deterministic_mode',
      'reinvestment_period'
    ]
  };
}

/**
 * Get portfolio strategy default values
 * @returns Portfolio strategy default values
 */
export function getPortfolioStrategyDefaults() {
  const schema = getPortfolioStrategySchema();
  return extractDefaultValues(schema);
}

/**
 * Get portfolio strategy Zod validation schema
 * @returns Zod validation schema for portfolio strategy
 */
export function getPortfolioStrategyValidationSchema() {
  const schema = getPortfolioStrategySchema();
  return createZodSchema(schema);
}

export default {
  extractDefaultValues,
  createZodSchema,
  getFundBasicsSchema,
  getFundBasicsDefaults,
  getFundBasicsValidationSchema,
  getPortfolioStrategySchema,
  getPortfolioStrategyDefaults,
  getPortfolioStrategyValidationSchema
};
