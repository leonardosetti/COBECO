# 🛒 COBECO - Cotação de Bens de Consumo (MVP)

**Sistema de Comparação de Preços para Listas de Compras**  
_Projeto acadêmico da disciplina de Laboratório de Engenharia de Software_  
_FATEC Taquaritinga - Análise e Desenvolvimento de Sistemas_

---

## 📖 Sobre o Projeto

### O Problema

Comparar preços manualmente entre múltiplos fornecedores é uma tarefa demorada, repetitiva e propensa a erros. Para piorar, nem sempre um único fornecedor possui todos os produtos desejados, forçando o consumidor a fracionar suas compras e perder tempo recalculando totais.

### A Solução

O **COBECO** é um MVP (Produto Mínimo Viável) que automatiza esse processo. Trata-se de uma aplicação web desktop-first que permite ao usuário:

1. **Criar listas de compras** personalizadas com itens, quantidades e categorias
2. **Submeter essas listas** a um motor de comparação que cruza os dados com um catálogo interno de fornecedores (populado via seed)
3. **Visualizar orçamentos consolidados** em uma tabela comparativa clara e objetiva
4. **Identificar lacunas** — o sistema destaca quais produtos estão faltando em cada fornecedor
5. **Tomar a melhor decisão** com base no menor custo consolidado

### Por que esse MVP é único?

Diferente de ferramentas complexas que dependem de web scraping ou APIs externas em tempo real, o COBECO adota uma abordagem **pragmática e realista**:

- ✅ **Dados mockados via seed** — foco 100% na lógica de negócio
- ✅ **Motor de comparação simplificado** — tabela flat ao invés de agrupamentos complexos
- ✅ **Stack moderna e FOSS** — React, NestJS, PostgreSQL, Docker
- ✅ **Clean Architecture** — separação clara de responsabilidades
- ✅ **SDD (Specification-Driven Development)** — API-first com OpenAPI

---

## 🎯 Objetivos do Projeto

### Objetivo Geral

Desenvolver um MVP funcional e minimalista que automatize a comparação de preços entre fornecedores a partir de listas de compras criadas pelo usuário, fornecendo orçamentos claros e evidenciando produtos ausentes em cada cenário.

### Objetivos Específicos (Entregáveis do MVP)

- ✅ Implementar autenticação segura (cadastro, login, recuperação de senha)
- ✅ Permitir CRUD completo de listas de compras (criar, editar, excluir, listar)
- ✅ Manter um cadastro interno de fornecedores, categorias e produtos (via seed)
- ✅ Desenvolver o motor de comparação que gera tabela flat com disponibilidade e preços
- ✅ Exibir comparativos destacando o melhor orçamento e os produtos faltantes
- ✅ Garantir a persistência dos dados em banco relacional (PostgreSQL)
- ✅ Estabelecer comunicação robusta entre Frontend e Backend via API RESTful (OpenAPI)

---

## ⚙️ Premissas e Restrições Fundamentais

| Pilar                        | Aplicação no Projeto                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| 🧼 **KISS (Keep It Simple)** | Escopo enxuto: dados mockados (sem APIs externas), UI exclusiva para desktop, lógica de negócio direta |
| 🏛️ **Clean Architecture**    | Separação rígida entre Domínio, Casos de Uso, Adaptadores e Frameworks                                 |
| ⚡ **ACID**                  | Operações no banco de dados garantem Atomicidade, Consistência, Isolamento e Durabilidade              |
| 📐 **SDD (Spec-Driven)**     | API RESTful definida via OpenAPI antes da implementação (API-First)                                    |
| 🧪 **Qualidade**             | Testes unitários críticos com cobertura >80%, CI/CD básico no GitHub Actions                           |
| 📦 **Containerização**       | Frontend, Backend e Banco de Dados rodam em containers Docker isolados                                 |
| 📊 **Metodologia Ágil**      | Desenvolvimento guiado por quadro Kanban para visualizar o fluxo de tarefas                            |

---

## 🧩 Principais Funcionalidades (Escopo MVP)

### Módulo de Autenticação

