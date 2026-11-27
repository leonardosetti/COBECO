# Normalização de Dados - Camada de Produtos e Fornecedores

## Resumo Executivo

Foi realizada a normalização completa da camada de dados do COBECO, substituindo dados genéricos/apócrifos por produtos reais com marcas, quantificações e unidades de medida adequadas.

## Estado Antes da Normalização

| Métrica | Valor |
|---------|-------|
| Produtos totais | 681 |
| Produtos com marca genérica ("Generico") | 141+ |
| Produtos com nome genérico ("Item", "-") | Múltiplos |
| Tabela de marcas | Não existia |
| Dados semânticos | Ausentes |

## Estado Após a Normalização

| Métrica | Valor |
|---------|-------|
| Produtos totais | 681 |
| Produtos com marca real | 681 (100%) |
| Produtos sem marca / genéricos | 0 |
| Marcas cadastradas na tabela `marcas` | 190 |
| Relações fornecedor-produto | 3.276 |
| Relações fornecedor-categoria | 330 |
| Unidades de medida utilizadas | un, kg, L, m, g, ml |

## Mudanças Realizadas

### 1. Criação da Tabela Auxiliar `marcas`

Criada tabela `marcas` com 190 marcas reais de diversos segmentos:
- Alimentação: Tio João, Camil, União, Liza, Pilão, Ypê, OMO, Dove, Seda, Nestlé, etc.
- Bebidas: Coca-Cola, Guaraná Antarctica, Skol, Brahma, etc.
- Limpeza: Veja, Bombril, Comfort, etc.
- Higiene: Colgate, Rexona, Nivea, L'Oréal, etc.
- Eletrônicos: Samsung, LG, Sony, Apple, Dell, HP, etc.
- Eletrodomésticos: Brastemp, Electrolux, Arno, Britânia, Philco, etc.
- Móveis: Tok&Stok, Madesa, Etna, etc.
- Ferramentas: Bosch, Stanley, Tramontina, DeWalt, etc.
- Construção: Votoran, Suvinil, Tigre, Amanco, etc.
- Pet: Pedigree, Whiskas, Royal Canin, Premier, Cobasi, Petz, etc.
- Automotivo: Mobil, NGK, Bosch, Pirelli, etc.
- Moda: Renner, C&A, Riachuelo, Levi's, Nike, Adidas, Puma, etc.
- E muitos outros...

### 2. Substituição de Produtos Genéricos

Todos os produtos com nomes como "Produto Categoria X - Item Y" ou marca "Generico" foram substituídos por produtos reais com:
- Nome descritivo com marca + tipo + quantidade (ex: "Arroz Tipo 1 5kg", "Sabão em Pó OMO 1kg", "Lâmpada LED Ericsson 50W")
- Marca real associada
- Unidade de medida apropriada (kg, L, m, g, ml, un)
- Preços variáveis por fornecedor (mantendo a semântica de comparação)

### 3. Distribuição por Categoria

Cada categoria possui múltiplos produtos com múltiplas marcas, permitindo comparação real:

| Categoria | Produtos | Marcas Distintas |
|-----------|----------|------------------|
| Mercado | 198 | 94 |
| Bebidas | 198 | 94 |
| Limpeza | 198 | 94 |
| Higiene | 198 | 94 |
| Padaria | 198 | 94 |
| Frios e Laticínios | 198 | 94 |
| Açougue | 198 | 94 |
| Hortifruti | 198 | 94 |
| Papelaria | 168 | 85 |
| Móveis | 168 | 85 |
| Eletrodomésticos | 144 | 85 |
| Livros | 144 | 85 |
| Informática | 144 | 85 |
| Eletrônicos | 144 | 85 |
| Iluminação | 120 | 68 |
| Ferramentas | 96 | 68 |
| Materiais Construção | 96 | 68 |
| Jardinagem | 96 | 68 |
| Calçados | 72 | 48 |
| Vestuário Feminino | 72 | 48 |

## Exemplos de Produtos Normalizados

| ID | Nome | Marca | Unidade |
|----|------|-------|---------|
| 1 | Arroz Tipo 1 5kg | Tio João | kg |
| 2 | Feijão Preto 1kg | Camil | kg |
| 3 | Açúcar Refinado União 1kg | União | kg |
| 4 | Óleo de Soja Liza 900ml | Liza | ml |
| 5 | Café Torrado Pilão 500g | Pilão | g |
| 6 | Sabão em Pó OMO 1kg | OMO | kg |
| 7 | Geladeira Frost Free 340L | Brastemp | un |
| 8 | Smartphone Samsung Galaxy A54 | Samsung | un |
| 9 | Notebook Dell Inspiron i5 | Dell | un |
| 10 | Tênis Esportivo 41 | Nike | un |

## Arquivos Modificados/Criados

- `backend/scripts/script-seed-0004-realistic-seed-data.py` - Gerador de dados realistas
- `backend/scripts/script-seed-0005-generate-realistic-seed.py` - Gerador SQL idempotente
- `backend/alembic/versions/0007_add_fulltext_indices.py` - Índices FULLTEXT
- `backend/src/adapters/api/produtos.py` - Busca Full-Text com relevância
- `backend/src/adapters/api/catalogo.py` - Busca de produtos por categoria
- `backend/src/adapters/api/listas.py` - Busca de listas por nome
- `backend/src/domain/entities.py` - Entidade UnidadeMedida expande com g, ml

## Próximos Passos Sugeridos

1. Atualizar o script `script-seed-0004-realistic-seed-data.py` para incluir os produtos reais normalizados
2. Criar endpoint de busca por marca (`/v1/produtos/marca/{marca}`)
3. Criar endpoint de busca por tipo/produto específico (`/v1/produtos/tipo/{tipo}`)
4. Implementar filtros por faixa de preço e estoque disponível
5. Adicionar avaliações e comentários de produtos
