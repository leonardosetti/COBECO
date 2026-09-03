import { afterEach, describe, expect, it, vi } from 'vitest';
import { OpenRouterClient, createOpenRouterClient } from './openrouter.client';
import { ProviderError } from '../provider-error';

const PRIMARY = { model: 'stealth/ox-alpha', apiKey: 'chave-primaria' };
const FALLBACK = { model: 'nvidia/nemotron-3.5-lightning:free', apiKey: 'chave-fallback' };
const MENSAGENS = [{ role: 'user' as const, content: 'Resuma esta cotação.' }];

function respostaOk(content: string, model = PRIMARY.model): Response {
  return {
    ok: true,
    status: 200,
    json: async () => ({ model, choices: [{ message: { role: 'assistant', content } }] }),
  } as unknown as Response;
}

function respostaErro(status: number): Response {
  return { ok: false, status, json: async () => ({}) } as unknown as Response;
}

describe('OpenRouterClient', () => {
  afterEach(() => {
    delete process.env.OPENROUTER_API_KEY;
    delete process.env.OPENROUTER_MODEL;
    delete process.env.OPENROUTER_FALLBACK_API_KEY;
    delete process.env.OPENROUTER_FALLBACK_MODEL;
  });

  it('envia o modelo e a credencial configurados e devolve o conteúdo', async () => {
    const fetchMock = vi.fn().mockResolvedValue(respostaOk('Grupo 1 tem o menor custo.'));
    const client = new OpenRouterClient(PRIMARY, undefined, 'https://openrouter.test/v1', fetchMock);

    const resultado = await client.complete(MENSAGENS);

    expect(resultado).toEqual({ model: PRIMARY.model, content: 'Grupo 1 tem o menor custo.' });
    const [url, init] = fetchMock.mock.calls[0];
    expect(url).toBe('https://openrouter.test/v1/chat/completions');
    expect(init.method).toBe('POST');
    expect(init.headers.Authorization).toBe(`Bearer ${PRIMARY.apiKey}`);
    expect(JSON.parse(init.body)).toEqual({ model: PRIMARY.model, messages: MENSAGENS });
  });

  it('recorre ao modelo de fallback quando o principal atinge o limite de cota', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce(respostaErro(429))
      .mockResolvedValueOnce(respostaOk('resposta do fallback', FALLBACK.model));
    const client = new OpenRouterClient(PRIMARY, FALLBACK, 'https://openrouter.test/v1', fetchMock);

    const resultado = await client.complete(MENSAGENS);

    expect(resultado.model).toBe(FALLBACK.model);
    expect(fetchMock).toHaveBeenCalledTimes(2);
    expect(fetchMock.mock.calls[1][1].headers.Authorization).toBe(`Bearer ${FALLBACK.apiKey}`);
  });

  it('não tenta o fallback quando a credencial é recusada', async () => {
    const fetchMock = vi.fn().mockResolvedValue(respostaErro(401));
    const client = new OpenRouterClient(PRIMARY, FALLBACK, 'https://openrouter.test/v1', fetchMock);

    await expect(client.complete(MENSAGENS)).rejects.toMatchObject({
      code: 'PROVIDER_UNAUTHORIZED',
    });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('rejeita resposta sem conteúdo utilizável', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ choices: [] }),
    } as unknown as Response);
    const client = new OpenRouterClient(PRIMARY, undefined, 'https://openrouter.test/v1', fetchMock);

    await expect(client.complete(MENSAGENS)).rejects.toBeInstanceOf(ProviderError);
  });

  it('createOpenRouterClient devolve null sem credencial configurada', () => {
    expect(createOpenRouterClient()).toBeNull();
  });

  it('createOpenRouterClient monta o cliente a partir do ambiente', async () => {
    process.env.OPENROUTER_API_KEY = PRIMARY.apiKey;
    process.env.OPENROUTER_MODEL = PRIMARY.model;
    const fetchMock = vi.fn().mockResolvedValue(respostaOk('ok'));

    const client = createOpenRouterClient(fetchMock);

    expect(client).not.toBeNull();
    await client!.complete(MENSAGENS);
    expect(fetchMock.mock.calls[0][0]).toContain('/chat/completions');
  });
});
