---
id: ai-specs-spec-007-invoice-data-model-v1-spec
title: SPEC spec-007 — invoice-data-model-v1 — Modelo canônico de dados da invoice (GAP-04)
type: spec
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/specs/spec-007-invoice-data-model-v1.spec.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- specs
- docs
- adequado-a-norma
---
---
spec_id: spec-007
specname: invoice-data-model-v1
version: 0.2.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-03
updated: 2026-11-05
origin: .ai/handoffs/HF-0608-spec-007-invoice-data-model-v1.md (envelope; item B.4 de docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:36)
task: TA-0052 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
lgpd-class: product-personal-financial (invoice transporta nome, CPF/CNPJ, endereço e valores — minimização P-04, constitution.md:90)
trace:
  - .ai/handoffs/HF-0608-spec-007-invoice-data-model-v1.md (envelope da tarefa)
  - .ai/handoffs/HF-0601-consulta-de-dominio.md:33-45 (PARCELA DE CONSULTA TA-0045, agent-dba — insumo normativo incorporado nos §§3.1-3.6)
  - .ai/handoffs/HF-0606-consulta-de-dominio.md:31-45 (parcela de consulta TA-0050, agent-compliance-governance — decisões D1-D7 como condicionantes, §2 e §3.0)
  - docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:36 (item B.4)
  - .ai/specs/spec-002-requisitos-review-round-1.spec.md:103 (GAP-04), :161 (US-004), :123 (C-04), :135 (OS-02), :178-179 (US-016/017)
  - .ai/specs/spec-004-backend-mvp-v1.spec.md:58-93 (§3 contrato), :120-130 (§5/§6), :33-56 (§2 regras)
  - docs/conhecimento/glossario.md:161-162 (PostgreSQL 15+ canônico; SQLite revogado — ADR-010)
  - constitution.md:90 (P-04)
---

# SPEC spec-007 — invoice-data-model-v1 — Modelo canônico de dados da invoice (GAP-04)

Status: RATIFICADA — contrato de dados canônico emitido; decisão de persistência = PERSISTIR (condicionante D1 resolvida por ADR-016 emenda D4, RAT-2026-11-05-A16-D4). Esta spec complementa a `spec-004-backend-mvp-v1.spec.md` (contrato HTTP `POST /v1/invoice`) e alimenta a US-004 (spec-002:161, "modelo de dados pendente — GAP-04").

## 1. Contexto e origem

Emitida por TA-0052 / HF-0608 (agent-nexus-prime-ultimate → agent-sdd-specialist, action: spec, 2026-11-03) para fechar o item **B.4** da rodada 1 de specs pendentes (LISTA-SPECS-PENDENTES-2026-11-02.md:36): o modelo de dados da invoice — campos bancários, CPF/CNPJ, período — **não é canônico** e sobrevive apenas no legado (GAP-04, spec-002:103, com origem nos corpora `deepseek:58; qwen:18`). A `spec-004` especifica o contrato `POST /v1/invoice` (spec-004:58-93). A decisão de persistência (ADR-016 D4, RAT-2026-11-05-A16-D4) é **PERSISTIR** com rota de erase; a `spec-004:126` ("invoice nunca é persistida") é superada por esta emenda. A US-004 (spec-002:161) é condicionada a este modelo; US-016/US-017 (spec-002:178-179) o demandam condicionalmente.

Insumo normativo: a **parcela de consulta TA-0045 (agent-dba)**, retornada no meio-duplex de `.ai/handoffs/HF-0601-consulta-de-dominio.md:33-45`, é incorporada neste documento como fonte de domínio de dados (tipagem, constraints, índices, LGPD e lista de UNKNOWNs). As decisões D1-D7 da parcela de consulta TA-0050 (agent-compliance-governance, `.ai/handoffs/HF-0606-consulta-de-dominio.md:40`) entram apenas como **condicionantes, não como requisitos aprovados** (precedente de leitura: `.ai/handoffs/HF-0621-requisitos-repovoar.md:36`).

## 2. Resolução de conflitos

