---
id: spec-arch-0001-container-layers-v1.0
type: spec-arch
title: SPEC ARCH — Container Layers
version: v1.0
status: ratificado
canonical: false
canonical_slug: container-layers
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
domain: specs
layer: spec
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
---
spec_id: spec-005
specname: container-layers-v1
version: 0.4.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-02
updated: 2026-11-05
origin: hf-exec-0029 (TA-0029) + amendment hf-exec-0030 (TA-0030)
task: TA-0030 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
wave: WS-4 | Onda 4 — Execução Técnica (camadas de containers)
lgpd-class: n/a (zero PII neste artefato; P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90)
trace:
  - .ai/handoffs/hf-exec-0029-container-layers-spec-v1.0.md
  - .ai/handoffs/hf-exec-0030-nginx-aceito-demo-v1.0.md
  - constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md (Art. 10.1, P-01, P-02, P-03, P-04, P-06, P-07, P-11)
  - docs/decisoes/adr-010-stack-infraestrutura.md
  - docs/decisoes/adr-001-stack.md
  - ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16)
---

# SPEC spec-005 — container-layers-v1 — Camadas de containers para a produção ortogonal do COBECO

Status: SPEC EMITIDA — AMENDADA PELA TA-0030 (2026-11-02) — PENDENTE DE REVISÃO E DE IMPLEMENTAÇÃO (onda seguinte, Art. 6.1 SDD) | Tarefa: TA-0030 (amenda cirúrgica; handoff `.ai/handoffs/hf-exec-0030-nginx-aceito-demo-v1.0.md`) sobre a emissão TA-0029 (`.ai/handoffs/hf-exec-0029-container-layers-spec-v1.0.md`, envelope `.ai/handoffs/task-ta-0029.json`) | Motivo da amenda: Nginx/proxy promovido de "profile opcional latente" para **ACEITO E MANTIDO** por ratificação GP/Humano 2026-11-02 (Art. 5.1, §2) | Orquestrador: agent-nexus-prime-ultimate | Custódia: agent-sdd-specialist (`.ai/specs/`)

Fonte única das decisões de camadas de containers. Em conflito, vale a hierarquia do Art. 2 da Constituição (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:41-50; resolução de cima para baixo, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:78).

Convenções: citação `arquivo:linha`. Identificadores/status/caminhos em EN; narrativa em PT-BR (P-10). Toda alegação sem fonte está marcada **UNKNOWN - verify**. Esta SPEC não implementa código (Art. 6.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:150 — especifica → implementa → valida → registra).

---

## 1. Contexto e tarefa (origem)

O Art. 10.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213) manda que as camadas de execução da aplicação rodem ortogonais: cada camada em container Docker próprio, construída/versionada/reiniciada/substituída independentemente, comunicando-se **apenas por interface declarada** (porta, volume ou API) — nunca por estado implícito compartilhado — e fixa a stack canônica **PostgreSQL + Docker Compose + Nginx latente, conforme ADR-010**. O Art. 10.4 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:219) torna violação de ortogonalidade defeito tratado, barrado nos portões reviewer → gatekeeper (P-06, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:94). **Amenda TA-0030:** quanto ao estado do proxy, vale a ratificação GP/Humano 2026-11-02 (Art. 5.1) — Nginx/proxy **aceito e mantido** (sempre ativo); a citação "Nginx latente, conforme ADR-010" acima é o texto constitdoc-arch-0006-uc-v1ional original, e a ADR-010 permanece inalterada, com sua emenda como follow-up pendente (§2, §13).

Estado atual no filesystem (verificado em 2026-11-02):

- `config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml` único com serviços `db` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:26, `postgres:15-alpine` pinnado por digest em :27), `migrate` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:50, Alembic `upgrade head` em :52), `web` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:62) e `proxy` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:89, `profiles: ["proxy"]` em :91 — latente **hoje**; alvo desta SPEC: sempre ativo, §2/§3.2).
- **Back e Front estão fundidos no serviço `web`**: uma única imagem (`x-app`, config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:11-15) que faz `COPY src ./src` (Dockerfile:59) e sobe `uvicorn src.backend.main:app` (Dockerfile:67); o template `src/frontend/templates/invoice.html` é renderizado in-process pelo backend para gerar o PDF (spec-004-backend-mvp-v1.spec.md:130). `src/frontend/templates/index.html` tem 0 B e `src/frontend/static/` está vazio (verificado em 2026-11-02).
- Redes: `data` (`internal: true`, config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:112-113; membros `db`, `migrate`, `web`) e `edge` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:115; membros `web` e `proxy` — comentário config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:114).
- `Dockerfile` multi-stage (Dockerfile:13, :25) com `USER cobeco` uid 10001 (Dockerfile:49-61); base `python:3.12-slim` pinnada por digest (Dockerfile:6); `config-env-0001-env-example-v1.0.example` com valores dummy (config-env-0001-env-example-v1.0.example:1-4); `infra/nginx/default.conf` com `proxy_pass http://web:8000` (infra/nginx/default.conf:16).

Tarefa (hf-exec-0029 §Tarefa): especificar a separação das três camadas (**Dados, Back, Front**) para a produção ortogonal, mais aderentes justificadas, topologia de redes, reprodutibilidade, segurança, testabilidade, CI/CD da fase, interoperabilidade, User Stories Padrão B doc-user-story-018-us-018+ e proposta de UAT — sem implementar nada nesta onda.

---

## 2. Resolução de conflitos documentais

