'use client';

import Link from 'next/link';

import { Study } from '@/salon-client';
import { DeleteStudy } from '@/components/Modals/DeleteStudy';
import { KebabMenu, Text } from '@/components/UI';
import { useContextStore } from '@/context';

type Props = {
  study?: Study;
};

/**
 * @description renders a card for a study with the study's name, description
 */
export const DiscoverStudyCard: React.FC<Props> = ({ study }) => {
  const createdBy = 'RHEINGOLD SALON';

  const { open, close } = useContextStore();
  const handleOpenDeleteModal = () => {
    if (!study) return;
    open({
      title: `Delete ${study.name}`,
      content: <DeleteStudy name={study.name} studyId={study.id} onClose={close} />,
    });
  };

  return (
    <Link
      className="flex overflow-x-hidden rounded-lg border border-volcanic-800 bg-volcanic-950 p-4 transition-colors duration-300 hover:bg-marble-950 dark:border-volcanic-300 dark:bg-volcanic-150 dark:hover:bg-volcanic-100"
      href={`/study/${study?.id}`}
    >
      <div className="flex h-full flex-grow flex-col items-start gap-y-2 overflow-x-hidden">
        <div className="flex w-full items-center gap-x-2">
          <div className="relative flex h-8 w-8 flex-shrink-0 items-center justify-center rounded bg-volcanic-800 duration-300">
            {/* You might want to add a study icon/logo here */}
          </div>
          <Text as="h5" className="truncate dark:text-mushroom-950" title={study?.name}>
            {study?.name}
          </Text>
          <div className="ml-auto">
            <KebabMenu
              anchor="right start"
              items={[
                {
                  iconName: 'edit',
                  label: 'Edit study',
                  href: `/study/edit/${study?.id}`,
                },
                {
                  iconName: 'trash',
                  label: 'Delete study',
                  iconClassName: 'fill-danger-500 dark:fill-danger-500',
                  onClick: handleOpenDeleteModal,
                },
              ]}
            />
          </div>
        </div>
        <Text className="line-clamp-2 flex-grow dark:text-mushroom-800">{study?.description}</Text>
        <Text className="dark:text-volcanic-500">BY {createdBy}</Text>
      </div>
    </Link>
  );
};
