# 📋 ANÁLISE COMPLETA DO SISTEMA COBECO — MVP Acadêmico v3.1

**Documento Consolidado de Engenharia de Requisitos e Modelagem UML**  
**Data:** 12 de Setembro de 2026  
**Status:** ✅ SSOT (Single Source of Truth)  
**Base:** Relatório Analítico Final v3.1 + Documentos de Refinamento

---

## 🔍 PARTE 1 — ANÁLISE DE FALHAS DE NEGÓCIO E LÓGICA SISTÊMICA

### 1.1 Inconsistências Identificadas nos Documentos

| # | Falha | Severidade | Descrição | Solução Proposta |
|---|-------|-----------|-----------|------------------|
| **F1** | Conflito de Stack Tecnológica | 🔴 Crítico | Documentos `Refinamento_de_Requisitos.md` e `Report_Espec_MVP.md` ainda referenciam PostgreSQL/NestJS/React/TypeScript, enquanto o Relatório Final v3.1 define SQLite3/FastAPI/Vanilla JS - Nota de revisão: alterar SGBD para MySql | **Consolidar em v3.1**: Stack minimalista é a oficial. Arquivar documentos anteriores como "histórico". |
| **F2** | Rate Limiting Inconsistente | 🟡 Médio | Alguns documentos definem 5 tentativas/15min, outros 6 tentativas | **Padronizar em 6 tentativas** conforme requisito explícito do projeto (anti-DDoS) |
| **F3** | Recuperação de Senha Ambígua | 🟡 Médio | Alguns docs falam em Resend (email real), outros em pergunta de segurança | **Dupla via aprovada**: Via A (log no stdout para dev) + Via B (pergunta de segurança para produção acadêmica), toggle via env var `RECOVERY_MODE` |
| **F4** | Modelo de Categorias Incorreto (v3.0) | 🔴 Crítico | DER v3.0 relacionava `products` diretamente com `categories` via FK `category_id`, contradizendo a semântica real (categorias são de FORNECEDORES) | **DER v3.1**: Tabela pivô `supplier_categories` (N:N). Produtos são agnósticos à categoria. |
| **F5** | Dualidade UC26 (Include + Extend) | 🟡 Médio | UC26 aparece como `<<include>>` (depende de UC25) E `<<extend>>` (é opcional sobre UC25) simultaneamente | **Documentar dualidade intencional**: Filtro PRECISA da seleção para existir (include), mas usuário PODE optar por não aplicá-lo (extend). Registrar no glossário. |
| **F6** | Export CSV Server-Side vs Client-Side | 🟢 Baixo | Alguns docs mencionam endpoint de export, outros definem Blob client-side | **Client-side (ADR-005)**: Geração via `Blob` + `URL.createObjectURL()`. Zero carga no backend. Funciona para visitantes. |
| **F7** | Persistência de Comparações | 🟢 Baixo | Alguns docs mencionam histórico de comparações, outros excluem explicitamente | **Não persistir comparações**: Apenas listas são persistidas. Seleção de fornecedores é temporária (sessão). |
| **F8** | Tela de Entrada Ambígua | 🟡 Médio | Alguns docs definem login como tela inicial, outros definem "Criar Lista" | **"Criar Lista" como tela de entrada**: Reduz fricção. Login é "lazy" — só exigido ao salvar. |
| **F9** | JWT Access Token em localStorage | 🔴 Crítico | Alguns docs sugerem localStorage para access token (vulnerável a XSS) | **Memória JS apenas**: Access token em variável (não persiste). Refresh token em cookie httpOnly. |
| **F10** | Soft Delete vs Hard Delete | 🟡 Médio | Alguns RFs falam em "remover permanentemente", outros em "soft delete" | **Soft delete consistente**: Campo `deleted_at` em `lists` e `users`. Dados preservados para auditoria. |

### 1.2 Falhas de Lógica Sistêmica Identificadas

| # | Falha | Impacto | Solução |
|---|-------|---------|---------|
| **L1** | Lista efêmera sem "promoção" | Usuário cria lista, faz login, perde dados | **Modal de promoção**: Ao fazer login, perguntar "Deseja salvar esta lista?" → move de `sessionStorage` para DB |
| **L2** | Filtro de disponibilidade quebra seleção | Usuário seleciona fornecedores, aplica filtro, perde seleção | **Manter seleção válida**: Se fornecedor ainda passa no filtro após mudança, manter checkbox ativo |
| **L3** | Cache de comparação não invalida | Usuário altera lista, vê resultados antigos | **Invalidar cache**: Se lista ou seleção mudar, descartar cache de 5min |
| **L4** | Categoria obrigatória limita flexibilidade | Usuário não pode criar lista com itens de categorias diferentes | **Categoria opcional**: Se definida, pré-filtra fornecedores. Se não, mostra todos. |
| **L5** | Rate limiting por IP é insuficiente | Usuário atrás de NAT (empresa/escola) bloqueia todos | **Rate limiting híbrido**: Por IP + por username (após login) |
| **L6** | Autocomplete sem debounce | Múltiplas requisições ao digitar | **Debounce 300ms** + cache frontend 5min |
| **L7** | Export CSV sem BOM | Excel PT-BR não reconhece acentos | **UTF-8 + BOM** (`\uFEFF`) obrigatório |
| **L8** | Impressão sem @media print | Menus e botões aparecem na impressão | **CSS `@media print`** oculta elementos não essenciais |

### 1.3 Soluções Propostas Consolidadas

