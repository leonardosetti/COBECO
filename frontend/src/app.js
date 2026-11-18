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

const showToast = (msg, type = 'info') => {
  const box = document.createElement('div');
  box.className = 'toast ' + (type === 'ok' ? 'ok' : type === 'err' ? 'err' : 'warn');
  box.innerHTML = `<span>${esc(msg)}</span>`;
  document.getElementById('toasts').appendChild(box);
  setTimeout(() => {
    box.style.opacity = '0';
    box.style.transition = 'opacity .4s';
    setTimeout(() => box.remove(), 420);
  }, 4200);
};

const openModal = (html) => {
  const container = document.getElementById('modal-root');
  container.innerHTML = `<div class="overlay"><div class="modal">${html}</div></div>`;
  container.classList.remove('hidden');
  container.setAttribute('aria-hidden', 'false');
};

const closeModal = () => {
  const container = document.getElementById('modal-root');
  container.innerHTML = '';
  container.classList.add('hidden');
  container.setAttribute('aria-hidden', 'true');
};

const state = {
  view: 'home',
  user: null,
  categorias: [],
  categoriasDisponiveis: [],
  fornecedoresDisponiveis: [],
  produtos: [],
  lista: { nome: '', itens: [] },
  fornecedores: [],
  filtroDisp: 0,
  resultado: null,
  busca: '',
};

class ApiClient {
  static async request(endpoint, options = {}) {
    const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
    const response = await fetch(API_BASE + endpoint, { ...options, headers, credentials: 'include' });
    if (response.status === 401) { showToast('Sessão expirada.', 'warn'); return null; }
    const data = await response.json().catch(() => ({}));
    if (!response.ok) { throw new Error(data.detail || 'Erro ' + response.status); }
    return data;
  }
  static listarCategorias() { return this.request('/catalogo/categorias'); }
  static listarProdutos() { return this.request('/catalogo/produtos'); }
  static listarFornecedores(categorias = []) {
    const q = categorias.length ? '?categorias=' + categorias.join(',') : '';
    return this.request('/catalogo/fornecedores' + q);
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
    if (cats && cats.length) state.categoriasDisponiveis = cats.map(c => ({ id: c.id, nome: c.nome, ic: '📂' }));
  } catch (e) { }
}

async function carregarProdutos() {
  try {
    const prods = await ApiClient.listarProdutos();
    if (prods && prods.length) state.produtos = prods.map(p => ({ id: p.id, nome: p.nome, un: p.unidade || 'un' }));
  } catch (e) { }
}

async function carregarFornecedores(categoriaIds = []) {
  try {
    const frns = await ApiClient.listarFornecedores(categoriaIds);
    if (frns && frns.length) {
      state.fornecedoresDisponiveis = frns.map(f => ({ id: f.id, nome: f.nome, cnpj: f.cnpj, cats: (f.categorias || []).map(c => c.id) }));
    }
  } catch (e) { }
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
    showToast('Erro ao calcular orçamento.', 'err');
    state.resultado = null;
  }
}

function fornecedoresElegiveis() {
  const base = state.fornecedoresDisponiveis.length ? state.fornecedoresDisponiveis : [];
  return base.filter(f => f.cats.some(c => state.categorias.includes(c)));
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
  try { document.getElementById('main').innerHTML = viewFn(); }
  catch(e) { document.getElementById('main').innerHTML = '<div style="color:red">Erro: ' + e.message + '</div>'; }
}

