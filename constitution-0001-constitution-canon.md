---
# === IDENTIFICAÇÃO UNIVERSAL ===
id: "constitution-0001-constitution--canon"
type: "constitution-0001"
title: "CONSTITUTION 0001 — "
version: "3.2"
status: "ratificado"
canonical: true
canonical_slug: ""

# === METADADOS DE GOVERNANÇA ===
created: "2026-11-14"
updated: "2026-11-14"
author: "Leonardo Setti (@leonardosetti)"
owner: "CCB"
ratified_by: "gh-sig:owner:leonardosetti:14863508"
ratified_at: "2026-11-14"
supersedes: null
superseded_by: null

# === RASTREABILIDADE (SSOT) ===
trace:
  constitution: ""
  req_func: []
  req_nfunc: []
  use_cases: []
  specs: []
  handoffs: []
  adrs: []
  code: []
  tests: []

# === CLASSIFICAÇÃO ===
domain: "general"
layer: "artifact"
tags: []
lgpd_class: "n/a"

# === WORKFLOW STATUS (P3) ===
workflow:
  stage: "ratificado"
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Constituição — COBECO MVP

**Projeto:** Cotação de Bens de Consumo (COBECO) — Cotação de preços entre fornecedores a partir de listas de compras.  
**Instituição:** FATEC Taquaritinga — Análise e Desenvolvimento de Sistemas.  
**Versão:** 2.0  
**Status:** Lei suprema do repositório (SSOT normativo).  
**Última revisão:** 13 de Novembro de 2026  
**Próxima revisão:** após ratificação do CCB ou alteração de escopo (Art. 5.1).

---

# TÍTULO I — IDENTIDADE, ESCOPO E PILARES

## Art. 1 — Identidade e escopo do projeto

1.1. O projeto denomina-se **COBECO** (Cotação de Bens de Consumo), um MVP desktop-first de comparação de preços entre fornecedores a partir de listas de compras, desenvolvido como trabalho acadêmico da FATEC Taquaritinga (ADS).

1.2. Escopo congelado (SSOT v3.2):
- 18 Requisitos Funcionais (RF01–RF18) definidos em `req-func-0001-requisitos-funcionais-canon.md`;
- 29 Casos de Uso (UC01–UC29) definidos em `req-use-case-0001-casos-de-uso-canon.md`;
- 8 tabelas PT-BR definidas em `doc-arch-0001-camada-de-dados-canon.md` (DER v3.2);
- Stack ratificada pelo ADR-001 (13/11/2026): FastAPI + Pydantic + SQLAlchemy 2.0 (async) + MySQL 8 InnoDB + Alembic + ReportLab (backend); Vanilla JS ES6+ + Tailwind CSS + nginx (frontend); Docker Compose (infra); GitHub Actions (CI).

1.3. Stack técnica oficial (não negociável sem CCB):
| Camada | Tecnologia | Versão | Porta |
|---|---|---|---|
| Banco de Dados | MySQL 8.0 InnoDB | 8.0 | 3306 (rede `data`, interna) |
| ORM / Migrações | SQLAlchemy 2.0 + Alembic | 2.0 / 1.14 | — |
| Backend | Python + FastAPI + Pydantic v2 | 3.11+ | 8000 (rede `edge`) |
| Frontend | Vanilla JS ES6+ + Tailwind CSS | ES6+ | 80 (nginx) |
| Proxy | nginx | Alpine | 8380 (exposta) |
| PDF | ReportLab | 4.3.1 | server-side |
| Testes | pytest + pytest-cov + pytest-asyncio | — | — |
| Lint / Formato / Tipos | ruff + black + mypy | — | — |
| CI/CD | GitHub Actions | — | — |

1.4. Princípios constitdoc-arch-0006-uc-v1ionais inafastáveis:
- **FOSS 100%**: nenhuma dependência paga ou proprietária sem Bypass de 3 pilares (Art. 4.5);
- **LGPD primária**: dados sintéticos apenas; zero PII reais em seeds, fixtures, logs, backups ou artefatos;
- **CPU-local**: execução local, zero cloud, zero CUDA;
- **Desktop-only**: layout exclusivo ≥ 1024px (RNF04); sem mobile.

