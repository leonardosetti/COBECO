# 🎯 LEVANTAMENTO OFICIAL DE CASOS DE USO — COBECO MVP v3.2

**Documento:** Casos de Uso Fechados do Projeto  
**Versão:** 3.2 (SSOT Final)  
**Data:** 14 de Setembro de 2026  
**Status:** ✅ APROVADO — Composição Oficial  
**Base:** DOC-01 do Pacote Documental Consolidado

---

## 🎭 ATORES DO SISTEMA

| Ator | Tipo | Papel | Generalização |
|------|------|-------|---------------|
| **Visitante** | Primário | Usuário não autenticado. Cria listas em memória, compara, exporta. | Ator base |
| **Usuário Autenticado** | Primário | Herda Visitante + persistência de listas. | Generaliza Visitante |
| **Sistema** | Secundário | Validações (Pydantic), hashing, rate limiting, geração PDF. | — |
| **API Mock de Fornecedores** | Secundário | Fornece catálogo, categorias, fornecedores e preços. | — |

---

## 🎬 CASOS DE USO PRINCIPAIS (19)

### Grupo A — Autenticação (UC09–UC13, UC16, UC18, UC19)

| ID | Caso de Uso | Ator | RF | Área | Prioridade |
|----|-------------|------|----|----|-----------|
| UC09 | Cadastrar-se | Visitante | RF01 | Auth | P0 |
| UC10 | Realizar Login | Visitante | RF02 | Auth | P0 |
| UC11 | Realizar Logout | Usuário Autenticado | RF03 | Auth | P0 |
| UC12 | Recuperar Senha | Visitante | RF04 | Auth | P1 |
| UC18 | Visualizar Perfil | Usuário Autenticado | RF05 | Auth | P1 |
| UC16 | Gerenciar Perfil | Usuário Autenticado | RF06 | Auth | P1 |

### Grupo B — Pré-filtro e Gestão de Listas (UC01, UC02, UC03, UC14, UC15, UC17)

| ID | Caso de Uso | Ator | RF | Área | Prioridade |
|----|-------------|------|----|----|-----------|
| UC03 ⭐ | Selecionar Categorias (Pré-filtro) | Visitante | RF12 | Pré-filtro | P0 |
| UC01 | Criar Lista em Memória | Visitante | RF07 | Listas | P0 |
| UC02 | Buscar Produtos (Autocomplete) | Visitante | RF07 | Listas | P0 |
| UC14 | Salvar Lista (Persistir) | Usuário Autenticado | RF08 | Listas | P0 |
| UC17 | Promover Lista Efêmera | Usuário Autenticado | RF08 | Listas | P0 |
| UC15 | Listar Minhas Listas | Usuário Autenticado | RF09 | Listas | P0 |
| UC13 | Editar/Excluir Lista Salva | Usuário Autenticado | RF10, RF11 | Listas | P1 |

### Grupo C — Comparação de Fornecedores (UC04, UC05, UC06, UC07)

| ID | Caso de Uso | Ator | RF | Área | Prioridade |
|----|-------------|------|----|----|-----------|
| UC04 | Selecionar Fornecedores | Visitante | RF13 | Comparação | P0 |
| UC05 | Filtrar por Disponibilidade | Visitante | RF14 | Comparação | P1 |
| UC06 | Calcular Orçamento (Tabela Flat) | Visitante | RF15 | Comparação | P0 |
| UC07 | Visualizar Resultados | Visitante | RF16 | Comparação | P0 |

### Grupo D — Exportação (UC08, UC09)

| ID | Caso de Uso | Ator | RF | Área | Prioridade |
|----|-------------|------|----|----|-----------|
| UC08 ⭐ | Exportar Lista PDF | Visitante | RF17 | Exportação | P0 |
| UC09 | Imprimir | Visitante | RF18 | Exportação | P1 |

---

## ⚙️ CASOS DE USO INTERNOS (10)

