# Runbook — <Nome da Operação>

**Documento:** Runbook / Playbook Operacional  
**Versão:** 1.0  
**Status:** Ativo | Arquivado  
**Data:** DD/MM/AAAA  
**Autor:** <Nome> (DevOps / Tech Lead)  
**Última revisão:** DD/MM/AAAA  
**Aplica-se a:** dev | homolog | prod  
**Classificação:** Interno — Senhas/Secrets apenas em `.env` (nunca no doc)

---

## 1. Propósito e Escopo

| Campo | Valor |
|-------|-------|
| **Operação** | <Ex.: Deploy Produção, Rollback, Seed DB, Backup/Restore, Migração> |
| **Frequência** | Sob demanda / Diária / Semanal / Por Release |
| **Tempo Estimado** | <Ex.: 5 min, 30 min, 2h> |
| **Impacto no Usuário** | Nenho / Degradação parcial / Indisponibilidade total |
| **Janela de Manutenção** | <Ex.: Fora horário comercial, qualquer hora> |
| **Aprovação Necessária** | Tech Lead / CCB Chair / Nenhuma (rotina) |

---

## 2. Pré-requisitos e Verificações

| # | Pré-requisito | Comando de Verificação | Critério de Sucesso |
|---|---------------|------------------------|---------------------|
| 1 | Docker Engine rodando | `docker version` | Client + Server respondem |
| 2 | Docker Compose v2 | `docker compose version` | v2.x.x |
| 3 | `.env` presente e válido | `ls -la .env && grep -q SECRET_KEY .env` | Arquivo existe + SECRET_KEY preenchida |
| 4 | Rede Docker `cobeco_data` e `cobeco_edge` | `docker network ls | grep cobeco` | Ambas existem |
| 5 | Imagens disponíveis (local ou registry) | `docker images | grep cobeco` | backend, frontend, proxy, mysql |
| 6 | Banco saudável (se operação precisa) | `make health` | `healthy` em todos containers |
| 7 | Backup recente (se operação destrutiva) | `ls -la backups/` | Backup < 24h |
| 8 | CI verde na branch alvo | GitHub Actions badge / `gh run list` | Último run: success |

---

## 3. Procedimentos Padrão (SOPs)

### 3.1 Subir Ambiente Completo (Desenvolvimento / Homologação)

```bash
# 1. Preparar environment
cp .env.example .env
# EDITAR .env: preencher SECRET_KEY (mín 32 chars), JWT_ALGORITHM=HS256, etc.

# 2. Subir tudo (build + up)
make up
# OU manualmente:
docker compose up -d --build

# 3. Aguardar health checks
make health
# OU manualmente:
# - nginx: curl -f http://localhost:8380/health
# - backend: curl -f http://localhost:8000/health (interno)
# - mysql: docker exec cobeco-mysql mysqladmin ping -h localhost -u root -proot

# 4. Verificar logs
make logs          # todos
make logs-backend  # apenas backend
make logs-frontend # apenas frontend (nginx)
make logs-db       # apenas MySQL

# 5. Smoke test rápido
curl -s http://localhost:8380/ | grep -q "COBECO" && echo "Frontend OK"
curl -s http://localhost:8380/v1/docs | grep -q "swagger" && echo "Backend API OK"
```

**Critério de Sucesso:** `make health` retorna todos `healthy` + smoke test passa.

---

### 3.2 Recriar Banco de Dados do Zero (Destrutivo — Cuidado!)

```bash
# ⚠️ DESTRUTIVO — PERDE TODOS OS DADOS
# Confirmar backup antes: make backup

# 1. Parar containers
docker compose down -v  # -v remove volumes (dados MySQL)

# 2. Subir apenas MySQL
docker compose up -d mysql

# 3. Aguardar MySQL ready
for i in {1..30}; do
  if docker exec cobeco-mysql mysqladmin ping -h localhost -u root -proot --silent; then
    echo "MySQL pronto"; break
  fi
  sleep 2
done

# 4. Rodar migrations
docker compose up -d backend
docker compose exec backend alembic upgrade head

# 5. Popular seed
docker compose exec backend python scripts/seed.py

# 6. Subir resto
docker compose up -d frontend proxy

# 7. Validar
make health
make test
```

