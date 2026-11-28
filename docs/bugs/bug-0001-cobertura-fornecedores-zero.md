# BUG-0001 — Fornecedores exibem 0% de cobertura na tela de seleção (antes do cálculo)

## Metadados

| Campo | Valor |
|-------|-------|
| ID | BUG-0001 |
| Título | Fornecedores exibem 0% de cobertura na tela de seleção antes do cálculo de orçamento |
| Status | **ABERTO** (aguardando teste manual de validação) |
| Prioridade | Alta |
| Severidade | Alta (calculada abaixo) |
| Impacto | Alto (calculado abaixo) |
| Reportado em | 25/11/2026 |
| Reportado por | Agente de desenvolvimento (sessão 20261124_233501) |
| Versão afetada | COBECO MVP v3.2 — frontend/src/app.js |
| Commit fix | `d464fb8` |
| PR | Pendente de criação |

---

## 1. Descrição

Na tela **Passo 3 de 5 · Fornecedores** (seleção de fornecedores para comparação), todos os cards de fornecedor exibem **0% de cobertura da lista** mesmo antes do usuário clicar em "Calcular orçamento". O usuário não consegue saber qual fornecedor cobre mais produtos da sua lista até executar o cálculo, o que quebra o fluxo de decisão prévio à comparação.

O fluxo esperado (UC03/UC04/RF12/RF13/RF14) é: usuário monta a lista → navega para fornecedores → visualiza a cobertura % de cada fornecedor → seleciona 2–10 → clica em Calcular. Com o bug, o passo de visualização prévia da cobertura está inutilizável.

### Comportamento observado
Todos os cards mostram `0% da lista`, independentemente de o fornecedor possuir ou não os produtos da lista em seu catálogo.

### Comportamento esperado
Cada card deve exibir o percentual real de itens da lista disponíveis naquele fornecedor (ex: Carrefour 100%, Extra 100%, Mercado e Informática 50%).

---

## 2. RCA — Root Cause Analysis

### Sintoma
`coberturaDe(fid)` retorna `0` para todo fornecedor na tela de seleção.

### Cadeia causal
1. A função `coberturaDe(fid)` (linha ~405 de `frontend/src/app.js`) lê a cobertura de `state.resultado.rows`.
2. `state.resultado` só é populado por `calcularResultado()`, que é acionado apenas ao clicar em "Calcular orçamento".
3. Antes desse clique, `state.resultado === null`, então `coberturaDe()` retorna `0` para todos.
4. `fornCardsHTML()` chama `coberturaDe(f.id)` para renderizar o badge de cobertura em cada card.
5. Resultado: todos os cards exibem `0% da lista`.

### Código afetado (antes do fix)
```javascript
function coberturaDe(fid) {
  if (state.resultado) {
    const row = state.resultado.rows.find(r => r.fid === fid);
    return row ? row.cobertura : 0;
  }
  return 0;  // ← sempre 0 antes do cálculo
}
```

### Raiz profunda
Não existia um cálculo de cobertura **prévio** ao cálculo do orçamento. O backend já possuía o endpoint individual `GET /v1/catalogo/fornecedores/{id}/disponibilidade`, mas não havia um endpoint **batch (lote)** para calcular a cobertura de todos os fornecedores de uma vez, nem o frontend o consumia na tela de seleção.

### Fix aplicado
1. **Backend** (`backend/src/adapters/api/catalogo.py`): novo endpoint `GET /v1/catalogo/fornecedores/disponibilidade-lote?produtos=...&fornecedores=...` que retorna cobertura de todos os fornecedores para uma lista de produtos.
2. **Frontend** (`frontend/src/app.js`):
   - Novo campo `state.coberturaPorFornecedor` (mapa fid → percentual).
   - Nova função `carregarCoberturaFornecedores()` que consulta o endpoint lote.
   - `fornCardsHTML()` usa `state.coberturaPorFornecedor[f.id] ?? coberturaDe(f.id)`.
   - Navegação para `/fornecedores` carrega a cobertura antes de renderizar (`carregarFornecedores(...).then(() => carregarCoberturaFornecedores().then(() => go('fornecedores')))`).

