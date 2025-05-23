import React from 'react';
import { Button, NonIdealState, Spinner, Tag, Intent } from '@blueprintjs/core';
import { useNavigate } from 'react-router-dom';
import Card from '../components/layout/Card';
import { useSimulationStore } from '../store';
import { formatDate } from '../utils/formatters';

const RunsList: React.FC = () => {
  const navigate = useNavigate();
  const { pastSimulations, isLoading } = useSimulationStore();
  
  // Function to get status tag
  const getStatusTag = (status: string) => {
    switch (status) {
      case 'running':
        return <Tag intent={Intent.PRIMARY} icon="refresh" minimal>Running</Tag>;
      case 'completed':
        return <Tag intent={Intent.SUCCESS} icon="tick" minimal>Completed</Tag>;
      case 'failed':
        return <Tag intent={Intent.DANGER} icon="error" minimal>Failed</Tag>;
      default:
        return <Tag intent={Intent.NONE} minimal>{status}</Tag>;
    }
  };
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-display font-semibold text-neutral-900">Simulations</h1>
          <p className="text-neutral-500 mt-1">View and manage your simulation runs</p>
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
      
      {/* Simulations list */}
      <Card 
        title="Recent Simulations" 
        icon="history"
        headerActions={
          <Button 
            minimal={true} 
            small={true}
            icon="refresh" 
            text="Refresh" 
          />
        }
      >
        {isLoading ? (
          <div className="flex justify-center items-center py-12">
            <Spinner />
          </div>
        ) : pastSimulations.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-neutral-200">
              <thead>
                <tr>
                  <th className="px-6 py-3 bg-neutral-50 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">ID</th>
                  <th className="px-6 py-3 bg-neutral-50 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Fund Name</th>
                  <th className="px-6 py-3 bg-neutral-50 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 bg-neutral-50 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Created</th>
                  <th className="px-6 py-3 bg-neutral-50 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-neutral-200">
                {pastSimulations.map((simulation) => (
                  <tr key={simulation.id} className="hover:bg-neutral-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900">
                      {simulation.id.substring(0, 8)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-700">
                      {simulation.config.fund_name || 'Unnamed Fund'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      {getStatusTag(simulation.status)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500">
                      {formatDate(simulation.startTime)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-500">
                      <Button
                        minimal={true}
                        small={true}
                        icon="eye-open"
                        text="View"
                        onClick={() => navigate(`/runs/${simulation.id}`)}
                      />
                    </td>
                  </tr>
                ))}
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
    </div>
  );
};

export default RunsList;
