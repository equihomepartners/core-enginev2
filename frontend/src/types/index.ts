// Re-export types from the SDK for consistency
export {
  SimulationRequest,
  SimulationResult,
  SimulationResponse,
} from '../api/sdk/models';

// Additional types for frontend-specific use
export interface Simulation {
  id: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  duration_seconds?: number;
  config: object; // This will be the actual config from the schema
  results?: SimulationResult;
  error?: {
    message: string;
    module?: string;
    details?: any;
  };
}

// WebSocket message types (based on AsyncAPI spec)
export interface WebSocketMessage {
  type: 'progress' | 'module_started' | 'module_completed' | 'intermediate_result' | 'result' | 'error' | 'guardrail_violation';
  data: any;
  timestamp: string;
}

export interface ProgressMessage {
  type: 'progress';
  data: {
    progress: number;
    module: string;
    message: string;
  };
}

export interface ModuleStartedMessage {
  type: 'module_started';
  data: {
    module: string;
    timestamp: string;
  };
}

export interface ModuleCompletedMessage {
  type: 'module_completed';
  data: {
    module: string;
    execution_time: number;
    timestamp: string;
  };
}

export interface IntermediateResultMessage {
  type: 'intermediate_result';
  data: {
    module: string;
    data: any;
    timestamp: string;
  };
}

export interface ResultMessage {
  type: 'result';
  data: {
    result: SimulationResult;
    timestamp: string;
  };
}

export interface ErrorMessage {
  type: 'error';
  data: {
    error: string;
    module?: string;
    details?: any;
    timestamp: string;
  };
}

export interface GuardrailViolationMessage {
  type: 'guardrail_violation';
  data: {
    violation: {
      severity: 'info' | 'warning' | 'error';
      message: string;
      module: string;
      details?: any;
    };
    timestamp: string;
  };
}
