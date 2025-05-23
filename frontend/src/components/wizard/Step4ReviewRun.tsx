import React, { useState } from 'react';
import { Tabs, Tab, Button, Intent, Callout } from '@blueprintjs/core';
import { useNavigate } from 'react-router-dom';
import { useSimulationStore } from '../../store';
import { simulationApi } from '../../api/client';
import JsonDiffPanel from './review/JsonDiffPanel';
import RuntimeEstimator from './review/RuntimeEstimator';
import { toast } from '../../api/toast';

const Step4ReviewRun: React.FC = () => {
  const navigate = useNavigate();
  const { config, setIsLoading } = useSimulationStore();
  const [isRunning, setIsRunning] = useState(false);

  const handleRunSimulation = async () => {
    try {
      setIsRunning(true);
      setIsLoading(true);

      // Show confirmation toast
      await toast.info('Starting simulation...');

      // Create simulation via SDK
      const response = await simulationApi.createSimulationSimulationsPost({
        simulationRequest: {
          config: config
        }
      });

      // Navigate to progress page with real simulation ID
      navigate(`/runs/${response.simulationId}`);

      await toast.success('Simulation started successfully');

    } catch (error) {
      console.error('Failed to start simulation:', error);
      await toast.error('Failed to start simulation');
    } finally {
      setIsRunning(false);
      setIsLoading(false);
    }
  };

  const handleSaveConfiguration = async () => {
    // Save configuration to local storage or API
    const configJson = JSON.stringify(config, null, 2);
    const blob = new Blob([configJson], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `simulation-config-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    await toast.success('Configuration saved successfully');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">Review & Run Simulation</h2>
        <p className="text-gray-600">
          Review your configuration, check estimated runtime, and start the simulation.
        </p>
      </div>

      {/* Pre-flight Check */}
      <Callout intent="success" icon="tick-circle">
        <strong>Configuration Complete</strong>
        <br />
        Your simulation configuration is ready. Review the settings below and click "Run Simulation" to start.
      </Callout>

      {/* Tabbed Content */}
      <Tabs id="review-tabs" renderActiveTabPanelOnly={false}>
        <Tab
          id="configuration-diff"
          title="Configuration Changes"
          panel={
            <div className="mt-4">
              <JsonDiffPanel currentConfig={config} />
            </div>
          }
        />
        <Tab
          id="runtime-estimation"
          title="Runtime Estimation"
          panel={
            <div className="mt-4">
              <RuntimeEstimator config={config} />
            </div>
          }
        />
        <Tab
          id="final-summary"
          title="Final Summary"
          panel={
            <div className="mt-4 space-y-6">
              {/* Quick Summary Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                  <h4 className="font-semibold text-blue-900 mb-2">Fund Overview</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-blue-700">Size:</span>
                      <span className="font-medium">${(config.fund_size || 0).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-blue-700">Term:</span>
                      <span className="font-medium">{config.fund_term || 10} years</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-blue-700">Vintage:</span>
                      <span className="font-medium">{config.vintage_year || 2024}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                  <h4 className="font-semibold text-green-900 mb-2">Portfolio Strategy</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-green-700">Avg LTV:</span>
                      <span className="font-medium">{((config.avg_loan_ltv || 0.4) * 100).toFixed(0)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-green-700">Avg Loan:</span>
                      <span className="font-medium">${(config.avg_loan_size || 400000).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-green-700">Green Zone:</span>
                      <span className="font-medium">{((config.zone_allocations?.green || 0.6) * 100).toFixed(0)}%</span>
                    </div>
                  </div>
                </div>

                <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                  <h4 className="font-semibold text-purple-900 mb-2">Advanced Features</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-purple-700">Tranches:</span>
                      <span className="font-medium">
                        {config.tranche_manager?.enabled ?
                          `${config.tranche_manager?.tranches?.length || 0} tranches` :
                          'Single tranche'
                        }
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-purple-700">Leverage:</span>
                      <span className="font-medium">
                        {config.leverage_engine?.enabled ? 'Enabled' : 'Disabled'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-purple-700">Tax Analysis:</span>
                      <span className="font-medium">
                        {config.cashflow_aggregator?.enable_tax_impact_analysis ? 'Enabled' : 'Disabled'}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Configuration Actions */}
              <div className="bg-gray-50 p-4 rounded-lg">
                <h4 className="font-semibold mb-3">Configuration Actions</h4>
                <div className="flex flex-wrap gap-3">
                  <Button
                    icon="floppy-disk"
                    text="Save Configuration"
                    onClick={handleSaveConfiguration}
                    minimal
                  />
                  <Button
                    icon="duplicate"
                    text="Clone Configuration"
                    minimal
                    disabled
                  />
                  <Button
                    icon="share"
                    text="Export to Excel"
                    minimal
                    disabled
                  />
                </div>
              </div>

              {/* Ready to Run */}
              <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border border-green-200">
                <div className="text-center">
                  <h3 className="text-xl font-bold text-gray-800 mb-2">Ready to Run Simulation</h3>
                  <p className="text-gray-600 mb-4">
                    Your configuration is complete and validated. Click the button below to start the simulation.
                  </p>
                  <Button
                    intent="success"
                    large
                    icon="play"
                    text="Run Simulation"
                    onClick={handleRunSimulation}
                    loading={isRunning}
                    className="shadow-md"
                  />
                </div>
              </div>
            </div>
          }
        />
      </Tabs>

      {/* Help Information */}
      <div className="p-4 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Review & Run Information</h4>
        <p>Before running your simulation:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2">
          <li><strong>Configuration Changes:</strong> Review all modifications from default settings</li>
          <li><strong>Runtime Estimation:</strong> Check estimated execution time and complexity factors</li>
          <li><strong>Final Summary:</strong> Verify key parameters and save configuration if needed</li>
          <li><strong>Progress Tracking:</strong> Once started, you'll see real-time progress updates</li>
        </ul>
        <p className="mt-2 text-xs text-gray-600">
          The simulation will run in the background and you can monitor progress on the results page.
        </p>
      </div>
    </div>
  );
};

export default Step4ReviewRun;
