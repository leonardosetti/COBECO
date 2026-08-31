## 📘 MANUAL DO PROJETO - COBECO MVP

### **1. Objetivo do Projeto**

O **COBECO (Cotação de Bens de Consumo)** é uma aplicação web desktop-first que automatiza a comparação de preços entre múltiplos fornecedores a partir de listas de compras criadas pelo usuário. O sistema cruza os itens da lista com um catálogo previamente populado de fornecedores, produtos e preços, gerando orçamentos consolidados que destacam a opção mais econômica e evidenciam produtos ausentes em cada cenário.

**Objetivo Estratégico:** Entregar um MVP funcional e validado em 30 dias, focando na lógica de negócio core (comparação de preços) e na experiência do usuário, eliminando complexidades desnecessárias e dependências externas instáveis.

---

### **2. Contexto & Problema**

**O Problema:**
Usuários que precisam comprar múltiplos itens (supermercado, materiais, eletrônicos, etc.) enfrentam um processo manual, demorado e propenso a erros:

1. Listar produtos desejados
2. Consultar preços em múltiplos fornecedores
3. Comparar disponibilidade (nem todos têm todos os produtos)
4. Calcular qual combinação resulta em menor custo total
5. Identificar quais itens ficariam faltando em cada fornecedor

**A Solução:**
O COBECO automatiza esse processo:

- Usuário cria lista de itens com quantidades
- Sistema cruza com catálogo base de fornecedores (populado via seed)
- Exibe tabela comparativa com: fornecedor, itens disponíveis, itens ausentes, preço total
- Destaca a opção mais econômica
- Permite exportar resultado (CSV) ou imprimir

**Diferencial:**
Diferente de ferramentas complexas que dependem de web scraping ou APIs externas em tempo real, o COBECO adota uma abordagem pragmática: todos os dados são mockados via seed, permitindo focar 100% na lógica de negócio e na qualidade da arquitetura.

---

### **3. Público Alvo**

**Usuários Primários:**

- Consumidores que planejam compras de múltiplos itens
- Pequenos empresários que precisam cotar materiais
- Estudantes e profissionais que buscam otimizar gastos

**Características:**

- Usuários comuns (não técnicos)
- Preferência por interfaces desktop
- Necessidade de comparação rápida e clara
- Valorizam economia de tempo e dinheiro

**Exemplos de Uso:**

- Comparar preços de supermercados
- Comparar lojas de roupas ou eletrônicos
- Comparar fornecedores de materiais de construção
- Preparar lista impressa para conferência física durante a compra

---

### **4. Escopo do Projeto**

#### **4.1. Dentro do Escopo (In Scope)**

| Área                    | Descrição                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------- |
| **Autenticação**        | Cadastro, login, logout, recuperação de senha via email                               |
| **Gestão de Listas**    | CRUD completo (criar, editar, excluir, listar)                                        |
| **Persistência**        | PostgreSQL com ACID, histórico de listas                                              |
| **Seed de Dados**       | 10 fornecedores + 50 produtos com preços variáveis                                    |
| **Motor de Comparação** | Tabela flat simplificada (fornecedor, itens disponíveis, itens ausentes, preço total) |
| **Visualização**        | Destaque do menor orçamento, lista de produtos ausentes                               |
| **Exportação**          | CSV + impressão via navegador (CSS @media print)                                      |
| **API RESTful**         | OpenAPI (Swagger) documentado, SDD (API-First)                                        |
| **Testes**              | Unitários críticos + CI básico (GitHub Actions)                                       |
| **Infraestrutura**      | Docker Compose (Frontend, Backend, PostgreSQL)                                        |

#### **4.2. Fora do Escopo (Out of Scope)**

- ❌ Apps móveis (iOS/Android/PWA)
- ❌ Integração com APIs externas reais de e-commerce
- ❌ Web scraping em tempo real
- ❌ Processamento de pagamentos
- ❌ Roteirização logística (cálculo de distância/frete)
- ❌ Geração de PDF nativo
- ❌ Validação de email real no cadastro (apenas formato)
- ❌ BDD/E2E tests completos
- ❌ Suporte a múltiplos idiomas/moedas
- ❌ Autenticação via OAuth (Google/Facebook)

---

### **5. Premissas e Restrições Fundamentais**

#### **5.1. Premissas**

| Premissa                           | Justificativa                                      |
| ---------------------------------- | -------------------------------------------------- |
| Dados de fornecedores são mockados | Elimina dependência de APIs externas instáveis     |
| Catálogo é populado via seed       | Permite teste rápido da lógica de negócio          |
| Usuário precisa se autenticar      | Essencial para persistência de listas e histórico  |
| Interface é desktop-first          | Foco no público-alvo, sem complexidade mobile      |
| Motor de paridade é simplificado   | Tabela flat atende 80% do valor com 30% do esforço |

