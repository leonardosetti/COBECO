# ESPECIFICAÇÃO DO MVP - SISTEMA COBECO (COTAÇÃO DE BENS DE CONSUMO)

**Disciplina:** Laboratório de Engenharia de Software | **Curso:** Análise e Desenvolvimento de Sistemas | **FATEC Taquaritinga**

---

## 1. OBJETIVO DO PROJETO

O **COBECO (Cotação de Bens de Consumo)** é uma aplicação web _desktop-first_ que tem como objetivo geral permitir que usuários criem listas de compras personalizadas e, a partir de um catálogo de preços previamente populado (via _seed_), realizem comparações de preços entre diferentes fornecedores, obtendo orçamentos consolidados com base na disponibilidade real de produtos por fornecedor.

A solução visa eliminar o trabalho manual de cotação, utilizando um algoritmo de otimização para:

1. Agrupar fornecedores por **paridade de disponibilidade** (percentual de itens da lista que cada fornecedor possui);
2. Calcular o orçamento de cada sublista resultante, considerando apenas os produtos disponíveis;
3. Destacar o melhor orçamento consolidado e evidenciar claramente os **produtos ausentes** em cada agrupamento.

O sistema será desenvolvido estritamente em formato de **MVP (Minimal Viable Product)** , com dados de fornecedores, produtos e preços previamente populados (via _seed_), permitindo validação rápida da lógica de negócio e da experiência do usuário dentro do prazo estabelecido.

---

## 2. ESCOPO

### 2.1. Incluso no Escopo (In Scope)

| Área                         | Descrição                                                                                                                          |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Autenticação**             | Cadastro, login, recuperação de senha e logout de usuários, com sessão segura                                                      |
| **Gestão de Listas**         | Criação, edição, exclusão, duplicação e visualização de listas de compras com itens (nome, categoria, quantidade)                  |
| **Persistência**             | Armazenamento de listas, itens, fornecedores, produtos e preços em banco de dados relacional (PostgreSQL)                          |
| **Seed de Dados**            | População inicial de fornecedores, categorias, produtos e preços via scripts de _seed_ (dados mockados)                            |
| **Motor de Orçamento**       | Algoritmo que cruza a lista do usuário com catálogos dos fornecedores, gerando sublistas agrupadas por paridade de disponibilidade |
| **Visualização Comparativa** | Exibição de orçamentos por sublista, com destaque para o menor custo consolidado e lista de produtos ausentes por agrupamento      |
| **API RESTful**              | Comunicação entre frontend e backend via API REST documentada com OpenAPI (Swagger)                                                |
| **Testes Automatizados**     | BDD (Gherkin/Cucumber), testes unitários e testes E2E (Playwright/Cypress)                                                         |
| **Infraestrutura**           | Containerização via Docker (Frontend, Backend, Banco de Dados) com CI/CD básico                                                    |

### 2.2. Excluído do Escopo (Out of Scope)

- Aplicativos nativos para dispositivos móveis (iOS/Android)
- Integração com APIs externas reais de comércio eletrônico
- _Web scraping_ em tempo real
- Processamento de pagamentos ou intermediação financeira
- Roteirização logística (cálculo de distância/frete)
- Suporte a múltiplos idiomas e moedas (exceto moeda local)
- Autenticação via contas de terceiros (Google, etc.)

---

## 3. REQUISITOS

Os requisitos estão organizados em três categorias: **Funcionais** (ações que o sistema deve executar), **Não Funcionais** (atributos de qualidade e restrições), e **Desejáveis** (podem ser implementados após o MVP).

---

### 3.1. Requisitos Funcionais (RF)

#### 3.1.1. Autenticação e Controle de Acesso

| Código   | Descrição do Requisito                                                                                                                         |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **RF01** | O sistema deve permitir o cadastro de novos usuários mediante nome, e-mail e senha, validando formato do e-mail e não duplicidade de registro. |
| **RF02** | O sistema deve permitir autenticação do usuário por e-mail e senha, redirecionando-o à área logada.                                            |
| **RF03** | O sistema deve permitir o encerramento seguro da sessão do usuário (logout).                                                                   |
| **RF04** | O sistema deve oferecer mecanismo de recuperação/redefinição de senha via e-mail cadastrado.                                                   |
| **RF05** | O sistema deve bloquear o acesso às rotas da plataforma a usuários não autenticados.                                                           |

#### 3.1.2. Gestão de Listas e Produtos

