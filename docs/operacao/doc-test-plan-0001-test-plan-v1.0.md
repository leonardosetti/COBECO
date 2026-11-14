# COBECO — Plano de Testes (Primeira Release / MVP)

**Versão:** 1.0  
**Data:** 14/11/2026  
**Status:** APROVADO PARA EXECUÇÃO  
**Responsável:** QA Lead / Tech Lead  
**Aprovação:** Proddoc-arch-0006-uc-v1t Owner + Tech Lead + Arquiteto  

---

## 1. Introdução

### 1.1 Objetivo
Definir a estratégia, escopo, recursos, cronograma e critérios de aceite para a validação da **Primeira Release (MVP)** do COBECO — Comparação de Preços para Listas de Compras.

### 1.2 Escopo do MVP (Release 1.0)
| Funcionalidade | RFs Cobertos | Status |
|----------------|--------------|--------|
| **Autenticação** | RF01–RF06, RF02–RF04 | ✅ Implementado |
| **Listas de Compras (CRUD + Itens)** | RF07–RF11 | ✅ Implementado |
| **Catálogo & Autocomplete** | RF12, RF13 | ✅ Implementado |
| **Comparação Flat (Ordenação + Slider)** | RF15, RF16 | ✅ Implementado |
| **Exportação PDF (ReportLab)** | RF17 | ✅ Implementado |
| **Infra: Docker, CI, OpenAPI, Seed** | RNF03, RNF08, RNF12 | ✅ Implementado |

**Fora do escopo (Release 1.0):** Email real (recovery), PWA, mobile, comparações persistidas, notificações, multi-idioma, analytics.

### 1.3 Referências Normativas
- Constitution v2.0 (Art. 6 — SDD, Art. 3.5 — Dados Sintéticos)
- req-func-0001-requisitos-funcionais-canon.md v3.2 (16 RFs + 10 RNFs)
- req-use-case-0001-casos-de-uso-canon.md (UC01–UC18)
- doc-arch-0001-camada-de-dados-canon.md v3.2 (8 tabelas PT-BR)
- ADR-001 (Stack: FastAPI + MySQL 8 + Vanilla JS + nginx)
- ISO 25010 (Qualidade), WCAG 2.1 AA (Acessibilidade), OWASP Top 10 (Segurança)

---

## 2. Estratégia de Testes

### 2.1 Pirâmide de Testes (Meta de Cobertura)

```
                    ┌─────────────┐
                    │   E2E       │  ← 15%  (Fluxos críticos usuário)
                    │  (Playwright)│
               ┌────┴────────────┴────┐
               │  Integração          │  ← 35%  (API + DB, UseCases)
               │  (pytest + Testcont.)│
        ┌──────┴──────────────────────┴──────┐
        │  Unitários                         │  ← 50%  (Domain, UseCases, Utils)
        │  (pytest + Vitest)                 │
        └────────────────────────────────────┘
```

| Nível | Ferramenta | Meta Cobertura | Criticidade |
|-------|------------|----------------|-------------|
| **Unit (Backend)** | pytest + pytest-cov | **≥85%** (domain/usecases) | P0 |
| **Unit (Frontend)** | Vitest | **≥70%** (State, ApiClient, Router, Utils) | P1 |
| **Integração (Backend)** | pytest + Testcontainers MySQL | **≥80%** (API endpoints) | P0 |
| **E2E (Frontend)** | Playwright (Chromium/Firefox/WebKit) | **100% fluxos críticos** | P0 |
| **Contrato** | Schemathesis/OpenAPI | **100% endpoints** | P1 |
| **Performance** | k6 | RNF11 (<10s comparação), RNF10 (rate limit) | P1 |
| **Segurança** | Bandit, npm audit, OWASP ZAP | 0 Critical/High | P0 |
| **Acessibilidade** | axe-core (Playwright) | WCAG 2.1 AA | P1 |

### 2.2 Princípios (Constitution Art. 3, Art. 6)
- **SDD**: Testes derivam de specs (`.ai/specs/*.md`) → implementação → validação
- **Dados Sintéticos**: Apenas seed.sql / factories — **zero dados reais** (LGPD)
- **Clean Architecture**: Testes respeitam camadas (Domain → UseCases → Adapters → API)
- **Determinismo**: Testes isolados, sem dependência de ordem, cleanup automático
- **Fail-Fast**: CI falha em <80% cobertura, qualquer teste flaky, vulnerabilidade High/Critical

---

## 3. Escopo Detalhado por Nível

### 3.1 Testes Unitários — Backend (`backend/tests/unit/`)

