'use client';

import { PropsWithChildren, useState } from 'react';

import { MobileHeader } from '@/components/Global';
import { Button, DarkModeToggle, Icon, Tabs, Text } from '@/components/UI';
import { cn } from '@/utils';

const tabs = [
  <div className="flex items-center gap-2" key="company">
    <Icon name="sun" kind="outline" />
    <Text>Aussehen</Text>
  </div>,
  <div className="flex items-center gap-2" key="private">
    <Icon name="profile" kind="outline" />
    <Text>Profil</Text>
  </div>,
];

export const Settings = () => {
  const [selectedTabIndex, setSelectedTabIndex] = useState(0);

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
        <div className="flex items-center gap-2">
          <Text styleAs="h4" className="text-volcanic-400 dark:text-mushroom-950">
            Einstellungen
          </Text>
        </div>
      </header>
      <section className="p-8">
        <Tabs
          tabs={tabs}
          selectedIndex={selectedTabIndex}
          onChange={setSelectedTabIndex}
          tabGroupClassName="h-full"
          tabClassName="pt-2.5"
          panelsClassName="pt-7 lg:pt-7 px-0 flex flex-col rounded-b-lg md:rounded-b-none"
          fitTabsContent
        >
          <Appearance />
          <Profile />
        </Tabs>
      </section>
    </div>
  );
};

const Wrapper: React.FC<PropsWithChildren> = ({ children }) => (
  <div className="max-w-screen-xl flex-grow overflow-y-auto">{children}</div>
);

const Profile = () => {
  return (
    <Wrapper>
      <Button label="Ausloggen" href="/logout" kind="secondary" icon="sign-out" theme="default" />
    </Wrapper>
  );
};

const Appearance = () => {
  return (
    <Wrapper>
      <Text styleAs="h5" className="mb-6">
        Appearance
      </Text>
      <DarkModeToggle />
    </Wrapper>
  );
};