function navHTML() {
  const logged = !!state.user;
  return `<header class="top"><div class="container top-in" id="topbar">
    <div class="logo"><div class="mark">🛒</div><div><b>COBECO</b><small>Cotação de Bens de Consumo · Wireframe v3.3</small></div></div>
    <nav class="main">
      <a href="#" class="${state.view === 'home' ? 'on' : ''}" data-action="nav-home">Início</a>
      <a href="#" class="${['categorias','lista','fornecedores','resultados','vencedora'].includes(state.view) ? 'on' : ''}" data-action="nav-nova">Nova lista</a>
      ${logged ? `<a href="#" class="${state.view === 'dashboard' ? 'on' : ''}" data-action="nav-dash">Minhas listas</a>
      <a href="#" class="${state.view === 'perfil' ? 'on' : ''}" data-action="nav-perfil">Perfil</a>` : ''}
    </nav>
    <div class="auth-zone">${logged ? `<span class="userchip">🟢 ${esc(state.user.nome_usuario)}</span><button class="btn btn-ghost btn-sm" data-action="sair">Sair</button>` : `<button class="btn btn-ghost btn-sm" data-action="page-login">Entrar</button><button class="btn btn-pri btn-sm" data-action="page-cadastro">Criar conta</button>`}</div>
  </div></header>`;
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
  return `<main class="page">
    <div class="hero"><div><div class="tag">Wireframe v3.3 · MVP</div>
      <h1>Comparação de preços para listas de compras</h1>
      <p>Wireframe sem dados mockados. Consome a API real para categorias, fornecedores e cálculo de orçamento.</p>
      <div class="cta-row"><button class="btn btn-pri btn-lg" data-action="nav-nova">Criar lista</button>
      <button class="btn btn-ghost btn-sm" data-action="page-login">${state.user ? 'Minhas listas' : 'Entrar'}</button></div></div></div>
    <div class="value-cards">
      <div class="card card-pad"><div class="ic">📂</div><h3>Pré-filtro por categorias (RF12)</h3><p>Selecione categorias para filtrar fornecedores.</p></div>
      <div class="card card-pad"><div class="ic">📊</div><h3>Comparação (RF15/RF16)</h3><p>Melhor oferta = maior cobertura; empate → menor total.</p></div>
      <div class="card card-pad"><div class="ic">📄</div><h3>PDF da vencedora (RF17)</h3><p>Exporta apenas a lista do fornecedor campeão.</p></div>
    </div>
  </main>`;
}

function vCategorias() {
  return `<main class="page">
    <div class="page-head"><span class="kicker">Passo 1 de 5 · Pré-filtro</span><h1>Selecione as categorias</h1><p>Mínimo 1 categoria (RF12).</p></div>
    ${stepperHTML(1)}
    <div class="card card-pad">
      <div class="toolbar"><span class="count-chip ${state.categorias.length ? 'ok' : ''}">${state.categorias.length} selecionada(s) · ${totalCategorias()} disponíveis</span>
        <div><button class="btn btn-ghost btn-sm" data-action="cat-all">Todas</button><button class="btn btn-ghost btn-sm" data-action="cat-none">Limpar</button></div></div>
      <div class="cat-grid">${(state.categoriasDisponiveis.length ? state.categoriasDisponiveis : []).map(c => `<label class="cat-card ${state.categorias.includes(c.id) ? 'sel' : ''}" data-catcard="${c.id}"><input type="checkbox" class="cat-cb" value="${c.id}" ${state.categorias.includes(c.id) ? 'checked' : ''}><span class="ci">${c.ic}</span><span class="cn">${esc(c.nome)}</span></label>`).join('')}</div>
      <div class="row-between"><button class="btn btn-ghost" data-action="nav-home">← Voltar</button><div><button class="btn btn-pri btn-lg" id="btn-to-lista" data-action="to-lista" ${state.categorias.length ? '' : 'disabled'}>Lista →</button></div></div>
    </div>
  </main>`;
}

function vLista() {
  const un = state.lista.itens.reduce((s, i) => s + i.qtd, 0);
  return `<main class="page">
    <div class="page-head"><span class="kicker">Passo 2 de 5 · Lista</span><h1>Lista de compras</h1><p>Adicione produtos e quantidades.</p></div>
    ${stepperHTML(2)}
    <div class="card card-pad">
      <div class="row-between"><span class="mode-chip mode-eph">⚠ Wireframe (sem login)</span><button class="btn btn-ghost btn-sm" data-action="demo-lista">Demo: lista rápida</button></div>
      <div class="field"><label>Nome da lista <span class="req">*</span></label><input type="text" id="nome-lista" value="${esc(state.lista.nome)}" placeholder="Ex.: Compras da semana"></div>
      <div class="field searchbox"><label>Produto (autocomplete)</label><input type="text" id="busca" placeholder="Digite o produto…"><div id="sug-box"></div></div>
      <h3 style="font-size:15px;margin:8px 0 10px">Itens</h3>
      <div id="itens-box">${itensTableHTML()}</div>
    </div>
    <div class="resumo"><h3>Resumo</h3><div class="res-line"><span>Produtos</span><b>${state.lista.itens.length}</b></div><div class="res-line"><span>Unidades</span><b>${un}</b></div><div class="actions-stack"><button class="btn btn-pri btn-lg" id="btn-to-forn" data-action="to-fornecedores" ${state.lista.itens.length ? '' : 'disabled'}>Comparar →</button></div></div>
  </main>`;
}

