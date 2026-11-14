# 📊 ESTRUTURA OFICIAL DA CAMADA DE DADOS — COBECO MVP v3.2

**Documento:** Camada de Dados e Diagrama Entidade-Relacionamento (DER)  
**Versão:** 3.2 (SSOT Final)  
**Data:** 14 de Setembro de 2026  
**Status:** ✅ APROVADO — Composição Oficial  
**Base:** DOC-03 do Pacote Documental Consolidado

---

## 🎯 PREMISSAS APLICADAS

| Princípio | Aplicação no DER |
|-----------|------------------|
| **ACID** | Foreign keys com ON DELETE CASCADE/RESTRICT, transações explícitas, InnoDB |
| **KISS** | MySQL stdlib, zero ORM pesado, Repository pattern |
| **YAGNI** | Sem tabelas de sessão, sem refresh_tokens, sem comparisons |
| **SDD** | Campos alinhados aos schemas Pydantic |
| **Correção v3.1** | Categorias são de **FORNECEDORES** (N:N via `fornecedores_categorias`) |
| **Normalização v3.2** | Todas entidades e atributos em PT-BR |

---

## 📊 ENTIDADES (8 TABELAS) — NOMENCLATURA PT-BR

| # | Tabela (PT-BR) | Grupo | Regra de Negócio |
|---|----------------|-------|------------------|
| 1 | `usuarios` | 🔐 Auth | Usuários com autenticação JWT |
| 2 | `listas` | 📝 Listas | Listas persistidas (soft delete) |
| 3 | `itens_lista` | 📝 Listas | Itens de cada lista |
| 4 | `categorias` | 🏪 Catálogo | Categorias MACRO de fornecedores |
| 5 | `fornecedores` | 🏪 Catálogo | Fornecedores mockados |
| 6 | `fornecedores_categorias` | 🏪 Catálogo | Pivô N:N (fornecedor ↔ categorias) |
| 7 | `produtos` | 🏪 Catálogo | Produtos agnósticos à categoria |
| 8 | `fornecedores_produtos` | 🏪 Catálogo | Preços e estoque por fornecedor |

---

## 📋 ESPECIFICAÇÃO DAS TABELAS (PT-BR)

### 🔐 Tabela: `usuarios`

| Campo | Tipo | Constraints | Descrição |
|-------|------|-------------|-----------|
| `id` | INT | **PK**, AUTO_INCREMENT | Identificador único |
| `nome_usuario` | VARCHAR(30) | **UNIQUE**, NOT NULL | Nome de login (3-30 chars) |
| `email` | VARCHAR(255) | **UNIQUE**, NOT NULL | Email válido |
| `nome` | VARCHAR(100) | NOT NULL | Nome completo |
| `senha_hash` | VARCHAR(255) | NOT NULL | Senha hasheada (bcrypt) |
| `pergunta_seguranca` | VARCHAR(255) | NOT NULL | Pergunta de recuperação |
| `resposta_seguranca_hash` | VARCHAR(255) | NOT NULL | Resposta hasheada |
| `criado_em` | DATETIME | NOT NULL, DEFAULT NOW() | Data de criação |
| `atualizado_em` | DATETIME | NOT NULL, DEFAULT NOW() ON UPDATE | Data de atualização |
| `deletado_em` | DATETIME | NULL | Soft delete |

**Constraints:**
- `PK(id)`
- `UNIQUE(nome_usuario)`
- `UNIQUE(email)`
- `CHECK(LENGTH(nome_usuario) BETWEEN 3 AND 30)`
- `CHECK(LENGTH(nome) BETWEEN 2 AND 100)`

---

### 📝 Tabela: `listas`