| Módulo | Arquivos | Casos de Teste | RFs |
|--------|----------|----------------|-----|
| **Entities** | `test_entities.py`, `test_value_objects.py` | Validações `__post_init__`, imutabilidade VOs, regras de negócio | RF01, RF06, RF08, RF10, RF11 |
| **UseCases Auth** | `test_cadastrar_usuario.py`, `test_login.py`, `test_logout.py`, `test_recuperar_senha.py` | Sdoc-arch-0006-uc-v1esso, falhas, edge cases, rate limit, token expiry | RF01–RF04 |
| **UseCases Listas** | `test_criar_lista.py`, `test_editar_lista.py`, `test_excluir_lista.py`, `test_listar_por_usuario.py` | Transações, confirmação exclusão, paginação, soft delete | RF07–RF11 |
| **UseCases Comparação** | `test_calcular_orcamento.py`, `test_buscar_precos.py` | Ordenação ASC, slider disponibilidade, cache 5min, timeout 10s | RF15, RF16 |
| **UseCases Export** | `test_gerar_pdf_lista.py` | A4, nome arquivo, visitante sem auth, <5s (100 itens) | RF17 |
| **Repositories (Mock)** | `test_repositories.py` | Contratos de interface, mapeamento domain↔model | Todos |

**Total estimado:** ~120 testes unitários

### 3.2 Testes Unitários — Frontend (`frontend/tests/unit/`)

| Módulo | Arquivos | Casos de Teste |
|--------|----------|----------------|
| **State** | `test_state.js` | Login/logout, user persistence, ephemeral list, token expiry |
| **ApiClient** | `test_apiclient.js` | Interceptors, 401→refresh, error mapping, timeout |
| **Router** | `test_router.js` | Hash navigation, route matching, 404 redirect, bindEvents |
| **Utils** | `test_formatters.js`, `test_escapeHtml.js` | Currency, date, XSS prevention |
| **Components** | `test_toast.js`, `test_modal.js`, `test_confirm.js` | Render, a11y, callbacks |

**Total estimado:** ~50 testes unitários

### 3.3 Testes de Integração — Backend (`backend/tests/integration/`)

| Suite | Arquivo | Endpoints | Cenários |
|-------|---------|-----------|----------|
| **Auth Flow** | `test_auth_flow.py` ✅ | `/auth/cadastrar`, `/auth/login`, `/auth/logout`, `/auth/recuperar-senha/*`, `/auth/perfil` | Fluxo completo, rate limit, JWT, cookies, refresh, revogação |
| **Listas CRUD** | `test_listas_integration.py` | `/listas`, `/listas/minhas`, `/listas/{id}`, `/listas/{id}/itens` | Transação lista+itens, paginação, busca, soft delete, isolamento usuário |
| **Catálogo** | `test_catalogo_integration.py` | `/categorias`, `/fornecedores`, `/produtos`, `/produtos/autocomplete` | Autocomplete, filtro categoria, pré-filtro comparação |
| **Comparação** | `test_comparacao_integration.py` | `/comparacao`, `/comparacao/flat` | Ordenação preço, slider disponibilidade, cache, timeout |
| **Exportação** | `test_exportacao_integration.py` | `/export/lista/{id}/pdf` | PDF A4, visitante sem auth, nome arquivo, performance |
| **Perfil/Sessões** | `test_perfil_integration.py` | `/perfil` (GET/PUT), `/auth/refresh`, `/auth/logout/all` | Atualização perfil, mudança senha, revogação sessões |

**Total estimado:** ~80 testes de integração

### 3.4 Testes E2E — Frontend (`frontend/tests/e2e/`)

| Suite | Arquivo | Fluxos Críticos (Prioridade P0) |
|-------|---------|----------------------------------|
| **Cadastro** | `tests/crud/cadastro.spec.ts` ✅ | Cadastro válido, validações, unicidade, navegação login/recuperação |
| **Autenticação** | `tests/crud/auth.spec.ts` ✅ | Login/logout, recovery, rate limit, sessão |
| **Perfil** | `tests/crud/perfil.spec.ts` ✅ | Visualizar, editar nome/email, mudar senha, logout |
| **Listas** | `tests/crud/listas.spec.ts` ✅ | CRUD listas, isolamento dados, visibilidade |
| **Itens** | `tests/crud/itens.spec.ts` ✅ | CRUD itens, checkbox marcar/desmarcar |
| **Catálogo** | `tests/crud/catalogo.spec.ts` 🆕 | Autocomplete produto, adicionar à lista, filtro categoria |
| **Comparação** | `tests/crud/comparacao.spec.ts` 🆕 | **Fluxo completo**: seleção lista → fornecedores → slider → tabela flat → ordenação |
| **Exportação** | `tests/crud/exportacao.spec.ts` 🆕 | Baixar PDF, impressão (@media print), visitante sem auth |
| **Navegação** | `tests/crud/navegacao.spec.ts` 🆕 | Hash routing, deep links, guards auth, 404 |
| **Responsividade** | `tests/crud/responsividade.spec.ts` 🆕 | 1024px, 1440px, 1920px, breakpoint único |
| **Acessibilidade** | `tests/crud/a11y.spec.ts` 🆕 | axe-core: labels, contraste, tab order, ARIA, landmarks |
| **Estados** | `tests/crud/estados.spec.ts` 🆕 | Loading, empty states, toasts error/sdoc-arch-0006-uc-v1cess, retry |

