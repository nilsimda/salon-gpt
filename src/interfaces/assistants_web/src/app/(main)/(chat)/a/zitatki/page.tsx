import { NextPage } from 'next';

import Chat from '@/app/(main)/(chat)/Chat';

const Page: NextPage = async () => {
  return <Chat agentName="zitatki" />;
};

export default Page;
