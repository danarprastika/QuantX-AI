'use client';

import { ReactNode } from 'react';
import { i18n } from '@/shared/i18n/i18n-manager';
import ErrorBoundary from '@/presentation/components/common/ErrorBoundary';

interface LayoutProps {
  children: ReactNode;
}

export default function RootLayout({ children }: LayoutProps) {
  const isRTL = i18n.isRTL();

  return (
    <html lang={i18n.getLocale()} dir={isRTL ? 'rtl' : 'ltr'}>
      <head />
      <body className={isRTL ? 'rtl' : 'ltr'}>
        <ErrorBoundary>
          <div className="app-container">{children}</div>
        </ErrorBoundary>
      </body>
    </html>
  );
}