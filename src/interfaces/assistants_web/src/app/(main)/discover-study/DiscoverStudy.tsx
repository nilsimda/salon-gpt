'use client';

import { useDeferredValue, useMemo, useState } from 'react';

import { AgentPublic, ConversationWithoutMessages } from '@/cohere-client';
import { MobileHeader } from '@/components/Global';
import { Button, Input, Text } from '@/components/UI';
import { useListStudies, useSession} from '@/hooks';
import { cn } from '@/utils';

import { DiscoverStudyCard } from './DiscoverStudyCard';

const GROUPED_ASSISTANTS_LIMIT = 15;

export const DiscoverStudy = () => {
  const { data: studies = [] } = useListStudies();

  return (
    <div className="flex h-full w-full flex-grow flex-col overflow-y-auto rounded-lg border border-marble-950 bg-marble-980 dark:border-volcanic-100 dark:bg-volcanic-100 md:ml-0">
      <header
        className={cn(
          'border-b border-marble-950 bg-cover dark:border-volcanic-200',
          'px-4 py-6 lg:px-10 lg:py-10',
          'flex flex-col gap-y-3'
        )}
      >
        <MobileHeader />
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Text styleAs="h4" className="text-volcanic-400 dark:text-mushroom-950">
              Alle Studien
            </Text>
          </div>
          <Button
            kind="secondary"
            theme="default"
            icon="add"
            label="Studie hinzufügen"
            href="/new-study"
            className="hidden md:block"
          />
          <Button kind="secondary" theme="default" icon="add" href="/new" className="md:hidden" />
        </div>
      </header>
      <section className="p-8">
        <CompanyStudies studies={studies} />
      </section>
    </div>
  );
};

const GroupAgents: React.FC<{ agents: AgentPublic[]; title: string }> = ({ agents, title }) => {
  const hasShowMore = agents.length > 3;
  const [showMore, setShowMore] = useState(false);
  const handleShowMore = () => setShowMore((prev) => !prev);
  const visibleAgents = showMore ? agents : agents.slice(0, 3);

  return (
    <section className="space-y-6">
      <header>
        <Text styleAs="h5" className="dark:text-marble-1000">
          {title}
        </Text>
      </header>
      <div className="grid grid-cols-1 gap-x-4 gap-y-5 md:grid-cols-3 xl:grid-cols-4">
        {visibleAgents.map((agent) => (
          <DiscoverStudyCard key={agent.id} agent={agent} />
        ))}
      </div>
      {hasShowMore && (
        <Button
          kind="secondary"
          label={showMore ? 'Show less' : 'Show more'}
          theme="marble"
          onClick={handleShowMore}
          icon="chevron-down"
          iconPosition="end"
          iconOptions={{
            className: cn('transform duration-300', {
              'rotate-180': showMore,
            }),
          }}
        />
      )}
    </section>
  );
};

const CompanyStudies: React.FC<{
  studies: StudiesPublic[];
}> = ({ studies }) => {
  const [query, setQuery] = useState('');
  const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => setQuery(e.target.value);
  const deferredQuery = useDeferredValue(query);
  const session = useSession();

  const filteredStudies = useMemo(
    () =>
      studies
        .filter((study) => study.name.toLowerCase().includes(deferredQuery.toLowerCase()))
        .sort((a, b) => b.name.toLowerCase().localeCompare(a.name.toLowerCase())),
    [studies, deferredQuery]
  );

  const createdByMeAgents = useMemo(
    () => filteredStudies.filter((study) => study.user_id === session.userId),
    [filteredStudies, session.userId]
  );

  return (
    <div className="max-w-screen-xl flex-grow overflow-y-auto">
      <div className="space-y-10">
        <Input
          placeholder="Suche nach Studien"
          type="text"
          onChange={handleOnChange}
          value={query}
        />
        <GroupAgents title="Werden hinzugefügt..." agents={createdByMeAgents} />
        <GroupAgents title="Hinzugefügte Studien" agents={filteredStudies} />
      </div>
    </div>
  );
};