**Browsers:** Chromium (P0), Firefox (P1), WebKit (P1)  
**Viewport:** 1280×720 (desktop-first ≥1024px)  
**Total estimado:** ~60 testes E2E

### 3.5 Testes de Contrato (`backend/tests/contract/`)

| Ferramenta | Escopo | Critério |
|------------|--------|----------|
| **Schemathesis** | Todos endpoints `/v1/` vs `/openapi.json` | 100% request/response válidos |
| **Drift Detection** | CI: comparar spec OpenAPI gerado vs commitado | Fail se drift detectado |

### 3.6 Testes de Performance (`backend/tests/performance/`)

| Cenário | Ferramenta | Critério de Aceite (RNF) |
|---------|------------|---------------------------|
| **Comparação 100 itens × 10 fornecedores** | k6 | p95 < 10s (RNF11) |
| **Exportação PDF 100 itens** | k6 | p95 < 5s (RNF11) |
| **Login concorrente (100 users)** | k6 | p95 < 2s, 0 erros |
| **Rate limit login (6/15min)** | k6 | Bloqueio correto após 5 tentativas |
| **Cache comparação (5min)** | k6 | 2ª request < 100ms |

### 3.7 Testes de Segurança

| Camada | Ferramenta | Critério |
|--------|------------|----------|
| **SAST Python** | Bandit | 0 High/Medium |
| **SAST JS** | Semgrep / ESLint Security | 0 High |
| **Dependências Python** | `pip-audit` | 0 CVEs Critical/High |
| **Dependências JS** | `npm audit` | 0 Critical/High |
| **DAST** | OWASP ZAP (baseline) | 0 Alertas High |
| **Auth Pen Test** | Manual | JWT tampering, refresh replay, rate limit bypass, IDOR |

### 3.8 Testes de Acessibilidade (`frontend/tests/e2e/tests/crud/a11y.spec.ts`)

| Critério WCAG 2.1 AA | Validação |
|----------------------|-----------|
| **1.4.3 Contraste Mínimo** | axe-core: 4.5:1 texto, 3:1 large text |
| **2.1.1 Teclado** | Tab order lógico, focus visible, skip links |
| **2.4.3 Ordem de Foco** | Navegação sequencial significativa |
| **3.3.2 Labels** | Todos inputs têm label associado |
| **4.1.2 Name/Role/Value** | ARIA roles, landmarks, live regions |
| **1.4.4 Redimensionamento** | Zoom 200% sem perda de conteúdo/função |

---

## 4. Ambientes de Teste

| Ambiente | Finalidade | Infraestrutura | Dados |
|----------|------------|----------------|-------|
| **Local (Dev)** | Unit, Integração, E2E (headed) | Docker Compose (MySQL, Backend, Frontend, Proxy) | Seed SQL (sintético) |
| **CI (GitHub Actions)** | Unit, Integração, Contrato, SAST, Dependency Scan | Ubuntu-latest + Docker + Testcontainers | Seed SQL + factories |
| **Staging (Opcional)** | E2E multi-browser, Performance, DAST, A11y | Docker Swarm / K3s (réplica produção) | Seed SQL + carga controlada |
| **Produção** | Smoke tests pós-deploy | Docker Compose (mesmo compose.yml) | Dados sintéticos apenas |

**Isolamento:** Cada execução de teste usa transação rollback (integração) ou banco dedicado (Testcontainers). E2E usa `authenticatedPage` fixture com cleanup automático.

---

## 5. Gerenciamento de Dados de Teste

### 5.1 Princípios (Constitution Art. 3.5)
- **Zero dados reais** — LGPD compliance
- **Seed determinístico** — `seed.sql` versionado (11 categorias, 10 fornecedores, 50 produtos, 300 preços)
- **Factories** — `createTestUser()`, `createListaData()` com timestamp/UUID para unicidade
- **Cleanup** — Rollback transação (integração), `localStorage.clear()` (E2E), `TRUNCATE` (performance)

