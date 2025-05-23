/**
 * TypeScript interfaces for EQU IHOME SIM ENGINE WebSocket API
 * Generated from AsyncAPI specification
 */

// Command payloads (client to server)

/**
 * Command to subscribe to updates for a specific simulation
 */
export interface SubscribeCommandPayload {
  action: 'subscribe';
  simulation_id: string;
}

/**
 * Command to unsubscribe from updates for a specific simulation
 */
export interface UnsubscribeCommandPayload {
  action: 'unsubscribe';
  simulation_id: string;
}

/**
 * Command to cancel a running simulation
 */
export interface CancelCommandPayload {
  action: 'cancel';
  simulation_id: string;
}

// Update payloads (server to client)

/**
 * Base interface for all update messages
 */
export interface BaseUpdatePayload {
  type: string;
  simulation_id: string;
  timestamp?: string;
}

/**
 * Update about the progress of a simulation
 */
export interface ProgressUpdatePayload extends BaseUpdatePayload {
  type: 'progress';
  progress: number;
  module?: string;
  message?: string;
}

/**
 * Notification that a simulation module has started execution
 */
export interface ModuleStartedPayload extends BaseUpdatePayload {
  type: 'module_started';
  module: string;
}

/**
 * Notification that a simulation module has completed execution
 */
export interface ModuleCompletedPayload extends BaseUpdatePayload {
  type: 'module_completed';
  module: string;
  execution_time?: number;
}

/**
 * Intermediate result from a simulation module
 */
export interface IntermediateResultPayload extends BaseUpdatePayload {
  type: 'intermediate_result';
  module: string;
  data: Record<string, any>;
}

/**
 * Final result of a completed simulation
 */
export interface FinalResultPayload extends BaseUpdatePayload {
  type: 'result';
  result: Record<string, any>;
  execution_time?: number;
}

/**
 * Error that occurred during simulation execution
 */
export interface ErrorUpdatePayload extends BaseUpdatePayload {
  type: 'error';
  error: string;
  module?: string;
}

/**
 * Guardrail violation details
 */
export interface GuardrailViolation {
  rule: string;
  severity: 'info' | 'warning' | 'error';
  message: string;
  details?: Record<string, any>;
}

/**
 * Notification that a guardrail has been violated
 */
export interface GuardrailViolationPayload extends BaseUpdatePayload {
  type: 'guardrail_violation';
  violation: GuardrailViolation;
}

/**
 * Union type of all possible update messages from server to client
 */
export type WebSocketUpdatePayload =
  | ProgressUpdatePayload
  | ModuleStartedPayload
  | ModuleCompletedPayload
  | IntermediateResultPayload
  | FinalResultPayload
  | ErrorUpdatePayload
  | GuardrailViolationPayload;

/**
 * Union type of all possible command messages from client to server
 */
export type WebSocketCommandPayload =
  | SubscribeCommandPayload
  | UnsubscribeCommandPayload
  | CancelCommandPayload;
