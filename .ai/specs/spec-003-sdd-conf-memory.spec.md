---
id: ai-specs-spec-003-sdd-conf-memory-spec
title: DOCUMENTO CANÔNICO DE EXECUÇÃO FASEADA — v3.1.0
type: spec
version: 1.0.0
status: ativo
owner: agent-project-analyst
derived-from:
- .ai/specs/spec-003-sdd-conf-memory.spec.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-05'
lgpd-class: n/a
tags:
- specs
- docs
- adequado-a-norma
---
---
spec_id: spec-003
specname: sdd-conf-memory
version: 3.2.0
status: ratificada
custody: agent-sdd-specialist (.ai/specs/)
created: 2026-10-30
updated: 2026-11-05
origin: run CANON-20261029-01 (ADR-011) + commit 149067f (2026-10-30) | handoff: UNKNOWN - verify
task: TA-0300 | sender: agent-nexus-prime-ultimate
kill_switch: inherited
wave: WS-4 | Onda 4 — Execução Técnica (memória persistente SDD)
lgpd-class: n/a (zero PII neste artefato; P-04, constitution.md:90)
trace:
  - ADR-011 (v1.0.0, aprovado CCB 29/10/2026)
  - scripts/validate_afa_output.py, scripts/nexus_dispatcher.py
  - .ai/agents/registry.yaml (roster SSOT)
  - ratificada CCB 05/11/2026 (instrumento RAT-2026-11-05-A16, ADR-LOG-012)
---

# DOCUMENTO CANÔNICO DE EXECUÇÃO FASEADA — v3.1.0

## Second Brain · Memória Persistente · MCPs · Prompt Ubíquo

### Input canônico reescrito em pacotes atômicos, com guarda de integridade e rollback obrigatório

**Run ID:** `CANON-20261029-01`
**ADR de cobertura:** `ADR-011` (v1.0.0, aprovado CCB 29/10/2026)
**Norma suprema:** `constitution.md` v1.1.0 — Art. 2
**Modelo executor:** `Qwen3-30B-A3B-Q4_K_M` (MoE, 3B ativos)
**kill_switch:** `inherited`
**Status:** Especificação. **Nenhuma ação executada por este documento.**

---

# PARTE 0 — DIAGNÓSTICO: POR QUE O v3.0.0 FALHARIA EM UMA RODADA

Aplicando a crítica ao próprio artefato anterior, identifico **cinco falhas de engenharia de contexto**:

| ID             | Falha do v3.0.0                                         | Consequência operacional                                                      | Correção neste v3.1.0                                                                                                        |
| -------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| **F-01** | O playbook inteiro era oferecido como prompt de sessão | ~15–20k tokens de instrução + leituras → estouro antes da primeira escrita | O playbook **não é prompt**. Vira repositório de pacotes. O driver emite **um** pacote por sessão.             |
| **F-02** | Instrução "faça as fases 0→4" em sequência         | Modelo tenta completar tudo; estado intermediário nunca persistido            | Máquina de estados em `ledger.yaml → canon_run`. Uma fase por sessão. Avanço só por parcel validada.                    |
| **F-03** | Guardrail de backup era **prosa**, não mecanismo | LLM pode sobrescrever `opencode.json` sem快照                                | Toda escrita de config passa por `canon_guard.py write`. Sem snapshot → `exit 1`.                                         |
| **F-04** | IDs de tarefa inválidos (`TA-RECONCILE-001`)         | `TASK_ID_RE = ^[A-Z]{2}-\d{3,4}$` rejeita; dispatcher falha                  | Todos os IDs normalizados para `TA-0300`…`TA-0312`. Errata registrada, ADR não editado sem CCB.                          |
| **F-05** | Propunha tocar 40 contratos de agente                   | Retrabalho massivo + 40 superfícies de corrupção                            | **Não tocar 40 contratos.** A camada ubíqua é `_base.md`. Apenas 2 contratos de custódia, opcional, fase separada. |

**Princípio corretor central:**

> **Prompt é aconselhamento. Filesystem é imposição.**
> Se a proteção depende do modelo "lembrar" de fazer backup, ela não existe.
> A proteção precisa estar num script que o modelo **não consegue pular para avançar de fase**.

---

# PARTE 1 — CONTRATO INEGOCIÁVEL DE EXECUÇÃO

## 1.1. Premissas de ambiente (somente fatos ratificados)

| Item                                       | Valor canônico                                                                              | Fonte                                 | Proibição                                     |
| ------------------------------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------- | ----------------------------------------------- |
| RAM total                                  | **58 GB** (não 64)                                                                    | `system-profile-20260907-133205.md` | Arredondar para cima em cálculo de viabilidade |
| Modelo principal                           | `Qwen3-30B-A3B-Q4_K_M.gguf` (MoE)                                                          | ADR-011 + config OpenCode             | Reverter para 27B/32B denso                     |
| Contexto configurado                       | `32768`                                                                                    | `.opencode/opencode.json` + unit    | Reduzir flag `-c` no service                  |
| Orçamento **político** por sessão | **24000 tokens**                                                                       | ADR-011 §2.1                         | Exceder                                         |
| Output máximo                             | `4096`                                                                                     | config OpenCode                       | Gerar parcel > 2048 tokens                      |
| Service                                    | `llama-server.service`, `MemoryMax=32G`, `-ngl 99`, `--flash-attn on`, `--no-mmap` | unit ratificado                       | **L1 intocável**                         |
| Obsidian                                   | vault já em `./docs/conhecimento/`                                                        | declaração CCB                      | Criar segundo vault                             |
| Personas                                   | `.ai/personas/` (não `prompts/`)                                                        | `lst.txt` real                      | Renomear diretório                             |
| Orquestrador                               | **inexistente** (Hermes rejeitado)                                                     | architecture_report                   | Reintroduzir framework                          |

## 1.2. Regras de escrita (hard rules)

1. **Nenhuma sobrescrita sem snapshot.** `canon_guard.py write` recusa se não houver `manifest.json` com hash de baseline do alvo.
2. **Nenhuma escrita fora da allowlist da fase.** O driver rejeita a parcel se `artifacts[]` contiver caminho não autorizado.
3. **Escrita atômica.** `tempfile` no mesmo diretório → `fsync` → `os.replace()`. Nunca `open(path, "w")` direto em config.
4. **Detecção de deriva.** Hash atual do alvo ≠ hash do baseline ⇒ `KS-04 DRIFT`, aborta, não sobrescreve.
5. **Lock exclusivo.** Duas fases nunca rodam em paralelo. Lock com PID + timestamp; stale só é rompido com autorização CCB.
6. **Backups fora do repositório.** `$HOME/.cache/cobeco-canon/backups/<run>/<snapshot>/`. Corrompeu o repo, o backup sobrevive.
7. **Idempotência.** Antes de criar, verificar existência + hash. Existindo e correto ⇒ `SKIPPED`, não reescrever.
8. **Regra de ouro `.ai/`.** Se não é lido por OpenCode ou por script, não entra. Máximo 10 entradas por diretório.
9. **L1 intocável.** Service systemd, binário llama-server, caminho do modelo, flags de inferência: **somente leitura**.
10. **Constitution acima de tudo.** Qualquer conflito ⇒ abortar, não "resolver criativamente".

## 1.3. Orçamento de contexto por sessão (mecânico)

