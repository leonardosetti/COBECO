import { describe, expect, it, vi } from 'vitest';
import { DummyJsonProvider } from './dummy-json.provider';
import { MercadoLivreProvider } from './mercado-livre.provider';
import { MockPriceProvider } from './mock.provider';

function response(payload: unknown): Response {
  return new Response(JSON.stringify(payload), { status: 200, headers: { 'content-type': 'application/json' } });
}

describe('price providers', () => {
  it('normalizes Mercado Livre search results', async () => {
    const fetchImplementation = vi.fn(async () =>
      response({
        results: [{ id: 'MLB1', title: 'Café', price: 22.5, currency_id: 'BRL', permalink: 'https://produto.mercadolivre.com.br/MLB1' }],
      })
    ) as unknown as typeof fetch;
    const products = await new MercadoLivreProvider('https://mercado.test', fetchImplementation).search({ query: 'cafe' });

    expect(products[0]).toMatchObject({
      id: 'mercado-livre:MLB1',
      productName: 'Café',
      price: 22.5,
      currency: 'BRL',
      deliveryDays: null,
      incompleteFields: ['deliveryDays'],
    });
    expect(fetchImplementation).toHaveBeenCalledWith(
      'https://mercado.test/sites/MLB/search?q=cafe&limit=20',
      expect.objectContaining({ headers: { Accept: 'application/json' } })
    );
  });

  it('normalizes DummyJSON products and flags missing delivery data', async () => {
    const fetchImplementation = vi.fn(async () =>
      response({ products: [{ id: 1, title: 'Phone', description: 'Smartphone', price: 99.99 }] })
    ) as unknown as typeof fetch;
    const products = await new DummyJsonProvider('https://dummy.test', fetchImplementation).search({ query: 'phone' });

    expect(products[0]).toMatchObject({
      id: 'dummyjson:1',
      productName: 'Phone',
      description: 'Smartphone',
      price: 99.99,
      currency: 'USD',
      deliveryDays: null,
      incompleteFields: ['deliveryDays'],
    });
  });

  it('provides deterministic development data', async () => {
    const provider = new MockPriceProvider([{ id: '1', productName: 'Arroz 5kg', price: 30, deliveryDays: 3 }]);
    const products = await provider.search({ query: 'arroz' });

    expect(provider.calls).toBe(1);
    expect(products[0].retailerSlug).toBe('mock');
    expect(products[0].price).toBe(30);
  });

  it('rejects malformed provider payloads', async () => {
    const fetchImplementation = vi.fn(async () => response({ unexpected: true })) as unknown as typeof fetch;

    await expect(new DummyJsonProvider('https://dummy.test', fetchImplementation).search({ query: 'phone' })).rejects.toMatchObject({
      code: 'PROVIDER_INVALID_RESPONSE',
    });
  });
});
