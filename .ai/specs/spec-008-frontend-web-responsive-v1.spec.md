---
id: ai-specs-spec-008-frontend-web-responsive-v1-spec
title: SPEC spec-008 — frontend-web-responsive-v1 — Interface web responsiva 100% FOSS do MVP (camada `front`)
type: spec
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/specs/spec-008-frontend-web-responsive-v1.spec.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- specs
- docs
- adequado-a-norma
---
---
spec_id: spec-008
specname: frontend-web-responsive-v1
version: 0.2.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-11-03
updated: 2026-11-05
origin: HF-0609 (TA-0053) | sender: agent-nexus-prime-ultimate | rodada 1 de specs (LISTA-SPECS-PENDENTES-2026-11-02.md, item B.1)
task: TA-0053 | handoff: HF-0609 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
wave: WS-4 | Onda 4 — Execução Técnica (frontend web)
lgpd-class: formulários da invoice coletam dados pessoais/financeiros (P-04, constitution.md:90) — minimização normativa na §6.4; este artefato não contém PII; critério LGPD de produto consolidado é item B.3 da LISTA (docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:35), condicionado a decisão CCB/PO
trace:
  - constitution.md (Art. 1.2/1.3/5.1/6.1/10.1/10.3/10.4; P-02 constitution.md:86, P-04 :90, P-06 :94, P-08 :98, P-10 :102, P-11 :104)
  - docs/decisoes/ADR-001-stack.md v1.1.0 (Ratificado CCB, ADR-001-stack.md:6; frontend HTML5+CSS3+JS vanilla :34; emenda de stack via ADR específica :53)
  - .ai/specs/MANIFEST.md (§1 template canônico camadas a–h; §2 nomenclatura/versionamento)
  - .ai/specs/spec-002-requisitos-review-round-1.spec.md (REQ-06 :67; REQ-01..05 :62-66; US-001..US-005 :158-162; US-007 :177; US-016/017 :178-179; C-07 :126; GAP-03 :102, GAP-04 :103, GAP-06 :105; OS-06 :139)
  - .ai/specs/spec-004-backend-mvp-v1.spec.md (§3 contrato /v1 :62-93; schemas :69-75; notice :77; invoice §6 :128-130; sem CORS :134; estrutura :136-153)
  - .ai/specs/spec-005-container-layers-v1.spec.md (camada front :62; estado vazio :30; custódia invoice.html :68; proxy 127.0.0.1:8080 :117; front encaminha /v1 :118; contrato front→back :221; compatibilidade /v1 :226; e2e navegador :181; UAT F-02/F-03 :324-325; evidências :342; numeração US-018+ :232)
  - .ai/handoffs/HF-0602-consulta-de-dominio.md (RESPOSTA — PARCELA DE CONSULTA TA-0046 / agent-ui-ux-advisor, :32-45 — insumo normativo meio-duplex, incorporado)
  - .ai/handoffs/HF-0609-spec-008-frontend-web-responsive-v1.md (envelope desta emissão, :17, :19-25)
  - docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md (:33 item B.1; :58 item D.1; :36 item B.4; :37 item B.5)
  - docs/planos/plano-granular/plano-producao-agentes.md (:121-131 onda 4 — A.11 agent-ui-ux-advisor :129 → A.12 agent-frontend-dev :130)
  - Verificação local de filesystem (2026-11-05): src/frontend/templates/index.html = tela de simulação funcional (era 0 B); src/frontend/static/ vazio; src/frontend/templates/invoice.html = 4996 B; schemas em src/shared/schemas.py:445-654
  - ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16)
---

# SPEC spec-008 — frontend-web-responsive-v1 — Interface web responsiva 100% FOSS do MVP (camada `front`)

Status: SPEC EMITIDA — PENDENTE DE REVISÃO E DE IMPLEMENTAÇÃO (onda seguinte, Art. 6.1, constitution.md:150 — especifica → implementa → valida → registra) | Tarefa: TA-0053 (handoff `.ai/handoffs/HF-0609-spec-008-frontend-web-responsive-v1.md`) | Orquestrador: agent-nexus-prime-ultimate | Custódia: agent-sdd-specialist (`.ai/specs/`)

Fonte única das decisões da camada `front`. Em conflito, vale a hierarquia do Art. 2 da Constituição. Convenções: citação `arquivo:linha`; identificadores/paths em EN; narrativa em PT-BR (P-10, constitution.md:102); alegação sem fonte = **UNKNOWN - verify** (P-08, constitution.md:98). Esta SPEC não implementa código (Art. 6.1).

