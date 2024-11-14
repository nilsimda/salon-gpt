'use client';

import { usePathname, useRouter } from 'next/navigation';

import { QuoteLogo, Text, Tooltip } from '@/components/UI';
import { useBrandedColors, useChatRoutes, useConversationFileActions, useIsDesktop } from '@/hooks';
import {
  useCitationsStore,
  useConversationStore,
  useParamsStore,
  useSettingsStore,
} from '@/stores';
import { cn } from '@/utils';

import { AgentLogo } from '../Agents/AgentLogo';

type Props = {
  name: string;
  isBaseAgent?: boolean;
  id?: string;
};

/**
 * @description This component renders an agent icon.
 * It shows a tooltip of the agent's name and a colored icon with the first letter of the agent's name.
 * If the agent is a base agent, it shows the Coral logo instead.
 */
export const AgentIcon: React.FC<Props> = ({ name, id, isBaseAgent }) => {
  const { conversationId } = useChatRoutes();
  const router = useRouter();
  const isDesktop = useIsDesktop();
  const isMobile = !isDesktop;
  const pathname = usePathname();
  const { setLeftPanelOpen } = useSettingsStore();

  const isActive = isBaseAgent
    ? conversationId
      ? pathname === `/c/${conversationId}`
      : pathname === '/'
    : conversationId
    ? pathname === `/a/${id}/c/${conversationId}`
    : pathname === `/a/${id}`;

  const { bg, contrastText, contrastFill } = useBrandedColors(id);

  const { resetConversation } = useConversationStore();
  const { resetCitations } = useCitationsStore();
  const { resetFileParams } = useParamsStore();
  const { clearComposerFiles } = useConversationFileActions();

  const resetConversationSettings = () => {
    clearComposerFiles();
    resetConversation();
    resetCitations();
    resetFileParams();
  };

  const handleClick = () => {
    if (isActive) return;

    const url = isBaseAgent ? '/' : `/a/${id}`;

    router.push(url);

    resetConversationSettings();
    isMobile && setLeftPanelOpen(false);
  };

  return (
    <Tooltip label={name} placement="bottom" hover size="sm">
      <div
        onClick={handleClick}
        className={cn(
          'group flex w-full items-center justify-between gap-x-2 rounded-lg p-2 transition-colors hover:cursor-pointer hover:bg-mushroom-800 dark:hover:bg-volcanic-200',
          {
            'bg-mushroom-800 dark:bg-volcanic-200': isActive,
          }
        )}
      >
        <div
          className={cn(
            'flex size-8 flex-shrink-0 items-center justify-center rounded duration-300',
            bg
          )}
        >
          <AgentLogo className={contrastFill} agent_id={id} />
        </div>
      </div>
    </Tooltip>
  );
};
