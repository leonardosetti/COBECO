---
id: runbook-deploy-0001-ciclo-codificacao-deploy-v1.0
type: runbook-deploy
title: RUNBOOK — Ciclo de Codificação e Deploy
version: v1.0
status: aprovado
canonical: false
canonical_slug: ciclo-codificacao-deploy
created: '2026-11-15'
updated: '2026-11-15'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: null
ratified_at: null
supersedes: null
superseded_by: null
trace:
  constitution: [constitution-0001-constitution-canon.md]
  req_func: [req-func-0001-requisitos-funcionais-canon.md]
  req_nfunc: []
  use_cases: [req-use-case-0001-casos-de-uso-canon.md]
  specs: [.ai/specs/spec-tech-0001-backend-mvp-v1.0.md, .ai/specs/spec-quality-0001-qualidade-pdca-ishikawa-v1.0.md]
  handoffs: [.ai/handoffs/hf-exec-0500-backend-mvp-v1.0.md]
  adrs: [docs/decisoes/doc-adr-0001-stack-decision-v1.0.md]
  code: [scripts/script-ci-0001-ci-green-check-v1.0.py, scripts/script-hooks-0001-install-hooks-v1.0.py]
  tests: [backend/tests/unit, backend/tests/integration]
domain: governance
layer: runbook
tags: [runbook, codificacao, deploy, pdca, stage, merge, ci-cd]
lgpd_class: n/a
workflow:
  stage: aprovado
  reviewer: CCB
  reviewed_at: '2026-11-15'
  approval_hash: null
  board_url: null
---
# Runbook — Ciclo de Codificação e Deploy (COBECO MVP)

**Objetivo:** padronizar o ciclo de ponta a ponta — da spec aprovada ao deploy em stage com aprovação para merge — aplicando gates de qualidade, PDCA contínuo, YAGNI+KISS, padrões de dev do projeto, testes unitários/integração (ou mock/stub), verificação de CI/CD verde a cada deploy e documentação obrigatória (logs e relatórios de testes, implantação e deploy).

**Norma vinculante:** Constituição (Art. 2, 6.3, 7.7, 9.3, 9.9, 17.3, 17.5, 17.7). Protocolo P1/P2/P3 (nomenclatura, frontmatter, rastreabilidade, workflow).

---

## 1. Princípios obrigatórios (não negociáveis)

| Princípio | Regra |
|-----------|-------|
| Specs aprovadas | Codificação só inicia com spec `workflow.stage` = `aprovado`/`ratificado`/`promulgado` (frontmatter P2). |
| YAGNI+KISS | Implementar só o que a spec exige. Nada de "para o futuro", nenhuma abstração antecipada, nenhum opcional. |
| Dev patterns do projeto | Seguir camadas Dados/Back/Front separadas, proxy sempre ativo, stack ratificada (ADR-016), Decimal para dinheiro, ROUND_HALF_EVEN, FastAPI+Pydantic v2+SQLAlchemy async. |
| PDCA contínuo | Planejar → Fazer → Checar → Agir em cada ciclo de revisão. Revisão contínua **antes** de implementar cada bloco. |
| Sem loop infinito | Máximo de 3 ciclos PDCA por bloco. Se persistir, escalar para CCB/PO e decidir (revisão, simplificação ou cancelamento do bloco). |
| Testes obrigatórios | Rodada de testes unitários locais; testes de integração quando existirem; senão, mock/stub. |
| Deploy em stage | Commit + push de código, documentação e testes; pipeline CI/CD all green; verificar status dos workflows a cada deploy. |
| Falha no pipeline | Decidir: reversão de código **ou** correção do issue de pipeline/workflow. Nunca ignorar. |
| Documentação | Emitir logs e relatórios de testes, implantação e deploy a cada ciclo. |
| Gate de stage | Após revisão do gate de implantação em stage, **aguardar aprovação para merge** (não fazer merge direto). |

---

## 2. Papéis e responsabilidades

- **Dev/agente implementador:** executa o ciclo, aplica PDCA, escreve código e testes, gera logs/relatórios, abre PR para stage.
- **Reviewer/CCB:** revisa specs aprovadas, aprova gate de implantação em stage, aprova merge.
- **DevOps/CI:** mantém workflows CI/CD verdes, apoia decisão de reversão vs correção de pipeline.

---

## 3. Fase A — Início da codificação (gate de entrada)

**A1. Confirmar specs aprovadas.**
- Listar specs em `.ai/specs/*.md` com frontmatter `workflow.stage` ∈ {aprovado, ratificado, promulgado}.
- Rejeitar specs em `rascunho`/`revisao`/`rejeitado` (não codificar).
- Saída: `REL-ESPEC-APROVADAS-<data>.json` (lista de spec_id, título, branch, dependências).

**A2. Verificar e resolver dependências antes de codificar.**
- Para cada spec, ler `trace.specs` e `workflow.depends_on` (se houver) para montar grafo de dependências.
- Spec dependente só inicia após a spec upstream estar `implementada` e seus testes passando.
- Dependências externas (Pacotes `requirements.txt`, Docker, MySQL): instalar/resolver localmente antes de iniciar.
- Registrar dependências resolvidas no relatório de início.