#### **5.2. Restrições**

| Restrição                   | Impacto                                  |
| --------------------------- | ---------------------------------------- |
| Prazo de entrega: 30 dias   | Escopo deve ser rigorosamente controlado |
| Equipe acadêmica (3-5 devs) | Capacidade limitada, foco em qualidade   |
| Stack FOSS apenas           | Sem custos de licenciamento              |
| PostgreSQL como banco       | Garantia de ACID e integridade           |
| Docker para containerização | Reprodutibilidade de ambiente            |

---

### **6. Regras de Negócio Essenciais**

#### **6.1. Autenticação**

- **Cadastro:** username (único, 3-30 chars), nome (2-100 chars), email (formato válido), senha (mín 8 chars, 1 maiúscula, 1 número, 1 especial)
- **Login:** email ou username + senha, rate limiting (5 tentativas/15min)
- **Recuperação de Senha:** Token de 15min, máximo 3 solicitações/hora
- **Sessão:** JWT (1h) + refresh token (7 dias, httpOnly cookie)

#### **6.2. Gestão de Listas**

- **Criação:** Nome obrigatório (1-100 chars), mínimo 1 item
- **Itens:** Produto (FK para catálogo), quantidade (1-9999)
- **Edição:** Validação de quantidade, confirmação antes de remover
- **Exclusão:** Confirmação obrigatória (digitar nome da lista), soft delete
- **Busca:** Autocomplete com debounce de 300ms, mínimo 2 caracteres

#### **6.3. Comparação de Fornecedores**

- **Cálculo:** Para cada fornecedor, calcular:
  - Itens disponíveis (presentes no catálogo do fornecedor)
  - Itens ausentes (não disponíveis)
  - Preço total (soma de quantidade × preço para itens disponíveis)
- **Ordenação:** Por preço total (menor para maior)
- **Destaque:** Linha com menor preço em verde
- **Timeout:** 10s para cálculo, cache de 5min

#### **6.4. Exportação**

- **CSV:** Encoding UTF-8 com BOM, delimitador ponto e vírgula (;)
- **Impressão:** CSS @media print oculta menus, formatação A4

---

### **7. Requisitos de UI/UX e Usabilidade**

#### **7.1. Princípios de Design**

- **Desktop-First:** Layout exclusivo para telas ≥1024px
- **KISS (Keep It Simple):** Interface minimalista, foco na tarefa
- **Feedback Visual:** Toasts (sucesso/erro/info), skeletons para loading >300ms
- **Validação em Tempo Real:** Campos validados no onBlur, mensagens claras

#### **7.2. Acessibilidade**

- Contraste de cores adequado (WCAG AA)
- Navegação por teclado (Tab, Enter, Esc)
- Tags semânticas HTML
- Rótulos claros em formulários

#### **7.3. Fluxos Críticos**

1. **Cadastro → Login → Dashboard** (<2 minutos)
2. **Criar Lista → Adicionar Itens → Salvar** (<3 minutos)
3. **Comparar Fornecedores → Visualizar Resultados → Exportar** (<1 minuto)

---

### **8. Arquitetura Definida**

#### **8.1. Clean Architecture (Backend)**

```
┌─────────────────────────────────────────┐
│         Frameworks & Drivers            │
│  (NestJS, Prisma, PostgreSQL, Docker)   │
├─────────────────────────────────────────┤
│            Adapters (Interface)         │
│  (Controllers, DTOs, Repositories)      │
├─────────────────────────────────────────┤
│            Use Cases (Application)      │
│  (Auth, ListManagement, Comparison)     │
├─────────────────────────────────────────┤
│              Domain (Enterprise)        │
│  (Entities, Value Objects, Rules)       │
└─────────────────────────────────────────┘
```

**Princípios:**

- Dependência apenas inwards (de fora para dentro)
- Injeção de dependência obrigatória
- Sem lógica de negócio em controllers
- Casos de uso isolados e testáveis

#### **8.2. Infraestrutura (Docker Compose)**

```yaml
services:
  frontend: # React + Vite + TypeScript
    port: 8080
  backend: # NestJS + Prisma
    port: 3000
  postgres: # PostgreSQL 16
    port: 5432
```

#### **8.3. Comunicação**

- **API RESTful:** OpenAPI 3.0 documentado em `/api/docs`
- **SDD (Specification-Driven Development):** Contratos definidos antes da implementação
- **Tipagem:** TypeScript gera tipos automaticamente a partir do OpenAPI

