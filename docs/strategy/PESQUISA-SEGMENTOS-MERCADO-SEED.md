# Levantamento de segmentos de mercado para o seed do COBECO

**Documento:** pesquisa de produto e taxonomia de seed
**Versão:** 1.1
**Status:** implementado e validado localmente; aguarda ratificação para promoção do perfil expandido
**Data:** 14/11/2026
**Responsável:** OpenCode
**Rastreabilidade:** RNF08, UC02, UC03, UC04, UC05, UC06, UC23–UC26

## 1. Objetivo

Levantar segmentos de consumo e categorias possíveis para ampliar o mock de fornecedores e
catálogos do COBECO sem alterar o DER v3.2 (8 tabelas) nem substituir o baseline normativo de
11 categorias, 10 fornecedores, 50 produtos e aproximadamente 300 preços.

A pesquisa define duas coisas distintas:

- **segmento de mercado**: conjunto de necessidades de consumo atendidos por categorias afins;
- **categoria de seed**: classificação persistida em `categorias` e vinculada a fornecedores por
  `fornecedores_categorias`.

Segmentos e canais de venda orientam a geração dos mocks, mas não viram novas tabelas. Isso
preserva a normalização e o escopo congelado do MVP.

## 2. Critérios de seleção

1. representa adequadamente bens de consumo comparáveis por preço;
2. possui fornecedores e produtos reconhecíveis no varejo brasileiro;
3. permite catálogo amplo sem introduzir serviços, dados pessoais ou integrações externas;
4. não altera as 8 tabelas canônicas;
5. pode ser gerado de forma determinística e idempotente;
6. cobre casos de busca, filtro, disponibilidade, comparação e ordenação por preço.

## 3. Segmentos e categorias selecionados

| Segmento de mercado | Categorias incluídas no perfil expandido | Arquétipos de fornecedor | Exemplos de produtos |
|---|---|---|---|
| Alimentação e hogar | Mercado; Bebidas; Limpeza e Higiene | supermercado, atacado, mercearia | arroz, óleo, café, detergente, água |
| Moda e acessórios | Vestuário; Calçados e Bolsas; Óculos e Relógios | rede de moda, calçados, joalheria | camiseta, tênis, mochila, relógio |
| Casa e construção | Decoração; Móveis; Eletrodomésticos; Materiais de Construção e Ferragens; Ferramentas; Jardinagem | mobiliário, loja de materiais, ferramenta, jardinagem | sofá, geladeira, cimento, martelo, irrigador |
| Tecnologia e comunicação | Informática; Celulares e Telecomunicações; Games e Acessórios | informática, telecom, games | notebook, smartphone, console, headset |
| Mobilidade | Automotivos; Bicicletas e Mobilidade | autopeças, oficina, ciclo e acessórios | filtro, óleo, pneu, bicicleta, capacete |
| Saúde e bem-estar | Farmácia e Saúde; Beleza e Cuidados Pessoais | farmácia, drogaria, cosméticos | frasco, medicamento, protetor, shampoo |
| Cultura e entretenimento | Livros | livraria, papelaria cultural, distribuidora | romance, técnico, infantil, didático |
| Esporte e lazer | Esportes e Lazer; Camping e Outdoor | loja esportiva, camping, ciclismo | tênis, mochila, tenda, garrafa térmica |
| Escritório e estudo | Papelaria e Escritório | papelaria, gráfico, escritório | caneta, pasta, papel, calculadora |
| Infância, pet e consumo operacional | Brinquedos e Infantil; Pet; Embalagens e Descartáveis | loja infantil, pet shop, distribuidor | brinquedo, ração, tapete higiênico, caixa |

**Total:** 10 segmentos e 26 categorias. As 11 categorias do baseline oficial permanecem com o
mesmo nome e descrição; as 15 categorias adicionais só entram no perfil `expanded`.

## 4. Segmentos avaliados, mas não semeados

