import { useMutation, useQueryClient } from '@tanstack/react-query';

import { GenerateTitleResponse, useSalonClient } from '@/salon-client';

export const useUpdateConversationTitle = () => {
  const salonClient = useSalonClient();
  const queryClient = useQueryClient();
  return useMutation<GenerateTitleResponse, Error, string>({
    mutationFn: (conversationId) => salonClient.generateTitle({ conversationId }),
    onSettled: () => queryClient.invalidateQueries({ queryKey: ['conversations'] }),
    retry: 1,
  });
};