| Falha | Solução | Responsável | Prazo |
|-------|---------|-------------|-------|
| F1-F10 | Atualizar SSOT para v3.1 | Arquiteto | Dia 1 |
| L1 | Implementar modal de promoção | Frontend Dev | Sprint 2 |
| L2 | Lógica de manutenção de seleção | Frontend Dev | Sprint 3 |
| L3 | Invalidação de cache | Backend Dev | Sprint 3 |
| L4 | Categoria opcional no schema | Backend Dev | Sprint 2 |
| L5 | Rate limiting híbrido | Backend Dev | Sprint 1 |
| L6 | Debounce + cache | Frontend Dev | Sprint 2 |
| L7 | BOM no export | Frontend Dev | Sprint 4 |
| L8 | CSS @media print | Frontend Dev | Sprint 4 |

---

## 📋 PARTE 2 — LISTA DE REQUISITOS DO SISTEMA COBECO

### 2.1 Requisitos Funcionais (RF) — Versão Final v3.1

#### 🔐 Grupo A — Autenticação e Perfil (RF01–RF06)

| ID | Requisito | Descrição | Guard-Rails | Prioridade |
|----|-----------|-----------|-------------|------------|
| **RF01** | **Cadastrar Usuário** | Criar conta com username (único), email, senha + confirmação, pergunta de segurança | Username: 3-30 chars, alfanumérico. Senha: mín 8 chars, 1 maiúscula, 1 número, 1 especial. Email: formato válido. Confirmação idêntica. Pergunta obrigatória. | **P0** |
| **RF02** | **Login** | Autenticar via username + senha | **6 tentativas consecutivas** → lockout 15min (anti-DDoS). Mensagem genérica: "Credenciais inválidas". Sessão via JWT (access 15min em memória + refresh 7d httpOnly). | **P0** |
| **RF03** | **Logout** | Encerrar sessão ativa | Invalidar cookie de sessão. Limpar access token da memória. Redirecionar para tela de criação de lista. | **P0** |
| **RF04** | **Recuperar Senha** | Reset via pergunta de segurança (sem email) | Pergunta definida no cadastro. 3 tentativas de resposta. Nova senha segue regras do RF01. Modo alternativo: token logado no stdout (env `RECOVERY_MODE=log`). | **P1** |
| **RF05** | **Visualizar Perfil** | Ver dados pessoais (username, email, nome) | Apenas usuário autenticado. Username é read-only. | **P1** |
| **RF06** | **Editar Perfil** | Alterar email, nome e senha | Senha antiga obrigatória para qualquer alteração. Email único. | **P1** |

#### 📝 Grupo B — Gestão de Listas (RF07–RF11)

| ID | Requisito | Descrição | Guard-Rails | Prioridade |
|----|-----------|-----------|-------------|------------|
| **RF07** | **Criar Lista (em memória)** | Qualquer usuário cria lista com nome + itens (produto + quantidade) | Mínimo 1 item. Quantidade: 1-9999. Produto deve existir no catálogo (autocomplete). Lista reside em memória JS até salvar. | **P0** |
| **RF08** | **Salvar Lista (persistir)** | Persistir lista no banco de dados | **Requer autenticação**. Se não logado → modal de login. Validação de FK de produto. ACID: transação para lista + itens. | **P0** |
| **RF09** | **Listar Minhas Listas** | Exibir listas salvas do usuário autenticado | Paginação simples (20/página). Ordenação: data criação DESC. Soft delete (excluídas não aparecem). | **P0** |
| **RF10** | **Editar Lista Salva** | Alterar nome, itens, quantidades de lista persistida | Validação de propriedade (user_id). Confirmação antes de remover item. | **P1** |
| **RF11** | **Excluir Lista Salva** | Remover lista do banco (soft delete) | Confirmação obrigatória. Soft delete (campo `deleted_at`). | **P1** |

#### 🔄 Grupo C — Comparação de Fornecedores (RF12–RF15)

| ID | Requisito | Descrição | Guard-Rails | Prioridade |
|----|-----------|-----------|-------------|------------|
| **RF12** | **Selecionar Fornecedores** | Escolher quais fornecedores comparar (mínimo 2) | Checkboxes com nome + % disponibilidade. Máximo: todos os fornecedores do seed. Seleção em memória (não persiste). | **P0** |
| **RF13** | **Filtrar por Disponibilidade** | Slider 0-100% para filtrar fornecedores | Padrão: 0% (mostrar todos). Atualiza checkboxes em tempo real. Mantém seleção válida. | **P1** |
| **RF14** | **Calcular Orçamento** | Gerar tabela flat comparativa | Timeout 10s. Cache 5min. Calcular: itens disponíveis, ausentes, preço total. Ordenar por preço ASC. | **P0** |
| **RF15** | **Visualizar Resultados** | Tabela com destaque de melhor oferta | Destacar menor preço (verde). Mostrar % disponibilidade. Tooltip de itens ausentes. | **P0** |

#### 📤 Grupo D — Exportação (RF16–RF17)

| ID | Requisito | Descrição | Guard-Rails | Prioridade |
|----|-----------|-----------|-------------|------------|
| **RF16** | **Exportar Lista CSV** | Download de lista em CSV | **Funciona para TODOS os usuários** (sem login). UTF-8 + BOM. Delimitador `;`. Nome: `lista_YYYYMMDD.csv`. | **P0** |
| **RF17** | **Imprimir** | View otimizada para Ctrl+P | CSS `@media print`. Oculta menus. Formatação A4. | **P1** |

### 2.2 Requisitos Não Funcionais (RNF)