| Tema | Decisão | Fonte vencedora | Texto superado |
|---|---|---|---|
| Banco | PostgreSQL 15+ (`db`), SQLAlchemy async, asyncpg, Alembic | Constituição Art. 10.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213), ADR-010 Decisão 1 (ADR-010:65), consolidado em ADR-001 v1.1.0 (ADR-001-stack.md:18,29; ADR-LOG.md:24) | Textos SQLite: REQ-07 "cache SQLite" (.ai/specs/spec-req-0001-requisitos-review-round-1-v1.0.md:68), Tabela 1 OUT/IN (plano-escopo.md:76, via spec-002-requisitos-review-round-1.spec.md:123), ADR-001 v1.0.0; SQLite sobrevive **apenas como fixture de teste isolado** (ADR-001-stack.md:30,43) e rollback temporário do kill_switch (ADR-010:98), nunca como estado final |
| Vigência da ADR-010 | Conteúdo vigente da stack está consolidado em ADR-001 v1.1.0; ADR-010 permanece citada pela Constituição Art. 10.1 como origem da stack canônica e como artefato histórico de rastreamento | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213 (cita ADR-010) + ADR-010:3,8 (nota de supersedida por ADR-001 v1.1.0, ADR-LOG-001) + ADR-LOG.md:58 | Ler ADR-010 isoladamente como norma vigente sem consultar ADR-001 v1.1.0 (referência circular proibida — P-08) |
| Back+Front fundidos | Separação explícita em três camadas (Dados/Back/Front) conforme Art. 10.1 | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213 (ortogonalidade) | Estado atual `web` fundido (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:62) — texto superado por esta SPEC |
| Origem única do navegador (CORS) | Mantém **sem CORS**, tudo em mesma origem | spec-004-backend-mvp-v1.spec.md:134 ("Sem CORS: o frontend é servido na mesma origem") | Solução de duas portas host (front:8000 + back:8001), que exigiria CORS e violaria spec-004-backend-mvp-v1.spec.md:134 — rejeitada (§4.3) |
| Nginx/proxy | **ACEITO E MANTIDO** — serviço sempre ativo no fluxo padrão (não mais "profile opcional latente"), com comunicação integrada em cadeia usuário → `proxy` → `front` → `back` → `db` (+ `migrate` → `db` no boot) e healthchecks em cadeia (§4.2, §7.1); `front` alcançável pelo usuário somente via `proxy` em `127.0.0.1:8080` (§4.3) | **Ratificação GP/Humano 2026-11-02, Art. 5.1** (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:138; registrada pelo orquestrador) + hf-exec-0030 §Tarefa 1 | Texto superado: "Nginx latente (perfil opcional)" — ADR-010 Decisão 3 (ADR-010:67) e `profiles: ["proxy"]` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:91). **ADR-010 não alterada nesta onda**: emenda de ADR-010 listada como follow-up pendente (arquiteto → CCB) — §13 |
| G-05 (ci.yml) | Gap registrado como `ci.yml` vazio; **fato verificado em 2026-11-02: o arquivo tem 189 linhas** com 6 jobs | Fato: .github/workflows/config-ci-0001-github-actions-v1.0.yml:1-189 (`kill-switch-check` :17, `foss-compliance` :36, `sdd-validation` :69, `agent-health` :91, `test-suite` :108, `final-status` :176) × registro histórico: docs/planos/plano-granular/plano-proddoc-arch-0006-uc-v1ao-agentes.md:33 e .ai/handoffs/HF-RELATORIO-ANALISE-CONSTITUICAO.md:84,108 (GAP-10) | Alegar "ci.yml vazio" sem verificar (delta: nenhum job constrói/sobe as camadas Docker; `test-suite` com `timeout-minutes: 15` em ci.yml:111 × doc-user-story-011-us-011 ≤5min — ver §8) |
| Referência do Padrão B | Padrão B está em `docs/conhecimento/OKB.md:539` (seção **7.4**) | OKB.md:534-539 (arquivo) | Citação do handoff "OKB §9.3" (§9.3 = ITIL, OKB.md:650) — divergência documental registrada aqui; prevalece o arquivo (P-08) |

Fora do escopo desta SPEC: autenticação, novos endpoints, mudanças de regra de negócio, TLS/domínio, cache em serviço separado (ver §13).

---

## 3. Camadas obrigatórias e aderentes

### 3.1 As três camadas (obrigatórias)

| Camada | Serviço (nome EN) | Conteúdo | Fronteira declarada |
|---|---|---|---|
| **Dados** | `db` | PostgreSQL 15-alpine pinnado por digest (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:27), volume nomeado `cobeco_pgdata` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:34, :118), healthcheck `pg_isready` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:42-47) | Única interface de saída: TCP `db:5432` na rede `data`; **sem `ports` no host** (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:35) |
| **Back** | `back` (separação do `web` atual) | API FastAPI/Uvicorn `/v1` (spec-004-backend-mvp-v1.spec.md §3), regras de negócio, cotações, invoice PDF, persistência via `COBECO_DATABASE_URL` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:17) | Interface de entrada: HTTP `back:8000` rotas `/v1/*`; interface de saída: `db:5432` (rede `data`) e egress HTTPS para Frankfurter/PTAX (rede `edge`, ADR-010:71) |
| **Front** | `front` (separação do `web` atual) | Camada de apresentação: HTML5 + CSS3 + JS vanilla (ADR-001-stack.md:34), templates e assets `src/frontend/` (hoje `index.html` 0 B — §1) | Interface de entrada: HTTP na porta declarada (§4.3); interface de saída: API `back:8000/v1` (rede `edge`) |

Regras de fronteira (Art. 10.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213):

1. Cada camada é um serviço Compose próprio: `db`, `back`, `front` — construída, versionada e reiniciada independentemente (`docker compose restart back` não toca `front` nem `db`).
2. Nenhuma camada lê estado de outra por filesystem compartilhado. Único bind mount de config é o do `proxy` (`./infra/nginx/default.conf`, somente leitura, config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:99); volumes de dados são nomeados (`cobeco_pgdata`).
3. `invoice.html` permanece sob custódia do **Back** (é insumo do `POST /v1/invoice`, spec-004-backend-mvp-v1.spec.md:130), não do Front — a separação é de camada de execução, não de reescrita do contrato.
4. Violador dessas regras = defeito de ortogonalidade barrado em reviewer → gatekeeper (Art. 10.4, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:219).

### 3.2 Camadas aderentes (análise YAGNI, P-11 constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:104)

| Aderente | Decisão | Justificativa |
|---|---|---|
| `migrate` (Alembic) | **Mantida** | Job de execução única que precisa terminar antes do Back subir (`depends_on: migrate: service_completed_sdoc-arch-0006-uc-v1cessfully`, config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:68-69), usa a mesma imagem do Back (comentário config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:49; Dockerfile:64-66), roda só na rede `data` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:55) e é substituída a cada migração sem reiniciar as camadas — ortogonalidade prática (Art. 10.1). Fundi-la no startup do Back esconderia falha de schema e violaria a independência de restart. |
| `proxy` (Nginx/edge) | **Mantida — ACEITO E MANTIDO (sempre ativa no fluxo padrão)** | Exigida pela stack canônica (Art. 10.1 citando ADR-010; ADR-010:67) e já existente (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:89-108; infra/nginx/default.conf). Promovido de "profile opcional latente" por **ratificação GP/Humano 2026-11-02, Art. 5.1** (§2): sobe sempre em `docker compose up --build` e expõe o usuário em `127.0.0.1:8080`. Ausência de TLS/domínio (infra/nginx/default.conf:2) não condiciona mais a ativação. Estado alvo declarado nesta SPEC; remover `profiles: ["proxy"]` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:91) é implementação da onda seguinte (Art. 6.1) — compose real não alterado aqui. ADR-010 não alterada (emenda = follow-up, §2/§13). |
| Camada de **cache** | **Recusada por YAGNI (P-11)** | O cache de cotações já vive dentro do Back: tabela `fx_quotes` no PostgreSQL (spec-004-backend-mvp-v1.spec.md:122) + cache em memória com TTL (spec-004-backend-mvp-v1.spec.md:107). Redis aparece só em corpora legados `legacy-contradicts` (.ai/specs/spec-req-0001-requisitos-review-round-1-v1.0.md:86,123) e ADR-010/ADR-001 não o incluem. Novo serviço = capacidade sem demanda do ciclo atual. |
| Kubernetes / orquestrador extra | **Recusada** | ORCH3 "absolutamente desnecessário para MVP; overengineering flagrante" (ADR-010:44). |
| Serviço de static separado do Front (CDN/obj storage) | **Recusada** | Nuvem/terceiro vetado para dados do projeto (P-02/P-03, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:86-88); assets servidos pelo próprio Front. |

Escopo desta SPEC cobre as camadas da **aplicação**. As demais camadas enumeradas no Art. 10.1 (runtime de agentes SDD, CI) não são objeto deste artefato: o runner de CI é GitHub Actions Free Tier sob Bypass registrado (P-01, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84) e o runtime de agentes é L1/L3 conforme Art. 6.5 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:160-162) — **UNKNOWN - verify** se o orquestrador deseja SPEC própria para elas.

