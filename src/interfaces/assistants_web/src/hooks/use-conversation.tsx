import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { DeleteConversations } from '@/components/Modals/DeleteConversations';
import { EditConversationTitle } from '@/components/Modals/EditConversationTitle';
import { useContextStore } from '@/context';
import { useNavigateToNewChat, useNotify } from '@/hooks';
import {
  ApiError,
  CohereNetworkError,
  ConversationPublic,
  ConversationWithoutMessages,
  DeleteConversationResponse,
  ToggleConversationPinRequest,
  UpdateConversationRequest,
  useSalonClient,
} from '@/salon-client';
import { useConversationStore } from '@/stores';
import { isAbortError } from '@/utils';

export const useConversations = (params: {
  offset?: number;
  limit?: number;
  orderBy?: string;
  agentId?: string;
}) => {
  const client = useSalonClient();

  return useQuery<ConversationWithoutMessages[], ApiError>({
    queryKey: ['conversations', params.agentId],
    queryFn: () => client.listConversations(params),
    retry: 0,
    refetchOnWindowFocus: false,
  });
};

export const useConversation = ({
  conversationId,
  disabledOnMount,
}: {
  conversationId?: string;
  disabledOnMount?: boolean;
}) => {
  const client = useSalonClient();

  return useQuery<ConversationPublic | undefined, Error>({
    queryKey: ['conversation', conversationId],
    enabled: !!conversationId && !disabledOnMount,
    queryFn: async () => {
      try {
        if (!conversationId) throw new Error('Conversation ID not found');
        return await client.getConversation({
          conversationId: conversationId,
        });
      } catch (e) {
        if (!isAbortError(e)) {
          console.error(e);
          throw e;
        }
      }
    },
    retry: 0,
    refetchOnWindowFocus: false,
  });
};

export const useEditConversation = () => {
  const client = useSalonClient();
  const queryClient = useQueryClient();
  return useMutation<
    ConversationPublic,
    CohereNetworkError,
    { request: UpdateConversationRequest; conversationId: string }
  >({
    mutationFn: ({ request, conversationId }) => client.editConversation(request, conversationId),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
    },
  });
};

export const useToggleConversationPin = () => {
  const client = useSalonClient();
  const queryClient = useQueryClient();
  return useMutation<
    ConversationWithoutMessages,
    CohereNetworkError,
    { request: ToggleConversationPinRequest; conversationId: string }
  >({
    mutationFn: ({ request, conversationId }) =>
      client.toggleConversationPin(request, conversationId),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
    },
  });
};

export const useDeleteConversation = () => {
  const client = useSalonClient();
  const queryClient = useQueryClient();
  return useMutation<DeleteConversationResponse, CohereNetworkError, { conversationId: string }>({
    mutationFn: ({ conversationId }: { conversationId: string }) =>
      client.deleteConversation({ conversationId }),
    onSettled: (_, _err, { conversationId }: { conversationId: string }) => {
      queryClient.setQueriesData<ConversationPublic[]>(
        { queryKey: ['conversations'] },
        (oldConversations) => oldConversations?.filter((c) => c.id !== conversationId)
      );
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
    },
  });
};

export const useConversationActions = () => {
  const { open, close } = useContextStore();
  const {
    conversation: { id: conversationId },
    setConversation,
  } = useConversationStore();
  const notify = useNotify();
  const navigateToNewChat = useNavigateToNewChat();
  const { mutateAsync: deleteConversation, isPending } = useDeleteConversation();

  const handleDeleteConversation = async ({
    id,
    onComplete,
  }: {
    id: string;
    onComplete?: VoidFunction;
  }) => {
    const onDelete = () => {
      close();
      onComplete?.();
      setConversation({ id: undefined });

      if (id === conversationId) {
        navigateToNewChat();
      }
    };

    const onConfirm = async () => {
      try {
        await deleteConversation({ conversationId: id });
        onDelete();
      } catch (e) {
        console.error(e);
        notify.error('Etwas ist schief gelaufen. Bitte versuche es nochmal.');
      }
    };

    open({
      title: `Willst du die Konversation wirklich löschen?`,
      content: (
        <DeleteConversations
          conversationIds={[id]}
          onClose={close}
          onConfirm={onConfirm}
          isPending={isPending}
        />
      ),
    });
  };

  const editConversationTitle = ({ id, title }: { id: string; title: string }) => {
    const onClose = () => {
      close();
    };

    open({
      title: 'Titel ändern',
      content: (
        <EditConversationTitle
          conversationId={id}
          initialConversationTitle={title}
          onClose={onClose}
        />
      ),
    });
  };

  return { deleteConversation: handleDeleteConversation, editConversationTitle };
};
