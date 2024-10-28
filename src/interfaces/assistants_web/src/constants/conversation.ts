import { AgentPublic } from '@/cohere-client';
import { FileAccept } from '@/components/UI';
import { DEPLOYMENT_LOCAL_MODEL } from '@/constants/setup';
import {
  AGENT_SETTINGS_TOOLS,
  FILE_UPLOAD_TOOLS,
  TOOL_READ_DOCUMENT_ID,
  TOOL_SEARCH_FILE_ID,
  TOOL_WEB_SCRAPE_ID,
} from '@/constants/tools';

export const DEFAULT_CONVERSATION_NAME = 'Neue Konversation';
export const DEFAULT_AGENT_MODEL = 'mistral-nemo';
export const DEFAULT_TYPING_VELOCITY = 35;
export const CONVERSATION_HISTORY_OFFSET = 100;

export const DEFAULT_PREAMBLE =
  "## Du hilfst bei der Beantwortung von Fragen aus allen Themengebieten, insbesondere bist du Experte in tiefenpsychologischer Marktforschung.";

export const DEFAULT_AGENT_TOOLS = [TOOL_SEARCH_FILE_ID, TOOL_READ_DOCUMENT_ID, TOOL_WEB_SCRAPE_ID];

export const BASE_AGENT: AgentPublic = {
  id: '',
  deployments: [],
  name: 'ZitatKIn',
  description: 'Finde Zitate aus Studien.',
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  preamble: DEFAULT_PREAMBLE,
  version: 1,
  temperature: 0.1,
  tools: [],
  model: DEFAULT_AGENT_MODEL,
  deployment: DEPLOYMENT_LOCAL_MODEL,
  user_id: '',
  is_private: false,
};

export const TRANSCRIPTION_AGENT: AgentPublic = {
    id: 'transcription',
    deployments: [],
    name: 'TransKrIption',
    description: 'Transkribiere Audio- und Videodateien.',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    preamble: '',
    version: 1,
    temperature: 0.0,
    tools: [],
    model: 'whisper-large-v3',
    deployment: DEPLOYMENT_LOCAL_MODEL,
    user_id: '',
    is_private: false,
}

export const SYNTHETIC_USER_AGENT: AgentPublic = {
    id: 'kerlin',
    deployments: [],
    name: 'KerlIn',
    description: 'Interviewe einen synthetischen Studienteilnehmer.',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    preamble: 'Du bist Teilnehmer einer tiefenspsychologischen Marktforschungsstudie. Bitte beantworte die Fragen so ehrlich wie möglich.',
    version: 1,
    temperature: 0.2,
    tools: [],
    model: DEFAULT_AGENT_MODEL,
    deployment: DEPLOYMENT_LOCAL_MODEL,
    user_id: '',
    is_private: false,
}

export const ACCEPTED_FILE_TYPES: FileAccept[] = [
  'text/csv',
  'text/plain',
  'text/html',
  'text/markdown',
  'text/tab-separated-values',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  'application/json',
  'application/pdf',
  'application/epub+zip',
  'application/vnd.apache.parquet',
];
export const MAX_NUM_FILES_PER_UPLOAD_BATCH = 50;
