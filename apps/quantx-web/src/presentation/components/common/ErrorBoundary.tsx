'use client';

import React, { Component, ReactNode } from 'react';
import { logger } from '@/shared/observability/logger';
import { i18n } from '@/shared/i18n/i18n-manager';
import { ErrorEnvelope } from '@/shared/kernel/error-envelope';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, correlationId?: string) => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  correlationId?: string;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  override componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    const correlationId = this.extractCorrelationId(error);
    
    logger.error('Component error caught', {
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
      correlationId,
    });

    if (this.props.onError) {
      this.props.onError(error, correlationId);
    }
  }

  private extractCorrelationId(error: Error): string | undefined {
    const errorData = error.message.match(/{[^}]+}/);
    if (errorData) {
      try {
        const parsed = JSON.parse(errorData[0]) as ErrorEnvelope;
        return parsed.error.correlationId;
      } catch {
        return undefined;
      }
    }
    return undefined;
  }

  private handleRetry = (): void => {
    this.setState({ hasError: false, error: undefined, correlationId: undefined });
  };

  override render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      const correlationId = this.state.correlationId;

      return (
        <div className="error-boundary" role="alert" aria-live="polite">
          <h2>{i18n.t('common.error')}</h2>
          <p>
            {this.state.error?.message || i18n.t('common.error')}
          </p>
          {correlationId && (
            <p className="correlation-id">
              {i18n.t('support.correlationId')}: {correlationId}
            </p>
          )}
          <button
            onClick={this.handleRetry}
            className="retry-button"
            aria-label={i18n.t('common.retry')}
          >
            {i18n.t('common.retry')}
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;