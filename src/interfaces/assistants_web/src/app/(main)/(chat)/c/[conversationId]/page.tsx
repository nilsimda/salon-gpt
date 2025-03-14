import { HydrationBoundary, QueryClient, dehydrate } from '@tanstack/react-query';
import { NextPage } from 'next';

import Chat from '@/app/(main)/(chat)/Chat';
import { BASE_AGENT } from '@/constants';
import { getSalonServerClient } from '@/server/salonServerClient';

type Props = {
  params: {
    conversationId: string;
  };
  searchParams: Record<string, string>;
};

const Page: NextPage<Props> = async ({ params }) => {
  const salonServerClient = getSalonServerClient();
  const queryClient = new QueryClient();

  await Promise.all([
    queryClient.prefetchQuery({
      queryKey: ['conversation', params.conversationId],
      queryFn: async () =>
        salonServerClient.getConversation({ conversationId: params.conversationId }),
    }),
    queryClient.prefetchQuery({
      queryKey: ['agent', null],
      queryFn: () => BASE_AGENT,
    }),
  ]);

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <Chat conversationId={params.conversationId} />
    </HydrationBoundary>
  );
};

export default Page;
