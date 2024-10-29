import { Metadata } from 'next';

import { DiscoverStudy } from './DiscoverStudy';

export const metadata: Metadata = {
  title: 'Studie hinzufügen',
};

const DiscoverStudyPage: React.FC = () => {
  return <DiscoverStudy />;
};

export default DiscoverStudyPage;
