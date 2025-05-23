import React from 'react';
import { Group } from '@visx/group';
import { LinePath } from '@visx/shape';
import { scaleLinear } from '@visx/scale';
import { curveCardinal } from '@visx/curve';
import Card from '../../layout/Card';

interface RiskSparklinesProps {
  riskMetrics: {
    appreciation_rates: {
      green: number;
      orange: number;
      red: number;
    };
    default_rates: {
      green: number;
      orange: number;
      red: number;
    };
    variation_factors: {
      property_value_volatility: number;
      default_rate_volatility: number;
    };
  };
}

const RiskSparklines: React.FC<RiskSparklinesProps> = ({ riskMetrics }) => {
  const width = 120;
  const height = 40;
  const margin = { top: 5, right: 5, bottom: 5, left: 5 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Generate sample data points for sparklines based on risk parameters
  const generateSparklineData = (baseValue: number, volatility: number, trend: number = 0) => {
    const points = 20;
    const data = [];
    
    for (let i = 0; i < points; i++) {
      const time = i / (points - 1);
      const noise = (Math.sin(i * 0.5) + Math.sin(i * 0.3) * 0.5) * volatility;
      const trendComponent = trend * time;
      const value = baseValue + noise + trendComponent;
      data.push({ x: i, y: Math.max(0, value) });
    }
    
    return data;
  };

  // Generate data for each zone
  const greenAppreciationData = generateSparklineData(
    riskMetrics.appreciation_rates.green,
    riskMetrics.variation_factors.property_value_volatility * 0.5,
    0.01
  );
  
  const orangeAppreciationData = generateSparklineData(
    riskMetrics.appreciation_rates.orange,
    riskMetrics.variation_factors.property_value_volatility * 0.7,
    0.005
  );
  
  const redAppreciationData = generateSparklineData(
    riskMetrics.appreciation_rates.red,
    riskMetrics.variation_factors.property_value_volatility * 0.9,
    0
  );

  const greenDefaultData = generateSparklineData(
    riskMetrics.default_rates.green,
    riskMetrics.variation_factors.default_rate_volatility * 0.3,
    0
  );
  
  const orangeDefaultData = generateSparklineData(
    riskMetrics.default_rates.orange,
    riskMetrics.variation_factors.default_rate_volatility * 0.5,
    0.002
  );
  
  const redDefaultData = generateSparklineData(
    riskMetrics.default_rates.red,
    riskMetrics.variation_factors.default_rate_volatility * 0.7,
    0.005
  );

  const Sparkline: React.FC<{
    data: Array<{ x: number; y: number }>;
    color: string;
    title: string;
  }> = ({ data, color, title }) => {
    const xScale = scaleLinear({
      domain: [0, data.length - 1],
      range: [0, innerWidth],
    });

    const yScale = scaleLinear({
      domain: [Math.min(...data.map(d => d.y)), Math.max(...data.map(d => d.y))],
      range: [innerHeight, 0],
    });

    return (
      <div className="text-center">
        <div className="text-xs font-medium text-gray-600 mb-1">{title}</div>
        <svg width={width} height={height} className="border border-gray-200 rounded">
          <Group left={margin.left} top={margin.top}>
            <LinePath
              data={data}
              x={d => xScale(d.x)}
              y={d => yScale(d.y)}
              stroke={color}
              strokeWidth={1.5}
              curve={curveCardinal}
            />
            {/* Add dots for data points */}
            {data.map((d, i) => (
              <circle
                key={i}
                cx={xScale(d.x)}
                cy={yScale(d.y)}
                r={1}
                fill={color}
                opacity={0.6}
              />
            ))}
          </Group>
        </svg>
        <div className="text-xs text-gray-500 mt-1">
          Current: {(data[data.length - 1].y * 100).toFixed(1)}%
        </div>
      </div>
    );
  };

  return (
    <Card
      title="Risk Trend Visualizations"
      icon="timeline-line-chart"
      subtitle="Historical trends and projections for risk parameters"
    >
      <div className="space-y-6">
        {/* Appreciation Rate Trends */}
        <div>
          <h4 className="text-sm font-semibold mb-3 text-gray-700">Appreciation Rate Trends</h4>
          <div className="grid grid-cols-3 gap-4">
            <Sparkline
              data={greenAppreciationData}
              color="#10B981"
              title="Green Zone"
            />
            <Sparkline
              data={orangeAppreciationData}
              color="#F59E0B"
              title="Orange Zone"
            />
            <Sparkline
              data={redAppreciationData}
              color="#EF4444"
              title="Red Zone"
            />
          </div>
        </div>

        {/* Default Rate Trends */}
        <div>
          <h4 className="text-sm font-semibold mb-3 text-gray-700">Default Rate Trends</h4>
          <div className="grid grid-cols-3 gap-4">
            <Sparkline
              data={greenDefaultData}
              color="#10B981"
              title="Green Zone"
            />
            <Sparkline
              data={orangeDefaultData}
              color="#F59E0B"
              title="Orange Zone"
            />
            <Sparkline
              data={redDefaultData}
              color="#EF4444"
              title="Red Zone"
            />
          </div>
        </div>

        {/* Risk Insights */}
        <div className="bg-gray-50 p-4 rounded-md">
          <h5 className="font-medium mb-2 text-sm">Risk Trend Insights</h5>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <div className="font-medium text-gray-700">Appreciation Outlook</div>
              <ul className="list-disc pl-4 space-y-1 text-gray-600">
                <li>Green zone showing steady growth trend</li>
                <li>Orange zone with moderate volatility</li>
                <li>Red zone experiencing higher uncertainty</li>
              </ul>
            </div>
            <div>
              <div className="font-medium text-gray-700">Default Risk Assessment</div>
              <ul className="list-disc pl-4 space-y-1 text-gray-600">
                <li>Green zone maintains low default rates</li>
                <li>Orange zone showing slight increase</li>
                <li>Red zone requires close monitoring</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Volatility Indicators */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-blue-50 p-3 rounded-md text-center">
            <div className="text-lg font-bold text-blue-600">
              {(riskMetrics.variation_factors.property_value_volatility * 100).toFixed(1)}%
            </div>
            <div className="text-xs text-blue-700">Property Value Volatility</div>
          </div>
          <div className="bg-red-50 p-3 rounded-md text-center">
            <div className="text-lg font-bold text-red-600">
              {(riskMetrics.variation_factors.default_rate_volatility * 100).toFixed(1)}%
            </div>
            <div className="text-xs text-red-700">Default Rate Volatility</div>
          </div>
        </div>
      </div>

      {/* Help Information */}
      <div className="mt-4 p-3 bg-gray-100 rounded-md text-sm">
        <h4 className="font-semibold mb-2">Sparkline Information</h4>
        <p>These mini charts show simulated historical trends and projections based on your risk parameters:</p>
        <ul className="list-disc pl-5 space-y-1 mt-2 text-xs">
          <li><strong>Appreciation Trends:</strong> Show expected property value growth patterns by zone</li>
          <li><strong>Default Trends:</strong> Display probability of default evolution over time</li>
          <li><strong>Volatility Impact:</strong> Higher volatility settings create more variable trend lines</li>
          <li><strong>Zone Comparison:</strong> Compare risk profiles across different geographic zones</li>
        </ul>
      </div>
    </Card>
  );
};

export default RiskSparklines;
