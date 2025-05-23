import React, { useState, useEffect } from 'react';
import { Tabs, Tab, Button, Intent, Card, Icon, Tag, Spinner } from '@blueprintjs/core';
import { useParams, useNavigate } from 'react-router-dom';
import { simulationApi } from '../../api/client';
import { SimulationResult } from '../../api/sdk/models';
import FundLPEconomics from './results/FundLPEconomics';
import GPEconomics from './results/GPEconomics';
import PortfolioZones from './results/PortfolioZones';
import Product from './results/Product';
import Advanced from './results/Advanced';

// Placeholder chart component
const PlaceholderChart: React.FC<{ title: string; height?: number }> = ({ title, height = 300 }) => (
  <div
    className="border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center bg-gray-50"
    style={{ height }}
  >
    <div className="text-center text-gray-500">
      <Icon icon="chart" size={48} className="mb-2" />
      <div className="font-medium">{title}</div>
      <div className="text-sm">Chart placeholder - will be implemented with visx</div>
    </div>
  </div>
);

// Placeholder table component
const PlaceholderTable: React.FC<{ title: string; rows?: number }> = ({ title, rows = 5 }) => (
  <div className="border border-gray-200 rounded-lg">
    <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
      <h4 className="font-medium text-gray-800">{title}</h4>
    </div>
    <div className="p-4">
      <div className="space-y-2">
        {Array.from({ length: rows }, (_, i) => (
          <div key={i} className="flex space-x-4 py-2 border-b border-gray-100 last:border-b-0">
            <div className="w-1/4 h-4 bg-gray-200 rounded animate-pulse"></div>
            <div className="w-1/4 h-4 bg-gray-200 rounded animate-pulse"></div>
            <div className="w-1/4 h-4 bg-gray-200 rounded animate-pulse"></div>
            <div className="w-1/4 h-4 bg-gray-200 rounded animate-pulse"></div>
          </div>
        ))}
      </div>
      <div className="text-center text-gray-500 mt-4">
        <Icon icon="th" size={24} className="mb-2" />
        <div className="text-sm">Data table placeholder - will show actual simulation results</div>
      </div>
    </div>
  </div>
);

