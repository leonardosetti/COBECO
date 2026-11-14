---
id: doc-arch-0013-c4-components-frontend-v1.0
type: doc-arch
title: DOC ARCH — C4 Components Frontend
version: v1.0
status: ratificado
canonical: false
canonical_slug: c4-components-frontend
created: '2026-11-14'
updated: '2026-11-14'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: null
ratified_at: null
supersedes: null
superseded_by: null
trace:
  constitution: []
  req_func: []
  req_nfunc: []
  use_cases: []
  specs: []
  handoffs: []
  adrs: []
  code: []
  tests: []
domain: architecture
layer: architecture
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Diagrama de Componentes — Frontend (C4 Level 3)

**Versão:** 1.0  
**Data:** 15/09/2026  
**Autor:** Nicholas Anthony (Arquiteto) + Eduardo Passarelli (Dev Frontend)  
**Ferramenta:** Mermaid.js (Docs-as-Code)  
**Base:** ADR-001, spec-008, Constitution v2.0 (KISS, YAGNI, Desktop-first)  
**Status:** Ratificado (Gate 2 — 29/09/2026)

---

## Diagrama Mermaid — Arquitetura Modular Vanilla JS

```mermaid
C4Component
    title Diagrama de Componentes — Frontend COBECO (Vanilla JS ES6+ Modular)

    Container_Boundary(frontend_boundary, "Frontend SPA (nginx static files)") {
        Component(app_js, "app.js (Entry Point)", "Vanilla JS Module (IIFE)", "Bootstrap da SPA: roteamento hash-based, inicialização módulos, estado global, event listeners globais")
        Component(router, "Router", "JS Module", "Roteamento hash-based (#/rota): parse hash, carrega view correspondente, gerencia histórico, guards auth")
        Component(state_store, "State Store", "JS Module", "Gerenciamento estado: sessionStorage (lista_efemera, categorias_selecionadas, fornecedores_selecionados), memória (access_token, user_data), reatividade simples via CustomEvent")
        
        Component(auth_module, "Auth Module", "JS Module", "Páginas Login/Cadastro/Recuperar: forms, validação client-side, submit fetch, armazenamento access_token memória, redirect guards")
        Component(listas_module, "Listas Module", "JS Module", "Dashboard, Nova Lista, Editar Lista: CRUD UI, integração Autocomplete, sessionStorage ↔ API, modais confirmação")
        Component(autocomplete_module, "Autocomplete Module", "JS Module", "Componente reutilizável: input + dropdown, debounce 300ms, normalização NFD+lowerCase, fetch /v1/produtos/busca, seleção → callback com produto_id")
        Component(comparacao_module, "Comparação Module", "JS Module", "Pré-filtro (CategoriasChecklist, FornecedoresChecklist, SliderDisponibilidade), CalculaOrcamento (POST /v1/orcamento + loading), Resultados (TabelaResultados expansível)")
        Component(export_module, "Export Module", "JS Module", "Botão Exportar PDF → POST /v1/export/pdf (blob download), filename data, toast sdoc-arch-0006-uc-v1esso/erro")
        Component(perfil_module, "Perfil Module", "JS Module", "Visualizar Perfil (read-only cards), Editar Perfil (3 forms: Email, Nome, Senha — cada um com senha_atual), validação, toast, redirect login se refresh invalidado")
        Component(ui_components, "UI Components", "JS Module", "Biblioteca componentes reutilizáveis: Toast (sdoc-arch-0006-uc-v1esso/erro/info, auto-dismiss 3s), Skeleton (loading tabelas/cards), Modal (confirmação, promoção lista, excluir), LoadingOverlay, Badge (% disponibilidade)")
        Component(api_client, "API Client", "JS Module", "Fetch wrapper centralizado: baseURL /v1/, interceptors (Authorization Bearer access_token, refresh automático 401), error handling padronizado, retry idempotente")
        Component(utils, "Utils", "JS Module", "Funções puras: normalizar(str) NFD+lowerCase, formatCurrency(BRL), formatDate(PT-BR), debounce(fn, ms), generateId(), validateEmail(), validateRequired()")
    }

    Container(backend, "Backend API", "FastAPI", "REST /v1/* via nginx proxy (mesma origem)")

    Rel(app_js, router, "Inicializa + delega navegação")
    Rel(app_js, state_store, "Registra listeners estado")
    Rel(app_js, auth_module, "Monta se rota auth")
    Rel(app_js, listas_module, "Monta se rota listas")
    Rel(app_js, comparacao_module, "Monta se rota comparacao")
    Rel(app_js, export_module, "Disponibiliza exportar global")
    Rel(app_js, perfil_module, "Monta se rota perfil")
    Rel(app_js, ui_components, "Registra componentes globais")
    Rel(app_js, api_client, "Configura baseURL + interceptors")

    Rel(router, auth_module, "Rota /login, /cadastro, /recuperar")
    Rel(router, listas_module, "Rota /listas, /listas/nova, /listas/{id}/editar")
    Rel(router, comparacao_module, "Rota /comparacao, /resultado")
    Rel(router, perfil_module, "Rota /perfil, /perfil/editar")
    Rel(router, state_store, "Guards: rotas auth requerem access_token")

    Rel(auth_module, api_client, "POST /v1/auth/login, /register, /logout, /recover, /reset-password")
    Rel(auth_module, state_store, "Salva access_token memória, user_data, limpa no logout")
    Rel(auth_module, ui_components, "Toast sdoc-arch-0006-uc-v1esso/erro, LoadingOverlay")

    Rel(listas_module, api_client, "GET/POST/PUT/DELETE /v1/listas, /v1/listas/{id}/itens, /v1/produtos/busca")
    Rel(listas_module, autocomplete_module, "Usa componente na Nova Lista e Editar Lista")
    Rel(listas_module, state_store, "Lê/Escreve sessionStorage `cobeco_lista_efemera`")
    Rel(listas_module, ui_components, "Modal Promoção (login), Modal Excluir (confirmação nome), Toast, Skeleton")

    Rel(autocomplete_module, api_client, "GET /v1/produtos/busca?q={termo}&limit=10 (debounce 300ms)")
    Rel(autocomplete_module, utils, "normalizar(termo) NFD+lowerCase")
    Rel(autocomplete_module, ui_components, "Dropdown acessível (teclado, ARIA)")

    Rel(comparacao_module, api_client, "GET /v1/categorias, GET /v1/fornecedores?categorias=, POST /v1/orcamento")
    Rel(comparacao_module, state_store, "Lê/Escreve `cobeco_categorias_selecionadas`, `cobeco_fornecedores_selecionados`")
    Rel(comparacao_module, ui_components, "CategoriasChecklist, FornecedoresChecklist, SliderDisponibilidade, TabelaResultados, Toast, Skeleton")

    Rel(export_module, api_client, "POST /v1/export/pdf (blob response → download)")
    Rel(export_module, ui_components, "Toast download, LoadingOverlay")

    Rel(perfil_module, api_client, "GET/PUT /v1/perfil")
    Rel(perfil_module, state_store, "Limpa access_token se refresh invalidado (redirect login)")
    Rel(perfil_module, ui_components, "Toast, Modal confirmação senha, LoadingOverlay")

    Rel(api_client, backend, "HTTP/JSON via nginx proxy (mesma origem /v1/*)")
    Rel(api_client, state_store, "Intercepta 401 → tenta refresh automático → se falha limpa estado + redirect login")

    UpdateLayoutConfig($c4ShapeInRow="4", $c4BoundaryInRow="1")
```