| Componente                             | Budget                    |
| -------------------------------------- | ------------------------- |
| Router `_base.md`                    | ≤ 600 tokens             |
| Pacote de fase emitido pelo driver     | ≤ 1500 tokens            |
| Fatia de estado (`canon_run` apenas) | ≤ 300 tokens             |
| Leituras de trabalho (allowlist)       | ≤ 6000 tokens            |
| Raciocínio + saída                   | ≤ 4000 tokens            |
| **Margem de segurança**         | **≥ 11600 tokens** |
| **Teto absoluto**                | **24000 tokens**    |

**Regra:** se a soma estimada ultrapassar 24000, o agente **não lê o restante**. Emite parcel com `dod:false`, `reason:"KS-01 CONTEXT_BUDGET"`, e pede decomposição via CCB. Nunca compacta "por conta própria" arquivo de configuração.

---

# PARTE 2 — ARQUITETURA DE CONTROLE

## 2.1. Separação: o que é prompt, o que é dado, o que é mecanismo

```
┌─────────────────────────────────────────────────────────────────┐
│ L2 · .ai/personas/_base.md   ← ROUTER (~500 tokens, NÃO playbook) │
│    "Execute: python3 scripts/canon_run.py --emit-next"           │
└───────────────────────────┬─────────────────────────────────────┘
                            ↓ lê apenas a fase atual
┌─────────────────────────────────────────────────────────────────┐
│ L3 · .ai/specs/canon/*.md    ← REPOSITÓRIO DE PACOTES             │
│    INDEX.md + 00-foundation.md + 10-config.md                    │
│    + 20-mcp.md + 30-governance.md   (5 entradas, dentro do limite)│
└───────────────────────────┬─────────────────────────────────────┘
                            ↓ driver extrai UM pacote
┌─────────────────────────────────────────────────────────────────┐
│ MECANISMO · scripts/canon_run.py  ← MÁQUINA DE ESTADOS           │
│    --emit-next / --emit Fxx / --accept / --status / --block      │
└───────────────────────────┬─────────────────────────────────────┘
                            ↓ delega toda escrita
┌─────────────────────────────────────────────────────────────────┐
│ MECANISMO · scripts/canon_guard.py ← SNAPSHOT / WRITE / RESTORE  │
│    lock · snapshot · verify · write · restore · status           │
└───────────────────────────┬─────────────────────────────────────┘
                            ↓ estado persistente
┌─────────────────────────────────────────────────────────────────┐
│ SSOT · .ai/agents/ledger.yaml → canon_run (única fonte)          │
│ Backup · $HOME/.cache/cobeco-canon/backups/  (fora do Git)        │
└─────────────────────────────────────────────────────────────────┘
```

**Decisão first-principles:** o modelo nunca precisa carregar o playbook inteiro. Ele recebe **um pacote**, executa, devolve **uma parcel**, e o driver avança o estado. Reiniciar a sessão custa ~2k tokens, não 20k.

## 2.2. Estado persistente (extensão do ledger existente — não arquivo novo)

```yaml
# .ai/agents/ledger.yaml — acréscimo, preservando audit_trail existente
canon_run:
  run_id: "CANON-20261029-01"
  adr: "ADR-011"
  version: "3.1.0"
  state_version: 1
  current_phase: "F00"
  status: "NOT_STARTED"        # NOT_STARTED|RUNNING|BLOCKED|COMPLETED|ROLLED_BACK
  lock: null                   # {pid, hostname, acquired_at, phase}
  active_snapshot: null
  completed: []                # [{phase, task_id, parcel, snapshot, sha256_after, at}]
  blocked_reason: null
  budget:
    session_max_tokens: 24000
    packet_max_tokens: 1500
    output_max_tokens: 4096
```

**Não criar** `.ai/memory/`, `context-state.md`, `KB-BLOCKERS.md` ou `KB-DECISIONS.md`. SSOT já existe.

## 2.3. Estrutura de pacotes (dentro do limite de 10 entradas)

```
.ai/specs/canon/                 # 5 entradas
├── INDEX.md                     # mapa F00..F12 + ponteiros (não SSOT)
├── 00-foundation.md             # F00 F01 F02
├── 10-config.md                 # F03 F04 F05
├── 20-mcp.md                    # F06 F07 F08
└── 30-governance.md             # F09 F10 F11 F12
```

Cada pacote é delimitado por marcadores que o driver usa para extração:

```markdown
<!-- PHASE:F06 -->
...conteúdo do pacote...
<!-- /PHASE:F06 -->
```

---

# PARTE 3 — GUARDRAILS E KILL SWITCHES

## 3.1. Matriz de kill switch (determinística, com recuperação)

| ID              | Gatilho                                  | Detecção mecânica                                            | Ação imediata                      | Recuperação                                  |
| --------------- | ---------------------------------------- | --------------------------------------------------------------- | ------------------------------------ | ---------------------------------------------- |
| **KS-01** | Contexto > 24000 tokens                  | `--accept` rejeita parcel com `context_used_tokens > 24000` | Parar leitura; parcel `dod:false`  | CCB decompõe fase                             |
| **KS-02** | Violação `constitution.md`           | Avaliação semântica + Art. 2                                 | Abortar; registrar `audit_trail`   | CCB emenda                                     |
| **KS-03** | Snapshot ausente/incompleto              | `guard write` sem `--snapshot` válido                      | `exit 1`, nenhuma escrita          | Executar `guard snapshot`                    |
| **KS-04** | Deriva de hash no alvo                   | `hash_atual != baseline`                                      | Abortar; **não sobrescrever** | Investigar; novo snapshot com CCB              |
| **KS-05** | Escrita fora da allowlist                | `--accept` compara `artifacts[]` × allowlist               | Rollback automático dos alvos       | Refazer fase com pacote correto                |
| **KS-06** | Lock concorrente                         | `guard lock` falha                                            | Abortar; não esperar em loop        | Aguardar PID ou CCB autoriza `--break-stale` |
| **KS-07** | YAML/JSON inválido pós-escrita         | `yaml.safe_load` / `json.loads` no staging                  | Rejeitar staging; original intacto   | Corrigir conteúdo                             |
| **KS-08** | Sintaxe shell/Python inválida           | `bash -n` / `py_compile` no staging                         | Rejeitar staging                     | Corrigir                                       |
| **KS-09** | Auto-delegação / half-duplex violado   | `sender == target` no envelope                                | Rejeitar envelope                    | Redespachar para agente correto                |
| **KS-10** | `task_id` fora do regex                | `^[A-Z]{2}-\d{3,4}$`                                          | Rejeitar parcel                      | Normalizar ID                                  |
| **KS-11** | Tentativa de tocar L1                    | allowlist contém unit / binário / modelo                      | `exit 1`                           | CCB abre fase L1 específica                   |
| **KS-12** | `blocked_tasks` não vazio para a fase | leitura da fatia de estado                                      | Não iniciar                         | Resolver blocker primeiro                      |
| **KS-13** | > 10 entradas em diretório `.ai/`     | contagem no `--accept`                                        | Rejeitar criação                   | Consolidar                                     |
| **KS-14** | Invenção de conteúdo (spec/ADR/repo)  | origem não rastreável no pacote                               | Bloquear fase (`BLOCKED`)          | Fornecer fonte canônica                       |

## 3.2. Classes de risco e tratamento obrigatório