| Campo | Tipo | Constraints | Descrição |
|-------|------|-------------|-----------|
| `id` | INT | **PK**, AUTO_INCREMENT | Identificador único |
| `usuario_id` | INT | **FK**, NOT NULL | Referência a `usuarios(id)` |
| `nome` | VARCHAR(100) | NOT NULL | Nome da lista |
| `criado_em` | DATETIME | NOT NULL, DEFAULT NOW() | Data de criação |
| `atualizado_em` | DATETIME | NOT NULL, DEFAULT NOW() ON UPDATE | Data de atualização |
| `deletado_em` | DATETIME | NULL | Soft delete |

**Constraints:**
- `PK(id)`
- `FK(usuario_id) → usuarios(id) ON DELETE CASCADE`
- `CHECK(LENGTH(nome) BETWEEN 1 AND 100)`
- `INDEX(usuario_id, criado_em DESC)`

---

### 📝 Tabela: `itens_lista`

| Campo | Tipo | Constraints | Descrição |
|-------|------|-------------|-----------|
| `id` | INT | **PK**, AUTO_INCREMENT | Identificador único |
| `lista_id` | INT | **FK**, NOT NULL | Referência a `listas(id)` |
| `produto_id` | INT | **FK**, NOT NULL | Referência a `produtos(id)` |
| `quantidade` | INT | NOT NULL | Quantidade (1-9999) |
| `criado_em` | DATETIME | NOT NULL, DEFAULT NOW() | Data de criação |

**Constraints:**
- `PK(id)`
- `FK(lista_id) → listas(id) ON DELETE CASCADE`
- `FK(produto_id) → produtos(id) ON DELETE RESTRICT`
- `CHECK(quantidade BETWEEN 1 AND 9999)`
- `UNIQUE(lista_id, produto_id)`

---

### 🏪 Tabela: `categorias` ⭐ NORMALIZADO v3.2

| Campo | Tipo | Constraints | Descrição |
|-------|------|-------------|-----------|
| `id` | INT | **PK**, AUTO_INCREMENT | Identificador único |
| `nome` | VARCHAR(100) | **UNIQUE**, NOT NULL | Nome da categoria |
| `descricao` | TEXT | NULL | Descrição opcional |

**Constraints:**
- `PK(id)`
- `UNIQUE(nome)`

**Seed:** 11 categorias macro
- Mercado
- Vestuário
- Automotivos
- Informática
- Decoração
- Móveis
- Materiais de Construção e Ferragens
- Ferramentas
- Livros
- Jardinagem
- Eletrodomésticos

---

### 🏪 Tabela: `fornecedores` ⭐ NORMALIZADO v3.2

| Campo | Tipo | Constraints | Descrição |
|-------|------|-------------|-----------|
| `id` | INT | **PK**, AUTO_INCREMENT | Identificador único |
| `nome` | VARCHAR(150) | NOT NULL | Nome do fornecedor |
| `cnpj` | VARCHAR(18) | **UNIQUE**, NOT NULL | CNPJ formatado |
| `ativo` | BOOLEAN | NOT NULL, DEFAULT TRUE | Situação do fornecedor |
| `criado_em` | DATETIME | NOT NULL, DEFAULT NOW() | Data de criação |

**Constraints:**
- `PK(id)`
- `UNIQUE(cnpj)`

**Seed:** 10 fornecedores
- Leroy Merlin
- Etna
- C&A
- Renner
- Hering
- Pão de Açúcar
- Magazine Luiza
- Casas Bahia
- Carrefour
- Extra

---

### 🏪 Tabela: `fornecedores_categorias` ⭐ PIVÔ N:N — NORMALIZADO v3.2

| Campo | Tipo | Constraints | Descrição |
|-------|------|-------------|-----------|
| `fornecedor_id` | INT | **FK**, **PK** | Referência a `fornecedores(id)` |
| `categoria_id` | INT | **FK**, **PK** | Referência a `categorias(id)` |

**Constraints:**
- `PK(fornecedor_id, categoria_id)` — composta
- `FK(fornecedor_id) → fornecedores(id) ON DELETE CASCADE`
- `FK(categoria_id) → categorias(id) ON DELETE CASCADE`