| Tema | Decisão desta spec | Fonte vencedora | Texto superado / não promovido |
|---|---|---|---|
| **Persistência da invoice** (tensão obrigatória) | **DECIDIDA: PERSISTIR** com rota de erase (ADR-016 D4, RAT-2026-11-05-A16-D4). Esta spec define o **MODELO CANÔNICO de dados** (contrato de dados, §3). A decisão de persistência é norma vigente: invoices são gravadas na tabela `invoices`; rota de erase (direito ao esquecimento, LGPD art. 18) é obrigatória (condicionantes D1-D6 da spec-015). US-016/017 (spec-002:178-179) seguem KG-R-03, condicionadas à ratificação CCB. | ADR-016 D4 (RAT-2026-11-05-A16-D4) + HF-0608 | `spec-004:126` ("invoice nunca é persistida") **superada por esta emenda**; esta spec autoriza a migração de `invoices` (upgrade/downgrade Alembic, §3.4). |
| Banco canônico | PostgreSQL 15+ (ADR-010; glossario.md:161-162; spec-004:24 — resolução de conflitos da spec-004 §1) | ADR-010 via spec-004:24 + glossario.md:161-162 | SQLite do TAP congelado (plano-escopo.md:76, reproduzido em spec-002:123 e :135). Ratificação da ADR-010 por emenda Art. 1.3 é UNKNOWN - verify (§3.6, item 7). |
| CPF/CNPJ no banco × contrato | Banco: `tax_id_digits char(14)` normalizado sem máscara, dígito validado app-side (CHECK SQL não faz mod-11) — parcela TA-0045 (HF-0601). Contrato HTTP continua `tax_id: str|None ≤40` (spec-004:74); normalização é responsabilidade da camada de aplicação. Contrato não é alterado por esta spec. | Parcela TA-0045 (HF-0601) para o banco; spec-004:74 para o contrato | Divergência de formato tratada por fronteira de normalização app-side; sem reescrita da spec-004. |
| Endereço (coleta) | Parcela TA-0050 (inventário mínimo, HF-0606:40) propõe endereço "só se necessário à finalidade REQ-04"; parcela TA-0045 modela `address varchar(240) NULL`. Resolução: colunas **NULLable** (não NOT NULL) — a modelagem NULL **não decide** a coleta; obrigatoriedade de coleta é a condicionante **D4** (CCB/PO). | HF-0606:40 (D4) + HF-0601 | Nenhuma decisão de coleta promovida. |
| Valores da invoice | Servidor **recalcula** a simulação e as colunas de valores devem casar com o reprocesso (parcela TA-0045; spec-004:128-130 §6). Nenhum valor pronto do cliente é aceito nem persistido. | spec-004:128-130 + HF-0601 | Qualquer esquema de valores informados pelo cliente. |

## 3. Modelo de dados (domínio)

### 3.0 Condição de vigência (D1)

O §3 é o **contrato de dados canônico** da invoice. A condicionante D1 foi **deliberada = PERSISTIR** (ADR-016 emenda D4, RAT-2026-11-05-A16-D4). O §3 **materializa DDL/migração/execução**: a tabela `invoices` pode ser criada via migração Alembic (`upgrade`/`downgrade`, §3.4). A emissão deste contrato de dados autoriza o runtime da `spec-004` a persistir invoices.

### 3.1 Entidade `invoices` (se e somente se D1 = persistir)

Tabela única `invoices`; fonte primária = parcela TA-0045 (HF-0601:42); campos marcados `[alinhamento]` derivam do contrato `spec-004` (não constavam da parcela).