function itensTableHTML() {
  if (!state.lista.itens.length) return `<div class="empty"><div class="big">🧺</div>Nenhum item.</div>`;
  return `<table class="tbl"><thead><tr><th>Produto</th><th style="width:100px">Qtd</th><th style="width:80px">Un</th><th style="width:56px"></th></tr></thead><tbody>
   ${state.lista.itens.map((i, ix) => `<tr><td><b>${esc(nomeProduto(i.pid))}</b></td><td><span class="qty"><button data-action="dec" data-ix="${ix}">−</button><input type="text" value="${i.qtd}" data-qtdix="${ix}"><button data-action="inc" data-ix="${ix}">+</button></span></td><td class="muted">${unidadeProduto(i.pid)}</td><td><button class="icon-del" data-action="del-item" data-ix="${ix}">✕</button></td></tr>`).join('')}
  </tbody></table>`;
}

function vFornecedores() {
  return `<main class="page">
    <div class="page-head"><span class="kicker">Passo 3 de 5 · Fornecedores</span><h1>Escolha fornecedores</h1><p>Mínimo 2 (RF13). Cobertura da lista por fornecedor.</p></div>
    ${stepperHTML(3)}
    <div class="card card-pad slider-box">
      <div class="sl-head"><label>Disponibilidade mínima (UC05)</label><output id="slider-out">${state.filtroDisp}%</output></div>
      <input type="range" id="slider-disp" min="0" max="100" step="5" value="${state.filtroDisp}">
      <div class="sl-scale"><span>0%</span><span>50%</span><span>100%</span></div>
    </div>
    <div class="card card-pad">
      <div class="toolbar"><span class="count-chip ${state.fornecedores.length >= 2 ? 'ok' : ''}">${state.fornecedores.length} selecionado(s) · mín 2</span>
        <div><button class="btn btn-ghost btn-sm" data-action="forn-all">Todos</button><button class="btn btn-ghost btn-sm" data-action="forn-clear">Limpar</button></div></div>
      <div id="forn-grid" class="forn-grid">${fornCardsHTML()}</div>
      <div class="row-between"><button class="btn btn-ghost" data-action="goto-step" data-step="lista">← Voltar</button><div><button class="btn btn-pri btn-lg" id="btn-calc" data-action="calcular" ${state.fornecedores.length >= 2 ? '' : 'disabled'}>Calcular →</button></div></div>
    </div>
  </main>`;
}

function fornCardsHTML() {
  const eleg = fornecedoresElegiveis();
  if (!eleg.length) return `<div class="empty"><div class="big">🔎</div>Nenhum fornecedor nas categorias selecionadas.</div>`;
  return eleg.map(f => {
    const cov = Math.round(coberturaDe(f.id) * 100);
    const passa = cov >= state.filtroDisp;
    const sel = state.fornecedores.includes(f.id);
    return `<label class="forn-card ${sel ? 'sel' : ''} ${passa ? '' : 'off'}" data-forncard="${f.id}">
     <div class="forn-cb-row"><input type="checkbox" class="forn-cb" value="${f.id}" ${sel ? 'checked' : ''} ${passa ? '' : 'disabled'}>
     <div style="flex:1"><div class="forn-top"><b>${esc(f.nome)}</b><span class="cov-badge ${cov >= 80 ? 'cov-hi' : cov >= 40 ? 'cov-md' : 'cov-lo'}">${cov}% da lista</span></div>
     <div class="forn-cats">${(f.cats || []).filter(c => state.categorias.includes(c)).map(c => `<span class="mini-tag">${nomeCategoria(c)}</span>`).join('')}</div>
     ${cov === 0 ? `<div class="small muted" style="margin-top:6px">Sem itens da lista</div>` : ''}
     </div></div></label>`;
  }).join('');
}