---

## 1. Contexto e origem

Item **B.1** da lista de specs pendentes (docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:33): "nenhuma spec de frontend existe (só `spec-005` define a camada `front`)", com escopo derivado da onda 4 (A.11 `agent-ui-ux-advisor` → A.12 `agent-frontend-dev`, docs/planos/plano-granular/plano-producao-agentes.md:129-130; item D.1, :58). REQ-06 exige "Interface web responsiva FOSS — Chrome/Firefox/Edge ult. 2 versões" na fase N5.3 (.ai/specs/spec-002-requisitos-review-round-1.spec.md:67).

Estado atual verificado (2026-11-03): `src/frontend/templates/index.html` tem **0 B** e `src/frontend/static/` está **vazio** (fato também registrado em .ai/specs/spec-005-container-layers-v1.spec.md:30); `src/frontend/templates/invoice.html` existe (4996 B) e permanece sob custódia do **Back** como insumo do `POST /v1/invoice` (spec-005:68). Ou seja: greenfield de UI — esta SPEC define o **primeiro template real de navegador** e o inventário de `src/frontend/` (parcela TA-0046, item 5, .ai/handoffs/HF-0602-consulta-de-dominio.md:41).

**Insumo normativo meio-duplex:** a parcela de consulta TA-0046 (agent-ui-ux-advisor, `.ai/handoffs/HF-0602-consulta-de-dominio.md:32-45`) é incorporada como norma desta SPEC nos eixos: matriz de browsers (REQ-06), templates/estados, fluxos cotação/invoice, acessibilidade baseline e estado vazio (:41). Recomendações dela que exijam decisão de camada superior (HTMX, defaults de spread/IOF, wording da defasagem) são resolvidas na §2 ou marcadas `UNKNOWN - verify`.

## 2. Resolução de conflitos

| Tema | Decisão | Fonte vencedora | Texto superado |
|---|---|---|---|
| HTMX vs JS vanilla | **JS vanilla** (HTML5+CSS3+JS, ADR-001-stack.md:34). Qualquer biblioteca JS/HTMX exige emenda de ADR específica (regime de emenda controlada, ADR-001-stack.md:53) — decisão é de ADR, não de spec | ADR-001-stack.md:34,53 | Hipótese HTMX da parcela TA-0046 — que já condicionava "HTMX so via ADR whiteliste" (.ai/handoffs/HF-0602-consulta-de-dominio.md:41) |
| Default de spread/IOF na UI | Campos **informados pelo usuário; nenhuma alíquota no código** (.ai/specs/spec-004-backend-mvp-v1.spec.md:29). Pré-preenchimento de valor default na UI = decisão de produto → **UNKNOWN - verify** (PO/CCB) | spec-004-backend-mvp-v1.spec.md:29 (Plano de Riscos RE-04) | "spread/IOF default" (HF-0602-consulta-de-dominio.md:41) |
| Banner de defasagem da cotação | Indicador visual condicionado ao campo `quote.stale` — **dado já presente no contrato** (`RateQuote.stale`, spec-004:71). Política de fallback e wording exato ("dados com defasagem") = US-007, KG-R-02, pendente de ratificação PO/CCB → **UNKNOWN - verify** | spec-004-backend-mvp-v1.spec.md:71 + spec-002-requisitos-review-round-1.spec.md:177 | Promessa comportamental de fallback da US-007 tratada como norma vigente |
| Custódia de `invoice.html` | Permanece do **Back** (insumo do PDF, spec-005:68); os templates de UI de navegador são arquivos novos e não alteram `invoice.html` | spec-005-container-layers-v1.spec.md:68 | Reescrita/reaproveitamento de `invoice.html` como página de navegador |
| App nativo vs web responsivo | **Web responsivo mobile-first em CSS** (HF-0602-consulta-de-dominio.md:41); app mobile nativo permanece OUT (OS-06, spec-002-requisitos-review-round-1.spec.md:139) | spec-002:139 (Tabela 1 OUT) | Qualquer entrega nativa |
| e2e de navegador nesta onda | e2e de navegador está em backlog YAGNI (spec-005:181); testes desta camada = render server-side + verificação manual/estrutural (§10). **UNKNOWN - verify** se o GP exige e2e de UI nesta onda | spec-005-container-layers-v1.spec.md:181 | Inserção de suíte Playwright/Selenium nesta onda |

## 3. Requisitos da interface (normas da camada `front`)

