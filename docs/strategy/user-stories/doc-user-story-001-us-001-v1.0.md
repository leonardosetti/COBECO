---
id: doc-user-story-001-us-001-v1.0
type: doc-user-story
title: DOC USER STORY — Us 001
version: v1.0
status: ratificado
canonical: false
canonical_slug: us-001
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
# User Story — doc-user-story-001-us-001

**Título:** Cadastrar Usuário  
**ID Único:** doc-user-story-001-us-001  
**Status:** Done  
**Sprint:** S1 | **Milestone:** S1: Setup, Docs e Auth  
**Prioridade:** P0  
**Story Points:** 5  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 29/09/2026  
**Rastreabilidade:** RF01, UC09, spec-004

---

## 1. História

Como **visitante não autenticado**,  
eu quero **cadastrar-me no sistema informando nome de usuário, email, senha e pergunta de segurança**,  
para **ter uma conta pessoal e acessar todas as funcionalidades (listas persistidas, perfil, histórico)**.

---

## 2. Critérios de Aceite — Formato Gherkin

### Cenário 1: Cadastro bem-sdoc-arch-0006-uc-v1edido com dados válidos
```gherkin
Dado que sou um visitante na página de cadastro
Quando preencho "nome_usuario" único, "email" único, "senha" (mín 8 chars), "confirmar_senha" igual, "pergunta_seguranca" e "resposta"
E clico em "Cadastrar"
Então o sistema cria minha conta
E faz hash da senha com bcrypt (salt=12)
E faz hash da resposta da pergunta de segurança
E me redireciona para a página de login com mensagem "Cadastro realizado com sdoc-arch-0006-uc-v1esso"
E meu usuário fica com "deletado_em" nulo
```

### Cenário 2: Cadastro falha — nome de usuário já existe
```gherkin
Dado que já existe um usuário com "nome_usuario" = "joao123"
Quando tento cadastrar novo usuário com "nome_usuario" = "joao123"
Então o sistema retorna erro 409 "Nome de usuário já cadastrado"
E não cria nova conta
E mantém-me na página de cadastro
```

### Cenário 3: Cadastro falha — email já existe
```gherkin
Dado que já existe um usuário com "email" = "joao@email.com"
Quando tento cadastrar novo usuário com "email" = "joao@email.com"
Então o sistema retorna erro 409 "Email já cadastrado"
E não cria nova conta
```

### Cenário 4: Cadastro falha — senhas não conferem
```gherkin
Dado que estou na página de cadastro
Quando preencho "senha" = "senha123" e "confirmar_senha" = "senha456"
Então o sistema retorna erro 400 "Senhas não conferem"
E não cria conta
```

### Cenário 5: Cadastro falha — senha muito curta
```gherkin
Dado que estou na página de cadastro
Quando preencho "senha" = "123" (menos de 8 chars)
Então o sistema retorna erro 400 "Senha deve ter no mínimo 8 caracteres"
```

---

## 3. Critérios de Aceite — Tabela Resumo

| # | Critério (Resumo) | Tipo | Automatizável? | Teste Relacionado | Status |
|---|-------------------|------|----------------|-------------------|--------|
| AC-01 | Cadastro sdoc-arch-0006-uc-v1esso com dados válidos + bcrypt + hash resposta | Funcional | Sim | `test_cadastrar_usuario_sdoc-arch-0006-uc-v1esso.py` | ✅ |
| AC-02 | Erro 409 nome_usuario duplicado | Funcional | Sim | `test_cadastrar_usuario_duplicado_username.py` | ✅ |
| AC-03 | Erro 409 email duplicado | Funcional | Sim | `test_cadastrar_usuario_duplicado_email.py` | ✅ |
| AC-04 | Erro 400 senhas não conferem | Funcional | Sim | `test_cadastrar_usuario_senhas_nao_conferem.py` | ✅ |
| AC-05 | Erro 400 senha < 8 chars | Funcional | Sim | `test_cadastrar_usuario_senha_curta.py` | ✅ |
| AC-06 | Hash bcrypt salt=12 armazenado | Não-funcional | Sim | `test_cadastrar_usuario_bcrypt_hash.py` | ✅ |
| AC-07 | Hash resposta pergunta segurança armazenado | Não-funcional | Sim | `test_cadastrar_usuario_resposta_hash.py` | ✅ |

---

## 4. Tarefas Técnicas (Tasks)