| ID | Caso de Uso | Ator | Invocado Por | Comportamento |
|----|-------------|------|--------------|---------------|
| UC20 | Validar Dados | Sistema | UC09, UC14, UC16 | Valida schemas Pydantic em todas requisições |
| UC21 | Hash de Senha (bcrypt) | Sistema | UC09 | Salt=12 no cadastro e alteração |
| UC22 | Gerar Sessão (JWT) | Sistema | UC10 | Access (15min) + refresh (7d httpOnly) |
| UC23 | Fornecer Catálogo | API Mock | UC02 | Retorna 50 produtos do seed |
| UC24 ⭐ | Fornecer Categorias | API Mock | UC03 | Retorna 11 categorias macro |
| UC25 ⭐ | Fornecer Fornecedores (filtrado) | API Mock | UC04, UC06 | Retorna fornecedores filtrados por categorias |
| UC26 | Fornecer Preços | API Mock | UC06 | Retorna ~300 preços do seed |
| UC27 | Rate Limiting | Sistema | UC10, UC12 | 6 tentativas/15min por IP + username |
| UC28 | Invalidar Sessão | Sistema | UC11 | Logout + rotação de refresh tokens |
| UC29 ⭐ | Gerar PDF (ReportLab) | Sistema | UC08 | Gera PDF A4 server-side |

---

## 🔄 FLUXOS DETALHADOS (Happy Paths + Exceções + Edge-Cases)

### 🔐 GRUPO A — AUTENTICAÇÃO

#### UC09 — Cadastrar-se (RF01)

**Happy Paths:**
- **HP1:** Visitante preenche formulário (nome_usuario, nome, email, senha, confirmação, pergunta de segurança, resposta) → validação frontend → backend hasheia senha (bcrypt salt=12) → INSERT em `usuarios` → retorna 201 Created → redireciona para login.
- **HP2:** Visitante preenche todos os campos com valores válidos → backend valida unicidade de nome_usuario e email → retorna 201 → toast verde "Conta criada com sucesso" → redireciona para /login.

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | nome_usuario já existe | RF01 + UNIQUE constraint | Mensagem genérica "Credenciais inválidas" (não revela qual campo) |
| E2 | Senha fraca (<8 chars, sem maiúscula, sem número, sem especial) | RF01 | Erro inline no campo no `onBlur` |
| E3 | Email inválido (formato incorreto) | RF01 (regex) | Validação frontend impede submit + mensagem "Email inválido" |
| E4 | Confirmação de senha diferente | RF01 | Erro inline "As senhas não coincidem" |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário submete formulário 2x rapidamente (duplo clique) | Botão desabilitado após primeiro submit + loading state |
| EC2 | Resposta da pergunta de segurança muito curta (<3 chars) | Validação rejeita + mensagem "Resposta muito curta" |
| EC3 | Nome com caracteres especiais (acentos, espaços) | Aceito (UTF-8) — validação permite 2-100 chars |
| EC4 | Perda de conexão durante submit | Toast vermelho "Falha ao criar conta. Tente novamente." |

#### UC10 — Realizar Login (RF02)

**Happy Paths:**
- **HP1:** Usuário informa nome_usuario + senha → backend valida → gera JWT access (15min em memória) + refresh (7d httpOnly cookie) → retorna 200 → redireciona para dashboard.
- **HP2:** Usuário com lista efêmera ativa faz login → modal "Deseja salvar esta lista?" → se SIM → UC17 (Promover Lista Efêmera) é disparado → lista persistida no DB.

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | 6ª tentativa falha | RF02 + UC27 (Rate Limiting) | HTTP 429 + lockout 15min + toast "Tente novamente em X minutos" |
| E2 | Credenciais inválidas | RF02 | Mensagem genérica "Credenciais inválidas" |
| E3 | Conta com `deletado_em` preenchido (soft-deleted) | RF02 | Mensagem genérica "Credenciais inválidas" |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário abre 5 abas e faz login em todas | Todas compartilham o mesmo refresh token (cookie) |
| EC2 | Access token expira durante requisição | Frontend detecta 401 → chama /auth/refresh → retry automático |
| EC3 | Refresh token expirado (7d) | Redireciona para /login + toast "Sessão expirada" |
| EC4 | Usuário atrás de NAT (empresa/escola) | Rate limiting híbrido: por IP + por username (após login) |

#### UC11 — Realizar Logout (RF03)

