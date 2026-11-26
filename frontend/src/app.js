// COBECO Frontend — Wireframe v3.3 (sem dados mockados)
// Estrutura alinhada ao protótipo canônico doc-prototype-0003.
// Consome API real: /catalogo/categorias, /catalogo/fornecedores, /catalogo/produtos,
// /comparacao/calcular-efemera, /export/pdf/vencedora.

const API_BASE = '/v1';

const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
}[c] || c));

const norm = (s) => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

const BRL = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

const hoje = () => new Date().toLocaleDateString('pt-BR');

const stamp = () => {
  const d = new Date();
  return `${d.getFullYear()}${String(d.getMonth()+1).padStart(2,'0')}${String(d.getDate()).padStart(2,'0')}`;
};

// ============================================================
// TOAST — success/error/warning/info, auto-dismiss 3-4s, stack top-right
// ============================================================
const showToast = (msg, type = 'info') => {
  const container = document.getElementById('toasts');
  const box = document.createElement('div');
  const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
  const classes = { success: 'toast-success', error: 'toast-error', warning: 'toast-warning', info: 'toast-info' };
  box.className = `toast ${classes[type] || classes.info}`;
  box.setAttribute('role', 'alert');
  box.setAttribute('aria-live', 'polite');
  box.innerHTML = `<span class="toast-icon" aria-hidden="true">${icons[type] || icons.info}</span><span>${esc(msg)}</span><button class="toast-close" aria-label="Fechar">✕</button>`;
  container.appendChild(box);
  box.querySelector('.toast-close').addEventListener('click', () => dismissToast(box));
  const duration = type === 'error' ? 5000 : 3500;
  const timer = setTimeout(() => dismissToast(box), duration);
  box.dataset.timer = timer;
};

const dismissToast = (box) => {
  const timer = box.dataset.timer;
  if (timer) clearTimeout(timer);
  box.style.opacity = '0';
  box.style.transform = 'translateX(100%)';
  box.style.transition = 'opacity .3s, transform .3s';
  setTimeout(() => box.remove(), 300);
};

// ============================================================
// LOADING — skeleton loaders for lists/tables, spinner overlay for actions
// ============================================================
const Loading = {
  // Skeleton para lista de itens
  skeletonItens: (count = 3) => `<div id="itens-box">${Array.from({ length: count }, () => `
    <div class="skeleton skeleton-table-row" style="margin-bottom: 8px;"></div>
  `).join('')}</div>`,

  // Skeleton para grid de fornecedores
  skeletonFornecedores: (count = 4) => `<div id="forn-grid" class="forn-grid">${Array.from({ length: count }, () => `
    <div class="skeleton skeleton-card" style="margin-bottom: 12px;"></div>
  `).join('')}</div>`,

  // Skeleton para tabela de resultados
  skeletonResultados: (rows = 3) => `<table class="tbl"><thead><tr><th>#</th><th>Fornecedor</th><th>Cobertura</th><th>Itens</th><th>Ausentes</th><th style="text-align:right">Total</th></tr></thead><tbody>
    ${Array.from({ length: rows }, () => `
      <tr><td class="skeleton skeleton-text" style="width:30px;height:16px"></td>
      <td class="skeleton skeleton-text" style="width:180px;height:16px"></td>
      <td class="skeleton skeleton-text" style="width:80px;height:16px"></td>
      <td class="skeleton skeleton-text" style="width:50px;height:16px"></td>
      <td class="skeleton skeleton-text" style="width:50px;height:16px"></td>
      <td class="skeleton skeleton-text" style="width:100px;height:16px"></td></tr>
    `).join('')}
  </tbody></table>`,

  // Skeleton para lista de categorias
  skeletonCategorias: (count = 6) => `<div class="cat-grid">${Array.from({ length: count }, () => `
    <div class="skeleton skeleton-card" style="height:80px;margin-bottom:8px;"></div>
  `).join('')}</div>`,

  // Overlay spinner para ações (calcular, exportar, etc.)
  showOverlay: (msg = 'Carregando…') => {
    const existing = document.getElementById('loading-overlay');
    if (existing) existing.remove();
    const overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'loading-overlay';
    overlay.setAttribute('role', 'status');
    overlay.setAttribute('aria-live', 'polite');
    overlay.innerHTML = `<div class="loading-content"><div class="loading-spinner" aria-hidden="true"></div><span class="loading-text">${esc(msg)}</span></div>`;
    document.body.appendChild(overlay);
    return overlay;
  },

  hideOverlay: () => {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) overlay.remove();
  },

  // Spinner inline para botões
  setButtonLoading: (btn, loading = true, originalText = '') => {
    if (loading) {
      btn.dataset.originalText = btn.textContent;
      btn.disabled = true;
      btn.innerHTML = `<span class="spinner" aria-hidden="true"></span><span>Carregando…</span>`;
    } else {
      btn.disabled = false;
      btn.textContent = btn.dataset.originalText || originalText;
      delete btn.dataset.originalText;
    }
  }
};

// ============================================================
// MODAL — confirmation dialogs (delete, logout), accessible (focus trap, ESC close)
// ============================================================
let lastFocusedElement = null;
let focusTrapCleanup = null;

const openModal = (html, options = {}) => {
  const container = document.getElementById('modal-root');
  lastFocusedElement = document.activeElement;
  const modalId = `modal-${Date.now()}`;
  const { title = '', size = 'md', closable = true, onClose } = options;
  container.innerHTML = `
    <div class="modal-overlay" id="${modalId}" role="dialog" aria-modal="true" ${title ? `aria-labelledby="${modalId}-title"` : ''}>
      <div class="modal modal-${size}">
        ${title ? `<header class="modal-header"><h2 id="${modalId}-title" class="modal-title">${esc(title)}</h2>${closable ? `<button class="modal-close" aria-label="Fechar">✕</button>` : ''}</header>` : ''}
        <div class="modal-body">${html}</div>
      </div>
    </div>
  `;
  container.classList.remove('hidden');
  container.setAttribute('aria-hidden', 'false');

  const overlay = container.querySelector('.modal-overlay');
  const modal = container.querySelector('.modal');
  const closeBtn = container.querySelector('.modal-close');

  // Focus trap
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  const trapFocus = (e) => {
    if (e.key !== 'Tab') return;
    if (e.shiftKey) {
      if (document.activeElement === firstFocusable) {
        e.preventDefault();
        lastFocusable.focus();
      }
    } else {
      if (document.activeElement === lastFocusable) {
        e.preventDefault();
        firstFocusable.focus();
      }
    }
  };

  const handleKeydown = (e) => {
    if (e.key === 'Escape' && closable) {
      closeModal();
    } else {
      trapFocus(e);
    }
  };

  const handleOverlayClick = (e) => {
    if (e.target === overlay && closable) closeModal();
  };

  const handleCloseClick = () => closeModal();

  overlay.addEventListener('keydown', handleKeydown);
  overlay.addEventListener('click', handleOverlayClick);
  if (closeBtn) closeBtn.addEventListener('click', handleCloseClick);

  focusTrapCleanup = () => {
    overlay.removeEventListener('keydown', handleKeydown);
    overlay.removeEventListener('click', handleOverlayClick);
    if (closeBtn) closeBtn.removeEventListener('click', handleCloseClick);
  };

  // Focus first element
  setTimeout(() => firstFocusable?.focus(), 0);

  return {
    close: closeModal,
    element: overlay
  };
};

const closeModal = () => {
  const container = document.getElementById('modal-root');
  if (focusTrapCleanup) {
    focusTrapCleanup();
    focusTrapCleanup = null;
  }
  container.innerHTML = '';
  container.classList.add('hidden');
  container.setAttribute('aria-hidden', 'true');
  if (lastFocusedElement) {
    lastFocusedElement.focus();
    lastFocusedElement = null;
  }
};

