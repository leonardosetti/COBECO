---
id: ai-specs-kb-taxonomy
title: Taxonomia unificada da base de conhecimento COBECO (SSOT particionado ortogonal)
type: spec
version: 1.1.0
status: ativo
owner: agent-sdd-specialist
derived-from:
- TA-0007 (analyst), TA-0008 (pm), TA-0009 (architect), TA-0010 (auditor AUD-2610-01) via .ai/agents/config-ledger-0001-ledger-v1.0.yaml
- constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Art. 2, Art. 4.6, Art. 6.1, Art. 9, principios P-04/P-05/P-08
- docs/decisoes/ADR-004-tasklists.md
- docs/decisoes/ADR-005-freeze.md (escopo congelado Arts. 1.2-1.3)
- .config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0/agents/agent-sdd-specialist.md (custodia .ai/specs)
last-revised: '2026-10-23'
lgpd-class: n/a
tags:
- specs
- docs
- adequado-a-norma
---

# 1. METADADOS DE VERSIONAMENTO (frontmatter YAML obrigatorio)

Todo artefato de conhecimento (novo ou migrado) carrega YAML frontmatter com EXATAMENTE estes 10 campos:

```yaml
id: <PREFIXO-NNN do padrao | slug kebab-case>   # padrao por classe (Secao 2); specs usam <SLUG>-NNN
title: <titulo em PT-BR>
version: MAJOR.MINOR.PATCH          # bump semantico (Secao 4)
class: <uma das 10 classes da Secao 2>   # EXATAMENTE uma; classes sao ortogonais
status: draft | active | ratified | archived    # enum do ciclo Secao 4
owner: <agent-custodio-slug>        # custodia constitdoc-arch-0006-uc-v1ional Art. 4
derived-from:                       # fontes upstream: caminhos ou IDs (ledger/parcelas)
  - <path|id>
last-revised: YYYY-MM-DD
lgpd-class: n/a | pessoal-basico | financeiro    # n/a por padrao (P-04: minimo necessario)
caveats:                            # lista; [] se nenhum — a chave nunca e omitida
  - "UNKNOWN-GAP: <topico>; acao: <artefato-alvo>"
```

Regras:
1. **YAGNI:** nada alem dos 10 campos. Novo campo exige proposta a CCB com necessidade demonstrada e critério testável de uso; campo sem caso de uso = violacao (gate Secao 6).
2. Artefato 0B ou sem frontmatter = violacao de DoR ("nao-0B ou gap declarado" — AUD-2610-01/F-06).
3. `derived-from` nao vazio satisfaz P-05/P-08 (toda alegacao com fonte; silencio documental = defeito).

# 2. CLASSES TAXONOMICAS ORTOGONAIS (10 — papeis sem sobreposicao)

