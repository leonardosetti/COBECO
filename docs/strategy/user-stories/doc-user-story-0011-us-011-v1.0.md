---
id: doc-user-story-0011-us-011-v1.0
type: doc-user-story
title: DOC USER STORY — Us 011
version: v1.0
status: ratificado
canonical: false
canonical_slug: us-011
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
# User Story — doc-user-story-0011-us-011

**Título:** Excluir Lista (Soft Delete)  
**ID Único:** doc-user-story-0011-us-011  
**Status:** Done  
**Sprint:** S2 | **Milestone:** S2: Listas e Catálogo  
**Prioridade:** P1  
**Story Points:** 2  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 06/10/2026  
**Rastreabilidade:** RF11, UC13, spec-004

---

## 1. História

Como **usuário autenticado**,  
eu quero **excluir uma lista minha com confirmação digitando o nome**,  
para **remover listas antigas sem risco de exclusão acidental**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: Excluir com confirmação correta
```gherkin
Dado que tenho lista ID 123 com nome "Compras Antiga"
Quando faço DELETE /v1/listas/123 com body {"confirmacao_nome": "Compras Antiga"}
Então o sistema faz soft delete: UPDATE listas SET deletado_em = NOW() WHERE id = 123
E retorna 200 {"message": "Lista excluída com sdoc-arch-0006-uc-v1esso"}
E a lista NÃO aparece mais em GET /v1/listas (filtro deletado_em IS NULL)
E os itens da lista permanecem no banco (FK RESTRICT) mas não são acessíveis via lista
```

### Cenário 2: Confirmação incorreta → 400
```gherkin
Dado que tento excluir lista "Compras Antiga"
Quando envio DELETE /v1/listas/123 com {"confirmacao_nome": "Nome Errado"}
Então retorna 400 "Confirmação incorreta. Digite o nome exato da lista."
E a lista NÃO é excluída
```

### Cenário 3: Lista inexistente/outro usuário → 404
```gherkin
Dado que tento excluir ID 999
Quando faço DELETE /v1/listas/999
Então retorna 404 "Lista não encontrada"
```

### Cenário 4: Frontend — Modal confirmação com input nome
```gherkin
Dado que estou no Dashboard
Quando clico no ícone "Excluir" da lista "Compras Antiga"
Então abre modal "Excluir Lista" com texto "Digite o nome da lista para confirmar:"
E input text + botões "Cancelar" / "Excluir" (desabilitado até nome conferir)
Quando digito "Compras Antiga" corretamente
E clico "Excluir"
Então chama DELETE API, fecha modal, toast "Lista excluída", remove linha da tabela
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | DELETE /v1/listas/{id} + confirmação nome → soft delete (deletado_em) | Funcional | Sim | `test_excluir_lista_sdoc-arch-0006-uc-v1esso.py` | ✅ |
| AC-02 | Confirmação incorreta → 400 mensagem clara | Funcional | Sim | `test_excluir_lista_confirmacao_errada.py` | ✅ |
| AC-03 | Lista inexistente/outro user → 404 | Segurança | Sim | `test_excluir_lista_404.py` | ✅ |
| AC-04 | Soft delete: GET /v1/listas não retorna deletadas | Funcional | Sim | `test_excluir_lista_soft_delete.py` | ✅ |
| AC-05 | Frontend: Modal com input nome, validação tempo real, loading, toast | Frontend | Sim (E2E) | `test_excluir_lista_frontend.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-100 | Backend: DELETE /v1/listas/{id} — valida ownership, body confirmação, soft delete | Backend | 2 | Fabrício | ✅ | `feat/UC-13-editar-excluir-lista` |
| TA-101 | Backend: Query `deletado_em IS NULL` em todos GET /v1/listas (já em doc-user-story-0009-us-009) | Backend | 0 | — | ✅ | — |
| TA-102 | Testes: soft delete, confirmação, ownership, itens permanecem | Backend | 1 | Nicolas | ✅ | `feat/UC-13-editar-excluir-lista` |
| TA-103 | Frontend: Modal Excluir — input nome, validação tempo real (habilita botão), loading, toast | Frontend | 3 | Eduardo | ✅ | `feat/UC-13-editar-excluir-lista` |

---

## 5. DoD

- [x] Soft delete via `deletado_em` timestamp (não hard delete)
- [x] Confirmação digitando nome exato (case-sensitive)
- [x] Ownership check
- [x] Itens preservados (FK RESTRICT em `itens_lista.lista_id`)
- [x] GET /v1/listas filtra `deletado_em IS NULL`
- [x] Testes ≥80%, Code review, CI, CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF11 |
| req-use-case-0001-casos-de-uso-canon.md | UC13 |
| spec-004 | Spec ID |
| Branch | `feat/UC-13-editar-excluir-lista` |

---

## 7. Notas

- **FK RESTRICT:** `itens_lista.lista_id` → `listas.id` ON DELETE RESTRICT. Itens ficam órfãos mas preservados (auditoria).
- **Recuperação Futura:** Admin pode restaurar (`deletado_em = NULL`) se necessário.
- **Frontend:** Validação tempo real — botão "Excluir" só habilita quando `input.value === lista.nome`.

---

**Fim doc-user-story-0011-us-011**