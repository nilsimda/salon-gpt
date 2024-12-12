import { NextPage } from 'next';

import Chat from '@/app/(main)/(chat)/Chat';

const Page: NextPage = async () => {
  return <Chat agentName="kerlin" />;
};

export default Page;
