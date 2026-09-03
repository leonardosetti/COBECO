import { AppError } from '../types';
import { CircuitBreaker } from './circuit-breaker';
import { isProviderError, ProviderError } from './provider-error';
import { NormalizedPriceResult, PriceProvider, PriceSearchResponse, ProviderSearchStatus } from './price-provider';
import { TtlCache } from './ttl-cache';

interface PriceIntegrationOptions {
  cacheTtlMs?: number;
  circuitFailureThreshold?: number;
  circuitResetTimeoutMs?: number;
  now?: () => number;
}

export interface PriceSearchOptions {
  allowEmpty?: boolean;
}

export class PriceIntegrationService {
  private readonly cache: TtlCache<NormalizedPriceResult[]>;
  private readonly circuits = new Map<string, CircuitBreaker>();

  constructor(private readonly providers: PriceProvider[], options: PriceIntegrationOptions = {}) {
    this.cache = new TtlCache(options.cacheTtlMs ?? 60_000, options.now);
    for (const provider of providers) {
      this.circuits.set(
        provider.slug,
        new CircuitBreaker({
          failureThreshold: options.circuitFailureThreshold,
          resetTimeoutMs: options.circuitResetTimeoutMs,
          now: options.now,
        })
      );
    }
  }

  async search(query: string, options: PriceSearchOptions = {}): Promise<PriceSearchResponse> {
    const normalizedQuery = query.trim().replace(/\s+/g, ' ');
    if (!normalizedQuery) throw new AppError('VALIDATION_ERROR', 'Informe um produto para pesquisar', 400);
    if (!this.providers.length) throw new AppError('SOURCE_UNAVAILABLE', 'Nenhuma fonte de preços está configurada', 503);

    const settled = await Promise.all(this.providers.map((provider) => this.searchProvider(provider, normalizedQuery)));
    const results = settled.flatMap((item) => item.results);
    const providers = settled.map(({ status }) => status);
    const successfulProviders = providers.filter((provider) => provider.state !== 'failed');

    if (!results.length && successfulProviders.length === 0 && !options.allowEmpty) {
      throw new AppError('SOURCE_UNAVAILABLE', 'As fontes de preços estão indisponíveis no momento', 503);
    }
    if (!results.length && !options.allowEmpty) {
      throw new AppError('NO_RESULTS', 'Nenhum produto foi encontrado', 404);
    }

    return { query: normalizedQuery, searchedAt: new Date().toISOString(), results, providers };
  }

  clearCache(): void {
    this.cache.clear();
  }

  private async searchProvider(provider: PriceProvider, query: string): Promise<{ results: NormalizedPriceResult[]; status: ProviderSearchStatus }> {
    try {
      const results = await this.cache.getOrSet(`${provider.slug}:${query.toLocaleLowerCase('pt-BR')}`, () =>
        this.executeProvider(provider, query)
      );
      const incompleteCount = results.filter((result) => result.incompleteFields.length > 0).length;
      return {
        results,
        status: {
          providerSlug: provider.slug,
          providerName: provider.displayName,
          state: results.length ? 'success' : 'empty',
          resultCount: results.length,
          incompleteCount,
          ...(incompleteCount ? { errorCode: 'INCOMPLETE_DATA', message: 'Alguns resultados não informam preço ou prazo.' } : {}),
          ...(!results.length ? { errorCode: 'NO_RESULTS', message: 'Nenhum produto encontrado nesta fonte.' } : {}),
        },
      };
    } catch (error) {
      const providerError = normalizeProviderError(error);
      return {
        results: [],
        status: {
          providerSlug: provider.slug,
          providerName: provider.displayName,
          state: 'failed',
          resultCount: 0,
          incompleteCount: 0,
          errorCode: publicErrorCode(providerError),
          message: publicErrorMessage(providerError),
        },
      };
    }
  }

  private executeProvider(provider: PriceProvider, query: string): Promise<NormalizedPriceResult[]> {
    const circuit = this.circuits.get(provider.slug);
    if (!circuit) {
      return Promise.reject(new ProviderError('PROVIDER_UNAVAILABLE', 'A fonte não está configurada corretamente.'));
    }
    return circuit.execute(() => provider.search({ query }));
  }
}

function normalizeProviderError(error: unknown): ProviderError {
  if (isProviderError(error)) return error;
  return new ProviderError('PROVIDER_UNAVAILABLE', 'Não foi possível consultar a fonte.', error);
}

function publicErrorCode(error: ProviderError): string {
  switch (error.code) {
    case 'PROVIDER_RATE_LIMIT':
      return 'RATE_LIMIT_EXCEEDED';
    case 'PROVIDER_TIMEOUT':
    case 'PROVIDER_UNAVAILABLE':
    case 'PROVIDER_CIRCUIT_OPEN':
      return 'SOURCE_UNAVAILABLE';
    case 'PROVIDER_UNAUTHORIZED':
      return 'SOURCE_UNAUTHORIZED';
    case 'PROVIDER_INVALID_RESPONSE':
      return 'SOURCE_INVALID_RESPONSE';
  }
}

function publicErrorMessage(error: ProviderError): string {
  switch (publicErrorCode(error)) {
    case 'RATE_LIMIT_EXCEEDED':
      return 'A fonte informou que o limite de requisições foi atingido.';
    case 'SOURCE_UNAUTHORIZED':
      return 'Esta fonte exige credenciais de acesso que não estão configuradas.';
    case 'SOURCE_INVALID_RESPONSE':
      return 'A fonte retornou dados em formato inválido.';
    default:
      return 'Esta fonte está indisponível; os demais resultados continuam disponíveis.';
  }
}