| Código   | Descrição do Requisito                                                                                                                                  |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RF06** | O sistema deve permitir que o usuário autenticado crie listas nomeadas de produtos destinadas à cotação.                                                |
| **RF07** | O sistema deve permitir a inclusão de itens em uma lista com os atributos: nome do produto, categoria (selecionada de lista pré-definida) e quantidade. |
| **RF08** | O sistema deve permitir a edição do nome da lista, bem como a edição e remoção dos itens nela contidos.                                                 |
| **RF09** | O sistema deve permitir a duplicação de uma lista existente.                                                                                            |
| **RF10** | O sistema deve permitir a exclusão de listas, mediante confirmação da ação pelo usuário.                                                                |
| **RF11** | O sistema deve exibir todas as listas pertencentes ao usuário autenticado, com resumo de itens e data de criação.                                       |

#### 3.1.3. Cotação e Comparação de Preços (Motor de Paridade)

| Código   | Descrição do Requisito                                                                                                                                                          |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RF12** | O sistema deve permitir a solicitação de cotação para uma lista específica, processando todos os itens nela contidos.                                                           |
| **RF13** | O sistema deve agrupar os fornecedores em **sublistas** conforme a quantidade de itens da lista do usuário que cada fornecedor possui: Grupo 100%, Grupo ≥80%, Grupo ≥60%, etc. |
| **RF14** | O sistema deve calcular o valor total de cada sublista, considerando apenas os produtos disponíveis no catálogo daquele agrupamento de fornecedores.                            |
| **RF15** | O sistema deve identificar e destacar visualmente a sublista com o **menor custo consolidado**.                                                                                 |
| **RF16** | O sistema deve listar, para cada sublista, os **produtos ausentes** (não disponíveis naquele agrupamento de fornecedores).                                                      |
| **RF17** | O sistema deve permitir que o usuário escolha quais fornecedores devem ser incluídos ou excluídos da comparação.                                                                |
| **RF18** | O sistema deve apresentar os resultados em painel comparativo contendo: nome do produto, fornecedor, preço, disponibilidade, e orçamento consolidado por agrupamento.           |

#### 3.1.4. Histórico e Persistência

| Código   | Descrição do Requisito                                                                                            |
| -------- | ----------------------------------------------------------------------------------------------------------------- |
| **RF19** | O sistema deve persistir em banco de dados todas as cotações realizadas pelo usuário, com data/hora e resultados. |
| **RF20** | O sistema deve permitir a visualização e reabertura de cotações anteriormente realizadas.                         |
| **RF21** | O sistema deve permitir a exclusão de registros do histórico de cotações do usuário.                              |

#### 3.1.5. Tratamento de Exceções

| Código   | Descrição do Requisito                                                                                                       |
| -------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **RF22** | O sistema deve exibir mensagem apropriada quando nenhum fornecedor possuir produtos da lista pesquisada.                     |
| **RF23** | O sistema deve sinalizar casos em que informações de preço ou disponibilidade não estiverem completas para um produto.       |
| **RF24** | O sistema deve validar a integridade dos dados da lista antes de submeter à cotação (ex: itens sem nome ou quantidade zero). |

---

### 3.2. Requisitos Não Funcionais (RNF)

#### 3.2.1. Arquitetura e Código

| Código    | Descrição do Requisito                                                                                                                                                                                                      |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RNF01** | O projeto deve seguir rigorosamente os princípios de **Clean Code** (código legível, nomes significativos, funções pequenas) e **Clean Architecture** (separação clara entre domínio, casos de uso, adapters e frameworks). |
| **RNF02** | Toda comunicação entre UI e backend deve ocorrer via **API RESTful**, regida por contratos **OpenAPI (Swagger)**, adotando a abordagem _API-First_ (**SDD - Specification-Driven Development**).                            |
| **RNF03** | O banco de dados relacional (**PostgreSQL**) deve garantir as propriedades **ACID**, utilizando _migrations_ versionadas para controle de schema.                                                                           |
| **RNF04** | A aplicação deve ser containerizada com **Docker** em três serviços: Frontend (UI), Backend (API) e Banco de Dados (PostgreSQL).                                                                                            |

#### 3.2.2. Testes e Qualidade

| Código    | Descrição do Requisito                                                                                                                                           |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RNF05** | O sistema deve adotar **BDD (Behavior-Driven Development)** com cenários escritos em **Gherkin** (ex: Cucumber) para validação das regras de paridade e cotação. |
| **RNF06** | O sistema deve ter cobertura de **testes unitários** para os casos de uso e regras de domínio (ex: Jest/Vitest).                                                 |
| **RNF07** | O sistema deve ter **testes E2E (End-to-End)** para validação de fluxos críticos na UI (ex: Playwright ou Cypress).                                              |
| **RNF08** | O sistema deve implementar **CI/CD** básico (ex: GitHub Actions) para execução automática de testes e validação de qualidade a cada _push_.                      |

