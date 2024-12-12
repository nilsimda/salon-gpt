import { NextPage } from 'next';

import { getCohereServerClient } from '@/server/salonServerClient';

import { UpdateAgent } from './UpdateAgent';

type Props = {
  params: {
    agentId: string;
  };
  searchParams: Record<string, string>;
};

const Page: NextPage<Props> = async ({ params }) => {
  const salonServerClient = getCohereServerClient();
  const agent = await salonServerClient.getAgent(params.agentId);

  return <UpdateAgent agent={agent} />;
};

export default Page;
