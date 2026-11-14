# 📚 BASE DOCUMENTAL CONSOLIDADA — COBECO MVP v3.2

**Pacote de 4 Documentos Analíticos Ortogonais**
**Data:** 14 de Setembro de 2026
**Status:** ✅ SSOT (Single Source of Truth)
**Público-Alvo:** Equipe de Desenvolvimento, QA, Product Owner (Thais Cristina Casagrande), Stakeholders Acadêmicos

---

## 📑 Índice do Pacote Documental

| #                | Documento                                | Propósito                                                   | Seção         |
| ---------------- | ---------------------------------------- | ------------------------------------------------------------ | --------------- |
| **DOC-01** | Análise de Casos de Uso e Consistência | Modelagem UML, happy paths, exceções, matriz de relações | [DOC-01](#doc01) |
| **DOC-02** | Análise de Requisitos e Consistência   | RFs, RNFs, RDs, rastreabilidade, validação                 | [DOC-02](#doc02) |
| **DOC-03** | Análise da Camada de Dados (DER)        | Modelo relacional, normalização PT-BR, ACID                | [DOC-03](#doc03) |
| **DOC-04** | Relatório Analítico COBECO (Geral)     | ADRs, stack, cronograma, governança                         | [DOC-04](#doc04) |

---

<a id="doc01"></a>

# 📄 DOC-01 — ANÁLISE DE CASOS DE USO E CONSISTÊNCIA

**Versão:** 3.2 | **Data:** 14/09/2026 | **Status:** ✅ APROVADO
**Cross-ref:** Requisitos em [DOC-02](#doc02) | DER em [DOC-03](#doc03) | Geral em [DOC-04](#doc04)

---

## 📜 1. HISTÓRICO DE MUDANÇAS

| Versão        | Data                 | Mudança Principal                                                         | Impacto                     |
| -------------- | -------------------- | -------------------------------------------------------------------------- | --------------------------- |
| v1.0           | Ago/2026             | MVP sem autenticação, 14 UCs, SQLite3, CSV                               | Baseline                    |
| v2.0           | 31/08/2026           | Auth adicionada (UC01-UC04), tabela flat simplificada                      | +7 UCs                      |
| v2.1           | 01/09/2026           | UC25 (Selecionar Fornecedores) + UC26 (Filtro Disponibilidade)             | +2 UCs, RF11-12             |
| v3.0           | 12/09/2026           | Primeira análise crítica, 26 UCs consolidados                            | Revisão completa           |
| v3.1           | 12/09/2026           | DER com`supplier_categories` (N:N), categorias de fornecedores           | Correção conceitual       |
| **v3.2** | **14/09/2026** | **MySQL InnoDB, PDF server-side, pré-filtro por categorias, PT-BR** | **+3 UCs, 29 totais** |

### 1.1 Mudanças Específicas v3.1 → v3.2

| Mudança                            | UCs Afetados                              | Tipo           |
| ----------------------------------- | ----------------------------------------- | -------------- |
| Pré-filtro por categorias          | UC03 (novo), UC04 (ajustado), UC24 (novo) | Adição       |
| Exportação PDF server-side        | UC08 (renomeado), UC29 (novo)             | Substituição |
| Validação de categorias no salvar | UC14 → UC03 (`<<include>>`)            | Nova relação |
| Normalização PT-BR                | Todos UCs (nomenclatura)                  | Renomeação   |
| MySQL InnoDB (não SQLite3)         | Boundary do diagrama                      | Infraestrutura |

---

## 🎭 2. ATORES DO SISTEMA

| Ator                               | Tipo        | Papel                                                                 | Generalização                |
| ---------------------------------- | ----------- | --------------------------------------------------------------------- | ------------------------------ |
| **Visitante**                | Primário   | Usuário não autenticado. Cria listas em memória, compara, exporta. | Ator base                      |
| **Usuário Autenticado**     | Primário   | Herda Visitante + persistência de listas.                            | **Generaliza Visitante** |
| **Sistema**                  | Secundário | Validações (Pydantic), hashing, rate limiting, geração PDF.       | —                             |
| **API Mock de Fornecedores** | Secundário | Fornece catálogo, categorias, fornecedores e preços.                | —                             |

---

## 🎬 3. CATÁLOGO DE CASOS DE USO (29 UCs)

### 3.1 Casos Principais (19)

| ID             | Caso de Uso                                      | Ator                 | RF         | Área        |
| -------------- | ------------------------------------------------ | -------------------- | ---------- | ------------ |
| UC09           | Cadastrar-se                                     | Visitante            | RF01       | Auth         |
| UC10           | Realizar Login                                   | Visitante            | RF02       | Auth         |
| UC11           | Realizar Logout                                  | Usuário Autenticado | RF03       | Auth         |
| UC12           | Recuperar Senha                                  | Visitante            | RF04       | Auth         |
| UC18           | Visualizar Perfil                                | Usuário Autenticado | RF05       | Auth         |
| UC16           | Gerenciar Perfil                                 | Usuário Autenticado | RF06       | Auth         |
| UC01           | Criar Lista em Memória                          | Visitante            | RF07       | Listas       |
| UC02           | Buscar Produtos (Autocomplete)                   | Visitante            | RF07       | Listas       |
| UC14           | Salvar Lista (Persistir)                         | Usuário Autenticado | RF08       | Listas       |
| UC17           | Promover Lista Efêmera                          | Usuário Autenticado | RF08       | Listas       |
| UC15           | Listar Minhas Listas                             | Usuário Autenticado | RF09       | Listas       |
| UC13           | Editar/Excluir Lista Salva                       | Usuário Autenticado | RF10, RF11 | Listas       |
| **UC03** | **Selecionar Categorias (Pré-filtro)** ⭐ | Visitante            | RF12       | Pré-filtro  |
| UC04           | Selecionar Fornecedores                          | Visitante            | RF13       | Comparação |
| UC05           | Filtrar por Disponibilidade                      | Visitante            | RF14       | Comparação |
| UC06           | Calcular Orçamento                              | Visitante            | RF15       | Comparação |
| UC07           | Visualizar Resultados                            | Visitante            | RF16       | Comparação |
| **UC08** | **Exportar Lista PDF** ⭐                  | Visitante            | RF17       | Exportação |
| UC09           | Imprimir                                         | Visitante            | RF18       | Exportação |

### 3.2 Casos Internos (10)

| ID             | Caso de Uso                                   | Ator     | Descrição                           |
| -------------- | --------------------------------------------- | -------- | ------------------------------------- |
| UC20           | Validar Dados                                 | Sistema  | Validação Pydantic cross-cutting    |
| UC21           | Hash de Senha (bcrypt)                        | Sistema  | Salt=12                               |
| UC22           | Gerar Sessão (JWT)                           | Sistema  | Access 15min + refresh 7d httpOnly    |
| UC23           | Fornecer Catálogo                            | API Mock | 50 produtos do seed                   |
| **UC24** | **Fornecer Categorias** ⭐              | API Mock | 11 categorias macro                   |
| **UC25** | **Fornecer Fornecedores (filtrado)** ⭐ | API Mock | Fornecedores filtrados por categorias |
| UC26           | Fornecer Preços                              | API Mock | ~300 preços do seed                  |
| UC27           | Rate Limiting                                 | Sistema  | 6 tentativas/15min                    |
| UC28           | Invalidar Sessão                             | Sistema  | Logout + rotação de tokens          |
| **UC29** | **Gerar PDF (ReportLab)** ⭐            | Sistema  | Geração server-side A4              |

---

## 🔄 4. FLUXOS DETALHADOS (Happy Paths + Exceções + Edge-Cases)

### 🔐 Fluxo A — Autenticação

#### UC09 — Cadastrar-se (RF01)

**Happy Paths:**

- HP1: Formulário completo → validação frontend → bcrypt → INSERT `usuarios` → 201 → redirect /login
- HP2: Campos válidos → unicidade validada → toast "Conta criada com sucesso"

**Exceções:**
| E1 | nome_usuario duplicado | "Credenciais inválidas" (genérico) |
| E2 | Senha fraca | Erro inline no `onBlur` |
| E3 | Email inválido | Validação frontend bloqueia submit |
| E4 | Confirmação diferente | "As senhas não coincidem" |

**Edge-Cases:**

- EC1: Duplo clique → botão desabilitado após 1º submit
- EC2: Resposta de segurança <3 chars → rejeita
- EC3: Nome com acentos → aceito (UTF-8)
- EC4: Perda de conexão → toast "Tente novamente"

#### UC10 — Realizar Login (RF02)

**Happy Paths:**

- HP1: Credenciais válidas → JWT access (15min memória) + refresh (7d cookie) → 200 → dashboard
- HP2: Lista efêmera ativa → modal "Salvar lista?" → UC17 dispara

**Exceções:**
| E1 | 6ª tentativa falha | HTTP 429 + lockout 15min |
| E2 | Credenciais inválidas | Mensagem genérica |
| E3 | Conta soft-deleted | Mensagem genérica |

**Edge-Cases:**

- EC1: 5 abas logando → mesmo refresh token
- EC2: Access expira → retry via /auth/refresh
- EC3: Refresh expirado → redirect /login
- EC4: NAT → rate limiting híbrido (IP + username)

#### UC11 — Realizar Logout (RF03)

**Happy Paths:**

- HP1: "Sair" → invalida refresh → limpa access → redirect /
- HP2: Sessão expirada → redirect automático

**Exceções:**
| E1 | Erro de rede | Toast "Falha ao encerrar" |
| E2 | Refresh expirado | Logout forçado sem erro |
| E3 | Múltiplas abas | Apenas aba atual deslogada |

#### UC12 — Recuperar Senha (RF04)

**Happy Paths:**

- HP1 (Via B — Pergunta): username → pergunta → resposta → nova senha → 200
- HP2 (Via A — Log): username → token no stdout → nova senha

**Exceções:**
| E1 | username inexistente | "Usuário não encontrado" |
| E2 | 3 respostas erradas | Bloqueio temporário |
| E3 | Token expirado (>15min) | "Solicite novamente" |

#### UC16 — Gerenciar Perfil (RF05, RF06)

**Happy Paths:**

- HP1: Altera email → confirma senha antiga → atualiza
- HP2: Altera senha → bcrypt → atualiza

**Exceções:**
| E1 | Email já existe | "Email já cadastrado" |
| E2 | Senha antiga errada | "Senha atual incorreta" |
| E3 | Nova senha igual à antiga | Rejeita |

#### UC18 — Visualizar Perfil (RF05)

**Happy Paths:**

- HP1: /perfil → dados pessoais (username, email, nome, data criação)
- HP2: Botão "Editar Perfil" visível

**Exceções:**
| E1 | Não autenticado | Redirect /login |
| E2 | Dados corrompidos | Toast "Erro ao carregar" |
| E3 | Conta soft-deleted | "Conta desativada" |

---

### 📝 Fluxo B — Pré-filtro e Listas

#### UC03 — Selecionar Categorias (Pré-filtro) ⭐ NOVO v3.2 (RF12)

**Happy Paths:**

- HP1: 11 categorias macro visíveis → seleciona "Mercado" → fornecedores filtrados
- HP2: Seleciona múltiplas (ex: "Mercado" + "Eletrodomésticos") → fornecedores de ambas aparecem

**Exceções:**
| E1 | Nenhuma categoria selecionada | "Selecione ao menos 1 categoria" + botão desabilitado |
| E2 | API lenta (>500ms) | Skeleton loading |
| E3 | Categoria inativa | Não aparece na lista |

**Edge-Cases:**

- EC1: Seleciona todas 11 → todos fornecedores aparecem
- EC2: Categoria sem fornecedores → toast + sugere outra
- EC3: Recarrega página → seleção perdida (toast)
- EC4: Fornecedor em 5+ categorias → aparece 1x com badges

#### UC01 — Criar Lista em Memória (RF07)

**Happy Paths:**

- HP1: Nome "Compras do Mês" + 3 produtos via autocomplete → subtotal em tempo real → sessionStorage
- HP2: Fecha aba → reabre → lista perdida (comportamento esperado)

**Exceções:**
| E1 | Nome vazio | "Informe um nome" |
| E2 | Quantidade = 0 | Validação inline |
| E3 | Produto não encontrado | Toast "Tente outro termo" |

**Edge-Cases:**

- EC1: Mesmo produto 2x → soma quantidades
- EC2: Nome >100 chars → contador "X/100"
- EC3: Quantidade = 10000 → rejeita
- EC4: sessionStorage cheio → toast "Salve a lista"

#### UC02 — Buscar Produtos (Autocomplete) (RF07)

**Happy Paths:**

- HP1: Digita "arr" → debounce 300ms → ["Arroz Tipo 1 5kg", "Arroz Integral 1kg"]
- HP2: Seleciona produto → adicionado com quantidade 1

**Exceções:**
| E1 | Termo <2 chars | Busca não iniciada |
| E2 | API lenta | Skeleton loading |
| E3 | Nenhum resultado | "Nenhum produto encontrado" |

#### UC14 — Salvar Lista (Persistir) (RF08)

**Happy Paths:**

- HP1: "Salvar" → valida FK + valida categorias (UC03) → INSERT `listas` + `itens_lista` (ACID) → 201
- HP2: Promove lista efêmera (UC17) → modal → transação ACID

**Exceções:**
| E1 | Não autenticado | Modal de login |
| E2 | Produto descontinuado | Toast "Remova da lista" |
| E3 | Erro de conexão | Toast "Tente novamente" |
| E4 | Nenhuma categoria selecionada | Toast "Selecione ao menos 1 categoria" |

**Edge-Cases:**

- EC1: 100+ itens → atomicidade ACID
- EC2: Produto removido durante salvamento → rollback
- EC3: Duplo clique → botão desabilitado
- EC4: MySQL lock → busy_timeout=5000 → retry

#### UC17 — Promover Lista Efêmera ⭐ NOVO v3.2 (RF08)

**Happy Paths:**

- HP1: Login com lista ativa → modal "Salvar?" → SIM → UC17 dispara
- HP2: Login → modal → NÃO → mantém efêmera

**Exceções:**
| E1 | Lista vazia | Modal não aparece |
| E2 | Erro ao promover | Toast + mantém efêmera |
| E3 | Fecha modal (X) | Mantém efêmera |

#### UC15 — Listar Minhas Listas (RF09)

**Happy Paths:**

- HP1: /dashboard → lista paginada (20/página) ordenada DESC
- HP2: Busca por nome → filtro case-insensitive

**Exceções:**
| E1 | Nenhuma lista | "Você ainda não tem listas" |
| E2 | Página inválida | Redirect página 1 |
| E3 | Erro de carregamento | Toast "Falha ao carregar" |

#### UC13 — Editar/Excluir Lista Salva (RF10, RF11)

**Happy Paths:**

- HP1 (Editar): Altera nome → UPDATE `listas` → toast "Atualizada"
- HP2 (Excluir): "Excluir" → digita nome → soft delete → toast "Excluída"

**Exceções:**
| E1 | Lista não pertence ao usuário | HTTP 403 |
| E2 | Confirmação não digitada | Botão desabilitado |
| E3 | Lista já excluída | "Não encontrada" |

---

### 🔄 Fluxo C — Comparação

#### UC04 — Selecionar Fornecedores (RF13)

**Happy Paths:**

- HP1: Vê fornecedores filtrados por categorias (UC03) → seleciona 3
- HP2: "Selecionar Todos" → todos marcados

**Exceções:**
| E1 | Apenas 1 fornecedor | "Selecione ao menos 2" + botão desabilitado |
| E2 | Fornecedor inativo | Não aparece |
| E3 | Recarrega página | Seleção perdida (toast) |

**Edge-Cases:**

- EC1: Nenhum fornecedor nas categorias → toast + sugere outras
- EC2: Seleciona todos 10 → permitido
- EC3: Fornecedor 0% disponibilidade → badge "0%" + tooltip
- EC4: Filtro (UC05) elimina selecionado → mantém se ainda válido

#### UC05 — Filtrar por Disponibilidade (RF14)

**Happy Paths:**

- HP1: Slider 70% → lista reduz para ≥70%
- HP2: Slider 0% → todos reaparecem

**Exceções:**
| E1 | Filtro 100% elimina todos | "Nenhum atende ao filtro" |
| E2 | Filtro desmarca selecionado | Mantém se válido |
| E3 | Valor fora do range | Validação rejeita |

**⚠️ Dualidade Documentada:** UC05 aparece como `<<include>>` (depende de UC04) E `<<extend>>` (opcional sobre UC04). Filtro PRECISA da seleção (include), mas usuário PODE optar por não aplicá-lo (extend).

#### UC06 — Calcular Orçamento (RF15)

**Happy Paths:**

- HP1: "Calcular" → valida → UC23 + UC24 → tabela flat 200ms → cache 5min
- HP2: Altera seleção → cache invalidado → novo cálculo

**Exceções:**
| E1 | Timeout >10s | Toast "Tempo esgotado" |
| E2 | Lista excluída | Redirect /dashboard |
| E3 | Fornecedor sem preço | Ícone ⚠️ + "N/D" |

#### UC07 — Visualizar Resultados (RF16)

**Happy Paths:**

- HP1: Tabela ordenada por preço ASC → menor em verde
- HP2: Hover sobre item ausente → tooltip detalhes

**Exceções:**
| E1 | Todos preços iguais | "Empate técnico" |
| E2 | Lista vazia | Redirect criação |
| E3 | Erro de formatação | Fallback genérico |

---

### 📤 Fluxo D — Exportação

#### UC08 — Exportar Lista PDF ⭐ NOVO v3.2 (RF17)

**Happy Paths:**

- HP1: "Exportar PDF" → UC29 (ReportLab) → PDF A4 → download `lista_20260914.pdf`
- HP2: Visitante (sem login) exporta lista em memória → funciona

**Exceções:**
| E1 | Erro ao gerar PDF | Toast "Tente novamente" |
| E2 | Lista >100 itens | Múltiplas páginas (quebras automáticas) |
| E3 | Nome com caracteres especiais | Escaping automático |

**Edge-Cases:**

- EC1: Duplo clique → botão desabilitado
- EC2: PDF >10MB → geração assíncrona + toast
- EC3: Fonte especial → UTF-8 suportado
- EC4: Cancela download → estado preservado

#### UC09 — Imprimir (RF18)

**Happy Paths:**

- HP1: "Imprimir" → CSS @media print → diálogo nativo → A4
- HP2: Quebras automáticas + cores preservadas

**Exceções:**
| E1 | Tela <1024px | Aviso "Otimizada para ≥1024px" |
| E2 | Cancela diálogo | Nenhum erro |
| E3 | Impressora offline | Erro do navegador |

---

### ⚙️ Casos Internos (sem happy paths detalhados)

| ID   | Invocado Por     | Comportamento                         |
| ---- | ---------------- | ------------------------------------- |
| UC20 | UC09, UC14, UC16 | Valida schemas Pydantic               |
| UC21 | UC09             | bcrypt salt=12                        |
| UC22 | UC10             | JWT access 15min + refresh 7d         |
| UC23 | UC02             | 50 produtos do seed                   |
| UC24 | UC03             | 11 categorias macro                   |
| UC25 | UC04, UC06       | Fornecedores filtrados por categorias |
| UC26 | UC06             | ~300 preços do seed                  |
| UC27 | UC10, UC12       | 6 tentativas/15min                    |
| UC28 | UC11             | Invalida refresh tokens               |
| UC29 | UC08             | Gera PDF A4 server-side               |

---

## 🔗 5. MATRIZ DE RELAÇÕES NOMEADAS

### 5.1 Relações `<<include>>` (Obrigatórias) — 16 relações

| #  | Origem         | Destino           | Rótulo Descritivo                                     | Justificativa           |
| -- | -------------- | ----------------- | ------------------------------------------------------ | ----------------------- |
| 1  | UC09           | UC20              | "valida dados de cadastro"                             | Validação Pydantic    |
| 2  | UC09           | UC21              | "hasheia senha (bcrypt)"                               | Segurança salt=12      |
| 3  | UC10           | UC22              | "gera JWT access + refresh"                            | Stateless               |
| 4  | UC10           | UC27              | "aplica rate limiting (6/15min)"                       | Anti-DDoS               |
| 5  | UC12           | UC27              | "aplica rate limiting"                                 | Anti-abuso              |
| 6  | UC16           | UC20              | "valida dados do perfil"                               | Consistência           |
| 7  | UC14           | UC20              | "valida FK de produto"                                 | Integridade             |
| 8  | **UC14** | **UC03** ⭐ | **"valida categorias selecionadas"**             | **NOVO v3.2**     |
| 9  | UC02           | UC23              | "consulta catálogo de produtos"                       | Busca seed              |
| 10 | **UC03** | **UC24** ⭐ | **"lista categorias macro"**                     | **NOVO v3.2**     |
| 11 | **UC04** | **UC25** ⭐ | **"lista fornecedores filtrados por categoria"** | **AJUSTADO v3.2** |
| 12 | UC06           | UC20              | "valida lista e seleção"                             | Integridade             |
| 13 | UC06           | UC25              | "busca fornecedores selecionados"                      | Cálculo                |
| 14 | UC06           | UC26              | "busca preços dos produtos"                           | Cálculo                |
| 15 | **UC08** | **UC29** ⭐ | **"gera PDF server-side (ReportLab)"**           | **NOVO v3.2**     |
| 16 | UC11           | UC28              | "invalida refresh token"                               | Segurança              |

### 5.2 Relações `<<extend>>` (Opcionais) — 5 relações

| # | Origem         | Destino           | Rótulo Descritivo                        | Condição           |
| - | -------------- | ----------------- | ----------------------------------------- | -------------------- |
| 1 | UC05           | UC04              | "filtra fornecedores por disponibilidade" | Se aplicar slider    |
| 2 | **UC08** | **UC07** ⭐ | **"exporta resultados em PDF"**     | Após visualização |
| 3 | UC09           | UC07              | "imprime resultados em A4"                | Após visualização |
| 4 | UC16           | UC18              | "edita dados do perfil"                   | Se usuário optar    |
| 5 | UC17           | UC14              | "promove lista efêmera para persistente" | Após login          |

---

## ✅ 6. VALIDAÇÃO DE PRINCÍPIOS UML

| Princípio                             | Status | Observação                                                              |
| -------------------------------------- | ------ | ------------------------------------------------------------------------- |
| Separação Ator Primário/Secundário | ✅     | Visitante/Autenticado vs Sistema/API                                      |
| Boundary do Sistema                    | ✅     | Todos 29 UCs dentro                                                       |
| Generalização de Atores              | ✅     | Autenticado generaliza Visitante                                          |
| Cardinalidade 1:N                      | ✅     | Respeitada                                                                |
| Direção das Setas                    | ✅     | `<<include>>` e `<<extend>>` corretos                                 |
| Coesão de Áreas                      | ✅     | 5 áreas (Auth, Pré-filtro/Listas, Comparação, Exportação, Internos) |
| Ausência de Ciclos                    | ✅     | Sem loops                                                                 |
| Nenhum UC Solitário                   | ✅     | Todos conectados                                                          |
| Rótulos Descritivos                   | ✅     | 21 relações nomeadas em PT-BR                                           |

---

## 📊 7. MATRIZ DE RASTREABILIDADE (RF → UC)

| RF   | UC Principal      | UCs Internos      | Prioridade |
| ---- | ----------------- | ----------------- | ---------- |
| RF01 | UC09              | UC20, UC21        | P0         |
| RF02 | UC10              | UC22, UC27        | P0         |
| RF03 | UC11              | UC28              | P0         |
| RF04 | UC12              | UC27              | P1         |
| RF05 | UC18              | —                | P1         |
| RF06 | UC16              | UC20              | P1         |
| RF07 | UC01, UC02        | UC23              | P0         |
| RF08 | UC14, UC17        | UC20, UC03        | P0         |
| RF09 | UC15              | —                | P0         |
| RF10 | UC13              | UC20              | P1         |
| RF11 | UC13              | —                | P1         |
| RF12 | **UC03** ⭐ | **UC24** ⭐ | P0         |
| RF13 | UC04              | UC25              | P0         |
| RF14 | UC05              | UC04              | P1         |
| RF15 | UC06              | UC20, UC25, UC26  | P0         |
| RF16 | UC07              | —                | P0         |
| RF17 | **UC08** ⭐ | **UC29** ⭐ | P0         |
| RF18 | UC09              | —                | P1         |

---

## 📈 8. ESTATÍSTICAS FINAIS

| Métrica                   | v3.1         | v3.2         | Variação       |
| -------------------------- | ------------ | ------------ | ---------------- |
| UCs principais             | 18           | 19           | +1 (UC03)        |
| UCs internos               | 8            | 10           | +2 (UC24, UC29)  |
| **Total UCs**        | **26** | **29** | **+3**     |
| Atores                     | 4            | 4            | =                |
| `<<include>>`            | 14           | 16           | +2               |
| `<<extend>>`             | 5            | 5            | =                |
| **Total relações** | 19           | 21           | +2               |
| Áreas funcionais          | 4            | 5            | +1 (Pré-filtro) |
| RFs cobertos               | 17/17        | 18/18        | +1 (RF12)        |
| Happy paths                | 36           | 38           | +2               |
| Exceções                 | 54           | 57           | +3               |
| Edge-cases                 | 55+          | 60+          | +5               |

---

## ✅ 9. CHECKLIST DE VALIDAÇÃO

- [X] 29 Casos de Uso (19 principais + 10 internos)
- [X] 4 Atores com generalização UML correta
- [X] 18 RFs cobertos (100%)
- [X] 12 RNFs atendidos (100%)
- [X] 16 relações `<<include>>` (todas nomeadas)
- [X] 5 relações `<<extend>>` (todas nomeadas)
- [X] Nenhum UC solitário
- [X] Fluxo correto: Categorias → Lista → Fornecedores → Comparação → Exportação
- [X] MySQL InnoDB (ACID)
- [X] PDF server-side (ReportLab)
- [X] Normalização PT-BR completa
- [X] 38 happy paths documentados
- [X] 57 exceções documentadas
- [X] 60+ edge-cases documentados
- [X] Dualidade UC05 documentada
- [X] Histórico de mudanças completo

---

<a id="doc02"></a>

# 📄 DOC-02 — ANÁLISE DE REQUISITOS E CONSISTÊNCIA

**Versão:** 3.2 | **Data:** 14/09/2026 | **Status:** ✅ APROVADO
**Cross-ref:** UCs em [DOC-01](#doc01) | DER em [DOC-03](#doc03) | Geral em [DOC-04](#doc04)

---

## 📜 1. HISTÓRICO DE MUDANÇAS

| Versão        | Data                 | Mudança Principal                                         | Impacto                    |
| -------------- | -------------------- | ---------------------------------------------------------- | -------------------------- |
| v1.0           | Ago/2026             | 14 RFs, sem auth, CSV                                      | Baseline                   |
| v2.0           | 31/08/2026           | +5 RFs (auth), tabela flat                                 | +5 RFs                     |
| v2.1           | 01/09/2026           | RF11-12 (seleção/filtro fornecedores)                    | +2 RFs                     |
| v3.0           | 12/09/2026           | 17 RFs consolidados                                        | Revisão                   |
| v3.1           | 12/09/2026           | DER corrigido (categorias de fornecedores)                 | Conceitual                 |
| **v3.2** | **14/09/2026** | **RF12 (pré-filtro categorias), RF17 (PDF), PT-BR** | **+1 RF, 18 totais** |

### 1.1 Mudanças Específicas v3.1 → v3.2

| Mudança                            | RFs Afetados              | Tipo           |
| ----------------------------------- | ------------------------- | -------------- |
| Pré-filtro por categorias          | RF12 (novo)               | Adição       |
| Exportação PDF server-side        | RF17 (substitui RF16 CSV) | Substituição |
| Validação de categorias no salvar | RF08 (ajustado)           | Refinamento    |
| Normalização PT-BR                | Todos RFs (nomenclatura)  | Renomeação   |
| MySQL InnoDB                        | RNF03 (ajustado)          | Infraestrutura |

---

## 📋 2. REQUISITOS FUNCIONAIS (RF) — VERSÃO FINAL v3.2

### 🔐 Grupo A — Autenticação e Perfil (RF01–RF06)

| ID             | Requisito                    | Descrição                                                                                 | Guard-Rails                                                                                                                             | Prioridade   |
| -------------- | ---------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| **RF01** | **Cadastrar Usuário** | Criar conta com nome_usuario (único), email, senha + confirmação, pergunta de segurança | Nome_usuario: 3-30 chars alfanumérico. Senha: mín 8, 1 maiúsc, 1 número, 1 especial. Email: formato válido. Pergunta obrigatória. | **P0** |
| **RF02** | **Login**              | Autenticar via nome_usuario + senha                                                         | **6 tentativas consecutivas** → lockout 15min (anti-DDoS). Mensagem genérica. JWT: access 15min memória + refresh 7d httpOnly. | **P0** |
| **RF03** | **Logout**             | Encerrar sessão ativa                                                                      | Invalida cookie. Limpa access da memória. Redirect para home.                                                                          | **P0** |
| **RF04** | **Recuperar Senha**    | Reset via pergunta de segurança (sem email)                                                | Pergunta do cadastro. 3 tentativas. Nova senha segue RF01. Modo alternativo: token no stdout (RECOVERY_MODE=log).                       | **P1** |
| **RF05** | **Visualizar Perfil**  | Ver dados pessoais (nome_usuario, email, nome)                                              | Apenas autenticado. Nome_usuario read-only.                                                                                             | **P1** |
| **RF06** | **Editar Perfil**      | Alterar email, nome e senha                                                                 | Senha antiga obrigatória. Email único.                                                                                                | **P1** |

### 📝 Grupo B — Gestão de Listas (RF07–RF11)

| ID             | Requisito                           | Descrição                                                          | Guard-Rails                                                                                                                                                 | Prioridade   |
| -------------- | ----------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| **RF07** | **Criar Lista (em memória)** | Qualquer usuário cria lista com nome + itens (produto + quantidade) | Mínimo 1 item. Quantidade: 1-9999. Produto deve existir no catálogo (autocomplete). Lista em memória JS até salvar.                                     | **P0** |
| **RF08** | **Salvar Lista (persistir)**  | Persistir lista no banco MySQL                                       | Requer autenticação. Se não logado → modal. Validação de FK.**Validação de categorias selecionadas (UC03)**. ACID: transação lista + itens. | **P0** |
| **RF09** | **Listar Minhas Listas**      | Exibir listas salvas do usuário                                     | Paginação 20/página. Ordenação: data DESC. Soft delete (excluídas não aparecem).                                                                     | **P0** |
| **RF10** | **Editar Lista Salva**        | Alterar nome, itens, quantidades                                     | Validação de propriedade (usuario_id). Confirmação antes de remover.                                                                                    | **P1** |
| **RF11** | **Excluir Lista Salva**       | Remover lista (soft delete)                                          | Confirmação obrigatória. Campo`deletado_em`.                                                                                                           | **P1** |

### 🔄 Grupo C — Pré-filtro e Comparação (RF12–RF16) ⭐ REFINADO v3.2

| ID                | Requisito                                     | Descrição                                               | Guard-Rails                                                                                                                      | Prioridade   |
| ----------------- | --------------------------------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| **RF12** ⭐ | **Selecionar Categorias (Pré-filtro)** | Escolher uma ou mais categorias para filtrar fornecedores | Mínimo 1 categoria. Checkboxes. Fornecedores filtrados dinamicamente. Seleção em memória.                                    | **P0** |
| **RF13**    | **Selecionar Fornecedores**             | Escolher quais fornecedores comparar (mínimo 2)          | Checkboxes com nome + % disponibilidade.**Apenas fornecedores das categorias selecionadas (RF12)**. Seleção em memória. | **P0** |
| **RF14**    | **Filtrar por Disponibilidade**         | Slider 0-100% para filtrar fornecedores                   | Padrão: 0% (todos). Atualiza em tempo real. Mantém seleção válida.                                                          | **P1** |
| **RF15**    | **Calcular Orçamento**                 | Gerar tabela flat comparativa                             | Timeout 10s. Cache 5min. Calcular: disponíveis, ausentes, preço total. Ordenar por preço ASC.                                 | **P0** |
| **RF16**    | **Visualizar Resultados**               | Tabela com destaque de melhor oferta                      | Destacar menor preço (verde). Mostrar % disponibilidade. Tooltip de ausentes.                                                   | **P0** |

### 📤 Grupo D — Exportação (RF17–RF18) ⭐ REFINADO v3.2

| ID                | Requisito                    | Descrição                | Guard-Rails                                                                                                                                | Prioridade   |
| ----------------- | ---------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| **RF17** ⭐ | **Exportar Lista PDF** | Download de lista em PDF   | **Funciona para TODOS usuários** (sem login). Geração server-side (Python + ReportLab). Nome: `lista_YYYYMMDD.pdf`. Formato A4. | **P0** |
| **RF18**    | **Imprimir**           | View otimizada para Ctrl+P | CSS`@media print`. Oculta menus. Formatação A4.                                                                                        | **P1** |

---

## 📋 3. REQUISITOS NÃO FUNCIONAIS (RNF) — VERSÃO FINAL v3.2

| ID                 | Requisito                     | Descrição                                                     | Métrica            |
| ------------------ | ----------------------------- | --------------------------------------------------------------- | ------------------- |
| **RNF01**    | Clean Architecture            | Camadas: Domain → UseCase → Adapter → Framework              | Code review         |
| **RNF02**    | SDD (OpenAPI First)           | Contrato OpenAPI 3.0 antes de implementar                       | Swagger em`/docs` |
| **RNF03**    | **ACID (MySQL InnoDB)** | Transações explícitas, engine InnoDB                         | Zero dados órfãos |
| **RNF04**    | Desktop-Only                  | Layout exclusivo ≥1024px. Sem mobile.                          | Breakpoint único   |
| **RNF05**    | Feedback Visual               | Toasts, loading states, modais                                  | <100ms feedback     |
| **RNF06**    | Testes Unitários             | Cobertura ≥80% das regras de negócio                          | pytest --cov        |
| **RNF07**    | CI/CD (Docker)                | Docker Compose (app + MySQL). GitHub Actions.                   | Pipeline <5min      |
| **RNF08**    | Seed de Dados                 | 10 fornecedores + 50 produtos + 11 categorias                   | `make seed` <10s  |
| **RNF09**    | Performance                   | API <500ms p95                                                  | curl + time         |
| **RNF10**    | Segurança                    | Rate limiting 6 req/15min. Hash bcrypt. JWT access em memória. | Zero brute-force    |
| **RNF11** ⭐ | **Geração de PDF**    | PDF gerado em <5s para listas até 100 itens                    | ReportLab           |
| **RNF12** ⭐ | **MySQL InnoDB**        | Engine InnoDB, charset utf8mb4, collation utf8mb4_unicode_ci    | ACID garantido      |

---

## 📋 4. REQUISITOS DESEJÁVEIS (Backlog Pós-MVP)

| ID                | Requisito                           | Descrição                                | Prioridade |
| ----------------- | ----------------------------------- | ------------------------------------------ | ---------- |
| RD01              | Histórico de Comparações         | Persistir resultados anteriores            | P3         |
| RD02              | Importação de Lista via CSV       | Upload de CSV para criar lista             | P3         |
| RD03              | Notificações de Preço            | Alertar quando preço cair                 | P3         |
| RD04              | Compartilhamento de Lista           | Link público                              | P3         |
| RD05              | App Mobile (PWA)                    | Versão responsiva                         | P3         |
| RD06              | Integração com Fornecedores Reais | Web scraping em tempo real                 | P4         |
| RD07              | Recomendações por IA              | Sugerir fornecedores baseado em histórico | P4         |
| RD08              | Multi-idioma                        | Inglês e espanhol                         | P4         |
| **RD09** ⭐ | **Export CSV (opcional)**     | Manter opção CSV além de PDF            | P3         |

---

## 🔗 5. MATRIZ DE RASTREABILIDADE RF → UC → RNF

| RF   | UC Principal | UCs Internos     | RNFs Relacionados   | Prioridade |
| ---- | ------------ | ---------------- | ------------------- | ---------- |
| RF01 | UC09         | UC20, UC21       | RNF01, RNF03, RNF10 | P0         |
| RF02 | UC10         | UC22, UC27       | RNF01, RNF10        | P0         |
| RF03 | UC11         | UC28             | RNF01, RNF10        | P0         |
| RF04 | UC12         | UC27             | RNF01, RNF10        | P1         |
| RF05 | UC18         | —               | RNF01, RNF04        | P1         |
| RF06 | UC16         | UC20             | RNF01, RNF03        | P1         |
| RF07 | UC01, UC02   | UC23             | RNF01, RNF03, RNF05 | P0         |
| RF08 | UC14, UC17   | UC20, UC03       | RNF01, RNF03        | P0         |
| RF09 | UC15         | —               | RNF01, RNF04, RNF09 | P0         |
| RF10 | UC13         | UC20             | RNF01, RNF03, RNF05 | P1         |
| RF11 | UC13         | —               | RNF01, RNF03        | P1         |
| RF12 | UC03 ⭐      | UC24 ⭐          | RNF04, RNF05, RNF06 | P1         |
| RF13 | UC04         | UC25             | RNF04, RNF05, RNF06 | P0         |
| RF14 | UC05         | UC04             | RNF04, RNF05, RNF09 | P1         |
| RF15 | UC06         | UC20, UC25, UC26 | RNF01, RNF03, RNF09 | P0         |
| RF16 | UC07         | —               | RNF04, RNF05, RNF09 | P0         |
| RF17 | UC08 ⭐      | UC29 ⭐          | RNF04, RNF05, RNF11 | P0         |
| RF18 | UC09         | —               | RNF04, RNF05        | P1         |

---

## ✅ 6. VALIDAÇÃO DE CONSISTÊNCIA

| Aspecto              | Status | Justificativa                       |
| -------------------- | ------ | ----------------------------------- |
| Completude           | ✅     | 18 RFs cobrem todo fluxo            |
| Ortogonalidade       | ✅     | RFs não se sobrepõem              |
| Rastreabilidade      | ✅     | 100% RF → UC → RNF                |
| Guard-Rails          | ✅     | Todos RFs têm critérios claros    |
| Priorização        | ✅     | P0 (11) + P1 (7) = 18               |
| Testabilidade        | ✅     | Cada RF tem métricas verificáveis |
| Normalização PT-BR | ✅     | Todos RFs em português             |

---

## 📈 7. ESTATÍSTICAS FINAIS

| Métrica      | v3.1 | v3.2 | Variação        |
| ------------- | ---- | ---- | ----------------- |
| RFs totais    | 17   | 18   | +1 (RF12)         |
| RNFs totais   | 10   | 12   | +2 (RNF11, RNF12) |
| RDs totais    | 8    | 9    | +1 (RD09)         |
| RFs P0        | 10   | 11   | +1                |
| RFs P1        | 7    | 7    | =                 |
| Cobertura UC  | 100% | 100% | =                 |
| Cobertura RNF | 100% | 100% | =                 |

---

## ✅ 8. CHECKLIST DE VALIDAÇÃO

- [X] 18 RFs definidos e rastreáveis
- [X] 12 RNFs definidos e mensuráveis
- [X] 9 RDs mapeados para backlog
- [X] 100% RFs cobertos por UCs
- [X] 100% RNFs exercitados
- [X] Matriz de rastreabilidade completa
- [X] Guard-Rails em todos RFs
- [X] Priorização P0/P1 definida
- [X] Normalização PT-BR completa
- [X] Histórico de mudanças documentado

---

<a id="doc03"></a>

# 📄 DOC-03 — ANÁLISE DA CAMADA DE DADOS (DER)

**Versão:** 3.2 | **Data:** 14/09/2026 | **Status:** ✅ APROVADO
**Cross-ref:** UCs em [DOC-01](#doc01) | Requisitos em [DOC-02](#doc02) | Geral em [DOC-04](#doc04)

---

## 📜 1. HISTÓRICO DE MUDANÇAS

| Versão        | Data                 | Mudança Principal                                          | Impacto                           |
| -------------- | -------------------- | ----------------------------------------------------------- | --------------------------------- |
| v1.0           | Ago/2026             | 6 tabelas, SQLite3, produtos com categoria                  | Baseline                          |
| v2.0           | 31/08/2026           | +2 tabelas (auth), soft delete                              | +2 tabelas                        |
| v2.1           | 01/09/2026           | Tabelas de seleção de fornecedores                        | Refinamento                       |
| v3.0           | 12/09/2026           | 8 tabelas consolidadas                                      | Revisão                          |
| v3.1           | 12/09/2026           | `supplier_categories` (N:N) — categorias de fornecedores | Correção conceitual             |
| **v3.2** | **14/09/2026** | **MySQL InnoDB, PT-BR, 11 categorias**                | **Normalização completa** |

### 1.1 Mudanças Específicas v3.1 → v3.2

| Mudança                                    | Tabelas Afetados         | Tipo           |
| ------------------------------------------- | ------------------------ | -------------- |
| MySQL InnoDB (não SQLite3)                 | Todas (infraestrutura)   | Substituição |
| Normalização PT-BR                        | Todas (nomenclatura)     | Renomeação   |
| 11 categorias macro (não 5)                | `categorias`           | Expansão seed |
| Campos`deletado_em` (não `deleted_at`) | `usuarios`, `listas` | Renomeação   |
| Campos`criado_em`, `atualizado_em`      | Todas                    | Renomeação   |

---

## 🎯 2. PREM ISSAS APLICADAS

| Princípio                    | Aplicação no DER                                                             |
| ----------------------------- | ------------------------------------------------------------------------------ |
| **ACID**                | Foreign keys com ON DELETE CASCADE/RESTRICT, transações explícitas, InnoDB  |
| **KISS**                | MySQL stdlib, zero ORM pesado, Repository pattern                              |
| **YAGNI**               | Sem tabelas de sessão, sem refresh_tokens, sem comparisons                    |
| **SDD**                 | Campos alinhados aos schemas Pydantic                                          |
| **Correção v3.1**     | Categorias são de**FORNECEDORES** (N:N via `fornecedores_categorias`) |
| **Normalização v3.2** | Todas entidades e atributos em PT-BR                                           |

---

## 📊 3. ENTIDADES (8 TABELAS) — NOMENIZAÇÃO PT-BR

| # | Tabela (PT-BR)              | Grupo        | Regra de Negócio                    |
| - | --------------------------- | ------------ | ------------------------------------ |
| 1 | `usuarios`                | 🔐 Auth      | Usuários com autenticação JWT     |
| 2 | `listas`                  | 📝 Listas    | Listas persistidas (soft delete)     |
| 3 | `itens_lista`             | 📝 Listas    | Itens de cada lista                  |
| 4 | `categorias`              | 🏪 Catálogo | Categorias MACRO de fornecedores     |
| 5 | `fornecedores`            | 🏪 Catálogo | Fornecedores mockados                |
| 6 | `fornecedores_categorias` | 🏪 Catálogo | Pivô N:N (fornecedor ↔ categorias) |
| 7 | `produtos`                | 🏪 Catálogo | Produtos agnósticos à categoria    |
| 8 | `fornecedores_produtos`   | 🏪 Catálogo | Preços e estoque por fornecedor     |

---

## 📋 4. ESPECIFICAÇÃO DAS TABELAS (PT-BR)

### 🔐 Tabela: `usuarios`

| Campo                       | Tipo         | Constraints                       | Descrição                |
| --------------------------- | ------------ | --------------------------------- | -------------------------- |
| `id`                      | INT          | **PK**, AUTO_INCREMENT      | Identificador único       |
| `nome_usuario`            | VARCHAR(30)  | **UNIQUE**, NOT NULL        | Nome de login (3-30 chars) |
| `email`                   | VARCHAR(255) | **UNIQUE**, NOT NULL        | Email válido              |
| `nome`                    | VARCHAR(100) | NOT NULL                          | Nome completo              |
| `senha_hash`              | VARCHAR(255) | NOT NULL                          | Senha hasheada (bcrypt)    |
| `pergunta_seguranca`      | VARCHAR(255) | NOT NULL                          | Pergunta de recuperação  |
| `resposta_seguranca_hash` | VARCHAR(255) | NOT NULL                          | Resposta hasheada          |
| `criado_em`               | DATETIME     | NOT NULL, DEFAULT NOW()           | Data de criação          |
| `atualizado_em`           | DATETIME     | NOT NULL, DEFAULT NOW() ON UPDATE | Data de atualização      |
| `deletado_em`             | DATETIME     | NULL                              | Soft delete                |

**Constraints:**

- `PK(id)`
- `UNIQUE(nome_usuario)`
- `UNIQUE(email)`
- `CHECK(LENGTH(nome_usuario) BETWEEN 3 AND 30)`
- `CHECK(LENGTH(nome) BETWEEN 2 AND 100)`

---

### 📝 Tabela: `listas`

| Campo             | Tipo         | Constraints                       | Descrição                   |
| ----------------- | ------------ | --------------------------------- | ----------------------------- |
| `id`            | INT          | **PK**, AUTO_INCREMENT      | Identificador único          |
| `usuario_id`    | INT          | **FK**, NOT NULL            | Referência a`usuarios(id)` |
| `nome`          | VARCHAR(100) | NOT NULL                          | Nome da lista                 |
| `criado_em`     | DATETIME     | NOT NULL, DEFAULT NOW()           | Data de criação             |
| `atualizado_em` | DATETIME     | NOT NULL, DEFAULT NOW() ON UPDATE | Data de atualização         |
| `deletado_em`   | DATETIME     | NULL                              | Soft delete                   |

**Constraints:**

- `PK(id)`
- `FK(usuario_id) → usuarios(id) ON DELETE CASCADE`
- `CHECK(LENGTH(nome) BETWEEN 1 AND 100)`
- `INDEX(usuario_id, criado_em DESC)`

---

### 📝 Tabela: `itens_lista`

| Campo          | Tipo     | Constraints                  | Descrição                   |
| -------------- | -------- | ---------------------------- | ----------------------------- |
| `id`         | INT      | **PK**, AUTO_INCREMENT | Identificador único          |
| `lista_id`   | INT      | **FK**, NOT NULL       | Referência a`listas(id)`   |
| `produto_id` | INT      | **FK**, NOT NULL       | Referência a`produtos(id)` |
| `quantidade` | INT      | NOT NULL                     | Quantidade (1-9999)           |
| `criado_em`  | DATETIME | NOT NULL, DEFAULT NOW()      | Data de criação             |

**Constraints:**

- `PK(id)`
- `FK(lista_id) → listas(id) ON DELETE CASCADE`
- `FK(produto_id) → produtos(id) ON DELETE RESTRICT`
- `CHECK(quantidade BETWEEN 1 AND 9999)`
- `UNIQUE(lista_id, produto_id)`

---

### 🏪 Tabela: `categorias` ⭐ NORMALIZADO v3.2

| Campo         | Tipo         | Constraints                  | Descrição          |
| ------------- | ------------ | ---------------------------- | -------------------- |
| `id`        | INT          | **PK**, AUTO_INCREMENT | Identificador único |
| `nome`      | VARCHAR(100) | **UNIQUE**, NOT NULL   | Nome da categoria    |
| `descricao` | TEXT         | NULL                         | Descrição opcional |

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

| Campo         | Tipo         | Constraints                  | Descrição              |
| ------------- | ------------ | ---------------------------- | ------------------------ |
| `id`        | INT          | **PK**, AUTO_INCREMENT | Identificador único     |
| `nome`      | VARCHAR(150) | NOT NULL                     | Nome do fornecedor       |
| `cnpj`      | VARCHAR(18)  | **UNIQUE**, NOT NULL   | CNPJ formatado           |
| `ativo`     | BOOLEAN      | NOT NULL, DEFAULT TRUE       | Situação do fornecedor |
| `criado_em` | DATETIME     | NOT NULL, DEFAULT NOW()      | Data de criação        |

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

| Campo             | Tipo | Constraints                | Descrição                       |
| ----------------- | ---- | -------------------------- | --------------------------------- |
| `fornecedor_id` | INT  | **FK**, **PK** | Referência a`fornecedores(id)` |
| `categoria_id`  | INT  | **FK**, **PK** | Referência a`categorias(id)`   |

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

| Campo         | Tipo         | Constraints                  | Descrição                      |
| ------------- | ------------ | ---------------------------- | -------------------------------- |
| `id`        | INT          | **PK**, AUTO_INCREMENT | Identificador único             |
| `nome`      | VARCHAR(200) | NOT NULL                     | Nome do produto                  |
| `unidade`   | VARCHAR(10)  | NOT NULL                     | Unidade de medida (un, kg, L, m) |
| `ativo`     | BOOLEAN      | NOT NULL, DEFAULT TRUE       | Situação do produto            |
| `criado_em` | DATETIME     | NOT NULL, DEFAULT NOW()      | Data de criação                |

**Constraints:**

- `PK(id)`
- `INDEX(nome)`

**Seed:** 50 produtos (agnósticos à categoria)

---

### 🏪 Tabela: `fornecedores_produtos` ⭐ NORMALIZADO v3.2

| Campo             | Tipo          | Constraints                | Descrição                       |
| ----------------- | ------------- | -------------------------- | --------------------------------- |
| `fornecedor_id` | INT           | **FK**, **PK** | Referência a`fornecedores(id)` |
| `produto_id`    | INT           | **FK**, **PK** | Referência a`produtos(id)`     |
| `preco`         | DECIMAL(10,2) | NOT NULL                   | Preço unitário                  |
| `estoque`       | INT           | NOT NULL, DEFAULT 0        | Estoque disponível               |
| `ativo`         | BOOLEAN       | NOT NULL, DEFAULT TRUE     | Situação do vínculo            |

**Constraints:**

- `PK(fornecedor_id, produto_id)` — composta
- `FK(fornecedor_id) → fornecedores(id) ON DELETE CASCADE`
- `FK(produto_id) → produtos(id) ON DELETE RESTRICT`
- `CHECK(preco >= 0)`
- `CHECK(estoque >= 0)`

**Seed:** ~300 preços (variação ±20%)

---

## 🔗 5. RELACIONAMENTOS (CARDINALIDADES)

| Origem           | → | Destino                   | Cardinalidade | Constraint                            |
| ---------------- | -- | ------------------------- | ------------- | ------------------------------------- |
| `usuarios`     | → | `listas`                | 1:N           | FK`usuario_id` ON DELETE CASCADE    |
| `listas`       | → | `itens_lista`           | 1:N           | FK`lista_id` ON DELETE CASCADE      |
| `produtos`     | → | `itens_lista`           | 1:N           | FK`produto_id` ON DELETE RESTRICT   |
| `fornecedores` | ↔ | `categorias`            | N:N           | Via`fornecedores_categorias`        |
| `fornecedores` | → | `fornecedores_produtos` | 1:N           | FK`fornecedor_id` ON DELETE CASCADE |
| `produtos`     | → | `fornecedores_produtos` | 1:N           | FK`produto_id` ON DELETE RESTRICT   |

---

## 🔒 6. VALIDAÇÃO ACID

| Princípio            | Garantia no DER                                                              |
| --------------------- | ---------------------------------------------------------------------------- |
| **Atomicity**   | Transações explícitas via`BEGIN/COMMIT` em todas operações de escrita |
| **Consistency** | FKs com CASCADE/RESTRICT, CHECK constraints, UNIQUE                          |
| **Isolation**   | InnoDB permite leitura concorrente sem bloqueio (MVCC)                       |
| **Durability**  | MySQL InnoDB grava em disco com redo log automático                         |

---

## 📊 7. ESTATÍSTICAS FINAIS

| Métrica            | Valor                                 |
| ------------------- | ------------------------------------- |
| Total de tabelas    | 8                                     |
| Primary Keys        | 8 (todas simples, exceto 2 compostas) |
| Foreign Keys        | 9                                     |
| Constraints UNIQUE  | 4                                     |
| Constraints CHECK   | 5                                     |
| Relacionamentos 1:N | 5                                     |
| Relacionamentos N:N | 1 (via pivô)                         |
| Soft deletes        | 2 (`usuarios`, `listas`)          |
| Índices compostos  | 2                                     |

---

## 📦 8. SEED DE DADOS

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

## ✅ 9. CHECKLIST DE VALIDAÇÃO

- [X] 8 tabelas conforme especificação v3.2
- [X] Tabela pivô `fornecedores_categorias` presente (N:N)
- [X] `produtos` SEM FK para `categorias` (correção conceitual)
- [X] Todas PKs, FKs, UNIQUE, CHECK visíveis
- [X] Cardinalidades 1:N e N:N corretas
- [X] Soft delete em `usuarios` e `listas` (`deletado_em`)
- [X] Seed documentado (10 forn + 50 prod + 11 cat)
- [X] MySQL InnoDB configurado (ACID)
- [X] Legenda completa com ícones 🔑 🔗
- [X] Normalização PT-BR completa
- [X] Histórico de mudanças documentado

---

<a id="doc04"></a>

# 📄 DOC-04 — RELATÓRIO ANALÍTICO COBECO (PROPÓSITO GERAL)

**Versão:** 3.2 | **Data:** 14/09/2026 | **Status:** ✅ APROVADO
**Cross-ref:** UCs em [DOC-01](#doc01) | Requisitos em [DOC-02](#doc02) | DER em [DOC-03](#doc03)

---

## 📜 1. HISTÓRICO DE MUDANÇAS

| Versão        | Data                 | Mudança Principal                                                     | Impacto                    |
| -------------- | -------------------- | ---------------------------------------------------------------------- | -------------------------- |
| v1.0           | Ago/2026             | MVP sem auth, SQLite3, CSV, 14 RFs                                     | Baseline                   |
| v2.0           | 31/08/2026           | Auth adicionada, tabela flat, 16 RFs                                   | +5 RFs                     |
| v2.1           | 01/09/2026           | Seleção/filtro fornecedores (RF11-12)                                | +2 RFs                     |
| v3.0           | 12/09/2026           | Primeira análise crítica, 26 UCs                                     | Revisão completa          |
| v3.1           | 12/09/2026           | DER com`supplier_categories` (N:N)                                   | Correção conceitual      |
| **v3.2** | **14/09/2026** | **MySQL InnoDB, PDF server-side, pré-filtro categorias, PT-BR** | **Stack + UX + DER** |

### 1.1 Mudanças Consolidadas v3.1 → v3.2

| Mudança                    | Impacto                      | Status |
| --------------------------- | ---------------------------- | ------ |
| MySQL InnoDB (não SQLite3) | ADR-003 revisado             | ✅     |
| Exportação PDF (não CSV) | ADR-005 revisado + UC29 novo | ✅     |
| Pré-filtro por categorias  | UC03 novo + UC04 ajustado    | ✅     |
| Normalização PT-BR        | Todas entidades e atributos  | ✅     |
| 11 categorias macro         | Seed atualizado              | ✅     |
| Todas relações nomeadas   | 21 rótulos descritivos      | ✅     |

---

## 🎯 2. DECISÕES ARQUITETURAIS CONSOLIDADAS (ADRs)

### 2.1 Matriz de Aprovação

| ADR               | Decisão                                             | Status                  | Princípio        | Esforço |
| ----------------- | ---------------------------------------------------- | ----------------------- | ----------------- | -------- |
| ADR-001           | Frontend Vanilla JS + ES6 Modules                    | ✅ APROVADO             | KISS + YAGNI      | Baixo    |
| ADR-002           | Backend FastAPI (Python 3.12)                        | ✅ APROVADO             | SDD + KISS        | Baixo    |
| **ADR-003** | **MySQL InnoDB** ⭐                            | ✅ APROVADO             | KISS + ACID       | Zero     |
| ADR-004           | JWT Stateless (access memória + refresh httpOnly)   | ✅ APROVADO COM AJUSTES | KISS + Segurança | Médio   |
| **ADR-005** | **Export PDF Server-Side (ReportLab)** ⭐      | ✅ APROVADO             | KISS + YAGNI      | Médio   |
| ADR-006           | Recuperação de Senha — Dupla Via (log + pergunta) | ✅ APROVADO COM AJUSTES | KISS + YAGNI      | Baixo    |

### 2.2 Detalhamento dos ADRs

#### 🔵 ADR-001: Frontend sem Framework

| Aspecto                  | Detalhe                                                                                                                 |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| **Contexto**       | MVP acadêmico, sem necessidade de reatividade complexa                                                                 |
| **Decisão**       | HTML5 + CSS3 + Tailwind (CDN) + Vanilla JS com ES6 Modules (`type="module"`)                                          |
| **Justificativa**  | Zero build step, zero npm, zero bundler. Aprendizado máximo. Deploy trivial.                                           |
| **Consequências** | Código mais verboso, sem reatividade automática. Compensado com funções`render()` explícitas.                    |
| **Estrutura**      | 8 módulos ES6:`app.js`, `state.js`, `api.js`, `auth.js`, `list.js`, `compare.js`, `export.js`, `ui.js` |

#### 🔵 ADR-002: Backend com FastAPI

| Aspecto                  | Detalhe                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| **Contexto**       | Python + OpenAPI-first (SDD nativo)                                                        |
| **Decisão**       | FastAPI como framework web, Pydantic para validação                                      |
| **Justificativa**  | Gera OpenAPI automaticamente em`/openapi.json`. Async nativo. Mais KISS que Django.      |
| **Consequências** | Clean Architecture não é enforceada pelo framework — disciplina manual via code review. |
| **Estrutura**      | 4 camadas:`domain/` → `usecases/` → `adapters/` → `routers/`                    |

#### 🔵 ADR-003: MySQL InnoDB ⭐ REVISADO v3.2

| Aspecto                  | Detalhe                                                                                         |
| ------------------------ | ----------------------------------------------------------------------------------------------- |
| **Contexto**       | Banco robusto, ACID, servidor dedicado                                                          |
| **Decisão**       | MySQL 8.0+ com engine InnoDB, charset utf8mb4, collation utf8mb4_unicode_ci                     |
| **Justificativa**  | ACID garantido. Multi-writer. Melhor suporte a concorrência. Mais robusto para MVP acadêmico. |
| **Consequências** | Requer container Docker separado. Mais configuração que SQLite3.                              |
| **Configuração** | `innodb_buffer_pool_size=256M`, `max_connections=100`, volume `./data:/var/lib/mysql`     |

#### 🔵 ADR-004: JWT Stateless com Ajustes de Segurança

| Aspecto                         | Detalhe                                                                                                |
| ------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Contexto**              | API stateless, sem tabela de sessões, sem Redis                                                       |
| **Decisão**              | JWT via`python-jose`: Access Token (15min, em memória JS) + Refresh Token (7 dias, cookie httpOnly) |
| **Justificativa**         | Stateless = alinhado com Clean Architecture. YAGNI para Redis.                                         |
| **Ajustes de Segurança** | Access em memória (não localStorage) → imune a XSS. Refresh com`SameSite=Strict` → imune a CSRF. |
| **Rate Limiting**         | 6 tentativas consecutivas → lockout 15min (anti-DDoS)                                                 |

#### 🔵 ADR-005: Export PDF Server-Side ⭐ REVISADO v3.2

| Aspecto                  | Detalhe                                                                                        |
| ------------------------ | ---------------------------------------------------------------------------------------------- |
| **Contexto**       | Exportação profissional para apresentação acadêmica                                       |
| **Decisão**       | Geração server-side via ReportLab (Python). Endpoint`POST /api/export/pdf`.                |
| **Justificativa**  | PDF tem valor estratégico para apresentação acadêmica e uso profissional. Tradeoff aceito. |
| **Consequências** | Requer ReportLab no backend. Geração em <5s para listas até 100 itens.                      |
| **Fallback**       | Se ReportLab falhar, fallback para impressão via navegador.                                   |

#### 🔵 ADR-006: Recuperação de Senha — Dupla Via

| Aspecto                  | Detalhe                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| **Contexto**       | MVP acadêmico sem serviço de email                                                       |
| **Decisão**       | Via A: Token logado no stdout (dev). Via B: Pergunta de segurança (produção acadêmica) |
| **Justificativa**  | KISS + utilizável em demo real. Toggle via`RECOVERY_MODE` env var.                      |
| **Consequências** | Documentar como limitação conhecida. Não utilizável em produção real.                |

---

## 🛠️ 3. STACK TECNOLÓGICA DEFINITIVA

### 3.1 Matriz de Tecnologias

| Camada           | Tecnologia                                               | Versão       | Justificativa              |
| ---------------- | -------------------------------------------------------- | ------------- | -------------------------- |
| Frontend         | HTML5 + CSS3 + Tailwind (CDN) + Vanilla JS (ES6 modules) | —            | KISS + YAGNI               |
| Backend          | Python + FastAPI + Pydantic + Pydantic-Settings          | 3.12 / 0.110+ | SDD nativo                 |
| **Banco**  | **MySQL InnoDB** ⭐                                | 8.0+          | ACID + robustez            |
| Auth             | python-jose (JWT) + bcrypt                               | Latest        | Stateless + seguro         |
| **Export** | **ReportLab (server-side)** ⭐                     | Latest        | PDF profissional           |
| CI/CD            | Docker + Docker Compose + GitHub Actions                 | Latest        | Reprodutibilidade          |
| Seed             | Script Python no entrypoint do container                 | —            | 10 forn + 50 prod + 11 cat |
| Kanban           | GitHub Projects (5 colunas)                              | —            | Gestão ágil              |
| Testes           | pytest + pytest-cov                                      | Latest        | Cobertura ≥80%            |
| Lint             | ruff                                                     | Latest        | Qualidade de código       |

### 3.2 Diagrama da Stack

```
┌─────────────────────────────────────────────────────┐
│              BROWSER (Desktop ≥1024px)              │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │  HTML5   │  │ Tailwind │  │  JS (ES6 Modules) │  │
│  │  (Telas) │  │  (CDN)   │  │  (Lógica + DOM)   │  │
│  └─────┬────┘  └────┬─────┘  └────────┬──────────┘  │
│        └────────────┼─────────────────┘             │
│                     │ fetch()                       │
└─────────────────────┼───────────────────────────────┘
                      │ HTTP/JSON
                      ▼
┌───────────────────────────────────────────────────────┐
│                  DOCKER COMPOSE                       │
│  ┌────────────────────────────────────────────────┐   │
│  │            FastAPI (Python 3.12)               │   │
│  │  ┌─────────┐ ┌──────────┐ ┌───────────────┐    │   │
│  │  │ Routers │ │ UseCases │ │   Domain      │    │   │
│  │  │ (API)   │ │ (Logic)  │ │   (Entities)  │    │   │
│  │  └────┬────┘ └────┬─────┘ └───────┬───────┘    │   │
│  │       └───────────┼───────────────┘            │   │
│  │                   │                            │   │
│  │  ┌────────────────▼────────────────────────┐   │   │
│  │  │       Adapters (MySQL / Pydantic)       │   │   │
│  │  └────────────────┬────────────────────────┘   │   │
│  └───────────────────┼────────────────────────────┘   │
│                      │                                │
│  ┌───────────────────▼────────────────────────────┐   │
│  │          MySQL 8.0 (InnoDB + UTF-8)            │   │
│  │   usuarios | listas | itens_lista | produtos | │   │
│  │   fornecedores | categorias |                  │   │
│  │        fornecedores_categorias |               │   │
│  │       fornecedores_produtos                    │   │
│  └────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────┘
```

---

## 📁 	

### 4.1 Layout de Diretórios

```
COBECO/
├── .git/
├── .gitignore
├── .env.example
├── README.md
├── docker-compose.yml
├── Dockerfile
├── Makefile # seed, test, run, lint, sdd-cycle
│
├── src/ # Código-fonte da aplicação (Clean Architecture)
│ ├── backend/ # 🐍 Python FastAPI
│ │ ├── main.py # FastAPI app + CORS + static mount
│ │ ├── config.py # Settings via pydantic-settings
│ │ ├── domain/ # 🟢 Camada de Domínio (pura, sem deps externas)
│ │ │ ├── entities.py # Dataclasses: Usuario, Lista, Produto, Fornecedor
│ │ │ ├── rules.py # Regras de negócio puras (agrupamento, cálculo)
│ │ │ └── exceptions.py # Domain exceptions
│ │ ├── usecases/ # 🔵 Camada de Casos de Uso (Orquestração)
│ │ │ ├── auth_usecase.py
│ │ │ ├── list_usecase.py
│ │ │ ├── compare_usecase.py
│ │ │ └── export_usecase.py
│ │ ├── adapters/ # 🟡 Camada de Adaptadores (Infraestrutura)
│ │ │ ├── database.py # MySQL connection + InnoDB
│ │ │ ├── repositories.py # CRUD operations (Repository pattern)
│ │ │ ├── schemas.py # Pydantic models (request/response)
│ │ │ └── security.py # bcrypt, JWT, rate limiter
│ │ ├── routers/ # 🔴 Camada de Framework (API Endpoints)
│ │ │ ├── auth_router.py
│ │ │ ├── list_router.py
│ │ │ ├── compare_router.py
│ │ │ └── catalog_router.py
│ │ └── seed.py # Script de seed (10 forn + 50 prod + 11 cat)
│ │
│ └── frontend/ # 🌐 Vanilla JS + HTML (Servido como static)
│ ├── index.html # Tela de entrada: Selecionar Categorias
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html # Minhas Listas
│ ├── compare.html # Seleção + Comparação
│ ├── profile.html
│ ├── css/
│ │ └── style.css # Customizações + @media print
│ └── js/
│ ├── app.js # Entry point + router simples
│ ├── state.js # AppState + sessionStorage
│ ├── api.js # fetch() wrappers (consome OpenAPI)
│ ├── auth.js # Login/logout/register
│ ├── list.js # CRUD de listas
│ ├── compare.js # Seleção + motor de comparação
│ ├── export.js # PDF via API
│ └── ui.js # Toasts, modais, render helpers
│
├── tests/ # Testes automatizados
│ ├── backend/
│ │ ├── conftest.py
│ │ ├── test_domain_rules.py
│ │ ├── test_auth.py
│ │ ├── test_list.py
│ │ └── test_compare.py
│ └── frontend/ # Testes de lógica JS (opcional no MVP, mas SDD-compliant)
│ └── test_ui_logic.js
│
├── docs/ # Documentação HUMANA (não lida pela IA)
│ ├── project-plan.md
│ ├── roadmap.md
│ ├── meeting-notes/
│ └── decisions/ # ADRs humanos (ex: ADR-001 a ADR-006)
│
├── .ai/ # CONTEXTO DA IA (versionado, lido pelo OpenCode/LLM)
│ ├── prompts/
│ │ ├── _base.md
│ │ ├── coder.md
│ │ ├── reviewer.md
│ │ ├── tester.md
│ │ ├── pm.md
│ │ └── active.md → (symlink ou cópia de coder.md para contexto ativo)
│ │
│ ├── specs/ # Especificações que guiam a geração de código
│ │ ├── coding-standards.md # Regras de Clean Arch + PT-BR + Type hints
│ │ ├── api-contracts.md # Resumo/Link do openapi.json (SDD Contract)
│ │ ├── domain-rules.md # Regras de negócio (ex: categorias são de fornecedores)
│ │ └── architecture.md # ADRs técnicos que afetam código (MySQL, JWT, ReportLab)
│ │
│ ├── handoffs/ # Rastro do ciclo SDD (Spec → Code → Review → Test)
│ │ ├── 001-setup-infra-spec.md
│ │ ├── 001-setup-infra-code.md
│ │ ├── 001-setup-infra-review.md
│ │ └── 001-setup-infra-test.md
│ │
│ └── workflows/
│ └── sdd-cycle.sh # Script para orquestrar spec -> code -> review -> test
│
├── openapi/
│ └── openapi.json # Exportado via /openapi.json (Single Source of Truth da API)
│
├── .github/
│ ├── workflows/
│ │ └── ci.yml # lint → test → build (Validação SDD automática)
│ └── projects/ # Kanban configurado
│
└── .obsidian/ # Configuração do vault (opcional, para gestão de conhecimento)
└── workspace.json
```

### 4.2 Regras de Clean Architecture

| Camada   | Pode depender de   | Não pode depender de       |
| -------- | ------------------ | --------------------------- |
| Domain   | Nada (pura)        | UseCases, Adapters, Routers |
| UseCases | Domain             | Adapters, Routers           |
| Adapters | Domain, UseCases   | Routers                     |
| Routers  | UseCases, Adapters | Domain diretamente          |

---

## 📅 5. PLANO DE IMPLEMENTAÇÃO — 30 DIAS

### 5.1 Cronograma de Sprints

| Sprint | Dias   | Foco                       | Entregáveis                                                                          | RFs                    |
| ------ | ------ | -------------------------- | ------------------------------------------------------------------------------------- | ---------------------- |
| S1     | 1–6   | Setup + Auth               | Docker (app + MySQL), seed, OpenAPI, login/cadastro/logout, recuperação (dupla via) | RF01–RF04             |
| S2     | 7–12  | Listas + Catálogo         | CRUD listas, autocomplete, persistência, categorias de fornecedores                  | RF07–RF11             |
| S3     | 13–18 | Pré-filtro + Comparação | Seleção categorias, seleção fornecedores, motor flat, resultados                  | RF12–RF16             |
| S4     | 19–24 | Export + Perfil + Polish   | PDF server-side, impressão, perfil, testes 80%                                       | RF05, RF06, RF17–RF18 |
| S5     | 25–30 | Buffer + Demo              | Bug fixes, documentação, apresentação, deploy                                     | Todos                  |

### 5.2 Kanban — GitHub Projects (5 Colunas)

| Coluna         | Labels               | Critério de Entrada           | Critério de Saída       |
| -------------- | -------------------- | ------------------------------ | ------------------------- |
| 📋 Backlog     | `P1`, `P2`       | Requisito aprovado no SSOT     | Priorizado para sprint    |
| 🎯 Sprint      | `P0`, `sprint-N` | Sprint planning realizado      | Desenvolvimento iniciado  |
| 🔨 In Progress | `in-progress`      | Branch criada (`feat/UC-XX`) | PR aberto                 |
| 👀 Review      | `review`           | PR aberto + CI verde           | Aprovado por ≥1 reviewer |
| ✅ Done        | `done`             | Merge em`main`               | Deploy em staging         |

### 5.3 Convenções de Branch

| Tipo    | Padrão             | Exemplo                     |
| ------- | ------------------- | --------------------------- |
| Feature | `feat/UC-XX-nome` | `feat/UC-03-categorias`   |
| Fix     | `fix/issue-XX`    | `fix/issue-12-rate-limit` |
| Docs    | `docs/nome`       | `docs/openapi-spec`       |
| Release | `release/vX.Y`    | `release/v1.0`            |

---

## 🎯 6. MATRIZ DE RISCOS E MITIGAÇÕES

### 6.1 Riscos Técnicos

| #  | Risco                                   | Prob.  | Impacto | Mitigação                                         |
| -- | --------------------------------------- | ------ | ------- | --------------------------------------------------- |
| R1 | Vanilla JS vira "spaghetti"             | Alta   | Médio  | Módulos ES6 + funções puras + code review        |
| R2 | MySQL corrompe                          | Baixa  | Alto    | InnoDB + volume Docker + backup diário             |
| R3 | JWT access token vazado                 | Média | Alto    | Expiry curto (15min) + memória (não localStorage) |
| R4 | Categoria mal interpretada              | Baixa  | Médio  | Documentação: "categorias são de FORNECEDORES"   |
| R5 | Recuperação de senha não utilizável | Alta   | Baixo   | Dupla via (log + pergunta de segurança)            |
| R6 | Clean Architecture não respeitada      | Média | Alto    | Code review rigoroso + lint rules                   |
| R7 | Alunos não conhecem Python             | Média | Alto    | FastAPI é intuitivo;`/docs` automático          |
| R8 | PDF generation lenta (>5s)              | Baixa  | Médio  | Timeout 10s + fallback para impressão              |

### 6.2 Riscos de Escopo

| #   | Risco                           | Prob.  | Impacto | Mitigação                                         |
| --- | ------------------------------- | ------ | ------- | --------------------------------------------------- |
| R10 | Scope creep (novos RFs)         | Alta   | Alto    | SSOT congelado; mudanças via ADR complementar      |
| R11 | Prazo estourado                 | Média | Alto    | Sprint 5 como buffer; P1 cortável                  |
| R12 | Professor exige "mais robustez" | Baixa  | Alto    | Clean Architecture + testes 80% + OpenAPI compensam |

---

## 📋 7. RECOMENDAÇÕES OPERACIONAIS

### 7.1 ✅ Fazer (Aprovar Imediatamente)

| # | Ação                                                                    | Responsável | Justificativa                 |
| - | ------------------------------------------------------------------------- | ------------ | ----------------------------- |
| 1 | Implementar DER v3.2 com tabela pivô`fornecedores_categorias`          | Dev + DBA    | Alinhamento com domínio real |
| 2 | Adotar todos os ADRs com ajustes propostos                                | Tech Lead    | Consistência arquitetural    |
| 3 | Estruturar frontend em módulos ES6 (um módulo por funcionalidade)       | Frontend Dev | KISS + manutenibilidade       |
| 4 | Usar Pydantic para TODA validação (request/response/entidades)          | Backend Dev  | Type-safety + SDD             |
| 5 | Documentar OpenAPI antes de implementar cada endpoint (SDD)               | Arquiteto    | Contrato antes do código     |
| 6 | Testes unitários ≥80% focados em regras de negócio (domain + usecases) | QA + Dev     | Qualidade garantida           |
| 7 | Criar repositório GitHub + Project Kanban                                | Tech Lead    | Gestão ágil                 |
| 8 | Setup Docker Compose (app + MySQL) + FastAPI skeleton                     | Dev          | Reprodutibilidade             |

### 7.2 ⚠️ Fazer com Disciplina

| # | Ação                                             | Guard-Rail           | Consequência se Violado |
| - | -------------------------------------------------- | -------------------- | ------------------------ |
| 1 | Clean Architecture em 4 camadas                    | Code review rigoroso | PR rejeitado             |
| 2 | Parameterized queries em TODAS operações MySQL   | Zero exceções      | Vulnerabilidade SQLi     |
| 3 | JWT access em memória (não localStorage)         | Segurança           | Vulnerabilidade XSS      |
| 4 | Rate limiting em todos endpoints sensíveis        | Auth, recovery       | Vulnerabilidade DDoS     |
| 5 | Contrato OpenAPI escrito ANTES de implementar      | SDD                  | Retrabalho               |
| 6 | Módulos ES6 — um módulo por tela/funcionalidade | Frontend             | Código bagunçado       |

### 7.3 ❌ Evitar (YAGNI)

| # | Item                                               | Justificativa                                        |
| - | -------------------------------------------------- | ---------------------------------------------------- |
| 1 | React, Vue, Angular ou qualquer framework frontend | MVP acadêmico não precisa de virtual DOM           |
| 2 | ORM pesado (SQLAlchemy)                            | Usar MySQL stdlib + Repository pattern               |
| 3 | Redis, Memcached ou qualquer cache externo         | MySQL InnoDB é suficiente                           |
| 4 | Serviço de email para recuperação de senha      | Dupla via (log + pergunta)                           |
| 5 | Microserviços                                     | Monólito modular é suficiente                      |
| 6 | Suporte mobile                                     | Desktop-only (≥1024px)                              |
| 7 | TypeScript no frontend                             | Stack já simplificada; Pydantic no backend compensa |
| 8 | BDD/E2E tests no MVP                               | Testes unitários 80% são suficientes               |
| 9 | Persistência de comparações                     | Apenas listas são persistidas                       |

---

## ✅ 8. CRITÉRIOS DE ACEITE DO MVP

### 8.1 Critérios Funcionais

| #  | Critério                                                                                                   | Verificação      |
| -- | ----------------------------------------------------------------------------------------------------------- | ------------------ |
| C1 | Usuário consegue criar lista, selecionar categorias, selecionar fornecedores, comparar e ver melhor oferta | Demo ao vivo       |
| C2 | Fluxo completo (cadastro → comparação) em <5 minutos                                                     | Cronometrado       |
| C3 | Export PDF funciona para visitantes E autenticados                                                          | Teste manual       |
| C4 | Impressão otimizada para A4 via Ctrl+P                                                                     | Teste manual       |
| C5 | Rate limiting bloqueia após 6 tentativas                                                                   | Teste automatizado |

### 8.2 Critérios Técnicos

| #   | Critério                                      | Métrica             |
| --- | ---------------------------------------------- | -------------------- |
| C6  | Cobertura de testes ≥80%                      | pytest --cov         |
| C7  | API <500ms p95                                 | curl + time          |
| C8  | Zero vulnerabilidades críticas (OWASP Top 10) | Code review          |
| C9  | ACID garantido (zero dados órfãos)           | Teste de transação |
| C10 | OpenAPI 100% documentado                       | `/docs` acessível |

### 8.3 Critérios de Qualidade

| #   | Critério                                     | Verificação  |
| --- | --------------------------------------------- | -------------- |
| C11 | Clean Architecture respeitada                 | Code review    |
| C12 | Parameterized queries em 100% das operações | Grep + review  |
| C13 | JWT access em memória (não localStorage)    | Code review    |
| C14 | Seed popula DB em <10s                        | `make seed`  |
| C15 | Pipeline CI <5min                             | GitHub Actions |

---

## 📊 9. ESTATÍSTICAS FINAIS DO PROJETO

| Métrica                          | Valor                                     |
| --------------------------------- | ----------------------------------------- |
| **Total de UCs**            | 29 (19 principais + 10 internos)          |
| **Total de RFs**            | 18                                        |
| **Total de RNFs**           | 12                                        |
| **Total de RDs**            | 9                                         |
| **Total de ADRs**           | 6                                         |
| **Total de tabelas**        | 8                                         |
| **Total de relações UML** | 21 (16`<<include>>` + 5 `<<extend>>`) |
| **Total de happy paths**    | 38                                        |
| **Total de exceções**     | 57                                        |
| **Total de edge-cases**     | 60+                                       |
| **Prazo**                   | 30 dias (5 sprints)                       |
| **Cobertura de testes**     | ≥80%                                     |

---

## 📋 10. PRÓXIMOS PASSOS IMEDIATOS

| # | Ação                                              | Responsável | Prazo    | Status |
| - | --------------------------------------------------- | ------------ | -------- | ------ |
| 1 | Aprovar este pacote documental (4 documentos)       | Stakeholders | Dia 1    | ⏳     |
| 2 | Criar repositório GitHub + Project Kanban          | Tech Lead    | Dia 1    | ⏳     |
| 3 | Gerar contrato OpenAPI 3.0 (SDD)                    | Arquiteto    | Dia 2–3 | ⏳     |
| 4 | Setup Docker Compose (app + MySQL)                  | Dev          | Dia 2–3 | ⏳     |
| 5 | Implementar`seed.py` (10 forn + 50 prod + 11 cat) | Dev          | Dia 3–4 | ⏳     |
| 6 | Diagrama de Transição de Estados                  | Arquiteto    | Dia 4–5 | ⏳     |
| 7 | Protótipo de Baixa Fidelidade (10 telas)           | UX/Dev       | Dia 6–7 | ⏳     |
| 8 | Iniciar Sprint 1 (Setup + Auth)                     | Dev          | Dia 8    | ⏳     |

---

## 🏛️ 11. GOVERNANÇA E COMUNICAÇÃO

### 11.1 Papéis e Responsabilidades

| Papel                                     | Responsabilidade                             |
| ----------------------------------------- | -------------------------------------------- |
| Product Owner (Thais Cristina Casagrande) | Aprovar escopo, validar entregas, demo final |
| Tech Lead                                 | Code review, decisões técnicas, mentoring  |
| Arquiteto de Software                     | ADRs, DER, UCD, OpenAPI                      |
| Dev Frontend                              | HTML/CSS/JS, módulos ES6, UX                |
| Dev Backend                               | FastAPI, MySQL, regras de negócio           |
| QA                                        | Testes unitários, cobertura 80%             |

### 11.2 Rituais Ágeis

| Ritual          | Frequência     | Duração |
| --------------- | --------------- | --------- |
| Daily Standup   | Diário         | 15min     |
| Sprint Planning | Semanal (sexta) | 1h        |
| Sprint Review   | Semanal (sexta) | 15min     |
| Retrospectiva   | Semanal (sexta) | 30min     |

### 11.3 Canais de Comunicação

- **GitHub:** Repositório oficial + Issues + Projects (Kanban)
- **GitHub Actions:** CI/CD pipeline
- **WhatsApp:** Grupo do projeto para comunicação rápida
- **Documentação:** README.md + `/docs` (Swagger)

---

## ✅ 12. CONCLUSÃO E APROVAÇÃO

### 12.1 Síntese das Decisões

✅ **DER v3.2** com tabela pivô `fornecedores_categorias` — categorias são de FORNECEDORES (N:N)
✅ **Stack minimalista** — HTML/JS + Python/FastAPI + MySQL InnoDB + Docker
✅ **6 ADRs aprovados** com ajustes de segurança e usabilidade
✅ **Clean Architecture** em 4 camadas com disciplina rigorosa
✅ **SDD** via OpenAPI nativo do FastAPI
✅ **ACID** via MySQL InnoDB
✅ **30 dias** de desenvolvimento em 5 sprints
✅ **8 tabelas** no banco de dados
✅ **18 RFs + 12 RNFs + 9 RDs** cobertos
✅ **Kanban** no GitHub Projects
✅ **Normalização PT-BR** completa
✅ **PDF server-side** (ReportLab)
✅ **Pré-filtro por categorias** (11 categorias macro)

### 12.2 Princípios Aplicados

| Princípio                   | Como foi aplicado                                                          |
| ---------------------------- | -------------------------------------------------------------------------- |
| **KISS**               | Stack simples, zero frameworks, zero cache externo, zero microserviços    |
| **YAGNI**              | Sem email real, sem mobile, sem BDD, sem persistência de comparações    |
| **SDD**                | OpenAPI antes do código, Pydantic para validação, contratos versionados |
| **Clean Architecture** | 4 camadas ortogonais, dependência apenas para dentro                      |
| **ACID**               | MySQL InnoDB + transações explícitas + foreign keys                     |

### 12.3 Veredito Final

> **O projeto COBECO MVP v3.2 está COMPLETO, CONSISTENTE e APROVADO para implementação.**
>
> Todas as decisões arquiteturais foram validadas, os riscos identificados e mitigados, e o cronograma é realista para 30 dias de desenvolvimento.
>
> A stack minimalista (HTML/JS + Python/FastAPI + MySQL InnoDB) combinada com Clean Architecture rigorosa e SDD via OpenAPI garante:
>
> - ✅ Aprendizado máximo para MVP acadêmico
> - ✅ Qualidade técnica (testes 80%, ACID, segurança)
> - ✅ Entregabilidade (30 dias, 5 sprints)
> - ✅ Demonstrabilidade (1 comando: `docker compose up`)

---

## 📝 13. ASSINATURAS DE APROVAÇÃO

| Papel                 | Nome                                | Data        | Status        |
| --------------------- | ----------------------------------- | ----------- | ------------- |
| Product Owner         | **THAIS CRISTINA CASAGRANDE** | ___/09/2026 | ⏳ Aguardando |
| Tech Lead             | _________________________           | ___/09/2026 | ⏳ Aguardando |
| Arquiteto de Software | _________________________           | ___/09/2026 | ⏳ Aguardando |
| Dev Frontend          | _________________________           | ___/09/2026 | ⏳ Aguardando |
| Dev Backend           | _________________________           | ___/09/2026 | ⏳ Aguardando |

---

> *"A simplicidade é a sofisticação suprema."* — Leonardo da Vinci
> *"Make it work, make it right, make it fast."* — Kent Beck
> *"You aren't gonna need it."* — Ron Jeffries

---

## 📚 FIM DO PACOTE DOCUMENTAL — COBECO MVP v3.2

**Próxima Ação Imediata:** Aprovação dos 4 documentos e início da Sprint 1 (Setup MySQL + Auth).

---

## 📊 RESUMO EXECUTIVO DO PACOTE

| Documento        | Propósito                               | Status                            |
| ---------------- | ---------------------------------------- | --------------------------------- |
| **DOC-01** | Análise de Casos de Uso e Consistência | ✅ 29 UCs, 21 relações nomeadas |
| **DOC-02** | Análise de Requisitos e Consistência   | ✅ 18 RFs, 12 RNFs, 9 RDs         |
| **DOC-03** | Análise da Camada de Dados (DER)        | ✅ 8 tabelas PT-BR, MySQL InnoDB  |
| **DOC-04** | Relatório Analítico COBECO (Geral)     | ✅ 6 ADRs, stack, cronograma      |

**Total de artefatos documentados:**

- 29 Casos de Uso
- 18 Requisitos Funcionais
- 12 Requisitos Não Funcionais
- 9 Requisitos Desejáveis
- 6 Decisões Arquiteturais
- 8 Tabelas no Banco de Dados
- 21 Relações UML nomeadas
- 38 Happy Paths
- 57 Exceções
- 60+ Edge-Cases
- 30 dias de cronograma
- 5 sprints planejados