**Critério de Sucesso:** `alembic upgrade head` sem erros + `seed.py` roda < 10s + `make test` passa.

---

### 3.3 Executar Testes (Local / CI)

```bash
# Testes unitários + cobertura
make test           # rápido
make test-cov       # com cobertura (falha se < 80%)

# Testes E2E (requer ambiente up)
cd frontend/tests/e2e
npm ci              # primeira vez
npm test            # roda Playwright

# Pipeline CI completo local (simula GitHub Actions)
make ci
# Equivale a: ruff + mypy + pytest --cov-fail-under=80 + build docker
```

**Critério de Sucesso:** `make test-cov` → coverage ≥ 80% + 0 falhas. `make ci` → todos steps passam.

---

### 3.4 Gerenciar Migrações (Alembic)

```bash
# Ver status atual
make migrate-status
# OU: docker compose exec backend alembic current

# Criar nova migration (após mudar models)
make migrate-create MSG="add_column_xyz"
# OU: docker compose exec backend alembic revision --autogenerate -m "add_column_xyz"

# Aplicar migrations
make migrate
# OU: docker compose exec backend alembic upgrade head

# Rollback 1 migration
make migrate-rollback
# OU: docker compose exec backend alembic downgrade -1

# Ver histórico
make migrate-history
# OU: docker compose exec backend alembic history --verbose
```

**Regra de Ouro:** Toda migration **deve** ser testada em CI antes de merge. `alembic downgrade -1` testado localmente.

---

### 3.5 Backup e Restore do Banco (MySQL)

```bash
# BACKUP (cria arquivo timestampado em ./backups/)
make backup
# OU manual:
mkdir -p backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker exec cobeco-mysql mysqldump -u root -proot cobeco > backups/cobeco_${TIMESTAMP}.sql
gzip backups/cobeco_${TIMESTAMP}.sql

# RESTORE (destrutivo — usa backup específico)
make restore BACKUP=backups/cobeco_20261115_143000.sql.gz
# OU manual:
gunzip -c backups/cobeco_20261115_143000.sql.gz | docker exec -i cobeco-mysql mysql -u root -proot cobeco
```

**Política:** Backup automático diário via cron (prod) / antes de toda migration destrutiva. Retenção: 30 dias.

---

### 3.6 Deploy de Nova Versão (Produção / Tag Release)

```bash
# PRÉ-REQUISITOS:
# - Tag criada no Git: git tag -a v0.1.0 -m "Release v0.1.0" && git push origin v0.1.0
# - CI/CD passou (GitHub Actions: build + push ghcr.io)
# - Runbooks de rollback testados

# 1. Pull das imagens da release
docker compose pull

# 2. Rolling update (zero-downtime se possível)
docker compose up -d --no-deps backend
# aguardar health check
sleep 10
make health | grep backend

docker compose up -d --no-deps frontend
docker compose up -d --no-deps proxy

# 3. Validar
make health
# Smoke test crítico
curl -f https://cobeco.exemplo.com/v1/health
curl -f https://cobeco.exemplo.com/

# 4. Marcar release no GitHub
gh release create v0.1.0 --notes-file CHANGELOG.md --verify-tag
```

**Rollback Imediato (se falha):**
```bash
# Voltar tag anterior
docker compose pull --tag v0.0.9
docker compose up -d --no-deps backend frontend proxy
make health
```

---

## 4. Resposta a Incidentes (Troubleshooting)

