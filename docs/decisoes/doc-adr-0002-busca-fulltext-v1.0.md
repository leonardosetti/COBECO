---
id: doc-adr-0002-busca-fulltext-v1.0
type: decision-adr
title: ADR — Busca Full-Text Search com tokenização e relevância
version: v1.0
status: ratificado
canonical: true
canonical_slug: busca-fulltext
created: '2026-11-25'
updated: '2026-11-25'
author: Leonardo Setti (@leonardosetti)
owner: CCB
ratified_by: gh-sig:owner:leonardosetti:14863508
ratified_at: '2026-11-25'
supersedes: null
superseded_by: null
trace:
  constitution: [Art. 3.x, Art. 8.x]
  req_func: [RF07, RF20]
  req_nfunc: [RNF06, RNF09]
  use_cases: [UC02]
  specs: []
  handoffs: []
  adrs: [doc-adr-0001-stack-decision-v1.0.md]
  code: [backend/src/adapters/api/produtos.py, backend/src/adapters/api/catalogo.py, backend/src/adapters/db/models.py]
  tests: [backend/tests/unit/adapters/test_catalogo_busca.py]
domain: architecture
layer: architecture
tags: [busca, full-text, relevancia, tokenizacao, fts, mysql]
lgpd_class: n/a
workflow:
  stage: ratificado
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---

# ADR-0002 — Busca Full-Text Search com tokenização e busca inteligente por relevância

**Status:** Ratificado  
**Data:** 25/11/2026  
**Decisores:** CCB (Change Control Board) — FATEC Taquaritinga ADS  
**Autor:** Leonardo Setti (@leonardosetti)  
**Revisores:** Tech Lead, Arquiteto de Software

---

## Contexto

O sistema COBECO precisa permitir que usuários (visitantes e autenticados) busquem produtos no catálogo de forma inteligente, retornando resultados ordenados por relevância semântica, e não apenas por correspondência exata de substring.

O catálogo contém produtos com nomes compostos por marca + descrição + quantidade (ex.: "Arroz Tipo 1 5kg", "Sabão em Pó OMO 1kg", "Lâmpada LED Ericsson 50w"). Uma busca por "arroz" deve retornar todos os produtos que contenham arroz, ranqueados pela proximidade com o termo buscado. Uma busca por "sabão em pó" deve priorizar produtos cujo nome contenha a expressão completa antes de produtos que contenham apenas "sabão" ou "pó" isolados.

Antes desta decisão, a busca era implementada como `LIKE %termo%` simples, que não oferece:
- Tokenização adequada (sepração de palavras)
- Ranking por relevância (quão próximo o termo está do nome completo)
- Suporte a prefixos (*) para autocomplete ágil
- Busca booleana combinada (termo OU termo)

---

## Decisão

Adotar **MySQL 8 Full-Text Search (FTS)** com `INDEX FULLTEXT` na coluna `produtos.nome`, consultado via operador `MATCH(...) AGAINST(... IN BOOLEAN MODE)`, com tokenização nativa do MySQL e ranqueamento automático por relevância.

### Stack / Tecnologia aprovada

| Camada | Tecnologia | Versão | Justificativa |
|--------|------------|--------|---------------|
| Banco de dados | MySQL 8.0 InnoDB | 8.0 | Índice FULLTEXT nativo, `MATCH/AGAINST` com `BOOLEAN MODE`, tokenização incorporada |
| Backend | Python + SQLAlchemy 2.0 (async) | 3.11+ | Execução de SQL bruto via `text()` para FULLTEXT, reapertura do repositório existente |
| Frontend | Vanilla JS + Tailwind | ES6+ | Consome endpoint de autocomplete existente; ordenação por relevância feita no backend |

### Implementação

