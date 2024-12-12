import { useState } from 'react';

import { Markdown } from '@/components/Markdown';
import { DocumentIcon, Icon, Text } from '@/components/UI';
import { useBrandedColors } from '@/hooks';
import { useCitationsStore } from '@/stores';
import { cn, getSafeUrl } from '@/utils';

type Props = {
  generationId: string;
  citationKey: string;
  agentId?: string;
};

export const Citation: React.FC<Props> = ({ generationId, citationKey, agentId }) => {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const { citations } = useCitationsStore();
  const citationsMap = citations.citationReferences[generationId];
  const documents = citationsMap[citationKey];
  const document = documents[selectedIndex];
  const safeUrl = getSafeUrl(document.url);
  const { text, lightText, fill, lightFill, dark, light } = useBrandedColors(agentId);

  const brandedClassName = cn(dark(lightText), light(text), dark(lightFill), light(fill));

  return (
    <div className="space-y-4">
      <header className="flex items-center justify-between">
        <div className="flex gap-2">
          <div className="grid size-8 place-items-center rounded bg-mushroom-800 dark:bg-volcanic-150">
            {document.url ? (
              <a href={safeUrl} target="_blank" data-connectorid={document.tool_name}>
                <DocumentIcon url={safeUrl} />
              </a>
            ) : (
              <Icon name="file" />
            )}
          </div>
        </div>
        {documents.length > 1 && (
          <div className="flex flex-shrink-0 items-center">
            <button
              className="py-[3px] pr-2"
              onClick={() =>
                setSelectedIndex((prev) => (prev - 1 + documents.length) % documents.length)
              }
            >
              <Icon name="chevron-left" />
            </button>
            <Text className="text-p-sm">
              {selectedIndex + 1} of {documents.length}
            </Text>
            <button
              className="py-[3px] pl-2"
              onClick={() => setSelectedIndex((prev) => (prev + 1) % documents.length)}
            >
              <Icon name="chevron-right" />
            </button>
          </div>
        )}
      </header>
      <article className="max-h-64 overflow-y-auto">
        <Markdown className="font-variable" text={document.text} />
      </article>
    </div>
  );
};
