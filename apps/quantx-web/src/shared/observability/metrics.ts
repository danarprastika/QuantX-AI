export interface MetricLabels {
  [key: string]: string | number | boolean;
}

export interface Metric {
  name: string;
  value: number;
  labels: MetricLabels;
  timestamp: string;
}

export interface WebVitals {
  lcp: number;
  fid: number;
  cls: number;
  fcp: number;
  ttfb: number;
}

class MetricsCollector {
  private metrics: Metric[] = [];

  collect(name: string, value: number, labels: MetricLabels = {}): void {
    const metric: Metric = {
      name,
      value,
      labels,
      timestamp: new Date().toISOString(),
    };
    this.metrics.push(metric);
    this.emit(metric);
  }

  collectWebVitals(vitals: WebVitals): void {
    this.collect('web_vitals_lcp', vitals.lcp, { type: 'core' });
    this.collect('web_vitals_fid', vitals.fid, { type: 'core' });
    this.collect('web_vitals_cls', vitals.cls, { type: 'core' });
    this.collect('web_vitals_fcp', vitals.fcp, { type: 'core' });
    this.collect('web_vitals_ttfb', vitals.ttfb, { type: 'core' });
  }

  collectRequestRate(endpoint: string, method: string): void {
    this.collect('api_request_rate', 1, { endpoint, method });
  }

  collectErrorRate(endpoint: string, method: string): void {
    this.collect('api_error_rate', 1, { endpoint, method });
  }

  collectDuration(endpoint: string, method: string, duration: number): void {
    this.collect('api_duration_ms', duration, { endpoint, method });
  }

  private emit(metric: Metric): void {
    if (typeof window !== 'undefined' && window.navigator) {
      const otelCollector = (window as any).__otelCollector;
      if (otelCollector) {
        otelCollector.emit(metric);
      }
    }
  }

  getMetrics(): Metric[] {
    return this.metrics;
  }

  clear(): void {
    this.metrics = [];
  }
}

export const metrics = new MetricsCollector();