---

## 4. Topologia de redes e interfaces declaradas (Art. 10.1)

### 4.1 Redes

| Rede | Tipo | Membros (alvo) | Papel |
|---|---|---|---|
| `data` | `internal: true` (fato: config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:112-113) | `db`, `migrate`, `back` | Tráfego de persistência **apenas**. Sem rota para a internet (fato: comentário config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:111) e sem `front` — o Front jamais alcança o banco. |
| `edge` | bridge com rota externa (fato: config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:115) | `proxy`, `front`, `back` | Entrada do proxy, tráfego Front ↔ Back e egress do Back para Frankfurter/PTAX (comentário config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:114). |

Nenhuma rede nova nesta fase (YAGNI). Alternativa "rede interna `app` só para Front ↔ Back" fica para backlog se um teste de contrato de §7 acusar exposição indevida — **UNKNOWN - verify** só se ocorrer falha de contrato.

### 4.2 Matriz quem-fala-com-quem (who-talks-to-whom)

| # | De | Para | Interface declarada | Rede | Fato/Proposta |
|---|---|---|---|---|---|
| 1 | Navegador/host | `proxy` | `127.0.0.1:8080` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:97) — **sempre ativa**, sem `--profile` (alvo da TA-0030, §2) | edge | Fato (porta) → proposta: remover `profiles: ["proxy"]` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:91) na onda de implementação |
| 2 | Navegador/host | `front` | **PROIBIDA ao usuário** — `front` não publica porta no host; alcançável somente via `proxy` em `127.0.0.1:8080` (§4.3) | — | Proposta (alvo TA-0030; hoje `web` publica `127.0.0.1:8000`, config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:71) |
| 3 | `proxy` | `front` | HTTP porta interna declarada do `front` (`location /`) | edge | Proposta; hoje `proxy_pass http://web:8000` (infra/nginx/default.conf:16) — amendamento na onda de implementação |
| 4 | `proxy` | `back` | HTTP `back:8000` (`location /v1/`) | edge | Proposta; mesma amendamento acima |
| 5 | `front` | `back` | HTTP `back:8000/v1/*` (OpenAPI, §9) | edge | Proposta (interface única de Front→Back: API) |
| 6 | `back` | `db` | TCP `db:5432` via `COBECO_DATABASE_URL` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:17; config-env-0001-env-example-v1.0.example:16) | data (internal) | Fato |
| 7 | `migrate` | `db` | TCP `db:5432` (Alembic, config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:52) | data (internal) | Fato |
| 8 | `back` | Frankfurter/PTAX | HTTPS egress (ADR-010:71; spec-004-backend-mvp-v1.spec.md:99-100) | edge | Fato |
| 9 | `front` | `db` | **PROIBIDA** — `front` não é membro de `data` | — | Proposta (prova por teste, §7.4) |
| 10 | `db` | qualquer | **PROIBIDA** — `db` sem `ports` e só em rede internal (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:35) | — | Fato |

**Cadeia integrada (alvo TA-0030, cobre TODOS os containers):** usuário → `proxy` (`127.0.0.1:8080`) → `front` → `back` → `db`, com `migrate` → `db` no boot — cada salto atrás do healthcheck da camada anterior (§7.1): `db` healthy (`pg_isready`) → `migrate` concluído (`service_completed_sdoc-arch-0006-uc-v1cessfully`) → `back` healthy (`/v1/health`) → `front` healthy (`GET /`) → `proxy` healthy (porta 80 interna). Fronteira do usuário: somente o `proxy` (matriz #1; #2 proibida).

### 4.3 Invariante de origem única (sem CORS)

Backend-mvp-v1.spec.md:121 fixa "Sem CORS: o frontend é servido na mesma origem". Portanto (amendado pela TA-0030 — ratificação GP/Humano 2026-11-02, Art. 5.1):

- **Perfil padrão único e sempre ativo:** entry point único do usuário = `127.0.0.1:8080` = Nginx (`proxy`), com `location / → front` e `location /v1/ → back:8000` (amendamento de infra/nginx/default.conf:16 na onda de implementação). O usuário **não** alcança `front` nem `back` diretamente (matriz #2).
- `front` e `back` **não publicam porta no host**: `front` é alcançado somente pelo `proxy`; `back` é alcançado por `proxy`, `front` e pelos jobs que falam com `db` (`migrate`, matriz #7). `front` serve páginas/static e encaminha `/v1/*` para `back:8000` (matriz #5).

Toda a matriz usa somente porta, volume ou API — a "interface declarada única" do Art. 10.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213).

---

## 5. Reprodutibilidade (local-only, CPU-only)

Fluxo obrigatório, passo a passo, em qualquer máquina do ciclo (hardware de referência: AMD Ryzen 7 8700G, RAM 58 GB, **sem CUDA, sem cloud** — P-02, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:86):

```bash
git pull
cp config-env-0001-env-example-v1.0.example config-env-0001-env-example-v1.0        # valores dummy; troque POSTGRES_* localmente
docker compose up --build   # proxy (nginx) + db + migrate + back + front — SEM --profile
# abrir http://127.0.0.1:8080 no navegador e validar os fluxos MVP
```

Caminho de demonstração (hf-exec-0030 §Tarefa 2): `git pull` → `cp config-env-0001-env-example-v1.0.example config-env-0001-env-example-v1.0` → `docker compose up --build` (proxy incluído) → abrir `127.0.0.1:8080` → fluxos MVP funcionando de ponta a ponta, local CPU-only (health `GET /v1/health`, simulação cambial `POST /v1/simulate`, invoice PDF `POST /v1/invoice`, todos via proxy).

1. `git pull` — o repositório é auto-suficiente: compose (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml), `Dockerfile`, `config-env-0001-env-example-v1.0.example`, `infra/nginx/default.conf` e `migrations/` (Dockerfile:57-59).
2. `config-env-0001-env-example-v1.0` derivado de `config-env-0001-env-example-v1.0.example` com **valores dummy**; `config-env-0001-env-example-v1.0` nunca é commitado (config-env-0001-env-example-v1.0.example:4; "Nenhuma credencial real é versionada", constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:176). `COBECO_DATABASE_URL` sem valor padrão real = fail-closed (spec-004-backend-mvp-v1.spec.md:134).
3. `docker compose up --build` constrói tudo localmente **com o `proxy` incluído** (sem `--profile` — §2); nenhum serviço exige CUDA, GPU ou nuvem (P-02). Downloads de imagens de registry externa são **operação de build pontual**, nunca fluxo de dados (Art. 10.3, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:217).
4. **Digest pinning imutável (Art. 10.2, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:215):** `postgres:15-alpine@sha256:54e0dd8e…` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:27), `nginx:alpine@sha256:785835ea…` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:90), `python:3.12-slim@sha256:aa943ce4…` (Dockerfile:6). Atualizar digest exige copiar o novo valor para `docs/dependencias/registro.md` (Dockerfile:4-5; ADR-010:104) e, se alterar componente de infra, ADR específica (ADR-010:103).
5. Critério de aceite do fluxo: saída íntegra do `compose up` em máquina limpa sem intervenção manual além de `cp config-env-0001-env-example-v1.0.example config-env-0001-env-example-v1.0` (testado por doc-user-story-018-us-018 e fluxo UAT F-01, §12) e `127.0.0.1:8080` servindo os fluxos MVP de ponta a ponta (health, simulação cambial, invoice PDF).

