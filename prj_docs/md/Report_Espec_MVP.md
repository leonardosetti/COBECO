# 📊 RELATÓRIO DE ESPECIFICAÇÃO - MVP COMPARADOR DE COMPRAS

**Versão:** 2.0 (MVP Simplificado)
**Data:** 31 de Agosto de 2026
**Status:** Aprovado para Desenvolvimento
**Público-Alvo:** Equipe de Desenvolvimento + Stakeholders

---

## 📋 SUMÁRIO EXECUTIVO

Este documento apresenta a especificação final do MVP "Comparador de Compras", uma aplicação web desktop-first que permite usuários criar listas de compras e comparar orçamentos entre múltiplos fornecedores, destacando a opção mais econômica e evidenciando produtos ausentes em cada cenário.

**Objetivo do MVP:** Validar a proposta de valor com implementação rápida (4-6 semanas), simplificando funcionalidades complexas e eliminando dependências externas desnecessárias.

**Decisões Críticas Tomadas:**

- ✅ Motor de paridade simplificado (tabela flat vs. agrupamento complexo)
- ✅ Validação de email por formato (eliminando dependência de serviço externo)
- ✅ Exportação reduzida (CSV + impressão via navegador, eliminando PDF)
- ✅ CI/CD focado em testes unitários críticos (eliminando BDD/E2E no MVP)
- ✅ Adição de recuperação de senha e histórico de listas (essenciais para usabilidade)

---

## 🎯 1. CONTEXTO E OBJETIVOS

### 1.1. Problema

Usuários que precisam comprar múltiplos itens (supermercado, materiais, etc.) enfrentam o trabalho manual de:

1. Listar produtos desejados
2. Consultar preços em múltiplos fornecedores
3. Comparar disponibilidade (nem todos têm todos os produtos)
4. Calcular qual combinação resulta em menor custo total

### 1.2. Solução Proposta

Aplicação web que automatiza esse processo:

- Usuário cria lista de itens com quantidades
- Sistema cruza com catálogo base de fornecedores (previamente populado)
- Exibe tabela comparativa com: fornecedor, itens disponíveis, itens ausentes, preço total
- Destaca a opção mais econômica
- Permite exportar resultado (CSV) ou imprimir

### 1.3. Escopo do MVP

**INCLUIDO:**

- Gestão de usuários (cadastro, login, logout, recuperação de senha)
- CRUD completo de listas de compras
- Motor de comparação simplificado (tabela flat)
- Exportação CSV + impressão via navegador
- Seed de dados (10 fornecedores, 50 produtos)
- Testes unitários críticos + CI básico

**EXCLUIDO:**

- Apps móveis (iOS/Android/PWA)
- Integração com LLMs
- Web scraping em tempo real
- Processamento de pagamentos
- Roteirização logística
- Geração de PDF nativo
- Validação de email real (envio de link)
- BDD/E2E tests no MVP

---

## 🔐 2. REQUISITOS FUNCIONAIS (RF) - VERSÃO FINAL

### 2.1. Autenticação e Gestão de Usuários

| ID       | Requisito                                                                                  | Guard-Rails                                                                                                                                                                                              | Validação                                                                                                                                                |
| -------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RF01** | **Cadastro de Usuário**Campos: username (único), nome completo, email, senha + confirmação | - Username: 3-30 chars, alfanumérico + underscore- Nome: 2-100 chars- Email: formato válido (regex), max 255 chars- Senha: mín 8 chars, 1 maiúscula, 1 número, 1 especial- Confirmação deve ser idêntica | - Username único (constraint DB)- Email único (constraint DB)- Senha hasheada (bcrypt, salt=12)- Mensagens de erro específicas por campo                 |
| **RF02** | **Login**Email ou username + senha                                                         | - Rate limiting: 5 tentativas/15min por IP- Bloqueio temporário após falhas consecutivas- Mensagem genérica: "Credenciais inválidas" (não revelar se email existe)                                       | - Validação de formato antes de enviar- Token JWT com expiração de 1h- Refresh token com expiração de 7 dias- Armazenar refresh token em httpOnly cookie |
| **RF03** | **Logout**Encerrar sessão ativa                                                            | - Invalidar refresh token no backend- Limpar storage do frontend- Redirecionar para /login                                                                                                               | - Endpoint POST /auth/logout- Retornar 204 No Content- Frontend limpa estado e redireciona                                                               |
| **RF04** | **Recuperação de Senha**Enviar link de reset via email                                     | - Token de reset com expiração de 15min- Máximo 3 solicitações/hora por email- Link único e de uso único- Nova senha deve seguir mesmas regras de RF01                                                   | - Validar formato de email- Gerar token criptograficamente seguro- Enviar email via Resend (free tier)- Tela de confirmação após envio                   |
| **RF05** | **Perfil do Usuário**Visualizar e editar dados pessoais                                    | - Email só pode ser alterado com validação- Senha antiga deve ser confirmada para alteração- Exclusão de conta requer confirmação (digitar "EXCLUIR")                                                    | - Validação de campos antes de salvar- Confirmar exclusão com modal- Soft delete (marcar como inativo, não remover dados)                                |

