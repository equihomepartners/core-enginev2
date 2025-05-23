import { z } from 'zod';

/**
 * Zod schema for fund basics validation
 */
export const fundBasicsSchema = z.object({
  fund_name: z.string().optional(),
  fund_size: z.number()
    .min(1000000, 'Fund size must be at least $1,000,000')
    .max(1000000000, 'Fund size must be at most $1,000,000,000'),
  fund_term: z.number().int()
    .min(1, 'Fund term must be at least 1 year')
    .max(30, 'Fund term must be at most 30 years'),
  vintage_year: z.number().int()
    .min(1900, 'Vintage year must be at least 1900')
    .max(2100, 'Vintage year must be at most 2100'),
  management_fee_rate: z.number()
    .min(0, 'Management fee rate must be at least 0%')
    .max(5, 'Management fee rate must be at most 5%'),
  carried_interest_rate: z.number()
    .min(0, 'Carried interest rate must be at least 0%')
    .max(30, 'Carried interest rate must be at most 30%'),
  hurdle_rate: z.number()
    .min(0, 'Hurdle rate must be at least 0%')
    .max(20, 'Hurdle rate must be at most 20%'),
});

/**
 * Zod schema for loan parameters validation
 */
export const loanParametersSchema = z.object({
  avg_loan_size: z.number()
    .min(10000, 'Average loan size must be at least $10,000')
    .max(10000000, 'Average loan size must be at most $10,000,000'),
  min_loan_size: z.number()
    .min(1000, 'Minimum loan size must be at least $1,000')
    .max(1000000, 'Minimum loan size must be at most $1,000,000'),
  max_loan_size: z.number()
    .min(100000, 'Maximum loan size must be at least $100,000')
    .max(100000000, 'Maximum loan size must be at most $100,000,000'),
  avg_loan_ltv: z.number()
    .min(0.1, 'Average LTV must be at least 10%')
    .max(0.9, 'Average LTV must be at most 90%'),
  min_ltv: z.number()
    .min(0.05, 'Minimum LTV must be at least 5%')
    .max(0.5, 'Minimum LTV must be at most 50%'),
  max_ltv: z.number()
    .min(0.5, 'Maximum LTV must be at least 50%')
    .max(0.95, 'Maximum LTV must be at most 95%'),
});

/**
 * Zod schema for zone allocations validation
 */
export const zoneAllocationsSchema = z.object({
  zone_green_allocation: z.number()
    .min(0, 'Green zone allocation must be at least 0%')
    .max(1, 'Green zone allocation must be at most 100%'),
  zone_orange_allocation: z.number()
    .min(0, 'Orange zone allocation must be at least 0%')
    .max(1, 'Orange zone allocation must be at most 100%'),
  zone_red_allocation: z.number()
    .min(0, 'Red zone allocation must be at least 0%')
    .max(1, 'Red zone allocation must be at most 100%'),
}).refine(
  (data) => {
    const sum = data.zone_green_allocation + data.zone_orange_allocation + data.zone_red_allocation;
    return Math.abs(sum - 1) < 0.001; // Allow for floating point imprecision
  },
  {
    message: 'Zone allocations must sum to 100%',
    path: ['zone_allocations'],
  }
);

/**
 * Zod schema for risk parameters validation
 */
export const riskParametersSchema = z.object({
  zone_green_volatility: z.number()
    .min(0, 'Green zone volatility must be at least 0%')
    .max(0.5, 'Green zone volatility must be at most 50%')
    .optional(),
  zone_orange_volatility: z.number()
    .min(0, 'Orange zone volatility must be at least 0%')
    .max(0.75, 'Orange zone volatility must be at most 75%')
    .optional(),
  zone_red_volatility: z.number()
    .min(0, 'Red zone volatility must be at least 0%')
    .max(1, 'Red zone volatility must be at most 100%')
    .optional(),
  zone_green_default_probability: z.number()
    .min(0, 'Green zone default probability must be at least 0%')
    .max(0.1, 'Green zone default probability must be at most 10%')
    .optional(),
  zone_orange_default_probability: z.number()
    .min(0, 'Orange zone default probability must be at least 0%')
    .max(0.2, 'Orange zone default probability must be at most 20%')
    .optional(),
  zone_red_default_probability: z.number()
    .min(0, 'Red zone default probability must be at least 0%')
    .max(0.3, 'Red zone default probability must be at most 30%')
    .optional(),
});

/**
 * Combined schema for simulation configuration validation
 */
export const simulationConfigSchema = z.object({
  ...fundBasicsSchema.shape,
  ...loanParametersSchema.shape,
  ...zoneAllocationsSchema.shape,
  ...riskParametersSchema.shape,
});

/**
 * Type for simulation configuration validation
 */
export type SimulationConfigValidation = z.infer<typeof simulationConfigSchema>;

/**
 * Validate simulation configuration
 * @param config Configuration to validate
 * @returns Validation result
 */
export const validateSimulationConfig = (config: any) => {
  try {
    return {
      success: true,
      data: simulationConfigSchema.parse(config),
      error: null,
    };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        success: false,
        data: null,
        error: error.format(),
      };
    }
    return {
      success: false,
      data: null,
      error: 'Unknown validation error',
    };
  }
};
