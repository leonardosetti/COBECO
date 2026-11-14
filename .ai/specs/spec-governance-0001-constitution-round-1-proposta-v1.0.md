---
id: ai-specs-spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta-spec
title: PROPOSTA DE EMENDAS CONSTITUCIONAIS — RODADA 1 (WS-1)
type: spec
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/specs/spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- specs
- docs
- adequado-a-norma
---
---
spec_id: spec-001
specname: constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta
version: 0.1.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-10-25
updated: 2026-11-05
origin: TA-0002 | handoff: HF-0001 | sender: agent-nexus-prime-ultimate
task: TA-0002
kill_switch: inherited
wave: WS-1 | Rodada 1 — definição canônica da constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md
lgpd-class: n/a (zero PII neste artefato; P-04, constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:90)
trace:
  - constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md v1.0.0 (Art. 9.1 — emendas; Art. 5.2 — ratificação humana)
  - docs/planos/COBECO.pdf (106 págs.; citações por linha do texto extraído via pdftotext)
  - docs/planos/plano-integral-tap-1-2-3-4-5.md (reprodução integral do TAP v3)
  - .ai/agents/config-registry-0001-registry-v1.0.yaml (roster SSOT, sincronizado por scripts/sync_agent_registry.py)
  - scripts/validate_afa_output.py, scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py, tests/validation/test_nexus_yaml.py
  - git commits dd3b087 ("ADRs 001–005 emitidas") e 7892561 ("requisitos, baseline de métricas")
  - ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16, ADR-LOG-012)
---

# PROPOSTA DE EMENDAS CONSTITUCIONAIS — RODADA 1 (WS-1)

Nenhuma decisão é tomada aqui. Esta proposta nasce do Art. 9.1 (proposta escrita →
parecer de auditoria → ratificação humana CCB) e do Art. 5.1 (o Humano decide).
Toda emenda abaixo está marcada **[REQUER RATIFICAÇÃO CCB]**. Nenhum arquivo de lei
foi editado (custódia restrita a `.ai/specs/`).

Nota de proveniência: citações "PDF:N" referem-se ao texto extraído de
`docs/planos/COBECO.pdf` via `pdftotext -layout` (arquivo de trabalho
`/tmp/config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/cobeco/cobeco.txt`); o PDF é imagem de documento Word, sem numeração
de linha nativa.

---

## 1. INVENTÁRIO DE GAPS / DRIFTS / CONTRADIÇÕES (com evidência)

Hipóteses do envelope TA-0002 foram verificadas uma a uma; veredito por item.

### G-01 — Art. 4.5 cita slug legado `agent-orchestrator` (CONFIRMADO)
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:46` (Art. 4.5): "Orquestração: `agent-orchestrator` (L0) dispara…".
- `.ai/agents/config-registry-0001-registry-v1.0.yaml:406-414`: L0 promulgado é `agent-nexus-prime-ultimate`
  (version 1.3.0-ULTIMATE, layer L0, role orchestrator, status promulgado).
- `tests/validation/test_nexus_yaml.py:107-118`: assevera que o registry DEVE conter
  `agent-nexus-prime-ultimate` e NÃO PODE conter `agent-orchestrator` ("slug legacy…
  substituído").
- Drift secundário: `scripts/script-dispatch-0001-nexus-dispatcher-v1.0.py:75,79` usa `agent-orchestrator`
  como sender default; `.ai/specs/doc-afa-0001-changelog-v1.0.md:2` cita "agent-orchestrator §15".
- **Veredito:** drift confirmado contra a própria lei (Art. 4.4 declara registry SSOT).
- **Rota do drift secundário (código):** correção do dispatcher pertence ao
  backend-dev, não a esta emenda — recomendado parcel futuro.

### G-02 — Co-assinatura humana PENDENTE sem mecanismo de fechamento (CONFIRMADO)
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:3`: "Status: VIGENTE (a co-assinatura humana pendula)" —
  adicionalmente, typo "pendula" (leia-se "pendente").
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:83` (CHANGELOG 1.0.0): "Co-assinatura humana pendente no primeiro
  commit da FASE 0."
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:52-54` (Art. 5.2): ratificação humana explícita é exigida, mas não
  existe forma material definida (o que é "co-assinatura"? onde registra? qual prazo?).
- **Veredito:** lacuna procedimental confirmada; sem fechamento, a promulgação v1.0.0
  permanece juridicamente ambígua.

