import { ReactNode } from 'react';
import { Card as BlueprintCard, H5, Elevation, Icon, IconName } from '@blueprintjs/core';

interface CardProps {
  title?: string;
  subtitle?: string;
  icon?: IconName;
  children: ReactNode;
  className?: string;
  elevation?: Elevation;
  headerActions?: ReactNode;
  noPadding?: boolean;
}

const Card = ({
  title,
  subtitle,
  icon,
  children,
  className = '',
  elevation = Elevation.TWO,
  headerActions,
  noPadding = false
}: CardProps) => {
  return (
    <BlueprintCard
      elevation={elevation}
      className={`overflow-hidden border border-neutral-200 ${noPadding ? 'p-0' : ''} ${className}`}
    >
      {(title || headerActions) && (
        <div className={`flex justify-between items-center ${!noPadding ? 'mb-4' : 'px-6 py-4 border-b border-neutral-200'}`}>
          <div className="flex items-center">
            {icon && (
              <div className="mr-3 p-2 rounded-full bg-primary bg-opacity-10">
                <Icon icon={icon} size={16} className="text-primary" />
              </div>
            )}
            <div>
              {title && <H5 className={`m-0 font-display text-neutral-900 ${subtitle ? 'mb-0.5' : ''}`}>{title}</H5>}
              {subtitle && <div className="text-sm text-neutral-500">{subtitle}</div>}
            </div>
          </div>
          {headerActions && (
            <div className="flex items-center">
              {headerActions}
            </div>
          )}
        </div>
      )}
      <div className={noPadding ? '' : 'px-0'}>{children}</div>
    </BlueprintCard>
  );
};

export default Card;
