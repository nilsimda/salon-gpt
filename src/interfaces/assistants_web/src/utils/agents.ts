import { AgentPublic } from '@/cohere-client';

/**
 * @description Checks if the agent is the base agent.
 * @param agent - The agent to check.
 */
export const checkIsBaseAgent = (agent: AgentPublic | undefined) => {
  return agent?.id === '';
};

/**
 * @description Checks if the agent is the transcription agent.
 * @param agent - The agent to check.
 */
export const checkIsTranscriptionAgent = (agent: AgentPublic | undefined) => {
  return agent?.id === 'transcription';
};

/**
 * @description Checks if the agent is the synthetic user agent.
 * @param agent - The agent to check.
 */
export const checkIsSyntheticUserAgent = (agent: AgentPublic | undefined) => {
  return agent?.id === 'synthetic-user';
};
