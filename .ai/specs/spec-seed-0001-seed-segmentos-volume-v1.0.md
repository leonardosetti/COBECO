---
id: spec-seed-0001-seed-segmentos-volume-v1.0
type: spec-seed
title: SPEC SEED — Seed Segmentos Volume
version: v1.0
status: ratificado
canonical: false
canonical_slug: seed-segmentos-volume
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
domain: specs
layer: spec
tags: []
lgpd_class: n/a
workflow:
  stage: rascunho
  reviewer: null
  reviewed_at: null
  approval_hash: null
  board_url: null
---
---
spec_id: spec-016
specname: seed-segmentos-volume-v1
version: 1.1.0
status: implementado
custody: config-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-0001-config-config-opencode-0001-opencode-v1-0001-config-opencode-0001-opencode-v1-v1.0-v1.0 (.ai/specs/)
created: 2026-11-13
updated: 2026-11-14
origin: solicitação do usuário de 2026-11-13 (branch feat/UC-02-03-seed-volume)
task: TA-0622
kill_switch: inherited
wave: WS-1 — Seed e catálogo
lgpd-class: PII-sintético (somente empresas, produtos e CNPJs fictícios)
trace:
- .ai/handoffs/HF-0622-seed-segmentos-volume.md
- docs/strategy/PESQUISA-SEGMENTOS-MERCADO-SEED.md
- constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md (Arts. 3.1-3.5, 7.7, 8.1-8.2, 12.7, 19.3)
---

# SPEC spec-016 — seed-segmentos-volume-v1 — Segmentos de mercado e perfis de seed

Status: **implementado e validado localmente** | Branch: `feat/UC-02-03-seed-volume` | Orquestrador: OpenCode

Fonte única das decisões desta especificação. Em conflito, vale a hierarquia do Art. 2 da
Constituição.

## 1. Resolução de conflitos documentais

| Tema | Decisão | Fonte vencedora | Texto superado |
|---|---|---|---|
| Volume oficial do seed | mantém 11 categorias, 10 fornecedores, 50 produtos e cerca de 300 preços | Constitution Art. 12.7 e req-func-0001-requisitos-funcionais-canon RNF08 | contagem incorreta observada no SQL legado |
| Volume para testes | novo perfil opt-in `expanded`, sem alterar DER, API ou baseline oficial | solicitação local de dados de teste | ausência de volume ampliado |
| Segmento de mercado | taxonomia de planejamento; persistência continua em `categorias` | doc-arch-0001-camada-de-dados-canon v3.2 | lista informal sem fonte canônica |
| Promoção do perfil expandido a padrão | não autorizada nesta execução; exige CR e ratificação humana | Constitution Arts. 1.5, 5.1 e 5.4 | nenhuma |

Fora do escopo: nova tabela de segmentos, migration, mudança de contrato HTTP, dados reais,
reais price feeds e promoção do perfil expandido a seed oficial.

## 2. Regras de negócio

1. O seed possui dois perfis: `baseline` e `expanded`.
2. `baseline` é o perfil oficial: 11 categorias, 10 fornecedores, 50 produtos, 300 preços e
   25 relações N:N.
3. `expanded` cobre 10 segmentos, 26 categorias, 60 fornecedores, 2.600 produtos, 31.200 preços
   e 312 relações N:N.
4. Ambos os perfis usam somente as oito tabelas de `doc-arch-0001-camada-de-dados-canon.md` v3.2.
5. A associação segmento/categoria do produto existe na fonte canônica de seed para geração e
   auditoria; ela não cria FK em `produtos`, conforme a decisão v3.2 do DER.
6. Texto é normalizado em Unicode NFC, com espaços internos colapsados e ausência de espaços nas
   extremidades.
7. Nomes, CNPJs e chaves compostas são únicos dentro de cada perfil.
8. CNPJs são fictícios, formatados em 18 caracteres e possuem dígitos verificadores válidos.
9. Unidades usam somente `un`, `kg`, `L` e `m`.
10. Preços usam `Decimal`, duas casas decimais e valor não negativo; estoque varia de 0 a 9999.
11. IDs são explícitos e determinísticos; a mesma versão e o mesmo perfil geram SQL idêntico.
12. Os perfis `baseline` e `expanded` reiniciam os dados mockados locais (usuários, listas e
    catálogo) para garantir estado determinístico; o perfil expanded exige confirmação operacional
    e nunca deve ser executado em ambiente com dados reais.

## 3. Contrato de API

Nenhuma alteração. Permanecem os endpoints UC02–UC06 e os schemas existentes:

