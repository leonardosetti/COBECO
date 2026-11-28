---
id: runbook-deploy-0001-deploy-v1.0
type: runbook-deploy
title: RUNBOOK DEPLOY — Deploy
version: v1.0
status: ratificado
canonical: false
canonical_slug: deploy
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
# Runbook — Deploy Produção (COBECO MVP)

**Documento:** Runbook / Playbook Operacional  
**Versão:** 1.0  
**Status:** Ativo  
**Data:** 27/10/2026  
**Autor:** Nicholas Anthony (DevOps / Tech Lead)  
**Última revisão:** 27/10/2026  
**Aplica-se a:** prod  
**Classificação:** Interno — Senhas/Secrets apenas em `config-env-0001-env-example-v1.0` (nunca no doc)

---

## 1. Propósito e Escopo

| Campo | Valor |
|-------|-------|
| **Operação** | Deploy de nova versão em Produção (tag release) |
| **Frequência** | Por Release (tag `vX.Y.Z`) |
| **Tempo Estimado** | 10 min (rolling update) |
| **Impacto no Usuário** | Zero-downtime (rolling) / Degradação parcial se rollback |
| **Janela de Manutenção** | Fora horário comercial (preferencialmente) |
| **Aprovação Necessária** | Tech Lead + CCB Chair (Gate 3) |

---

## 2. Pré-requisitos e Verificações

| # | Pré-requisito | Comando de Verificação | Critério de Sucesso |
|---|---------------|------------------------|---------------------|
| 1 | Tag release criada e pushed | `git tag -l "v*" | tail -1` | Tag `vX.Y.Z` existe no remote |
| 2 | CI/CD passou (GitHub Actions) | `gh run list --limit 1 --workflow=CI` | Último run: success (verde) |
| 3 | Imagens publicadas no ghcr.io | `docker pull ghcr.io/leonardosetti/cobeco/backend:vX.Y.Z` | Pull bem-sucedido |
| 4 | `config-env-0001-env-example-v1.0.prod` configurado no servidor | `ls -la /opt/cobeco/config-env-0001-env-example-v1.0.prod` | Arquivo existe + secrets preenchidos |
| 5 | Backup DB recente (< 24h) | `ls -la /opt/cobeco/backups/` | Arquivo `.sql.gz` < 24h |
| 6 | Health check endpoint responde | `curl -f https://cobeco.prod/v1/health` | HTTP 200 + JSON `{"status":"healthy"}` |
| 7 | Rollback testado em staging | `make rollback-staging` (simulação) | Rollback < 2 min |

---

## 3. Procedimento de Deploy (Rolling Update)

```bash
# 0. Conectar no servidor de produção
ssh deploy@cobeco.prod
cd /opt/cobeco

# 1. Fazer backup do banco (obrigatório antes de qualquer deploy)
make backup-prod
# Ou manual:
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker exec cobeco-mysql-prod mysqldump -u root -p${MYSQL_ROOT_PASSWORD} cobeco_prod | gzip > backups/cobeco_${TIMESTAMP}.sql.gz

# 2. Atualizar config-env-0001-env-example-v1.0.prod com nova tag (se variável de versão)
# Editar /opt/cobeco/config-env-0001-env-example-v1.0.prod: COBECO_VERSION=vX.Y.Z

# 3. Pull das imagens da nova release
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml pull

# 4. Rolling update - Backend primeiro (stateless)
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml up -d --no-deps backend
# Aguardar health check (máx 30s)
for i in {1..15}; do
  if curl -sf http://localhost:8000/health > /dev/null; then
    echo "Backend healthy"; break
  fi
  sleep 2
done

# 5. Frontend (arquivos estáticos via nginx)
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml up -d --no-deps frontend

# 6. Proxy (nginx) - por último
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml up -d --no-deps proxy

# 7. Validar saúde completa
make health-prod
# Ou manual:
curl -sf https://cobeco.prod/v1/health
curl -sf https://cobeco.prod/ | grep -q "COBECO"

# 8. Smoke test crítico (fluxo principal)
# - Acessar https://cobeco.prod
# - Login com usuário de teste
# - Criar lista → Comparar → Exportar PDF
# - Verificar logs: `docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml logs -f --tail=50`

# 9. Marcar release no GitHub
gh release create vX.Y.Z --notes-file CHANGELOG.md --verify-tag --repo leonardosetti/COBECO
```

