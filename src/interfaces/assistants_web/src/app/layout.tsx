import { Metadata } from 'next';
import { CookiesProvider } from 'next-client-cookies/server';
import { PublicEnvScript } from 'next-runtime-env';
import { cookies } from 'next/headers';

import { LayoutProviders } from '@/app/_providers';
import { COOKIE_KEYS } from '@/constants';
import '@/styles/main.css';

export const metadata: Metadata = {
  title: {
    template: '%s | rheingold salon',
    default: 'Chat | rheingold salon',
  },
};

const Layout: React.FC<React.PropsWithChildren> = ({ children }) => {
  const cookieStore = cookies();
  const authToken = cookieStore.get(COOKIE_KEYS.authToken)?.value;

  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <PublicEnvScript />
      </head>
      <body className="dark:selection:bg-green-250 text-volcanic-300 selection:bg-coral-900 selection:text-volcanic-300 dark:text-marble-950 dark:selection:text-marble-950">
        <CookiesProvider>
          <LayoutProviders authToken={authToken}>{children}</LayoutProviders>
        </CookiesProvider>
      </body>
    </html>
  );
};

export default Layout;