---

### **9. Tech Stack**

#### **9.1. Frontend**

| Tecnologia      | Versão | Justificativa                            |
| --------------- | ------ | ---------------------------------------- |
| React           | 18.x   | Padrão de mercado, ecossistema maduro    |
| TypeScript      | 5.x    | Segurança de tipos, SDD                  |
| Vite            | 5.x    | Build ultra-rápido (<1s)                 |
| Tailwind CSS    | 3.x    | Utility-first, design system consistente |
| shadcn/ui       | Latest | Componentes acessíveis, customizáveis    |
| TanStack Query  | 5.x    | Cache, loading states, retry automático  |
| React Hook Form | 7.x    | Performance, validação integrada         |
| Zod             | 3.x    | Validação de schemas                     |

#### **9.2. Backend**

| Tecnologia  | Versão     | Justificativa                                     |
| ----------- | ---------- | ------------------------------------------------- |
| Node.js     | 20.x (LTS) | Performance, async/await                          |
| NestJS      | 10.x       | Clean Architecture por padrão, OpenAPI automático |
| TypeScript  | 5.x        | Tipagem forte                                     |
| Prisma ORM  | 5.x        | Type-safe queries, migrations                     |
| PostgreSQL  | 16.x       | ACID, JSON support, FOSS                          |
| Passport.js | 0.7.x      | Autenticação flexível                             |
| bcrypt      | 5.x        | Hashing de senhas                                 |

#### **9.3. Infraestrutura**

| Tecnologia     | Versão    | Justificativa                     |
| -------------- | --------- | --------------------------------- |
| Docker         | 24.x      | Containers para dev/prod          |
| Docker Compose | 2.x       | Orquestração local                |
| GitHub Actions | Latest    | CI/CD gratuito                    |
| Resend         | Free tier | Envio de emails (3000/mês grátis) |
| Mailhog        | Latest    | SMTP local para desenvolvimento   |

---

### **10. Qualidade do Projeto**

#### **10.1. Testes**

- **Unitários:** Cobertura mínima de 80% nos casos de uso críticos
  - Autenticação (cadastro, login, recuperação)
  - Cálculo de orçamento (lógica de comparação)
  - Validações de negócio (campos obrigatórios, FKs)
- **Ferramentas:** Jest (backend), Vitest (frontend)
- **CI/CD:** GitHub Actions roda testes em cada push/PR

#### **10.2. Métricas de Qualidade**

| Métrica                 | Meta   |
| ----------------------- | ------ |
| Cobertura de testes     | >80%   |
| Tempo de pipeline CI    | <5min  |
| API response time (p95) | <500ms |
| Frontend FCP            | <1.5s  |
| Bundle size (gzipped)   | <500KB |
| Lighthouse score        | >90    |

#### **10.3. Code Review**

- Pull requests obrigatórios
- Aprovação de pelo menos 1 revisor
- Checklist de Clean Architecture
- Validação de testes passando

---

### **11. Riscos**

| Risco                              | Probabilidade | Impacto | Mitigação                                            |
| ---------------------------------- | ------------- | ------- | ---------------------------------------------------- |
| Atraso no desenvolvimento          | Média         | Alto    | Escopo rigorosamente controlado, sprints de 1 semana |
| Bugs críticos em produção          | Baixa         | Alto    | Testes unitários, code review, staging antes de prod |
| Dependência externa (Resend)       | Baixa         | Médio   | Fallback para Mailhog em dev, monitoramento em prod  |
| Performance do motor de comparação | Baixa         | Médio   | Cache de 5min, timeout de 10s, índice no banco       |
| Segurança (vazamento de dados)     | Baixa         | Crítico | HTTPS, bcrypt, httpOnly cookies, rate limiting       |

---

### **12. Definição de DONE para Atividades**

Uma atividade é considerada **DONE** quando:

- ✅ Código implementado e seguindo Clean Architecture
- ✅ Testes unitários escritos e passando (>80% cobertura)
- ✅ Code review aprovado por pelo menos 1 revisor
- ✅ Documentação atualizada (OpenAPI, README, comentários)
- ✅ CI/CD passando (lint, test, build)
- ✅ Deploy em staging validado
- ✅ Feedback do Product Owner/Stakeholder

---

### **13. Previsão de Entregáveis do MVP**

