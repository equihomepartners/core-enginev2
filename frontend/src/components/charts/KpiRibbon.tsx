import { Card, Elevation, Icon, Intent } from '@blueprintjs/core';

interface KpiItem {
  label: string;
  value: number | string;
  format?: string;
  trend?: number;
  trendDirection?: 'up' | 'down';
  description?: string;
}

interface KpiRibbonProps {
  items: KpiItem[];
  className?: string;
}

const KpiRibbon = ({ items, className = '' }: KpiRibbonProps) => {
  const formatValue = (value: number | string, format?: string): string => {
    if (typeof value === 'string') return value;
    
    switch (format) {
      case 'percent':
        return `${(value * 100).toFixed(2)}%`;
      case 'currency':
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        }).format(value);
      case 'number':
        return new Intl.NumberFormat('en-US').format(value);
      case 'decimal':
        return value.toFixed(2);
      default:
        return value.toString();
    }
  };
  
  const getTrendIntent = (direction?: 'up' | 'down'): Intent => {
    if (!direction) return Intent.NONE;
    return direction === 'up' ? Intent.SUCCESS : Intent.DANGER;
  };
  
  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 ${className}`}>
      {items.map((item, index) => (
        <Card key={index} elevation={Elevation.ONE} className="flex flex-col">
          <div className="text-sm text-gray-500 mb-1">{item.label}</div>
          <div className="flex items-end justify-between">
            <div className="text-2xl font-mono font-medium">
              {formatValue(item.value, item.format)}
            </div>
            {item.trend !== undefined && (
              <div className={`flex items-center text-sm ${
                item.trendDirection === 'up' ? 'text-green-600' : 'text-red-600'
              }`}>
                <Icon 
                  icon={item.trendDirection === 'up' ? 'trending-up' : 'trending-down'} 
                  intent={getTrendIntent(item.trendDirection)}
                  className="mr-1"
                />
                {formatValue(Math.abs(item.trend), item.format)}
              </div>
            )}
          </div>
          {item.description && (
            <div className="text-xs text-gray-500 mt-2">{item.description}</div>
          )}
        </Card>
      ))}
    </div>
  );
};

export default KpiRibbon;