### 2.2. Gestão de Listas de Compras

| ID       | Requisito                                                                  | Guard-Rails                                                                                                                                        | Validação                                                                                                                     |
| -------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **RF06** | **Criar Lista**Nome da lista + adicionar itens (produto + quantidade)      | - Nome da lista: 1-100 chars, obrigatório- Mínimo 1 item para salvar- Quantidade: inteiro positivo (1-9999)- Produto deve existir no catálogo (FK) | - Validar campos obrigatórios no frontend- Verificar se produto existe no DB- Calcular subtotal por item (quantidade × preço) |
| **RF07** | **Listar Listas**Mostrar todas as listas do usuário                        | - Paginação: 20 itens por página- Ordenação padrão: data de criação (mais recente primeiro)- Busca por nome (case-insensitive, contains)           | - Exibir: nome, data criação, qtd itens, valor estimado- Link para editar/excluir/comparar- Mensagem se não houver listas     |
| **RF08** | **Editar Lista**Alterar nome, adicionar/remover itens, ajustar quantidades | - Validação de quantidade (RF06)- Confirmação antes de remover item- Salvar automaticamente a cada 30s (draft)                                     | - Modal de confirmação para remoção- Toast de sucesso após salvar- Atualizar valor total em tempo real                        |
| **RF09** | **Excluir Lista**Remover lista permanentemente                             | - Confirmação obrigatória (modal)- Digitar nome da lista para confirmar- Soft delete (marcar como inativo)                                         | - Modal com campo de confirmação- Botão desabilitado até confirmação- Toast de sucesso após exclusão                          |
| **RF10** | **Buscar Produtos**Autocomplete ao digitar nome do produto                 | - Mínimo 2 caracteres para iniciar busca<br- Máximo 10 resultados exibidos- Debounce de 300ms- Destacar texto correspondente                       | - Query com LIKE '%termo%'- Retornar: id, nome, categoria, preço médio- Cache de resultados no frontend (5min)                |

### 2.3. Comparação de Fornecedores

| ID       | Requisito                                                                                       | Guard-Rails                                                                                                                                                       | Validação                                                                                                                                                                                 |
| -------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **RF11** | **Calcular Orçamento**Gerar tabela comparativa de fornecedores                                  | - Lista deve ter mínimo 1 item- Timeout de 10s para cálculo- Cache de resultados por 5min- Máximo 50 fornecedores comparados simultaneamente                      | - Validar se lista existe e pertence ao usuário- Verificar se há preços cadastrados- Calcular: itens disponíveis, itens ausentes, preço total- Ordenar por preço total (menor para maior) |
| **RF12** | **Visualizar Resultados**Tabela com: Fornecedor, Itens Disponíveis, Itens Ausentes, Preço Total | - Destacar linha com menor preço (verde)- Exibir % de disponibilidade (ex: "7/9 itens")- Tooltip explicando itens ausentes- Responsivo para largura mínima 1024px | - Formatação de moeda (BRL)- Ícone de alerta para itens ausentes- Botão "Exportar" e "Imprimir" sempre visíveis                                                                           |

### 2.4. Exportação e Impressão

