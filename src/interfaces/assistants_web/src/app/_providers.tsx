'use client';

import { QueryCache, QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { ThemeProvider } from 'next-themes';
import { useRouter } from 'next/navigation';
import { useMemo } from 'react';

import {
  GlobalHead,
  ToastNotification,
  ViewportFix,
  WebManifestHead,
} from '@/components/Providers';
import { ContextStore } from '@/context';
import { env } from '@/env.mjs';
import { useLazyRef } from '@/hooks';
import { CohereUnauthorizedError, Fetch, SalonClient, SalonClientProvider } from '@/salon-client';
import { clearAuthToken } from '@/server/actions';

const makeSalonClient = (authToken?: string) => {
  const apiFetch: Fetch = async (resource, config) => await fetch(resource, config);
  return new SalonClient({
    hostname: env.NEXT_PUBLIC_API_HOSTNAME,
    fetch: apiFetch,
    authToken,
  });
};

export const LayoutProviders: React.FC<React.PropsWithChildren<{ authToken?: string }>> = ({
  children,
  authToken,
}) => {
  const router = useRouter();

  const salonClient = useMemo(() => makeSalonClient(authToken), [authToken]);
  const queryClient = useLazyRef(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            retry: false,
          },
        },
        queryCache: new QueryCache({
          onError: (error) => {
            if (error instanceof CohereUnauthorizedError) {
              clearAuthToken();
              // Extract the current URL without query parameters or host.
              const currentPath = window.location.pathname + window.location.hash;
              router.push(`/login?redirect_uri=${encodeURIComponent(currentPath)}`);
            }
          },
        }),
      })
  );

  return (
    <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={true}>
      <SalonClientProvider client={salonClient}>
        <QueryClientProvider client={queryClient}>
          <ContextStore>
            <ViewportFix />
            <GlobalHead />
            <WebManifestHead />
            <ToastNotification />
            <ReactQueryDevtools />
            {children}
          </ContextStore>
        </QueryClientProvider>
      </SalonClientProvider>
    </ThemeProvider>
  );
};