| Classe | Proposito unico (papel no DAG SDD) | Caminho canonico | Formato | Owner | Regra de nao-duplicacao | DoR |
|---|---|---|---|---|---|---|
| `doc-decisao` | Registrar decisao nao-trivial com rastreio (P-05) | `docs/decisoes/ADR-NNN-*.md` | ADR Markdown | architect | 1 decisao = 1 ADR; outros artefatos citam ADR por caminho, nunca recopiam conteudo | nao-0B ou gap declarado |
| `plan` | Governo do projeto (TAP integral + planos de area PMBOK) | `docs/planos/`, `docs/tap/TAP.md` | Markdown (docx/pdf = export derivado) | pm | Planos de area nao repetem TAP; referenciam `TAP.md#<secao>` | nao-0B ou gap declarado |
| `okb` | Conhecimento tecnico-aplicado (stack, hardware, LLM, metodo) em **1 corpora unica** | `docs/conhecimento/OKB.md` | Markdown | architect | OKB unico SSOT; variantes historicas migradas para `archived` e referenciadas, nunca recopiadas | nao-0B ou gap declarado |
| `glossario` | Vocabulario normativo (definicao unica por termo) | `docs/conhecimento/glossario.md` | Markdown | sdd-specialist | Termo definido apenas aqui; demais artefatos linkam o termo | nao-0B ou gap declarado |
| `licoes` | Retrospectiva por milestone (conhecimento temporal, valido para o acordado em cada MF) | `docs/conhecimento/licoes-aprendidas/MF*.md` | Markdown (1 arquivo por MF-N) | pm | Fica confinada ao MF-N; promocao para OKB exige parecer de revisao | nao-0B ou gap declarado |
| `requisito` | Requisitos funcionais/nao-funcionais (camada 5 do Art. 2) | `docs/requisitos/requisitos.md` | Markdown | po | Unico arquivo de requisitos; RF/RNF com IDs globais unicos | nao-0B ou gap declarado |
| `spec` | Especificacao SDD-ingestivel — canal EXCLUSIVO de spec do DAG (Art. 6.1; F-06/REQ-13) | `.ai/specs/` | Markdown com frontmatter Sec.1 | sdd-specialist | Spec nao replica requisitos nem decisoes; aponta por caminho os `requisito`/`doc-decisao` consumidos | nao-0B ou gap declarado |
| `diagrama` | Visualizacao por area (escopo, cronograma, custos, eap, qualidade, integracao) | `docs/diagramas/<area>/` | SVG/Mermaid (PNG = export derivado) | architect | SVG fonte unico por diagrama; PNG nunca editado diretamente | existir a fonte (svg ou mermaid) |
| `log-baseline` | Registro metrico/registro de dependencias (dados sequenciais) | `docs/metricas/`, `docs/dependencias/` | Markdown | pm | Baseline nunca reescrita retroativamente; correcao = nova entrada com data | registro inicial presente (P-08) |
| `archived` | Conteudo terminal: historico, duplicados, artefatos fora do canon — imutaveis | `docs/archive/` | Qualquer | sdd-specialist | Imutavel; nenhum artefato vivo pode citar archive como fonte, exceto por proveniencia | frontmatter coerente na migracao |

**Regra de encaixe:** todo artefato do repositorio tem EXATAMENTE UMA classe. Classes sao ortogonais por definicao de proposito (tabela acima); sobreposicao detectada e defeito de migracao, nao justificativa para classe nova; propostas de separacao vao ao pm/architect por parcela.

# 3. MAPA DE PARTICAO MIGRATORIA (somente o MAPEAMENTO e custodia desta spec; a migracao executavel pertence ao downstream TA-0012 e a aprovacao humana (CCB))

