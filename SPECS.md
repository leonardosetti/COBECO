# SPECS — COBECO MVP v3.2

**Projeto:** COBECO — Comparador de Bens de Consumo  
**Versão:** 3.2 (SSOT)  
**Data:** 2026-09-14  
**Base:** Protótipos Alta Fidelidade (doc-prototype-0001/0002/0003, doc-figma-0001) + Requisitos (req-func-0001) + Casos de Uso (req-use-case-0001) + DER

---

## 1. VISÃO GERAL DO FLUXO

```
Visitante → [Categorias] → [Lista em Memória] → [Fornecedores] → [Comparação] → [Lista Vencedora/PDF]
                    ↑              ↑                 ↑              ↑                ↑
               UC03/RF12    UC01/UC02/RF07    UC04/UC05/RF13  UC06/UC07/RF15  UC08/RF17
                                                                     RF16
                              ↓
                    [Login/Salvar] → [Dashboard/Minhas Listas] → [Perfil]
                         UC10/UC17/RF08       UC15/RF09             UC16/UC18/RF05
                                                                      RF06
```

**Persona:** Mariana Duarte, 34 — dona do restaurante "Tempero da Mari" (Taquaritinga/SP). Compra semanal de insumos em 3 mercados.

---

## 2. TELAS / PASSOS (5 + Auth + Dashboard + Perfil)

### 2.1 Passo 1 — Categorias (Pré-filtro) ⭐ UC03 / RF12
**Arquivo:** `doc-prototype-0003` → `vCategorias()` | `doc-figma-0001` → Frame 02 | `doc-prototype-0001` → `screen-categories`

| Elemento | Especificação |
|----------|---------------|
| **Título** | "Selecione as categorias" — Passo 1 de 5 |
| **Categorias (11 macro)** | 1. Mercado 🛒  2. Vestuário 👕  3. Automotivos 🚗  4. Informática 💻  5. Decoração 🖼️  6. Móveis 🛋️  7. Materiais de Construção e Ferragens 🧱  8. Ferramentas 🔧  9. Livros 📚  10. Jardinagem 🪴  11. Eletrodomésticos 🔌 |
| **Interação** | Checkboxes (múltipla escolha). Mínimo 1 categoria. "Selecionar todas" / "Limpar". |
| **Feedback visual** | Chip contador: "N categoria(s) selecionada(s) · 11 disponíveis". Verde quando ≥1. |
| **Estado** | Em memória (transitória). Perdida ao recarregar (toast informativo). |
| **Ação primária** | "Continuar para a lista →" — habilitado apenas se ≥1 categoria. |
| **Regra de negócio** | Fornecedores da próxima etapa = união dos fornecedores das categorias marcadas. Fornecedor pode pertencer a múltiplas categorias (aparece uma vez com badges). |
| **Exceções** | E1: Nenhuma categoria → botão desabilitado + toast. E2: Categoria sem fornecedores → toast + sugestão. |

---

### 2.2 Passo 2 — Lista de Compras (Em Memória) UC01/UC02 / RF07
**Arquivo:** `doc-prototype-0003` → `vLista()` | `doc-figma-0001` → Frame 03 | `doc-prototype-0001` → `screen-list` | `doc-prototype-0002` → `screen-list`

| Elemento | Especificação |
|----------|---------------|
| **Título** | "Monte sua lista" — Passo 2 de 5 |
| **Modo** | Efêmero (visitante) / Conta (autenticado). Chip: "⚠ MODO EFÊMERO" ou "🔒 CONTA: {username}". |
| **Nome da lista** | Input texto, máx 100 chars. Contador "X/100". Obrigatório para salvar. |
| **Autocomplete produtos** | Mín 2 chars → debounce 300ms → busca no catálogo (50 produtos seed). Exibe: nome + unidade de venda. Seleção adiciona à lista (soma qtd se duplicado). |
| **Quantidade** | Input numérico 1–9999. Botões +/- inline. Validação inline. |
| **Tabela de itens** | Colunas: Produto (nome + unidade), Qtd (controle +/-, input), Un, Ação (🗑 remover). |
| **Resumo (sidebar sticky)** | Produtos (count), Unidades totais (soma qtd), Categorias filtradas (count), Modo (Efêmero/Conta). |
| **Ações** | 1. "Comparar preços →" (habilitado se ≥1 item) 2. "💾 Salvar lista" (visitante: abre modal login; autenticado: persiste via UC14) 3. "📄 Exportar PDF" (em dev no proto-0002; funcional no proto-0003). |
| **Persistência temporária** | `sessionStorage` key `cobeco_eph` → recupera ao reabrir aba (toast "Lista efêmera recuperada"). |
| **Exceções** | E1: Nome vazio → erro inline. E2: Qtd=0 → rejeita. E3: Produto não encontrado → toast. EC1: Mesmo produto 2x → soma qtd. EC3: Qtd>9999 → rejeita. |

---

### 2.3 Passo 3 — Fornecedores UC04/UC05 / RF13/RF14
**Arquivo:** `doc-prototype-0003` → `vFornecedores()` | `doc-figma-0001` → Frame 04 | `doc-prototype-0001` → `screen-suppliers` | `doc-prototype-0002` → `screen-suppliers`

| Elemento | Especificação |
|----------|---------------|
| **Título** | "Escolha os fornecedores" — Passo 3 de 5 |
| **Fornecedores (10 seed)** | Carrefour, Extra, Pão de Açúcar, Magazine Luiza, Casas Bahia, Leroy Merlin, Etna, C&A, Renner, Hering. Cada um com categorias associadas. |
| **Filtro dinâmico** | Apenas fornecedores das categorias selecionadas no Passo 1. |
| **Card fornecedor** | Nome, badge % cobertura da lista (verde ≥80%, amarelo 40-79%, cinza <40%), tags de categorias, checkbox. Se cobertura=0 → aviso "⚠ Não possui itens da sua lista". |
| **Slider Disponibilidade (UC05/RF14)** | Range 0–100% (step 5). Padrão 0%. Atualiza cards em tempo real (debounce 100ms). Fornecedores abaixo do filtro → `opacity:0.55`, checkbox disabled. Seleção mantida se ainda passar no filtro. |
| **Toolbar** | Contador "N selecionado(s) · mín 2 · máx 10" (verde se ≥2). "Selecionar todos" / "Limpar" (aplica apenas aos visíveis/filtro). |
| **Ação primária** | "Calcular orçamento →" — habilitado se ≥2 fornecedores selecionados. |
| **Exceções** | E1: <2 fornecedores → botão desabilitado. E2: Filtro 100% elimina todos → toast. E3: Máx 10 fornecedores → toast. EC1: Slider move rápido → debounce. EC3: Fornecedor com exatamente 70% → incluído (≥). |

