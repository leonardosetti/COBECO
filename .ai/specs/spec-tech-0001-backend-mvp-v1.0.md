---
id: spec-tech-0001-backend-mvp-v1.0
type: spec-tech
title: SPEC TECH — Backend Mvp
version: v1.0
status: ratificado
canonical: false
canonical_slug: backend-mvp
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
spec_id: spec-004
specname: backend-mvp-v1
version: 1.2.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-01
updated: 2026-11-05
origin: commit f6e0455 (2026-11-01, "docs(spec): especificar backend do MVP") + .ai/handoffs/hf-exec-0500-backend-mvp-v1.0.md
task: TA-0042 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
wave: WS-4 | Onda 4 — Execução Técnica (backend implementação)
lgpd-class: n/a (zero PII neste artefato; P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90)
trace:
  - .ai/handoffs/hf-exec-0500-backend-mvp-v1.0.md (registro de execução T1–T14)
  - docs/decisoes/adr-016-backend-mvp.md (ADR-016, fórmula spread/IOF ratificada)
  - constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md (Art. 2, P-02, P-03, P-04, P-06, P-07)
  - ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16-D4, ADR-LOG-010)
---

# SPEC spec-004 — backend-mvp-v1 — Backend do MVP COBECO (REQ-01 a REQ-05, REQ-07, REQ-14)

Status: IMPLEMENTADA EM BRANCH, COM COMMITS LOCAIS, PENDENTE DE PUSH E MERGE | Branch: `feat/backend-mvp` | Orquestrador: agent-nexus-prime-ultimate

Fonte única das decisões do backend. Em conflito, vale a hierarquia do Art. 2 da Constituição.

## 1. Resolução de conflitos documentais

| Tema | Decisão | Fonte vencedora | Texto superado |
|---|---|---|---|
| Banco | PostgreSQL 15+, SQLAlchemy async, asyncpg, Alembic | Constituição 10.1, ADR-010, Delta REQ-07 | ADR-001 e prompts dba/backend-dev/python (SQLite) |
| Cotação | Frankfurter primária; PTAX fallback obrigatório | ADR-010 §4 | desenvolvimento.md (PTAX primária) |
| Pydantic | v2 (exigido pelo FastAPI atual) | Código de terceiros | prompt api-specialist ("v1-style") |
| Dependências | Permitidas via ADR-010 §6, registradas em `docs/dependencias/registro.md` | ADR-010 §6 | prompts "stdlib + FastAPI only" |
| Python | `>=3.11`; ambiente local e CI usam 3.12 | CI vigente | prompt python-specialist ("pinned 3.11") |
| Spread/IOF | Informados pelo usuário; nenhuma alíquota no código | Plano de Riscos RE-04 | ADR-016 §D1 |

Fora do escopo: autenticação, cadastro, histórico de simulações, comparador Wise, telas (N5.3).

## 2. Regras de negócio (REQ-02, REQ-03)

Dinheiro é sempre `Decimal`; `float` é proibido. Arredondamento `ROUND_HALF_EVEN`, 2 casas nos valores em moeda; taxas com 6 casas.

Bruto estrangeiro por regime:

| regime | Fórmula | quantity |
|---|---|---|
| `hourly`, `daily`, `weekly`, `monthly` | `amount × quantity` | obrigatória, > 0 |
| `fixed` | `amount` | proibida |

Com `rate` = cotação em BRL por 1 unidade estrangeira:

1. `gross_foreign = q2(bruto)`
2. `gross_brl = q2(gross_foreign × rate)`
3. `spread_brl = q2(gross_brl × spread_pct / 100)`
4. `iof_brl = q2((gross_brl − spread_brl) × iof_pct / 100)`
5. `net_brl = gross_brl − spread_brl − iof_brl`
6. `effective_rate = q6(net_brl / gross_foreign)`

Propriedade obrigatória: `gross_brl − spread_brl − iof_brl == net_brl` em toda resposta.