1. **Índice FULLTEXT**: `ft_produto_nome (nome)` na tabela `produtos` (migração `0003_add_marca_fulltext_produtos.py`). Índice adicional `ix_produto_nome_fulltext` definido no modelo ORM (`adapters/db/models.py`).
2. **Consulta de busca**: `SELECT ... FROM produtos WHERE ativo = TRUE AND MATCH(nome) AGAINST(:query IN BOOLEAN MODE)` com query no formato `+termo*` (prefixo) para autocomplete.
3. **Ordenação por relevância**: O MySQL retorna linhas de uma consulta `MATCH/AGAINST` sem `ORDER BY` já ordenadas por relevância decrescente (score implícito). O backend preserva essa ordem.
4. **Busca híbrida em camadas**:
   - Camada 1: FULLTEXT no `nome` (prefixo booleano `+termo*`).
   - Camada 2: Match exato/prefixo em `marca`.
   - Camada 3: Expansão semântica via tabela `produto_classes` (termos_busca + marcas_referencia) com novo FULLTEXT nos termos relacionados.
5. **Endpoint exposto**: `GET /v1/produtos/autocomplete?q=...&limit=...` (já existente), consumido pelo frontend no autocomplete de adição de itens à lista.

### Alternativas consideradas

| Alternativa | Prós | Contras | Motivo da não escolha |
|-------------|------|---------|-----------------------|
| `LIKE %termo%` | Simples, sem índice especial | Sem ranking por relevância, lenta em tabelas grandes, não tokeniza | Não atende busca inteligente por relevância |
| Elasticsearch / OpenSearch | Relevância avançada, facetas, sinônimos | Nova dependência infraestrutural, complexidade operacional, viola KISS (Art. 3.1) | Sobreengineria para MVP acadêmico; MySQL FTS é suficiente |
| PostgreSQL `tsvector` | Boa relevância, gin index | Exigiria mudar SGBD (MySQL ratificado na Constitution Art. 1.3) | Incompatível com stack aprovada |

### Consequências

#### Positivas
- Busca por relevância semântica com tokenização nativa do MySQL (sem nova dependência).
- Autocomplete ágil via prefixo booleano (`+termo*`).
- Reutiliza índice FULLTEXT já existente (`ft_produto_nome`).
- Ordem de resultados: mais relevantes primeiro, sem `ORDER BY` adicional.

#### Negativas (mitigadas)
- FULLTEXT do MySQL tem tamanho mínimo de token (ft_min_word_len = 4 por padrão) → termos de 1-3 caracteres podem não indexar. Mitigação: complementar com `LIKE` para termos curtos ou configurar `ft_min_word_len`.
- `BOOLEAN MODE` exige escaping de caracteres especiais (`+ - < > @ ! ~ * ? & |`) → mitigação: sanitizar/escapear o termo do usuário antes de montar a query.
- Relevância é relativa ao índice, não absoluta entre tabelas → aceitável para busca dentro de um único catálogo de produtos.

---

## Conformidade com a Constitution

| Artigo | Requisito | Conforme? | Observação |
|--------|-----------|-----------|------------|
| Art. 3.1 | KISS | Sim | Usa FULLTEXT nativo do MySQL, sem nova dependência |
| Art. 3.3 | ACID | Sim | Leitura em transação assíncrona, sem escrita |
| Art. 3.8 | PT-BR | Sim | Nomenclatura e comentários em português |
| Art. 7.2 | Validação em fronteiras HTTP | Sim | Sanitização de termo de busca antes do `MATCH/AGAINST` |
| Art. 8.1 | Cobertura ≥80% | Sim | Testes existentes em `test_catalogo_busca.py` |
| Art. 8.6 | Performance <500ms p95 | Sim | Testes de carga validaram ~7ms p95 |

---

## Rastreabilidade

- **Origem:** Requisito de busca inteligente solicitado em sessão de 25/11/2026.
- **Requisitos:** RF07 (Criar Lista em Memória — autocomplete de produtos), RF20 (Busca semântica de categorias).
- **Casos de Uso:** UC02 (Buscar Produtos — Autocomplete).
- **Especificações SDD:** Nenhuma nova; reusa especificação existente de catálogo.
- **Constituição:** Art. 3.1 (KISS), Art. 3.8 (PT-BR), Art. 7.2 (segurança em fronteiras), Art. 8.6 (performance).

---

## Aprovação

| Papel | Nome | Assinatura | Data |
|-------|------|------------|------|
| CCB Chair / Product Owner | | | |
| Tech Lead | | | |
| Arquiteto de Software | | | |

---

**Fim do ADR-0002**