**A3. Calcular paralelismo (múltiplas specs).**
- Specs sem dependência entre si → codificam em paralelo (ondas/workstreams independentes).
- Specs dependentes → sequência forçada (gate de redes de projeto PMBOK: finish-to-start).
- Saída: plano de ondas `PLAN-ONDAS-<data>.md` com quais specs rodam em paralelo e quais em sequência.

**A4. Aplicar gate PMBOK de redes de projeto.**
- Validar crítica do caminho (specs no caminho crítico não atrasam).
- Se houver conflito de recurso, escalar para CCB antes de iniciar.

**Saída da Fase A:** `REL-INICIO-CODIFICACAO-<data>.md` (specs liberadas, dependências, plano de ondas, gate PMBOK aprovado).

---

## 4. Fase B — Codificação com revisão contínua PDCA

Ciclo repetido por bloco de implementação (máximo 3 iterações por bloco):

| Etapa PDCA | Ação | Critério de saída |
|------------|------|-------------------|
| **Planejar** | Definir o bloco (o que a spec exige, nada a mais), padrões de dev, entradas/saídas, testes a passar. | Escopo do bloco definido e revisado. |
| **Fazer** | Implementar o bloco localmente seguindo YAGNI+KISS e padrões do projeto. | Código implementado, commit local (não push ainda). |
| **Checar** | Revisão contínua: autovalidação, lint (ruff), mypy, validação de frontmatter/P1/P2/P3 do artefato tocado, testes unitários do bloco. | Lint/type check verde, testes unitários do bloco verdes, artefato válido. |
| **Agir** | Se falhar: corrigir e repetir PDCA (contar iteração). Se atingir 3 iterações sem sucesso: escalar CCB, simplificar (KISS) ou cancelar bloco. | Bloco aprovado ou escalonado. |

**Revisão contínua antes de implementar:** toda alteração passa por revisão (pair review ou self-review com checklist) antes de ser commitada.

**Critério de parada (anti-loop):** se o mesmo bloco falhar na mesma verificação em 3 ciclos PDCA, parar. Não entrar em loop sem fim de revisão. Decisão: simplificar escopo (YAGNI), reabrir spec com CCB, ou mover para dívida técnica registrada.

---

## 5. Fase C — Testes (local)

**C1. Testes unitários (obrigatório, sempre).**
- Executar `pytest backend/tests/unit` (ou equivalente da camada tocada).
- Cobertura mínima do bloco: manter cobertura geral ≥ 80% (conforme CI).
- Gerar `relatorio-testes-unitarios-<data>.md` (total, passou, falhou, cobertura).

**C2. Testes de integração (quando existirem).**
- Executar `pytest backend/tests/integration` se houver testes de integração para o bloco.
- Se não houver teste de integração aplicável: usar **mock/stub** para simular dependências externas (banco, APIs externas, proxy) e validar o fluxo localmente. Registrar uso de mock/stub no relatório.

**C3. Falha de teste.**
- Bloquear o ciclo. Corrigir código ou teste. Não prosseguir para deploy com teste falhando.

**Saída da Fase C:** `REL-TESTES-LOCAL-<data>.md` (unitários + integração ou mock/stub, evidências).

---

## 6. Fase D — Implementação local e validação de artefatos

- Commit local com **Conventional Commits** (`tipo(escopo): resumo imperativo`, ex: `feat(backend): calcular orcamento`).
- Validar artefatos tocados com `python scripts/script-validate-0002-artifact-validate-v1.0.py --file <caminho>` (P1/P2/P3).
- Validar referências cruzadas com `python scripts/script-validate-0001-validate-refs-v1.0.py`.
- Secret scan com `python scripts/script-security-0001-secret-scan-v1.0.py` (Art. 7.7).
- Se houver documentação associada ao bloco, emitir/atualizar em `docs/` com frontmatter P2.

**Saída da Fase D:** código commitado localmente, artefatos válidos, `REL-ARTEFATOS-<data>.md`.

---

## 7. Fase E — Deploy em stage

**E1. Pré-deploy (gate de CI/CD).**
- Abrir PR para branch `stage` (não push direto em `main`/`stage`/`master` — Art. 6.3).
- Executar `python scripts/script-ci-0001-ci-green-check-v1.0.py` (CI Green Check). CI deve estar verde (workflows `CI` concluídos com conclusão `success`).
- Verificar **a cada deploy** o status dos pipelines/workflows de CI/CD (GitHub Actions). Funcionamento pleno sem falhas.

**E2. Commit e push.**
- Commit: código + documentação + testes + logs/relatórios desta fase.
- Push para branch de feature (pre-push hook executa CI Green Check; não bypassar exceto emergência real com `--no-verify`).