| Fase                      | Duração     | Entregáveis                                        |
| ------------------------- | ----------- | -------------------------------------------------- |
| **Fase 1: Setup**         | 3 dias      | Repositórios, Docker Compose, CI/CD, seed de dados |
| **Fase 2: Backend Core**  | 10 dias     | Auth, CRUD de listas, motor de comparação, OpenAPI |
| **Fase 3: Frontend Core** | 10 dias     | Telas de auth, dashboard, comparação, exportação   |
| **Fase 4: Testes**        | 5 dias      | Testes unitários, ajustes de UI/UX, performance    |
| **Fase 5: Deploy**        | 2 dias      | Staging, validação com stakeholders, documentação  |
| **TOTAL**                 | **30 dias** | **MVP funcional e validado**                       |

---

### **14. Desejáveis Pós-Release**

| Código | Funcionalidade                                                | Prioridade |
| ------ | ------------------------------------------------------------- | ---------- |
| RD01   | Integração com LLMs para importação de listas por texto livre | Alta       |
| RD02   | Web scraping de preços em tempo real                          | Alta       |
| RD03   | App mobile (React Native)                                     | Média      |
| RD04   | Roteirização logística (distância até fornecedores)           | Média      |
| RD05   | Processamento de pagamentos                                   | Baixa      |
| RD06   | Geração de PDF nativo                                         | Baixa      |
| RD07   | Autenticação via OAuth (Google/Facebook)                      | Baixa      |
| RD08   | Suporte a múltiplos idiomas (i18n)                            | Baixa      |
| RD09   | Tema claro/escuro (Dark Mode)                                 | Baixa      |

---

### **15. Resumo Executivo**

O **COBECO** é um MVP de aplicação web desktop-first que automatiza a comparação de preços entre múltiplos fornecedores a partir de listas de compras criadas pelo usuário. Desenvolvido em 30 dias com stack FOSS (React, NestJS, PostgreSQL), o sistema foca na lógica de negócio core (comparação de preços) e na experiência do usuário, eliminando complexidades desnecessárias.

**Entregáveis Principais:**

- ✅ Autenticação completa (cadastro, login, recuperação de senha)
- ✅ CRUD de listas de compras com persistência em PostgreSQL
- ✅ Motor de comparação simplificado (tabela flat)
- ✅ Exportação CSV + impressão via navegador
- ✅ Testes unitários críticos + CI/CD básico

**Critérios de Sucesso:**

- Fluxo completo (cadastro → comparação) em <5 minutos
- Tempo de resposta <500ms em 95% das requisições
- Cobertura de testes >80%, zero bugs críticos
- Feedback positivo dos stakeholders na demo final

---

### **16. Considerações Finais**

O **COBECO MVP** representa uma solução pragmática e focada para um problema real: a comparação manual de preços entre múltiplos fornecedores. Ao adotar uma abordagem **KISS** (Keep It Simple, Stupid) e eliminar complexidades desnecessárias (web scraping, PDFs, BDD/E2E completos), o projeto consegue entregar valor real em 30 dias.

**Princípios Adotados:**

- **Clean Architecture:** Separação clara de responsabilidades
- **ACID:** Integridade de dados garantida
- **SDD:** Desenvolvimento orientado por contratos OpenAPI
- **FOSS:** Tecnologias gratuitas e de código aberto
- **Usabilidade:** Interface desktop-first, feedback visual claro

### **17. Glossário**

| Termo                  | Definição                                                                     |
| ---------------------- | ----------------------------------------------------------------------------- |
| **MVP**                | Minimum Viable Product (Produto Viável Mínimo)                                |
| **SDD**                | Specification-Driven Development (Desenvolvimento Orientado a Especificação)  |
| **ACID**               | Atomicity, Consistency, Isolation, Durability (propriedades de transações DB) |
| **KISS**               | Keep It Simple, Stupid (princípio de simplicidade)                            |
| **FOSS**               | Free and Open Source Software (Software Livre e de Código Aberto)             |
| **Clean Architecture** | Padrão de arquitetura que separa domínio, casos de uso, adapters e frameworks |
| **OpenAPI**            | Especificação para documentação de APIs RESTful (anteriormente Swagger)       |
| **CI/CD**              | Continuous Integration / Continuous Deployment (Integração/Deploy Contínuo)   |
| **Seed**               | Script que popula o banco de dados com dados iniciais (mockados)              |
| **Soft Delete**        | Marcar registro como inativo em vez de deletar permanentemente                |

---

**Próximos Passos:**

1. Aprovação deste manual por stakeholders
2. Geração de artefatos UML (Casos de Uso, Transição de Estados, DER)
3. Protótipo de baixa fidelidade (Figma/Excalidraw)
4. Setup inicial dos repositórios e infraestrutura

---

**Última atualização:** 31 de Agosto de 2026