### G-03 — Ausência de cláusula Docker / camadas ortogonais (CONFIRMADO COM RESERVA)
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` (arquivo inteiro, 86 linhas): zero menções a Docker/containers
  (verificação: busca textual completa).
- `docs/planos/COBECO.pdf` (texto extraído, 3.861 linhas): zero ocorrências de
  "docker", "container", "ortogonal" (grep: 0 hits).
- Canon do Humano (declarado no envelope TA-0002/HF-0001): "camadas ortogonais
  abrigadas em containers docker próprios".
- `.ai/agents/config-registry-0001-registry-v1.0.yaml:277-285`: roster promulga `agent-docker-specialist`
  (L2) — porém `.config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-docker-specialist.md:1-10` carrega o corpo de
  custódia de DOCUMENTAÇÃO (título "L2 · SPECIALIST · DOCUMENTATION"; descrição de
  doc-readme-0001-readme-canon/docs/glossário, idêntica à do docer). Defeito de forja (duplicata mal
  rotulada), não coberto por esta proposta — rota: AFA via nexus.
- **Veredito:** o canon existe na vontade do Humano e no roster (slug), mas não há
  âncora constitdoc-arch-0006-uc-v1ional nem registro em ADR/PDF. Emenda nasce do canon declarado
  (Art. 5.1) com KNOWLEDGE GAP declarado sobre fonte escrita (KG-04).

### G-04 — YAGNI e first-principles não codificados no Art. 3 (CONFIRMADO)
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:27-38` (P-01..P-10): nenhum princípio menciona YAGNI ou
  first-principles.
- Suporte escrito ao YAGNI: `docs/planos/COBECO.pdf:2191` (fronteira de escopo
  "fundamentada no princípio YAGNI"); Tabela 40 do PDF (coluna OUT operacionaliza
  exclusões YAGNI).