function vResultados() {
  if (!state.resultado) return vFornecedores();
  const R = state.resultado, W = R.winner;
  return `<main class="page">
    <div class="page-head"><span class="kicker">Passo 4 de 5 · Comparação</span><h1>Resultados</h1><p>Ordenado pelo menor total (RF15); melhor oferta destacada (RF16).</p></div>
    ${stepperHTML(4)}
    <div class="kpis">
      <div class="card kpi win"><div class="k">Melhor oferta</div><div class="v">${W.nome}</div><div class="s">${BRL(W.total)} · ${Math.round(W.cobertura*100)}% da lista</div></div>
      <div class="card kpi"><div class="k">Menor preço</div><div class="v">${BRL(R.minTotal)}</div><div class="s">pode ter itens ausentes</div></div>
      <div class="card kpi"><div class="k">Economia</div><div class="v">${BRL(R.maxTotal - W.total)}</div><div class="s">vs. maior total</div></div>
    </div>
    <table class="tbl"><thead><tr><th>#</th><th>Fornecedor</th><th>Cobertura</th><th>Itens</th><th>Ausentes</th><th style="text-align:right">Total</th></tr></thead><tbody>
   ${R.rows.map((r, i) => {
     const isW = r.fid === W.fid;
     return `<tr class="${isW ? 'row-win' : ''}"><td>${i+1}</td><td><b>${r.nome}</b>${isW ? ' <span class="badge b-ok">🏆 Melhor</span>' : ''}</td>
     <td><span class="cov-bar"><i style="width:${Math.round(r.cobertura*100)}%"></i></span>${Math.round(r.cobertura*100)}%</td>
     <td>${r.nDisp} de ${state.lista.itens.length}</td><td>${r.nAus}</td><td style="text-align:right">${BRL(r.total)}${r.parcial ? ' (parcial)' : ''}</td></tr>`;
   }).join('')}
   </tbody></table>
   <div class="warn-banner"><span>⚠️</span><span>Melhor oferta = maior cobertura; empate → menor total. Verifique a coluna "Ausentes".</span></div>
   <div class="row-between"><button class="btn btn-ghost" data-action="goto-step" data-step="fornecedores">← Editar fornecedores</button><div style="display:flex;gap:10px">
    <button class="btn btn-ghost" data-action="ver-vencedora" data-primary>🏆 Ver vencedora →</button></div></div>
  </main>`;
}

function vVencedora() {
  if (!state.resultado) return vResultados();
  const W = state.resultado.winner;
  return `<main class="page">
    <div class="page-head"><span class="kicker">Passo 5 de 5 · Vencedora</span><h1>Lista vencedora</h1><p>PDF exporta apenas esta lista (RF17).</p></div>
    ${stepperHTML(5)}
    <div class="win-hero"><div><span class="badge b-ok">🏆 Melhor oferta · ${Math.round(W.cobertura*100)}% da lista</span><h2>${W.nome}</h2><div class="meta">CNPJ ${W.cnpj} · ${hoje()} · “${esc(state.lista.nome || '(sem nome)')}”</div></div><div style="text-align:right"><div class="muted small">Total consolidado</div><div style="font-size:28px;font-weight:800">${BRL(W.total)}</div></div></div>
    <table class="tbl"><thead><tr><th>Produto</th><th>Un</th><th style="width:90px">Qtd</th><th style="text-align:right">Unitário</th><th style="text-align:right">Subtotal</th></tr></thead><tbody>
   ${state.lista.itens.map(i => {
     const itemWin = (W.itens || []).find(it => it.pid === i.pid);
     const p = state.produtos.find(x => x.id === i.pid) || { nome: 'Desconhecido', un: 'un' };
     if (itemWin && itemWin.disponivel) return `<tr><td>${esc(p.nome)}</td><td class="muted">${p.un}</td><td>${i.qtd}</td><td style="text-align:right">${BRL(itemWin.preco)}</td><td style="text-align:right">${BRL(itemWin.preco * i.qtd)}</td></tr>`;
     return `<tr style="opacity:.55"><td>${esc(p.nome)}</td><td class="muted">${p.un}</td><td>${i.qtd}</td><td colspan="2" style="text-align:right"><span class="badge b-warn">Indisponível</span></td></tr>`;
   }).join('')}
   </tbody></table>
   <div class="total-box"><span class="tl">Total consolidado</span><span class="tv">${BRL(W.total)}</span></div>
   <div class="row-between mt"><button class="btn btn-ghost" data-action="goto-step" data-step="resultados">← Resultados</button><div style="display:flex;gap:10px">
    <button class="btn btn-pri btn-lg" data-action="export-pdf" data-primary>⬇ Exportar PDF — lista_${stamp()}.pdf</button></div></div>
  </main>`;
}