---

## 3. Cálculo de Severidade e Impacto

### Severidade (S) — escala 1–4

| Critério | Valor | Justificativa |
|----------|-------|---------------|
| S1 — Afeta funcionalidade principal | 4 | Cobertura de fornecedores é o núcleo da comparação (RF12-RF16) |
| S2 — Sem workaround viável | 4 | Usuário não pode avaliar cobertura antes de calcular; só descobre depois |
| S3 — Afeta múltiplos usuários/telas | 3 | Afeta todo visitante que monta uma lista e vai para fornecedores |
| S4 — Dados exibidos incorretos | 4 | Exibe 0% para todos, informação falsa |

**Severidade = (S1 + S2 + S3 + S4) / 4 = (4 + 4 + 3 + 4) / 4 = 3.75 → ALTA**

### Impacto (I) — escala 1–4

| Critério | Valor | Justificativa |
|----------|-------|---------------|
| I1 — Usuários afetados | 4 | 100% dos visitantes que usam o fluxo de comparação |
| I2 — Frequência | 4 | Ocorre em toda navegação para a tela de fornecedores |
| I3 — Perda de funcionalidade | 3 | Não bloqueia o cálculo final, mas impede decisão informada prévia |
| I4 — Imagem/reputação | 2 | Exibição de dado incorreto (0%) gera desconfiança |

**Impacto = (I1 + I2 + I3 + I4) / 4 = (4 + 4 + 3 + 2) / 4 = 3.25 → ALTO**

### Classificação final
| Métrica | Valor | Classificação |
|---------|-------|---------------|
| Severidade | 3.75 | Alta |
| Impacto | 3.25 | Alto |
| Prioridade | Alta | Correção obrigatória antes de homologação |

---

## 4. Rastreabilidade com Requisitos

| Requisito | Título | Relação com o bug |
|-----------|--------|-------------------|
| **RF12** | Selecionar Categorias (Pré-filtro) | A cobertura depende das categorias selecionadas; sem cobertura real, o pré-filtro perde sentido |
| **RF13** | Selecionar Fornecedores | Usuário seleciona fornecedores com base na cobertura; 0% invalida a escolha informada |
| **RF14** | Filtrar por Disponibilidade | Slider 0–100% depende do % real; com 0% fixo, o filtro não tem base correta |
| **RF15** | Calcular Orçamento | O cálculo final continua correto, mas a decisão de *quais* fornecedores incluir fica prejudicada |
| **RF16** | Visualizar Resultados | A destacação de melhor oferta depende da cobertura calculada; sem prévia, o fluxo fica fragmentado |
| **UC03** | Selecionar Fornecedores | Caso de uso diretamente afetado |
| **UC04** | Filtrar por Disponibilidade | Caso de uso diretamente afetado |
| **UC05** | Calcular Orçamento | Fluxo downstream afetado indiretamente |

---

## 5. Evidências e Logs

### Teste E2E — Antes do fix (comportamento defeituoso)
Todos os cards exibiam `0% da lista` (verificado por inspeção de `state.resultado === null` na tela de fornecedores).

### Teste E2E — Após o fix (comportamento correto)
Execução via Playwright/crawler em 25/11/2026 contra `http://localhost:8380`:

