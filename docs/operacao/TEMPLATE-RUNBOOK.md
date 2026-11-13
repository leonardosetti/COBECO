# Runbook — <Nome da Operação / Incidente>

**Documento:** Runbook / Playbook  
**Versão:** 1.0  
**Status:** Ativo | Arquivado  
**Data:** DD/MM/AAAA  
**Autor:** <Nome>  
**Última revisão:** DD/MM/AAAA  
**Aplica-se a:** <ambiente (dev / homolog / prod)>

---

## 1. Propósito

O que este runbook cobre e quando deve ser usado.

---

## 2. Pré-requisitos

| Pré-requisito | Como verificar |
|---|---|
| Docker rodando | `docker ps` |
| `.env` configurado | `ls .env` |
| Banco saudável | `make health` |

---

## 3. Procedimento passo a passo

### 3.1. Iniciar ambiente (desenvolvimento)

```bash
cp .env.example .env   # preencher SECRET_KEY
make up
make health
```

### 3.2. Recriar banco de dados

```bash
make db-reset
make seed
```

### 3.3. Executar testes

```bash
make test          # testes unitários
make test-cov      # cobertura ≥ 80%
make ci            # pipeline local completo
```

### 3.4. Executar migrações

```bash
make migrate
make migrate-create MSG="descricao"
```

### 3.5. Verificar saúde

```bash
make health
```

---

## 4. Resposta a incidentes

| Sintoma | Causa provável | Ação |
|---|---|---|
| Backend não responde | Container parado | `docker compose up -d backend` |
| Banco não conecta | MySQL não saudável | Ver `make logs-db` |
| CI falha (coverage < 80%) | Testes faltando | Adicionar testes e re-run |

---

## 5. Segurança

- Nunca commitar `.env` (já no `.gitignore`)
- Token de recuperação só em stdout (modo `log`)
- Erros não expõem traceback de usuário

---

## 6. Contatos e escalonamento

| Papel | Nome | Contato |
|---|---|---|
| CCB Chair |  |  |
| Tech Lead |  |  |
| DevOps / Infra |  |  |

---

**Fim do Runbook**