// Confirmation dialog helpers
const Modal = {
  confirm: (message, options = {}) => {
    const { title = 'Confirmar', confirmText = 'Confirmar', cancelText = 'Cancelar', variant = 'danger', onConfirm } = options;
    return new Promise((resolve) => {
      openModal(`
        <p class="modal-message">${esc(message)}</p>
        <footer class="modal-footer">
          <button class="btn btn-ghost" data-action="modal-cancel">${esc(cancelText)}</button>
          <button class="btn btn-${variant}" data-action="modal-confirm">${esc(confirmText)}</button>
        </footer>
      `, { title });

      const handleClick = (e) => {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        const action = btn.dataset.action;
        if (action === 'modal-confirm') {
          closeModal();
          resolve(true);
          onConfirm?.();
        } else if (action === 'modal-cancel') {
          closeModal();
          resolve(false);
        }
      };
      document.getElementById('modal-root').addEventListener('click', handleClick);
    });
  },

  alert: (message, options = {}) => {
    const { title = 'Atenção', confirmText = 'OK', onConfirm } = options;
    return new Promise((resolve) => {
      openModal(`
        <p class="modal-message">${esc(message)}</p>
        <footer class="modal-footer">
          <button class="btn btn-pri" data-action="modal-ok">${esc(confirmText)}</button>
        </footer>
      `, { title });

      const handleClick = (e) => {
        if (e.target.closest('[data-action="modal-ok"]')) {
          closeModal();
          resolve(true);
          onConfirm?.();
        }
      };
      document.getElementById('modal-root').addEventListener('click', handleClick);
    });
  },

  // Delete confirmation with item name
  confirmDelete: (itemName, options = {}) => {
    return Modal.confirm(
      `Tem certeza que deseja excluir <strong>${esc(itemName)}</strong>? Esta ação não pode ser desfeita.`,
      { title: 'Excluir item', confirmText: 'Excluir', variant: 'danger', ...options }
    );
  },

  // Logout confirmation
  confirmLogout: () => {
    return Modal.confirm(
      'Deseja realmente sair da sua conta?',
      { title: 'Sair', confirmText: 'Sair', variant: 'secondary' }
    );
  }
};

const state = {
  view: 'home',
  user: null,
  categorias: [],
  categoriasDisponiveis: [],
  categoriasVisiveis: [],
  categoriaBusca: '',
  areasSelecionadas: [], // pré-filtro de grandes áreas (multi-seleção)
  areasGrandes: [],      // grandes áreas carregadas do backend
  fornecedoresDisponiveis: [],
  produtos: [],
  lista: { nome: '', itens: [] },
  listaGerada: null,     // última lista concluída (espaço próprio da sessão)
  historicoSessao: [],   // listas concluídas da sessão (até fechar browser)
  fornecedores: [],
  filtroDisp: 0,
  resultado: null,
  busca: '',
  coberturaPorFornecedor: {}, // mapa fid -> percentual (calculado antes de clicar em Calcular)
};

class ApiClient {
  static async request(endpoint, options = {}) {
    const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
    const response = await fetch(API_BASE + endpoint, { ...options, headers, credentials: 'include' });
    if (response.status === 401) { showToast('Sessão expirada.', 'warning'); return null; }
    const data = await response.json().catch(() => ({}));
    if (!response.ok) { throw new Error(data.detail || 'Erro ' + response.status); }
    return data;
  }
  static listarCategorias() { return this.request('/catalogo/categorias'); }
  static listarAreasGrandes() { return this.request('/catalogo/areas-grandes'); }
  static buscarCategorias(q) { return this.request('/catalogo/categorias/busca?q=' + encodeURIComponent(q)); }
  static listarProdutos(categorias = []) {
    const q = categorias.length ? '?categorias=' + categorias.join(',') : '';
    return this.request('/catalogo/produtos' + q);
  }
  static listarFornecedores(categorias = []) {
    const q = categorias.length ? '?categorias=' + categorias.join(',') : '';
    return this.request('/catalogo/fornecedores' + q);
  }
  static listarDisponibilidadeLote(produtoIds, fornecedorIds = null) {
    const q = '?produtos=' + produtoIds.join(',') + (fornecedorIds ? '&fornecedores=' + fornecedorIds.join(',') : '');
    return this.request('/catalogo/fornecedores/disponibilidade-lote' + q);
  }
  static buscarProdutos(q, limit = 10) {
    return this.request('/catalogo/produtos/autocomplete?q=' + encodeURIComponent(q) + '&limit=' + limit);
  }
  static calcularOrcamentoEfemera(data) {
    return this.request('/comparacao/calcular-efemera', {
      method: 'POST', body: JSON.stringify(data),
    });
  }
  static exportarPDFVencedora(data) {
    return fetch(API_BASE + '/export/pdf/vencedora', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      credentials: 'include', body: JSON.stringify(data),
    }).then((r) => { if (!r.ok) throw new Error('Erro ao gerar PDF'); return r.blob(); });
  }
}

async function carregarCategorias() {
  try {
    const cats = await ApiClient.listarCategorias();
    if (cats && cats.length) {
      state.categoriasDisponiveis = cats.map(c => ({ id: c.id, nome: c.nome, ic: '📂' }));
      state.categoriasVisiveis = state.categoriasDisponiveis.slice();
    }
  } catch (e) { }
}

async function carregarAreasGrandes() {
  try {
    const areas = await ApiClient.listarAreasGrandes();
    if (areas && areas.length) {
      state.areasGrandes = areas.map(a => ({ id: a.id, nome: a.nome, categorias: (a.categorias || []).map(c => c.id) }));
    } else {
      state.areasGrandes = [];
    }
  } catch (e) { state.areasGrandes = []; }
}

async function carregarProdutos(categoriaIds = []) {
  try {
    const prods = await ApiClient.listarProdutos(categoriaIds);
    if (prods && prods.length) state.produtos = prods.map(p => ({ id: p.id, nome: p.nome, un: p.unidade || 'un' }));
    else state.produtos = [];
  } catch (e) { state.produtos = []; }
}

async function carregarFornecedores(categoriaIds = []) {
  try {
    const frns = await ApiClient.listarFornecedores(categoriaIds);
    if (frns && frns.length) {
      state.fornecedoresDisponiveis = frns.map(f => ({ id: f.id, nome: f.nome, cnpj: f.cnpj, cats: (f.categorias || []).map(c => c.id) }));
    }
  } catch (e) { }
}

// Busca a cobertura de cada fornecedor para os produtos da lista (ANTES de calcular orçamento)
async function carregarCoberturaFornecedores() {
  const produtoIds = state.lista.itens.map(i => i.pid);
  if (!produtoIds.length) { state.coberturaPorFornecedor = {}; return; }
  const fornecedorIds = state.fornecedoresDisponiveis.map(f => f.id);
  try {
    const dados = await ApiClient.listarDisponibilidadeLote(produtoIds, fornecedorIds);
    const mapa = {};
    for (const d of dados || []) mapa[d.fornecedor_id] = d.percentual_disponibilidade / 100;
    state.coberturaPorFornecedor = mapa;
  } catch (e) { state.coberturaPorFornecedor = {}; }
}

function nomeCategoria(id) {
  const cat = state.categoriasDisponiveis.find(c => c.id === id);
  return cat ? cat.nome : '';
}

function nomeProduto(id) {
  const p = state.produtos.find(x => x.id === id);
  return p ? p.nome : 'Desconhecido';
}

function unidadeProduto(id) {
  const p = state.produtos.find(x => x.id === id);
  return p ? p.un : 'un';
}

// ============================================================
// CÁLCULO DE ORÇAMENTO VIA API (RF15/RF16)
// Porcentagem de cobertura = itens disponíveis / total de itens da lista
// Melhor oferta = maior cobertura; empate → menor custo total
// ============================================================
async function calcularResultado() {
  const itens = state.lista.itens;
  if (!itens.length) { state.resultado = null; return; }
  const fornecedorIds = state.fornecedores;
  if (fornecedorIds.length < 2) { state.resultado = null; return; }
  try {
    const data = await ApiClient.calcularOrcamentoEfemera({
      itens: itens.map(i => ({ produto_id: i.pid, quantidade: i.qtd })),
      fornecedor_ids: fornecedorIds,
      disponibilidade_minima: state.filtroDisp,
      lista_nome: state.lista.nome || 'Lista',
    });
    const fornecedores = (data.fornecedores || []).map(f => ({
      fid: f.fornecedor_id,
      nome: f.fornecedor_nome,
      cnpj: '',
      cobertura: f.percentual_disponibilidade / 100,
      nDisp: f.itens_disponiveis,
      nAus: f.itens_ausentes,
      total: f.preco_total,
      parcial: f.itens_ausentes > 0,
      itens: f.itens.map(i => ({ pid: i.produto_id, preco: i.preco_unitario || 0, disponivel: i.disponivel })),
    }));
    // Melhor oferta: maior cobertura; empate → menor total
    const winner = fornecedores.slice().sort((a, b) => b.cobertura - a.cobertura || a.total - b.total)[0];
    const display = fornecedores.slice().sort((a, b) => a.total - b.total);
    state.resultado = { rows: display, winner, minTotal: Math.min(...fornecedores.map(r => r.total)), maxTotal: Math.max(...fornecedores.map(r => r.total)) };
  } catch (e) {
    showToast('Erro ao calcular orçamento.', 'error');
    state.resultado = null;
  }
}

