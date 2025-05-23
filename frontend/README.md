# EQU IHOME SIM ENGINE v2 - Frontend

This is the frontend application for the EQU IHOME SIM ENGINE v2. It provides a user interface for configuring, running, and analyzing simulations.

## Getting Started

### Prerequisites

- Node.js 16+ and npm/yarn
- Backend API server running

### Installation

1. Install dependencies:

```bash
npm install
# or
yarn install
```

2. Copy the TypeScript SDK:

```bash
cp -r ../sdk-output/typescript ./src/api/sdk
```

3. Start the development server:

```bash
npm run dev
# or
yarn dev
```

4. Open your browser to http://localhost:5173

## Project Structure

```
frontend/
├─ public/                # Static assets
├─ src/
│  ├─ assets/             # Images, fonts, etc.
│  ├─ components/
│  │   ├─ layout/         # Header, layout components
│  │   ├─ charts/         # Chart components
│  │   └─ wizard/         # Wizard step components
│  ├─ pages/              # Page components
│  ├─ api/                # API client and hooks
│  ├─ types/              # TypeScript type definitions
│  ├─ store.ts            # Zustand store
│  └─ index.css           # Global styles
└─ package.json
```

## Key Features

- **Dashboard**: View recent simulations and key metrics
- **Simulation Wizard**: Configure and run new simulations
- **Results Page**: View detailed simulation results with charts and tables
- **Real-time Updates**: Track simulation progress in real-time

## Development Guidelines

### Data Sources

- **NO** hardcoded data anywhere in the codebase
- **NO** fallback data or default values not from the schema
- **ALL** data must come from the backend API or schema defaults

### API Integration

- Use the TypeScript SDK for all API calls
- WebSocket communication must use the SDK's WebSocketClient
- Follow the AsyncAPI specification for WebSocket communication

### Validation

- Use Zod for runtime validation with schemas derived from JSON Schema
- All user inputs must be validated before submission

### Error Handling

- Every API call must have proper error handling
- Display user-friendly error messages
- Log detailed errors for debugging

## Available Scripts

- `npm run dev`: Start the development server
- `npm run build`: Build the application for production
- `npm run preview`: Preview the production build locally
- `npm run lint`: Run ESLint to check for code quality issues
- `npm run test`: Run tests
- `npm run test:watch`: Run tests in watch mode
- `npm run test:coverage`: Run tests with coverage report
