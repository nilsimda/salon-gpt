import { StudySettingsFields } from '.';
import { Input, Text } from '@/components/UI';

type Props = {
  fields: StudySettingsFields;
  setFields: (fields: StudySettingsFields) => void;
};

export const InterviewsStep: React.FC<Props> = ({ fields, setFields }) => {
  return (
    <div className="flex flex-col space-y-6">
      <div className="flex flex-col space-y-4">
        <Input
          type="text"
          label="Individual Interviews"
          placeholder="0"
          value={fields.individual_interview_count?.toString() ?? '0'}
          onChange={(e) =>
            setFields({ ...fields, individual_interview_count: parseInt(e.target.value) || 0 })
          }
        />
        <Text className="text-sm text-gray-500">
          Number of one-on-one interviews planned for this study
        </Text>
      </div>
      
      <div className="flex flex-col space-y-4">
        <Input
          type="text"
          label="Group Interviews"
          placeholder="0"
          value={fields.group_interview_count?.toString() ?? '0'}
          onChange={(e) =>
            setFields({ ...fields, group_interview_count: parseInt(e.target.value) || 0 })
          }
        />
        <Text className="text-sm text-gray-500">
          Number of group interviews or focus groups planned for this study
        </Text>
      </div>
    </div>
  );
};