Exemplo sintético: USD, `hourly`, amount 30, quantity 160, rate 5.000000, spread 2, iof 0.38 →
gross_foreign 4800.00, gross_brl 24000.00, spread_brl 480.00, iof_brl 89.38 (23520 × 0,0038 = 89,376), net_brl 23430.62, effective_rate 4.881379.

## 3. Contrato HTTP `/v1`

Decimais trafegam como string JSON. Enums: `Currency = USD|EUR`; `Regime = hourly|daily|weekly|monthly|fixed`; `RateSource = frankfurter|ptax`.

| Verbo | Rota | Entrada | Saída | Erros |
|---|---|---|---|---|
| GET | `/v1/health` | — | 200 `{"status":"ok"}` | — |
| GET | `/v1/rates/{currency}` | path `Currency` | 200 `RateQuote` | 400, 503 |
| POST | `/v1/simulate` | `SimulationRequest` | 200 `SimulationResponse` | 400, 503 |
| POST | `/v1/invoice` | `InvoiceRequest` | 200 `application/pdf` | 400, 503 |

Schemas em `src/shared/schemas.py` (SSOT, `extra="forbid"`):

- `RateQuote`: `currency`, `rate`, `source`, `quoted_at` (datetime UTC), `bulletin: str|None`, `stale: bool`.
- `SimulationRequest`: `currency`, `regime`, `amount` (>0, máx. 2 casas, ≤ 1.000.000.000), `quantity: Decimal|None` (>0, máx. 2 casas, ≤ 100.000), `spread_pct` e `iof_pct` (0 a 100, máx. 4 casas). Validador cruza `regime` e `quantity` (§2).
- `SimulationResponse`: `currency`, `regime`, `gross_foreign`, `gross_brl`, `spread_brl`, `iof_brl`, `net_brl`, `effective_rate`, `spread_pct`, `iof_pct`, `quote: RateQuote`, `notice: str`.
- `InvoiceParty`: `name` (1–120), `tax_id: str|None` (≤40), `address: str|None` (≤240).
- `InvoiceRequest`: `simulation: SimulationRequest`, `issuer: InvoiceParty`, `client: InvoiceParty`, `invoice_number` (1–40), `issue_date: date`, `description` (1–500).

`notice` é constante: "Simulação de caráter informativo; spread e IOF foram informados pelo usuário e não substituem a orientação de um profissional habilitado."

Modelo canônico de erro (todas as falhas, inclusive validação, 404 e 500):

```json
{"error": {"key": "validation_error", "message": "Dados inválidos.", "details": [{"field": "amount", "message": "..."}]}}
```

| HTTP | key | Quando |
|---|---|---|
| 400 | `validation_error` | Corpo, path ou enum inválidos (substitui o 422 do FastAPI) |
| 404 | `not_found` | Rota inexistente |
| 503 | `rates_unavailable` | Sem fonte disponível e sem cache |
| 503 | `pdf_unavailable` | WeasyPrint/Pango ausente ou falha de renderização |
| 500 | `internal_error` | Inesperado, sem traceback nem dados do usuário |

Mensagens em PT-BR. `details` nunca ecoa o valor enviado.

## 4. Cotações (REQ-01, REQ-07)

Adapter `RateProvider` (Protocol) com `async fetch(currency) -> RateQuote`.

- **Frankfurter:** `GET https://api.frankfurter.dev/v1/latest?base=USD&symbols=BRL` → `{"amount":1.0,"base":"USD","date":"2026-10-30","rates":{"BRL":5.4325}}`. `quoted_at` = meia-noite UTC de `date`; `bulletin=None`.
- **PTAX:** OData `CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)` com `@moeda='USD'`, janela dos últimos 7 dias (datas `MM-DD-YYYY`), `$top=1`, `$orderby=dataHoraCotacao desc`, `$format=json`. Usa `cotacaoCompra` (o profissional vende moeda) e `tipoBoletim` em `bulletin`. `dataHoraCotacao` vem em `YYYY-MM-DD HH:MM:SS.ffffff`, horário de Brasília (`America/Sao_Paulo`), e é convertido para UTC. Janela sem linhas é falha da fonte.
- JSON lido com `parse_float=Decimal` para não passar por binário.