| Artefato atual (estado real verificado) | Classe → caminho-alvo | Status-alvo | Acao proposta |
|---|---|---|---|
| `docs/tap/TAP.md` (0B) + `TAP.docx` | `plan` → `docs/tap/TAP.md` | draft | Preencher a partir do docx; docx vira export derivado |
| `docs/planos/Plano-de-Projeto-COBECO_v1.0.md` + docx v1.0/v1.1 (divergentes) | `plan` → mesmo caminho | ratified | **Divergencia resolvida na Secao 4, item 6** — v1.1 `.md` canonico; docx export; v1.0 → archive |
| 13 planos de area + `plano-integral-tap-1-2-3-4-5.md` | `plan` → `docs/planos/` | draft | Planos 0B (comunicacoes, riscos, recursos) recebem `caveats: UNKNOWN-GAP` ate preenchimento |
| `docs/decisoes/ADR-001..004` (0B) | `doc-decisao` → in loco | draft | Preencher conforme P-08; ADR-005 (ratificado) serve de modelo de estrutura |
| `docs/conhecimento/OKB.md` (1080 linhas) | `okb` → mantem caminho | active | **3 corpora → 1**: absorver `drafts/OKB_COBECO_v3.1.md` e variantes v2.1 apos dedupe (decisao CCB pendente) |
| `docs/conhecimento/glossario.md` (344 linhas) | `glossario` → mantem caminho | active | Remover definicoes duplicadas com OKB; linkar termo ↔ OKB |
| `docs/conhecimento/licoes-aprendidas/MF1-3` (MF2/MF3 0B) | `licoes` → mantem caminho | draft | 0B = gap declarado em MF2/MF3 |
| `docs/requisitos/requisitos.md` (0B) | `requisito` → arquivo unico | draft | Popular a partir de TAP/parcela TA-0009 |
| `.ai/specs/{tap,eap,requisitos}.md` (0B) + `afa-changelog.md` + `estrutura-de-diretorios.md` | `spec` → in loco | draft | Stubs preenchidos como **pointers** (referenciam artefato real) ou `caveats: UNKNOWN-GAP: autor pendente` |
| `docs/map_report.md` (205l, artefato COBECO v3.2/legacy) | `archived` → `docs/archive/legacy-md-artifact/` | archived | Stack divergente do canon (FastAPI/SQLite/HTMX — TA-0009); mais nada o cita como fonte |
| `docs/conhecimento/drafts/` (27 arq.) | vivos → `okb`/`glossario` via merge; `[legacy]/*` e variantes v2.1/v3.1 → `archived` | draft | Dedupe pendente de CCB (caveat do frontmatter desta spec) |
| `docs/diagramas/` (6 areas, PNG+SVG) | `diagrama` → mantem caminho | active | Exigir svg/mermaid source por area (DoR da classe) |
| `docs/metricas/baseline.md` (0B), `docs/dependencias/registro.md` (0B) | `log-baseline` → in loco | draft/arquivo | Popular no M1: dependencias do stack canon quando codificar |
| `docs/archive/` (88 arq. legacy) | `archived` → mantem caminho | archived | Sem acao; sujeito apenas a auditoria/sdoc-arch-0006-uc-v1esao, nunca reativado como fonte viva |

Principio normativo de migracao: **uma fonte viva por conteudo**. Arquivos co-irmãos (docx/PNG/PDF) sao DERIVADOS do `.md`/SVG canônico e permanecem junto do fonte (ou em archive); nunca dois `.md` vivos com o mesmo proposito.

# 4. CICLO DE VIDA E NOMENCLATURA DE VERSÃO

```
draft ──> active ──> ratified ──┐
  ▲                    (CCB)    │
  └── rework solicitado via parcela (Art. 6.1: gate/audit)
                               └──> archived (imutavel; nova versao viva pode substitui-lo)
```

1. `draft`: em constrdoc-arch-0006-uc-v1ao. Consumo pelo DAG restrito a interrogacao; nunca merge/commit de codigo a partir dele.
2. `active`: conteudo validado pelos gates da Secao 6. O DAG consome (Secao 5).
3. `ratified`: ratificacao humana em CCB (Art. 5). Minimo obrigatorio: constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon, ADRs, TAP/plano-mestre; demais classes ratificaveis quando a CCB decidir. Ratificado = passivel de auditoria.
4. `archived`: terminal; so acessivel para auditoria/sdoc-arch-0006-uc-v1esao (Art. 8.2); nenhum link ativo o cita como fonte.
5. `Nomenclatura`: `MAJOR.MINOR.PATCH` — MAJOR: altera contrato ou alcance do artefato (ex.: nova classe taxonomica → nova versao da taxonomy); MINOR: conteudo substancial novo (ex.: corpo de um plano 0B preenchido); PATCH: correcao/clarificacao sem mudanca semantica. Cada edicao registra: bump no frontmatter + entrada de changelog no rodape do artefato (persona DO-04).
6. **Versão unica por artefato vivo:** um path canônico live carrega EXATAMENTE UMA versão. Divergencias existentes (Plano-de-Projeto v1.0 vs v1.1; OKB v2.1/v3.1) resolvem-se: versao mais recente prevalece como canonica; versoes anteriores movem-se para `docs/archive/legacy-backups/` com frontmatter `derived-from` apontando para a sdoc-arch-0006-uc-v1esora. **Nunca reativar versao arquivada como canonica** (gate da auditoria F-11).

# 5. FORNECIMENTO PARA O CICLO SDD (como o SDD v2 consome a taxonomia)

