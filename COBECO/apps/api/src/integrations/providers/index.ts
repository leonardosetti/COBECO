import { PriceProvider } from '../price-provider';
import { DummyJsonProvider } from './dummy-json.provider';
import { MercadoLivreProvider } from './mercado-livre.provider';
import { MockPriceProvider } from './mock.provider';

export { DummyJsonProvider } from './dummy-json.provider';
export { MercadoLivreProvider } from './mercado-livre.provider';
export { MockPriceProvider } from './mock.provider';

export function createDefaultPriceProviders(environment: NodeJS.ProcessEnv = process.env): PriceProvider[] {
  const providers = new Map<string, PriceProvider>([
    ['mercado-livre', new MercadoLivreProvider()],
    ['dummyjson', new DummyJsonProvider()],
    ['mock', new MockPriceProvider()],
  ]);

  const configured = environment.PRICE_PROVIDERS?.split(',')
    .map((value) => value.trim())
    .filter(Boolean);

  const slugs = configured || defaultSlugs(environment);

  return slugs.flatMap((slug) => {
    const provider = providers.get(slug);
    if (!provider) {
      console.warn(`[prices] Provider "${slug}" não existe e foi ignorado.`);
      return [];
    }
    return provider;
  });
}

function defaultSlugs(environment: NodeJS.ProcessEnv): string[] {
  if (environment.ENABLE_EXTERNAL_PRICE_PROVIDERS !== 'true') return ['mock'];
  const isProduction = environment.NODE_ENV === 'production';

  // O Mercado Livre exige credencial OAuth desde a descontinuação da busca
  // anônima. Embarcá-lo sem token só produz uma fonte permanentemente falha.
  const mercadoLivre = environment.MERCADO_LIVRE_ACCESS_TOKEN ? ['mercado-livre'] : [];

  if (!mercadoLivre.length) {
    console.warn(
      '[prices] MERCADO_LIVRE_ACCESS_TOKEN não configurado; a fonte Mercado Livre não será consultada.'
    );
  }

  return isProduction ? [...mercadoLivre, 'dummyjson'] : [...mercadoLivre, 'dummyjson', 'mock'];
}