Aceite de cotação (anti-envenenamento, kill switch DBA 5): `Decimal` finito, `0 < rate < 1000`. Fora disso é falha da fonte e nada é gravado.

Fluxo de `RateService.get_quote(currency)`:

1. Cache com idade ≤ `COBECO_RATE_TTL_SECONDS` (padrão 3600) → devolve sem chamar a rede. A idade conta de `fetched_at`.
2. Entra na fila da moeda (single-flight). Quem esperou e viu uma cadeia terminar herda o desfecho dela. Quem assume relê o cache, salvo se a primeira leitura falhou, e percorre a cadeia Frankfurter → PTAX, pulando provedor com circuito aberto. Sdoc-arch-0006-uc-v1esso grava e devolve.
3. Falha geral: última linha do cache com `stale=true`.
4. Sem cache: `RatesUnavailableError` (503).

Circuit breaker por provedor, em memória: abre após 3 falhas consecutivas e fica aberto por 60 s; depois admite uma tentativa. Relógio injetável. Cancelamento e corte pelo prazo da cadeia liberam a tentativa com `record_release`, sem contar como falha da fonte.

Orçamento de REQ-01: prazo total de 1,9 s por requisição (`total_timeout`), contado da chegada e válido inclusive na fila. Cada chamada ao repositório tem até 0,3 s (`repository_timeout`); estouro equivale a cache ausente na leitura e a gravação ignorada na escrita. Timeout por provedor de 0,9 s, com a cadeia inteira encerrada em t = 1,6 s, o que reserva 0,3 s à gravação. Pior caso: leitura 0,3 + releitura 0,3 + cadeia até 1,6 + gravação 0,3 = 1,9 s; a PTAX recebe o que restar depois da Frankfurter (0,1 a 0,7 s) enquanto o circuito desta não abre, e 0,9 s depois disso. Sem esse corte, 0,3 + 1,8 + 0,3 somariam 2,4 s.

Circuit breaker do repositório (`repository_breaker`), distinto dos provedores: abre após 3 estouros ou `RepositoryError` consecutivos e admite uma sonda a cada 5 s; sdoc-arch-0006-uc-v1esso fecha e cancelamento usa `record_release`. Aberto, leitura e gravação são puladas sem tocar no repositório: a leitura conta como cache ausente e a gravação é ignorada, com um registro por queda (`quote_cache_skipped`), não por requisição. Nesse período não há cache vencido para devolver, e sem fontes a resposta é 503. O circuito existe porque a consulta de DNS de um banco parado leva cerca de 3,8 s e não para quando a chamada é cortada: no uvloop ela ocupa o pool do libuv, compartilhado com o DNS das fontes. A primeira onda, anterior à abertura, ainda chega a 16 consultas, e o libuv padrão só admite 2 simultâneas; por isso a imagem define `UV_THREADPOOL_SIZE=64` no `Dockerfile`.

Seguidores herdam o desfecho do líder, inclusive falha: cotação, ou cache vencido próprio, ou 503, sem repetir a cadeia. O single-flight vale por processo, e o desfecho herdado vale só para quem chegou antes de a cadeia terminar.

## 5. Persistência (somente cotações)

Tabela `fx_quotes`: `id` bigint PK; `currency char(3)` com CHECK; `rate numeric(18,6)` CHECK `> 0`; `source varchar(20)`; `bulletin varchar(40)` NULL; `quoted_at timestamptz`; `fetched_at timestamptz`. Índice `(currency, fetched_at DESC)`. Retenção em manutenção futura; só há dados públicos.

Acesso via Repository (`QuoteRepository` Protocol), como exige o kill switch da ADR-010. Regra de negócio não importa SQLAlchemy. Migrações Alembic com `upgrade` e `downgrade`.