function fornecedoresElegiveis() {
  const base = state.fornecedoresDisponiveis.length ? state.fornecedoresDisponiveis : [];
  return base.filter(f => {
    if (!f.cats.some(c => state.categorias.includes(c))) return false;
    const cov = (state.coberturaPorFornecedor[f.id] ?? coberturaDe(f.id)) * 100;
    // RF14/RF22: omite fornecedores com 0% de cobertura e abaixo do filtro de disponibilidade
    return cov > 0 && cov >= state.filtroDisp;
  });
}

function coberturaDe(fid) {
  if (state.resultado) {
    const row = state.resultado.rows.find(r => r.fid === fid);
    return row ? row.cobertura : 0;
  }
  return 0;
}

function totalCategorias() {
  return state.categoriasDisponiveis.length;
}

function go(view) {
  state.view = view;
  render();
  window.scrollTo({ top: 0 });
}

// ============================================================
// RENDER
// ============================================================
function render() {
  const M = { home: vHome, categorias: vCategorias, lista: vLista, fornecedores: vFornecedores,
    resultados: vResultados, vencedora: vVencedora, login: vLogin, cadastro: vCadastro };
  const viewFn = M[state.view] || vHome;
  // Navbar fixa (RF24): sempre visível no topo, atualizada a cada navegação
  try { document.getElementById('topbar').innerHTML = navHTML(); } catch (e) { }
  try { document.getElementById('main').innerHTML = viewFn(); }
  catch(e) { document.getElementById('main').innerHTML = '<div style="color:red">Erro: ' + e.message + '</div>'; }
}

function navHTML() {
  const logged = !!state.user;
  return `
    <div class="logo"><div class="mark">🛒</div><div><b>COBECO</b><small>Cotação de Bens de Consumo · Wireframe v3.3</small></div></div>
    <nav class="main">
      <a href="#" class="${state.view === 'home' ? 'on' : ''}" data-action="nav-home">Início</a>
      <a href="#" class="${['categorias','lista','fornecedores','resultados','vencedora'].includes(state.view) ? 'on' : ''}" data-action="nav-nova">Nova lista</a>
      ${logged ? `<a href="#" class="${state.view === 'dashboard' ? 'on' : ''}" data-action="nav-dash">Minhas listas</a>
      <a href="#" class="${state.view === 'perfil' ? 'on' : ''}" data-action="nav-perfil">Perfil</a>` : ''}
    </nav>
    <div class="auth-zone">${logged ? `<span class="userchip">🟢 ${esc(state.user.nome_usuario)}</span><button class="btn btn-ghost btn-sm" data-action="sair">Sair</button>` : `<button class="btn btn-ghost btn-sm" data-action="page-login">Entrar</button><button class="btn btn-pri btn-sm" data-action="page-cadastro">Criar conta</button>`}</div>
  `;
}

function stepperHTML(step) {
  const steps = [['1','Categorias','categorias'],['2','Lista','lista'],['3','Fornecedores','fornecedores'],['4','Comparação','resultados'],['5','Vencedora','vencedora']];
  return `<div class="stepper">` + steps.map((s, i) => {
    const n = i + 1;
    const cls = n < step ? 'done' : n === step ? 'active' : '';
    return `${i > 0 ? '<div class="stp-bar ' + (n <= step ? 'done' : '') + '"></div>' : ''}<div class="stp ${cls}" ${n < step ? `data-action="goto-step" data-step="${s[2]}"` : ''}><div class="dot">${n < step ? '✓' : n}</div><div class="lb">${s[1]}</div></div>`;
  }).join('') + `</div>`;
}

function vHome() {
  const logged = !!state.user;
  return `<div class="container page">
    <section class="hero">
      <div>
        <span class="tag">Comparador inteligente · MVP</span>
        <h1>Compras mais inteligentes,<br>economia de verdade.</h1>
        <p>Crie sua lista, filtre fornecedores por categoria, compare preço e disponibilidade em uma única tela — e exporte a lista vencedora em PDF. Sem cadastro obrigatório.</p>
        <div class="cta-row">
          <button class="btn btn-white btn-lg" data-action="nav-nova" data-primary>Criar minha lista →</button>
          <button class="btn btn-outlinew btn-lg" data-action="page-login">${logged ? 'Minhas listas' : 'Entrar na minha conta'}</button>
        </div>
      </div>
      <div class="mini-compare" aria-hidden="true">
        <h4>Comparação da sua lista · 6 produtos · 3 fornecedores</h4>
        <div class="mini-row"><span>🏆 Carrefour · 100% disponível</span><b>R$ 158,47</b></div>
        <div class="mini-row"><span>Pão de Açúcar · 100% disponível</span><b>R$ 173,80</b></div>
        <div class="mini-row"><span>Extra · 83% disponível ⚠ 1 ausente</span><b>R$ 118,75</b></div>
        <div class="mini-foot"><span>Melhor oferta = maior cobertura</span><span>desempate: menor total</span></div>
      </div>
    </section>
    <section class="value-cards">
      <div class="card vcard"><div class="ic">🏷️</div><h3>Pré-filtro por categorias</h3><p>Escolha entre 11 categorias macro (Mercado, Vestuário, Eletrodomésticos…) para ver apenas fornecedores relevantes (RF12).</p></div>
      <div class="card vcard"><div class="ic">📊</div><h3>Comparação clara</h3><p>Tabela flat por fornecedor: preço total, % de cobertura e itens ausentes. A melhor oferta é destacada (RF15/RF16).</p></div>
      <div class="card vcard"><div class="ic">📄</div><h3>PDF da lista vencedora</h3><p>Exporte a lista do fornecedor campeão com itens precificados e total consolidado (RF17). Funciona sem login.</p></div>
    </section>
    <section class="card card-pad mt">
      <div class="row-between mb"><h2 style="font-size:18px">Como funciona</h2><span class="muted small">Fluxo principal · visitante percorre tudo sem autenticação</span></div>
      <div class="howto">
        <div class="how"><div class="n">1</div><b>Categorias</b><span>Pré-filtro</span></div>
        <div class="how"><div class="n">2</div><b>Lista</b><span>Produtos + qtd</span></div>
        <div class="how"><div class="n">3</div><b>Fornecedores</b><span>Seleção 2–10</span></div>
        <div class="how"><div class="n">4</div><b>Comparar</b><span>Tabela flat</span></div>
        <div class="how"><div class="n">5</div><b>Exportar</b><span>PDF / Imprimir</span></div>
      </div>
    </section>
    <section class="persona-strip"><span class="av">👩‍🍳</span>
      <div style="flex:1"><b>Conheça Mariana Duarte, 34 — dona do restaurante “Tempero da Mari”</b>
        <p>Toda semana ela compra insumos para ~40 refeições em 3 mercados diferentes. Sem o COBECO: planilha, telefone e risco de escolher o “mais barato” incompleto.</p></div>
      <button class="btn btn-pri" data-action="nav-nova">Iniciar jornada →</button>
    </section>
  </div>`;
}

