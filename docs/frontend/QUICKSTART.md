# EQU IHOME SIM ENGINE Frontend Quick Start Guide

This guide will help you quickly set up and start using the EQU IHOME SIM ENGINE API in your frontend application.

## 1. Choose Your Integration Method

### Option A: TypeScript SDK (Recommended for TypeScript Projects)

1. **Copy the SDK to your project**:
   ```bash
   cp -r sdk-output/typescript /path/to/your/frontend/project/src/sdk
   ```

2. **Install it in your project**:
   ```bash
   cd /path/to/your/frontend/project
   npm install ./src/sdk
   ```

3. **Basic REST API usage**:
   ```typescript
   import { Configuration, SimulationApi } from './sdk';

   const api = new SimulationApi(new Configuration({
     basePath: 'http://localhost:8000',
   }));

   // Run a simulation
   const result = await api.createSimulation({
     config: {
       fund_size: 100000000,
       fund_term: 10,
       vintage_year: 2023,
     }
   });
   ```

4. **Basic WebSocket usage**:
   ```typescript
   import { WebSocketClient } from './sdk';

   const wsClient = new WebSocketClient({
     baseUrl: 'ws://localhost:8000',
   });

   // Connect to WebSocket server
   wsClient.connect();

   // Subscribe to simulation updates
   wsClient.subscribe('simulation-id');

   // Handle updates
   wsClient.on('progress', (data) => {
     console.log(`Progress: ${data.progress}%`);
   });

   wsClient.on('result', (data) => {
     console.log('Simulation completed:', data.result);
   });
   ```

### Option B: Direct API Calls

1. **Use the OpenAPI specification**:
   - Reference `sdk-output/openapi.json` for endpoint details

2. **Basic usage with fetch**:
   ```javascript
   // Run a simulation
   const response = await fetch('http://localhost:8000/simulations', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({
       config: {
         fund_size: 100000000,
         fund_term: 10,
         vintage_year: 2023,
       }
     }),
   });

   const result = await response.json();
   ```

### Option C: GraphQL

1. **Use the GraphQL schema**:
   - Reference `sdk-output/schema.graphql` for available queries and mutations

2. **Basic usage with Apollo Client**:
   ```javascript
   import { ApolloClient, InMemoryCache, gql } from '@apollo/client';

   const client = new ApolloClient({
     uri: 'http://localhost:8000/graphql',
     cache: new InMemoryCache(),
   });

   const CREATE_SIMULATION = gql`
     mutation CreateSimulation($config: SimulationConfigInput!) {
       createSimulation(config: $config) {
         id
         status
       }
     }
   `;

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
   ```

## 2. Common API Operations

### Run a Simulation

```typescript
// Using TypeScript SDK
const simulation = await api.createSimulation({
  config: {
    fund_size: 100000000,
    fund_term: 10,
    vintage_year: 2023,
    management_fee_rate: 0.02,
    carried_interest_rate: 0.20,
    hurdle_rate: 0.08,
  }
});

// Store the simulation ID for later use
const simulationId = simulation.id;
```

### Get Simulation Results

```typescript
// Using TypeScript SDK
const results = await api.getSimulation(simulationId);

// Access metrics
const irr = results.metrics.irr;
const equityMultiple = results.metrics.equity_multiple;
```

### Get TLS (Territory, Location, Suburb) Data

```typescript
// Using TypeScript SDK
const suburbs = await api.getSuburbs();

// Get details for a specific suburb
const suburbDetails = await api.getSuburb(suburbId);
```

### Calculate Waterfall Distribution

```typescript
// Using TypeScript SDK
const waterfallResults = await api.calculateWaterfall(simulationId, {
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
```

## 3. Real-time Updates with WebSockets

For long-running simulations, use WebSockets to get real-time updates:

### Using the WebSocketClient (Recommended)