**LGPD:** invoice é persistida na tabela `invoices` (modelo canônico em spec-007 §3.1; ADR-016 D4, RAT-2026-11-05-A16-D4). Cada usuário pode gerar, armazenar persistentemente, baixar e imprimir a invoice conforme sua regra de jornada e rating de pagamento. Nomes, documentos e endereços são gravados na invoice com minimização (P-04, LGPD art. 6º III) e rota de erase (direito ao esquecimento, LGPD art. 18) é obrigatória (condicionantes D1-D6 da spec-015). Logs não trazem valores nem corpo de requisição.

## 6. Invoice (REQ-04)

`POST /v1/invoice` recalcula no servidor a simulação recebida; não aceita valores prontos do cliente. Template Jinja2 `src/frontend/templates/invoice.html`, com autoescape ativo, em PT-BR, exibindo partes, descrição, regime, cotação com fonte, data e boletim, valores e `notice`. Renderiza com WeasyPrint em threadpool, com `import` tardio para a API subir sem Pango, e `url_fetcher` que recusa tudo, sem recursos remotos. Resposta com `Content-Disposition: attachment; filename="invoice.pdf"`.

## 7. Configuração e segurança

Variáveis: `COBECO_DATABASE_URL`, `COBECO_RATE_TTL_SECONDS`, `COBECO_PROVIDER_TIMEOUT_SECONDS`, `COBECO_LOG_LEVEL`. Sem valor padrão de banco que contenha credencial real; ausência de `COBECO_DATABASE_URL` falha ao iniciar (fail-closed). O scanner do CI varre `src/` e `tests/` e rejeita `password=` literal em `.py`, `.yml` e `.yaml`: monte URLs sem esse padrão. `config-env-0001-env-example-v1.0.example` exige exceção `!**/config-env-0001-env-example-v1.0.example` no `.gitignore`. Compose publica portas só em `127.0.0.1`. Sem CORS: o frontend é servido na mesma origem.

## 8. Estrutura

```
src/shared/schemas.py            contrato
src/backend/main.py              app, lifespan, handlers de erro
src/backend/config.py            Settings
src/backend/errors.py            exceções de domínio
src/backend/routers/{health,rates,simulations,invoices}.py
src/backend/services/calculator.py   puro
src/backend/services/rate_providers.py
src/backend/services/circuit_breaker.py
src/backend/services/rate_service.py
src/backend/services/simulation_service.py
src/backend/services/invoice_service.py
src/backend/models/quote.py  models/database.py  models/repository.py
migrations/
tests/unit/  tests/integration/
```

Testes não usam rede nem relógio real. Integração com PostgreSQL usa `COBECO_TEST_DATABASE_URL` e marcador `postgres`. Cobertura ≥ 80 % sobre `src/`. Dados de teste são sintéticos. `tests/agents/` não é alterado.

## 8.1 Assinaturas internas (contrato entre T5, T6 e T7)

```python
# services/calculator.py (puro)
@dataclass(frozen=True)
class Breakdown: gross_foreign; gross_brl; spread_brl; iof_brl; net_brl; effective_rate  # Decimal
def calculate(regime, amount, quantity, rate, spread_pct, iof_pct) -> Breakdown

# services/circuit_breaker.py
class CircuitBreaker:
    def __init__(self, failure_threshold=3, reset_seconds=60.0, clock=time.monotonic)
    def allow(self) -> bool
    def record_sdoc-arch-0006-uc-v1cess(self) -> None
    def record_failure(self) -> None
    def record_release(self) -> None  # chamada sem veredito: libera a tentativa, sem penalizar

# services/rate_providers.py
class ProviderError(Exception)  # toda falha de fonte, inclusive timeout e aceite reprovado
class RateProvider(Protocol):
    name: RateSource
    async def fetch(self, currency: Currency) -> RateQuote
class FrankfurterProvider:  __init__(self, client: httpx.AsyncClient, timeout: float)
class PtaxProvider:         __init__(self, client: httpx.AsyncClient, timeout: float, today=<callable -> date>)

# services/rate_service.py
class RateService:
    def __init__(self, repository, providers: list[tuple[RateProvider, CircuitBreaker]],
                 ttl_seconds: int, now=<callable -> datetime UTC>,
                 repository_timeout: float = 0.3, total_timeout: float = 1.9,
                 repository_breaker: CircuitBreaker | None = None)  # padrão: 3 falhas, reset 5 s
    async def get_quote(self, currency: Currency) -> RateQuote

# services/simulation_service.py
async def simulate(request: SimulationRequest, rate_service: RateService) -> SimulationResponse

# services/invoice_service.py
async def render_invoice(request: InvoiceRequest, rate_service: RateService) -> bytes
```