---

### 2.4 Passo 4 — Comparação de Preços UC06/UC07 / RF15/RF16
**Arquivo:** `doc-prototype-0003` → `vResultados()` | `doc-figma-0001` → Frame 05 | `doc-prototype-0001` → `screen-compare` | `doc-prototype-0002` → `screen-compare`

| Elemento | Especificação |
|----------|---------------|
| **Título** | "Comparação de preços" — Passo 4 de 5 |
| **KPIs (4 cards)** | 1. 🏆 Melhor oferta (nome + total + % cobertura) — card verde  2. 💰 Menor preço (valor + aviso "pode ter itens ausentes")  3. 📊 Economia potencial (vs maior total)  4. Disponibilidade média (% + N fornecedores) |
| **Tabela Flat** | Colunas: #, Fornecedor, Cobertura (barra visual + %), Itens (disponíveis/total), Ausentes (badge + tooltip com nomes), Preço total (R$). |
| **Ordenação** | Por preço total ASC (RF15). |
| **Destaques** | Linha vencedora: background verde claro + border-left 4px verde + badge "🏆 Melhor oferta". Menor preço (se diferente): badge "💰 Menor preço". Preço parcial: badge "parcial". |
| **Regra da Melhor Oferta (RF16/Monografia)** | Maior % cobertura da lista; empate → menor custo total. |
| **Banner de atenção** | Amarelo: "O menor preço pode não incluir todos os itens. A melhor oferta considera a maior cobertura; empate → menor total. Verifique coluna Ausentes." |
| **Ações** | "← Editar fornecedores", "🖨️ Imprimir (A4)", "📄 Exportar PDF", "🏆 Ver lista vencedora →" (primária). |
| **Cache** | 5 min (chave: itens + fornecedores selecionados). |
| **Performance** | Meta p95 <500ms (RNF09). Proto simula ~180ms. |
| **Exceções** | E1: Timeout >10s → toast. E2: Lista excluída em outra aba → redirect dashboard. E3: Preço indisponível → "N/D" + alerta. |

---

### 2.5 Passo 5 — Lista Vencedora / Exportação UC07/UC08 / RF17
**Arquivo:** `doc-prototype-0003` → `vVencedora()` | `doc-figma-0001` → Frame 06 | `doc-prototype-0001` → (não tem tela separada, parte do resultados) | `doc-prototype-0002` → (não tem tela separada)

| Elemento | Especificação |
|----------|---------------|
| **Título** | "Lista vencedora" — Passo 5 de 5 |
| **Hero** | Badge "🏆 MELHOR OFERTA · XX% DA LISTA", Nome do fornecedor + CNPJ + data + nome da lista. Total consolidado grande (R$). Badge: "todos os itens disponíveis" (verde) ou "total parcial — há itens indisponíveis" (amarelo). |
| **Tabela de itens precificados** | Colunas: Produto, Un, Qtd, Preço unitário, Subtotal. Itens indisponíveis: opacity 0.55 + badge "⚠ Indisponível neste fornecedor" (sem preço). |
| **Total Box** | "Total consolidado da compra (N itens · M unidades)" + valor grande. |
| **Export Note** | "O arquivo `lista_YYYYMMDD.pdf` (A4, ReportLab) contém exatamente este documento." |
| **Ações** | "← Voltar aos resultados", "🖨️ Imprimir A4", "⬇ Exportar PDF — lista_YYYYMMDD.pdf" (primária). |
| **Premissa central** | PDF exporta **apenas a lista vencedora precificada** — nunca a tabela comparativa. |

---

### 2.6 Modal PDF (UC08 / RF17 / RNF11)
**Arquivo:** `doc-prototype-0003` → `exportPDF()` + `sheetHTML()` | `doc-figma-0001` → Frame 07

| Elemento | Especificação |
|----------|---------------|
| **Trigger** | Botão "Exportar PDF" (Passo 4 ou 5). Funciona para TODOS (sem login). |
| **Backend** | Python + ReportLab (server-side). Meta <5s para ≤100 itens (RNF11). |
| **Nome arquivo** | `lista_YYYYMMDD.pdf` (ex: `lista_20260918.pdf`). |
| **Formato** | A4, retrato. Cabeçalho: COBECO + "LISTA VENCEDORA — COTAÇÃO". Meta: lista, fornecedor vencedor (CNPJ), itens, unidades, cobertura. Tabela: #, Produto, Un, Qtd, Preço unit., Subtotal. Total consolidado em box destacado. Rodapé: gerado por COBECO, sem valor fiscal. |
| **Preview Modal** | Modal amplo (860px) com render HTML da A4 sheet. Botões: "Fechar", "⬇ Baixar" (abre print-to-PDF nativo). |
| **Exceções** | E1: Erro geração → toast. E2: >100 itens → múltiplas páginas (quebras automáticas). E3: Chars especiais no nome → escaping. |

---

### 2.7 Impressão (UC09 / RF18)
**Arquivo:** `doc-prototype-0003` → `printWinner()` | `doc-figma-0001` → CSS `@media print` | `doc-prototype-0001` → `@media print` | `doc-prototype-0002` → `@media print`

| Elemento | Especificação |
|----------|---------------|
| **CSS** | `@media print` oculta: header, nav, footer, modais, journey panel, toasts, botões no-print. `body {background:#fff}`. `#print-area` com `.a4-sheet` (sem borda/sombra). `@page {size:A4;margin:13mm}`. |
| **Conteúdo** | Mesma sheet do PDF (lista vencedora). Header repetido em cada página. Quebras automáticas. Cores preservadas (melhor oferta em verde). Fallback P&B legível. |

---

### 2.8 Auth — Login (UC10 / RF02)
**Arquivo:** `doc-prototype-0003` → `vLogin()` | `doc-figma-0001` → Frame 08 | `doc-prototype-0001` → `screen-login` | `doc-prototype-0002` → `screen-login`

