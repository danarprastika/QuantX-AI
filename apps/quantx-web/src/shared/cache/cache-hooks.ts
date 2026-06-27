import { useQuery, UseQueryOptions, QueryKey } from '@tanstack/react-query';
import { CACHE_CONFIG } from './query-client';

export interface CacheOptions {
  ttl?: number;
  staleTime?: number;
  cacheTime?: number;
  enabled?: boolean;
}

export function useCacheQuery<T>(
  queryKey: QueryKey,
  queryFn: () => Promise<T>,
  options: CacheOptions & Omit<UseQueryOptions<T>, 'queryKey' | 'queryFn'> = {}
) {
  const config = CACHE_CONFIG.default;

  return useQuery<T>({
    queryKey,
    queryFn,
    staleTime: options.staleTime ?? config.staleTime,
    cacheTime: options.cacheTime ?? config.cacheTime,
    enabled: options.enabled ?? true,
    retry: config.retry,
    retryDelay: config.retryDelay,
  });
}

export function useMarketSignalsQuery(symbol?: string) {
  const config = CACHE_CONFIG.marketSignals;
  const key = symbol
    ? ['market', 'signals', symbol]
    : ['market', 'signals'];

  return useCacheQuery(key, () => fetch(`/api/v1/market-signals?symbol=${symbol}`).then(r => r.json()), {
    ttl: config.ttl,
    staleTime: config.staleTime,
    cacheTime: config.cacheTime,
  });
}

export function usePortfoliosQuery() {
  const config = CACHE_CONFIG.portfolios;

  return useCacheQuery(['portfolio', 'positions'], () =>
    fetch('/api/v1/portfolios').then(r => r.json())
  );
}