- First-principles: zero ocorrências no PDF ("primeiros princípios", "first
  principle": 0 hits). Única fonte é o canon do Humano (envelope TA-0002).
- **Veredito:** lacuna confirmada; YAGNI com fonte escrita forte, first-principles
  com KG declarado.

### G-05 — Fluxo CR→ADR→CCB vs Art. 9 sem articulação (CONFIRMADO)
- Fluxo de mudança do projeto: `docs/planos/COBECO.pdf:2330-2340` — Issue com label
  `change-request` → análise GP ≤48h → decisão ≤24h → atualização de backlog/EAP;
  "Mudanças na stack tecnológica — incluindo a stack SDD … exigem ADR específica";
- `docs/planos/COBECO.pdf:2158-2161` — inclusão/exclusão/troca de ferramentas, modelos
  ou motores da stack "exigirá ADR específica" conforme gatilhos da política de ADRs.
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:76-79` (Art. 9.1): fluxo próprio de emenda (proposta escrita →
  parecer auditoria → ratificação CCB).
- **Veredito:** dois fluxos paralelos sem ponte constitdoc-arch-0006-uc-v1ional (quando uma muda
  escala para a outra?). Nada no Art. 9 diz que ADR não pode contrariar a
  Constituição — embora Art. 2 resolva conflito de cima para baixo, o operador do
  fluxo de mudança não tem regra explícita de escala.

### G-06 — Camada ADR estruturalmente VAZIA (CONFIRMADO — drift grave)
- `ls -la docs/decisoes/`: ADR-001..005 com 0 bytes cada.
- `git show dd3b087:docs/decisoes/ADR-005-freeze.md` = 0 bytes: os ADRs foram
  commitados vazios no commit "ADRs 001–005 emitidas (política de ADRs)".
- A mensagem de commit `dd3b087` sobrevive como único registro do conteúdo previsto:
  "ADR-001: Stack tecnológica FOSS (Python 3.11 + FastAPI + SQLite + WeasyPrint);
  ADR-002: Kanban…; ADR-003: Métricas de fluxo (EVM LEGADO); ADR-004: Tasklists
  Markdown; ADR-005: Regime de freeze do TAP + precedência intra-TAP §6 + Notas de
  Contexto".
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:14` (Art. 1.3) cita "escopo congelado (ADR-005)" — cita arquivo
  vazio. `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:25` (Art. 2, nível 3 da hierarquia) conta com essa camada.
- Registros sobreviventes do regime de freeze: `docs/planos/plano-integral-tap-1-2-3-4-5.md:464`
  (NC-00: freeze, decisão do GP 21/09/2026, "ADR-005 encaminhada para emissão antes
  do M2"); `:206` (TAP v3 congelado em 18/09/2026); `docs/planos/COBECO.pdf:2796`
  (NC-C4) e `:3048-3054` (NC-00, Tabela 55).
- **Veredito:** a camada 3 da hierarquia (Art. 2) está oca; a Constituição legisla
  sobre um congelamento cujo instrumento promulgado não existe. Repor o TEXTO dos
  ADRs está fora da minha custódia — propõe-se emenda transitória (E-07) + parcel
  ao architect/PM.

### G-07 — Art. 4.7 impreciso frente ao gate real (CONFIRMADO)
- `scripts/validate_afa_output.py:31`: `CUT_SCORE = 85` — o corte ≥85 do Art. 4.7
  BATE com o script.
- Porém `scripts/validate_afa_output.py:34-45` (SECTIONS + MIN_COUNTS): o gate exige
  19 cabeçalhos (§§0, 0.1, 0.2, 1–16) e mínimos Kill Switch ≥5, DOs ≥15, DON'Ts ≥15,
  Red Team ≥8, FAIL-CLOSED ≥6, métricas ≥8.
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:48` (Art. 4.7) diz "(16 seções, RT ≥ 8 vetores, FAIL-CLOSED ≥ 6,
  métricas ≥ 8)" — omite KS/DOs/DON'Ts e erra a contagem de seções.
- `scripts/validate_afa_output.py:124-133`: seção faltante ou mínimo estourado =
  rejeição INDEPENDENTE de score (fail-closed estrutural).
- **Veredito:** threshold ≥85 correto; parêntese do Art. 4.7 impreciso.

### G-08 — Artefatos de especificação vazios (CONFIRMADO)
- `docs/requisitos/requisitos.md`, `.ai/specs/tap.md`, `.ai/specs/requisitos.md`,
  `.ai/specs/eap.md`: 0 bytes (verificação: `wc -l`; `git show HEAD:.ai/specs/tap.md`
  = 0 bytes; `git show 7892561:docs/requisitos/requisitos.md` = 0 bytes).
- A camada 5 da hierarquia (Art. 2, `.ai/specs/`) está sem conteúdo executável.
- Fontes sobreviventes: `docs/planos/plano-integral-tap-1-2-3-4-5.md:10` ("reproduz,
  de maneira integral…, o conteúdo do TAP… emitido em 18/09/2026… regime de
  congelamento") e o PDF.
- **Veredito:** a missão pediu leitura de `.ai/specs/tap.md` — vazia; conteúdo de TAP
  consultado via plano-integral (KG-03). Repovoamento fora da minha custódia.

### G-09 — "WIP ≤ 3" sem qualificador "por pessoa" (CONFIRMADO, menor)
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:60` (Art. 6.2): "In Progress (WIP ≤ 3)".
- `docs/planos/COBECO.pdf:1677`: "WIP limit: 3 cards em 'In Progress' por pessoa";
  `:1642` (Figura 8): "WIP limit: máx. 3"; Tabela 32 (`:1817-1818`): "WIP em fluxo ≤ 9
  (3 × 3 pessoas)".
- **Veredito:** nuance real (3/pessoa, 9 total); micro-emenda de clareza.

### G-10 — `.ai/specs/doc-afa-0001-changelog-v1.0.md` cita artigo inexistente (CONFIRMADO, custódia minha)
- `.ai/specs/doc-afa-0001-changelog-v1.0.md:2`: "Custódia: constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Art. 15.4" — a
  Constituição v1.0.0 tem apenas Artigos 1–9 (`constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:10-79`). Além disso,
  cita "agent-orchestrator §15" (slug legado, ver G-01).
- **Veredito:** defeito de saneamento no MEU arquivo de custódia; correção fica para
  SIR/tarefa posterior — não alterado nesta missão (DoD restrito).

### G-11 — P-02 vs "Free Tier"/"sem cloud paga" do plano (VEREDITO SEM EMENDA)
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:30` (P-02): "Nenhum dado do projeto trafega para nuvem de
  terceiros" (proibição total).
- `docs/planos/COBECO.pdf` Tabela 44 (linha ~2530): "Infraestrutura e Hospedagem —
  Ambiente local/homologação (sem cloud paga)"; Tabela 40: "Free Tier" admitido no
  custo zero.
- **Veredito:** conflito latente de redação: o plano permite cloud gratuita, a
  Constituição proíbe qualquer nuvem de terceiros. Hierarquia (Art. 2): Constituição
  prevalece. Recomenda-se saneamento do plano de custos pelo PM (fora da minha
  custódia). Não proponho afrouxar P-01/P-02.

### G-12 — P-02 `qwen30b-moe` vs PDF "Qwen 32B" (VEREDITO SEM EMENDA)
- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:30`: modelo canônico `qwen30b-moe`.
- `docs/planos/COBECO.pdf:2156`: "modelo Qwen 32B".
- **Veredito:** drift de nomenclatura entre camadas; pela hierarquia (Art. 2) e
  cronologia (PDF: set/2026; Constituição: out/2026), a Constituição prevalece.
  Saneamento do PDF/plano é questão acadêmica do PM/docer — registrado, sem emenda.

### G-13 — ADR-002 (kanban) vs Art. 6.2 e ADR-003 (métricas) vs P-06 (VEREDITO SEM EMENDA)
- ADRs 002/003: 0 bytes (G-06) — nada há para contrapor textualmente; não é possível
  declarar contradição contra texto inexistente (P-08).
- Contraprova via PDF (registro sobrevivente): colunas do Kanban
  (`docs/planos/COBECO.pdf:1638-1646,1660-1661`: Backlog → Ready (DoR) → In Progress →
  Code Review → Done (DoD)) batem com `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:60` (Art. 6.2) — coerentes.
- Tabela 32 (`docs/planos/COBECO.pdf:1809-1830`): Coverage ≥80% por CI — igual à meta
  de P-06 (`constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:34`, "cobertura ≥ 80%") — coerentes. EVM LEGADO (ADR-003)
  é matéria de custos, não confronta P-06.
- **Veredito:** sem contradição verificável; dependência da repromulgação dos ADRs.

---

## 2. PROPOSTA DE EMENDAS (formato Art. 9.1 — PT-BR)

TODAS as emendas abaixo: **[REQUER RATIFICAÇÃO CCB]** (Art. 5.2). Formato:
artigo alvo → texto atual → texto proposto → justificativa → fonte.

### E-01 [REQUER RATIFICAÇÃO CCB] — Correção do slug do orquestrador
- **Artigo alvo:** Art. 4.5 (`constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:46`).
- **Texto atual:** "**Orquestração:** `agent-orchestrator` (L0) dispara; fluxo é
  half-duplex; delegação circular é proibida; `nexus_dispatcher.py` aplica
  AGENT_TOPOLOGY."
- **Texto proposto:** "**Orquestração:** `agent-nexus-prime-ultimate` (L0) dispara;
  fluxo é half-duplex; delegação circular é proibida; `nexus_dispatcher.py` aplica
  AGENT_TOPOLOGY."
- **Justificativa:** o Art. 4.4 declara o registry como SSOT do roster; o registry
  promulga `agent-nexus-prime-ultimate` como L0 (`.ai/agents/config-registry-0001-registry-v1.0.yaml:406-414`)
  e o próprio repositório testa que o slug legado NÃO pode mais existir
  (`tests/validation/test_nexus_yaml.py:107-118`). A lei cita um agente que o
  sistema proíbe.
- **Fonte:** registry linhas 406-414; test_nexus_yaml.py linhas 107-118;
  constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Arts. 4.4 e 4.5.

### E-02 [REQUER RATIFICAÇÃO CCB] — Mecanismo de fechamento da co-assinatura
- **Artigo alvo:** Art. 5 (inclusão de 5.4) + cabeçalho do arquivo (linha 3).
- **Texto atual:** não existe 5.4; cabeçalho: "Status: VIGENTE (a co-assinatura
  humana pendula)".
- **Texto proposto (novo 5.4):** "5.4. **Co-assinatura:** toda promulgação ou emenda
  desta Constituição registra bloco de co-assinatura ao pé do arquivo contendo:
  versão, SHA-256 do conteúdo integral, data e papel do ratificador humano (sem nome
  civil — minimização LGPD, Art. 7.3). Enquanto pendente, o cabeçalho marca
  `VIGENTE-INTERIM`; fechado, `VIGENTE-PLENA`. O fechamento da v1.0.0 deve ocorrer
  até o marco M2; vencido sem co-assinatura, o `project-auditor` registra não
  conformidade (Art. 8.1)."
- **Texto proposto (cabeçalho):** "Status: VIGENTE-INTERIM (co-assinatura humana
  pendente — fechamento conforme Art. 5.4)".
