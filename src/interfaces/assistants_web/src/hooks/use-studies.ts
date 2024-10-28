import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { uniq } from 'lodash';
import { useCallback, useMemo } from 'react';

import {
  StudyPublic,
  ApiError,
  CreateStudyRequest,
  UpdateStudyRequest,
  useCohereClient,
} from '@/cohere-client';

export const useListStudies = () => {
  const cohereClient = useCohereClient();
  return useQuery({
    queryKey: ['listStudies'],
    queryFn: async () => {
      return await cohereClient.listStudies({});
    },
  });
};

export const useCreateStudy = () => {
  const cohereClient = useCohereClient();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (request: CreateStudyRequest) => cohereClient.createStudy(request),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['listStudies'] });
    },
  });
};

export const useDeleteStudy = () => {
  const cohereClient = useCohereClient();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (request: { agentId: string }) => {
      try {
        return await cohereClient.deleteStudy(request);
      } catch (e) {
        console.error(e);
        throw e;
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['listStudies'] });
    },
  });
};

export const useStudy = ({ studyId }: { studyId?: string }) => {
  const cohereClient = useCohereClient();
  return useQuery({
    queryKey: ['study', studyId],
    queryFn: async () => {
      try {
        if (!studyId) {
          throw new Error('must have study id');
        }
        return await cohereClient.getStudy(studyId);
      } catch (e) {
        console.error(e);
        throw e;
      }
    },
  });
};


/**
 * @description Returns a function to check if an agent name is unique.
 */
export const useIsStudyNameUnique = () => {
  const { data: studies } = useListStudies();
  return (name: string, omittedStudyId?: string) => {
    return studies
      ?.filter((study) => study.id !== omittedStudyId)
      .some((study) => study.name === name);
  };
};

export const useUpdateStudy = () => {
  const cohereClient = useCohereClient();
  const queryClient = useQueryClient();
  return useMutation<StudyPublic, ApiError, { request: UpdateStudyRequest; studyId: string }>({
    mutationFn: ({ request, studyId }) => cohereClient.updateStudy(request, studyId),
    onSettled: (study) => {
      queryClient.invalidateQueries({ queryKey: ['study', study?.id] });
      queryClient.invalidateQueries({ queryKey: ['listStudies'] });
    },
  });
};
