---
id: ai-specs-spec-015-lgpd-produto-proposta-v1-spec
title: 'SPEC spec-015 — lgpd-produto-proposta-v1 — PROPOSTA: critérios LGPD de produto (B.3/GAP-08) — sujeita a ratificação
  CCB/PO'
type: spec
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/specs/spec-015-lgpd-produto-proposta-v1.spec.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- specs
- docs
- adequado-a-norma
---
---
spec_id: spec-015
specname: lgpd-produto-proposta-v1
version: 0.2.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-03
updated: 2026-11-05
origin: .ai/handoffs/HF-0616-spec-015-lgpd-produto-proposta-v1.md (envelope; item B.3 de docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:35)
task: TA-0060 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
lgpd-class: dados-pessoais
trace:
  - .ai/handoffs/HF-0616-spec-015-lgpd-produto-proposta-v1.md (envelope da tarefa)
  - .ai/handoffs/HF-0606-consulta-de-dominio.md:31-45 (PARCELA DE CONSULTA TA-0050, agent-compliance-governance — fundamentos LGPD e decisões D1-D7, incorporadas nos §§3-4)
  - docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:35 (B.3), :67 (E.1 — obsoleta, ver §2 e D7)
  - .ai/specs/spec-002-requisitos-review-round-1.spec.md:107 (GAP-08), :19 (lgpd-class precedente), :134 (OS-01), :161 (US-004), :178-179 (US-016/017), :201 (DoR item 10)
  - constitution.md:27 (Art. 1.1 — LGPD primária), :90 (P-04), :124 (Art. 4.6), :136-142 (Art. 5.1/5.4), :172-178 (Art. 7), :215 (Art. 10.2), :226, :229, :245 (ratificação E-01..E-08 e consolidação v1.2.1)
  - .ai/specs/spec-004-backend-mvp-v1.spec.md:122 (fx_quotes), :126 (LGPD: invoice nunca persistida; logs), :128-130 (§6 invoice)
  - .ai/specs/spec-007-invoice-data-model-v1.spec.md:26, :38, :41, :46-48, :114, :130, :157 (spec irmã B.4 — condicionante D1)
  - .ai/specs/spec-001-constitution-round-1-proposta.spec.md:213-219 (E-02), :238-239 (E-03)
  - LGPD Lei 13.709/2018 — art. 4º, I; art. 5º, II; art. 6º, I/III; art. 7º, V; art. 11; art. 18 (citação por artigo, §6)
---

# SPEC spec-015 — lgpd-produto-proposta-v1 — PROPOSTA: critérios LGPD de produto (B.3/GAP-08) — sujeita a ratificação CCB/PO

Status: **RATIFICADA (D1) / PROPOSTA (D2-D7)**. A decisão D1 (persistência da invoice) foi ratificada por ADR-016 emenda D4 (RAT-2026-11-05-A16-D4) = **PERSISTIR** com rota de erase. As decisões D2-D7 permanecem como condicionantes de ratificação CCB/PO (constitution.md:138, Art. 5.1). A LISTA condiciona a emissão de B.3 a decisão prévia de CCB/PO para D2-D7 (`docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:35`).

## 1. Contexto e origem

### 1.1 Origem

Emitida por TA-0060 / HF-0616 (agent-nexus-prime-ultimate → agent-sdd-specialist, action: spec, 2026-11-03) para tratar o item **B.3** da rodada 1 de specs pendentes (`docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:35`): os critérios LGPD de produto — minimização e tratamento de dados pessoais/financeiros na invoice e nos logs — ausentes dos REQ-01..15 (GAP-08, `spec-002-requisitos-review-round-1.spec.md:107`: "Sem criterio LGPD de produto: invoice carrega dados pessoais/financeiros (legado deepseek:58) e REQ-01..15 nao contemplam minimizacao/tratamento LGPD — requer decisao CCB/PO"), sob a **P-04** (constitution.md:90: "mínimo necessário, sem PII em artefatos técnicos de agentes; direito ao esquecimento por design").

### 1.2 Natureza de PROPOSTA (não ratificada)