| ID       | Requisito                                              | Guard-Rails                                                                                                                             | Validação                                                                                                                                                    |
| -------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **RF13** | **Exportar CSV**Baixar arquivo com dados da comparação | - Nome do arquivo: lista_nome_YYYYMMDD.csv- Encoding: UTF-8 com BOM- Delimitador: ponto e vírgula (;)- Máximo 1MB por arquivo           | - Incluir cabeçalho: Fornecedor,Itens Disponíveis,Itens Ausentes,Preço Total- Escapar caracteres especiais (aspas, vírgulas)- Toast de sucesso após download |
| **RF14** | **Imprimir**View otimizada para Ctrl+P                 | - CSS @media print oculta menus e botões- Formatação de tabela para A4- Quebras de página automáticas- Incluir data e hora da impressão | - Botão "Imprimir" chama window.print()- Preview antes de imprimir<br- Manter cores para destacar melhor oferta                                              |

---

## ⚙️ 3. REQUISITOS NÃO FUNCIONAIS (RNF) - VERSÃO FINAL

### 3.1. Arquitetura e Código

| ID        | Requisito                                                                       | Guard-Rails                                                                                                                                                    | Métrica de Sucesso                                                                                      |
| --------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **RNF01** | **Clean Architecture**Backend NestJS com camadas claras                         | - Separação: Domain → UseCase → Adapter → Framework- Dependência apenas inwards- Injeção de dependência obrigatória- Sem lógica de negócio em controllers      | - Code review aprova estrutura- Testes unitários isolam camadas- Documentação de arquitetura atualizada |
| **RNF02** | **SDD (Specification-Driven Development)**OpenAPI definido antes de implementar | - Contratos OpenAPI versionados- Geração automática de tipos TypeScript- Validação de request/response no backend- Documentação Swagger acessível em /api/docs | - Frontend e backend usam mesmos tipos- Zero erros de integração em produção- Swagger sempre atualizado |
| **RNF03** | **ACID com PostgreSQL**Integridade transacional garantida                       | - Todas writes em transações- Foreign keys com CASCADE ou RESTRICT- Isolation level: Read Committed- Migrations versionadas e reversíveis                      | - Zero dados órfãos no DB- Rollback automático em falhas- Migrations testadas em staging                |

### 3.2. UI/UX e Usabilidade

| ID        | Requisito                                                   | Guard-Rails                                                                                                                                                       | Métrica de Sucesso                                                                                                |
| --------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **RNF04** | **Desktop-First**Layout exclusivo para telas ≥1024px        | - Breakpoint mínimo: 1024px- Sem responsividade mobile<br- Grid system com 12 colunas<br- Espaçamento consistente (8px base)                                      | - Layout não quebra em 1024px+<br- Testado em Chrome, Firefox, Edge<br- Acessível por teclado (Tab, Enter, Esc)   |
| **RNF05** | **Feedback Visual**Toasts, skeletons, modais                | - Toasts: sucesso (verde), erro (vermelho), info (azul)- Skeletons para loading >300ms<br- Modais para ações destrutivas<br- Botões desabilitados durante loading | - Tempo de feedback <100ms<br- Zero "dead clicks" (cliques sem resposta)<br- Usuário sempre sabe o estado da ação |
| **RNF06** | **Validação em Tempo Real**Campos validados antes do submit | - Validação no onBlur (ao sair do campo)<br- Mensagens de erro abaixo do campo<br- Ícones de sucesso/erro nos campos<br- Botão submit desabilitado se inválido    | - Zero submits com dados inválidos<br- Mensagens claras e específicas<br- Usuário corrige erros antes de enviar   |

### 3.3. Qualidade e Testes

| ID        | Requisito                                              | Guard-Rails                                                                                                                                            | Métrica de Sucesso                                                                              |
| --------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| **RNF07** | **Testes Unitários**Cobertura de casos de uso críticos | - Cobertura mínima: 80%<br- Testes de: autenticação, cálculo de preço, validações<br- Mock de dependências externas<br- Testes isolados e idempotentes | - Cobertura >80% no SonarQube<br- Zero testes flaky (intermitentes)<br- Tempo de execução <2min |
| **RNF08** | **CI Básico**GitHub Actions rodando testes             | - Pipeline: lint → test → build<br- Roda em cada push e PR<br- Bloqueia merge se testes falharem<br- Cache de node_modules para velocidade             | - Pipeline completo <5min<br- Zero merges com testes falhando<br- Notificação no Slack/Discord  |

### 3.4. Dados e Performance

