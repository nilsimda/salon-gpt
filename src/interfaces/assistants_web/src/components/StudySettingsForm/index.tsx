import { useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

import { CreateStudyRequest, UpdateStudyRequest } from '@/cohere-client';
import { Button, CollapsibleSection } from '@/components/UI';
import { DefineStudyStep } from './DefineStep';
import { InterviewsStep } from './InterviewsStep';
import { VisibilityStep } from './VisibilityStep';
import { cn } from '@/utils';

type RequiredAndNotNull<T> = {
  [P in keyof T]-?: Exclude<T[P], null | undefined>;
};

type RequireAndNotNullSome<T, K extends keyof T> = RequiredAndNotNull<Pick<T, K>> & Omit<T, K>;

type CreateStudySettingsFields = RequireAndNotNullSome<
  CreateStudyRequest,
  'name'
>;

type UpdateStudySettingsFields = RequireAndNotNullSome<
  UpdateStudyRequest,
  'name'
> & { is_private?: boolean };

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

  const [currentStep, setCurrentStep] = useState<'define' | 'interviews' | 'visibility' | undefined>(
    'define'
  );

  return (
    <div className="flex flex-col space-y-6">
      <CollapsibleSection
        title="Define your study"
        number={1}
        description="What is this study about?"
        isExpanded={currentStep === 'define'}
        setIsExpanded={(expanded) => setCurrentStep(expanded ? 'define' : undefined)}
      >
        <DefineStudyStep
          fields={fields}
          setFields={setFields}
          isNewStudy={source === 'create'}
        />
        <StepButtons
          handleNext={() => setCurrentStep('interviews')}
          hide={source !== 'create'}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="Configure interviews"
        number={2}
        description="Specify the number of interviews planned."
        isExpanded={currentStep === 'interviews'}
        setIsExpanded={(expanded) => setCurrentStep(expanded ? 'interviews' : undefined)}
      >
        <InterviewsStep fields={fields} setFields={setFields} />
        <StepButtons
          handleNext={() => setCurrentStep('visibility')}
          handleBack={() => setCurrentStep('define')}
          hide={source !== 'create'}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="Set visibility"
        number={3}
        description="Control who can access this study."
        isExpanded={currentStep === 'visibility'}
        setIsExpanded={(expanded) => setCurrentStep(expanded ? 'visibility' : undefined)}
      >
        <VisibilityStep
          isPrivate={Boolean(fields.is_private)}
          setIsPrivate={(isPrivate) => setFields({ ...fields, is_private: isPrivate })}
        />
        <StepButtons
          handleNext={onSubmit}
          handleBack={() => setCurrentStep('interviews')}
          nextLabel="Create"
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
}> = ({ handleNext, handleBack, nextLabel = 'Next', isSubmit = false, disabled = false, hide = false }) => {
  return (
    <div
      className={cn('flex w-full items-center justify-between pt-5', {
        'justify-end': !handleBack,
        hidden: hide,
      })}
    >
      <Button
        label="Back"
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