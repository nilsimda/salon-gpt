'use client';

import { useRouter } from 'next/navigation';

import { Button, Text } from '@/components/UI';
import { useChatRoutes, useDeleteStudy } from '@/hooks';

type Props = {
  name: string;
  studyId: string;
  onClose: () => void;
};

/**
 * @description This component renders a confirmation dialog to delete a study.
 */
export const DeleteStudy: React.FC<Props> = ({ name, studyId, onClose }) => {
  const { mutateAsync: deleteStudy, isPending } = useDeleteStudy();
  const { studyId: currentStudyId } = useChatRoutes();
  const router = useRouter();

  const handleDeleteStudy = async () => {
    await deleteStudy({ studyId });
    onClose();
    //if (studyId === currentStudyId) {
     // router.push('/', undefined);
    //}
  };

  return (
    <div className="flex flex-col gap-y-20">
      <Text>
        Die Studie <strong>{name}</strong> wird unwiderruflich gelöscht.
      </Text>
      <div className="flex justify-between">
        <Button label="Cancel" kind="secondary" onClick={onClose} />
        <Button
          label={isPending ? 'Deleting' : 'Delete'}
          onClick={handleDeleteStudy}
          disabled={isPending}
          icon="arrow-right"
          theme="coral"
          iconPosition="end"
        />
      </div>
    </div>
  );
};