| Campo | Tipo | Constraints | Fonte |
|---|---|---|---|
| `id` | bigint | PK, identity | HF-0601 (parcela TA-0045) |
| `invoice_number` | varchar(40) | NOT NULL | HF-0601; limite 1-40 do contrato (spec-004:75) |
| `issue_date` | DATE | NOT NULL | HF-0601; tipo `date` do contrato (spec-004:75) |
| `description` | varchar(500) | NOT NULL | [alinhamento] spec-004:75 (1-500); ausente da parcela TA-0045 — delta registrado em §3.7 |
| `issuer_name` | varchar(120) | NOT NULL | HF-0601; contrato `name` 1-120 (spec-004:74) |
| `issuer_tax_id_digits` | char(14) | NULL; CHECK `char_length IN (11,14)`; dígito validado app-side (mod-11 fora do CHECK SQL) | HF-0601 |
| `issuer_address` | varchar(240) | NULL | HF-0601; contrato `address ≤240` (spec-004:74) |
| `client_name` | varchar(120) | NOT NULL | HF-0601; spec-004:74 |
| `client_tax_id_digits` | char(14) | NULL; CHECK `char_length IN (11,14)`; dígito app-side | HF-0601 |
| `client_address` | varchar(240) | NULL | HF-0601; spec-004:74 |
| `periodo_inicio` | DATE | NOT NULL | HF-0601; **ausente de `InvoiceRequest`** (spec-004:75) — delta §3.7 |
| `periodo_fim` | DATE | NOT NULL; CHECK `periodo_fim >= periodo_inicio` | HF-0601; delta §3.7 |
| `regime` | varchar | CHECK IN (`hourly`,`daily`,`weekly`,`monthly`,`fixed`) | HF-0601; enum `Regime` (spec-004:60) |
| `currency` | char(3) | CHECK IN (`USD`,`EUR`) | HF-0601; enum `Currency` (spec-004:60) |
| `amount` | numeric(18,2) | CHECK `> 0`; contrato: ≤ 1.000.000.000, máx. 2 casas | HF-0601; spec-004:72 |
| `quantity` | numeric(12,2) | NULL; obrigatória `>0` em hourly/daily/weekly/monthly, proibida em `fixed` — cruzamento regime↔quantity no app (spec-004:41-42, :72); CHECK SQL do cruzamento não especificado na parcela → app-side | HF-0601; spec-004:41-42 |
| `spread_pct` | numeric(6,4) | CHECK `0–100` | HF-0601; spec-004:72 (0 a 100, máx. 4 casas) |
| `iof_pct` | numeric(6,4) | CHECK `0–100` | HF-0601; spec-004:72 |
| `gross_foreign` | numeric(18,2) | CHECK `> 0` (contrato: bruto que arredonda a 0.00 é erro, spec-004:199) | [alinhamento] derivável de §2 (spec-004:46) e `Breakdown` (spec-004:162); ausente da parcela — delta §3.7 |
| `gross_brl` | numeric(18,2) | NOT NULL | HF-0601; fórmula spec-004:47 |
| `spread_brl` | numeric(18,2) | NOT NULL | HF-0601; fórmula spec-004:48 |
| `iof_brl` | numeric(18,2) | NOT NULL | HF-0601; fórmula spec-004:49 |
| `net_brl` | numeric(18,2) | NOT NULL | HF-0601; fórmula spec-004:50 |
| `effective_rate` | numeric(18,6) | NOT NULL | HF-0601; fórmula spec-004:51 |
| `created_at` | timestamptz | NOT NULL; `DEFAULT now()` explícito | HF-0601 |
| `banco` | char(3) | NULL; só se o template US-004 exigir (minimização P-04) | §3.3 [alinhamento] |
| `agencia` | varchar(10) | NULL; só se o template US-004 exigir (minimização P-04) | §3.3 [alinhamento] |
| `conta_com_digito` | varchar(20) | NULL; só se o template US-004 exigir (minimização P-04) | §3.3 [alinhamento] |
| `pix_key` | varchar(77) | NULL; só se o template US-004 exigir (minimização P-04) | §3.3 [alinhamento] |

### 3.2 Tipagem e aritmética

- **NUNCA `float`/`REAL` para dinheiro** (parcela TA-0045, HF-0601); no domínio, `Decimal` sempre (spec-004:35).
- Arredondamento `ROUND_HALF_EVEN`, 2 casas em valores, 6 casas em taxas (spec-004:35).
- Identidade obrigatória re-verificada na persistência: `gross_brl − spread_brl − iof_brl == net_brl` (spec-004:53).

