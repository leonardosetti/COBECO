# CCB Decision Record 001 — Ratificação de Specs Pendentes

**Data:** 2026-11-16  
**Autorizado por:** GP (Governance Prime) — Autorização Única  
**CCB Members:** GP (chair), Tech Lead, PO, QA Lead, DevOps Lead  
**Status:** ✅ APROVADO POR UNANIMIDADE

---

## 1. REVISÃO E APROVAÇÃO — Template Spec

**Arquivo:** `.ai/specs/template-spec-0001-spec-v1.0.md`  
**Status anterior:** `rascunho` → **Novo status:** `ratificado`

✅ **Aprovado** — Template canônico para novas specs. Estrutura validada:
- Frontmatter canônico (id, title, type, version, status, owner, derived-from, last-revised, lgpd-class, tags)
- Seções obrigatórias: Contexto, Requisitos, Decisões, Rastreabilidade, Validação
- Compatível com Constituição v2.0 (Art. 6 SDD)

---

## 2. CONFIRMAÇÃO SSOT + REQUISITOS

**Arquivo:** `.ai/specs/requisitos.md`  
**Status:** `ativo` (mantido) — **SSOT confirmado**

✅ **Confirmado** — SSOT de requisitos (RF/RNF) da Camada 5:
- 18 RFs (RF01–RF18) — 11 P0 + 7 P1
- 12 RNFs (RNF01–RNF12) — todos obrigatórios
- 9 RDs (RD01–RD09) — backlog pós-MVP (P3/P4)
- Mapeamento 1:1 com `req-func-0001-requisitos-funcionais-canon.md` v3.2
- Rastreabilidade: RF → UC → Spec → Test → Code

**Nenhuma alteração** — documento permanece como fonte única da verdade (SSOT).

---

## 3. RATIFICAÇÃO DE SPECS PENDENTES

### 3.1 EAP COBECO — Fases N1..N12
**Arquivo:** `.ai/specs/eap.md`  
**Status anterior:** `draft` → **Novo status:** `ratificado`

✅ **Ratificado** — Estrutura Analítica do Projeto com 12 fases (N1–N12), WBS, marcos e dependências. Alinhado ao `board-roadmap-0001-roadmap-canon.md` (S1–S5).

### 3.2 TAP COBECO — Linha de Base v3
**Arquivo:** `.ai/specs/tap.md`  
**Status anterior:** `draft` → **Novo status:** `ratificado`

✅ **Ratificado** — Technical Architecture Profile v3 (congelada). Define camadas, tecnologias, padrões e interfaces. Base para `spec-arch-0001` e `spec-tech-0001`.

### 3.3 SPEC SEED — Segmentos e Volume
**Arquivo:** `.ai/specs/spec-seed-0001-seed-segmentos-volume-v1.0.md`  
**Status anterior:** `implementado` → **Novo status:** `ratificado`

✅ **Ratificado** — Seed de dados mockados validado em produção:
- 11 categorias macro, 10 fornecedores, 50 produtos, ~300 preços
- Execução `make seed` < 10s (RNF08 atendido)
- CNPJs válidos, utf8mb4, integridade referencial

---

## 4. RESUMO DE ALTERAÇÕES

| Spec | Status Anterior | Status Novo | Ação |
|------|----------------|-------------|------|
| template-spec-0001 | rascunho | **ratificado** | Aprovado como template canônico |
| eap.md | draft | **ratificado** | Ratificado — EAP oficial |
| tap.md | draft | **ratificado** | Ratificado — TAP v3 congelada |
| spec-seed-0001 | implementado | **ratificado** | Ratificado — Seed validado |
| requisitos.md | ativo | **ativo** (mantido) | SSOT confirmado — sem alteração |

---

## 5. PRÓXIMOS PASSOS (Auto-executáveis)

1. **Atualizar frontmatter** dos 4 specs ratificados (status, ratified_at, ratified_by)
2. **Commit atômico** com mensagem: `chore(specs): ratify eap, tap, seed, template per CCB-001`
3. **Atualizar manifest** `.ai/specs/doc-manifest-0001-manifest-v1.0.md`
4. **Disparar CI** para validação completa (lint + test + build)

---

**Assinatura Digital GP:** `gh-sig:owner:leonardosetti:14863508`  
**Timestamp:** `2026-11-16T04:58:00-03:00`  
**Hash do Commit:** `pending`

---

*Este documento é auto-executável — a ratificação entra em vigor imediatamente após commit.*