| ID        | Requisito                                      | Guard-Rails                                                                                                                                                                                        | Métrica de Sucesso                                                                            |
| --------- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **RNF09** | **Seed de Dados**10 fornecedores + 50 produtos | - Dados realistas (nomes brasileiros, preços em BRL)<br- Variação de preços entre fornecedores (±20%)<br- Alguns fornecedores sem todos os produtos<br- Script de seed executável via npm run seed | - Seed popula DB em <10s<br- Dados consistentes (FKs válidas)<br- Preços realistas para teste |
| **RNF10** | **Performance**Tempos de resposta aceitáveis   | - API response time <500ms (p95)<br- Frontend First Contentful Paint <1.5s<br- Time to Interactive <3s<br- Bundle size <500KB (gzipped)                                                            | - Lighthouse score >90<br- Zero timeouts em produção<br- Cache de assets estáticos (1 ano)    |

### 3.5. Segurança

| ID        | Requisito                                           | Guard-Rails                                                                                                                                            | Métrica de Sucesso                                                                                                        |
| --------- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| **RNF11** | **Autenticação Segura**JWT + refresh tokens         | - Access token: 1h de expiração<br- Refresh token: 7 dias, httpOnly cookie<br- Senhas hasheadas com bcrypt (salt=12)<br- HTTPS obrigatório em produção | - Zero tokens vazados em logs<br- Refresh tokens rotacionados a cada uso<br- Rate limiting em endpoints sensíveis         |
| **RNF12** | **Proteção contra Ataques**CSRF, XSS, SQL Injection | - CSRF tokens em formulários<br- Sanitização de inputs (DOMPurify)<br- Parameterized queries (Prisma ORM)<br- Content Security Policy (CSP) headers    | - Zero vulnerabilidades críticas no OWASP ZAP<br- Headers de segurança configurados<br- Inputs validados em todas camadas |
| **RNF13** | **Rate Limiting**Proteção contra abuso              | - Auth endpoints: 5 req/15min por IP<br- API geral: 100 req/min por usuário<br- Retornar 429 Too Many Requests<br- Headers X-RateLimit-\*              | - Zero DDoS bem-sucedidos<br- Usuários legítimos não bloqueados<br- Logs de tentativas bloqueadas                         |

---

## 🛠️ 4. STACK TECNOLÓGICA DEFINIDA

### 4.1. Frontend

| Tecnologia          | Versão | Justificativa                                                 |
| ------------------- | ------ | ------------------------------------------------------------- |
| **React**           | 18.x   | Padrão de mercado, ecossistema maduro, comunidade ativa       |
| **TypeScript**      | 5.x    | Segurança de tipos, SDD, autocompletar, refactoring seguro    |
| **Vite**            | 5.x    | Build ultra-rápido (<1s), HMR instantâneo, config simples     |
| **Tailwind CSS**    | 3.x    | Utility-first, sem CSS customizado, design system consistente |
| **shadcn/ui**       | Latest | Componentes acessíveis, customizáveis, sem dependência pesada |
| **TanStack Query**  | 5.x    | Cache, loading states, retry automático, otimistic updates    |
| **React Hook Form** | 7.x    | Performance, validação integrada, menos re-renders            |
| **Zod**             | 3.x    | Validação de schemas, integração com React Hook Form          |
| **date-fns**        | 3.x    | Manipulação de datas, tree-shakable, leve                     |

### 4.2. Backend

| Tecnologia          | Versão     | Justificativa                                                 |
| ------------------- | ---------- | ------------------------------------------------------------- |
| **Node.js**         | 20.x (LTS) | Performance, ecossistema JavaScript, async/await              |
| **NestJS**          | 10.x       | Clean Architecture por padrão, decorators, OpenAPI automático |
| **TypeScript**      | 5.x        | Mesmas razões do frontend, tipagem forte                      |
| **Prisma ORM**      | 5.x        | Type-safe queries, migrations, introspection, excelente DX    |
| **PostgreSQL**      | 16.x       | ACID, JSON support, performance, FOSS                         |
| **Passport.js**     | 0.7.x      | Autenticação flexível, estratégias múltiplas                  |
| **bcrypt**          | 5.x        | Hashing de senhas, industry standard                          |
| **class-validator** | 0.14.x     | Validação de DTOs, integração com NestJS                      |
| **Swagger/OpenAPI** | 3.x        | Documentação automática, geração de tipos                     |