1. **R-INT-01 — Stack FOSS server-side:** templates Jinja2 renderizados server-side pelo serviço `front` (precedente de motor de template: `invoice.html` Jinja2, spec-004:130); HTML5 + CSS3 + JS vanilla (ADR-001-stack.md:34). Sem framework SPA, sem HTMX (§2).
2. **R-INT-02 — Origem única:** o usuário acessa tudo somente via `proxy` em `127.0.0.1:8080`; `front` não publica porta no host e encaminha `/v1/*` para `back:8000` (spec-005:117-118). Sem CORS — mesma origem (spec-004:134).
3. **R-INT-03 — URLs relativas:** toda URL de asset, action de formulário e chamada `fetch` é relativa (sem host absoluto), para funcionar sob a origem única `127.0.0.1:8080` (R-INT-02).
4. **R-INT-04 — Zero recursos remotos (100% FOSS):** nenhum asset externo, CDN, webfont remota ou chamada a serviço de terceiro em tempo de execução; assets de licença aberta são vendored em `static/` (parcela TA-0046, .ai/handoffs/HF-0602-consulta-de-dominio.md:41; precedente: `url_fetcher` do WeasyPrint recusa remotos, spec-004:130; P-02/P-03 intra-container, constitution.md:217). Fonte tipográfica: **font stack do sistema** (sem webfont) — elimina licenciamento e fetch remoto.
5. **R-INT-05 — Progressive enhancement:** os dois fluxos (simulação, invoice) completam **com JS desabilitado**, via POST nativo de formulário tratado server-side pelo `front` em rotas próprias fora do namespace `/v1` (rotas-alvo: `POST /simulate` e `POST /invoice` — decisão normativa desta SPEC; o contrato `/v1` não é alterado, spec-005:226). Com JS, submit via `fetch` para os mesmos endpoints `/v1/*` (mesma origem, spec-005:221).
6. **R-INT-06 — Idioma:** `lang="pt-BR"` no `<html>`; copy de UI e mensagens de erro visíveis em PT-BR (P-10, constitution.md:102; "Mensagens em PT-BR", spec-004:93).
7. **R-INT-07 — Sem promessa financeira (kill switch):** copy sem promessa de ganho; o aviso constante `notice` — "Simulação de caráter informativo; spread e IOF foram informados pelo usuário e não substituem a orientação de um profissional habilitado." (spec-004:77) — é renderizado integralmente na tela de resultado; sem dark patterns (HF-0602-consulta-de-dominio.md:41).
8. **R-INT-08 — Fronteira de rede:** `front` nunca acessa `db` (não é membro de `data`, spec-005:91,108); sua única interface de saída é a API `back:8000/v1` (spec-005:62,104).

## 4. Estrutura de `src/frontend/` e inventário de templates

Estrutura-alvo (normativa desta SPEC; implementação na onda seguinte, Art. 6.1):

```
src/frontend/
├── templates/
│   ├── base.html                     # esqueleto compartilhado: lang, skip-link, header, footer, blocos
│   ├── index.html                    # tela de simulação (hoje 0 B — alvo desta SPEC, spec-005:30)
│   ├── invoice_form.html             # tela de emissão de invoice (form)
│   ├── partials/
│   │   ├── _rate_quote.html          # cotação: rate, source, quoted_at, indicador stale
│   │   ├── _simulation_result.html   # trilha auditável bruto → despesas → líquido
│   │   ├── _form_errors.html         # erros canônicos por campo (details[].field)
│   │   └── _loading.html             # marcador de estado loading
│   └── invoice.html                  # EXISTENTE — custódia do Back (PDF, spec-005:68); fora do escopo UI
└── static/
    ├── css/app.css                   # design tokens, layout mobile-first, estados, a11y (contraste/foco)
    └── js/app.js                     # enhancement: submit fetch, estado loading, formatação pt-BR
```

Regras: (a) cada tela herda de `base.html` — nada de markup de esqueleto duplicado; (b) `static/` contém **apenas** assets vendored de licença aberta (R-INT-04); (c) nenhum template de UI ecoa valores enviados pelo usuário em contexto de erro sem escaping (autoescape ativo, precedente spec-004:130); (d) números e datas nunca são formatados em string no backend da UI — formatação pt-BR é responsabilidade da camada `front` (§6.3).

## 5. Estados de tela

Cada tela (simulação, invoice form) especifica os quatro estados (norma da parcela TA-0046, .ai/handoffs/HF-0602-consulta-de-dominio.md:41):