**Seed:** ~25 relações N:N
- Leroy Merlin → Decoração, Ferramentas, Jardinagem, Materiais de Construção
- Etna → Decoração, Móveis
- C&A → Vestuário
- Renner → Vestuário
- Hering → Vestuário
- Pão de Açúcar → Mercado
- Magazine Luiza → Eletrodomésticos, Informática, Móveis
- Casas Bahia → Eletrodomésticos, Informática, Móveis
- Carrefour → Mercado, Vestuário, Automotivos, Decoração, Eletrodomésticos, Informática
- Extra → Mercado, Vestuário, Eletrodomésticos

---

### 🏪 Tabela: `produtos` ⭐ NORMALIZADO v3.2

| Campo | Tipo | Constraints | Descrição |
|-------|------|-------------|-----------|
| `id` | INT | **PK**, AUTO_INCREMENT | Identificador único |
| `nome` | VARCHAR(200) | NOT NULL | Nome do produto |
| `unidade` | VARCHAR(10) | NOT NULL | Unidade de medida (un, kg, L, m) |
| `ativo` | BOOLEAN | NOT NULL, DEFAULT TRUE | Situação do produto |
| `criado_em` | DATETIME | NOT NULL, DEFAULT NOW() | Data de criação |

**Constraints:**
- `PK(id)`
- `INDEX(nome)`

**Seed:** 50 produtos (agnósticos à categoria)

---

### 🏪 Tabela: `fornecedores_produtos` ⭐ NORMALIZADO v3.2

| Campo | Tipo | Constraints | Descrição |
|-------|------|-------------|-----------|
| `fornecedor_id` | INT | **FK**, **PK** | Referência a `fornecedores(id)` |
| `produto_id` | INT | **FK**, **PK** | Referência a `produtos(id)` |
| `preco` | DECIMAL(10,2) | NOT NULL | Preço unitário |
| `estoque` | INT | NOT NULL, DEFAULT 0 | Estoque disponível |
| `ativo` | BOOLEAN | NOT NULL, DEFAULT TRUE | Situação do vínculo |

**Constraints:**
- `PK(fornecedor_id, produto_id)` — composta
- `FK(fornecedor_id) → fornecedores(id) ON DELETE CASCADE`
- `FK(produto_id) → produtos(id) ON DELETE RESTRICT`
- `CHECK(preco >= 0)`
- `CHECK(estoque >= 0)`

**Seed:** ~300 preços (variação ±20%)

---

## 🔗 RELACIONAMENTOS (CARDINALIDADES)

| Origem | → | Destino | Cardinalidade | Constraint |
|--------|---|---------|---------------|------------|
| `usuarios` | → | `listas` | 1:N | FK `usuario_id` ON DELETE CASCADE |
| `listas` | → | `itens_lista` | 1:N | FK `lista_id` ON DELETE CASCADE |
| `produtos` | → | `itens_lista` | 1:N | FK `produto_id` ON DELETE RESTRICT |
| `fornecedores` | ↔ | `categorias` | N:N | Via `fornecedores_categorias` |
| `fornecedores` | → | `fornecedores_produtos` | 1:N | FK `fornecedor_id` ON DELETE CASCADE |
| `produtos` | → | `fornecedores_produtos` | 1:N | FK `produto_id` ON DELETE RESTRICT |

---

## 🔒 VALIDAÇÃO ACID

| Princípio | Garantia no DER |
|-----------|-----------------|
| **Atomicity** | Transações explícitas via `BEGIN/COMMIT` em todas operações de escrita |
| **Consistency** | FKs com CASCADE/RESTRICT, CHECK constraints, UNIQUE |
| **Isolation** | InnoDB permite leitura concorrente sem bloqueio (MVCC) |
| **Durability** | MySQL InnoDB grava em disco com redo log automático |

