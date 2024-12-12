'use client';

import { cn } from '@/utils';

export const Quote: React.FC<{
  className?: string;
}> = ({ className }) => (
  <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" className={cn('size-3', className)}>
    {/* First quote mark */}
    <path fill="currentColor" d="M0 4v12h8c0 4.41-3.586 8-8 8v4c6.617 0 12-5.383 12-12V4H0z" />
    {/* Second quote mark */}
    <path fill="currentColor" d="M20 4v12h8c0 4.41-3.586 8-8 8v4c6.617 0 12-5.383 12-12V4H20z" />
  </svg>
);