| ID | Requisito | Descrição | Métrica |
|----|-----------|-----------|---------|
| **RNF01** | Clean Architecture | Camadas: Domain → UseCase → Adapter → Framework | Code review |
| **RNF02** | SDD (OpenAPI First) | Contrato OpenAPI 3.0 antes de implementar | Swagger em `/docs` |
| **RNF03** | ACID (SQLite3) | Transações explícitas, WAL mode | Zero dados órfãos |
| **RNF04** | Desktop-Only | Layout exclusivo ≥1024px. Sem mobile. | Breakpoint único |
| **RNF05** | Feedback Visual | Toasts, loading states, modais | <100ms feedback |
| **RNF06** | Testes Unitários | Cobertura ≥80% das regras de negócio | pytest --cov |
| **RNF07** | CI/CD (Docker) | Docker Compose para dev. GitHub Actions para CI. | Pipeline <5min |
| **RNF08** | Seed de Dados | 10 fornecedores + 50 produtos + 5 categorias | `make seed` <10s |
| **RNF09** | Performance | API <500ms p95 | curl + time |
| **RNF10** | Segurança | Rate limiting 6 req/15min. Hash bcrypt. JWT access em memória. | Zero brute-force |

### 2.3 Requisitos Desejáveis (Backlog Pós-MVP)

| ID | Requisito | Descrição | Prioridade |
|----|-----------|-----------|------------|
| **RD01** | Histórico de Comparações | Persistir resultados de comparações anteriores | P3 |
| **RD02** | Importação de Lista via CSV | Upload de CSV para criar lista | P3 |
| **RD03** | Notificações de Preço | Alertar quando preço de item da lista cair | P3 |
| **RD04** | Compartilhamento de Lista | Link público para compartilhar lista | P3 |
| **RD05** | App Mobile (PWA) | Versão responsiva para mobile | P3 |
| **RD06** | Integração com Fornecedores Reais | Web scraping de preços em tempo real | P4 |
| **RD07** | Recomendações por IA | Sugerir fornecedores baseado em histórico | P4 |
| **RD08** | Multi-idioma | Suporte a inglês e espanhol | P4 |

---

## 🎯 PARTE 3 — CATÁLOGO DE CASOS DE USO

### 3.1 Atores do Sistema

| Ator | Tipo | Papel | Generalização |
|------|------|-------|---------------|
| **Visitante** | Primário | Usuário não autenticado. Pode criar listas em memória, comparar e exportar. | Ator base |
| **Usuário Autenticado** | Primário | Visitante que fez login. Herda todos os casos do Visitante + adiciona persistência. | **Generaliza Visitante** |
| **Sistema** | Secundário | Validações, hashing, JWT, rate limiting, sessão. | — |
| **API de Fornecedores** | Secundário | Fornece catálogo, fornecedores e preços via endpoints mockados. | — |

> **⚠️ Nota UML:** "Usuário Autenticado" é uma **generalização** de "Visitante". Isso significa que todo Usuário Autenticado também é Visitante, mas com capacidades adicionais.

### 3.2 Casos de Uso Principais (18)

| ID | Caso de Uso | Ator Primário | RF | Área |
|----|-------------|---------------|----|---- |
| UC01 | Criar Lista em Memória | Visitante | RF07 | Listas |
| UC02 | Buscar Produtos (Autocomplete) | Visitante | RF07 | Listas |
| UC03 | Selecionar Fornecedores | Visitante | RF12 | Comparação |
| UC04 | Filtrar por Disponibilidade | Visitante | RF13 | Comparação |
| UC05 | Calcular Orçamento | Visitante | RF14 | Comparação |
| UC06 | Visualizar Resultados | Visitante | RF15 | Comparação |
| UC07 | Exportar Lista CSV | Visitante | RF16 | Exportação |
| UC08 | Imprimir | Visitante | RF17 | Exportação |
| UC09 | Cadastrar-se | Visitante | RF01 | Auth |
| UC10 | Realizar Login | Visitante | RF02 | Auth |
| UC11 | Realizar Logout | Usuário Autenticado | RF03 | Auth |
| UC12 | Recuperar Senha | Visitante | RF04 | Auth |
| UC13 | Salvar Lista (Persistir) | Usuário Autenticado | RF08 | Listas |
| UC14 | Listar Minhas Listas | Usuário Autenticado | RF09 | Listas |
| UC15 | Editar/Excluir Lista Salva | Usuário Autenticado | RF10, RF11 | Listas |
| UC16 | Gerenciar Perfil | Usuário Autenticado | RF05, RF06 | Auth |
| UC17 | Promover Lista Efêmera | Usuário Autenticado | RF08 | Listas |
| UC18 | Visualizar Perfil | Usuário Autenticado | RF05 | Auth |

### 3.3 Casos de Uso Internos (8)

| ID | Caso de Uso | Ator | Descrição |
|----|-------------|------|-----------|
| UC19 | Validar Dados | Sistema | Validação cross-cutting (Pydantic schemas) |
| UC20 | Hash de Senha | Sistema | bcrypt salt=12 |
| UC21 | Gerar Sessão | Sistema | JWT access + refresh cookie httpOnly |
| UC22 | Fornecer Catálogo | API Fornecedores | Seed: 50 produtos |
| UC23 | Fornecer Fornecedores | API Fornecedores | Seed: 10 fornecedores |
| UC24 | Fornecer Preços | API Fornecedores | Seed: ~300 preços |
| UC25 | Aplicar Rate Limiting | Sistema | 6 tentativas/15min |
| UC26 | Invalidar Sessão | Sistema | Logout + rotação de tokens |

---

## 🔄 PARTE 4 — FLUXOS DETALHADOS (2 Happy Paths + 3 Exceções por UC)

### UC01 — Criar Lista em Memória

**Happy Path 1:** Visitante acessa tela inicial, digita nome "Compras do Mês", adiciona 3 produtos via autocomplete, vê subtotal em tempo real.  
**Happy Path 2:** Visitante cria lista, fecha aba, reabre — lista perdida (comportamento esperado).  