**Happy Paths:**
- **HP1:** Usuário autenticado clica "Sair" → backend invalida refresh token → frontend limpa access token da memória → redireciona para home (/).
- **HP2:** Logout após sessão expirada → frontend detecta token inválido → redirecionamento automático para /login.

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Erro de rede ao chamar /auth/logout | RF03 | Toast "Falha ao encerrar sessão. Tente novamente." |
| E2 | Refresh token já expirado | RF03 | Logout forçado sem erro (frontend limpa estado local) |
| E3 | Múltiplas abas abertas | RF03 | Apenas a aba atual é deslogada; outras detectam via storage event |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário clica "Sair" 2x rapidamente | Segunda chamada retorna 204 (idempotente) |
| EC2 | Logout durante requisição em andamento | Requisição é abortada; estado limpo |
| EC3 | Cookie httpOnly corrompido | Frontend força logout + redireciona para /login |

#### UC12 — Recuperar Senha (RF04)

**Happy Paths:**
- **HP1 (Via B — Pergunta de Segurança):** Usuário informa nome_usuario → sistema exibe pergunta cadastrada → usuário responde → backend valida (bcrypt) → gera token de reset (15min) → usuário define nova senha → retorna 200.
- **HP2 (Via A — Log no stdout):** Usuário solicita reset → backend gera token → loga no stdout do container (RECOVERY_MODE=log) → usuário informa token → define nova senha.

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | nome_usuario não existe | RF04 | Mensagem genérica "Usuário não encontrado" |
| E2 | Resposta da pergunta errada (3 tentativas) | RF04 | Bloqueio temporário + toast "Muitas tentativas. Tente mais tarde." |
| E3 | Token expirado (>15min) | RF04 | Mensagem "Token expirado. Solicite novamente." |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário solicita reset 4x em 1 hora | Rate limiting: máx 3/hora → HTTP 429 |
| EC2 | Nova senha igual à antiga | Validação rejeita "Nova senha deve ser diferente da atual" |
| EC3 | Usuário tenta usar token já utilizado | Token é de uso único → mensagem "Token já utilizado" |

#### UC16 — Gerenciar Perfil (RF05, RF06)

**Happy Paths:**
- **HP1:** Usuário autenticado altera email → valida formato → confirma senha antiga → atualiza no DB → toast "Perfil atualizado".
- **HP2:** Usuário altera senha → informa senha antiga → nova senha hasheada (bcrypt) → atualiza → toast "Senha alterada com sucesso".

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Novo email já existe | RF06 + UNIQUE constraint | Mensagem "Email já cadastrado" |
| E2 | Senha antiga incorreta | RF06 | Erro "Senha atual incorreta" |
| E3 | Nova senha igual à antiga | RF06 | Validação rejeita "Nova senha deve ser diferente" |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário altera email e senha simultaneamente | Transação ACID: ambos ou nenhum |
| EC2 | Sessão expira durante edição | Redireciona para /login + toast "Sessão expirada" |
| EC3 | Nome com caracteres especiais | Aceito (UTF-8) — validação 2-100 chars |

#### UC18 — Visualizar Perfil (RF05)

**Happy Paths:**
- **HP1:** Usuário autenticado acessa /perfil → vê dados pessoais (nome_usuario, email, nome, data de criação).
- **HP2:** Usuário vê data de criação da conta + botão "Editar Perfil".

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Não autenticado | RF05 | Redireciona para /login |
| E2 | Dados corrompidos no DB | RF05 | Toast "Erro ao carregar perfil" |
| E3 | Conta com `deletado_em` preenchido | RF05 | Mensagem "Conta desativada" + redireciona para /login |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário abre /perfil em 2 abas | Ambas mostram os mesmos dados (consistência) |
| EC2 | Email muito longo (>255 chars) | Impossível (validação no cadastro) |

---

### 📝 GRUPO B — PRÉ-FILTRO E GESTÃO DE LISTAS

#### UC03 — Selecionar Categorias (Pré-filtro) ⭐ NOVO v3.2 (RF12)

