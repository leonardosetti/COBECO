// COBECO Frontend — Main Application (Vanilla JS ES6+)
// Desktop-first, Clean Architecture inspired, no frameworks

// ============================================================
// CONFIGURAÇÃO & CONSTANTES
// ============================================================
const API_BASE = '/v1';
const STORAGE_KEYS = {
  AUTH_TOKEN: 'cobeco_access_token',
  REFRESH_TOKEN: 'cobeco_refresh_token',
  USER: 'cobeco_user',
  EPHEMERAL_LIST: 'cobeco_ephemeral_list',
};

// ============================================================
// UTILITÁRIOS
// ============================================================
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

const formatCurrency = (value) => {
  if (value === null || value === undefined) return 'N/D';
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
};

const formatDate = (isoString) => {
  if (!isoString) return '';
  return new Date(isoString).toLocaleDateString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  });
};

const showToast = (message, type = 'info') => {
  const container = $('#toast-container');
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span class="flex-1">${message}</span>
    <button class="text-white/80 hover:text-white" aria-label="Fechar">&times;</button>
  `;
  toast.querySelector('button').onclick = () => toast.remove();
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 5000);
};

const showModal = (content, options = {}) => {
  const container = $('#modal-container');
  container.innerHTML = `
    <div class="modal-overlay" data-close-overlay>
      <div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
        ${options.title ? `<div class="modal-header"><h2 id="modal-title" class="text-lg font-semibold">${options.title}</h2><button class="text-gray-400 hover:text-gray-600" data-close-modal>&times;</button></div>` : ''}
        <div class="modal-body">${content}</div>
        ${options.footer ? `<div class="modal-footer">${options.footer}</div>` : ''}
      </div>
    </div>
  `;
  container.classList.remove('hidden');
  document.body.style.overflow = 'hidden';

  const close = () => {
    container.classList.add('hidden');
    container.innerHTML = '';
    document.body.style.overflow = '';
  };

  container.querySelector('[data-close-overlay]').onclick = (e) => {
    if (e.target === e.currentTarget) close();
  };
  container.querySelectorAll('[data-close-modal]').forEach(btn => btn.onclick = close);
  document.addEventListener('keydown', function esc(e) {
    if (e.key === 'Escape') { close(); document.removeEventListener('keydown', esc); }
  });

  return { close };
};

// ============================================================
// API CLIENT
// ============================================================
class ApiClient {
  static getToken() {
    return localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
  }

  static setTokens(access, refresh) {
    localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, access);
    // refresh token vem no cookie httpOnly
  }

  static clearTokens() {
    localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.USER);
  }

  static async request(endpoint, options = {}) {
    const token = this.getToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
      credentials: 'include', // Importante para cookies httpOnly
    });

    if (response.status === 401) {
      // Tenta refresh token
      const refreshed = await this.refreshToken();
      if (refreshed) {
        // Re-tenta requisição original
        return this.request(endpoint, options);
      }
      // Refresh falhou - logout
      this.clearTokens();
      window.location.href = '/login';
      throw new Error('Sessão expirada');
    }

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.detail || `Erro ${response.status}`);
    }

    return data;
  }

  static async refreshToken() {
    try {
      const response = await fetch(`${API_BASE}/auth/refresh`, {
        method: 'POST',
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        this.setTokens(data.access_token, data.refresh_token);
        return true;
      }
    } catch {}
    return false;
  }

  // Auth
  static login(credentials) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  static cadastrar(data) {
    return this.request('/auth/cadastrar', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  static logout() {
    return this.request('/auth/logout', { method: 'POST' });
  }

  static getPerfil() {
    return this.request('/auth/perfil');
  }

  static atualizarPerfil(data) {
    return this.request('/auth/perfil', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // Listas
  static salvarLista(data) {
    return this.request('/listas', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  static listarListas(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/listas?${query}`);
  }

  static buscarLista(id) {
    return this.request(`/listas/${id}`);
  }

  static atualizarLista(id, data) {
    return this.request(`/listas/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  static excluirLista(id, confirmacaoNome) {
    return this.request(`/listas/${id}?confirmacao_nome=${encodeURIComponent(confirmacaoNome)}`, {
      method: 'DELETE',
    });
  }

  static promoverEfemera(data) {
    return this.request('/listas/promover-efemera', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Catálogo
  static listarCategorias() {
    return this.request('/catalogo/categorias');
  }

  static listarFornecedores(categorias = []) {
    const query = categorias.length ? `?categorias=${categorias.join(',')}` : '';
    return this.request(`/catalogo/fornecedores${query}`);
  }

  static autocompleteProdutos(q, limit = 10) {
    return this.request(`/catalogo/produtos/autocomplete?q=${encodeURIComponent(q)}&limit=${limit}`);
  }

  static calcularDisponibilidade(fornecedorId, produtoIds) {
    return this.request(`/catalogo/fornecedores/${fornecedorId}/disponibilidade?produtos=${produtoIds.join(',')}`);
  }

  // Comparação
  static calcularOrcamento(data) {
    return this.request('/comparacao/calcular', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Exportação
  static exportarPDF(listaId) {
    return fetch(`${API_BASE}/export/pdf?lista_id=${listaId}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.getToken()}`,
      },
      credentials: 'include',
    }).then(r => {
      if (!r.ok) throw new Error('Erro ao gerar PDF');
      return r.blob();
    });
  }
}

// ============================================================
// STATE MANAGEMENT (Simples, reativo)
// ============================================================
const State = {
  user: null,
  ephemeralList: null,
  currentView: 'home',

  init() {
    const token = localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
    const user = localStorage.getItem(STORAGE_KEYS.USER);
    const ephemeral = sessionStorage.getItem(STORAGE_KEYS.EPHEMERAL_LIST);

    if (token && user) {
      this.user = JSON.parse(user);
    }
    if (ephemeral) {
      this.ephemeralList = JSON.parse(ephemeral);
    }
    this.updateAuthUI();
  },

  setUser(user, token) {
    this.user = user;
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
    localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, token);
    this.updateAuthUI();
  },

  clearUser() {
    this.user = null;
    localStorage.removeItem(STORAGE_KEYS.USER);
    localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
    this.updateAuthUI();
  },

  setEphemeralList(list) {
    this.ephemeralList = list;
    sessionStorage.setItem(STORAGE_KEYS.EPHEMERAL_LIST, JSON.stringify(list));
  },

  clearEphemeralList() {
    this.ephemeralList = null;
    sessionStorage.removeItem(STORAGE_KEYS.EPHEMERAL_LIST);
  },

  updateAuthUI() {
    const nav = $('#nav-auth');
    if (this.user) {
      nav.innerHTML = `
        <span class="text-sm text-gray-600">${this.user.nome}</span>
        <button id="btn-logout" class="btn btn-ghost text-sm">Sair</button>
      `;
      $('#btn-logout')?.addEventListener('click', () => AuthViews.logout());
    } else {
      nav.innerHTML = `
        <a href="/login" class="btn btn-ghost text-sm">Entrar</a>
        <a href="/cadastrar" class="btn btn-primary text-sm">Cadastrar</a>
      `;
    }
  },

  navigate(view, params = {}) {
    this.currentView = view;
    router.navigate(view, params);
  },
};

// ============================================================
// VIEWS — Cada tela da aplicação
// ============================================================
const Views = {
  // Home / Landing
  home() {
    return `
      <section class="text-center py-16">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">Compare preços e economize</h2>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Crie sua lista de compras, compare preços entre fornecedores e encontre o melhor orçamento.
          Dados mockados para fins acadêmicos.
        </p>
        <div class="flex gap-4 justify-center">
          <a href="#/criar-lista" class="btn btn-primary text-lg px-8" data-link>Criar Lista</a>
          <a href="#/comparar" class="btn btn-secondary text-lg px-8" data-link>Comparar Preços</a>
        </div>
      </section>

      <section class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="card">
          <div class="card-body text-center">
            <div class="w-12 h-12 mx-auto mb-4 bg-primary-100 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            </div>
            <h3 class="text-lg font-semibold mb-2">Crie sua Lista</h3>
            <p class="text-gray-600">Adicione produtos com autocomplete e defina quantidades.</p>
          </div>
        </div>
        <div class="card">
          <div class="card-body text-center">
            <div class="w-12 h-12 mx-auto mb-4 bg-primary-100 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
            </div>
            <h3 class="text-lg font-semibold mb-2">Compare Fornecedores</h3>
            <p class="text-gray-600">Filtre por categorias, selecione fornecedores e veja a tabela comparativa.</p>
          </div>
        </div>
        <div class="card">
          <div class="card-body text-center">
            <div class="w-12 h-12 mx-auto mb-4 bg-primary-100 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
            </div>
            <h3 class="text-lg font-semibold mb-2">Exporte e Imprima</h3>
            <p class="text-gray-600">Gere PDF profissional ou imprima direto do navegador.</p>
          </div>
        </div>
      </section>
    `;
  },

  // Login
  login() {
    return `
      <div class="max-w-md mx-auto">
        <div class="card">
          <div class="card-header">
            <h2 class="text-xl font-semibold">Entrar na sua conta</h2>
          </div>
          <div class="card-body">
            <form id="form-login" class="space-y-4">
              <div class="form-group">
                <label for="login-usuario" class="label">Nome de usuário</label>
                <input type="text" id="login-usuario" name="nome_usuario" class="input" required autocomplete="username">
              </div>
              <div class="form-group">
                <label for="login-senha" class="label">Senha</label>
                <input type="password" id="login-senha" name="senha" class="input" required autocomplete="current-password">
              </div>
              <button type="submit" class="btn btn-primary w-full">Entrar</button>
            </form>
            <p class="text-center text-sm text-gray-600 mt-6">
              Não tem conta? <a href="/cadastrar" class="text-primary-600 hover:underline" data-link>Cadastre-se</a>
            </p>
            <p class="text-center text-sm text-gray-600 mt-2">
              <a href="/recuperar-senha" class="text-primary-600 hover:underline" data-link>Esqueci minha senha</a>
            </p>
          </div>
        </div>
      </div>
    `;
  },

  // Cadastro
  cadastrar() {
    return `
      <div class="max-w-md mx-auto">
        <div class="card">
          <div class="card-header">
            <h2 class="text-xl font-semibold">Criar conta</h2>
          </div>
          <div class="card-body">
            <form id="form-cadastro" class="space-y-4">
              <div class="form-group">
                <label for="cad-nome-usuario" class="label">Nome de usuário <span class="text-red-500">*</span></label>
                <input type="text" id="cad-nome-usuario" name="nome_usuario" class="input" required
                  minlength="3" maxlength="30" pattern="[a-zA-Z0-9]+" autocomplete="username">
                <p class="text-xs text-gray-500 mt-1">3-30 caracteres, apenas letras e números</p>
              </div>
              <div class="form-group">
                <label for="cad-email" class="label">Email <span class="text-red-500">*</span></label>
                <input type="email" id="cad-email" name="email" class="input" required autocomplete="email">
              </div>
              <div class="form-group">
                <label for="cad-nome" class="label">Nome completo <span class="text-red-500">*</span></label>
                <input type="text" id="cad-nome" name="nome" class="input" required minlength="2" maxlength="100" autocomplete="name">
              </div>
              <div class="form-group">
                <label for="cad-senha" class="label">Senha <span class="text-red-500">*</span></label>
                <input type="password" id="cad-senha" name="senha" class="input" required minlength="8" autocomplete="new-password">
                <p class="text-xs text-gray-500 mt-1">Mín. 8 chars: 1 maiúscula, 1 minúscula, 1 número, 1 especial</p>
              </div>
              <div class="form-group">
                <label for="cad-confirmar-senha" class="label">Confirmar senha <span class="text-red-500">*</span></label>
                <input type="password" id="cad-confirmar-senha" name="confirmar_senha" class="input" required autocomplete="new-password">
              </div>
              <div class="form-group">
                <label for="cad-pergunta" class="label">Pergunta de segurança <span class="text-red-500">*</span></label>
                <input type="text" id="cad-pergunta" name="pergunta_seguranca" class="input" required minlength="5" placeholder="Ex: Nome do seu primeiro animal de estimação?">
              </div>
              <div class="form-group">
                <label for="cad-resposta" class="label">Resposta <span class="text-red-500">*</span></label>
                <input type="text" id="cad-resposta" name="resposta_seguranca" class="input" required minlength="3">
              </div>
              <button type="submit" class="btn btn-primary w-full">Criar conta</button>
            </form>
            <p class="text-center text-sm text-gray-600 mt-6">
              Já tem conta? <a href="/login" class="text-primary-600 hover:underline" data-link>Entre</a>
            </p>
          </div>
        </div>
      </div>
    `;
  },

  // Criar Lista (em memória)
  criarLista() {
    return `
      <div class="max-w-4xl mx-auto">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold">Nova Lista de Compras</h2>
          <span class="badge badge-info" id="badge-itens">0 itens</span>
        </div>

        <div class="card mb-6">
          <div class="card-body">
            <div class="form-group">
              <label for="lista-nome" class="label">Nome da lista <span class="text-red-500">*</span></label>
              <input type="text" id="lista-nome" class="input" placeholder="Ex: Compras da semana" maxlength="100">
            </div>
          </div>
        </div>

        <div class="card mb-6">
          <div class="card-header flex items-center justify-between">
            <h3 class="font-semibold">Adicionar Itens</h3>
          </div>
          <div class="card-body">
            <div class="form-row mb-4">
              <div class="form-group flex-1">
                <label for="item-produto" class="label">Produto <span class="text-red-500">*</span></label>
                <div class="relative">
                  <input type="text" id="item-produto" class="input" placeholder="Digite para buscar..." autocomplete="off">
                  <div id="autocomplete-results" class="absolute z-10 w-full mt-1 hidden bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto"></div>
                </div>
                <input type="hidden" id="item-produto-id">
              </div>
              <div class="form-group w-32">
                <label for="item-quantidade" class="label">Qtd <span class="text-red-500">*</span></label>
                <input type="number" id="item-quantidade" class="input" value="1" min="1" max="9999">
              </div>
            </div>
            <button type="button" id="btn-add-item" class="btn btn-primary" disabled>Adicionar à Lista</button>
          </div>
        </div>

        <div class="card" id="card-itens-lista" style="display: none;">
          <div class="card-header">
            <h3 class="font-semibold">Itens da Lista (<span id="count-itens">0</span>)</h3>
          </div>
          <div class="card-body">
            <div class="table-container">
              <table class="table">
                <thead>
                  <tr>
                    <th class="w-1/2">Produto</th>
                    <th class="w-1/6">Un.</th>
                    <th class="w-1/6">Qtd</th>
                    <th class="w-1/6"></th>
                  </tr>
                </thead>
                <tbody id="tbody-itens"></tbody>
              </table>
            </div>
          </div>
          <div class="card-footer flex justify-end gap-3">
            <button type="button" id="btn-limpar-lista" class="btn btn-secondary">Limpar</button>
            <button type="button" id="btn-salvar-lista" class="btn btn-primary">Salvar Lista</button>
          </div>
        </div>
      </div>
    `;
  },

  // Minhas Listas
  async minhasListas() {
    if (!State.user) {
      State.navigate('login');
      return '';
    }

    try {
      const data = await ApiClient.listarListas({ pagina: 1, por_pagina: 20 });
      const listas = data.items || [];

      return `
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-2xl font-bold">Minhas Listas</h2>
          <a href="#/criar-lista" class="btn btn-primary" data-link>Nova Lista</a>
        </div>

        <div class="card">
          <div class="card-body p-0">
            ${listas.length === 0 ? `
              <div class="p-12 text-center text-gray-500">
                <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
                <p class="text-lg">Nenhuma lista salva</p>
                <p class="text-sm mt-1">Crie sua primeira lista de compras</p>
                <a href="#/criar-lista" class="btn btn-primary mt-4 inline-block" data-link>Criar Lista</a>
              </div>
            ` : `
              <div class="table-container">
                <table class="table">
                  <thead>
                    <tr>
                      <th>Nome</th>
                      <th>Itens</th>
                      <th>Criada em</th>
                      <th class="w-32"></th>
                    </tr>
                  </thead>
                  <tbody>
                    ${listas.map(l => `
                      <tr>
                        <td class="font-medium">${l.nome}</td>
                        <td>${l.total_itens}</td>
                        <td>${formatDate(l.criado_em)}</td>
                        <td>
                          <div class="flex items-center gap-2">
                            <a href="#/lista/${l.id}" class="btn btn-ghost text-sm p-1.5" data-link title="Ver">👁</a>
                            <button class="btn btn-danger text-sm p-1.5 btn-excluir" data-id="${l.id}" data-nome="${l.nome}" title="Excluir">🗑</button>
                          </div>
                        </td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
              ${data.total_paginas > 1 ? `
                <div class="card-footer flex items-center justify-between">
                  <span class="text-sm text-gray-500">Página ${data.pagina} de ${data.total_paginas} (${data.total} total)</span>
                  <div class="flex gap-2">
                    ${data.pagina > 1 ? `<button class="btn btn-secondary btn-pagina" data-pagina="${data.pagina - 1}">Anterior</button>` : ''}
                    ${data.pagina < data.total_paginas ? `<button class="btn btn-primary btn-pagina" data-pagina="${data.pagina + 1}">Próxima</button>` : ''}
                  </div>
                </div>
              ` : ''}
            }
          </div>
        </div>
      `;
    } catch (e) {
      showToast('Erro ao carregar listas: ' + e.message, 'error');
      return '<div class="card"><div class="card-body text-center text-red-600">Erro ao carregar listas</div></div>';
    }
  },

  // Ver Lista
  async verLista(params) {
    if (!State.user) { State.navigate('login'); return ''; }

    try {
      const lista = await ApiClient.buscarLista(params.id);
      return `
        <div class="flex items-center justify-between mb-6">
          <div>
            <a href="#/minhas-listas" class="text-primary-600 hover:underline text-sm" data-link>← Voltar</a>
            <h2 class="text-2xl font-bold mt-1">${lista.nome}</h2>
          </div>
          <div class="flex gap-2">
            <button id="btn-editar-lista" class="btn btn-secondary" data-id="${lista.id}">Editar</button>
            <button id="btn-excluir-lista" class="btn btn-danger" data-id="${lista.id}" data-nome="${lista.nome}">Excluir</button>
            <button id="btn-exportar-pdf" class="btn btn-primary">Exportar PDF</button>
          </div>
        </div>

        <div class="card">
          <div class="card-body">
            <div class="table-container">
              <table class="table">
                <thead>
                  <tr>
                    <th>Produto</th>
                    <th>Un.</th>
                    <th>Qtd</th>
                  </tr>
                </thead>
                <tbody>
                  ${lista.itens.map(item => `
                    <tr>
                      <td>${item.produto_nome}</td>
                      <td>${item.produto_nome.includes('Desconhecido') ? 'un' : 'un'}</td>
                      <td>${item.quantidade}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      `;
    } catch (e) {
      showToast('Erro ao carregar lista: ' + e.message, 'error');
      State.navigate('minhas-listas');
      return '';
    }
  },

  // Comparar (Pré-filtro + Seleção + Resultado)
  async comparar() {
    try {
      const [categorias, fornecedores] = await Promise.all([
        ApiClient.listarCategorias(),
        ApiClient.listarFornecedores(),
      ]);

      return `
        <div class="max-w-6xl mx-auto">
          <!-- Passo 1: Selecionar Categorias -->
          <section class="card mb-6" id="step-categorias">
            <div class="card-header">
              <h2 class="text-xl font-semibold flex items-center gap-2">
                <span class="badge badge-primary">1</span> Selecionar Categorias
              </h2>
            </div>
            <div class="card-body">
              <p class="text-gray-600 mb-4">Escolha uma ou mais categorias para filtrar os fornecedores disponíveis.</p>
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3" id="categorias-checkboxes">
                ${categorias.map(c => `
                  <label class="flex items-center gap-2 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition">
                    <input type="checkbox" name="categoria" value="${c.id}" class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500">
                    <span class="text-sm">${c.nome}</span>
                  </label>
                `).join('')}
              </div>
              <div class="mt-4 flex justify-end">
                <button id="btn-proximo-fornecedores" class="btn btn-primary" disabled>Próximo: Fornecedores →</button>
              </div>
            </div>
          </section>

          <!-- Passo 2: Selecionar Fornecedores -->
          <section class="card mb-6 hidden" id="step-fornecedores">
            <div class="card-header">
              <h2 class="text-xl font-semibold flex items-center gap-2">
                <span class="badge badge-primary">2</span> Selecionar Fornecedores
              </h2>
            </div>
            <div class="card-body">
              <p class="text-gray-600 mb-4">Selecione pelo menos 2 fornecedores para comparar.</p>
              <div class="mb-4">
                <label class="label">Disponibilidade mínima</label>
                <div class="flex items-center gap-4">
                  <input type="range" id="slider-disponibilidade" min="0" max="100" value="0" class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none accent-primary-600">
                  <span id="valor-disponibilidade" class="text-sm font-mono text-gray-600 w-16">0%</span>
                </div>
              </div>
              <div id="fornecedores-checkboxes" class="space-y-2 max-h-80 overflow-y-auto">
                ${fornecedores.map(f => `
                  <label class="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition">
                    <input type="checkbox" name="fornecedor" value="${f.id}" class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500" data-categorias='${JSON.stringify(f.categorias.map(c => c.id))}'>
                    <div class="flex-1">
                      <div class="font-medium">${f.nome}</div>
                      <div class="text-xs text-gray-500">${f.categorias.map(c => c.nome).join(', ')}</div>
                    </div>
                    <span class="badge badge-info" id="disp-${f.id}">--%</span>
                  </label>
                `).join('')}
              </div>
              <div class="mt-4 flex justify-between">
                <button id="btn-voltar-categorias" class="btn btn-secondary">← Voltar</button>
                <button id="btn-calcular-orcamento" class="btn btn-primary" disabled>Calcular Orçamento →</button>
              </div>
            </div>
          </section>

          <!-- Passo 3: Resultado -->
          <section class="card hidden" id="step-resultado">
            <div class="card-header flex items-center justify-between">
              <h2 class="text-xl font-semibold flex items-center gap-2">
                <span class="badge badge-success">Resultado</span> Comparação de Preços
              </h2>
              <button id="btn-nova-comparacao" class="btn btn-ghost">Nova Comparação</button>
            </div>
            <div class="card-body" id="resultado-comparacao">
              <!-- Preenchido via JS -->
            </div>
          </section>
        </div>
      `;
    } catch (e) {
      showToast('Erro ao carregar comparação: ' + e.message, 'error');
      return '<div class="card"><div class="card-body text-center text-red-600">Erro ao carregar</div></div>';
    }
  },

  // Perfil
  async perfil() {
    if (!State.user) { State.navigate('login'); return ''; }

    return `
      <div class="max-w-2xl mx-auto">
        <h2 class="text-2xl font-bold mb-6">Meu Perfil</h2>

        <div class="card mb-6">
          <div class="card-header">
            <h3 class="font-semibold">Dados Pessoais</h3>
          </div>
          <div class="card-body">
            <dl class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <dt class="text-sm text-gray-500">Nome de usuário</dt>
                <dd class="font-medium">${State.user.nome_usuario}</dd>
              </div>
              <div>
                <dt class="text-sm text-gray-500">Email</dt>
                <dd class="font-medium">${State.user.email}</dd>
              </div>
              <div>
                <dt class="text-sm text-gray-500">Nome</dt>
                <dd class="font-medium">${State.user.nome}</dd>
              </div>
              <div>
                <dt class="text-sm text-gray-500">Cadastrado em</dt>
                <dd class="font-medium">${formatDate(State.user.criado_em)}</dd>
              </div>
            </dl>
          </div>
        </div>

        <div class="card">
          <div class="card-header">
            <h3 class="font-semibold">Editar Perfil</h3>
          </div>
          <div class="card-body">
            <form id="form-perfil" class="space-y-4">
              <div class="form-group">
                <label for="perfil-email" class="label">Email</label>
                <input type="email" id="perfil-email" name="email" class="input" value="${State.user.email}">
              </div>
              <div class="form-group">
                <label for="perfil-nome" class="label">Nome</label>
                <input type="text" id="perfil-nome" name="nome" class="input" value="${State.user.nome}" minlength="2" maxlength="100">
              </div>
              <div class="form-group">
                <label for="perfil-senha-atual" class="label">Senha atual (para alterar)</label>
                <input type="password" id="perfil-senha-atual" name="senha_atual" class="input" autocomplete="current-password">
              </div>
              <div class="form-group">
                <label for="perfil-nova-senha" class="label">Nova senha</label>
                <input type="password" id="perfil-nova-senha" name="nova_senha" class="input" minlength="8" autocomplete="new-password">
              </div>
              <div class="form-group">
                <label for="perfil-confirmar-nova-senha" class="label">Confirmar nova senha</label>
                <input type="password" id="perfil-confirmar-nova-senha" name="confirmar_nova_senha" class="input" autocomplete="new-password">
              </div>
              <button type="submit" class="btn btn-primary">Salvar Alterações</button>
            </form>
          </div>
        </div>
      </div>
    `;
  },
};