| Estado | Simulação (`index.html`) | Invoice (`invoice_form.html`) |
|---|---|---|
| **empty** | Primeiro carregamento: só o formulário curto; região de resultado ausente; instrução do primeiro passo visível | Formulário vazio com obrigatórios marcados (§6.4) |
| **loading** | Submit desabilitado + indicador visível; orçamento de tempo: simulação E2E ≤3s P95 (REQ-05, spec-002:66; leitura C-07 — 2s chamada API, 3s E2E, spec-002:126) | Indicador enquanto o PDF é gerado; orçamento ≤3s/documento (REQ-04, spec-002:65) |
| **error** | 400: mensagens por campo a partir de `details[].field` (spec-004:82-87); 503 `rates_unavailable`: mensagem global com affordance de retry; `details` nunca ecoa o valor enviado (spec-004:93) | 400: por campo; 503 `pdf_unavailable`: mensagem global com retry (spec-004:90) |
| **success** | Partial `_simulation_result.html` + `_rate_quote.html` + `notice` (spec-004:77); se `quote.stale == true`, indicador visual de defasagem (§2) | Download do PDF acionado (`Content-Disposition: attachment`, spec-004:130) com confirmação visual |

Regra transversal: nenhuma tela permanece em estado indefinido — todo desfecho da API (200/400/500/503, spec-004:79-93) tem render correspondente; 500 `internal_error` renderiza mensagem genérica sem traceback nem dados do usuário (spec-004:91).

## 6. Fluxos e integração com a API `/v1`

### 6.1 Fluxo de simulação (US-001/US-002/US-003 — candidatas, spec-002:158-160)

1. Formulário curto (`POST /v1/simulate`, spec-004:66): moeda (`currency`), regime (`regime` — 5 opções `hourly|daily|weekly|monthly|fixed`, spec-004:60), `amount`, `quantity` (condicional ao regime: obrigatória nos regimes por período, proibida em `fixed` — spec-004:41-43,72), `spread_pct`, `iof_pct` (0–100, informados pelo usuário — spec-004:29,72).
2. Ao submeter: estado loading (§5) até a resposta; orçamento ≤3s P95 (§5).
3. Resultado: trilha auditável **bruto → despesas → líquido** com 2 casas decimais (REQ-03, spec-002:64; US-003 "trilha auditavel", spec-002:160), exibindo `gross_foreign`, `gross_brl`, `spread_brl`, `iof_brl`, `net_brl`, `effective_rate` e a cotação usada (`quote.rate`, `quote.source`, `quote.quoted_at`), seguidos do `notice` (spec-004:73,77). A identidade `gross_brl − spread_brl − iof_brl == net_brl` é propriedade do backend (spec-004:53); a UI exibe os quatro valores **sem recalcular nada**.
4. Comparações lado a lado entre os 5 regimes (US-002) são story candidata — não compromisso de escopo (Art. 5.1, nota spec-002:149-152); fora das telas normativas desta emissão (§12).

### 6.2 Registro de rótulos — labels 1:1 com os schemas da spec-004

Vínculo normativo: cada rótulo renderizado corresponde a **exatamente um** campo de `src/shared/schemas.py` (SSOT, `extra="forbid"`, spec-004:69); nenhum campo inventado; mudança de rótulo exige editar esta tabela (rastreabilidade). Fontes dos campos: spec-004:71-75 e `src/shared/schemas.py:463-468,500-522` (verificado 2026-11-03).

| Campo (schema) | Rótulo UI (PT-BR) | Formato/regra |
|---|---|---|
| `currency` (`USD\|EUR`, spec-004:60) | Moeda | Select com as 2 opções canônicas |
| `regime` (spec-004:60) | Regime de contratação | Select com os 5 regimes |
| `amount` (spec-004:72) | Valor por unidade do regime | Numérico pt-BR; >0, ≤1.000.000.000, 2 casas |
| `quantity` (spec-004:72) | Quantidade de unidades | Numérico pt-BR; exibida/obrigatória só em `hourly/daily/weekly/monthly`; oculta em `fixed` |
| `spread_pct` (spec-004:72) | Spread (%) | Numérico; 0–100, até 4 casas; sem default no código (§2) |
| `iof_pct` (spec-004:72) | IOF (%) | Numérico; 0–100, até 4 casas; sem default no código (§2) |
| `gross_foreign` / `gross_brl` (spec-004:73) | Bruto em moeda estrangeira / Bruto em BRL | 2 casas, pt-BR (1.234,56 — HF-0602-consulta-de-dominio.md:41) |
| `spread_brl` / `iof_brl` (spec-004:73) | Desconto de spread / IOF | 2 casas, pt-BR |
| `net_brl` (spec-004:73) | Líquido a receber em BRL | Destaque visual; 2 casas, pt-BR |
| `effective_rate` (spec-004:73) | Câmbio efetivo | 6 casas (precedente `q6`, spec-004:35,51) |
| `quote.rate` (`RateQuote`, spec-004:71) | Cotação (BRL por 1 unidade) | 6 casas |
| `quote.source` (spec-004:71) | Fonte da cotação | `frankfurter\|ptax` (spec-004:60) |
| `quote.quoted_at` (spec-004:71) | Data/hora da cotação | Data/hora pt-BR (instante UTC, schemas.py:466) |
| `quote.stale` (spec-004:71) | Indicador de defasagem | Renderizado se `true`; wording **UNKNOWN - verify** (§2) |
| `notice` (spec-004:77) | Aviso (obrigatório, integral) | Texto literal da constante |