**Exceções:**
- **E1:** Nome da lista vazio → mensagem "Informe um nome para a lista"
- **E2:** Quantidade = 0 → validação inline rejeita
- **E3:** Produto não encontrado no catálogo → toast "Produto não encontrado, tente outro termo"

---

### UC02 — Buscar Produtos (Autocomplete)

**Happy Path 1:** Usuário digita "arr" → debounce 300ms → lista sugere "Arroz Tipo 1 5kg", "Arroz Integral 1kg"  
**Happy Path 2:** Usuário seleciona produto → adicionado à lista com quantidade padrão 1  

**Exceções:**
- **E1:** Termo com <2 caracteres → busca não iniciada
- **E2:** API lenta (>500ms) → skeleton loading exibido
- **E3:** Nenhum resultado → mensagem "Nenhum produto encontrado"

---

### UC03 — Selecionar Fornecedores

**Happy Path 1:** Usuário vê 10 fornecedores com checkboxes + % disponibilidade, seleciona 3  
**Happy Path 2:** Usuário clica "Selecionar Todos" → todos marcados  

**Exceções:**
- **E1:** Seleciona apenas 1 → botão "Calcular" desabilitado + mensagem "Selecione ao menos 2"
- **E2:** Fornecedor inativo → não aparece na lista
- **E3:** Recarrega página → seleção perdida (toast informativo)

---

### UC04 — Filtrar por Disponibilidade

**Happy Path 1:** Usuário move slider para 70% → lista reduz para 6 fornecedores  
**Happy Path 2:** Usuário volta slider para 0% → todos os fornecedores reaparecem  

**Exceções:**
- **E1:** Filtro 100% elimina todos → mensagem "Nenhum fornecedor atende ao filtro"
- **E2:** Filtro desmarca fornecedor já selecionado → sistema mantém se ainda válido
- **E3:** Valor fora do range (0-100) → validação rejeita

---

### UC05 — Calcular Orçamento

**Happy Path 1:** Usuário clica "Calcular" → backend valida → retorna tabela flat em 200ms  
**Happy Path 2:** Usuário altera seleção → cache invalidado → novo cálculo disparado  

**Exceções:**
- **E1:** Timeout >10s → toast "Tempo esgotado, tente menos fornecedores"
- **E2:** Lista excluída em outra aba → redireciona para dashboard + toast "Lista não encontrada"
- **E3:** Fornecedor sem preço → ícone alerta ⚠️ + valor "N/D"

---

### UC06 — Visualizar Resultados

**Happy Path 1:** Tabela exibe fornecedores ordenados por preço, menor destacado em verde  
**Happy Path 2:** Usuário passa mouse sobre item ausente → tooltip mostra detalhes  

**Exceções:**
- **E1:** Todos fornecedores com preço igual → mensagem "Empate técnico"
- **E2:** Lista vazia → redireciona para criação de lista
- **E3:** Erro de formatação (moeda) → fallback para formato genérico

---

### UC07 — Exportar Lista CSV

**Happy Path 1:** Usuário clica "Exportar CSV" → download inicia com nome `lista_20260912.csv`  
**Happy Path 2:** Visitante (sem login) exporta lista em memória → funciona normalmente  

**Exceções:**
- **E1:** Arquivo >1MB → toast "Arquivo muito grande"
- **E2:** Nome com caracteres especiais → escaping automático com aspas
- **E3:** Sem espaço em disco → toast "Falha ao salvar arquivo"

---

### UC08 — Imprimir

**Happy Path 1:** Usuário clica "Imprimir" → CSS @media print oculta menus → diálogo nativo abre  
**Happy Path 2:** Impressão em A4 com quebras automáticas de página  

**Exceções:**
- **E1:** Tela <1024px → aviso "Impressão otimizada para telas ≥1024px"
- **E2:** Usuário cancela diálogo → nenhum erro, estado preservado
- **E3:** Impressora offline → erro do navegador tratado

---

### UC09 — Cadastrar-se

**Happy Path 1:** Usuário preenche formulário → validação frontend → backend hasheia senha → retorna 201  
**Happy Path 2:** Usuário define pergunta de segurança → resposta hasheada com bcrypt  

**Exceções:**
- **E1:** Username já existe → mensagem genérica "Credenciais inválidas"
- **E2:** Senha fraca → erro inline no campo
- **E3:** Email inválido → validação frontend impede submit

---

### UC10 — Realizar Login

**Happy Path 1:** Usuário informa credenciais → backend valida → gera JWT access (15min) + refresh (7d httpOnly)  
**Happy Path 2:** Após login, modal pergunta "Deseja salvar lista atual?" → se sim, promove para DB  

**Exceções:**
- **E1:** 6ª tentativa falha → HTTP 429 + lockout 15min
- **E2:** Credenciais inválidas → mensagem genérica "Credenciais inválidas"
- **E3:** Conta bloqueada → mensagem "Conta temporariamente bloqueada"

---

### UC11 — Realizar Logout

**Happy Path 1:** Usuário clica "Sair" → backend invalida refresh → frontend limpa access → redireciona para home  
**Happy Path 2:** Logout após sessão expirada → redirecionamento automático  

**Exceções:**
- **E1:** Erro de rede → toast "Falha ao encerrar sessão, tente novamente"
- **E2:** Refresh token já expirado → logout forçado sem erro
- **E3:** Múltiplas abas → apenas a aba atual é deslogada

---

### UC12 — Recuperar Senha

**Happy Path 1 (Via B):** Usuário informa username → sistema exibe pergunta → usuário responde → nova senha definida  
**Happy Path 2 (Via A):** Usuário solicita reset → token gerado e logado no stdout → usuário informa token → nova senha  