function vLogin() {
  return `<div class="auth-wrap"><div class="card auth-card"><span class="step-pill">Login</span><h1>Entrar</h1><p class="sub">A autenticação é exigida apenas para salvar listas.</p>
    <form id="form-login" novalidate>
      <div class="field"><label>Usuário</label><input type="text" id="l-user" placeholder="usuário"></div>
      <div class="field"><label>Senha</label><input type="password" id="l-pass" placeholder="senha"></div>
      <button class="btn btn-pri btn-lg" style="width:100%" data-primary>Entrar</button>
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
      <button class="btn btn-pri btn-lg" style="width:100%" data-primary>Criar conta</button>
    </form><div class="auth-foot">Já tem conta? <button class="linklike" data-action="page-login">Entrar</button></div></div></div>`;
}

// ============================================================
// DISPATCH DE CLIQUES
// ============================================================
document.addEventListener('click', (e) => {
  const t = e.target;
  if (t.classList.contains('cat-cb')) {
    const id = +t.value;
    state.categorias = state.categorias.includes(id) ? state.categorias.filter(x => x !== id) : [...state.categorias, id];
    render();
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
    case 'nav-home': go('home'); break;
    case 'nav-nova': go('categorias'); break;
    case 'nav-dash': case 'nav-perfil': showToast('Em construção (wireframe).', 'info'); break;
    case 'page-login': go('login'); break;
    case 'page-cadastro': go('cadastro'); break;
    case 'sair': state.user = null; showToast('Saiu.', 'info'); render(); break;
    case 'cat-all': state.categorias = state.categoriasDisponiveis.map(c => c.id); render(); break;
    case 'cat-none': state.categorias = []; render(); break;
    case 'to-lista': if (!state.categorias.length) { showToast('Selecione ≥1 categoria.', 'err'); return; } go('lista'); break;
    case 'goto-step': go(el.dataset.step); break;
    case 'demo-lista': state.lista = { nome: 'Lista demo', itens: [{ pid: 1, qtd: 2 }, { pid: 2, qtd: 1 }, { pid: 3, qtd: 3 }] }; if (!state.categorias.length) state.categorias = [1]; persistEph(); render(); showToast('Lista demo carregada.', 'ok'); break;
    case 'to-fornecedores': if (!state.lista.itens.length) { showToast('Adicione ≥1 item.', 'err'); return; } carregarFornecedores(state.categorias).then(() => go('fornecedores')); break;
    case 'forn-all': state.fornecedores = fornecedoresElegiveis().filter(f => coberturaDe(f.id) * 100 >= state.filtroDisp).map(f => f.id); refreshFornecedores(); break;
    case 'forn-clear': state.fornecedores = []; refreshFornecedores(); break;
    case 'calcular': {
      if (state.fornecedores.length < 2) { showToast('Selecione ≥2 fornecedores.', 'err'); return; }
      const btn = el; btn.disabled = true; btn.textContent = 'Calculando…';
      calcularResultado().then(() => { go('resultados'); btn.disabled = false; btn.textContent = 'Calcular →'; }).catch(() => { btn.disabled = false; btn.textContent = 'Calcular →'; });
      break;
    }
    case 'ver-vencedora': go('vencedora'); break;
    case 'export-pdf': {
      if (!state.resultado) { showToast('Compare antes de exportar.', 'warn'); return; }
      showToast('Gerando PDF…', 'info');
      ApiClient.exportarPDFVencedora({ itens: state.lista.itens.map(i => ({ produto_id: i.pid, quantidade: i.qtd })), fornecedor_ids: state.fornecedores, lista_nome: state.lista.nome || 'Lista' })
        .then(blob => {
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a'); a.href = url; a.download = `lista_${stamp()}.pdf`; a.click();
          URL.revokeObjectURL(url);
          showToast('PDF baixado.', 'ok');
        }).catch(() => showToast('Erro ao gerar PDF.', 'err'));
      break;
    }
    case 'dec': case 'inc': {
      const ix = +el.dataset.ix; const it = state.lista.itens[ix];
      it.qtd = Math.min(9999, Math.max(1, it.qtd + (a === 'inc' ? 1 : -1))); persistEph(); refreshListaUI(); break;
    }
    case 'del-item': state.lista.itens.splice(+el.dataset.ix, 1); persistEph(); refreshListaUI(); break;
    case 'nome-lista': case 'busca': break;
  }
});

