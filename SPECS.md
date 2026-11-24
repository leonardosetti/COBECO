# SPECS — COBECO MVP v3.3 (SSOT Consolidado)

**Projeto:** COBECO — Comparador de Bens de Consumo  
**Versão:** 3.3 (SSOT único — consolida SPECS v3.2 + req-func-0001 + req-use-case-0001)  
**Data:** 2026-11-17  
**Status:** Em validação  
**Base:** Protótipos Alta Fidelidade (doc-prototype-0001/0002/0003/0004) + Requisitos + Casos de Uso + DER  
**Canon:** Substitui SPECS.md v3.2, req-func-0001-requisitos-funcionais-canon.md v3.2, req-use-case-0001-casos-de-uso-canon.md v3.2

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

| Elemento | Especificação |
|----------|---------------|
| **Título** | "Selecione as categorias" — Passo 1 de 5 |
| **Categorias (11 macro)** | Mercado, Vestuário, Automotivos, Informática, Decoração, Móveis, Materiais de Construção e Ferragens, Ferramentas, Livros, Jardinagem, Eletrodomésticos |
| **Interação** | Checkboxes (múltipla escolha). Mínimo 1 categoria. "Selecionar todas" / "Limpar". |
| **Feedback visual** | Chip contador: "N categoria(s) selecionada(s) · 11 disponíveis". Verde quando ≥1. |
| **Estado** | Em memória (transitória). Perdida ao recarregar (toast informativo). |
| **Ação primária** | "Continuar para a lista →" — habilitado apenas se ≥1 categoria. |
| **Regra de negócio** | Fornecedores da próxima etapa = união dos fornecedores das categorias marcadas. Fornecedor pode pertencer a múltiplas categorias (aparece uma vez com badges). |
| **Exceções** | E1: Nenhuma categoria → botão desabilitado + toast. E2: Categoria sem fornecedores → toast + sugestão. |

---

## 3. REQUISITOS FUNCIONAIS (18 RFs)

| ID | Requisito | Descrição | Guard-Rails | Prioridade |
|----|-----------|-----------|-------------|------------|
| RF01 | Cadastrar Usuário | nome_usuario (único), email, senha + confirmação, pergunta de segurança | Nome 3-30 alfanumérico. Senha ≥8, 1 maiúscula, 1 número, 1 especial. Email válido. Pergunta obrigatória. | P0 |
| RF02 | Login | Autenticar nome_usuario + senha | 6 tentativas → lockout 15min. Mensagem genérica. JWT: access 15min mem + refresh 7d httpOnly. | P0 |
| RF03 | Logout | Encerrar sessão ativa | Invalida cookie. Limpa access da memória. Redirect home. | P0 |
| RF04 | Recuperar Senha | Reset via pergunta de segurança | Pergunta do cadastro. 3 tentativas. Nova senha segue RF01. RECOVERY_MODE=log dev. | P1 |
| RF05 | Visualizar Perfil | Ver nome_usuario, email, nome | Apenas autenticado. Nome_usuario read-only. | P1 |
| RF06 | Editar Perfil | Alterar email, nome, senha | Senha antiga obrigatória. Email único. Transação ACID. | P1 |
| RF07 | Criar Lista (memória) | Nome + itens (produto + quantidade) | Mínimo 1 item. Qtd 1-9999. Produto existe no catálogo (autocomplete). | P0 |
| RF08 | Salvar Lista (persistir) | Persistir no MySQL | Requer auth. Valida categorias (UC03). FK de produto. ACID lista+itens. | P0 |
| RF09 | Listar Minhas Listas | Exibir listas salvas | Paginação 20/página. Ordenação data DESC. Soft delete (deletado_em). | P0 |
| RF10 | Editar Lista Salva | Alterar nome, itens, quantidades | Valida propriedade (usuario_id). | P1 |
| RF11 | Excluir Lista Salva | Soft delete | Confirmação digitando nome. Campo deletado_em. | P1 |
| RF12 ⭐ | Selecionar Categorias | Pré-filtro de fornecedores | Mínimo 1 categoria. Checkboxes. Fornecedores filtrados dinamicamente. | P0 |
| RF13 | Selecionar Fornecedores | Escolher 2 ou mais fornecedores (sem limite superior) | Checkboxes + % disponibilidade. Apenas das categorias (RF12). | P0 |
| RF14 | Filtrar Disponibilidade | Slider 0-100% | Padrão 0%. Atualiza tempo real. Mantém seleção válida. | P1 |
| RF15 | Calcular Orçamento | Tabela flat comparativa | Timeout 10s. Cache 5min. Disponíveis, ausentes, preço total. Ordena preço ASC. | P0 |
| RF16 ⭐ | Visualizar Resultados | Melhor oferta destacada | **Maior % cobertura; empate → menor custo total.** % disponibilidade. Tooltip ausentes. | P0 |
| RF17 ⭐ | Exportar Lista PDF | Download PDF | Todos usuários (sem login). Server-side ReportLab. Nome lista_YYYYMMDD.pdf. A4. Apenas lista vencedora precificada — nunca tabela comparativa. | P0 |
| RF18 | Imprimir | View Ctrl+P | CSS @media print. Oculta menus. A4. | P1 |

---

## 4. REQUISITOS NÃO FUNCIONAIS (12 RNFs)

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

## 5. CASOS DE USO (29 UCs)

### Principais (19)