**E3. Implantação em stage.**
- Fazer deploy em stage (merge do PR para `stage` ou workflow de deploy dedicado).
- Verificar funcionamento pleno em stage (smoke test: endpoints, proxy em 127.0.0.1:8080, frontend/backend Docker compose `EXIT 0`).
- Gerar `REL-IMPLANTACAO-STAGE-<data>.md` e `REL-DEPLOY-<data>.md` (status CI, URLs, smoke test, timestamp, agente responsável).

**E4. Decisão em caso de falha no pipeline/workflow.**
Se qualquer pipeline de deploy CI/CD falhar:
1. Parar o ciclo. Não forçar merge.
2. Decidir (dev + devops + CCB):
   - **Reversão de código:** reverter o commit que quebrou o pipeline (`git revert`) e re-deploy em stage.
   - **Correção do issue de pipeline/workflow:** corrigir workflow/action/dependência de CI e re-executar.
3. Documentar a decisão e o desfecho em `REL-FALHA-PIPELINE-<data>.md`.
4. Só prosseguir após pipeline verde novamente.

**Saída da Fase E:** relatórios de implantação e deploy, stage funcionando, pipeline all green.

---

## 8. Fase F — Gate de implantação em stage e aprovação para merge

**F1. Revisão do gate de implantação em stage.**
- Revisor (CCB/PO) revisa: relatórios de testes, implantação, deploy, logs, CI verde, smoke test em stage, conformidade P1/P2/P3, YAGNI+KISS.
- Gate aprovado ou rejeitado com justificativa.

**F2. Aguardar aprovação para merge.**
- **Não fazer merge para `main` antes da aprovação explícita do gate de stage.**
- Após aprovação: merge autorizado via PR (Conventional Commits), manter rastreabilidade (trace.code, trace.tests no frontmatter dos artefatos).

**Saída da Fase F:** `REL-APROVACAO-MERGE-<data>.md` (aprovador, data, hash do merge, gate de stage revisado).

---

## 9. Documentação obrigatória (emitir a cada ciclo)

| Relatório | Conteúdo mínimo | Onde |
|-----------|-----------------|------|
| REL-INICIO-CODIFICACAO | specs aprovadas, dependências, plano de ondas/paralelismo, gate PMBOK | `docs/reports/` |
| REL-TESTES-LOCAL | unitários (passou/falhou/cobertura), integração ou mock/stub usados | `docs/reports/` |
| REL-ARTEFATOS | validação P1/P2/P3, secret scan, referências cruzadas | `docs/reports/` |
| REL-IMPLANTACAO-STAGE | status CI, smoke test stage, timestamp, responsável | `docs/reports/` |
| REL-DEPLOY | pipelines CI/CD verificados a cada deploy, all green | `docs/reports/` |
| REL-FALHA-PIPELINE | decisão reversão vs correção de pipeline, desfecho | `docs/reports/` |
| REL-APROVACAO-MERGE | aprovador do gate de stage, data, hash do merge | `docs/reports/` |
| Logs | saída de execução dos scripts/hook, erros, avisos | `docs/logs/` |

Nomes seguem P1: `rel-...-v1.0.md` com frontmatter P2 (tipo-classe `doc-test-log`, `doc-release-notes`, `doc-status-report` conforme cabível).

---

## 10. Checklist resumido (ciclo completo)

- [ ] Spec aprovada (workflow.stage ∈ {aprovado, ratificado, promulgado})
- [ ] Dependências verificadas e resolvidas
- [ ] Paralelismo calculado (ondas independentes vs sequência PMBOK)
- [ ] PDCA aplicado (máx 3 ciclos/bloco, sem loop infinito)
- [ ] YAGNI+KISS + dev patterns do projeto aplicados
- [ ] Testes unitários locais executados (relatório emitido)
- [ ] Testes de integração ou mock/stub (relatório emitido)
- [ ] Código implementado localmente, commit Conventional Commits
- [ ] Artefatos validados (P1/P2/P3, secret scan, refs)
- [ ] Deploy em stage: commit + push de código, docs e testes
- [ ] CI/CD all green verificado a cada deploy
- [ ] Falha de pipeline: decisão reversão vs correção documentada
- [ ] Gate de implantação em stage revisado
- [ ] **Aprovação para merge aguardada (não mergear antes)**
- [ ] Logs e relatórios de testes, implantação e deploy emitidos

---

## 11. Hook associado

O ciclo é automatizado pelo hook:

`scripts/script-hooks-0002-ciclo-codificacao-deploy-v1.0.py`

Subcomandos:
- `gate-inicio` — valida specs aprovadas, dependências, paralelismo e gate PMBOK (Fase A).
- `gate-ciclo` — executa PDCA, testes unitários/integração/mock, valida artefatos (Fases B–D).
- `deploy-stage` — CI green check, commit/push, deploy em stage, relatórios, decisão de falha (Fase E).
- `gate-stage` — emite relatório de aprovação de merge aguardando aprovador (Fase F).

Instalar: `python scripts/script-hooks-0001-install-hooks-v1.0.py` (pre-commit, pre-push, commit-msg) e usar o hook 0002 nos gates de ciclo.

---
*Fim do runbook. Versão v1.0 — sujeita a revisão do CCB.*
