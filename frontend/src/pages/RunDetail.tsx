import { useParams } from 'react-router-dom';
import { Button, Card, Elevation, Tabs, Tab } from '@blueprintjs/core';
import { useNavigate } from 'react-router-dom';

const RunDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Simulation Results</h1>
        <div className="space-x-4">
          <Button 
            icon="duplicate" 
            text="Clone & Edit" 
            onClick={() => navigate('/wizard')} 
          />
          <Button 
            intent="primary" 
            icon="play" 
            text="Run New Simulation" 
            onClick={() => navigate('/wizard')} 
          />
        </div>
      </div>
      
      <Card elevation={Elevation.TWO} className="mb-6">
        <div className="p-4">
          <h2 className="text-lg font-semibold mb-2">Simulation ID: {id}</h2>
          <div className="grid grid-cols-4 gap-4">
            <div>
              <div className="text-sm text-gray-500">Status</div>
              <div className="font-medium">Completed</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Created</div>
              <div className="font-medium">2023-11-15 10:30 AM</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Duration</div>
              <div className="font-medium">45 seconds</div>
            </div>
            <div>
              <div className="text-sm text-gray-500">Fund Size</div>
              <div className="font-medium">$10,000,000</div>
            </div>
          </div>
        </div>
      </Card>
      
      <Tabs id="resultTabs" renderActiveTabPanelOnly>
        <Tab 
          id="overview" 
          title="Overview" 
          panel={
            <Card elevation={Elevation.TWO} className="p-4">
              <p>Overview content will go here</p>
            </Card>
          } 
        />
        <Tab 
          id="cashflows" 
          title="Cashflows" 
          panel={
            <Card elevation={Elevation.TWO} className="p-4">
              <p>Cashflows content will go here</p>
            </Card>
          } 
        />
        <Tab 
          id="portfolio" 
          title="Portfolio" 
          panel={
            <Card elevation={Elevation.TWO} className="p-4">
              <p>Portfolio content will go here</p>
            </Card>
          } 
        />
        <Tab 
          id="risk" 
          title="Risk" 
          panel={
            <Card elevation={Elevation.TWO} className="p-4">
              <p>Risk content will go here</p>
            </Card>
          } 
        />
      </Tabs>
    </div>
  );
};

export default RunDetail;
