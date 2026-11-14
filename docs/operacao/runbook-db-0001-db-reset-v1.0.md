---
id: runbook-db-0001-db-reset-v1.0
type: runbook-db
title: RUNBOOK DB — Db Reset
version: v1.0
status: ratificado
canonical: false
canonical_slug: db-reset
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
# Runbook — Reset e Seed do Banco de Dados (COBECO MVP)

**Documento:** Runbook Operacional  
**Versão:** 1.0  
**Status:** Ativo  
**Data:** 27/10/2026  
**Autor:** Nicholas Anthony (DevOps / Tech Lead)  
**Aplica-se a:** dev | homolog | prod  
**Classificação:** Interno

---

## 1. Propósito

Recriar o banco de dados do zero (destrutivo), aplicar migrations e popular com seed determinístico. Usado para: novo ambiente, troubleshooting, testes limpos, demo.

---

## 2. Pré-requisitos

| Item | Verificação |
|------|-------------|
| Docker rodando | `docker ps` |
| `config-env-0001-env-example-v1.0` configurado | `ls config-env-0001-env-example-v1.0` |
| Porta 3306 livre | `lsof -i :3306` |
| Backup recente (se prod) | `ls -la backups/` |

---

## 3. Procedimento

### 3.1 Reset Completo (Destrutivo — Cuidado!)

```bash
# 1. Parar tudo e remover volumes (PERDE DADOS)
make down
# OU: docker compose down -v

# 2. Subir apenas MySQL
docker compose up -d mysql

# 3. Aguardar MySQL ready (max 60s)
for i in {1..30}; do
  if docker exec cobeco-mysql mysqladmin ping -h localhost -u root -proot --silent; then
    echo "MySQL pronto"; break
  fi
  sleep 2
done

# 4. Subir backend para rodar migrations
docker compose up -d backend

# 5. Aguardar backend healthy
sleep 10

# 6. Rodar migrations
docker compose exec backend alembic upgrade head

# 7. Popular seed
docker compose exec backend python scripts/seed.py

# 8. Subir frontend + proxy
docker compose up -d frontend proxy

# 9. Validar
make health
make test
```

### 3.2 Apenas Re-seed (Mantém Schema)

```bash
# Sem derrubar containers
docker compose exec backend python scripts/seed.py
make test
```

### 3.3 Verificar Integridade Pós-Seed

```bash
docker compose exec backend python -c "
from src.infrastrdoc-arch-0006-uc-v1ture.database import SessionLocal
from src.domain.entities import Categoria, Fornecedor, Produto, Preco
db = SessionLocal()
print(f'Categorias: {db.query(Categoria).count()}')
print(f'Fornecedores: {db.query(Fornecedor).count()}')
print(f'Produtos: {db.query(Produto).count()}')
print(f'Preços: {db.query(Preco).count()}')
db.close()
"
# Esperado: 11 cat, 10 forn, 50 prod, ~300 preços
```

---

## 4. Troubleshooting

| Sintoma | Causa | Ação |
|---------|-------|------|
| `alembic upgrade head` falha | Migration conflict | Verificar `alembic history`, corrigir migration, `alembic downgrade -1` |
| Seed > 10s | Insert individual | Verificar se `bulk_save_objects` está sendo usado |
| FK violation no seed | Ordem errada | Categorias → Fornecedores → Produtos → Preços → Usuários → Listas → Itens |
| MySQL não sobe | Porta ocupada / config | `make ports-free`, verificar `config-env-0001-env-example-v1.0` |

---

## 4. Validação de Sdoc-arch-0006-uc-v1esso

- [ ] `alembic upgrade head` sem erros
- [ ] `seed.py` roda < 10s
- [ ] Contagens: 11 cat, 10 forn, 50 prod, ~300 preços
- [ ] `make test` passa
- [ ] `make health` retorna healthy

---

## 5. Rollback (Se Necessário)

```bash
# Downgrade 1 migration
docker compose exec backend alembic downgrade -1

# Ou restore backup (se fez backup antes)
gunzip -c backups/cobeco_YYYYMMDD_HHMMSS.sql.gz | docker exec -i cobeco-mysql mysql -u root -proot cobeco
```

---

## Controle de Versões

| Versão | Data | Autor | Mudança |
|--------|------|-------|---------|
| 1.0 | 27/10/2026 | Nicholas Anthony | Criação inicial |

---

**Fim do Runbook — DB Reset/Seed**  
*Testado em staging (25/10/2026). Executar apenas com aprovação.*