### 6.3 Fluxo de invoice (US-004 — candidata, spec-002:161)

1. Formulário (`POST /v1/invoice`, spec-004:67): reutiliza os campos de simulação (§6.2, `InvoiceRequest.simulation: SimulationRequest`, spec-004:75) e adiciona os campos de parte e documento: `issuer` e `client` como `InvoiceParty` — `name` (1–120, obrigatório), `tax_id` (≤40, opcional), `address` (≤240, opcional; spec-004:74) — mais `invoice_number` (1–40), `issue_date` (date) e `description` (1–500; spec-004:75).
2. **Nenhum valor monetário é aceito/confirmado do cliente:** o Back recalcula a simulação recebida (spec-004:130); a UI não exibe nem simula campos de resultado editáveis.
3. Sucesso: resposta é `application/pdf` com `Content-Disposition: attachment; filename="invoice.pdf"` (spec-004:130) — a UI aciona o download e confirma (§5).
4. **Dependência GAP-04:** o modelo canônico de dados da invoice (campos bancários, CPF/CNPJ, período) está pendente (spec-002:103; item B.4, docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:36) — campos de invoice **além** do contrato `spec-004` §3: `UNKNOWN - verify` (a emitir na spec de modelo de dados da rodada 1). Política de numeração (`invoice_number` pré-preenchido/travado?) e ciclo de vida Rascunho/Finalizada (US-016/US-017, spec-002:178-179): pendentes de ratificação CCB → `UNKNOWN - verify`.

### 6.4 Minimização LGPD nos formulários (P-04, constitution.md:90)

- Só é coletado o que o contrato exige (spec-004:74-75): `tax_id` e `address` são **opcionais** — a UI não os marca como obrigatórios e não induz preenchimento; `name` é o único obrigatório de parte.
- Nada de dado pessoal é persistido pela UI (a invoice nunca é persistida pelo Back — spec-004:126); sem autocomplete sensível para `tax_id` (`autocomplete="off"`), sem armazenamento local (`localStorage`) de dados de formulário.
- Erros de validação nunca ecoam o valor enviado (spec-004:93); logs da camada `front` sem valores nem corpo de requisição (bloco LGPD spec-005:156).
- Critério de produto LGPD consolidado: pendente (item B.3 da LISTA, docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:35; envelope `.ai/handoffs/HF-0616-spec-015-lgpd-produto-proposta-v1.md`) — **UNKNOWN - verify** até decisão CCB/PO.

## 7. Acessibilidade baseline (norma da parcela TA-0046, .ai/handoffs/HF-0602-consulta-de-dominio.md:41)

| # | Requisito | Verificação (§10) |
|---|---|---|
| A1 | Contraste mínimo 4.5:1 (tema claro; tema dark fora de escopo, §12) | Medição local |
| A2 | Foco sempre visível (`:focus-visible`), ordem de tabulação lógica | Navegação por teclado |
| A3 | Todo input com `<label>` programático; campos obrigatórios com `aria-required` | Inspeção + leitor de tela local |
| A4 | Tabelas navegáveis (`caption`, `th scope`) — trilha auditável §6.1 | Inspeção + teclado |
| A5 | Alvos de toque/clique ≥44px | Inspeção |
| A6 | `lang="pt-BR"`; skip-link para o conteúdo principal; landmarks (`header`/`main`/`footer`) | Inspeção |
| A7 | Sem texto embutido em imagem; sem dark patterns; `notice` legível (R-INT-07) | Revisão |
| A8 | 100% dos elementos interativos operáveis por teclado nos 2 fluxos | Roteiro de teclado |

## 8. Responsividade e matriz de browsers