1.5. Qualquer alteração de escopo, stack, prazos ou orçamento requer Change Request (CR) com ratificação humana do CCB (Art. 5.1).

---

# TÍTULO II — HIERARQUIA NORMATIVA

## Art. 2 — Hierarquia de documentos

Em caso de conflito, vence o documento de nível superior, na ordem:

1. `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` (lei suprema — este documento);
2. `doc-agents-0001-agents-canon.md` (estado do repo e convenções de trabalho);
3. `req-func-0001-requisitos-funcionais-canon.md` + `req-use-case-0001-casos-de-uso-canon.md` + `doc-arch-0001-camada-de-dados-canon.md` (SSOT v3.2 — requisitos e modelo de dados);
4. `board-roadmap-0001-roadmap-canon.md` + `doc-readme-0001-readme-canon.md` (planejamento de sprints e marcos);
5. `docs/decisoes/` (ADRs — decisões arquiteturais ratificadas);
6. `.ai/specs/*.md` (especificações técnicas SDD);
7. `.ai/handoffs/HF-*.md` (handoffs de execução);
8. Código-fonte (`backend/`, `frontend/`, `proxy/`, `scripts/`);
9. Arquivos de agente (`.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/`, `.ai/agents/`, `.planning/`).

2.1. Nenhum artefato de nível inferior pode sobrescrever ou contradizer um de nível superior. Conflitos devem ser submetidos ao CCB via CR (Art. 5.1).

2.2. A fonte única da verdade (SSOT) para requisitos é `req-func-0001-requisitos-funcionais-canon.md v3.2`; para modelo de dados, `doc-arch-0001-camada-de-dados-canon.md v3.2`; para stack, `ADR-001`.

---

# TÍTULO III — PRINCÍPIOS DE DESENVOLVIMENTO

## Art. 3 — Princípios gerais

3.1. **KISS**: escopo enxuto, dados mockados via seed, UI desktop-first, nenhuma funcionalidade além dos 18 RF.

3.2. **Clean Architecture**: separação rígida em quatro camadas — Domínio (entities, repositories, usecases), Casos de Uso, Adaptadores (API, DB), Frameworks (FastAPI, SQLAlchemy, nginx). Nenhuma dependência de framework vaza para o Domain.

3.3. **ACID**: transações explícitas (`BEGIN`/`COMMIT`), engine InnoDB, sem dados órfãos, FKs com `ON DELETE CASCADE/RESTRICT`.

3.4. **SDD (Spec-Driven Development)**: todo código entra apenas via par spec + handoff aprovado (Art. 6). Sem código solto.

3.5. **LGPD**: dados sintéticos apenas; zero PII reais em qualquer artefato do repositório.

3.6. **FOSS-first**: nenhuma dependência paga/proprietária sem Bypass de 3 pilares (Art. 4.5).

3.7. **YAGNI**: nenhuma abstração, wrapper, opção ou config "para depois" que não seja exigida pelo escopo atual dos 18 RF.

3.8. **PT-BR**: nomenclatura de banco de dados, variáveis, comentários e mensagens de erro em português do Brasil.

3.9. **Segurança por padrão**: validação em fronteiras HTTP, parameterized queries, sem segredos em repositório, erros sem traceback de usuário.

---

# TÍTULO IV — GOVERNANÇA DE AGENTES

## Art. 4 — Roster, orquestrador e kill switch

4.1. O roster canônico de agentes é `.ai/agents/config-registry-0001-registry-v1.0.yaml` (projeto: COBECO). É a única fonte de quem pode atuar e em que escopo.

4.2. O orquestrador L0 é `agent-nexus-prime-ultimate`; despacha tarefas via `scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py`. Nenhum agente age sem dispatch do L0.

4.3. Todo agente responde com parcel half-duplex contendo campos `dod` (Definição de Pronto) e `kill_switch`.

