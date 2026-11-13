# Plano de Implementação — COBECO MVP (sequencial)

**Status:** rascunho de execução  
**Base:** constitution.md (lei suprema), REQUISITOS.md v3.2, CAMADADEDADOS.md v3.2, CASOSDEUSO.md v3.2, ADR-001 (stack ratificada), board_roadmap.md (marcos S1–S5)  
**Stack aprovada:** FastAPI + Pydantic + SQLAlchemy 2.0 (async) + MySQL 8 InnoDB + Alembic + ReportLab (backend); Vanilla JS + Tailwind + nginx (frontend); Docker Compose (infra); GitHub Actions (CI)

---

## Contexto remoto (GitHub)

- Remote `origin` = `git@github.com:leonardosetti/COBECO.git`
- Branches locais: `main` (atual), `stage`; `integracao-leonardo` só no remote
- Últimos commits locais: `881c971 revisão de texto`, `a5d93c1 prototipo de baixa SVG`, `6241891 demo COBECO`
- **Todo o scaffold do MVP (backend, frontend, docker, .github, specs, Makefile, .env) está não versionado** (`git status` mostra `??` em tudo). Não está no GitHub ainda.
- Antes de criar cards/issues no GitHub, fazer o commit inicial em `main` (exemplo de mensagem abaixo) e depois criar milestones/labels/issues.

### Commit inicial (exemplo, caveman-commit)

```
chore: import scaffold COBECO MVP

Importa backend FastAPI, frontend Vanilla JS, nginx proxy, Docker Compose,
seed SQL, Alembic, specs SDD, CI GitHub Actions e documentação v3.2.
Aplica DoD: Clean Architecture, queries parameterizadas, nomenclatura PT-BR.
```

## 0. Estado atual (o que já existe — não recriar)

| Artefato | Estado | Observação |
|---|---|---|
| `constitution.md` | ✅ v1.0 | Lei suprema; Art. 6 obriga SDD (spec → handoff) |
| `REQUISITOS.md` | ✅ v3.2 | 18 RF / 12 RNF / 9 desejáveis (backlog pós-MVP) |
| `CAMADADEDADOS.md` | ✅ v3.2 | 8 tabelas PT-BR, seed 11 cat + 10 forn + 50 prod + ~300 preços |
| `.ai/specs/*.md` | ✅ spec-001…015 | Contratos SDD já produzidos |
| `.ai/handoffs/HF-*.md` | ✅ ~126 | Handoffs já gerados |
| `ADR-001-stack-decision.md` | ✅ Ratificada 13/11/2026 | Stack FastAPI + MySQL + Vanilla JS |
| `docker-compose.yml` + override | ✅ | db/migrate/seed/backend/frontend/proxy, redes `data` e `edge` |
| `backend/src/` | ✅ Scaffold | domain (entities/repositories/usecases), adapters (api/db), config, main |
| Routers API | ⚠️ Parcial | auth, listas, catalogo, comparação, exportação prontos; **perfil só tem health stub** |
| Modelos SQLAlchemy + Alembic | ✅ | 8 tabelas, migração inicial `20261113_000001` |
| `seed.sql` | ✅ | Idempotente, executado no container `seed` |
| Frontend `app.js` | ✅ | ~1.5k linhas: ApiClient, auth, listas, catálogo, comparação, export, print |
| `.github/workflows/ci.yml` | ✅ | ruff + pytest --cov≥80 + mypy + build Docker |
| Makefile | ✅ | up/down/test/test-cov/lint/seed/migrate/ci/health |
| `.env` | ✅ | Existe (não commitar valores reais) |

**O que falta para o MVP completo:** router de perfil (RF05/RF06), revisão de stubs `pass` em use cases, testes unitários (coverage ≥80%), testes E2E Playwright, CI verde local, `docker compose up` sem config manual, demo + docs finais.

---

## 1. Passos sequenciais (execução)

> Regra (constitution Art. 3.6/3.7): nada de abstração, wrapper ou opção "para depois". Nada que não esteja nos 18 RF.  
> Regra (constitution Art. 6): cada fluxo entra como spec em `.ai/specs/` e sai como handoff em `.ai/handoffs/` antes do dispatch.

### Fase 0 — Documentação base (constitution, requisitos, specs)

**0.1** Validar que `constitution.md`, `REQUISITOS.md`, `CAMADADEDADOS.md`, `CASOSDEUSO.md` estão alinhados (SSOT v3.2).  
→ Critério de saída: nenhuma contradição entre os três documentos de requisitos e o DER (8 tabelas, N:N fornecedores↔categorias, soft delete em `usuarios`/`listas`).

