'use client';

import { Textarea } from '@/components/UI';
import { Select } from '@headlessui/react'

import { useParamsStore } from '@/stores';
import React from 'react';

type Props = {
  agentId?: string;
};

export const ConversationPanel: React.FC<Props> = ({ agentId }) => {
  const {
    setParams,
    params: { description },
  } = useParamsStore();

  const handleDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setParams({ description: e.target.value });
  }

  return (
    <aside className="flex flex-col space-y-5 overflow-y-auto py-4">
      {agentId === 'kerlin' &&
        <Textarea label="Beschreibung" defaultRows={5} value={description || ' '} onChange={handleDescriptionChange} />
      }
      {agentId === 'zitatki' &&
        <p>Coming Soon... </p>
      }
      {agentId === 'transcription' &&
        <Select name="status" className="border data-[hover]:shadow data-[focus]:bg-blue-100" aria-label="Project status">
          <option value="active">Active</option>
          <option value="paused">Paused</option>
          <option value="delayed">Delayed</option>
          <option value="canceled">Canceled</option>
        </Select>
      }
    </aside>
  );
};
