'use client';

import { useMemo, useState } from 'react';
import { Flipped, Flipper } from 'react-flip-toolkit';

import {
  AgentIcon,
  ConversationListLoading,
  ConversationListPanelGroup,
} from '@/components/SideNavPanel';
import { Icon, InputSearch, Text, Tooltip } from '@/components/UI';
import { useConversations, useSearchConversations } from '@/hooks';
import { ConversationWithoutMessages as Conversation } from '@/salon-client';
import { useSettingsStore } from '@/stores';
import { cn } from '@/utils';

const sortByDate = (a: Conversation, b: Conversation) => {
  return Date.parse(b.updated_at ?? '') - Date.parse(a.updated_at ?? '');
};

/**
 * @description This component renders a list of agents.
 * It shows the most recent agents and the base agents.
 */
export const ConversationList: React.FC = () => {
  const { isLeftPanelOpen } = useSettingsStore();
  const { data: conversations = [] } = useConversations({ orderBy: 'is_pinned' });
  const { search, setSearch, searchResults } = useSearchConversations(conversations);

  return (
    <>
      <div className="flex flex-col gap-8">
        <Search searchQuery={search} setSearchQuery={setSearch} />
      </div>
      <div
        className={cn('flex-grow', {
          'overflow-y-auto': conversations.length > 0,
          'space-y-4': isLeftPanelOpen,
          '> *:not(:first-child) space-y-2': !isLeftPanelOpen,
        })}
      >
        <Chats searchQuery={search} searchResults={searchResults} conversations={conversations} />
      </div>
    </>
  );
};

const Search: React.FC<{
  searchQuery: string;
  setSearchQuery: (value: string) => void;
}> = ({ searchQuery, setSearchQuery }) => {
  const { isLeftPanelOpen, setLeftPanelOpen } = useSettingsStore();

  return (
    <section className={cn('flex flex-col gap-4', { 'items-center': !isLeftPanelOpen })}>
      {isLeftPanelOpen ? (
        <InputSearch
          placeholder="Chats durchsuchen"
          value={searchQuery}
          onChange={setSearchQuery}
          maxLength={40}
        />
      ) : (
        <Tooltip label="Search" hover size="sm">
          <button onClick={() => setLeftPanelOpen(true)}>
            <Icon name="search" kind="outline" className="dark:fill-marble-950" />
          </button>
        </Tooltip>
      )}
    </section>
  );
};

const Chats: React.FC<{
  searchQuery: string;
  searchResults: Conversation[];
  conversations: Conversation[];
}> = ({ searchQuery, searchResults, conversations }) => {
  const { isLeftPanelOpen } = useSettingsStore();
  const { isLoading, isError } = useConversations({ orderBy: 'is_pinned' });
  const [checkedConversations, setCheckedConversations] = useState<Set<string>>(new Set());

  const handleCheckConversationToggle = (id: string) => {
    const newCheckedConversations = new Set(checkedConversations);
    if (!newCheckedConversations.delete(id)) {
      newCheckedConversations.add(id);
    }
    setCheckedConversations(newCheckedConversations);
  };

  const [pinnedConversations, recentConversations] = useMemo(() => {
    const filteredConversations = searchQuery ? searchResults : conversations.sort(sortByDate);
    return [
      filteredConversations.filter((c) => c.is_pinned),
      filteredConversations.filter((c) => !c.is_pinned),
    ];
  }, [searchQuery, searchResults, conversations]);

  if (isLoading) {
    return <ConversationListLoading />;
  }

  if (isError && isLeftPanelOpen) {
    return (
      <span className="my-auto flex flex-col items-center gap-2 text-center">
        <Icon name="warning" />
        <Text>Konversationen konnten nicht geladen werden.</Text>
      </span>
    );
  }

  if (searchQuery && !searchResults.length && isLeftPanelOpen) {
    return (
      <Text as="span" className="line-clamp-3">
        Keine Ergebnisse für &quot;{searchQuery}&quot; gefunden.
      </Text>
    );
  }

  if (!conversations.length && isLeftPanelOpen) {
    return (
      <span className="flex h-full w-full items-center justify-center text-volcanic-500">
        <Text>Hier ist es ruhig... fürs Erste.</Text>
      </span>
    );
  }

  return (
    <>
      {pinnedConversations.length > 0 && (
        <ChatsGroup
          title="Angeheftete Chats"
          conversations={pinnedConversations}
          showWeekHeadings={false}
          checkedConversations={checkedConversations}
          handleCheckConversationToggle={handleCheckConversationToggle}
        />
      )}
      {recentConversations.length > 0 && (
        <ChatsGroup
          title="Zuletzt verwendete Chats"
          conversations={recentConversations}
          showWeekHeadings={!searchQuery.length && isLeftPanelOpen}
          checkedConversations={checkedConversations}
          handleCheckConversationToggle={handleCheckConversationToggle}
        />
      )}
    </>
  );
};

const ChatsGroup: React.FC<{
  title: string;
  conversations: Conversation[];
  showWeekHeadings: boolean;
  checkedConversations: Set<string>;
  handleCheckConversationToggle: (id: string) => void;
}> = ({
  title,
  conversations,
  showWeekHeadings,
  checkedConversations,
  handleCheckConversationToggle,
}) => {
  const { isLeftPanelOpen } = useSettingsStore();

  return (
    <>
      {isLeftPanelOpen && (
        <Text styleAs="label" className="truncate dark:text-mushroom-800">
          {title}
        </Text>
      )}
      <ConversationListPanelGroup
        conversations={conversations}
        showWeekHeadings={showWeekHeadings}
        checkedConversations={checkedConversations}
        onCheckConversation={handleCheckConversationToggle}
        className={cn('flex flex-col items-center space-y-1', { 'space-y-2': !isLeftPanelOpen })}
      />
    </>
  );
};