Regras adicionadas na T2:

- `RateQuote` rejeita taxa com mais de 6 casas; o provedor quantiza com `q6` antes de montá-la. `ValidationError` no provedor vira `ProviderError`.
- Bruto que arredonda para 0.00 é erro de validação (`gross_rounds_to_zero`), o que evita divisão por zero em `effective_rate`.
- `SimulationResponse` valida a identidade do §2 e o `notice`.
- Corpos JSON são lidos com `parse_float=Decimal`, pois `json.loads` padrão colapsaria literais longos em `float` antes do schema.
- O handler de validação usa só `loc` e mensagem PT-BR, nunca `input` nem `ctx`, e traduz erros nativos da Pydantic por `type`. Em `extra_forbidden`, o nome da chave enviada não é ecoado.

## 9. Tarefas

| ID | Agente | Modelo | Entrega |
|---|---|---|---|
| T1 | python-specialist | Sonnet 5.5 | pyproject, requirements, registro de dependências, config.py |
| T2 | api-specialist | Opus 5.5 | schemas.py, errors.py |
| T3 | dba | Sonnet 5.5 | modelos, repositório, Alembic |
| T4 | devops + docker-specialist | Sonnet 5.5 | Dockerfile, compose, config-env-0001-env-example-v1.0.example, CI |
| T5 | qa-sdet | Haiku 5.5 | Testes unitários e de contrato (primeiro) |
| T6 | backend-dev | Opus 5.5 | Serviços de cálculo, cotação e circuit breaker |
| T7 | backend-dev | Sonnet 5.5 | Routers, main.py, invoice |
| T8 | qa-sdet | Haiku 5.5 | Testes de integração e fechamento de cobertura |
| T9 | digital-security + reviewer | Sonnet 5.5 | Revisão de segurança e código |
| T10 | architect (redação) | Haiku 5.5 | ADR-016 proposta, doc-readme-0001-readme-canon, status nos planos, handoff |
| T11 | backend-dev | Opus 5.5 | Timeouts do repositório, single-flight, prazo total, circuit breaker do repositório |
| T12 | devops + backend-dev | Sonnet 5.5 | Desconexão do cliente, endurecimento do compose, lint e Alembic no CI, .gitignore |
| T13 | qa-sdet | Haiku 5.5 | Teste instável, testes do circuit breaker do repositório e do lifespan |

---

## 10. Contexto e origem (camada b)

Spec de fonte única das decisões do backend, anterior à implementação na branch `feat/backend-mvp`: commit `f6e0455` (2026-11-01, "docs(spec): especificar backend do MVP") e registro de execução das tarefas em `.ai/handoffs/hf-exec-0500-backend-mvp-v1.0.md` (§9, `status: blocked` — única pendência declarada é a ratificação da ADR-016, ato humano do CCB). Decisão de stack correlata: `docs/decisoes/ADR-016-backend-mvp.md:18`. Handoff de criação da spec: `UNKNOWN - verify` (não há envelope `task-ta-*.json` correspondente em `.ai/handoffs/`).

## 11. Critérios de aceite e testes (camada e)

Histórico: esta SPEC não possuía seção própria de critérios de aceite antes da normalização TA-0031 — nada foi inventado então (marcador vigente até a emenda TA-0061, hf-exec-0617); a evidência observável então registrada permanece válida (docstrings dos testes citam esta spec por seção: `tests/integration/test_api_contract.py:1` → §2, §3; `tests/unit/test_calculator.py:1` → §2, §3; T5/T8 de §9 definem quem entrega os testes). Emenda TA-0061 (C.1): os critérios abaixo consolidam, em forma binária verificável, ACs **já existentes no corpo** (§§2–9) — nenhum requisito novo; o que o corpo não fundamenta permanece `UNKNOWN - verify` (P-08).

