import { Configuration } from './sdk/runtime';
import {
  SimulationApi,
  TlsApi,
  RiskApi,
  PortfolioApi,
  FinanceApi,
  PricePathApi,
  GuardrailApi,
  PerformanceApi
} from './sdk/apis';
import { toast } from './toast';

// API configuration
const getConfig = () => {
  const apiKey = import.meta.env.VITE_API_KEY || localStorage.getItem('api_key');

  return new Configuration({
    basePath: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
    apiKey: apiKey ? async () => apiKey : undefined,
    middleware: [
      {
        pre: async (context: any) => {
          // Add request timestamp for debugging
          context.init.headers = {
            ...context.init.headers,
            'X-Request-Time': new Date().toISOString(),
          };
          return context;
        },
        post: async (context: any) => {
          // Log successful responses if needed
          return context;
        },
        onError: async (context: any) => {
          // Handle and log errors
          const { error } = context;

          console.error('API Error:', error);

          // Show user-friendly error message
          if (error.response) {
            const status = error.response.status;

            if (status === 401) {
              toast.error('Authentication failed. Please log in again.');
              localStorage.removeItem('api_key');
              // Redirect to login if needed
            } else if (status === 403) {
              toast.error('You do not have permission to perform this action.');
            } else if (status === 404) {
              toast.error('The requested resource was not found.');
            } else if (status >= 500) {
              toast.error('A server error occurred. Please try again later.');
            } else {
              try {
                const data = await error.response.json();
                if (data.detail) {
                  toast.error(data.detail);
                } else {
                  toast.error('An error occurred. Please try again.');
                }
              } catch (e) {
                toast.error('An error occurred. Please try again.');
              }
            }
          } else if (error.request) {
            toast.error('Network error. Please check your connection.');
          } else {
            toast.error('An unexpected error occurred.');
          }

          return context;
        }
      }
    ]
  });
};

// API client instances
export const simulationApi = new SimulationApi(getConfig());
export const tlsApi = new TlsApi(getConfig());
export const riskApi = new RiskApi(getConfig());
export const portfolioApi = new PortfolioApi(getConfig());
export const financeApi = new FinanceApi(getConfig());
export const pricePathApi = new PricePathApi(getConfig());
export const guardrailApi = new GuardrailApi(getConfig());
export const performanceApi = new PerformanceApi(getConfig());

// Re-export WebSocket client
export { WebSocketClient } from './sdk/websocket/client';
