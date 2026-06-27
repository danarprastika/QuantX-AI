import { apiClient } from '@/application/api/client';

export interface TraceSpan {
  id: string;
  traceId: string;
  parentId?: string;
  name: string;
  startTime: number;
  endTime?: number;
  attributes: Record<string, unknown>;
  status: 'ok' | 'error';
}

export interface TraceContext {
  traceId: string;
  spanId: string;
}

class FrontendTracer {
  private spans: TraceSpan[] = [];
  private activeSpans: Map<string, TraceSpan> = new Map();

  startSpan(name: string, parentId?: string): TraceSpan {
    const spanId = crypto.randomUUID();
    const traceId = parentId
      ? (this.activeSpans.get(parentId)?.traceId ?? crypto.randomUUID())
      : crypto.randomUUID();

    const span: TraceSpan = {
      id: spanId,
      traceId,
      parentId,
      name,
      startTime: performance.now(),
      attributes: {
        'service.name': 'quantx-web',
        'service.version': process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
        'deployment.environment': process.env.NODE_ENV || 'development',
      },
      status: 'ok',
    };

    this.activeSpans.set(spanId, span);
    return span;
  }

  endSpan(spanId: string, status: 'ok' | 'error' = 'ok', error?: Error): void {
    const span = this.activeSpans.get(spanId);
    if (span) {
      span.endTime = performance.now();
      span.status = status;
      if (error) {
        span.attributes.error = error.message;
        span.attributes['error.stack'] = error.stack;
      }
      this.spans.push(span);
      this.activeSpans.delete(spanId);
      this.emit(span);
    }
  }

  setAttribute(spanId: string, key: string, value: unknown): void {
    const span = this.activeSpans.get(spanId);
    if (span) {
      span.attributes[key] = value;
    }
  }

  private emit(span: TraceSpan): void {
    if (typeof window !== 'undefined') {
      const otelSdk = (window as any).__otelSdk;
      if (otelSdk) {
        otelSdk.trace(span);
      }
    }
  }

  getTraceContext(): TraceContext {
    const activeSpanIds = Array.from(this.activeSpans.keys());
    if (activeSpanIds.length > 0) {
      const span = this.activeSpans.get(activeSpanIds[0]);
      return {
        traceId: span!.traceId,
        spanId: span!.id,
      };
    }
    return {
      traceId: crypto.randomUUID(),
      spanId: crypto.randomUUID(),
    };
  }

  getSpans(): TraceSpan[] {
    return this.spans;
  }

  clear(): void {
    this.spans = [];
    this.activeSpans.clear();
  }
}

export const tracer = new FrontendTracer();

export const traceApiCall = async <T>(
  method: string,
  url: string,
  operation: () => Promise<T>
): Promise<T> => {
  const span = tracer.startSpan(`HTTP ${method.toUpperCase()}`, undefined);
  tracer.setAttribute(span.id, 'http.method', method.toUpperCase());
  tracer.setAttribute(span.id, 'http.url', url);

  try {
    const result = await operation();
    tracer.endSpan(span.id, 'ok');
    return result;
  } catch (error) {
    tracer.endSpan(span.id, 'error', error as Error);
    throw error;
  }
};