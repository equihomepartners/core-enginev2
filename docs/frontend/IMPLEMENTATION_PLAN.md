# EQU IHOME SIM ENGINE v2 - Frontend Implementation Plan

## ⚠️ CRITICAL RULES AND GUIDELINES ⚠️

### Data Sources and Validation

1. **ZERO MOCK DATA POLICY**
   - **NO** hardcoded data anywhere in the codebase
   - **NO** fallback data or default values not from the schema
   - **NO** synthetic/fake data generation
   - **ALL** data must come from the backend API or schema defaults

2. **Schema as Single Source of Truth**
   - Use `/schemas/simulation_config_schema.json` for all input parameters
   - Use `/schemas/simulation_result_schema.json` for all output structures
   - Generate TypeScript types directly from these schemas

3. **SDK Integration Requirements**
   - Use the TypeScript SDK from `sdk-output/typescript` for all API calls
   - **DO NOT** create custom API clients or bypass the SDK
   - WebSocket communication must use the SDK's WebSocketClient

4. **Validation Chain**
   - Frontend validation must mirror schema constraints
   - Use Zod for runtime validation with schemas derived from JSON Schema
   - All user inputs must be validated before submission

5. **Error Handling Protocol**
   - Every API call must have proper error handling
   - Display user-friendly error messages
   - Log detailed errors for debugging
   - Implement retry mechanisms for transient failures

6. **Real-time Updates with AsyncAPI**
   - Use WebSockets for all real-time progress and updates
   - Follow the AsyncAPI specification in `schemas/asyncapi.yaml` for WebSocket communication
   - Implement handlers for all message types defined in the AsyncAPI spec
   - Ensure proper connection management (reconnection, error handling)
   - Display progress indicators for long-running operations
   - Process intermediate results as they become available

## Table of Contents

