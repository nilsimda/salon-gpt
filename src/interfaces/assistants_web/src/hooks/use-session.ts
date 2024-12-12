'use client';

import { useMutation } from '@tanstack/react-query';
import Cookies from 'js-cookie';
import { jwtDecode } from 'jwt-decode';
import { useCookies } from 'next-client-cookies';
import { useRouter } from 'next/navigation';
import { useCallback, useMemo } from 'react';

import { COOKIE_KEYS } from '@/constants';
import { useServerAuthStrategies } from '@/hooks';
import { ApiError, JWTResponse, useSalonClient } from '@/salon-client';
import { clearAuthToken, setAuthToken } from '@/server/actions';

interface LoginParams {
  email: string;
  password: string;
}

interface RegisterParams {
  name: string;
  email: string;
  password: string;
}

interface UserSession {
  email: string;
  fullname: string;
  id: string;
}

export const useSession = () => {
  const cookies = useCookies();
  const authToken = cookies.get(COOKIE_KEYS.authToken);
  const router = useRouter();
  const { data: authStrategies, isLoading: isLoadingStrategies } = useServerAuthStrategies();

  const isLoading = isLoadingStrategies;

  const isLoggedIn = useMemo(
    () =>
      (authStrategies && authStrategies.length > 0 && !!authToken) ||
      !authStrategies ||
      authStrategies.length === 0,
    [authToken, authStrategies]
  );

  const salonClient = useSalonClient();
  const session = useMemo(
    () => (authToken ? (jwtDecode(authToken) as { context: UserSession }).context : null),
    [authToken]
  );

  const loginMutation = useMutation<JWTResponse | null, ApiError, LoginParams>({
    mutationFn: (params) => salonClient.login(params),
    onSuccess: async (data: JWTResponse | null) => {
      if (!data) {
        throw new Error('Invalid login');
      }
      await setAuthToken(data.token);
      return data?.token;
    },
  });

  const logoutMutation = useMutation({
    mutationFn: async () => {
      await clearAuthToken();
      return salonClient.logout();
    },
  });

  const registerMutation = useMutation({
    mutationFn: async (params: RegisterParams) => {
      return salonClient.createUser({
        fullname: params.name,
        email: params.email,
        password: params.password,
      });
    },
  });

  const redirectToLogin = useCallback(() => {
    router.push(`/login?redirect_uri=${encodeURIComponent(window.location.href)}`);
  }, [router]);

  const googleSSOMutation = useMutation({
    mutationFn: async (params: { code: string }) => {
      return salonClient.googleSSOAuth(params);
    },
    onSuccess: async (data: { token: string }) => {
      await setAuthToken(data.token);
      return data.token;
    },
  });

  const oidcSSOMutation = useMutation({
    mutationFn: async (params: { code: string; strategy: string }) => {
      const codeVerifier = Cookies.get('code_verifier');
      return salonClient.oidcSSOAuth({
        ...params,
        ...(codeVerifier && { codeVerifier }),
      });
    },
    onSuccess: async (data: { token: string }) => {
      await setAuthToken(data.token);
      return data.token;
    },
    onSettled: () => {
      Cookies.remove('code_verifier');
      Cookies.remove('code_challenge');
    },
  });

  return {
    session,
    userId: session && 'id' in session ? session.id : 'user-id',
    authToken,
    isLoading,
    isLoggedIn,
    loginMutation,
    logoutMutation,
    registerMutation,
    redirectToLogin,
    googleSSOMutation,
    oidcSSOMutation,
  };
};
