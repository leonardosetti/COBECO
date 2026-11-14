// COBECO Frontend — ApiClient Unit Tests
// Testes para ApiClient: request/response, interceptors, error handling

import { ApiClient } from '../../src/app.js';

// Mock fetch global
global.fetch = jest.fn();

// Mock State
jest.mock('../../src/app.js', () => {
  const actual = jest.requireActual('../../src/app.js');
  return {
    ...actual,
    State: {
      getAccessToken: jest.fn(),
      clearUser: jest.fn(),
    },
  };
});

import { State } from '../../src/app.js';

describe('ApiClient', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    fetch.mockReset();
    State.getAccessToken.mockReturnValue('test_token');
    State.clearUser.mockImplementation(() => {});
  });

  describe('request method', () => {
    test('faz requisição GET com headers corretos', async () => {
      const mockResponse = { ok: true, json: () => Promise.resolve({ data: 'test' }) };
      fetch.mockResolvedValue(mockResponse);

      const result = await ApiClient.request('/test-endpoint', { method: 'GET' });

      expect(fetch).toHaveBeenCalledWith(
        '/v1/test-endpoint',
        expect.objectContaining({
          method: 'GET',
          headers: expect.objectContaining({
            'Authorization': 'Bearer test_token',
            'Content-Type': 'application/json',
          }),
        })
      );
      expect(result).toEqual({ data: 'test' });
    });

    test('faz requisição POST com body', async () => {
      const mockResponse = { ok: true, json: () => Promise.resolve({ sdoc-arch-0006-uc-v1cess: true }) };
      fetch.mockResolvedValue(mockResponse);

      const result = await ApiClient.request('/test', {
        method: 'POST',
        body: JSON.stringify({ key: 'value' }),
      });

      expect(fetch).toHaveBeenCalledWith(
        '/v1/test',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ key: 'value' }),
        })
      );
    });

    test('adiciona Authorization header quando token existe', async () => {
      fetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({}) });
      
      await ApiClient.request('/test');
      
      const callArgs = fetch.mock.calls[0];
      expect(callArgs[1].headers.Authorization).toBe('Bearer test_token');
    });

    test('não adiciona Authorization quando token não existe', async () => {
      State.getAccessToken.mockReturnValue(null);
      fetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({}) });
      
      await ApiClient.request('/test');
      
      const callArgs = fetch.mock.calls[0];
      expect(callArgs[1].headers.Authorization).toBeUndefined();
    });
  });

  describe('Error Handling', () => {
    test('lança erro em resposta 401', async () => {
      fetch.mockResolvedValue({ ok: false, status: 401 });
      
      await expect(ApiClient.request('/test')).rejects.toThrow('Não autenticado');
    });

    test('lança erro em resposta 403', async () => {
      fetch.mockResolvedValue({ ok: false, status: 403 });
      
      await expect(ApiClient.request('/test')).rejects.toThrow('Acesso negado');
    });

    test('lança erro em resposta 404', async () => {
      fetch.mockResolvedValue({ ok: false, status: 404 });
      
      await expect(ApiClient.request('/test')).rejects.toThrow('Recurso não encontrado');
    });

    test('lança erro genérico em outras falhas', async () => {
      fetch.mockResolvedValue({ ok: false, status: 500 });
      
      await expect(ApiClient.request('/test')).rejects.toThrow('Erro na requisição');
    });

    test('chama clearUser em 401', async () => {
      fetch.mockResolvedValue({ ok: false, status: 401 });
      
      await expect(ApiClient.request('/test')).rejects.toThrow();
      expect(State.clearUser).toHaveBeenCalled();
    });
  });

  describe('Convenience Methods', () => {
    test('login faz POST para /auth/login', async () => {
      fetch.mockResolvedValue({ 
        ok: true, 
        json: () => Promise.resolve({ access_token: 'token', user_id: 1 }) 
      });
      
      const result = await ApiClient.login({ nome_usuario: 'user', senha: 'pass' });
      
      expect(fetch).toHaveBeenCalledWith(
        '/v1/auth/login',
        expect.objectContaining({ method: 'POST' })
      );
      expect(result).toEqual({ access_token: 'token', user_id: 1 });
    });

    test('cadastrar faz POST para /auth/cadastrar', async () => {
      fetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ usuario_id: 1 }) });
      
      await ApiClient.cadastrar({ nome_usuario: 'user', email: 'a@b.com', senha: 'pass' });
      
      expect(fetch).toHaveBeenCalledWith('/v1/auth/cadastrar', expect.objectContaining({ method: 'POST' }));
    });

    test('getPerfil faz GET para /auth/perfil', async () => {
      fetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ nome: 'User' }) });
      
      const result = await ApiClient.getPerfil();
      
      expect(fetch).toHaveBeenCalledWith('/v1/auth/perfil', expect.objectContaining({ method: 'GET' }));
      expect(result).toEqual({ nome: 'User' });
    });

    test('atualizarPerfil faz PUT para /auth/perfil', async () => {
      fetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ nome: 'Novo' }) });
      
      const result = await ApiClient.atualizarPerfil({ nome: 'Novo' });
      
      expect(fetch).toHaveBeenCalledWith(
        '/v1/auth/perfil',
        expect.objectContaining({ method: 'PUT', body: JSON.stringify({ nome: 'Novo' }) })
      );
      expect(result).toEqual({ nome: 'Novo' });
    });
  });
});