- [Phase 1: Frontend Setup and Environment Configuration](#phase-1-frontend-setup-and-environment-configuration)
- [Phase 2: Homepage Implementation](#phase-2-homepage-implementation)
- [Phase 3: Simulation Wizard Implementation](#phase-3-simulation-wizard-implementation)
- [Phase 4: Simulation Results Page](#phase-4-simulation-results-page)
- [Phase 5: Testing and Optimization](#phase-5-testing-and-optimization)

## Phase 1: Frontend Setup and Environment Configuration

### 1.1 Project Structure Setup

- [x] Create frontend directory with the specified folder structure
  - [x] `public/` directory for static assets
  - [x] `src/assets/` for images and SVGs
  - [x] `src/components/` with layout, charts, and wizard subdirectories
  - [x] `src/pages/` for main page components
  - [x] `src/api/` for SDK integration
  - [x] `src/types/` for TypeScript definitions
  - [x] `src/store.ts` for Zustand store

- [x] Configure build tools and dependencies
  - [x] Set up package.json with React, TypeScript, Vite
  - [x] Configure Tailwind CSS with custom color tokens
  - [x] Set up ESLint and Prettier with strict rules
  - [x] Configure TypeScript with strict mode enabled
  - [x] Set up Vite for development and production builds

- [x] Create base configuration files
  - [x] `tsconfig.json` with strict type checking
  - [x] `vite.config.ts` with proper aliases and plugins
  - [x] `tailwind.config.js` with custom theme
  - [x] `.eslintrc.js` with React and TypeScript rules
  - [x] `.prettierrc` for code formatting

### 1.2 SDK Integration

- [x] Create script to copy TypeScript SDK from `sdk-output/typescript` to `src/api/sdk`
  - [x] Add copy-sdk.sh script for easy SDK integration
  - [x] Make script executable with proper permissions

- [x] Create API client configuration
  - [x] Set up base URL configuration with proxy in Vite
  - [x] Implement authentication handling with token support
  - [x] Add request/response interceptors for logging and error handling

- [x] Implement WebSocket client using AsyncAPI specification
  - [x] Create connection management with auto-reconnect
  - [x] Implement message handlers for all event types
  - [x] Add subscription management for simulation updates
  - [x] Handle all message types defined in the AsyncAPI spec:
    - progress
    - module_started
    - module_completed
    - intermediate_result
    - result
    - error
    - guardrail_violation

- [x] Create placeholder TypeScript types
  - [x] Define SimulationConfig interface
  - [x] Define SimulationResult interface
  - [x] Define Simulation interface with status tracking

### 1.3 State Management and Routing

- [x] Set up Zustand store
  - [x] Create simulation config slice with setters
  - [x] Create simulation results slice with setters
  - [x] Create UI state slice for tracking progress and errors
  - [x] Create simulation status tracking

- [x] Configure React Router
  - [x] Set up route definitions for Home, Wizard, and RunDetail
  - [x] Implement nested routes with layout wrapper
  - [x] Add NotFound page for 404 handling

- [x] Create base layout components
  - [x] Header component with logo and navigation
  - [x] Layout component with container and outlet
  - [x] Card component for content containers
  - [x] Logo component for branding

- [x] Implement error handling
  - [x] Add Blueprint Toaster for notifications
  - [x] Implement API error handling in interceptors
  - [x] Add error state management in store

## Phase 2: Homepage Implementation

### 2.1 Header and Navigation

- [x] Create HeaderBar component
  - [x] Add logo on the left
  - [x] Add "Equihome Simulation" title
  - [x] Style with Tailwind bg-midnight, h-14
  - [x] Make header sticky at the top

- [x] Implement responsive design
  - [x] Hide navigation links on mobile
  - [x] Implement responsive container
  - [x] Add proper spacing and alignment

### 2.2 Quick Actions Section

- [x] Create "Run New Simulation" button
  - [x] Style with Blueprint Button primary
  - [x] Add icon and text
  - [x] Implement navigation to wizard

- [x] Add action button container
  - [x] Position in header and on homepage
  - [x] Add proper spacing and alignment
  - [x] Ensure responsive behavior

### 2.3 Recent Simulations Table

- [x] Create placeholder for table component
  - [x] Add Card container for the table
  - [x] Prepare for future implementation
  - [x] Add title and structure

- [x] Prepare API integration
  - [x] Create API hooks for data fetching
  - [x] Set up TanStack Query configuration
  - [x] Add loading and error state handling

- [x] Add status display
  - [x] Create placeholder for status information
  - [x] Prepare for status badge implementation
  - [x] Add structure for status display

- [x] Create loading skeleton placeholder
  - [x] Add dependencies for content loading
  - [x] Prepare structure for loading states
  - [x] Set up for animation implementation

- [x] Implement empty state
  - [x] Use Blueprint NonIdealState component
  - [x] Add "No simulations yet" message
  - [x] Provide "Run New Simulation" call to action

### 2.4 Dashboard Metrics

- [x] Create KPI ribbon component
  - [x] Design metric cards with icons
  - [x] Implement color coding for values
  - [x] Add trend indicators with directional colors

- [x] Implement charts
  - [x] Set up visx for chart rendering
  - [x] Create reusable LineChart component
  - [x] Implement responsive sizing with ParentSize
  - [x] Add axes, grids, and proper styling

- [x] Prepare WebSocket integration
  - [x] Create WebSocket client with event handlers
  - [x] Set up connection management
  - [x] Add error handling for connection issues

## Phase 3: Simulation Wizard Implementation

### 3.1 Wizard Framework

- [x] Create WizardContainer component
  - [x] Implement 4-step indicator with titles
  - [x] Add navigation buttons (Previous, Next, Cancel)
  - [x] Create content area for steps
  - [x] Add progress bar at the top

- [x] Implement navigation logic
  - [x] Track current step in state
  - [x] Add next/previous functionality
  - [x] Add conditional rendering for final step
  - [x] Implement button state management

- [x] Create form state management
  - [x] Set up form state in component
  - [x] Implement onChange handlers for form fields
  - [x] Add state persistence between steps
  - [x] Create custom form components

- [x] Add progress tracking
  - [x] Create visual progress indicator with ProgressBar
  - [x] Update progress as steps are completed
  - [x] Add step indicators with active state
  - [x] Implement step navigation

### 3.2 Step 1: Fund Basics

- [x] Create form fields for fund basics
  - [x] fund_name (text input)
  - [x] fund_size (number input with validation)
  - [x] vintage_year (year selector)
  - [x] management_fee_rate (percentage input)
  - [x] carried_interest_rate (percentage input)
  - [x] hurdle_rate (percentage input)

- [x] Implement validation
  - [x] Add min/max constraints for numeric inputs
  - [x] Create validation with Blueprint components
  - [x] Add real-time validation feedback

- [x] Add help text and tooltips
  - [x] Use Blueprint FormGroup helperText
  - [x] Add explanatory text for each field
  - [x] Include examples and constraints

- [x] Create visual feedback
  - [x] Style inputs with Blueprint components
  - [x] Add focus states for accessibility
  - [x] Implement error handling
  - [x] Create two-column Tailwind card layout

### 3.3 Step 2: Portfolio Strategy

- [x] Create zone weight sliders
  - [x] Implement interactive sliders for zone allocations
  - [x] Ensure allocations sum to 100%
  - [x] Add visual feedback for allocation balance
  - [x] Create color-coded zone indicators

- [x] Implement mean LTV slider
  - [x] Create slider with min/max from schema
  - [x] Add numeric input alongside slider
  - [x] Show distribution curve based on selected value

- [x] Add ticket size controls
  - [x] Create inputs for min/max/avg loan size
  - [x] Implement validation for ticket size constraints
  - [x] Add visual representation of ticket size distribution

- [x] Create guardrail pre-check chips
  - [x] Implement color-coded chips for guardrail status
  - [x] Add tooltips explaining guardrail constraints
  - [x] Update chips in real-time as values change

### 3.4 Step 3: Risk & Volatility

- [ ] Create editable σ and PD table
  - [ ] Implement table with rows for each zone
  - [ ] Add editable cells for volatility (σ) values
  - [ ] Add editable cells for probability of default (PD)
  - [ ] Implement validation for table values

- [ ] Add mini sparkline visualizations
  - [ ] Create visx line charts for each zone
  - [ ] Implement dynamic updates based on input values
  - [ ] Add tooltips explaining the visualizations
  - [ ] Create placeholder with dummy sin wave when no data

- [ ] Implement risk parameter controls
  - [ ] Add controls for correlation between zones
  - [ ] Create inputs for stress test parameters
  - [ ] Implement validation for risk parameters

- [ ] Add risk visualization
  - [ ] Create heat map for risk by zone
  - [ ] Implement risk distribution chart
  - [ ] Add color coding for risk levels

### 3.5 Step 4: Review & Run

- [ ] Create JSON diff panel
  - [ ] Show comparison between default and current config
  - [ ] Highlight changes with color coding
  - [ ] Add collapsible sections for different parameter categories
  - [ ] Implement syntax highlighting for JSON

- [ ] Add estimated runtime indicator
  - [ ] Show "est runtime: 40 s" placeholder
  - [ ] Create visual indicator for complexity
  - [ ] Add tooltip explaining runtime factors

- [ ] Create run button
  - [ ] Implement confirmation dialog
  - [ ] Add API call to start simulation:
    ```typescript
    const runSimulation = async (config) => {
      try {
        const response = await api.runSimulation({ config });
        navigate(`/runs/${response.id}`);
      } catch (error) {
        setError(error);
      }
    };
    ```
  - [ ] Handle success/error responses
  - [ ] Navigate to results page on success

- [ ] Add configuration saving
  - [ ] Create save dialog
  - [ ] Implement local storage saving
  - [ ] Add load from saved configuration option

## Phase 4: Simulation Results Page

### 4.1 Progress Tracking

- [ ] Implement WebSocket connection using AsyncAPI specification
  - [ ] Connect to simulation-specific WebSocket channel
  - [ ] Handle connection lifecycle (connect, disconnect, reconnect)
  - [ ] Process all message types defined in AsyncAPI spec:
    - [ ] progress: Update progress bar and status message
    - [ ] module_started: Display which module is currently running
    - [ ] module_completed: Update module status and execution time
    - [ ] intermediate_result: Display partial results as they become available
    - [ ] result: Handle final simulation results
    - [ ] error: Display error messages and handle recovery
    - [ ] guardrail_violation: Show guardrail violations with severity levels

- [ ] Create progress indicators
  - [ ] Implement overall progress bar with percentage
  - [ ] Add module-specific progress indicators
  - [ ] Display detailed status messages from backend
  - [ ] Create animated indicators for active modules

- [ ] Add cancellation capability
  - [ ] Create cancel button with confirmation dialog
  - [ ] Implement cancellation confirmation
  - [ ] Send cancellation request to backend API
  - [ ] Handle cancellation response and update UI
  - [ ] Show partial results if available after cancellation

- [ ] Implement error handling
  - [ ] Display error messages from backend with context
  - [ ] Add retry capability for recoverable errors
  - [ ] Provide troubleshooting information and next steps
  - [ ] Log detailed error information for debugging

### 4.2 Results Dashboard

- [x] Create tabbed interface
  - [x] Overview tab
  - [x] Cashflows tab
  - [x] Portfolio tab
  - [x] Risk tab

- [ ] Implement charts and visualizations
  - [ ] Create IRR and equity multiple charts
  - [ ] Implement cashflow waterfall chart
  - [ ] Add zone allocation visualization
  - [ ] Create risk metrics charts

- [ ] Add data tables
  - [ ] Implement sortable and filterable tables
  - [ ] Add pagination for large datasets
  - [ ] Create expandable rows for details

- [ ] Create export functionality
  - [ ] Add CSV export
  - [ ] Implement Excel export
  - [ ] Add PDF report generation

### 4.3 Detailed Analysis

- [ ] Implement drill-down capabilities
  - [ ] Create detail views for specific aspects
  - [ ] Add navigation between related data
  - [ ] Implement context-sensitive details

- [ ] Create comparison views
  - [ ] Add ability to select multiple simulations
  - [ ] Implement side-by-side comparison
  - [ ] Create difference highlighting

- [ ] Add filtering and sorting
  - [ ] Implement advanced filtering controls
  - [ ] Add multi-column sorting
  - [ ] Create saved filter presets

- [ ] Implement visualization controls
  - [ ] Add chart type selection
  - [ ] Create axis configuration options
  - [ ] Implement color scheme selection
  - [ ] Add data point highlighting

## Phase 5: Testing and Optimization

### 5.1 Unit Testing

- [ ] Set up testing framework
  - [ ] Configure Jest and React Testing Library
  - [ ] Set up test coverage reporting
  - [ ] Create test utilities and mocks

- [ ] Write component tests
  - [ ] Test layout components
  - [ ] Test form components
  - [ ] Test chart components
  - [ ] Test utility functions

- [ ] Test API integration
  - [ ] Mock API responses
  - [ ] Test error handling
  - [ ] Verify data transformation

- [ ] Test state management
  - [ ] Verify store actions
  - [ ] Test selectors
  - [ ] Ensure proper state updates

### 5.2 Integration Testing

- [ ] Test complete workflows
  - [ ] Test wizard flow end-to-end
  - [ ] Verify form validation
  - [ ] Test navigation between pages

- [ ] Test WebSocket integration
  - [ ] Verify connection handling
  - [ ] Test message processing
  - [ ] Ensure UI updates correctly

- [ ] Test error scenarios
  - [ ] Verify error boundary functionality
  - [ ] Test network error handling
  - [ ] Verify validation error display

### 5.3 Performance Optimization

- [ ] Analyze bundle size
  - [ ] Set up bundle analysis
  - [ ] Identify large dependencies
  - [ ] Implement code splitting

- [ ] Optimize rendering
  - [ ] Use React.memo for expensive components
  - [ ] Implement virtualization for large lists
  - [ ] Optimize chart rendering

- [ ] Improve load times
  - [ ] Add loading skeletons
  - [ ] Implement lazy loading
  - [ ] Optimize asset sizes

### 5.4 Accessibility and Usability

- [ ] Perform accessibility audit
  - [ ] Test with screen readers
  - [ ] Verify keyboard navigation
  - [ ] Check color contrast

- [ ] Improve usability
  - [ ] Add keyboard shortcuts
  - [ ] Implement responsive design
  - [ ] Test on different devices

- [ ] Add documentation
  - [ ] Create user guide
  - [ ] Add tooltips and help text
  - [ ] Implement onboarding flow

## Progress Tracking

| Phase | Total Tasks | Completed | Progress |
|-------|-------------|-----------|----------|
| Phase 1: Setup | 20 | 20 | 100% |
| Phase 2: Homepage | 15 | 15 | 100% |
| Phase 3: Wizard | 20 | 9 | 45% |
| Phase 4: Results | 15 | 1 | 7% |
| Phase 5: Testing | 12 | 0 | 0% |
| **Total** | **82** | **45** | **55%** |

## Technical Implementation Details

### Design System

The frontend will use a consistent design system with the following tokens:

| Token | Value | Usage |
|-------|-------|-------|
| --color-midnight | #0B1C3F | Header bar, dark hero bg |
| --color-steel | #314C7E | Card borders, axes |
| --color-aqua | #00A0B0 | Accent buttons, KPI ↑ |
| --color-ribbon-red | #D9395F | Guardrail FAIL |
| Radius | 4px | Buttons, cards |
| Spacing scale | 0.25rem increments | Tailwind default |

Fonts: Inter for body text, Roboto Mono for numeric KPI digits.

### API Integration Patterns

1. **Data Fetching with TanStack Query**
   ```typescript
   const { data, isLoading, error } = useQuery({
     queryKey: ['simulations'],
     queryFn: () => api.getSimulations({ limit: 10 }),
     refetchInterval: 60000, // Refetch every 60 seconds
   });
   ```

2. **WebSocket Integration with AsyncAPI**
   ```typescript
   // Using the WebSocketClient from the SDK (based on AsyncAPI spec)
   useEffect(() => {
     const wsClient = new WebSocketClient({
       baseUrl: 'ws://localhost:8000',
       apiKey: API_KEY,
       autoReconnect: true,
       maxReconnectAttempts: 5,
       reconnectDelay: 3000
     });

     wsClient.connect();
     wsClient.subscribe(simulationId);

     // Handle different message types as defined in AsyncAPI spec
     wsClient.on('progress', (data) => {
       setProgress(data.progress);
       setStatus(`${data.module}: ${data.message}`);
     });

     wsClient.on('module_started', (data) => {
       console.log(`Module started: ${data.module}`);
       updateStatus(`Running ${data.module}...`);
     });

     wsClient.on('module_completed', (data) => {
       console.log(`Module completed: ${data.module} in ${data.execution_time}s`);
     });

     wsClient.on('intermediate_result', (data) => {
       updateIntermediateResults(data.module, data.data);
     });

     wsClient.on('result', (data) => {
       setResults(data.result);
       setComplete(true);
     });

     wsClient.on('error', (data) => {
       setError(data.error);
     });

     wsClient.on('guardrail_violation', (data) => {
       addGuardrailViolation(data.violation);
     });

     return () => {
       wsClient.unsubscribe(simulationId);
       wsClient.disconnect();
     };
   }, [simulationId]);
   ```

3. **Form Validation with Zod**
   ```typescript
   const schema = z.object({
     fund_size: z.number().min(1000000),
     fund_term: z.number().int().min(1).max(30),
     vintage_year: z.number().int().min(1900).max(2100),
   });

   const { register, handleSubmit, formState: { errors } } = useForm({
     resolver: zodResolver(schema),
   });
   ```

### State Management with Zustand

```typescript
interface SimulationStore {
  config: SimulationConfig;
  results: SimulationResult | null;
  isRunning: boolean;
  progress: number;
  error: Error | null;
  setConfig: (config: Partial<SimulationConfig>) => void;
  resetConfig: () => void;
  setResults: (results: SimulationResult) => void;
  setProgress: (progress: number) => void;
  setError: (error: Error | null) => void;
  setRunning: (isRunning: boolean) => void;
}

const useSimulationStore = create<SimulationStore>((set) => ({
  config: DEFAULT_CONFIG,
  results: null,
  isRunning: false,
  progress: 0,
  error: null,
  setConfig: (config) => set((state) => ({ config: { ...state.config, ...config } })),
  resetConfig: () => set({ config: DEFAULT_CONFIG }),
  setResults: (results) => set({ results }),
  setProgress: (progress) => set({ progress }),
  setError: (error) => set({ error }),
  setRunning: (isRunning) => set({ isRunning }),
}));
```

### Component Architecture

Components should follow these principles:

1. **Single Responsibility**: Each component should do one thing well
2. **Composition Over Inheritance**: Build complex UIs by composing simple components
3. **Container/Presentational Pattern**: Separate data fetching from rendering
4. **Prop Drilling Avoidance**: Use context or state management for deeply nested data
5. **Consistent Naming**: Use clear, consistent naming conventions

Example component structure:
```typescript
// Presentational component
const MetricCard: React.FC<{
  title: string;
  value: number;
  format: string;
  trend?: number;
  trendDirection?: 'up' | 'down';
}> = ({ title, value, format, trend, trendDirection }) => {
  // Rendering logic only
};

// Container component
const MetricCardContainer: React.FC<{
  metricKey: keyof SimulationMetrics;
}> = ({ metricKey }) => {
  const metrics = useSimulationStore((state) => state.results?.metrics);
  const isLoading = useSimulationStore((state) => state.isRunning);

  if (isLoading) return <MetricCardSkeleton />;
  if (!metrics) return <MetricCardEmpty />;

  return (
    <MetricCard
      title={METRIC_LABELS[metricKey]}
      value={metrics[metricKey]}
      format={METRIC_FORMATS[metricKey]}
      trend={metrics[`${metricKey}_trend`]}
      trendDirection={metrics[`${metricKey}_trend`] > 0 ? 'up' : 'down'}
    />
  );
};
```

### Error Handling Strategy

1. **API Error Handling**
   - Use try/catch for async operations
   - Categorize errors (network, validation, server)
   - Display appropriate messages to users
   - Log detailed errors for debugging

2. **Form Validation Errors**
   - Show inline validation errors
   - Prevent form submission with invalid data
   - Provide clear guidance on how to fix errors

3. **Runtime Errors**
   - Use error boundaries to catch rendering errors
   - Implement fallback UI for error states
   - Provide retry mechanisms where appropriate

4. **WebSocket Errors**
   - Handle connection failures
   - Implement reconnection logic
   - Show connection status to users

### Performance Considerations

1. **Code Splitting**
   - Split code by route
   - Lazy load heavy components
   - Use dynamic imports for large dependencies

2. **Rendering Optimization**
   - Memoize expensive components
   - Use virtualization for long lists
   - Implement windowing for large tables

3. **Network Optimization**
   - Implement request batching
   - Use proper caching strategies
   - Optimize asset loading

4. **State Management**
   - Minimize state updates
   - Use selectors to prevent unnecessary rerenders
   - Structure state for efficient access patterns

## Implementation Timeline

### Week 1: Setup and Homepage

#### Days 1-2: Project Setup and SDK Integration
- Set up project structure and build tools
- Integrate TypeScript SDK
- Create base layout components
- Set up state management

#### Days 3-4: Homepage Implementation
- Create header and navigation
- Implement recent simulations table
- Add loading states and error handling
- Create empty state for no simulations

#### Day 5: Dashboard Metrics and Quick Actions
- Implement KPI ribbon
- Create chart components
- Add quick action buttons
- Test and refine homepage

### Week 2: Wizard Implementation

#### Days 1-2: Wizard Framework and Fund Basics
- Create wizard container and navigation
- Implement form state management
- Build Step 1 (Fund Basics) form
- Add validation and error handling

#### Days 3-4: Loan Parameters and Advanced Settings
- Implement Step 2 (Loan Parameters) form
- Create zone allocation controls
- Build Step 3 (Advanced Settings) with expandable sections
- Add parameter dependencies and validation

#### Day 5: Review, Run, and Testing
- Create Step 4 (Review and Run) screen
- Implement configuration saving
- Add API integration for starting simulations
- Test wizard flow end-to-end

### Week 3: Results Page and Refinement

#### Days 1-2: Progress Tracking and WebSocket Integration
- Implement WebSocket connection management
- Create progress indicators
- Add cancellation capability
- Handle error states

#### Days 3-4: Results Dashboard
- Create tabbed interface for results
- Implement charts and visualizations
- Add data tables for detailed exploration
- Create export functionality

#### Day 5: Detailed Analysis and Final Testing
- Implement drill-down capabilities
- Add filtering and sorting
- Create comparison views
- Test and refine the entire application

## Getting Started

### Prerequisites
- Node.js 16+ and npm/yarn
- Git
- Basic knowledge of React, TypeScript, and Tailwind CSS

### Setup Instructions
1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```
4. Copy the TypeScript SDK:
   ```bash
   cp -r ../sdk-output/typescript ./src/api
   ```
5. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```
6. Open your browser to http://localhost:5173

### Development Workflow
1. Create a new branch for your feature
2. Implement the feature following the guidelines in this document
3. Write tests for your code
4. Submit a pull request for review
5. Address any feedback and merge when approved

## Conclusion

This implementation plan provides a comprehensive roadmap for building the frontend for the EQU IHOME SIM ENGINE v2. By following this plan and adhering to the strict guidelines regarding data sources, validation, and SDK integration, we will create a robust, maintainable, and user-friendly application that meets all the requirements.

Remember the core principles:
- NO mock data, hardcoded values, or fallbacks
- Use schemas as the single source of truth
- Integrate properly with the TypeScript SDK
- Implement comprehensive validation and error handling
- Use WebSockets for real-time updates

By following this plan, we will deliver a high-quality frontend that provides a seamless user experience for configuring, running, and analyzing simulations.
