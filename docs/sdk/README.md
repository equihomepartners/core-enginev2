# EQU IHOME SIM ENGINE SDK Generation

This document describes the SDK generation process for the EQU IHOME SIM ENGINE v2.

## Overview

The SDK generation process creates client SDKs for the EQU IHOME SIM ENGINE API. It generates:

- OpenAPI specification from the FastAPI app
- TypeScript SDK using OpenAPI Generator
- Python SDK using OpenAPI Generator
- GraphQL schema and resolvers

## Prerequisites

The SDK generation requires the following dependencies:

- Docker (recommended for consistent environment)
- Python 3.11+
- Node.js and npm (for OpenAPI Generator)
- Poetry (for Python dependency management)

## Quick Start

The easiest way to generate the SDKs is using Docker:

```bash
# Generate all SDKs
docker compose -f docker-compose.sdk.yml run --rm sdkgen

# Generate specific SDK
docker compose -f docker-compose.sdk.yml run --rm sdkgen --typescript
```

## Docker-based SDK Generation

The Docker-based approach ensures a consistent environment for SDK generation:

1. **Build the SDK generator image**:
   ```bash
   docker build -f sdk-build/Dockerfile -t sdkgen .
   ```

2. **Generate all SDKs**:
   ```bash
   docker run --rm -v $(pwd):/workspace sdkgen --all
   ```

3. **Generate specific SDK**:
   ```bash
   # Generate TypeScript SDK
   docker run --rm -v $(pwd):/workspace sdkgen --typescript
   
   # Generate Python SDK
   docker run --rm -v $(pwd):/workspace sdkgen --python
   
   # Generate GraphQL schema
   docker run --rm -v $(pwd):/workspace sdkgen --graphql
   ```

## Local SDK Generation

If you prefer to generate the SDKs locally:

1. **Install dependencies**:
   ```bash
   # Install Python dependencies
   poetry install
   
   # Install OpenAPI Generator
   npm install -g @openapitools/openapi-generator-cli
   ```

2. **Generate all SDKs**:
   ```bash
   python -m src.sdk.openapi_gen --all
   ```

3. **Generate specific SDK**:
   ```bash
   # Generate TypeScript SDK
   python -m src.sdk.openapi_gen --typescript
   
   # Generate Python SDK
   python -m src.sdk.openapi_gen --python
   
   # Generate GraphQL schema
   python -m src.sdk.openapi_gen --graphql
   ```

## SDK Generation Options

The SDK generation script supports the following options:

```
usage: openapi_gen.py [-h] [--output-dir OUTPUT_DIR] [--openapi-file OPENAPI_FILE]
                     [--format {json,yaml}] [--typescript] [--python] [--graphql]
                     [--all] [--validate] [--no-validate]

Generate OpenAPI specification and SDKs

options:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR
                        Output directory for SDKs
  --openapi-file OPENAPI_FILE
                        Path to the OpenAPI specification file (generated if not provided)
  --format {json,yaml}  Output format for OpenAPI specification
  --typescript          Generate TypeScript SDK
  --python              Generate Python SDK
  --graphql             Generate GraphQL schema
  --all                 Generate all SDKs
  --validate            Validate OpenAPI specification
  --no-validate         Skip OpenAPI specification validation
```

## Output Structure

The SDK generation creates the following output structure:

```
sdk-output/
├── openapi.json        # OpenAPI specification
├── schema.graphql      # GraphQL schema
├── python/             # Python SDK
│   ├── setup.py
│   ├── README.md
│   └── ...
└── typescript/         # TypeScript SDK
    ├── api.ts
    ├── package.json
    └── ...
```

## Using the Generated SDKs

### TypeScript SDK

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

### Python SDK

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

### GraphQL API

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

## CI/CD Integration

The SDK generation is integrated with GitHub Actions:

1. **Automatic SDK generation**: The SDK is automatically generated when changes are made to the API or schemas.
2. **Validation**: The CI pipeline validates that the generated SDK is up-to-date.
3. **Artifacts**: The generated SDK is uploaded as an artifact for easy download.

## Troubleshooting

### Common Issues

1. **OpenAPI Generator not found**:
   ```
   openapi-generator-cli not found
   ```
   Solution: Install OpenAPI Generator CLI:
   ```bash
   npm install -g @openapitools/openapi-generator-cli
   ```

2. **Invalid OpenAPI specification**:
   ```
   OpenAPI specification validation failed
   ```
   Solution: Fix the API definition in the FastAPI app.

3. **Docker permission issues**:
   ```
   Permission denied
   ```
   Solution: Run Docker with appropriate permissions:
   ```bash
   sudo docker compose -f docker-compose.sdk.yml run --rm sdkgen
   ```

### Getting Help

If you encounter issues with the SDK generation, please:

1. Check the logs for error messages
2. Verify that all dependencies are installed
3. Ensure that the API definition is valid
4. Contact the development team for assistance