- [ ] **AC-01** — toda resposta de `POST /v1/simulate` satisfaz `gross_brl − spread_brl − iof_brl == net_brl` (verificação: teste de propriedade sobre `calculate`/`SimulationResponse`). Fonte: §2:53, §8.1:200.
- [ ] **AC-02** — dinheiro é exclusivamente `Decimal` com `ROUND_HALF_EVEN` (`float` proibido), 2 casas em valores de moeda e 6 casas em taxas; `RateQuote` rejeita taxa com mais de 6 casas (verificação: grep de `float` em `services/calculator.py` = zero matches + teste de quantização). Fonte: §2:35, §8.1:198.
- [ ] **AC-03** — o exemplo sintético canônico (USD, `hourly`, amount 30, quantity 160, rate 5.000000, spread 2, iof 0.38) produz `net_brl` 23430.62 e `effective_rate` 4.881379 (verificação: caso golden no teste unitário). Fonte: §2:55-56.
- [ ] **AC-04** — bruto que arredonda para 0.00 rejeita a requisição com `gross_rounds_to_zero` (verificação: teste de validação). Fonte: §8.1:199.
- [ ] **AC-05** — cotação fora do aceite `Decimal` finito e `0 < rate < 1000` é falha da fonte e nada é gravado (verificação: teste com rate 0, 1000 e NaN). Fonte: §4:103.
- [ ] **AC-06** — cache vigente (idade ≤ `COBECO_RATE_TTL_SECONDS`, padrão 3600) responde sem chamada externa; sem cache e sem fonte → 503 `rates_unavailable`; cache vencido é devolvido com `stale=true` (verificação: teste com relógio injetável). Fonte: §4:107-110.
- [ ] **AC-07** — circuit breaker de provedor abre após 3 falhas consecutivas por 60 s; breaker do repositório abre após 3 estouros/`RepositoryError` com sonda a cada 5 s; seguidores herdam o desfecho do líder (verificação: testes dos breakers com relógio injetável). Fonte: §4:112,116,118.
- [ ] **AC-08** — orçamento de cotação: `total_timeout` de 1,9 s por requisição, `repository_timeout` de 0,3 s, cadeia de provedores encerrada em t=1,6 s e timeout por provedor de 0,9 s (verificação: teste de timeout com relógio fake). Fonte: §4:114.
- [ ] **AC-09** — provedores cumprem o contrato de parsing: Frankfurter (`quoted_at` = meia-noite UTC de `date`, `bulletin=None`) e PTAX (`cotacaoCompra`, `tipoBoletim` em `bulletin`, conversão para UTC; janela sem linhas é falha da fonte), com JSON lido em `parse_float=Decimal` (verificação: testes unitários com as respostas de exemplo de §4). Fonte: §4:99-101, §8.1:201.
- [ ] **AC-10** — schemas do contrato `/v1` vivem unicamente em `src/shared/schemas.py` com `extra="forbid"`; campo desconhecido → 400 `validation_error` (verificação: teste de contrato). Fonte: §3:69,87.
- [ ] **AC-11** — toda falha (400/404/503/500) responde no modelo canônico de erro com mensagem PT-BR, sem traceback e sem ecoar o valor enviado; handler de validação usa só `loc` (nunca `input`/`ctx`) (verificação: testes de contrato de erro). Fonte: §3:79-93, §8.1:202.
- [ ] **AC-12** — `POST /v1/invoice` recalcula a simulação no servidor e não aceita valores prontos do cliente (verificação: teste com corpo adulterado rejeitado). Fonte: §6:130.
- [ ] **AC-13** — invoice em PDF com `Content-Disposition: attachment; filename="invoice.pdf"`, template com autoescape ativo e `url_fetcher` que recusa todo recurso remoto (verificação: teste de integração). Fonte: §6:130.
- [ ] **AC-14** — invoice não é persistida; nomes/documentos/endereços não aparecem em logs; logs não trazem valores nem corpo de requisição (verificação: revisão dos logs dos testes de integração; política LGPD de produto é objeto da spec-015, proposta). Fonte: §5:126.
- [ ] **AC-15** — ausência de `COBECO_DATABASE_URL` impede a inicialização da API (fail-closed); compose publica portas só em `127.0.0.1`; sem CORS (verificação: teste de boot sem a variável + leitura do compose). Fonte: §7:134.
- [ ] **AC-16** — testes sem rede nem relógio real; integração com PostgreSQL via `COBECO_TEST_DATABASE_URL` e marcador `postgres`; dados 100% sintéticos; `tests/agents/` não alterado (verificação: convenção de fixtures). Fonte: §8:155.
- [ ] **AC-17** — migrações Alembic completam o round-trip `upgrade`/`downgrade` (verificação: teste de round-trip; análogo ao F-06 da spec-005 §12). Fonte: §5:124.
- [ ] **AC-18** — cobertura ≥ 80 % sobre `src/`, fail-closed no CI (`--cov-fail-under=80`, ci.yml:170) (verificação: run do CI). Fonte: §8:155.