document.addEventListener('input', (e) => {
  const t = e.target;
  if (t.id === 'nome-lista') { state.lista.nome = t.value; persistEph(); }
  else if (t.id === 'busca') { state.busca = t.value; updateSugestoes(); }
  else if (t.id === 'slider-disp') { state.filtroDisp = +t.value; document.getElementById('slider-out').textContent = t.value + '%'; refreshFornecedores(); }
});

let sugTimer = null;
function updateSugestoes() {
  const q = state.busca;
  const box = document.getElementById('sug-box');
  clearTimeout(sugTimer);
  sugTimer = setTimeout(() => {
    if (!q.length) { box.innerHTML = ''; return; }
    const hits = state.produtos.filter(p => norm(p.nome).includes(q)).slice(0, 6);
    box.innerHTML = hits.length ? '<div class="sug">' + hits.map(p => `<div class="sug-item" data-action-add="${p.id}"><span>${esc(p.nome)}</span><span class="un">${p.un}</span></div>`).join('') + '</div>' : '<div class="sug-empty">Nenhum produto encontrado.</div>';
  }, 280);
}

document.addEventListener('click', (e) => {
  const s = e.target.closest('[data-action-add]');
  if (!s) return;
  const pid = +s.dataset.actionAdd;
  const ex = state.lista.itens.find(i => i.pid === pid);
  if (ex) ex.qtd = Math.min(9999, ex.qtd + 1); else state.lista.itens.push({ pid, qtd: 1 });
  state.busca = ''; const b = document.getElementById('busca'); if (b) b.value = ''; document.getElementById('sug-box').innerHTML = '';
  persistEph(); refreshListaUI();
  showToast('➕ ' + nomeProduto(pid) + ' adicionado.', 'ok');
});

// ============================================================
// PERSISTÊNCIA EFÊMERA
// ============================================================
function persistEph() {
  try { sessionStorage.setItem('cobeco_eph', JSON.stringify({ lista: state.lista, categorias: state.categorias })); } catch (e) { }
}
function loadEph() {
  try {
    const raw = sessionStorage.getItem('cobeco_eph');
    if (!raw) return;
    const d = JSON.parse(raw);
    if (d.lista && d.lista.itens && d.lista.itens.length) { state.lista = d.lista; state.categorias = d.categorias || []; showToast('Lista efêmera recuperada.', 'ok'); }
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
}

// ============================================================
// BOOT
// ============================================================
document.addEventListener("DOMContentLoaded", async () => {
  try {
    await carregarCategorias();
    await carregarProdutos();
    loadEph();
    render();
  } catch (e) { document.getElementById('main').innerHTML = '<div style="color:red">Erro: ' + e.message + '</div>'; }
});

window.state = state;
window.refreshFornecedores = refreshFornecedores;
window.refreshListaUI = refreshListaUI;
