import { create } from 'zustand';
import { SimulationConfig, SimulationResult } from './api/sdk/models';

interface SimulationStore {
  // Simulation configuration
  config: SimulationConfig;
  setConfig: (config: Partial<SimulationConfig>) => void;
  resetConfig: () => void;

  // Simulation results
  results: SimulationResult | null;
  setResults: (results: SimulationResult) => void;

  // Wizard state
  currentStep: number;
  setCurrentStep: (step: number) => void;

  // Simulation status
  isRunning: boolean;
  progress: number;
  currentModule: string;
  error: Error | null;

  // Status setters
  setRunning: (isRunning: boolean) => void;
  setProgress: (progress: number) => void;
  setCurrentModule: (module: string) => void;
  setError: (error: Error | null) => void;
}

// Default configuration from schema defaults
const DEFAULT_CONFIG: SimulationConfig = {
  fund_size: 10000000,
  fund_term: 10,
  vintage_year: new Date().getFullYear(),
  management_fee_rate: 2,
  carried_interest_rate: 20,
  hurdle_rate: 8,
  avg_loan_size: 250000,
  min_loan_size: 100000,
  max_loan_size: 500000,
  avg_loan_ltv: 0.5,
  min_ltv: 0.3,
  max_ltv: 0.7,
  zone_allocations: {
    green: 0.6,
    orange: 0.3,
    red: 0.1,
  },
};

export const useSimulationStore = create<SimulationStore>((set) => ({
  // Simulation configuration
  config: DEFAULT_CONFIG,
  setConfig: (config) => set((state) => ({
    config: { ...state.config, ...config }
  })),
  resetConfig: () => set({ config: DEFAULT_CONFIG }),

  // Simulation results
  results: null,
  setResults: (results) => set({ results }),

  // Wizard state
  currentStep: 1,
  setCurrentStep: (currentStep) => set({ currentStep }),

  // Simulation status
  isRunning: false,
  progress: 0,
  currentModule: '',
  error: null,

  // Status setters
  setRunning: (isRunning) => set({ isRunning }),
  setProgress: (progress) => set({ progress }),
  setCurrentModule: (currentModule) => set({ currentModule }),
  setError: (error) => set({ error }),
}));
