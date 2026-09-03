import { ProviderError } from './provider-error';

export type FetchImplementation = typeof fetch;

interface FetchJsonOptions {
  signal?: AbortSignal;
  timeoutMs: number;
  fetchImplementation?: FetchImplementation;
  headers?: Record<string, string>;
}

export async function fetchJson<T>(url: string, options: FetchJsonOptions): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), options.timeoutMs);
  const abortParent = () => controller.abort();

  options.signal?.addEventListener('abort', abortParent, { once: true });

  try {
    const fetchImplementation = options.fetchImplementation || fetch;
    const response = await fetchImplementation(url, {
      headers: { Accept: 'application/json', ...options.headers },
      signal: controller.signal,
    });

    if (response.status === 429) {
      throw new ProviderError('PROVIDER_RATE_LIMIT', 'A fonte atingiu o limite de requisições.');
    }

    // 401/403 significa credencial ausente ou recusada, não payload malformado.
    if (response.status === 401 || response.status === 403) {
      throw new ProviderError(
        'PROVIDER_UNAUTHORIZED',
        `A fonte recusou a consulta por falta de credenciais (HTTP ${response.status}).`
      );
    }

    if (!response.ok) {
      throw new ProviderError(
        response.status >= 500 ? 'PROVIDER_UNAVAILABLE' : 'PROVIDER_INVALID_RESPONSE',
        `A fonte respondeu com HTTP ${response.status}.`
      );
    }

    try {
      return (await response.json()) as T;
    } catch (error) {
      throw new ProviderError('PROVIDER_INVALID_RESPONSE', 'A fonte retornou um JSON inválido.', error);
    }
  } catch (error) {
    if (error instanceof ProviderError) throw error;

    if (controller.signal.aborted) {
      throw new ProviderError('PROVIDER_TIMEOUT', 'A fonte demorou mais que o tempo limite.', error);
    }

    throw new ProviderError('PROVIDER_UNAVAILABLE', 'Não foi possível consultar a fonte.', error);
  } finally {
    clearTimeout(timeout);
    options.signal?.removeEventListener('abort', abortParent);
  }
}