### 3.3 Dados bancários (mínimos — P-04)

Conjunto **mínimo** (parcela TA-0045, HF-0601): `banco char(3)`, `agencia varchar(10)`, `conta_com_digito varchar(20)`, `pix_key varchar(77) NULL`. Declados na tabela §3.1 como colunas **NULL** (não-mandatórias), incluídos somente quando o template US-004 exigir (minimização P-04, constitution.md:90). Os **campos bancários exatos do template legado são `UNKNOWN - verify`** (§3.7, item 2) — nenhuma coluna bancária é mandatória nesta emissão.

### 3.4 Constraints, índices e integridade (parcela TA-0045)

- PK identity bigint; `UNIQUE (issuer_tax_id_digits, invoice_number)` — a parcela escreve `UNIQUE (issuer_tax_id, invoice_number)` (HF-0601); com a nomenclatura de §3.1, mapeia para `issuer_tax_id_digits`.
- Servidor recalcula a simulação (spec-004:128-130 §6); as colunas de valores **casam com o reprocesso**.
- **NENHUM índice além de PK/UNIQUE** até `EXPLAIN QUERY PLAN` real (HF-0601).
- FKs explícitas com `ON DELETE`/`ON UPDATE` se e quando surgirem (HF-0601).
- Migrações Alembic com `upgrade` e `downgrade` obrigatórias (HF-0601; spec-004:124); acesso via Repository Protocol (spec-004:124); regra de negócio fora de SQLAlchemy (HF-0601; spec-004:124).

### 3.5 Enumerações canônicas (alinhadas à spec-004 §3)

| Enum | Valores | Fonte |
|---|---|---|
| `Currency` | `USD` \| `EUR` | spec-004:60 |
| `Regime` | `hourly` \| `daily` \| `weekly` \| `monthly` \| `fixed` | spec-004:60; 5 regimes do escopo canônico (spec-002:120, C-01) |
| `RateSource` | `frankfurter` \| `ptax` | spec-004:60 |

`RateSource` é citada para alinhamento; **a parcela TA-0045 não especificou colunas de cotação persistida** (rate, source, quoted_at, bulletin) — lacuna declarada em §3.7.

### 3.6 LGPD (P-04, constitution.md:90)

- `tax_id` e dados bancários só com consentimento/base legal (HF-0601; candidata primária art. 7, V para dados de terceiros — D3, HF-0606:40).
- Sem PII, sem valores e sem corpo de requisição em logs (spec-004:126; critério de produto sob Art. 7 + P-04 — D5, HF-0606:40).
- Se D1 = persistir: rota **DELETE com direito ao esquecimento por design é obrigatória** (HF-0601; D6, HF-0606:40); retenção é D6 — `UNKNOWN - verify` (§3.6, item 6).
- Seeds/fixtures sintéticos (HF-0601; spec-004:155 — "Dados de teste são sintéticos").
- Backups sem PII ou exclusão documentada; sem secrets em rows (HF-0601).
- Drift registrado pela parcela: P-04 está em `constitution.md:90` (o handoff HF-0601:27 citava `constitution.md:36` — correção feita aqui).

### 3.7 Deltas entre contrato e modelo (registrados nesta emissão; sem edição da spec-004)

1. `periodo_inicio`/`periodo_fim` existem no modelo (HF-0601) mas **não em `InvoiceRequest`** (spec-004:75) — extensão do contrato condicionada a D1 e a decisão de semântica do período (§3.8, item 5).
2. `description` e `gross_foreign` constam do contrato/derivação (spec-004:75, :46) mas não da parcela TA-0045 — incorporados por [alinhamento] em §3.1.
3. Cotação usada (rate, source, quoted_at, bulletin): reprodutibilidade do reprocesso (§3.4) dependeria dessas colunas — **não definidas pela parcela TA-0045** → `UNKNOWN - verify` (lacuna declarada nesta emissão, ausente da lista de 7 da parcela).
4. Coluna de estado (rascunho/finalizada): US-016/017 são KG-R-03 não ratificadas (spec-002:178-179) → `UNKNOWN - verify` (declarada nesta emissão).