1. A decisão D1 (persistência da invoice) foi ratificada por ADR-016 emenda D4 (RAT-2026-11-05-A16-D4) = **PERSISTIR** com rota de erase. As decisões D2-D7 permanecem condicionadas a decisão prévia de CCB/PO (LISTA:35); o item B.3 fecha com a deliberação humana sobre D2-D7.
2. Os fundamentos técnicos-compliance vêm da parcela de consulta TA-0050 (agent-compliance-governance, `.ai/handoffs/HF-0606-consulta-de-dominio.md:31-45`), incorporada aqui por citação nos §§3-4. A parcela declara expressamente: "Esta parcela NAO autoriza emissao aprovada" (HF-0606:40).
3. Nenhuma seção deste documento promove decisão: §4 lista as sete decisões CCB/PO pendentes (D1-D7) como **condicionantes de ratificação**.
4. Quem valida: **agent-reviewer** valida a conformidade documental desta emissão (template MANIFEST §1, citações, sem promoção de decisão); **CCB/PO** ratifica ou devolve o conteúdo (constitution.md:138, Art. 5.1). DoD desta emissão: proposta draft emitida com D1-D7 incorporadas, zero decisão promovida.

## 2. Resolução de conflitos

| Tema | Registro nesta PROPOSTA | Fonte | Texto/estado superado |
|---|---|---|---|
| **Persistência da invoice (D1)** | Tensão declarada, NÃO decidida: `spec-004:126` ("invoice nunca é persistida") × US-016/US-017 + GAP-04 (spec-002:161, :178-179). Enquanto D1 não for deliberada, vigora `spec-004:126`; nenhuma alternativa ("transitória" × "persistida com retenção+erase") é promovida aqui. | HF-0606:40 (D1); `spec-007-invoice-data-model-v1.spec.md:38, :46-48, :130` (spec irmã desta rodada, mesma leitura) | Nenhum texto é reescrito: `spec-004:126` permanece vigente; esta spec não o edita. |
| **Drift E.1 da LISTA** | E-01..E-08 **já foram ratificadas em 26/10/2026** — constitution v1.1.0 (CHANGELOG constitution.md:226; co-assinatura constitution.md:245), v1.2.1 vigente (constitution.md:229). A linha E.1 da LISTA (`:67`, "pendentes de CCB") está **obsoleta**; sua correção é a condicionante D7. | HF-0606:40 ("DRIFT DETECTADO (Art. 2.5)"); constitution.md:226, :245 | `docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:67` (E.1) perde eficácia como condicionante de emissão. |
| **Localização de P-04** | P-04 reside hoje em constitution.md:90. As citações `constitution.md:36` em `spec-002:107`, LISTA:35 e HF-0616:23 são referências históricas pré-consolidação v1.2.1 (constitution.md:229 consolidou Arts. 5-10 duplicados). | constitution.md:90 (verificado 2026-11-03); constitution.md:229 | Referência numérica `constitution.md:36` (histórica). |
| **Dados sensíveis × dados comuns** | CPF/dados bancários são dados pessoais **comuns** (LGPD art. 5º, II) — NÃO sensíveis (art. 5º, VI); o regime agravado do art. 11 não se aplica; base legal suficiente é do art. 7º. | HF-0606:40 ("basta base art. 7, sem regime art. 11") | Qualquer leitura de "dados financeiros = dados sensíveis". |
| **Modelo de dados da invoice** | A coleta de campos é matéria do modelo canônico (B.4 — spec-007, draft, condicionada à mesma D1/D4); esta spec fixa apenas os critérios LGPD que o modelo deve satisfazer. | LISTA:36 (B.4); spec-007:26, :38 | Duplicação do contrato de dados aqui (YAGNI — §7). |

## 3. Critérios LGPD de produto — PROPOSTA de domínio (não ratificada)

> Todo o §3 é conteúdo **proposto** (status: draft), derivado da parcela TA-0050 (HF-0606:40) e dos artefatos citados. Nenhum item é requisito executável antes da ratificação CCB/PO (Art. 5.1, constitution.md:138).

### 3.1 Minimização na invoice (LGPD art. 6º, I/III)