// ============================================================
// AUTH VIEWS — Lógica de autenticação
// ============================================================
const AuthViews = {
  async login() {
    const form = $('#form-login');
    if (!form) return;

    form.onsubmit = async (e) => {
      e.preventDefault();
      const data = {
        nome_usuario: form.nome_usuario.value,
        senha: form.senha.value,
      };

      const btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner"></span> Entrando...';

      try {
        const response = await ApiClient.login(data);
        State.setUser({
          id: response.user_id,
          nome_usuario: data.nome_usuario,
          // Outros campos viriam do /auth/perfil
        }, response.access_token);

        // Busca perfil completo
        const perfil = await ApiClient.getPerfil();
        State.setUser(perfil, response.access_token);

        showToast('Login realizado com sucesso!', 'success');

        // Verifica lista efêmera
        if (State.ephemeralList) {
          const modal = showModal(`
            <p>Você tem uma lista em memória. Deseja salvá-la na sua conta?</p>
          `, {
            title: 'Lista Efêmera Encontrada',
            footer: `
              <button class="btn btn-secondary" data-action="manter">Manter Efêmera</button>
              <button class="btn btn-primary" data-action="salvar">Salvar na Conta</button>
            `,
          });

          modal.close = () => {
            const action = document.querySelector('[data-action]')?.dataset.action;
            if (action === 'salvar') {
              ApiClient.promoverEfemera(State.ephemeralList).then(() => {
                showToast('Lista salva com sucesso!', 'success');
                State.clearEphemeralList();
              }).catch(e => showToast('Erro: ' + e.message, 'error'));
            } else {
              State.clearEphemeralList();
            }
            $('#modal-container').classList.add('hidden');
          };
        }

        State.navigate('home');
      } catch (e) {
        showToast(e.message, 'error');
        btn.disabled = false;
        btn.textContent = 'Entrar';
      }
    };
  },

  async cadastrar() {
    const form = $('#form-cadastro');
    if (!form) return;

    form.onsubmit = async (e) => {
      e.preventDefault();

      // Validações
      if (form.senha.value !== form.confirmar_senha.value) {
        showToast('As senhas não coincidem', 'error');
        return;
      }

      const data = {
        nome_usuario: form.nome_usuario.value,
        email: form.email.value,
        nome: form.nome.value,
        senha: form.senha.value,
        pergunta_seguranca: form.pergunta_seguranca.value,
        resposta_seguranca: form.resposta_seguranca.value,
      };

      const btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner"></span> Cadastrando...';

      try {
        await ApiClient.cadastrar(data);
        showToast('Conta criada com sucesso! Redirecionando...', 'success');
        setTimeout(() => State.navigate('login'), 1500);
      } catch (e) {
        showToast(e.message, 'error');
        btn.disabled = false;
        btn.textContent = 'Criar conta';
      }
    };
  },

  async logout() {
    try {
      await ApiClient.logout();
    } catch {}
    State.clearUser();
    showToast('Logout realizado', 'success');
    State.navigate('home');
  },

  async perfil() {
    const form = $('#form-perfil');
    if (!form) return;

    form.onsubmit = async (e) => {
      e.preventDefault();

      if (form.nova_senha.value && form.nova_senha.value !== form.confirmar_nova_senha.value) {
        showToast('As senhas não coincidem', 'error');
        return;
      }

      const data = {};
      if (form.email.value) data.email = form.email.value;
      if (form.nome.value) data.nome = form.nome.value;
      if (form.senha_atual.value) {
        if (!form.nova_senha.value) {
          showToast('Nova senha é obrigatória', 'error');
          return;
        }
        data.senha_atual = form.senha_atual.value;
        data.nova_senha = form.nova_senha.value;
      }

      try {
        await ApiClient.atualizarPerfil(data);
        showToast('Perfil atualizado!', 'success');
        // Recarrega perfil
        const perfil = await ApiClient.getPerfil();
        State.setUser(perfil, ApiClient.getToken());
      } catch (e) {
        showToast(e.message, 'error');
      }
    };
  },
};