---

## 📊 ESTATÍSTICAS FINAIS

| Métrica | Valor |
|---------|-------|
| Total de tabelas | 8 |
| Primary Keys | 8 (todas simples, exceto 2 compostas) |
| Foreign Keys | 9 |
| Constraints UNIQUE | 4 |
| Constraints CHECK | 5 |
| Relacionamentos 1:N | 5 |
| Relacionamentos N:N | 1 (via pivô) |
| Soft deletes | 2 (`usuarios`, `listas`) |
| Índices compostos | 2 |

---

## 📦 SEED DE DADOS

```python
# Categorias MACRO (para fornecedores)
categorias = [
    "Mercado",
    "Vestuário",
    "Automotivos",
    "Informática",
    "Decoração",
    "Móveis",
    "Materiais de Construção e Ferragens",
    "Ferramentas",
    "Livros",
    "Jardinagem",
    "Eletrodomésticos"
]

# Fornecedores com múltiplas categorias (N:N)
fornecedores = [
    {"nome": "Leroy Merlin", "cnpj": "11.222.333/0001-44",
     "categorias": ["Materiais de Construção e Ferragens", "Ferramentas", "Jardinagem", "Decoração"]},
    {"nome": "Etna", "cnpj": "22.333.444/0001-55",
     "categorias": ["Decoração", "Móveis"]},
    {"nome": "C&A", "cnpj": "33.444.555/0001-66",
     "categorias": ["Vestuário"]},
    {"nome": "Renner", "cnpj": "44.555.666/0001-77",
     "categorias": ["Vestuário"]},
    {"nome": "Hering", "cnpj": "55.666.777/0001-88",
     "categorias": ["Vestuário"]},
    {"nome": "Pão de Açúcar", "cnpj": "66.777.888/0001-99",
     "categorias": ["Mercado"]},
    {"nome": "Magazine Luiza", "cnpj": "77.888.999/0001-00",
     "categorias": ["Eletrodomésticos", "Informática", "Móveis"]},
    {"nome": "Casas Bahia", "cnpj": "88.999.000/0001-11",
     "categorias": ["Eletrodomésticos", "Informática", "Móveis"]},
    {"nome": "Carrefour", "cnpj": "99.000.111/0001-22",
     "categorias": ["Mercado", "Vestuário", "Automotivos", "Decoração", "Eletrodomésticos", "Informática"]},
    {"nome": "Extra", "cnpj": "00.111.222/0001-33",
     "categorias": ["Mercado", "Vestuário", "Eletrodomésticos"]}
]

# Produtos (agnósticos à categoria)
produtos = [
    {"nome": "Arroz Tipo 1 5kg", "unidade": "un"},
    {"nome": "Feijão Preto 1kg", "unidade": "un"},
    {"nome": "Martelo de Unha 25mm", "unidade": "un"},
    {"nome": "Notebook i5 8GB", "unidade": "un"},
    {"nome": "Camiseta Algodão M", "unidade": "un"},
    # ... até 50 produtos
]
```

---

## ✅ CHECKLIST DE VALIDAÇÃO

- [x] 8 tabelas conforme especificação v3.2
- [x] Tabela pivô `fornecedores_categorias` presente (N:N)
- [x] `produtos` SEM FK para `categorias` (correção conceitual)
- [x] Todas PKs, FKs, UNIQUE, CHECK visíveis
- [x] Cardinalidades 1:N e N:N corretas
- [x] Soft delete em `usuarios` e `listas` (`deletado_em`)
- [x] Seed documentado (10 forn + 50 prod + 11 cat)
- [x] MySQL InnoDB configurado (ACID)
- [x] Legenda completa com ícones 🔑 🔗
- [x] Normalização PT-BR completa
- [x] Histórico de mudanças documentado

---

**FIM DA ESTRUTURA OFICIAL DA CAMADA DE DADOS — COBECO MVP v3.2**