### 4.3. Infraestrutura e Ferramentas

| Tecnologia         | Versão    | Justificativa                                                  |
| ------------------ | --------- | -------------------------------------------------------------- |
| **GitHub Actions** | Latest    | CI/CD gratuito para repos públicos/privados pequenos           |
| **Docker**         | 24.x      | Containers para dev/prod, consistência de ambiente             |
| **Docker Compose** | 2.x       | Orquestração local (app + DB + cache)                          |
| **Resend**         | Free tier | Envio de emails (recuperação de senha), 3000 emails/mês grátis |
| **Mailhog**        | Latest    | SMTP local para desenvolvimento, FOSS                          |
| **SonarQube**      | Community | Análise de código, métricas de qualidade, gratuito             |
| **ESLint**         | 8.x       | Linting de código, regras customizáveis                        |
| **Prettier**       | 3.x       | Formatação automática, consistência de estilo                  |
| **Husky**          | 9.x       | Git hooks, rodar lint/test antes de commit                     |
| **Jest**           | 29.x      | Testes unitários, integração com NestJS e React                |

---

## 🗺️ 5. ARTEFATOS A SEREM GERADOS

Com base nesta especificação final, os próximos artefatos serão:

### 5.1. Diagrama de Casos de Uso (UML)

**Escopo:** 14 requisitos funcionais organizados em 4 atores:

- **Usuário Não Autenticado:** Cadastro, Login, Recuperação de Senha
- **Usuário Autenticado:** CRUD de Listas, Comparação, Exportação, Perfil
- **Sistema:** Seed de Dados, Validações, Cache
- **Admin:** (Fora do escopo do MVP)

**Entregável:** Diagrama visual mostrando relações entre atores e casos de uso.

### 5.2. Diagrama de Transição de Estados (UML)

**Escopo:** 3 máquinas de estado críticas:

1. **Autenticação:** Idle → Loading → Success/Error → Redirect
2. **Lista de Compras:** Draft → Saved → Comparing → Compared → Exporting
3. **Recuperação de Senha:** Request → Email Sent → Token Validated → Password Reset

**Entregável:** Diagramas mostrando transições válidas, gatilhos e estados finais.

### 5.3. DER - Diagrama Entidade-Relacionamento

**Escopo:** 6 tabelas principais aplicando ACID:

- **users:** id, username, name, email, password_hash, created_at, updated_at
- **lists:** id, user_id, name, created_at, updated_at, deleted_at (soft delete)
- **list_items:** id, list_id, product_id, quantity, created_at
- **suppliers:** id, name, cnpj, created_at
- **products:** id, name, category, unit, created_at
- **prices:** id, supplier_id, product_id, price, valid_from, valid_until

**Entregável:** DER com cardinalidades, constraints (PK, FK, UNIQUE), índices.

### 5.4. Protótipo de Baixa Fidelidade

**Escopo:** 8 telas principais contemplando todo fluxo do MVP:

1. **Login/Cadastro** (tela única com tabs)
2. **Recuperação de Senha** (2 telas: solicitar + resetar)
3. **Dashboard** (lista de listas do usuário)
4. **Criar/Editar Lista** (formulário + tabela de itens)
5. **Comparação de Fornecedores** (tabela com resultados)
6. **Perfil do Usuário** (visualizar/editar dados)
7. **Modal de Confirmação** (exclusão de lista)
8. **View de Impressão** (otimizada para Ctrl+P)

**Entregável:** Wireframes em Figma/Excalidraw com navegação entre telas.

---

## 📅 6. CRONOGRAMA ESTIMADO (MVP)