// ============================================================
// LISTA VIEWS — Lógica de listas
// ============================================================
const ListaViews = {
  bindCriarLista() {
    const produtoInput = $('#item-produto');
    const produtoIdInput = $('#item-produto-id');
    const autocompleteResults = $('#autocomplete-results');
    const qtdInput = $('#item-quantidade');
    const addBtn = $('#btn-add-item');
    const tbody = $('#tbody-itens');
    const countEl = $('#count-itens');
    const badge = $('#badge-itens');
    const cardItens = $('#card-itens-lista');
    const clearBtn = $('#btn-limpar-lista');
    const saveBtn = $('#btn-salvar-lista');
    const nomeInput = $('#lista-nome');

    let itens = State.ephemeralList?.itens || [];
    let debounceTimer;

    const renderItens = () => {
      tbody.innerHTML = itens.map((item, idx) => `
        <tr>
          <td>${item.produto_nome}</td>
          <td>${item.unidade}</td>
          <td>${item.quantidade}</td>
          <td><button class="text-red-600 hover:text-red-800" data-remove="${idx}">✕</button></td>
        </tr>
      `).join('');

      countEl.textContent = itens.length;
      badge.textContent = `${itens.length} itens`;
      cardItens.style.display = itens.length ? 'block' : 'none';
      addBtn.disabled = !produtoIdInput.value || !qtdInput.value;
      saveBtn.disabled = itens.length === 0 || !nomeInput.value.trim();

      // Bind remove
      tbody.querySelectorAll('[data-remove]').forEach(btn => {
        btn.onclick = () => {
          itens.splice(parseInt(btn.dataset.remove), 1);
          renderItens();
        };
      });
    };

    // Autocomplete
    produtoInput.addEventListener('input', () => {
      clearTimeout(debounceTimer);
      const q = produtoInput.value.trim();
      if (q.length < 2) {
        autocompleteResults.classList.add('hidden');
        return;
      }
      debounceTimer = setTimeout(async () => {
        try {
          const produtos = await ApiClient.autocompleteProdutos(q, 10);
          if (produtos.length === 0) {
            autocompleteResults.classList.add('hidden');
            return;
          }
          autocompleteResults.innerHTML = produtos.map(p => `
            <button type="button" class="w-full px-3 py-2 text-left hover:bg-gray-100" data-id="${p.id}" data-nome="${p.nome}" data-unidade="${p.unidade}">
              ${p.nome} <span class="text-gray-500">(${p.unidade})</span>
            </button>
          `).join('');
          autocompleteResults.classList.remove('hidden');

          autocompleteResults.querySelectorAll('button').forEach(btn => {
            btn.onclick = () => {
              produtoInput.value = btn.dataset.nome;
              produtoIdInput.value = btn.dataset.id;
              qtdInput.focus();
              autocompleteResults.classList.add('hidden');
              addBtn.disabled = !qtdInput.value;
            };
          });
        } catch (e) {
          console.error(e);
        }
      }, 300);
    });

    // Fecha autocomplete ao clicar fora
    document.addEventListener('click', (e) => {
      if (!autocompleteResults.contains(e.target) && e.target !== produtoInput) {
        autocompleteResults.classList.add('hidden');
      }
    });

    // Add item
    addBtn.onclick = () => {
      const produtoId = parseInt(produtoIdInput.value);
      const produtoNome = produtoInput.value;
      const unidade = 'un'; // TODO: buscar do produto
      const quantidade = parseInt(qtdInput.value);

      if (!produtoId || !quantidade) return;

      // Verifica duplicata
      const existing = itens.findIndex(i => i.produto_id === produtoId);
      if (existing >= 0) {
        itens[existing].quantidade += quantidade;
      } else {
        itens.push({ produto_id: produtoId, produto_nome: produtoNome, unidade, quantidade });
      }

      produtoInput.value = '';
      produtoIdInput.value = '';
      qtdInput.value = 1;
      autocompleteResults.classList.add('hidden');
      renderItens();
    };

    // Clear
    clearBtn.onclick = () => {
      if (confirm('Limpar toda a lista?')) {
        itens = [];
        nomeInput.value = '';
        renderItens();
      }
    };

    // Save
    saveBtn.onclick = async () => {
      const nome = nomeInput.value.trim();
      if (!nome || itens.length === 0) return;

      saveBtn.disabled = true;
      saveBtn.innerHTML = '<span class="spinner"></span> Salvando...';

      try {
        if (State.user) {
          await ApiClient.salvarLista({ nome, itens });
        } else {
          await ApiClient.promoverEfemera({ nome, itens });
        }
        showToast('Lista salva com sucesso!', 'success');
        State.clearEphemeralList();
        itens = [];
        nomeInput.value = '';
        renderItens();
        State.navigate('minhas-listas');
      } catch (e) {
        showToast('Erro ao salvar: ' + e.message, 'error');
      } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = 'Salvar Lista';
      }
    };

    // Initial render
    renderItens();
  },

  bindMinhasListas() {
    // Pagination
    document.querySelectorAll('.btn-pagina').forEach(btn => {
      btn.onclick = () => Views.minhasListas().then(html => {
        $('#main-content').innerHTML = html;
        ListaViews.bindMinhasListas();
      });
    });

    // Delete
    document.querySelectorAll('.btn-excluir').forEach(btn => {
      btn.onclick = async () => {
        const id = parseInt(btn.dataset.id);
        const nome = btn.dataset.nome;
        const confirmacao = prompt(`Digite o nome da lista para confirmar exclusão:\n"${nome}"`);
        if (confirmacao !== nome) {
          showToast('Nome de confirmação incorreto', 'error');
          return;
        }
        try {
          await ApiClient.excluirLista(id, nome);
          showToast('Lista excluída', 'success');
          State.navigate('minhas-listas');
        } catch (e) {
          showToast('Erro: ' + e.message, 'error');
        }
      };
    });
  },

  bindVerLista(params) {
    $('#btn-editar-lista')?.addEventListener('click', () => {
      State.navigate('editar-lista', { id: params.id });
    });

    $('#btn-excluir-lista')?.addEventListener('click', async () => {
      const id = parseInt(document.querySelector('#btn-excluir-lista').dataset.id);
      const nome = document.querySelector('#btn-excluir-lista').dataset.nome;
      const confirmacao = prompt(`Digite o nome da lista para confirmar exclusão:\n"${nome}"`);
      if (confirmacao !== nome) return;
      try {
        await ApiClient.excluirLista(id, nome);
        showToast('Lista excluída', 'success');
        State.navigate('minhas-listas');
      } catch (e) {
        showToast('Erro: ' + e.message, 'error');
      }
    });

    $('#btn-exportar-pdf')?.addEventListener('click', async () => {
      const btn = document.querySelector('#btn-exportar-pdf');
      btn.disabled = true;
      btn.innerHTML = '<span class="spinner"></span> Gerando...';
      try {
        const blob = await ApiClient.exportarPDF(params.id);
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `lista_${new Date().toISOString().split('T')[0].replace(/-/g, '')}.pdf`;
        a.click();
        URL.revokeObjectURL(url);
        showToast('PDF baixado!', 'success');
      } catch (e) {
        showToast('Erro ao gerar PDF: ' + e.message, 'error');
      } finally {
        btn.disabled = false;
        btn.textContent = 'Exportar PDF';
      }
    });
  },
};

