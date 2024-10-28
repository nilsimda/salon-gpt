'use client';

import { cloneDeep } from 'lodash';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';

import { MobileHeader } from '@/components/Global';
import { Button, Icon, Text } from '@/components/UI';
import { useContextStore } from '@/context';
import { useCreateStudy, useNotify } from '@/hooks';

const DEFAULT_FIELD_VALUES = {
  name: '',
  description: '',
  is_private: false,
};

/**
 * @description Form to create a new study.
 */
export const CreateStudy: React.FC = () => {
  const router = useRouter();
  const { open, close } = useContextStore();
  const { error } = useNotify();
  const { mutateAsync: createStudy } = useCreateStudy();

  const [fields, setFields] = useState(cloneDeep(DEFAULT_FIELD_VALUES));
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleOpenSubmitModal = () => {
    if (fields.is_private) {
      handleSubmit();
      return;
    }

    open({
      title: `Create ${fields.name}?`,
      content: (
        <SubmitModalContent
          studyName={fields.name}
          onSubmit={handleSubmit}
          isSubmitting={isSubmitting}
          onClose={close}
        />
      ),
    });
  };

  const handleSubmit = async () => {
    try {
      setIsSubmitting(true);
      const study = await createStudy(fields);
      close();
      router.push(`/studies/${study.id}`);
    } catch (e) {
      setIsSubmitting(false);
      close();
      error('Failed to create study');
      console.error(e);
    }
  };

  return (
    <div className="flex h-full w-full flex-col overflow-y-auto rounded-lg border border-marble-950 bg-marble-980 pb-6 dark:border-volcanic-100 dark:bg-volcanic-100">
      <header className="flex flex-col gap-y-3 border-b px-4 py-6 dark:border-volcanic-150 lg:px-10 lg:py-10">
        <MobileHeader />
        <div className="flex items-center space-x-2">
          <Link href="/studies">
            <Text className="dark:text-volcanic-600">Explore studies</Text>
          </Link>
          <Icon name="chevron-right" className="dark:text-volcanic-600" />
          <Text className="dark:text-volcanic-600">Create study</Text>
        </div>
        <Text styleAs="h4">Create study</Text>
      </header>
      <div className="flex flex-grow flex-col gap-y-8 overflow-y-hidden px-8 pt-8">
        <div className="flex-grow overflow-y-auto">
          <StudySettingsForm
            source="create"
            fields={fields}
            setFields={setFields}
            onSubmit={handleOpenSubmitModal}
          />
        </div>
      </div>
    </div>
  );
};

const SubmitModalContent: React.FC<{
  studyName: string;
  isSubmitting: boolean;
  onSubmit: () => void;
  onClose: () => void;
}> = ({ studyName, isSubmitting, onSubmit, onClose }) => (
  <div className="flex flex-col gap-y-20">
    <Text>
      Your study {studyName} is about be visible publicly. Everyone in your organization will be
      able to see and use it.
    </Text>
    <div className="flex justify-between">
      <Button label="Cancel" kind="secondary" onClick={onClose} />
      <Button
        label={isSubmitting ? 'Creating study' : 'Yes, make it public'}
        onClick={onSubmit}
        icon="arrow-right"
        iconPosition="end"
        disabled={isSubmitting}
      />
    </div>
  </div>
);
