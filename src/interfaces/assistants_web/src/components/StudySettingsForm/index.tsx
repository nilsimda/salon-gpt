import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

import { CreateStudyRequest, UpdateStudyRequest } from '@/cohere-client';
import { Button, CollapsibleSection } from '@/components/UI';
import { cn } from '@/utils';

import { DefineStudyStep } from './DefineStep';
import { UploadFilesStep } from './UploadFilesStep';

type RequiredAndNotNull<T> = {
  [P in keyof T]-?: Exclude<T[P], null | undefined>;
};

type RequireAndNotNullSome<T, K extends keyof T> = RequiredAndNotNull<Pick<T, K>> & Omit<T, K>;

type CreateStudySettingsFields = RequireAndNotNullSome<CreateStudyRequest, 'name'>;

type UpdateStudySettingsFields = RequireAndNotNullSome<UpdateStudyRequest, 'name'> & {
  is_private?: boolean;
};

export type StudySettingsFields = CreateStudySettingsFields | UpdateStudySettingsFields;

type BaseProps = {
  fields: StudySettingsFields;
  setFields: (fields: StudySettingsFields) => void;
  onSubmit: VoidFunction;
};

type CreateProps = BaseProps & {
  source: 'create';
};

type UpdateProps = BaseProps & {
  source: 'update';
  studyId: string;
};

export type Props = CreateProps | UpdateProps;

export const StudySettingsForm: React.FC<Props> = (props) => {
  const { source = 'create', fields, setFields, onSubmit } = props;
  const studyId = 'studyId' in props ? props.studyId : undefined;
  const params = useSearchParams();
  const defaultState = params.has('state');

  useEffect(() => {
    if (defaultState) {
      const state = params.get('state');
      if (state) {
        try {
          const fields = JSON.parse(atob(state));
          setFields(fields);
        } catch {
          console.error('Error parsing state');
        }
      }
    }
  }, [defaultState, params, setFields]);

  const [currentStep, setCurrentStep] = useState<
    'define' | 'tiefeninterviews' | 'groupDiscussions' | 'memos' | undefined
  >('define');

  return (
    <div className="flex flex-col space-y-6">
      <CollapsibleSection
        title="Studieninformation"
        number={1}
        description="Worum geht es in dieser Studie?"
        isExpanded={currentStep === 'define'}
        setIsExpanded={(expanded) => setCurrentStep(expanded ? 'define' : undefined)}
      >
        <DefineStudyStep fields={fields} setFields={setFields} isNewStudy={source === 'create'} />
        <StepButtons
          handleNext={() => setCurrentStep('tiefeninterviews')}
          hide={source !== 'create'}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="Tiefeninterviews"
        number={2}
        description="Füge Tiefeninterviews hinzu."
        isExpanded={currentStep === 'tiefeninterviews'}
        setIsExpanded={(expanded) => setCurrentStep(expanded ? 'tiefeninterviews' : undefined)}
      >
        <UploadFilesStep fields={fields} setFields={setFields} />
        <StepButtons
          handleNext={() => setCurrentStep('groupDiscussions')}
          handleBack={() => setCurrentStep('define')}
          hide={source !== 'create'}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="Gruppendiskussionen"
        number={3}
        description="Füge Gruppendiskussionen hinzu."
        isExpanded={currentStep === 'groupDiscussions'}
        setIsExpanded={(expanded) => setCurrentStep(expanded ? 'groupDiscussions' : undefined)}
      >
        <UploadFilesStep fields={fields} setFields={setFields} />
        <StepButtons
          handleNext={() => setCurrentStep('memos')}
          handleBack={() => setCurrentStep('tiefeninterviews')}
          hide={source !== 'create'}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="Memos"
        number={4}
        description="Füge Memos hinzu."
        isExpanded={currentStep === 'memos'}
        setIsExpanded={(expanded) => setCurrentStep(expanded ? 'memos' : undefined)}
      >
        <UploadFilesStep fields={fields} setFields={setFields} />
        <StepButtons
          handleNext={onSubmit}
          handleBack={() => setCurrentStep('groupDiscussions')}
          nextLabel="Erstellen"
          isSubmit
          hide={source !== 'create'}
        />
      </CollapsibleSection>
    </div>
  );
};

const StepButtons: React.FC<{
  handleNext: VoidFunction;
  handleBack?: VoidFunction;
  nextLabel?: string;
  isSubmit?: boolean;
  disabled?: boolean;
  hide?: boolean;
}> = ({
  handleNext,
  handleBack,
  nextLabel = 'Weiter',
  isSubmit = false,
  disabled = false,
  hide = false,
}) => {
  return (
    <div
      className={cn('flex w-full items-center justify-between pt-5', {
        'justify-end': !handleBack,
        hidden: hide,
      })}
    >
      <Button
        label="Zurück"
        kind="secondary"
        onClick={handleBack}
        className={cn({ hidden: !handleBack })}
      />
      <div className="flex items-center gap-4">
        <Button
          label={nextLabel}
          theme="default"
          kind="cell"
          icon={isSubmit ? 'checkmark' : 'arrow-right'}
          disabled={disabled}
          onClick={handleNext}
        />
      </div>
    </div>
  );
};