4.4. **Kill Switch é não-negociável**: ativa-se diante de vetores LGPD, vigilância não autorizada, bypass de CI ou meta-bypass. Interrompe execução imediata e aciona CCB.

4.5. **Bypass de dependência FOSS**: requer (i) force majeure justificada, (ii) saída FOSS nomeada e documentada, (iii) ratificação humana do CCB.

4.6. Nenhum agente escreve código, specs, handoffs ou arquivos de outro agente sem dispatch do L0 e revisão cruzada (Art. 8.3).

4.7. **RAG/DAG/Roster canônicos**: quando o volume de documentos exceder a janela de contexto, instituir:
- **Roster canônico**: `.ai/agents/config-registry-0001-registry-v1.0.yaml` atualizado a cada mudança de agente/tarefa;
- **RAG**: indexação de specs e handoffs em `.planning/` para recuperação contextual;
- **DAG**: grafo de dependências entre specs, handoffs e tasks em `.planning/graphs/`.

---

# TÍTULO V — AUTORIDADE HUMANA E CCB

## Art. 5 — Decisão humana

5.1. O Humano é decisor único (CCB chair). Aprovação humana é separada e obrigatória para: merge, release, alteração de escopo, alteração de stack, mudança de prazos e orçamento.

5.2. Nenhum agente decide datas, orçamento ou escopo. Agentes só executam o que o CCB ratificou.

5.3. **Recusa de conflito de interesse**: agente não revisa, não aprova e não faz merge de próprio trabalho.

5.4. **Change Request (CR)**: qualquer pedido de alteração no escopo, prazo, custo ou requisitos aprovados deve ser formalizado em CR, passar por análise de impacto e ser ratificado pelo CCB antes da execução.

---

# TÍTULO VI — MÉTODO SDD E CADEIA DE MERGE

## Art. 6 — Spec-Driven Development

6.1. Todo fluxo de trabalho entra como **spec** (`.ai/specs/*.md`) e sai como **handoff** (`.ai/handoffs/HF-*.md`).

6.2. O handoff deve passar pelo `handoff_parser.py` antes do dispatch do L0.

6.3. **Cadeia de merge obrigatória**: reviewer (rubrica R-01..R-07) → qa-sdet (evidência) → CI verde → gatekeeper → aprovação humana (CCB).

6.4. Templates de artefatos SDD: `.ai/specs/spec-template-0001-adr-template-v1.0.md` para ADRs; specs seguem o frontmatter canônico (`id`, `title`, `type`, `version`, `status`, `owner`, `derived-from`, `last-revised`, `lgpd-class`, `tags`).

6.5. Uma spec só é considerada "ativa" quando ratificada no INDEX de specs e vinculada a pelo menos um handoff pronto.

---

# TÍTULO VII — SEGURANÇA

## Art. 7 — Guardrails de segurança

7.1. **Nenhum segredo em repositório**: `config-env-0001-env-example-v1.0`, `secrets/`, `*.pem`, `*.key`, `*.secret` estão no `.gitignore`; jamais commitar credenciais, chaves, tokens ou senhas.

7.2. **Validação em fronteiras HTTP**: rate limiting (6 req/15min por IP + username — RNF10), validação de entrada Pydantic em todos os endpoints, parameterized queries apenas (proteção contra SQLi).

7.3. **Autenticação**: JWT access token (15 min, memória) + refresh token (7 dias, cookie `httpOnly`, `SameSite=Strict`); bcrypt com salt=12 (RF01, RF02).

7.4. **Recuperação de senha**: modo `log` (token no stdout do container) para desenvolvimento; modo `email` requer SMTP configurado (RF04). Nunca expor token em resposta HTTP ao cliente.

7.5. **Tratamento de erros**: erros nunca expõem tracebacks, payloads de usuário ou dados financeiros (retornar mensagens genéricas).

7.6. **LGPD**: dados sintéticos apenas; DPIA/Threat Model obrigatório antes de qualquer lançamento que toque dados reais (Art. 14).

