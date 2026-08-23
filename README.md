```markdown
# 🛒 COBECO - Cotação de Bens de Consumo (MVP)

**Sistema de Comparação de Preços para Listas de Compras**  
*Projeto acadêmico da disciplina de Laboratório de Engenharia de Software*  
**FATEC Taquariting - Análise e Desenvolvimento de Sistemas**

---

## 📖 1. Sobre o Projeto

### O Contexto
Em um mundo com múltiplas opções de fornecedores (supermercados, lojas de departamento, eletrônicos, etc.), comparar preços manualmente item a item é uma tarefa demorada, repetitiva e sujeita a erros. Para piorar, nem sempre um único fornecedor possui todos os produtos desejados, forçando o consumidor a fracionar suas compras.

### A Solução (MVP)
O **COBECO** surge como um **MVP (Produto Mínimo Viável)** acadêmico para resolver exatamente esse problema. Trata-se de uma aplicação *web-based* (focada em desktop) que permite ao usuário:

1. **Criar listas de compras** personalizadas com itens, quantidades e categorias;
2. **Submeter essas listas** a um motor de comparação que cruza os dados com um catálogo interno de fornecedores (populado via *seed*);
3. **Visualizar orçamentos consolidados**, agrupados por fornecedores com paridade de disponibilidade;
4. **Identificar lacunas** — o sistema gera sub-listas destacando quais produtos estão faltando em cada fornecedor, além de exibir o orçamento parcial para os itens disponíveis;
5. **Tomar a melhor decisão** com base no menor custo consolidado e na cobertura de itens.

### Por que esse MVP é único?
Diferente de ferramentas complexas que dependem de *web scraping* ou APIs externas em tempo real, o COBECO adota uma abordagem **pragmática e realista** para o prazo estipulado: todos os dados de fornecedores, produtos e preços são **mockados via scripts de seed** no banco de dados. Isso nos permite focar 100% da energia no desenvolvimento da **lógica de negócio** (cálculo de paridade e sub-listas), na **qualidade da arquitetura** (Clean Architecture + ACID) e na **experiência do usuário** (UI/UX Desktop-first), sem as dores de cabeça de integrações externas instáveis.

---

## 🎯 2. Objetivos do Projeto

**Objetivo Geral:**  
Desenvolver um MVP funcional e minimalista que automatize a comparação de preços entre fornecedores a partir de listas de compras criadas pelo usuário, fornecendo orçamentos claros e evidenciando produtos ausentes em cada cenário.

**Objetivos Específicos (Entregáveis do MVP):**
- Implementar autenticação segura (cadastro, login, recuperação de senha);
- Permitir CRUD completo de listas de compras (criar, editar, excluir, duplicar);
- Manter um cadastro interno de fornecedores, categorias e produtos (via *seed*);
- Desenvolver o "Motor de Paridade" que agrupa fornecedores por percentual de itens disponíveis e gera sub-listas;
- Exibir comparativos destacando o melhor orçamento e os produtos faltantes;
- Garantir a persistência dos dados (listas e históricos) em banco relacional (PostgreSQL);
- Estabelecer comunicação robusta entre Frontend e Backend via API RESTful documentada (OpenAPI).

---

## ⚙️ 3. Premissas e Restrições Fundamentais

Para garantir a entrega dentro do prazo (até **13 de Novembro de 2026**) e a qualidade esperada, o projeto está rigidamente ancorado nos seguintes pilares:

| Pilar | Aplicação no Projeto |
| :--- | :--- |
| **🧼 KISS (Keep It Simple)** | Escopo enxuto: dados mockados (sem APIs externas), UI exclusiva para desktop (sem complexidade mobile), lógica de negócio direta e objetiva. |
| **🏛️ Clean Architecture** | Separação rígida entre Domínio (regras de paridade), Casos de Uso, Adaptadores (Controllers/Repositories) e Frameworks (UI e DB). |
| **⚡ ACID** | Operações no banco de dados (criação de listas, salvamento de cotações) garantem Atomicidade, Consistência, Isolamento e Durabilidade. |
| **📐 SDD (Spec-Driven Development)** | Desenvolvimento orientado a contrato: a API RESTful é definida via OpenAPI antes da implementação (API-First). |
| **🧪 SQA & BDD** | Qualidade assegurada desde o início com cenários em Gherkin (Cucumber), testes unitários (Jest/Vitest) e testes E2E (Playwright/Cypress). |
| **📦 Containerização (Docker)** | Os três pilares do sistema (Frontend, Backend, Banco de Dados) rodam em contêineres Docker isolados, orquestrados por Docker Compose. |
| **📊 Metodologia Ágil** | Desenvolvimento guiado por quadro **Kanban** para visualizar o fluxo de tarefas e priorizar entregas contínuas. |

---

## 🧩 4. Principais Funcionalidades (Escopo MVP)

### Módulo de Autenticação
- Cadastro de novos usuários (nome, e-mail, senha criptografada com hash).
- Login/Logout seguro.
- Recuperação de senha via e-mail.

### Módulo de Listas de Compras
- **CRUD completo**: Criação, edição (nome e itens), exclusão e duplicação.
- Adição de itens com campos: *Nome do Produto*, *Categoria* (ex: Alimentos, Limpeza) e *Quantidade*.
- Visualização de todas as listas salvas pelo usuário.

### Módulo de Fornecedores e Catálogo (Seed)
- Dados populados automaticamente na inicialização do sistema.
- Fornecedores associados a uma ou mais categorias (ex: Supermercado, Informática, Eletrodomésticos).
- Catálogo de produtos com preços e *flag* de disponibilidade em estoque.

### Módulo de Cotação e Comparação (Motor de Paridade)
- Submissão de uma lista para cotação.
- Agrupamento de fornecedores por **paridade de disponibilidade**:
  - Ex: Grupo 100% (possuem todos os itens), Grupo ≥80%, Grupo ≥60%, etc.
- Cálculo do valor total para cada sub-lista (considerando apenas os itens disponíveis).
- **Destaque visual** para o menor orçamento consolidado.
- Listagem explícita dos **produtos ausentes** em cada agrupamento (essencial para a decisão de compra).

### Módulo de Histórico
- Persistência de todas as cotações realizadas.
- Possibilidade de reabrir e reexibir cotações antigas.

---

## 🛠️ 5. Stack Tecnológica (FOSS - Gratuita e Open Source)

| Camada | Tecnologias | Motivo da Escolha |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, TypeScript / **Alpine.js** ou **Vue.js** (leve) | Foco em simplicidade e renderização rápida. *Evitamos React + jQuery (anti-pattern)*. |
| **Backend** | Node.js + **Fastify** (ou Express) / **NestJS** | NestJS oferece tipagem forte e arquitetura modular, ideal para Clean Architecture. |
| **Banco de Dados** | **PostgreSQL** | Suporte robusto a ACID, excelente performance para queries matemáticas e integração com ORMs modernos. |
| **ORM/Migrations** | **Prisma** ou **Drizzle** | Facilita o versionamento do schema e a execução de seeds. |
| **API** | RESTful + **OpenAPI (Swagger)** | Garante contratos claros entre Front e Back (SDD). |
| **Infraestrutura** | **Docker** + **Docker Compose** | Isolamento dos serviços (Front, Back, DB) e reprodutibilidade do ambiente. |
| **Versionamento/CI** | **GitHub** + **GitHub Actions** | CI/CD básico para rodar testes e validar código a cada *push*. |
| **Testes** | **Gherkin/Cucumber** (BDD), **Jest/Vitest** (Unitário), **Playwright/Cypress** (E2E) | Cobertura total da pirâmide de testes, validando regras de negócio e interface. |

---

## 🏗️ 6. Arquitetura Geral (Docker Compose)

```text
┌─────────────────────────────────────────────────────────────┐
│                      DOCKER NETWORK                         │
├─────────────────┬─────────────────┬───────────────────────┤
│   FRONTEND      │    BACKEND      │   POSTGRESQL          │
│   (UI - UI/UX)  │ (API - Lógica)  │   (Persistência)      │
│   Porta: 8080   │   Porta: 3000   │   Porta: 5432         │
├─────────────────┴─────────────────┴───────────────────────┤
│               Comunicação via API REST (OpenAPI)           │
└─────────────────────────────────────────────────────────────┘
```

- **Frontend** consome a API do Backend.
- **Backend** aplica as regras de negócio (paridade) e acessa o Banco via ORM.
- **Banco de Dados** armazena usuários, listas, fornecedores, produtos e histórico.
- O *Seed* é executado automaticamente na subida do container do Banco, populando fornecedores e produtos mockados.

---

## 🚀 7. Como Executar o Projeto (Passos Rápidos)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/cobeco-mvp.git

# 2. Acesse o diretório
cd cobeco-mvp

# 3. Suba os containers via Docker Compose
docker-compose up -d --build

# 4. Acesse a aplicação no navegador
http://localhost:8080

# 5. (Opcional) Execute os testes
docker-compose exec backend npm run test
docker-compose exec frontend npm run test:e2e
```

