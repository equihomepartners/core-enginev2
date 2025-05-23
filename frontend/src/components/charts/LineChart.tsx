import { useMemo } from 'react';
import { Group } from '@visx/group';
import { scaleLinear, scaleTime } from '@visx/scale';
import { LinePath } from '@visx/shape';
import { AxisLeft, AxisBottom } from '@visx/axis';
import { GridRows, GridColumns } from '@visx/grid';
import { ParentSize } from '@visx/responsive';
import { extent, max, min } from 'd3-array';

interface DataPoint {
  x: Date | number;
  y: number;
}

interface LineChartProps {
  data: DataPoint[];
  width?: number;
  height?: number;
  margin?: { top: number; right: number; bottom: number; left: number };
  xAxisLabel?: string;
  yAxisLabel?: string;
  color?: string;
}

const LineChartInner = ({
  data,
  width = 500,
  height = 300,
  margin = { top: 20, right: 20, bottom: 40, left: 50 },
  xAxisLabel,
  yAxisLabel,
  color = '#00A0B0',
}: LineChartProps) => {
  // Bounds
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  // Scales
  const xScale = useMemo(() => {
    const domain = extent(data, d => d.x) as [Date | number, Date | number];
    return typeof data[0]?.x === 'number'
      ? scaleLinear({
          domain,
          range: [0, innerWidth],
        })
      : scaleTime({
          domain,
          range: [0, innerWidth],
        });
  }, [data, innerWidth]);
  
  const yScale = useMemo(() => {
    const minValue = min(data, d => d.y) || 0;
    const maxValue = max(data, d => d.y) || 0;
    const padding = (maxValue - minValue) * 0.1;
    
    return scaleLinear({
      domain: [minValue - padding, maxValue + padding],
      range: [innerHeight, 0],
      nice: true,
    });
  }, [data, innerHeight]);
  
  if (width < 10) return null;
  
  return (
    <svg width={width} height={height}>
      <Group left={margin.left} top={margin.top}>
        <GridRows
          scale={yScale}
          width={innerWidth}
          stroke="#e0e0e0"
          strokeOpacity={0.2}
          strokeDasharray="1,3"
        />
        <GridColumns
          scale={xScale}
          height={innerHeight}
          stroke="#e0e0e0"
          strokeOpacity={0.2}
          strokeDasharray="1,3"
        />
        <AxisLeft
          scale={yScale}
          label={yAxisLabel}
          labelProps={{
            fill: '#314C7E',
            textAnchor: 'middle',
            fontSize: 12,
            fontWeight: 'bold',
          }}
          stroke="#314C7E"
          tickStroke="#314C7E"
          tickLabelProps={() => ({
            fill: '#314C7E',
            textAnchor: 'end',
            fontSize: 10,
            dx: '-0.25em',
            dy: '0.25em',
          })}
        />
        <AxisBottom
          top={innerHeight}
          scale={xScale}
          label={xAxisLabel}
          labelProps={{
            fill: '#314C7E',
            textAnchor: 'middle',
            fontSize: 12,
            fontWeight: 'bold',
            dy: '2.5em',
          }}
          stroke="#314C7E"
          tickStroke="#314C7E"
          tickLabelProps={() => ({
            fill: '#314C7E',
            textAnchor: 'middle',
            fontSize: 10,
            dy: '0.75em',
          })}
        />
        <LinePath
          data={data}
          x={d => xScale(d.x) || 0}
          y={d => yScale(d.y) || 0}
          stroke={color}
          strokeWidth={2}
          curve="monotoneX"
        />
      </Group>
    </svg>
  );
};

// Wrap with ParentSize for responsiveness
const LineChart = (props: Omit<LineChartProps, 'width' | 'height'>) => {
  return (
    <ParentSize>
      {({ width, height }) => (
        <LineChartInner {...props} width={width} height={height} />
      )}
    </ParentSize>
  );
};

export default LineChart;