// ============================================================
// COMPARAÇÃO VIEWS — Lógica de comparação
// ============================================================
const ComparacaoViews = {
  bindComparar() {
    const catCheckboxes = $$('input[name="categoria"]');
    const fornCheckboxes = $$('input[name="fornecedor"]');
    const slider = $('#slider-disponibilidade');
    const valorDisp = $('#valor-disponibilidade');
    const btnProxForn = $('#btn-proximo-fornecedores');
    const btnVoltarCat = $('#btn-voltar-categorias');
    const btnCalc = $('#btn-calcular-orcamento');
    const btnNova = $('#btn-nova-comparacao');
    const stepCat = $('#step-categorias');
    const stepForn = $('#step-fornecedores');
    const stepRes = $('#step-resultado');

    let categoriasSelecionadas = [];
    let fornecedoresSelecionados = [];

    // Step 1: Categorias
    catCheckboxes.forEach(cb => {
      cb.onchange = () => {
        categoriasSelecionadas = catCheckboxes.filter(c => c.checked).map(c => parseInt(c.value));
        btnProxForn.disabled = categoriasSelecionadas.length === 0;
      };
    });

    btnProxForn.onclick = () => {
      // Filtra fornecedores por categorias
      fornCheckboxes.forEach(cb => {
        const cats = JSON.parse(cb.dataset.categorias || '[]');
        const match = categoriasSelecionadas.some(c => cats.includes(c));
        cb.closest('label').style.display = match ? 'flex' : 'none';
        if (!match) cb.checked = false;
      });
      stepCat.classList.add('hidden');
      stepForn.classList.remove('hidden');
      updateDisponibilidade();
    };

    btnVoltarCat.onclick = () => {
      stepForn.classList.add('hidden');
      stepCat.classList.remove('hidden');
    };

    // Slider disponibilidade
    slider.oninput = () => {
      valorDisp.textContent = slider.value + '%';
      updateDisponibilidade();
    };

    function updateDisponibilidade() {
      const minDisp = parseFloat(slider.value);
      let count = 0;
      fornCheckboxes.forEach(cb => {
        if (cb.closest('label').style.display !== 'none') {
          const badge = document.getElementById(`disp-${cb.value}`);
          // TODO: buscar disponibilidade real via API
          // Por enquanto, simula
          const simulated = Math.random() * 100;
          badge.textContent = simulated.toFixed(1) + '%';
          badge.className = 'badge ' + (simulated >= minDisp ? 'badge-success' : 'badge-warning');
          if (simulated < minDisp) {
            cb.checked = false;
            cb.disabled = true;
            cb.closest('label').classList.add('opacity-50');
          } else {
            cb.disabled = false;
            cb.closest('label').classList.remove('opacity-50');
          }
        }
      });
      updateCalcButton();
    }

    // Fornecedores checkboxes
    fornCheckboxes.forEach(cb => {
      cb.onchange = updateCalcButton;
    });

    function updateCalcButton() {
      fornecedoresSelecionados = fornCheckboxes.filter(c => c.checked).map(c => parseInt(c.value));
      btnCalc.disabled = fornecedoresSelecionados.length < 2;
    }

    // Calcular orçamento
    btnCalc.onclick = async () => {
      btnCalc.disabled = true;
      btnCalc.innerHTML = '<span class="spinner"></span> Calculando...';

      // Pega IDs dos produtos da lista efêmera ou salva
      // Por simplicidade, usa uma lista mockada
      // TODO: integrar com lista real do usuário
      const produtoIds = [1, 2, 3, 11, 21]; // Mock

      try {
        const result = await ApiClient.calcularOrcamento({
          lista_id: 0, // TODO: lista real
          fornecedor_ids: fornecedoresSelecionados,
          disponibilidade_minima: parseFloat(slider.value),
        });
        renderResultado(result);
        stepForn.classList.add('hidden');
        stepRes.classList.remove('hidden');
      } catch (e) {
        showToast('Erro: ' + e.message, 'error');
      } finally {
        btnCalc.disabled = false;
        btnCalc.textContent = 'Calcular Orçamento →';
      }
    };

    // Nova comparação
    btnNova.onclick = () => {
      stepRes.classList.add('hidden');
      stepCat.classList.remove('hidden');
      catCheckboxes.forEach(cb => cb.checked = false);
      fornCheckboxes.forEach(cb => { cb.checked = false; cb.disabled = false; cb.closest('label').style.display = 'flex'; cb.closest('label').classList.remove('opacity-50'); });
      slider.value = 0;
      valorDisp.textContent = '0%';
      categoriasSelecionadas = [];
      fornecedoresSelecionados = [];
      btnProxForn.disabled = true;
      btnCalc.disabled = true;
    };
  },
};