| Elemento | Especificação |
|----------|---------------|
| **Campos** | Username, Senha. Demo hint: "mariana / Comida123!". |
| **Rate Limiting** | 6 tentativas consecutivas → lockout 15 min (RF02 + UC27). Contador visual de tentativas (proto-0001: 5 estados visuais). Mensagem **sempre genérica** "Credenciais inválidas". |
| **JWT** | Access token: 15 min, apenas memória (RNF10). Refresh token: 7 dias, httpOnly cookie. |
| **Pós-login** | Se lista efêmera ativa → Modal UC17 "Salvar lista efêmera?". Senão → Dashboard. |
| **Exceções** | E1: 6ª falha → HTTP 429 + lockout 15min. E2: Credenciais inválidas → msg genérica. E3: Conta soft-deleted → msg genérica. |

---

### 2.9 Auth — Cadastro (UC09 / RF01)
**Arquivo:** `doc-prototype-0003` → `vCadastro()` | `doc-figma-0001` → Frame 09 | `doc-prototype-0001` → `screen-register` | `doc-prototype-0002` → `screen-register`

| Elemento | Especificação |
|----------|---------------|
| **Campos** | Username (3-30 alfanumérico, único), Nome completo (2-100), Email (válido, único), Senha (mín 8, 1 maiúscula, 1 número, 1 especial), Confirmar senha, Pergunta de segurança (3 opções), Resposta (mín 3 chars). |
| **Validação** | Inline no `onBlur` + submit. Mensagem genérica para duplicados ("Credenciais inválidas"). Senha: bcrypt salt=12 (UC21). |
| **Exceções** | E1: Username existe → msg genérica. E2: Senha fraca → erro inline. E3: Email inválido → validação frontend. E4: Confirmação diferente → erro inline. |

---

### 2.10 Auth — Recuperar Senha (UC12 / RF04)
**Arquivo:** `doc-prototype-0003` → `vRecuperar()` (3 steps) | `doc-figma-0001` → Frame 10 | `doc-prototype-0001` → `screen-recover` | `doc-prototype-0002` → `screen-recovery`

| Elemento | Especificação |
|----------|---------------|
| **Fluxo** | 3 passos: 1) Username → 2) Pergunta de segurança → 3) Nova senha. |
| **Via B (Padrão)** | Pergunta do cadastro. 3 tentativas. Token reset 15 min (uso único). Nova senha segue RF01 + diferente da atual. |
| **Via A (Dev)** | `RECOVERY_MODE=log` → token logado no stdout. |
| **Rate Limit** | Máx 3 solicitações/hora por IP. |
| **Exceções** | E1: Username não existe → msg genérica. E2: Resposta errada 3x → bloqueio temporário. E3: Token expirado → "Solicite novamente". |

---

### 2.11 Dashboard — Minhas Listas (UC15 / RF09)
**Arquivo:** `doc-prototype-0003` → `vDashboard()` | `doc-figma-0001` → Frame 11 | `doc-prototype-0001` → `screen-lists` | `doc-prototype-0002` → `screen-dashboard`

| Elemento | Especificação |
|----------|---------------|
| **Tabela** | Colunas: Nome, Itens (count), Categorias (badges), Criada em, Ações (✏️ Editar, 🗑 Excluir). |
| **Ordenação** | Data criação DESC (mais recente primeiro). |
| **Paginação** | 20 por página. |
| **Busca** | Input "Buscar por nome…" — case-insensitive, acentos normalizados. |
| **Filtro ordenação** | Select: Mais recentes / Mais antigas / A-Z. |
| **Soft Delete** | `deletado_em` preenchido → não aparece na listagem. |
| **Exceções** | E1: Nenhuma lista → empty state + botão "Criar lista". E2: Página inválida → redirect página 1. |

---

### 2.12 Perfil (UC16/UC18 / RF05/RF06)
**Arquivo:** `doc-prototype-0003` → `vPerfil()` | `doc-figma-0001` → Frame 12 | `doc-prototype-0001` → `screen-profile` | `doc-prototype-0002` → `screen-profile`

| Elemento | Especificação |
|----------|---------------|
| **Visualização (padrão)** | Username (read-only badge), Nome completo, Email, Data criação. Botões: "🚪 Logout", "✏️ Editar perfil". |
| **Edição** | Form: Novo nome, Novo email, Senha atual (obrigatória), Nova senha (opcional), Confirmar nova senha. Transação ACID: email/nome/senha atualizam juntos ou nada muda. |
| **Validação** | Email único, senha atual confere, nova senha segue RF01 + diferente da atual. |
| **Exceções** | E1: Email existe → "Email já cadastrado". E2: Senha atual incorreta → erro. E3: Nova senha = antiga → rejeita. |

---

### 2.13 Modal Promover Lista Efêmera ⭐ UC17 / RF08
**Arquivo:** `doc-prototype-0003` → `afterLogin()` + modal | `doc-figma-0001` → Frame 13 | `doc-prototype-0002` → `modal-promote`

| Elemento | Especificação |
|----------|---------------|
| **Trigger** | Login bem-sucedido (UC10) + lista efêmera ativa (itens > 0). |
| **Conteúdo** | "Você tem uma lista ativa na sessão: 'Nome' · N itens. Deseja salvá-la permanentemente na sua conta?" + aviso "Se escolher 'Não', a lista permanece em memória e será perdida ao fechar a aba." |
| **Ações** | "Não, manter efêmera" (fecha modal, vai dashboard, lista em sessionStorage) / "Sim, salvar lista" (dispara UC14 Salvar Lista). |
| **Edge Cases** | EC1: Login → fecha modal → logout → login novamente → modal reaparece. EC2: Produto descontinuado → toast + mantém efêmera. |

---

### 2.14 Modal Confirmar Exclusão (RF11)
**Arquivo:** `doc-prototype-0003` → `excluir-lista` action | `doc-figma-0001` → Frame 14 | `doc-prototype-0002` → `modal-delete`

| Elemento | Especificação |
|----------|---------------|
| **Conteúdo** | "Esta ação não pode ser desfeita. Digite o nome da lista para confirmar." + input. |
| **Validação** | Botão "Excluir permanentemente" habilitado apenas se input === nome exato da lista. |
| **Ação** | Soft delete: UPDATE `deletado_em` = now(). Toast "Lista excluída". |

---