| Fase                             | Duração                 | Entregáveis                                                                                                   |
| -------------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Fase 1: Setup e Infra**        | 3 dias                  | - Repositórios GitHub<br- Docker Compose (app + DB)<br- CI/CD básico (lint + test)<br- Seed de dados          |
| **Fase 2: Backend Core**         | 10 dias                 | - Auth (cadastro, login, logout, recovery)<br- CRUD de listas<br- Motor de comparação<br- OpenAPI documentado |
| **Fase 3: Frontend Core**        | 10 dias                 | - Telas de auth<br- Dashboard + CRUD de listas<br- Tela de comparação<br- Exportação CSV + impressão          |
| **Fase 4: Testes e Refinamento** | 5 dias                  | - Testes unitários (80% cobertura)<br- Ajustes de UI/UX<br- Performance tuning<br- Bug fixes                  |
| **Fase 5: Deploy e Validação**   | 2 dias                  | - Deploy em staging<br- Validação com stakeholders<br- Ajustes finais<br- Documentação de uso                 |
| **TOTAL**                        | **30 dias (6 semanas)** | **MVP funcional e validado**                                                                                  |

---

## ✅ 7. CRITÉRIOS DE SUCESSO DO MVP

O MVP será considerado **bem-sucedido** se:

1. ✅ **Funcionalidade Core:** Usuário consegue criar lista, comparar fornecedores e ver melhor oferta
2. ✅ **Usabilidade:** Fluxo completo (cadastro → comparação) em <5 minutos
3. ✅ **Performance:** Tempo de resposta <500ms em 95% das requisições
4. ✅ **Qualidade:** Cobertura de testes >80%, zero bugs críticos
5. ✅ **Segurança:** Zero vulnerabilidades críticas (OWASP Top 10)
6. ✅ **Stakeholder Approval:** Feedback positivo dos stakeholders na demo final

---

## 🚀 8. PRÓXIMOS PASSOS

### Imediato (Próxima Semana)

1. **Aprovação desta especificação** por stakeholders
2. **Geração dos artefatos UML** (Casos de Uso, Transição de Estados, DER)
3. **Protótipo de baixa fidelidade** no Figma
4. **Setup inicial dos repositórios** (frontend + backend + infra)

### Curto Prazo (Semanas 2-6)

1. **Desenvolvimento iterativo** em sprints de 1 semana
2. **Demos semanais** para stakeholders (feedback contínuo)
3. **Testes unitários** a cada feature implementada
4. **Deploy em staging** na semana 5

### Pós-MVP (Futuro)

- Integração com LLMs para importação de listas por texto livre
- Web scraping de preços em tempo real
- App mobile (React Native)
- Roteirização logística (distância até fornecedores)
- Processamento de pagamentos

---

## 📞 9. CONTATO E GOVERNANÇA

~~**Product Owner:** [Nome do Stakeholder]
**Tech Lead:** [Nome do Desenvolvedor Sênior]
**Arquiteto de Software:** [Nome do Arquiteto]
**Scrum Master:** [Nome do SM]~~

**Rituais:**

- ~~Daily Standup: 15min, 19:00~~
- Sprint Planning: 1h, toda sexta-feira
- Sprint Review: 15min, toda sexta-feira
- Retrospectiva: 30min toda sexta-feira

**Canais de Comunicação:**

- WhatsApp: [#COBECO-MVP](https://chat.whatsapp.com/LV33cRZKwFAAoaPljTcvLx)
- Email: TBD
- Documentação: [Github](https://github.com/leonardosetti/COBECO)

---

## 📝 10. APÊNDICES

### Apêndice A: Glossário de Termos

- **MVP:** Minimum Viable Product (Produto Viável Mínimo)
- **SDD:** Specification-Driven Development (Desenvolvimento Orientado a Especificação)
- **ACID:** Atomicity, Consistency, Isolation, Durability (propriedades de transações DB)
- **KISS:** Keep It Simple, Stupid (princípio de simplicidade)
- **FOSS:** Free and Open Source Software (Software Livre e de Código Aberto)

### Apêndice B: Referências

- Clean Architecture (Robert C. Martin)
- The Pragmatic Programmer (David Thomas, Andrew Hunt)
- Domain-Driven Design (Eric Evans)
- OpenAPI Specification 3.0

### Apêndice C: Licenças e Compliance

- Todas as tecnologias utilizadas são FOSS ou possuem free tiers adequados
- Resend: Free tier (3000 emails/mês)
- GitHub Actions: Free para repos públicos, 2000 min/mês para privados
- PostgreSQL, Node.js, React: Licenças MIT/Apache

---

**FIM DO RELATÓRIO**

**Próxima Ação:** Aprovação desta especificação e início da geração dos artefatos UML + protótipo de baixa fidelidade.
