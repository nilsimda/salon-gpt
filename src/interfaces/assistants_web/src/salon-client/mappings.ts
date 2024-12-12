import { SalonChatRequest } from './generated';

export const mapToChatRequest = (request: SalonChatRequest): SalonChatRequest => {
  return {
    user_id: request.user_id,
    agent_id: request.agent_id,
    message: request.message,
    conversation_id: request.conversation_id,
    description: request.description,
    interview_ids: request.interview_ids
  };
};