### 2.15 Journey Panel (Painel Lateral Direito)
**Arquivo:** `doc-prototype-0003` → `renderJourney()` | `doc-figma-0001` → (não presente)

| Elemento | Especificação |
|----------|---------------|
| **Posição** | Fixed bottom-right (desktop ≥1024px). |
| **Conteúdo** | 9 passos da jornada de Mariana. Estado: done (✓ verde), current (bold + azul), pending (cinza). Descrição contextual do passo atual. Botão "🎯 Destacar próxima ação" → scroll + pulse no botão primário da tela. |
| **Colapsável** | Botão ▾/▴ no header. |

---

## 3. MODELO DE DADOS (DER v0.1.1)

### 3.1 Tabelas

| Tabela | Colunas Principais | Relacionamentos |
|--------|-------------------|-----------------|
| **users** | id (uuid PK), username (varchar(30) UNIQUE), name (varchar(100)), email (varchar(255) UNIQUE), password_hash (text), created_at, updated_at | 1:N → lists |
| **lists** | id (uuid PK), user_id (uuid FK→users), name (varchar(100)), deleted_at (timestamptz NULL, soft delete), created_at, updated_at | N:1 ← users, 1:N → list_items |
| **list_items** | id (uuid PK), list_id (uuid FK→lists), product_id (uuid FK→products), quantity (int 1–9999), created_at | N:1 ← lists, N:1 ← products |
| **products** | id (uuid PK), name (varchar(100)), category (varchar(50)), unit (varchar(20)), created_at | 1:N → list_items, 1:N → prices |
| **suppliers** | id (uuid PK), name (varchar(100)), cnpj (char(14) UNIQUE NULL), created_at | 1:N → prices |
| **prices** | id (uuid PK), supplier_id (FK→suppliers), product_id (FK→products), price (numeric(10,2) > 0), valid_from (date NOT NULL), valid_until (date NULL), created_at | N:1 ← suppliers, N:1 ← products |

### 3.2 Seed Determinístico (v3.2)
- **11 Categorias** macro (fixas)
- **10 Fornecedores** reais (Carrefour, Extra, Pão de Açúcar, Magazine Luiza, Casas Bahia, Leroy Merlin, Etna, C&A, Renner, Hering)
- **20 Produtos** (mistos: mercado, ferramentas, informática, vestuário, decoração, jardinagem)
- **Catálogo por fornecedor** (mapping fixo `CATALOGO[fornecedor_id] = [produto_ids]`)
- **Fator de preço por fornecedor** (`FATOR[fornecedor_id]` = multiplicador 0.93–1.14) + jitter determinístico `sin(f*997+p*131)*0.03`

---

## 4. REQUISITOS FUNCIONAIS (Resumo RF v3.2)

| Grupo | RF | Descrição | Prioridade |
|-------|----|-----------|------------|
| **Auth** | RF01 | Cadastrar Usuário | P0 |
|  | RF02 | Login (6 tentativas → lockout 15min, JWT mem+cookie) | P0 |
|  | RF03 | Logout | P0 |
|  | RF04 | Recuperar Senha (pergunta segurança, 3 tentativas) | P1 |
|  | RF05 | Visualizar Perfil | P1 |
|  | RF06 | Editar Perfil (senha antiga obrigatória) | P1 |
| **Listas** | RF07 | Criar Lista em memória (nome + itens, autocomplete, qtd 1-9999) | P0 |
|  | RF08 | Salvar Lista (persistir MySQL, requer auth, ACID, valida categorias) | P0 |
|  | RF09 | Listar Minhas Listas (paginação 20, DESC, soft delete) | P0 |
|  | RF10 | Editar Lista Salva (valida propriedade) | P1 |
|  | RF11 | Excluir Lista (soft delete, confirmação digitando nome) | P1 |
| **Pré-filtro/Comp** | RF12 ⭐ | Selecionar Categorias (mín 1, 11 macro, filtra fornecedores) | P0 |
|  | RF13 | Selecionar Fornecedores (2-10, checkboxes, % disponibilidade) | P0 |
|  | RF14 | Filtrar por Disponibilidade (slider 0-100%, tempo real) | P1 |
|  | RF15 | Calcular Orçamento (tabela flat, timeout 10s, cache 5min, ordena preço ASC) | P0 |
|  | RF16 | Visualizar Resultados (destaque melhor oferta: maior cobertura, empate→menor total) | P0 |
| **Export** | RF17 ⭐ | Exportar PDF (todos usuários, server-side ReportLab, A4, lista vencedora) | P0 |
|  | RF18 | Imprimir (CSS @media print, A4, oculta UI) | P1 |

---

## 5. REQUISITOS NÃO FUNCIONAIS (RNF v3.2)

| ID | Requisito | Métrica/Validação |
|----|-----------|-------------------|
| RNF01 | Clean Architecture (Domain→UseCase→Adapter→Framework) | Code review |
| RNF02 | SDD OpenAPI First (contrato antes de implementar) | Swagger em `/docs` |
| RNF03 | ACID MySQL InnoDB (transações explícitas) | Zero dados órfãos |
| RNF04 | Desktop-Only (≥1024px, sem mobile) | Breakpoint único |
| RNF05 | Feedback Visual (toasts, loading, modais) | <100ms feedback |
| RNF06 | Testes Unitários (cobertura ≥80% regras negócio) | `pytest --cov` |
| RNF07 | CI/CD Docker (app+MySQL, GitHub Actions) | Pipeline <5min |
| RNF08 | Seed Dados (10 forn + 50 prod + 11 cat) | `make seed` <10s |
| RNF09 | Performance API | p95 <500ms |
| RNF10 | Segurança (rate limit 6/15min, bcrypt, JWT mem) | Zero brute-force |
| RNF11 ⭐ | Geração PDF | <5s para ≤100 itens (ReportLab) |
| RNF12 ⭐ | MySQL InnoDB | Engine InnoDB, utf8mb4, ACID |

---

## 6. CASOS DE USO (Resumo UC v3.2)