| Classe                                           | Exemplos                                                         | Exigência antes de escrever                                                                                                  |
| ------------------------------------------------ | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **R0 — novo arquivo**                     | `mcp_nexus_ledger.py`, `transversais.md`                     | Lock + verificação de inexistência + snapshot do diretório-pai (manifest)                                                 |
| **R1 — extensão aditiva**                | `ledger.yaml`, `KB-INDEX.md`                                 | Snapshot + hash baseline + prova de preservação do conteúdo pré-existente                                                 |
| **R2 — configuração viva** ⚠️         | `.opencode/opencode.json`, `.ai/personas/_base.md`           | Snapshot + `--dry-run-diff` + validação de schema + **prova de restore executada em arquivo de teste** + CCB ciente |
| **R3 — executável em produção** ⚠️️ | `download_model.sh`, `sdd-cycle.sh`                          | Snapshot + `bash -n` + execução em modo `--dry-run` + rollback testado                                                  |
| **R4 — intocável**                       | `llama-server.service`, binário, `.gguf`, `registry.yaml` | **Nenhuma escrita.** Somente leitura/verificação                                                                      |

> **Regra dura R2:** antes de modificar `opencode.json` ou `_base.md`, o agente deve executar `guard restore --selftest`, que comprova que o mecanismo de rollback realmente restaura um bytes-identical. Se o selftest falhar, **não se toca no arquivo vivo**.

---

# PARTE 4 — PROTOCOLO DE SNAPSHOT / ROLLBACK

## 4.1. Ciclo obrigatório de toda fase mutativa

```
1. guard lock --phase Fxx
2. guard snapshot --phase Fxx --targets <allowlist de arquivos existentes>
      → cria $HOME/.cache/cobeco-canon/backups/<run>/<ts>/
      → grava manifest.json {path, sha256_before, bytes, mode}
      → grava git_head + git_status (evidência)
3. ler APENAS os arquivos da allowlist de leitura
4. produzir nova versão em staging (FORA do caminho vivo)
5. validar staging (JSON/YAML/bash -n/py_compile/testes)
6. guard write --snapshot <ts> --path <alvo> --source <staging>
      → confere lock, allowlist, hash baseline
      → tmp + fsync + os.replace
      → registra sha256_after no manifest
7. gate de saída da fase (comandos do pacote)
8. parcel JSON → guard/canon_run --accept
9. guard unlock
```

**Se qualquer passo de 5 a 8 falhar:** `guard restore --snapshot <ts> --confirm-ccb` para os alvos já gravados. Nunca deixar configuração meia-escrita.

## 4.2. Comandos canônicos

```bash
# Aquisição de lock
python3 scripts/canon_guard.py lock --phase F08

# Snapshot dos alvos existentes (R1/R2/R3)
python3 scripts/canon_guard.py snapshot --phase F08 \
  --targets .opencode/opencode.json

# Prévia sem escrever
python3 scripts/canon_guard.py write --snapshot "$SNAP" \
  --path .opencode/opencode.json --source /tmp/opencode.new.json --dry-run

# Escrita atômica guardada
python3 scripts/canon_guard.py write --snapshot "$SNAP" \
  --path .opencode/opencode.json --source /tmp/opencode.new.json

# Verificação de deriva / integridade
python3 scripts/canon_guard.py verify --snapshot "$SNAP"

# Rollback (exige confirmação explícita)
python3 scripts/canon_guard.py restore --snapshot "$SNAP" --confirm-ccb

# Liberação
python3 scripts/canon_guard.py unlock
```

---

# PARTE 5 — MAPA DE FASES (sequência canônica)

| Fase          | Task ID     | Objetivo                                                    | Writes (allowlist)                                                                         | Risco        | Gate de saída                                                           | Bloqueio externo                             |
| ------------- | ----------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------ | ------------------------------------------------------------------------ | -------------------------------------------- |
| **F00** | `TA-0300` | Baseline forense + snapshot + criar repositório de pacotes | `.ai/specs/canon/*` (novos)                                                              | R0           | 5 arquivos presentes; `INDEX` coerente; nenhum config tocado           | —                                           |
| **F01** | `TA-0301` | Implementar guard + driver + selftest de rollback           | `scripts/canon_guard.py`, `scripts/canon_run.py`                                       | R0           | `py_compile` + `restore --selftest` OK                               | —                                           |
| **F02** | `TA-0302` | Integrar ADR-011 ao contexto (idempotente)                  | `docs/decisoes/ADR-011-sddai-v3.md`, `docs/decisoes/INDEX.md`                          | R1           | ADR indexada; sobreposições referenciadas                              | —                                           |
| **F03** | `TA-0303` | Estender `ledger.yaml` p/ schema v2 + `canon_run`       | `.ai/agents/ledger.yaml`                                                                 | R1           | YAML válido; `audit_trail` preservado; `current_session` presente   | F01                                          |
| **F04** | `TA-0304` | Perfis canônicos de hardware e modelos                     | `.ai/config/hardware-profile.yaml`, `.ai/config/models-catalog.yaml`                   | R0           | Valores rastreáveis; sem métricas inventadas                           | F03                                          |
| **F05** | `TA-0305` | Reconciliar `download_model.sh` (ex-`TA-RECONCILE-001`) | `download_model.sh`                                                                      | R3           | `bash -n` + dry-run + repo HF **verificado**                     | **repo HF não verificado ⇒ BLOCKED** |
| **F06** | `TA-0306` | MCP `nexus-ledger` + testes                               | `scripts/mcp_nexus_ledger.py`, `tests/agents/test_mcp_ledger.py`                       | R0           | testes verdes; ledger não corrompido                                    | F03                                          |
| **F07** | `TA-0307` | MCPs `dispatch`, `validate`, `kb`                     | 3 scripts novos em `scripts/`                                                            | R0           | wrappers chamam scripts existentes; sem lógica duplicada                | F06                                          |
| **F08** | `TA-0308` | Registrar MCPs no OpenCode                                  | `.opencode/opencode.json`                                                                | **R2** | JSON válido; restore selftest OK; endpoint responde                     | F07                                          |
| **F09** | `TA-0309` | `transversais.md` + índice KB                            | `docs/conhecimento/licoes-aprendidas/transversais.md`, `docs/conhecimento/KB-INDEX.md` | R0/R1        | gate de admissão aplicado; índice aponta                               | F03                                          |
| **F10** | `TA-0310` | Popular `eap.md`, `requisitos.md`, `tap.md`           | 3 specs                                                                                    | R1           | conteúdo derivado do **TAP v3 congelado**, sem invenção         | **TAP acessível ⇒ senão BLOCKED**   |
| **F11** | `TA-0311` | Instalar **router** ubíquo em `_base.md`           | `.ai/personas/_base.md`                                                                  | **R2** | router ≤ 600 tokens; personas específicas preservadas; restore testado | F08                                          |
| **F12** | `TA-0312` | E2E + métricas + encerramento                              | relatório em `docs/auditorias/`, `ledger.yaml`                                        | R1           | todos os gates verdes; parcel `dod:true`                               | todas                                        |

**Observação crítica de sequência:** F00 e F01 são **bootstrap manual** (ainda não existe driver). A partir de F02, tudo é dirigido por `canon_run.py --emit-next`.

---

# PARTE 6 — PACOTES DE FASE (unidades de sessão)

> Cada bloco abaixo é um **pacote autocontido**. Copie para o arquivo batch correspondente em `.ai/specs/canon/`. O modelo recebe **apenas um** por vez.

## 6.1. `00-foundation.md`

