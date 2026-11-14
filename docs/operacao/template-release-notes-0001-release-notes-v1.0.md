---
id: template-release-notes-0001-release-notes-v1.0
type: template-release
title: TEMPLATE RELEASE — 0001 Release Notes
version: v1.0
status: rascunho
canonical: false
canonical_slug: 0001-release-notes
created: '2026-11-14'
updated: '2026-11-14'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: gh-sig:owner:leonardosetti:14863508
ratified_at: '2026-11-14'
supersedes: null
superseded_by: null
trace:
  constitution: []
  req_func: []
  req_nfunc: []
  use_cases: []
  specs: []
  handoffs: []
  adrs: []
  code: []
  tests: []
domain: general
layer: artifact
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Release Notes — COBECO v<X.Y.Z>

**Versão:** v<X.Y.Z> (SemVer)  
**Data de Release:** DD/MM/AAAA  
**Tag Git:** `v<X.Y.Z>`  
**Commit Base:** `<hash curto>`  
**Branch:** `main`  
**CI Run:** `<GitHub Actions Run ID / URL>` — ✅ Verde  
**Cobertura Testes:** XX% (unit) + YY% (E2E críticos)  
**Autor:** Proddoc-arch-0006-uc-v1t Owner  
**Aprovado por:** CCB (Gate 3)

---

## 1. Resumo da Release

<Uma frase descrevendo o foco desta release. Ex.: "Primeira release funcional do MVP COBECO com autenticação, CRUD de listas, comparação de preços e exportação PDF.">

### Tipo de Release
- [ ] **Major (X.0.0)** — Breaking changes, nova arquitetura
- [ ] **Minor (X.Y.0)** — Novas funcionalidades compatíveis
- [x] **Patch (X.Y.Z)** — Correções, melhorias, sem breaking changes
- [ ] **Release Candidate (X.Y.Z-rc.N)** — Candidata a release, testes finais

---

## 2. Novidades (Added)

| Item | RF/UC | Descrição | PR | Autor |
|------|-------|-----------|----|-------|
| <Ex.: Autenticação JWT completa> | RF01-RF04 / UC09-UC12 | Cadastro, Login, Logout, Recuperação senha com bcrypt + JWT HS256 | #12 | Dev Back 1 |
| <Ex.: CRUD Listas de Compras> | RF07-RF11 / UC01,UC02,UC13-UC17 | Lista em memória, autocomplete, persistir, listar, editar, excluir, promover efêmera | #15 | Dev Back 2 + Dev Front |
| <Ex.: Comparação de Preços> | RF12-RF16 / UC03-UC07 | Seleção categorias/fornecedores, slider disponibilidade, cálculo orçamento, visualização resultados | #18 | Dev Back 1 + Dev Front |
| <Ex.: Exportação PDF A4> | RF17 / UC08/UC29 | ReportLab server-side, funciona para visitantes e autenticados | #21 | Dev Back 2 |
| <Ex.: Gestão de Perfil> | RF05,RF06 / UC16,UC18 | Visualizar/editar perfil, alterar senha com validação atual | #22 | Dev Back 1 |
| <Ex.: UI Feedback Global> | RNF05 | Toast, skeletons, modais confirmação, loading states | #23 | Dev Front |

---

## 3. Melhorias (Changed)

| Item | Descrição | PR | Autor |
|------|-----------|----|-------|
| <Ex.: Performance seed script> | Bulk insert + índices pós-carga → < 5s para 300 preços | #24 | Dev Back 2 |
| <Ex.: Docker Compose otimizado> | Health checks robustos, redes ortogonais (data/edge), proxy nginx | #10 | DevOps |
| <Ex.: CI Pipeline < 5 min> | Cache Docker layers, parallel jobs, ruff+mypy+pytest otimizados | #11 | DevOps |

---

## 4. Correções (Fixed)

| Item | Bug/Issue | Descrição | PR | Autor |
|------|-----------|-----------|----|-------|
| <Ex.: Rate limit login> | #45 | Corrigido contador por IP (era por usuário) | #46 | Dev Back 1 |
| <Ex.: Soft delete lista> | #52 | `deletado_em` não era filtrado em `ListarMinhasListas` | #53 | Dev Back 2 |

---

