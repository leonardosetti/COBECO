# User Story — doc-user-story-016-us-016

**Título:** Visualizar Resultados da Comparação  
**ID Único:** doc-user-story-016-us-016  
**Status:** Done  
**Sprint:** S3 | **Milestone:** S3: Pré-filtro e Comparação  
**Prioridade:** P0  
**Story Points:** 5  
**Autor:** Leonardo Setti (PO)  
**Data Criação:** 15/09/2026  
**Data Atualização:** 13/10/2026  
**Rastreabilidade:** RF16, UC07, spec-008

---

## 1. História

Como **usuário que calculou o orçamento**,  
eu quero **visualizar a tabela de resultados ordenada por preço total ASC com highlight verde na melhor oferta**,  
para **decidir rapidamente onde comprar e ver itens faltantes**.

---

## 2. Critérios de Aceite — Gherkin

### Cenário 1: Tabela ordenada por total ASC + highlight verde
```gherkin
Dado que calculei orçamento com 3 fornecedores: A (R$ 100), B (R$ 85), C (R$ 95)
Quando acesso a página de resultados
Então exibe tabela com colunas: Fornecedor, Itens Disponíveis (count), Itens Ausentes (count), Total
E ordenada por Total ASC: B (85) → C (95) → A (100)
E linha do melhor (B) tem classe `bg-green-50` / `border-green-300` (highlight verde)
E badge "Melhor Preço" na linha do melhor
```

### Cenário 2: Detalhar itens de um fornecedor (expansível)
```gherkin
Dado que estou na tabela de resultados
Quando clico na seta/expandir do fornecedor "Supermercado A"
Então mostra sub-tabela com itens: Produto, Qtd, Preço Unit, Subtotal
E itens ausentes em seção separada com badge "N/D" (Não Disponível) vermelho
```

### Cenário 3: Tooltip para itens ausentes
```gherkin
Dado que fornecedor tem itens ausentes
Quando passo mouse sobre badge "N/D" ou contador "2 ausentes"
Então tooltip mostra: "Itens não disponíveis: Óleo 500ml, Sal 1kg"
```

### Cenário 4: Botão "Exportar PDF" e "Imprimir"
```gherkin
Dado que estou nos resultados
Quando clico "Exportar PDF"
Então chama POST /v1/export/pdf (doc-user-story-017-us-017) e faz download `lista_20261015.pdf`
Quando clico "Imprimir"
Então abre `window.print()` — CSS @media print otimizado (doc-user-story-020-us-020)
```

### Cenário 5: Voltar para ajustar seleções
```gherkin
Dado que quero mudar fornecedores
Quando clico "Voltar ao Pré-filtro"
Então navega para tela de Categorias (doc-user-story-012-us-012) mantendo estado anterior
```

---

## 3. Critérios — Tabela

| # | Critério | Tipo | Auto? | Teste | Status |
|---|----------|------|-------|-------|--------|
| AC-01 | Tabela ordenada Total ASC + highlight verde linha melhor | Funcional | Sim | `test_resultados_ordenacao_highlight.py` | ✅ |
| AC-02 | Expansível: itens disponíveis + ausentes (N/D) | Funcional | Sim | `test_resultados_expansivel.py` | ✅ |
| AC-03 | Tooltip itens ausentes | Funcional | Sim | `test_resultados_tooltip.py` | ✅ |
| AC-04 | Botões Exportar PDF + Imprimir funcionais | Funcional | Sim (E2E) | `test_resultados_botoes.py` | ✅ |
| AC-05 | Botão Voltar mantém estado pré-filtro | Funcional | Sim | `test_resultados_voltar.py` | ✅ |
| AC-06 | Frontend: Tabela responsiva, acessível, loading skeleton | Frontend | Sim (E2E) | `test_resultados_frontend.py` | ✅ |

---

## 4. Tarefas Técnicas

| Task ID | Descrição | Camada | Est. | Resp. | Status | Branch |
|---------|-----------|--------|------|-------|--------|--------|
| TA-150 | Frontend: Componente TabelaResultados — ordenação, highlight verde, linhas expansíveis | Frontend | 5 | Eduardo | ✅ | `feat/UC-07-visualizar-resultados` |
| TA-151 | Frontend: Tooltip itens ausentes (CSS only ou JS simples) | Frontend | 1 | Eduardo | ✅ | `feat/UC-07-visualizar-resultados` |
| TA-152 | Frontend: Botões Exportar PDF (chama doc-user-story-017-us-017) + Imprimir (window.print) + Voltar | Frontend | 2 | Eduardo | ✅ | `feat/UC-07-visualizar-resultados` |
| TA-153 | Testes E2E: fluxo completo calculo → resultados → exportar → imprimir → voltar | Frontend | 2 | Nicolas | ✅ | `feat/UC-07-visualizar-resultados` |

---

## 5. DoD

- [x] Ordenação ASC por total (menor primeiro)
- [x] Highlight verde: `bg-green-50 border-l-4 border-green-500` na linha melhor
- [x] Badge "Melhor Preço" verde
- [x] Linhas expansíveis (accordion) para detalhar itens
- [x] Itens ausentes: badge vermelho "N/D" + tooltip com nomes
- [x] Botões: Exportar PDF, Imprimir, Voltar
- [x] Testes ≥80%, Code review, CI, CCB

---

## 6. Rastreabilidade

| Artefato | ID |
|----------|-----|
| req-func-0001-requisitos-funcionais-canon.md | RF16 |
| req-use-case-0001-casos-de-uso-canon.md | UC07 |
| spec-008 | Spec ID |
| Branch | `feat/UC-07-visualizar-resultados` |

---

## 7. Notas

- **Estado:** Resultado do orçamento passado via `sessionStorage` ou URL state (`/resultado?data=...`).
- **Highlight Verde:** Aplicado apenas na linha do `melhor_fornecedor_id` retornado pelo backend.
- **Acessibilidade:** Tabela com `<th scope="col">`, `aria-sort`, expandíveis com `aria-expanded`.

---

**Fim doc-user-story-016-us-016**