**Happy Paths:**
- **HP1:** Visitante acessa tela inicial → vê 11 categorias macro (Mercado, Vestuário, Automotivos, Informática, Decoração, Móveis, Materiais de Construção, Ferramentas, Livros, Jardinagem, Eletrodomésticos) → seleciona "Mercado" → lista de fornecedores é filtrada dinamicamente.
- **HP2:** Usuário seleciona múltiplas categorias (ex: "Mercado" + "Eletrodomésticos") → fornecedores de ambas categorias aparecem (ex: Carrefour aparece em ambas).

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Nenhuma categoria selecionada | RF12 | Mensagem "Selecione ao menos 1 categoria" + botão "Continuar" desabilitado |
| E2 | API de categorias lenta (>500ms) | RNF09 | Skeleton loading exibido |
| E3 | Categoria inativa (ativo=false) | RF12 | Não aparece na lista |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário seleciona todas as 11 categorias | Todos os fornecedores aparecem (sem filtro) |
| EC2 | Categoria selecionada não tem fornecedores | Toast "Nenhum fornecedor nesta categoria" + sugere outra |
| EC3 | Usuário recarrega página | Seleção perdida (toast informativo) — sessão temporária |
| EC4 | Fornecedor pertence a 5+ categorias | Aparece uma vez na lista com badges de todas categorias |

#### UC01 — Criar Lista em Memória (RF07)

**Happy Paths:**
- **HP1:** Visitante acessa tela inicial → digita nome "Compras do Mês" → adiciona 3 produtos via autocomplete (UC02) → vê subtotal em tempo real → lista armazenada em memória JS (sessionStorage).
- **HP2:** Visitante cria lista → fecha aba → reabre → lista perdida (comportamento esperado — efêmera).

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Nome da lista vazio | RF07 | Mensagem "Informe um nome para a lista" |
| E2 | Quantidade = 0 | RF07 | Validação inline rejeita "Quantidade deve ser ≥ 1" |
| E3 | Produto não encontrado no catálogo | RF07 | Toast "Produto não encontrado, tente outro termo" |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário adiciona mesmo produto 2x | Sistema soma quantidades (não duplica item) |
| EC2 | Nome da lista >100 chars | Contador visual "X/100" + bloqueio de digitação |
| EC3 | Quantidade = 10000 (limite) | Validação rejeita "Máximo 9999" |
| EC4 | sessionStorage cheio (~5MB) | Toast "Memória cheia. Salve a lista ou remova itens." |

#### UC02 — Buscar Produtos (Autocomplete) (RF07)

**Happy Paths:**
- **HP1:** Usuário digita "arr" → debounce 300ms → API retorna ["Arroz Tipo 1 5kg", "Arroz Integral 1kg"] → lista exibida.
- **HP2:** Usuário seleciona "Arroz Tipo 1 5kg" → adicionado à lista com quantidade padrão 1 → subtotal atualizado.

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Termo com <2 caracteres | RF07 | Busca não iniciada |
| E2 | API lenta (>500ms) | RNF09 | Skeleton loading exibido |
| E3 | Nenhum resultado | RF07 | Mensagem "Nenhum produto encontrado" |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário digita rapidamente "arroz integral" | Debounce 300ms → apenas última requisição é processada |
| EC2 | Produto com nome muito longo (>200 chars) | Truncado com "..." no autocomplete |
| EC3 | Caracteres especiais na busca (acentos) | Busca case-insensitive + acentos normalizados |
| EC4 | Cache frontend expirado (5min) | Nova requisição à API |

#### UC14 — Salvar Lista (Persistir) (RF08)

**Happy Paths:**
- **HP1:** Usuário autenticado clica "Salvar" → backend valida FK de produto (UC20) + valida categorias selecionadas (UC03) → INSERT em `listas` + `itens_lista` (transação ACID) → retorna 201 → toast "Lista salva com sucesso".
- **HP2:** Usuário promove lista efêmera (UC17) → modal confirma → transação ACID → lista persistida.

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Não autenticado | RF08 | Modal de login aparece |
| E2 | Produto foi descontinuado (ativo=false) | RF08 | Toast "Produto indisponível, remova da lista" |
| E3 | Erro de conexão | RF08 | Toast "Falha ao salvar, tente novamente" |
| E4 | Nenhuma categoria selecionada (UC03) | RF08 + UC03 | Toast "Selecione ao menos 1 categoria antes de salvar" |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Lista com 100+ itens | Transação ACID garante atomicidade (tudo ou nada) |
| EC2 | Produto removido do catálogo durante salvamento | Rollback da transação + toast "Produto indisponível" |
| EC3 | Usuário clica "Salvar" 2x rapidamente | Botão desabilitado após primeiro clique |
| EC4 | MySQL InnoDB em lock (concorrência) | busy_timeout=5000 → retry automático |

#### UC17 — Promover Lista Efêmera ⭐ NOVO v3.2 (RF08)

