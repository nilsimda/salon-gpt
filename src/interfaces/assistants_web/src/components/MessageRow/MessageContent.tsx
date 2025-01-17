'use client';

import { Transition } from '@headlessui/react';
import { PropsWithChildren } from 'react';

import { Markdown } from '@/components/Markdown';
import { SearchResults } from '@/components/MessageRow';
import { Icon, Text } from '@/components/UI';
import {
  type ChatMessage,
  MessageType,
  isAbortedMessage,
  isErroredMessage,
  isFulfilledOrTypingMessage,
  isLoadingMessage,
} from '@/types/message';
import { cn } from '@/utils';

type Props = {
  isLast: boolean;
  message: ChatMessage;
  onRetry?: VoidFunction;
};

const BOT_ERROR_MESSAGE = 'Unable to generate a response since an error was encountered. ';

export const MessageContent: React.FC<Props> = ({ isLast, message, onRetry }) => {
  const isUser = message.type === MessageType.USER;
  const isLoading = isLoadingMessage(message);
  const isBotError = isErroredMessage(message);
  const isUserError = isUser && message.error;
  const isAborted = isAbortedMessage(message);
  const isTypingOrFulfilledMessage = isFulfilledOrTypingMessage(message);

  if (isUserError) {
    return (
      <MessageWrapper>
        <Text>{message.text}</Text>
        <MessageInfo type="error">
          {message.error}
          {isLast && (
            <button className="underline underline-offset-1" type="button" onClick={onRetry}>
              Erneut versuchen?
            </button>
          )}
        </MessageInfo>
      </MessageWrapper>
    );
  }

  if (isUser) {
    return (
      <MessageWrapper>
        <Markdown text={message.text} renderRawHtml={false} />
      </MessageWrapper>
    );
  }

  if (isLoading) {
    const hasLoadingMessage = message.text.length > 0;
    return (
      <MessageWrapper>
        <Text className={cn('flex min-w-0 text-volcanic-400')} as="span">
          {hasLoadingMessage && (
            <Transition
              as="div"
              appear={true}
              show={true}
              enterFrom="opacity-0"
              enterTo="opacity-full"
              enter="transition-opacity ease-in-out duration-500"
            >
              {message.text}
            </Transition>
          )}
          {!hasLoadingMessage && (
            <span className="w-max">
              <div className="animate-typing-ellipsis overflow-hidden whitespace-nowrap pr-1">
                ...
              </div>
            </span>
          )}
        </Text>
      </MessageWrapper>
    );
  }

  if (isBotError) {
    return (
      <MessageWrapper>
        {message.text.length > 0 ? (
          <Markdown text={message.text} />
        ) : (
          <Text className={cn('text-volcanic-400')}>{BOT_ERROR_MESSAGE}</Text>
        )}
        <MessageInfo type="error">{message.error}</MessageInfo>
      </MessageWrapper>
    );
  }

  const hasCitations =
    isTypingOrFulfilledMessage && message.citations && message.citations.length > 0;
  return (
    <>
      <MessageWrapper>
        <Markdown
          className={cn({
            'text-volcanic-400': isAborted,
          })}
          text={message.text}
          renderLaTex={!hasCitations}
        />
        {isAborted && (
          <MessageInfo>
            Diese Antwort wurde unterbrochen.{' '}
            {isLast && isAborted && (
              <button className="underline underline-offset-1" type="button" onClick={onRetry}>
                Erneut versuchen?
              </button>
            )}
          </MessageInfo>
        )}
      </MessageWrapper>
      <SearchResults searchResults={message.search_results} />
    </>
  );
};

const MessageInfo = ({
  type = 'default',
  children,
}: PropsWithChildren & { type?: 'default' | 'error' }) => (
  <div
    className={cn('flex items-start gap-1', {
      'text-volcanic-400': type === 'default',
      'text-danger-350': type === 'error',
    })}
  >
    <Icon name="warning" size="sm" className="mt-1 flex flex-shrink-0 items-center" />
    <Text as="span">{children}</Text>
  </div>
);

const MessageWrapper = ({ children }: PropsWithChildren) => (
  <div className="flex w-full flex-col justify-center gap-y-1 py-1">
    <Text
      as="div"
      className="flex flex-col gap-y-1 whitespace-pre-wrap [overflow-wrap:anywhere] md:max-w-4xl"
    >
      {children}
    </Text>
  </div>
);
