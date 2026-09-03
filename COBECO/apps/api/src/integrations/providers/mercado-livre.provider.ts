import { fetchJson, FetchImplementation } from '../http-client';
import { NormalizedPriceResult, PriceProvider, PriceSearchInput } from '../price-provider';
import { ProviderError } from '../provider-error';

interface MercadoLivreProduct {
  id?: unknown;
  title?: unknown;
  price?: unknown;
  currency_id?: unknown;
  permalink?: unknown;
}

interface MercadoLivreResponse {
  results: unknown[];
}

export class MercadoLivreProvider implements PriceProvider {
  readonly slug = 'mercado-livre';
  readonly displayName = 'Mercado Livre';

  constructor(
    private readonly baseUrl = 'https://api.mercadolibre.com',
    private readonly fetchImplementation?: FetchImplementation,
    private readonly timeoutMs = 5_000,
    /**
     * `/sites/MLB/search` deixou de aceitar chamadas anônimas e responde 403.
     * Informe um token OAuth em MERCADO_LIVRE_ACCESS_TOKEN para usar a fonte.
     */
    private readonly accessToken = process.env.MERCADO_LIVRE_ACCESS_TOKEN
  ) {}

  async search(input: PriceSearchInput): Promise<NormalizedPriceResult[]> {
    const url = new URL('/sites/MLB/search', this.baseUrl);
    url.searchParams.set('q', input.query);
    url.searchParams.set('limit', '20');
    const payload = await fetchJson<MercadoLivreResponse>(url.toString(), {
      signal: input.signal,
      timeoutMs: this.timeoutMs,
      fetchImplementation: this.fetchImplementation,
      ...(this.accessToken ? { headers: { Authorization: `Bearer ${this.accessToken}` } } : {}),
    });

    if (!isMercadoLivreResponse(payload)) {
      throw new ProviderError('PROVIDER_INVALID_RESPONSE', 'O Mercado Livre retornou uma resposta inesperada.');
    }

    return payload.results.flatMap((candidate, index) => {
      if (!isMercadoLivreProduct(candidate)) return [];
      const price = toPrice(candidate.price);
      const deliveryDays = null;
      return [
        {
          id: `${this.slug}:${String(candidate.id || index)}`,
          providerSlug: this.slug,
          retailerName: this.displayName,
          retailerSlug: this.slug,
          productName: candidate.title,
          price,
          currency: typeof candidate.currency_id === 'string' ? candidate.currency_id : 'BRL',
          deliveryDays,
          redirectUrl:
            typeof candidate.permalink === 'string'
              ? candidate.permalink
              : `https://lista.mercadolivre.com.br/${encodeURIComponent(candidate.title)}`,
          fetchedAt: new Date(),
          incompleteFields: [...(price === null ? ['price' as const] : []), 'deliveryDays' as const],
        },
      ];
    });
  }
}

function isMercadoLivreProduct(value: unknown): value is MercadoLivreProduct & { title: string } {
  if (!value || typeof value !== 'object') return false;
  const product = value as MercadoLivreProduct;
  return typeof product.title === 'string' && product.title.trim().length > 0;
}

function isMercadoLivreResponse(value: unknown): value is MercadoLivreResponse {
  return Boolean(value && typeof value === 'object' && Array.isArray((value as MercadoLivreResponse).results));
}

function toPrice(value: unknown): number | null {
  return typeof value === 'number' && Number.isFinite(value) && value >= 0 ? value : null;
}
