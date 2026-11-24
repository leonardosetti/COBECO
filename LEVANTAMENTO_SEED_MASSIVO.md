# Levantamento Rigoroso — Candidatos para Seed Massivo COBECO

**Data:** 2026-11-19  
**Base:** SPECS v3.3 + DER v1.0 + 3 seeds existentes (baseline, expanded, prototype)  
**Objetivo:** Mapear todas as fontes, estratégias e vetores para aumentar exponencialmente o volume e diversidade de dados do seed.

---

## 1. Estado Atual — Perfis Existentes

| Perfil | Categorias | Fornecedores | Produtos | Preços (ofertas) | Relações N:N |
|--------|------------|--------------|----------|------------------|--------------|
| baseline | 11 | 10 | 50 | 300 | 25 |
| expanded | 26 | 60 | 2.600 | 31.200 | 312 |
| prototype | 11 | 10 | 20 | ~160 | ~40 |

**Gargalo identificado:** O perfil `expanded` usa **variantes sintéticas** (12 variantes × 10 produtos-base por categoria) — não dados reais. O salto para seed massivo exige **fontes reais/externalizadas**.

---

## 2. Tabelas Alvo — Capacidade de Expansão

| Tabela | Chaves | Atual (expanded) | Limite Teórico | Fator de Escala |
|--------|--------|------------------|----------------|-----------------|
| `categorias` | PK `id`, UK `nome` | 26 | ~200 (macro + micro) | **7.7×** |
| `fornecedores` | PK `id`, UK `cnpj`, UK `nome` | 60 | ~5.000 (CNPJs válidos) | **83×** |
| `produtos` | PK `id`, UK `nome` | 2.600 | ~500.000 (GTIN/EAN) | **192×** |
| `fornecedores_produtos` | PK composta | 31.200 | ~50M (sparse matrix) | **1.600×** |
| `fornecedores_categorias` | PK composta | 312 | ~50.000 | **160×** |

---

## 3. Fontes de Dados Candidatas — Classificadas por Viabilidade

### 3.1 Fontes Abertas / Públicas (Zero Custo, Alta Confiabilidade)

| Fonte | Tipo | Cobertura | Acesso | Volume Estimado | Esforço Integração |
|-------|------|-----------|--------|-----------------|-------------------|
| **ReceitaWS / CNPJ.io** | CNPJ válidos + razão social | Brasil todo | API REST gratuita | 20M+ empresas | Baixo |
| **IBGE - CNAE 2.0** | Classificação atividades econômicas | 1.300+ códigos | Download CSV | 1.300 categorias | Baixo |
| **GS1 Brasil / GTIN** | Códigos de barras produtos | Varejo formal | API paga / parceria | 1M+ GTINs | Médio |
| **Mercado Livre / Shopee / Amazon** | Catálogo público (scraping) | E-commerce BR | HTML/GraphQL | 50M+ SKUs | Alto (legal/rate limit) |
| **Open Food Facts** | Produtos alimentícios | Global, foco BR | API aberta / dump | 3M+ produtos | Baixo |
| **Wikidata (SPARQL)** | Entidades comerciais | Global | Endpoint público | 100M+ items | Médio |
| **Dados Abertos Gov.br** | Fornecedores públicos, licitações | Setor público | CSV/API | 500k+ CNPJs | Baixo |
| **ABRAS / ABAD / GS1 BR** | Listas associados varejo/atacado | Setor organizado | Site/PDF | 10k+ empresas | Médio |

### 3.2 Fontes Semi-Estruturadas (Requerem Parsing)

| Fonte | Tipo | Volume | Dificuldade |
|-------|------|--------|-------------|
| **Sites de redes varejistas** (Carrefour, Extra, Pão de Açúcar, etc.) | Catálogo online | 50k-200k SKUs/red | Alta (JS-rendered, anti-bot) |
| **Marketplaces B2B** (Mercado Livre B2B, B2W, Magalu Marketplace) | Sellers + produtos | 1M+ sellers | Muito alta |
| **Listas de preços públicas** (Diários Oficiais, portais transparência) | Preços referência | 100k+ itens | Média |
| **Catálogos industriais** (DIN, ISO, NCM) | Produtos técnicos | 50k+ códigos | Baixa (CSV/Excel) |

### 3.3 Fontes Sintéticas Controladas (Geração Programática)