### 5.2 Dados por Camada
| Camada | Fonte | Exemplos |
|--------|-------|----------|
| Unit (Domain) | Factories inline | `Usuario(id=1, nome_usuario="test", ...)` |
| Integração | `seed.sql` + factories | `await repo.criar(createTestUser())` |
| E2E | Fixtures Playwright | `authenticatedPage` (cadastra + loga) |
| Performance | k6 data generators | `generateLista(100 itens)` |

---

## 6. Critérios de Entrada / Saída

### 6.1 Entry Criteria (Início da Fase de Testes)
- [ ] Código em branch `feat/*` com PR aberta
- [ ] CI verde (lint, typecheck, unit, integração, contrato)
- [ ] `docker compose up -d` sobe sem erros (health check OK)
- [ ] Seed executado (`migrate` + `seed` containers exited 0)
- [ ] OpenAPI `/openapi.json` acessível e válido
- [ ] Test plan revisado e aprovado (PO + Tech Lead)

### 6.2 Exit Criteria (Release Candidate)
| Critério | Meta | Evidência |
|----------|------|-----------|
| **Cobertura Unit Backend** | ≥85% | `pytest --cov=src --cov-report=xml` |
| **Cobertura Unit Frontend** | ≥70% | `vitest run --coverage` |
| **Cobertura Integração** | ≥80% endpoints | Relatório pytest + OpenAPI validation |
| **E2E Fluxos Críticos** | 100% passando | Playwright HTML report (0 failed P0) |
| **Testes Contrato** | 0 drift | Schemathesis report |
| **Performance** | RNF11, RNF10 atendidos | k6 summary (p95) |
| **Segurança** | 0 Critical/High | Bandit, npm audit, ZAP baseline |
| **Acessibilidade** | WCAG 2.1 AA | axe-core report (0 violations P0) |
| **Documentação** | OpenAPI atualizado, doc-readme-0001-readme-canon testes | `/docs` commitado |

---

## 7. Papéis e Responsabilidades (RACI)

| Atividade | QA Lead | Dev Backend | Dev Frontend | Tech Lead | PO |
|-----------|---------|-------------|--------------|-----------|-----|
| Escrever testes unitários | C | **R** | **R** | A | I |
| Escrever testes integração | C | **R** | I | A | I |
| Escrever testes E2E | **R** | C | **R** | A | I |
| Configurar CI/CD | **R** | C | C | A | I |
| Executar performance/security | **R** | C | C | A | I |
| Triar falhas / classificar bugs | **R** | R | R | A | C |
| Aprovar Release Candidate | C | C | C | **R** | **R** |
| Validar UAT (critérios negócio) | C | I | I | C | **R** |

---

## 8. Ferramentas e Infraestrutura

| Categoria | Ferramenta | Versão | Uso |
|-----------|------------|--------|-----|
| **Test Runner (Py)** | pytest | 8.x | Unit, Integration |
| **Coverage (Py)** | pytest-cov | 5.x | XML/HTML reports |
| **Mock/DB (Py)** | Testcontainers, pytest-mock | Latest | Integration isolation |
| **Contract** | Schemathesis | Latest | OpenAPI validation |
| **Test Runner (JS)** | Vitest | 2.x | Unit Frontend |
| **E2E** | Playwright | 1.47+ | Chromium, Firefox, WebKit |
| **A11y** | @axe-core/playwright | Latest | WCAG 2.1 AA |
| **Performance** | k6 | 0.50+ | Load/stress |
| **SAST Py** | Bandit | 1.7+ | Security scan |
| **SAST JS** | Semgrep / ESLint Security | Latest | Security scan |
| **Deps Scan** | pip-audit / npm audit | Latest | CVE detection |
| **DAST** | OWASP ZAP | 2.14+ | Baseline scan |
| **CI/CD** | GitHub Actions | - | Pipeline orchestration |
| **Reports** | Playwright HTML, pytest-html, k6 HTML | - | Evidence packaging |

---

## 9. Cronograma (Sprint 5 — QA / Release)

| Semana | Atividades | Entregáveis |
|--------|------------|-------------|
| **S5.1 (Seg-Ter)** | Setup ambientes, seed, health checks | Ambientes validados |
| **S5.1 (Qua-Qui)** | Execução Unit + Integração + Contrato (CI) | Cobertura reports, 0 falhas |
| **S5.1 (Sex)** | Execução E2E multi-browser (Chromium P0) | Playwright report |
| **S5.2 (Seg)** | Execução E2E Firefox/WebKit + A11y | Cross-browser + axe-core report |
| **S5.2 (Ter)** | Performance (k6) + Security (Bandit, ZAP, deps) | k6 summary, security reports |
| **S5.2 (Qua)** | Triagem bugs, correções, re-execução | Bug log, regression passing |
| **S5.2 (Qui)** | Smoke tests staging, UAT com PO | UAT sign-off |
| **S5.2 (Sex)** | **Release Candidate 1.0** — Tag `v1.0.0` | Artifacts, changelog, deploy notes |

