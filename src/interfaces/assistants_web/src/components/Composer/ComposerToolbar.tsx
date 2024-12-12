'use client';

import React from 'react';

import { DataSourceMenu } from '@/components/Composer';
import { Study } from '@/salon-client';
import { cn } from '@/utils';

type Props = {
  agentName?: string;
  study?: Study;
};

/**
 * @description Renders the bottom toolbar of the composer that shows available and selected data sources.
 */
export const ComposerToolbar: React.FC<Props> = ({ agentName, study }) => {
  return (
    <div
      className={cn(
        'flex items-center gap-x-2',
        'border-t border-marble-950 dark:border-volcanic-300',
        'mx-2 py-2'
      )}
    >
      <DataSourceMenu agentName={agentName} />
    </div>
  );
};