```markdown
<!-- PHASE:F00 -->
# F00 — Baseline e Bootstrap do Repositório de Pacotes
Task: TA-0300 | Risco: R0 | Leitura: este pacote apenas
Escrita permitida: .ai/specs/canon/{INDEX.md,00-foundation.md,10-config.md,20-mcp.md,30-governance.md}
Proibido: qualquer arquivo existente fora da allowlist; L1; registry.yaml

OBJETIVO
Instalar o mapa de fases como dado de projeto. NÃO implementar código nesta fase.

AÇÕES
1. Registrar baseline de integridade (somente leitura):
   git rev-parse HEAD; git status --porcelain
   sha256sum .opencode/opencode.json .ai/personas/_base.md \
     .ai/agents/ledger.yaml download_model.sh > /tmp/canon-baseline.txt
2. Criar .ai/specs/canon/ com EXATAMENTE 5 entradas (INDEX + 4 batches).
3. Copiar para os batches os blocos PHASE correspondentes deste playbook.
4. INDEX.md deve conter: tabela F00..F12, Task IDs, classes de risco,
   dependências, e a linha "SSOT de estado: .ai/agents/ledger.yaml → canon_run".
5. NÃO criar .ai/memory/, nem context-state.md, nem segundo vault Obsidian.

GATE DE SAÍDA
test $(find .ai/specs/canon -maxdepth 1 -type f | wc -l) -eq 5
grep -q 'PHASE:F12' .ai/specs/canon/30-governance.md
sha256sum -c /tmp/canon-baseline.txt   # DEVE continuar íntegro

PARCEL: task_id=TA-0300, dod=true, artifacts=[5 arquivos], baseline_intact=true
KILL: KS-03 se baseline mudou; KS-13 se >5 entradas; KS-11 se tocou L1.
<!-- /PHASE:F00 -->
```

```markdown
<!-- PHASE:F01 -->
# F01 — Motor de Guarda e Driver de Estados
Task: TA-0301 | Risco: R0 | Leitura: pacote + /tmp/canon-baseline.txt
Escrita permitida: scripts/canon_guard.py, scripts/canon_run.py
Proibido: modificar scripts existentes; tocar opencode.json

OBJETIVO
Implementar os dois mecanismos descritos na Parte 7. Arquivos NOVOS.

AÇÕES
1. Criar canon_guard.py com: lock, unlock, snapshot, verify, write, restore,
   restore --selftest. Backup em $HOME/.cache/cobeco-canon/backups/<run>/.
2. Criar canon_run.py com: --emit-next, --emit Fxx, --accept, --status, --block.
3. Validar: python3 -m py_compile scripts/canon_guard.py scripts/canon_run.py
4. PROVAR rollback: criar arquivo temporário de teste, alterá-lo, restaurar,
   comparar sha256. Guardar evidência em /tmp/canon-restore-selftest.txt.
5. NÃO conectar ao OpenCode nesta fase.

GATE DE SAÍDA
python3 -m py_compile scripts/canon_guard.py scripts/canon_run.py
python3 scripts/canon_guard.py restore --selftest   # exit 0
python3 scripts/canon_run.py --status              # exit 0 ou NOT_STARTED

PARCEL: dod=true, artifacts=[2 scripts], selftest_sha256=<hash>
KILL: KS-07/KS-08 se sintaxe inválida; KS-03 se selftest falhar.
<!-- /PHASE:F01 -->
```

```markdown
<!-- PHASE:F02 -->
# F02 — Integração da ADR-011 (idempotente)
Task: TA-0302 | Risco: R1 | Leitura: ADR-011 fornecida, docs/decisoes/INDEX.md
Escrita permitida: docs/decisoes/ADR-011-sddai-v3.md, docs/decisoes/INDEX.md

PRECONDIÇÃO: F01 COMPLETED. Guard lock + snapshot dos alvos existentes.

AÇÕES
1. Verificar se ADR-011 já está em docs/decisoes/. Se sim e hash confere → SKIPPED.
2. Se ausente, gravar ADR-011 com o texto CCB-ratificado (não rescrever conteúdo).
3. Acrescentar entrada no INDEX.md referenciando ADR-011 e suas sobreposições
   parciais: ADR-006 (Módulo Inteligência SDD) e ADR-001 (stack local).
4. Registrar errata OPERACIONAL (não editar ADR): o ID "TA-RECONCILE-001"
   viola TASK_ID_RE; mapping canônico = TA-0305. Anotar no INDEX, não na ADR.
5. Preservar integralmente o corpo aprovado da ADR.

GATE
test -f docs/decisoes/ADR-011-sddai-v3.md
grep -q 'ADR-011' docs/decisoes/INDEX.md
grep -q 'TA-0305' docs/decisoes/INDEX.md   # errata de mapping

KILL: KS-02 se alterar conteúdo CCB; KS-04 se hash de baseline divergir.
<!-- /PHASE:F02 -->
```

## 6.2. `10-config.md`

```markdown
<!-- PHASE:F03 -->
# F03 — Schema v2 do ledger + canon_run
Task: TA-0303 | Risco: R1 | Leitura: .ai/agents/ledger.yaml
Escrita permitida: .ai/agents/ledger.yaml (APENAS acréscimo)

PRECOND: F02 COMPLETED. snapshot obrigatório. Selftest de rollback OK.

AÇÕES
1. Ler ledger atual. Preservar TODAS as chaves e entradas existentes.
2. Acrescentar bloco canon_run conforme Parte 2.2, current_phase=F04,
   status=RUNNING, lock=null, completed=[F00,F01,F02,F03 após validação].
3. Acrescentar current_session e blocked_tasks se ausentes (não substituir).
4. Escrever staging → yaml.safe_load → comparar chaves originais preservadas
   → guard write → verify.

GATE
python3 - <<'PY'
import yaml
d=yaml.safe_load(open('.ai/agents/ledger.yaml'))
assert 'canon_run' in d and 'audit_trail' in d
assert d['canon_run']['budget']['session_max_tokens']==24000
PY

KILL: KS-07 se YAML inválido; KS-04 se audit_trail original alterado.
<!-- /PHASE:F03 -->
```

```markdown
<!-- PHASE:F04 -->
# F04 — Perfis canônicos de hardware e modelos
Task: TA-0304 | Risco: R0 | Leitura: system-profile, hardware.md, unit, opencode.json
Escrita permitida: .ai/config/hardware-profile.yaml, .ai/config/models-catalog.yaml

AÇÕES
1. Criar hardware-profile.yaml: RAM 58GB (medido), 8C/16T, AVX-512,
   RDNA3/radv, kernel zen, MemoryMax=32G, paths /var e /extra.
2. Criar models-catalog.yaml: primary=Qwen3-30B-A3B Q4_K_M (MoE 3B ativos),
   context_configured=32768, context_policy=24000, output_max=4096;
   fallback=14B (PLANNED), batch=72B (DEFERRED); deprecated=27B/32B denso.
3. Marcar todo campo NÃO medido como "target" ou "unverified". NUNCA como medido.
4. Não inventar throughput. t/s é target até benchmark em F12.

GATE
python3 -c "import yaml;[yaml.safe_load(open(p)) for p in ['.ai/config/hardware-profile.yaml','.ai/config/models-catalog.yaml']]"
grep -q 'total_gb: 58' .ai/config/hardware-profile.yaml

KILL: KS-14 se inventar valor; KS-11 se tentar alterar unit/modelo.
<!-- /PHASE:F04 -->
```