function vCategorias() {
  const totalCats = totalCategorias();
  const areasHTML = state.areasGrandes.length
    ? `<div class="areas-bar"><strong>Grandes áreas:</strong>
      ${state.areasGrandes.map(a => `<label class="area-cb"><input type="checkbox" class="area-cb-input" value="${a.id}" ${state.areasSelecionadas.includes(a.id) ? 'checked' : ''}> ${esc(a.nome)}</label>`).join('')}
      <button class="btn btn-ghost btn-sm" data-action="area-limpar">Limpar áreas</button></div>`
    : `<div class="areas-bar" style="color:#9ca3af;font-size:13px">Grandes áreas não carregadas.</div>`;
  return `<div class="container page">
    <div class="page-head"><span class="kicker">Passo 1 de 5 · Pré-filtro</span>
      <h1>Selecione as categorias</h1>
      <p>Escolha uma ou mais categorias macro para filtrar os fornecedores. Mínimo: 1 categoria (RF12). Use as grandes áreas para enxergar o catálogo; a seleção fica em memória (transitória).</p></div>
    ${stepperHTML(1)}
    <div class="card card-pad">
      ${areasHTML}
      <div class="toolbar">
        <span class="count-chip ${state.categorias.length ? 'ok' : ''}" id="cat-count">${state.categorias.length} categoria(s) selecionada(s) · ${totalCats} disponíveis</span>
        <div><button class="btn btn-ghost btn-sm" data-action="cat-all">Selecionar todas</button>
        <button class="btn btn-ghost btn-sm" data-action="cat-none">Limpar</button></div>
      </div>
        <div class="search-box"><label>Buscar categoria (semântica)</label>
          <input type="text" id="busca-cat" value="${esc(state.categoriaBusca)}" placeholder="Ex.: roupas, camiseta, pá, rastelo" autocomplete="off" role="combobox">
        </div>
      <div class="cat-grid" role="group" aria-label="Categorias macro">
        ${(state.categoriasVisiveis.length ? state.categoriasVisiveis : []).map(c => `<label class="cat-card ${state.categorias.includes(c.id) ? 'sel' : ''}" data-catcard="${c.id}">
          <input type="checkbox" class="cat-cb" value="${c.id}" ${state.categorias.includes(c.id) ? 'checked' : ''}>
          <span class="ci">${c.ic}</span><span class="cn">${esc(c.nome)}</span></label>`).join('')}
      </div>
      <div class="tip">ℹ️ <b>Como funciona:</b> os fornecedores exibidos na próxima etapa pertencem às categorias selecionadas. Categorias já escolhidas permanecem visíveis mesmo durante a busca (RF26).</div>
      <div class="row-between mt">
        <button class="btn btn-ghost" data-action="nav-home">← Voltar</button>
        <div>
          <button class="btn btn-pri btn-lg" id="btn-to-lista" data-action="to-lista" data-primary ${state.categorias.length ? '' : 'disabled'}>Continuar para a lista →</button>
          ${state.categorias.length ? '' : `<div class="hint-disabled">⚠️ Selecione ao menos 1 categoria para continuar.</div>`}
        </div>
      </div>
    </div>
  </div>`;
}

// Recalcula categorias visíveis aplicando filtro de áreas grandes + busca,
// garantindo que categorias já selecionadas permaneçam visíveis (RF26).
function recalcularVisiveis(baseCats, { fullRender = true } = {}) {
  const baseIds = new Set(baseCats.map(c => c.id));
  const selecionadas = state.categoriasDisponiveis.filter(c => state.categorias.includes(c.id));
  const mescladas = [...baseCats];
  selecionadas.forEach(s => { if (!baseIds.has(s.id)) mescladas.push(s); });
  state.categoriasVisiveis = mescladas;
  if (fullRender) {
    render();
  } else {
    atualizarGridCategorias();
  }
}

// Atualiza apenas o grid de categorias e contador, sem full render (preserva foco)
function atualizarGridCategorias() {
  const grid = document.getElementById('cat-grid');
  if (!grid) return;
  grid.innerHTML = state.categoriasVisiveis.map(c => `<label class="cat-card ${state.categorias.includes(c.id) ? 'sel' : ''}" data-catcard="${c.id}">
    <input type="checkbox" class="cat-cb" value="${c.id}" ${state.categorias.includes(c.id) ? 'checked' : ''}>
    <span class="ci">${c.ic}</span><span class="cn">${esc(c.nome)}</span></label>`).join('');
  const countChip = document.getElementById('cat-count');
  if (countChip) {
    countChip.textContent = `${state.categorias.length} categoria(s) selecionada(s) · ${totalCategorias()} disponíveis`;
    countChip.classList.toggle('ok', state.categorias.length > 0);
  }
  const btn = document.getElementById('btn-to-lista');
  if (btn) btn.disabled = !state.categorias.length;
}

function areasParaCategorias(areaIds) {
  if (!areaIds.length) return state.categoriasDisponiveis.slice();
  const out = [];
  state.areasGrandes.forEach(a => {
    if (areaIds.includes(a.id)) {
      a.categorias.forEach(cid => {
        const c = state.categoriasDisponiveis.find(x => x.id === cid);
        if (c && !out.find(o => o.id === c.id)) out.push(c);
      });
    }
  });
  return out;
}

function vLista() {
  const un = state.lista.itens.reduce((s, i) => s + i.qtd, 0);
  const logado = !!state.user;
  return `<div class="container page">
    <div class="page-head"><span class="kicker">Passo 2 de 5 · Lista de compras</span>
      <h1>Monte sua lista</h1>
      <p>Adicione produtos do catálogo e ajuste quantidades (1–9999). Armazenamento: <b>em memória / sessionStorage</b> até salvar.</p></div>
    ${stepperHTML(2)}
    <div class="two-col">
      <div class="card card-pad">
        <div class="row-between mb"><span class="mode-chip ${logado ? 'mode-db' : 'mode-eph'}">${logado ? '🔒 CONTA: ' + esc(state.user) : '⚠ MODO EFÊMERO (visitante)'}</span>
          <button class="btn btn-ghost btn-sm" data-action="demo-lista" title="Acelera a live demo">⚡ Preencher com a lista da Mariana (demo)</button></div>
        <div class="field" id="f-nome">
          <label for="nome-lista">Nome da lista <span class="req">*</span></label>
          <input type="text" id="nome-lista" maxlength="100" value="${esc(state.lista.nome)}" placeholder="Ex.: Compras do Mês" autocomplete="off">
          <div class="counter"><span id="nome-count">${state.lista.nome.length}</span>/100</div>
          <div class="err-msg">Informe um nome para a lista.</div>
        </div>
        <div class="field searchbox">
          <label for="busca">Adicionar produto — autocomplete (mín. 2 caracteres)</label>
          <input type="text" id="busca" value="${esc(state.busca)}" placeholder="Digite para buscar no catálogo… ex.: arroz" autocomplete="off" role="combobox" aria-expanded="false">
          <div id="sug-box"></div>
        </div>
        <h3 style="font-size:15px;margin:8px 0 10px">Itens da lista</h3>
        <div id="itens-box">${itensTableHTML()}</div>
      </div>
      <aside class="card card-pad resumo"><h3>Resumo</h3>
        <div class="res-line"><span>Produtos</span><b id="r-prod">${state.lista.itens.length}</b></div>
        <div class="res-line"><span>Unidades totais</span><b id="r-un">${un}</b></div>
        <div class="res-line"><span>Categorias filtradas</span><b>${state.categorias.length}</b></div>
        <div class="res-line"><span>Modo</span><b>${logado ? 'Conta' : 'Efêmero'}</b></div>
        <div class="actions-stack">
          <button class="btn btn-pri btn-lg" id="btn-to-forn" data-action="to-fornecedores" data-primary ${state.lista.itens.length ? '' : 'disabled'}>Comparar preços →</button>
          ${state.lista.itens.length ? '' : `<div class="hint-disabled">Adicione ao menos 1 item para comparar.</div>`}
          <button class="btn btn-ghost" data-action="salvar-lista">${logado ? '💾 Salvar lista' : '💾 Salvar lista 🔒'}</button>
        </div>
        <div class="tip">💡 Visitantes podem comparar e exportar sem conta. A autenticação é exigida <b>apenas para salvar</b> (RF08) — o rascunho é preservado durante o login.</div>
      </aside>
    </div>
  </div>`;
}

function itensTableHTML() {
  if (!state.lista.itens.length) return `<div class="empty"><div class="big">🧺</div>Nenhum produto adicionado. Use a busca acima.</div>`;
  return `<table class="tbl"><thead><tr><th>Produto</th><th style="width:130px">Qtd.</th><th style="width:80px">Un.</th><th style="width:44px"></th></tr></thead><tbody>
   ${state.lista.itens.map((i, ix) => { const p = state.produtos.find(x => x.id === i.pid); return `<tr>
    <td><b>${esc(p ? p.nome : 'Desconhecido')}</b></td>
    <td><span class="qty"><button data-action="dec" data-ix="${ix}" aria-label="Diminuir">−</button>
     <input type="text" inputmode="numeric" value="${i.qtd}" data-qtdix="${ix}" aria-label="Quantidade">
     <button data-action="inc" data-ix="${ix}" aria-label="Aumentar">+</button></span></td>
    <td class="muted">${p ? p.un : 'un'}</td>
    <td><button class="icon-del" data-action="del-item" data-ix="${ix}" title="Remover item" aria-label="Remover">${esc(p ? p.nome : '')} ✕</button></td></tr>`; }).join('')}
  </tbody></table>`;
}