1. **Ingresso (o canal):** `.ai/specs/` e o UNICO canal de especificacoes para o DAG SDD (Art. 6.1, REQ-13/F-06). Nenhum trabalho de constrdoc-arch-0006-uc-v1ao (code) nasce de backlog, conversa ou artefato fora do canal; planos (`docs/planos/`) alimentam SPECS, nunca o codigo diretamente.
2. **Consumo (durante o ciclo):** cada spec declara no frontmatter `derived-from` os artefatos consultados com `class` + `version`; o ciclo v2 (`sdd-cycle.sh`) valida este inventario antes do dispatch.
3. **Gap-declarado (P-08):** qualquer spec pode declarar:
   `UNKNOWN-GAP: <topico>; acao: <artefato-alvo>`
   Nada prossegue (handoff/merge downstream) sobre conteudo tocado por gap sem que o gap esteja declarado ou resolvido — fail-closed (persona FC-5).
4. O ciclo (`sdd-cycle.sh v2`: parser → dispatcher → config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0 run) inspeciona a spec antes do run; spec `draft` com `caveats` pode seguir para o DAG desde que declare os UNKNOWN-GAPs pendentes em seu frontmatter.

# 6. GATES DA TAXONOMIA (checklist pre/post-migration; violacao = BLOCK fail-closed)

| # | Gate | Regra |
|---|---|---|
| G1 | YAGNI-frontmatter | Nada alem dos 10 campos da Secao 1; campo extra sem ratificação CCB = BLOCK |
| G2 | Fonte-unica | Nenhuma ideia em 2 classes (Sobreposicao = defeito); conteudo vivo nunca duplicado — links por referencia |
| G3 | Nao-0B | Todo artefato deve ser nao-0B OU ter `caveats` com UNKNOWN-GAP declarado; 0B silencioso = BLOCK |
| G4 | Enum classes | `class` ∈ 10 da Secao 2; valor fora = BLOCK |
| G5 | LGPD-screen | `lgpd-class` presente e avaliado (P-04); `pessoal-basico`/`financeiro` exigem nota de minimizacao no corpo |
| G6 | Versão única | 1 path live = 1 versão; divergencia v1.0/v1.1 resolvida ANTES de ratificar (Secao 4, item 6) |
| G7 | Fallback | Encaixe impossível → classificar `archived` + propor classe nova AO HUMANO (CCB, Art. 9); nunca inventar classe silenciosamente; proposta registrada no ledger |

**Propriedade da custodia:** o agent-sdd-specialist aplica G1..G7 a cada spec que autorar e a cada spec entrante por parcela (ACCEPT do nexus_dispatcher); o agent-reviewer e o agent-gatekeeper auditam esses gates nos pareceres de auditoria de milestone (AUD: F-04/F-06/F-10/F-01/F-11).

---

**Traceabilidade (fontes):** constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md Arts. 2/4.6/5/6/9 e P-04/P-05/P-08 (fontes de enum/ciclo/gates); parcelas TA-0007..TA-0010 (ledger .ai/agents/config-ledger-0001-ledger-v1.0.yaml); AUD-2610-01 F-04/F-06/F-10/F-01/F-11 (motivos); ADR-004-tasklists.md (bump semantico de listas); ADR-005-freeze.md Arts. 1.2-1.3 (escopo congelado; backlog espelha escopo); persona agent-sdd-specialist (custodia .ai/specs, kill-switch herdado, YAGNI).

**Ratificação:** RATIFICADA por CCB do Humano em 23/10/2026 — aplicada e ratificada na prática pelos itens C1–C5 (ledger TA-0013; versão 1.1.0). A parte executável da migracao mapeada na Seção 3 que exige decisão humana explícita (mescla docx v1.0/v1.1; merge remanescente de drafts) permanece PENDENTE de CCB; demais frentes executadas: dedupe OKB (v4.0.0, TA-0017), grafia (glossário v3.2.0), planos de área e specs preenchidos (TA-0013..TA-0016).
