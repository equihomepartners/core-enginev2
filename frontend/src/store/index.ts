import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { extractDefaultValues } from '../utils/schemaUtils';

// Define a simplified schema for development
// In production, this would be imported from the actual schema file
const simulationConfigSchema = {
  "properties": {
    "fund_name": {
      "type": "string",
      "default": "Equihome Fund I"
    },
    "fund_size": {
      "type": "number",
      "default": 100000000
    },
    "fund_term": {
      "type": "integer",
      "default": 10
    },
    "vintage_year": {
      "type": "integer",
      "default": 2023
    },
    "management_fee_rate": {
      "type": "number",
      "default": 0.02
    },
    "carried_interest_rate": {
      "type": "number",
      "default": 0.20
    },
    "hurdle_rate": {
      "type": "number",
      "default": 0.08
    },
    "fee_engine": {
      "type": "object",
      "properties": {
        "origination_fee_rate": {
          "type": "number",
          "default": 0.01
        },
        "annual_fund_expenses": {
          "type": "number",
          "default": 0.005
        },
        "fixed_annual_expenses": {
          "type": "number",
          "default": 100000
        },
        "setup_costs": {
          "type": "number",
          "default": 250000
        },
        "expense_growth_rate": {
          "type": "number",
          "default": 0.02
        },
        "acquisition_fee_rate": {
          "type": "number",
          "default": 0
        },
        "disposition_fee_rate": {
          "type": "number",
          "default": 0
        },
        "fee_allocation": {
          "type": "object",
          "properties": {
            "origination_fee_gp_share": {
              "type": "number",
              "default": 1.0
            },
            "acquisition_fee_gp_share": {
              "type": "number",
              "default": 1.0
            },
            "disposition_fee_gp_share": {
              "type": "number",
              "default": 1.0
            }
          },
          "default": {
            "origination_fee_gp_share": 1.0,
            "acquisition_fee_gp_share": 1.0,
            "disposition_fee_gp_share": 1.0
          }
        }
      },
      "default": {
        "origination_fee_rate": 0.01,
        "annual_fund_expenses": 0.005,
        "fixed_annual_expenses": 100000,
        "setup_costs": 250000,
        "expense_growth_rate": 0.02,
        "acquisition_fee_rate": 0,
        "disposition_fee_rate": 0,
        "fee_allocation": {
          "origination_fee_gp_share": 1.0,
          "acquisition_fee_gp_share": 1.0,
          "disposition_fee_gp_share": 1.0
        }
      }
    }
  }
};

// Define the simulation configuration type
export interface SimulationConfig {
  [key: string]: any;
  fund_name?: string;
  fund_size?: number;
  fund_term?: number;
  vintage_year?: number;
  management_fee_rate?: number;
  management_fee_basis?: string;
  carried_interest_rate?: number;
  hurdle_rate?: number;
  waterfall_structure?: string;
  gp_commitment_percentage?: number;
  catch_up_rate?: number;
  reinvestment_period?: number;
  fee_engine?: {
    origination_fee_rate?: number;
    annual_fund_expenses?: number;
    fixed_annual_expenses?: number;
    setup_costs?: number;
    expense_growth_rate?: number;
    acquisition_fee_rate?: number;
    disposition_fee_rate?: number;
  };
  zone_allocations?: {
    green?: number;
    orange?: number;
    red?: number;
  };
  appreciation_rates?: {
    green?: number;
    orange?: number;
    red?: number;
  };
  price_path?: {
    model_type?: string;
    volatility?: {
      green?: number;
      orange?: number;
      red?: number;
    };
  };
  default_rates?: {
    green?: number;
    orange?: number;
    red?: number;
  };
  recovery_rates?: {
    green?: number;
    orange?: number;
    red?: number;
  };
  monte_carlo_enabled?: boolean;
  num_simulations?: number;
  deterministic_mode?: boolean;
}

// Define the simulation result type
export interface SimulationResult {
  id: string;
  status: 'running' | 'completed' | 'failed';
  progress: number;
  config: SimulationConfig;
  results?: any;
  error?: string;
  startTime: string;
  endTime?: string;
}

// Define the simulation store state
interface SimulationState {
  // Configuration
  config: SimulationConfig;
  setConfig: (config: Partial<SimulationConfig>) => void;
  resetConfig: () => void;

  // Current simulation
  currentSimulation: SimulationResult | null;
  setCurrentSimulation: (simulation: SimulationResult | null) => void;
  updateCurrentSimulation: (updates: Partial<SimulationResult>) => void;

  // Past simulations
  pastSimulations: SimulationResult[];
  addPastSimulation: (simulation: SimulationResult) => void;
  removePastSimulation: (id: string) => void;
  clearPastSimulations: () => void;

  // Wizard state
  currentStep: number;
  setCurrentStep: (step: number) => void;

  // UI state
  isLoading: boolean;
  setIsLoading: (isLoading: boolean) => void;
  error: string | null;
  setError: (error: string | null) => void;
}

// Get default values from schema
const defaultConfig = extractDefaultValues(simulationConfigSchema);

// Create the store
export const useSimulationStore = create<SimulationState>()(
  devtools(
    (set) => ({
      // Configuration
      config: { ...defaultConfig, fund_name: 'Equihome Fund I' },
      setConfig: (newConfig) => set((state) => ({
        config: { ...state.config, ...newConfig }
      })),
      resetConfig: () => set({
        config: { ...defaultConfig, fund_name: 'Equihome Fund I' }
      }),

      // Current simulation
      currentSimulation: null,
      setCurrentSimulation: (simulation) => set({ currentSimulation: simulation }),
      updateCurrentSimulation: (updates) => set((state) => ({
        currentSimulation: state.currentSimulation
          ? { ...state.currentSimulation, ...updates }
          : null
      })),

      // Past simulations
      pastSimulations: [],
      addPastSimulation: (simulation) => set((state) => ({
        pastSimulations: [...state.pastSimulations, simulation]
      })),
      removePastSimulation: (id) => set((state) => ({
        pastSimulations: state.pastSimulations.filter((s) => s.id !== id)
      })),
      clearPastSimulations: () => set({ pastSimulations: [] }),

      // Wizard state
      currentStep: 1,
      setCurrentStep: (step) => set({ currentStep: step }),

      // UI state
      isLoading: false,
      setIsLoading: (isLoading) => set({ isLoading }),
      error: null,
      setError: (error) => set({ error }),
    })
  )
);

export default useSimulationStore;