**Happy Paths:**
- **HP1:** Usuário faz login com lista efêmera ativa → modal "Deseja salvar esta lista?" → SIM → UC14 (Salvar Lista) é disparado → lista persistida no DB.
- **HP2:** Usuário faz login → modal aparece → NÃO → lista permanece em sessionStorage (efêmera).

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Lista efêmera vazia | RF08 | Modal não aparece |
| E2 | Erro ao promover | RF08 | Toast "Falha ao salvar lista" + mantém efêmera |
| E3 | Usuário fecha modal (X) | RF08 | Lista permanece efêmera |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário faz login, fecha modal, faz logout, faz login novamente | Modal reaparece (lista ainda efêmera) |
| EC2 | Lista efêmera com produto descontinuado | Toast "Produto indisponível" + mantém efêmera |
| EC3 | sessionStorage corrompido | Lista perdida + toast "Erro ao carregar lista" |

#### UC15 — Listar Minhas Listas (RF09)

**Happy Paths:**
- **HP1:** Usuário autenticado acessa /dashboard → vê lista paginada (20/página) ordenada por data criação DESC → exibe nome, data, qtd itens, valor estimado.
- **HP2:** Usuário busca por nome → filtro case-insensitive aplicado → resultados filtrados.

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Nenhuma lista | RF09 | Mensagem "Você ainda não tem listas salvas" + botão "Criar lista" |
| E2 | Página inválida (ex: /dashboard?page=999) | RF09 | Redireciona para página 1 |
| E3 | Erro de carregamento | RF09 | Toast "Falha ao carregar listas" |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário tem 1000+ listas | Paginação 20/página → 50 páginas |
| EC2 | Lista com `deletado_em` preenchido | Não aparece na listagem (soft delete) |
| EC3 | Busca com caracteres especiais | Filtro case-insensitive + acentos normalizados |
| EC4 | Ordenação por nome (não data) | Futuro: botão de ordenação (fora do MVP) |

#### UC13 — Editar/Excluir Lista Salva (RF10, RF11)

**Happy Paths:**
- **HP1 (Editar):** Usuário altera nome → salva → UPDATE em `listas` → toast "Lista atualizada".
- **HP2 (Excluir):** Usuário clica "Excluir" → modal pede digitar nome da lista → confirmação → UPDATE `deletado_em` (soft delete) → toast "Lista excluída".

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Lista não pertence ao usuário | RF10, RF11 | HTTP 403 Forbidden |
| E2 | Confirmação de exclusão não digitada | RF11 | Botão "Excluir" desabilitado |
| E3 | Lista já excluída (deletado_em preenchido) | RF11 | Mensagem "Lista não encontrada" |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário edita lista em 2 abas simultaneamente | Última gravação vence (optimistic locking) |
| EC2 | Usuário exclui lista durante edição em outra aba | Toast "Lista foi excluída" + redireciona para /dashboard |
| EC3 | Nome da lista com caracteres especiais | Aceito (UTF-8) — validação 1-100 chars |

---

### 🔄 GRUPO C — COMPARAÇÃO DE FORNECEDORES

#### UC04 — Selecionar Fornecedores (RF13)

**Happy Paths:**
- **HP1:** Usuário vê fornecedores filtrados por categorias selecionadas (UC03) → checkboxes com nome + % disponibilidade → seleciona 3 fornecedores.
- **HP2:** Usuário clica "Selecionar Todos" → todos os fornecedores filtrados marcados.

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Seleciona apenas 1 fornecedor | RF13 | Botão "Calcular" desabilitado + mensagem "Selecione ao menos 2" |
| E2 | Fornecedor inativo (ativo=false) | RF13 | Não aparece na lista |
| E3 | Recarrega página | RF13 | Seleção perdida (toast informativo) — sessão temporária |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Nenhum fornecedor nas categorias selecionadas | Toast "Nenhum fornecedor disponível" + sugere outras categorias |
| EC2 | Usuário seleciona todos os 10 fornecedores | Permitido (dentro do limite) |
| EC3 | Fornecedor com 0% de disponibilidade | Aparece com badge "0%" + tooltip "Não possui itens da lista" |
| EC4 | Filtro de disponibilidade (UC05) elimina fornecedor selecionado | Sistema mantém checkbox ativo SE ainda passar no filtro |

