// COBECO Frontend — Protótipo Alta Fidelidade v3.2 (monolito)
// Adequado ao protótipo canonico doc-prototype-0003.
// Sem router hash: navegação por views (state.view). Autenticação tardia (só para salvar).
// Todas as regras de negócio desenhadas pelo protótipo estão implementadas aqui.

const API_BASE = '/v1';
const STORAGE_KEYS = {
  EPHEMERAL: 'cobeco_eph',
};

// ============================================================
// UTILITÁRIOS
// ============================================================
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

const formatDate = (isoString) => {
  if (!isoString) return '';
  return new Date(isoString).toLocaleDateString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  });
};

const showToast = (msg, type = 'info') => {
  const box = document.createElement('div');
  box.className = 'toast ' + (type === 'ok' ? 'ok' : type === 'err' ? 'err' : type === 'warn' ? 'warn' : '');
  box.innerHTML = `<span>${esc(msg)}</span>`;
  document.getElementById('toasts').appendChild(box);
  setTimeout(() => {
    box.style.opacity = '0';
    box.style.transition = 'opacity .4s';
    setTimeout(() => box.remove(), 420);
  }, 4200);
};

const openModal = (html) => {
  document.getElementById('modal-root').innerHTML =
    `<div class="overlay" data-action="overlay-click"><div class="modal" role="dialog" aria-modal="true">${html}</div></div>`;
};

const closeModal = () => {
  document.getElementById('modal-root').innerHTML = '';
};

// ============================================================
// SEED (DOC-03) — dados determinísticos do protótipo
// ============================================================
const CATEGORIAS = [
  {id:1,nome:"Mercado",ic:"🛒"},{id:2,nome:"Vestuário",ic:"👕"},{id:3,nome:"Automotivos",ic:"🚗"},
  {id:4,nome:"Informática",ic:"💻"},{id:5,nome:"Decoração",ic:"🖼️"},{id:6,nome:"Móveis",ic:"🛋️"},
  {id:7,nome:"Materiais de Construção e Ferragens",ic:"🧱"},{id:8,nome:"Ferramentas",ic:"🔧"},
  {id:9,nome:"Livros",ic:"📚"},{id:10,nome:"Jardinagem",ic:"🪴"},{id:11,nome:"Eletrodomésticos",ic:"🔌"}];

const FORNECEDORES = [
  {id:1,nome:"Carrefour",cnpj:"99.000.111/0001-22",cats:[1,2,3,5,11,4]},
  {id:2,nome:"Extra",cnpj:"00.111.222/0001-33",cats:[1,2,11]},
  {id:3,nome:"Pão de Açúcar",cnpj:"66.777.888/0001-99",cats:[1]},
  {id:4,nome:"Magazine Luiza",cnpj:"77.888.999/0001-00",cats:[11,4,6]},
  {id:5,nome:"Casas Bahia",cnpj:"88.999.000/0001-11",cats:[11,4,6]},
  {id:6,nome:"Leroy Merlin",cnpj:"11.222.333/0001-44",cats:[7,8,10,5]},
  {id:7,nome:"Etna",cnpj:"22.333.444/0001-55",cats:[5,6]},
  {id:8,nome:"C&A",cnpj:"33.444.555/0001-66",cats:[2]},
  {id:9,nome:"Renner",cnpj:"44.555.666/0001-77",cats:[2]},
  {id:10,nome:"Hering",cnpj:"55.666.777/0001-88",cats:[2]}];

const PRODUTOS = [
  {id:1,nome:"Arroz Tipo 1 5kg",un:"un",base:25.9},{id:2,nome:"Feijão Preto 1kg",un:"un",base:8.2},
  {id:3,nome:"Óleo de Soja 900ml",un:"un",base:6.9},{id:4,nome:"Café Torrado e Moído 500g",un:"un",base:17.5},
  {id:5,nome:"Açúcar Refinado 1kg",un:"un",base:4.4},{id:6,nome:"Leite Integral UHT 1L",un:"un",base:5.1},
  {id:7,nome:"Macarrão Espaguete 500g",un:"un",base:4.8},{id:8,nome:"Molho de Tomate 340g",un:"un",base:3.9},
  {id:9,nome:"Farinha de Trigo 1kg",un:"un",base:5.5},{id:10,nome:"Ovos Brancos (dúzia)",un:"dz",base:9.9},
  {id:11,nome:"Detergente Neutro 500ml",un:"un",base:2.9},{id:12,nome:"Papel Toalha 2 rolos",un:"un",base:6.5},
  {id:13,nome:"Liquidificador 2 Velocidades",un:"un",base:129.9},{id:14,nome:"Notebook i5 8GB",un:"un",base:2899.0},
  {id:15,nome:"Martelo de Unha 25mm",un:"un",base:32.9},{id:16,nome:"Parafuso Philips 5mm (cx)",un:"cx",base:12.5},
  {id:17,nome:"Camiseta Algodão M",un:"un",base:39.9},{id:18,nome:"Calça Jeans 40",un:"un",base:119.9},
  {id:19,nome:"Vaso de Barro 20cm",un:"un",base:45.9},{id:20,nome:"Cadeira de Escritório",un:"un",base:449.9}];

const CATALOGO = {
  1:[1,2,3,4,5,6,7,8,9,10,11,12,13,14,17,18],
  2:[1,2,3,5,6,7,8,9,10,11,12,13,17],
  3:[1,2,3,4,5,6,7,8,9,10,11,12],
  4:[13,14,20],5:[13,14,20],
  6:[15,16,19,20],7:[19,20],8:[17,18],9:[17,18],10:[17]};
const FATOR = {1:.99,2:.93,3:1.14,4:.96,5:1.05,6:.97,7:1.10,8:.95,9:1.00,10:1.04};
const PERGUNTAS = {
  pet:"Qual era o nome do seu primeiro animal de estimação?",
  cidade:"Qual é o nome da sua cidade natal?",
  escola:"Qual era o nome da sua escola de infância?",
};

const temOferta = (f, p) => CATALOGO[f].includes(p);
const preco = (f, p) => {
  const pr = PRODUTOS.find(x => x.id === p);
  const jit = Math.sin(f * 997 + p * 131) * 0.03;
  return Math.round(pr.base * FATOR[f] * (1 + jit) * 100) / 100;
};

// ============================================================
// ESTADO (espelha state do protótipo)
// ============================================================
const state = {
  view: 'home',
  user: null,
  categorias: [],
  categoriasDisponiveis: [], // categorias vindas da API (RF12/UC03)
  fornecedoresDisponiveis: [], // fornecedores vindos da API (RF13/UC04)
  lista: { nome: '', itens: [] },
  listaEditId: null,
  fornecedores: [],
  filtroDisp: 0,
  resultado: null,
  busca: '',
  recStep: 1,
  recUser: null,
  perfilEdit: false,
  flags: { pdf: false, saved: false, done: false },
  attempts: 0,
  lockedUntil: 0,
};

const USERS = [{
  nome_usuario: 'mariana',
  nome: 'Mariana Duarte',
  email: 'mariana@temperodamari.com.br',
  senha: 'Comida123!',
  pergunta: 'pet',
  resposta: 'Thor',
  criado_em: '15/08/2026',
}];

const LISTAS = {
  mariana: [{ id: 101, nome: 'Compras da semana passada', criado_em: '11/09/2026', categorias: [1],
    itens: [{ pid: 1, qtd: 2 }, { pid: 6, qtd: 4 }, { pid: 8, qtd: 3 }] }],
};
let listSeq = 200;

// sessão efêmera: sessionStorage (RF07/UC01)
function persistEph() {
  try {
    sessionStorage.setItem(STORAGE_KEYS.EPHEMERAL, JSON.stringify({ lista: state.lista, categorias: state.categorias }));
  } catch (e) {}
}
function loadEph() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEYS.EPHEMERAL);
    if (!raw) return;
    const d = JSON.parse(raw);
    if (d.lista && d.lista.itens && d.lista.itens.length) {
      state.lista = d.lista;
      state.categorias = d.categorias || [];
      setTimeout(() => showToast('Lista efêmera recuperada da sessão: “' + state.lista.nome + '” (' + state.lista.itens.length + ' itens).', 'ok'), 600);
    }
  } catch (e) {}
}

// ============================================================
// CARREGAMENTO DE DADOS MESTRES VIA API (remove hardcodes)
// RF12/UC03 — categorias | RF13/UC04 — fornecedores
// ============================================================
async function carregarCategorias() {
  try {
    const cats = await ApiClient.listarCategorias();
    if (cats && cats.length) {
      state.categoriasDisponiveis = cats.map(c => ({ id: c.id, nome: c.nome, ic: '📂' }));
      showToast(`Categorias carregadas do servidor (${cats.length}).`, 'ok');
    }
  } catch (e) {
    // Fallback para hardcode se a API estiver indisponível
  }
}

async function carregarFornecedores(categoriaIds = []) {
  try {
    const frns = await ApiClient.listarFornecedores(categoriaIds);
    if (frns && frns.length) {
      state.fornecedoresDisponiveis = frns.map(f => ({
        id: f.id,
        nome: f.nome,
        cnpj: f.cnpj,
        cats: (f.categorias || []).map(c => c.id),
      }));
      showToast(`Fornecedores carregados do servidor (${frns.length}).`, 'ok');
    }
  } catch (e) {
    // Fallback para hardcode se a API estiver indisponível
  }
}

