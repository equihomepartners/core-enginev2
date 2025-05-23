import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { simulationApi } from './client';
import { SimulationRequest, SimulationResult, SimulationResponse } from './sdk/models';
import { toast } from './toast';

/**
 * Hook to fetch all simulations
 * @param options Query options
 * @returns Query result with simulations data
 */
export const useSimulations = (options?: { enabled?: boolean }) => {
  return useQuery({
    queryKey: ['simulations'],
    queryFn: async () => {
      return await simulationApi.listSimulationsSimulationsGet();
    },
    refetchInterval: 60000, // Refetch every 60 seconds
    enabled: options?.enabled !== false,
  });
};

/**
 * Hook to fetch a single simulation by ID
 * @param id Simulation ID
 * @param options Query options
 * @returns Query result with simulation data
 */
export const useSimulation = (id: string, options?: { enabled?: boolean }) => {
  return useQuery({
    queryKey: ['simulation', id],
    queryFn: async () => {
      return await simulationApi.getSimulationSimulationsSimulationIdGet({ simulationId: id });
    },
    enabled: !!id && options?.enabled !== false,
  });
};

/**
 * Hook to create a new simulation
 * @returns Mutation function and state
 */
export const useCreateSimulation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (config: object) => {
      const request: SimulationRequest = { config };
      return await simulationApi.createSimulationSimulationsPost({ simulationRequest: request });
    },
    onSuccess: (data) => {
      // Invalidate simulations query to refetch the list
      queryClient.invalidateQueries({ queryKey: ['simulations'] });
      toast.success('Simulation created successfully');
      return data;
    },
    onError: (error: any) => {
      console.error('Error creating simulation:', error);
      // Error handling is done in the API client middleware
    },
  });
};

/**
 * Hook to delete a simulation
 * @returns Mutation function and state
 */
export const useDeleteSimulation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      return await simulationApi.deleteSimulationSimulationsSimulationIdDelete({ simulationId: id });
    },
    onSuccess: (_, variables) => {
      // Invalidate simulations query to refetch the list
      queryClient.invalidateQueries({ queryKey: ['simulations'] });
      // Remove the deleted simulation from the cache
      queryClient.removeQueries({ queryKey: ['simulation', variables] });
      toast.success('Simulation deleted successfully');
    },
    onError: (error: any) => {
      console.error('Error deleting simulation:', error);
      // Error handling is done in the API client middleware
    },
  });
};
