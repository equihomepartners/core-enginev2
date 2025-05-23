import { Button, NonIdealState, Icon, Tag, Callout } from '@blueprintjs/core';
import { useNavigate } from 'react-router-dom';
import Card from '../components/layout/Card';
import { useSimulationStore } from '../store';
import { EQUIHOME_100M_FUND_PRESET } from '../utils/presets';
import { formatCurrency } from '../utils/formatters';

const Home = () => {
  const navigate = useNavigate();
  const { setConfig } = useSimulationStore();

  const handleLoadPreset = () => {
    // Load the comprehensive 100M fund preset
    setConfig(EQUIHOME_100M_FUND_PRESET.config);

    // Navigate directly to Review & Run page (step 4)
    navigate('/wizard?step=4');
  };

  // This is a placeholder. In the real implementation, we'll fetch data from the API
  const hasSimulations = false;

  // Sample metrics data (will be replaced with real data from API)
  const metrics = [
    { id: 1, title: 'Total Simulations', value: '0', icon: 'chart', trend: null },
    { id: 2, title: 'Avg. IRR', value: '0%', icon: 'trending-up', trend: null },
    { id: 3, title: 'Avg. Loan Size', value: '$0', icon: 'dollar', trend: null },
    { id: 4, title: 'Avg. LTV', value: '0%', icon: 'percentage', trend: null },
  ];

  return (
    <div className="space-y-8">
      {/* Page header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-display font-semibold text-neutral-900">Dashboard</h1>
          <p className="text-neutral-500 mt-1">Welcome to Equihome Simulation Engine</p>
        </div>
        <Button
          intent="primary"
          icon="play"
          text="Run New Simulation"
          large={true}
          className="shadow-md"
          onClick={() => navigate('/wizard')}
        />
      </div>

      {/* Metrics section */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map(metric => (
          <Card key={metric.id} className="metric-card">
            <div className="flex items-start justify-between">
              <div>
                <div className="text-sm font-medium text-neutral-500 mb-1">{metric.title}</div>
                <div className="text-2xl font-semibold text-neutral-900">{metric.value}</div>
                {metric.trend && (
                  <div className={metric.trend > 0 ? 'metric-trend-up' : 'metric-trend-down'}>
                    <Icon icon={metric.trend > 0 ? 'arrow-up' : 'arrow-down'} size={12} className="mr-1" />
                    <span>{Math.abs(metric.trend)}%</span>
                  </div>
                )}
              </div>
              <div className="p-2 rounded-full bg-primary bg-opacity-10">
                <Icon icon={metric.icon} size={20} className="text-primary" />
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Quick Start Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Quick Start Preset Card */}
        <Card
          title="🚀 Quick Start: 100M Fund"
          icon="flash"
          subtitle="Jump directly to simulation with a comprehensive preset"
        >
          <div className="space-y-4">
            <Callout intent="success" icon="info-sign">
              <strong>Comprehensive Configuration</strong>
              <br />
              Pre-configured with institutional-grade settings using the entire schema
            </Callout>

            <div className="bg-blue-50 p-3 rounded-md text-sm">
              <h4 className="font-semibold mb-2">Preset Highlights</h4>
              <ul className="space-y-1 text-xs">
                <li>• <strong>Fund Size:</strong> {formatCurrency(EQUIHOME_100M_FUND_PRESET.config.fund_size)}</li>
                <li>• <strong>LTV Range:</strong> 15% - 65% (40% avg), Pro-rata LTV appreciation share</li>
                <li>• <strong>Loan Terms:</strong> 10-year avg term, 5% interest, 3% origination fee</li>
                <li>• <strong>Multi-Tranche:</strong> Senior Debt (60%), Mezzanine (25%), Equity (15%)</li>
                <li>• <strong>Management Fee:</strong> 2% for entire 10-year fund term</li>
                <li>• <strong>Exit Strategy:</strong> 2.5-year avg exit with 18-month std dev</li>
              </ul>
            </div>

            <div className="flex flex-wrap gap-2">
              <Tag intent="success" minimal>Multi-Tranche</Tag>
              <Tag intent="primary" minimal>Leverage</Tag>
              <Tag intent="warning" minimal>Risk Analysis</Tag>
              <Tag minimal>Scenarios</Tag>
            </div>

            <Button
              intent="success"
              large
              fill
              icon="fast-forward"
              onClick={handleLoadPreset}
            >
              Load Preset & Review
            </Button>
          </div>
        </Card>

        {/* New Simulation Card */}
        <Card
          title="New Simulation"
          icon="plus"
          subtitle="Create a new fund simulation from scratch"
        >
          <div className="space-y-4">
            <p className="text-gray-600">
              Configure your fund parameters, portfolio strategy, and risk settings
              to run a comprehensive simulation step by step.
            </p>

            <div className="bg-gray-50 p-3 rounded-md text-sm">
              <h4 className="font-semibold mb-2">Wizard Steps</h4>
              <ul className="space-y-1 text-xs">
                <li>• <strong>Step 1:</strong> Fund Basics & Capital Structure</li>
                <li>• <strong>Step 2:</strong> Portfolio Strategy & Allocations</li>
                <li>• <strong>Step 3:</strong> Risk & Volatility Settings</li>
                <li>• <strong>Step 4:</strong> Review & Run Simulation</li>
              </ul>
            </div>

            <div className="flex flex-wrap gap-2">
              <Tag minimal>Fund Setup</Tag>
              <Tag minimal>Portfolio Strategy</Tag>
              <Tag minimal>Risk Analysis</Tag>
              <Tag minimal>Step-by-Step</Tag>
            </div>

            <Button
              intent="primary"
              large
              fill
              icon="arrow-right"
              onClick={() => navigate('/wizard')}
            >
              Start New Simulation
            </Button>
          </div>
        </Card>
      </div>

      {/* Recent simulations */}
      <Card
        title="Recent Simulations"
        subtitle="View and manage your simulation runs"
        icon="history"
        className="mt-4"
        headerActions={
          <Button
            minimal={true}
            small={true}
            icon="refresh"
            text="Refresh"
          />
        }
      >
        {hasSimulations ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-neutral-200">
              <thead>
                <tr>
                  <th className="px-6 py-3 bg-neutral-50 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">ID</th>
                  <th className="px-6 py-3 bg-neutral-50 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Name</th>
                  <th className="px-6 py-3 bg-neutral-50 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 bg-neutral-50 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Created</th>
                  <th className="px-6 py-3 bg-neutral-50 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-neutral-200">
                {/* Table rows will go here */}
              </tbody>
            </table>
          </div>
        ) : (
          <NonIdealState
            icon="history"
            title="No simulations yet"
            description="Run your first simulation to see results here."
            action={
              <Button
                intent="primary"
                text="Run New Simulation"
                onClick={() => navigate('/wizard')}
              />
            }
          />
        )}
      </Card>

      {/* Quick links */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card
          title="Documentation"
          icon="manual"
          className="hover:shadow-lg transition-shadow cursor-pointer"
          onClick={() => navigate('/docs')}
        >
          <p className="text-neutral-600 mb-4">Learn how to use the simulation engine and understand the results.</p>
          <Button minimal={true} icon="arrow-right" text="View Documentation" />
        </Card>

        <Card
          title="API Reference"
          icon="code"
          className="hover:shadow-lg transition-shadow cursor-pointer"
          onClick={() => navigate('/docs/api')}
        >
          <p className="text-neutral-600 mb-4">Explore the API endpoints and integrate with your applications.</p>
          <Button minimal={true} icon="arrow-right" text="View API Reference" />
        </Card>

        <Card
          title="Support"
          icon="help"
          className="hover:shadow-lg transition-shadow cursor-pointer"
          onClick={() => window.open('mailto:support@equihome.com')}
        >
          <p className="text-neutral-600 mb-4">Need help? Contact our support team for assistance.</p>
          <Button minimal={true} icon="arrow-right" text="Contact Support" />
        </Card>
      </div>
    </div>
  );
};

export default Home;