7.7. **Sanitização recorrente**: antes de todo commit/push, verificar que nenhum arquivo de segredo está staged (`git diff --cached --name-only | grep -iE '\config-env-0001-env-example-v1.0$|secrets/|\.pem$|\.key$|\.secret$'`).

---

# TÍTULO VIII — QUALIDADE E TESTES

## Art. 8 — Padrões de qualidade

8.1. **Cobertura de testes**: ≥ 80% nos módulos tocados (gate CI via `pytest --cov-fail-under=80`, não negociável — RNF06).

8.2. **Testes determinísticos**: sem relógio de parede, sem rede, sem dados reais (usar fakes/mocks determinísticos).

8.3. **Code review**: todo PR passa por review com rubrica R-01..R-07 antes do merge; agente não revisa próprio trabalho (Art. 5.3).

8.4. **DoD (Definição de Pronto) por PR**:
- Código segue Clean Architecture (4 camadas), sem vazar framework para o Domain;
- Todas as queries usam parameterized queries;
- Nomenclatura DB e variáveis em PT-BR (DER v3.2);
- Testes unitários escritos; cobertura não diminuiu;
- Contrato OpenAPI (`/docs`) atualizado (SDD — RNF02);
- Funciona via `docker compose up` sem configuração manual extra.

8.5. **CI/CD**: pipeline GitHub Actions executa `ruff` + `pytest --cov` + `mypy` + build Docker em < 5 minutos (RNF07).

8.6. **Performance**: API < 500 ms p95 (RNF09); geração de PDF < 5 s para listas até 100 itens (RNF11).

8.7. **Tech Debt Log**: TODO/FIXME no código ou backlog devem ter data, autor e link para issue; revisados a cada sprint.

---

# TÍTULO IX — PERMISSÕES EXPLÍCITAS (DOS)

## Art. 9 — O que é permitido e encorajado

9.1. **DOS — Estratégia e Planejamento**: produzir PRD, BRD, RFC, CR e Roadmap antes da execução técnica, quando o escopo exigir clareza de negócio ou mudança estrutural.

9.2. **DOS — Arquitetura e Especificação**: produzir ADR para toda decisão arquitetural, SPEC/Design Doc para cada funcionalidade, API Contract (OpenAPI) para endpoints, diagramas C4 para onboarding e auditoria.

9.3. **DOS — Execução**: usar Epic / User Story / Task para quebrar o escopo; TODO/FIXME com data e autor para débito técnico; Test Plan / QA Sign-off antes de release; Changelog / Release Notes por versão.

9.4. **DOS — Operação e Conformidade**: Runbook/Playbook para operação e incidentes; Post-Mortem/RCA sem busca de culpados após falhas; SLA/SLO/SLI para confiabilidade; DPIA/Threat Model para LGPD.

9.5. **DOS — Scripts**: scripts de automação preferencialmente em Python (outros permitidos se justificados), localizados em `scripts/`, versionados, com execução determinística.

9.6. **DOS — Custom Skills**: criar skill customizada apenas quando a tarefa se repete e nenhuma skill instalada cobre o caso; registrar em `config-skills-0001-config-skills-0001-config-skills-0001-config-skills-0001-skills-lock-v1-v1.0-v1.0-v1.0.json` com hash computado.

9.7. **DOS — Agents**: usar agentes do roster `.ai/agents/config-registry-0001-registry-v1.0.yaml`; dispatch apenas via L0; respeitar kill_switch e `dod` em cada resposta.

9.8. **DOS — RAG/DAG/Roster**: instituir roster canônico, indexação RAG de specs/handoffs e grafo DAG de dependências quando o corpus exceder a janela de contexto.

9.9. **DOS — Hooks e Webhooks**: custom hooks OpenCode para pre-commit (sanitização de segredos) e pre-push (CI verde); webhooks do GitHub para CI/CD e notificações de PR.

9.10. **DOS — MCPs**: usar MCPs do projeto (ex.: github, github-kanban, github-remote) apenas com PAT com escopos mínimos (repo, read:org, workflow); nunca expor token do MCP no repositório.