// ============================================================
// REGRAS DE COMPARAÇÃO (RF15/RF16) — espelho do backend
// ============================================================
function calcularResultado() {
  const itens = state.lista.itens;
  const rows = state.fornecedores.map((fid) => {
    const f = FORNECEDORES.find(x => x.id === fid);
    const disp = itens.filter(i => temOferta(fid, i.pid));
    const aus = itens.filter(i => !temOferta(fid, i.pid));
    const cobertura = disp.length / itens.length;
    const total = disp.reduce((s, i) => s + preco(fid, i.pid) * i.qtd, 0);
    return { fid, nome: f.nome, cnpj: f.cnpj, cobertura, nDisp: disp.length, ausentes: aus, total, parcial: aus.length > 0 };
  });
  const winner = rows.slice().sort((a, b) => b.cobertura - a.cobertura || a.total - b.total)[0]; // monografia: maior cobertura; empate → menor total
  const display = rows.slice().sort((a, b) => a.total - b.total); // RF15: ordem por preço ASC
  state.resultado = {
    rows: display,
    winner,
    minTotal: Math.min(...rows.map(r => r.total)),
    maxTotal: Math.max(...rows.map(r => r.total)),
  };
}
function coberturaDe(fid) {
  const it = state.lista.itens;
  if (!it.length) return 0;
  return it.filter(i => temOferta(fid, i.pid)).length / it.length;
}
function fornecedoresElegiveis() {
  const base = state.fornecedoresDisponiveis.length ? state.fornecedoresDisponiveis : FORNECEDORES;
  return base.filter(f => f.cats.some(c => state.categorias.includes(c)));
}

function totalCategorias() {
  return state.categoriasDisponiveis.length ? state.categoriasDisponiveis.length : CATEGORIAS.length;
}

function nomeCategoria(id) {
  const cat = (state.categoriasDisponiveis.length ? state.categoriasDisponiveis : CATEGORIAS).find(c => c.id === id);
  return cat ? cat.nome : '';
}

// ============================================================
// API CLIENT (adaptado: token em memória, auth tardia)
// ============================================================
class ApiClient {
  static async request(endpoint, options = {}) {
    const token = state.user ? 'mem-token' : null;
    const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
    if (token) headers['Authorization'] = 'Bearer ' + token;

    const response = await fetch(API_BASE + endpoint, {
      ...options,
      headers,
      credentials: 'include',
    });

    if (response.status === 401) {
      state.user = null;
      showToast('Sessão expirada. Entre novamente.', 'warn');
      render();
      throw new Error('Sessão expirada');
    }

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.detail || 'Erro ' + response.status);
    }
    return data;
  }

  static login(credentials) {
    return this.request('/auth/login', { method: 'POST', body: JSON.stringify(credentials) });
  }
  static cadastrar(data) {
    return this.request('/auth/cadastrar', { method: 'POST', body: JSON.stringify(data) });
  }
  static logout() {
    return this.request('/auth/logout', { method: 'POST' });
  }
  static getPerfil() {
    return this.request('/auth/perfil');
  }
  static atualizarPerfil(data) {
    return this.request('/auth/perfil', { method: 'PUT', body: JSON.stringify(data) });
  }
  static salvarLista(data) {
    return this.request('/listas', { method: 'POST', body: JSON.stringify(data) });
  }
  static listarListas(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request('/listas?' + query);
  }
  static buscarLista(id) {
    return this.request('/listas/' + id);
  }
  static atualizarLista(id, data) {
    return this.request('/listas/' + id, { method: 'PUT', body: JSON.stringify(data) });
  }
  static excluirLista(id, confirmacaoNome) {
    return this.request('/listas/' + id + '?confirmacao_nome=' + encodeURIComponent(confirmacaoNome), { method: 'DELETE' });
  }
  static promoverEfemera(data) {
    return this.request('/listas/promover-efemera', { method: 'POST', body: JSON.stringify(data) });
  }
  static listarCategorias() {
    return this.request('/catalogo/categorias');
  }
  static listarFornecedores(categorias = []) {
    const query = categorias.length ? '?categorias=' + categorias.join(',') : '';
    return this.request('/catalogo/fornecedores' + query);
  }
  static autocompleteProdutos(q, limit = 10) {
    return this.request('/catalogo/produtos/autocomplete?q=' + encodeURIComponent(q) + '&limit=' + limit);
  }
  static calcularDisponibilidade(fornecedorId, produtoIds) {
    return this.request('/catalogo/fornecedores/' + fornecedorId + '/disponibilidade?produtos=' + produtoIds.join(','));
  }
  static calcularOrcamento(data) {
    return this.request('/comparacao/calcular', { method: 'POST', body: JSON.stringify(data) });
  }
  static calcularOrcamentoEfemera(data) {
    return this.request('/comparacao/calcular-efemera', { method: 'POST', body: JSON.stringify(data) });
  }
  static exportarPDF(listaId) {
    return fetch(API_BASE + '/export/pdf?lista_id=' + listaId, {
      method: 'POST',
      headers: { 'Authorization': 'Bearer mem-token' },
      credentials: 'include',
    }).then((r) => {
      if (!r.ok) throw new Error('Erro ao gerar PDF');
      return r.blob();
    });
  }
  static exportarPDFVencedora(data) {
    return fetch(API_BASE + '/export/pdf/vencedora', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer mem-token' },
      credentials: 'include',
      body: JSON.stringify(data),
    }).then((r) => {
      if (!r.ok) throw new Error('Erro ao gerar PDF da lista vencedora');
      return r.blob();
    });
  }
}
// ============================================================
// PERSONA / JORNADA
// ============================================================
const JOURNEY = [
  { t: 'Mariana descobre o COBECO', d: 'Dona do restaurante “Tempero da Mari”: precisa cotar a compra da semana em vários mercados sem perder a manhã. Clique em “Criar minha lista”.' },
  { t: 'Pré-filtro por categorias (UC03)', d: 'Ela marca “Mercado” — só fornecedores relevantes aparecem depois (RF12). Mínimo 1 categoria.' },
  { t: 'Monta a lista (UC01/UC02)', d: 'Nome da lista + 6 produtos do catálogo com quantidades (RF07). Tudo em memória, sem cadastro obrigatório. Dica: use “⚡ Preencher demo”.' },
  { t: 'Escolhe os fornecedores (UC04/UC05)', d: 'Marca os 3 mercados elegíveis (2–10, RF13). O slider filtra por disponibilidade mínima (RF14).' },
  { t: 'Compara orçamentos (UC06/UC07)', d: 'Tabela flat: cobertura, itens ausentes e total por fornecedor. A melhor oferta é destacada (RF15/RF16).' },
  { t: 'Abre a lista vencedora', d: 'Vencedor = maior cobertura; empate → menor total. Itens precificados pelo fornecedor campeão.' },
  { t: 'Exporta o PDF (UC08/RF17)', d: 'O PDF contém a LISTA VENCEDORA com itens precificados + total consolidado — nunca a “lista de listas”.' },
  { t: 'Salva na conta (UC14/UC17)', d: 'Só agora a autenticação é exigida (RF08): modal de login + promoção da lista efêmera. Demo: mariana / Comida123!' },
  { t: 'Confere Minhas Listas (UC15)', d: 'Lista persistida no “banco” simulado: busca, ordenação e ações (RF09–RF11). Jornada concluída! 🎉' },
];
function journeyIndex() {
  if (state.flags.done) return 8;
  if (state.flags.saved) return 8;
  if (state.flags.pdf) return 7;
  switch (state.view) {
    case 'home': return 0;
    case 'categorias': return 1;
    case 'lista': return 2;
    case 'fornecedores': return 3;
    case 'resultados': return 4;
    case 'vencedora': return 5;
    case 'dashboard': return 8;
    default: return state.flags.pdf ? 7 : 0;
  }
}
function renderJourney() {
}

// ============================================================
// NAVEGAÇÃO E STEPPER
// ============================================================
function navHTML() {
  const v = state.view;
  const logged = !!state.user;
  return `<a class="logo" href="#" data-action="nav-home"><span class="mark">🛒</span>
    <span>COBECO<small>Cotação de Bens de Consumo · v3.2</small></span></a>
  <nav class="main" aria-label="Navegação principal">
    <a href="#" class="${v === 'home' ? 'on' : ''}" data-action="nav-home">Início</a>
    <a href="#" class="${['categorias', 'lista', 'fornecedores', 'resultados', 'vencedora'].includes(v) ? 'on' : ''}" data-action="nav-nova">Nova lista</a>
    ${logged ? `<a href="#" class="${v === 'dashboard' ? 'on' : ''}" data-action="nav-listas">Minhas listas</a>
    <a href="#" class="${v === 'perfil' ? 'on' : ''}" data-action="nav-perfil">Perfil</a>` : ''}
  </nav>
  <div class="auth-zone">${logged
    ? `<span class="userchip">🟢 ${esc(state.user.nome_usuario)} · sessão ativa</span>
      <button class="btn btn-ghost btn-sm" data-action="sair">Sair</button>`
    : `<button class="btn btn-ghost btn-sm" data-action="page-login">Entrar</button>
      <button class="btn btn-pri btn-sm" data-action="page-cadastro">Criar conta</button>`}
  </div>`;
}

