'use client';

import { useEffect } from 'react';

import { Conversation, ConversationError } from '@/components/Conversation';
import { useConversation } from '@/hooks';
import { useCitationsStore, useConversationStore, useParamsStore } from '@/stores';
import { createStartEndKey, fixInlineCitationsForMarkdown, mapHistoryToMessages } from '@/utils';

const Chat: React.FC<{ agentName: string; conversationId?: string }> = ({
  agentName,
  conversationId,
}) => {
  const { setConversation } = useConversationStore();
  const { addCitation } = useCitationsStore();
  const { setParams, resetFileParams } = useParamsStore();

  const {
    data: conversation,
    isError,
    error,
  } = useConversation({
    conversationId: conversationId,
  });

  // Reset citations and file params when switching between conversations
  useEffect(() => {
    resetFileParams();

    if (conversationId) {
      setConversation({ id: conversationId });
    }
  }, [agentName, conversation, setParams, resetFileParams, setConversation, conversationId]);

  useEffect(() => {
    if (!conversation) return;

    const messages = mapHistoryToMessages(
      conversation?.messages?.sort((a, b) => a.position - b.position)
    );

    setConversation({ name: conversation.title, messages });

    (conversation?.messages ?? []).forEach((message) => {
      fixInlineCitationsForMarkdown(message.citations, message.text)?.forEach((citation) => {
        const startEndKey = createStartEndKey(citation.start ?? 0, citation.end ?? 0);
        addCitation(message.generation_id ?? '', startEndKey, []);
      });
    });
  }, [conversation?.id, conversation?.messages.length, setConversation]);

  return isError ? (
    <ConversationError error={error} />
  ) : (
    <Conversation agentName={agentName} startOptionsEnabled />
  );
};

export default Chat;
