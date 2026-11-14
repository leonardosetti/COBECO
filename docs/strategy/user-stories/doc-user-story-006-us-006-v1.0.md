# User Story — doc-user-story-006-us-006

**Título:** Autocomplete de Produtos  
**ID Único:** doc-user-story-006-us-006  
**Status:** Done  
**Sprint:** S2 | **Milestone:** S2: Listas e Catálogo  
**Prioridade:** P0  
**Story Points:** 3  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 06/10/2026  
**Rastreabilidade:** RF07, UC02, spec-008

---

## 1. História

Como **usuário criando lista**,  
eu quero **buscar produtos com autocomplete (debounce 300ms, normalização acentos/case-insensitive)**,  
para **encontrar e adicionar itens rapidamente sem digitar nomes completos**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: Busca com resultados
```gherkin
Dado que estou no input de busca de produtos
Quando digito "ar" (mín 2 chars)
E aguardo 300ms (debounce)
Então o sistema faz GET /v1/produtos/busca?q=ar&limit=10
E exibe dropdown com até 10 sugestões: "Arroz tipo 1 5kg", "Arroz integral 1kg", "Azeite extra virgem 500ml"
E cada sugestão mostra: nome, categoria, unidade
```

### Cenário 2: Normalização acentos e case
```gherkin
Dado que digito "CAFÉ" (maiúsculo, com acento)
Quando debounce 300ms
Então busca normalizado para "cafe" e retorna "Café torrado 500g", "Café solúvel 200g"
```

### Cenário 3: Seleção de sugestão
```gherkin
Dado que dropdown de sugestões está aberto
Quando clico em "Arroz tipo 1 5kg"
Então o input é preenchido com o nome do produto
E o ID do produto é armazenado para adição à lista
E dropdown fecha
```

### Cenário 4: Sem resultados
```gherkin
Dado que digito "xyzqwe" (termo sem match)
Quando debounce
Então dropdown mostra "Nenhum produto encontrado"
E não permite adicionar à lista
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | Debounce 300ms, mín 2 chars, limit 10 | Funcional | Sim | `test_autocomplete_debounce.py` | ✅ |
| AC-02 | Normalização acentos (NFD) + case-insensitive | Funcional | Sim | `test_autocomplete_normalizacao.py` | ✅ |
| AC-03 | Seleção preenche input + armazena produto_id | Funcional | Sim | `test_autocomplete_selecao.py` | ✅ |
| AC-04 | Sem resultados → mensagem amigável | Funcional | Sim | `test_autocomplete_vazio.py` | ✅ |
| AC-05 | Endpoint backend: GET /v1/produtos/busca?q=&limit= | Backend | Sim | `test_busca_produtos.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-050 | Backend: GET /v1/produtos/busca?q=&limit=10 — ILIKE normalizado, índice trigram | Backend | 3 | Nicholas | ✅ | `feat/UC-02-autocomplete` |
| TA-051 | Frontend: Componente Autocomplete reutilizável (debounce, fetch, dropdown, seleção) | Frontend | 4 | Eduardo | ✅ | `feat/UC-02-autocomplete` |
| TA-052 | Integração: doc-user-story-005-us-005 usa componente Autocomplete | Frontend | 1 | Eduardo | ✅ | `feat/UC-01-lista-memoria` |
| TA-053 | Testes: backend busca + frontend componente + integração | Ambos | 2 | Nicolas | ✅ | `feat/UC-02-autocomplete` |

---

## 5. DoD

- [x] Backend: query parameterizada, ILIKE com normalização, índice pg_trgm (ou LIKE otimizado MySQL)
- [x] Frontend: componente reutilizável, debounce 300ms, acessível (teclado)
- [x] Normalização idêntica client/server
- [x] Testes unit + integração ≥80%
- [x] Code review + CI + CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF07 |
| req-use-case-0001-casos-de-uso-canon.md | UC02 |
| spec-008 | Spec ID |
| Branch | `feat/UC-02-autocomplete` |

---

## 7. Notas

- **MySQL Normalização:** `WHERE normalizar(nome) LIKE normalizar(?)` — function `normalizar(str)` remove acentos + lower.
- **Índice:** `CREATE INDEX idx_produtos_nome_norm ON produtos (normalizar(nome))` — ou trigram se PostgreSQL.
- **Compartilhado:** Componente usado em doc-user-story-005-us-005 (Nova Lista) e doc-user-story-010-us-010 (Editar Lista).

---

**Fim doc-user-story-006-us-006**