function stepperHTML(step) {
  const steps = [
    ['1', 'Categorias', 'categorias'],
    ['2', 'Lista', 'lista'],
    ['3', 'Fornecedores', 'fornecedores'],
    ['4', 'Comparação', 'resultados'],
    ['5', 'Lista vencedora', 'vencedora'],
  ];
  return `<div class="stepper" aria-label="Progresso do fluxo">` + steps.map((s, i) => {
    const n = i + 1;
    const cls = n < step ? 'done' : n === step ? 'active' : '';
    return `${i > 0 ? `<div class="stp-bar ${n <= step ? 'done' : ''}"></div>` : ''}
     <div class="stp ${cls}" ${n < step ? `data-action="goto-step" data-step="${s[2]}" title="Voltar para ${s[1]}"` : ''}>
      <div class="dot">${n < step ? '✓' : n}</div><div class="lb">${s[1]}</div></div>`;
  }).join('') + `</div>`;
}

function go(view) {
  state.view = view;
  render();
  window.scrollTo({ top: 0 });
}

function render() {
  document.getElementById('topbar').innerHTML = navHTML();
  const M = {
    home: vHome, categorias: vCategorias, lista: vLista, fornecedores: vFornecedores,
    resultados: vResultados, vencedora: vVencedora, login: vLogin, cadastro: vCadastro,
    recuperar: vRecuperar, dashboard: vDashboard, perfil: vPerfil,
  };
  const viewFn = M[state.view] || vHome;
  try {
    document.getElementById('main').innerHTML = viewFn();
  } catch(e) {
    document.getElementById('main').innerHTML = '<div style="color:red">ERRO: ' + e.message + '</div>';
  }
}

// ============================================================
// VIEWS
// ============================================================

function vHome() {
  return `<div class="container page">
  <section class="hero">
   <div><span class="tag">Comparador inteligente · MVP v3.2</span>
    <h1>Compras mais inteligentes,<br>economia de verdade.</h1>
    <p>Crie sua lista, filtre fornecedores por categoria, compare preço e disponibilidade em uma única tela — e exporte a lista vencedora em PDF. Sem cadastro obrigatório.</p>
    <div class="cta-row">
     <button class="btn btn-white btn-lg" data-action="nav-nova" data-primary>Criar minha lista →</button>
     <button class="btn btn-outlinew btn-lg" data-action="page-login">${state.user ? 'Minhas listas' : 'Entrar na minha conta'}</button>
    </div></div>
   <div class="mini-compare" aria-hidden="true">
    <h4>Comparação da sua lista · 6 produtos · 3 fornecedores</h4>
    <div class="mini-row"><span>🏆 Carrefour · 100% disponível</span><b>${BRL(158.47)}</b></div>
    <div class="mini-row"><span>Pão de Açúcar · 100% disponível</span><b>${BRL(173.80)}</b></div>
    <div class="mini-row"><span>Extra · 83% disponível ⚠ 1 ausente</span><b>${BRL(118.75)}</b></div>
    <div class="mini-foot"><span>Melhor oferta = maior cobertura</span><span>desempate: menor total</span></div>
   </div>
  </section>
  <section class="value-cards">
   <div class="card vcard"><div class="ic">🏷️</div><h3>Pré-filtro por categorias</h3><p>Escolha entre 11 categorias macro (Mercado, Vestuário, Eletrodomésticos…) para ver apenas fornecedores relevantes (RF12).</p></div>
   <div class="card vcard"><div class="ic">📊</div><h3>Comparação clara</h3><p>Tabela flat por fornecedor: preço total, % de cobertura e itens ausentes. A melhor oferta é destacada (RF15/RF16).</p></div>
   <div class="card vcard"><div class="ic">📄</div><h3>PDF da lista vencedora</h3><p>Exporte a lista do fornecedor campeão com itens precificados e total consolidado (RF17). Funciona sem login.</p></div>
  </section>
  <section class="card card-pad mt"><div class="row-between mb"><h2 style="font-size:18px">Como funciona</h2><span class="muted small">Fluxo principal · visitante percorre tudo sem autenticação</span></div>
   <div class="howto">
    <div class="how"><div class="n">1</div><b>Categorias</b><span>Pré-filtro</span></div>
    <div class="how"><div class="n">2</div><b>Lista</b><span>Produtos + qtd</span></div>
    <div class="how"><div class="n">3</div><b>Fornecedores</b><span>Seleção 2–10</span></div>
    <div class="how"><div class="n">4</div><b>Comparar</b><span>Tabela flat</span></div>
    <div class="how"><div class="n">5</div><b>Exportar</b><span>PDF / Imprimir</span></div>
   </div></section>
  <section class="persona-strip"><span class="av">👩‍🍳</span>
   <div style="flex:1"><b>Conheça Mariana Duarte, 34 — dona do restaurante “Tempero da Mari” (Taquaritinga/SP)</b>
   <p>Toda semana ela compra insumos para ~40 refeições em 3 mercados diferentes. Sem o COBECO: planilha, telefone e risco de escolher o “mais barato” incompleto. Acompanhe a jornada dela no painel ao lado →</p></div>
   <button class="btn btn-pri" data-action="nav-nova">Iniciar jornada →</button>
  </section>
 </div>`;
}

