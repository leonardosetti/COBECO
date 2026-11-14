# CR-001 — Quality Board Público (Página de Qualidade, Testes e Saúde do App)

**Documento:** Change Request (Solicitação de Mudança)  
**Versão:** 1.0  
**Status:** Proposto | Em Análise | Aprovado | Rejeitado | Obsoleto  
**Data:** 14/11/2026  
**Autor:** Leonardo Setti (Proddoc-arch-0006-uc-v1t Owner / Tech Lead)  
**Avaliadores:** CCB (Change Control Board) — FATEC Taquaritinga ADS  
**Prazo para Decisão:** 20/11/2026  
**Prioridade:** P2 (Backlog — Pós-MVP)  
**Tipo:** Novo Requisito (RD08 → RF19)  
**Rastreabilidade:** Constitution Art. 5.1, 11.7, 126 | PRD RF01-RF18 | spec-010 (Qualidade PDCA/Ishikawa)

---

## 1. Resumo Executivo

Criar uma **página pública de Quality Board** no aplicativo COBECO que exiba métricas de qualidade, saúde dos testes, status de build/deploy e indicadores de confiabilidade do sistema. A página seria acessível sem autenticação (pública) e serviria como demonstração de transparência técnica e maturidade de engenharia do projeto, alinhada com a especificação **spec-010 (Qualidade PDCA/Ishikawa)** já ratificada.

---

## 2. Contexto e Motivação

### 2.1 Problema / Oportunidade
- A **spec-010** já define baseline de qualidade: 12 PDCAs, 3 diagramas Ishikawa 6M, métricas verificadas, quality gates, RACI onda 6.
- Não existe **visualização pública** dessas métricas no aplicativo — ficam apenas em docs internos (`.ai/specs/`, `docs/operacao/`, CI logs).
- **Transparência técnica** é diferencial competitivo e eddoc-arch-0006-uc-v1acional: mostra maturidade de SDD, CI/CD, testes, governança.
- Alinhado com **RD08** (Quality Board Público) do PRD — atualmente no backlog pós-MVP.

### 2.2 Por que Agora?
- MVP (18 RFs) está **concluído e validado** (Gate 3 passado em 27/10/2026).
- Infraestrutura de métricas **já existe**: CI/CD (GitHub Actions), cobertura pytest, Test Plan, RAID Log, spec-010.
- Implementação **baixo risco** — página somente leitura, consome dados já coletados.
- Valor **eddoc-arch-0006-uc-v1acional e de portfólio** para a equipe e instituição (FATEC).

---

## 3. Proposta

### 3.1 Funcionalidades (MVP da Quality Board)

| Funcionalidade | Descrição | Fonte de Dados |
|----------------|-----------|----------------|
| **Build Status** | Status do último build CI (passed/failed), tempo, commit SHA | GitHub Actions API (`/repos/{owner}/{repo}/actions/runs`) |
| **Cobertura Testes** | % cobertura unitária + E2E, trend últimas 10 runs | `pytest --cov` XML + GitHub Actions artifacts |
| **Test Results** | Total testes, passed, failed, skipped, duração | GitHub Actions API + JUnit XML |
| **Deploy Status** | Última release tag, data, ambiente (staging/prod) | GitHub Releases API |
| **Quality Gates** | Status de cada gate: Lint (ruff), Type Check (mypy), Security (bandit), Coverage | GitHub Actions job status |
| **PDCA/Ishikawa Summary** | Cards resumidos dos 12 PDCAs + 3 Ishikawa (spec-010) | Dados estáticos do repo (`.ai/specs/spec-010...`) |
| **RAID Log Health** | Contagem riscos abertos/fechados, issues críticas | `docs/operacao/doc-raid-log-0001-raid-log-v1.0.md` (parsed) |
| **Performance** | Tempo de resposta API (p95), uptime | Health check endpoint + logs |

### 3.2 Requisitos Não-Funcionais

