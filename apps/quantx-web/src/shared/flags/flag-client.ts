import { logger } from '@/shared/observability/logger';

export interface FeatureFlag {
  key: string;
  value: boolean | string | number;
  variant?: string;
  source: 'local' | 'remote';
}

export interface FlagEvaluation {
  flagKey: string;
  value: boolean | string | number;
  variant?: string;
  timestamp: string;
}

export type FlagType = 'release' | 'operational' | 'experiment' | 'permission';

export interface FlagConfig {
  key: string;
  type: FlagType;
  default: boolean | string | number;
  description: string;
  owner: string;
  removalDate?: string;
}

export const FLAG_CONFIG: Record<string, FlagConfig> = {
  'sharia.mode.enabled': {
    key: 'sharia.mode.enabled',
    type: 'release',
    default: false,
    description: 'Enable Sharia Mode for compliance features',
    owner: 'compliance-team',
  },
  'sharia.screening.strict': {
    key: 'sharia.screening.strict',
    type: 'operational',
    default: true,
    description: 'Strict Sharia screening mode',
    owner: 'compliance-team',
    removalDate: '2026-12-31',
  },
  'feature.trading.signals': {
    key: 'feature.trading.signals',
    type: 'release',
    default: true,
    description: 'Enable trading signals feature',
    owner: 'trading-team',
  },
  'feature.portfolio.optimization': {
    key: 'feature.portfolio.optimization',
    type: 'experiment',
    default: false,
    description: 'Experiment: portfolio optimization',
    owner: 'portfolio-team',
    removalDate: '2026-09-30',
  },
};

class FeatureFlagClient {
  private flags: Map<string, FeatureFlag> = new Map();
  private evaluations: FlagEvaluation[] = [];

  constructor() {
    this.initializeFlags();
  }

  private initializeFlags(): void {
    Object.values(FLAG_CONFIG).forEach((config) => {
      this.flags.set(config.key, {
        key: config.key,
        value: config.default,
        source: 'local',
      });
    });

    this.loadRemoteFlags().catch((error) => {
      logger.warn('Failed to load remote flags, using local defaults', { error });
    });
  }

  private async loadRemoteFlags(): Promise<void> {
    try {
      const response = await fetch('/api/v1/feature-flags');
      if (response.ok) {
        const remoteFlags = await response.json();
        remoteFlags.forEach((flag: FeatureFlag) => {
          this.flags.set(flag.key, { ...flag, source: 'remote' });
          this.recordEvaluation(flag.key, flag.value, flag.variant);
        });
      }
    } catch (error) {
      logger.error('Remote flag fetch failed', { error });
    }
  }

  private recordEvaluation(
    flagKey: string,
    value: boolean | string | number,
    variant?: string
  ): void {
    this.evaluations.push({
      flagKey,
      value,
      variant,
      timestamp: new Date().toISOString(),
    });
    logger.info('Flag evaluated', { flagKey, value, variant });
  }

  isEnabled(key: string): boolean {
    const flag = this.flags.get(key);
    if (!flag) {
      return false;
    }
    const value = typeof flag.value === 'boolean' ? flag.value : !!flag.value;
    this.recordEvaluation(key, value);
    return value;
  }

  getValue<T = boolean | string | number>(key: string): T {
    const flag = this.flags.get(key);
    if (!flag) {
      const config = FLAG_CONFIG[key];
      return (config?.default ?? false) as T;
    }
    this.recordEvaluation(key, flag.value, flag.variant);
    return flag.value as T;
  }

  getVariant(key: string): string | undefined {
    const flag = this.flags.get(key);
    if (!flag) {
      return undefined;
    }
    this.recordEvaluation(key, flag.value, flag.variant);
    return flag.variant;
  }

  isShariaMode(): boolean {
    return this.isEnabled('sharia.mode.enabled');
  }

  getAllEvaluations(): FlagEvaluation[] {
    return this.evaluations;
  }

  clearEvaluations(): void {
    this.evaluations = [];
  }
}

export const featureFlags = new FeatureFlagClient();