---

## 6. Segurança (bloco completo — fail-closed, P-07)

| Controle | Evidência/fato | Aplicação alvo por camada |
|---|---|---|
| **non-root** | `USER cobeco` uid 10001, shell nologin (Dockerfile:49-61) | `back`, `front`, `migrate`. Exceções documentadas: entrypoint do Postgres troca de usuário (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:37-38); master do Nginx sobe como root e faz drop para workers `nginx` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:102-104) |
| **no-new-privileges** | `security_opt: ["no-new-privileges:true"]` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:22, :39, :101) | Todos os serviços, incluindo `back`/`front` herdados do anchor `x-app` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:22) |
| **cap_drop: ALL** | config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:23 (anchor `x-app`), :105 (`proxy`) | `back`, `front`, `migrate`, `proxy`. Exceções mínimas documentadas: `proxy` com `cap_add: [CHOWN, SETUID, SETGID]` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:106); `db` sem `cap_drop` por exigir CHOWN/SETUID/SETGID/DAC_OVERRIDE/FOWNER do entrypoint (comentário config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:37-38) |
| **read_only + tmpfs** | `read_only: true` + `tmpfs: [/tmp]` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:72-73) | `back`, `front`, `migrate` (mesmo anchor). `db` exceção: precisa escrever no volume (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:34) |
| **Portas em 127.0.0.1** | `127.0.0.1:8000` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:71), `127.0.0.1:8080` (:97), `db` sem `ports` (:35) | Entry point do usuário = `127.0.0.1:8080` (`proxy`); `front` e `back` **sem publicação no host** (alvo §4.3 — TA-0030); `db` sem `ports` |
| **Segredos só via config-env-0001-env-example-v1.0** | Nada sensível no compose (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:2); `${VAR:?…}` obrigatório (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:17,30-32); `config-env-0001-env-example-v1.0.example` dummy (config-env-0001-env-example-v1.0.example:8-16); exceção `!**/config-env-0001-env-example-v1.0.example` no `.gitignore` exigida (spec-004-backend-mvp-v1.spec.md:134) | Todas as camadas. Credencial real em repo = incidente (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:96) |
| **Digest pinning** | §5.4 acima; Art. 10.2 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:215) | Imagens base de todas as camadas |
| **LGPD (Art. 10.3)** | P-02/P-03 intra-container: zero dado sensível para registry/serviço de terceiros (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:217); invoice nunca persistida e zero PII em logs (spec-004-backend-mvp-v1.spec.md:126); "mínimo necessário, sem PII em artefatos" (P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90) | Logs das três camadas sem valores, corpo de requisição ou PII; volumes só `cobeco_pgdata` (dados de cotação pública, spec-004-backend-mvp-v1.spec.md:122); nenhum log/PII em serviço de terceiro |
| **Defense in depth** | `mem_limit`/`pids_limit` por serviço (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:40-41, :56-57, :75-76, :107-108) | Todas as camadas novas (`back`, `front`) declaram limites análogos — valores exatos: **UNKNOWN - verify** na implementação (referência: `web` 768m/256, `migrate` 256m/100) |

---

## 7. Testabilidade

### 7.1 Healthcheck por camada

| Camada | Healthcheck | Fato/Proposta |
|---|---|---|
| Dados | `pg_isready -U $POSTGRES_USER -d $POSTGRES_DB` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:42-47) | Fato |
| Back | `GET http://127.0.0.1:8000/v1/health` → `{"status":"ok"}` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:77-86; contrato spec-004-backend-mvp-v1.spec.md:64) | Fato |
| Front | `GET /` na porta interna → 200 | Proposta |
| `migrate` | `condition: service_completed_sdoc-arch-0006-uc-v1cessfully` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:68-69) | Fato |
| `proxy` | `depends_on` com `condition: service_healthy` em `front`/`back` (hoje `web`, config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:93-95) + healthcheck HTTP próprio na porta 80 interna do container `proxy` | Fato (hoje `web`) → proposta de amendamento; alvo: serviço **sempre ativo** (§2) |
| **Cadeia (alvo TA-0030)** | Ordem de healthy no `docker compose up`: `db` (`pg_isready`) → `migrate` (`service_completed_sdoc-arch-0006-uc-v1cessfully`) → `back` (`/v1/health`) → `front` (`GET /`) → `proxy` (porta 80 interna); a stack só reporta pronta quando `127.0.0.1:8080` responde | Proposta (hf-exec-0030 §Tarefa 1) |
| Dependência Back→Dados | `depends_on: db: condition: service_healthy` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:65-67) | Fato |
| Dependência Front→Back | `depends_on: back: condition: service_healthy` | Proposta |

### 7.2 Pirâmide de testes

- **Unitário** (base): `tests/unit/` — 10 módulos verificados (calculator, rate_service, circuit_breaker, schemas, simulation_service etc.). Sem rede nem relógio real (spec-004-backend-mvp-v1.spec.md:155).
- **Contrato**: `tests/integration/test_api_contract.py` e `tests/integration/test_openapi.py` (verificados em 2026-11-02) — blindam o `/v1` contra drift (spec-004-backend-mvp-v1.spec.md §3).
- **Integração**: `tests/integration/test_postgres_repository.py`, `test_lifespan.py`, `test_invoice.py`, `test_api_validation.py` com PostgreSQL real via `COBECO_TEST_DATABASE_URL` e marcador `postgres` (spec-004-backend-mvp-v1.spec.md:155; serviço efêmero do CI em ci.yml:115-130).
- **E2E**: **hoje não existe** teste de navegador/E2E — ausência verificada em 2026-11-02 (zero ocorrências de playwright/selenium/cypress em `tests/` e `requirements*`). A SPEC define o e2e mínimo desta fase como orquestração `docker compose up --build` + verificação dos fluxos F-01..F-06 do §12 via HTTP/healthchecks; e2e de navegador fica em backlog (YAGNI) — **UNKNOWN - verify** se o GP exige e2e de UI nesta onda.
- **Cobertura:** ≥ 80 % sobre `src/` (doc-user-story-008-us-008, .ai/specs/spec-req-0001-requisitos-review-round-1-v1.0.md:164; REQ-08 :69; P-06 constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:94), enforced por `--cov-fail-under=80` (ci.yml:170).

### 7.3 Testes de contrato de rede (quem fala com quem)

Para cada linha da matriz §4.2, um caso automatizado binário:

