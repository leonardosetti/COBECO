// COBECO Frontend — State Management Unit Tests
// Testes para State singleton: user, token, ephemeral list

import { State } from '../../src/app.js';

// Mock localStorage
const mockLocalStorage = {
  store: {},
  getItem(key) { return this.store[key] || null; },
  setItem(key, value) { this.store[key] = value.toString(); },
  removeItem(key) { delete this.store[key]; },
  clear() { this.store = {}; },
};

global.localStorage = mockLocalStorage;
global.sessionStorage = mockLocalStorage;

describe('State Management', () => {
  beforeEach(() => {
    mockLocalStorage.clear();
    // Reset State singleton
    State.user = null;
    State.accessToken = null;
  });

  describe('User Authentication State', () => {
    test('setUser armazena usuário e token', () => {
      const user = {
        id: 1,
        nome_usuario: 'testuser',
        email: 'test@teste.com',
        nome: 'Test User',
      };
      const token = 'access_token_123';

      State.setUser(user, token);

      expect(State.user).toEqual(user);
      expect(State.accessToken).toBe(token);
      expect(localStorage.getItem('cobeco_user')).toBe(JSON.stringify(user));
      expect(localStorage.getItem('cobeco_access_token')).toBe(token);
    });

    test('clearUser remove usuário e tokens', () => {
      State.setUser({ id: 1, nome_usuario: 'test' }, 'token');
      State.clearUser();

      expect(State.user).toBeNull();
      expect(State.accessToken).toBeNull();
      expect(localStorage.getItem('cobeco_user')).toBeNull();
      expect(localStorage.getItem('cobeco_access_token')).toBeNull();
    });

    test('isAuthenticated retorna true quando usuário logado', () => {
      State.setUser({ id: 1 }, 'token');
      expect(State.isAuthenticated()).toBe(true);
    });

    test('isAuthenticated retorna false quando não logado', () => {
      State.clearUser();
      expect(State.isAuthenticated()).toBe(false);
    });

    test('getUser retorna usuário atual', () => {
      const user = { id: 1, nome_usuario: 'test' };
      State.setUser(user, 'token');
      expect(State.getUser()).toEqual(user);
    });

    test('getAccessToken retorna token atual', () => {
      State.setUser({ id: 1 }, 'my_token');
      expect(State.getAccessToken()).toBe('my_token');
    });
  });

  describe('Ephemeral List State', () => {
    test('setEphemeralList armazena lista temporária', () => {
      const list = { nome: 'Teste', itens: [{ produto_id: 1, quantidade: 2 }] };
      State.setEphemeralList(list);

      expect(State.ephemeralList).toEqual(list);
      expect(JSON.parse(localStorage.getItem('cobeco_ephemeral_list'))).toEqual(list);
    });

    test('getEphemeralList retorna lista', () => {
      const list = { nome: 'Teste', itens: [] };
      State.setEphemeralList(list);
      expect(State.getEphemeralList()).toEqual(list);
    });

    test('clearEphemeralList limpa lista', () => {
      State.setEphemeralList({ nome: 'Teste' });
      State.clearEphemeralList();

      expect(State.ephemeralList).toBeNull();
      expect(localStorage.getItem('cobeco_ephemeral_list')).toBeNull();
    });

    test('hasEphemeralList verifica existência', () => {
      expect(State.hasEphemeralList()).toBe(false);
      State.setEphemeralList({ nome: 'Teste' });
      expect(State.hasEphemeralList()).toBe(true);
      State.clearEphemeralList();
      expect(State.hasEphemeralList()).toBe(false);
    });
  });

  describe('Persistência', () => {
    test('init restaura usuário do localStorage', () => {
      const user = { id: 1, nome_usuario: 'persisted' };
      localStorage.setItem('cobeco_user', JSON.stringify(user));
      localStorage.setItem('cobeco_access_token', 'persisted_token');

      State.init();

      expect(State.user).toEqual(user);
      expect(State.accessToken).toBe('persisted_token');
    });

    test('init restaura ephemeral list', () => {
      const list = { nome: 'Restaurada', itens: [{ id: 1 }] };
      localStorage.setItem('cobeco_ephemeral_list', JSON.stringify(list));

      State.init();

      expect(State.ephemeralList).toEqual(list);
    });

    test('init ignora localStorage corrompido', () => {
      localStorage.setItem('cobeco_user', 'invalid_json{');
      State.init();
      expect(State.user).toBeNull();
    });
  });
});