## 5. Removido / Deprecado (Removed / Deprecated)

| Item | Motivo | Substituto | PR |
|------|--------|------------|----|
| — | — | — | — |

---

## 6. Segurança (Security)

| Item | Descrição | Severidade | PR |
|------|-----------|------------|----|
| <Ex.: Dependência atualizada> | `python-jose` 3.3.0 → 3.4.0 (CVE-2024-XXXXX) | Média | #25 |
| <Ex.: Headers de segurança> | CSP, HSTS, X-Frame-Options no nginx | Baixa | #26 |

---

## 7. Migrações de Banco (Database Migrations)

| Migration ID | Descrição | Rollback Testado? |
|--------------|-----------|-------------------|
| `<hash>_add_coluna_xyz` | Adiciona coluna `xyz` na tabela `usuarios` | ✅ Sim (`alembic downgrade -1`) |

---

## 8. Quebras de Compatibilidade (Breaking Changes)

> **Nenhuma nesta release (Patch).**  
> Se houver: documentar aqui + guia de migração para usuários/desenvolvedores.

---

## 9. Métricas de Qualidade (Quality Gates)

| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Cobertura Testes Unitários | XX% | ≥ 80% | 🟢 Pass |
| Testes E2E Críticos | YY/ZZ | 100% | 🟢 Pass |
| CI Pipeline Tempo | XXXs | < 300s | 🟢 Pass |
| Lint (ruff) | 0 erros | 0 | 🟢 Pass |
| Type Check (mypy) | 0 erros | 0 | 🟢 Pass |
| Segurança (bandit) | 0 achados | 0 | 🟢 Pass |
| Docker Build | Sdoc-arch-0006-uc-v1esso | Sdoc-arch-0006-uc-v1esso | 🟢 Pass |

---

## 10. Como Atualizar (Upgrade Instrdoc-arch-0006-uc-v1tions)

### Desenvolvimento / Homologação
```bash
git fetch origin
git checkout main
git pull origin main
git checkout v<X.Y.Z>  # ou tag específica
make down
make up              # reconstrói com novas imagens
make health
make test-cov        # validar
```

### Produção (se aplicável)
```bash
# Ver Runbook "Deploy Produção" (docs/operacao/runbook-deploy-0001-deploy-v1.0.md)
docker compose pull
docker compose up -d --no-deps backend frontend proxy
make health
# Smoke test crítico
```

---

## 11. Rollback (Se Necessário)

```bash
# Voltar tag anterior
git checkout v<X.Y.Z-1>
docker compose pull
docker compose up -d --no-deps backend frontend proxy
make health
```

**Tag Anterior:** `v<X.Y.Z-1>` — Release Notes: `RELEASE-NOTES-v<X.Y.Z-1>.md`

---

## 12. Links Úteis

- **Changelog Completo:** `CHANGELOG.md` (Keep a Changelog format)
- **GitHub Release:** `https://github.com/leonardosetti/COBECO/releases/tag/v<X.Y.Z>`
- **CI Run:** `https://github.com/leonardosetti/COBECO/actions/runs/<RUN_ID>`
- **PRs Incluídos:** `#12, #15, #18, #21, #22, #23, #24, #25, #26`
- **Roadmap:** `board-roadmap-0001-roadmap-canon.md` + GitHub Projects

---

## 13. Aprovação (Gate 3 — Go-Live)

| Papel | Nome | Assinatura | Data | Decisão |
|-------|------|------------|------|---------|
| **CCB Chair / PO** | | | | ☐ Aprovar Release ☐ Bloquear |
| **Tech Lead** | | | | ☐ Aprovar Release ☐ Bloquear |
| **QA Lead** | | | | ☐ Aprovar Release ☐ Bloquear |
| **Orientador** | | | | ☐ Ciência ☐ Exige Ajuste |

---

## Controle de Versões deste Documento

| Versão | Data | Autor | Mudança |
|--------|------|-------|---------|
| 1.0 | DD/MM/AAAA | PO | Criação para release v<X.Y.Z> |

---

**Fim das Release Notes v<X.Y.Z>**  
*Formato: Keep a Changelog + SemVer. Arquivar em `docs/operacao/RELEASE-NOTES-v<X.Y.Z>.md`*