---
id: ai-specs-spec-<NNN>-<slug>-v<ver>-spec
title: SPEC spec-<NNN> — <slug> — <Nome da Especificação>
type: spec
version: <ver>
status: ativo | ratificado | arquivado
owner: <agent-responsável>
derived-from:
- req-func-0001-requisitos-funcionais-canon.md (RF-XX)
- req-use-case-0001-casos-de-uso-canon.md (UC-YY)
last-revised: 'DD/MM/AAAA'
lgpd-class: n/a | PII-zero | PII-sintético
tags:
- specs
- docs
- rf-XX
- doc-arch-0006-uc-v1-YY
---

---
spec_id: spec-<NNN>
specname: <slug>
version: <ver>
status: ratificado
custody: <agent-responsável> (.ai/specs/)
created: DD/MM/AAAA
updated: DD/MM/AAAA
origin: <commit ou handoff origem>
task: TA-<NNNN>
kill_switch: inherited
wave: WS-<N> — Onda <N> — <Fase>
lgpd-class: n/a (justificar)
trace:
- .ai/handoffs/HF-<NNNN>.md
- docs/decisoes/ADR-<MMM>-<slug>.md (se houver)
- constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md (Art. X.Y)
- ratificada CCB DD/MM/AAAA (instrumento RAT-YYYY-MM-DD-...)
---

# SPEC spec-<NNN> — <slug> — <Nome da Especificação>

Status: <ativo | implementado em branch | pendente de push e merge> | Branch: `feat/<descricao>` | Orquestrador: <agent-orquestrador>

Fonte única das decisões desta especificação. Em conflito, vale a hierarquia do Art. 2 da Constituição.

---

## 1. Resolução de conflitos documentais

| Tema | Decisão | Fonte vencedora | Texto superado |
|---|---|---|---|
| <tema> | <decisão> | <fonte> | <texto superado> |

Fora do escopo: <o que não entra nesta spec>.

---

## 2. Regras de negócio (RF-XX, UC-YY)

Descrever regras de negócio, validações, cálculos, arredondamentos (ex: Dinheiro sempre `Decimal`; `float` proibido).

---

## 3. Contrato de API

| Endpoint | Método | Parâmetros | Resposta | Código de erro |
|---|---|---|---|---|
| `/v1/<recurso>` | GET/POST | <params> | <schema> | 400, 401, 404, 500 |

OpenAPI disponível em `/docs` quando `DEBUG=true`.

---

## 4. Modelagem de dados

Tabelas PT-BR envolvidas (conforme doc-arch-0001-camada-de-dados-canon.md v3.2), FKs, CHECK constraints, soft delete.

---

## 5. Segurança

- Validação de entrada (Pydantic)
- Rate limiting (6 req/15min)
- Parameterized queries (sem SQLi)
- Sem PII real
- Erros genéricos (sem traceback de usuário)

---

## 6. Critérios de aceite (DoD)

- [ ] Clean Architecture (4 camadas)
- [ ] Queries parameterizadas
- [ ] Nomenclatura PT-BR
- [ ] Testes unitários (cobertura ≥ 80% nos módulos tocados)
- [ ] OpenAPI atualizado
- [ ] Funciona via `docker compose up`

---

## 7. Testes

| Módulo | Caso de teste | Resultado esperado | Automatizado? |
|---|---|---|---|
| <modulo> | <cenario> | <esperado> | Sim/Não |

---

**Rastreabilidade:** RF-XX → UC-YY → spec-<NNN> → handoff HF-<NNNN> → código → teste → merge.

**Fim da SPEC spec-<NNN>**