| ID | Caso de Uso | Ator | RF | Área | Prioridade |
|----|-------------|------|----|------|-----------|
| UC09 | Cadastrar-se | Visitante | RF01 | Auth | P0 |
| UC10 | Realizar Login | Visitante | RF02 | Auth | P0 |
| UC11 | Realizar Logout | Usuário Autenticado | RF03 | Auth | P0 |
| UC12 | Recuperar Senha | Visitante | RF04 | Auth | P1 |
| UC18 | Visualizar Perfil | Usuário Autenticado | RF05 | Auth | P1 |
| UC16 | Gerenciar Perfil | Usuário Autenticado | RF06 | Auth | P1 |
| UC03 ⭐ | Selecionar Categorias (Pré-filtro) | Visitante | RF12 | Pré-filtro | P0 |
| UC01 | Criar Lista em Memória | Visitante | RF07 | Listas | P0 |
| UC02 | Buscar Produtos (Autocomplete) | Visitante | RF07 | Listas | P0 |
| UC14 | Salvar Lista (Persistir) | Usuário Autenticado | RF08 | Listas | P0 |
| UC17 | Promover Lista Efêmera | Usuário Autenticado | RF08 | Listas | P0 |
| UC15 | Listar Minhas Listas | Usuário Autenticado | RF09 | Listas | P0 |
| UC13 | Editar/Excluir Lista Salva | Usuário Autenticado | RF10,RF11 | Listas | P1 |
| UC04 | Selecionar Fornecedores | Visitante | RF13 | Comparação | P0 |
| UC05 | Filtrar por Disponibilidade | Visitante | RF14 | Comparação | P1 |
| UC06 | Calcular Orçamento (Tabela Flat) | Visitante | RF15 | Comparação | P0 |
| UC07 | Visualizar Resultados | Visitante | RF16 | Comparação | P0 |
| UC08 ⭐ | Exportar Lista PDF | Visitante | RF17 | Exportação | P0 |
| UC09 | Imprimir | Visitante | RF18 | Exportação | P1 |

### Internos (10)

| ID | Caso de Uso | Invocado Por | Comportamento |
|----|-------------|--------------|---------------|
| UC20 | Validar Dados | UC09, UC14, UC16 | Valida schemas Pydantic em todas requisições |
| UC21 | Hash de Senha (bcrypt) | UC09 | Salt=12 no cadastro e alteração |
| UC22 | Gerar Sessão (JWT) | UC10 | Access (15min) + refresh (7d httpOnly) |
| UC23 | Fornecer Catálogo | UC02 | Retorna 50 produtos do seed |
| UC24 ⭐ | Fornecer Categorias | UC03 | Retorna 11 categorias macro |
| UC25 ⭐ | Fornecer Fornecedores (filtrado) | UC04, UC06 | Retorna fornecedores filtrados por categorias |
| UC26 | Fornecer Preços | UC06 | Retorna ~300 preços do seed |
| UC27 | Rate Limiting | UC10, UC12 | 6 tentativas/15min por IP + username |
| UC28 | Invalidar Sessão | UC11 | Logout + rotação de refresh tokens |
| UC29 ⭐ | Gerar PDF (ReportLab) | UC08 | Gera PDF A4 server-side |

---

## 6. REGRAS DE NEGÓCIO CRÍTICAS

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

## 7. MODELO DE DADOS (DER)

### 7.1 Tabelas

| Tabela | Colunas Principais | Relacionamentos |
|--------|-------------------|-----------------|
| **usuarios** | id (int PK), nome_usuario (varchar(30) UNIQUE), email (varchar(255) UNIQUE), nome (varchar(100)), senha_hash (text), pergunta_seguranca, resposta_seguranca_hash, criado_em, atualizado_em, deletado_em | 1:N → listas |
| **listas** | id (int PK), usuario_id (int FK→usuarios), nome (varchar(100)), categorias (varchar(200) NULL, JSON texto IDs), criado_em, atualizado_em, deletado_em | N:1 ← usuarios, 1:N → itens_lista |
| **itens_lista** | id (int PK), lista_id (int FK→listas), produto_id (int FK→produtos), quantidade (int 1-9999), criado_em | N:1 ← listas, N:1 ← produtos |
| **produtos** | id (int PK), nome (varchar(200)), unidade (varchar(10)), ativo (bool), criado_em | 1:N → itens_lista, 1:N → fornecedores_produtos |
| **fornecedores** | id (int PK), nome (varchar(150)), cnpj (varchar(18) UNIQUE), ativo (bool), criado_em | 1:N → fornecedores_produtos |
| **fornecedores_categorias** | fornecedor_id (int PK FK), categoria_id (int PK FK) | N:N entre fornecedores e categorias |
| **categorias** | id (int PK), nome (varchar(100)), descricao | 1:N → fornecedores_categorias |
| **fornecedores_produtos** | fornecedor_id (int PK FK), produto_id (int PK FK), preco (decimal(10,2) > 0), estoque (int ≥ 0), ativo (bool) | N:1 ← fornecedores, N:1 ← produtos |
| **sessoes** | id (int PK), usuario_id (int FK→usuarios), refresh_token_hash (varchar(255) UNIQUE), user_agent, ip, criado_em, expira_em, revogada_em | N:1 ← usuarios |

### 7.2 Seed Determinístico

- **11 Categorias** macro (fixas)
- **10 Fornecedores** reais (Carrefour, Extra, Pão de Açúcar, Magazine Luiza, Casas Bahia, Leroy Merlin, Etna, C&A, Renner, Hering)
- **50 Produtos** (mix: mercado, ferramentas, informática, vestuário, decoração, jardinagem, eletrodomésticos)
- **~300 Preços** (mapping fornecedor→produto com preço e estoque)
- **25 Relações N:N** fornecedor↔categoria

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

## 9. FLUXOS DE EXCEÇÃO / EDGE CASES MAIS IMPORTANTES

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

## 10. DEFINITION OF DONE

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
**FIM DO DOCUMENTO SPECS — COBECO MVP v3.3 (SSOT)**

