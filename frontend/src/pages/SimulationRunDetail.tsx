import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Button, Intent, Callout } from '@blueprintjs/core';
import SimulationProgress from '../components/simulation/SimulationProgress';
import SimulationResults from '../components/simulation/SimulationResults';

const SimulationRunDetail: React.FC = () => {
  const { simulationId } = useParams<{ simulationId: string }>();
  const [simulationStatus, setSimulationStatus] = useState<'running' | 'completed' | 'error' | 'cancelled'>('running');
  const [showResults, setShowResults] = useState(false);

  // Simulate status changes for demonstration
  useEffect(() => {
    if (!simulationId) return;

    // Simulate completion after some time
    const timer = setTimeout(() => {
      setSimulationStatus('completed');
    }, 15000); // 15 seconds for demo

    return () => clearTimeout(timer);
  }, [simulationId]);

  if (!simulationId) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <Callout intent={Intent.DANGER} icon="error">
          <h4>Invalid Simulation</h4>
          <p>No simulation ID provided.</p>
        </Callout>
      </div>
    );
  }

  // Show results if completed and user wants to see them
  if (simulationStatus === 'completed' && showResults) {
    return <SimulationResults />;
  }

  return (
    <div className="space-y-6">
      {/* Status-specific callouts */}
      {simulationStatus === 'completed' && !showResults && (
        <Callout intent={Intent.SUCCESS} icon="tick-circle">
          <div className="flex justify-between items-center">
            <div>
              <h4>Simulation Completed</h4>
              <p>Your simulation has finished successfully. View the detailed results below.</p>
            </div>
            <Button
              intent={Intent.SUCCESS}
              icon="chart"
              text="View Results"
              onClick={() => setShowResults(true)}
            />
          </div>
        </Callout>
      )}

      {simulationStatus === 'error' && (
        <Callout intent={Intent.DANGER} icon="error">
          <h4>Simulation Failed</h4>
          <p>An error occurred during simulation execution. Please check the logs below for details.</p>
        </Callout>
      )}

      {simulationStatus === 'cancelled' && (
        <Callout intent={Intent.WARNING} icon="warning-sign">
          <h4>Simulation Cancelled</h4>
          <p>The simulation was cancelled by user request.</p>
        </Callout>
      )}

      {/* Progress Component */}
      <SimulationProgress simulationId={simulationId} />
    </div>
  );
};

export default SimulationRunDetail;
