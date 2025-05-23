import {
  WebSocketUpdatePayload,
  WebSocketCommandPayload,
  SubscribeCommandPayload,
  UnsubscribeCommandPayload,
  CancelCommandPayload,
  ProgressUpdatePayload,
  ModuleStartedPayload,
  ModuleCompletedPayload,
  IntermediateResultPayload,
  FinalResultPayload,
  ErrorUpdatePayload,
  GuardrailViolationPayload
} from './types';

/**
 * Event types for the WebSocket client
 */
export type WebSocketEventType =
  | 'open'
  | 'close'
  | 'error'
  | 'progress'
  | 'module_started'
  | 'module_completed'
  | 'intermediate_result'
  | 'result'
  | 'error_update'
  | 'guardrail_violation'
  | 'message';

/**
 * Options for the WebSocket client
 */
export interface WebSocketClientOptions {
  /**
   * Base URL of the WebSocket server
   */
  baseUrl: string;

  /**
   * Whether to automatically reconnect on connection loss
   */
  autoReconnect?: boolean;

  /**
   * Maximum number of reconnection attempts
   */
  maxReconnectAttempts?: number;

  /**
   * Delay between reconnection attempts in milliseconds
   */
  reconnectDelay?: number;

  /**
   * API key for authentication
   */
  apiKey?: string;
}

/**
 * Client for the EQU IHOME SIM ENGINE WebSocket API
 */
export class WebSocketClient {
  private _socket: WebSocket | null = null;
  private eventListeners: Map<WebSocketEventType, Function[]> = new Map();
  private reconnectAttempts = 0;
  private options: Required<WebSocketClientOptions>;

  /**
   * Create a new WebSocket client
   * @param options Client options
   */
  constructor(options: WebSocketClientOptions) {
    this.options = {
      autoReconnect: true,
      maxReconnectAttempts: 5,
      reconnectDelay: 3000,
      ...options
    };
  }

  /**
   * Connect to the WebSocket server for a specific simulation
   * @param simulationId ID of the simulation to connect to
   */
  public connect(simulationId?: string): void {
    if (this._socket && (this._socket.readyState === WebSocket.OPEN || this._socket.readyState === WebSocket.CONNECTING)) {
      return;
    }

    // Use the simulation ID if provided, otherwise use a default
    const simId = simulationId || 'default';
    const url = new URL(`/ws/simulations/${simId}`, this.options.baseUrl);

    // Add API key as query parameter if provided
    if (this.options.apiKey) {
      url.searchParams.append('api_key', this.options.apiKey);
    }

    this._socket = new WebSocket(url.toString());

    this._socket.onopen = (event) => {
      this.reconnectAttempts = 0;
      this.emit('open', event);
    };

    this._socket.onclose = (event) => {
      this.emit('close', event);

      if (this.options.autoReconnect && this.reconnectAttempts < this.options.maxReconnectAttempts) {
        this.reconnectAttempts++;
        setTimeout(() => this.connect(simulationId), this.options.reconnectDelay);
      }
    };

    this._socket.onerror = (event) => {
      this.emit('error', event);
    };

    this._socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as WebSocketUpdatePayload;
        this.emit('message', data);

        // Emit specific event based on message type
        switch (data.type) {
          case 'progress':
            this.emit('progress', data as ProgressUpdatePayload);
            break;
          case 'module_started':
            this.emit('module_started', data as ModuleStartedPayload);
            break;
          case 'module_completed':
            this.emit('module_completed', data as ModuleCompletedPayload);
            break;
          case 'intermediate_result':
            this.emit('intermediate_result', data as IntermediateResultPayload);
            break;
          case 'result':
            this.emit('result', data as FinalResultPayload);
            break;
          case 'error':
            this.emit('error_update', data as ErrorUpdatePayload);
            break;
          case 'guardrail_violation':
            this.emit('guardrail_violation', data as GuardrailViolationPayload);
            break;
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
  }

  /**
   * Get the current WebSocket instance
   */
  public get socket(): WebSocket | null {
    return this._socket;
  }

  /**
   * Disconnect from the WebSocket server
   */
  public disconnect(): void {
    if (this._socket) {
      this._socket.close();
      this._socket = null;
    }
  }

  /**
   * Subscribe to simulation updates
   * @param simulationId ID of the simulation to subscribe to
   */
  public subscribe(simulationId: string): void {
    this.sendCommand({
      action: 'subscribe',
      simulation_id: simulationId
    });
  }

  /**
   * Unsubscribe from simulation updates
   * @param simulationId ID of the simulation to unsubscribe from
   */
  public unsubscribe(simulationId: string): void {
    this.sendCommand({
      action: 'unsubscribe',
      simulation_id: simulationId
    });
  }

  /**
   * Cancel a running simulation
   * @param simulationId ID of the simulation to cancel
   */
  public cancelSimulation(simulationId: string): void {
    this.sendCommand({
      action: 'cancel',
      simulation_id: simulationId
    });
  }

  /**
   * Send a command to the WebSocket server
   * @param command Command to send
   */
  public sendCommand(command: WebSocketCommandPayload): void {
    if (!this._socket || this._socket.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket is not connected');
    }

    this._socket.send(JSON.stringify(command));
  }

  /**
   * Add an event listener
   * @param event Event type
   * @param listener Event listener
   */
  public on(event: WebSocketEventType, listener: Function): void {
    if (!this.eventListeners.has(event)) {
      this.eventListeners.set(event, []);
    }

    this.eventListeners.get(event)!.push(listener);
  }

  /**
   * Remove an event listener
   * @param event Event type
   * @param listener Event listener to remove
   */
  public off(event: WebSocketEventType, listener: Function): void {
    if (!this.eventListeners.has(event)) {
      return;
    }

    const listeners = this.eventListeners.get(event)!;
    const index = listeners.indexOf(listener);

    if (index !== -1) {
      listeners.splice(index, 1);
    }
  }

  /**
   * Emit an event
   * @param event Event type
   * @param data Event data
   */
  private emit(event: WebSocketEventType, data: any): void {
    if (!this.eventListeners.has(event)) {
      return;
    }

    for (const listener of this.eventListeners.get(event)!) {
      listener(data);
    }
  }
}