1. **Inventário mínimo PROPOSTO** (HF-0606:40): nome (partes), CPF/CNPJ, período, descrição e valores — nenhum campo além deste inventário deve ser coletado ou exibido pela invoice (princípio da necessidade, art. 6º, III; finalidade determinada, art. 6º, I).
2. **Endereço condicional** (HF-0606:40): coletado "só se necessário à finalidade REQ-04". A spec-007 irmã modela o campo como NULLable — a modelagem NULL não decide a coleta (spec-007:41); a obrigatoriedade é a condicionante **D4**.
3. **Classificação**: CPF/dados bancários = dados pessoais comuns (art. 5º, II), não sensíveis (art. 5º, VI) — regime do art. 11 não se aplica (HF-0606:40; §2).
4. **Reconciliação com o contrato atual**: o template vigente exibe "partes, descrição, regime, cotação com fonte, data e boletim, valores e `notice`" (spec-004:130); o modelo canônico de dados (spec-007, §3) alimenta o inventário final — o conjunto mínimo ratificado em D4 deve ser incorporado lá (B.4), não aqui.
5. **UNKNOWN - verify** (HF-0606:40): a invoice inclui dados de **terceiros/cliente**? (modelo GAP-04 inexistente; "partes" em spec-004:130) — determina qual cenário do §3.4 se aplica.

### 3.2 Tratamento em logs — critério de produto (D5)

1. **PROPOSTA** (HF-0606:40): os logs de produto **não contêm PII, não contêm valores e não contêm corpo de requisição** — elevando o que hoje é nota de implementação da spec-004:126 ("Nomes, documentos e endereços só existem durante a requisição e nunca vão para log. Logs não trazem valores nem corpo de requisição.") a **critério de produto verificável** (D5), sob o Art. 7 da constitution (constitution.md:172-178 — segurança e privacidade) + P-04 (constitution.md:90).
2. O critério permanece cumulativo com `spec-004:126`: esta proposta não rebaixa nem substitui a exigência vigente — torna-a auditável como aceite de produto (D5, §4).
3. **UNKNOWN - verify** (HF-0606:40): retenção de `fx_quotes` — dados públicos de cotação (spec-004:122), fora do alcance da LGPD; retenção é matéria de manutenção futura, não de critério LGPD.

### 3.3 Direito ao esquecimento por design (LGPD art. 18)

1. **Contexto verificado**: MVP single-user/local, sem autenticação (OS-01, spec-002:134; P-02/P-03, constitution.md:86, :88) — o usuário É o titular; o acesso do titular é trivial (HF-0606:40).
2. **PROPOSTA**: erasure é operação **local**, sem propagação remota (HF-0606:40) — direito de eliminação (art. 18, IV e VI) atendido por design, sem portal de titular, por ser escopo single-user (§7).
3. **Cenário D1 = persistir**: a rota de erase (DELETE) torna-se **obrigatória**, com política de retenção ratificada (D6; `spec-007:114` — "rota DELETE com direito ao esquecimento por design é obrigatória (HF-0601; D6)"; retenção `UNKNOWN - verify` em spec-007:114/§3.6). Teste de LGPD na rota de persistência espelhando spec-007:157.
4. **Cenário D1 = transitória** (vigora hoje, spec-004:126): a eliminação se dá por **não-persistência** — o PDF existe só durante a requisição (spec-004:126, :130) e o descarte local é ato do próprio titular.

### 3.4 Bases legais propostas (LGPD art. 7º)

1. **Cenário A — invoice com dados de TERCEIROS (cliente)** (HF-0606:40): base legal primária PROPOSTA = **art. 7º, V** (execução de contrato ou procedimentos preliminares relacionados a contrato do qual seja parte o titular). A ratificação é a condicionante **D3**.
2. **Cenário B — só dados do próprio usuário** (HF-0606:40): avaliar a **exclusão do alcance da LGPD pelo art. 4º, I** (tratamento "para fins exclusivamente particulares e não econômicos") — questão jurídica nova, requer revisão humana; decisão **D2**.
3. **UNKNOWN - verify** (HF-0606:40): aplicabilidade do art. 4º, I; **CNPJ fora do escopo LGPD — confirmar** (pessoa jurídica não é titular do art. 5º, II, mas pode identificar pessoa natural — confirmar antes de ratificar D3/D4).

### 3.5 `lgpd-class` em artefatos de agente