---

## Descrição dos Módulos (Vanilla JS ES6+)

| Módulo | Arquivo | Responsabilidade | Padrão |
|--------|---------|------------------|--------|
| **app.js** | `app.js` | Entry point, bootstrap, roteamento, estado global | IIFE + Module Pattern |
| **router** | `router.js` | Hash-based routing (`#/rota`), guards auth, histórico | State Machine simples |
| **state_store** | `store.js` | sessionStorage (persistente) + memória (volátil), eventos `CustomEvent` | Observer Pattern |
| **auth_module** | `modules/auth.js` | Login, Cadastro, Recuperar, Logout — forms + validação + fetch | Page Controller |
| **listas_module** | `modules/listas.js` | Dashboard, Nova Lista, Editar — CRUD UI completo | Page Controller |
| **autocomplete_module** | `components/autocomplete.js` | Input + dropdown, debounce, normalização, seleção | Reusable Component |
| **comparacao_module** | `modules/comparacao.js` | Pré-filtro (3 etapas), Cálculo, Resultados | Page Controller + Wizard |
| **export_module** | `components/export.js` | PDF download, filename, toast | Utility Component |
| **perfil_module** | `modules/perfil.js` | Visualizar (read-only) + Editar (3 forms) | Page Controller |
| **ui_components** | `components/ui/*.js` | Toast, Skeleton, Modal, LoadingOverlay, Badge | Design System mínimo |
| **api_client** | `api/client.js` | Fetch wrapper, interceptors (auth, refresh, error), retry | Singleton |
| **utils** | `utils/*.js` | Funções puras: normalizar, currency, date, debounce, validação | Functional |