| RNF | Critério |
|-----|----------|
| **Acesso Público** | Sem autenticação — rota `/quality` ou `/health` acessível a todos |
| **Performance** | Carregamento < 2s (dados cacheados 5min) |
| **Atualização** | Dados refreshed a cada 5min (cache) ou push via webhook GitHub |
| **Responsivo** | Desktop-first ≥1024px (consistente com RNF04) — mobile opcional |
| **Acessibilidade** | WCAG AA básico (contraste, aria-labels, foco) |
| **Segurança** | Zero exposição de secrets, tokens, PII — apenas métricas agregadas |
| **LGPD** | Dados sintéticos apenas — zero PII real |

### 3.3 Arquitetura Técnica

```mermaid
flowchart LR
    subgraph Frontend[Frontend - Nova Página /quality]
        A[QualityBoard Module] --> B[API Client]
        B --> C[Cache 5min (sessionStorage)]
    end
    subgraph Backend[Novo Endpoint /v1/quality]
        D[QualityController] --> E[Aggregator Service]
        E --> F[GitHub API Client]
        E --> F2[CI Artifacts Parser]
        E --> F3[Repo Docs Parser]
    end
    F --> G[(GitHub API)]
    F2 --> H[(GitHub Actions Artifacts)]
    F3 --> I[(Repo Files .md)]
```

- **Backend:** Novo endpoint `GET /v1/quality` (público, sem auth) que agrega dados de múltiplas fontes.
- **Cache:** 5 minutos em memória (dict + TTL) — evita rate limit GitHub API (5000 req/h).
- **Frontend:** Novo módulo `quality_module.js` + rota `#/quality` — consome `/v1/quality`, renderiza dashboard com componentes UI existentes (Badge, Skeleton, DataTable).
- **GitHub Webhook (Opcional v2):** `workflow_run` completed → invalida cache + push update via SSE/WebSocket.

---

## 4. Alternativas Consideradas

| Alternativa | Prós | Contras | Decisão |
|-------------|------|---------|---------|
| **A — Página no App (Proposta)** | Integrada, usa componentes UI existentes, demonstração real do app | Requer endpoint backend + frontend | ✅ **Escolhida** |
| B — GitHub Pages estático gerado no CI | Zero backend, hospedagem grátis | Não integrado ao app, dados defasados entre builds | ☐ |
| C — Dashboard externo (Grafana, Datadog) | Rico em features, alertas | Overkill, custo, não "dogfooding" do próprio app | ☐ |
| D — Apenas docs internas (status quo) | Zero esforço | Não atende objetivo transparência pública | ☐ |

---

## 5. Impacto

| Área | Impacto | Detalhes |
|------|---------|----------|
| **Escopo (RF/UC)** | **Novo RF19** (Quality Board Público) + UC19/UC20 | Adiciona ao PRD como RD08 promovido |
| **Arquitetura** | Baixo | Novo endpoint GET `/v1/quality` (público), novo módulo frontend |
| **Banco de Dados** | **Nenhum** | Apenas leitura de fontes externas (GitHub API, artifacts, repo files) |
| **Segurança / LGPD** | Baixo (mitigado) | Endpoint público sem auth — apenas métricas agregadas, zero PII, zero secrets |
| **Testes / Qualidade** | Médio | Novos testes unit (aggregator) + E2E (página quality) — meta ≥80% mantida |
| **Prazos / Roadmap** | **P2 — Pós-MVP** | Estimativa: 3-5 dias (1 dev backend + 1 dev frontend) — **não afeta MVP** |
| **Infra/CI** | Baixo | GitHub API token (já existe em CI) com escopo `repo:read` + `actions:read` |

---

