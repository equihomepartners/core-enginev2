# EQU IHOME SIM ENGINE Frontend Integration Guide

This guide provides comprehensive information on how to integrate your frontend application with the EQU IHOME SIM ENGINE backend.

## Table of Contents

- [Overview](#overview)
- [Available Integration Methods](#available-integration-methods)
- [TypeScript SDK](#typescript-sdk)
- [REST API (OpenAPI)](#rest-api-openapi)
- [GraphQL API](#graphql-api)
- [WebSocket API](#websocket-api)
- [Authentication](#authentication)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

## Overview

The EQU IHOME SIM ENGINE provides multiple ways to interact with the backend:

1. **TypeScript SDK**: Pre-built TypeScript client with type definitions
2. **REST API**: RESTful API endpoints documented with OpenAPI
3. **GraphQL API**: GraphQL endpoint for flexible data querying
4. **WebSocket API**: Real-time updates and notifications

Choose the integration method that best fits your frontend technology stack and requirements.

## Available Integration Methods

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| TypeScript SDK | TypeScript/JavaScript frontends | Type safety, IntelliSense support | Additional dependency |
| REST API | Any frontend | Universal compatibility, simplicity | Requires manual request handling |
| GraphQL | Complex data requirements | Flexible queries, reduced over-fetching | Learning curve if new to GraphQL |
| WebSocket | Real-time updates | Live data, push notifications | Requires connection management |

## TypeScript SDK

The TypeScript SDK provides a strongly-typed client for interacting with the backend API.

### Installation

```bash
# Copy the SDK to your project
cp -r sdk-output/typescript /path/to/your/frontend/project/src/sdk

# Install it in your project
cd /path/to/your/frontend/project
npm install ./src/sdk
```

### Usage

```typescript
import { Configuration, SimulationApi } from './sdk';

// Create a configuration
const config = new Configuration({
  basePath: 'http://localhost:8000',
  // Add authentication if needed
  // apiKey: 'YOUR_API_KEY',
});

// Create an API client
const api = new SimulationApi(config);

// Example: Create a simulation
async function createSimulation() {
  try {
    const response = await api.createSimulation({
      config: {
        fund_size: 100000000,
        fund_term: 10,
        vintage_year: 2023,
      }
    });
    console.log('Simulation created:', response);
    return response;
  } catch (error) {
    console.error('Error creating simulation:', error);
    throw error;
  }
}

// Example: Get simulation results
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

### Available API Clients

The SDK provides the following API clients:

- `SimulationApi`: For running simulations and retrieving results
- `TlsApi`: For accessing TLS (Territory, Location, Suburb) data
- `PortfolioApi`: For portfolio management
- `PricePathApi`: For price path simulation
- `WaterfallApi`: For waterfall calculations
- `RiskApi`: For risk metrics
- `FinanceApi`: For financial calculations
- `WebSocketClient`: For real-time updates and notifications

## REST API (OpenAPI)

The REST API is documented using OpenAPI and can be accessed directly using any HTTP client.

### OpenAPI Specification

The OpenAPI specification is available at:
- JSON: `sdk-output/openapi.json`

You can use this specification with tools like Swagger UI, Postman, or OpenAPI Generator.

### Example: Fetch with JavaScript

```javascript
// Create a simulation
async function createSimulation() {
  try {
    const response = await fetch('http://localhost:8000/simulations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        config: {
          fund_size: 100000000,
          fund_term: 10,
          vintage_year: 2023,
        }
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    console.log('Simulation created:', data);
    return data;
  } catch (error) {
    console.error('Error creating simulation:', error);
    throw error;
  }
}

// Get simulation results
async function getSimulationResults(simulationId) {
  try {
    const response = await fetch(`http://localhost:8000/simulations/${simulationId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();
    console.log('Simulation results:', data);
    return data;
  } catch (error) {
    console.error('Error fetching simulation results:', error);
    throw error;
  }
}
```

### Example: Axios with TypeScript

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

interface SimulationConfig {
  fund_size: number;
  fund_term: number;
  vintage_year: number;
  [key: string]: any;
}

interface SimulationRequest {
  config: SimulationConfig;
}

interface SimulationResponse {
  simulation_id: string;
  status: string;
  created_at: string;
}

// Create a simulation
async function createSimulation(config: SimulationConfig): Promise<SimulationResponse> {
  try {
    const response = await api.post<SimulationResponse>('/simulations', {
      config,
    });
    return response.data;
  } catch (error) {
    console.error('Error creating simulation:', error);
    throw error;
  }
}

// Get simulation results
async function getSimulationResults(simulationId: string): Promise<any> {
  try {
    const response = await api.get(`/simulations/${simulationId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching simulation results:', error);
    throw error;
  }
}
```

## GraphQL API

The GraphQL API provides a flexible way to query and mutate data.

### GraphQL Schema

The GraphQL schema is available at:
- `sdk-output/schema.graphql`

### Example: Apollo Client

```typescript
import { ApolloClient, InMemoryCache, gql } from '@apollo/client';

// Create Apollo Client
const client = new ApolloClient({
  uri: 'http://localhost:8000/graphql',
  cache: new InMemoryCache(),
});

// Query: Get simulation
const GET_SIMULATION = gql`
  query GetSimulation($id: String!) {
    simulation(id: $id) {
      id
      status
      createdAt
      completedAt
      executionTime
      metrics {
        irr
        equityMultiple
        roi
        paybackPeriod
      }
    }
  }
`;

// Mutation: Create simulation
const CREATE_SIMULATION = gql`
  mutation CreateSimulation($config: SimulationConfigInput!) {
    createSimulation(config: $config) {
      id
      status
      createdAt
    }
  }
`;

// Example: Create a simulation
async function createSimulation() {
  try {
    const { data } = await client.mutate({
      mutation: CREATE_SIMULATION,
      variables: {
        config: {
          fundSize: 100000000,
          fundTerm: 10,
          vintageYear: 2023,
        },
      },
    });
    console.log('Simulation created:', data.createSimulation);
    return data.createSimulation;
  } catch (error) {
    console.error('Error creating simulation:', error);
    throw error;
  }
}

// Example: Get simulation results
async function getSimulationResults(simulationId: string) {
  try {
    const { data } = await client.query({
      query: GET_SIMULATION,
      variables: { id: simulationId },
    });
    console.log('Simulation results:', data.simulation);
    return data.simulation;
  } catch (error) {
    console.error('Error fetching simulation results:', error);
    throw error;
  }
}
```

## Authentication

The API supports API key authentication. Include your API key in the request headers:

```typescript
// With TypeScript SDK
const config = new Configuration({
  basePath: 'http://localhost:8000',
  apiKey: 'YOUR_API_KEY',
});

// With fetch
fetch('http://localhost:8000/simulations', {
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'YOUR_API_KEY',
  },
  // ...
});

// With Apollo Client
const client = new ApolloClient({
  uri: 'http://localhost:8000/graphql',
  cache: new InMemoryCache(),
  headers: {
    'X-API-Key': 'YOUR_API_KEY',
  },
});
```

## WebSocket API

The WebSocket API provides real-time updates and notifications for simulations.

### WebSocket Connection

Connect to the WebSocket server:

```typescript
// Using the WebSocketClient from the SDK (recommended)
import { WebSocketClient } from 'equihome-sim-sdk';

const wsClient = new WebSocketClient({
  baseUrl: 'ws://localhost:8000',
  apiKey: 'YOUR_API_KEY',
  autoReconnect: true
});

wsClient.connect();

// Or using the native WebSocket API
const socket = new WebSocket('ws://localhost:8000/ws');
```

### Subscribing to Simulation Updates

```typescript
// Using the WebSocketClient
wsClient.subscribe('your-simulation-id');

// Or using the native WebSocket API
socket.onopen = () => {
  socket.send(JSON.stringify({
    action: 'subscribe',
    simulation_id: 'your-simulation-id',
  }));
};
```

### Handling WebSocket Messages

```typescript
// Using the WebSocketClient
wsClient.on('progress', (data) => {
  console.log(`Progress: ${data.progress}%`);
  updateProgressBar(data.progress);
});

wsClient.on('result', (data) => {
  console.log('Simulation completed:', data.result);
  displayResults(data.result);
});

wsClient.on('error_update', (data) => {
  console.error('Simulation error:', data.error);
  showError(data.error);
});

// Or using the native WebSocket API
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received update:', data);

  // Handle different message types
  switch (data.type) {
    case 'progress':
      updateProgressBar(data.progress);
      break;
    case 'result':
      displayResults(data.result);
      break;
    case 'error':
      showError(data.error);
      break;
  }
};
```

For more detailed information about the WebSocket API, see the [WebSocket API Documentation](./WEBSOCKET_API.md).

## Common Use Cases

### Handling Long-running Simulations

For simulations that take a long time to complete:

1. Create the simulation (returns immediately with a simulation ID)
2. Poll for results or use WebSockets for real-time updates
3. Display progress to the user
4. Show results when the simulation completes

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend has CORS enabled for your frontend domain
2. **Authentication Errors**: Verify your API key is correct and properly included in requests
3. **Network Errors**: Check that the backend server is running and accessible

### Debugging Tips

1. Use browser developer tools to inspect network requests
2. Enable verbose logging in the SDK:
   ```typescript
   const config = new Configuration({
     basePath: 'http://localhost:8000',
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

## Additional Resources

- [Backend API Documentation](http://localhost:8000/docs)
- [OpenAPI Specification](http://localhost:8000/openapi.json)
- [GraphQL Playground](http://localhost:8000/graphql)
- [WebSocket API Documentation](./WEBSOCKET_API.md)
- [AsyncAPI Specification](../schemas/asyncapi.yaml)
- [TypeScript SDK Guide](./TYPESCRIPT_SDK_GUIDE.md)
- [Quick Start Guide](./QUICKSTART.md)