- **Browsers alvo (REQ-06, spec-002:67):** Chrome, Firefox e Edge — **últimas 2 versões** de cada; o layout responde sem quebra funcional em todos (US-005, spec-002:162). Sem promessa para Safari ou outros (HF-0602-consulta-de-dominio.md:41).
- **Mobile-first em CSS** (parcela TA-0046, :41): layout utilizável a partir de viewport de 360px (sem scroll horizontal), coluna única em larguras estreitas e aproveitamento de largura no desktop — desktop é o uso primário ("trabalhar a partir de qualquer desktop", US-005, spec-002:162).
- Breakpoints concretos e design tokens visuais = decisão de implementação da onda seguinte, dentro dos limites acima (Art. 6.1); esta SPEC fixa os limites verificáveis (360px, sem quebra funcional), não a estética.

## 9. User Stories candidatas (Padrão B — OKB §7.4, docs/conhecimento/OKB.md:539)

Numeração sequencial a partir de US-022 (precedente spec-005:232). **Nota de governança (Art. 5.1):** stories candidatas de backlog; entram em `ready` só após refinement/CCB (spec-002:149-152). Colisão de numeração com specs paralelas da rodada 1 (spec-006/007): resolve-se no refinement — `UNKNOWN - verify`.

### US-022 — foss-responsive-template-base
**Narrativa:** Como usuário, quero acessar o sistema por interface web responsiva 100% FOSS servida pela camada `front`, para trabalhar a partir de qualquer desktop (US-005, spec-002:162).
**Cenários:** 1. Dado `docker compose up --build` com a stack separada (spec-005:111), Quando abro `127.0.0.1:8080`, Então `index.html` renderiza tela de simulação com `lang="pt-BR"`, skip-link e zero recursos remotos no network inspector. 2. Dado viewport de 360px, Quando navego pelas duas telas, Então não há scroll horizontal nem quebra funcional (§8). 3. Dado JS desabilitado, Quando submeto o formulário, Então o fluxo completa server-side (R-INT-05).
**Rastreabilidade:** REQ-06 (spec-002:67) + REQ-15 (spec-002:76) + ADR-001-stack.md:34 + spec-005:62. **Dependências:** separação de camadas (US-018, spec-005:236). **Atribuição:** agent-frontend-dev (A.12, plano-producao-agentes.md:130). **Status:** `candidate`.

### US-023 — simulation-screen-flow-states
**Narrativa:** Como profissional que fatura em moeda estrangeira, quero simular USD/EUR→BRL na tela de simulação com estados loading/empty/error/success, para saber o valor recebível (US-001, spec-002:158).
**Cenários:** 1. Dado formulário válido com os 5 regimes, Quando submeto, Então a trilha bruto→despesas→líquido renderiza com 2 casas (6 no câmbio efetivo) e o `notice` integral (§6.1-6.2). 2. Dado payload inválido, Quando o Back responde 400, Então cada `details[].field` recebe mensagem junto ao campo, sem eco do valor (§5; spec-004:93). 3. Dado fontes indisponíveis e sem cache, Quando o Back responde 503 `rates_unavailable`, Então mensagem global com retry é exibida (§5; spec-004:89).
**Rastreabilidade:** REQ-01..03, REQ-05 (spec-002:62-66) + spec-004:66,73,77. **Dependências:** US-022; contrato `/v1` (spec-004 §3). **Atribuição:** agent-frontend-dev. **Status:** `candidate`.

### US-024 — invoice-screen-flow-states
**Narrativa:** Como prestador, quero emitir a invoice em PDF a partir da tela de invoice, para documentar formalmente o serviço (US-004, spec-002:161).
**Cenários:** 1. Dado formulário válido (partes + documento, §6.3), Quando submeto, Então o PDF baixa com `Content-Disposition: attachment` e confirmação visual (spec-004:130). 2. Dado WeasyPrint/Pango ausente, Quando o Back responde 503 `pdf_unavailable`, Então mensagem global com retry (spec-004:90). 3. Dado minimização P-04, Quando inspeciono o form, Então só `name` é obrigatório entre os campos de parte; sem armazenamento local de dados (§6.4).
**Rastreabilidade:** REQ-04 (spec-002:65) + spec-004:67,74-75,126,130. **Dependências:** US-022; modelo de dados GAP-04 (§6.3). **Atribuição:** agent-frontend-dev. **Status:** `candidate`.

## 10. Critérios de aceite e testes

