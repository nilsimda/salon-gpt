// @todo: import from generated types when available
export enum FinishReason {
  ERROR = 'ERROR',
  COMPLETE = 'COMPLETE',
  MAX_TOKENS = 'MAX_TOKENS',
}

// Chat
export const OLLAMA_DEPLOYMENT = "Ollama";
export const OLLAMA_DEPLOYMENT_DEFAULT_CHAT_MODEL = "llama3.2"

export const DEFAULT_CHAT_TEMPERATURE = 0.3;
export const DEFAULT_CHAT_TOOL = 'Wikipedia';
export const FILE_TOOL_CATEGORY = 'File loader';