**Exceções:**
- **E1:** Username não existe → mensagem genérica "Usuário não encontrado"
- **E2:** Resposta errada (3 tentativas) → bloqueio temporário
- **E3:** Token expirado (>15min) → mensagem "Token expirado, solicite novamente"

---

### UC13 — Salvar Lista (Persistir)

**Happy Path 1:** Usuário autenticado clica "Salvar" → lista persistida no DB com ACID  
**Happy Path 2:** Usuário promove lista efêmera → modal confirma → move de sessionStorage para DB  

**Exceções:**
- **E1:** Não autenticado → modal de login aparece
- **E2:** Produto foi descontinuado → toast "Produto indisponível, remova da lista"
- **E3:** Erro de conexão → toast "Falha ao salvar, tente novamente"

---

### UC14 — Listar Minhas Listas

**Happy Path 1:** Usuário vê lista paginada (20/página) ordenada por data  
**Happy Path 2:** Usuário busca por nome → filtro case-insensitive aplicado  

**Exceções:**
- **E1:** Nenhuma lista → mensagem "Você ainda não tem listas salvas"
- **E2:** Página inválida → redireciona para página 1
- **E3:** Erro de carregamento → toast "Falha ao carregar listas"

---

### UC15 — Editar/Excluir Lista Salva

**Happy Path 1 (Editar):** Usuário altera nome → salva → toast "Lista atualizada"  
**Happy Path 2 (Excluir):** Usuário clica "Excluir" → confirmação → soft delete → toast "Lista excluída"  

**Exceções:**
- **E1:** Lista não pertence ao usuário → HTTP 403
- **E2:** Confirmação de exclusão não digitada → botão desabilitado
- **E3:** Lista já excluída → mensagem "Lista não encontrada"

---

### UC16 — Gerenciar Perfil

**Happy Path 1:** Usuário altera email → validação → senha antiga confirmada → atualizado  
**Happy Path 2:** Usuário altera senha → senha antiga obrigatória → nova senha hasheada  

**Exceções:**
- **E1:** Email já existe → mensagem "Email já cadastrado"
- **E2:** Senha antiga incorreta → erro "Senha atual incorreta"
- **E3:** Nova senha igual à antiga → validação rejeita

---

### UC17 — Promover Lista Efêmera

**Happy Path 1:** Usuário faz login → modal "Deseja salvar esta lista?" → SIM → lista persistida  
**Happy Path 2:** Usuário faz login → modal aparece → NÃO → lista permanece em sessionStorage  

**Exceções:**
- **E1:** Lista efêmera vazia → modal não aparece
- **E2:** Erro ao promover → toast "Falha ao salvar lista" + mantém efêmera
- **E3:** Usuário fecha modal → lista permanece efêmera

---

### UC18 — Visualizar Perfil

**Happy Path 1:** Usuário vê dados pessoais (username, email, nome)  
**Happy Path 2:** Usuário vê data de criação da conta  

**Exceções:**
- **E1:** Não autenticado → redireciona para login
- **E2:** Dados corrompidos → toast "Erro ao carregar perfil"
- **E3:** Conta desativada → mensagem "Conta desativada"

---

### UC19–UC26 (Casos Internos)

**UC19 — Validar Dados:** Valida schemas Pydantic em todas requisições  
**UC20 — Hash de Senha:** bcrypt salt=12 no cadastro e alteração  
**UC21 — Gerar Sessão:** JWT access (15min) + refresh (7d httpOnly)  
**UC22 — Fornecer Catálogo:** Retorna 50 produtos do seed  
**UC23 — Fornecer Fornecedores:** Retorna 10 fornecedores com % disponibilidade  
**UC24 — Fornecer Preços:** Retorna ~300 preços do seed  
**UC25 — Aplicar Rate Limiting:** 6 tentativas/15min por IP + username  
**UC26 — Invalidar Sessão:** Logout + rotação de refresh tokens  

*(Casos internos não têm happy paths/exceções detalhados pois são auxiliares)*

---

