'use client';

import { cn } from '@/utils';

export const SearchLogo: React.FC<{
  className?: string;
}> = ({ className }) => (
  <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" className={cn('size-6', className)}>
    {/* Search glass circle */}
    <circle
      cx="14"
      cy="14"
      r="8"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
    />

    {/* Search handle */}
    <path d="M20 20L26 26" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
  </svg>
);