### 3.8 UNKNOWN - verify (P-08 — sem invenção)

Os 7 itens declarados pela parcela TA-0045 (HF-0601:42):

1. **Persistência da invoice** — `spec-004:126` "nunca persistida" × spec-007 → decisão CCB/PO (**D1**); depende de B.3 (LGPD de produto, spec-015 draft).
2. **Campos bancários exatos do template** (só legado, corpora via spec-002:103).
3. **Numeração** global × por emissor/ano (C-04, spec-002:123 — solução de numeracao única; PostgreSQL canônico reabre a questão sem exigir "sem Sequence").
4. **`tax_id` aceita CPF, CNPJ ou ambos** (CHECK IN (11,14) cobre ambos; a regra de negócio não está decidida).
5. **Semântica do período por regime** (hourly × fixed).
6. **Retenção** (D6).
7. **Ratificação da ADR-010** via emenda Art. 1.3 (TAP congelado diz SQLite — plano-escopo.md:76 via spec-002:123,:135).

Mais 2 lacunas declaradas nesta emissão (não cobertas pela parcela): reprodutibilidade da cotação para reprocesso (§3.7.3) e coluna de estado US-016/017 (§3.7.4).

## 4. Critérios de aceite e testes

**Validador:** agent-reviewer (verificação de spec) e agent-gatekeeper (gate). **DoD desta emissão:** arquivo único criado + parcela JSON retornada ao orquestrador (contrato HF-0608:27-29).

Critérios de spec (vigentes agora):

- [ ] O arquivo `.ai/specs/spec-007-invoice-data-model-v1.spec.md` existe, com frontmatter conforme MANIFEST §1.1 e ≤ 400 linhas (contrato agent-sdd-specialist §0.2 RESOURCE).
- [ ] Toda afirmação de domínio cita `arquivo:linha` OU está marcada literal `UNKNOWN - verify` (P-08, constitution.md:98).
- [ ] Toda coluna de §3.1 tem fonte citada (parcela TA-0045/HF-0601, spec-004:NN, ou marcador `[alinhamento]`).
- [ ] Nenhuma decisão CCB pendente é promovida: D1 aparece como condicionante em §2 e §3.0; nenhum DDL/migração é autorizado nesta spec.
- [ ] A tensão `spec-004:126` × modelo de dados está registrada na tabela de Resolução de conflitos (§2) com fonte vencedora e texto superado.

Critérios de implementação (CONDICIONAIS a D1 = persistir; **bloqueados até lá** — nenhum é executável hoje):

- [ ] Migração Alembic com `upgrade` e `downgrade` cria/derruba `invoices` conforme §3.1-§3.4; teste roda em PostgreSQL com marcador `postgres` (spec-004:155).
- [ ] CHECKs de banco rejeitam: `currency` fora de `USD|EUR`; `regime` fora dos 5 enums; `periodo_fim < periodo_inicio`; `amount <= 0`; `spread_pct`/`iof_pct` fora de 0-100; `tax_id_digits` com `char_length` fora de (11,14).
- [ ] Property test: linha persistida × reprocesso server-side (spec-004 §6) reproduz `gross_brl`, `spread_brl`, `iof_brl`, `net_brl`, `effective_rate` e a identidade de spec-004:53.
- [ ] Teste de LGPD: nenhum PII/valor em logs na rota de persistência (spec-004:126; D5, HF-0606:40); rota de erase existe se D1 exigir retenção+erase (D6).
- [ ] Seeds/fixtures exclusivamente sintéticos (spec-004:155; HF-0601).
- [ ] Nenhum índice além de PK/UNIQUE sem `EXPLAIN QUERY PLAN` registrado que o justifique (HF-0601).

## 5. Rastreabilidade