| Estratégia | Descrição | Volume Potencial | Qualidade |
|------------|-----------|------------------|-----------|
| **Combinação CNAE × Região × Porte** | Gera fornecedores plausíveis por segmento/UF | 500k+ CNPJs únicos | Média (precisa validação CNPJ) |
| **GTIN sintético + atributos** | EAN-13 válido + nome composto (categoria + marca + spec) | 1M+ produtos | Alta (determinístico) |
| **Matriz esparsa preços** | Algoritmo de pricing realista (custo + margem + região + sazonalidade) | 50M+ ofertas | Alta |
| **Variação temporal** | Preços com histórico (semanas/meses) | N× volume base | Alta |

---

## 4. Vetores de Expansão por Entidade

### 4.1 Categorias — De 26 para ~200 (Macro + Micro)

**Estratégia:** Hierarquia CNAE 2.0 → Macro (seção) → Micro (classe/subclasse)

```
Seção G (Comércio) → 47.11-1-01 (Hipermercados) → Macro "Mercado"
                    → 47.51-2-01 (Móveis) → Macro "Móveis"
                    → 47.71-7-01 (Vestuário) → Macro "Vestuário"
Seção C (Indústria) → 10.11-2-01 (Abate) → Macro "Alimentos"
```

**Candidatos imediatos (macro):**
- Alimentos e Bebidas (dividir Mercado em: Mercearia, Açougue, Padaria, Hortifruti, Bebidas)
- Casa e Construção (dividir em: Elétrica, Hidráulica, Pintura, Ferramentas, Madeira, Cerâmica)
- Tecnologia (dividir em: Informática, Celulares, Áudio/Video, Gaming, Acessórios, Componentes)
- Moda (dividir em: Vestuário Masc/Fem/Inf, Calçados, Bolsas, Acessórios, Íntima, Praia)
- Saúde (Farmácia, Perfumaria, Ortopedia, Ótica, Suplementos, Natural)
- Automotivo (Peças, Acessórios, Pneus, Lubrificantes, Ferramentas, Som)
- Pet (Raças, Medicamentos, Acessórios, Higiene, Brinquedos)
- Esportes (Academia, Corrida, Futebol, Natação, Bike, Outdoor, Lutas)
- Infantil (Brinquedos, Puericultura, Moda Infantil, Escolar, Móveis)
- Escritório (Papelaria, Móveis, Informática, Organização, Impressão)
- Jardim (Plantas, Vasos, Ferramentas, Irrigação, Decoração, Piscina)
- Eletro (Linha Branca, Linha Marrom, Portáteis, Climatização, Peças)

**Total viável: 50-80 macro categorias bem definidas.**

### 4.2 Fornecedores — De 60 para 5.000+