function vFornecedores() {
  return `<div class="container page">
    <div class="page-head"><span class="kicker">Passo 3 de 5 · Fornecedores</span>
      <h1>Escolha os fornecedores</h1>
      <p>Selecione de <b>2 a 10</b> fornecedores (RF13). Apenas fornecedores das categorias escolhidas (${state.categorias.map(c => (state.categoriasDisponiveis.find(x => x.id === c) || { nome: '' }).nome).join(', ')}) são exibidos. O % indica a cobertura da sua lista.</p></div>
    ${stepperHTML(3)}
    <div class="card card-pad slider-box">
      <div class="sl-head"><label for="slider-disp"><b>Filtro de disponibilidade (UC05)</b> — mostrar apenas fornecedores com cobertura mínima da lista</label>
       <output id="slider-out">${state.filtroDisp}%</output></div>
      <input type="range" id="slider-disp" min="0" max="100" step="5" value="${state.filtroDisp}" aria-label="Disponibilidade mínima">
      <div class="sl-scale"><span>0% (todos)</span><span>50%</span><span>100%</span></div>
    </div>
    <div class="card card-pad">
      <div class="toolbar">
        <span class="count-chip ${state.fornecedores.length >= 2 ? 'ok' : ''}" id="forn-count">${state.fornecedores.length} selecionado(s) · mín 2 · máx 10</span>
        <div><button class="btn btn-ghost btn-sm" data-action="forn-all">Selecionar todos</button>
        <button class="btn btn-ghost btn-sm" data-action="forn-clear">Limpar</button></div>
      </div>
      <div id="forn-grid" class="forn-grid">${fornCardsHTML()}</div>
      <div class="row-between mt">
        <button class="btn btn-ghost" data-action="goto-step" data-step="lista">← Voltar à lista</button>
        <div>
          <button class="btn btn-pri btn-lg" id="btn-calc" data-action="calcular" data-primary ${state.fornecedores.length >= 2 ? '' : 'disabled'}>Calcular orçamento →</button>
          ${state.fornecedores.length >= 2 ? '' : `<div class="hint-disabled">⚠️ Selecione ao menos 2 fornecedores.</div>`}
        </div>
      </div>
    </div>
  </div>`;
}

function fornCardsHTML() {
  const eleg = fornecedoresElegiveis();
  if (!eleg.length) return `<div class="empty" style="grid-column:1/-1"><div class="big">🔎</div>Nenhum fornecedor disponível nas categorias selecionadas.<br>Tente incluir outras categorias ou reduzir o filtro de disponibilidade.</div>`;
  return eleg.map(f => {
    const covPct = state.coberturaPorFornecedor[f.id] ?? coberturaDe(f.id);
    const cov = Math.round(covPct * 100);
    const sel = state.fornecedores.includes(f.id);
    const cls = cov >= 80 ? 'cov-hi' : cov >= 40 ? 'cov-md' : 'cov-lo';
    return `<label class="forn-card ${sel ? 'sel' : ''}" data-forncard="${f.id}">
     <div class="forn-cb-row"><input type="checkbox" class="forn-cb" value="${f.id}" ${sel ? 'checked' : ''}>
     <div style="flex:1"><div class="forn-top"><b>${esc(f.nome)}</b>
       <span class="cov-badge ${cls}" title="Itens da sua lista disponíveis neste fornecedor">${cov}% da lista</span></div>
      <div class="forn-cats">${(f.cats || []).filter(c => state.categorias.includes(c)).map(c => `<span class="mini-tag">${nomeCategoria(c)}</span>`).join('')}</div>
     </div></div></label>`;
  }).join('');
}

function vResultados() {
  if (!state.resultado) return vFornecedores();
  const R = state.resultado, W = R.winner;
  return `<div class="container page">
    <div class="page-head"><span class="kicker">Passo 4 de 5 · Resultados</span>
      <h1>Comparação de preços</h1>
      <p>Lista “${esc(state.lista.nome || '(sem nome)')}” · ${state.lista.itens.length} itens · ${state.resultado.rows.length} fornecedores. Ordenado pelo menor total (RF15); melhor oferta destacada (RF16).</p></div>
    ${stepperHTML(4)}
    <div class="kpis">
      <div class="card kpi win"><div class="k">🏆 Melhor oferta</div><div class="v">${W.nome}</div><div class="s">${BRL(W.total)} · ${Math.round(W.cobertura*100)}% da lista</div></div>
      <div class="card kpi"><div class="k">💰 Menor preço</div><div class="v">${BRL(R.minTotal)}</div><div class="s">pode ter itens ausentes</div></div>
      <div class="card kpi"><div class="k">📊 Economia potencial</div><div class="v">${BRL(R.maxTotal - W.total > 0 ? R.maxTotal - W.total : 0)}</div><div class="s">vs. maior total cotado</div></div>
      <div class="card kpi"><div class="k">Disponibilidade média</div><div class="v">${Math.round(R.rows.reduce((s, r) => s + r.cobertura, 0) / R.rows.length * 100)}%</div><div class="s">${R.rows.length} fornecedores comparados</div></div>
    </div>
    <div class="card" style="overflow:auto">
      <table class="tbl"><thead><tr><th style="width:44px">#</th><th>Fornecedor</th><th>Cobertura</th><th>Itens</th><th>Ausentes</th><th style="text-align:right">Preço total</th></tr></thead><tbody>
   ${R.rows.map((r, i) => {
     const isW = r.fid === W.fid;
     const isMin = r.total === R.minTotal;
     return `<tr class="${isW ? 'row-win' : ''}">
      <td class="muted">${i + 1}</td>
      <td><b>${r.nome}</b> ${isW ? `<span class="badge b-ok">🏆 Melhor oferta</span>` : ''} ${isMin && !isW ? `<span class="badge b-warn">💰 Menor preço</span>` : ''}</td>
      <td><span class="cov-bar"><i style="width:${Math.round(r.cobertura * 100)}%"></i></span>${Math.round(r.cobertura * 100)}%</td>
      <td>${r.nDisp} de ${state.lista.itens.length}</td>
      <td>${r.parcial ? `<span class="badge b-warn">⚠ ${r.nAus} item(ns)</span>` : `<span class="muted">—</span>`}</td>
      <td style="text-align:right;font-weight:800;font-variant-numeric:tabular-nums">${BRL(r.total)}${r.parcial ? ` <span class="badge b-mut">parcial</span>` : ''}</td></tr>`;
   }).join('')}
   </tbody></table>
   </div>
    <div class="warn-banner"><span>⚠️</span><span><b>Atenção:</b> o menor preço pode não incluir todos os itens da sua lista. A melhor oferta considera a <b>maior cobertura</b>; em caso de empate, vence o <b>menor total</b> — verifique a coluna “Ausentes”.</span></div>
    <div class="row-between">
      <button class="btn btn-ghost" data-action="goto-step" data-step="fornecedores">← Editar fornecedores</button>
      <div class="btn-group">
        <button class="btn btn-ghost" data-action="print-a4">🖨️ Imprimir (A4)</button>
        <button class="btn btn-ghost" data-action="export-pdf">📄 Exportar PDF</button>
        <button class="btn btn-ok btn-lg" data-action="ver-vencedora" data-primary>🏆 Ver lista vencedora →</button>
      </div>
    </div>
    <p class="rule-note">Regra da melhor oferta (RF16): maior percentual de cobertura da lista; empate → menor custo total.</p>
  </div>`;
}

