import { StudySettingsFields } from '.';
import { Input, Textarea } from '@/components/UI';

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
        placeholder="e.g., Customer Feedback Study 2024"
        value={fields.name}
        onChange={(e) => setFields({ ...fields, name: e.target.value })}
      />
      <Textarea
        label="Description"
        placeholder="e.g., Research study to gather customer feedback on our new product features."
        defaultRows={4}
        value={fields.description ?? ''}
        onChange={(e) => setFields({ ...fields, description: e.target.value })}
      />
    </div>
  );
};