function vCategorias() {
  return `<div class="container page">
  <div class="page-head"><span class="kicker">Passo 1 de 5 · Pré-filtro</span>
   <h1>Selecione as categorias</h1>
   <p>Escolha uma ou mais categorias macro para filtrar os fornecedores. Mínimo: 1 categoria (RF12). A seleção fica apenas em memória (transitória).</p></div>
  ${stepperHTML(1)}
  <div class="card card-pad">
   <div class="toolbar">
    <span class="count-chip ${state.categorias.length ? 'ok' : ''}" id="cat-count">${state.categorias.length} categoria(s) selecionada(s) · ${totalCategorias()}</span>
    <div><button class="btn btn-ghost btn-sm" data-action="cat-all">Selecionar todas</button>
    <button class="btn btn-ghost btn-sm" data-action="cat-none">Limpar</button></div>
   </div>
   <div class="cat-grid" role="group" aria-label="Categorias macro">
     ${(state.categoriasDisponiveis.length ? state.categoriasDisponiveis : CATEGORIAS).map(c => `<label class="cat-card ${state.categorias.includes(c.id) ? 'sel' : ''}" data-catcard="${c.id}">
       <input type="checkbox" class="cat-cb" value="${c.id}" ${state.categorias.includes(c.id) ? 'checked' : ''}>
       <span class="ci">${c.ic}</span><span class="cn">${c.nome}</span></label>`).join('')}
   </div>
   <div class="tip">ℹ️ <b>Como funciona:</b> os fornecedores exibidos na próxima etapa pertencem às categorias selecionadas. Ex.: “Mercado” + “Eletrodomésticos” → Carrefour, Extra, Pão de Açúcar, Magazine Luiza, Casas Bahia…</div>
   <div class="row-between mt">
    <button class="btn btn-ghost" data-action="nav-home">← Voltar</button>
    <div>
     <button class="btn btn-pri btn-lg" id="btn-to-lista" data-action="to-lista" data-primary ${state.categorias.length ? '' : 'disabled'}>Continuar para a lista →</button>
     ${state.categorias.length ? '' : `<div class="hint-disabled">⚠️ Selecione ao menos 1 categoria para continuar.</div>`}
    </div>
   </div>
  </div></div>`;
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
    <div class="row-between mb"><span class="mode-chip ${logado ? 'mode-db' : 'mode-eph'}">${logado ? '🔒 CONTA: ' + esc(state.user.nome_usuario) : '⚠ MODO EFÊMERO (visitante)'}</span>
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
  </div></div>`;
}

function itensTableHTML() {
  if (!state.lista.itens.length) return `<div class="empty"><div class="big">🧺</div>Nenhum produto adicionado. Use a busca acima.</div>`;
  return `<table class="tbl"><thead><tr><th>Produto</th><th style="width:130px">Qtd.</th><th style="width:80px">Un.</th><th style="width:44px"></th></tr></thead><tbody>
   ${state.lista.itens.map((i, ix) => {
    const p = PRODUTOS.find(x => x.id === i.pid);
    return `<tr>
     <td><b>${esc(p.nome)}</b></td>
     <td><span class="qty"><button data-action="dec" data-ix="${ix}" aria-label="Diminuir">−</button>
      <input type="text" inputmode="numeric" value="${i.qtd}" data-qtdix="${ix}" aria-label="Quantidade">
      <button data-action="inc" data-ix="${ix}" aria-label="Aumentar">+</button></span></td>
     <td class="muted">${p.un}</td>
     <td><button class="icon-del" data-action="del-item" data-ix="${ix}" title="Remover item" aria-label="Remover ${esc(p.nome)}">✕</button></td></tr>`;
   }).join('')}
  </tbody></table>`;
}

function refreshListaUI() {
  document.getElementById('itens-box').innerHTML = itensTableHTML();
  const un = state.lista.itens.reduce((s, i) => s + i.qtd, 0);
  document.getElementById('r-prod').textContent = state.lista.itens.length;
  document.getElementById('r-un').textContent = un;
  const b = document.getElementById('btn-to-forn');
  if (b) {
    b.disabled = !state.lista.itens.length;
    const h = b.nextElementSibling;
    if (h && h.classList.contains('hint-disabled')) h.style.display = state.lista.itens.length ? 'none' : 'flex';
  }
}

function vFornecedores() {
  return `<div class="container page">
  <div class="page-head"><span class="kicker">Passo 3 de 5 · Fornecedores</span>
   <h1>Escolha os fornecedores</h1>
   <p>Selecione de <b>2 ou mais</b> fornecedores (RF13). Apenas fornecedores das categorias escolhidas (${state.categorias.map(nomeCategoria).join(', ')}) são exibidos. O % indica a cobertura da sua lista.</p></div>
  ${stepperHTML(3)}
  <div class="card card-pad slider-box">
   <div class="sl-head"><label for="slider-disp"><b>Filtro de disponibilidade (UC05)</b> — mostrar apenas fornecedores com cobertura mínima da lista</label>
    <output id="slider-out">${state.filtroDisp}%</output></div>
   <input type="range" id="slider-disp" min="0" max="100" step="5" value="${state.filtroDisp}" aria-label="Disponibilidade mínima">
   <div class="sl-scale"><span>0% (todos)</span><span>50%</span><span>100%</span></div>
  </div>
  <div class="card card-pad">
   <div class="toolbar">
    <span class="count-chip ${state.fornecedores.length >= 2 ? 'ok' : ''}" id="forn-count">${state.fornecedores.length} selecionado(s) · mín 2</span>
    <div><button class="btn btn-ghost btn-sm" data-action="forn-all">Selecionar todos</button>
    <button class="btn btn-ghost btn-sm" data-action="forn-clear">Limpar</button></div>
   </div>
   <div id="forn-grid" class="forn-grid">${fornCardsHTML()}</div>
   <div class="row-between mt">
    <button class="btn btn-ghost" data-action="goto-step" data-step="lista">← Voltar à lista</button>
    <div><button class="btn btn-pri btn-lg" id="btn-calc" data-action="calcular" data-primary ${state.fornecedores.length >= 2 ? '' : 'disabled'}>Calcular orçamento →</button>
    ${state.fornecedores.length >= 2 ? '' : `<div class="hint-disabled">⚠️ Selecione ao menos 2 fornecedores.</div>`}</div>
   </div>
  </div></div>`;
}

function fornCardsHTML() {
  const eleg = fornecedoresElegiveis();
  if (!eleg.length) return `<div class="empty" style="grid-column:1/-1"><div class="big">🔎</div>Nenhum fornecedor disponível nas categorias selecionadas.<br>Tente incluir outras categorias.</div>`;
  return eleg.map(f => {
    const cov = Math.round(coberturaDe(f.id) * 100);
    const passa = cov >= state.filtroDisp;
    const sel = state.fornecedores.includes(f.id);
    const cls = cov >= 80 ? 'cov-hi' : cov >= 40 ? 'cov-md' : 'cov-lo';
    return `<label class="forn-card ${sel ? 'sel' : ''} ${passa ? '' : 'off'}" data-forncard="${f.id}">
     <div class="forn-cb-row"><input type="checkbox" class="forn-cb" value="${f.id}" ${sel ? 'checked' : ''} ${passa ? '' : 'disabled'}>
     <div style="flex:1"><div class="forn-top"><b>${f.nome}</b>
       <span class="cov-badge ${cls}" title="Itens da sua lista disponíveis neste fornecedor">${cov}% da lista</span></div>
      <div class="forn-cats">${(f.categorias || f.cats).filter(c => state.categorias.includes(typeof c === 'number' ? c : c.id)).map(c => `<span class="mini-tag">${typeof c === 'number' ? nomeCategoria(c) : c.nome}</span>`).join('')}</div>
     ${cov === 0 ? `<div class="small muted" style="margin-top:6px">⚠ Não possui itens da sua lista</div>` : ''}
    </div></div></label>`;
  }).join('');
}

function refreshFornecedores() {
  document.getElementById('forn-grid').innerHTML = fornCardsHTML();
  const c = document.getElementById('forn-count');
  c.textContent = `${state.fornecedores.length} selecionado(s) · mín 2`;
  c.classList.toggle('ok', state.fornecedores.length >= 2);
  const b = document.getElementById('btn-calc');
  b.disabled = state.fornecedores.length < 2;
  const h = b.nextElementSibling;
  if (h && h.classList.contains('hint-disabled')) h.style.display = state.fornecedores.length >= 2 ? 'none' : 'flex';
}

function vResultados() {
  if (!state.resultado) return vFornecedores();
  const R = state.resultado;
  const W = R.winner;
  const avg = Math.round(R.rows.reduce((s, r) => s + r.cobertura, 0) / R.rows.length * 100);
  const eco = R.maxTotal - W.total;
  return `<div class="container page">
  <div class="page-head"><span class="kicker">Passo 4 de 5 · Resultados</span>
   <h1>Comparação de preços</h1>
   <p>Lista “${esc(state.lista.nome || '(sem nome)')}” · ${state.lista.itens.length} itens · ${R.rows.length} fornecedores. Ordenado pelo menor total (RF15); melhor oferta destacada (RF16).</p></div>
  ${stepperHTML(4)}
  <div class="kpis">
   <div class="card kpi win"><div class="k">🏆 Melhor oferta</div><div class="v">${W.nome}</div><div class="s">${BRL(W.total)} · ${Math.round(W.cobertura * 100)}% da lista</div></div>
   <div class="card kpi"><div class="k">💰 Menor preço</div><div class="v">${BRL(R.minTotal)}</div><div class="s">pode ter itens ausentes</div></div>
   <div class="card kpi"><div class="k">📊 Economia potencial</div><div class="v">${BRL(eco > 0 ? eco : 0)}</div><div class="s">vs. maior total cotado</div></div>
   <div class="card kpi"><div class="k">Disponibilidade média</div><div class="v">${avg}%</div><div class="s">${R.rows.length} fornecedores comparados</div></div>
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
     <td>${r.parcial ? `<span class="badge b-warn" title="${r.ausentes.map(a => esc(PRODUTOS.find(p => p.id === a.pid).nome)).join('; ')}">⚠ ${r.ausentes.length} item(ns)</span>` : `<span class="muted">—</span>`}</td>
     <td style="text-align:right;font-weight:800;font-variant-numeric:tabular-nums">${BRL(r.total)}${r.parcial ? ` <span class="badge b-mut" title="Total parcial: considera apenas itens disponíveis">parcial</span>` : ''}</td></tr>`;
   }).join('')}
   </tbody></table>
  </div>
  <div class="warn-banner"><span>⚠️</span><span><b>Atenção:</b> o menor preço pode não incluir todos os itens da sua lista. A melhor oferta considera a <b>maior cobertura</b>; em caso de empate, vence o <b>menor total</b> — verifique a coluna “Ausentes” (passe o mouse no badge).</span></div>
  <div class="row-between">
   <button class="btn btn-ghost" data-action="goto-step" data-step="fornecedores">← Editar fornecedores</button>
   <div style="display:flex;gap:10px;flex-wrap:wrap">
    <button class="btn btn-ghost" data-action="print-a4">🖨️ Imprimir (A4)</button>
    <button class="btn btn-ghost" data-action="export-pdf">📄 Exportar PDF</button>
    <button class="btn btn-ok btn-lg" data-action="ver-vencedora" data-primary>🏆 Ver lista vencedora →</button>
   </div>
  </div>
  <p class="rule-note">Regra da melhor oferta (monografia/RF16): maior percentual de cobertura da lista; empate → menor custo total. A comparação não é persistida (YAGNI).</p>
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
  <div class="card" style="overflow:auto"><table class="tbl">
   <thead><tr><th>Produto</th><th>Un.</th><th style="width:90px">Qtd.</th><th style="text-align:right">Preço unitário</th><th style="text-align:right">Subtotal</th></tr></thead><tbody>
   ${state.lista.itens.map(i => {
    const p = PRODUTOS.find(x => x.id === i.pid);
    const tem = temOferta(W.fid, i.pid);
    return tem ? `<tr><td><b>${esc(p.nome)}</b></td><td class="muted">${p.un}</td><td>${i.qtd}</td>
     <td style="text-align:right">${BRL(preco(W.fid, i.pid))}</td>
     <td style="text-align:right;font-weight:700">${BRL(preco(W.fid, i.pid) * i.qtd)}</td></tr>`
     : `<tr style="opacity:.55"><td>${esc(p.nome)}</td><td class="muted">${p.un}</td><td>${i.qtd}</td>
     <td colspan="2" style="text-align:right"><span class="badge b-warn">⚠ Indisponível neste fornecedor</span></td></tr>`;
   }).join('')}
   </tbody></table></div>
  <div class="total-box"><span class="tl">Total consolidado da compra (${state.lista.itens.length} itens)</span><span class="tv">${BRL(W.total)}</span></div>
  <div class="export-note">ℹ️ O arquivo <b>lista_${stamp()}.pdf</b> (A4, gerado no servidor via ReportLab) contém exatamente este documento: itens, preços unitários, subtotais e total consolidado.</div>
  <div class="row-between mt">
   <button class="btn btn-ghost" data-action="goto-step" data-step="resultados">← Voltar aos resultados</button>
   <div style="display:flex;gap:10px;flex-wrap:wrap">
    <button class="btn btn-ghost btn-lg" data-action="print-a4">🖨️ Imprimir A4</button>
    <button class="btn btn-pri btn-lg" data-action="export-pdf" data-primary>⬇ Exportar PDF — lista_${stamp()}.pdf</button>
   </div>
  </div></div>`;
}