### Principais (19)
| Grupo | UC | Ator | RF | Prioridade |
|-------|----|------|----|------------|
| Auth | UC09 Cadastrar | Visitante | RF01 | P0 |
|  | UC10 Login | Visitante | RF02 | P0 |
|  | UC11 Logout | Autenticado | RF03 | P0 |
|  | UC12 Recuperar Senha | Visitante | RF04 | P1 |
|  | UC18 Visualizar Perfil | Autenticado | RF05 | P1 |
|  | UC16 Gerenciar Perfil | Autenticado | RF06 | P1 |
| Pré-filtro/Listas | UC03 ⭐ Categorias | Visitante | RF12 | P0 |
|  | UC01 Criar Lista Memória | Visitante | RF07 | P0 |
|  | UC02 Autocomplete | Visitante | RF07 | P0 |
|  | UC14 Salvar Lista | Autenticado | RF08 | P0 |
|  | UC17 ⭐ Promover Efêmera | Autenticado | RF08 | P0 |
|  | UC15 Minhas Listas | Autenticado | RF09 | P0 |
|  | UC13 Editar/Excluir | Autenticado | RF10,RF11 | P1 |
| Comparação | UC04 Selecionar Fornecedores | Visitante | RF13 | P0 |
|  | UC05 Filtrar Disponibilidade | Visitante | RF14 | P1 |
|  | UC06 Calcular Orçamento | Visitante | RF15 | P0 |
|  | UC07 Visualizar Resultados | Visitante | RF16 | P0 |
| Export | UC08 ⭐ Exportar PDF | Visitante | RF17 | P0 |
|  | UC09 Imprimir | Visitante | RF18 | P1 |

### Internos (10)
UC20 Validar Dados, UC21 Hash Senha, UC22 Gerar Sessão JWT, UC23 Catálogo, UC24 ⭐ Categorias, UC25 ⭐ Fornecedores Filtrados, UC26 Preços, UC27 Rate Limiting, UC28 Invalidar Sessão, UC29 ⭐ Gerar PDF ReportLab.

---

## 7. REGRAS DE NEGÓCIO CRÍTICAS

| Regra | Descrição | Onde Aplica |
|-------|-----------|-------------|
| **Melhor Oferta** | Maior % cobertura da lista; empate → menor custo total. | RF16, UC07, Passo 4/5 |
| **Lista Vencedora no PDF** | PDF exporta **apenas** a lista do fornecedor campeão (itens precificados + total consolidado). Nunca a tabela comparativa. | RF17, UC08, Passo 5, Modal PDF |
| **Autenticação Tardia** | Visitante percorre todo fluxo (Passos 1-5) sem login. Auth só exigida para **salvar** (RF08/UC14/UC17). | RF08, UC14, UC17 |
| **Lista Efêmera** | Armazenada em `sessionStorage` (memória JS). Recuperada ao reabrir aba. Perdida ao fechar aba/limpar storage. | RF07, UC01, UC17 |
| **Soft Delete** | Listas excluídas: `deletado_em` preenchido. Não aparecem no dashboard. | RF11, UC13 |
| **Preço Parcial** | Se fornecedor não tem item → preço total calculado apenas sobre disponíveis. Badge "parcial" + aviso no banner. | RF15, RF16, UC06, UC07 |
| **Rate Limiting Híbrido** | Por IP + por username (após login). 6 req/15min. | RF02, UC10, UC27 |
| **Validação Categorias no Save** | Salvar lista (RF08) exige ≥1 categoria selecionada (UC03). | RF08, UC14 |

---

## 8. ESTADOS DE TELA / NAVEGAÇÃO

| View/State | Proto-0003 (state.view) | Proto-0001 (screen ID) | Proto-0002 (screen ID) |
|------------|-------------------------|------------------------|------------------------|
| Home/Landing | `home` | `landing` | `home` |
| Categorias (Passo 1) | `categorias` | `categories` / `builder` | `categories` |
| Lista (Passo 2) | `lista` | `builder` | `list` |
| Fornecedores (Passo 3) | `fornecedores` | `providers` | `suppliers` |
| Comparação (Passo 4) | `resultados` | `results` | `compare` |
| Lista Vencedora (Passo 5) | `vencedora` | — | — |
| Login | `login` | `login` | `login` |
| Cadastro | `cadastro` | `register` | `register` |
| Recuperar Senha | `recuperar` | `recover` | `recovery` |
| Dashboard | `dashboard` | `lists` | `dashboard` |
| Perfil | `perfil` | `profile` | `profile` |

**Stepper (5 passos fixos):**
1. Categorias → 2. Lista → 3. Fornecedores → 4. Comparação → 5. Lista vencedora

---

## 9. COMPONENTES DE UI / DESIGN SYSTEM (Tokens) — Inspirado no McCormick.com

### 9.1 Paleta de Cores (McCormick-inspired)

| Token | Valor | Origem McCormick | Uso COBECO |
|-------|-------|------------------|------------|
| **Brand-Red** | `#C41E3A` | Red Cap label / CTA primário | Botões primários, links, stepper ativo, badges "Melhor oferta" |
| **Brand-Red-Dark** | `#A0182F` | Hover do red cap | Hover botões primários, stepper completed |
| **Brand-Red-Light** | `#FCECEE` | Backgrounds sutis da marca | Chips "Melhor oferta", backgrounds de destaque |
| **Brand-Blue** | `#00529D` | Announcement bar / Header sticky | Header sticky, announcement/info bars, links secundários |
| **Brand-Blue-Light** | `#E8F1FA` | Overlay transparente | Backgrounds de cards informativos |
| **Success-Green** | `#1E7D32` | "Add to Cart" success / Disponibilidade | Melhor oferta (cobertura), slider disponibilidade, badges ok |
| **Success-Green-Light** | `#E8F5E9` | Product cards hover | Cards vencedor, badges disponibilidade |
| **Warning-Amber** | `#F57F17` | Price highlight / Promo | Preço parcial, economia, atenção |
| **Warning-Amber-Light** | `#FFF8E1` | Sale badges | Banners atenção, chips modo efêmero |
| **Error-Red** | `#C62828` | Out of stock / Error states | Erros, exclusão, lockout |
| **Error-Red-Light** | `#FDEDEC` | Error inline | Backgrounds de erro inline |
| **Neutral-900** | `#1A1A2E` | Heading text / Logo | Texto principal (headings) |
| **Neutral-700** | `#374151` | Body text | Texto secundário, labels |
| **Neutral-500** | `#6B7280` | Meta text / Placeholders | Texto meta, hints, contadores |
| **Neutral-300** | `#D1D5DB` | Borders / Dividers | Bordas cards, inputs, divisores |
| **Neutral-100** | `#F3F4F6` | Page background | Background página |
| **Neutral-0** | `#FFFFFF` | Cards / Modals / Inputs | Cards, modais, inputs bg |
| **Overlay-Dark** | `rgba(0,0,0,0.55)` | Modal backdrops | Modal overlays, drawer |

