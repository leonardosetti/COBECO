# User Story — doc-user-story-015-us-015

**Título:** Calcular Orçamento (Motor de Comparação)  
**ID Único:** doc-user-story-015-us-015  
**Status:** Done  
**Sprint:** S3 | **Milestone:** S3: Pré-filtro e Comparação  
**Prioridade:** P0  
**Story Points:** 8  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 13/10/2026  
**Rastreabilidade:** RF15, UC06, spec-004

---

## 1. História

Como **usuário com lista e fornecedores selecionados**,  
eu quero **calcular o orçamento comparado recebendo tabela flat (disponíveis, ausentes, preço total por fornecedor)**,  
para **saber exatamente quanto vou gastar em cada fornecedor e qual a melhor opção**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: Calcular orçamento com sdoc-arch-0006-uc-v1esso
```gherkin
Dado que sou usuário (autenticado ou visitante) com lista de itens (ex: Arroz 2, Feijão 1, Óleo 1)
E selecionei fornecedores "Supermercado A" (ID 1) e "Atacadão B" (ID 2)
Quando faço POST /v1/orcamento com {
  "itens": [{"produto_id": 1, "quantidade": 2}, {"produto_id": 2, "quantidade": 1}, {"produto_id": 5, "quantidade": 1}],
  "fornecedor_ids": [1, 2]
}
Então o sistema retorna 200 com JSON:
{
  "fornecedores": [
    {
      "fornecedor_id": 1,
      "nome": "Supermercado A",
      "itens_disponiveis": [
        {"produto_id": 1, "nome": "Arroz", "quantidade": 2, "preco_unit": 25.90, "subtotal": 51.80},
        {"produto_id": 2, "nome": "Feijão", "quantidade": 1, "preco_unit": 8.50, "subtotal": 8.50},
        {"produto_id": 5, "nome": "Óleo", "quantidade": 1, "preco_unit": 12.90, "subtotal": 12.90}
      ],
      "itens_ausentes": [],
      "total": 73.20
    },
    {
      "fornecedor_id": 2,
      "nome": "Atacadão B",
      "itens_disponiveis": [
        {"produto_id": 1, "nome": "Arroz", "quantidade": 2, "preco_unit": 23.50, "subtotal": 47.00},
        {"produto_id": 2, "nome": "Feijão", "quantidade": 1, "preco_unit": 7.90, "subtotal": 7.90}
      ],
      "itens_ausentes": [
        {"produto_id": 5, "nome": "Óleo", "quantidade": 1}
      ],
      "total": 54.90
    }
  ],
  "melhor_fornecedor_id": 2,
  "economia_vs_pior": 18.30
}
E resposta vem em < 10s (timeout)
E usa cache de 5min para mesma lista+fornecedores
```

### Cenário 2: Cache 5min — segunda chamada igual retorna cache
```gherkin
Dado que fiz chamada idêntica há 3 minutos
Quando repito POST /v1/orcamento com mesmo payload
Então retorna resposta do cache (header X-Cache: HIT)
E tempo resposta < 100ms
```

### Cenário 3: Timeout 10s — fallback
```gherkin
Dado que cálculo demora > 10s (ex: muitos itens/fornecedores)
Quando faço POST /v1/orcamento
Então retorna 504 "Tempo limite excedido. Tente com menos itens ou fornecedores."
E loga warning no backend
```

### Cenário 4: Fornecedor sem preço para item → item_ausente
```gherkin
Dado que "Atacadão B" não tem preço para "Óleo"
Quando calculo orçamento
Então "Óleo" aparece em `itens_ausentes` do Atacadão B
E `total` do Atacadão B soma apenas itens disponíveis
```

