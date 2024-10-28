import { AgentPublic } from '@/cohere-client';
import { QuoteLogo, AudioLogo, Text } from '@/components/UI';
import { useBrandedColors } from '@/hooks';
import { checkIsBaseAgent, checkIsSyntheticUserAgent, checkIsTranscriptionAgent, cn } from '@/utils';

export const AgentLogo: React.FC<{ agent_id?: string, className?: string}> = ({ agent_id, className }) => {
  const isBaseAgent = !agent_id;
  const isTranscriptionAgent = agent_id === 'transcription';
  const isSyntheticUserAgent = agent_id === 'kerlin';
  const { bg, contrastText, contrastFill } = useBrandedColors(agent_id);

  return (
    <div className={cn('flex size-5 flex-shrink-0 items-center justify-center rounded', bg)}>
      {isBaseAgent ? (<QuoteLogo className={className} />) :
        isTranscriptionAgent ? (<AudioLogo className={className} />) :(
        <Text className={className} styleAs="p-sm">
          {agent_id[0]}
        </Text>
      )}
    </div>
  );
};