### 9.2 Tipografia (McCormick-inspired)

| Token | Valor | Classe McCormick | Uso |
|-------|-------|------------------|-----|
| **Font-Heading** | `'Inter', 'Helvetica Neue', Arial, sans-serif` | `ff-heading` | Headings, navegação, botões |
| **Font-Body** | `'Inter', system-ui, -apple-system, sans-serif` | `ff-body` | Body text, inputs, tabelas |
| **FS-Display** | `clamp(32px, 5vw, 48px) / 1.1 / 800` | Hero headlines | Hero landing |
| **FS-H1** | `28px / 1.2 / 700` | `fs-heading-1` | Títulos de página (Passo X) |
| **FS-H2** | `22px / 1.3 / 700` | `fs-heading-2` | Títulos de seção, cards |
| **FS-H3** | `18px / 1.4 / 600` | `fs-heading-3` | Subtítulos, card titles |
| **FS-Body-LG** | `16px / 1.5 / 400` | `fs-body-25` | Body principal, descrições |
| **FS-Body** | `14px / 1.5 / 400` | `fs-body` | Inputs, tabelas, badges |
| **FS-SM** | `12px / 1.4 / 500` | `fs-body-150` | Meta, hints, contadores |
| **FS-XS** | `11px / 1.3 / 600` | Micro copy | Timestamps, contadores char |
| **Kicker** | `11px / 1.0 / 800 / uppercase / ls: 1px` | `ff-heading` + custom | Labels de passo, badges categoria |

### 9.3 Espaçamento & Layout (McCormick-inspired)

| Token | Valor | Origem | Uso |
|-------|-------|--------|-----|
| **Space-1** | `4px` | Base unit | Gap micro |
| **Space-2** | `8px` | Base unit | Gap pequeno, padding chips |
| **Space-3** | `12px` | Base unit | Gap médio, padding inputs |
| **Space-4** | `16px` | Base unit | Gap padrão, padding cards |
| **Space-5** | `24px` | Base unit | Gap grande, section padding |
| **Space-6** | `32px` | Base unit | Section gap, modal padding |
| **Space-7** | `48px` | Base unit | Hero padding, page margins |
| **Container-Max** | `1280px` | Header max-width | Container principal |
| **Container-Padding** | `24px` desktop / `16px` mobile | Header padding | Lateral padding |
| **Header-Height** | `72px` (desktop) / `60px` (mobile) | `--height-header` | Header sticky |
| **Announcement-Height** | `40px` | `--announcement-height` | Top bar |

### 9.4 Border Radius & Shadows (McCormick-inspired)

| Token | Valor | Uso |
|-------|-------|-----|
| **Radius-SM** | `4px` | Badges, chips, icon buttons |
| **Radius-MD** | `8px` | Inputs, buttons, cards pequenos |
| **Radius-LG** | `12px` | Cards principais, modais, dropdowns |
| **Radius-XL** | `16px` | Hero cards, modais grandes |
| **Radius-Full** | `9999px` | Pills, avatars, stepper dots |
| **Shadow-SM** | `0 1px 2px rgba(0,0,0,0.05)` | Cards hover, input focus |
| **Shadow-MD** | `0 4px 12px rgba(0,0,0,0.08)` | Cards principais, dropdowns |
| **Shadow-LG** | `0 12px 28px rgba(0,0,0,0.12)` | Modais, mega nav, toast |
| **Shadow-XL** | `0 20px 40px rgba(0,0,0,0.15)` | Modal PDF preview |

### 9.5 Componentes Base (McCormick Patterns)

#### Botões
```css
/* Primary — Brand Red (CTA principal) */
.btn--primary {
  background: var(--brand-red);
  color: var(--neutral-0);
  border: none;
  border-radius: var(--radius-md);
  padding: 12px 24px;
  font: var(--fs-body) var(--font-heading);
  font-weight: 600;
  transition: background 0.15s, transform 0.05s;
}
.btn--primary:hover { background: var(--brand-red-dark); }
.btn--primary:active { transform: translateY(1px); }
.btn--primary:disabled { opacity: 0.45; cursor: not-allowed; }

/* Secondary — Outline Brand Blue */
.btn--secondary {
  background: transparent;
  color: var(--brand-blue);
  border: 2px solid var(--brand-blue);
  border-radius: var(--radius-md);
  padding: 10px 22px;
  font: var(--fs-body) var(--font-heading);
  font-weight: 600;
}
.btn--secondary:hover { background: var(--brand-blue-light); }

/* Ghost — Neutral outline */
.btn--ghost {
  background: transparent;
  color: var(--neutral-700);
  border: 1px solid var(--neutral-300);
  border-radius: var(--radius-md);
  padding: 10px 22px;
}
.btn--ghost:hover { background: var(--neutral-100); }

/* Danger — Error Red */
.btn--danger {
  background: transparent;
  color: var(--error-red);
  border: 1px solid var(--error-red);
  border-radius: var(--radius-md);
  padding: 10px 22px;
}
.btn--danger:hover { background: var(--error-red-light); }

/* Callout — Full width primary (Mega nav "SHOP ALL") */
.btn--callout {
  width: 100%;
  padding: 14px 24px;
  font-size: var(--fs-body-lg);
}
```

#### Inputs & Form
```css
.input {
  width: 100%;
  height: 44px;
  padding: 0 14px;
  border: 1px solid var(--neutral-300);
  border-radius: var(--radius-md);
  background: var(--neutral-0);
  color: var(--neutral-900);
  font: var(--fs-body) var(--font-body);
  transition: border-color 0.15s, box-shadow 0.15s;
}
.input:focus {
  outline: none;
  border-color: var(--brand-blue);
  box-shadow: 0 0 0 3px var(--brand-blue-light);
}
.input--error { border-color: var(--error-red); }
.input--error:focus { box-shadow: 0 0 0 3px var(--error-red-light); }

.label {
  display: block;
  font: var(--fs-sm) var(--font-heading);
  font-weight: 600;
  color: var(--neutral-700);
  margin-bottom: 6px;
}
.error-message {
  font: var(--fs-xs) var(--font-body);
  color: var(--error-red);
  margin-top: 4px;
}
```