```
[log] 8. Total de cards de fornecedores: 5
[log]    Fornecedor: Carrefour | Cobertura: 100% da lista | Selecionado: false | Desabilitado: false
[log]    Fornecedor: Extra | Cobertura: 100% da lista | Selecionado: false | Desabilitado: false
[log]    Fornecedor: Mercado e Informática | Cobertura: 50% da lista | Selecionado: false | Desabilitado: false
[log]    Fornecedor: Mercado Popular | Cobertura: 100% da lista | Selecionado: false | Desabilitado: false
[log]    Fornecedor: Pão de Açúcar | Cobertura: 100% da lista | Selecionado: false | Desabilitado: false
[log] 9. ALGUM FORNECEDOR COM COBERTURA > 0%: true
[log] 12. Total de linhas na comparação: 2
[log]    Carrefour 🏆 Melhor oferta | Cobertura: 100% | Total: R$ 23,00
[log]    Extra  💰 Menor preço | Cobertura: 100% | Total: R$ 23,00
[log] TESTE CONCLUÍDO COM SUCESSO
```

### Validação de API (endpoint lote)
`GET http://localhost:8380/v1/catalogo/fornecedores/disponibilidade-lote?produtos=1,2,3,4,5`
Retorna cobertura real por fornecedor (ex: Carrefour 100%, Extra 80%, Mercado Popular 40%, etc.).

### Banco de dados (perfil semantica aplicado)
- 12 categorias, 14 fornecedores, 60 produtos, 82 preços, 32 relações N:N
- Categoria 9 (Livros) corrigida: vinculada ao Fornecedor Extra (id 2)

---

## 6. Registro dos Fixes

| Item | Valor |
|------|-------|
| Commit fix | `d464fb8` |
| Mensagem do commit | `fix(seed): corrigir cobertura de fornecedores na tela de seleção (RF12-RF16)` |
| Arquivos alterados | `backend/src/adapters/api/catalogo.py`, `frontend/src/app.js` |
| Inserções / Deleções | 68 inserções, 3 deleções |
| PR | Pendente (não criado ainda) |
| Testes executados | E2E Playwright contra porta 8380 — aprovado; `node -c app.js` — sintaxe válida; `pytest backend/tests/unit/test_seed_data.py` — 7 passed |

### Diff resumido
- `catalogo.py`: +60 linhas (novo endpoint `disponibilidade-lote` + schema `FornecedorDisponibilidadeLoteItem`)
- `app.js`: +8 linhas (`state.coberturaPorFornecedor`, `carregarCoberturaFornecedores()`, uso do mapa em `fornCardsHTML()`, carregamento na navegação)

---

## 7. Plano de Teste Manual (bloqueador para fechamento)

O bug permanece **ABERTO** até que um teste manual seja executado:

1. Acessar `http://localhost:8380/` em navegador desktop (≥1024px, RNF04).
2. Clicar "Criar minha lista".
3. Selecionar categoria "Mercado" → Continuar para a lista.
4. Adicionar produtos: Mercado Item 1, Mercado Item 2, Mercado Item 3.
5. Clicar "Comparar preços" → tela de fornecedores.
6. **Verificar:** cada card deve exibir % de cobertura diferente de 0 (ex: Carrefour 100%, Extra 80%).
7. Selecionar 2 fornecedores → clicar "Calcular orçamento".
8. **Verificar:** tela de resultados exibe cobertura correta e melhor oferta destacada.
9. Testar slider de disponibilidade (RF14) — deve filtrar fornecedores com base no % real.

**Critério de aceitação:** nenhum fornecedor exibe 0% quando possui produtos da lista em estoque.

---

## 8. Anexo — Links e Referências

- Repositório: `/lab/FATEC/202602/lab_eng_software/COBECO`
- Sessão de checkpoint: `session/20261124_233501/`
- Protótipo fonte: `doc-prototype-0003-prototype-high-v2-v1.0.html`
- Documento de dados: `doc-arch-0001-camada-de-dados-canon.md`
- Requisitos: `req-func-0001-requisitos-funcionais-canon.md`
- Casos de uso: `req-use-case-0001-casos-de-uso-canon.md`

---

**Status:** ABERTO — aguardando teste manual de validação (seção 7).
**Responsável:** Equipe de desenvolvimento COBECO.
**Última atualização:** 25/11/2026.
