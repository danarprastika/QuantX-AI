import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios';
import { ErrorEnvelope } from '@/shared/kernel/error-envelope';

export interface ApiConfig {
  baseURL: string;
  timeout: number;
  retryAttempts: number;
  retryDelay: number;
}

export interface CorrelationContext {
  correlationId?: string;
  traceId?: string;
}

export class ApiClient {
  private client: AxiosInstance;
  private correlationContext: CorrelationContext = {};

  constructor(config: Partial<ApiConfig> = {}) {
    this.client = axios.create({
      baseURL: config.baseURL || process.env.NEXT_PUBLIC_API_URL || '/api/v1',
      timeout: config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    this.client.interceptors.request.use((config) => {
      const token = this.getAuthToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }

      if (this.correlationContext.correlationId) {
        config.headers['X-Correlation-ID'] = this.correlationContext.correlationId;
      }

      if (this.correlationContext.traceId) {
        config.headers['X-Trace-ID'] = this.correlationContext.traceId;
      }

      const idempotencyKey = this.getIdempotencyKey();
      if (idempotencyKey) {
        config.headers['Idempotency-Key'] = idempotencyKey;
      }

      return config;
    });

    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const { config } = error;
        const retryAttempts = config.headers?.['X-Retry-Attempts']
          ? parseInt(config.headers['X-Retry-Attempts'] as string, 10)
          : 0;

        if (error.response?.status === 429 && retryAttempts < 3) {
          const retryAfter = parseInt(
            error.response.headers['retry-after'] || '5',
            10
          );
          await this.delay(retryAfter * 1000);
          return this.client(config);
        }

        return Promise.reject(this.transformError(error));
      }
    );
  }

  private transformError(error: AxiosError): ErrorEnvelope {
    if (error.response?.data) {
      return error.response.data as ErrorEnvelope;
    }

    return {
      error: {
        code: 'NETWORK_ERROR',
        message: error.message || 'Network error occurred',
        correlationId: this.correlationContext.correlationId ?? crypto.randomUUID(),
        timestamp: new Date().toISOString(),
      },
    };
  }

  private getAuthToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('auth_token');
    }
    return null;
  }

  private getIdempotencyKey(): string | null {
    if (typeof window !== 'undefined') {
      return sessionStorage.getItem('idempotency_key') || null;
    }
    return null;
  }

  private delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  setCorrelationContext(context: CorrelationContext): void {
    this.correlationContext = context;
  }

  getCorrelationId(): string | undefined {
    return this.correlationContext.correlationId;
  }

  async get<T>(url: string, params?: Record<string, unknown>): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get(url, { params });
    this.extractCorrelationContext(response);
    return response.data;
  }

  async post<T>(url: string, data?: unknown, idempotencyKey?: string): Promise<T> {
    if (idempotencyKey && typeof window !== 'undefined') {
      sessionStorage.setItem('idempotency_key', idempotencyKey);
    }
    const response: AxiosResponse<T> = await this.client.post(url, data);
    this.extractCorrelationContext(response);
    return response.data;
  }

  async put<T>(url: string, data?: unknown): Promise<T> {
    const response: AxiosResponse<T> = await this.client.put(url, data);
    this.extractCorrelationContext(response);
    return response.data;
  }

  async patch<T>(url: string, data?: unknown): Promise<T> {
    const response: AxiosResponse<T> = await this.client.patch(url, data);
    this.extractCorrelationContext(response);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response: AxiosResponse<T> = await this.client.delete(url);
    this.extractCorrelationContext(response);
    return response.data;
  }

  private extractCorrelationContext(response: AxiosResponse): void {
    const correlationId = response.headers['x-correlation-id'];
    if (correlationId) {
      this.correlationContext.correlationId = correlationId;
    }
  }
}

export const apiClient = new ApiClient();