function vLogin() {
  const locked = Date.now() < state.lockedUntil;
  return `<div class="container page"><div class="auth-wrap"><div class="card auth-card">
   <span class="step-pill">Autenticação</span><h1>Entre na sua conta</h1>
   <p class="sub">Acesse suas listas salvas. A autenticação só é exigida para <b>salvar</b> listas.</p>
   <div class="demo-hint"><span>🎬 <b>Demo:</b> mariana / Comida123!</span><button class="linklike" data-action="demo-login-fill" type="button">preencher</button></div>
   <form id="form-login" novalidate>
    <div class="field" id="fl-u"><label>Nome de usuário</label><input type="text" id="l-user" autocomplete="username"><div class="err-msg">Informe o nome de usuário.</div></div>
    <div class="field" id="fl-p"><label>Senha</label><input type="password" id="l-pass" autocomplete="current-password"><div class="err-msg">Informe a senha.</div></div>
    ${locked ? `<div class="warn-banner"><span>🔒</span><span>Muitas tentativas. Acesso bloqueado por 15 minutos (RF02, anti-força bruta).<br><button class="linklike" type="button" data-action="reset-lock">(modo demo: zerar bloqueio)</button></span></div>` : ''}
    <button class="btn btn-pri btn-lg" style="width:100%" ${locked ? 'disabled' : ''} data-primary>Entrar</button>
    <p class="small muted mt" style="text-align:center">6 tentativas consecutivas → bloqueio de 15 min · mensagem sempre genérica (segurança)</p>
   </form>
   <div class="auth-foot"><a href="#" data-action="page-recuperar">Esqueci minha senha</a> · Ainda não possui conta? <a href="#" data-action="page-cadastro">Criar conta</a></div>
  </div></div></div>`;
}

function vCadastro() {
  return `<div class="container page"><div class="auth-wrap" style="max-width:520px"><div class="card auth-card">
   <span class="step-pill">Cadastro · UC09</span><h1>Criar conta</h1><p class="sub">Preencha seus dados para salvar listas. Leva menos de um minuto.</p>
   <form id="form-cad" novalidate>
    <div class="field" id="fc-u"><label>Username <span class="req">*</span></label><input type="text" id="c-user" placeholder="3–30 caracteres alfanuméricos, único"><div class="err-msg" id="fc-u-e">Username inválido (3–30 alfanuméricos) ou já cadastrado.</div></div>
    <div class="field" id="fc-n"><label>Nome completo <span class="req">*</span></label><input type="text" id="c-nome" placeholder="2–100 caracteres"><div class="err-msg">Nome deve ter de 2 a 100 caracteres.</div></div>
    <div class="field" id="fc-e"><label>Email <span class="req">*</span></label><input type="email" id="c-email" placeholder="voce@exemplo.com"><div class="err-msg">Email inválido ou já cadastrado.</div></div>
    <div class="field" id="fc-s"><label>Senha <span class="req">*</span></label><input type="password" id="c-senha" placeholder="Mín. 8 · 1 maiúscula · 1 número · 1 especial"><div class="err-msg">Senha fraca: mín. 8, 1 maiúscula, 1 número e 1 caractere especial.</div></div>
    <div class="field" id="fc-c"><label>Confirmar senha <span class="req">*</span></label><input type="password" id="c-conf"><div class="err-msg">As senhas não coincidem.</div></div>
    <div class="field" id="fc-p"><label>Pergunta de segurança <span class="req">*</span></label>
     <select id="c-perg"><option value="">Selecione…</option>${Object.entries(PERGUNTAS).map(([k, v]) => `<option value="${k}">${v}</option>`).join('')}</select>
     <div class="err-msg">Selecione uma pergunta (usada na recuperação de senha).</div></div>
    <div class="field" id="fc-r"><label>Resposta <span class="req">*</span></label><input type="text" id="c-resp" placeholder="mín. 3 caracteres"><div class="err-msg">Resposta muito curta (mín. 3).</div></div>
    <button class="btn btn-pri btn-lg" style="width:100%" data-primary>Criar conta</button>
    <p class="small muted mt" style="text-align:center">Validação inline · mensagens genéricas para duplicados · senha com hash bcrypt (simulado)</p>
   </form>
   <div class="auth-foot">Já tenho conta · <a href="#" data-action="page-login">Entrar</a></div>
  </div></div></div>`;
}

function vRecuperar() {
  let body = '';
  if (state.recStep === 1) {
    body = `<form id="form-rec1" novalidate><div class="field" id="fr-u"><label>Nome de usuário</label>
     <input type="text" id="r-user" placeholder="seu username"><div class="err-msg">Usuário não encontrado.</div></div>
   <button class="btn btn-pri btn-lg" style="width:100%" data-primary>Continuar →</button></form>
   <p class="small muted mt">⚠️ Máx. 3 tentativas por etapa · 3 solicitações/hora (rate limit). Modo dev: token também seria logado no stdout (RECOVERY_MODE=log).</p>`;
  } else if (state.recStep === 2) {
    const u = USERS.find(x => x.nome_usuario === state.recUser);
    body = `<p class="small muted mb">Responda para gerar o token de reset (uso único · 15 min):</p>
   <form id="form-rec2" novalidate><div class="field" id="fr-r"><label>${PERGUNTAS[u.pergunta]}</label>
    <input type="text" id="r-resp" placeholder="sua resposta (demo: Thor)"><div class="err-msg">Resposta incorreta. Tentativas restantes serão limitadas (3).</div></div>
   <button class="btn btn-pri btn-lg" style="width:100%" data-primary>Validar resposta →</button></form>`;
  } else {
    body = `<p class="small muted mb">Token válido ✔ (uso único, 15 min). Defina a nova senha — regras do RF01 e diferente da atual.</p>
   <form id="form-rec3" novalidate>
    <div class="field" id="fr-s"><label>Nova senha</label><input type="password" id="r-senha"><div class="err-msg">Senha fraca ou igual à anterior.</div></div>
    <div class="field" id="fr-c"><label>Confirmar nova senha</label><input type="password" id="r-conf"><div class="err-msg">As senhas não coincidem.</div></div>
   <button class="btn btn-pri btn-lg" style="width:100%" data-primary>Redefinir senha</button></form>`;
  }
  return `<div class="container page"><div class="auth-wrap"><div class="card auth-card">
   <span class="step-pill">Recuperação · passo ${state.recStep} de 3</span>
   <h1>Recuperar senha</h1><p class="sub">Via pergunta de segurança (contexto acadêmico, sem envio de email).</p>
   ${body}<div class="auth-foot"><a href="#" data-action="page-login">← Voltar ao login</a></div>
  </div></div></div>`;
}

function vDashboard() {
  if (!state.user) return vLogin();
  const q = (state.dashQ || '').toLowerCase();
  let lists = (LISTAS[state.user.nome_usuario] || []).slice().sort((a, b) => b.criado_em.localeCompare(a.criado_em));
  if (q) lists = lists.filter(l => norm(l.nome).includes(norm(q)));
  return `<div class="container page">
  <div class="page-head row-between"><div><span class="kicker">Área logada · UC15</span><h1>Minhas listas</h1>
   <p>Listas salvas de <b>${esc(state.user.nome_usuario)}</b>, ordenadas da mais recente para a mais antiga · paginação de 20 (demo com ${lists.length}).</p></div>
   <button class="btn btn-pri" data-action="nav-nova">+ Nova lista</button></div>
  <div class="card card-pad">
   <div class="toolbar"><input type="text" id="dash-q" value="${esc(state.dashQ || '')}" placeholder="🔍 Buscar por nome…" style="padding:10px 13px;border:1px solid #cbd5e1;border-radius:10px;min-width:300px" aria-label="Buscar listas por nome">
    <span class="count-chip">${lists.length} lista(s)</span></div>
   ${lists.length ? `<table class="tbl"><thead><tr><th>Nome</th><th>Itens</th><th>Categorias</th><th>Criada em</th><th style="width:190px">Ações</th></tr></thead><tbody>
   ${lists.map(l => `<tr><td><b>${esc(l.nome)}</b></td><td>${l.itens.length} produtos</td>
   <td>${(l.categorias || []).map(c => `<span class="mini-tag">${nomeCategoria(c)}</span>`).join(' ') || '—'}</td>
   <td class="muted">${l.criado_em}</td>
   <td><button class="btn btn-ghost btn-sm" data-action="editar-lista" data-id="${l.id}">✏️ Editar</button>
   <button class="btn btn-danger btn-sm" data-action="excluir-lista" data-id="${l.id}">🗑 Excluir</button></td></tr>`).join('')}
   </tbody></table><p class="small muted mt">Mostrando ${lists.length} de ${lists.length} listas · « 1 » · exclusão é lógica (soft delete)</p>`
   : `<div class="empty"><div class="big">🗂️</div>Você ainda não tem listas salvas.<br><br><button class="btn btn-pri" data-action="nav-nova">Criar lista</button></div>`}
  </div></div>`;
}