---

## Fluxo de Dados (Data Flow)

```mermaid
flowchart LR
    subgraph Browser[Navegador]
        A[app.js] --> B[router]
        B --> C{Auth?}
        C -->|Sim| D[listas_module / comparacao_module / perfil_module]
        C -->|Não| E[auth_module]
        D --> F[api_client]
        E --> F
        F --> G[Backend /v1/*]
        G --> H[(MySQL)]
        F --> I[state_store]
        I --> J[sessionStorage / Memória]
    end
```

---

## Roteamento (Hash-based)

| Rota | Módulo | Auth | Descrição |
|------|--------|------|-----------|
| `#/` | Redirect → `#/listas` (auth) ou `#/login` | — | Home |
| `#/login` | auth_module | Público | Login + aba Cadastro |
| `#/cadastro` | auth_module | Público | Cadastro (mesma página, tab) |
| `#/recuperar` | auth_module | Público | Solicitar recuperação |
| `#/redefinir?token=...` | auth_module | Público | Redefinir senha |
| `#/listas` | listas_module (Dashboard) | **Obrigatório** | Minhas listas (paginado, busca) |
| `#/listas/nova` | listas_module (Nova) | **Obrigatório** | Criar lista + autocomplete |
| `#/listas/{id}/editar` | listas_module (Editar) | **Obrigatório** | Editar nome/itens |
| `#/comparacao` | comparacao_module (Etapa 1: Categorias) | Opcional | Selecionar categorias |
| `#/comparacao/fornecedores` | comparacao_module (Etapa 2: Fornecedores) | Opcional | Selecionar fornecedores + slider |
| `#/resultado` | comparacao_module (Resultados) | Opcional | Tabela + exportar/imprimir |
| `#/perfil` | perfil_module (Visualizar) | **Obrigatório** | Dados read-only |
| `#/perfil/editar` | perfil_module (Editar) | **Obrigatório** | 3 forms: Email, Nome, Senha |

> **Guards:** Rotas "Obrigatório" verificam `state_store.hasAccessToken()` — se falso, redirect `#/login?next=...`.

---

## Gerenciamento de Estado (State Store)

| Chave sessionStorage | Conteúdo | TTL | Usado Por |
|----------------------|----------|-----|-----------|
| `cobeco_lista_efemera` | `{nome, itens: [{produto_id, quantidade, ...}]}` | Sessão | listas_module (Nova Lista, Promoção) |
| `cobeco_categorias_selecionadas` | `[categoria_id, ...]` | Sessão | comparacao_module |
| `cobeco_fornecedores_selecionados` | `[fornecedor_id, ...]` | Sessão | comparacao_module |
| `cobeco_orcamento_resultado` | `{fornecedores: [...], melhor_id, ...}` | Sessão | comparacao_module (Resultados) |

| Variável Memória (Volátil) | Conteúdo | Usado Por |
|----------------------------|----------|-----------|
| `accessToken` | JWT string (15min) | api_client (Authorization header) |
| `userData` | `{nome_usuario, email, nome, criado_em}` | perfil_module, ui_components |
| `refreshTokenPromise` | Promise de refresh em andamento | api_client (evita race condition) |

> **Reatividade:** `state_store` emite `CustomEvent('state:changed', {key, value})` — módulos ouvem via `addEventListener`.

---

## API Client (Singleton)