1. `back` resolve e conecta em `db:5432` (rede `data`) — positivo.
2. `front` **não** alcança `db:5432` (não é membro de `data`; matriz #9) — negativo.
3. `db` não expõe porta no host (`docker compose port` vazio; matriz #10) — negativo.
4. `front` alcança `back:8000/v1/health` e recebe 200 (matriz #5) — positivo.
5. Toda rota `/v1` respondida por `back` é compatível com spec-004-backend-mvp-v1.spec.md §3 (sobrepõe ao teste de contrato HTTP existente).

Implementação desses casos pertence à onda de implementação (Art. 6.1); aqui estão especificados com resultado esperado binário.

---

## 8. CI/CD desta fase

**Fatos verificados (2026-11-02):**

- G-05 está registrado como "`ci.yml` vazio" (docs/planos/plano-granular/plano-proddoc-arch-0006-uc-v1ao-agentes.md:33; .ai/handoffs/HF-RELATORIO-ANALISE-CONSTITUICAO.md:84,108 — GAP-10, "ALTA", bloqueia P-06/Art. 4.6), **mas o arquivo hoje tem 189 linhas** com os jobs `kill-switch-check` (ci.yml:17), `foss-compliance` (:36), `sdd-validation` (:69), `agent-health` (:91), `test-suite` (:108) e `final-status` (:176). O delta de G-05 que esta SPEC precisa declarar: **nenhum job constrói nem sobe as camadas Docker** e o `test-suite` tem `timeout-minutes: 15` (ci.yml:111).
- Existe também `.github/workflows/sddai-verify.yml` (1117 B, verificado em 2026-11-02).
- Gates hoje: coverage fail-closed (ci.yml:170), kill switch por job (ci.yml:17-31), scanner de credenciais (ci.yml:50-59), validação de registry/DAG (ci.yml:69-86).

**Pipeline desta fase (proposta — fecha o delta de G-05):**

1. **Job `lint-and-unit`:** flake8 + mypy + `pytest tests/unit tests/integration --cov=src --cov-fail-under=80` — orçamento **≤ 5 min por push** (doc-user-story-011-us-011, spec-002-requisitos-review-round-1.spec.md:167; REQ-11 :72). Reduzir `timeout-minutes` do `test-suite` de 15 (ci.yml:111) para ≤5 e paralelizar é obrigação de implementação; enquanto não reduzido, doc-user-story-011-us-011 está **não atendido** (delta declarado, não contornado).
2. **Job `build-layers`:** `docker compose build` das imagens de `proxy`/`back`/`front` (+ verificação de que todo `image:` externo tem digest — Art. 10.2). Pode exceder os 5 min isolado; o orçamento ≤5min aplica-se ao feedback lint+testes por push (leitura de doc-user-story-011-us-011) — execução paralela ao job 1.
3. **Job `contract-network`:** sobe a stack efêmera e roda os casos §7.3 (marcador, ex.: `compose`). **Resolução C.4 (emenda TA-0061, hf-exec-0617):** o job **NÃO EXISTE** no `ci.yml` real (auditado 2026-11-03 — 189 linhas, 6 jobs: `kill-switch-check` :17, `foss-compliance` :36, `sdd-validation` :69, `agent-health` :91, `test-suite` :108, `final-status` :176; nenhum com esse nome — coerente com os fatos de §8 acima e spec-011 §3.1) e o nome foi **FIXADO como `contract-network` pela spec-011, como JOB NOVO a implementar** na onda seguinte (Art. 6.1): `needs: [test-suite]`, stack efêmera digest-pinned, `timeout-minutes` ≤10, sem porta no host, executando os 5 casos binários de §7.3 (spec-011:100-110; parcela TA-0048, hf-exec-0604:42 — "spec-011 FIXA nome contract-network como job novo").
4. **Gates nunca bypassados:** nenhum job pode ser pulado por label, `continue-on-error` ou re-run seletivo; cobertura <80% falha (ci.yml:170); merge exige reviewer → gatekeeper (P-06, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:94; Art. 10.4, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:219). "Automation serves gates, never bypasses them" (custódia declarada em .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-devops.md:6). GitHub Actions Free Tier é Bypass registrado (P-01, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:84) — não veta, mas exige registro.
5. **Zero bypass do kill switch:** o job `kill-switch-check` (ci.yml:17) permanece obrigatório e primeiro em qualquer extensão (Art. 4.6, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:124; veto absoluto herdado por todos os agentes).

---

## 9. Interoperabilidade: contrato declarado entre as três camadas

| Interface | Contrato | Versão/porta | Healthcheck de dependência |
|---|---|---|---|
| Dados → Back | PostgreSQL wire; schema gerido por Alembic (`migrations/`, Dockerfile:57-58; `upgrade`+`downgrade`, spec-004-backend-mvp-v1.spec.md:124); URL `COBECO_DATABASE_URL` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:17) | `db:5432`, porta interna, sem publicação no host | `db` `pg_isready` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:42-47) → `back` espera `service_healthy` (:65-67) |
| Front → Back | **API HTTP `/v1`** — mesmas rotas, schemas e erros de spec-004-backend-mvp-v1.spec.md §3: `GET /v1/health`, `GET /v1/rates/{currency}`, `POST /v1/simulate`, `POST /v1/invoice` (spec-004-backend-mvp-v1.spec.md:64-67); decimais como string JSON (:60); modelo de erro canônico (:79-93); OpenAPI servido pelo próprio FastAPI (REQ-14, spec-002-requisitos-review-round-1.spec.md:170; `tests/integration/test_openapi.py`) | `back:8000` interna; rota versionada `/v1`; nenhuma porta host para `back` (§4.3) | `front` espera `back` healthy (proposta §7.1); `back` responde `/v1/health` (compose:77-86) |
| proxy → Front/Back | Nginx `location` por caminho (`/` → front, `/v1/` → back) em `infra/nginx/default.conf` (hoje unificado em `web:8000`, default.conf:16) — serviço **sempre ativo** (§2) | `127.0.0.1:8080` host, porta 80 interna | `proxy` espera front/back healthy (hoje `web`, compose:93-95) e responde healthcheck na cadeia §7.1 |
| Estado persistente | Volume nomeado **único** `cobeco_pgdata` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:34, :118) — interface de volume declarada do Art. 10.1 | `/var/lib/postgresql/data` dentro de `db` | `db` healthy antes de `migrate`/`back` (compose:58-60, :65-67) |
| Configuração | Segredos/variáveis só por `config-env-0001-env-example-v1.0` → `environment` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:16-20) | — | Fail-closed sem `COBECO_DATABASE_URL` (spec-004-backend-mvp-v1.spec.md:134) |

**Compatibilidade com `/v1` (spec-004-backend-mvp-v1.spec.md §3):** a separação em camadas **não altera** rotas, schemas, enums, modelo de erro, nem a identidade `gross_brl − spread_brl − iof_brl == net_brl` (spec-004-backend-mvp-v1.spec.md:53), nem o `notice` (:77), nem `Content-Disposition` da invoice (:130). O `POST /v1/invoice` continua no **Back** (PDF é resposta da API, não página do Front). Testes de contrato existentes (`test_api_contract.py`, `test_openapi.py`) são a rede de segurança da migração.

---

## 10. User Stories (Padrão B — GWT)

Padrão B conforme `docs/conhecimento/OKB.md:539` (§7.4): título `US-NN — slug EN`, narrativa "Como/quero/para", contexto, ≥2 cenários Dado/Quando/Então, rastreabilidade, dependências, atribuição, status. Numeração **doc-user-story-018-us-018+** — doc-user-story-001-us-001..doc-user-story-017-us-017 já existem em `.ai/specs/spec-req-0001-requisitos-review-round-1-v1.0.md` (§C, :156-179).

