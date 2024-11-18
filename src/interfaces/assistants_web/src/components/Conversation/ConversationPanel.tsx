'use client';

import { Transition } from '@headlessui/react';
import { group } from 'console';
import { uniqBy } from 'lodash';
import { useMemo, useState } from 'react';

import { Interview, InterviewType } from '@/cohere-client';
import { Banner, Button, Icon, IconButton, Text, Tooltip } from '@/components/UI';
import { TOOL_GOOGLE_DRIVE_ID, TOOL_READ_DOCUMENT_ID, TOOL_SEARCH_INTERVIEW_ID } from '@/constants';
import {
  useAgent,
  useBrandedColors,
  useChatRoutes,
  useSession,
  useListStudyFiles
} from '@/hooks';
import { useParamsStore, useSettingsStore } from '@/stores';
import { DataSourceArtifact } from '@/types/tools';
import { pluralize } from '@/utils';
import { useEffect } from 'react';

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

    // Add loading state check
  const { data: currentInterviews, isLoading: isLoadingInterviews } = useListStudyFiles(selected_study?.id);

  // Use an effect to ensure interviews are always in sync
  useEffect(() => {
    if (currentInterviews && !isLoadingInterviews) {
      setParams(prev => ({ ...prev, interviews: currentInterviews }));
    }
  }, [currentInterviews, isLoadingInterviews, setParams]);

  const agentToolMetadataArtifacts = useMemo(() => {
    if (!agent) {
      return {
        files: [],
        folders: [],
      };
    }

    const fileArtifacts = uniqBy(
      (
        agent.tools_metadata?.filter((tool_metadata) =>
          [TOOL_GOOGLE_DRIVE_ID, TOOL_READ_DOCUMENT_ID, TOOL_SEARCH_INTERVIEW_ID].includes(
            tool_metadata.tool_name
          )
        ) ?? []
      )
        .map((tool_metadata) => tool_metadata.artifacts as DataSourceArtifact[])
        .flat(),
      'id'
    );

    const files = fileArtifacts.filter((artifact) => artifact.type !== 'folder'); // can be file, document, pdf, etc.
    const folders = fileArtifacts.filter((artifact) => artifact.type === 'folder');
    return {
      files,
      folders,
    };
  }, [agent]);

  const agentKnowledgeFiles = [
    ...agentToolMetadataArtifacts.files,
    ...agentToolMetadataArtifacts.folders,
  ];

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
              {/* @DEV_NOTE: This is disabled while we add the ability in BE to enable/disable assistant knowledge */}
              {/* <Switch
                theme={theme}
                checked={!disabledAssistantKnowledge.includes(agentId)}
                onChange={(checked) => setUseAssistantKnowledge(checked, agentId)}
              /> */}
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
              {agentKnowledgeFiles.length === 0 && session.userId === agent?.user_id ? (
                <Banner className="flex flex-col">
                  Add a data source to expand the assistant’s knowledge.
                  <Button
                    theme={theme}
                    className="mt-4 w-full"
                    label="Add Data Source"
                    stretch
                    icon="add"
                    href={`/edit/${agentId}?datasources=1`}
                  />
                </Banner>
              ) : (
                <div className="flex flex-col gap-y-3">
                  <Text as="div" className="flex items-center gap-x-3">
                    <Icon name="folder" kind="outline" className="flex-shrink-0" />
                    {/*  This renders the number of folders and files in the agent's Google Drive.
                    For example, if the agent has 2 folders and 3 files, it will render:
                    - "2 folders and 3 files" */}
                    {agentToolMetadataArtifacts.folders.length > 0 &&
                      `${agentToolMetadataArtifacts.folders.length} ${pluralize(
                        'folder',
                        agentToolMetadataArtifacts.folders.length
                      )} ${agentToolMetadataArtifacts.files.length > 0 ? 'and ' : ''}`}
                    {agentToolMetadataArtifacts.files.length > 0 &&
                      `${agentToolMetadataArtifacts.files.length} ${pluralize(
                        'file',
                        agentToolMetadataArtifacts.files.length
                      )}`}
                  </Text>
                  <ol className="space-y-2">
                    {agentKnowledgeFiles.map((file) => (
                      <li key={file.id} className="ml-6 flex items-center gap-x-3">
                        <Icon
                          name={file.type === 'folder' ? 'folder' : 'file'}
                          kind="outline"
                          className="flex-shrink-0"
                        />
                        <Text>{file.name}</Text>
                      </li>
                    ))}
                  </ol>
                </div>
              )}
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
