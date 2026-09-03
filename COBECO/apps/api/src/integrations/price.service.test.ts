import { describe, expect, it, vi } from 'vitest';
import { PriceIntegrationService } from './price.service';
import { ProviderError } from './provider-error';
import { NormalizedPriceResult, PriceProvider } from './price-provider';

function result(providerSlug: string, productName = 'Produto teste'): NormalizedPriceResult {
  return {
    id: `${providerSlug}:1`,
    providerSlug,
    retailerName: providerSlug,
    retailerSlug: providerSlug,
    productName,
    price: 10,
    currency: 'BRL',
    deliveryDays: 2,
    redirectUrl: 'https://example.com/product',
    fetchedAt: new Date(),
    incompleteFields: [],
  };
}

function provider(slug: string, search: PriceProvider['search']): PriceProvider {
  return { slug, displayName: slug, search };
}

describe('PriceIntegrationService', () => {
  it('deduplicates simultaneous calls and reuses cached results', async () => {
    let resolveRequest: ((value: NormalizedPriceResult[]) => void) | undefined;
    const search = vi.fn(
      () =>
        new Promise<NormalizedPriceResult[]>((resolve) => {
          resolveRequest = resolve;
        })
    );
    const service = new PriceIntegrationService([provider('one', search)], { cacheTtlMs: 60_000 });

    const first = service.search(' arroz ');
    const second = service.search('arroz');
    expect(search).toHaveBeenCalledTimes(1);
    if (!resolveRequest) throw new Error('A requisição de teste não foi iniciada');
    resolveRequest([result('one')]);
    await expect(Promise.all([first, second])).resolves.toHaveLength(2);

    await service.search('ARROZ');
    expect(search).toHaveBeenCalledTimes(1);
  });

  it('expires cached values after the configured TTL', async () => {
    let now = 1_000;
    const search = vi.fn(async () => [result('one')]);
    const service = new PriceIntegrationService([provider('one', search)], {
      cacheTtlMs: 100,
      now: () => now,
    });

    await service.search('arroz');
    now += 101;
    await service.search('arroz');
    expect(search).toHaveBeenCalledTimes(2);
  });

  it('isolates one provider failure and returns the other provider results', async () => {
    const service = new PriceIntegrationService([
      provider('offline', async () => {
        throw new ProviderError('PROVIDER_TIMEOUT', 'timeout');
      }),
      provider('healthy', async () => [result('healthy')]),
    ]);

    const response = await service.search('cafe');
    expect(response.results).toHaveLength(1);
    expect(response.providers.find((item) => item.providerSlug === 'offline')).toMatchObject({
      state: 'failed',
      errorCode: 'SOURCE_UNAVAILABLE',
    });
    expect(response.providers.find((item) => item.providerSlug === 'healthy')).toMatchObject({
      state: 'success',
      resultCount: 1,
    });
  });

  it('opens a circuit after consecutive provider failures', async () => {
    const search = vi.fn(async () => {
      throw new ProviderError('PROVIDER_UNAVAILABLE', 'offline');
    });
    const service = new PriceIntegrationService([provider('offline', search)], {
      cacheTtlMs: 0,
      circuitFailureThreshold: 2,
    });

    await expect(service.search('one')).rejects.toMatchObject({ code: 'SOURCE_UNAVAILABLE' });
    await expect(service.search('two')).rejects.toMatchObject({ code: 'SOURCE_UNAVAILABLE' });
    await expect(service.search('three')).rejects.toMatchObject({ code: 'SOURCE_UNAVAILABLE' });
    expect(search).toHaveBeenCalledTimes(2);
  });

  it('maps rate limit and incomplete data to user-facing statuses', async () => {
    const incomplete = result('partial');
    incomplete.price = null;
    incomplete.deliveryDays = null;
    incomplete.incompleteFields = ['price', 'deliveryDays'];
    const service = new PriceIntegrationService([
      provider('limited', async () => {
        throw new ProviderError('PROVIDER_RATE_LIMIT', 'rate limited');
      }),
      provider('partial', async () => [incomplete]),
    ]);

    const response = await service.search('produto');
    expect(response.providers.find((item) => item.providerSlug === 'limited')).toMatchObject({
      errorCode: 'RATE_LIMIT_EXCEEDED',
    });
    expect(response.providers.find((item) => item.providerSlug === 'partial')).toMatchObject({
      errorCode: 'INCOMPLETE_DATA',
      incompleteCount: 1,
    });
  });

  it('returns explicit errors when all providers fail or no provider finds results', async () => {
    const unavailable = new PriceIntegrationService([
      provider('offline', async () => {
        throw new ProviderError('PROVIDER_TIMEOUT', 'timeout');
      }),
    ]);
    await expect(unavailable.search('produto')).rejects.toMatchObject({ code: 'SOURCE_UNAVAILABLE' });

    const empty = new PriceIntegrationService([provider('empty', async () => [])]);
    await expect(empty.search('produto')).rejects.toMatchObject({ code: 'NO_RESULTS' });
  });
});
