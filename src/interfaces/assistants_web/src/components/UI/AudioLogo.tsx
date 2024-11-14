'use client';

import { cn } from '@/utils';

export const AudioLogo: React.FC<{
  className?: string;
}> = ({ className }) => (
  <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" className={cn('size-6', className)}>
    {/* Centered microphone body */}
    <rect x="13" y="4" width="6" height="12" rx="3" fill="currentColor" />

    {/* Adjusted stand and base */}
    <path
      d="M11 12v2a5 5 0 0010 0v-2M16 19v5M12 24h8"
      stroke="currentColor"
      fill="none"
      strokeWidth="2"
      strokeLinecap="round"
    />
  </svg>
);