| Sintoma | Verificação Rápida | Causa Provável | Ação Imediata | Escalação |
|---------|-------------------|----------------|---------------|-----------|
| **Frontend não carrega** (502/503) | `make logs-frontend` | nginx não acha arquivos static / backend down | `docker compose restart frontend proxy` | Tech Lead |
| **Backend API 500** | `make logs-backend` | Exceção não tratada / DB error | Ver traceback → fix + deploy | Dev Backend |
| **Backend não responde** (timeout) | `docker ps | grep backend` | Container parado / OOM / deadlock | `docker compose restart backend` | DevOps |
| **MySQL não conecta** | `make logs-db` | Container down / volume corrompido / senha errada | `docker compose restart mysql` → se persistir: restore backup | DevOps |
| **CI falha: coverage < 80%** | GitHub Actions log | Testes faltando / código novo sem teste | Adicionar testes → push novo | QA / Dev |
| **CI falha: ruff/mypy errors** | GitHub Actions log | Lint ou type error | Fix local → `make lint` → push | Dev |
| **Seed falha / demora > 10s** | `make logs-backend` | FK violation / bulk insert error / lock | Ver SQL error → fix seed.py | Dev Backend |
| **PDF não gera / erro 500** | `make logs-backend` | ReportLab exception / fonte faltando / memória | Ver traceback → fix usecase | Dev Backend |
| **JWT inválido / expirado** | Frontend console / Network tab | Clock skew / secret mismatch / cookie bloqueado | Ver `.env` SECRET_KEY / SameSite / clock sync | Dev Backend |

---

## 5. Segurança e Conformidade

- **`.env` NUNCA no Git** — já no `.gitignore`. Secrets apenas via GitHub Actions secrets / 1Password / vault.
- **Modo Recuperação de Senha:** `RECOVERY_MODE=log` → token no stdout (logs do container), **nunca** por email em dev.
- **Dados Sintéticos Only** — Constitution Art. 3.5. Seed **não** usa PII real. CPF/CNPJ/emails são gerados (faker).
- **Erro não vaza traceback** — FastAPI `debug=False` em prod. Logs estruturados (JSON) para auditoria.
- **Rate Limit Auth** — 6 tentativas / 15 min por IP (middleware). Configurável via `.env`.
- **Cookies Seguros** — `httpOnly`, `SameSite=Strict`, `Secure` (HTTPS apenas em prod).

---

## 6. Contatos e Escalonamento

| Nível | Papel | Nome | Contato (Discord/Email/Phone) | SLA Resposta |
|-------|-------|------|-------------------------------|--------------|
| L1 | Dev de Plantão | <Nome> | Discord @usuario | 15 min (horário comercial) |
| L2 | Tech Lead | <Nome> | Discord @usuario + Email | 30 min |
| L3 | CCB Chair / PO | <Nome> | Discord @usuario + Email | 1h |
| L4 | Orientador (se impacto acadêmico) | <Nome> | Email institucional | 4h |

**Critérios de Escalação:**
- L1 → L2: Incidente não resolvido em 30 min OU impacto em > 1 usuário
- L2 → L3: Indisponibilidade total > 1h OU perda de dados OU decisão de escopo/prazo
- L3 → L4: Impacto na nota final / entrega acadêmica / conformidade institucional

---

## 7. Checklist Pós-Incidente (Obrigatório para Incidentes Críticos)

- [ ] Incidente documentado no RAID Log (I-<NNN>)
- [ ] Causa raiz identificada (5 Porquês)
- [ ] Ação corretiva implementada (fix no código/config)
- [ ] Ação preventiva documentada (evitar recorrência)
- [ ] Post-Mortem Blameless criado (`docs/auditorias/POST-MORTEM-<ID>.md`)
- [ ] Runbook atualizado se procedimento mudou
- [ ] Comunicação para stakeholders (Status Report extraordinário)

---

## 8. Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | DD/MM/AAAA | DevOps | Criação inicial (Deploy, Rollback, Seed, Backup, Incidentes) | Tech Lead |

---

**Fim do Runbook**  
*Versão no Git. Testar procedimentos a cada Sprint Review (Game Day leve).*