**Nota de governança (Art. 5.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:138):** stories são candidatas de backlog; entram em `ready` só após refinement/CCB do Humano/PO (precedente: spec-002-requisitos-review-round-1.spec.md:149-152).

### doc-user-story-018-us-018 — orthogonal-container-layers-separation

**Narrativa:** Como orquestrador de infraestrutura, quero que o serviço `web` atual (Back+Front fundidos) seja separado nas camadas Dados, Back e Front — cada uma em container próprio —, para que sejam construídas, versionadas e reiniciadas de forma independente (Art. 10.1).

**Contexto:** hoje `db`+`migrate`+`web`(fundido)+`proxy` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:26,50,62,89); a SPEC exige `db`+`migrate`+`back`+`front` com fronteiras da §3.1.

**Cenários (Acceptance Criteria):**

1. **Dado** um clone limpo do repositório com `config-env-0001-env-example-v1.0` copiado de `config-env-0001-env-example-v1.0.example`, **Quando** executo `docker compose up --build`, **Então** sobem os serviços `db`, `migrate`, `back` e `front` (o serviço fundido `web` não existe mais) e cada camada reporta healthy pelo seu healthcheck (§7.1) em ≤60 s.
2. **Dado** a stack completa em execução, **Quando** executo `docker compose restart front` (ou `restart back`), **Então** as demais camadas continuam healthy, o volume `cobeco_pgdata` permanece intacto e o serviço reiniciado volta a responder seu healthcheck sem rebuild das outras camadas.
3. **Dado** a stack em execução, **Quando** consulto `GET /v1/health` pela origem única (§4.3), **Então** recebo `200 {"status":"ok"}` — prova de que a separação não quebrou o contrato `/v1`.

**Rastreabilidade (dupla):** Art. 10.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213) + ADR-010 Decisão 2 (ADR-010:65-66; consolidado em ADR-001-stack.md:18) | REQ-14 (spec-002-requisitos-review-round-1.spec.md:75) | hf-exec-0029 §Tarefa 1.
**Dependências:** SPEC aprovada (esta); implementação na onda seguinte (Art. 6.1). **Atribuição:** devops + docker-specialist; ≤8h ou tasklist (OKB.md:541, §7.5). **Status:** `candidate`.

### doc-user-story-019-us-019 — declared-network-topology-contract-tests

**Narrativa:** Como auditor de segurança, quero a topologia de redes declarada (`data` internal × `edge`) com matriz quem-fala-com-quem e testes de contrato de rede, para provar que a comunicação entre as três camadas é somente por interface declarada.

**Contexto:** `data` é `internal: true` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:112-113) e `edge` abre rota externa (:115); a matriz §4.2 é a norma desta SPEC.

**Cenários (Acceptance Criteria):**

1. **Dado** a stack levantada, **Quando** inspeciono a pertinência dos containers às redes, **Então** `db` e `migrate` só estão em `data`, `front` não é membro de `data`, `back` está em `data`+`edge` e nenhum serviço declara caminho de rede fora da matriz §4.2.
2. **Dado** o container `front` em execução, **Quando** tento abrir TCP para `db:5432` a partir dele, **Então** a conexão falha (sem rota — matriz #9) e o teste automatizado correspondente (§7.3) passa em verde.
3. **Dado** a stack em execução, **Quando** verifico `docker compose port db`, **Então** não há mapeamento de porta no host (matriz #10) e o teste negativo passa.

**Rastreabilidade (dupla):** Art. 10.1 + Art. 10.4 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213,219) + ADR-010 (redes: config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:110-115, comentário ADR-010:66) | REQ-08 (spec-002-requisitos-review-round-1.spec.md:69) | hf-exec-0029 §Tarefa 2.
**Dependências:** doc-user-story-018-us-018. **Atribuição:** digital-security + qa-sdet; ≤8h. **Status:** `candidate`.

### doc-user-story-020-us-020 — container-security-hardening-lgpd

**Narrativa:** Como digital-security, quero o bloco de hardening completo e verificável em todas as camadas (non-root, no-new-privileges, cap_drop ALL, read_only+tmpfs, portas 127.0.0.1, segredos só em config-env-0001-env-example-v1.0, digest pinning, LGPD), para que a produção ortogonal seja fail-closed por padrão.

**Contexto:** os controles já existem parcialmente no anchor `x-app` (config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:21-23) e no `Dockerfile` (Dockerfile:49-61); a SPEC exige que `back` e `front` os herdem integralmente (§6).

**Cenários (Acceptance Criteria):**

1. **Dado** as imagens das três camadas construídas, **Quando** executo inspeção (`docker compose config` + inspeção de container), **Então** `back`, `front` e `migrate` rodam com uid 10001 non-root, `no-new-privileges:true`, `cap_drop: [ALL]`, `read_only: true` + `tmpfs`, portas do host em `127.0.0.1` e imagens referenciadas por digest `sha256:` (exceções `db`/`proxy` apenas com as justificativas de config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:37-38 e :102-106).
2. **Dado** o scanner do CI e a revisão de logs da stack, **Quando** varro artefatos e saída de log, **Então** não há credencial real no repositório (Art. 7.2, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:176), nenhum PII em logs ou volumes de terceiros (Art. 10.3, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:217; spec-004-backend-mvp-v1.spec.md:126) e nenhum segredo embutido em camada de imagem (Art. 10.2, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:215).

**Rastreabilidade (dupla):** Art. 10.2 + Art. 10.3 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:215,217) + P-04/P-07 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90,96) + ADR-010 Governança (ADR-010:104 — registro de imagens) | REQ-15 FOSS (spec-002-requisitos-review-round-1.spec.md:76) | hf-exec-0029 §Tarefa 4.
**Dependências:** doc-user-story-018-us-018. **Atribuição:** digital-security + devops; ≤8h. **Status:** `candidate`.

### US-021 — ci-layer-build-test-gate

**Narrativa:** Como dev, quero pipeline de CI que execute lint+testes e build das camadas em ≤5 min por push com gates nunca bypassados, para fechar o delta de G-05 e sustentar coverage ≥80%.

**Contexto:** G-05 registrado como `ci.yml` vazio (plano-proddoc-arch-0006-uc-v1ao-agentes.md:33), arquivo hoje com 189 linhas e 6 jobs, porém sem build Docker e com `timeout-minutes: 15` no `test-suite` (ci.yml:111) — ver §8.

**Cenários (Acceptance Criteria):**

1. **Dado** um push em feature branch, **Quando** o pipeline executa, **Então** lint (flake8+mypy) + testes unit/contrato/integração + build das imagens `back`/`front`/`db` concluem com o feedback de lint+testes em ≤5 min (doc-user-story-011-us-011, spec-002-requisitos-review-round-1.spec.md:167) e qualquer falha bloqueia o merge.
2. **Dado** o report de cobertura do job, **Quando** a cobertura sobre `src/` fica <80%, **Então** `--cov-fail-under=80` (ci.yml:170) falha o job e o merge é impedido (doc-user-story-008-us-008, spec-002-requisitos-review-round-1.spec.md:164; P-06, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:94).
3. **Dado** qualquer job do pipeline, **Quando** alguém tenta pulá-lo por bypass/re-run seletivo, **Então** o gate reviewer → gatekeeper mantém o bloqueio (Art. 10.4, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:219) e o registro fica auditável — "Automation serves gates, never bypasses them" (.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-devops.md:6).