- **Justificativa:** a pendência está declarada (`constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:3` e `:83`), mas
  sem forma material, prazo ou estado, a ratificação do Art. 5.2 é inexecutável e
  inauditorável. O bloco com hash dá falsificabilidade e sdoc-arch-0006-uc-v1essão (Art. 8.2).
- **Fonte:** constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md linhas 3, 52-54, 83; PDF:1984-1993 (governança CCB de
  membro único é prática já documentada).

### E-03 [REQUER RATIFICAÇÃO CCB] — Containers Docker e ortogonalidade de camadas
- **Artigo alvo:** novo Art. 10 (Infraestrutura e Isolamento).
- **Texto atual:** inexistente (zero menções a Docker/containers em
  constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md).
- **Texto proposto:** "## ART. 10 — INFRAESTRUTURA E ISOLAMENTO
  10.1. As camadas de execução do projeto (runtime de agentes SDD, aplicação,
  dados, CI) rodam ortogonais: cada camada é abrigada em container Docker próprio e
  pode ser construída, versionada, reiniciada ou substituída independentemente;
  comunicação entre camadas ocorre apenas por interface declarada (porta, volume ou
  API), nunca por estado implícito compartilhado.
  10.2. Toda imagem base é FOSS e referenciada por digest imutável; segredo e PII
  nunca entram em camada de imagem (Arts. 7.2, 7.3).
  10.3. Os princípios P-02 e P-03 aplicam-se intra-container: nenhum dado do projeto
  transita para registry ou serviço de terceiros; download de imagens de registry
  externa é operação de build pontual e registrada (P-05), nunca fluxo de dados.
  10.4. Violação de ortogonalidade (vazamento de estado/dependência entre camadas)
  é defeito tratado, barrado nos portões reviewer → gatekeeper (P-06)."