| # | Critério (verificável) | Método |
|---|---|---|
| AC-1 | Navegação por teclado: 100% dos interativos das 2 telas alcançáveis/operáveis; foco visível (A2, A8) | Roteiro manual estruturado |
| AC-2 | Contraste ≥4.5:1 em todos os pares texto/fundo (A1) | Medição local (inspeção calculada) |
| AC-3 | Estados: as 2 telas implementam empty/loading/error/success conforme §5 | Render por fixture + inspeção |
| AC-4 | Fluxo de simulação completo sem quebra funcional em Chrome/Firefox/Edge (últ. 2 versões) (§8; REQ-06) | Matriz manual de browsers |
| AC-5 | Fluxo completo com JS desabilitado (R-INT-05) | Browsers com JS off |
| AC-6 | Zero requisição fora de `127.0.0.1:8080` durante o uso (R-INT-04) | Network inspector local |
| AC-7 | Labels 1:1: todo rótulo renderizado consta da tabela §6.2 e mapeia campo de schema; nenhum campo extra | Revisão contra spec-004:71-75 |
| AC-8 | Números pt-BR: 2 casas nos monetários, 6 no câmbio/cotação; datas/hora pt-BR (§6.2) | Render de fixture |
| AC-9 | 400 por campo via `details[].field`; 503 com retry; `notice` integral no sucesso (§5, §6.1) | Render por fixture de erro |
| AC-10 | Sem scroll horizontal em 360px; desktop sem quebra (§8) | Inspeção de viewport |
| AC-11 | Contrato `/v1` inalterado: `tests/integration/test_api_contract.py` e `test_openapi.py` seguem verdes após a separação | Suíte de contrato existente (spec-005:179,226) |
| AC-12 | `static/` sem asset de licença não-OSI; sem webfont remota (R-INT-04; REQ-15, spec-002:76) | Revisão + scanner FOSS do CI (ci.yml `foss-compliance`) |
| AC-13 | Isolamento: `front` não alcança `db:5432` (R-INT-08) | Caso negativo da §7.3 da spec-005 (spec-005:189) |

Testes automatizados desta camada: render server-side dos templates por fixture (sem rede nem relógio real, precedente spec-004:155); e2e de navegador permanece em backlog (spec-005:181 — **UNKNOWN - verify** se o GP exige nesta onda, §2). UAT de produto: os fluxos de front integram F-02/F-03 (spec-005:324-325) e a UAT de produto B.5 (docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:37); destino das evidências: **UNKNOWN - verify** (spec-005:342).

## 11. Rastreabilidade

| Fonte | Onde nesta spec |
|---|---|
| REQ-06 (spec-002:67; US-005 :162) | §§3, 8, 10 (AC-4), US-022 |
| REQ-01..REQ-05 (spec-002:62-66; US-001..US-004 :158-161) | §§5, 6.1, 6.3, US-023, US-024 |
| REQ-15 FOSS (spec-002:76) | R-INT-04, AC-12 |
| ADR-001-stack.md:34,53 | §2 (vanilla vs HTMX), R-INT-01 |
| spec-004 §3/§6 (contrato, schemas, notice, invoice) | §§5, 6.1-6.3, 10 (AC-7, AC-11) |
| spec-005 (camada front :62; estado vazio :30; proxy :117-118; fronteira :68; e2e :181; UAT :324-325) | §§1, 3, 4, 10 |
| Parcela TA-0046 (HF-0602:32-45) | §§1, 3, 5, 7, 8 (insumo normativo incorporado) |
| GAP-03/GAP-04/GAP-06 (spec-002:102-105) | §2, §6.3 (`UNKNOWN - verify`) |
| US-007/US-016/US-017 (spec-002:177-179) | §2, §6.3 (condicionais — `UNKNOWN - verify`) |
| Onda 4 A.11→A.12 (plano-producao-agentes.md:129-130) | §§1, 9 (atribuição) |

## 12. Fora de escopo (YAGNI — P-11, constitution.md:104)

- App mobile nativo (OS-06, spec-002:139); Safari e demais browsers fora da matriz §8.
- Framework SPA (React/Vue/etc.) e HTMX — exigiriam emenda de ADR-001 (§2; ADR-001-stack.md:53).
- Recursos remotos: CDN, webfonts externas, analytics, chamadas a serviço de terceiro em runtime (R-INT-04; P-02/P-03, constitution.md:217).
- Tema dark, i18n multi-idioma, autenticação/multiusuário (OS-01, spec-002:134), histórico de simulações (fora do escopo declarado em spec-004:31).
- Comparador de regimes lado a lado (US-002) e ciclo de vida de invoice Rascunho/Finalizada + clone (US-016/US-017) — stories candidatas pendentes de ratificação CCB (spec-002:159,178-179); não são telas normativas desta emissão.
- Novos endpoints `/v1` ou alteração do contrato existente (spec-005:226); mecanismo interno de render/wiring do serviço `front` (implementação da onda seguinte, Art. 6.1).
- e2e de navegador automatizado nesta onda (spec-005:181).