- Cadastro de novos usuários (username, nome, email, senha)
- Login/Logout seguro com JWT + refresh tokens
- Recuperação de senha via email (token de 15min)

### Módulo de Listas de Compras

- CRUD completo: Criação, edição, exclusão e listagem
- Adição de itens com campos: Produto (autocomplete), Quantidade
- Busca por nome de lista com paginação

### Módulo de Fornecedores e Catálogo (Seed)

- Dados populados automaticamente na inicialização do sistema
- 10 fornecedores + 50 produtos com preços variáveis
- Fornecedores associados a categorias (Supermercado, Informática, etc.)

### Módulo de Comparação de Preços

- Submissão de uma lista para cotação
- Geração de tabela flat com: Fornecedor, Itens Disponíveis, Itens Ausentes, Preço Total
- Destaque visual para o menor orçamento consolidado
- Listagem explícita dos produtos ausentes em cada fornecedor

### Módulo de Exportação

- Exportação para CSV (UTF-8 com BOM, delimitador `;`)
- Impressão otimizada via navegador (CSS `@media print`)

---

## 🛠️ Stack Tecnológica (FOSS - Gratuita e Open Source)

| Camada             | Tecnologias                                             | Motivo da Escolha                                                |
| ------------------ | ------------------------------------------------------- | ---------------------------------------------------------------- |
| **Frontend**       | React 18 + TypeScript + Vite + Tailwind CSS + shadcn/ui | Padrão de mercado, build ultra-rápido, componentes acessíveis    |
| **Backend**        | Node.js 20 + NestJS 10 + TypeScript                     | Clean Architecture por padrão, OpenAPI automático, tipagem forte |
| **Banco de Dados** | PostgreSQL 16 + Prisma ORM 5                            | ACID, JSON support, type-safe queries, migrations                |
| **API**            | RESTful + OpenAPI (Swagger)                             | Contratos claros entre Front e Back (SDD)                        |
| **Infraestrutura** | Docker 24 + Docker Compose 2                            | Isolamento dos serviços, reprodutibilidade de ambiente           |
| **CI/CD**          | GitHub Actions                                          | Pipeline automatizado para testes e validação de código          |
| **Testes**         | Jest (backend) + Vitest (frontend)                      | Cobertura de casos de uso críticos (>80%)                        |
| **Email**          | Resend (free tier) + Mailhog (dev)                      | Envio de emails para recuperação de senha                        |

---

## 🏗️ Arquitetura Geral (Docker Compose)

```
┌─────────────────────────────────────────────────────────────┐
│                      DOCKER NETWORK                         │
├─────────────────┬─────────────────┬─────────────────────────┤
│   FRONTEND      │    BACKEND      │   POSTGRESQL            │
│   (React + TS)  │ (NestJS + TS)   │   (Database)            │
│   Porta: 8080   │   Porta: 3000   │   Porta: 5432           │
├─────────────────┴─────────────────┴─────────────────────────┤
│               Comunicação via API REST (OpenAPI)            │
└─────────────────────────────────────────────────────────────┘
```

- **Frontend** consome a API do Backend via TanStack Query
- **Backend** aplica as regras de negócio e acessa o Banco via Prisma ORM
- **Banco de Dados** armazena usuários, listas, fornecedores, produtos e preços
- **Seed** é executado automaticamente na subida do container do Banco

---

## 🚀 Como Executar o Projeto (Passos Rápidos)

```bash
# 1. Clone o repositório
git clone https://github.com/leonardosetti/COBECO.git

# 2. Acesse o diretório
cd COBECO

# 3. Copie o arquivo de variáveis de ambiente
cp .env.example .env

# 4. Suba os containers via Docker Compose
docker-compose up -d --build

# 5. Acesse a aplicação no navegador
# Frontend: http://localhost:8080
# Backend API: http://localhost:3000
# Swagger Docs: http://localhost:3000/api/docs

# 6. (Opcional) Execute os testes
docker-compose exec backend npm run test
docker-compose exec frontend npm run test
```

**Nota:** O banco de dados já será populado com fornecedores, categorias e produtos de exemplo assim que subir (via seed automático).

---

