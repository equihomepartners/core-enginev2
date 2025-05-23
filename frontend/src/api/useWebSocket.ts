import { useState, useEffect, useRef, useCallback } from 'react';
import { WebSocketClient, WebSocketEventType } from './sdk/websocket/client';
import { toast } from './toast';
import { useSimulationStore } from '../store';

// WebSocket event handlers type
type WebSocketEventHandlers = {
  [key in WebSocketEventType]?: (data: any) => void;
};

// WebSocket hook options
interface UseWebSocketOptions {
  autoConnect?: boolean;
  autoReconnect?: boolean;
  maxReconnectAttempts?: number;
  reconnectDelay?: number;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: any) => void;
}

/**
 * Hook for WebSocket communication using the SDK's WebSocketClient
 * @param baseUrl WebSocket server URL
 * @param options WebSocket options
 * @returns WebSocket utilities
 */
export const useWebSocket = (
  baseUrl: string,
  options: UseWebSocketOptions = {}
) => {
  const {
    autoConnect = true,
    autoReconnect = true,
    maxReconnectAttempts = 5,
    reconnectDelay = 3000,
    onOpen,
    onClose,
    onError,
  } = options;

  // Store connection state
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  
  // Store subscriptions
  const [subscriptions, setSubscriptions] = useState<string[]>([]);
  
  // Store WebSocket client instance
  const clientRef = useRef<WebSocketClient | null>(null);
  
  // Store event handlers
  const handlersRef = useRef<WebSocketEventHandlers>({});
  
  // Get API key from environment or local storage
  const apiKey = process.env.REACT_APP_API_KEY || localStorage.getItem('api_key');
  
  // Get simulation store for updating state
  const setProgress = useSimulationStore(state => state.setProgress);
  const setCurrentModule = useSimulationStore(state => state.setCurrentModule);
  const setResults = useSimulationStore(state => state.setResults);
  const setError = useSimulationStore(state => state.setError);
  const setRunning = useSimulationStore(state => state.setRunning);
  
  // Initialize WebSocket client
  const initClient = useCallback(() => {
    if (clientRef.current) {
      return clientRef.current;
    }
    
    clientRef.current = new WebSocketClient({
      baseUrl,
      apiKey,
      autoReconnect,
      maxReconnectAttempts,
      reconnectDelay,
    });
    
    // Set up default event handlers
    clientRef.current.on('open', () => {
      setIsConnected(true);
      setIsConnecting(false);
      
      // Resubscribe to all simulations
      subscriptions.forEach(id => {
        clientRef.current?.subscribe(id);
      });
      
      onOpen?.();
    });
    
    clientRef.current.on('close', () => {
      setIsConnected(false);
      onClose?.();
    });
    
    clientRef.current.on('error', (error) => {
      console.error('WebSocket error:', error);
      onError?.(error);
    });
    
    // Set up simulation event handlers
    clientRef.current.on('progress', (data) => {
      setProgress(data.progress);
      if (data.module) {
        setCurrentModule(data.module);
      }
    });
    
    clientRef.current.on('module_started', (data) => {
      setCurrentModule(data.module);
      toast.info(`Started module: ${data.module}`);
    });
    
    clientRef.current.on('module_completed', (data) => {
      toast.success(`Completed module: ${data.module} in ${data.execution_time?.toFixed(2)}s`);
    });
    
    clientRef.current.on('result', (data) => {
      setResults(data.result);
      setRunning(false);
      toast.success('Simulation completed successfully');
    });
    
    clientRef.current.on('error_update', (data) => {
      setError(new Error(data.error));
      setRunning(false);
      toast.error(`Simulation error: ${data.error}`);
    });
    
    clientRef.current.on('guardrail_violation', (data) => {
      const { violation } = data;
      
      if (violation.severity === 'error') {
        toast.error(`Guardrail violation: ${violation.message}`);
      } else if (violation.severity === 'warning') {
        toast.warning(`Guardrail warning: ${violation.message}`);
      } else {
        toast.info(`Guardrail info: ${violation.message}`);
      }
    });
    
    return clientRef.current;
  }, [
    baseUrl, 
    apiKey, 
    autoReconnect, 
    maxReconnectAttempts, 
    reconnectDelay, 
    onOpen, 
    onClose, 
    onError,
    subscriptions,
    setProgress,
    setCurrentModule,
    setResults,
    setError,
    setRunning
  ]);
  
  // Connect to WebSocket server
  const connect = useCallback(() => {
    if (isConnected || isConnecting) {
      return;
    }
    
    setIsConnecting(true);
    const client = initClient();
    client.connect();
  }, [isConnected, isConnecting, initClient]);
  
  // Disconnect from WebSocket server
  const disconnect = useCallback(() => {
    if (!clientRef.current) {
      return;
    }
    
    clientRef.current.disconnect();
    setIsConnected(false);
  }, []);
  
  // Subscribe to a simulation
  const subscribe = useCallback((simulationId: string) => {
    if (!clientRef.current) {
      initClient();
    }
    
    if (!isConnected) {
      connect();
    }
    
    clientRef.current?.subscribe(simulationId);
    
    setSubscriptions(prev => {
      if (!prev.includes(simulationId)) {
        return [...prev, simulationId];
      }
      return prev;
    });
  }, [isConnected, connect, initClient]);
  
  // Unsubscribe from a simulation
  const unsubscribe = useCallback((simulationId: string) => {
    if (!clientRef.current || !isConnected) {
      return;
    }
    
    clientRef.current.unsubscribe(simulationId);
    
    setSubscriptions(prev => prev.filter(id => id !== simulationId));
  }, [isConnected]);
  
  // Add event handler
  const on = useCallback((event: WebSocketEventType, handler: (data: any) => void) => {
    handlersRef.current[event] = handler;
    
    if (clientRef.current) {
      clientRef.current.on(event, handler);
    }
  }, []);
  
  // Remove event handler
  const off = useCallback((event: WebSocketEventType) => {
    if (clientRef.current && handlersRef.current[event]) {
      clientRef.current.off(event, handlersRef.current[event]!);
      delete handlersRef.current[event];
    }
  }, []);
  
  // Connect on mount if autoConnect is true
  useEffect(() => {
    if (autoConnect) {
      connect();
    }
    
    return () => {
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);
  
  return {
    isConnected,
    isConnecting,
    connect,
    disconnect,
    subscribe,
    unsubscribe,
    on,
    off,
  };
};