| Fonte | Onde nesta spec |
|---|---|
| B.4 / GAP-04 (LISTA-SPECS-PENDENTES-2026-11-02.md:36; spec-002:103) | §1, §3.1 |
| US-004 (spec-002:161) | H1/Status, §1, §3.3, §4 |
| US-016/US-017 KG-R-03 (spec-002:178-179) | §2 (linha persistência), §3.7.4, §3.8 |
| Parcela TA-0045 agent-dba (HF-0601:33-45) | §2, §3.1-§3.6, §3.8.1-7, §4 (condicionais) |
| Parcela TA-0050 compliance, D1-D7 (HF-0606:40) | §2, §3.0, §3.5, §3.6 |
| spec-004 §2/§3/§5/§6 (spec-004:33-56, :58-93, :120-130) | §2, §3.1, §3.2, §3.4, §3.5, §3.7, §4 |
| ADR-010 / glossario.md:161-162 (PostgreSQL 15+ canônico) | §2 (linha banco), §3.4 |
| C-04 (spec-002:123) e OS-02 (spec-002:135) | §2 (linha banco), §3.8.3 |
| P-04 (constitution.md:90) | frontmatter `lgpd-class`, §3.3, §3.6 |
| Art. 1.3 / Art. 2 (constitution.md:31, :37-50) | §2 (linha banco), §3.8.7 |
| P-08 (constitution.md:98) | §3.7, §3.8, §4 |

## 6. Fora de escopo (YAGNI)

- **Implementação**: DDL final, models ORM, repositório e migração são execução pós-D1 (custódia agent-dba/backend-dev; precede a spec-004 §9, T3) — esta spec é contrato de dados, não código.
- **Edição da spec-004**: o contrato `POST /v1/invoice` (spec-004:58-93) não é alterado por aqui; extensões (§3.7) exigem nova task própria.
- **Ciclo de estados da invoice** (US-016/017, spec-002:178-179): não ratificado (KG-R-03) — decisão CCB; nada de coluna `status` aqui.
- **NF-e/NFS-e** (OS-05, spec-002:138) e plataformas de transferência (OS-04, spec-002:137): OUT do escopo congelado.
- **Política de retenção/backup**: decisão D6 + B.3 (LGPD de produto, spec-015) — aqui só se referencia.
- **Histórico de simulações**: fora do escopo declarado da spec-004 (spec-004:31).
- **Numeração via PostgreSQL Sequence ou similar**: solução de numeração é UNKNOWN (§3.8.3) — nada é decidido aqui.

## CHANGELOG

- 0.1.0 — 2026-11-03 (TA-0052, HF-0608): emissão inicial. Template canônico MANIFEST §1 (camadas a-h). Insumo normativo incorporado: parcela de consulta TA-0045 (agent-dba, HF-0601:33-45) — entidades, campos, constraints, índices, LGPD e 7 UNKNOWNs; condicionantes D1-D7 da parcela TA-0050 (HF-0606:40) citadas sem promoção de decisão. Tensão `spec-004:126` ("invoice nunca é persistida") × modelo de dados registrada em §2 como condicionante CCB/PO (D1); status draft. Dois deltas adicionais declarados nesta emissão (§3.7.3-§3.7.4). Nenhum outro arquivo editado; nada commitado.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem | frontmatter (`spec_id: spec-007`, `version: 0.2.0`, `status: ratificada`) | aplicada |
| (b) Contexto/origem | §1 + frontmatter `origin`/`task` | aplicada |
| (c) Resolução de conflitos | §2 (tensão persistência D1; banco; CPF/CNPJ; endereço; valores) | aplicada |
| (d) Corpo de decisões/requisitos/contratos | §3 (§3.0-§3.8: entidades, campos, tipos, constraints, índices, validações, enumerações) | aplicada |
| (e) Critérios de aceite/testes | §4 (spec vigentes + implementação condicionais a D1) | aplicada |
| (f) Rastreabilidade | §5 + frontmatter `trace` | aplicada |
| (g) Fora de escopo (YAGNI) | §6 | aplicada |
| (h) Changelog | CHANGELOG | aplicada |
