'use client';

import { useState } from 'react';

import { useIsDesktop } from '@/hooks';
import { cn } from '@/utils';

export const CellBackground: React.FC = () => {
  const isDesktop = useIsDesktop();
  const [isVideoError, setIsVideoError] = useState(false);

  const handleVideoError = () => {
    setIsVideoError(true);
  };
  return (
    <div
      className="absolute z-0 h-full w-full overflow-hidden bg-black"
    />
  );
};
