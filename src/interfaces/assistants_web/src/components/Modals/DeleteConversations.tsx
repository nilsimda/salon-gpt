'use client';

import { Button, Text } from '@/components/UI';
import { pluralize } from '@/utils';

type Props = {
  conversationIds: string[];
  onClose: VoidFunction;
  onConfirm: VoidFunction;
  isPending: boolean;
};

export const DeleteConversations: React.FC<Props> = ({
  conversationIds,
  onClose,
  onConfirm,
  isPending,
}) => {
  const numConversations = conversationIds.length;

  return (
    <section>
      <Text className="mb-5">
        Sobald du diese {numConversations === 1 ? 'Konversation' : 'Konversationen'} löschst kannst du die Nachrichten weder sehen noch abrufen. Es kann nicht rückgangig gemacht werden.
      </Text>
      <div className="flex flex-col-reverse items-center justify-between gap-y-4 md:flex-row">
        <Button kind="secondary" onClick={onClose} label="Abbrechen" />
        <Button
          kind="cell"
          onClick={onConfirm}
          icon="trash"
          disabled={isPending}
          label={
            isPending
              ? 'Wird gelöscht...'
              : 'Konversation löschen'
          }
        />
      </div>
    </section>
  );
};
