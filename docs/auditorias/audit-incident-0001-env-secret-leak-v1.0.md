---
id: audit-incident-0001-env-secret-leak-v1.0
type: audit-incident
title: AUDIT INCIDENT — Leak de secret (.env commitado)
version: v1.0
status: rascunho
canonical: false
canonical_slug: incident-env-secret-leak
created: '2026-11-15'
updated: '2026-11-15T04:39:33Z'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: gh-sig:owner:leonardosetti:7e3764ef0785f581ca5114f31ec2719bb76b07424c5f708d22afd1fa4973e12f
ratified_at: '2026-11-15T04:39:33Z'
supersedes: null
superseded_by: null
trace:
  constitution: [Art. 6.3, Art. 7.7, Art. 17.7, Art. 9.9, Art. 17.5]
  req_func: []
  req_nfunc: []
  use_cases: []
  specs: []
  handoffs: []
  adrs: []
  code: [commit 770e504, PR #67, d9cc5db, e639a0a]
  tests: []
domain: operation
layer: incident
tags: [segredo, leak, env, secrets, seguranca, SEV-2]
lgpd_class: n/a (sem dados de terceiros; apenas credenciais de dev do repositorio)
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: 7e3764ef0785f581ca5114f31ec2719bb76b07424c5f708d22afd1fa4973e12f
  board_url: null
---

# INCIDENTE — Leak de secret: .env commitado no repositorio (COBECO MVP)

## 1. Classificacao de severidade (Runbook Incident §2)

| Item | Valor |
|------|-------|
| Severidade | **SEV-2 (Alto)** |
| Definicao | Exposicao de segredo (credenciais de ambiente) sem indisponibilidade de sistema e sem evidencia de uso indevido / exfiltracao |
| SLA Resposta | 30 min |
| SLA Resolucao | 4 horas |
| Escala | L1 → L2 em 1h |

Justificativa: o `.env` foi commitado e enviado ao remote `origin` (branch `stage`). Nao ha indicacao de acesso externo ao repositorio nem de uso das credenciais expostas. Classificado como SEV-2 (nao SEV-1) por nao configurar indisponibilidade de sistema nem perda de dados confirmada.

## 2. Resumo do incidente

- O que aconteceu: o arquivo `.env` (1220 bytes, contendo credenciais de ambiente de desenvolvimento) foi commitado e rastreado pelo git.
- Quando: commit `e639a0a` (migracao P1/P2/P3), presente na mescla `d9cc5db` (14/11/2026), ramo `stage`.
- Onde: repositorio `github.com/leonardosetti/COBECO.git`, branch `stage` (remoto `origin`).
- Quem detectou: GitHub Guardian (secret scanning) apontou leak de secret.
- Impacto: segredos de ambiente expostos no historico publico do remoto. Arquivos de configuracao sensivel nao deveriam estar versionados.
- Detecção: alerta externo (GitHub Guardian / secret scanner), nao por monitoramento interno.

## 3. Cronograma

| Horario/Data | Evento | Acao tomada |
|--------------|--------|-------------|
| 14/11/2026 | Commit `e639a0a` / mescla `d9cc5db` inclui `.env` rastreado | — (incidente nao detectado na epoca) |
| 15/11/2026 | GitHub Guardian aponta leak de secret | Triagem e analise do commit |
| 15/11/2026 | `.env` adicionado ao `.gitignore` | `git rm --cached .env` (arquivo local mantido) |
| 15/11/2026 | Commit `770e504` fix(security) | Remove `.env` do index e ignora o arquivo |
| 15/11/2026 | PR #67 `fix/env-leak` → `stage` | Criado e mergado (commit `d5cffa5`) |
| 15/11/2026 | `.env` sai do rastreamento no `stage` | Fix aplicado ao branch protegido via PR |
| 15/11/2026 | Registro de incidente (este documento) | Post-incidente / RCA em aberto |
| 15/11/2026 | Rotacao de `GITHUB_TOKEN` e `CR_PAT` (usuario, prioridade 0) | Concluido pelo usuario |
| 15/11/2026 | Rotacao de segredos locais COBECO (`MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD`, `SECRET_KEY`, `DATABASE_URL`) | Concluido (este agente) |

## 4. Causa raiz (RCA) — analise sem busca de culpados

- Causa direta: durante a migracao P1/P2/P3 (133 arquivos renomeados, frontmatter universal, 874 refs atualizadas) o arquivo `.env` foi incluido acidentalmente no escopo de arquivos renomeados/movidos e commitado sem passar pelo filtro de secrets.
- Causa contribuinte: `.env` nao constava no `.gitignore` na epoca (so constavam exemplos `config-env-0001-env-example-*` e `secrets/`).
- Causa contribuinte: o hook `pre-commit` "Secret Scanner" referencia `scripts/secret_scan.py`, que **nao existe** no repositorio (arquivo real: `scripts/script-security-0001-secret-scan-v1.0.py`), entao o hook falha silenciosamente e nao bloqueia o commit.
- Causa contribuinte: o hook `pre-push` "CI Green Check" referencia `scripts/ci_green_check.py`, tambem inexistente, permitindo push sem validacao CI.

## 5. Contribuicao de fatores

| Fator | Efeito |
|-------|--------|
| Gancho secret scanner quebrado (script ausente) | Nao detectou o `.env` no commit `e639a0a` |
| `.env` ausente do `.gitignore` | Permitiu rastreamento pelo git |
| Migracao em massa (133 arquivos) | Mascarou a inclusao do arquivo sensivel |
| Push direto bloqueado (branch protegido) | Forçou PR — mitigacao que permitiu revisao antes do merge |

## 6. Acoes corretivas e preventivas

| Acao | Responsavel | Prazo | Status |
|------|-------------|-------|--------|
| Rotacionar todas as credenciais constantes do `.env` (expostas no remote) | Tech Lead / Dev / Usuario | Imediato | CONCLUIDO |
| Consertar hook `pre-commit` (apontar para `scripts/script-security-0001-secret-scan-v1.0.py`) | DevOps | 1 dia útil | CONCLUIDO |
| Consertar hook `pre-push` (apontar para `scripts/script-ci-0001-ci-green-check-v1.0.py`) | DevOps | 1 dia útil | CONCLUIDO |
| Manter `.env` e `.*` no `.gitignore` (feito no PR #67) | — | Concluido | CONCLUIDO |
| Verificar que nenhum outro arquivo sensível (.pem, .key, secrets/) esta rastreado | QA | 1 dia útil | CONCLUIDO |
| Avaliacao para remocao do historico publico (git filter-repo / BFG + force push) | CCB + time extraordinario | APOS aprovacao CCB | BLOQUEADO (ver §7) |

## 7. Remocao do historico publico — ordem expressa (CCB)

Conforme ordem expressa, apagar o `.env` do historico do GitHub exigiria:
- `git filter-repo` ou BFG + force push no remoto `origin`;
- Aprovacao formal do **CCB** (Change Control Board);
- Execucao por **time em ata extraordinaria**, com acta produzida e **assinada por hash** (`approval_hash` / `ratified_by` preenchidos apos aprovacao).

Este merge do PR #67 apenas remove o `.env` do rastreamento futuro (arquivo local mantido). Como o `.env` ja esta no remote `stage`, os segredos estao considerados **comprometidos**: devem ser rotacionados. A remocao do historico publico **nao foi executada** neste incidente por falta de aprovacao CCB + ata extraordinaria — fica como acao preventiva aberta (§6).

## 8. Lições aprendidas

- Todo arquivo de ambiente/secreto deve constar do `.gitignore` ANTES de qualquer migracao em massa.
- Ganchos de seguranca (secret scanner) devem apontar para scripts existentes; hooks quebrados criam falso sentimento de seguranca.
- Branch protegido + PR forçou revisao e impediu push direto — mecanismo de governança funcionou para o fix.

## 9. Rastreabilidade

- **Runbook relacionado:** `docs/operacao/runbook-incident-0001-incident-v1.0.md` (fluxo: detecção → triage → contenção → resolução → validação → comunicação → pós-incidente)
- **Fix aplicado:** PR #67 (`fix/env-leak` → `stage`), commit `770e504`, mesclado em `d5cffa5`
- **Commit origem do leak:** `e639a0a` / mescla `d9cc5db`
- **Issue vinculada:** <nao existe ainda — criar no GitHub para rastreamento>
- **Constitution:** Art. 6.3 (branch protegido), Art. 7.7 / 17.7 (secret scanner), Art. 9.9 / 17.5 (CI green check)

---
**Fim do incidente — todos os segredos do .env rotacionados. Aguardando aprovacao CCB para remocao do historico publico (ordem expressa).**