function vPerfil() {
  if (!state.user) return vLogin();
  const u = USERS.find(x => x.nome_usuario === state.user.nome_usuario);
  const edit = state.perfilEdit;
  return `<div class="container page"><div class="auth-wrap" style="max-width:560px">
  <div class="page-head"><span class="kicker">Perfil · UC18/UC16</span><h1>Meu perfil</h1>
   <p>Visualize seus dados e edite nome, email ou senha — qualquer alteração exige a senha atual (RF06).</p></div>
  <div class="card card-pad">
   <div class="res-line"><span>Username</span><b>🔒 ${esc(u.nome_usuario)} <span class="badge b-mut">read-only</span></b></div>
   <div class="res-line"><span>Nome completo</span><b>${esc(u.nome)}</b></div>
   <div class="res-line"><span>Email</span><b>${esc(u.email)}</b></div>
   <div class="res-line"><span>Conta criada em</span><b>${u.criado_em}</b></div>
   ${!edit ? `<div class="row-between mt">
     <button class="btn btn-ghost" data-action="sair">🚪 Logout</button>
     <button class="btn btn-pri" data-action="perfil-editar" data-primary>✏️ Editar perfil</button></div>`
     : `<form id="form-perfil" novalidate class="mt">
     <div class="field" id="fp-n"><label>Novo nome</label><input type="text" id="p-nome" value="${esc(u.nome)}"><div class="err-msg">Nome deve ter de 2 a 100 caracteres.</div></div>
     <div class="field" id="fp-e"><label>Novo email</label><input type="email" id="p-email" value="${esc(u.email)}"><div class="err-msg">Email inválido ou já cadastrado.</div></div>
     <div class="field" id="fp-a"><label>Senha atual <span class="req">*</span></label><input type="password" id="p-atual"><div class="err-msg">Senha atual incorreta.</div></div>
     <div class="field" id="fp-s"><label>Nova senha (opcional)</label><input type="password" id="p-nova" placeholder="deixe em branco para manter"><div class="err-msg">Senha fraca ou igual à atual.</div></div>
     <div class="row-between"><button class="btn btn-ghost" type="button" data-action="perfil-cancelar">Cancelar</button>
     <button class="btn btn-ok" data-primary>💾 Salvar alterações</button></div>
     <p class="small muted mt">Transação ACID simulada: email/nome/senha atualizam juntos ou nada muda.</p></form>`}
  </div></div></div>`;
}

// ============================================================
// PDF / IMPRESSÃO — sempre a LISTA VENCEDORA (premissa)
// ============================================================
function sheetHTML() {
  const W = state.resultado.winner;
  const rows = state.lista.itens.map(i => {
    const p = PRODUTOS.find(x => x.id === i.pid);
    const tem = temOferta(W.fid, i.pid);
    return { nome: p.nome, un: p.un, qtd: i.qtd, preco: tem ? preco(W.fid, i.pid) : null };
  });
  return `<div class="a4-sheet" id="a4-sheet">
   <div class="a4-head"><div class="brand">🛒 COBECO<small>COTAÇÃO DE BENS DE CONSUMO</small></div>
    <div class="doc"><b>LISTA VENCEDORA — COTAÇÃO</b><br>Arquivo: lista_${stamp()}.pdf<br>Formato A4 · ${hoje()}</div></div>
   <div class="a4-meta">
    <span>Lista: <b>${esc(state.lista.nome || '(sem nome)')}</b></span>
    <span>Fornecedor vencedor: <b>${W.nome}</b> (CNPJ ${W.cnpj})</span>
    <span>Itens: <b>${state.lista.itens.length}</b> · Unidades: <b>${rows.reduce((s, r) => s + r.qtd, 0)}</b></span>
    <span>Cobertura da lista: <b>${Math.round(W.cobertura * 100)}%</b>${W.parcial ? ' (total parcial)' : ''}</span>
   </div>
   <table class="a4-tbl"><thead><tr><th style="width:34px">#</th><th>Produto</th><th style="width:50px">Un.</th>
    <th class="num" style="width:60px">Qtd.</th><th class="num" style="width:110px">Preço unitário</th><th class="num" style="width:110px">Subtotal</th></tr></thead>
   <tbody>${rows.map((r, ix) => `<tr><td>${ix + 1}</td><td>${esc(r.nome)}</td><td>${r.un}</td><td class="num">${r.qtd}</td>
    <td class="num">${r.preco != null ? BRL(r.preco) : '—'}</td><td class="num">${r.preco != null ? BRL(r.preco * r.qtd) : '⚠ indisponível'}</td></tr>`).join('')}</tbody></table>
   <div class="a4-total"><span><b>TOTAL CONSOLIDADO DA COMPRA</b> — preços de ${W.nome}</span><b>${BRL(W.total)}</b></div>
   ${W.parcial ? `<p style="font-size:11px;color:#7a4a00;margin-bottom:10px">⚠ Itens indisponíveis no vencedor: ${W.ausentes.map(a => esc(PRODUTOS.find(p => p.id === a.pid).nome)).join('; ')}. Total calculado sobre itens disponíveis.</p>` : ''}
   <div class="a4-foot"><span>Gerado por COBECO · protótipo MVP v3.2 · PDF server-side simulado (ReportLab)</span><span>Documento de cotação — sem valor fiscal</span></div>
  </div>`;
}

function exportPDF() {
  if (!state.resultado) { showToast('Compare os preços antes de exportar.', 'warn'); return; }
  showToast('⏳ Gerando PDF no servidor (ReportLab)…', 'info');
  setTimeout(() => {
    state.flags.pdf = true;
    openModal(`<button class="x" data-action="close-modal" aria-label="Fechar">✕</button>
     <h3>📄 PDF gerado com sucesso</h3>
     <p class="small muted mb">Pré-visualização de <b>lista_${stamp()}.pdf</b> — lista vencedora precificada + total consolidado (RF17/RNF11: &lt;5s).</p>
     <div style="max-height:56vh;overflow:auto;border:1px solid var(--line);border-radius:8px;background:#eef0f3;padding:16px">${sheetHTML()}</div>
     <div class="modal-actions">
      <button class="btn btn-ghost" data-action="close-modal">Fechar</button>
      <button class="btn btn-pri" data-action="baixar-pdf" data-primary>⬇ Baixar lista_${stamp()}.pdf</button>
     </div>`);
  }, 900);
}

function printWinner() {
  if (!state.resultado) { showToast('Compare os preços antes de imprimir.', 'warn'); return; }
  document.getElementById('print-area').innerHTML = sheetHTML();
  setTimeout(() => window.print(), 60);
}

// ============================================================
// REGRAS DE LOGIN / LISTA (core)
// ============================================================
function loginCore(user, pass, after) {
  if (Date.now() < state.lockedUntil) { showToast('🔒 Conta bloqueada temporariamente (6 tentativas).', 'err'); return false; }
  const u = USERS.find(x => x.nome_usuario === user);
  if (!u || u.senha !== pass) {
    state.attempts++;
    if (state.attempts >= 6) {
      state.lockedUntil = Date.now() + 15 * 60 * 1000;
      state.attempts = 0;
      showToast('🔒 6 tentativas falhas — bloqueio de 15 minutos (RF02).', 'err');
    } else {
      showToast('Credenciais inválidas. (mensagem genérica · tentativa ' + state.attempts + '/6)', 'err');
    }
    return false;
  }
  state.attempts = 0;
  state.user = u;
  showToast('✅ Bem-vinda(o), ' + u.nome.split(' ')[0] + '! Sessão ativa — token em memória, cookie httpOnly simulado.', 'ok');
  return true;
}

function afterLogin() {
  const hasEph = state.lista.itens.length > 0;
  if (hasEph) {
    openModal(`<button class="x" data-action="close-modal" aria-label="Fechar">✕</button>
     <h3>💾 Salvar lista efêmera?</h3>
     <p class="small" style="margin:8px 0">Você tem uma lista ativa na sessão: <b>“${esc(state.lista.nome || '(sem nome)')}” · ${state.lista.itens.length} itens</b>. Deseja salvá-la permanentemente na sua conta? (UC17 — Promover Lista Efêmera)</p>
     <p class="small warn-banner" style="margin:10px 0"><span>⚠️</span><span>Se escolher “Não”, a lista permanece em memória e será perdida ao fechar a aba.</span></p>
     <div class="modal-actions"><button class="btn btn-ghost" data-action="promote-no">Não, manter efêmera</button>
     <button class="btn btn-ok" data-action="promote-yes" data-primary>Sim, salvar lista</button></div>`);
  } else {
    go('dashboard');
  }
}

function salvarListaCore() {
  if (!state.lista.nome.trim()) { showToast('Informe um nome para a lista.', 'err'); return false; }
  if (!state.lista.itens.length) { showToast('A lista precisa de ao menos 1 item.', 'err'); return false; }
  if (!state.categorias.length) { showToast('Selecione ao menos 1 categoria antes de salvar (UC03).', 'err'); return false; }
  const db = LISTAS[state.user.nome_usuario] = LISTAS[state.user.nome_usuario] || [];
  const snap = { nome: state.lista.nome, itens: state.lista.itens.map(i => ({ ...i })), categorias: [...state.categorias] };
  if (state.listaEditId) {
    const l = db.find(x => x.id === state.listaEditId);
    Object.assign(l, snap);
    showToast('✅ Lista atualizada (transação ACID simulada).', 'ok');
  } else {
    db.push({ id: ++listSeq, criado_em: hoje(), ...snap });
    state.listaEditId = listSeq;
    state.flags.saved = true;
    showToast('✅ Lista salva com sucesso! Persistida no banco (simulado).', 'ok');
  }
  persistEph();
  return true;
}

