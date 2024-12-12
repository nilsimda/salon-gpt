import { NextPage } from 'next';

import Chat from '@/app/(main)/(chat)/Chat';
import { BASE_AGENT } from '@/constants';

const Page: NextPage = async () => {
  return <Chat agentName={BASE_AGENT} />;
};

export default Page;
