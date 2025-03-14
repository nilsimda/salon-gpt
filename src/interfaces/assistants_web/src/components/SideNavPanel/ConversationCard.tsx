'use client';

import Link from 'next/link';

import { KebabMenu, KebabMenuItem, QuoteLogo, Text, Tooltip } from '@/components/UI';
import { useContextStore } from '@/context';
import {
  getIsTouchDevice,
  useBrandedColors,
  useConversationActions,
  useIsDesktop,
  useToggleConversationPin,
} from '@/hooks';

import { useConversationStore, useSettingsStore } from '@/stores';
import { cn, formatDateToShortDate } from '@/utils';

import { AgentLogo } from '../Agents/AgentLogo';

export type ConversationListItem = {
  conversationId: string;
  updatedAt: string;
  title: string;
  description: string | null;
  isPinned: boolean;
  weekHeading?: string;
  agentName?: string;
};

type Props = {
  isChecked: boolean;
  isActive: boolean;
  showCheckbox: boolean;
  conversation: ConversationListItem;
  /* Config values necessary for react-flipped-toolkit */
  flippedProps: Object;
  onCheck: (id: string) => void;
};

const useMenuItems = ({
  conversationId,
  isPinned,
}: {
  conversationId: string;
  isPinned: boolean;
}) => {
  const { deleteConversation } = useConversationActions();
  const { open } = useContextStore();
  const { mutateAsync: toggleConversationPin } = useToggleConversationPin();

  const menuItems: KebabMenuItem[] = [
    {
      label: isPinned ? 'Chat Lösen' : 'Chat Anheften',
      iconName: 'pin',
      onClick: async () => {
        await toggleConversationPin({ request: { is_pinned: !isPinned }, conversationId });
      },
    },
    {
      label: 'Chat Teilen',
      iconName: 'share',
    },
    {
      label: 'Chat Löschen',
      iconName: 'trash',
      iconClassName: 'dark:text-danger-500',
      onClick: () => {
        deleteConversation({ id: conversationId });
      },
    },
  ];

  return menuItems;
};

export const ConversationCard: React.FC<Props> = ({ isActive, conversation, flippedProps }) => {
  const { title, conversationId, isPinned } = conversation;
  const {
    conversation: { id: selectedConversationId, name: conversationName },
    setConversation,
  } = useConversationStore();
  const { isLeftPanelOpen, setLeftPanelOpen } = useSettingsStore();
  const isDesktop = useIsDesktop();
  const isMobile = !isDesktop;
  const isTouchDevice = getIsTouchDevice();
  const { bg, contrastText, contrastFill } = useBrandedColors(conversation.agentName);

  // if the conversation card is for the selected conversation we use the `conversationName`
  // from the context store, otherwise we use the name from the conversation object
  // this is to ensure that we use the typed animation
  // @see "handleUpdateConversationTitle" in hooks/chat.ts
  const name = conversationId === selectedConversationId ? conversationName : title;

  const menuItems = useMenuItems({ conversationId, isPinned });

  const info = (
    <div className="flex flex-col gap-y-2 pl-3">
      <div className="flex w-full items-center justify-between gap-x-0.5">
        <div className="flex w-full flex-col">
          <Text
            as="span"
            className={cn('h-[21px] truncate font-medium text-volcanic-300 dark:text-mushroom-950')}
          >
            {name}
          </Text>
          <Text styleAs="p-sm" className="truncate">
            {conversation.description}
          </Text>
        </div>

        {/* Placeholder for the kebab menu */}
        <div className="flex h-4 w-4 flex-shrink-0" />
      </div>
      <div className="flex h-[18px] w-full items-center gap-2">
        <div
          className={cn(
            'flex size-4 flex-shrink-0 items-center justify-center rounded',
            bg,
            contrastText
          )}
        >
          {conversation.agentName ? (
            <Text className={contrastText} styleAs="p-xs">
              {conversation.agentName[0]}
            </Text>
          ) : (
            <AgentLogo agent_id={conversation.agentName} className={cn('scale-50', contrastFill)} />
          )}
        </div>
        <Text styleAs="p-sm" className="truncate text-volcanic-500 dark:text-mushroom-800">
          {conversation.agentName ?? 'Rheingold Salon'}
        </Text>
        <Text styleAs="code-sm" className="ml-auto mt-0.5 uppercase dark:text-mushroom-800">
          {formatDateToShortDate(conversation.updatedAt)}
        </Text>
      </div>
    </div>
  );

  const conversationUrl = conversation.agentName
    ? `/a/${conversation.agentName}/c/${conversationId}`
    : `/c/${conversationId}`;

  const wrapperClassName = cn('flex w-full flex-col gap-y-1 pr-2 py-3 truncate');
  const conversationLink =
    isActive && isDesktop ? (
      <div className={cn('select-none', wrapperClassName)}>{info}</div>
    ) : (
      <Link
        href={conversationUrl}
        key={conversationId}
        shallow
        onClick={() => {
          setConversation({ id: conversationId, name });
          isMobile && setLeftPanelOpen(false);
        }}
        className={wrapperClassName}
      >
        {info}
      </Link>
    );

  if (!isLeftPanelOpen) {
    const content = (
      <div
        className={cn(
          'flex size-8 flex-shrink-0 items-center justify-center rounded',
          bg,
          contrastText
        )}
      >
        {conversation.agentName ? (
          <Text>{conversation.agentName[0]}</Text>
        ) : (
          <AgentLogo agent_id={conversation.agentName} className={contrastFill} />
        )}
      </div>
    );
    return (
      <div {...flippedProps}>
        <Tooltip label={conversation.title} placement={'bottom-end'} hover size="sm">
          {isActive && isDesktop ? (
            <div className="select-none">{content}</div>
          ) : (
            <Link
              href={conversationUrl}
              key={conversationId}
              shallow
              onClick={() => {
                setConversation({ id: conversationId, name });
                isMobile && setLeftPanelOpen(false);
              }}
            >
              {content}
            </Link>
          )}
        </Tooltip>
      </div>
    );
  }

  return (
    <div
      {...flippedProps}
      className={cn('group relative flex w-full rounded-lg', 'flex items-start gap-x-1', {
        'transition-colors ease-in-out hover:bg-white dark:hover:bg-volcanic-200': !isActive,
        'bg-white dark:bg-volcanic-200': isActive,
      })}
    >
      {conversationLink}
      <div className="absolute right-3 top-3.5 flex">
        <KebabMenu
          anchor="right start"
          items={menuItems}
          className={cn('flex', {
            'hidden group-hover:flex': !isTouchDevice,
          })}
        />
      </div>
    </div>
  );
};