#### UC05 — Filtrar por Disponibilidade (RF14)

**Happy Paths:**
- **HP1:** Usuário move slider para 70% → lista reduz para fornecedores com ≥70% de disponibilidade.
- **HP2:** Usuário volta slider para 0% → todos os fornecedores reaparecem.

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Filtro 100% elimina todos | RF14 | Mensagem "Nenhum fornecedor atende ao filtro" + sugere reduzir % |
| E2 | Filtro desmarca fornecedor já selecionado | RF14 | Sistema mantém se ainda válido |
| E3 | Valor fora do range (0-100) | RF14 | Validação rejeita |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Slider em 50% → 6 fornecedores → usuário seleciona 3 → slider em 80% → 2 fornecedores | Seleção mantida apenas para os 2 que ainda passam no filtro |
| EC2 | Usuário move slider rapidamente | Debounce 100ms → apenas último valor processado |
| EC3 | Fornecedor com exatamente 70% de disponibilidade | Incluido (≥70%) |

> **⚠️ Dualidade Documentada:** UC05 aparece como `<<include>>` (depende de UC04 para existir) E `<<extend>>` (é opcional sobre UC04). Filtro PRECISA da seleção para operar (include), mas usuário PODE optar por não aplicá-lo (extend).

#### UC06 — Calcular Orçamento (RF15)

**Happy Paths:**
- **HP1:** Usuário clica "Calcular" → backend valida lista + seleção → UC25 (Fornecedores) + UC26 (Preços) → retorna tabela flat em 200ms → cache 5min.
- **HP2:** Usuário altera seleção → cache invalidado → novo cálculo disparado.

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Timeout >10s | RF15 | Toast "Tempo esgotado, tente menos fornecedores" |
| E2 | Lista excluída em outra aba | RF15 | Redireciona para /dashboard + toast "Lista não encontrada" |
| E3 | Fornecedor sem preço para produto | RF15 | Ícone alerta ⚠️ + valor "N/D" |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Lista com 100 itens + 10 fornecedores | Cálculo em <2s (RNF09) |
| EC2 | Cache expirado (5min) | Nova requisição à API |
| EC3 | Produto com preço = 0 | Ícone alerta ⚠️ + valor "R$ 0,00" |
| EC4 | Todos fornecedores com mesmo preço | Mensagem "Empate técnico" |

#### UC07 — Visualizar Resultados (RF16)

**Happy Paths:**
- **HP1:** Tabela exibe fornecedores ordenados por preço ASC → menor destacado em verde → exibe % disponibilidade.
- **HP2:** Usuário passa mouse sobre item ausente → tooltip mostra detalhes (produto, quantidade, motivo).

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Todos fornecedores com preço igual | RF16 | Mensagem "Empate técnico" |
| E2 | Lista vazia | RF16 | Redireciona para criação de lista |
| E3 | Erro de formatação (moeda) | RF16 | Fallback para formato genérico "R$ X,XX" |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Tabela com 10 fornecedores + 50 itens | Scroll horizontal + sticky header |
| EC2 | Nome de fornecedor muito longo | Truncado com "..." + tooltip completo |
| EC3 | Preço muito alto (>R$ 999.999,99) | Exibido normalmente (DECIMAL(10,2)) |

---

### 📤 GRUPO D — EXPORTAÇÃO

#### UC08 — Exportar Lista PDF ⭐ NOVO v3.2 (RF17)

**Happy Paths:**
- **HP1:** Usuário clica "Exportar PDF" → backend UC29 (Gerar PDF via ReportLab) → gera PDF A4 → download inicia com nome `lista_20260914.pdf`.
- **HP2:** Visitante (sem login) exporta lista em memória → backend gera PDF → funciona normalmente.

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Erro ao gerar PDF | RF17 | Toast "Falha ao gerar PDF. Tente novamente." |
| E2 | Lista muito grande (>100 itens) | RF17 | PDF gerado em múltiplas páginas (quebras automáticas) |
| E3 | Nome da lista com caracteres especiais | RF17 | Escaping automático no nome do arquivo |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Usuário clica "Exportar PDF" 2x rapidamente | Botão desabilitado após primeiro clique |
| EC2 | PDF >10MB | Geração assíncrona + toast "Gerando PDF..." |
| EC3 | Fonte especial no nome da lista | ReportLab suporta UTF-8 |
| EC4 | Usuário cancela download | Nenhum erro; estado preservado |