### Cenário 5: Validação — lista vazia ou fornecedores < 2
```gherkin
Dado que envio itens=[] ou fornecedor_ids=[1]
Quando POST /v1/orcamento
Então retorna 400 "Lista de itens não pode ser vazia" ou "Mínimo 2 fornecedores"
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | POST /v1/orcamento → tabela flat por fornecedor (disponíveis, ausentes, total) | Funcional | Sim | `test_calcular_orcamento_sdoc-arch-0006-uc-v1esso.py` | ✅ |
| AC-02 | Cache 5min (X-Cache: HIT/MISS) | Não-funcional | Sim | `test_calcular_orcamento_cache.py` | ✅ |
| AC-03 | Timeout 10s → 504 graceful | Não-funcional | Sim | `test_calcular_orcamento_timeout.py` | ✅ |
| AC-04 | Itens ausentes por fornecedor + total apenas disponíveis | Funcional | Sim | `test_calcular_orcamento_ausentes.py` | ✅ |
| AC-05 | Validação itens vazios / fornecedores < 2 | Funcional | Sim | `test_calcular_orcamento_validacao.py` | ✅ |
| AC-06 | Identifica melhor_fornecedor_id (menor total) + economia | Funcional | Sim | `test_calcular_orcamento_melhor.py` | ✅ |
| AC-07 | Frontend: Loading skeleton, erro 504/400, sdoc-arch-0006-uc-v1esso → navega resultados | Frontend | Sim (E2E) | `test_calcular_orcamento_frontend.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-140 | Backend: POST /v1/orcamento — query otimizada (JOIN produtos, preços, fornecedores), cache Redis/memória 5min | Backend | 6 | Nicholas | ✅ | `feat/UC-06-calcular-orcamento` |
| TA-141 | Backend: Timeout 10s (asyncio.wait_for), cache key = hash(payload), invalidação se preços mudam | Backend | 3 | Nicholas | ✅ | `feat/UC-06-calcular-orcamento` |
| TA-142 | Backend: Lógica flat table — agrupa por fornecedor, separa disponíveis/ausentes, calcula totais, encontra menor | Backend | 4 | Nicholas | ✅ | `feat/UC-06-calcular-orcamento` |
| TA-143 | Testes: sdoc-arch-0006-uc-v1esso, cache, timeout, ausentes, validações, concorrência, performance | Backend | 3 | Nicolas | ✅ | `feat/UC-06-calcular-orcamento` |
| TA-144 | Frontend: Página "Calculando..." com skeleton, polling/websockets? Não — POST síncrono com loading, depois redirect resultados | Frontend | 3 | Eduardo | ✅ | `feat/UC-06-calcular-orcamento` |

---

## 5. DoD

- [x] Query otimizada (single query com JOINs ou CTE) — < 500ms sem cache
- [x] Cache 5min em memória (dict + TTL) — chave = hash SHA256(payload)
- [x] Timeout 10s hard (asyncio.wait_for)
- [x] Response flat: fornecedores[] com itens_disponiveis[], itens_ausentes[], total
- [x] `melhor_fornecedor_id` = menor total (desconsidera ausentes? Não — total só disponíveis)
- [x] `economia_vs_pior` = pior_total - melhor_total
- [x] Testes ≥80%, Code review, CI, CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF15 |
| req-use-case-0001-casos-de-uso-canon.md | UC06 |
| spec-004 | Spec ID |
| Branch | `feat/UC-06-calcular-orcamento` |

---

## 7. Notas

- **Cache Invalidação:** Se qualquer preço dos produtos/fornecedores envolvidos mudar, invalida cache (evento `preco_atualizado` → limpa chaves relacionadas).
- **Timeout:** `asyncio.wait_for(calcular(), timeout=10.0)` — cancela task se exceder.
- **Melhor Fornecedor:** Menor `total` (soma apenas itens_disponiveis). Itens ausentes não contam no total mas são informados.
- **Frontend:** POST síncrono com loading spinner. Se 504, mostra erro + botão "Tentar novamente". Se sdoc-arch-0006-uc-v1esso, `window.location.href = '/resultado?orcamento_id=...'` (ou passa via state).

---

**Fim doc-user-story-015-us-015**