```markdown
<!-- PHASE:F05 -->
# F05 — Reconciliação de download_model.sh  (ex-TA-RECONCILE-001)
Task: TA-0305 | Risco: R3 | Leitura: download_model.sh, qwen_list.txt
Escrita permitida: download_model.sh

BLOQUEIO EXTERNO OBRIGATÓRIO
qwen_list.txt anexado está VAZIO. Não há evidência do repositório HF do MoE.
Portanto: NÃO escrever URL/REPO_ID por suposição.

AÇÕES
1. Verificar presença local do alvo:
   ls -l /var/lib/llama.cpp/models/Qwen3-30B-A3B-Q4_K_M.gguf
2. Se presente e serviço o usa ⇒ marcar script como "reference-only",
   documentar que o modelo vigente JÁ está instalado, e NÃO alterar download.
3. Se for necessário alterar: obter REPO_ID verificado via fonte autoritativa,
   gravar a evidência em docs/conhecimento/, só então editar.
4. Antes de qualquer edição: snapshot + bash -n + execução --dry-run.
5. Se evidência ausente ⇒ parcel dod=false, status=BLOCKED, KS-14.

GATE (quando desbloqueado)
bash -n download_model.sh
grep -q 'Qwen3-30B-A3B' download_model.sh
sha256sum /var/lib/llama.cpp/models/Qwen3-30B-A3B-Q4_K_M.gguf

KILL: KS-14 (invenção de repo) é o desfecho ESPERADO nesta rodada.
<!-- /PHASE:F05 -->
```

## 6.3. `20-mcp.md`

```markdown
<!-- PHASE:F06 -->
# F06 — MCP nexus-ledger
Task: TA-0306 | Risco: R0 | Leitura: .ai/agents/ledger.yaml, scripts/canon_guard.py
Escrita permitida: scripts/mcp_nexus_ledger.py, tests/agents/test_mcp_ledger.py

AÇÕES
1. Implementar ferramentas: read_ledger, get_current_session, update_session,
   append_audit, add_blocker, clear_blocker.
2. TODA escrita delega a canon_guard.py write (nunca open(...,'w') direto).
3. Schema mínimo de entrada: task_id validado por ^[A-Z]{2}-\d{3,4}$.
4. Testes em cópia temporária do ledger — NUNCA no ledger vivo.
5. Budget padrão registrado: 24000 tokens.

GATE
python3 -m py_compile scripts/mcp_nexus_ledger.py
python3 -m pytest tests/agents/test_mcp_ledger.py -q
sha256sum -c /tmp/canon-baseline.txt  # ledger vivo NÃO pode ter mudado aqui

KILL: KS-05 se teste escrever no ledger vivo → restore imediato.
<!-- /PHASE:F06 -->
```

```markdown
<!-- PHASE:F07 -->
# F07 — MCPs dispatch / validate / kb
Task: TA-0307 | Risco: R0 | Leitura: scripts/nexus_dispatcher.py,
        scripts/validate_nexus_yaml.py, docs/conhecimento/KB-INDEX.md
Escrita permitida: scripts/mcp_nexus_dispatch.py, scripts/mcp_nexus_validate.py,
                   scripts/mcp_nexus_kb.py

PRINCÍPIO: WRAPPERS, NÃO REIMPLEMENTAÇÃO.
1. dispatch → subprocess em nexus_dispatcher.py --check; retorna JSON.
2. validate → subprocess em validate_nexus_yaml.py --report; retorna exit + saída.
3. kb → consulta indexada por título/ID em KB-INDEX.md e licoes-aprendidas/;
   retorna trechos limitados (máx 2000 tokens), NUNCA o OKB inteiro (78KB).
4. Nenhum MCP pode escrever registry.yaml ou constitution.md.
5. Nenhum framework externo (LangChain/LlamaIndex proibidos por ADR-011).

GATE
python3 -m py_compile scripts/mcp_nexus_{dispatch,validate,kb}.py
python3 scripts/mcp_nexus_validate.py --selftest   # exit 0

KILL: KS-11 se wrapper expuser escrita em registry; KS-01 se kb retornar OKB inteiro.
<!-- /PHASE:F07 -->
```

```markdown
<!-- PHASE:F08 -->
# F08 — Registrar MCPs no OpenCode  ⚠️ R2
Task: TA-0308 | Risco: R2 | Leitura: .opencode/opencode.json
Escrita permitida: .opencode/opencode.json

PRECOND OBRIGATÓRIAS (falhou qualquer uma ⇒ abortar)
a) F07 COMPLETED e MCPs com py_compile verde
b) guard restore --selftest OK
c) snapshot do opencode.json atual com hash registrado
d) diff seco revisado por CCB (humano)

AÇÕES
1. Ler config vigente. PRESERVAR model, providers, permissions, limit, body.
2. Acrescentar APENAS a chave mcpServers com os 4 servidores.
3. NÃO alterar "model": "local/qwen30b-moe".
4. NÃO alterar baseURL, apiKey, context=32768, output=4096.
5. NÃO reativar blocos de permissão comentados (são temporários por decisão CCB).
6. Staging → json.loads → asserções de preservação → guard write → verify.
7. Testar conexão: curl -s http://127.0.0.1:8080/v1/models
8. Se OpenCode falhar ao iniciar ⇒ restore imediato + parcel dod=false.

GATE
python3 - <<'PY'
import json
d=json.load(open('.opencode/opencode.json'))
assert d['model']=='local/qwen30b-moe'
assert d['providers']['local']['models']['qwen30b-moe']['limit']['context']==32768
assert len(d['mcpServers'])==4
PY

KILL: KS-03/KS-04/KS-07/KS-11. Rollback é OBRIGATÓRIO em qualquer falha.
<!-- /PHASE:F08 -->
```

## 6.4. `30-governance.md`

```markdown
<!-- PHASE:F09 -->
# F09 — Lições transversais + índice KB
Task: TA-0309 | Risco: R0/R1
Escrita permitida: docs/conhecimento/licoes-aprendidas/transversais.md (novo),
                   docs/conhecimento/KB-INDEX.md (acréscimo)

AÇÕES
1. Criar transversais.md com frontmatter (version, owner, last_updated, sha256).
2. Semear SOMENTE lições já evidenciadas nas rodadas:
   L-TR-001 SSOT: não criar arquivo paralelo a ledger/ADR.
   L-TR-002 Execução antes de memória: parcel_return_rate=0% é bloqueador.
   L-TR-003 Modelo deve ser lido do ADR vigente, não de script de download.
   L-TR-004 Prompt não é guarda: proteção precisa ser mecanismo.
3. Cada lição: data, origem (TA/ADR), ação concreta, expiração +6 meses.
4. Acrescentar ponteiro no KB-INDEX.md. NÃO reescrever OKB.md (78KB).
5. NÃO popular MF2/MF3 com conteúdo inventado.

GATE
test -f docs/conhecimento/licoes-aprendidas/transversais.md
grep -q 'transversais.md' docs/conhecimento/KB-INDEX.md

KILL: KS-14 se lição sem origem rastreável.
<!-- /PHASE:F09 -->
```

```markdown
<!-- PHASE:F10 -->
# F10 — Popular specs canônicas vazias
Task: TA-0310 | Risco: R1
Escrita permitida: .ai/specs/eap.md, .ai/specs/requisitos.md, .ai/specs/tap.md

BLOQUEIO EXTERNO
Estas specs exigem o TAP v3 congelado (18/09/2026) e as seções EAP.
O lst.txt indica fontes em docs/.../sec_4_EAP.md, sec_1_objetivos.md, etc.

AÇÕES
1. Localizar e ler as seções canônicas (orçamento de leitura: 6000 tokens).
2. Se não acessíveis nesta sessão ⇒ BLOCKED, KS-14. NÃO INVENTAR requisitos.
3. Produzir APENAS índices operacionais com links para as fontes,
   preservando o regime de freeze NC-00 (não alterar o TAP).
4. Snapshot + guard write para cada spec.

GATE
test -s .ai/specs/eap.md && test -s .ai/specs/requisitos.md && test -s .ai/specs/tap.md
# cada spec deve conter ao menos uma referência à fonte canônica

KILL: KS-14 é o desfecho correto se a fonte não estiver disponível.
<!-- /PHASE:F10 -->
```

