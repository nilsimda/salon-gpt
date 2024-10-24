import { AgentPublic } from '@/cohere-client';
import { QuoteLogo, Text } from '@/components/UI';
import { useBrandedColors } from '@/hooks';
import { cn } from '@/utils';

export const AgentLogo = ({ agent }: { agent: AgentPublic }) => {
  const isBaseAgent = !agent.id;
  const { bg, contrastText, contrastFill } = useBrandedColors(agent.id);

  return (
    <div className={cn('flex size-5 flex-shrink-0 items-center justify-center rounded', bg)}>
      {isBaseAgent && <QuoteLogo className={cn(contrastFill, 'size-3')} />}
      {!isBaseAgent && (
        <Text className={cn('uppercase', contrastText)} styleAs="p-sm">
          {agent.name[0]}
        </Text>
      )}
    </div>
  );
};
