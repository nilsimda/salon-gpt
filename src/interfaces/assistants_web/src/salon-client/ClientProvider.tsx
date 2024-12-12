'use client';

import React, { useContext } from 'react';

import { SalonClient } from './client';

const SalonClientContext = React.createContext<SalonClient | null>(null);

interface Props {
  client?: SalonClient;
  children: React.ReactNode;
}

/**
 * A provider component for the CohereClient. Render this component at the top of your
 * component tree to make the client available to all components that use useSalonClient().
 */
export const SalonClientProvider: React.FC<Props> = ({ client, children }) => {
  if (!client) return null;
  return <SalonClientContext.Provider value={client}>{children}</SalonClientContext.Provider>;
};

/**
 * A hook that returns the CohereClientContext instance. This hook should only be used within a
 * CohereClientContext Provider.
 */
export const useSalonClient = () => {
  const client = useContext(SalonClientContext);

  if (!client) {
    throw new Error('No SalonClientContext set. Use SalonClientProvider to set one.');
  }

  return client;
};