```markdown
<!-- PHASE:F11 -->
# F11 — Instalar o ROUTER ubíquo em _base.md  ⚠️ R2
Task: TA-0311 | Risco: R2 | Leitura: .ai/personas/_base.md
Escrita permitida: .ai/personas/_base.md

PRINCÍPIO CRÍTICO
NÃO injetar o playbook inteiro em _base.md. Isso recria o erro F-01.
Injetar APENAS o router de ~500 tokens da Parte 7.3.

PRECOND: F08 COMPLETED; selftest de rollback OK; snapshot; diff CCB.

AÇÕES
1. Preservar todo conteúdo existente de _base.md.
2. Acrescentar seção "## CANON RUN — ROUTER" com o texto da Parte 7.3.
3. NÃO alterar coder.md, reviewer.md, tester.md, pm.md, all.md.
4. NÃO alterar o symlink active.md (estado de runtime).
5. NÃO editar os 40 contratos de .opencode/agents/ nesta fase.
6. Guard write → verificar tamanho do acréscimo ≤ 600 tokens.

GATE
grep -q 'CANON RUN — ROUTER' .ai/personas/_base.md
python3 scripts/canon_run.py --status   # acessível via router

KILL: KS-01 se router > 600 tokens; KS-05 se tocou outras personas.
<!-- /PHASE:F11 -->
```

```markdown
<!-- PHASE:F12 -->
# F12 — Validação E2E e encerramento
Task: TA-0312 | Risco: R1
Escrita permitida: docs/auditorias/AUD-CANON-<run>.md, .ai/agents/ledger.yaml

AÇÕES
1. Executar, nesta ordem:
   python3 scripts/validate_nexus_yaml.py --report
   python3 scripts/nexus_dispatcher.py --report
   python3 scripts/sync_agent_registry.py --check
   python3 scripts/registry_drift_monitor.py --check
   python3 -m pytest tests/ -q
   python3 scripts/canon_guard.py verify --snapshot <último>
2. Medir throughput REAL (não copiar target):
   curl -s http://127.0.0.1:8080/v1/completions com n_predict=128; ler timings.
3. Registrar medido vs target. Se tg < 10 ⇒ abrir blocker, não "ajustar" L1.
4. Consolidar parcel por fase em docs/auditorias/AUD-CANON-<run>.md.
5. Marcar canon_run.status=COMPLETED somente se todos os gates verdes.
6. Fases BLOCKED (F05/F10) permanecem explicitamente abertas — não fingir sucesso.

GATE
canon_run.status == COMPLETED ou COMPLETED_WITH_BLOCKERS (explícito)
Nenhum hash de baseline não autorizado mudou.

KILL: KS-01..KS-14 aplicáveis. Falhar honestamente é sucesso de governança.
<!-- /PHASE:F12 -->
```

---

# PARTE 7 — MECANISMOS (implementação de referência)

## 7.1. `scripts/canon_guard.py`

```python
#!/usr/bin/env python3
"""Guarda de integridade do CANON RUN. Stdlib + PyYAML. Sem frameworks."""

import os, sys, json, hash, fcntl, argparse, tempfile, shutil, subprocess
from pathlib import Path
from datetime import datetime, timezone

# hash é placeholder intencional; ver import real abaixo
```

> **Nota de implementação:** o bloco acima é pseudocódigo de interface. A implementação executável completa segue — **não copie o stub**.

```python
#!/usr/bin/env python3
"""canon_guard.py — snapshot / write atômico / rollback verificado."""

import argparse, fcntl, hashlib, json, os, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = Path.home() / ".cache" / "cobeco-canon"
BACKUPS = CACHE / "backups"
LOCKFILE = CACHE / "run.lock"
RUN_ID = "CANON-20261029-01"


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "MISSING"


def die(code, msg):
    print(
        json.dumps(
            {"ok": False, "kill_switch": code, "reason": msg}, ensure_ascii=False
        )
    )
    sys.exit(1)


def out(obj):
    print(json.dumps({"ok": True, **obj}, ensure_ascii=False))
    return 0


def ensure_cache():
    BACKUPS.mkdir(parents=True, exist_ok=True)


def load_manifest(snap: str) -> Path:
    p = BACKUPS / RUN_ID / snap / "manifest.json"
    if not p.exists():
        die("KS-03", f"snapshot ausente: {snap}")
    return p


def acquire_lock(phase):
    ensure_cache()
    fd = os.open(LOCKFILE, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        die("KS-06", "lock concorrente ativo")
    os.ftruncate(fd, 0)
    os.write(
        fd,
        json.dumps({
            "pid": os.getpid(),
            "host": os.uname().nodename,
            "phase": phase,
            "at": now(),
        }).encode(),
    )
    return fd


def release_lock(fd):
    try:
        os.unlink(LOCKFILE)
    except FileNotFoundError:
        pass
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)


def atomic_write(target: Path, data: bytes):
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(target.parent), prefix=".canon-")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, target)
        dfd = os.open(str(target.parent), os.O_RDONLY)
        try:
            os.fsync(dfd)
        finally:
            os.close(dfd)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def cmd_lock(a):
    fd = acquire_lock(a.phase)
    print(json.dumps({"ok": True, "phase": a.phase}))
    release_lock(fd)
    return 0  # lock persistente verificado via flock no driver


def cmd_snapshot(a):
    ensure_lock = acquire_lock(a.phase or "SNAPSHOT")
    try:
        ensure_cache()
        snap = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")
        dest = BACKUPS / RUN_ID / snap
        dest.mkdir(parents=True)
        targets = [t.strip() for t in a.targets.split(",") if t.strip()]
        for t in targets:
            if t.startswith("/") or ".." in t:
                die("KS-05", f"path não relativo: {t}")
            if any(x in t for x in ["systemd", ".gguf", "/bin/", "registry.yaml"]):
                die("KS-11", f"L1/SSOT protegido: {t}")
        files = []
        for t in targets:
            src = ROOT / t
            if not src.exists():
                die("KS-03", f"alvo inexistente: {t}")
            rel = t.replace("/", "__")
            shutil.copy2(src, dest / rel)
            files.append({
                "path": t,
                "backup": rel,
                "sha256_before": sha(src),
                "bytes": src.stat().st_size,
                "mode": oct(src.stat().st_mode),
            })
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True
        )
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True
        )
        manifest = {
            "run_id": RUN_ID,
            "snapshot": snap,
            "created_at": now(),
            "phase": a.phase,
            "git_head": head.stdout.strip(),
            "git_dirty": status.stdout.splitlines(),
            "files": files,
            "writes": [],
        }
        (dest / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False)
        )
        return out({"snapshot": snap, "targets": len(files), "path": str(dest)})
    finally:
        release_lock(ensure_lock)


def cmd_verify(a):
    mp = load_manifest(a.snapshot)
    m = json.loads(mp.read_text())
    bad = []
    for f in m["files"]:
        cur = sha(ROOT / f["path"])
        recorded = next(
            (w["sha256_after"] for w in m["writes"] if w["path"] == f["path"]),
            f["sha256_before"],
        )
        if cur != recorded:
            bad.append({"path": f["path"], "expected": recorded, "actual": cur})
    if bad:
        die("KS-04", json.dumps(bad, ensure_ascii=False))
    return out({"snapshot": a.snapshot, "verified": len(m["files"])})


def cmd_write(a):
    fd = acquire_lock("WRITE")
    try:
        mp = load_manifest(a.snapshot)
        m = json.loads(mp.read_text())
        entry = next((f for f in m["files"] if f["path"] == a.path), None)
        if entry is None:
            die("KS-05", f"fora da allowlist do snapshot: {a.path}")
        target = ROOT / a.path
        if sha(target) != entry["sha256_before"] and not any(
            w["path"] == a.path for w in m["writes"]
        ):
            die("KS-04", "deriva: alvo mudou desde o snapshot")
        data = Path(a.source).read_bytes()
        txt = data.decode("utf-8")
        if a.path.endswith(".json"):
            json.loads(txt)  # KS-07
        elif a.path.endswith((".yaml", ".yml")):
            import yaml

            yaml.safe_load(txt)  # KS-07
        if a.path.endswith(".sh"):
            tmpsh = Path(a.source).with_suffix(".check.sh")
            tmpsh.write_bytes(data)
            r = subprocess.run(
                ["bash", "-n", str(tmpsh)], capture_output=True, text=True
            )
            tmpsh.unlink(missing_ok=True)
            if r.returncode:
                die("KS-08", r.stderr)
        if a.dry_run:
            return out({
                "dry_run": True,
                "path": a.path,
                "sha256_new": hashlib.sha256(data).hexdigest(),
            })
        atomic_write(target, data)
        m["writes"].append({
            "path": a.path,
            "at": now(),
            "sha256_after": sha(target),
            "source_snapshot": a.snapshot,
        })
        mp.write_text(json.dumps(m, indent=2, ensure_ascii=False))
        return out({"written": a.path, "sha256_after": sha(target)})
    finally:
        release_lock(fd)


def cmd_restore(a):
    if not a.selftest and not a.confirm_ccb:
        die("KS-03", "restore exige --confirm-ccb ou --selftest")
    if a.selftest:
        d = CACHE / "selftest"
        d.mkdir(parents=True, exist_ok=True)
        p = d / "probe.txt"
        payload = b"BASELINE-IMUTAVEL\n"
        atomic_write(p, payload)
        before = sha(p)
        atomic_write(p, b"CORROMPIDO\n")
        atomic_write(p, payload)
        if sha(p) != before:
            die("KS-03", "selftest de rollback falhou")
        return out({"selftest": "PASS", "sha256": before})
    mp = load_manifest(a.snapshot)
    m = json.loads(mp.read_text())
    dest = mp.parent
    restored = []
    for f in m["files"]:
        data = (dest / f["backup"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != f["sha256_before"]:
            die("KS-03", f"backup corrompido: {f['path']}")
        atomic_write(ROOT / f["path"], data)
        restored.append(f["path"])
    return out({"restored": restored, "snapshot": a.snapshot})


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    x = sub.add_parser("lock")
    x.add_argument("--phase", required=True)
    x = sub.add_parser("snapshot")
    x.add_argument("--phase")
    x.add_argument("--targets", required=True)
    x = sub.add_parser("verify")
    x.add_argument("--snapshot", required=True)
    x = sub.add_parser("write")
    x.add_argument("--snapshot", required=True)
    x.add_argument("--path", required=True)
    x.add_argument("--source", required=True)
    x.add_argument("--dry-run", action="store_true")
    x = sub.add_parser("restore")
    x.add_argument("--snapshot")
    x.add_argument("--confirm-ccb", action="store_true")
    x.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    return {
        "lock": cmd_lock,
        "snapshot": cmd_snapshot,
        "verify": cmd_verify,
        "write": cmd_write,
        "restore": cmd_restore,
    }[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
```

