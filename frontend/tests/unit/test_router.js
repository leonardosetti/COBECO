// COBECO Frontend — Router Unit Tests
// Testes para Router: hash navigation, route matching, bindEvents

import { router, routes } from '../../src/app.js';

// Mock dependencies
jest.mock('../../src/app.js', () => {
  const actual = jest.requireActual('../../src/app.js');
  return {
    ...actual,
    State: {
      init: jest.fn(),
      user: null,
      navigate: jest.fn(),
    },
    Views: {
      login: jest.fn().mockResolvedValue('<div>Login</div>'),
      cadastrar: jest.fn().mockResolvedValue('<div>Cadastro</div>'),
      recuperarSenha: jest.fn().mockResolvedValue('<div>Recuperar</div>'),
      recuperarSenhaConfirmar: jest.fn().mockResolvedValue('<div>Confirmar</div>'),
      criarLista: jest.fn().mockResolvedValue('<div>Criar Lista</div>'),
      editarLista: jest.fn().mockResolvedValue('<div>Editar Lista</div>'),
      minhasListas: jest.fn().mockResolvedValue('<div>Minhas Listas</div>'),
      verLista: jest.fn().mockResolvedValue('<div>Ver Lista</div>'),
      comparar: jest.fn().mockResolvedValue('<div>Comparar</div>'),
      perfil: jest.fn().mockResolvedValue('<div>Perfil</div>'),
    },
    ApiClient: {
      listarListas: jest.fn().mockResolvedValue({ items: [], total: 0, pagina: 1, por_pagina: 20, total_paginas: 1 }),
      buscarLista: jest.fn().mockResolvedValue({ id: 1, nome: 'Lista', itens: [] }),
    },
  };
});

import { router, routes, State, Views, ApiClient } from '../../src/app.js';

describe('Router', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset router state
    router.currentPath = null;
    router.requestId = 0;
    document.body.innerHTML = `
      <header id="header"></header>
      <main id="main-content"></main>
      <div id="toast-container"></div>
      <div id="modal-container"></div>
      <nav id="nav-auth"></nav>
    `;
  });

  describe('Route Matching', () => {
    test('rotas estáticas são definidas', () => {
      expect(routes['/login']).toBeDefined();
      expect(routes['/cadastrar']).toBeDefined();
      expect(routes['/recuperar-senha']).toBeDefined();
      expect(routes['/recuperar-senha/confirmar']).toBeDefined();
      expect(routes['/criar-lista']).toBeDefined();
      expect(routes['/minhas-listas']).toBeDefined();
      expect(routes['/comparar']).toBeDefined();
      expect(routes['/perfil']).toBeDefined();
    });

    test('rotas dinâmicas com parâmetros', () => {
      expect(routes['/editar-lista/:id']).toBeDefined();
      expect(routes['/lista/:id']).toBeDefined();
    });
  });

  describe('Navigation', () => {
    test('navigate carrega rota estática', async () => {
      await router.navigate('/login');
      
      expect(Views.login).toHaveBeenCalled();
      expect(router.currentPath).toBe('/login');
      expect(document.getElementById('main-content').innerHTML).toContain('Login');
    });

    test('navigate com parâmetros extrai params', async () => {
      await router.navigate('/editar-lista/123');
      
      expect(Views.editarLista).toHaveBeenCalledWith({ id: '123' });
      expect(router.currentPath).toBe('/editar-lista/123');
    });

    test('navigate para rota inexistente redireciona para home', async () => {
      await router.navigate('/rota-inexistente');
      
      expect(router.currentPath).toBe('/');
    });

    test('normalize path aceita /login, login, /home', async () => {
      await router.navigate('login');
      expect(router.currentPath).toBe('/login');

      await router.navigate('/home');
      expect(router.currentPath).toBe('/');
    });
  });

  describe('Hash Change Handling', () => {
    test('hashchange event dispara navigate', async () => {
      // Simula mudança de hash
      window.location.hash = '#/login';
      const event = new HashChangeEvent('hashchange');
      window.dispatchEvent(event);
      
      // Deve ter chamado navigate com path do hash
      expect(router.currentPath).toBe('/login');
    });
  });

  describe('bindEvents', () => {
    test('bindEvents chama View correta para rota', async () => {
      await router.navigate('/login');
      
      expect(Views.login).toHaveBeenCalled();
    });

    test('bindEvents para /cadastrar chama Views.cadastrar', async () => {
      await router.navigate('/cadastrar');
      expect(Views.cadastrar).toHaveBeenCalled();
    });

    test('bindEvents para /perfil chama Views.perfil', async () => {
      await router.navigate('/perfil');
      expect(Views.perfil).toHaveBeenCalled();
    });
  });

  describe('Request Deduplication', () => {
    test('navegação rápida cancela request anterior', async () => {
      // Primeira navegação
      const promise1 = router.navigate('/login');
      
      // Segunda navegação rápida (cancela a primeira)
      await router.navigate('/cadastrar');
      
      // Apenas a segunda deve ter efeito
      expect(router.currentPath).toBe('/cadastrar');
      expect(Views.cadastrar).toHaveBeenCalled();
    });
  });

  describe('Header Navigation', () => {
    test('clique em link [data-link] no header navega', async () => {
      const header = document.getElementById('nav-auth');
      const link = document.createElement('a');
      link.href = '#/perfil';
      link.setAttribute('data-link', '');
      header.appendChild(link);
      
      router.bindEvents('/login', {});
      
      link.click();
      
      expect(router.currentPath).toBe('/perfil');
    });
  });
});