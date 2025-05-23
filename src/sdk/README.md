# SDK Generation Module

## Overview

The SDK Generation module is responsible for generating OpenAPI specifications and client SDKs for the EQU IHOME SIM ENGINE v2 API. It also provides GraphQL schema generation and resolvers.

## Features

- OpenAPI specification generation from FastAPI app
- TypeScript SDK generation using OpenAPI Generator
- Python SDK generation using OpenAPI Generator
- GraphQL schema generation
- GraphQL resolvers for FastAPI integration

## Components

### OpenAPI Generator

The `openapi_gen.py` module provides functionality for generating OpenAPI specifications and client SDKs:

- `generate_openapi_spec()`: Generates an OpenAPI specification from the FastAPI app
- `generate_typescript_sdk()`: Generates a TypeScript SDK from an OpenAPI specification
- `generate_python_sdk()`: Generates a Python SDK from an OpenAPI specification
- `generate_all_sdks()`: Generates all SDKs

### GraphQL Schema Generator

The `graphql_schema.py` module provides functionality for generating GraphQL schemas and resolvers:

- `generate_graphql_schema()`: Generates a GraphQL schema from the FastAPI app
- `generate_graphql_router()`: Generates a GraphQL router for the FastAPI app
- `save_graphql_schema()`: Saves the GraphQL schema to a file
- `mount_graphql_router()`: Mounts the GraphQL router on the FastAPI app

### CLI Utilities

The `cli.py` module provides command-line utilities for generating OpenAPI specifications and SDKs:

- `openapi`: Generates an OpenAPI specification
- `graphql`: Generates a GraphQL schema
- `typescript`: Generates a TypeScript SDK
- `python`: Generates a Python SDK
- `all`: Generates all SDKs

## Usage

### Generating OpenAPI Specification

```bash
# Generate OpenAPI specification in JSON format
python -m src.sdk.cli openapi --output-file schemas/openapi.json

# Generate OpenAPI specification in YAML format
python -m src.sdk.cli openapi --output-file schemas/openapi.yaml --format yaml
```

### Generating GraphQL Schema

```bash
# Generate GraphQL schema
python -m src.sdk.cli graphql --output-file schemas/schema.graphql
```

### Generating TypeScript SDK

```bash
# Generate TypeScript SDK
python -m src.sdk.cli typescript --openapi-file schemas/openapi.json --output-dir sdk-output/typescript
```

### Generating Python SDK

```bash
# Generate Python SDK
python -m src.sdk.cli python --openapi-file schemas/openapi.json --output-dir sdk-output/python
```

### Generating All SDKs

```bash
# Generate all SDKs
python -m src.sdk.cli all --output-dir sdk-output
```

## Dependencies

- FastAPI: For API definition
- Strawberry: For GraphQL schema generation
- OpenAPI Generator: For SDK generation (installed via npm)

## Installation

The SDK Generation module requires the following dependencies:

```bash
# Install Python dependencies
pip install fastapi strawberry-graphql

# Install OpenAPI Generator (optional, for SDK generation)
npm install @openapitools/openapi-generator-cli -g
```

## Integration with FastAPI

The GraphQL router is automatically mounted on the FastAPI app at `/graphql` when the server starts. You can access the GraphQL playground at `/graphql` when the server is running.

The OpenAPI specification is automatically generated and available at `/openapi.json` when the server is running. You can access the Swagger UI at `/docs` and the ReDoc UI at `/redoc`.

## Examples

### Using the TypeScript SDK

```typescript
import { SimulationApi, Configuration } from 'equihome-sim-sdk';

// Create configuration
const config = new Configuration({
  basePath: 'http://localhost:8000',
  apiKey: 'your-api-key',
});

// Create API client
const api = new SimulationApi(config);

// Run a simulation
const result = await api.createSimulation({
  config: {
    fund_size: 100000000,
    fund_term: 10,
    vintage_year: 2023,
  },
});

console.log(result);
```

### Using the Python SDK

```python
from equihome_sim_sdk import SimulationApi, Configuration

# Create configuration
config = Configuration(
    host="http://localhost:8000",
    api_key={"apiKey": "your-api-key"},
)

# Create API client
api = SimulationApi(config)

# Run a simulation
result = api.create_simulation(
    simulation_request={
        "config": {
            "fund_size": 100000000,
            "fund_term": 10,
            "vintage_year": 2023,
        }
    }
)

print(result)
```

### Using the GraphQL API

```graphql
# Query a simulation
query GetSimulation {
  simulation(id: "sim-123") {
    id
    status
    metrics {
      irr
      equity_multiple
    }
  }
}

# Create a simulation
mutation CreateSimulation {
  createSimulation(
    config: {
      fund_size: 100000000
      fund_term: 10
      vintage_year: 2023
    }
  ) {
    id
    status
  }
}
```
