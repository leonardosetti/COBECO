# 📋 LEVANTAMENTO OFICIAL DE REQUISITOS — COBECO MVP v3.2

**Documento:** Requisitos Fechados do Projeto  
**Versão:** 3.2 (SSOT Final)  
**Data:** 14 de Setembro de 2026  
**Status:** ✅ APROVADO — Composição Oficial  
**Base:** DOC-02 do Pacote Documental Consolidado

---

## 🔐 REQUISITOS FUNCIONAIS (RF)

### Grupo A — Autenticação e Perfil (RF01–RF06)

| ID | Requisito | Descrição | Guard-Rails | Prioridade |
|----|-----------|-----------|-------------|------------|
| **RF01** | Cadastrar Usuário | Criar conta com nome_usuario (único), email, senha + confirmação, pergunta de segurança | Nome_usuario: 3-30 chars alfanumérico. Senha: mín 8, 1 maiúsc, 1 número, 1 especial. Email: formato válido. Pergunta obrigatória. | **P0** |
| **RF02** | Login | Autenticar via nome_usuario + senha | 6 tentativas consecutivas → lockout 15min (anti-DDoS). Mensagem genérica. JWT: access 15min memória + refresh 7d httpOnly. | **P0** |
| **RF03** | Logout | Encerrar sessão ativa | Invalida cookie. Limpa access da memória. Redirect para home. | **P0** |
| **RF04** | Recuperar Senha | Reset via pergunta de segurança (sem email) | Pergunta do cadastro. 3 tentativas. Nova senha segue RF01. Modo alternativo: token no stdout (RECOVERY_MODE=log). | **P1** |
| **RF05** | Visualizar Perfil | Ver dados pessoais (nome_usuario, email, nome) | Apenas autenticado. Nome_usuario read-only. | **P1** |
| **RF06** | Editar Perfil | Alterar email, nome e senha | Senha antiga obrigatória. Email único. | **P1** |

### Grupo B — Gestão de Listas (RF07–RF11)

| ID | Requisito | Descrição | Guard-Rails | Prioridade |
|----|-----------|-----------|-------------|------------|
| **RF07** | Criar Lista (em memória) | Qualquer usuário cria lista com nome + itens (produto + quantidade) | Mínimo 1 item. Quantidade: 1-9999. Produto deve existir no catálogo (autocomplete). Lista em memória JS até salvar. | **P0** |
| **RF08** | Salvar Lista (persistir) | Persistir lista no banco MySQL | Requer autenticação. Se não logado → modal. Validação de FK. Validação de categorias selecionadas (UC03). ACID: transação lista + itens. | **P0** |
| **RF09** | Listar Minhas Listas | Exibir listas salvas do usuário | Paginação 20/página. Ordenação: data DESC. Soft delete (excluídas não aparecem). | **P0** |
| **RF10** | Editar Lista Salva | Alterar nome, itens, quantidades | Validação de propriedade (usuario_id). Confirmação antes de remover. | **P1** |
| **RF11** | Excluir Lista Salva | Remover lista (soft delete) | Confirmação obrigatória. Campo `deletado_em`. | **P1** |

### Grupo C — Pré-filtro e Comparação (RF12–RF16) ⭐ REFINADO v3.2

| ID | Requisito | Descrição | Guard-Rails | Prioridade |
|----|-----------|-----------|-------------|------------|
| **RF12** ⭐ | Selecionar Categorias (Pré-filtro) | Escolher uma ou mais categorias para filtrar fornecedores | Mínimo 1 categoria. Checkboxes. Fornecedores filtrados dinamicamente. Seleção em memória. | **P0** |
| **RF13** | Selecionar Fornecedores | Escolher quais fornecedores comparar (mínimo 2) | Checkboxes com nome + % disponibilidade. Apenas fornecedores das categorias selecionadas (RF12). Seleção em memória. | **P0** |
| **RF14** | Filtrar por Disponibilidade | Slider 0-100% para filtrar fornecedores | Padrão: 0% (todos). Atualiza em tempo real. Mantém seleção válida. | **P1** |
| **RF15** | Calcular Orçamento | Gerar tabela flat comparativa | Timeout 10s. Cache 5min. Calcular: disponíveis, ausentes, preço total. Ordenar por preço ASC. | **P0** |
| **RF16** | Visualizar Resultados | Tabela com destaque de melhor oferta | Destacar menor preço (verde). Mostrar % disponibilidade. Tooltip de ausentes. | **P0** |