const SimulationResults: React.FC = () => {
  const { simulationId } = useParams<{ simulationId: string }>();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('fund-lp-economics');
  const [simulationData, setSimulationData] = useState<SimulationResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch simulation results
  useEffect(() => {
    const fetchSimulationResults = async () => {
      if (!simulationId) return;

      try {
        setIsLoading(true);
        const result = await simulationApi.getSimulationSimulationsSimulationIdGet({
          simulationId
        });
        setSimulationData(result);
      } catch (err) {
        console.error('Failed to fetch simulation results:', err);
        setError('Failed to load simulation results');
      } finally {
        setIsLoading(false);
      }
    };

    fetchSimulationResults();
  }, [simulationId]);

  // Extract metrics from simulation data - NO FALLBACKS
  const metrics = simulationData?.results ? {
    irr: simulationData.results.irr,
    equity_multiple: simulationData.results.equity_multiple,
    total_return: simulationData.results.total_return,
    loan_count: simulationData.results.loan_count,
    avg_loan_size: simulationData.results.avg_loan_size,
    avg_ltv: simulationData.results.avg_ltv,
    default_rate: simulationData.results.default_rate,
    recovery_rate: simulationData.results.recovery_rate
  } : null;

  const formatPercentage = (value: number) => `${(value * 100).toFixed(1)}%`;
  const formatCurrency = (value: number) => `$${value.toLocaleString()}`;
  const formatNumber = (value: number) => value.toLocaleString();

  // Loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <Spinner size={50} />
          <div className="mt-4 text-lg font-medium">Loading simulation results...</div>
          <div className="text-gray-500">Fetching data for simulation {simulationId}</div>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <Card className="text-center p-8">
          <Icon icon="error" size={48} intent={Intent.DANGER} className="mb-4" />
          <h3 className="text-xl font-bold mb-2">Failed to Load Results</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <div className="space-x-2">
            <Button
              icon="refresh"
              text="Retry"
              onClick={() => window.location.reload()}
            />
            <Button
              icon="arrow-left"
              text="Back to Progress"
              onClick={() => navigate(`/runs/${simulationId}`)}
            />
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-display font-semibold text-neutral-900">
            Simulation Results
          </h1>
          <p className="text-neutral-500 mt-1">
            Simulation ID: {simulationId}
          </p>
        </div>
        <div className="flex space-x-2">
          <Button
            icon="download"
            text="Export Results"
            intent={Intent.PRIMARY}
            disabled
          />
          <Button
            icon="duplicate"
            text="Clone Simulation"
            disabled
          />
          <Button
            icon="arrow-left"
            text="Back to Progress"
            onClick={() => navigate(`/runs/${simulationId}`)}
          />
        </div>
      </div>

      {/* Status Banner */}
      <Card className="bg-green-50 border-green-200">
        <div className="flex items-center space-x-3">
          <Icon icon="tick-circle" intent={Intent.SUCCESS} size={24} />
          <div>
            <div className="font-semibold text-green-800">Simulation Completed Successfully</div>
            <div className="text-sm text-green-600">
              {simulationData?.completedAt ? (
                <>
                  Completed at {new Date(simulationData.completedAt).toLocaleString()}
                  {simulationData.startedAt && (
                    <> • Runtime: {Math.round((new Date(simulationData.completedAt).getTime() - new Date(simulationData.startedAt).getTime()) / 1000 / 60)}m</>
                  )}
                </>
              ) : (
                'Simulation completed'
              )}
            </div>
          </div>
        </div>
      </Card>

      {/* Key Metrics - Only show if data exists */}
      {metrics && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {metrics.irr !== undefined ? formatPercentage(metrics.irr) : 'N/A'}
            </div>
            <div className="text-sm text-gray-600">IRR</div>
          </Card>
          <Card className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {metrics.equity_multiple !== undefined ? `${metrics.equity_multiple.toFixed(2)}x` : 'N/A'}
            </div>
            <div className="text-sm text-gray-600">Equity Multiple</div>
          </Card>
          <Card className="text-center">
            <div className="text-2xl font-bold text-purple-600">
              {metrics.total_return !== undefined ? `${formatCurrency(metrics.total_return)}M` : 'N/A'}
            </div>
            <div className="text-sm text-gray-600">Total Return</div>
          </Card>
          <Card className="text-center">
            <div className="text-2xl font-bold text-orange-600">
              {metrics.loan_count !== undefined ? formatNumber(metrics.loan_count) : 'N/A'}
            </div>
            <div className="text-sm text-gray-600">Total Loans</div>
          </Card>
        </div>
      )}

      {/* No Data Message */}
      {!metrics && (
        <Card className="text-center p-8">
          <Icon icon="info-sign" size={48} intent={Intent.WARNING} className="mb-4" />
          <h3 className="text-xl font-bold mb-2">No Metrics Available</h3>
          <p className="text-gray-600">
            Simulation results do not contain performance metrics.
          </p>
        </Card>
      )}

      {/* Institutional-Grade Tabbed Results */}
      <Tabs
        id="results-tabs"
        selectedTabId={activeTab}
        onChange={(tabId) => setActiveTab(tabId as string)}
        renderActiveTabPanelOnly={true}
        className="institutional-results-tabs"
      >
        <Tab
          id="fund-lp-economics"
          title="Fund/LP Economics"
          panel={
            <div className="mt-6">
              <FundLPEconomics
                simulationData={simulationData}
                isLoading={isLoading}
                error={error}
              />
            </div>
          }
        />

        <Tab
          id="gp-economics"
          title="GP Economics"
          panel={
            <div className="mt-6">
              <GPEconomics
                simulationData={simulationData}
                isLoading={isLoading}
                error={error}
              />
            </div>
          }
        />

        <Tab
          id="portfolio-zones"
          title="Portfolio & Zones"
          panel={
            <div className="mt-6">
              <PortfolioZones
                simulationData={simulationData}
                isLoading={isLoading}
                error={error}
              />
            </div>
          }
        />

        <Tab
          id="product"
          title="Product"
          panel={
            <div className="mt-6">
              <Product
                simulationData={simulationData}
                isLoading={isLoading}
                error={error}
              />
            </div>
          }
        />

        <Tab
          id="advanced"
          title="Advanced"
          panel={
            <div className="mt-6">
              <Advanced
                simulationData={simulationData}
                isLoading={isLoading}
                error={error}
              />
            </div>
          }
        />
      </Tabs>
    </div>
  );
};

export default SimulationResults;