**Buffer:** 20% tempo para correções/re-execução

---

## 10. Riscos e Mitigação

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **Testes flaky (E2E)** | Alta | Médio | Retry 2x CI, isolamento fixtures, waitForLoadState/networkidle |
| **Cobertura < meta** | Média | Alto | Gate CI falha, pair programming para testes faltantes |
| **Performance não atende RNF11** | Baixa | Alto | Profiling prévio, otimização query/índice, cache Redis (futuro) |
| **Vulnerabilidade Critical em dep** | Baixa | Crítico | `npm audit fix` / `pip-audit` automático no CI, pin versions |
| **Dados de teste vazam** | Baixa | Crítico | Apenas seed sintético, `config-env-0001-env-example-v1.0` no `.gitignore`, CI usa secrets |
| **Browser WebKit instável** | Média | Baixo | P1 apenas, Chromium é P0 |
| **A11y regressions** | Média | Médio | axe-core no CI, baseline commitada |

---

## 11. Entregáveis (Artifacts)

| Artefato | Formato | Local | Retenção |
|----------|---------|-------|----------|
| **Test Plan** | Markdown | `docs/operacao/doc-test-plan-0001-test-plan-v1.0.md` | Permanente |
| **Unit Coverage (Py)** | XML (Cobertura) + HTML | `backend/coverage/` | 30 dias |
| **Unit Coverage (JS)** | HTML | `frontend/coverage/` | 30 dias |
| **Integration Report** | JUnit XML + HTML | `backend/test-results/` | 30 dias |
| **E2E Report** | Playwright HTML | `frontend/tests/e2e/playwright-report/` | 30 dias |
| **Performance Report** | k6 HTML/JSON | `backend/tests/performance/results/` | 30 dias |
| **Security Reports** | SARIF / JSON | `security-reports/` | 90 dias |
| **A11y Report** | HTML (axe-core) | `frontend/tests/e2e/a11y-report/` | 30 dias |
| **Contract Validation** | JSON | `backend/tests/contract/results/` | 30 dias |
| **Bug Log** | Markdown | `docs/auditorias/BUG-LOG-RELEASE-1.0.md` | Permanente |
| **UAT Sign-off** | PDF assinado | `docs/operacao/UAT-SIGNOFF-1.0.pdf` | Permanente |
| **Release Notes** | Markdown | `CHANGELOG.md` | Permanente |

---

## 12. Aprovação

| Papel | Nome | Assinatura | Data |
|-------|------|------------|------|
| **Proddoc-arch-0006-uc-v1t Owner** | _________________________ | _______________ | __/__/2026 |
| **Tech Lead** | _________________________ | _______________ | __/__/2026 |
| **Arquiteto de Software** | _________________________ | _______________ | __/__/2026 |
| **QA Lead** | _________________________ | _______________ | __/__/2026 |

---

## 13. Apêndices

### A. Glossário
- **SDD**: Specification-Driven Development
- **RNF**: Requisito Não Funcional
- **RF**: Requisito Funcional
- **UC**: Caso de Uso
- **p95**: Percentil 95 (latência)
- **DAST**: Dynamic Application Security Testing
- **SAST**: Static Application Security Testing

### B. Comandos de Referência
```bash
# Backend
cd backend && pytest --cov=src --cov-report=html          # Unit + coverage
cd backend && pytest tests/integration/ -v                 # Integração
cd backend && schemathesis run /openapi.json               # Contrato
cd backend && k6 run tests/performance/comparacao.js       # Performance
cd backend && bandit -r src/ -f json -o bandit-report.json # SAST

# Frontend
cd frontend/tests/e2e && npx playwright test --project=chromium  # E2E
cd frontend && vitest run --coverage                       # Unit + coverage
cd frontend/tests/e2e && npx playwright test tests/crud/a11y.spec.ts  # A11y

# Full CI Local
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.override.yml up -d
make test          # Backend unit + integration
make test-e2e      # Frontend E2E
```

---

**FIM DO PLANO DE TESTES — COBECO MVP Release 1.0**  
**Próxima revisão:** Pós-Release 1.0 (lições aprendidas → Release 1.1)