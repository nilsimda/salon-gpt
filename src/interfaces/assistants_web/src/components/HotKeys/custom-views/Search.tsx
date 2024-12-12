'use client';

import { ComboboxOptions } from '@headlessui/react';
import { useDebouncedEffect } from '@react-hookz/web';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

import { AgentLogo } from '@/components/Agents/AgentLogo';
import { CommandActionGroup, HotKeyGroupOption, HotKeysDialogInput } from '@/components/HotKeys';
import { BASE_AGENT, AGENTS } from '@/constants';
import { useConversations } from '@/hooks';

type Props = {
  isOpen: boolean;
  close: VoidFunction;
  onBack: VoidFunction;
};

export const Search: React.FC<Props> = ({ isOpen, close, onBack }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<HotKeyGroupOption[]>([
    {
      group: 'Conversations',
      quickActions: [],
    },

    {
      group: 'Assistants',
      quickActions: [],
    },
  ]);
  const router = useRouter();

  const assistants = AGENTS;
  const { data: conversations } = useConversations({});

  useDebouncedEffect(
    () => {
      if (!query) {
        setResults([
          {
            group: 'Conversations',
            quickActions: [],
          },
          {
            group: 'Assistants',
            quickActions: [],
          },
        ]);
        return;
      }

      const foundConversations = conversations?.filter((conversation) => {
        const title = conversation.title.toLowerCase();
        const description = conversation.description?.toLowerCase();
        return title.includes(query) || (description && description.includes(query));
      });

      const foundAssistants = assistants?.filter((assistant) => {
        const name = assistant.toLowerCase();

        return (
          name.includes(query)
        );
      });

      setResults([
        {
          group: 'Conversations',
          quickActions:
            foundConversations?.map((conversation) => ({
              name: conversation.title,
              label: (
                <div className="flex items-center gap-x-2">
                  <AgentLogo
                    agent_id={
                      assistants?.find((assistant) => assistant === conversation.agent_id) ??
                      BASE_AGENT
                    }
                  />
                  <span>{conversation.title}</span>
                  <span className="ml-2 truncate text-p-sm text-volcanic-600">
                    {conversation.description}
                  </span>
                </div>
              ),
              action: () => {
                if (conversation.agent_id) {
                  router.push(`/a/${conversation.agent_id}/c/${conversation.id}`);
                } else {
                  router.push(`/c/${conversation.id}`);
                }
              },
              closeDialogOnRun: true,
              commands: [],
              registerGlobal: false,
            })) || [],
        },
        {
          group: 'Assistants',
          quickActions:
            foundAssistants?.map((assistant) => ({
              name: assistant,
              label: (
                <div className="flex items-center gap-x-2">
                  <AgentLogo agent_id={assistant} />
                  <span>{assistant}</span>
                </div>
              ),
              action: () => router.push(`/a/${assistant}`),
              closeDialogOnRun: true,
              commands: [],
              registerGlobal: false,
            })) || [],
        },
      ]);
    },
    [query, assistants, conversations],
    500
  );

  return (
    <span className="mb-3">
      <HotKeysDialogInput
        value={query}
        setValue={setQuery}
        placeholder="Search conversations and assistants"
        close={close}
        onBack={onBack}
        isSearch
      />
      <ComboboxOptions className="mb-3 flex flex-col gap-y-6 overflow-y-auto" static>
        <CommandActionGroup isOpen={isOpen} options={results} />
      </ComboboxOptions>
    </span>
  );
};
