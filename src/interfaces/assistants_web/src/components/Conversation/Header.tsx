'use client';

import { Button, Icon, IconButton, Logo, Text } from '@/components/UI';
import { useContextStore } from '@/context';
import { env } from '@/env.mjs';
import { useBrandedColors } from '@/hooks';
import { useConversationStore, useSettingsStore } from '@/stores';
import { cn } from '@/utils';

type Props = {
  agentName: string;
};

export const Header: React.FC<Props> = ({ agentName }) => {
  console.log('Header re-rendered with agentName:', agentName);
  const {
    conversation: { id },
  } = useConversationStore();
  const { setLeftPanelOpen, setRightPanelOpen } = useSettingsStore();
  const { open } = useContextStore();
  const { text, bg, contrastText, lightText, fill, lightFill, dark, light } = useBrandedColors('');

  const handleOpenLeftSidePanel = () => {
    setRightPanelOpen(false);
    setLeftPanelOpen(true);
  };

  const handleOpenRightSidePanel = () => {
    setLeftPanelOpen(false);
    setRightPanelOpen(true);
  };

  return (
    <div className="flex h-header w-full min-w-0 items-center">
      <div className="flex w-full flex-1 items-center justify-between px-6">
        <div className="flex items-center gap-4">
          <button
            onClick={handleOpenLeftSidePanel}
            className="flex h-full items-center gap-4 lg:hidden"
          >
            <Logo hasCustomLogo={env.NEXT_PUBLIC_HAS_CUSTOM_LOGO} includeBrandName={false} />
            <Text className="truncate dark:text-mushroom-950" styleAs="p-lg" as="span">
              {agentName}
            </Text>
          </button>
        </div>
        <section className="flex items-center gap-4">
          {id && (
            <Button
              kind="secondary"
              className="[&>div]:gap-x-0 lg:[&>div]:gap-x-3"
              label={
                <Text className={cn(dark(lightText), light(text), 'hidden lg:flex')}>Teilen</Text>
              }
              iconOptions={{
                customIcon: (
                  <Icon name="share" kind="outline" className={cn(light(fill), dark(lightFill))} />
                ),
              }}
              iconPosition="start"
            />
          )}
          <IconButton
            iconName="kebab"
            iconClassName="dark:fill-marble-950 fill-volcanic-100"
            onClick={handleOpenRightSidePanel}
            className="flex h-auto w-auto lg:hidden"
          />
        </section>
      </div>
    </div>
  );
};