| Task ID | Descrição Técnica | Camada | Estimativa (h) | Responsável | Status | Branch |
|---------|-------------------|--------|----------------|-------------|--------|--------|
| TA-001 | Criar endpoint POST /v1/usuarios com validação Pydantic (UsuarioCreate) | Backend | 4 | Fabrício | ✅ Done | `feat/UC-09-cadastrar-usuario` |
| TA-002 | Implementar bcrypt hash (passlib) + unicidade nome_usuario/email no DB | Backend | 3 | Fabrício | ✅ Done | `feat/UC-09-cadastrar-usuario` |
| TA-003 | Hash da resposta da pergunta de segurança (bcrypt) | Backend | 2 | Fabrício | ✅ Done | `feat/UC-09-cadastrar-usuario` |
| TA-004 | Testes unitários: sdoc-arch-0006-uc-v1esso, duplicados, validações, bcrypt | Backend | 3 | Nicolas | ✅ Done | `feat/UC-09-cadastrar-usuario` |
| TA-005 | Página Cadastro (Vanilla JS + Tailwind): form, validação client-side, submit fetch | Frontend | 6 | Eduardo | ✅ Done | `feat/UC-09-cadastrar-usuario` |
| TA-006 | Integração Front↔Back: exibir erros 409/400, redirect login sdoc-arch-0006-uc-v1esso | Frontend | 2 | Eduardo | ✅ Done | `feat/UC-09-cadastrar-usuario` |

---

## 5. Definição de Pronto (DoD)

- [x] **Código:** Clean Architecture (4 camadas), sem vazamento de framework para Domain
- [x] **Segurança:** Queries parameterizadas (SQLAlchemy ORM), validação Pydantic, bcrypt salt=12
- [x] **Padronização:** Nomenclatura PT-BR (DB, variáveis, comentários, erros)
- [x] **Testes:** Unitários escritos + cobertura ≥ 80% nos módulos tocados (`pytest --cov`)
- [x] **Contrato:** OpenAPI (`/docs`) atualizado (SDD — spec-004 → handoff → impl)
- [x] **Infra:** Funciona via `docker compose up` sem config manual extra
- [x] **Revisão:** Code review aprovado (rubrica R-01..R-07) + CI verde
- [x] **Governança:** Aprovação humana (CCB) + merge em `main` → kanban "Done"
- [x] **Documentação:** Spec-004 ratificada + Handoff hf-exec-0500 processado

---

## 6. Rastreabilidade Bidirecional

| Direção | Artefato | ID / Localização |
|---------|----------|------------------|
| **Origem (Negócio)** | req-func-0001-requisitos-funcionais-canon.md | RF01 |
| **Origem (Caso de Uso)** | req-use-case-0001-casos-de-uso-canon.md | UC09 |
| **Especificação (SDD)** | `.ai/specs/spec-tech-0001-backend-mvp-v1.0.md` | Spec ID |
| **Handoff (Execução)** | `.ai/handoffs/hf-exec-0500-backend-mvp-v1.0.md` | Handoff ID |
| **Implementação** | Branch Git | `feat/UC-09-cadastrar-usuario` |
| **Testes** | `backend/tests/test_cadastrar_usuario.py` | Test IDs |
| **Deploy** | Release / Tag | v0.1.0 |

---

## 7. Notas Técnicas

- **Unicidade:** Constraints UNIQUE no DB (`nome_usuario`, `email`) + validação Pydantic prévia.
- **bcrypt:** `passlib.hash.bcrypt` com `rounds=12` (configurável via `config-env-0001-env-example-v1.0`).
- **Pergunta Segurança:** Armazenada em texto plano (pergunta) + hash bcrypt (resposta).
- **Campos Obrigatórios:** `nome_usuario`, `email`, `senha`, `pergunta_seguranca`, `resposta_seguranca`.
- **Soft Delete:** Campo `deletado_em` (nullable timestamp) — não usado no cadastro, apenas para exclusão lógica futura.

---

## 8. Controle de Versões da User Story

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | 15/09/2026 | PO | Criação inicial | — |
| 1.1 | 22/09/2026 | PO | Ajuste critérios após refinamento Sprint 1 | Tech Lead |
| 1.2 | 29/09/2026 | PO | Atualização status Done + evidências teste | QA Lead |

---

**Fim da User Story doc-user-story-001-us-001**  
*Arquivo versionado em `docs/strategy/user-stories/doc-user-story-001-us-001-v1.0.md` + Issue #9 no GitHub Projects.*