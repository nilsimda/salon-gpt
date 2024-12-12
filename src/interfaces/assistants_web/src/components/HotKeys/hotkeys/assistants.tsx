'use client';

import { useRouter } from 'next/navigation';

import { SwitchAssistants } from '@/components/HotKeys/custom-views/SwitchAssistants';
import { HotKeyGroupOption } from '@/components/HotKeys/domain';

export const useAssistantHotKeys = ({
  displayRecentAgentsInDialog,
}: {
  displayRecentAgentsInDialog: boolean;
}): HotKeyGroupOption[] => {
  const router = useRouter();

  const navigateToAssistants = () => {
    router.push('/discover-agent');
  };

  const navigateToNewAssistant = () => {
    router.push('/new-agent');
  };

  return [
    {
      group: 'Assistants',
      quickActions: [
        {
          name: 'Assistenten wechseln',
          commands: ['ctrl+space+1-5', 'ctrl+space+1-5'],
          displayInDialog: !displayRecentAgentsInDialog,
          customView: ({ isOpen, close, onBack }) => (
            <SwitchAssistants isOpen={isOpen} close={close} onBack={onBack} />
          ),
          closeDialogOnRun: false,
          registerGlobal: false,
          options: {
            preventDefault: true,
          },
        },
        {
          name: 'Alle Assistenten anzeigen',
          action: navigateToAssistants,
          closeDialogOnRun: true,
          commands: [],
          displayInDialog: !displayRecentAgentsInDialog,
          registerGlobal: false,
        },
        {
          name: 'Assistent erstellen',
          action: navigateToNewAssistant,
          closeDialogOnRun: true,
          displayInDialog: !displayRecentAgentsInDialog,
          commands: [],
          registerGlobal: false,
        },
      ],
    },
  ];
};
