'use client';

import { HotKeyGroupOption } from '@/components/HotKeys/domain';
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