function renderResultado(data) {
  const container = $('#resultado-comparacao');
  if (!container) return;

  if (!data.fornecedores || data.fornecedores.length === 0) {
    container.innerHTML = `
      <div class="text-center py-12 text-gray-500">
        <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
        <p class="text-lg">Nenhum fornecedor atende aos critérios</p>
        <p class="text-sm mt-1">Tente reduzir a disponibilidade mínima ou selecionar mais fornecedores</p>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="mb-6">
      <div class="flex items-center gap-2 mb-2">
        <span class="badge badge-success">Lista: ${data.lista_nome}</span>
        ${data.melhor_fornecedor_id ? `
          <span class="badge badge-success">🏆 Melhor: Fornecedor #${data.melhor_fornecedor_id}</span>
        ` : ''}
      </div>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>Fornecedor</th>
            <th class="text-center">Disponíveis</th>
            <th class="text-center">Ausentes</th>
            <th class="text-center">% Disp.</th>
            <th class="text-right">Total</th>
          </tr>
        </thead>
        <tbody>
          ${data.fornecedores.map(f => `
            <tr class="${f.eh_melhor ? 'bg-green-50' : ''}">
              <td class="font-medium">${f.fornecedor_nome} ${f.eh_melhor ? '<span class="badge badge-success ml-2">MELHOR</span>' : ''}</td>
              <td class="text-center">${f.itens_disponiveis}</td>
              <td class="text-center text-red-600">${f.itens_ausentes}</td>
              <td class="text-center">${f.percentual_disponibilidade.toFixed(1)}%</td>
              <td class="text-right font-semibold ${f.eh_melhor ? 'text-green-700' : ''}">${formatCurrency(f.preco_total)}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>

    <details class="mt-6">
      <summary class="cursor-pointer font-medium text-gray-700">Ver detalhes por item</summary>
      <div class="mt-4 space-y-4">
        ${data.fornecedores.map(f => `
          <div class="card ${f.eh_melhor ? 'ring-2 ring-green-500' : ''}">
            <div class="card-header flex items-center justify-between">
              <h4 class="font-semibold">${f.fornecedor_nome} ${f.eh_melhor ? '<span class="badge badge-success">MELHOR OFERTA</span>' : ''}</h4>
              <span class="text-right">Total: <strong>${formatCurrency(f.preco_total)}</strong></span>
            </div>
            <div class="card-body p-0">
              <div class="table-container">
                <table class="table">
                  <thead>
                    <tr>
                      <th>Produto</th>
                      <th class="text-center">Un.</th>
                      <th class="text-center">Qtd</th>
                      <th class="text-right">Preço Unit.</th>
                      <th class="text-right">Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${f.itens.map(i => `
                      <tr class="${!i.disponivel ? 'bg-red-50 text-red-600' : ''}">
                        <td>${i.produto_nome}</td>
                        <td class="text-center">${i.unidade}</td>
                        <td class="text-center">${i.quantidade}</td>
                        <td class="text-right">${i.preco_unitario !== null ? formatCurrency(i.preco_unitario) : '<span class="text-red-600">N/D</span>'}</td>
                        <td class="text-right">${i.preco_total !== null ? formatCurrency(i.preco_total) : '<span class="text-red-600">N/D</span>'}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        `).join('')}
      </div>
    </details>

    <div class="mt-6 flex gap-3 justify-end">
      <button id="btn-exportar-pdf-resultado" class="btn btn-primary">Exportar PDF</button>
      <button id="btn-imprimir" class="btn btn-secondary no-print">Imprimir</button>
    </div>
  `;

  $('#btn-imprimir')?.addEventListener('click', () => window.print());
  $('#btn-exportar-pdf-resultado')?.addEventListener('click', async () => {
    // TODO: implementar exportação do resultado da comparação
    showToast('Exportação de comparação em desenvolvimento', 'info');
  });
}

// ============================================================
// ROUTER — Navegação SPA
// ============================================================
const routes = {
  '/': Views.home,
  '/login': Views.login,
  '/cadastrar': Views.cadastrar,
  '/criar-lista': Views.criarLista,
  '/minhas-listas': Views.minhasListas,
  '/lista/:id': Views.verLista,
  '/comparar': Views.comparar,
  '/perfil': Views.perfil,
};

const router = {
  async navigate(path, params = {}) {
    // Match route
    let matchedRoute = null;
    let matchedParams = {};

    for (const [routePath, viewFn] of Object.entries(routes)) {
      const regex = new RegExp('^' + routePath.replace(/:(\w+)/g, '([^/]+)') + '$');
      const match = path.match(regex);
      if (match) {
        matchedRoute = viewFn;
        const paramNames = routePath.match(/:(\w+)/g) || [];
        paramNames.forEach((name, i) => {
          matchedParams[name.slice(1)] = match[i + 1];
        });
        break;
      }
    }

    if (!matchedRoute) {
      // 404 -> home
      window.location.hash = '#/';
      return;
    }

    // Render
    const main = $('#main-content');
    main.innerHTML = '<div class="flex items-center justify-center h-64"><span class="spinner text-2xl"></span></div>';

    try {
      const html = await matchedRoute(matchedParams);
      main.innerHTML = html;

      // Bind events based on route
      this.bindEvents(path, matchedParams);
    } catch (e) {
      console.error(e);
      main.innerHTML = '<div class="card"><div class="card-body text-center text-red-600">Erro ao carregar página</div></div>';
    }

    // Scroll to top
    window.scrollTo(0, 0);
  },

  bindEvents(path, params) {
    // Delegated event binding for links
    document.querySelectorAll('[data-link]').forEach(link => {
      link.onclick = (e) => {
        e.preventDefault();
        const href = link.getAttribute('href');
        if (href.startsWith('#')) {
          this.navigate(href.slice(1));
        }
      };
    });

    // Route-specific bindings
    if (path === '/login') AuthViews.login();
    else if (path === '/cadastrar') AuthViews.cadastrar();
    else if (path === '/criar-lista') ListaViews.bindCriarLista();
    else if (path === '/minhas-listas') ListaViews.bindMinhasListas();
    else if (path.startsWith('/lista/')) ListaViews.bindVerLista(params);
    else if (path === '/comparar') ComparacaoViews.bindComparar();
    else if (path === '/perfil') AuthViews.perfil();

    // Header navigation
    $('#nav-auth')?.addEventListener('click', (e) => {
      const link = e.target.closest('[data-link]');
      if (link) {
        e.preventDefault();
        this.navigate(link.getAttribute('href').slice(1));
      }
    });
  },

  init() {
    // Handle hash changes
    window.addEventListener('hashchange', () => {
      this.navigate(window.location.hash.slice(1) || '/');
    });

    // Initial load
    this.navigate(window.location.hash.slice(1) || '/');
  },
};

// ============================================================
// INIT
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  State.init();
  router.init();
});

// Expose for debugging
window.COBECO = { State, ApiClient, Views, router };