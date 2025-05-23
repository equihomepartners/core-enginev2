import React, { useState, useEffect, useRef } from 'react';
import {
  ProgressBar,
  Intent,
  Button,
  Card,
  Icon,
  Tag,
  Callout,
  Collapse
} from '@blueprintjs/core';
import { useNavigate } from 'react-router-dom';
import { WebSocketClient } from '../../api/sdk/websocket/client';
import { toast } from '../../api/toast';

interface SimulationProgressProps {
  simulationId: string;
}

interface ProgressUpdate {
  progress: number;
  module: string;
  message: string;
  timestamp: string;
}

interface ModuleStatus {
  name: string;
  status: 'pending' | 'running' | 'completed' | 'error';
  progress: number;
  startTime?: string;
  endTime?: string;
  executionTime?: number;
  message?: string;
}

interface GuardrailViolation {
  severity: 'INFO' | 'WARN' | 'FAIL';
  module: string;
  message: string;
  timestamp: string;
}

const SimulationProgress: React.FC<SimulationProgressProps> = ({ simulationId }) => {
  const navigate = useNavigate();
  const wsClientRef = useRef<WebSocketClient | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [overallProgress, setOverallProgress] = useState(0);
  const [currentModule, setCurrentModule] = useState<string>('');
  const [currentMessage, setCurrentMessage] = useState<string>('Initializing simulation...');
  const [isCompleted, setIsCompleted] = useState(false);
  const [isCancelled, setIsCancelled] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);

  // Module tracking
  const [modules, setModules] = useState<ModuleStatus[]>([
    { name: 'Loan Generation', status: 'pending', progress: 0 },
    { name: 'Price Path Simulation', status: 'pending', progress: 0 },
    { name: 'Exit Event Modeling', status: 'pending', progress: 0 },
    { name: 'Cashflow Calculation', status: 'pending', progress: 0 },
    { name: 'Risk Analysis', status: 'pending', progress: 0 },
    { name: 'Report Generation', status: 'pending', progress: 0 },
  ]);

  // Progress history and logs
  const [progressHistory, setProgressHistory] = useState<ProgressUpdate[]>([]);
  const [guardrailViolations, setGuardrailViolations] = useState<GuardrailViolation[]>([]);
  const [intermediateResults, setIntermediateResults] = useState<any[]>([]);

  // WebSocket connection management
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        // Create WebSocket client
        const wsClient = new WebSocketClient({
          baseUrl: import.meta.env.VITE_WS_URL || 'ws://localhost:8000',
          apiKey: import.meta.env.VITE_API_KEY || localStorage.getItem('api_key') || undefined,
          autoReconnect: true,
          maxReconnectAttempts: 5,
          reconnectDelay: 3000
        });

        wsClientRef.current = wsClient;

        // Set up event listeners
        wsClient.on('open', () => {
          setIsConnected(true);
          console.log('WebSocket connected');
          // Subscribe to simulation updates
          wsClient.subscribe(simulationId);
        });

        wsClient.on('close', () => {
          setIsConnected(false);
          console.log('WebSocket disconnected');
        });

        wsClient.on('error', (error) => {
          console.error('WebSocket error:', error);
          setError('Connection error occurred');
        });

        // Handle progress updates
        wsClient.on('progress', (data) => {
          setOverallProgress(data.progress);
          setCurrentMessage(data.message);

          setProgressHistory(prev => [...prev, {
            progress: data.progress,
            module: data.module || currentModule,
            message: data.message,
            timestamp: new Date().toISOString()
          }]);
        });

        // Handle module events
        wsClient.on('module_started', (data) => {
          setCurrentModule(data.module);
          setModules(prev => prev.map(module =>
            module.name === data.module
              ? { ...module, status: 'running', startTime: new Date().toISOString() }
              : module
          ));
        });

        wsClient.on('module_completed', (data) => {
          setModules(prev => prev.map(module =>
            module.name === data.module
              ? {
                  ...module,
                  status: 'completed',
                  progress: 100,
                  endTime: new Date().toISOString(),
                  executionTime: data.execution_time
                }
              : module
          ));
        });

        // Handle guardrail violations
        wsClient.on('guardrail_violation', (data) => {
          setGuardrailViolations(prev => [...prev, {
            severity: data.severity,
            module: data.module,
            message: data.message,
            timestamp: new Date().toISOString()
          }]);
        });

        // Handle intermediate results
        wsClient.on('intermediate_result', (data) => {
          setIntermediateResults(prev => [...prev, data.result]);
        });

        // Handle final result
        wsClient.on('result', (data) => {
          setIsCompleted(true);
          setOverallProgress(100);
          setCurrentMessage('Simulation completed successfully');
        });

        // Handle errors
        wsClient.on('error_update', (data) => {
          setError(data.message);
          setCurrentMessage(`Error: ${data.message}`);
        });

        // Connect to WebSocket with simulation ID
        wsClient.connect(simulationId);

        // Fallback to simulation if WebSocket fails
        setTimeout(() => {
          if (!isConnected) {
            console.warn('WebSocket connection failed, falling back to simulation');
            simulateProgressUpdates();
          }
        }, 5000);

      } catch (err) {
        console.error('Failed to connect to WebSocket:', err);
        setError('Failed to connect to simulation service');
        // Fallback to simulation
        simulateProgressUpdates();
      }
    };

    connectWebSocket();

    return () => {
      if (wsClientRef.current) {
        try {
          // Only unsubscribe if WebSocket is connected
          if (wsClientRef.current.socket && wsClientRef.current.socket.readyState === WebSocket.OPEN) {
            wsClientRef.current.unsubscribe(simulationId);
          }
          wsClientRef.current.disconnect();
        } catch (error) {
          console.warn('Error during WebSocket cleanup:', error);
        }
      }
    };
  }, [simulationId]);

  // Simulate progress updates for demonstration
  const simulateProgressUpdates = () => {
    const moduleNames = [
      'Loan Generation',
      'Price Path Simulation',
      'Exit Event Modeling',
      'Cashflow Calculation',
      'Risk Analysis',
      'Report Generation'
    ];

    let currentModuleIndex = 0;
    let moduleProgress = 0;

    const updateProgress = () => {
      if (currentModuleIndex >= moduleNames.length) {
        setIsCompleted(true);
        setCurrentMessage('Simulation completed successfully');
        setOverallProgress(100);
        return;
      }

      const moduleName = moduleNames[currentModuleIndex];

      // Update current module status
      setModules(prev => prev.map((module, index) => {
        if (index === currentModuleIndex) {
          return {
            ...module,
            status: 'running' as const,
            progress: moduleProgress,
            startTime: module.startTime || new Date().toISOString(),
            message: `Processing ${moduleName}...`
          };
        } else if (index < currentModuleIndex) {
          return {
            ...module,
            status: 'completed' as const,
            progress: 100,
            endTime: module.endTime || new Date().toISOString(),
            executionTime: 5 + Math.random() * 10 // Random execution time
          };
        }
        return module;
      }));

      setCurrentModule(moduleName);
      setCurrentMessage(`Processing ${moduleName}... ${moduleProgress}%`);

      const overallProg = ((currentModuleIndex * 100) + moduleProgress) / moduleNames.length;
      setOverallProgress(overallProg);

      // Add to progress history
      setProgressHistory(prev => [...prev, {
        progress: overallProg,
        module: moduleName,
        message: `Processing ${moduleName}... ${moduleProgress}%`,
        timestamp: new Date().toISOString()
      }]);

      // Simulate some guardrail violations
      if (Math.random() < 0.1 && guardrailViolations.length < 3) {
        const violations = [
          { severity: 'WARN' as const, module: moduleName, message: 'LTV concentration above 75% in green zone', timestamp: new Date().toISOString() },
          { severity: 'INFO' as const, module: moduleName, message: 'Portfolio diversification within acceptable range', timestamp: new Date().toISOString() },
          { severity: 'WARN' as const, module: moduleName, message: 'Interest rate sensitivity above threshold', timestamp: new Date().toISOString() },
        ];
        setGuardrailViolations(prev => [...prev, violations[Math.floor(Math.random() * violations.length)]]);
      }

      moduleProgress += 10 + Math.random() * 20;

      if (moduleProgress >= 100) {
        moduleProgress = 0;
        currentModuleIndex++;
      }

      if (!isCompleted && !isCancelled) {
        setTimeout(updateProgress, 500 + Math.random() * 1000);
      }
    };

    setTimeout(updateProgress, 1000);
  };

  const handleCancel = async () => {
    if (window.confirm('Are you sure you want to cancel the simulation?')) {
      setIsCancelled(true);
      setCurrentMessage('Cancelling simulation...');

      // Send cancellation request via WebSocket
      if (wsClientRef.current) {
        try {
          wsClientRef.current.cancelSimulation(simulationId);
          await toast.warning('Cancellation request sent');
        } catch (error) {
          console.error('Failed to cancel simulation:', error);
          await toast.error('Failed to cancel simulation');
        }
      } else {
        // Fallback for when WebSocket is not available
        setTimeout(async () => {
          setCurrentMessage('Simulation cancelled');
          await toast.warning('Simulation cancelled');
        }, 1000);
      }
    }
  };

  const handleViewResults = () => {
    navigate(`/runs/${simulationId}/results`);
  };

  const getModuleIcon = (status: ModuleStatus['status']) => {
    switch (status) {
      case 'completed': return 'tick-circle';
      case 'running': return 'refresh';
      case 'error': return 'error';
      default: return 'circle';
    }
  };

  const getModuleIntent = (status: ModuleStatus['status']) => {
    switch (status) {
      case 'completed': return Intent.SUCCESS;
      case 'running': return Intent.PRIMARY;
      case 'error': return Intent.DANGER;
      default: return Intent.NONE;
    }
  };

  const getGuardrailIntent = (severity: GuardrailViolation['severity']) => {
    switch (severity) {
      case 'FAIL': return Intent.DANGER;
      case 'WARN': return Intent.WARNING;
      default: return Intent.PRIMARY;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-display font-semibold text-neutral-900">
            Simulation Progress
          </h1>
          <p className="text-neutral-500 mt-1">
            Simulation ID: {simulationId}
          </p>
        </div>
        <div className="flex space-x-2">
          <Button
            icon="eye-open"
            text="Show Details"
            minimal
            active={showDetails}
            onClick={() => setShowDetails(!showDetails)}
          />
          {!isCompleted && !isCancelled && (
            <Button
              icon="cross"
              text="Cancel"
              intent={Intent.DANGER}
              onClick={handleCancel}
            />
          )}
        </div>
      </div>

      {/* Connection Status */}
      <Callout intent={isConnected ? Intent.SUCCESS : Intent.WARNING}>
        <div className="flex items-center space-x-2">
          <Icon icon={isConnected ? 'satellite' : 'offline'} />
          <span>
            {isConnected ? 'Connected to simulation service' : 'Connecting to simulation service...'}
          </span>
        </div>
      </Callout>

      {/* Overall Progress */}
      <Card>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Overall Progress</h3>
            <Tag intent={isCompleted ? Intent.SUCCESS : Intent.PRIMARY} large>
              {overallProgress.toFixed(1)}%
            </Tag>
          </div>

          <ProgressBar
            value={overallProgress / 100}
            intent={isCompleted ? Intent.SUCCESS : Intent.PRIMARY}
            stripes={!isCompleted}
            animate={!isCompleted}
          />

          <div className="text-sm text-gray-600">
            {currentMessage}
          </div>

          {isCompleted && (
            <div className="flex justify-center">
              <Button
                intent={Intent.SUCCESS}
                large
                icon="chart"
                text="View Results"
                onClick={handleViewResults}
              />
            </div>
          )}
        </div>
      </Card>

      {/* Module Progress */}
      <Card title="Module Progress" icon="list">
        <div className="space-y-3">
          {modules.map((module, index) => (
            <div key={index} className="flex items-center space-x-3 p-2 rounded border">
              <Icon
                icon={getModuleIcon(module.status)}
                intent={getModuleIntent(module.status)}
                className={module.status === 'running' ? 'animate-spin' : ''}
              />
              <div className="flex-1">
                <div className="flex justify-between items-center">
                  <span className="font-medium">{module.name}</span>
                  <span className="text-sm text-gray-500">
                    {module.status === 'completed' && module.executionTime &&
                      `${module.executionTime.toFixed(1)}s`
                    }
                  </span>
                </div>
                {module.status === 'running' && (
                  <ProgressBar
                    value={module.progress / 100}
                    intent={Intent.PRIMARY}
                    stripes
                    animate
                    className="mt-1"
                  />
                )}
                {module.message && (
                  <div className="text-xs text-gray-500 mt-1">{module.message}</div>
                )}
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Detailed Information */}
      <Collapse isOpen={showDetails}>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Guardrail Violations */}
          <Card title="Guardrail Violations" icon="shield">
            {guardrailViolations.length > 0 ? (
              <div className="space-y-2">
                {guardrailViolations.map((violation, index) => (
                  <Callout key={index} intent={getGuardrailIntent(violation.severity)}>
                    <div className="text-sm">
                      <div className="font-medium">{violation.module}</div>
                      <div>{violation.message}</div>
                      <div className="text-xs opacity-75 mt-1">
                        {new Date(violation.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  </Callout>
                ))}
              </div>
            ) : (
              <div className="text-gray-500 text-sm">No violations detected</div>
            )}
          </Card>

          {/* Progress History */}
          <Card title="Progress Log" icon="history">
            <div className="max-h-64 overflow-y-auto space-y-1">
              {progressHistory.slice(-10).reverse().map((update, index) => (
                <div key={index} className="text-sm p-2 bg-gray-50 rounded">
                  <div className="flex justify-between">
                    <span className="font-medium">{update.module}</span>
                    <span className="text-gray-500">
                      {new Date(update.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <div className="text-gray-600">{update.message}</div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </Collapse>
    </div>
  );
};

export default SimulationProgress;