9.11. **DOS — Sanitização**: avaliação recorrente de arquitetura e conformidade de regras (negociais e técnicas) a cada sprint; `.gitignore` mantido atualizado para excluir segredos, build outputs e artefatos gerados.

9.12. **DOS — Templates de elite**: usar os templates definidos no Art. 15 para PRD, BRD, RFC, CR, Roadmap, ADR, SPEC, API Contract, C4, User Story, Task, Test Plan, Runbook, Post-Mortem, SLA/SLO/SLI, DPIA, Threat Model, Changelog e Tech Debt Log.

---

# TÍTULO X — PROIBIÇÕES EXPLÍCITAS (DON'TS)

## Art. 11 — O que é proibido

11.1. **DON'TS — Segurança**: commitar `config-env-0001-env-example-v1.0`, `secrets/`, `*.pem`, `*.key`, `*.secret` ou qualquer credencial; expor tracebacks, payloads de usuário ou dados financeiros em erros; usar PII real em seeds/fixtures/logs.

11.2. **DON'TS — Arquitetura**: vazar dependência de framework para o Domain (Clean Architecture); usar queries não parameterizadas (SQLi); adicionar abstração/wrapper/opção "para depois" (YAGNI).

11.3. **DON'TS — Processo**: escrever código sem par spec + handoff (SDD); merge sem aprovação humana do CCB; agente revisar próprio trabalho (conflito de interesse); pular CI verde antes do merge.

11.4. **DON'TS — Agentes**: agente agir sem dispatch do L0; ignorar `kill_switch`; pular revisão cruzada de arquivo de outro agente.

11.5. **DON'TS — Dados**: usar dados reais de usuários em ambiente de desenvolvimento ou teste; gerar PDF com PII real.

11.6. **DON'TS — Repositório**: commitar `node_modules/`, `__pycache__/`, `.pytest_cache/`, `coverage/`, `dist/`, `build/`, `graphify-out/`, logs temporários ou backups `.bkp` não solicitados.

11.7. **DON'TS — Escopo**: implementar funcionalidades fora dos 18 RF sem CR ratificado; decidir datas, orçamento ou escopo como agente.

---

# TÍTULO XI — ARQUITETURA OTIMIZADA E IMPLEMENTAÇÃO

## Art. 12 — Guardrails de arquitetura e implementação

12.1. **Camadas ortogonais (infra)**: Docker Compose com redes `data` (interna, DB only) e `edge` (externo, frontend/backend/proxy); proxy nginx na porta 8380 roteia `/` → frontend e `/v1/` → backend; sem CORS necessário (mesma origem via proxy).

12.2. **Banco**: MySQL 8 InnoDB, charset `utf8mb4`, collation `utf8mb4_unicode_ci`, FKs com `ON DELETE CASCADE/RESTRICT`, soft delete (`deletado_em`) em `usuarios` e `listas`.

12.3. **Backend**: Clean Architecture manual (`domain/usecases/adapters/infrastrdoc-arch-0006-uc-v1ture`); schemas Pydantic v2; JWT em `python-jose`; senhas em `passlib[bcrypt]` salt=12; rate limiting custom.

12.4. **Frontend**: Vanilla JS + Tailwind + nginx; estado da lista em `sessionStorage` (lista efêmera); autocomplete com debounce 300ms; slider de disponibilidade 0–100%; tabela ordenada por preço ASC; destaque verde na melhor oferta; `@media print` para A4.

12.5. **PDF**: ReportLab server-side, formato A4, nome `lista_YYYYMMDD.pdf`, funciona para visitantes e autenticados, < 5 s para até 100 itens.

12.6. **Cache**: cache de 5 min no cálculo de orçamento (RF15); timeout de 10 s.

12.7. **Seed**: 11 categorias, 10 fornecedores, 50 produtos, ~300 preços em < 10 s (RNF08); `make seed` idempotente.

12.8. **Testes**: `pytest` + `pytest-cov` + `pytest-asyncio`; cobertura ≥ 80% nos módulos tocados; E2E com Playwright no frontend.

---

# TÍTULO XII — PRODUÇÃO DE ARTEFATOS