1. **PROPOSTA** (HF-0606:40): todo artefato técnico de agente que produz ou transporta dados de produto declara `lgpd-class` no frontmatter — tornando a triagem P-04 (constitution.md:90, "sem PII em artefatos técnicos de agentes") auditável por metadado.
2. **Precedentes citados**: `spec-002:19` (`lgpd-class: n/a (zero PII neste artefato; P-04)`) e DoR item 10 (`spec-002:201`: "Screen LGPD: sem PII no card/artefato de agente; dados de produto minimizados (P-04)"). Exemplo de valor para artefato que toca dados de produto: `dados-pessoais` (este frontmatter) — a taxonomia de valores segue o uso dos precedentes (`n/a` × classe do dado), sem enumeração nova nesta rodada.
3. Artefatos de agente continuam PROIBIDOS de carregar PII real (P-04; kill switch LGPD, constitution.md:124 — Art. 4.6).

### 3.6 Delimitação (dados fora do alcance)

Cotações de câmbio em `fx_quotes` são dados públicos (moeda, taxa, fonte, boletim — spec-004:122): fora do alcance da LGPD; qualquer política de retenção ali é de manutenção futura, não critério LGPD (HF-0606:40, UNKNOWN - verify).

## 4. Condicionantes de ratificação (OBRIGATÓRIA) — decisões D1-D7 pendentes do CCB/PO

A parcela TA-0050 (agent-compliance-governance, HF-0606:40) enumera as **DECISOES CCB/PO ANTES DA RATIFICACAO DE B.3 (Art. 5.1)**. Nenhuma foi deliberada; esta PROPOSTA não ratifica nada e permanece `status: draft` até deliberação humana (constitution.md:138):

| # | Decisão pendente CCB/PO | Fonte |
|---|---|---|
| **D1** | **Persistência da invoice** — **DECIDIDO = PERSISTIR** com rota de erase (ADR-016 D4, RAT-2026-11-05-A16-D4). Supera `spec-004:126` ("invoice nunca é persistida"). | HF-0606:40; spec-007:38, :46-48, :130; ADR-016 D4 |
| **D2** | **Controlador/titular e exclusão art. 4º, I** — decidir se o tratamento é para fins exclusivamente particulares e não econômicos (exclusão art. 4º, I) ou se há controlador/terceiros no tratamento. | HF-0606:40; §3.4.2 |
| **D3** | **Base legal art. 7º, V** — ratificar a execução de contrato como base, **se** a invoice carregar dados de terceiros. | HF-0606:40; §3.4.1 |
| **D4** | **Conjunto mínimo de campos** — ratificar o inventário mínimo (§3.1), incluindo se o endereço é coletado; alimenta B.4 (spec-007). | HF-0606:40; spec-007:41 |
| **D5** | **Política de logs sem PII/valores como critério de aceite** de produto (§3.2; herda spec-004:126). | HF-0606:40 |
| **D6** | **Retenção e rota de erase se persistida** — política de retenção (`UNKNOWN - verify`) + obrigação de rota DELETE de esquecimento (se D1 = persistir). | HF-0606:40; spec-007:114, :157 |
| **D7** | **Corrigir o drift E.1 da LISTA** — E-01..E-08 já ratificadas 26/10/2026 (constitution.md:226, :245); LISTA:67 obsoleta. | HF-0606:40; constitution.md:226, :245 |

**UNKNOWN - verify herdado da parcela** (HF-0606:40 — deve ser resolvido ou mantido declarado até a ratificação):

1. A invoice inclui dados de terceiros/cliente? (modelo GAP-04 inexistente; "partes" em spec-004:130) — condiciona D2/D3.
2. Aplicabilidade do art. 4º, I (fins exclusivamente particulares e não econômicos).
3. CNPJ fora do escopo LGPD — confirmar.
4. Retenção de `fx_quotes` (dados públicos, LGPD n/a; spec-004:122).

**Relação com as emendas E-01..E-08 já ratificadas** (26/10/2026 — constitution.md:226): E-02 fixou minimização na co-assinatura constitucional — papel do ratificador humano "sem nome civil" (spec-001:213-219; hoje constitution.md:142); E-03 fixou "segredo e PII nunca entram em camada de imagem" (spec-001:238-239; hoje constitution.md:215, Art. 10.2). Esta PROPOSTA não reabre emendas ratificadas; sua relação é de subordinação às normas já vigentes.

## 5. Critérios de aceite e testes

