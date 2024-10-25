'use client';

import { HotKeyGroupOption } from '@/components/HotKeys/domain';
import { ShareConversation } from '@/components/Modals/ShareConversation';
import { useContextStore } from '@/context';
import { useConversationActions, useNavigateToNewChat } from '@/hooks';
import { useConversationStore } from '@/stores';

export const useConversationHotKeys = (): HotKeyGroupOption[] => {
  const {
    conversation: { id },
  } = useConversationStore();
  const { deleteConversation } = useConversationActions();
  const navigateToNewChat = useNavigateToNewChat();
  const { open } = useContextStore();

  if (!id) return [];

  const handleOpenShareModal = () => {
    if (!id) return;
    open({
      title: 'Link zu dieser Unterhaltung teilen',
      content: <ShareConversation conversationId={id} />,
    });
  };

  return [
    {
      group: 'Conversation',
      quickActions: [
        {
          name: 'Neue Unterhaltung',
          commands: ['ctrl+shift+o', 'meta+shift+o'],
          registerGlobal: true,
          closeDialogOnRun: true,
          action: navigateToNewChat,
          options: {
            preventDefault: true,
          },
        },
        {
          name: 'Teilen',
          commands: ['ctrl+alt+a', 'meta+alt+a'],
          registerGlobal: true,
          closeDialogOnRun: true,
          action: handleOpenShareModal,
          options: {
            preventDefault: true,
          },
        },
        {
          name: 'Unterhaltung löschen',
          commands: ['ctrl+shift+backspace', 'meta+shift+backspace'],
          registerGlobal: true,
          closeDialogOnRun: true,
          action: () => {
            if (!id) return;
            deleteConversation({ id });
          },
          options: {
            preventDefault: true,
          },
        },
      ],
    },
  ];
};
