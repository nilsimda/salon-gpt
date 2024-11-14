import { DragDropFileInput, Input, Text, Textarea } from '@/components/UI';

import { StudySettingsFields } from '.';

type Props = {
  fields: StudySettingsFields;
  isNewStudy: boolean;
  setFields: (fields: StudySettingsFields) => void;
};

export const DefineStudyStep: React.FC<Props> = ({ fields, setFields }) => {
  return (
    <div className="flex flex-col space-y-4">
      <Input
        label="Name"
        placeholder="z.B., Jack Daniels"
        value={fields.name}
        onChange={(e) => setFields({ ...fields, name: e.target.value })}
      />
      <Textarea
        label="Beschreibung"
        placeholder="z.B., eine Studie über die Marktgröße von Whiskey"
        defaultRows={4}
        value={fields.description ?? ''}
        onChange={(e) => setFields({ ...fields, description: e.target.value })}
      />
      <Text className="text-sm text-gray-500">Füge eine Infotabelle hinzu.</Text>
      <DragDropFileInput
        accept={[
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
          'application/vnd.ms-excel',
        ]}
        onFilesChange={(files) => setFields({ ...fields, files })}
      />
    </div>
  );
};