**Quem valida / DoD:** agent-reviewer valida a conformidade documental (template MANIFEST §1, citações, sem promoção de decisão); CCB/PO ratifica o conteúdo (constitution.md:138). DoD desta emissão: proposta draft emitida com D1-D7 incorporadas, zero decisão promovida, nenhum outro arquivo editado.

### 5.1 Critérios de aceite da EMISSÃO (verificáveis hoje)

- [ ] O arquivo `.ai/specs/spec-015-lgpd-produto-proposta-v1.spec.md` existe com `status: draft` no frontmatter e "PROPOSTA" no H1.
- [ ] O §4 lista D1-D7 como pendentes do CCB/PO, sem promoção de nenhuma delas a decisão.
- [ ] Nenhuma palavra deste documento atribui ratificação/aprovação à própria spec; a seção Status declara o condicionamento Art. 5.1.
- [ ] `spec-004:126` permanece intocado (esta spec não o reescreve — ver §2); nenhum outro arquivo foi editado; nada foi commitado.
- [ ] Toda afirmação de domínio possui citação `arquivo:linha` ou artigo de lei; os UNKNOWN da parcela TA-0050 estão declarados (§4), não resolvidos.

### 5.2 Critérios de produto PROPOSTOS (executáveis SOMENTE após ratificação CCB/PO; nenhum é requisito hoje)

- [ ] **CP-1** (pós-D4): nenhum campo além do inventário mínimo ratificado é coletado ou exibido pela invoice (art. 6º, III); endereço presente somente se D4 o ratificar.
- [ ] **CP-2** (pós-D5): verificação automatizada de que logs de produto não contêm PII, valores nem corpo de requisição (herda spec-004:126).
- [ ] **CP-3** (pós-D1/D6): se D1 = persistir — rota de erase local operante, retenção ratificada e teste de LGPD na rota de persistência (espelha spec-007:157); se D1 = transitória — não-persistência vigente (spec-004:126) é o mecanismo de eliminação (§3.3.4).
- [ ] **CP-4** (pós-ratificação): 100% dos artefatos novos de agente que tocam dados de produto declaram `lgpd-class` no frontmatter (§3.5).
- [ ] **CP-5** (pós-D7): drift E.1 da LISTA corrigido antes de qualquer referência normativa futura à LISTA (constitution.md:226).

## 6. Rastreabilidade

| Referência | Fonte |
|---|---|
| B.3 (item de origem) | docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:35 |
| GAP-08 (criterio LGPD de produto ausente) | spec-002-requisitos-review-round-1.spec.md:107 |
| P-04 (mínimo necessário; sem PII em artefatos; esquecimento por design) | constitution.md:90 (histórico: `constitution.md:36` — ver §2) |
| LGPD primária (jurisdição) | constitution.md:27 (Art. 1.1); Art. 3 princípios (P-04) |
| Art. 5.1 (decisor único via CCB; agentes são conselho) | constitution.md:138 |
| Art. 4.6 (kill switch LGPD não supersável) | constitution.md:124 |
| Art. 7 (segurança e privacidade) | constitution.md:172-178 |
| Art. 10.2 (PII fora de camada de imagem — E-03 ratificada) | constitution.md:215; spec-001-constitution-round-1-proposta.spec.md:238-239 |
| E-02 (minimização na co-assinatura — ratificada) | spec-001-constitution-round-1-proposta.spec.md:213-219; constitution.md:142 |
| E-01..E-08 ratificadas 26/10/2026 (drift E.1) | constitution.md:226 (CHANGELOG v1.1.0), :245 (co-assinatura), :229 (v1.2.1) |
| Parcela de consulta TA-0050 (fundamentos LGPD + D1-D7) | .ai/handoffs/HF-0606-consulta-de-dominio.md:31-45, :40 |
| Invoice nunca persistida; logs sem PII/valores/corpo | spec-004-backend-mvp-v1.spec.md:126; §6 invoice: :128-130 |
| fx_quotes — dados públicos | spec-004-backend-mvp-v1.spec.md:122 |
| Spec irmã B.4 (modelo de dados; condicionante D1) | spec-007-invoice-data-model-v1.spec.md:26, :38, :41, :46-48, :114, :130, :157 |
| US-004 / US-016/017 (demandantes condicionais) | spec-002-requisitos-review-round-1.spec.md:161, :178-179 |
| OS-01 (single-user, sem auth) | spec-002-requisitos-review-round-1.spec.md:134 |
| `lgpd-class` precedente / DoR item 10 | spec-002-requisitos-review-round-1.spec.md:19, :201 |
| LGPD Lei 13.709/2018 — art. 4º, I (exclusão: fins exclusivamente particulares e não econômicos) | §3.4.2; D2 |
| LGPD art. 5º, II (dado pessoal — CPF/dados bancários comuns) | §3.1.3 |
| LGPD art. 6º, I/III (finalidade; necessidade — minimização) | §3.1.1 |
| LGPD art. 7º, V (execução de contrato) | §3.4.1; D3 |
| LGPD art. 11 (regime de dados sensíveis — NÃO aplicado) | §2; §3.1.3 |
| LGPD art. 18 (direitos do titular — eliminação/anonimização) | §3.3 |

