import { StateCreator } from 'zustand';

import { DEFAULT_CHAT_TEMPERATURE, SalonChatRequest, Study } from '@/salon-client';

import { StoreState } from '..';

const INITIAL_STATE: ConfigurableParams = {
  model: undefined,
  temperature: DEFAULT_CHAT_TEMPERATURE,
  preamble: '',
  tools: [],
  interviews: [],
  deployment: undefined,
  deploymentConfig: undefined,
};

export type ConfigurableParams = Pick<SalonChatRequest, 'temperature' | 'tools'> & {
  preamble: string;
  interviews: SalonChatRequest['interviews'];
  selected_study?: Study;
  model?: string;
  deployment?: string;
  deploymentConfig?: string;
};

type State = ConfigurableParams;
type Actions = {
  setParams: (params?: Partial<ConfigurableParams> | null) => void;
  resetFileParams: VoidFunction;
};

export type ParamStore = {
  params: State;
} & Actions;

export const createParamsSlice: StateCreator<StoreState, [], [], ParamStore> = (set) => ({
  setParams(params?) {
    let tools = params?.tools;
    let interviews = params?.interviews;

    set((state) => {
      return {
        params: {
          ...state.params,
          ...params,
          ...(tools ? { tools } : []),
          ...(interviews ? { interviews } : {}),
        },
      };
    });
  },
  resetFileParams() {
    set((state) => {
      return {
        params: {
          ...state.params,
          fileIds: [],
        },
      };
    });
  },
  params: INITIAL_STATE,
});