## 📐 PARTE 5 — DIAGRAMA DE CASOS DE USO (UML) — XML Draw.io

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-09-12T00:00:00.000Z" agent="COBECO MVP v3.1" version="24.0.0" type="device">
  <diagram id="cobeco-ucd-v31" name="COBECO — Casos de Uso MVP v3.1">
    <mxGraphModel dx="2800" dy="2000" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2800" pageHeight="2000" math="0" shadow="1">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- ===================== TÍTULO ===================== -->
        <mxCell id="title" value="&lt;b&gt;Diagrama de Casos de Uso — COBECO MVP v3.1&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:11px;&quot; color=&quot;#666&quot;&gt;26 Casos de Uso (18 principais + 8 internos) • 4 Atores • 12/09/2026&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontColor=#1A237E;" vertex="1" parent="1">
          <mxGeometry x="700" y="20" width="1400" height="55" as="geometry"/>
        </mxCell>

        <!-- ===================== BOUNDARY DO SISTEMA ===================== -->
        <mxCell id="boundary" value="Sistema COBECO — Comparador de Compras (MVP v3.1)" style="swimlane;startSize=35;fillColor=#FAFAFA;strokeColor=#1A237E;fontStyle=1;fontSize=15;rounded=1;arcSize=4;shadow=1;strokeWidth=2;swimlaneLine=0;" vertex="1" parent="1">
          <mxGeometry x="450" y="100" width="1900" height="1700" as="geometry"/>
        </mxCell>

        <!-- ===================== ATORES ===================== -->
        <mxCell id="actorVisitor" value="Visitante&#xa;(Não Autenticado)" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontSize=13;fontStyle=1;fillColor=#FFEBEE;strokeColor=#C62828;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="150" y="300" width="50" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="actorAuth" value="Usuário&#xa;Autenticado" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontSize=13;fontStyle=1;fillColor=#E8F5E9;strokeColor=#2E7D32;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="150" y="900" width="50" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="actorSystem" value="Sistema" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontSize=13;fontStyle=1;fillColor=#FFF3E0;strokeColor=#E65100;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="2500" y="300" width="50" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="actorAPI" value="API Mock&#xa;de Fornecedores" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontSize=13;fontStyle=1;fillColor=#E3F2FD;strokeColor=#1565C0;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="2500" y="1000" width="50" height="100" as="geometry"/>
        </mxCell>

        <!-- ===================== GENERALIZAÇÃO ===================== -->
        <mxCell id="gen1" value="" style="endArrow=empty;endSize=20;html=1;strokeColor=#616161;strokeWidth=2;dashed=1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;" edge="1" source="actorAuth" target="actorVisitor" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="gen1t" value="&lt;i&gt;generaliza&lt;/i&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=10;fontStyle=2;fontColor=#616161;" vertex="1" parent="1">
          <mxGeometry x="180" y="600" width="80" height="20" as="geometry"/>
        </mxCell>

        <!-- ===================== ÁREA 1 — AUTENTICAÇÃO ===================== -->
        <mxCell id="area1" value="🔐 AUTENTICAÇÃO (RF01–RF04)" style="swimlane;startSize=28;fillColor=#FFEBEE;strokeColor=#C62828;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#B71C1C;swimlaneLine=0;shadow=0;" vertex="1" parent="boundary">
          <mxGeometry x="40" y="50" width="900" height="280" as="geometry"/>
        </mxCell>

        <mxCell id="UC09" value="UC09&#xa;Cadastrar-se" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C62828;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area1">
          <mxGeometry x="40" y="60" width="170" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC10" value="UC10&#xa;Realizar Login" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C62828;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area1">
          <mxGeometry x="240" y="60" width="170" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC12" value="UC12&#xa;Recuperar Senha" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C62828;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area1">
          <mxGeometry x="440" y="60" width="170" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC11" value="UC11&#xa;Realizar Logout" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C62828;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area1">
          <mxGeometry x="640" y="60" width="170" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC18" value="UC18&#xa;Visualizar Perfil" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C62828;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area1">
          <mxGeometry x="240" y="170" width="170" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC16" value="UC16&#xa;Gerenciar Perfil" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C62828;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area1">
          <mxGeometry x="440" y="170" width="170" height="70" as="geometry"/>
        </mxCell>

        <!-- ===================== ÁREA 2 — GESTÃO DE LISTAS ===================== -->
        <mxCell id="area2" value="📝 GESTÃO DE LISTAS (RF07–RF11)" style="swimlane;startSize=28;fillColor=#E3F2FD;strokeColor=#1565C0;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#0D47A1;swimlaneLine=0;shadow=0;" vertex="1" parent="boundary">
          <mxGeometry x="40" y="360" width="900" height="380" as="geometry"/>
        </mxCell>

        <mxCell id="UC01" value="UC01&#xa;Criar Lista&#xa;em Memória" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="40" y="60" width="180" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="UC02" value="UC02&#xa;Buscar Produtos&#xa;(Autocomplete)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="250" y="60" width="180" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="UC13" value="UC13&#xa;Salvar Lista&#xa;(Persistir)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="460" y="60" width="180" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="UC17" value="UC17&#xa;Promover Lista&#xa;Efêmera" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="670" y="60" width="180" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="UC14" value="UC14&#xa;Listar Minhas&#xa;Listas" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="40" y="180" width="180" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="UC15" value="UC15&#xa;Editar/Excluir&#xa;Lista Salva" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="250" y="180" width="180" height="80" as="geometry"/>
        </mxCell>

        <!-- ===================== ÁREA 3 — COMPARAÇÃO ===================== -->
        <mxCell id="area3" value="🔄 COMPARAÇÃO DE FORNECEDORES (RF12–RF15)" style="swimlane;startSize=28;fillColor=#E8F5E9;strokeColor=#2E7D32;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#1B5E20;swimlaneLine=0;shadow=0;" vertex="1" parent="boundary">
          <mxGeometry x="980" y="50" width="880" height="400" as="geometry"/>
        </mxCell>

        <mxCell id="UC03" value="UC03&#xa;Selecionar&#xa;Fornecedores" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#2E7D32;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area3">
          <mxGeometry x="40" y="60" width="180" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="UC04" value="UC04&#xa;Filtrar por&#xa;Disponibilidade" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#2E7D32;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area3">
          <mxGeometry x="40" y="180" width="180" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="UC05" value="UC05&#xa;Calcular Orçamento&#xa;(Tabela Flat)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#2E7D32;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area3">
          <mxGeometry x="260" y="60" width="200" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="UC06" value="UC06&#xa;Visualizar Resultados&#xa;(Tabela Comparativa)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#2E7D32;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area3">
          <mxGeometry x="500" y="60" width="200" height="80" as="geometry"/>
        </mxCell>

        <!-- ===================== ÁREA 4 — EXPORTAÇÃO ===================== -->
        <mxCell id="area4" value="📤 EXPORTAÇÃO (RF16–RF17)" style="swimlane;startSize=28;fillColor=#F3E5F5;strokeColor=#6A1B9A;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#4A148C;swimlaneLine=0;shadow=0;" vertex="1" parent="boundary">
          <mxGeometry x="980" y="480" width="880" height="260" as="geometry"/>
        </mxCell>

        <mxCell id="UC07" value="UC07&#xa;Exportar Lista CSV" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6A1B9A;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area4">
          <mxGeometry x="100" y="80" width="200" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC08" value="UC08&#xa;Imprimir" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6A1B9A;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area4">
          <mxGeometry x="500" y="80" width="200" height="70" as="geometry"/>
        </mxCell>

        <!-- ===================== ÁREA 5 — CASOS INTERNOS ===================== -->
        <mxCell id="areaInternal" value="⚙️ CASOS INTERNOS / AUXILIARES DE DOMÍNIO" style="swimlane;startSize=28;fillColor=#F5F5F5;strokeColor=#616161;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#424242;swimlaneLine=0;shadow=0;dashed=1;dashPattern=8 4;" vertex="1" parent="boundary">
          <mxGeometry x="40" y="770" width="1820" height="300" as="geometry"/>
        </mxCell>

        <mxCell id="UC19" value="UC19&#xa;Validar Dados" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="40" y="60" width="160" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC20" value="UC20&#xa;Hash de Senha&#xa;(bcrypt)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="220" y="60" width="160" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC21" value="UC21&#xa;Gerar Sessão&#xa;(JWT)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="400" y="60" width="160" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC22" value="UC22&#xa;Fornecer Catálogo" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="580" y="60" width="160" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC23" value="UC23&#xa;Fornecer Fornecedores" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="760" y="60" width="160" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC24" value="UC24&#xa;Fornecer Preços" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="940" y="60" width="160" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC25" value="UC25&#xa;Rate Limiting" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="1120" y="60" width="160" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC26" value="UC26&#xa;Invalidar Sessão" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="1300" y="60" width="160" height="70" as="geometry"/>
        </mxCell>

        <!-- ===================== ASSOCIAÇÕES — VISITANTE ===================== -->
        <mxCell id="a1" style="endArrow=none;html=1;strokeColor=#C62828;strokeWidth=2;exitX=1;exitY=0.2;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorVisitor" target="UC09" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a2" style="endArrow=none;html=1;strokeColor=#C62828;strokeWidth=2;exitX=1;exitY=0.35;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorVisitor" target="UC10" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a3" style="endArrow=none;html=1;strokeColor=#C62828;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorVisitor" target="UC12" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a4" style="endArrow=none;html=1;strokeColor=#C62828;strokeWidth=2;exitX=1;exitY=0.65;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorVisitor" target="UC01" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a5" style="endArrow=none;html=1;strokeColor=#C62828;strokeWidth=2;exitX=1;exitY=0.8;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorVisitor" target="UC03" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a6" style="endArrow=none;html=1;strokeColor=#C62828;strokeWidth=2;exitX=1;exitY=0.95;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorVisitor" target="UC07" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== ASSOCIAÇÕES — USUÁRIO AUTENTICADO ===================== -->
        <mxCell id="a7" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=2;exitX=1;exitY=0.1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuth" target="UC11" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a8" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=2;exitX=1;exitY=0.2;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuth" target="UC18" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a9" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=2;exitX=1;exitY=0.3;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuth" target="UC16" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a10" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=2;exitX=1;exitY=0.4;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuth" target="UC13" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a11" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=2;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuth" target="UC17" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a12" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=2;exitX=1;exitY=0.6;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuth" target="UC14" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a13" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=2;exitX=1;exitY=0.7;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuth" target="UC15" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a14" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=2;exitX=1;exitY=0.8;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuth" target="UC05" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a15" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=2;exitX=1;exitY=0.9;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuth" target="UC08" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== ASSOCIAÇÕES — SISTEMA ===================== -->
        <mxCell id="b1" style="endArrow=none;html=1;strokeColor=#E65100;strokeWidth=2;exitX=0;exitY=0.2;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorSystem" target="UC19" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="b2" style="endArrow=none;html=1;strokeColor=#E65100;strokeWidth=2;exitX=0;exitY=0.35;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorSystem" target="UC20" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="b3" style="endArrow=none;html=1;strokeColor=#E65100;strokeWidth=2;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorSystem" target="UC21" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="b4" style="endArrow=none;html=1;strokeColor=#E65100;strokeWidth=2;exitX=0;exitY=0.65;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorSystem" target="UC25" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="b5" style="endArrow=none;html=1;strokeColor=#E65100;strokeWidth=2;exitX=0;exitY=0.8;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorSystem" target="UC26" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== ASSOCIAÇÕES — API MOCK ===================== -->
        <mxCell id="c1" style="endArrow=none;html=1;strokeColor=#1565C0;strokeWidth=2;exitX=0;exitY=0.3;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAPI" target="UC22" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="c2" style="endArrow=none;html=1;strokeColor=#1565C0;strokeWidth=2;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAPI" target="UC23" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="c3" style="endArrow=none;html=1;strokeColor=#1565C0;strokeWidth=2;exitX=0;exitY=0.7;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAPI" target="UC24" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== RELAÇÕES <<include>> ===================== -->
        <mxCell id="inc1" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC09" target="UC19" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc2" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.3;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC09" target="UC20" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc3" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC10" target="UC21" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc4" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.7;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC10" target="UC25" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc5" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC12" target="UC25" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc6" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC16" target="UC19" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc7" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.3;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC13" target="UC19" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc8" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#0D47A1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC02" target="UC22" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc9" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#0D47A1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.3;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC05" target="UC19" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc10" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#0D47A1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC05" target="UC23" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc11" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#0D47A1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.7;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC05" target="UC24" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc12" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#0D47A1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC03" target="UC23" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc13" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#0D47A1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC04" target="UC03" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="inc14" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC11" target="UC26" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== RELAÇÕES <<extend>> ===================== -->
        <mxCell id="ext1" value="&lt;&lt;extend&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#6A1B9A;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#4A148C;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="UC04" target="UC03" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="ext2" value="&lt;&lt;extend&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#6A1B9A;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#4A148C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.3;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC07" target="UC06" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="ext3" value="&lt;&lt;extend&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#6A1B9A;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#4A148C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.7;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC08" target="UC06" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="ext4" value="&lt;&lt;extend&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#6A1B9A;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#4A148C;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="UC16" target="UC18" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="ext5" value="&lt;&lt;extend&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#6A1B9A;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#4A148C;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="UC17" target="UC13" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== LEGENDA ===================== -->
        <mxCell id="legend" value="&lt;b&gt;LEGENDA — COBECO MVP v3.1&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1A237E;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontSize=12;shadow=1;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="150" y="1200" width="280" height="500" as="geometry"/>
        </mxCell>

        <mxCell id="leg1" value="" style="endArrow=none;html=1;strokeColor=#C62828;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="170" y="1250" as="sourcePoint"/>
            <mxPoint x="230" y="1250" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg1t" value="Visitante (Não Autenticado)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1235" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg2" value="" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="170" y="1285" as="sourcePoint"/>
            <mxPoint x="230" y="1285" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg2t" value="Usuário Autenticado" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1270" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg2b" value="" style="endArrow=empty;endSize=15;html=1;strokeColor=#616161;strokeWidth=2;dashed=1;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="170" y="1320" as="sourcePoint"/>
            <mxPoint x="230" y="1320" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg2bt" value="Generalização (herança)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1305" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg3" value="" style="endArrow=none;html=1;strokeColor=#E65100;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="170" y="1355" as="sourcePoint"/>
            <mxPoint x="230" y="1355" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg3t" value="Sistema (ator secundário)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1340" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg4" value="" style="endArrow=none;html=1;strokeColor=#1565C0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="170" y="1390" as="sourcePoint"/>
            <mxPoint x="230" y="1390" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg4t" value="API Mock (ator secundário)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1375" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg5" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=10;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=9;fontStyle=1;fontColor=#BF360C;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="170" y="1430" as="sourcePoint"/>
            <mxPoint x="230" y="1430" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg5t" value="Inclusão (obrigatória)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1415" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg6" value="&lt;&lt;extend&gt;&gt;" style="endArrow=open;endSize=10;dashed=1;html=1;strokeColor=#6A1B9A;strokeWidth=2;fontSize=9;fontStyle=1;fontColor=#4A148C;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="170" y="1465" as="sourcePoint"/>
            <mxPoint x="230" y="1465" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg6t" value="Extensão (opcional)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1450" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg7" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;dashed=1;dashPattern=4 3;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="180" y="1500" width="40" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="leg7t" value="Caso Interno (auxiliar)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1495" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg8" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFEBEE;strokeColor=#C62828;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="180" y="1535" width="40" height="20" as="geometry"/>
        </mxCell>
        <mxCell id="leg8t" value="Autenticação" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1530" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg9" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1565C0;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="180" y="1560" width="40" height="20" as="geometry"/>
        </mxCell>
        <mxCell id="leg9t" value="Gestão de Listas" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1555" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg10" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#2E7D32;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="180" y="1585" width="40" height="20" as="geometry"/>
        </mxCell>
        <mxCell id="leg10t" value="Comparação" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1580" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg11" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F3E5F5;strokeColor=#6A1B9A;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="180" y="1610" width="40" height="20" as="geometry"/>
        </mxCell>
        <mxCell id="leg11t" value="Exportação" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1605" width="180" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg12" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#616161;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="1">
          <mxGeometry x="180" y="1635" width="40" height="20" as="geometry"/>
        </mxCell>
        <mxCell id="leg12t" value="Casos Internos" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="240" y="1630" width="180" height="30" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 📊 PARTE 6 — MATRIZ DE RASTREABILIDADE FINAL