**Rastreabilidade (dupla):** Art. 10.4 + P-06 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:219,94) + ADR-010 CI (ADR-010:105 — PostgreSQL efêmero) | REQ-11 + REQ-08 (spec-002-requisitos-review-round-1.spec.md:72,69), doc-user-story-008-us-008/doc-user-story-011-us-011 (:164,:167), gap G-05 (plano-proddoc-arch-0006-uc-v1ao-agentes.md:33) | hf-exec-0029 §Tarefa 6.
**Dependências:** doc-user-story-018-us-018 (build das camadas); custódia `agent-devops` (G-05). **Atribuição:** devops; ≤8h ou tasklist (OKB.md:541). **Status:** `candidate`.

---

## 11. Critérios de aceite binários desta SPEC

| # | Critério (hf-exec-0029) | Como está atendido |
|---|---|---|
| 1 | Spec em `./.ai/specs/` com cabeçalho Status estilo `spec-004-backend-mvp-v1.spec.md` | Este arquivo; cabeçho Status no topo (estilo spec-004-backend-mvp-v1.spec.md:16) |
| 2 | Três camadas nomeadas + aderentes justificadas/recusadas | §3.1 (Dados/Back/Front) e §3.2 (migrate mantida, **proxy aceito e mantido** — §2, ratificação 2026-11-02 Art. 5.1; cache recusado por YAGNI) |
| 3 | Topologia de redes declarada + interface declarada única (Art. 10.1) | §4.1 (redes), §4.2 (matriz), §4.3 (origem única), citação constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:213 |
| 4 | Fluxo de reprodutibilidade passo a passo e local-only | §5 (`git pull` → `config-env-0001-env-example-v1.0` → `docker compose up --build`, CPU-only P-02) |
| 5 | Bloco de segurança completo | §6 (non-root, no-new-privileges, cap_drop, read_only+tmpfs, 127.0.0.1, segredos config-env-0001-env-example-v1.0, digest, LGPD) |
| 6 | Estratégia de testes por camada, coverage ≥80%, healthchecks | §7.1 (healthchecks), §7.2 (pirâmide + ≥80%), §7.3 (contrato de rede) |
| 7 | Pipeline CI/CD da fase citando G-05 e doc-user-story-011-us-011 | §8 (fatos G-05 delta + proposta ≤5min + gates) |
| 8 | Contrato de interoperabilidade entre as três camadas | §9 (tabela API/porta/volume/healthcheck + compatibilidade `/v1`) |
| 9 | ≥3 US Padrão B (doc-user-story-018-us-018+) com ≥2 AC cada e rastreabilidade | §10 (doc-user-story-018-us-018..US-021, 2-3 cenários Dado/Quando/Então cada, rastreabilidade dupla) |
| 10 | Proposta de UAT com fluxos críticos, critério de passagem e evidências | §12 |
| 11 | Conflito PostgreSQL vs SQLite resolvido por tabela de conflitos | §2 (linha 1: Constituição Art. 10.1 + ADR-010/ADR-001 v1.1.0 vencem; textos SQLite superados) |

---

## 12. Proposta de UAT

**Escopo:** validação das camadas Dados/Back/Front + aderentes (`migrate`, `proxy`) em ambiente local CPU-only (P-02), sobre a stack `docker compose up --build` da §5, cobrindo as fronteiras da §3 e a matriz da §4. Não cobre: regra de negócio já validada em outras stories, TLS, e2e de navegador (§7.2).

**Fluxos críticos (100% obrigatórios):**

| ID | Fluxo | Critério de passagem | Origem |
|---|---|---|---|
| F-01 | Reprodutibilidade: clone limpo → `config-env-0001-env-example-v1.0` de `config-env-0001-env-example-v1.0.example` → `docker compose up --build` (proxy incluído, sem `--profile`) sobe tudo sem intervenção extra e `127.0.0.1:8080` responde | Todos os serviços (incl. `proxy`) healthy em ≤5 min; demo via `127.0.0.1:8080` (§5) | §5; hf-exec-0029 §Tarefa 3; hf-exec-0030 §Tarefa 2 |
| F-02 | Simulação E2E: `POST /v1/simulate` com os 5 regimes retorna identidade monetária e decimais string | 100% dos regimes respondem 200 corretos | spec-004-backend-mvp-v1.spec.md:53-56; REQ-02 (spec-002-requisitos-review-round-1.spec.md:63) |
| F-03 | Invoice: `POST /v1/invoice` devolve PDF em ≤3 s | PDF válido, sem PII em logs | spec-004-backend-mvp-v1.spec.md:130; REQ-04 (:64) |
| F-04 | Isolamento: `front` não alcança `db:5432`; `db` sem porta no host | Testes negativos §7.3 passam | Art. 10.1; doc-user-story-019-us-019 |
| F-05 | Degradação: `db` parado → `back` responde 503 `rates_unavailable`/erro canônico sem crash e sem traceback | 503 canônico, sem PII | spec-004-backend-mvp-v1.spec.md:89-93 |
| F-06 | Migração: `alembic upgrade head` + `downgrade base` idempotentes via serviço `migrate` | Round trip limpo | config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0-v1.0.yml:52; spec-004-backend-mvp-v1.spec.md:124 |
| F-07 | Segurança: inspeção de todas as controles da §6 em todas as camadas | 100% controles presentes (exceções documentadas) | §6; doc-user-story-020-us-020 |

**Critério de passagem (binário, fail-closed):** **100% dos fluxos críticos F-01..F-07 passam** e existem **zero defeitos críticos ou bloqueantes** em aberto. Qualquer reprovado = UAT reprovada; defeitos não críticos vão ao backlog com severidade e decisão do PO (precedente doc-user-story-009-us-009 / REQ-09: "100% fluxos criticos, zero defeitos criticos/bloqueantes" — spec-002-requisitos-review-round-1.spec.md:165 e :70).

**Papéis:**

| Papel | Exercido por | Base |
|---|---|---|
| Executor | agent-qa-sdet (roteiro e execução) | Roster (Art. 2.2, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:58) |
| Revisor de segurança | agent-digital-security + agent-reviewer | precedente backend-mvp T9 (spec-004-backend-mvp-v1.spec.md:216) |
| Aprovador do resultado | Humano — GP via CCB (merge/release é ato humano) | Art. 5.3 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:142) |
| Stakeholder avaliador acadêmico | Prof. Dr. Nivaldo Carleto (canônico) | Art. 1.1 (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:27) |

