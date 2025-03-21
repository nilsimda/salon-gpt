'use client';

import Lottie from 'react-lottie-player';

import logoTyping from '@/assets/lotties/icon-loop-coral-950.json';
import { Icon } from '@/components/UI';
import { useBrandedColors, useChatRoutes } from '@/hooks';
import { BotState, ChatMessage, MessageType, isFulfilledMessage } from '@/types/message';
import { cn } from '@/utils';

import { AgentLogo } from '../Agents/AgentLogo';

type Props = {
  message: ChatMessage;
};

export const Avatar: React.FC<Props> = ({ message }) => {
  const isUser = message.type === MessageType.USER;
  const isBot = message.type === MessageType.BOT;
  const isLoading = isBot && message.state === BotState.LOADING;
  const isTyping = isBot && message.state === BotState.TYPING;
  const isErrored = isBot && message.state === BotState.ERROR;
  const isAborted = isBot && message.state === BotState.ABORTED;

  const isFulfilled = isFulfilledMessage(message);
  const isTypingOrLoading = isBot && (isTyping || isLoading);
  const isErroredOrAborted = isBot && (isErrored || isAborted);

  // Not having the tools property means that this message is loaded from conversation history
  // and with the current info we get from the backend we don't know if it has tools or not.
  const { agentId } = useChatRoutes();
  const { bg, lightFill } = useBrandedColors(agentId);
  return (
    <div
      className={cn(
        'flex flex-shrink-0 items-center justify-center rounded text-white',
        'h-7 w-7 transition-colors duration-300 ease-in-out md:h-9 md:w-9',
        {
          'bg-volcanic-600': isErroredOrAborted,
          'bg-white': isUser,
          [bg]: isFulfilled || isTypingOrLoading,
        }
      )}
    >
      {isBot && <BotAvatar state={message.state} className={lightFill} />}
      {isUser && <UserAvatar />}
    </div>
  );
};

export const BotAvatar: React.FC<{
  state: BotState;
  className?: string;
}> = ({ state, className }) => {
  const { agentId } = useChatRoutes();
  if (state === BotState.TYPING || state === BotState.LOADING) {
    return <Lottie animationData={logoTyping} play loop className="size-5 md:size-6" />;
  }
  return <AgentLogo agent_id={agentId} />;
};

const UserAvatar: React.FC = () => {
  return (
    <Icon
      name="profile"
      className="h-ep-icon-md w-ep-icon-md md:h-ep-icon-lg md:w-ep-icon-lg fill-marble-980 dark:fill-volcanic-100"
    />
  );
};
