---
id: doc-user-story-020-us-020-v1.0
type: doc-user-story
title: DOC USER STORY — Us 020
version: v1.0
status: ratificado
canonical: false
canonical_slug: us-020
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
domain: strategy
layer: user-story
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
# User Story — doc-user-story-020-us-020

**Título:** Gerenciar Perfil (Editar Email, Nome, Senha)  
**ID Único:** doc-user-story-020-us-020  
**Status:** Done  
**Sprint:** S4 | **Milestone:** S4: Export, Perfil e Polish  
**Prioridade:** P1  
**Story Points:** 3  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 20/10/2026  
**Rastreabilidade:** RF06, UC16, spec-004

---

## 1. História

Como **usuário autenticado**,  
eu quero **alterar meu email, nome e senha (exigindo senha atual)**,  
para **manter meus dados atualizados e seguro**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: Alterar email com sdoc-arch-0006-uc-v1esso
```gherkin
Dado que sou usuário autenticado com email "antigo@email.com"
Quando faço PUT /v1/perfil com {"email": "novo@email.com", "senha_atual": "senha123456"}
E o email "novo@email.com" não está em uso
E a senha_atual confere (bcrypt check)
Então o sistema atualiza email no banco (transação ACID)
E retorna 200 com perfil atualizado {email: "novo@email.com", ...}
E invalida refresh_token atual (força re-login por segurança)
E toast "Perfil atualizado. Faça login novamente."
```

### Cenário 2: Alterar nome com sdoc-arch-0006-uc-v1esso
```gherkin
Dado que sou usuário autenticado
Quando faço PUT /v1/perfil com {"nome": "João Silva Santos", "senha_atual": "senha123456"}
Então atualiza nome
E retorna 200 com perfil atualizado
E invalida refresh_token
```

### Cenário 3: Alterar senha com sdoc-arch-0006-uc-v1esso
```gherkin
Dado que sou usuário autenticado
Quando faço PUT /v1/perfil com {"senha_atual": "senha123456", "nova_senha": "novaSenha789", "confirmar_nova_senha": "novaSenha789"}
E senha_atual confere
E nova_senha ≠ senha_atual
E nova_senha ≥ 8 chars
Então faz hash bcrypt(nova_senha, salt=12) e atualiza senha_hash
E retorna 200
E invalida TODOS refresh_tokens do usuário (força re-login em todos dispositivos)
E toast "Senha alterada. Faça login novamente."
```

### Cenário 4: Senha atual incorreta → 401
```gherkin
Dado que tento alterar email com senha_atual errada
Quando envio PUT /v1/perfil com senha_atual="errada"
Então retorna 401 "Senha atual incorreta"
E NÃO altera nada
```

### Cenário 5: Novo email já em uso → 409
```gherkin
Dado que "outro@email.com" já pertence a outro usuário
Quando tento alterar meu email para "outro@email.com"
Então retorna 409 "Email já cadastrado"
```

### Cenário 6: Nova senha = senha atual → 400
```gherkin
Dado que tento alterar senha para a mesma atual
Quando nova_senha === senha_atual
Então retorna 400 "Nova senha deve ser diferente da atual"
```

### Cenário 7: Transação ACID — atualização simultânea
```gherkin
Dado que duas requisições PUT /v1/perfil chegam simultaneamente (ex: alterar email + alterar nome)
Quando processam
Então uma transação COMMIT, outra ROLLBACK com retry ou 409 "Conflito de atualização. Tente novamente."
E estado final consistente
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | PUT /v1/perfil — email, nome, senha (com senha_atual) | Funcional | Sim | `test_gerenciar_perfil_email.py`, `test_gerenciar_perfil_nome.py`, `test_gerenciar_perfil_senha.py` | ✅ |
| AC-02 | Validação senha_atual (bcrypt) obrigatória | Segurança | Sim | `test_gerenciar_perfil_senha_atual_errada.py` | ✅ |
| AC-03 | Email único → 409 se duplicado | Funcional | Sim | `test_gerenciar_perfil_email_duplicado.py` | ✅ |
| AC-04 | Nova senha ≠ atual, ≥ 8 chars, bcrypt salt=12 | Funcional | Sim | `test_gerenciar_perfil_nova_senha_validacao.py` | ✅ |
| AC-05 | Invalida refresh_token (email/nome) ou TODOS (senha) | Segurança | Sim | `test_gerenciar_perfil_invalida_refresh.py` | ✅ |
| AC-06 | Transação ACID — concorrência | Não-funcional | Sim | `test_gerenciar_perfil_concorrencia.py` | ✅ |
| AC-07 | Frontend: Formulário 3 abas (Email, Nome, Senha), validação client, loading, toast | Frontend | Sim (E2E) | `test_gerenciar_perfil_frontend.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-190 | Backend: PUT /v1/perfil — valida senha_atual, campos opcionais (email, nome, nova_senha), transação ACID | Backend | 4 | Fabrício | ✅ | `feat/UC-16-gerenciar-perfil` |
| TA-191 | Backend: Invalidação refresh: email/nome → invalida token atual; senha → invalida TODOS tokens do user | Backend | 2 | Fabrício | ✅ | `feat/UC-16-gerenciar-perfil` |
| TA-192 | Backend: Concorrência — optimistic lock via `atualizado_em` ou `version` column | Backend | 2 | Fabrício | ✅ | `feat/UC-16-gerenciar-perfil` |
| TA-193 | Testes: email, nome, senha, validações, invalidação refresh, concorrência | Backend | 2 | Nicolas | ✅ | `feat/UC-16-gerenciar-perfil` |
| TA-194 | Frontend: Página Editar Perfil — 3 seções (Email, Nome, Senha), cada uma com senha_atual, validação, toast | Frontend | 4 | Eduardo | ✅ | `feat/UC-16-gerenciar-perfil` |

---

## 5. DoD

- [x] PUT /v1/perfil com senha_atual obrigatória
- [x] Campos: email (unique), nome, senha (bcrypt salt=12, ≠ atual, ≥8)
- [x] Transação ACID (BEGIN/COMMIT/ROLLBACK) + optimistic lock
- [x] Invalidação refresh: parcial (email/nome) ou total (senha)
- [x] 401 senha_atual errada, 409 email duplicado, 400 validações
- [x] Força re-login (limpa access_token memória + redirect login)
- [x] Testes ≥80%, Code review, CI, CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF06 |
| req-use-case-0001-casos-de-uso-canon.md | UC16 |
| spec-004 | Spec ID |
| Branch | `feat/UC-16-gerenciar-perfil` |

---

## 7. Notas

- **Optimistic Lock:** Coluna `version INTEGER DEFAULT 1` em `usuarios`. PUT incrementa e valida `WHERE id = ? AND version = ?`. Se 0 rows affected → 409 "Conflito".
- **Invalidação Refresh:** 
  - Email/Nome: `blacklist.add(current_refresh_token_jti)` — invalida só sessão atual.
  - Senha: `blacklist.add_all(user_refresh_tokens_jti)` — invalida todas sessões (segurança).
- **Frontend:** 3 formulários independentes, cada um com seu `senha_atual`. Validação client-side antes de submit.

---

**Fim doc-user-story-020-us-020**