## Art. 13 — Estratégia e planejamento de artefatos

13.1. **PRD (Proddoc-arch-0006-uc-v1t Requirements Document)**: define requisitos de negócio, objetivos do produto, público-alvo e métricas de sdoc-arch-0006-uc-v1esso. Guia principal de produto e engenharia. Template: `docs/strategy/PRD-<id>.md`.

13.2. **BRD (Business Requirements Document)**: necessidades de negócio de alto nível e retorno esperado. Usado para aprovação de orçamento. Template: `docs/strategy/BRD-<id>.md`.

13.3. **RFC (Request for Comments)**: proposta de mudança ampla, nova funcionalidade ou padrão técnico para coleta de feedback. Template: `docs/rfc/RFC-<id>.md`.

13.4. **CR (Change Request)**: formaliza alteração de escopo, prazo, custo ou requisitos aprovados. Análise de impacto obrigatória. Template: `docs/change/CR-<id>.md`.

13.5. **Roadmap**: visão macro de entregas por marco/sprint. Alinha stakeholders. Template: `board-roadmap-0001-roadmap-canon.md`.

13.6. Cada artefato de estratégia deve ter: ID, status (draft/ativo/arquivado), autor, data, revisores, e link para requisitos trafegados (RF/UC).

---

## Art. 14 — Arquitetura e especificação técnica

14.1. **ADR (Architecture Decision Record)**: contexto, alternativas consideradas, decisão e consequências. `docs/decisoes/ADR-<NNN>-<slug>.md`.

14.2. **SPEC / Design Doc**: planta baixa da implementação — fluxos de dados, contratos de API, modelagem de banco, segurança. `.ai/specs/spec-<NNN>-<slug>-v<ver>.spec.md`.

14.3. **API Contract (OpenAPI/Swagger)**: endpoints, parâmetros, formatos de resposta, códigos de erro. Disponível em `/docs` (backend) quando `DEBUG=true`.

14.4. **C4 / Diagramas de Arquitetura**: níveis Contexto, Contêineres, Componentes, Código. `docs/arquitetura/`.

14.5. Todo artefato técnico deve ter frontmatter canônico (`id`, `title`, `type`, `version`, `status`, `owner`, `derived-from`, `last-revised`, `lgpd-class`, `tags`).

---

## Art. 15 — Execução e controle operacional

15.1. **Epic / User Story / Task**: unidades de trabalho rastreadas em GitHub Projects (milestones S1–S5); branch `feat/UC-XX-descricao`.

15.2. **TODO / FIXME / Tech Debt Log**: no código ou backlog, com data, autor e issue vinculada.

15.3. **Test Plan / QA Sign-off**: estratégia de testes, cenários críticos, critérios de aceite antes do deploy.

15.4. **Changelog / Release Notes**: novidades, correções, breaking changes por versão. `CHANGELOG.md`.

15.5. Critérios de aceite (DoD) definidos no Art. 8.4 aplicam a toda entrega.

---

## Art. 16 — Operação, riscos e conformidade

16.1. **Runbook / Playbook**: instruções passo a passo para operação, manutenção e resposta a incidentes. `docs/operacao/runbook.md`.

16.2. **Post-Mortem / RCA**: análise sem busca de culpados, foco na causa raiz e ações preventivas. `docs/operacao/postmortem-<id>.md`.

16.3. **SLA / SLO / SLI**: acordos de nível de serviço, objetivos de confiabilidade e indicadores de medição.

16.4. **DPIA / Threat Model**: avaliação de riscos de segurança e privacidade (LGPD) antes de lançamentos que toquem dados reais.

16.5. Avaliação recorrente de arquitetura e conformidade de regras (negociais e técnicas) a cada sprint; resultado documentado em `docs/auditorias/`.

---

## Art. 17 — Scripts, Skills, Agents, RAG/DAG/Roster, Hooks e MCPs

17.1. **Scripts**: `scripts/` — automação em Python preferencialmente; versionados; execução determinística.

