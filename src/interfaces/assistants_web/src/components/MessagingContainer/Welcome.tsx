'use client';

import { Transition } from '@headlessui/react';
import React from 'react';

import { Icon, Text } from '@/components/UI';
import { useBrandedColors } from '@/hooks';
import { cn } from '@/utils';

import { AgentLogo } from '../Agents/AgentLogo';

const getDescription = (agentId?: string): string => {
  switch (agentId) {
    case 'zitatki':
      return 'Finde Zitate aus Studien';
    case 'kerlin':
      return 'Befrage einen synthetischen Nutzer';
    case 'transcription':
      return 'Transkribiere Interviews';
    default:
      return '';
  }
};

type Props = {
  show: boolean;
  agentId?: string;
};

/**
 * @description Welcome message shown to the user when they first open the chat.
 */
export const Welcome: React.FC<Props> = ({ show, agentId }) => {
  const { contrastText, bg, contrastFill } = useBrandedColors('');
  const description = getDescription(agentId);

  return (
    <Transition
      show={show}
      enter="transition-all duration-300 ease-out delay-300"
      enterFrom="opacity-0"
      enterTo="opacity-100"
      leave="transition-opacity duration-200"
      leaveFrom="opacity-100"
      leaveTo="opacity-0"
      as="div"
    >
      <div className="flex flex-col gap-y-4 p-4 md:w-[380px] lg:w-[520px]">
        <div className="flex w-full items-center gap-x-3">
          <div
            className={cn(
              'flex h-7 w-7 items-center justify-center rounded md:h-9 md:w-9',
              contrastText,
              bg
            )}
          >
            <AgentLogo agent_id={agentId} />
          </div>
          <Text styleAs="h4" className="truncate">
            {agentId}
          </Text>
          <Text className="ml-auto" styleAs="caption">
            By Rheingold Salon
          </Text>
        </div>
        <Text className="text-mushroom-300 dark:text-marble-800">
          {description}
        </Text>
      </div>
    </Transition>
  );
};
