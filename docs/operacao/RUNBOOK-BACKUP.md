# Runbook — Backup e Restore do Banco de Dados (COBECO MVP)

**Documento:** Runbook Operacional  
**Versão:** 1.0  
**Status:** Ativo  
**Data:** 27/10/2026  
**Autor:** Nicholas Anthony (DevOps / Tech Lead)  
**Aplica-se a:** prod | homolog  
**Classificação:** Interno

---

## 1. Propósito

Procedimentos para backup automatizado, manual e restore do banco MySQL. Garante recuperação ante falhas, corrupção, erro humano ou disaster recovery.

---

## 2. Políticas de Backup

| Aspecto | Política |
|---------|----------|
| **Frequência** | Diário às 03:00 UTC (cron) + Antes de todo deploy/migration |
| **Retenção** | 30 dias (diários) + 12 meses (mensais - 1º dia) |
| **Armazenamento** | `/opt/cobeco/backups/` (volume persistente) + S3/Cloud (futuro) |
| **Formato** | `mysqldump` + `gzip` (`.sql.gz`) |
| **Naming** | `cobeco_YYYYMMDD_HHMMSS.sql.gz` |
| **Verificação** | `gunzip -t` + `mysql -e "SHOW TABLES"` no restore teste |
| **Criptografia** | AES-256 (futuro - GPG) |

---

## 3. Backup Automatizado (Cron)

### 3.1 Configuração no Servidor

```bash
# Editar crontab do usuário deploy
crontab -e

# Adicionar linha:
0 3 * * * /opt/cobeco/scripts/backup.sh >> /var/log/cobeco-backup.log 2>&1
```

### 3.2 Script de Backup (`/opt/cobeco/scripts/backup.sh`)

```bash
#!/bin/bash
set -euo pipefail

BACKUP_DIR="/opt/cobeco/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/cobeco_${TIMESTAMP}.sql.gz"
MYSQL_CONTAINER="cobeco-mysql-prod"
MYSQL_USER="root"
MYSQL_PASS="${MYSQL_ROOT_PASSWORD}"
DB_NAME="cobeco_prod"

mkdir -p "${BACKUP_DIR}"

echo "[$(date)] Iniciando backup: ${BACKUP_FILE}"

# Dump + compress
docker exec "${MYSQL_CONTAINER}" mysqldump \
  -u "${MYSQL_USER}" \
  -p"${MYSQL_PASS}" \
  --single-transaction \
  --routines \
  --triggers \
  --events \
  "${DB_NAME}" | gzip > "${BACKUP_FILE}"

# Verificar integridade
if gunzip -t "${BACKUP_FILE}"; then
  echo "[$(date)] Backup OK: ${BACKUP_FILE}"
  # Log tamanho
  ls -lh "${BACKUP_FILE}"
else
  echo "[$(date)] ERRO: Backup corrompido!" >&2
  rm -f "${BACKUP_FILE}"
  exit 1
fi

# Limpeza retenção (mantém 30 dias + 1º dia de cada mês por 12 meses)
find "${BACKUP_DIR}" -name "cobeco_*.sql.gz" -mtime +30 -not -name "cobeco_??????01_*.sql.gz" -delete
find "${BACKUP_DIR}" -name "cobeco_??????01_*.sql.gz" -mtime +365 -delete

echo "[$(date)] Backup concluído. Arquivos mantidos:"
ls -lh "${BACKUP_DIR}"
```

---

## 4. Backup Manual (Antes de Deploy/Migration)

```bash
# Script único
/opt/cobeco/scripts/backup.sh

# Ou manual:
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker exec cobeco-mysql-prod mysqldump -u root -p"${MYSQL_ROOT_PASSWORD}" --single-transaction cobeco_prod | gzip > /opt/cobeco/backups/cobeco_${TIMESTAMP}_pre-deploy.sql.gz

# Verificar
gunzip -t /opt/cobeco/backups/cobeco_${TIMESTAMP}_pre-deploy.sql.gz && echo "OK"
```

---

## 5. Restore (Recuperação)

### 5.1 Restore Completo (Destrutivo)

```bash
# 1. Identificar backup
ls -lh /opt/cobeco/backups/

# 2. Parar aplicação (manter MySQL)
docker compose -f docker-compose.prod.yml stop backend frontend proxy

# 3. Restore
gunzip -c /opt/cobeco/backups/cobeco_20261027_030000.sql.gz | docker exec -i cobeco-mysql-prod mysql -u root -p"${MYSQL_ROOT_PASSWORD}" cobeco_prod

# 4. Subir aplicação
docker compose -f docker-compose.prod.yml up -d backend frontend proxy

# 5. Validar
make health-prod
```

### 5.2 Restore Parcial (Tabela Específica)

```bash
# Extrair tabela do backup
gunzip -c backup.sql.gz | sed -n '/CREATE TABLE `tabela`/,/UNLOCK TABLES/p' > tabela.sql

# Aplicar
docker exec -i cobeco-mysql-prod mysql -u root -p"${MYSQL_ROOT_PASSWORD}" cobeco_prod < tabela.sql
```

### 5.3 Validação Pós-Restore

```bash
# 1. Contagens
docker exec cobeco-mysql-prod mysql -u root -p"${MYSQL_ROOT_PASSWORD}" cobeco_prod -e "
SELECT 'usuarios' t, COUNT(*) c FROM usuarios
UNION SELECT 'listas', COUNT(*) FROM listas
UNION SELECT 'itens_lista', COUNT(*) FROM itens_lista
UNION SELECT 'categorias', COUNT(*) FROM categorias
UNION SELECT 'fornecedores', COUNT(*) FROM fornecedores
UNION SELECT 'produtos', COUNT(*) FROM produtos
UNION SELECT 'precos', COUNT(*) FROM precos;
"

# 2. Health check
make health-prod

# 3. Smoke test crítico
curl -sf https://cobeco.prod/v1/health
curl -sf https://cobeco.prod/ | grep COBECO
```

---

## 6. Testes de Restore (Obrigatórios)

| Frequência | Teste | Responsável | Critério |
|------------|-------|-------------|----------|
| **Mensal** | Restore completo em staging | DevOps | `make health-prod` + smoke test OK |
| **Trimestral** | Restore completo em prod (janela) | DevOps + TL | Downtime < 15 min |
| **Anual** | Disaster Recovery completo (novo servidor) | DevOps + TL | RTO < 4h, RPO < 24h |

**Registro:** Cada teste deve gerar entrada em `/var/log/cobeco-restore-test.log`

---

## 7. Monitoramento e Alertas

| Métrica | Alerta | Ação |
|---------|--------|------|
| Backup falhou | Exit code ≠ 0 | Email/Slack imediato |
| Backup > 30 min | Timeout | Investigar performance |
| Tamanho backup < 10MB | Possível dump vazio | Investigar |
| Restore teste falhou | Qualquer erro | Escalação L2 imediata |

---

## 8. Disaster Recovery (RTO/RPO)

| Métrica | Target | Atual |
|---------|--------|-------|
| **RTO** (Recovery Time Objective) | < 4 horas | ~30 min (testado) |
| **RPO** (Recovery Point Objective) | < 24 horas | 24h (backup diário) |
| **RTO Restore Parcial** | < 30 min | ~10 min |
| **Teste DR Anual** | 1x/ano | Agendado |

---

## Controle de Versões

| Versão | Data | Autor | Mudança |
|--------|------|-------|---------|
| 1.0 | 27/10/2026 | Nicholas Anthony | Criação inicial |

---

**Fim do Runbook — Backup/Restore**  
*Testar restore mensalmente em staging. Documentar cada execução.*