**Evidências:** (i) log de execução por fluxo com timestamp e resultado pass/fail; (ii) screenshots do estado healthy por camada (`docker compose ps`); (iii) relatório de defeitos com severidade e status; (iv) artefato de cobertura ≥80% (ci.yml:170); (v) run do CI com duração ≤5 min por push (doc-user-story-011-us-011); (vi) saída dos testes de contrato de rede (§7.3). Destino/armazenamento das evidências: **decidido = `docs/uat/`, classificado por rodada (`docs/uat/rodada-NN/`), com relatório analítico por rodada (taxa de aceite, cobertura analizada, ciclo de implementação)** — decisão GP/CCB fechada em 05/11/2026 (pendência #6 resolvida). Formato: `relatorio-analitico.md` + `evidencias/<id>__US-<slug>__<yyyymmdd>__run<nn>.log|.png`, retenção permanente versionada em git, conteúdo exclusivamente sintético (P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90). Fonte: spec-009 §3.8.

---

## 13. Fora de escopo (YAGNI — P-11)

- Qualquer código, compose, Dockerfile, workflow ou ADR alterado nesta onda (Art. 6.1 — implementação é onda seguinte; restrição dos handoffs hf-exec-0029/hf-exec-0030).
- Emenda da ADR-010 ("Nginx latente", ADR-010:67) para refletir o proxy **aceito e mantido** — **follow-up pendente (arquiteto → CCB)**; ADR-010 não alterada nesta onda (ratificação GP/Humano 2026-11-02, Art. 5.1, registrada em §2).
- TLS/domínio, cache em serviço separado, Kubernetes, e2e de navegador, CDN de static, camada `app` extra de rede (§3.2, §4.1, §7.2).
- Alterações do contrato `/v1`, de regra de negócio ou de escopo congelado (Art. 1.3, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:31).
- SPEC das camadas L1 (runtime de agentes) e CI como camadas do Art. 10.1 — escopo a confirmar (§3.2, final).

## Conformidade desta emissão

- Arquivo único editado: `.ai/specs/spec-arch-0001-container-layers-v1.0.md` (custódia L1 de `./.ai/specs`, Art. 6/6.5). Nenhum outro arquivo alterado (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md, registry, ADRs, handoffs, compose, Dockerfile, workflows — intocados).
- Kill switch herdado (Art. 4.6, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:124); zero PII (P-04); 100% local, sem cloud/CUDA (P-02); slugs/IDs EN + narrativa PT-BR (P-10); alegações com `arquivo:linha` ou marcadas **UNKNOWN - verify** (P-08); nenhuma capacidade especulativa (P-11).
- Hierarquia respeitada: Constituição > ADR-010/ADR-001 v1.1.0 > planos > SDD (esta SPEC) > código (Art. 2.1, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:41-50).

## CHANGELOG

- 0.1.0 — 2026-11-02 (TA-0029, hf-exec-0029): emissão inicial. Três camadas (Dados/Back/Front) + aderentes justificadas; matriz de redes `data`×`edge`; reprodutibilidade local-only; bloco de segurança; testabilidade com contract tests de rede; CI com delta de G-05 declarado; contrato `/v1` preservado; 4 stories doc-user-story-018-us-018..US-021 (Padrão B, OKB.md:539); proposta de UAT F-01..F-07; tabela de conflitos com PostgreSQL vs SQLite.
- 0.2.0 — 2026-11-02 (TA-0030, hf-exec-0030): amenda cirúrgica. Promoção do proxy de "profile opcional latente" para **ACEITO E MANTIDO** (sempre ativo) por ratificação GP/Humano 2026-11-02 (Art. 5.1), registrada na tabela de conflitos §2; matriz §4.2 integrada em cadeia usuário → proxy → front → back → db (+ migrate) com healthchecks em cadeia (§4.2, §7.1); `front`/`back` sem porta no host e usuário somente via `proxy` em `127.0.0.1:8080` (§4.3, §6); caminho de demo em §5 (`git pull` → `cp config-env-0001-env-example-v1.0.example config-env-0001-env-example-v1.0` → `docker compose up --build` → `127.0.0.1:8080` → fluxos MVP, CPU-only); coerência em §8 (`build-layers` com `proxy`), §9, §11, §12 (F-01) e §13; ADR-010 não alterada — emenda listada como follow-up (arquiteto → CCB, §2/§13). doc-user-story-018-us-018..US-021, AC, segurança (§6) e UAT (§12) preservados.

- Normalização estrutural — 2026-11-02 (TA-0031, hf-exec-0031): frontmatter canônico (`spec_id: spec-005`), slug `container-layers-v1.spec.md` → `spec-005-container-layers-v1.spec.md` (mapa em `.ai/specs/doc-manifest-0001-manifest-v1.0.md`), mapa de camadas a–h. **Versão mantida 0.2.0**; amenda TA-0030 (proxy Nginx ACEITO E MANTIDO) preservada integralmente; nenhum conteúdo reescrito.
- 0.3.0 — 2026-11-03 (TA-0061, hf-exec-0617): emendas de conteúdo C.4+C.5 (docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:51,52). C.4 (§8.3): marcador do job `contract-network` substituído pela RESOLUÇÃO — job **inexistente** no `ci.yml` real (auditado 2026-11-03: 189 linhas, 6 jobs, nenhum com esse nome) e nome **FIXADO pela spec-011 §3.4 como job novo a implementar** (parcela TA-0048, hf-exec-0604:42). C.5 (§12): destino das evidências passa de `UNKNOWN - verify` para **"proposta emitida (spec-009 §3.8): `docs/uat/N6.2/`, retenção permanente — ratificação CCB/PO pendente"** (parcela TA-0047, hf-exec-0603:40); a reserva de decisão ao GP é mantida. Frontmatter: `version` 0.2.0 → 0.3.0; `updated` → 2026-11-03. **Amenda TA-0030 (proxy ACEITO E MANTIDO) e linha `Status:` preservadas integralmente**; nenhuma decisão reescrita; emendas in-place sem deslocamento de linhas (citações externas a `spec-005:210` e `spec-005:342` permanecem endereçáveis; valores `UNKNOWN - verify` residuais em :81 e :352 dizem respeito a B.10/spec-014 — fora do escopo desta emenda).
- 0.4.0 — 2026-11-05 (refinamento de ratificação, Grupo A): frontmatter atualizado ao padrão TA-0031 ratificado (adicionado `wave: WS-4`, `lgpd-class`, `trace`; `task` definido como TA-0030, `sender` separado; removido `sender` embutido em `origin`); `version` 0.3.0 → 0.4.0. Aderência ao padrão de nomenclatura `spec-NNN-specname.spec.md` confirmada (ADR-018, RAT-2026-11-05-A18). Proxy **sempre ativo** confirmado em config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0 (commit `abc7350`, separação `web` → `back`+`front`+proxy). Nenhuma decisão de negócio de §§1–13 reescrita. **Ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16)**.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem | frontmatter (`spec_id: spec-005`, `version: 0.4.0`) + linha `Status:` | aplicada |
| (b) Contexto/origem | §1 (origem: hf-exec-0029/TA-0029; amenda hf-exec-0030/TA-0030) | aplicada |
| (c) Resolução de conflitos | §2 | aplicada |
| (d) Corpo de decisões/requisitos/contratos | §§3–10 e §12 | aplicada |
| (e) Critérios de aceite/testes | §11 (AC binários) + §7 (testabilidade) + §12 (UAT F-01..F-07) | aplicada |
| (f) Rastreabilidade (REQ/ADR/Art./US) | blocos "Rastreabilidade (dupla)" das doc-user-story-018-us-018..US-021 (§10) + §11 | aplicada |
| (g) Fora de escopo (YAGNI) | §13 | aplicada |
| (h) Changelog | CHANGELOG (0.1.0, 0.2.0, 0.3.0 + anotação TA-0031) | aplicada |
