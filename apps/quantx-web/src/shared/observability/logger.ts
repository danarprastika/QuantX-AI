import { apiClient } from '@/application/api/client';

export interface LoggerConfig {
  level: 'error' | 'warn' | 'info' | 'debug';
  environment: string;
  service: string;
}

export interface LogEntry {
  timestamp: string;
  severity: string;
  service: string;
  environment: string;
  traceId?: string;
  spanId?: string;
  correlationId?: string;
  message: string;
}

class FrontendLogger {
  private config: LoggerConfig;

  constructor(config: LoggerConfig) {
    this.config = config;
  }

  private formatEntry(
    severity: string,
    message: string,
    context?: Record<string, unknown>
  ): LogEntry {
    return {
      timestamp: new Date().toISOString(),
      severity,
      service: this.config.service,
      environment: this.config.environment,
      ...context,
      message,
    };
  }

  private emit(entry: LogEntry): void {
    if (typeof window !== 'undefined' && window.console) {
      console.log(JSON.stringify(entry));
    } else {
      console.log(JSON.stringify(entry));
    }
  }

  error(message: string, context?: Record<string, unknown>): void {
    this.emit(this.formatEntry('ERROR', message, context));
  }

  warn(message: string, context?: Record<string, unknown>): void {
    this.emit(this.formatEntry('WARN', message, context));
  }

  info(message: string, context?: Record<string, unknown>): void {
    this.emit(this.formatEntry('INFO', message, context));
  }

  debug(message: string, context?: Record<string, unknown>): void {
    if (this.config.level !== 'debug') return;
    this.emit(this.formatEntry('DEBUG', message, context));
  }
}

export const logger = new FrontendLogger({
  level: (process.env.NEXT_PUBLIC_LOG_LEVEL as LoggerConfig['level']) || 'info',
  environment: process.env.NODE_ENV || 'development',
  service: 'quantx-web',
});

export const logApiCall = (
  method: string,
  url: string,
  duration: number,
  status: number
): void => {
  logger.info('API Call', {
    method,
    url,
    duration,
    status,
    correlationId: apiClient.getCorrelationId(),
  });
};

export const logUserAction = (
  action: string,
  component: string,
  metadata?: Record<string, unknown>
): void => {
  logger.info('User Action', {
    action,
    component,
    ...metadata,
  });
};