**0.2** Validar specs SDD em `.ai/specs/` contra os requisitos (spec-004 backend MVP, spec-005 container layers, spec-008 frontend, spec-009 UAT, spec-011 CI/CD).  
→ Critério de saída: cada RF01–RF18 rastreável a pelo menos uma spec; specs aprovadas pelo CCB (ratificação humana, constitution Art. 5.1).

**0.3** Consolidar documentação e gerar o PDF ABNT (objetivo, escopo, RFs/RNFs, caso de uso, DER, protótipos, stack, nomes dos 5 integrantes).  
→ Critério de saída: PDF gerado; card `[DOCS-P0]` da Sprint 1 movido para Done (board_roadmap.md).

**0.4** (Apenas se houver gap) Produzir/especificar quaisquer requisito ou spec em falta, seguindo a cadeia spec → handoff → `handoff_parser.py` → dispatch do L0.  
→ Não criar specs para requisitos já cobertos (YAGNI).

### Fase 1 — Backend: completar autenticação e perfil (RF01–RF06)

**1.1** Revisar stubs `pass` em `backend/src/domain/usecases.py` (linhas ~230 recuperação de senha modo log, ~299 criar-lista-memória — esta é frontend-only por decisão de projeto) e `backend/src/adapters/db/database.py` (linha 21 `class Base` — `pass` é correto para `DeclarativeBase`, não alterar).  
→ Apenas o modo log de recuperação de senha precisa imprimir o token no stdout (`RECOVERY_MODE=log`).

**1.2** Implementar router de perfil completo em `backend/src/adapters/api/perfil.py`:  
- `GET /perfil` → visualizar perfil (RF05): nome_usuario read-only, email, nome, criado_em.  
- `PUT /perfil` → gerenciar perfil (RF06): alterar email, nome e senha; exigir senha atual; email único; transação ACID.

**1.3** Incluir `perfil.router` em `backend/src/main.py` (prefixo `/perfil`, tag "Perfil").

**1.4** Executar `make test` (integration `test_auth_flow.py`) e ajustar até verde.  
→ Critério de saída: RF01–RF06 funcionando via `docker compose up`; JWT access 15min em memória, refresh 7d cookie `httpOnly`/`SameSite=Strict`; rate limiting 6 req/15min; bcrypt salt=12.

### Fase 2 — Catálogo, listas e comparação (RF07–RF16)

**2.1** Verificar routers `catalogo.py` (categorias/fornecedores/autocomplete), `listas.py` (salvar/listar/editar/excluir/promover efêmera) e `comparacao.py` (calcular orçamento com cache 5min + timeout 10s, visualizar resultados).  
→ Critério de saída: endpoints respondem conforme schemas Pydantic; queries parameterizadas (sem SQLi); transação explícita `BEGIN/COMMIT` em salvar-lista; soft delete respeitado (`deletado_em`).

**2.2** Verificar frontend `app.js` contra RF07–RF16 (autocomplete debounce 300ms, lista em memória `sessionStorage`, mínimo 2 fornecedores, slider disponibilidade, tabela ordenada preço ASC, destaque verde melhor oferta, tooltip ausentes).  
→ Critério de saída: fluxo completo no navegador: cadastro → login → categorias → fornecedores → cálculo → resultados.

**2.3** Rodar `make seed` e confirmar <10s (RNF08).  
→ Critério de saída: 11 categorias, 10 fornecedores, 50 produtos, ~300 preços populados.

### Fase 3 — Exportação e impressão (RF17–RF18)

**3.1** Verificar router `exportacao.py` (`POST /export/pdf` com ReportLab, PDF A4, nome `lista_YYYYMMDD.pdf`, funciona para visitantes e autenticados, <5s até 100 itens — RNF11).  
→ Critério de saída: PDF baixável e válido.

**3.2** Verificar CSS `@media print` no frontend (ocultar menus, quebras de página, header repetido em tabelas longas).  
→ Critério de saída: `Ctrl+P` gera view A4 limpa.

### Fase 4 — Testes e qualidade (RNF06, RNF09, RNF10)

**4.1** Escrever testes unitários em `backend/tests/unit/` (regras de negócio: validação de senha RF01, cálculo de orçamento RF15, validações de lista).  
→ Critério de saída: `pytest --cov=src --cov-fail-under=80` passa; cobertura ≥80% nos módulos tocados; testes determinísticos (sem relógio de parede, sem rede, sem dados reais — Art. 8.2).