## 7. Fora de escopo (YAGNI)

- **Fluxos de exercício de direitos do titular remotos** (portais de titular, formulários de requisição, kanban de atendimento): fora — single-user/local torna a erasure local suficiente (§3.3; OS-01, spec-002:134).
- **DPO/Encarregado, ROPA (registro de operações), relatórios à ANPD, plano formal de resposta a incidentes**: fora do escopo desta rodada — projeto acadêmico single-user; exigiriam emenda de escopo (constitution Art. 1.3).
- **Dados pessoais sensíveis (art. 11)**: fluxo de regime agravado não é especificado — dados tratados são comuns (§2; HF-0606:40).
- **Autenticação/multiusuário**: fora (OS-01, spec-002:134).
- **NF-e/NFS-e e plataformas de transferência**: fora do escopo congelado (OS-05; precedente spec-007, §6).
- **Telemetria/rastreio**: proibidos por P-03 (constitution.md:88) — nunca são critério de produto aqui.
- **Contrato de dados da invoice** (tipos, constraints, DDL): matéria da spec-007 irmã (B.4) — aqui só os critérios LGPD que o modelo deve satisfazer (§2, última linha).
- **Política de retenção/backup da invoice**: decisão D6 + spec-007:114 — aqui só se referencia.
- **Edição da spec-004 ou de qualquer outro artefato por esta emissão**: proibida — mudanças pós-ratificação entram por nova task/handoff.

## CHANGELOG

- **0.1.0 — 2026-11-03 (TA-0060, HF-0616):** emissão inicial como **PROPOSTA (status: draft)**, sujeita a ratificação CCB/PO (Art. 5.1, constitution.md:138). Template canônico MANIFEST §1 (camadas a-h). Fundamentos incorporados por citação da parcela de consulta TA-0050 (agent-compliance-governance, HF-0606:40): minimização art. 6º, I/III; dados comuns art. 5º, II; logs sem PII/valores/corpo como critério de produto (D5); esquecimento por design local (art. 18); bases legais art. 7º, V / art. 4º, I; `lgpd-class` em artefatos de agente. Seção obrigatória de Condicionantes de ratificação com as decisões D1-D7 pendentes do CCB/PO + 4 UNKNOWN - verify. Drift E.1 da LISTA (:67) registrado como obsoleto (E-01..E-08 ratificadas 26/10 — constitution.md:226, :245) e correção condicionada a D7. Tensão de persistência spec-004:126 × GAP-04/US-016-017 registrada como D1, sem promoção; spec irmã spec-007 citada. Nenhum outro arquivo editado; nada commitado.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem | frontmatter (`spec_id: spec-015`, `version: 0.1.0`, `status: draft`) | aplicada |
| (b) Contexto/origem | §1 + frontmatter `origin`/`task` | aplicada |
| (c) Resolução de conflitos | §2 (persistência D1; drift E.1; localização P-04; sensíveis × comuns; fronteira com B.4) | aplicada |
| (d) Corpo de decisões/requisitos/contratos | §3 (§3.1-§3.6 critérios LGPD propostos) + §4 (condicionantes D1-D7 — conteúdo condicionante, não decisão) | aplicada |
| (e) Critérios de aceite/testes | §5 (§5.1 emissão; §5.2 produto proposto, condicional) | aplicada |
| (f) Rastreabilidade | §6 + frontmatter `trace` | aplicada |
| (g) Fora de escopo (YAGNI) | §7 | aplicada |
| (h) Changelog | CHANGELOG | aplicada |
