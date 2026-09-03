import { describe, expect, it, vi } from 'vitest';
import { PriceIntegrationService } from '../integrations/price.service';
import { NormalizedPriceResult, PriceProvider, PriceSearchInput } from '../integrations/price-provider';
import { MemoryListRepository, MemoryQuotationRepository } from '../repositories/memory.repository';
import { QuotationService } from './quotation.service';

function offer(id: string, price: number, deliveryDays: number): NormalizedPriceResult {
  return {
    id,
    providerSlug: 'test',
    retailerName: 'Lojista teste',
    retailerSlug: 'test',
    productName: 'Produto',
    price,
    currency: 'BRL',
    deliveryDays,
    redirectUrl: 'https://example.com',
    fetchedAt: new Date(),
    incompleteFields: [],
  };
}

function provider(search: PriceProvider['search']): PriceProvider {
  return { slug: 'test', displayName: 'Provider teste', search };
}

describe('QuotationService', () => {
  it('quotes every item in a list in parallel and calculates highlights', async () => {
    const started: string[] = [];
    const releases: Array<() => void> = [];
    const search = vi.fn((input: PriceSearchInput) => {
      started.push(input.query);
      return new Promise<NormalizedPriceResult[]>((resolve) => {
        releases.push(() => resolve(input.query === 'arroz'
          ? [offer('arroz:1', 10, 5), offer('arroz:2', 12, 2)]
          : [offer(`${input.query}:1`, 20, 2)]));
      });
    });
    const priceService = new PriceIntegrationService([provider(search)], { cacheTtlMs: 0 });
    const listRepository = new MemoryListRepository();
    const list = await listRepository.create('user-1', 'Compras');
    await listRepository.createItems('user-1', list.id, [{ description: 'arroz', quantity: 2 }, { description: 'cafe', quantity: 1 }]);
    const service = new QuotationService(priceService, listRepository);

    const quotationPromise = service.quoteList('user-1', list.id);
    await vi.waitFor(() => expect(search).toHaveBeenCalledTimes(2));
    expect(started.sort()).toEqual(['arroz', 'cafe']);
    releases.forEach((release) => release());
    const quotation = await quotationPromise;

    expect(quotation.mode).toBe('list');
    expect(quotation.items).toHaveLength(2);
    expect(quotation.items[0].highlights.lowestPriceIds).toEqual(['arroz:1']);
    expect(quotation.items[0].highlights.fastestDeliveryIds).toEqual(['arroz:2']);
  });

  it('does not allow quoting another user\'s list', async () => {
    const priceService = new PriceIntegrationService([provider(async () => [])]);
    const listRepository = new MemoryListRepository();
    const list = await listRepository.create('owner', 'Privada');
    const service = new QuotationService(priceService, listRepository);

    await expect(service.quoteList('another-user', list.id)).rejects.toMatchObject({ code: 'LIST_NOT_FOUND' });
  });

  it('persists, reopens, compares and deletes quotation history', async () => {
    const priceService = new PriceIntegrationService([provider(async () => [offer('offer-1', 10, 3)])]);
    const listRepository = new MemoryListRepository();
    const quotationRepository = new MemoryQuotationRepository();
    const service = new QuotationService(priceService, listRepository, quotationRepository);

    const first = await service.quoteItem('user-1', 'arroz');
    priceService.clearCache();
    const second = await service.quoteItem('user-1', 'arroz');
    const firstId = requireQuotationId(first.quotationId);
    const secondId = requireQuotationId(second.quotationId);
    const history = await service.listHistory('user-1');

    expect(history.items).toHaveLength(2);
    expect(history.total).toBe(2);
    expect(history.items.every((item) => item.status === 'completed')).toBe(true);
    const firstPage = await service.listHistory('user-1', 1, 1);
    expect(firstPage.items).toHaveLength(1);
    expect(firstPage.totalPages).toBe(2);
    await expect(service.getHistory('user-1', firstId)).resolves.toMatchObject({ quotationId: firstId });
    await expect(service.compareHistory('user-1', firstId, secondId)).resolves.toMatchObject({ items: [{ description: 'arroz' }] });

    await service.deleteHistory('user-1', firstId);
    await expect(service.getHistory('user-1', firstId)).rejects.toMatchObject({ code: 'QUOTATION_NOT_FOUND' });
  });

  it('keeps a failed quotation in history', async () => {
    const priceService = new PriceIntegrationService([provider(async () => { throw new Error('offline'); })]);
    const service = new QuotationService(priceService, new MemoryListRepository(), new MemoryQuotationRepository());

    await expect(service.quoteItem('user-1', 'produto')).rejects.toMatchObject({ code: 'SOURCE_UNAVAILABLE' });
    await expect(service.listHistory('user-1')).resolves.toMatchObject({ items: [{ status: 'failed', itemCount: 1, descriptions: ['produto'] }] });
  });
});

function requireQuotationId(id: string | null): string {
  if (!id) throw new Error('A cotação não foi persistida');
  return id;
}