## Conformidade desta emissão

- Arquivo único criado: `.ai/specs/spec-008-frontend-web-responsive-v1.spec.md` (custódia `.ai/specs/`). Nenhum outro arquivo editado; nada commitado.
- Kill switch herdado (Art. 4.6); zero PII no artefato (P-04, §6.4 registra a minimização dos fluxos); 100% local, sem cloud (P-02); slugs/paths EN + narrativa PT-BR (P-10); toda alegação com `arquivo:linha` ou `UNKNOWN - verify` (P-08); nenhuma capacidade especulativa (P-11).
- Hierarquia respeitada: Constituição > ADR-001 v1.1.0 > planos > specs > código (Art. 2). **Validação (quem valida e DoD):** agent-reviewer audita citações e testabilidade dos AC; agent-ui-ux-advisor confirma fidelidade da parcela TA-0046; DoD = camadas a–h aplicadas, AC verificáveis, rastreabilidade ≥2 fontes, arquivo ≤400 linhas, zero escrita fora deste arquivo.

## CHANGELOG

- 0.1.0 — 2026-11-03 (TA-0053, HF-0609): emissão inicial. Normas da camada `front` (R-INT-01..08); inventário de `src/frontend/` e templates-alvo; estados de tela (empty/loading/error/success); registro de labels 1:1 com os schemas da spec-004; fluxos `POST /v1/simulate` e `POST /v1/invoice` com minimização P-04; acessibilidade baseline A1..A8; matriz de browsers REQ-06 (Chrome/Firefox/Edge últ. 2 versões); parcela TA-0046 (HF-0602:32-45) incorporada como insumo normativo; tabela de conflitos (HTMX vs vanilla, default spread/IOF, stale banner, custódia invoice.html, mobile, e2e); 3 stories candidatas US-022..US-024; 13 ACs verificáveis; lacunas declaradas: GAP-03 (ratificação da fórmula), GAP-04 (modelo de dados invoice), GAP-06 (TTL/stale), ratificação US-007/016/017, whitelist HTMX via ADR, destino de evidências UAT (spec-005:342), e2e de UI nesta onda.
- 0.2.0 — 2026-11-05 (refinamento de ratificação, Grupo A): frontmatter atualizado ao padrão TA-0031 ratificado (adicionado `wave: WS-4`, `trace`; `version` 0.1.0 → 0.2.0). `src/frontend/templates/index.html` agora é tela de simulação funcional (era 0 B, commit `abc7350`), chamando `POST /v1/simulate` pela mesma origem via proxy `127.0.0.1:8080`. GAP-04 (modelo de dados invoice) fechado por ADR-016 D4 (RAT-2026-11-05-A16-D4, spec-007 ratificada). Destino de evidências UAT fechado = `docs/uat/` (pendência #6 resolvida). Aderência ao padrão de nomenclatura `spec-NNN-specname.spec.md` confirmada (ADR-018, RAT-2026-11-05-A18). Nenhuma decisão de negócio de §§1–12 reescrita. **Ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16)**.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem | frontmatter (`spec_id: spec-008`, `version: 0.2.0`, `status: draft`, `created: 2026-11-03`, `updated: 2026-11-05`, `task`/`sender`, `trace`, `lgpd-class`, `wave`) | aplicada |
| (b) Contexto/origem | §1 (B.1/D.1 da LISTA; estado vazio verificado; insumo TA-0046) | aplicada |
| (c) Resolução de conflitos | §2 (6 temas com fonte vencedora e texto superado) | aplicada |
| (d) Corpo de decisões/requisitos/contratos | §§3–9 (R-INT, templates, estados, fluxos, labels 1:1, a11y, responsividade, stories) | aplicada |
| (e) Critérios de aceite/testes | §10 (AC-1..AC-13 binários com método) | aplicada |
| (f) Rastreabilidade | §11 (REQ/ADR/US/arquivo:linha) + frontmatter `trace` | aplicada |
| (g) Fora de escopo (YAGNI) | §12 | aplicada |
| (h) Changelog | CHANGELOG (0.1.0) | aplicada |