17.2. **Custom Skills**: somente quando a tarefa se repete e nenhuma skill instalada cobre; registrar em `config-skills-0001-config-skills-0001-config-skills-0001-config-skills-0001-skills-lock-v1-v1.0-v1.0-v1.0.json` com hash.

17.3. **Agents**: roster `.ai/agents/config-registry-0001-registry-v1.0.yaml`; dispatch via L0 (`scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py`); cada resposta com `dod` e `kill_switch`.

17.4. **RAG/DAG/Roster**: roster canônico atualizado; indexação RAG de specs/handoffs em `.planning/`; grafo DAG de dependências em `.planning/graphs/`.

17.5. **Custom Hooks / Webhooks**: pre-commit (sanitização de segredos), pre-push (CI verde); webhooks GitHub para CI/CD e notificações de PR.

17.6. **MCPs**: usar MCPs do projeto com PAT de escopos mínimos (`repo`, `read:org`, `workflow`); nunca expor token do MCP no repositório.

17.7. **Sanitização de projetos**: antes de todo commit/push, verificar arquivos de segredo; `.gitignore` atualizado para excluir segredos, build outputs e artefatos gerados (`graphify-out/`, `log_llama.txt`, `*.bkp` não solicitados).

17.8. **Avaliação recorrente de arquitetura**: a cada sprint, revisar conformidade com Clean Architecture, parameterized queries, nomenclatura PT-BR, cobertura de testes e DoD.

---

## Art. 18 — Templates de elite

18.1. Os templates obrigatórios para cada tipo de artefato estão definidos nos Arts. 13–16 e devem ser copiados e preenchidos antes de iniciar qualquer trabalho correspondente.

18.2. Templates mínimos incluem: cabeçalho (id, título, tipo, versão, status, autor, data), seção de contexto/porquê, seção de o quê, seção de como (quando aplicável), rastreabilidade (RF/UC vinculados), assinatura/ratificação CCB.

---

# TÍTULO XIII — PROPAGAÇÃO E CAMINHOS DE DESTINO (SDD + OpenCode)

## Art. 19 — Propagação da Constitution para o projeto

19.1. A Constitution é a lei suprema; todos os artefatos do projeto devem ser alinhados a ela. Qualquer divergência é corrigida antes do merge.

19.2. Caminhos de destino (SDD + OpenCode):
- **Especificações**: `.ai/specs/spec-<NNN>-<slug>-v<ver>.spec.md`;
- **Handoffs**: `.ai/handoffs/HF-<NNNN>.md`;
- **ADRs**: `docs/decisoes/ADR-<NNN>-<slug>.md`;
- **Estratégia (PRD/BRD/RFC/CR/Roadmap)**: `docs/strategy/` e `board-roadmap-0001-roadmap-canon.md`;
- **Execução (Epic/User Story/Task)**: GitHub Projects (milestones S1–S5), branches `feat/UC-XX-descricao`;
- **Operação (Runbook/Post-Mortem/SLA/DPIA)**: `docs/operacao/` e `docs/auditorias/`;
- **Scripts**: `scripts/`;
- **Custom Skills**: registradas em `config-skills-0001-config-skills-0001-config-skills-0001-config-skills-0001-skills-lock-v1-v1.0-v1.0-v1.0.json`;
- **Hooks/Webhooks**: `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/hooks/` e webhooks do GitHub;
- **MCPs**: configurados via `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/mcp.json` (tokens nunca no repositório);
- **Código**: `backend/`, `frontend/`, `proxy/`.

19.3. Toda nova funcionalidade segue o fluxo: PRD/RFC (quando aplicável) → ADR (se decisão arquitetural) → SPEC → Handoff → dispatch L0 → implementação → revisão cruzada → CI verde → gatekeeper → aprovação humana → merge em `main` → kanban "Done".

19.4. O `doc-agents-0001-agents-canon.md` deve ser mantido atualizado com o estado do repo e convenções, refletindo sempre a Constitution vigente.

---

**Fim da Constituição — COBECO MVP v2.0**  
*Ratificada pelo CCB — FATEC Taquaritinga ADS — 13/11/2026*
