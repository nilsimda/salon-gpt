'use client';

import React from 'react';

import { AgentPublic, ManagedTool } from '@/cohere-client';
import { DataSourceMenu, FilesMenu } from '@/components/Composer';
import { cn } from '@/utils';

type Props = {
  agent?: AgentPublic;
  tools?: ManagedTool[];
  onUploadFile: (files: File[]) => void;
};

/**
 * @description Renders the bottom toolbar of the composer that shows available and selected data sources.
 */
export const ComposerToolbar: React.FC<Props> = ({ agent, tools, onUploadFile }) => {
  return (
    <div
      className={cn(
        'flex items-center gap-x-2',
        'border-t border-marble-950 dark:border-volcanic-300',
        'mx-2 py-2'
      )}
    >
      <FilesMenu onUploadFile={onUploadFile} />
      <DataSourceMenu agent={agent} />
    </div>
  );
};