| Possível segmento | Motivo da não inclusão |
|---|---|
| Imóveis, crédito e seguros | não representa bem de consumo comparável por lista de compras |
| Serviços profissionais e contratistas | exigiria modelo de agenda, técnico e disponibilidade, fora do DER |
| Marketplace de usados | inventário e estado de item exigiriam atributos e ciclo de vida próprios |
| Licitações e compras públicas | exige documentos, vigência e habilitação específica |
| Produtos digitais e assinaturas | não se encaixa em preço unitário, estoque físico e unidade de medida |

Esses segmentos podem ser tratados em uma CR futura, sem contaminar o seed do MVP.

## 5. Perfis de seed

| Perfil | Uso | Categorias | Fornecedores | Produtos | Preços | Relações N:N |
|---|---|---:|---:|---:|---:|---:|
| `baseline` | demonstração oficial e conformidade RNF08 | 11 | 10 | 50 | 300 | 25 |
| `expanded` | testes de escala, filtros e catálogo | 26 | 60 | 2.600 | 31.200 | 312 |

O perfil `baseline` é o seed oficial e idempotente. O perfil `expanded` é opt-in, usa a mesma
estrutura de oito tabelas e destina-se à preparação de grandes volumes de dados de teste sem
alterar os contratos de API ou o DER.

## 6. Regras de normalização

- texto em Unicode NFC, sem espaços duplicados, tabs, controles ou espaço nas extremidades;
- nomes de categorias, fornecedores e produtos únicos dentro do perfil;
- unidade canônica entre `un`, `kg`, `L` e `m`;
- CNPJ sintético, único e com dígitos verificadores válidos;
- IDs explícitos e determinísticos em todas as tabelas inseridas;
- preços em `Decimal`, quantized para duas casas, nunca negativos;
- estoque inteiro entre 0 e 9999;
- chaves `(fornecedor_id, produto_id)` únicas;
- dados fictícios, sem pessoas, telefones, endereços ou credenciais reais;
- geração determinística: mesma versão e perfil produzem o mesmo SQL byte a byte.

## 7. Como usar

```bash
# Seed oficial, mantém o baseline normativo
make seed

# Perfil expandido para testes de volume (confirmação obrigatória)
make seed-expanded SEED_EXPANDED_CONFIRM=SIM

# Regenerar o SQL versionado a partir da fonte canônica
python3 backend/scripts/script-seed-0001-generate-seed-v1.0.py --profile baseline --output backend/config-seed-0001-seed-v1.0.sql
```

O perfil expandido é destrutivo para os dados mockados locais (usuários, listas e catálogo) e
exige `SEED_EXPANDED_CONFIRM=SIM`. Ele não deve ser executado contra ambiente com dados reais.
Promover o perfil expandido como padrão exige CR e ratificação humana, conforme
`constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` Arts. 5.1 e 5.4.

## 8. Implementação e validação

- fonte canônica: `backend/scripts/script-seed-0002-seed-data-v1.0.py`;
- gerador SQL: `backend/scripts/script-seed-0001-generate-seed-v1.0.py`;
- testes automatizados: `backend/tests/unit/test_seed_data.py`;
- seed oficial reproduzível: `backend/config-seed-0001-seed-v1.0.sql`;
- carga validada em bancos MySQL isolados para `baseline` e `expanded`;
- `make seed-expanded SEED_EXPANDED_CONFIRM=SIM` exige confirmação e remove o arquivo temporário
  ao término.

## 9. Rastreabilidade

- `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md`: Arts. 3.1, 3.3, 3.4, 3.5, 7.7, 8.1, 8.2, 12.7 e 19.3;
- `req-func-0001-requisitos-funcionais-canon.md`: RNF08;
- `req-use-case-0001-casos-de-uso-canon.md`: UC02–UC06 e UC23–UC26;
- `doc-arch-0001-camada-de-dados-canon.md`: 8 tabelas, N:N de categorias e chaves compostas;
- SPEC: `.ai/specs/spec-seed-0001-seed-segmentos-volume-v1.0.md`;
- Handoff: `.ai/handoffs/HF-0622-seed-segmentos-volume.md`.