- **Justificativa:** canon declarado pelo Humano (envelope TA-0002/HF-0001: "camadas
  ortogonais abrigadas em containers docker próprios"). O roster já promulga um
  agente de Docker (registry:277-285), o que evidencia que a camada existe de fato
  sem lei que a governe. Sem este artigo, P-02/P-03 ficam sem instrumento de
  isolamento material.
- **Fonte:** HF-0001 (canon do Humano) — KG-04 declarado (nem Constituição nem PDF
  registram o canon); registry:277-285; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Arts. 2, 7.2-7.3, P-02, P-03.

### E-04 [REQUER RATIFICAÇÃO CCB] — Codificação de YAGNI e primeiros princípios
- **Artigo alvo:** Art. 3 (inclusão de P-11 e P-12).
- **Texto atual:** P-01..P-10 (`constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:27-38`) não os mencionam.
- **Texto proposto:** "**P-11 — YAGNI:** nenhuma capacidade é construída sem demanda
  do ciclo atual; extrapolação de futuro vai ao backlog Kanban; as exclusões da
  fronteira de escopo (Tabela 40 do Plano de Escopo) são a operacionalização deste
  princípio. **P-12 — PRIMEIROS PRINCÍPIOS:** toda decisão de design parte de
  fundamentos verificáveis até a primeira causa; pressuposto sem fundamentação é
  KNOWLEDGE GAP declarado (P-08) antes de virar premissa."
- **Justificativa:** YAGNI já rege a fronteira de escopo do plano
  (`docs/planos/COBECO.pdf:2191`: exclusões "fundamentadas no princípio YAGNI"; Tabela
  40) mas não existe na lei suprema — princípio usado sem codificação é vetor de
  drift. P-12 formaliza o método que o próprio Art. 9.2 e o protocolo
  anti-aldoc-arch-0006-uc-v1inação já exigem na prática.
- **Fonte:** COBECO.pdf:2191 e Tabela 40 (YAGNI); HF-0001 (canon do Humano para
  first-principles — KG-01 declarado); constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Art. 3, P-08.

### E-05 [REQUER RATIFICAÇÃO CCB] — Articulação do fluxo de mudança (CR → ADR → CCB → Emenda)
- **Artigo alvo:** Art. 9 (inclusão de 9.3).
- **Texto atual:** Art. 9 tem apenas 9.1 (fluxo de emenda) e 9.2 (não-retroação)
  (`constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:76-79`).
- **Texto proposto:** "9.3. **Fluxo de mudança integrado:** (i) toda mudança abre
  Issue com label `change-request`, com análise de impacto pelo GP em ≤48h e decisão
  em ≤24h; (ii) mudanças que alterem marcos (M1–M4), o escopo do MVP, a linha de
  base ou a stack tecnológica — incluindo a stack SDD — exigem ADR específica
  (gatilhos de impacto transversal e irreversibilidade prática); (iii) nenhuma ADR
  pode contrariar esta Constituição: divergência com camada superior resolve-se por
  emenda (Art. 9.1), nunca por ADR; (iv) mudança que toque Kill Switch, Bypass
  Protocol ou os princípios do Art. 3 escala diretamente a emenda constitdoc-arch-0006-uc-v1ional com
  ratificação humana (Art. 5.2)."
- **Justificativa:** o projeto já opera um fluxo formal de mudança
  (`docs/planos/COBECO.pdf:2330-2340`; Tabela 34 do Plano de Integração;
  `:2158-2161`: mudança de stack exige ADR), mas a Constituição não o reconhece nem
  define a fronteira entre os dois fluxos — hoje, uma ADR poderia, na prática,
  tentar emendar a lei sem o rito do Art. 9.1.
- **Fonte:** COBECO.pdf:2330-2340, :2158-2161, Tabela 34; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Arts. 2, 5.2,
  9.1-9.2.

### E-06 [REQUER RATIFICAÇÃO CCB] — Precisão do gate de forja (Art. 4.7)
- **Artigo alvo:** Art. 4.7 (`constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:48`).
- **Texto atual:** "**Gate de forja:** agente só é promulgado com score ≥ 85/100 em
  `validate_afa_output.py` (16 seções, RT ≥ 8 vetores, FAIL-CLOSED ≥ 6, métricas ≥
  8)."
- **Texto proposto:** "**Gate de forja:** agente só é promulgado com score ≥ 85/100
  em `validate_afa_output.py` (19 cabeçalhos canônicos §§0–16, Kill Switch ≥5, DOs
  ≥15, DON'Ts ≥15, Red Team ≥8, FAIL-CLOSED ≥6, métricas ≥8; seção faltante ou
  mínimo não atingido = rejeição independente do score)."
- **Justificativa:** o parêntese atual é impreciso frente ao gate real: o script
  exige 19 cabeçalhos (SECTIONS: 0, 0.1, 0.2 + 1–16), mínimos KS ≥5 / DOs ≥15 /
  DON'Ts ≥15 (MIN_COUNTS) e rejeição estrutural fail-closed independente de score.
  O corte ≥85 está correto (`CUT_SCORE = 85`).
- **Fonte:** scripts/validate_afa_output.py linhas 12-14, 31, 34-45, 124-133;
  constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:48.

### E-07 [REQUER RATIFICAÇÃO CCB] — Re-ancoragem transitória do freeze (Art. 1.3)
- **Artigo alvo:** Art. 1.3 (`constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:14`).
- **Texto atual:** "Nada fora do escopo congelado (ADR-005) entra sem emenda
  constitdoc-arch-0006-uc-v1ional prévia."
- **Texto proposto:** "Nada fora do escopo congelado entra sem emenda constitdoc-arch-0006-uc-v1ional
  prévia. Fonte transitória do congelamento: TAP v3 (18/09/2026) sob regime de
  freeze com precedência intra-TAP §6 (NC-00 e NC-C4, Notas de Contexto; Tabela 55),
  decisão do GP de 21/09/2026. Esta referência é substituída pela ADR-005 assim que
  repromulgada com conteúdo integral (Art. 2, nível 3)."
- **Justificativa:** o Art. 1.3 hoje legisla sobre um instrumento vazio (G-06:
  ADR-005 = 0 bytes no HEAD, `git show dd3b087:…` = 0 bytes). As Notas de Contexto
  do plano integral (`docs/planos/plano-integral-tap-1-2-3-4-5.md:464` — NC-00,
  incluindo "ADR-005 encaminhada para emissão antes do M2") e do PDF
  (`:2796`, `:3048-3054`) são os registros sobreviventes do regime. A emenda é
  TRANSITÓRIA e não substitui a obrigação de repromulgar a ADR-005 (parcel ao
  architect/PM).
- **Fonte:** git dd3b087 (mensagem e conteúdo vazio); plano-integral:10, :206, :464;
  COBECO.pdf:2796, :3048-3054; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:14, Art. 2.

### E-08 [REQUER RATIFICAÇÃO CCB] — WIP por pessoa (micro-emenda)
- **Artigo alvo:** Art. 6.2 (`constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:60`).
- **Texto atual:** "…→ In Progress (WIP ≤ 3) →…"
- **Texto proposto:** "…→ In Progress (WIP ≤ 3 por pessoa) →…"
- **Justificativa:** o limite canônico é 3 cards por pessoa (equivalente a 9 no
  time): `docs/planos/COBECO.pdf:1677` ("3 cards em 'In Progress' por pessoa") e
  Tabela 32 ("WIP em fluxo ≤ 9 (3 × 3 pessoas)"). Sem o qualificador, o Art. 6.2
  pode ser lido como limite global de 3 — contradição operacional com o plano.
- **Fonte:** COBECO.pdf:1642, :1677, :1817-1818; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:60.

---

## 3. MATRIZ DE RASTREABILIDADE — FONTE → ARTIGO → EMENDA

| # | Fonte (arquivo:linha/artigo) | Achado | Artigo alvo | Emenda | Status |
|---|---|---|---|---|---|
| 1 | registry.yaml:406-414; test_nexus_yaml.py:107-118; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:46 | slug legado no Art. 4.5 | Art. 4.5 | E-01 | proposta |
| 2 | constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:3, :52-54, :83 | co-assinatura pendente sem rito | Art. 5 (novo 5.4) + cabeçalho | E-02 | proposta |
| 3 | HF-0001 (canon Humano); registry:277-285; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md (0 hits Docker); COBECO.pdf (0 hits Docker) | sem cláusula Docker/ortogonalidade | Art. 10 (novo) | E-03 | proposta (KG-04) |
| 4 | COBECO.pdf:2191 + Tabela 40; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:27-38 | YAGNI/first-principles fora da lei | Art. 3 (P-11, P-12) | E-04 | proposta (KG-01 p/ P-12) |
| 5 | COBECO.pdf:2330-2340, :2158-2161, Tabela 34; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:76-79 | CR→ADR→CCB sem ponte com Art. 9 | Art. 9 (novo 9.3) | E-05 | proposta |
| 6 | validate_afa_output.py:12-14,31,34-45,124-133; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:48 | parêntese do Art. 4.7 impreciso | Art. 4.7 | E-06 | proposta |
| 7 | git dd3b087 (0 bytes); plano-integral:10,206,464; COBECO.pdf:2796,3048-3054; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:14 | ADR-005 vazia; freeze sem instrumento | Art. 1.3 | E-07 | proposta transitória |
| 8 | COBECO.pdf:1642,1677,1817-1818; constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:60 | WIP ≤3 sem "por pessoa" | Art. 6.2 | E-08 | proposta |
| 9 | nexus_dispatcher.py:75,79; afa-changelog.md:2 | slug legado em código/espec | — | — | recomendação (parcel backend-dev / SIR) |
| 10 | ls docs/decisoes (0 bytes ×5) | camada ADR oca | — | — | recomendação (parcel architect/PM: repromulgar ADRs) |
| 11 | wc/git show: requisitos.md, tap.md, eap.md (0 bytes) | camada spec oca | — | — | recomendação (parcel PM/docer: repovoar) |
| 12 | COBECO.pdf Tabela 44 (~:2530) vs constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:30 | "sem cloud paga" vs P-02 total | — | — | veredito: P-02 prevalece; saneamento do plano (PM) |
| 13 | COBECO.pdf:2156 vs constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:30 | "Qwen 32B" vs `qwen30b-moe` | — | — | veredito: Constituição prevalece (Art. 2); saneamento (PM/docer) |
| 14 | COBECO.pdf:1638-1661, 1809-1830 vs constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:60, :34 | ADR-002/003 vs Art. 6.2/P-06 | — | — | veredito: sem contradição (ADRs vazios; PDF coerente) |
| 15 | afa-changelog.md:2 vs constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md:10-79 | cita "Art. 15.4" inexistente | — | — | recomendação (SIR — custódia do sdd-specialist) |

---

## 4. KNOWLEDGE GAPS DECLARADOS (P-08)

- **KG-01:** "first-principles" sem fonte escrita localizada (0 hits no PDF). A
  proposta P-12 nasce do canon do Humano (HF-0001) — requer ratificação CCB para
  existir como lei.
- **KG-02:** texto integral das ADRs 001–005 NÃO existe no repositório (arquivos de
  0 bytes desde o commit de emissão). O que sobrevive: mensagens de commit dd3b087,
  COBECO.pdf e plano-integral-tap. Nenhuma citação de conteúdo ADR além dessas fontes
  foi feita nesta proposta.
- **KG-03:** `.ai/specs/tap.md`, `.ai/specs/requisitos.md`, `.ai/specs/eap.md` e
  `docs/requisitos/requisitos.md` vazios. O TAP foi consultado pela reprodução
  integral em `docs/planos/plano-integral-tap-1-2-3-4-5.md:10`.
- **KG-04:** canon Docker ("camadas ortogonais em containers docker próprios") sem
  registro em Constituição ou PDF; E-03 nasce exclusivamente do canon declarado no
  envelope TA-0002/HF-0001 e do fato de o roster já promulgar agente Docker.

## 5. RESTRIÇÕES E CONFORMIDADE

- Kill Switch herdado respeitado: nenhum arquivo de lei editado (constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md,
  docs/decisoes/*, docs/planos/* intocados); trabalho 100% local; sem telemetria;
  sem PII (ratificador identificado por PAPEL, não nome — E-02); slugs em EN,
  narrativa em PT-BR (P-10); YAGNI: 8 emendas, todas nascidas de evidência citada,
  nenhuma capacidade especulativa proposta.
- **Validação (quem valida e o DoD):** agent-reviewer audita citações
  (linha-a-linha) e testabilidade; agent-project-auditor emite parecer (Art. 9.1);
  CCB humana ratifica (Art. 5.1/5.2). DoD desta spec: artefato criado em
  `.ai/specs/spec-001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta.spec.md`, contendo inventário com evidência
  (§1), emendas no rito Art. 9.1 (§2) e matriz de rastreabilidade (§3).
- Critérios de aceite: [x] gaps com evidência arquivo+linha; [x] 8 hipóteses do
  envelope avaliadas com veredito; [x] emendas com texto atual/proposto/justificativa/
  fonte; [x] marcação REQUER RATIFICAÇÃO CCB; [x] KGs declarados; [x] matriz fonte→
  artigo→emenda; [x] arquivo ≤400 linhas.

## CHANGELOG

- 0.1.0 — 2026-10-25: proposta inicial R1 (WS-1): 13 gaps (G-01..G-13, sendo 3
  vereditos sem emenda), 8 emendas propostas (E-01..E-08), 4 KGs declarados.
- 0.1.0 — 2026-11-05 (refinamento de ratificação, Grupo B): frontmatter atualizado ao
  padrão TA-0031 ratificado (adicionado `wave: WS-1`, `handoff` em `origin`; `updated`
  2026-10-25 → 2026-11-05; `status: draft` → `ratificada`). Ratificação CCB 05/11/2026
  (instrumento RAT-2026-11-05-A16, ADR-LOG-012). Aderência ao padrão de nomenclatura
  `spec-NNN-specname.spec.md` confirmada (ADR-018, RAT-2026-11-05-A18). Nenhuma decisão
  de negócio das §§1–5 reescrita.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

Normalização estrutural (TA-0031, HF-0031): `spec_id` atualizado de `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-round-1-proposta-1` para `spec-001` (slug `spec_id-specname.spec.md`); conteúdo das §1–§5 e do CHANGELOG preservado; nenhuma linha anterior renumerada (referências `arquivo:linha` históricas permanecem válidas).

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho — spec_id, versão, status, custódia, datas, origem | frontmatter (`spec_id: spec-001`, `version: 0.1.0`, `status: ratificada`, `created: 2026-10-25`, `updated: 2026-11-05`, `origin: TA-0002 | handoff: HF-0001`) | aplicada |
| (b) Contexto/origem | parágrafo inicial sob o H1 (rito Art. 9.1 e Art. 5.1; WS-1) | aplicada |
| (c) Resolução de conflitos | §1 (inventário de gaps/drifts/contradições com veredito por item) | aplicada |
| (d) Corpo de decisões/requisitos | §2 (emendas E-01..E-08 no formato Art. 9.1) | aplicada |
| (e) Critérios de aceite/testes | §5 ("Critérios de aceite" — lista de checkboxes do DoD desta spec) | aplicada |
| (f) Rastreabilidade | §3 (matriz fonte → artigo → emenda) + frontmatter `trace` | aplicada |
| (g) Fora de escopo (YAGNI) | §5 (restrições e conformidade: zero escrita fora deste arquivo; nenhum arquivo de lei/plano/TAP/ADR tocado) | aplicada como restrições; YAGNI de produto: `UNKNOWN - verify` |
| (h) Changelog | CHANGELOG (0.1.0) | aplicada |

Nota de honestidade (P-08): o DoD da emissão original (TA-0002, §5) fixava "arquivo ≤400 linhas"; após a normalização TA-0031 o arquivo tem 413 linhas — excedido em 13 apenas pelo bloco de camadas desta tarefa (MAPA + esta nota, anexados ao final; zero linha pré-existente renumerada), declarado aqui e não silenciado.