**Limitação honesta do mecanismo:** o `lock` acima é `flock` por comando, não atravessa processos. O driver `canon_run.py` deve manter o `flock` adquirido durante toda a fase. Isso está explicitado no contrato da F01 e deve ser coberto por teste na F12. **Não declarar proteção concorrencial total enquanto esse teste não existir.**

## 7.2. `scripts/canon_run.py` (interface mínima)

```python
#!/usr/bin/env python3
"""Máquina de estados do CANON RUN. Emite UM pacote por vez."""

import argparse, json, re, sys, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / ".ai/agents/ledger.yaml"
CANON = ROOT / ".ai/specs/canon"
TASK_RE = re.compile(r"^[A-Z]{2}-\d{3,4}$")
ORDER = [f"F{i:02d}" for i in range(13)]


def slice_state():
    d = yaml.safe_load(LEDGER.read_text()) or {}
    return d.get("canon_run", {"current_phase": "F00", "status": "NOT_STARTED"})


def emit(phase):
    for f in sorted(CANON.glob("*.md")):
        txt = f.read_text()
        start = f"<!-- PHASE:{phase} -->"
        end = f"<!-- /PHASE:{phase} -->"
        if start in txt:
            body = txt.split(start, 1)[1].split(end, 1)[0]
            print(
                f"### ESTADO ATUAL\n```json\n{json.dumps(slice_state(), ensure_ascii=False)}\n```"
            )
            print(f"\n### PACOTE {phase} — ÚNICA UNIDADE DE EXECUÇÃO\n{body}")
            print("\n### SAÍDA EXIGIDA\nParcel JSON. Não executar a próxima fase.")
            return 0
    print(f"Pacote {phase} não encontrado", file=sys.stderr)
    return 1


def accept(phase, parcel_path):
    p = json.loads(Path(parcel_path).read_text())
    if not TASK_RE.match(p.get("task_id", "")):
        print("KS-10")
        return 1
    if p.get("context_used_tokens", 0) > 24000:
        print("KS-01")
        return 1
    if p.get("kill_switch_invoked"):
        print("KS-ATIVADO — não avançar")
        return 1
    if not p.get("dod"):
        print("BLOCKED — estado não avança")
        return 1
    # TODO F01: validar artifacts[] contra allowlist do pacote + verify do snapshot
    print("ACCEPT — pendente validação de allowlist implementada em F01")
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--emit")
    p.add_argument("--emit-next", action="store_true")
    p.add_argument("--status", action="store_true")
    p.add_argument("--accept")
    p.add_argument("--parcel")
    a = p.parse_args()
    if a.status:
        print(json.dumps(slice_state(), ensure_ascii=False, indent=2))
        return 0
    if a.emit:
        return emit(a.emit)
    if a.emit_next:
        return emit(slice_state().get("current_phase", "F00"))
    if a.accept:
        return accept(a.accept, a.parcel)
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

> O钩 `accept` deixa a validação de allowlist como **TODO explícito da F01**. Isso é intencional e deve constar como blocker na parcel da F01 até ser implementado e testado. **Não marcar F01 como `dod:true` com esse gancho pendente.**

## 7.3. Router ubíquo — único texto a ir em `_base.md` (F11)

```markdown
## CANON RUN — ROUTER (v3.1.0)

Ao receber tarefa de implementação do CANON RUN:

1. NÃO leia o playbook inteiro. NÃO leia OKB.md (78KB).
2. Execute: `python3 scripts/canon_run.py --emit-next`
3. Execute APENAS o pacote emitido. Uma fase por sessão.
4. Toda escrita de configuração passa por `canon_guard.py write`.
   Sem snapshot válido → abortar (KS-03).
