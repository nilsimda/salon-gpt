'use client';

import { Transition } from '@headlessui/react';
import { useState } from 'react';

import { Interview, InterviewType } from '@/cohere-client';
import { Icon, IconButton, Text, Tooltip } from '@/components/UI';
import {
  useAgent,
  useBrandedColors,
  useChatRoutes,
  useSession,
  useListStudyFiles
} from '@/hooks';
import { useParamsStore, useSettingsStore } from '@/stores';

type Props = {};

export const ConversationPanel: React.FC<Props> = () => {
  const { disabledAssistantKnowledge, setRightPanelOpen } = useSettingsStore();
  const { agentId, conversationId } = useChatRoutes();
  const { data: agent } = useAgent({ agentId });
  const { theme } = useBrandedColors(agentId);

  const {
    params: { interviews: interviews, selected_study: selected_study },
    setParams,
  } = useParamsStore();

  const session = useSession();

  const { data: currentInterviews } = useListStudyFiles(selected_study?.id);

  const groupedInterviews = interviews?.reduce((groups, interview) => {
    const type = interview.type;
    if (!groups[type]) {
      groups[type] = [];
    }
    groups[type].push(interview);
    return groups;
  }, {} as Record<InterviewType, Interview[]>);

  const [collapsedTables, setCollapsedTables] = useState({
    "TI": false,
    "GD": false,
    "Memo": false,
  });

  const toggleTable = (type: InterviewType) => {
    setCollapsedTables((prev) => ({ ...prev, [type]: !prev[type] }));
  };

  return (
    <aside className="flex flex-col space-y-5 overflow-y-auto py-4">
      <header className="flex items-center gap-2">
        <IconButton
          onClick={() => setRightPanelOpen(false)}
          iconName="arrow-right"
          className="flex h-auto flex-shrink-0 self-center lg:hidden"
        />
        <Text styleAs="p-sm" className="font-medium uppercase">
          Interviews
        </Text>
      </header>
      <div className="flex flex-col gap-y-10">
        {agentId && (
          <div className="flex flex-col gap-y-4">
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-x-2">
                <Text styleAs="label" className="font-medium">
                  Interviews
                </Text>
                <Tooltip
                  hover
                  size="sm"
                  placement="top-start"
                  hoverDelay={250}
                  label="Enables assistant knowledge to provide more accurate responses."
                />
              </span>
            </div>
            <Transition
              show={!disabledAssistantKnowledge.includes(agentId) ?? false}
              enter="duration-300 ease-in-out transition-all"
              enterFrom="opacity-0 scale-90"
              enterTo="opacity-100 scale-100"
              leave="duration-200 ease-in-out transition-all"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-90"
              as="div"
            >
            </Transition>
          </div>
        )}
        <section className="relative flex flex-col gap-y-6">
          <div className="flex gap-x-2">
            <Text styleAs="label" className="font-medium">
              {selected_study?.name ?? 'Studie'}
            </Text>
            <Tooltip
              hover
              size="sm"
              placement="top-start"
              label="To use uploaded files, at least 1 File Upload tool must be enabled"
            />
          </div>
          {groupedInterviews && interviews && interviews.length > 0 && (
            <div className="flex flex-col gap-y-4">
              {[InterviewType.TI, InterviewType.GD, InterviewType.MEMO].map((type) => (
                <div
                  key={type}
                  className="group flex w-full flex-col gap-y-2 rounded-lg p-2 dark:hover:bg-volcanic-200"
                >
                  <h2
                    className="flex cursor-pointer items-center"
                    onClick={() => toggleTable(type)}
                  >
                    {type}s
                    <Icon
                      name={collapsedTables[type] ? 'chevron-down' : 'chevron-up'}
                      className="ml-2"
                    />
                  </h2>
                  {!collapsedTables[type] && groupedInterviews[type]?.length > 0 && (
                    <table>
                      <thead>
                        <tr>
                          {Object.keys(groupedInterviews[type][0]?.fields || {}).map((fieldKey) => (
                            <th key={fieldKey}>{fieldKey}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {groupedInterviews[type]?.map((interview: Interview, index) => (
                          <tr key={interview.id}>
                            <td>{index}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              ))}
            </div>
          )}
          {!selected_study && (
            <Text styleAs="caption" className="text-mushroom-300 dark:text-marble-800">
              Keine Studie ausgewählt
            </Text>
          )}
        </section>
      </div>
    </aside>
  );
};
