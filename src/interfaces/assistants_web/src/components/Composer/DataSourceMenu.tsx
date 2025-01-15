'use client';

import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react';
import React from 'react';

import { Icon, Switch, Text } from '@/components/UI';
import { useBrandedColors, useListStudies } from '@/hooks';
import { Study } from '@/salon-client';
import { useParamsStore } from '@/stores';
import { cn } from '@/utils';
import { BASE_AGENT } from '@/constants';

export type Props = {
  agentName?: string;
};

/**
 * @description Displays a list of available studies
 */
export const DataSourceMenu: React.FC<Props> = ({ agentName }) => {
  const { data: studies } = useListStudies();
  const { text, contrastText, border, bg } = useBrandedColors(agentName);
  const isBaseAgent = agentName === BASE_AGENT;

  const {
    setParams,
    params: { study_id },
  } = useParamsStore();

  const handleSelectStudy = (study: Study) => {
    setParams({ study_id: study.id });
  };

  return (
    <Popover className="relative">
      <PopoverButton
        as="button"
        className={({ open }) =>
          cn(
            'flex items-center justify-center rounded border px-1.5 py-1 outline-none transition-colors',
            border,
            { [bg]: open }
          )
        }
      >
        {({ open }) => (
          <Text
            styleAs="label"
            as="span"
            className={cn('font-medium', text, { [contrastText]: open })}
          >
            Studie: {studies?.filter(studies => studies.id === study_id)[0]?.name}
          </Text>
        )}
      </PopoverButton>
      <PopoverPanel
        className="flex min-w-[200px] origin-top -translate-y-2 flex-col transition duration-200 ease-out data-[closed]:scale-95 data-[closed]:opacity-0"
        anchor="top start"
        transition
      >
        <div
          className={cn(
            'z-tag-suggestions flex flex-col',
            'w-full rounded-md p-2 focus:outline-none',
            'bg-mushroom-950 dark:bg-volcanic-150'
          )}
        >
          <Text styleAs="label" className="mb-2 text-mushroom-300 dark:text-marble-800">
            Hinzugefügte Studien
          </Text>
          {studies?.length === 0 && (
            <Text as="span" styleAs="caption" className="text-mushroom-400 dark:text-volcanic-500">
              Keine Studien hinzugefügt
            </Text>
          )}
          {studies?.map((study, i) => (
            <div
              key={study.id}
              className={cn(
                'flex w-full items-start justify-between gap-x-2 px-1.5 py-3',
                'focus:outline focus:outline-volcanic-300',
                {
                  'border-b border-mushroom-800 dark:border-volcanic-300 md:w-[300px]':
                    i !== studies?.length - 1,
                }
              )}
            >
              <div className="flex flex-1 justify-between gap-x-2">
                <div className="flex gap-x-2">
                  <div className="relative flex items-center justify-center rounded bg-mushroom-800 p-1 dark:bg-volcanic-200">
                    <Icon
                      name="circles-four"
                      kind="outline"
                      size="sm"
                      className="flex items-center fill-mushroom-300 dark:fill-marble-800"
                    />
                    <div
                      className={cn(
                        'absolute -bottom-0.5 -right-0.5  size-2 rounded-full transition-colors duration-300',
                        {
                          'bg-success-300': study_id === study.id,
                          'bg-mushroom-400 dark:bg-volcanic-600': study_id !== study.id,
                        }
                      )}
                    />
                  </div>
                  <div className="flex flex-col text-left">
                    <Text as="span">{study.name}</Text>
                  </div>
                </div>
                {isBaseAgent && (
                  <Switch
                    theme="evolved-blue"
                    checked={study.id === study_id}
                    onChange={() => handleSelectStudy(study)}
                    showCheckedState
                  />
                )}
              </div>
            </div>
          ))}
        </div>
      </PopoverPanel>
    </Popover>
  );
};
