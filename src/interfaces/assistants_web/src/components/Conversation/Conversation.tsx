'use client';

import React, { useRef } from 'react';

import { Composer } from '@/components/Composer';
import { Header } from '@/components/Conversation';
import { MessagingContainer, WelcomeGuideTooltip } from '@/components/MessagingContainer';
import { WelcomeGuideStep, useChat, useWelcomeGuideState } from '@/hooks';
import { useConversationStore } from '@/stores';
import { ConfigurableParams } from '@/stores/slices/paramsSlice';
import { ChatMessage } from '@/types/message';

type Props = {
  startOptionsEnabled?: boolean;
  agentName: string;
  history?: ChatMessage[];
};

/**
 * @description Renders the entire conversation pane, which includes the header, messages,
 * composer, and the citation panel.
 */
export const Conversation: React.FC<Props> = ({ agentName, startOptionsEnabled = false }) => {
  const { welcomeGuideState, finishWelcomeGuide } = useWelcomeGuideState();
  const {
    conversation: { messages, id: conversationId },
  } = useConversationStore();

  const {
    userMessage,
    isStreaming,
    isStreamingToolEvents,
    streamingMessage,
    setUserMessage,
    handleSend: send,
    handleStop,
    handleRetry,
    handleRegenerate,
  } = useChat({
    onSend: () => {
      if (welcomeGuideState !== WelcomeGuideStep.DONE) {
        finishWelcomeGuide();
      }
    },
  });

  const chatWindowRef = useRef<HTMLDivElement>(null);

  const handleSend = (msg?: string, overrides?: Partial<ConfigurableParams>) => {
    send({ suggestedMessage: msg }, overrides);
  };

  return (
    <div className="flex h-full flex-grow">
      <div className="flex h-full w-full min-w-0 flex-col rounded-l-lg rounded-r-lg border border-marble-950 bg-marble-980 dark:border-volcanic-200 dark:bg-volcanic-100 lg:rounded-r-none">
        <Header agentName={agentName} />
        <div className="relative flex h-full w-full flex-col" ref={chatWindowRef}>
          <MessagingContainer
            conversationId={conversationId}
            startOptionsEnabled={startOptionsEnabled}
            isStreaming={isStreaming}
            isStreamingToolEvents={isStreamingToolEvents}
            onRetry={handleRetry}
            onRegenerate={handleRegenerate}
            messages={messages}
            streamingMessage={streamingMessage}
            agentId={agentName}
            composer={
              <>
                <WelcomeGuideTooltip step={3} className="absolute bottom-full mb-4" />
                <Composer
                  isStreaming={isStreaming}
                  value={userMessage}
                  streamingMessage={streamingMessage}
                  chatWindowRef={chatWindowRef}
                  onChange={(message) => setUserMessage(message)}
                  onSend={handleSend}
                  onStop={handleStop}
                  agentName={agentName}
                  lastUserMessage={messages.findLast((m) => m.type === 'user')}
                />
              </>
            }
          />
        </div>
      </div>
    </div>
  );
};