```typescript
import { WebSocketClient } from './sdk';

// Create WebSocket client
const wsClient = new WebSocketClient({
  baseUrl: 'ws://localhost:8000',
  autoReconnect: true,
});

// Connect to WebSocket server
wsClient.connect();

// Subscribe to simulation updates
wsClient.subscribe(simulationId);

// Handle different types of updates
wsClient.on('progress', (data) => {
  // Update progress bar
  updateProgressBar(data.progress);
  console.log(`Progress: ${data.progress}%, Module: ${data.module}`);
});

wsClient.on('module_started', (data) => {
  console.log(`Module started: ${data.module}`);
});

wsClient.on('module_completed', (data) => {
  console.log(`Module completed: ${data.module} in ${data.execution_time}s`);
});

wsClient.on('result', (data) => {
  // Show final results
  displayResults(data.result);
  console.log('Simulation completed:', data.result);

  // Unsubscribe when done
  wsClient.unsubscribe(simulationId);
});

wsClient.on('error_update', (data) => {
  console.error('Simulation error:', data.error);
  showError(data.error);
});

// Disconnect when done
function cleanup() {
  wsClient.disconnect();
}
```

### Using Native WebSocket API

```javascript
// Connect to WebSocket
const socket = new WebSocket('ws://localhost:8000/ws');

// Listen for messages
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === 'progress') {
    // Update progress bar
    updateProgressBar(data.progress);
  } else if (data.type === 'result') {
    // Show final results
    displayResults(data.result);
  } else if (data.type === 'error') {
    // Show error message
    showError(data.error);
  }
};

// Subscribe to simulation updates
socket.onopen = () => {
  socket.send(JSON.stringify({
    action: 'subscribe',
    simulation_id: simulationId,
  }));
};
```

## 4. Error Handling

```typescript
// Using TypeScript SDK
try {
  const simulation = await api.createSimulation({
    config: {
      fund_size: 100000000,
      fund_term: 10,
      vintage_year: 2023,
    }
  });
} catch (error) {
  if (error.status === 400) {
    // Handle validation errors
    console.error('Invalid simulation parameters:', error.body);
  } else if (error.status === 401) {
    // Handle authentication errors
    console.error('Authentication failed');
  } else {
    // Handle other errors
    console.error('An error occurred:', error);
  }
}
```

## 5. Configuration Parameters

The simulation engine accepts the following key parameters:

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| fund_size | number | Total fund size in dollars | Required |
| fund_term | number | Fund term in years | Required |
| vintage_year | number | Fund vintage year | Required |
| management_fee_rate | number | Management fee as decimal (e.g., 0.02 for 2%) | 0.02 |
| carried_interest_rate | number | Carried interest as decimal (e.g., 0.20 for 20%) | 0.20 |
| hurdle_rate | number | Hurdle rate as decimal (e.g., 0.08 for 8%) | 0.08 |
| target_irr | number | Target IRR as decimal | 0.15 |
| target_equity_multiple | number | Target equity multiple | 1.5 |
| max_ltv | number | Maximum loan-to-value ratio | 0.50 |
| max_loan_size | number | Maximum loan size in dollars | 500000 |
| avg_exit_year | number | Average loan exit year | 5 |

## 6. Next Steps

- Explore the full [Frontend Integration Guide](./README.md) for detailed information
- Check the [OpenAPI specification](../sdk-output/openapi.json) for all available endpoints
- Review the [GraphQL schema](../sdk-output/schema.graphql) for all available queries and mutations
- Read the [WebSocket API Documentation](./WEBSOCKET_API.md) for real-time updates
- Examine the [AsyncAPI specification](../schemas/asyncapi.yaml) for WebSocket message formats

## 7. Troubleshooting

- **CORS Issues**: Ensure the backend has CORS enabled for your frontend domain
- **Connection Errors**: Verify the backend server is running at the expected URL
- **Authentication Errors**: Check if you need to include an API key in your requests

For more detailed information, refer to the [Frontend Integration Guide](./README.md).
