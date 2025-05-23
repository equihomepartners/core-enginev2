# EQU IHOME SIM ENGINE TypeScript SDK Guide

This guide provides detailed information on how to use the TypeScript SDK to interact with the EQU IHOME SIM ENGINE API.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [API Clients](#api-clients)
- [Common Operations](#common-operations)
- [Advanced Usage](#advanced-usage)
- [Error Handling](#error-handling)
- [TypeScript Types](#typescript-types)

## Installation

### Option 1: Install from Local Directory

```bash
# Copy the SDK to your project
cp -r sdk-output/typescript /path/to/your/frontend/project/src/sdk

# Install it in your project
cd /path/to/your/frontend/project
npm install ./src/sdk
```

### Option 2: Install from Package Registry (if published)

```bash
npm install equihome-sim-sdk
```

## Configuration

Create a configuration object to initialize the API clients:

```typescript
import { Configuration } from './sdk';

const config = new Configuration({
  // Base URL of the API
  basePath: 'http://localhost:8000',

  // Optional: API key for authentication
  apiKey: 'YOUR_API_KEY',

  // Optional: Custom headers
  headers: {
    'X-Custom-Header': 'custom-value',
  },

  // Optional: Request middleware for logging, etc.
  middleware: [
    {
      pre: async (context) => {
        console.log('Request:', context.init);
        return context;
      },
      post: async (context) => {
        console.log('Response:', context.response);
        return context;
      },
    },
  ],
});
```

## API Clients

The SDK provides the following API clients:

### SimulationApi

For running simulations and retrieving results:

```typescript
import { SimulationApi } from './sdk';

const simulationApi = new SimulationApi(config);
```

### WebSocketClient

For real-time updates and notifications:

```typescript
import { WebSocketClient } from './sdk';

const wsClient = new WebSocketClient({
  baseUrl: 'ws://localhost:8000',
  apiKey: 'YOUR_API_KEY',
  autoReconnect: true,
  maxReconnectAttempts: 5,
  reconnectDelay: 3000
});

wsClient.connect();
```

### TlsApi

For accessing TLS (Territory, Location, Suburb) data:

```typescript
import { TlsApi } from './sdk';

const tlsApi = new TlsApi(config);
```

### PortfolioApi

For portfolio management:

```typescript
import { PortfolioApi } from './sdk';

const portfolioApi = new PortfolioApi(config);
```

### PricePathApi

For price path simulation:

```typescript
import { PricePathApi } from './sdk';

const pricePathApi = new PricePathApi(config);
```

### WaterfallApi

For waterfall calculations:

```typescript
import { WaterfallApi } from './sdk';

const waterfallApi = new WaterfallApi(config);
```

### RiskApi

For risk metrics:

```typescript
import { RiskApi } from './sdk';

const riskApi = new RiskApi(config);
```

### FinanceApi

For financial calculations:

```typescript
import { FinanceApi } from './sdk';

const financeApi = new FinanceApi(config);
```

## Common Operations

### Create a Simulation

```typescript
import { SimulationApi, Configuration } from './sdk';

const api = new SimulationApi(new Configuration({
  basePath: 'http://localhost:8000',
}));

async function createSimulation() {
  try {
    const response = await api.createSimulation({
      config: {
        fund_size: 100000000,
        fund_term: 10,
        vintage_year: 2023,
        management_fee_rate: 0.02,
        carried_interest_rate: 0.20,
        hurdle_rate: 0.08,
      }
    });

    console.log('Simulation created:', response);
    return response;
  } catch (error) {
    console.error('Error creating simulation:', error);
    throw error;
  }
}
```

### Get Simulation Results

```typescript
async function getSimulationResults(simulationId: string) {
  try {
    const results = await api.getSimulation(simulationId);
    console.log('Simulation results:', results);
    return results;
  } catch (error) {
    console.error('Error fetching simulation results:', error);
    throw error;
  }
}
```

### Get TLS Data

```typescript
import { TlsApi, Configuration } from './sdk';

const api = new TlsApi(new Configuration({
  basePath: 'http://localhost:8000',
}));

async function getSuburbs() {
  try {
    const suburbs = await api.getSuburbs();
    console.log('Suburbs:', suburbs);
    return suburbs;
  } catch (error) {
    console.error('Error fetching suburbs:', error);
    throw error;
  }
}

async function getSuburbDetails(suburbId: string) {
  try {
    const suburb = await api.getSuburb(suburbId);
    console.log('Suburb details:', suburb);
    return suburb;
  } catch (error) {
    console.error('Error fetching suburb details:', error);
    throw error;
  }
}
```

### Calculate Waterfall

```typescript
import { WaterfallApi, Configuration } from './sdk';

const api = new WaterfallApi(new Configuration({
  basePath: 'http://localhost:8000',
}));

async function calculateWaterfall(simulationId: string) {
  try {
    const waterfall = await api.calculateWaterfall(simulationId, {
      tranches: [
        {
          name: "Senior Debt",
          type: "debt",
          rate: 0.05,
          size: 50000000,
          priority: 1
        },
        {
          name: "Mezzanine",
          type: "debt",
          rate: 0.08,
          size: 20000000,
          priority: 2
        },
        {
          name: "Equity",
          type: "equity",
          size: 30000000,
          priority: 3
        }
      ]
    });

    console.log('Waterfall calculation:', waterfall);
    return waterfall;
  } catch (error) {
    console.error('Error calculating waterfall:', error);
    throw error;
  }
}
```

## Advanced Usage

### Real-time Updates with WebSocketClient

The SDK includes a WebSocketClient for handling real-time updates:

```typescript
import { WebSocketClient } from './sdk';

// Create WebSocket client
const wsClient = new WebSocketClient({
  baseUrl: 'ws://localhost:8000',
  autoReconnect: true,
});

// Connect to WebSocket server
wsClient.connect();

// Event listeners
wsClient.on('open', () => {
  console.log('WebSocket connected');
});

wsClient.on('close', (event) => {
  console.log('WebSocket disconnected:', event.code, event.reason);
});

wsClient.on('error', (error) => {
  console.error('WebSocket error:', error);
});

// Subscribe to simulation updates
wsClient.subscribe('simulation-id');

// Handle different types of updates
wsClient.on('progress', (data) => {
  console.log(`Progress: ${data.progress}%, Module: ${data.module}`);
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
  updateIntermediateResults(data.module, data.data);
});

wsClient.on('result', (data) => {
  console.log('Simulation completed:', data.result);
  displayResults(data.result);

  // Unsubscribe when done
  wsClient.unsubscribe('simulation-id');
});

wsClient.on('error_update', (data) => {
  console.error('Simulation error:', data.error);
  showError(data.error);
});

wsClient.on('guardrail_violation', (data) => {
  console.warn('Guardrail violation:', data.violation);
  showWarning(data.violation.message, data.violation.severity);
});

// Disconnect when done
function cleanup() {
  wsClient.disconnect();
}
```

### Handling Long-running Simulations

For simulations that take a long time to complete, combine the REST API and WebSocket API:

```typescript
import { SimulationApi, Configuration, WebSocketClient } from './sdk';

const api = new SimulationApi(new Configuration({
  basePath: 'http://localhost:8000',
}));

const wsClient = new WebSocketClient({
  baseUrl: 'ws://localhost:8000',
  autoReconnect: true,
});

async function runLongSimulation() {
  // Connect to WebSocket
  wsClient.connect();

  // Start the simulation
  const simulation = await api.createSimulation({
    config: {
      fund_size: 100000000,
      fund_term: 10,
      vintage_year: 2023,
    }
  });

  const simulationId = simulation.id;

  return new Promise((resolve, reject) => {
    // Subscribe to simulation updates
    wsClient.subscribe(simulationId);

    // Handle progress updates
    wsClient.on('progress', (data) => {
      console.log(`Progress: ${data.progress}%`);
      updateProgressBar(data.progress);
    });

    // Handle final results
    wsClient.on('result', (data) => {
      console.log('Simulation completed:', data.result);
      wsClient.unsubscribe(simulationId);
      resolve(data.result);
    });

    // Handle errors
    wsClient.on('error_update', (data) => {
      console.error('Simulation failed:', data.error);
      wsClient.unsubscribe(simulationId);
      reject(new Error(data.error));
    });
  });
}
```

### Batch Operations

For running multiple simulations in parallel:

```typescript
import { SimulationApi, Configuration } from './sdk';

const api = new SimulationApi(new Configuration({
  basePath: 'http://localhost:8000',
}));

async function runBatchSimulations(configs) {
  // Run simulations in parallel
  const simulationPromises = configs.map(config =>
    api.createSimulation({ config })
  );

  // Wait for all simulations to start
  const simulations = await Promise.all(simulationPromises);

  // Get simulation IDs
  const simulationIds = simulations.map(sim => sim.id);

  console.log('Started simulations:', simulationIds);
  return simulationIds;
}
```

## Error Handling

The SDK throws exceptions for API errors. Handle them appropriately:

```typescript
import { SimulationApi, Configuration } from './sdk';

const api = new SimulationApi(new Configuration({
  basePath: 'http://localhost:8000',
}));

async function createSimulationWithErrorHandling() {
  try {
    const response = await api.createSimulation({
      config: {
        fund_size: 100000000,
        fund_term: 10,
        vintage_year: 2023,
      }
    });

    return response;
  } catch (error) {
    // Check error status
    if (error.status === 400) {
      console.error('Invalid simulation parameters:', error.body);
      // Handle validation errors
    } else if (error.status === 401) {
      console.error('Authentication failed');
      // Handle authentication errors
    } else if (error.status === 404) {
      console.error('Resource not found');
      // Handle not found errors
    } else if (error.status === 500) {
      console.error('Server error:', error.body);
      // Handle server errors
    } else {
      console.error('Unknown error:', error);
      // Handle other errors
    }

    throw error;
  }
}
```

## TypeScript Types

The SDK provides TypeScript types for all API requests and responses:

```typescript
import {
  SimulationConfig,
  SimulationResult,
  Suburb,
  PricePath,
  WaterfallResult,
  RiskMetrics,
  Tranche,
  // WebSocket types
  WebSocketUpdatePayload,
  ProgressUpdatePayload,
  ModuleStartedPayload,
  ModuleCompletedPayload,
  IntermediateResultPayload,
  FinalResultPayload,
  ErrorUpdatePayload,
  GuardrailViolationPayload
} from './sdk';

// Example: Create a strongly-typed simulation config
const config: SimulationConfig = {
  fund_size: 100000000,
  fund_term: 10,
  vintage_year: 2023,
  management_fee_rate: 0.02,
  carried_interest_rate: 0.20,
  hurdle_rate: 0.08,
};

// Example: Define tranches with proper typing
const tranches: Tranche[] = [
  {
    name: "Senior Debt",
    type: "debt",
    rate: 0.05,
    size: 50000000,
    priority: 1
  },
  {
    name: "Equity",
    type: "equity",
    size: 30000000,
    priority: 2
  }
];
```

## Additional Resources

- [Full Frontend Integration Guide](./README.md)
- [Quick Start Guide](./QUICKSTART.md)
- [WebSocket API Documentation](./WEBSOCKET_API.md)
- [OpenAPI Specification](../sdk-output/openapi.json)
- [AsyncAPI Specification](../schemas/asyncapi.yaml)