`UNKNOWN - verify` (sem base no corpo desta spec — não inventado): medição de latência em ambiente real (o corpo fixa apenas orçamentos nominais, §4:114); quantidade de casos de teste por endpoint; aceite formal destes critérios pelo reviewer (spec em `status: in_progress`, pendente de push/merge).

## 12. Rastreabilidade consolidada (camada f)

| Fonte | Onde nesta spec |
|---|---|
| REQ-01, REQ-07 | §4 Cotações (título da seção) |
| REQ-02, REQ-03 | §2 Regras de negócio (título) |
| REQ-04 | §6 Invoice (título) |
| REQ-05, REQ-14 | declarados no H1 ("REQ-01 a REQ-05, REQ-07, REQ-14"); seção dedicada `UNKNOWN - verify` |
| ADR-016 | §9, tarefa T10 (proposta de ADR) + `docs/decisoes/ADR-016-backend-mvp.md:18` |
| Art. 2 (Constituição) | §1 (hierarquia de resolução de conflitos, parágrafo introdutório) |

## 13. Fora de escopo (camada g)

Escopo negativo já declarado em §1 (parágrafo "Fora do escopo: autenticação, cadastro, histórico de simulações, comparador Wise, telas (N5.3)" — telas de front são objeto da spec-008, spec-008:28). Emenda TA-0061 (C.2) — exclusões adicionais derivadas do corpo e do corpus da rodada, por cross-ref, **sem promover decisão nova** (P-11):

- **Persistência de invoice / modelo de dados estendido (condicionante D1)** — invoice é persistida na tabela `invoices` (modelo canônico em spec-007 §3.1; ADR-016 D4, RAT-2026-11-05-A16-D4). Cada usuário pode gerar, armazenar persistentemente, baixar e imprimir a invoice conforme sua regra de jornada e rating de pagamento. Rota de erase (direito ao esquecimento, LGPD art. 18) é obrigatória (condicionantes D1-D6 da spec-015). O modelo de dados da invoice é objeto da spec-007 e não altera o contrato §3 desta spec.
- **Política LGPD de produto (B.3)** — objeto da spec-015, emitida como PROPOSTA `draft` condicionada a ratificação CCB/PO (envelope `.ai/handoffs/hf-exec-0616-spec-015-lgpd-produto-proposta-v1-v1.0.md`); esta spec retém apenas o critério vigente de §5:126.
- **NFR consolidados (NF-01..NF-10)** — norma da spec-006 (NF-01..NF-04 em spec-006:71-74; NF-05 :80; NF-07 :87; NF-10 :90); esta spec cita apenas os orçamentos que já fixa no corpo (ex.: 1,9 s em §4:114).
- **UAT de produto (REQ-09, fase N6.2)** e **UAT de camadas** — plano/roteiro normados pela spec-009 (spec-009 §3) e pela spec-005 §12 (F-01..F-07); esta spec não define UAT.
- **Pipeline CI/CD detalhado (REQ-11)** — norma da spec-011 (spec-011 §3) e da spec-005 §8; esta spec consome apenas o gate de cobertura (§8:155, ci.yml:170).
- **Documentação técnica (REQ-14)** — doc de arquitetura e revisão formal da OpenAPI são objeto da spec-013 (spec-013:32); a seção dedicada à REQ-14 nesta spec permanece `UNKNOWN - verify` (§12).
- **Retenção de dados de `fx_quotes`** — §5:122 declara a retenção "em manutenção futura"; política de retenção não é decisão desta spec.