## 📋 Escopo: O que NÃO está incluso (Out of Scope)

Para manter o KISS e entregar dentro do prazo (30 dias), os seguintes itens estão deliberadamente fora do escopo desta versão:

- ❌ Integração com APIs reais de e-commerce ou web scraping
- ❌ Desenvolvimento de aplicativos mobile nativos (Android/iOS)
- ❌ Processamento de pagamentos ou intermediação financeira
- ❌ Cálculo de fretes ou roteirização logística
- ❌ Geração de PDF nativo (apenas CSV + impressão via navegador)
- ❌ Suporte a múltiplos idiomas ou moedas (apenas BRL)
- ❌ Autenticação via OAuth (Google/Facebook)
- ❌ BDD/E2E tests completos (apenas unitários críticos)

---

## 🧠 Princípios de Desenvolvimento Adotados

| Princípio               | Aplicação no Projeto                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| **UI/UX Desktop-First** | Interface otimizada para telas ≥1024px, feedback visual claro (spinners, skeletons, toasts) |
| **Clean Code**          | Código legível, nomenclatura significativa, funções com responsabilidade única              |
| **Clean Architecture**  | Separação entre Domínio, Casos de Uso, Adaptadores e Frameworks                             |
| **ACID**                | Garantia de atomicidade, consistência, isolamento e durabilidade nas operações de banco     |
| **SDD (Spec-Driven)**   | Contratos OpenAPI definidos antes do desenvolvimento                                        |
| **CI/CD**               | Pipeline automatizado no GitHub Actions para validar builds e execução de testes            |
| **Kanban**              | Gestão do projeto com quadro Kanban (GitHub Projects) para visualização do fluxo            |

---

## 📅 Cronograma e Status Atual

| Fase                             | Duração     | Status                                     |
| -------------------------------- | ----------- | ------------------------------------------ |
| **Fase 1: Setup e Infra**        | 3 dias      | 🟢 Em andamento                            |
| **Fase 2: Backend Core**         | 10 dias     | ⏳ Aguardando                              |
| **Fase 3: Frontend Core**        | 10 dias     | ⏳ Aguardando                              |
| **Fase 4: Testes e Refinamento** | 5 dias      | ⏳ Aguardando                              |
| **Fase 5: Deploy e Validação**   | 2 dias      | ⏳ Aguardando                              |
| **TOTAL**                        | **30 dias** | 🚩 **Data Limite: 13 de Novembro de 2026** |

**Metodologia de Gestão:** Kanban (GitHub Projects)  
**Rituais:** Daily Standup (19:00), Sprint Planning/Review/Retrospectiva (sextas-feiras)

---

## 📞 Contato e Governança

**Canais de Comunicação:**

- **WhatsApp:** [#COBECO-MVP](https://chat.whatsapp.com/LV33cRZKwFAAoaPljTcvLx)
- **Documentação:** [GitHub](https://github.com/leonardosetti/COBECO)
- **Email:** TBD

**Equipe:**

- **Product Owner:** [Nome do Stakeholder]
- **Tech Lead:** [Nome do Desenvolvedor Sênior]
- **Arquiteto de Software:** [Nome do Arquiteto]

---

## 📝 Licenças e Compliance

Todas as tecnologias utilizadas são **FOSS** (Free and Open Source Software) ou possuem free tiers adequados:

- **Resend:** Free tier (3000 emails/mês)
- **GitHub Actions:** Free para repos públicos, 2000 min/mês para privados
- **PostgreSQL, Node.js, React:** Licenças MIT/Apache

---

## 🚀 Próximos Passos

1. ✅ Aprovação deste README e especificação do MVP
2. ⏳ Geração dos artefatos UML (Casos de Uso, Transição de Estados, DER)
3. ⏳ Protótipo de baixa fidelidade no Figma/Excalidraw
4. ⏳ Setup inicial dos repositórios (frontend + backend + infra)
5. ⏳ Desenvolvimento iterativo em sprints de 1 semana

---

**Este README é um documento vivo e será atualizado conforme o progresso do desenvolvimento.**

**Última atualização:** 31 de Agosto de 2026
