import { fetchJson, FetchImplementation } from '../http-client';
import { NormalizedPriceResult, PriceProvider, PriceSearchInput } from '../price-provider';
import { ProviderError } from '../provider-error';

interface DummyProduct {
  id?: unknown;
  title?: unknown;
  description?: unknown;
  price?: unknown;
}

interface DummyJsonResponse {
  products: unknown[];
}

export class DummyJsonProvider implements PriceProvider {
  readonly slug = 'dummyjson';
  readonly displayName = 'DummyJSON Catalog';

  constructor(
    private readonly baseUrl = 'https://dummyjson.com',
    private readonly fetchImplementation?: FetchImplementation,
    private readonly timeoutMs = 5_000
  ) {}

  async search(input: PriceSearchInput): Promise<NormalizedPriceResult[]> {
    const url = new URL('/products/search', this.baseUrl);
    url.searchParams.set('q', input.query);
    url.searchParams.set('limit', '20');
    const payload = await fetchJson<DummyJsonResponse>(url.toString(), {
      signal: input.signal,
      timeoutMs: this.timeoutMs,
      fetchImplementation: this.fetchImplementation,
    });

    if (!isDummyJsonResponse(payload)) {
      throw new ProviderError('PROVIDER_INVALID_RESPONSE', 'O catálogo retornou uma resposta inesperada.');
    }

    return payload.products.flatMap((candidate, index) => {
      if (!isDummyProduct(candidate)) return [];
      const price = toPrice(candidate.price);
      return [
        {
          id: `${this.slug}:${String(candidate.id || index)}`,
          providerSlug: this.slug,
          retailerName: this.displayName,
          retailerSlug: this.slug,
          productName: candidate.title,
          description: typeof candidate.description === 'string' ? candidate.description : undefined,
          price,
          currency: 'USD',
          deliveryDays: null,
          redirectUrl: `${this.baseUrl.replace(/\/$/, '')}/products/${encodeURIComponent(String(candidate.id || index))}`,
          fetchedAt: new Date(),
          incompleteFields: [...(price === null ? ['price' as const] : []), 'deliveryDays' as const],
        },
      ];
    });
  }
}

function isDummyProduct(value: unknown): value is DummyProduct & { title: string } {
  if (!value || typeof value !== 'object') return false;
  const product = value as DummyProduct;
  return typeof product.title === 'string' && product.title.trim().length > 0;
}

function isDummyJsonResponse(value: unknown): value is DummyJsonResponse {
  return Boolean(value && typeof value === 'object' && Array.isArray((value as DummyJsonResponse).products));
}

function toPrice(value: unknown): number | null {
  return typeof value === 'number' && Number.isFinite(value) && value >= 0 ? value : null;
}