## 14. CHANGELOG (camada h)

- 1.0.0 — 2026-11-02 (TA-0031, hf-exec-0031): versionamento inicial + template canônico (camadas a–h). Conteúdo pré-existente preservado integralmente (origem: commit `f6e0455`, 2026-11-01); slug antigo `backend-mvp-v1.spec.md` → `spec-004-backend-mvp-v1.spec.md` (mapa em `.ai/specs/doc-manifest-0001-manifest-v1.0.md`); nenhuma decisão reescrita; `status: in_progress` mapeado da linha `Status:` original (IMPLEMENTADA EM BRANCH, PENDENTE DE PUSH E MERGE).
- 1.1.0 — 2026-11-03 (TA-0061, hf-exec-0617): emendas de conteúdo C.1+C.2 (docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:49,50). C.1: §11 preenchida com 18 critérios binários (AC-01..AC-18) consolidados exclusivamente do corpo pré-existente (§§2–9) — nenhum requisito novo; itens sem base no corpo permanecem `UNKNOWN - verify` (§11, final). C.2: §13 preenchida com exclusões YAGNI por cross-ref (spec-007/D1, spec-015 proposta via hf-exec-0616, spec-006, spec-009, spec-011, spec-013, retenção `fx_quotes`) — nenhuma decisão nova promovida. Frontmatter: `version` 1.0.0 → 1.1.0; `updated` → 2026-11-03. Mapa de camadas (e) atualizado por coerência. Nenhuma decisão de §§1–9 reescrita. Deslocamento de linhas: §§11/13 expandidas — linhas ≥ 231 do arquivo deslocam (citações externas às linhas ≥ 231, ex.: LISTA item B.9 → `spec-004:239`, resolvem-se pela leitura de §/seção).
- 1.2.0 — 2026-11-05 (refinamento de ratificação, Grupo A): frontmatter atualizado ao padrão TA-0031 ratificado (adicionado `wave: WS-4`, `lgpd-class`, `trace`; `task` definido como TA-0042; removido `creation_handoff` não-padrão); `version` 1.1.0 → 1.2.0. Seção 13 (Fora de escopo) corrigida: persistência de invoice agora segue D4 da ADR-016 (PERSISTIR com rota de erase, RAT-2026-11-05-A16-D4) em vez de "nunca persistida". Aderência ao padrão de nomenclatura `spec-NNN-specname.spec.md` confirmada (ADR-018, RAT-2026-11-05-A18). **Ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16)**. Nenhuma decisão de negócio de §§1–9 reescrita.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem | frontmatter (`spec_id: spec-004`, `version: 1.2.0`) | aplicada |
| (b) Contexto/origem | §10 + frontmatter `origin` + parágrafo introdutório | aplicada |
| (c) Resolução de conflitos | §1 | aplicada |
| (d) Corpo de decisões/requisitos/contratos | §§2–9 | aplicada |
| (e) Critérios de aceite/testes | §11 | aplicada (emenda TA-0061: AC-01..AC-18 binários consolidados do corpo §§2–9; sem seção própria pré-TA-0031 — histórico em §11) |
| (f) Rastreabilidade | §12 + títulos das §§2–6 | aplicada |
| (g) Fora de escopo (YAGNI) | §13 + §1 | aplicada |
| (h) Changelog | §14 | aplicada (criada em TA-0031) |
