# EQU IHOME SIM ENGINE WebSocket API

This document describes the WebSocket API for real-time communication with the EQU IHOME SIM ENGINE.

## Table of Contents

- [Overview](#overview)
- [Connection](#connection)
- [Message Types](#message-types)
  - [Commands (Client to Server)](#commands-client-to-server)
  - [Updates (Server to Client)](#updates-server-to-client)
- [TypeScript SDK Integration](#typescript-sdk-integration)
- [Examples](#examples)
- [Error Handling](#error-handling)

## Overview

The WebSocket API allows clients to:
- Subscribe to real-time updates about simulations
- Receive progress updates during simulation execution
- Get notified when simulation modules start and complete
- Receive intermediate results during simulation
- Get final simulation results
- Be notified of errors and guardrail violations
- Cancel running simulations

## Connection

Connect to the WebSocket server at:

```
ws://localhost:8000/ws
```

Authentication can be provided via an API key as a query parameter:

```
ws://localhost:8000/ws?api_key=YOUR_API_KEY
```

## Message Types

### Commands (Client to Server)

Commands are messages sent from the client to the server to perform actions.

#### Subscribe to Simulation Updates

Subscribe to updates for a specific simulation:

```json
{
  "action": "subscribe",
  "simulation_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### Unsubscribe from Simulation Updates

Unsubscribe from updates for a specific simulation:

```json
{
  "action": "unsubscribe",
  "simulation_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### Cancel a Simulation

Cancel a running simulation:

```json
{
  "action": "cancel",
  "simulation_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### Updates (Server to Client)

Updates are messages sent from the server to the client to provide information.

#### Progress Update

Update about the progress of a simulation:

```json
{
  "type": "progress",
  "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
  "progress": 45.5,
  "module": "loan_generator",
  "message": "Generating loans...",
  "timestamp": "2023-05-21T15:30:45Z"
}
```

#### Module Started

Notification that a simulation module has started execution:

```json
{
  "type": "module_started",
  "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
  "module": "price_path_simulator",
  "timestamp": "2023-05-21T15:30:45Z"
}
```

#### Module Completed

Notification that a simulation module has completed execution:

```json
{
  "type": "module_completed",
  "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
  "module": "price_path_simulator",
  "execution_time": 1.25,
  "timestamp": "2023-05-21T15:30:46Z"
}
```

#### Intermediate Result

Intermediate result from a simulation module:

```json
{
  "type": "intermediate_result",
  "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
  "module": "waterfall_engine",
  "data": {
    "tranches": [
      {
        "name": "Senior Debt",
        "return": 0.05
      },
      {
        "name": "Equity",
        "return": 0.12
      }
    ]
  },
  "timestamp": "2023-05-21T15:30:47Z"
}
```

#### Final Result

Final result of a completed simulation:

```json
{
  "type": "result",
  "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
  "result": {
    "metrics": {
      "irr": 0.15,
      "equity_multiple": 1.8,
      "roi": 0.8
    },
    "loans": 100,
    "fund_size": 100000000
  },
  "execution_time": 5.75,
  "timestamp": "2023-05-21T15:30:50Z"
}
```

#### Error Update

Error that occurred during simulation execution:

```json
{
  "type": "error",
  "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
  "error": "Failed to generate price paths",
  "module": "price_path_simulator",
  "timestamp": "2023-05-21T15:30:45Z"
}
```

#### Guardrail Violation

Notification that a guardrail has been violated:

```json
{
  "type": "guardrail_violation",
  "simulation_id": "123e4567-e89b-12d3-a456-426614174000",
  "violation": {
    "rule": "max_ltv",
    "severity": "warning",
    "message": "Maximum LTV exceeded",
    "details": {
      "max_allowed": 0.5,
      "actual": 0.55
    }
  },
  "timestamp": "2023-05-21T15:30:46Z"
}
```

## TypeScript SDK Integration

The TypeScript SDK includes a WebSocket client that makes it easy to connect to the WebSocket API:

```typescript
import { WebSocketClient } from 'equihome-sim-sdk';

// Create a WebSocket client
const wsClient = new WebSocketClient({
  baseUrl: 'ws://localhost:8000',
  apiKey: 'YOUR_API_KEY',
  autoReconnect: true
});

// Connect to the WebSocket server
wsClient.connect();

// Subscribe to simulation updates
wsClient.on('open', () => {
  wsClient.subscribe('123e4567-e89b-12d3-a456-426614174000');
});

// Handle progress updates
wsClient.on('progress', (data) => {
  console.log(`Progress: ${data.progress}%`);
  updateProgressBar(data.progress);
});

// Handle final results
wsClient.on('result', (data) => {
  console.log('Simulation completed:', data.result);
  displayResults(data.result);
});

// Handle errors
wsClient.on('error_update', (data) => {
  console.error('Simulation error:', data.error);
  showErrorMessage(data.error);
});

// Disconnect when done
function cleanup() {
  wsClient.disconnect();
}
```

## Examples

### Running a Simulation and Monitoring Progress

```typescript
import { Configuration, SimulationApi, WebSocketClient } from 'equihome-sim-sdk';

// Create API client
const config = new Configuration({
  basePath: 'http://localhost:8000',
});
const api = new SimulationApi(config);

// Create WebSocket client
const wsClient = new WebSocketClient({
  baseUrl: 'ws://localhost:8000',
});

// Connect to WebSocket
wsClient.connect();

// Run a simulation and monitor progress
async function runSimulation() {
  try {
    // Start the simulation
    const simulation = await api.createSimulation({
      config: {
        fund_size: 100000000,
        fund_term: 10,
        vintage_year: 2023,
      }
    });
    
    const simulationId = simulation.id;
    
    // Subscribe to updates
    wsClient.subscribe(simulationId);
    
    // Handle different update types
    wsClient.on('progress', (data) => {
      console.log(`Progress: ${data.progress}%`);
      updateProgressBar(data.progress);
    });
    
    wsClient.on('module_started', (data) => {
      console.log(`Module started: ${data.module}`);
      updateStatus(`Running ${data.module}...`);
    });
    
    wsClient.on('module_completed', (data) => {
      console.log(`Module completed: ${data.module} in ${data.execution_time}s`);
    });
    
    wsClient.on('intermediate_result', (data) => {
      console.log(`Intermediate result from ${data.module}:`, data.data);
      updateIntermediateResults(data.data);
    });
    
    wsClient.on('result', (data) => {
      console.log('Simulation completed:', data.result);
      displayFinalResults(data.result);
      wsClient.unsubscribe(simulationId);
    });
    
    wsClient.on('error_update', (data) => {
      console.error('Simulation error:', data.error);
      showErrorMessage(data.error);
      wsClient.unsubscribe(simulationId);
    });
    
    wsClient.on('guardrail_violation', (data) => {
      console.warn('Guardrail violation:', data.violation);
      showWarning(data.violation.message);
    });
    
    return simulationId;
  } catch (error) {
    console.error('Error starting simulation:', error);
    throw error;
  }
}

// Cancel a simulation
function cancelSimulation(simulationId) {
  wsClient.cancelSimulation(simulationId);
}

// Cleanup when done
function cleanup() {
  wsClient.disconnect();
}
```

## Error Handling

The WebSocket client includes built-in error handling:

- **Connection Errors**: The client will automatically attempt to reconnect if the connection is lost
- **Message Parsing Errors**: Invalid JSON messages are logged and ignored
- **Application Errors**: Error updates from the server are emitted as 'error_update' events

You can also listen for WebSocket errors:

```typescript
wsClient.on('error', (error) => {
  console.error('WebSocket error:', error);
});

wsClient.on('close', (event) => {
  console.log('WebSocket connection closed:', event.code, event.reason);
});
```

For more detailed information, refer to the [AsyncAPI specification](../../schemas/asyncapi.yaml).