function vVencedora() {
  if (!state.resultado) return vResultados();
  const W = state.resultado.winner;
  return `<div class="container page">
    <div class="page-head"><span class="kicker">Passo 5 de 5 · Exportação</span>
      <h1>Lista vencedora</h1>
      <p>Conteúdo da sua lista <b>precificado pelo fornecedor campeão</b>, com total consolidado. É este documento que o PDF exporta (RF17) — nunca a tabela comparativa.</p></div>
    ${stepperHTML(5)}
    <div class="win-hero">
      <div><span class="badge b-ok" style="margin-bottom:8px">🏆 MELHOR OFERTA · ${Math.round(W.cobertura * 100)}% DA LISTA</span>
        <h2>${W.nome}</h2><div class="meta">CNPJ ${W.cnpj} · cotação de ${hoje()} · lista “${esc(state.lista.nome || '(sem nome)')}”</div></div>
      <div style="text-align:right"><div class="muted small">Total consolidado</div>
        <div style="font-size:30px;font-weight:800;font-variant-numeric:tabular-nums">${BRL(W.total)}</div>
        ${W.parcial ? `<span class="badge b-warn">total parcial — há itens indisponíveis</span>` : `<span class="badge b-ok">todos os itens disponíveis</span>`}</div>
    </div>
    <table class="tbl"><thead><tr><th>Produto</th><th>Un</th><th style="width:90px">Qtd</th><th style="text-align:right">Unitário</th><th style="text-align:right">Subtotal</th></tr></thead><tbody>
   ${state.lista.itens.map(i => {
     const itemWin = (W.itens || []).find(it => it.pid === i.pid);
     const p = state.produtos.find(x => x.id === i.pid) || { nome: 'Desconhecido', un: 'un' };
     if (itemWin && itemWin.disponivel) return `<tr><td>${esc(p.nome)}</td><td class="muted">${p.un}</td><td>${i.qtd}</td><td style="text-align:right">${BRL(itemWin.preco)}</td><td style="text-align:right">${BRL(itemWin.preco * i.qtd)}</td></tr>`;
     return `<tr style="opacity:.55"><td>${esc(p.nome)}</td><td class="muted">${p.un}</td><td>${i.qtd}</td><td colspan="2" style="text-align:right"><span class="badge b-warn">Indisponível</span></td></tr>`;
   }).join('')}
   </tbody></table>
   </div>
   <div class="row-between mt">
      <button class="btn btn-ghost" data-action="goto-step" data-step="resultados">← Voltar aos resultados</button>
      <div class="btn-group">
        <button class="btn btn-ghost btn-lg" data-action="print-a4">🖨️ Imprimir A4</button>
        <button class="btn btn-pri btn-lg" data-action="export-pdf" data-primary>⬇ Exportar PDF — lista_${stamp()}.pdf</button>
      </div>
   </div>
</div>`;
}

function vLogin() {
  return `<div class="auth-wrap"><div class="card auth-card"><span class="step-pill">Login</span><h1>Entrar</h1><p class="sub">A autenticação é exigida apenas para salvar listas.</p>
    <form id="form-login" novalidate>
      <div class="field"><label>Usuário</label><input type="text" id="l-user" placeholder="usuário"></div>
      <div class="field"><label>Senha</label><input type="password" id="l-pass" placeholder="senha"></div>
      <button class="btn btn-pri btn-lg btn-block" data-action="login" data-primary>Entrar</button>
    </form><div class="auth-foot">Não tem conta? <button class="linklike" data-action="page-cadastro">Criar conta</button></div></div></div>`;
}

function vCadastro() {
  return `<div class="auth-wrap"><div class="card auth-card"><span class="step-pill">Cadastro</span><h1>Criar conta</h1><p class="sub">Preencha para salvar listas.</p>
    <form id="form-cad" novalidate>
      <div class="field"><label>Usuário</label><input type="text" id="c-user" placeholder="mín. 3 alfanuméricos"></div>
      <div class="field"><label>Nome</label><input type="text" id="c-nome" placeholder="Nome completo"></div>
      <div class="field"><label>Email</label><input type="email" id="c-email" placeholder="email@exemplo.com"></div>
      <div class="field"><label>Senha</label><input type="password" id="c-senha" placeholder="mín. 8 · 1 maiúscula · 1 número · 1 especial"></div>
      <div class="field"><label>Confirmar senha</label><input type="password" id="c-conf"></div>
      <div class="field"><label>Pergunta de segurança</label><select id="c-perg"><option value="">Selecione…</option><option value="pet">Qual seu pet?</option><option value="cidade">Cidade natal?</option><option value="escola">Escola?</option></select></div>
      <div class="field"><label>Resposta</label><input type="text" id="c-resp" placeholder="mín. 3"></div>
      <button class="btn btn-pri btn-lg btn-block" data-action="cadastrar" data-primary>Criar conta</button>
    </form><div class="auth-foot">Já tem conta? <button class="linklike" data-action="page-login">Entrar</button></div></div></div>`;
}

// ============================================================
// HANDLERS DE AUTENTICAÇÃO
// ============================================================
async function handleCadastro() {
  const form = document.getElementById('form-cad');
  if (!form) return;

  const data = {
    nome_usuario: document.getElementById('c-user').value.trim(),
    nome: document.getElementById('c-nome').value.trim(),
    email: document.getElementById('c-email').value.trim(),
    senha: document.getElementById('c-senha').value,
    confirmar_senha: document.getElementById('c-conf').value,
    pergunta_seguranca: document.getElementById('c-perg').value,
    resposta_seguranca: document.getElementById('c-resp').value.trim(),
  };

  // Validação básica
  if (!data.nome_usuario || !data.nome || !data.email || !data.senha || !data.confirmar_senha || !data.pergunta_seguranca || !data.resposta_seguranca) {
    showToast('Preencha todos os campos.', 'error');
    return;
  }
  if (data.senha !== data.confirmar_senha) {
    showToast('As senhas não coincidem.', 'error');
    return;
  }
  if (data.senha.length < 8) {
    showToast('Senha deve ter no mínimo 8 caracteres.', 'error');
    return;
  }

  const btn = form.querySelector('button[data-action="cadastrar"]');
  if (btn) { btn.disabled = true; btn.textContent = 'Criando…'; }

  try {
    const res = await ApiClient.request('/auth/cadastrar', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (res?.access_token) {
      state.user = { nome_usuario: data.nome_usuario };
      showToast('Conta criada e login automático realizado!', 'success');
      go('categorias');
    }
  } catch (e) {
    showToast(e.message || 'Erro ao cadastrar.', 'error');
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = 'Criar conta'; }
  }
}

async function handleLogin() {
  const form = document.getElementById('form-login');
  if (!form) return;

  const data = {
    nome_usuario: document.getElementById('l-user').value.trim(),
    senha: document.getElementById('l-pass').value,
  };

  if (!data.nome_usuario || !data.senha) {
    showToast('Preencha usuário e senha.', 'error');
    return;
  }

  const btn = form.querySelector('button[data-action="login"]');
  if (btn) { btn.disabled = true; btn.textContent = 'Entrando…'; }

  try {
    const res = await ApiClient.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (res?.access_token) {
      state.user = { nome_usuario: data.nome_usuario };
      showToast('Login realizado com sucesso!', 'success');
      go('categorias');
    }
  } catch (e) {
    showToast(e.message || 'Erro ao entrar.', 'error');
  } finally {
    if (btn) { btn.disabled = false; btn.textContent = 'Entrar'; }
  }
}

// ============================================================
// DISPATCH DE CLIQUES
// ============================================================

function temRascunho() {
  return state.lista.itens.length > 0 || state.categorias.length > 0 || state.areasSelecionadas.length > 0;
}

function limparRascunho() {
  state.lista = { nome: '', itens: [] };
  state.categorias = [];
  state.areasSelecionadas = [];
  persistJornada();
}

// RF25: ao tentar voltar ao início com rascunho, pergunta se esquece a lista em andamento
async function irParaInicioComModal(destino) {
  if (!temRascunho()) { go(destino); return; }
  const esquecer = await Modal.confirm(
    `Esquecer lista em andamento? (${state.lista.itens.length} itens, ${state.categorias.length} categorias, ${state.areasSelecionadas.length} áreas)`,
    { title: 'Lista em andamento', confirmText: 'Sim — começar nova', cancelText: 'Não — manter', variant: 'warning' }
  );
  if (esquecer) { limparRascunho(); go(destino); }
  // Não → mantém tela e rascunho (não navega)
}

// RF22/RF23: concluir lista efêmera → espaço próprio (gerada/historico),
// limpa rascunho e retorna ao início para próxima lista.
function concluirJornada() {
  const gerada = {
    lista: { ...state.lista },
    categorias: [...state.categorias],
    areas: [...state.areasSelecionadas],
    fornecedores: [...state.fornecedores],
    resultado: state.resultado ? { ...state.resultado } : null,
    exportadoEm: new Date().toISOString()
  };
  state.historicoSessao = [...(state.historicoSessao || []), gerada];
  state.listaGerada = gerada;
  limparRascunho();
  go('home');
  showToast('Lista concluída. Inicie uma nova lista.', 'success');
}