#### Cards (Product/Provider style)
```css
.card {
  background: var(--neutral-0);
  border: 1px solid var(--neutral-300);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s, border-color 0.2s;
}
.card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--brand-blue);
}
.card--selected {
  border-color: var(--success-green);
  box-shadow: 0 0 0 3px var(--success-green-light);
}
.card--disabled { opacity: 0.55; pointer-events: none; }
```

#### Badges & Chips
```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font: var(--fs-xs) var(--font-heading);
  font-weight: 700;
}
.badge--success { background: var(--success-green-light); color: var(--success-green); }
.badge--warning { background: var(--warning-amber-light); color: var(--warning-amber); }
.badge--error { background: var(--error-red-light); color: var(--error-red); }
.badge--info { background: var(--brand-blue-light); color: var(--brand-blue); }
.badge--brand { background: var(--brand-red-light); color: var(--brand-red); }

.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: var(--radius-full);
  font: var(--fs-sm) var(--font-heading);
  font-weight: 700;
  border: 1px solid var(--neutral-300);
  background: var(--neutral-0);
  color: var(--neutral-500);
}
.chip--active { border-color: var(--success-green); background: var(--success-green-light); color: var(--success-green); }
```

#### Stepper (McCormick-style)
```css
.stepper { display: flex; gap: 0; margin: 16px 0 24px; }
.step { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px; position: relative; }
.step::before { content: ''; position: absolute; top: 16px; left: -50%; width: 100%; height: 2px; background: var(--neutral-300); z-index: 0; }
.step:first-child::before { display: none; }
.step.completed::before { background: var(--success-green); }
.step .dot { width: 32px; height: 32px; border-radius: var(--radius-full); display: flex; align-items: center; justify-content: center; font: var(--fs-sm) var(--font-heading); font-weight: 700; background: var(--neutral-300); color: var(--neutral-500); border: 2px solid transparent; z-index: 1; transition: all 0.2s; }
.step.active .dot { background: var(--brand-red); color: var(--neutral-0); border-color: var(--brand-red-light); box-shadow: 0 0 0 4px var(--brand-red-light); }
.step.completed .dot { background: var(--success-green); color: var(--neutral-0); border-color: var(--success-green-light); }
.step .label { font: var(--fs-xs) var(--font-heading); font-weight: 600; color: var(--neutral-500); text-align: center; }
.step.active .label { color: var(--brand-red); }
.step.completed .label { color: var(--success-green); }
```

#### Header & Navigation
```css
.header {
  position: sticky; top: 0; z-index: 50;
  height: var(--header-height);
  background: var(--neutral-0);
  border-bottom: 1px solid var(--neutral-300);
  box-shadow: var(--shadow-sm);
}
.header__inner { max-width: var(--container-max); margin: 0 auto; padding: 0 var(--container-padding); height: 100%; display: flex; align-items: center; justify-content: space-between; gap: 24px; }
.header__logo { display: flex; align-items: center; gap: 10px; text-decoration: none; }
.header__logo-mark { width: 40px; height: 40px; border-radius: var(--radius-md); background: var(--brand-red); color: var(--neutral-0); display: flex; align-items: center; justify-content: center; font: var(--fs-h2) var(--font-heading); font-weight: 800; }
.header__nav { display: flex; gap: 4px; }
.header__nav-link { padding: 8px 14px; border-radius: var(--radius-md); color: var(--neutral-700); text-decoration: none; font: var(--fs-body) var(--font-heading); font-weight: 600; transition: all 0.15s; }
.header__nav-link:hover { background: var(--neutral-100); color: var(--neutral-900); }
.header__nav-link.active { background: var(--brand-red-light); color: var(--brand-red); }
.header__auth { display: flex; align-items: center; gap: 10px; }
```

#### Announcement Bar (McCormick signature)
```css
.announcement-bar {
  height: var(--announcement-height);
  background: var(--brand-blue);
  color: var(--neutral-0);
  display: flex; align-items: center; justify-content: center;
  font: var(--fs-sm) var(--font-heading); font-weight: 600;
  overflow: hidden; position: relative;
}
.announcement-bar__slider { display: flex; gap: 24px; animation: scroll 20s linear infinite; }
@keyframes scroll { from { transform: translateX(0); } to { transform: translateX(-50%); } }
```

#### Mega Nav Pattern (para Categorias)
```css
.meganav { position: absolute; top: 100%; left: 0; right: 0; background: var(--neutral-0); border-bottom: 1px solid var(--neutral-300); box-shadow: var(--shadow-lg); padding: 24px; z-index: 40; display: grid; grid-template-columns: repeat(var(--column-count, 2), 1fr); gap: 24px; }
.meganav__item { display: flex; flex-direction: column; align-items: center; text-align: center; text-decoration: none; color: inherit; gap: 10px; padding: 16px; border-radius: var(--radius-lg); transition: background 0.15s; }
.meganav__item:hover { background: var(--neutral-100); }
.meganav__item-image { width: 80px; height: 80px; border-radius: var(--radius-md); overflow: hidden; background: var(--neutral-100); }
.meganav__item-title { font: var(--fs-body) var(--font-heading); font-weight: 600; color: var(--neutral-900); }
.meganav__shop-all { justify-self: start; }
```

### 9.6 CSS Custom Properties (para implementação)
```css
:root {
  /* Brand */
  --brand-red: #C41E3A;
  --brand-red-dark: #A0182F;
  --brand-red-light: #FCECEE;
  --brand-blue: #00529D;
  --brand-blue-light: #E8F1FA;

  /* Semantic */
  --success: #1E7D32;
  --success-light: #E8F5E9;
  --warning: #F57F17;
  --warning-light: #FFF8E1;
  --error: #C62828;
  --error-light: #FDEDEC;

  /* Neutral */
  --neutral-900: #1A1A2E;
  --neutral-700: #374151;
  --neutral-500: #6B7280;
  --neutral-300: #D1D5DB;
  --neutral-100: #F3F4F6;
  --neutral-0: #FFFFFF;

  /* Layout */
  --header-height: 72px;
  --announcement-height: 40px;
  --container-max: 1280px;
  --container-padding: 24px;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 12px 28px rgba(0,0,0,0.12);
  --shadow-xl: 0 20px 40px rgba(0,0,0,0.15);

  /* Transitions */
  --transition-fast: 0.1s ease;
  --transition-base: 0.15s ease;
  --transition-slow: 0.2s ease;
}
```

