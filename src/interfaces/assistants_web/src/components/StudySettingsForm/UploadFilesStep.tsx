import { DragDropFileInput, Text } from '@/components/UI';
import { useConversationFileActions } from '@/hooks/use-files';

import { StudySettingsFields } from '.';

type Props = {
  fields: StudySettingsFields;
  setFields: (fields: StudySettingsFields) => void;
};

export const UploadFilesStep: React.FC<Props> = ({ fields, setFields }) => {
  const { uploadFiles } = useConversationFileActions();
  return (
    <div className="flex flex-col space-y-6">
      <div className="flex flex-col space-y-4">
        <Text className="text-lg font-medium">Audio oder Video Dateien hochladen</Text>

        <DragDropFileInput
          active={true}
          accept={['video/*', 'audio/*']}
          onUploadFile={async (files) => {
            await uploadFiles(files, fields.id);
          }}
        />
      </div>
    </div>
  );
};