### Grupo D — Exportação (RF17–RF18) ⭐ REFINADO v3.2

| ID | Requisito | Descrição | Guard-Rails | Prioridade |
|----|-----------|-----------|-------------|------------|
| **RF17** ⭐ | Exportar Lista PDF | Download de lista em PDF | Funciona para TODOS usuários (sem login). Geração server-side (Python + ReportLab). Nome: `lista_YYYYMMDD.pdf`. Formato A4. | **P0** |
| **RF18** | Imprimir | View otimizada para Ctrl+P | CSS `@media print`. Oculta menus. Formatação A4. | **P1** |

---

## ⚙️ REQUISITOS NÃO FUNCIONAIS (RNF)

| ID | Requisito | Descrição | Métrica |
|----|-----------|-----------|---------|
| **RNF01** | Clean Architecture | Camadas: Domain → UseCase → Adapter → Framework | Code review |
| **RNF02** | SDD (OpenAPI First) | Contrato OpenAPI 3.0 antes de implementar | Swagger em `/docs` |
| **RNF03** | ACID (MySQL InnoDB) | Transações explícitas, engine InnoDB | Zero dados órfãos |
| **RNF04** | Desktop-Only | Layout exclusivo ≥1024px. Sem mobile. | Breakpoint único |
| **RNF05** | Feedback Visual | Toasts, loading states, modais | <100ms feedback |
| **RNF06** | Testes Unitários | Cobertura ≥80% das regras de negócio | pytest --cov |
| **RNF07** | CI/CD (Docker) | Docker Compose (app + MySQL). GitHub Actions. | Pipeline <5min |
| **RNF08** | Seed de Dados | 10 fornecedores + 50 produtos + 11 categorias | `make seed` <10s |
| **RNF09** | Performance | API <500ms p95 | curl + time |
| **RNF10** | Segurança | Rate limiting 6 req/15min. Hash bcrypt. JWT access em memória. | Zero brute-force |
| **RNF11** ⭐ | Geração de PDF | PDF gerado em <5s para listas até 100 itens | ReportLab |
| **RNF12** ⭐ | MySQL InnoDB | Engine InnoDB, charset utf8mb4, collation utf8mb4_unicode_ci | ACID garantido |

---

## 📦 REQUISITOS DESEJÁVEIS (Backlog Pós-MVP)

| ID | Requisito | Descrição | Prioridade |
|----|-----------|-----------|------------|
| **RD01** | Histórico de Comparações | Persistir resultados anteriores | P3 |
| **RD02** | Importação de Lista via CSV | Upload de CSV para criar lista | P3 |
| **RD03** | Notificações de Preço | Alertar quando preço cair | P3 |
| **RD04** | Compartilhamento de Lista | Link público | P3 |
| **RD05** | App Mobile (PWA) | Versão responsiva | P3 |
| **RD06** | Integração com Fornecedores Reais | Web scraping em tempo real | P4 |
| **RD07** | Recomendações por IA | Sugerir fornecedores baseado em histórico | P4 |
| **RD08** | Multi-idioma | Inglês e espanhol | P4 |
| **RD09** ⭐ | Export CSV (opcional) | Manter opção CSV além de PDF | P3 |

---

## 📊 RESUMO QUANTITATIVO

| Categoria | Quantidade | Detalhamento |
|-----------|------------|--------------|
| **Requisitos Funcionais** | **18** | 11 P0 + 7 P1 |
| **Requisitos Não Funcionais** | **12** | Todos obrigatórios |
| **Requisitos Desejáveis** | **9** | Backlog pós-MVP (P3/P4) |
| **Total** | **39** | — |

---

**FIM DO LEVANTAMENTO OFICIAL DE REQUISITOS — COBECO MVP v3.2**