#### UC09 — Imprimir (RF18)

**Happy Paths:**
- **HP1:** Usuário clica "Imprimir" → CSS `@media print` oculta menus → diálogo nativo abre → impressão em A4.
- **HP2:** Impressão com quebras automáticas de página + cores preservadas (melhor oferta em verde).

**Exceções:**

| # | Exceção | Guard-Rail | Resposta do Sistema |
|---|---------|------------|---------------------|
| E1 | Tela <1024px | RNF04 | Aviso "Impressão otimizada para telas ≥1024px" |
| E2 | Usuário cancela diálogo | RF18 | Nenhum erro; estado preservado |
| E3 | Impressora offline | RF18 | Erro do navegador tratado |

**Edge-Cases:**

| # | Cenário | Comportamento Esperado |
|---|---------|------------------------|
| EC1 | Tabela com 50+ linhas | Quebras automáticas + header repetido em cada página |
| EC2 | Usuário imprime em PDF (via navegador) | Funciona normalmente (browser print-to-PDF) |
| EC3 | Cores desabilitadas no navegador | Versão P&B legível (fallback) |

---

## 🔗 MATRIZ DE RELAÇÕES UML

### Relações `<<include>>` (Obrigatórias) — 16 relações

| # | Origem | Destino | Rótulo Descritivo | Justificativa |
|---|--------|---------|-------------------|---------------|
| 1 | UC09 (Cadastrar) | UC20 (Validar) | "valida dados de cadastro" | Validação cross-cutting Pydantic |
| 2 | UC09 (Cadastrar) | UC21 (Hash) | "hasheia senha (bcrypt)" | Segurança — salt=12 |
| 3 | UC10 (Login) | UC22 (Gerar Sessão) | "gera JWT access + refresh" | Autenticação stateless |
| 4 | UC10 (Login) | UC27 (Rate Limit) | "aplica rate limiting (6/15min)" | Anti-DDoS |
| 5 | UC12 (Recuperar) | UC27 (Rate Limit) | "aplica rate limiting" | Anti-abuso |
| 6 | UC16 (Gerenciar Perfil) | UC20 (Validar) | "valida dados do perfil" | Consistência |
| 7 | UC14 (Salvar Lista) | UC20 (Validar) | "valida FK de produto" | Integridade referencial |
| 8 | **UC14 (Salvar Lista)** | **UC03 (Categorias)** ⭐ | **"valida categorias selecionadas"** | **NOVO v3.2 — Pré-requisito** |
| 9 | UC02 (Autocomplete) | UC23 (Catálogo) | "consulta catálogo de produtos" | Busca no seed |
| 10 | **UC03 (Categorias)** | **UC24 (Categorias)** ⭐ | **"lista categorias macro"** | **NOVO v3.2 — Pré-filtro** |
| 11 | **UC04 (Fornecedores)** | **UC25 (Fornecedores)** ⭐ | **"lista fornecedores filtrados por categoria"** | **AJUSTADO v3.2 — Pré-filtro** |
| 12 | UC06 (Calcular) | UC20 (Validar) | "valida lista e seleção" | Integridade |
| 13 | UC06 (Calcular) | UC25 (Fornecedores) | "busca fornecedores selecionados" | Cálculo |
| 14 | UC06 (Calcular) | UC26 (Preços) | "busca preços dos produtos" | Cálculo |
| 15 | **UC08 (PDF)** | **UC29 (Gerar PDF)** ⭐ | **"gera PDF server-side (ReportLab)"** | **NOVO v3.2** |
| 16 | UC11 (Logout) | UC28 (Invalidar) | "invalida refresh token" | Segurança |

### Relações `<<extend>>` (Opcionais) — 5 relações

| # | Origem | Destino | Rótulo Descritivo | Condição |
|---|--------|---------|-------------------|----------|
| 1 | UC05 (Filtro) | UC04 (Seleção) | "filtra fornecedores por disponibilidade" | Se usuário aplicar slider |
| 2 | **UC08 (PDF)** | **UC07 (Resultados)** ⭐ | **"exporta resultados em PDF"** | **Após visualização** |
| 3 | UC09 (Imprimir) | UC07 (Resultados) | "imprime resultados em A4" | Após visualização |
| 4 | UC16 (Perfil) | UC18 (Visualizar) | "edita dados do perfil" | Se usuário optar |
| 5 | UC17 (Promover) | UC14 (Salvar) | "promove lista efêmera para persistente" | Após login com lista ativa |