#### 3.2.3. UX/UI e Usabilidade (IHC)

| Código    | Descrição do Requisito                                                                                                                              |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RNF09** | A interface deve ser **Desktop-First**, otimizada para telas de desktop (resolução ≥ 1024x768), com organização visual clara e foco em usabilidade. |
| **RNF10** | O sistema deve exibir indicadores de carregamento (spinners, skeleton screens) e mensagens de erro compreensíveis ao usuário.                       |
| **RNF11** | A aplicação deve observar boas práticas de acessibilidade (contraste adequado, navegação por teclado, rótulos claros em formulários).               |
| **RNF12** | O layout deve priorizar a rápida compreensão dos resultados comparativos, com uso de cores e ícones para destacar o melhor orçamento.               |

#### 3.2.4. Segurança e Desempenho

| Código    | Descrição do Requisito                                                                                                                      |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **RNF13** | As senhas dos usuários devem ser armazenadas mediante algoritmo de hash seguro (ex: bcrypt), jamais em texto puro.                          |
| **RNF14** | Toda comunicação entre cliente e servidor deve ocorrer sob protocolo HTTPS (em ambiente de produção).                                       |
| **RNF15** | As sessões de usuário devem expirar após período de inatividade previamente definido (ex: 30 minutos).                                      |
| **RNF16** | O sistema deve ser otimizado para consultas rápidas, utilizando índices adequados no banco de dados para as operações de cotação.           |
| **RNF17** | A indisponibilidade de um serviço específico (ex: banco de dados) não deve comprometer a exibição de páginas estáticas (fallback adequado). |

#### 3.2.5. Tecnologias e Ferramentas

| Código    | Descrição do Requisito                                                                                                                                                                                         |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RNF18** | Toda a stack tecnológica deve utilizar ferramentas, frameworks e tecnologias **FOSS (Free and Open Source Software)** ou de uso livre/gratuito.                                                                |
| **RNF19** | **Backend:** Node.js (com Fastify ou Express) ou NestJS (recomendado para tipagem forte e Clean Architecture).                                                                                                 |
| **RNF20** | **Frontend:** HTML5, CSS3 e JavaScript/TypeScript. Recomenda-se **Alpine.js** ou **Vue.js** para reatividade simples, evitando complexidade de frameworks pesados (React + jQuery é considerado anti-pattern). |
| **RNF21** | **Banco de Dados:** PostgreSQL com **Prisma ORM** ou **Drizzle ORM** para mapeamento e migrations.                                                                                                             |
| **RNF22** | **Versionamento:** GitHub com Git Flow ou GitHub Flow.                                                                                                                                                         |

---

### 3.3. Requisitos Desejáveis (Pós-MVP)

| Código   | Descrição do Requisito                                                                |
| -------- | ------------------------------------------------------------------------------------- |
| **RD01** | Autenticação por meio de contas de terceiros (Google, etc.).                          |
| **RD02** | Notificação ao usuário quando um produto atingir valor inferior a um limite definido. |
| **RD03** | Exportação dos resultados de cotação em PDF ou planilha eletrônica (CSV).             |
| **RD04** | Representação gráfica (gráficos) da variação de preços.                               |
| **RD05** | Compartilhamento de listas com outros usuários.                                       |
| **RD06** | Tema claro/escuro (Dark Mode).                                                        |
| **RD07** | Perfil administrativo para gerenciamento de fornecedores e produtos.                  |
| **RD08** | Suporte a múltiplos idiomas (i18n).                                                   |

---

## 4. EXEMPLO DE SAÍDA ESPERADA (COTAÇÃO COM PARIDADE)

**Lista do Usuário (9 produtos):** Leite, Pão, Manteiga, Arroz, Feijão, Óleo, Açúcar, Café, Sabonete

| Grupo de Paridade    | Fornecedores                              | Itens Disponíveis                                                 | Itens Ausentes                   | Orçamento Total           |
| -------------------- | ----------------------------------------- | ----------------------------------------------------------------- | -------------------------------- | ------------------------- |
| **Grupo 100%** (9/9) | Supermercado A, Supermercado D, Mercado I | Leite, Pão, Manteiga, Arroz, Feijão, Óleo, Açúcar, Café, Sabonete | Nenhum                           | **R$ 142,50** ⭐ _Melhor_ |
| **Grupo 78%** (7/9)  | Mercado B, Supermercado F, Mercado H      | Leite, Pão, Arroz, Feijão, Óleo, Café, Sabonete                   | Manteiga, Açúcar                 | R$ 98,30                  |
| **Grupo 56%** (5/9)  | Loja E, Mercado G                         | Leite, Pão, Arroz, Feijão, Óleo                                   | Manteiga, Açúcar, Café, Sabonete | R$ 61,20                  |

