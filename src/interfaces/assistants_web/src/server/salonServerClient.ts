import fetch from 'cross-fetch';
import { cookies } from 'next/headers';

import { SalonClient, Fetch } from '@/salon-client';
import { COOKIE_KEYS } from '@/constants';
import { env } from '@/env.mjs';

export const getSalonServerClient = () => {
  const cookieStore = cookies();
  const token = cookieStore.get(COOKIE_KEYS.authToken);
  const apiFetch: Fetch = async (resource, config) => await fetch(resource, config);
  return new SalonClient({
    hostname: env.API_HOSTNAME,
    fetch: apiFetch,
    authToken: token?.value,
  });
};