// ============================================================
// HANDLERS DE AUTENTICAÇÃO E SALVAMENTO DE LISTA
// ============================================================
async function handleSalvarLista() {
  const logado = !!state.user;

  if (!logado) {
    // Usuário não logado: modal de aviso para cadastro
    const querCadastrar = await Modal.confirm(
      'Salvar listas é apenas para usuários cadastrados. Deseja criar uma conta agora?',
      { title: 'Cadastro necessário', confirmText: 'Criar conta', cancelText: 'Cancelar', variant: 'info' }
    );
    if (!querCadastrar) {
      // Usuário não quer cadastrar: pergunta se quer descartar a lista
      const descartar = await Modal.confirm(
        'Deseja descartar a lista em andamento?',
        { title: 'Descartar lista', confirmText: 'Sim, descartar', cancelText: 'Não, manter', variant: 'warning' }
      );
      if (descartar) {
        limparRascunho();
        go('home');
        showToast('Lista descartada.', 'info');
      }
      return;
    }
    // Redireciona para cadastro; após cadastro bem-sucedido, handleCadastro promoverá a lista
    go('cadastro');
    return;
  }

  // Usuário logado: confirmação para salvar
  const confirmar = await Modal.confirm(
    'Deseja salvar a lista em andamento?',
    { title: 'Salvar lista', confirmText: 'Salvar', cancelText: 'Cancelar', variant: 'primary' }
  );
  if (!confirmar) return;

  // Salva via API
  try {
    const btn = document.querySelector('[data-action="salvar-lista"]');
    if (btn) { btn.disabled = true; btn.textContent = 'Salvando…'; }

    const data = {
      nome: state.lista.nome || 'Lista',
      itens: state.lista.itens.map(i => ({ produto_id: i.pid, quantidade: i.qtd })),
      categorias: state.categorias,
    };
    const res = await ApiClient.request('/listas', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (res) {
      showToast('Lista salva com sucesso!', 'success');
      limparRascunho();
      go('home');
    }
  } catch (e) {
    showToast(e.message || 'Erro ao salvar lista.', 'error');
  } finally {
    const btn = document.querySelector('[data-action="salvar-lista"]');
    if (btn) { btn.disabled = false; btn.textContent = '💾 Salvar lista'; }
  }
}

async function handleCadastro() {
  const form = document.getElementById('form-cad');
  if (!form) return;

  const data = {
    nome_usuario: document.getElementById('c-user').value.trim(),
    nome: document.getElementById('c-nome').value.trim(),
    email: document.getElementById('c-email').value.trim(),
    senha: document.getElementById('c-senha').value,
    confirmar_senha: document.getElementById('c-conf').value,
    pergunta_seguranca: document.getElementById('c-perg').value,
    resposta_seguranca: document.getElementById('c-resp').value.trim(),
  };

  // Validação básica
  if (!data.nome_usuario || !data.nome || !data.email || !data.senha || !data.confirmar_senha || !data.pergunta_seguranca || !data.resposta_seguranca) {
    showToast('Preencha todos os campos.', 'error');
    return;
  }
  if (data.senha !== data.confirmar_senha) {
    showToast('As senhas não coincidem.', 'error');
    return;
  }
  if (data.senha.length < 8) {
    showToast('Senha deve ter no mínimo 8 caracteres.', 'error');
    return;
  }

  const btn = form.querySelector('button[type="submit"]');
  if (btn) { btn.disabled = true; btn.textContent = 'Criando…'; }

  try {
    const res = await ApiClient.request('/auth/cadastrar', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (res?.access_token) {
      state.user = { nome_usuario: data.nome_usuario };
      showToast('Conta criada e login automático realizado!', 'success');
      // Após cadastro, promove a lista efêmera se houver
      if (state.lista.itens.length > 0) {
        await promoverListaEfemera();
      }
      go('categorias');
    }
  } catch (e) {
    showToast(e.message || 'Erro ao cadastrar.', 'error');
  } finally {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) { btn.disabled = false; btn.textContent = 'Criar conta'; }
  }
}

async function promoverListaEfemera() {
  try {
    const btn = document.querySelector('[data-action="salvar-lista"]');
    if (btn) { btn.disabled = true; btn.textContent = 'Salvando lista…'; }

    const data = {
      nome: state.lista.nome || 'Lista',
      itens: state.lista.itens.map(i => ({ produto_id: i.pid, quantidade: i.qtd })),
      categorias: state.categorias,
    };
    const res = await ApiClient.request('/listas/promover-efemera', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (res) {
      showToast('Lista efêmera salva com sucesso!', 'success');
      limparRascunho();
    }
  } catch (e) {
    showToast(e.message || 'Erro ao salvar lista efêmera.', 'error');
  } finally {
    const btn = document.querySelector('[data-action="salvar-lista"]');
    if (btn) { btn.disabled = false; btn.textContent = '💾 Salvar lista'; }
  }
}

async function handleLogin() {
  const form = document.getElementById('form-login');
  if (!form) return;

  const data = {
    nome_usuario: document.getElementById('l-user').value.trim(),
    senha: document.getElementById('l-pass').value,
  };

  if (!data.nome_usuario || !data.senha) {
    showToast('Preencha usuário e senha.', 'error');
    return;
  }

  const btn = form.querySelector('button[type="submit"]');
  if (btn) { btn.disabled = true; btn.textContent = 'Entrando…'; }

  try {
    const res = await ApiClient.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (res?.access_token) {
      state.user = { nome_usuario: data.nome_usuario };
      showToast('Login realizado com sucesso!', 'success');
      // Após login, promove a lista efêmera se houver
      if (state.lista.itens.length > 0) {
        await promoverListaEfemera();
      }
      go('categorias');
    }
  } catch (e) {
    showToast(e.message || 'Erro ao entrar.', 'error');
  } finally {
    const btn = form.querySelector('button[type="submit"]');
    if (btn) { btn.disabled = false; btn.textContent = 'Entrar'; }
  }
}
document.addEventListener('click', (e) => {
  const t = e.target;
  if (t.classList.contains('cat-cb')) {
    const id = +t.value;
    state.categorias = state.categorias.includes(id) ? state.categorias.filter(x => x !== id) : [...state.categorias, id];
    render();
    return;
  }
  if (t.classList.contains('area-cb-input')) {
    const id = +t.value;
    state.areasSelecionadas = state.areasSelecionadas.includes(id)
      ? state.areasSelecionadas.filter(x => x !== id)
      : [...state.areasSelecionadas, id];
    recalcularVisiveis(areasParaCategorias(state.areasSelecionadas));
    return;
  }
  if (t.classList.contains('forn-cb')) {
    const id = +t.value;
    state.fornecedores = state.fornecedores.includes(id) ? state.fornecedores.filter(x => x !== id) : [...state.fornecedores, id];
    const card = t.closest('[data-forncard]');
    if (card) card.classList.toggle('sel', state.fornecedores.includes(id));
    refreshFornecedores();
    return;
  }
  const el = e.target.closest('[data-action]');
  if (!el) return;
  e.preventDefault();
  const a = el.dataset.action;
  switch (a) {
    case 'nav-home': irParaInicioComModal('home'); break;
    case 'nav-nova': irParaInicioComModal('categorias'); break;
    case 'nav-dash': case 'nav-perfil': showToast('Em construção (wireframe).', 'info'); break;
    case 'page-login': go('login'); break;
    case 'page-cadastro': go('cadastro'); break;
    case 'cadastrar': handleCadastro(); break;
    case 'login': handleLogin(); break;
    case 'sair': state.user = null; showToast('Saiu.', 'info'); render(); break;
    case 'cat-all': state.categorias = state.categoriasDisponiveis.map(c => c.id); render(); break;
    case 'cat-none': state.categorias = []; render(); break;
    case 'area-limpar': state.areasSelecionadas = []; recalcularVisiveis(areasParaCategorias([])); break;
    case 'to-lista': if (!state.categorias.length) { showToast('Selecione ≥1 categoria.', 'error'); return; } carregarProdutos(state.categorias); go('lista'); break;
    case 'goto-step': { const destino = el.dataset.step; if (destino === 'fornecedores' && state.lista.itens.length) { carregarFornecedores(state.categorias).then(() => carregarCoberturaFornecedores().then(() => go(destino))); } else { go(destino); } break; }
    case 'login': handleLogin(); break;
    case 'cadastrar': handleCadastro(); break;
    case 'demo-lista': state.lista = { nome: 'Lista demo', itens: [{ pid: 1, qtd: 2 }, { pid: 2, qtd: 1 }, { pid: 3, qtd: 3 }] }; if (!state.categorias.length) state.categorias = [1]; persistJornada(); render(); showToast('Lista demo carregada.', 'success'); break;
    case 'to-fornecedores': if (!state.lista.itens.length) { showToast('Adicione ≥1 item.', 'error'); return; } carregarFornecedores(state.categorias).then(() => carregarCoberturaFornecedores().then(() => go('fornecedores'))); break;
    case 'forn-all': state.fornecedores = fornecedoresElegiveis().slice(0, 10).map(f => f.id); refreshFornecedores(); break;
    case 'forn-clear': state.fornecedores = []; refreshFornecedores(); break;
    case 'calcular': {
      if (state.fornecedores.length < 2) { showToast('Selecione ≥2 fornecedores.', 'error'); return; }
      const btn = el; btn.disabled = true; btn.textContent = 'Calculando…';
      calcularResultado().then(() => { go('resultados'); btn.disabled = false; btn.textContent = 'Calcular →'; }).catch(() => { btn.disabled = false; btn.textContent = 'Calcular →'; });
      break;
    }
    case 'ver-vencedora': go('vencedora'); break;
    case 'export-pdf': {
      if (!state.resultado) { showToast('Compare antes de exportar.', 'warning'); return; }
      showToast('Gerando PDF…', 'info');
      ApiClient.exportarPDFVencedora({ itens: state.lista.itens.map(i => ({ produto_id: i.pid, quantidade: i.qtd })), fornecedor_ids: state.fornecedores, lista_nome: state.lista.nome || 'Lista' })
        .then(blob => {
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a'); a.href = url; a.download = `lista_${stamp()}.pdf`; a.click();
          URL.revokeObjectURL(url);
          showToast('PDF baixado.', 'success');
          concluirJornada();
        }).catch(() => showToast('Erro ao gerar PDF.', 'error'));
      break;
    }
    case 'dec': case 'inc': {
      const ix = +el.dataset.ix; const it = state.lista.itens[ix];
      it.qtd = Math.min(9999, Math.max(1, it.qtd + (a === 'inc' ? 1 : -1))); persistJornada(); refreshListaUI(); break;
    }
    case 'del-item': state.lista.itens.splice(+el.dataset.ix, 1); persistJornada(); refreshListaUI(); break;
    case 'nome-lista': case 'busca': break;
    case 'salvar-lista': handleSalvarLista(); break;
  }
});

document.addEventListener('input', (e) => {
  const t = e.target;
  if (t.id === 'nome-lista') { state.lista.nome = t.value; persistJornada(); }
  else if (t.id === 'busca') { state.busca = t.value; updateSugestoes(); }
  else if (t.id === 'busca-cat') { state.categoriaBusca = t.value; buscarCategoriasUI(); }
  else if (t.id === 'slider-disp') { state.filtroDisp = +t.value; document.getElementById('slider-out').textContent = t.value + '%'; refreshFornecedores(); }
});

let sugTimer = null;
async function updateSugestoes() {
  const q = norm(state.busca);
  const box = document.getElementById('sug-box');
  clearTimeout(sugTimer);
  sugTimer = setTimeout(async () => {
    if (!q.length) { box.innerHTML = ''; return; }
    try {
      const res = await ApiClient.buscarProdutos(q, 10);
      const hits = (res || []).slice(0, 10);
      box.innerHTML = hits.length
        ? '<div class="sug">' + hits.map(p => `<div class="sug-item" data-action-add="${p.id}"><span>${esc(p.nome)}</span><span class="un">${p.un || 'un'}</span><span class="rel">${Math.round((p.relevancia || 0) * 100)}% relevância</span></div>`).join('') + '</div>'
        : '<div class="sug-empty">Nenhum produto encontrado.</div>';
    } catch (e) {
      // Fallback para busca local se a API falhar
      const hits = state.produtos.filter(p => norm(p.nome).includes(q)).slice(0, 10);
      box.innerHTML = hits.length ? '<div class="sug">' + hits.map(p => `<div class="sug-item" data-action-add="${p.id}"><span>${esc(p.nome)}</span><span class="un">${p.un}</span></div>`).join('') + '</div>' : '<div class="sug-empty">Nenhum produto encontrado.</div>';
    }
  }, 300);
}

let catTimer = null;
async function buscarCategoriasUI() {
  const q = norm(state.categoriaBusca);
  clearTimeout(catTimer);
  if (!q.length) {
    recalcularVisiveis(areasParaCategorias(state.areasSelecionadas), { fullRender: false });
    return;
  }
  catTimer = setTimeout(async () => {
    try {
      const res = await ApiClient.buscarCategorias(q);
      const base = (res || []).map(c => ({ id: c.id, nome: c.nome, ic: '📂' }));
      // RF26: busca nunca esconde categorias já selecionadas
      recalcularVisiveis(base, { fullRender: false });
    } catch (e) { recalcularVisiveis(areasParaCategorias(state.areasSelecionadas), { fullRender: false }); }
  }, 300);
}

document.addEventListener('click', (e) => {
  const s = e.target.closest('[data-action-add]');
  if (!s) return;
  const pid = +s.dataset.actionAdd;
  const ex = state.lista.itens.find(i => i.pid === pid);
  if (ex) ex.qtd = Math.min(9999, ex.qtd + 1); else state.lista.itens.push({ pid, qtd: 1 });
  state.busca = ''; const b = document.getElementById('busca'); if (b) b.value = ''; document.getElementById('sug-box').innerHTML = '';
  persistJornada(); refreshListaUI();
  showToast('➕ ' + nomeProduto(pid) + ' adicionado.', 'success');
});

// ============================================================
// PERSISTÊNCIA DA JORNADA (sessionStorage — espaço próprio até fechar browser)
// ============================================================
function persistJornada() {
  try {
    sessionStorage.setItem('cobeco_jornada', JSON.stringify({
      rascunho: { lista: state.lista, categorias: state.categorias, areas: state.areasSelecionadas },
      gerada: state.listaGerada,
      historico: state.historicoSessao
    }));
  } catch (e) { }
}
function loadJornada() {
  try {
    const raw = sessionStorage.getItem('cobeco_jornada');
    if (!raw) return;
    const d = JSON.parse(raw);
    if (d.rascunho?.lista?.itens?.length) {
      state.lista = d.rascunho.lista;
      state.categorias = d.rascunho.categorias || [];
      state.areasSelecionadas = d.rascunho.areas || [];
      showToast('Lista efêmera recuperada.', 'success');
    }
    state.listaGerada = d.gerada || null;
    state.historicoSessao = d.historico || [];
  } catch (e) { }
}

function refreshListaUI() {
  document.getElementById('itens-box').innerHTML = itensTableHTML();
  const b = document.getElementById('btn-to-forn'); if (b) b.disabled = !state.lista.itens.length;
}

function refreshFornecedores() {
  document.getElementById('forn-grid').innerHTML = fornCardsHTML();
  const c = document.getElementById('forn-count'); if (c) c.textContent = state.fornecedores.length + ' selecionado(s) · mín 2';
  const b = document.getElementById('btn-calc'); if (b) b.disabled = state.fornecedores.length < 2;
  // Mantém seleção apenas entre fornecedores ainda elegíveis (filtro de disponibilidade/cobertura)
  const elegiveis = new Set(fornecedoresElegiveis().map(f => f.id));
  state.fornecedores = state.fornecedores.filter(id => elegiveis.has(id));
}

// ============================================================
// BOOT
// ============================================================
document.addEventListener("DOMContentLoaded", async () => {
  try {
    await carregarCategorias();
    await carregarAreasGrandes();
    await carregarProdutos();
    loadJornada();
    if (state.areasSelecionadas.length) recalcularVisiveis(areasParaCategorias(state.areasSelecionadas));
    render();
  } catch (e) { document.getElementById('main').innerHTML = '<div style="color:red">Erro: ' + e.message + '</div>'; }
});

window.state = state;
window.refreshFornecedores = refreshFornecedores;
window.refreshListaUI = refreshListaUI;