> O sistema exibirá essa tabela ordenada, destacando o melhor orçamento consolidado (Grupo 100%) e deixando explícito o que o usuário deixaria de comprar em cada cenário alternativo.

---

## 5. PRINCÍPIOS E BOAS PRÁTICAS ADOTADOS

| Princípio                             | Aplicação no Projeto                                                                                                                           |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **KISS (Keep It Simple)**             | Dados mockados via seed (sem integração com APIs externas), escopo enxuto, UI desktop-first sem complexidade de responsividade mobile.         |
| **Clean Architecture**                | Separação entre Domínio (regras de negócio de paridade), Casos de Uso, Adaptadores (Controllers/Repositories) e Frameworks (Frontend/Backend). |
| **ACID**                              | Garantia de atomicidade, consistência, isolamento e durabilidade nas operações de banco de dados (criação de listas, salvamento de cotações).  |
| **SDD (Spec-Driven Development)**     | Contratos OpenAPI definidos antes do desenvolvimento; desenvolvimento orientado pela especificação da API.                                     |
| **BDD (Behavior-Driven Development)** | Cenários em Gherkin para validar as regras de paridade e cálculo de orçamentos.                                                                |
| **SQA (Software Quality Assurance)**  | Testes automatizados em todos os níveis (unitários, integração, E2E) desde o início do desenvolvimento.                                        |
| **Kanban**                            | Gestão do projeto com quadro Kanban (GitHub Projects ou Trello) para visualização do fluxo de desenvolvimento.                                 |
| **CI/CD**                             | Pipeline automatizado para validação de código, execução de testes e deploy (quando aplicável).                                                |

---

## 6. INFRAESTRUTURA E DEPLOY

```
┌─────────────────────────────────────────────────────────────┐
│                          DOCKER                             │
├─────────────────┬─────────────────┬───────────────────────┤
│  FRONTEND       │  BACKEND        │  POSTGRESQL           │
│  (Alpine.js /   │  (Node.js +     │  (Database)           │
│   Vue.js)       │   Fastify)      │                       │
├─────────────────┴─────────────────┴───────────────────────┤
│                    REDE INTERNA DOCKER                     │
└─────────────────────────────────────────────────────────────┘
```

- **Frontend:** Servido via Nginx ou Vite Preview (porta 80/8080)
- **Backend:** API RESTful (porta 3000/8080)
- **Banco de Dados:** PostgreSQL (porta 5432)
- **Docker Compose** para orquestração dos três serviços
- **Seed:** Script executado na inicialização do banco para popular fornecedores, categorias e produtos

---

## 7. CRONOGRAMA SUGERIDO (ATÉ 13/11/2026)

| Fase                        | Atividades                                                      | Duração Estimada |
| --------------------------- | --------------------------------------------------------------- | ---------------- |
| 1. Planejamento e Modelagem | Definição de requisitos, modelagem do banco, contrato OpenAPI   | 3 dias           |
| 2. Setup Inicial            | Configuração do projeto, Docker, CI/CD, estrutura de pastas     | 2 dias           |
| 3. Seed de Dados            | Criação de fornecedores, categorias, produtos e preços mockados | 1 dia            |
| 4. Desenvolvimento Backend  | Implementação da API, lógica de paridade, regras de cotação     | 5 dias           |
| 5. Desenvolvimento Frontend | Telas de autenticação, gestão de listas, resultados de cotação  | 4 dias           |
| 6. Testes                   | BDD, testes unitários, testes E2E                               | 3 dias           |
| 7. Integração e Ajustes     | Integração front-back, correções de bugs, refinamentos de UI    | 2 dias           |
| 8. Entrega Final            | Documentação, apresentação, deploy (se aplicável)               | 1 dia            |

**Total estimado:** 21 dias (com folga para ajustes)

---

Este documento unificado servirá como base para o desenvolvimento do MVP do sistema COBECO, garantindo alinhamento com as premissas do projeto, escopo definido, e adesão às boas práticas de engenharia de software exigidas pela disciplina.

{
"nodes":[
{"id":"9683de21074046cc","type":"file","file":"FATEC/lab_eng_software/mermaid-1786774301969.png","x":-880,"y":-320,"width":2065,"height":420,"color":"5"}
],
"edges":[]
}
