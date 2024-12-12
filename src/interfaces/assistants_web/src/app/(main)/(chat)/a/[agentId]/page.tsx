import { NextPage } from 'next';

import Chat from '@/app/(main)/(chat)/Chat';

type Props = {
  params: {
    agentId: string;
  };
  searchParams: Record<string, string>;
};

const Page: NextPage<Props> = async ( {params} ) => {
  return <Chat agentName={params.agentId} />;
};

export default Page;