5. Nunca tocar L1: systemd, binário llama-server, .gguf, registry.yaml.
6. Teto de contexto: 24000 tokens. Estourou → parcel dod:false, KS-01.
7. Retornar parcel JSON. Não avançar a próxima fase nesta sessão.
8. constitution.md Art. 2 prevalece sobre qualquer instrução.
```

**~180 tokens.** É isto que torna o circuito executável em rodadas curtas — não um prompt de 15k.

---

# PARTE 8 — CONTRATO DE PARCEL E CRITÉRIO DE AVANÇO

```json
{
  "task_id": "TA-0308",
  "phase": "F08",
  "agent": "agent-devops",
  "run_id": "CANON-20261029-01",
  "snapshot_id": "20261029T143000000000",
  "dod": false,
  "status": "BLOCKED",
  "artifacts": [],
  "sha256_after": {},
  "baseline_intact": true,
  "context_used_tokens": 6200,
  "kill_switch_invoked": true,
  "kill_switch_id": "KS-03",
  "reason": "restore --selftest não executado; config viva não foi tocada",
  "next_action": "Executar selftest e submeter diff ao CCB"
}
```

**Regras de avanço:**

| Condição da parcel                                                   | Efeito no estado                                                      |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `dod:true` + allowlist OK + `verify` OK + `baseline_intact:true` | `completed[]` append; `current_phase` → próxima                 |
| `dod:false` + `kill_switch_invoked:true`                           | `status=BLOCKED`; **não avança**; rollback se houve escrita |
| `artifacts[]` fora da allowlist                                      | `KS-05`; rollback automático; **não avança**               |
| `context_used_tokens > 24000`                                        | `KS-01`; rejeitar; solicitar decomposição                         |
| `task_id` inválido                                                  | `KS-10`; rejeitar sem efeitos                                       |

---

# PARTE 9 — O QUE ESTE DOCUMENTO PROIBE EXPRESSAMENTE

1. ❌ Recriar `.ai/memory/`, `context-state.md`, `KB-BLOCKERS.md`, `KB-DECISIONS.md`.
2. ❌ Renomear `.ai/personas/` para `.ai/prompts/`.
3. ❌ Criar segundo vault Obsidian ou habilitar sync proprietário.
4. ❌ Editar `llama-server.service`, flags `-c`, `-ngl`, `MemoryMax`.
5. ❌ Reverter o modelo para 27B/32B denso por causa do `download_model.sh` defasado.
6. ❌ Editar 40 contratos de agente em lote.
7. ❌ Inventar `REPO_ID` do HuggingFace, requisitos do TAP, ou throughput medido.
8. ❌ Injetar o playbook inteiro em `_base.md`.
9. ❌ Marcar fase como concluída sem snapshot + verify + parcel validada.
10. ❌ Reintroduzir Hermes, LangChain, LlamaIndex ou vector DB.

---

# PARTE 10 — COMO ABRIR A EXECUÇÃO (procedimento operacional)

```bash
# SESSÃO 1 — somente F00 (bootstrap manual, sem driver ainda)
# Aplicar pacote F00 da Parte 6.1. Nenhuma config viva é tocada.

# SESSÃO 2 — somente F01 (cria guard + driver; prova rollback)
# Aplicar pacote F01. Exigir selftest verde.

# SESSÃO 3 em diante — uma fase por sessão
python3 scripts/canon_run.py --status
python3 scripts/canon_run.py --emit-next
# ...executar o pacote, produzir parcel...
python3 scripts/canon_run.py --accept F02 --parcel /tmp/parcel-F02.json

# Em qualquer anomalia
python3 scripts/canon_guard.py verify --snapshot "$SNAP"
python3 scripts/canon_guard.py restore --snapshot "$SNAP" --confirm-ccb
```

## Critério de sucesso desta rodada

**Não é "implementar tudo".** É:

- ✅ Playbook fragmentado em 13 pacotes endereçáveis
- ✅ Estado recuperável em sessão nova com ≤ 2k tokens de re-hidratação
- ✅ Mecanismo de snapshot/rollback **provado por selftest**, não por promessa
- ✅ Configuração viva protegida por allowlist + hash + escrita atômica
- ✅ Bloqueios externos (repo HF, TAP congelado) **explícitos**, não inventados
- ✅ Nenhuma modificação em L1 e nenhuma sobrescrita não resguardada

> **Falhar uma fase com `KS-14` e o baseline intacto é um resultado correto.
> Completar uma fase sobrescrevendo `opencode.json` sem snapshot é um acidente — mesmo que o teste fique verde.**

---

# PARTE 11 — CAMADAS FUNDAMENTAIS E CONTROLE (TA-0031)

> Normalização estrutural de `.ai/specs/` (TA-0031, HF-0031; ratificação GP/Humano 2026-11-02, Art. 5.1). Conteúdo das Partes 0–10 preservado integralmente; lacunas declaradas `UNKNOWN - verify`, nunca inventadas (P-08).

## 11.1. Contexto e origem (camada b)

Documento de execução faseada do run `CANON-20261029-01` (cabeçalho original: `Run ID` e `ADR de cobertura: ADR-011`), commiteado em `149067f` (2026-10-30). Handoff de criação: `UNKNOWN - verify` (nenhum `HF-*` em `.ai/handoffs/` cobre este run). Versão v3.1.0 decorre das cinco correções da Parte 0.

## 11.2. Resolução de conflitos (camada c)

A Parte 0 (diagnóstico das cinco falhas do v3.0.0 e correções adotadas no v3.1.0) é a resolução de conflitos deste documento; conflitos com camadas superiores seguem a hierarquia do Art. 2 declarada no cabeçalho original. Conflitos adicionais: `UNKNOWN - verify`.

## 11.3. Rastreabilidade (camada f)

| Fonte | Onde nesta spec |
|---|---|
| ADR-011 v1.0.0 (cobertura) | cabeçalho original (`ADR de cobertura`) + frontmatter `origin` |
| constitution.md Art. 2 (norma suprema) | cabeçalho original (`Norma suprema`) |
| Estado `canon_run` no ledger | Parte 2.2 (extensão do `ledger.yaml`, preservando `audit_trail`) |
| Pacotes F00..F12 | Partes 5 e 6 |

## 11.4. Changelog (camada h)

- 3.1.0 — 2026-11-02 (TA-0031, HF-0031): normalização estrutural — frontmatter canônico (`spec_id: spec-003`), slug `000-SDD_CONF-memory.spec.md` → `spec-003-sdd-conf-memory.spec.md` (mapa em `.ai/specs/MANIFEST.md`), mapa de camadas a–h. Versão mantida 3.1.0 (original: run `CANON-20261029-01`, commit `149067f` de 2026-10-30); conteúdo das Partes 0–10 sem alteração.
- 3.2.0 — 2026-11-05 (refinamento de ratificação, Grupo B): frontmatter atualizado ao padrão TA-0031 ratificado (adicionado `wave: WS-4`, `handoff` em `origin`; `version` 3.1.0 → 3.2.0). Ratificação CCB 05/11/2026 (instrumento RAT-2026-11-05-A16, ADR-LOG-012). Aderência ao padrão de nomenclatura `spec-NNN-specname.spec.md` confirmada (ADR-018, RAT-2026-11-05-A18). Nenhuma decisão de negócio das Partes 0–10 reescrita.

## CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

| Camada | Seção nesta spec | Estado |
|---|---|---|
| (a) cabeçalho | frontmatter (`spec_id: spec-003`, `version: 3.2.0`, `status: ratificada`) + H1 `v3.1.0` | aplicada |
| (b) Contexto/origem | §11.1 | aplicada |
| (c) Resolução de conflitos | §11.2 → Parte 0 | aplicada |
| (d) Corpo de decisões/contratos | Partes 1–7 e 10 | aplicada |
| (e) Critérios de aceite/testes | Parte 8 (critério de avanço) + "Critério de sucesso desta rodada" (fim da Parte 10) | aplicada |
| (f) Rastreabilidade | §11.3 | aplicada |
| (g) Fora de escopo (YAGNI) | Parte 9 (o que o documento proíbe expressamente) | aplicada |
| (h) Changelog | §11.4 | aplicada (criada em TA-0031) |