---

## 4. Rollback Imediato (Se Falha Crítica)

```bash
# 1. Voltar tag anterior no config-env-0001-env-example-v1.0.prod (ou usar tag anterior diretamente)
# Exemplo: tag anterior era v0.0.9
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml pull --tag v0.0.9

# 2. Rolling update reverso
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml up -d --no-deps backend
# aguardar health check
sleep 10
curl -sf http://localhost:8000/health

docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml up -d --no-deps frontend
docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml up -d --no-deps proxy

# 3. Validar
make health-prod
curl -sf https://cobeco.prod/v1/health
curl -sf https://cobeco.prod/

# 4. Se DB migration foi aplicada e precisa reverter (raro)
# APENAS se migration quebrou compatibilidade:
# docker compose -f config-docker-0001-config-docker-0001-config-docker-0001-config-docker-0002-docker-compose-override-v1-v1-v1.0-v1.0.prod.yml exec backend alembic downgrade -1
# RESTAURAR BACKUP DB (ver seção 5)
```

**Tempo Máximo Rollback:** 5 minutos  
**Critério de Acionamento:** Health check falha > 2 min OU smoke test crítico falha OU erro 500 em > 5% requests

---

## 5. Restore Backup Banco de Dados (MySQL)

```bash
# LISTAR BACKUPS DISPONÍVEIS
ls -la /opt/cobeco/backups/

# RESTORE ESPECÍFICO (DESTRUTIVO — CUIDADO!)
# Exemplo: restore do backup das 14:30
gunzip -c /opt/cobeco/backups/cobeco_20261027_143000.sql.gz | docker exec -i cobeco-mysql-prod mysql -u root -p${MYSQL_ROOT_PASSWORD} cobeco_prod

# VALIDAR RESTORE
docker exec cobeco-mysql-prod mysql -u root -p${MYSQL_ROOT_PASSWORD} cobeco_prod -e "SELECT COUNT(*) FROM usuarios;"
make health-prod
```

**Política:** Backup automático diário às 03:00 via cron. Retenção: 30 dias. Restore testado mensalmente.

---

## 6. Validação Pós-Deploy (Checklist Obrigatório)

| Check | Comando/Verificação | Responsável | Status |
|-------|---------------------|-------------|--------|
| Health Check API | `curl -sf https://cobeco.prod/v1/health` | Deployer | ☐ |
| Health Check Frontend | `curl -sf https://cobeco.prod/ | grep COBECO` | Deployer | ☐ |
| Login Funciona | Acessar /login, credenciais teste | QA | ☐ |
| Criar Lista | Fluxo completo Nova Lista | QA | ☐ |
| Comparar Preços | Pré-filtro → Fornecedores → Calcular | QA | ☐ |
| Exportar PDF | Botão Exportar → download .pdf | QA | ☐ |
| Logs Sem Erros 5xx | `docker compose logs --since=10m | grep -c " 5.. "` | Deployer | ☐ |
| Métricas Prometheus | Verificar dashboards (se houver) | DevOps | ☐ |
| Notificar Stakeholders | Email/Slack "Deploy vX.Y.Z concluído" | PO | ☐ |

---

## 7. Contatos e Escalação

| Nível | Papel | Nome | Contato | SLA |
|-------|-------|------|---------|-----|
| L1 | Deployer de Plantão | Nicholas Anthony | Discord @nathony + Phone | Imediato |
| L2 | Tech Lead | Leonardo Setti | Discord @leosetti + Phone | 15 min |
| L3 | CCB Chair / PO | Leonardo Setti | Discord @leosetti + Phone | 30 min |
| L4 | Orientador (se impacto demo) | [Nome] | Email institucional | 1h |

---

## 8. Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | 27/10/2026 | Nicholas Anthony | Criação inicial (Deploy, Rollback, Backup, Validação) | Tech Lead |

---

**Fim do Runbook — Deploy Produção COBECO MVP**  
*Testado em staging (25/10/2026). Executar apenas com aprovação Gate 3.*