import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import {
  ApiError,
  CreateStudyRequest,
  Study,
  UpdateStudyRequest,
  useSalonClient,
} from '@/salon-client';

export const useListStudies = () => {
  const salonClient = useSalonClient();
  return useQuery({
    queryKey: ['listStudies'],
    queryFn: async () => {
      return await salonClient.listStudies({});
    },
  });
};

export const useCreateStudy = () => {
  const salonClient = useSalonClient();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (request: CreateStudyRequest) => salonClient.createStudy(request),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['listStudies'] });
    },
  });
};

export const useDeleteStudy = () => {
  const salonClient = useSalonClient();
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (request: { agentId: string }) => {
      try {
        return await salonClient.deleteStudy(request);
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
  const salonClient = useSalonClient();
  return useQuery({
    queryKey: ['study', studyId],
    queryFn: async () => {
      try {
        if (!studyId) {
          throw new Error('must have study id');
        }
        return await salonClient.getStudy(studyId);
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
  const salonClient = useSalonClient();
  const queryClient = useQueryClient();
  return useMutation<Study, ApiError, { request: UpdateStudyRequest; studyId: string }>({
    mutationFn: ({ request, studyId }) => salonClient.updateStudy(request, studyId),
    onSettled: (study) => {
      queryClient.invalidateQueries({ queryKey: ['study', study?.id] });
      queryClient.invalidateQueries({ queryKey: ['listStudies'] });
    },
  });
};
