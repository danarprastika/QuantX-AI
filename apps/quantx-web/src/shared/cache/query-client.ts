import { QueryClient } from '@tanstack/react-query';

export interface CacheKeyNamespace {
  domain: string;
  resource: string;
  variant?: string;
}

export interface CacheConfig {
  ttl: number;
  staleTime: number;
  cacheTime: number;
  retry: number;
  retryDelay: number;
}

export const CACHE_CONFIG: Record<string, CacheConfig> = {
  marketSignals: {
    ttl: 60000,
    staleTime: 300000,
    cacheTime: 600000,
    retry: 3,
    retryDelay: 1000,
  },
  portfolios: {
    ttl: 60000,
    staleTime: 120000,
    cacheTime: 300000,
    retry: 3,
    retryDelay: 1000,
  },
  default: {
    ttl: 300000,
    staleTime: 60000,
    cacheTime: 300000,
    retry: 2,
    retryDelay: 1000,
  },
};

export const createCacheKey = (
  namespace: CacheKeyNamespace,
  identifier?: string
): string[] => {
  const parts = [namespace.domain, namespace.resource];
  if (namespace.variant) {
    parts.push(namespace.variant);
  }
  if (identifier) {
    parts.push(identifier);
  }
  return parts;
};

export const cacheKeys = {
  marketSignals: {
    all: () => createCacheKey({ domain: 'market', resource: 'signals' }),
    bySymbol: (symbol: string) =>
      createCacheKey({ domain: 'market', resource: 'signals', variant: symbol }),
    byUser: () => createCacheKey({ domain: 'market', resource: 'signals', variant: 'user' }),
  },
  portfolios: {
    all: () => createCacheKey({ domain: 'portfolio', resource: 'positions' }),
    byId: (id: string) =>
      createCacheKey({ domain: 'portfolio', resource: 'positions', variant: id }),
    byUser: (userId: string) =>
      createCacheKey({ domain: 'portfolio', resource: 'positions', variant: userId }),
  },
  sharia: {
    compliance: () => createCacheKey({ domain: 'sharia', resource: 'compliance' }),
    screening: (symbol: string) =>
      createCacheKey({ domain: 'sharia', resource: 'screening', variant: symbol }),
  },
};

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: CACHE_CONFIG.default.staleTime,
      cacheTime: CACHE_CONFIG.default.cacheTime,
      retry: CACHE_CONFIG.default.retry,
      retryDelay: CACHE_CONFIG.default.retryDelay,
      refetchOnWindowFocus: false,
      refetchOnMount: false,
    },
    mutations: {
      retry: 1,
    },
  },
});

export const invalidateCache = async (keys: string[]): Promise<void> => {
  await queryClient.invalidateQueries({ queryKey: keys });
};

export const prefetchQuery = async <T>(
  key: string[],
  fetcher: () => Promise<T>
): Promise<void> => {
  await queryClient.prefetchQuery({
    queryKey: key,
    queryFn: fetcher,
    staleTime: CACHE_CONFIG.default.staleTime,
  });
};