| Endpoint | Método | Parâmetros | Resposta | Código de erro |
|---|---|---|---|---|
| `/v1/catalogo/categorias` | GET | — | lista de categorias | 500 |
| `/v1/catalogo/fornecedores` | GET | `categorias` opcional | lista de fornecedores | 500 |
| `/v1/catalogo/produtos/autocomplete` | GET | `q`, `limit` | lista de produtos | 422, 500 |
| `/v1/catalogo/produtos` | GET | — | lista de produtos | 500 |

OpenAPI não requer atualização porque o contrato não muda.

## 4. Modelagem de dados

Sem alteração de schema. O gerador produz comandos para:

- `categorias` (`id`, `nome`, `descricao`);
- `fornecedores` (`id`, `nome`, `cnpj`, `ativo`);
- `fornecedores_categorias` (`fornecedor_id`, `categoria_id`);
- `produtos` (`id`, `nome`, `unidade`, `ativo`);
- `fornecedores_produtos` (`fornecedor_id`, `produto_id`, `preco`, `estoque`, `ativo`).

As tabelas `usuarios`, `listas` e `itens_lista` são reiniciadas junto com o catálogo. O reset é
explícito no artefato, preserva o comportamento idempotente do seed legado e garante estado
determinístico para os testes de integração. Nenhuma tabela é criada ou alterada.

## 5. Segurança

- validação de entrada no CLI: perfil deve ser `baseline` ou `expanded`;
- dados exclusivamente fictícios, sem pessoas, telefones, endereços ou credenciais;
- queries do runtime permanecem parametrizadas;
- escaping SQL de strings no gerador evita interpolação insegura;
- seed expanded exige confirmação operacional por ser destrutivo;
- nenhum segredo é gravado em seeds, fixtures, logs ou artefatos.

## 6. Critérios de aceite (DoD)

- [x] levantamento de segmentos e taxonomia documentado em PT-BR;
- [x] baseline oficial permanece em 11/10/50/300;
- [x] perfil expanded gera 26/60/2.600/31.200;
- [x] DER de oito tabelas sem alteração;
- [x] IDs, textos, CNPJs, unidades, preços e chaves são normalizados;
- [x] geração determinística e idempotente;
- [x] testes automatizados validam contagens e invariantes;
- [x] `make seed-expanded` disponível com confirmação operacional;
- [x] queries de runtime permanecem parametrizadas;
- [x] nenhum PII real;
- [ ] CI completo verde — bloqueado por débitos preexistentes fora do escopo do seed;
- [ ] review R-01..R-07 e aprovação humana antes de merge.

## 7. Testes

| Módulo | Caso de teste | Resultado esperado | Automatizado? |
|---|---|---|---|
| `scripts.seed_data` | contagens do baseline | 11/10/50/300 e 25 relações | Sim |
| `scripts.seed_data` | contagens do expandido | 26/60/2.600/31.200 e 312 relações | Sim |
| `scripts.seed_data` | normalização | NFC, espaços colapsados, unidades canônicas | Sim |
| `scripts.seed_data` | integridade | nomes/CNPJ/chaves únicos, preços e estoque válidos | Sim |
| `scripts.seed_data` | determinismo | duas gerações produzem SQL idêntico | Sim |
| seed SQL | carga no MySQL | volume persistido corresponde ao perfil | Sim |

**Rastreabilidade:** RNF08 → UC02–UC06/UC23–UC26 → spec-016 → HF-0622 → código → teste → merge.

## 8. Evidências de execução

- `04b10a9`: fonte canônica, gerador SQL e sete testes automatizados do seed;
- `713d1e1`: seed baseline reproduzível, comando de regeneração e carregamento opt-in expanded;
- testes do seed: `7 passed` no Python 3.11 do container do backend;
- carga baseline em banco MySQL isolado: `11/10/50/300/25`;
- carga expanded em banco MySQL isolado: `26/60/2.600/31.200/312`;
- reprodução byte a byte de `backend/config-seed-0001-seed-v1.0.sql` confirmada pelo gerador;
- lint dos três arquivos do seed aprovado com Ruff 0.9.1 em modo isolado.

## CHANGELOG

- **1.1.0 — 2026-11-14:** implementação concluída com validação determinística e carga dos dois
  perfis em bancos MySQL isolados.
- **1.0.0 — 2026-11-13:** baseline corrigido para a contagem normativa; perfil expanded opt-in
  com taxonomia de 10 segmentos e 26 categorias; geração determinística e normalizada.

**Fim da SPEC spec-016**