```javascript
// api/client.js — principios
const api = {
  baseURL: '/v1',
  async request(method, path, body) {
    const headers = { 'Content-Type': 'application/json' };
    if (state_store.getAccessToken()) headers.Authorization = `Bearer ${state_store.getAccessToken()}`;
    
    const response = await fetch(`${this.baseURL}${path}`, { method, headers, body: JSON.stringify(body) });
    
    if (response.status === 401) {
      // Tentar refresh automático (uma vez)
      if (!this._refreshing) {
        this._refreshing = true;
        await this.refreshToken();
        this._refreshing = false;
        return this.request(method, path, body); // retry
      } else {
        state_store.clearAuth(); // logout forçado
        router.navigate('#/login');
        throw new Error('Sessão expirada');
      }
    }
    return response.json();
  },
  refreshToken: async () => { /* POST /v1/auth/refresh com cookie */ }
};
```

---

## UI Components (Design System Mínimo)

| Componente | Arquivo | Props/API | Uso |
|------------|---------|-----------|-----|
| **Toast** | `components/ui/toast.js` | `show(message, type: 'sdoc-arch-0006-uc-v1cess'|'error'|'info', duration=3000)` | Global — `ui.toast.sdoc-arch-0006-uc-v1cess('Salvo!')` |
| **Skeleton** | `components/ui/skeleton.js` | `render(container, rows=5, cols=4)` | Tabelas/listas loading |
| **Modal** | `components/ui/modal.js` | `open({title, body, confirmText, onConfirm, cancelText, onCancel})` | Confirmações, promoção, exclusão |
| **LoadingOverlay** | `components/ui/loading.js` | `show()/hide()` | Full-screen spinner |
| **Badge** | `components/ui/badge.js` | `render(text, variant: 'green'|'yellow'|'red')` | % disponibilidade |
| **Autocomplete** | `components/autocomplete.js` | `new Autocomplete(inputEl, {fetchUrl, onSelect, debounce=300})` | Listas, Editar |
| **DataTable** | `components/datatable.js` | `render(container, {columns, data, expandable, onExpand})` | Dashboard, Resultados |

---

## Convenções Frontend (Constitution + ADR-001)

| Regra | Implementação |
|-------|---------------|
| **Vanilla JS ES6+** | Modules (`import`/`export`), `const`/`let`, arrow functions, `async`/`await`, `fetch` |
| **Zero Build Step** | Arquivos servidos diretamente por nginx — sem Vite/Webpack/Babel |
| **Desktop-first ≥1024px** | Media queries `min-width: 1024px` — mobile não suportado (RNF04) |
| **Tailwind CSS 3.x** | Via CDN ou build local — classes utilitárias, design system consistente |
| **PT-BR** | Variáveis, comentários, strings, mensagens de erro — tudo em português |
| **Acessibilidade Básica** | `aria-label`, `role`, `tabindex`, foco visível, cores contraste WCAG AA |
| **Normalização** | `normalizar(str) = str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()` — client + server |
| **Debounce Padrão** | 300ms (busca), 100ms (slider), 200ms (checkboxes) |
| **sessionStorage** | Chave prefixada `cobeco_*` — sobrevive a refresh/F5, limpa ao fechar aba |

---

## Rastreabilidade

| Artefato | Localização |
|----------|-------------|
| ADR-001 | `docs/decisoes/doc-adr-0001-stack-decision-v1.0.md` |
| spec-008 | `.ai/specs/spec-ui-0001-frontend-web-responsive-v1.0.md` |
| Spec-010 | `.ai/specs/spec-quality-0001-qualidade-pdca-ishikawa-v1.0.md` (feedback visual) |
| Código Fonte | `frontend/` (estrutura modular) |
| User Stories | `docs/strategy/user-stories/doc-user-story-0005-us-005` a `doc-user-story-0020-us-020` |

---

## Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|--------|-------|---------|--------------|
| 1.0 | 15/09/2026 | Nicholas Anthony + Eduardo Passarelli | Criação inicial baseada em ADR-001 + spec-008 | CCB (Gate 2) |

---

**Fim do Diagrama de Componentes — Frontend (C4 Level 3)**  
*Renderize no GitHub/VS Code/Mermaid Live Editor. Atualizar a cada ADR/CR que mude módulos ou fluxos frontend.*