## 6. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Rate limit GitHub API (5000/h) excedido | Baixa | Cache 5min + fallback dados estáticos | Cache 5min obrigatório, monitorar headers `X-RateLimit-Remaining` |
| Dados sensíveis vazados no endpoint público | Muito Baixa | Auditoria de código + revisão de segurança | Code review obrigatório, checklist: zero secrets, zero PII, apenas agregados |
| Frontend quebra se API mudar | Média | Contrato OpenAPI versionado + testes E2E | Spec-first para `/v1/quality`, testes contrato no CI |
| Scope creep — adicionar muitas métricas | Média | Definir MVP claro (tabela acima), CR para expansões | CR obrigatório para qualquer métrica extra |
| Performance página > 2s | Baixa | Cache 5min + lazy loading componentes | Skeleton loading, cache aggressivo |

---

## 7. Rastreabilidade

- **Constitution:** Art. 5.1 (CCB approval), Art. 11.7 (CR obrigatório para novo RF), Art. 126 (change request process)
- **PRD:** `docs/strategy/PRD.md` — RD08 (Quality Board Público) promovido a RF19
- **Spec-010:** `.ai/specs/spec-quality-0001-qualidade-pdca-ishikawa-v1.0.md` — baseline qualidade (PDCA, Ishikawa, métricas, gates)
- **Spec-011:** `.ai/specs/spec-infra-0001-cicd-pipeline-v1.0.md` — CI/CD pipeline (fonte de dados build/test)
- **RAID Log:** `docs/operacao/doc-raid-log-0001-raid-log-v1.0.md` — fonte de dados health
- **Test Plan:** `docs/operacao/doc-test-plan-0001-test-plan-v1.0.md` — estratégia testes novo módulo
- **ADR-001:** Stack definida — novo endpoint segue mesmos padrões (FastAPI, Pydantic, cache, OpenAPI)

---

## 8. Decisão (CCB)

| Papel | Nome | Voto (Aprovar / Rejeitar / Abster) | Data | Comentário |
|-------|------|-----------------------------------|------|------------|
| **CCB Chair / PO** | Leonardo Setti | ☐ Aprovar ☐ Rejeitar ☐ Abster | __/__/____ | |
| **Tech Lead** | Leonardo Setti | ☐ Aprovar ☐ Rejeitar ☐ Abster | __/__/____ | |
| **Arquiteto** | Nicholas Anthony | ☐ Aprovar ☐ Rejeitar ☐ Abster | __/__/____ | |
| **QA Lead** | Nicolas Mallouk | ☐ Aprovar ☐ Rejeitar ☐ Abster | __/__/____ | |
| **Orientador Acadêmico** | [Nome] | ☐ Aprovar ☐ Rejeitar ☐ Abster | __/__/____ | |

**Decisão Final:** ☐ **Aprovado** — Incluir no Sprint 6 (Pós-MVP) | ☐ **Rejeitado** — Manter no backlog RD08 | ☐ **Em Revisão** — Solicitar mais detalhes

---

## 9. Próximos Passos (Se Aprovado)

1. **Criar Spec SDD** — `spec-017-quality-board-publico.spec.md` (spec-first, contrato OpenAPI)
2. **Criar Handoff** — `HF-XXXX-quality-board.md` → dispatch L0
3. **Implementar Backend** — `GET /v1/quality` (aggregator + cache + GitHub API client)
4. **Implementar Frontend** — `quality_module.js` + rota `#/quality` + componentes UI
5. **Testes** — Unit (≥80%) + E2E Playwright (página quality)
6. **CI/CD** — Adicionar job quality no pipeline
7. **Documentação** — Atualizar PRD (RF19), TRACEABILITY, doc-readme-0001-readme-canon
7. **Deploy** — Tag `v0.2.0` com Quality Board

---

## Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | 14/11/2026 | Leonardo Setti | Criação inicial — proposta Quality Board Público | CCB (pendente) |

---

**Fim do CR-001 — Quality Board Público**  
*Submetido ao CCB para análise e decisão. Se aprovado, segue fluxo SDD: Spec → Handoff → L0 → Implementação → Review → CI → Gatekeeper → CCB → Merge.*