**4.2** Implementar testes E2E com Playwright (fluxo demo: cadastro → comparação → exportação PDF).  
→ Critério de saída: E2E verde em `docker compose up`.

**4.3** Rodar `make ci` localmente (ruff + pytest + mypy + build Docker).  
→ Critério de saída: pipeline local <5min; CI do GitHub Actions verde em `main` e `stage`.

### Fase 5 — Infra, buffer e demo (S5 do board_roadmap)

**5.1** Confirmar `docker compose up -d --build` sobe tudo sem configuração manual extra (DoD).  
→ Critério de saída: `make health` retorna Proxy OK + Backend OK na porta 8380.

**5.2** Refinar README.md com instruções `docker compose up`, arquitetura e OpenAPI (`/docs` validado pelo Swagger — RNF02).

**5.3** Ensaio da apresentação final (30–35 min, 5 integrantes, roteiro cadastro → comparação → exportação PDF).

**5.4** Code review com rubrica R-01…R-07 (constitution Art. 8.3), gatekeeper, aprovação humana (Art. 5.1) e merge em `main`.

---

## 2. Avaliação: runbooks, hooks e custom skills

### Runbooks — RECOMENDADO (mínimo)

O Makefile já cumpre o papel operacional (`up`, `down`, `seed`, `migrate`, `test-cov`, `health`, `ci`, `clean`).  
**Decisão:** criar **1 runbook leve** (`RUNBOOK.md`, 1 página) com: iniciar ambiente, recriar DB (`make db-reset`), re-seed, recuperar senha (modo log = token no stdout do container), reset de `SECRET_KEY`, e comandos de troubleshooting mais comuns.  
Não criar biblioteca de runbooks SRE completa: é MVP acadêmico, desktop-only, zero cloud (constitution Art. 1.2). YAGNI.

### Hooks — RECOMENDADO (1–2 leves)

`.opencode/hooks` já existe. OpenCode pode garantir antes do commit/push:
- **pre-commit:** nenhum segredo/commitado (constitution Art. 7.1) — grep por `SECRET_KEY=`, senhas, tokens reais.
- **pre-push:** `make ci` ou `make test-cov` verde (não mergear com CI vermelho).

Não criar hooks de CI dentro do repositório além do GitHub Actions já existente (`.github/workflows/ci.yml`). Evitar duplicação.

### Custom skills — NÃO criar agora (YAGNI, Art. 3.7)

- `skills-lock.json` já trava caveman + ponytail (e derivados). `.opencode/skills` tem ~80 skills instaladas.
- O fluxo SDD já roda via spec → handoff → `handoff_parser.py` → `scripts/nexus_dispatcher.py` (constitution Art. 4.2/6).
- **Decisão:** não desenvolver custom skills neste MVP. Reutilizar ponytail (este plano), lean-build (execução enxuta) e caveman-review (code review). Reavaliar apenas se o time quiser automatizar parsing de specs/handoffs — e então com CCB + ratificação humana.

---

## 3. Definição de Pronto (DoD) — por PR

- [ ] Clean Architecture (4 camadas), sem vazar framework para o Domain
- [ ] Queries parameterizadas (proteção SQLi)
- [ ] Nomenclatura DB e variáveis em PT-BR (DER v3.2)
- [ ] Testes unitários escritos; cobertura não diminuiu (≥80% nos tocados)
- [ ] Contrato OpenAPI (`/docs`) atualizado (SDD)
- [ ] Funciona via `docker compose up` sem config manual
- [ ] CI verde + code review rubrica R-01…R-07 + aprovação humana

---

## 4. Riscos conhecidos

- **AGENTS.md está desatualizado** (diz "docs only, no source code"); não reescrever a menos que o time peça — fora do escopo deste plano.
- `requirements.txt` usa `asyncmy`; `pyproject.toml` lista `aiomysql` — consistência de dependência a checar no build do Docker.
- Perfil router era apenas stub (`perfil_health`): RF05/RF06 dependem totalmente do passo 1.2.
- Modo `recovery=log` coloca token no stdout do container: adequado para demo acadêmica, não para produção (documentar limitação).

---

**Próxima ação imediata:** executar passo 0.1–0.3 (alinhar documentação + PDF ABNT), depois passo 1.2 (perfil).
