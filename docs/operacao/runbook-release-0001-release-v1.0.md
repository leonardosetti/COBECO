---
id: runbook-release-0001-release-v1.0
type: runbook-release
title: RUNBOOK RELEASE — Release
version: v1.0
status: ratificado
canonical: false
canonical_slug: release
created: '2026-11-14'
updated: '2026-11-14'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: null
ratified_at: null
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
domain: operation
layer: runbook
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# Runbook — Release e Tagging (COBECO MVP)

**Documento:** Runbook Operacional  
**Versão:** 1.0  
**Status:** Ativo  
**Data:** 27/10/2026  
**Autor:** Leonardo Setti (PO / Tech Lead)  
**Aplica-se a:** prod  
**Classificação:** Interno

---

## 1. Propósito

Procedimento padronizado para criar release, tag SemVer, gerar changelog, publicar no GitHub e fazer deploy em produção.

---

## 2. Pré-requisitos

| Item | Verificação |
|------|-------------|
| Gate 3 aprovado | CCB + Orientador assinaram |
| CI verde na `main` | Último run `sdoc-arch-0006-uc-v1cess` |
| Coverage ≥ 80% | `pytest --cov-fail-under=80` passa |
| Runbooks testados | Game Day realizado |
| CHANGELOG.md atualizado | Entrada para nova versão |

---

## 3. Versionamento (SemVer)

| Tipo | Formato | Quando |
|------|---------|--------|
| **Major** | `X.0.0` | Breaking changes, nova arquitetura |
| **Minor** | `X.Y.0` | Novas funcionalidades compatíveis |
| **Patch** | `X.Y.Z` | Correções, melhorias, sem breaking |
| **RC** | `X.Y.Z-rc.N` | Candidata a release, testes finais |

**MVP Atual:** `v0.1.0` (Primeira release funcional)

---

## 4. Procedimento de Release

### 4.1 Preparação (Branch `main`)

```bash
# 1. Estar na main atualizada
git checkout main
git pull origin main

# 2. Verificar CI status
gh run list --branch main --limit 1
# Deve mostrar "sdoc-arch-0006-uc-v1cess" no último run

# 3. Verificar coverage
git checkout main
make test-cov
# Deve mostrar ≥ 80%

# 4. Atualizar CHANGELOG.md (Keep a Changelog format)
# Editar docs/operacao/CHANGELOG.md ou CHANGELOG.md na raiz
# Adicionar seção para nova versão
```

### 4.2 Exemplo Entrada CHANGELOG.md

```markdown
## [v0.1.0] - 2026-10-27

### Added
- Autenticação JWT completa (RF01-RF04)
- CRUD Listas de Compras + Autocomplete (RF07-RF11)
- Comparação de Preços com motor de cálculo (RF12-RF16)
- Exportação PDF A4 server-side (RF17)
- Gestão de Perfil (RF05, RF06)
- UI Feedback Global: Toast, Skeleton, Modal (RNF05)

### Changed
- Performance seed script: 18s → 4.2s (bulk insert)
- PDF ReportLab otimizado: 7s → 3.8s

### Fixed
- Rate limit login: agora por IP (era por usuário)
- Soft delete lista: filtro deletado_em em listagem

### Security
- python-jose 3.3.0 → 3.4.0 (CVE-2024-XXXXX)
- Headers segurança nginx: CSP, HSTS, X-Frame-Options
```

### 4.3 Criar Tag e Release

```bash
# 1. Definir versão
VERSION="v0.1.0"

# 2. Criar tag anotada
git tag -a "${VERSION}" -m "Release ${VERSION}"

# 3. Push tag
git push origin "${VERSION}"

# 4. Criar GitHub Release (gera notes do CHANGELOG)
gh release create "${VERSION}" \
  --title "Release ${VERSION}" \
  --notes-file CHANGELOG.md \
  --verify-tag \
  --target main
```

### 4.4 Deploy Produção (Pós-Tag)

```bash
# O CD pipeline (GitHub Actions) fará automaticamente:
# - Build + Push images para ghcr.io com tag ${VERSION} e latest
# Verificar em: https://github.com/leonardosetti/COBECO/actions

# Validar deploy
make health-prod
# Smoke test
curl -sf https://cobeco.prod/v1/health
curl -sf https://cobeco.prod/ | grep COBECO
```

---

## 5. Rollback de Release

```bash
# 1. Identificar tag anterior
git tag -l "v*" | sort -V | tail -2
# Ex: v0.0.9

# 2. Checkout tag anterior
git checkout v0.0.9

# 3. Re-deploy (CD pipeline fará build/push das images antigas)
# Ou manual:
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml pull
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml up -d --no-deps backend frontend proxy

# 4. Validar
make health-prod
```

---

## 6. Checklist de Release (Gate 3 → Release)

| Item | Verificação | Responsável |
|------|-------------|-------------|
| Gate 3 aprovado | CCB + Orientador assinaram | PO |
| CI verde na main | Último run sdoc-arch-0006-uc-v1cess | DevOps |
| Coverage ≥ 80% | `make test-cov` passa | QA |
| Runbooks testados | Game Day realizado | DevOps |
| CHANGELOG.md atualizado | Entrada nova versão | PO |
| Tag SemVer criada | `git tag -a vX.Y.Z` | Tech Lead |
| GitHub Release criada | `gh release create` | PO |
| Deploy produção OK | `make health-prod` passa | DevOps |
| Smoke test crítico | Login → Lista → Comparação → PDF | QA |
| Notificação stakeholders | Email/Slack "Release vX.Y.Z deployado" | PO |

---

## 7. Rollback de Emergência (Hotfix)

Se bug crítico em produção:

```bash
# 1. Criar branch hotfix da tag atual
git checkout v0.1.0
git checkout -b hotfix/critical-bug

# 2. Fix + test
# ... correção ...
make test-cov

# 3. PR hotfix → main (fast-track review)
# 4. Merge → CI → Tag patch (v0.1.1)
# 5. Deploy automático via CD
```

---

## Controle de Versões

| Versão | Data | Autor | Mudança |
|--------|------|-------|---------|
| 1.0 | 27/10/2026 | Leonardo Setti | Criação inicial |

---

**Fim do Runbook — Release/Tagging**  
*Seguir checklist rigorosamente. Release = compromisso com qualidade.*