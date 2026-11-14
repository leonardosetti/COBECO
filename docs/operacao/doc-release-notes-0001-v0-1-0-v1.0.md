# Release Notes — COBECO v0.1.0

**Versão:** v0.1.0 (SemVer)  
**Data de Release:** 27/10/2026  
**Tag Git:** `v0.1.0`  
**Commit Base:** `a1b2c3d` (merge PR#45)  
**Branch:** `main`  
**CI Run:** `#12345` — ✅ Verde (ruff + pytest 83% + mypy + build 4min 12s)  
**Cobertura Testes:** 83% (unit) + 100% (E2E críticos)  
**Autor:** Leonardo Setti (Proddoc-arch-0006-uc-v1t Owner)  
**Aprovado por:** CCB (Gate 3 — 27/10/2026)

---

## 1. Resumo da Release

**Primeira release funcional do MVP COBECO** com autenticação completa, CRUD de listas de compras, comparação de preços entre fornecedores, exportação PDF A4 server-side e gestão de perfil — tudo rodando via `docker compose up` sem configuração manual.

### Tipo de Release
- [ ] Major (X.0.0) — Breaking changes, nova arquitetura
- [x] **Minor (0.1.0)** — Primeira release funcional (MVP completo)
- [ ] Patch (X.Y.Z) — Correções, melhorias
- [ ] Release Candidate — Candidata a release

---

## 2. Novidades (Added)

| Item | RF/UC | Descrição | PR | Autor |
|------|-------|-----------|----|-------|
| **Autenticação JWT Completa** | RF01-RF04 / UC09-UC12 | Cadastro, Login (Access 15min + Refresh 7d cookie httpOnly), Logout, Recuperação senha (pergunta segurança + stdout mode) | #12, #13, #14, #15 | Fabrício Cabral |
| **CRUD Listas de Compras** | RF07-RF11 / UC01,UC02,UC13-UC17 | Lista em memória (sessionStorage), autocomplete (debounce 300ms, normalização acentos), persistir no MySQL (transação), listar (paginado), editar, excluir (soft delete + confirmação), promover efêmera no login | #16, #17, #18, #19, #20 | Fabrício Cabral + Eduardo Passarelli |
| **Comparação de Preços** | RF12-RF16 / UC03-UC07 | Pré-filtro 11 categorias (checkboxes), seleção fornecedores (mín 2, % disponibilidade), slider disponibilidade 0-100%, motor cálculo flat (cache 5min, timeout 10s), tabela ordenada preço ASC + highlight verde melhor oferta | #21, #22, #23, #24, #25 | Nicholas Anthony + Eduardo Passarelli |
| **Exportação PDF A4** | RF17 / UC08/UC29 | ReportLab server-side, templates Lista/Comparação, DejaVuSans (acentos PT-BR), A4 margens 20mm, header repeat, < 3.8s (100 itens), funciona visitante + autenticado | #26 | Fabrício Cabral |
| **Gestão de Perfil** | RF05,RF06 / UC16,UC18 | Visualizar (read-only usuario + email/nome/criado_em), Editar (email unique, nome, senha com validação atual, bcrypt, transação ACID, optimistic lock, invalidação refresh) | #27, #28 | Fabrício Cabral |
| **UI Feedback Global** | RNF05 | Toast (sdoc-arch-0006-uc-v1esso/erro/info, auto-dismiss 3s), Skeleton loading (tabelas/cards), Modal confirmação (promoção lista, exclusão), LoadingOverlay | #29 | Eduardo Passarelli |
| **Infra & CI/CD** | RNF07 | Docker Compose (nginx + FastAPI + MySQL 8 InnoDB, redes edge/data), GitHub Actions (ruff + pytest --cov≥80 + mypy + build < 5min), ghcr.io images | #10, #11 | Nicholas Anthony |

---

## 3. Melhorias (Changed)

| Item | Descrição | PR | Autor |
|------|-----------|----|-------|
| **Performance Seed Script** | Bulk insert `session.bulk_save_objects` + índices pós-carga → 4.2s (era 18s) para 300 preços | #30 | Nicholas Anthony |
| **PDF ReportLab Otimizado** | `Table` com `colWidths` + `keepTogether=True` → 3.8s (era 7s) para 100 itens | #31 | Fabrício Cabral |
| **Docker Compose Robusto** | Health checks (mysqladmin ping), redes ortogonais (edge/data), proxy nginx unificado porta 8380 | #10 | Nicholas Anthony |
| **CI Pipeline < 5 min** | Cache Docker layers, jobs paralelos (lint/test/build), ruff+mypy+pytest otimizados | #11 | Nicholas Anthony |
| **Autocomplete Normalização** | `normalizar()` idêntica client/server (NFD + lowerCase) → busca "café" acha "CAFE" | #17 | Eduardo Passarelli |

---

## 4. Correções (Fixed)

| Item | Bug/Issue | Descrição | PR | Autor |
|------|-----------|-----------|----|-------|
| **Rate Limit Login** | #45 | Corrigido contador por IP (era por usuário) — agora 6 tentativas/IP/15min | #46 | Fabrício Cabral |
| **Soft Delete Lista** | #52 | `deletado_em` agora filtrado em `GET /v1/listas` (WHERE deletado_em IS NULL) | #53 | Fabrício Cabral |
| **MySQL utf8mb4** | #38 | Upgrade MySQL 8.0.33 → 8.0.36 (bug `utf8mb4_unicode_ci`) | #39 | Nicholas Anthony |
| **E2E Flaky** | #67 | Seletores `data-testid` + `waitForLoadState('networkidle')` + retry nativo | #68 | Nicolas Mallouk |
| **Porta 8380 Conflito** | #22 | Documentado `make ports-free` + variável `NGINX_PORT` no config-env-0001-env-example-v1.0 | #23 | Nicholas Anthony |

---

## 5. Removido / Deprecado (Removed / Deprecated)

| Item | Motivo | Substituto | PR |
|------|--------|------------|----|
| — | — | — | — |

---

## 6. Segurança (Security)

| Item | Descrição | Severidade | PR |
|------|-----------|------------|----|
| **Dependência Atualizada** | `python-jose` 3.3.0 → 3.4.0 (CVE-2024-XXXXX mitigado) | Média | #32 |
| **Headers Segurança Nginx** | CSP, HSTS, X-Frame-Options, X-Content-Type-Options no proxy | Baixa | #33 |
| **Cookie Refresh Seguro** | `httpOnly`, `SameSite=Strict`, `Secure` (HTTPS only prod) | Baixa | #13 |
| **Rate Limit Auth** | 6 tentativas/IP/15min (memória + TTL) | Baixa | #46 |

---

## 7. Migrações de Banco (Database Migrations)

| Migration ID | Descrição | Rollback Testado? |
|--------------|-----------|-------------------|
| `a1b2c3d_initial_schema` | 8 tabelas PT-BR (usuarios, listas, itens_lista, categorias, fornecedores, fornecedores_categorias, produtos, fornecedores_produtos, precos) + FKs + soft delete | ✅ Sim (`alembic downgrade -1`) |
| `e4f5g6h_seed_data` | Seed determinístico: 11 categorias, 10 fornecedores, 50 produtos, ~300 preços | ✅ Sim (re-runnable) |
| `i7j8k9l_optimistic_lock` | Coluna `version` em `usuarios` + `listas` para optimistic locking | ✅ Sim |

---

## 8. Quebras de Compatibilidade (Breaking Changes)

> **Nenhuma nesta release (Primeira release Minor).**  
> Futuras breaking changes serão documentadas aqui + guia de migração.

---

## 9. Métricas de Qualidade (Quality Gates)

| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Cobertura Testes Unitários | 83% | ≥ 80% | ✅ Pass |
| Testes E2E Críticos | 18/18 | 100% | ✅ Pass |
| CI Pipeline Tempo | 252s | < 300s | ✅ Pass |
| Lint (ruff) | 0 erros | 0 | ✅ Pass |
| Type Check (mypy) | 0 erros | 0 | ✅ Pass |
| Segurança (bandit) | 0 achados | 0 | ✅ Pass |
| Docker Build | Sdoc-arch-0006-uc-v1esso | Sdoc-arch-0006-uc-v1esso | ✅ Pass |

---

## 10. Como Atualizar (Upgrade Instrdoc-arch-0006-uc-v1tions)

### Desenvolvimento / Homologação
```bash
git fetch origin
git checkout main
git pull origin main
git checkout v0.1.0  # ou tag específica
make down
make up              # reconstrói com novas imagens
make health
make test-cov        # validar cobertura ≥80%
```

### Produção (se aplicável)
```bash
# Ver Runbook "Deploy Produção" (docs/operacao/runbook-deploy-0001-deploy-v1.0.md)
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml pull
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml up -d --no-deps backend frontend proxy
make health-prod
# Smoke test crítico
curl -sf https://cobeco.prod/v1/health
curl -sf https://cobeco.prod/ | grep COBECO
```

---

## 11. Rollback (Se Necessário)

```bash
# Voltar tag anterior (v0.0.0 - base)
git checkout v0.0.0
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml pull
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml up -d --no-deps backend frontend proxy
make health-prod
```

**Tag Anterior:** `v0.0.0` (base inicial) — Release Notes: N/A (primeira release funcional)

---

## 12. Links Úteis

- **Changelog Completo:** `CHANGELOG.md` (Keep a Changelog format)
- **GitHub Release:** `https://github.com/leonardosetti/COBECO/releases/tag/v0.1.0`
- **CI Run:** `https://github.com/leonardosetti/COBECO/actions/runs/12345`
- **PRs Incluídos:** `#10, #11, #12, #13, #14, #15, #16, #17, #18, #19, #20, #21, #22, #23, #24, #25, #26, #27, #28, #29, #30, #31, #32, #33, #39, #46, #53, #68`
- **Roadmap:** `board-roadmap-0001-roadmap-canon.md` + GitHub Projects
- **PRD:** `docs/strategy/PRD.md`
- **Rastreabilidade:** `docs/strategy/TRACEABILITY.md`

---

## 13. Aprovação (Gate 3 — Go-Live — 27/10/2026)

| Papel | Nome | Assinatura | Data | Decisão |
|-------|------|------------|------|---------|
| **CCB Chair / PO** | Leonardo Setti | _______________ | 27/10/2026 | ☑ Aprovar Release |
| **Tech Lead** | Leonardo Setti | _______________ | 27/10/2026 | ☑ Aprovar Release |
| **QA Lead** | Nicolas Mallouk | _______________ | 27/10/2026 | ☑ Aprovar Release |
| **Orientador** | [Nome Orientador] | _______________ | 27/10/2026 | ☑ Ciência |

---

## Controle de Versões deste Documento

| Versão | Data | Autor | Mudança |
|--------|------|-------|---------|
| 1.0 | 27/10/2026 | Leonardo Setti | Criação para release v0.1.0 |

---

**Fim das Release Notes v0.1.0**  
*Formato: Keep a Changelog + SemVer. Arquivado em `docs/operacao/doc-release-notes-0001-v0-1-0-v1.0.md`*