---

## 📊 MATRIZ DE RASTREABILIDADE (RF → UC)

| RF | UC Principal | UCs Internos | Prioridade |
|----|-------------|-------------|------------|
| RF01 | UC09 | UC20, UC21 | P0 |
| RF02 | UC10 | UC22, UC27 | P0 |
| RF03 | UC11 | UC28 | P0 |
| RF04 | UC12 | UC27 | P1 |
| RF05 | UC18 | — | P1 |
| RF06 | UC16 | UC20 | P1 |
| RF07 | UC01, UC02 | UC23 | P0 |
| RF08 | UC14, UC17 | UC20, UC03 | P0 |
| RF09 | UC15 | — | P0 |
| RF10 | UC13 | UC20 | P1 |
| RF11 | UC13 | — | P1 |
| RF12 | UC03 ⭐ | UC24 ⭐ | P0 |
| RF13 | UC04 | UC25 | P0 |
| RF14 | UC05 | UC04 | P1 |
| RF15 | UC06 | UC20, UC25, UC26 | P0 |
| RF16 | UC07 | — | P0 |
| RF17 | UC08 ⭐ | UC29 ⭐ | P0 |
| RF18 | UC09 | — | P1 |

---

## 📈 RESUMO QUANTITATIVO

| Categoria | Quantidade | Detalhamento |
|-----------|------------|--------------|
| **Atores** | 4 | Visitante, Usuário Autenticado, Sistema, API Mock |
| **Casos de Uso Principais** | 19 | 13 P0 + 6 P1 |
| **Casos de Uso Internos** | 10 | Todos auxiliares de domínio |
| **Total de Casos de Uso** | 29 | — |
| **Relações `<<include>>`** | 16 | Obrigatórias |
| **Relações `<<extend>>`** | 5 | Opcionais |
| **Total de Relações UML** | 21 | Todas nomeadas em PT-BR |
| **Happy Paths documentados** | 38 | 2 por UC principal |
| **Exceções documentadas** | 57 | 3 por UC principal |
| **Edge-cases documentados** | 60+ | Cobertura de cenários críticos |
| **Áreas funcionais** | 5 | Auth, Pré-filtro/Listas, Comparação, Exportação, Internos |

---

## ✅ VALIDAÇÃO DE PRINCÍPIOS UML

| Princípio | Status | Observação |
|-----------|--------|------------|
| Separação Ator Primário/Secundário | ✅ | Visitante/Usuário Autenticado (primários) vs Sistema/API (secundários) |
| Boundary do Sistema | ✅ | Todos os 29 UCs dentro do boundary |
| Generalização de Atores | ✅ | Usuário Autenticado generaliza Visitante |
| Cardinalidade das Associações | ✅ | 1:N (ator → múltiplos UCs) respeitada |
| Direção das Setas | ✅ | `<<include>>` e `<<extend>>` apontam corretamente |
| Coesão de Áreas | ✅ | 5 áreas funcionais bem definidas |
| Ausência de Ciclos | ✅ | Não há loops nas relações |
| Nenhum UC Solitário | ✅ | Todos conectados a pelo menos um ator ou relação |
| Rótulos Descritivos | ✅ | Todas as 21 relações nomeadas em português |

---

## 🔄 FLUXO PRINCIPAL DO SISTEMA

```
1. Visitante acessa aplicação
   ↓
2. UC03: Seleciona CATEGORIAS (pré-filtro) ⭐
   ↓
3. UC01: Cria LISTA de produtos (em memória)
   ↓
4. UC04: Seleciona FORNECEDORES (filtrado por categorias)
   ↓
5. UC05: [Opcional] Filtra por disponibilidade
   ↓
6. UC06: Calcula orçamento (tabela flat)
   ↓
7. UC07: Visualiza resultados
   ↓
8. UC08/UC09: Exporta PDF ou imprime
   ↓
9. [Se autenticado] UC14: Salva lista no DB
```

---

**FIM DO LEVANTAMENTO OFICIAL DE CASOS DE USO — COBECO MVP v3.2**