**Fontes primárias:**
1. **ReceitaWS** — Consulta CNPJ por CNAE + UF → gera lista por categoria
2. **CNAE × UF × Porte** — Matriz: 1.300 CNAEs × 27 UFs × 3 portes = 105k combinações
3. **Redes conhecidas** — Expandir 10 atuais para 100+ bandeiras (Carrefour → Atacadão, Sam's, etc.)
4. **Marketplaces** — Sellers ativos com CNPJ válido

**Atributos enriquecidos por fornecedor:**
- `nome_fantasia`, `razao_social`, `cnpj`, `uf`, `municipio`, `cnae_principal`, `cnaes_secundarios`
- `porte` (MEI, ME, EPP, DEMAIS), `capital_social`, `data_abertura`, `situacao_cadastral`
- `latitude`, `longitude` (para geo-filtro futuro)
- `categorias` (via CNAE → macro categoria mapeamento)

**Validação obrigatória:** CNPJ dígito verificador + situação "ATIVA" + não MEI (para B2B).

### 4.3 Produtos — De 2.600 para 100.000+

**Estratégia em camadas:**

| Camada | Fonte | Método | Volume | Qualidade |
|--------|-------|--------|--------|-----------|
| **Core Real** | Open Food Facts + GS1 dump | Import direto | 50k-100k | Alta (GTIN, nome, marca, categoria, ingredientes, nutrição) |
| **Catálogo Varejo** | Scraping seletivo (categorias-alvo) | Playwright + parsing | 200k+ | Média (precisa dedup) |
| **Sintético Estruturado** | GTIN válido + template nome | Geração determinística | 1M+ | Alta (controlado) |
| **Variantes** | Produto-base × (marca × embalagem × especificação) | Expansão combinatória | 10× base | Alta |

**Template nome produto (determinístico):**
```
{Marca} {Linha} {Produto} {Especificação} {Embalagem}
Ex: "Nestlé Nescau Chocolate 370g Lata"
```

**Atributos enriquecidos:**
- `gtin` (EAN-13 válido, UK), `marca`, `linha`, `categoria_macro`, `categoria_micro`
- `unidade` (un, kg, L, m, cx, dz, pct, m2, m3), `peso_liquido`, `dimensoes`
- `ncm` (NCM/SH), `cest`, `origem` (0-8), `ativo`

### 4.4 Preços/Ofertas — De 31.200 para 5.000.000+

**Modelo de pricing realista (determinístico, seedável):**

```
preco_final = custo_base × (1 + margem_categoria) × fator_fornecedor × fator_regiao × fator_tempo × ruído
```

**Fatores determinísticos (seed = hash(fornecedor_id, produto_id, data)):**
- `margem_categoria`: 15-60% por macro categoria (alimentos 15-25%, eletrônicos 10-20%, moda 50-100%)
- `fator_fornecedor`: 0.85-1.20 (atacado vs varejo vs premium)
- `fator_regiao`: 0.95-1.10 (capital vs interior, UF)
- `fator_tempo`: sazonalidade (Black Friday, Natal, volta aulas, etc.)
- `ruído`: ±3% (simula variação real)

**Estoque:** Distribuição log-normal por categoria (alimentos: alto giro/baixo estoque; duráveis: baixo giro/alto estoque).

**Cobertura (sparsity):** Matriz esparsa ~5-10% (fornecedor não tem todos produtos). Regra: fornecedor tem produtos apenas das suas categorias + 5-15% cross-category.

---

## 5. Estratégias de Geração — Arquitetura Recomendada

### 5.1 Pipeline em Estágios (Determinístico, Paralelizável)

```
┌─────────────┐   ┌──────────────┐   ┌─────────────┐   ┌──────────────┐   ┌────────────┐
│ 1. CNAE/    │──▶│ 2. Forneced  │──▶│ 3. Produtos │──▶│ 4. Ofertas   │──▶│ 5. Valida  │
│    Categorias│   │    ores      │   │    (GTIN)   │   │  (Preços)    │   │    & SQL   │
└─────────────┘   └──────────────┘   └─────────────┘   └──────────────┘   └────────────┘
     (CSV/IBGE)      (ReceitaWS +      (OpenFoodFacts +   (Algoritmo       (Checks +
      + sintético)   sintético)        sintético)         pricing)         UK/FK/CK)
```

### 5.2 Perfis de Volume (Configuráveis)

| Perfil | Categorias | Fornecedores | Produtos | Ofertas | Tempo Est. | Uso |
|--------|------------|--------------|----------|---------|------------|-----|
| **micro** | 11 | 10 | 50 | 300 | <5s | Testes unitários |
| **baseline** | 26 | 60 | 2.600 | 31k | <30s | Dev local |
| **standard** | 50 | 500 | 25k | 500k | ~5min | CI/CD, Staging |
| **large** | 80 | 2.000 | 100k | 5M | ~30min | Performance, Load test |
| **massive** | 150 | 10.000 | 500k | 50M | ~4h | Benchmark, Stress |

### 5.3 Determinismo — Requisitos Obrigatórios

- **Seed global único** → todos os RNGs derivados (Python `random`, `numpy`, `hashlib`)
- **IDs estáveis** — Atribuição por hash(entidade) não por ordem de inserção
- **Ordenação canônica** — SQL ORDER BY PK em todos INSERTs
- **Validação pós-geração** — Counts, UKs, FKs, CKs, ranges (igual ao `validate_dataset` atual)

---

## 6. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **CNPJ inválido/duplicado** | Alta | Quebra FK/UK | Validação `is_valid_cnpj` + set() antes de insert |
| **GTIN colisão** | Média | UK violada | Prefixo GS1 reservado (789/790 BR) + hash determinístico |
| **Nome produto duplicado** | Alta | UK violada | Template + hash sufixo (ex: "Arroz Tipo 1 5kg #a1b2") |
| **Matriz densa demais** | Média | Performance/Storage | Sparsity target 5-10% + chunking INSERT 5k rows |
| **Tempo geração > CI timeout** | Alta (large+) | Pipeline falha | Perfil `standard` no CI; `large`/`massive` só manual |
| **Dados sensíveis (LGPD)** | Baixa | Legal | Só CNPJ público + dados sintéticos; zero PII real |
| **Dependência API externa** | Média | Indisponibilidade | Cache local + fallback sintético; ReceitaWS tem rate limit |

---

## 7. Próximos Passos — Roadmap de Implementação

### Fase 1 — Fundação (1-2 dias)
- [ ] Estender `script-seed-0002-seed-data-v1.0.py` com novo perfil `standard`
- [ ] Adicionar `CNAE_MACRO_MAP` (CNAE → 50 macro categorias)
- [ ] Implementar `generate_suppliers_from_cnae(cnae, uf, count)` determinístico
- [ ] Validar contagens esperadas no `validate_dataset`

### Fase 2 — Produtos Reais (2-3 dias)
- [ ] Integrar dump Open Food Facts (produtos alimentícios BR)
- [ ] Parser NCM/GTIN → `produtos` + `categoria_macro`
- [ ] Gerar variantes sintéticas por produto-base (marca × embalagem)

### Fase 3 — Pricing Engine (2 dias)
- [ ] `PricingEngine` class com fatores determinísticos por hash
- [ ] Sparsity controlada (matriz esparsa por categoria)
- [ ] Estoque log-normal por categoria

### Fase 4 — Perfis Grandes (1 dia)
- [ ] Perfil `large` (2k fornecedores, 100k produtos, 5M ofertas)
- [ ] Otimização: `COPY`/`LOAD DATA` vs INSERT chunked
- [ ] Benchmark tempo/ram

### Fase 5 — Validação Contínua (contínuo)
- [ ] Testes property-based (hypothesis) para validação estatística
- [ ] Contrato: seed `standard` roda em <5min no CI
- [ ] Documentar como adicionar nova macro categoria

---

## 8. Estimativa de Volume Final (Perfil `massive`)

| Entidade | Registros | Tamanho Estimado (MySQL) |
|----------|-----------|--------------------------|
| categorias | 150 | ~50 KB |
| fornecedores | 10.000 | ~5 MB |
| fornecedores_categorias | ~50.000 | ~3 MB |
| produtos | 500.000 | ~150 MB |
| fornecedores_produtos | 50.000.000 | ~8 GB |
| **Total** | **~50.5M** | **~8.2 GB** |

**Tempo geração estimado:** 2-4 horas (single-thread) / 30-60 min (paralelo 8 cores)  
**Tempo carga MySQL:** 15-30 min (LOAD DATA INFILE otimizado)

---

## 9. Decisões de Design — Registradas

| Decisão | Justificativa | Reversível? |
|---------|---------------|-------------|
| Categorias = Macro Fornecedores (não produtos) | DER v3.1 corrigido; alinhado a UC03/RF12 | Não (quebra domínio) |
| Produtos agnósticos a categoria | Flexibilidade; um produto vende em múltiplas categorias via fornecedores | Não |
| CNPJ como UK + validação dígito | Realismo; evita lixo; ReceitaWS usa CNPJ | Não |
| GTIN/EAN-13 como UK produto | Padrão indústria; permite integração futura | Sim (pode adicionar coluna) |
| Preços determinísticos por hash | Reprodutibilidade; zero flakiness em testes | Não |
| Matriz esparsa (5-10%) | Realismo; performance; storage | Sim (parâmetro configurável) |
| Perfis em arquivo único (Python) | Versionável; testável; sem migrações SQL manuais | Sim |

---

## 10. Checklist de Validação para Novo Perfil

- [ ] `counts` batem com `_EXPECTED_COUNTS[profile]`
- [ ] Zero UK violations (nome categoria, cnpj, nome fornecedor, nome produto, gtin)
- [ ] Zero FK violations (todas relações apontam para IDs existentes)
- [ ] Zero CHECK violations (preço ≥ 0, estoque ≥ 0, unidade ∈ {un,kg,L,m,cx,dz,pct,m2,m3})
- [ ] CNPJs válidos (formato + dígito verificador + filial 0001)
- [ ] Distribuição fornecedor/categoria: ~12 fornecedores/categoria (configurável)
- [ ] Cobertura ofertas: 5-10% da matriz fornecedor×produto
- [ ] Seed idempotente: rodar 2x produz SQL byte-a-byte idêntico
- [ ] Tempo geração < threshold do perfil
- [ ] SQL carrega em MySQL sem erros (FK checks on)

---

**Fim do Levantamento.** Este documento serve como especificação para implementação do seed massivo. Cada fase deve produzir diff atômico com testes.