> **Nota:** O banco de dados já será populado com fornecedores, categorias e produtos de exemplo assim que subir.

---

## 📋 8. Escopo: O que NÃO está incluso (Out of Scope)

Para manter o **KISS** e entregar dentro do prazo, os seguintes itens estão deliberadamente fora do escopo desta versão:

- ❌ Integração com APIs reais de e-commerce ou *web scraping*.
- ❌ Desenvolvimento de aplicativos mobile nativos (Android/iOS).
- ❌ Processamento de pagamentos ou intermediação financeira.
- ❌ Cálculo de fretes ou roteirização logística.
- ❌ Suporte a múltiplos idiomas ou moedas (apenas moeda local).
- ❌ Autenticação via OAuth (Google/Facebook).

---

## 🧠 9. Princípios de Desenvolvimento Adotados

- **UI/UX e IHC**: Interface Desktop-first com foco em usabilidade, feedback visual claro (spinners, skeletons) e acessibilidade básica (contraste, navegação por teclado).
- **Clean Code**: Código legível, nomenclatura significativa, funções com responsabilidade única.
- **CI/CD**: Pipeline automatizada no GitHub Actions para validar builds e execução de testes.
- **Melhoria Contínua**: Adoção de BDD desde o dia 1, garantindo que os requisitos sejam testáveis e rastreáveis.

---

## 👥 Equipe e Contexto Acadêmico

Projeto desenvolvido como requisito avaliativo para a disciplina de **Laboratório de Engenharia de Software** do curso de **Análise e Desenvolvimento de Sistemas** na **FATEC Taquariting**.

---

## 📅 Cronograma e Status Atual

- **Início do Desenvolvimento:** 🟢 Em andamento.
- **Data Limite para Entrega:** 🚩 13 de Novembro de 2026.
- **Metodologia de Gestão:** Kanban (Quadro no GitHub Projects ou Trello).

---

*Este README é um documento vivo e será atualizado conforme o progresso do desenvolvimento.*
```
