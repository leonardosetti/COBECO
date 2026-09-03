import { FetchImplementation } from '../http-client';
import { ProviderError } from '../provider-error';

export interface OpenRouterModelConfig {
  model: string;
  apiKey: string;
}

export interface OpenRouterMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface OpenRouterCompletion {
  model: string;
  content: string;
}

interface ChatCompletionResponse {
  model?: unknown;
  choices?: unknown;
}

const DEFAULT_BASE_URL = 'https://openrouter.ai/api/v1';
const DEFAULT_TIMEOUT_MS = 30_000;

/**
 * Cliente de chat completion do OpenRouter.
 *
 * Ainda não é consumido por nenhuma rota: existe para que a integração de LLM
 * prevista para depois do MVP comece de um ponto testado, com credenciais já
 * isoladas em variáveis de ambiente. Segue o mesmo contrato de erro dos demais
 * providers (`ProviderError`), então pode ser embrulhado pelo circuit breaker
 * e pelo cache TTL existentes sem adaptação.
 */
export class OpenRouterClient {
  constructor(
    private readonly primary: OpenRouterModelConfig,
    private readonly fallback?: OpenRouterModelConfig,
    private readonly baseUrl = DEFAULT_BASE_URL,
    private readonly fetchImplementation?: FetchImplementation,
    private readonly timeoutMs = DEFAULT_TIMEOUT_MS
  ) {}

  /**
   * Envia as mensagens ao modelo principal. Se ele estiver indisponível ou
   * limitado por cota, repete a chamada no modelo de fallback — quando houver.
   */
  async complete(messages: OpenRouterMessage[], signal?: AbortSignal): Promise<OpenRouterCompletion> {
    if (!messages.length) {
      throw new ProviderError('PROVIDER_INVALID_RESPONSE', 'Informe ao menos uma mensagem.');
    }

    try {
      return await this.request(this.primary, messages, signal);
    } catch (error) {
      if (!this.fallback || !isRetryable(error)) throw error;
      return this.request(this.fallback, messages, signal);
    }
  }

  private async request(
    config: OpenRouterModelConfig,
    messages: OpenRouterMessage[],
    signal?: AbortSignal
  ): Promise<OpenRouterCompletion> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.timeoutMs);
    const abortParent = () => controller.abort();
    signal?.addEventListener('abort', abortParent, { once: true });

    try {
      const fetchImplementation = this.fetchImplementation || fetch;
      const response = await fetchImplementation(`${this.baseUrl}/chat/completions`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${config.apiKey}`,
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({ model: config.model, messages }),
        signal: controller.signal,
      });

      if (response.status === 429) {
        throw new ProviderError('PROVIDER_RATE_LIMIT', 'O OpenRouter atingiu o limite de requisições.');
      }

      if (response.status === 401 || response.status === 403) {
        throw new ProviderError(
          'PROVIDER_UNAUTHORIZED',
          `O OpenRouter recusou a credencial (HTTP ${response.status}).`
        );
      }

      if (!response.ok) {
        throw new ProviderError(
          response.status >= 500 ? 'PROVIDER_UNAVAILABLE' : 'PROVIDER_INVALID_RESPONSE',
          `O OpenRouter respondeu com HTTP ${response.status}.`
        );
      }

      const payload = (await response.json()) as ChatCompletionResponse;
      const content = extractContent(payload);
      if (content === null) {
        throw new ProviderError('PROVIDER_INVALID_RESPONSE', 'O OpenRouter retornou uma resposta sem conteúdo.');
      }

      return {
        model: typeof payload.model === 'string' ? payload.model : config.model,
        content,
      };
    } catch (error) {
      if (error instanceof ProviderError) throw error;
      if (controller.signal.aborted) {
        throw new ProviderError('PROVIDER_TIMEOUT', 'O OpenRouter demorou mais que o tempo limite.', error);
      }
      throw new ProviderError('PROVIDER_UNAVAILABLE', 'Não foi possível consultar o OpenRouter.', error);
    } finally {
      clearTimeout(timeout);
      signal?.removeEventListener('abort', abortParent);
    }
  }
}

/**
 * Monta o cliente a partir do ambiente. Devolve `null` quando não há chave
 * configurada, para que a ausência da credencial desabilite o recurso em vez de
 * derrubar a inicialização da API.
 */
export function createOpenRouterClient(
  fetchImplementation?: FetchImplementation
): OpenRouterClient | null {
  const apiKey = process.env.OPENROUTER_API_KEY?.trim();
  const model = process.env.OPENROUTER_MODEL?.trim();
  if (!apiKey || !model) return null;

  const fallbackKey = process.env.OPENROUTER_FALLBACK_API_KEY?.trim();
  const fallbackModel = process.env.OPENROUTER_FALLBACK_MODEL?.trim();
  const fallback =
    fallbackKey && fallbackModel ? { apiKey: fallbackKey, model: fallbackModel } : undefined;

  return new OpenRouterClient(
    { apiKey, model },
    fallback,
    process.env.OPENROUTER_BASE_URL?.trim() || DEFAULT_BASE_URL,
    fetchImplementation
  );
}

function isRetryable(error: unknown): boolean {
  return (
    error instanceof ProviderError &&
    (error.code === 'PROVIDER_RATE_LIMIT' ||
      error.code === 'PROVIDER_UNAVAILABLE' ||
      error.code === 'PROVIDER_TIMEOUT')
  );
}

function extractContent(payload: ChatCompletionResponse): string | null {
  if (!Array.isArray(payload.choices) || !payload.choices.length) return null;
  const [choice] = payload.choices;
  if (!choice || typeof choice !== 'object') return null;
  const message = (choice as { message?: unknown }).message;
  if (!message || typeof message !== 'object') return null;
  const content = (message as { content?: unknown }).content;
  return typeof content === 'string' && content.length > 0 ? content : null;
}