| RF | UC Principal | UCs Internos | Prioridade |
|----|-------------|-------------|------------|
| RF01 | UC09 | UC19, UC20 | P0 |
| RF02 | UC10 | UC21, UC25 | P0 |
| RF03 | UC11 | UC26 | P0 |
| RF04 | UC12 | UC25 | P1 |
| RF05 | UC18 | — | P1 |
| RF06 | UC16 | UC19 | P1 |
| RF07 | UC01, UC02 | UC22 | P0 |
| RF08 | UC13, UC17 | UC19 | P0 |
| RF09 | UC14 | — | P0 |
| RF10 | UC15 | UC19 | P1 |
| RF11 | UC15 | — | P1 |
| RF12 | UC03 | UC23 | P0 |
| RF13 | UC04 | UC03 | P1 |
| RF14 | UC05 | UC19, UC23, UC24 | P0 |
| RF15 | UC06 | — | P0 |
| RF16 | UC07 | — | P0 |
| RF17 | UC08 | — | P1 |

---

## ✅ CONCLUSÃO

O sistema COBECO MVP v3.1 está **completo e consistente**:

- ✅ **26 Casos de Uso** (18 principais + 8 internos)
- ✅ **4 Atores** com generalização UML correta
- ✅ **17 Requisitos Funcionais** cobertos
- ✅ **10 Requisitos Não Funcionais** atendidos
- ✅ **8 Requisitos Desejáveis** mapeados para backlog
- ✅ **14 relações `<<include>>`** (obrigatórias)
- ✅ **5 relações `<<extend>>`** (opcionais)
- ✅ **Nenhum caso solitário** — todos conectados
- ✅ **XML Draw.io** pronto para importação

**Próximo passo:** Aprovação deste documento e início da Sprint 1 (Setup + Auth).
