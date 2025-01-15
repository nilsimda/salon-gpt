import { StateCreator } from 'zustand';

import { SalonChatRequest } from '@/salon-client';

import { StoreState } from '..';

const INITIAL_STATE: ConfigurableParams = {
  interview_ids: [],
  study_id: '',
  description: ''
};

export type ConfigurableParams = Pick<SalonChatRequest, 'study_id' | 'interview_ids' | 'description'>;

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
    set((state) => {
      return {
        params: {
          ...state.params,
          ...params,
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
