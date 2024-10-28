import { Metadata } from 'next';

import { CreateStudy } from './CreateStudy';

export const metadata: Metadata = {
  title: 'Neue Studie',
};

const NewStudyPage: React.FC = () => {
  return <CreateStudy />;
};

export default NewStudyPage;
