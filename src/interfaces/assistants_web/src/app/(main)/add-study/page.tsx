import { Metadata } from 'next';

import { AddStudy } from './AddStudy';

export const metadata: Metadata = {
  title: 'Studie hinzufügen',
};

const AddStudyPage: React.FC = () => {
  return <AddStudy />;
};

export default AddStudyPage;