// ============================================================
// AÇÕES — clique delegado
// ============================================================
document.addEventListener('click', (e) => {
  const el = e.target.closest('[data-action]');
  if (!el) return;
  const a = el.dataset.action;
  e.preventDefault();
  switch (a) {
    case 'overlay-click': if (e.target === el) closeModal(); break;
    case 'close-modal': closeModal(); break;
    case 'nav-home': go('home'); break;
    case 'nav-nova': go(state.categorias.length ? 'lista' : 'categorias'); break;
    case 'nav-listas': state.user ? go('dashboard') : (go('login'), showToast('Entre para acessar suas listas.', 'warn')); break;
    case 'nav-perfil': state.user ? go('perfil') : go('login'); break;
    case 'page-login': go('login'); break;
    case 'page-cadastro': go('cadastro'); break;
    case 'page-recuperar': state.recStep = 1; go('recuperar'); break;
    case 'sair': {
      const hadEph = state.lista.itens.length > 0;
      state.user = null;
      state.perfilEdit = false;
      showToast('Sessão encerrada. ' + (hadEph ? 'Rascunho da aba preservado (RF03).' : ''), 'info');
      go('home');
      break;
    }
    case 'cat-all': state.categorias = (state.categoriasDisponiveis.length ? state.categoriasDisponiveis : CATEGORIAS).map(c => c.id); render(); break;
    case 'cat-none': state.categorias = []; render(); break;
    case 'to-lista': if (!state.categorias.length) { showToast('Selecione ao menos 1 categoria.', 'err'); break; } go('lista'); break;
    case 'goto-step': {
      const s = el.dataset.step;
      if (s === 'lista' && !state.categorias.length) { go('categorias'); break; }
      if ((s === 'fornecedores' || s === 'resultados') && !state.lista.itens.length) { go('lista'); break; }
      if (s === 'resultados' && !state.resultado) { go('fornecedores'); break; }
      go(s);
      break;
    }
    case 'demo-lista':
      state.lista = { nome: 'Compras do Mês', itens: [{ pid: 1, qtd: 2 }, { pid: 2, qtd: 2 }, { pid: 3, qtd: 3 }, { pid: 4, qtd: 2 }, { pid: 5, qtd: 2 }, { pid: 6, qtd: 6 }] };
      if (!state.categorias.length) state.categorias = [1];
      persistEph(); render();
      showToast('⚡ Lista da Mariana preenchida: 6 produtos de mercado.', 'ok');
      break;
    case 'inc':
    case 'dec': {
      const ix = +el.dataset.ix;
      const it = state.lista.itens[ix];
      it.qtd = Math.min(9999, Math.max(1, it.qtd + (a === 'inc' ? 1 : -1)));
      persistEph(); refreshListaUI();
      break;
    }
    case 'del-item': state.lista.itens.splice(+el.dataset.ix, 1); persistEph(); refreshListaUI(); break;
    case 'to-fornecedores':
      if (!state.lista.itens.length) { showToast('Adicione ao menos 1 item.', 'err'); break; }
      carregarFornecedores(state.categorias).then(() => go('fornecedores'));
      break;
    case 'forn-all':
      state.fornecedores = fornecedoresElegiveis().filter(f => coberturaDe(f.id) * 100 >= state.filtroDisp).map(f => f.id);
      refreshFornecedores();
      break;
    case 'forn-clear': state.fornecedores = []; refreshFornecedores(); break;
    case 'calcular': {
      if (state.fornecedores.length < 2) { showToast('Selecione ao menos 2 fornecedores.', 'err'); break; }
      const btn = el;
      btn.disabled = true;
      btn.textContent = '⏳ Calculando orçamento…';
      setTimeout(() => {
        calcularResultado();
        go('resultados');
        showToast('✅ Comparação concluída em ~180ms (meta p95 <500ms). Melhor oferta: ' + state.resultado.winner.nome + '.', 'ok');
      }, 700);
      break;
    }
    case 'ver-vencedora': go('vencedora'); break;
    case 'export-pdf': exportPDF(); break;
    case 'baixar-pdf':
      document.getElementById('print-area').innerHTML = sheetHTML();
      setTimeout(() => window.print(), 80);
      break;
    case 'print-a4': printWinner(); break;
    case 'salvar-lista': {
      if (!state.user) {
        openModal(`<button class="x" data-action="close-modal" aria-label="Fechar">✕</button>
         <h3>🔒 Entre para salvar sua lista</h3>
         <p class="small muted mb">Sua lista permanece aqui enquanto você entra (RF08 — rascunho preservado).</p>
         <div class="demo-hint"><span>🎬 <b>Demo:</b> mariana / Comida123!</span><button class="linklike" type="button" data-action="demo-modal-fill">preencher</button></div>
         <form id="form-login-modal" novalidate>
          <div class="field"><label>Nome de usuário</label><input type="text" id="m-user"></div>
          <div class="field"><label>Senha</label><input type="password" id="m-pass"></div>
          <button class="btn btn-pri btn-lg" style="width:100%" data-primary>Entrar e salvar</button></form>
         <div class="auth-foot"><a href="#" data-action="close-modal">Cancelar</a> · <a href="#" data-action="goto-cad-from-modal">Criar conta</a></div>`);
      } else {
        if (salvarListaCore()) go('dashboard');
      }
      break;
    }
    case 'goto-cad-from-modal': closeModal(); go('cadastro'); break;
    case 'demo-modal-fill': document.getElementById('m-user').value = 'mariana'; document.getElementById('m-pass').value = 'Comida123!'; break;
    case 'demo-login-fill': document.getElementById('l-user').value = 'mariana'; document.getElementById('l-pass').value = 'Comida123!'; break;
    case 'reset-lock': state.lockedUntil = 0; render(); break;
    case 'promote-yes': closeModal(); if (salvarListaCore()) go('dashboard'); break;
    case 'promote-no': closeModal(); showToast('Lista mantida em memória (efêmera).', 'info'); go('dashboard'); break;
    case 'editar-lista': {
      const l = (LISTAS[state.user.nome_usuario] || []).find(x => x.id === +el.dataset.id);
      if (!l) break;
      state.listaEditId = l.id;
      state.lista = { nome: l.nome, itens: l.itens.map(i => ({ ...i })) };
      state.categorias = [...(l.categorias || [])];
      persistEph(); go('lista');
      showToast('✏️ Editando “' + l.nome + '”. Ao salvar, os dados serão atualizados (UC13).', 'info');
      break;
    }
    case 'excluir-lista': {
      const id = +el.dataset.id;
      const l = (LISTAS[state.user.nome_usuario] || []).find(x => x.id === id);
      openModal(`<button class="x" data-action="close-modal" aria-label="Fechar">✕</button>
       <h3>🗑️ Confirmar exclusão</h3>
       <p class="small" style="margin:8px 0">Esta ação não pode ser desfeita (na demo). Digite o nome da lista para confirmar (RF11):</p>
       <div class="field"><label>“${esc(l.nome)}”</label><input type="text" id="excl-nome" placeholder="digite o nome exato" autocomplete="off"></div>
       <div class="modal-actions"><button class="btn btn-ghost" data-action="close-modal">Cancelar</button>
       <button class="btn btn-danger" id="btn-excl" data-action="confirmar-exclusao" data-id="${id}" disabled>Excluir permanentemente</button></div>`);
      break;
    }
    case 'confirmar-exclusao': {
      const id = +el.dataset.id;
      const db = LISTAS[state.user.nome_usuario] || [];
      const ix = db.findIndex(x => x.id === id);
      if (ix >= 0) db.splice(ix, 1);
      closeModal();
      showToast('🗑 Lista excluída (soft delete simulado — deletado_em).', 'ok');
      render();
      break;
    }
    case 'perfil-editar': state.perfilEdit = true; render(); break;
    case 'perfil-cancelar': state.perfilEdit = false; render(); break;
    case 'journey-toggle': document.getElementById('journey').classList.toggle('min'); break;
    case 'journey-next': {
      const p = document.querySelector('[data-primary]');
      if (p) {
        p.scrollIntoView({ behavior: 'smooth', block: 'center' });
        p.classList.remove('pulse');
        void p.offsetWidth;
        p.classList.add('pulse');
        p.focus({ preventScroll: true });
      } else {
        showToast('Nenhuma ação disponível neste ponto.', 'info');
      }
      break;
    }
  }
});