### 9.7 Acessibilidade (McCormick Standards)
- **Focus Visible**: `outline: 2px solid var(--brand-blue); outline-offset: 2px; border-radius: 2px;`
- **Contrast**: Mínimo 4.5:1 (textos), 3:1 (UI elements) — brand red sobre branco = 4.8:1 ✓
- **Reduced Motion**: `@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }`
- **ARIA**: `aria-label`, `aria-expanded`, `aria-controls`, `aria-live="polite"` (toasts), `role="dialog"` (modais)
- **Keyboard**: Tab order lógico, skip links, focus trap em modais

---

## 10. FLUXOS DE EXCEÇÃO / EDGE CASES MAIS IMPORTANTES

| Cenário | Comportamento |
|---------|---------------|
| Recarregar página em qualquer passo | Seleções perdidas (memória) + toast informativo |
| Login com lista efêmera → fecha modal "Não" → logout → login novamente | Modal reaparece (lista ainda em sessionStorage) |
| Slider disponibilidade remove fornecedor selecionado | Mantém checkbox se ainda ≥ filtro; senão desmarca + toast |
| Todos fornecedores com mesmo preço total | "Empate técnico" — melhor oferta = maior cobertura |
| Lista com 100+ itens + 10 fornecedores | Cálculo <2s (RNF09), transação ACID garante atomicidade no save |
| Usuário edita lista em 2 abas simultâneas | Última gravação vence (optimistic locking) |
| Access token expira durante requisição | Frontend detecta 401 → `/auth/refresh` → retry automático |
| PDF >10MB | Geração assíncrona + toast "Gerando PDF..." |
| Impressão em tela <1024px | Aviso "Otimizado para ≥1024px" (RNF04) |

---

## 11. ARTEFATOS DE ENTREGA (Specs para Implementação)

### 11.1 Backend (FastAPI + MySQL InnoDB)
- **Endpoints** (OpenAPI First):
  - `POST /auth/register` (UC09/RF01)
  - `POST /auth/login` (UC10/RF02) — returns access (mem) + refresh (cookie)
  - `POST /auth/refresh` (UC22)
  - `POST /auth/logout` (UC11/RF03)
  - `POST /auth/recover/step1|step2|step3` (UC12/RF04)
  - `GET /categories` (UC24/RF12)
  - `GET /products/search?q=` (UC23/UC02)
  - `GET /suppliers?categories=` (UC25/RF13)
  - `POST /compare` (UC26/UC06/RF15) — body: list_items + supplier_ids
  - `POST /lists` (UC14/RF08) — auth required, transação ACID
  - `GET /lists` (UC15/RF09) — paginação, busca, ordenação
  - `PUT /lists/{id}` (UC13/RF10)
  - `DELETE /lists/{id}` (UC13/RF11) — soft delete
  - `GET /profile` (UC18/RF05)
  - `PUT /profile` (UC16/RF06) — transação ACID
  - `POST /export/pdf` (UC29/UC08/RF17) — ReportLab, retorna file stream

- **Validação**: Pydantic schemas em todos endpoints (UC20).
- **Segurança**: bcrypt salt=12 (UC21), rate limit 6/15min IP+user (UC27), JWT access 15min mem + refresh 7d httpOnly (UC22).
- **Seed**: `make seed` → 11 cat, 10 forn, 50 prod, preços (~300), catálogo mapping.

### 11.2 Frontend (Vanilla JS / TypeScript + Vite)
- **SPA** com roteamento hash/history (`state.view`).
- **Estado global**: `state` object (view, user, categorias, lista, fornecedores, filtroDisp, resultado, flags).
- **Persistência efêmera**: `sessionStorage` key `cobeco_eph` (lista + categorias).
- **Componentes**: Header (nav + auth), Stepper, Toast container, Modal root, Journey panel, Print area.
- **Screens**: 10 views (home, categorias, lista, fornecedores, resultados, vencedora, login, cadastro, recuperar, dashboard, perfil).
- **Estilo**: Design tokens (CSS vars), desktop-only (≥1024px), `@media print` para PDF/impressão.
- **Acessibilidade**: `aria-label`, `role`, focus-visible, contrast ratios.

### 11.3 PDF Generation (Python + ReportLab)
- **Entrada**: `state.resultado.winner` + `state.lista.itens` + `state.lista.nome`.
- **Saída**: `BytesIO` PDF A4, filename `lista_YYYYMMDD.pdf`.
- **Conteúdo**: Cabeçalho COBECO, meta (lista, fornecedor, CNPJ, cobertura), tabela itens precificados, total consolidado box, rodapé.
- **Performance**: <5s para 100 itens (RNF11).

---

## 12. CHECKLIST DE VALIDAÇÃO (Definition of Done)

- [ ] Todos 18 RFs implementados e testados
- [ ] Todos 12 RNFs atendidos (incl. performance, segurança, arquitetura)
- [ ] 19 UCs principais + 10 internos cobertos
- [ ] Fluxo completo: Home → Categorias → Lista → Fornecedores → Comparação → Vencedora → PDF
- [ ] Auth tardia: visitante completa fluxo sem login; login só para salvar
- [ ] Lista efêmera em sessionStorage + recuperação + promoção pós-login
- [ ] PDF exporta **apenas lista vencedora** (nunca tabela comparativa)
- [ ] Melhor oferta = maior cobertura; empate → menor total
- [ ] Soft delete em listas
- [ ] Rate limiting 6/15min + bcrypt + JWT mem/cookie
- [ ] ACID transações em save lista / edit perfil
- [ ] Seed determinístico roda em <10s
- [ ] CI/CD pipeline <5min
- [ ] Cobertura testes ≥80% regras negócio
- [ ] Desktop-only ≥1024px, print CSS funcional

---

**FIM DO DOCUMENTO SPECS — COBECO MVP v3.2**  
*Gerado a partir da análise dos protótipos (0001/0002/0003), Figma export (0001), Requisitos Funcionais (req-func-0001), Casos de Uso (req-use-case-0001) e DER (v0.1.1).*