import { SalonChatRequest } from './generated';

export const mapToChatRequest = (request: SalonChatRequest): SalonChatRequest => {
  return {
    agent_id: request.agent_id,
    message: request.message,
    conversation_id: request.conversation_id,
    study_id: request.study_id,
    description: request.description,
    interview_ids: request.interview_ids,
  };
};