// ============================================================
// SUBMITS
// ============================================================
document.addEventListener('submit', (e) => {
  const id = e.target.id;
  if (!id) return;
  e.preventDefault();
  const val = (x) => { const n = document.getElementById(x); return n ? n.value.trim() : ''; };
  const bad = (fid) => { const f = document.getElementById(fid); if (f) f.classList.add('invalid'); };
  const clear = (fid) => { const f = document.getElementById(fid); if (f) f.classList.remove('invalid'); };

  if (id === 'form-login' || id === 'form-login-modal') {
    const u = id === 'form-login' ? val('l-user') : val('m-user');
    const p = id === 'form-login' ? val('l-pass') : val('m-pass');
    if (!u || !p) { showToast('Informe usuário e senha.', 'err'); return; }
    if (loginCore(u, p)) { closeModal(); afterLogin(); } else if (id === 'form-login') render();
  }
  else if (id === 'form-cad') {
    let ok = true;
    ['fc-u', 'fc-n', 'fc-e', 'fc-s', 'fc-c', 'fc-p', 'fc-r'].forEach(clear);
    const u = val('c-user'), n = val('c-nome'), em = val('c-email'), s = val('c-senha'), c = val('c-conf'), pg = val('c-perg'), r = val('c-resp');
    if (!/^[a-zA-Z0-9]{3,30}$/.test(u) || USERS.some(x => x.nome_usuario === u)) { bad('fc-u'); ok = false; }
    if (n.length < 2 || n.length > 100) { bad('fc-n'); ok = false; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em) || USERS.some(x => x.email === em)) { bad('fc-e'); ok = false; }
    if (!(s.length >= 8 && /[A-Z]/.test(s) && /\d/.test(s) && /[^A-Za-z0-9]/.test(s))) { bad('fc-s'); ok = false; }
    if (c !== s) { bad('fc-c'); ok = false; }
    if (!pg) { bad('fc-p'); ok = false; }
    if (r.length < 3) { bad('fc-r'); ok = false; }
    if (!ok) { showToast('Verifique os campos destacados.', 'err'); return; }
    USERS.push({ nome_usuario: u, nome: n, email: em, senha: s, pergunta: pg, resposta: r, criado_em: hoje() });
    showToast('✅ Conta criada com sucesso! Agora faça login. (201 Created)', 'ok');
    go('login');
  }
  else if (id === 'form-rec1') {
    const u = val('r-user'); clear('fr-u');
    if (!USERS.some(x => x.nome_usuario === u)) { bad('fr-u'); showToast('Usuário não encontrado.', 'err'); return; }
    state.recUser = u; state.recStep = 2; render();
  }
  else if (id === 'form-rec2') {
    const u = USERS.find(x => x.nome_usuario === state.recUser); clear('fr-r');
    if (val('r-resp').toLowerCase() !== u.resposta.toLowerCase()) { bad('fr-r'); showToast('Resposta incorreta (máx. 3 tentativas).', 'err'); return; }
    showToast('✔ Resposta validada. Token de reset emitido (uso único · 15 min).', 'ok'); state.recStep = 3; render();
  }
  else if (id === 'form-rec3') {
    const u = USERS.find(x => x.nome_usuario === state.recUser); let ok = true; ['fr-s', 'fr-c'].forEach(clear);
    const s = val('r-senha'), c = val('r-conf');
    if (!(s.length >= 8 && /[A-Z]/.test(s) && /\d/.test(s) && /[^A-Za-z0-9]/.test(s)) || s === u.senha) { bad('fr-s'); ok = false; }
    if (c !== s) { bad('fc-c'); ok = false; }
    if (!ok) { showToast('Verifique a nova senha.', 'err'); return; }
    u.senha = s; state.recStep = 1; showToast('✅ Senha redefinida! Faça login com a nova senha.', 'ok'); go('login');
  }
  else if (id === 'form-perfil') {
    const u = USERS.find(x => x.nome_usuario === state.user.nome_usuario); let ok = true; ['fp-n', 'fp-e', 'fp-a', 'fp-s'].forEach(clear);
    const n = val('p-nome'), em = val('p-email'), at = val('p-atual'), nv = val('p-nova');
    if (n.length < 2 || n.length > 100) { bad('fp-n'); ok = false; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em) || USERS.some(x => x.email === em && x.nome_usuario !== u.nome_usuario)) { bad('fp-e'); ok = false; }
    if (at !== u.senha) { bad('fp-a'); ok = false; }
    if (nv && (!(nv.length >= 8 && /[A-Z]/.test(nv) && /\d/.test(nv) && /[^A-Za-z0-9]/.test(nv)) || nv === u.senha)) { bad('fp-s'); ok = false; }
    if (!ok) { showToast('Verifique os campos destacados.', 'err'); return; }
    u.nome = n; u.email = em; if (nv) u.senha = nv; state.perfilEdit = false;
    showToast('✅ Perfil atualizado (transação ACID simulada).', 'ok'); render();
  }
});

// ============================================================
// INPUTS
// ============================================================
document.addEventListener('input', (e) => {
  const t = e.target;
  if (t.id === 'nome-lista') {
    state.lista.nome = t.value; persistEph();
    const c = document.getElementById('nome-count');
    if (c) c.textContent = t.value.length;
  }
  else if (t.id === 'busca') { state.busca = t.value; updateSugestoes(); }
  else if (t.id === 'slider-disp') {
    state.filtroDisp = +t.value;
    document.getElementById('slider-out').textContent = t.value + '%';
    const removed = state.fornecedores.filter(f => coberturaDe(f.id) * 100 < state.filtroDisp);
    if (removed.length) {
      state.fornecedores = state.fornecedores.filter(f => coberturaDe(f.id) * 100 >= state.filtroDisp);
      showToast(removed.length + ' fornecedor(es) removido(s) da seleção pelo filtro (UC05).', 'warn');
    }
    refreshFornecedores();
  }
  else if (t.id === 'dash-q') {
    state.dashQ = t.value; render();
    const i = document.getElementById('dash-q');
    i.focus(); i.setSelectionRange(i.value.length, i.value.length);
  }
  else if (t.id === 'excl-nome') {
    const id = +document.getElementById('btn-excl').dataset.id;
    const l = (LISTAS[state.user.nome_usuario] || []).find(x => x.id === id);
    document.getElementById('btn-excl').disabled = t.value.trim() !== l.nome;
  }
  else if (t.dataset.qtdix !== undefined) {
    const ix = +t.dataset.qtdix;
    let v = parseInt(t.value, 10);
    if (isNaN(v)) v = 1;
    v = Math.min(9999, Math.max(1, v));
    state.lista.itens[ix].qtd = v; persistEph();
  }
});

document.addEventListener('change', (e) => {
  const t = e.target;
  if (t.classList.contains('cat-cb')) {
    const id = +t.value;
    state.categorias = state.categorias.includes(id) ? state.categorias.filter(x => x !== id) : [...state.categorias, id];
    const card = t.closest('[data-catcard]');
    if (card) card.classList.toggle('sel', state.categorias.includes(id));
    const c = document.getElementById('cat-count');
    c.textContent = state.categorias.length + ' categoria(s) selecionada(s) · 11 disponíveis';
    c.classList.toggle('ok', state.categorias.length > 0);
    const b = document.getElementById('btn-to-lista');
    b.disabled = !state.categorias.length;
    const h = b.nextElementSibling;
    if (h && h.classList.contains('hint-disabled')) h.style.display = state.categorias.length ? 'none' : 'flex';
  }
  else if (t.classList.contains('forn-cb')) {
    const id = +t.value;
    if (state.fornecedores.length >= 10 && !state.fornecedores.includes(id)) { showToast('Máximo de 10 fornecedores (RF13).', 'warn'); t.checked = false; return; }
    state.fornecedores = state.fornecedores.includes(id) ? state.fornecedores.filter(x => x !== id) : [...state.fornecedores, id];
    const card = t.closest('[data-forncard]');
    if (card) card.classList.toggle('sel', state.fornecedores.includes(id));
    refreshFornecedores();
  }
});

let sugTimer = null;
function updateSugestoes() {
  const box = document.getElementById('sug-box');
  if (!box) return;
  const q = norm(state.busca);
  if (q.length < 2) { box.innerHTML = ''; return; }
  box.innerHTML = '<div class=sug><div class=sug-empty>🔎 Buscando no catálogo…</div></div>';
  clearTimeout(sugTimer);
  sugTimer = setTimeout(() => {
    const hits = PRODUTOS.filter(p => norm(p.nome).includes(q)).slice(0, 6);
    box.innerHTML = hits.length ? '<div class=sug role=listbox>' + hits.map(p =>
      '<div class=sug-item data-action-add= + p.id +  role=option><span>' + esc(p.nome) + '</span><span class=un>por unidade de venda: ' + p.un + '</span></div>').join('') + '</div>'
      : '<div class=sug><div class=sug-empty>Nenhum produto encontrado — tente outro termo.</div></div>';
  }, 280);
}

document.addEventListener('click', (e) => {
  const s = e.target.closest('[data-action-add]');
  if (!s) return;
  const pid = +s.dataset.actionAdd;
  const ex = state.lista.itens.find(i => i.pid === pid);
  if (ex) ex.qtd = Math.min(9999, ex.qtd + 1); else state.lista.itens.push({ pid, qtd: 1 });
  state.busca = '';
  const b = document.getElementById('busca');
  if (b) b.value = '';
  document.getElementById('sug-box').innerHTML = '';
  persistEph(); refreshListaUI();
  const p = PRODUTOS.find(x => x.id === pid);
  showToast('➕ ' + p.nome + ' adicionado' + (ex ? ' (quantidade somada)' : '') + '.', 'ok');
});

// ============================================================
// BOOT
// Inicializar após DOM carregado: carrega categorias da API e render
document.addEventListener("DOMContentLoaded", async () => {
  try {
    await carregarCategorias();
    render();
  } catch(e) {
    document.getElementById("main").innerHTML = '<div style="color:red">Erro: ' + e.message + '</div>';
  }
});