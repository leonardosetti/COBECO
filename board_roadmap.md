### 1. Configuração do Quadro (Board Settings)

**Colunas (Views):**
1. `📋 Backlog` (Tudo o que está aprovado no SSOT v3.2)
2. `🎯 Sprint Backlog` (Selecionado para a Sprint ativa)
3. `🔨 In Progress` (Branch criada, desenvolvimento em andamento)
4. `👀 Review` (PR aberto, CI verde, aguardando Code Review de outro membro)
5. `✅ Done` (Merge na `main`, critérios de aceite/DoD atendidos)

**Labels (Etiquetas) Obrigatórias:**
*   **Prioridade:** `P0` (Crítico/Bloqueante), `P1` (Alto), `P2` (Médio/Backlog)
*   **Camada:** `frontend` (HTML/Tailwind/JS ES6), `backend` (FastAPI/Pydantic), `database` (MySQL InnoDB), `infra` (Docker/CI), `docs`
*   **Tipo:** `feature`, `bug`, `test`, `chore`

---

### 2. Marcos (Milestones)
*Crie estes 5 Milestones no GitHub com as datas ajustadas a partir de hoje (15/09/2026).*

| Milestone | Descrição | Prazo | RFs Atendidos |
| :--- | :--- | :--- | :--- |
| **S1: Setup, Docs e Auth** | Infra Docker, Schema MySQL, Seed e Autenticação completa + **Entrega da Documentação**. | 20/09/2026 (Dia 6) | RF01, RF02, RF03, RF04 |
| **S2: Listas e Catálogo** | CRUD de listas, persistência ACID, autocomplete e promoção de lista efêmera. | 26/09/2026 (Dia 12) | RF07, RF08, RF09, RF10, RF11 |
| **S3: Pré-filtro e Comparação** | Seleção de categorias (UC03), fornecedores, slider de disponibilidade e motor de cálculo flat. | 02/10/2026 (Dia 18) | RF12, RF13, RF14, RF15, RF16 |
| **S4: Export, Perfil e Polish** | Geração de PDF (ReportLab), impressão A4 (`@media print`), gestão de perfil e feedbacks visuais. | 08/10/2026 (Dia 24) | RF05, RF06, RF17, RF18 |
| **S5: Buffer, QA e Demo** | Cobertura de testes ≥80%, refinamento de performance, docs finais e ensaio da apresentação. | 15/10/2026 (Dia 30) | Todos (QA e Polish) |

---

### 3. Cards de Backlog (Issues) por Sprint
*Crie estas issues e vincule-as ao Milestone correspondente. Use o padrão de branch: `feat/UC-XX-descricao`.*

#### 🏁 Sprint 1: Setup, Docs e Auth (Dias 1-6)
- `[DOCS-P0]` **Finalizar e Entregar Documentação ABNT**  
  *Descrição:* Consolidar PDF com Objetivo, Escopo, RFs/RNFs, Diagrama de Caso de Uso (Mermaid/Draw.io), DER, Protótipos e Stack. Incluir nomes dos 5 integrantes. Prazo: 18/09 às 19h.
- `[INFRA-P0]` **Setup Docker Compose (FastAPI + MySQL InnoDB)**  
  *Descrição:* Criar `docker-compose.yml` com app Python e MySQL 8.0. Configurar `utf8mb4` e `utf8mb4_unicode_ci`.
- `[DB-P0]` **Criar Schema do Banco (8 Tabelas PT-BR)**  
  *Descrição:* Implementar as 8 tabelas (`usuarios`, `listas`, `itens_lista`, `categorias`, `fornecedores`, `fornecedores_categorias`, `produtos`, `fornecedores_produtos`) com FKs, `ON DELETE CASCADE/RESTRICT` e campos `deletado_em`.
- `[DB-P0]` **Implementar Script de Seed (`seed.py`)**  
  *Descrição:* Popular o DB com 11 categorias macro, 10 fornecedores (com relações N:N na pivô), 50 produtos e ~300 preços em <10s.
- `[BACKEND-P0]` **UC09: Cadastrar Usuário (RF01)**  
  *Descrição:* Endpoint + validação Pydantic. Hash bcrypt (salt=12), unicidade de `nome_usuario` e `email`, pergunta de segurança.
- `[BACKEND-P0]` **UC10: Realizar Login com JWT (RF02)**  
  *Descrição:* Access token (15min, memória) + Refresh token (7 dias, cookie `httpOnly`, `SameSite=Strict`). Rate limiting (6 tentativas/15min).
- `[BACKEND-P1]` **UC11: Realizar Logout (RF03)**  
  *Descrição:* Invalidar cookie de refresh e limpar estado no frontend.
- `[BACKEND-P1]` **UC12: Recuperar Senha (RF04)**  
  *Descrição:* Fluxo via pergunta de segurança (hash da resposta) ou token no stdout (`RECOVERY_MODE=log`).

#### 📝 Sprint 2: Listas e Catálogo (Dias 7-12)
- `[FRONTEND-P0]` **UC02: Autocomplete de Produtos (RF07)**  
  *Descrição:* Campo de busca com debounce (300ms). Normalização de acentos e case-insensitive.
- `[FRONTEND-P0]` **UC01: Criar Lista em Memória (RF07)**  
  *Descrição:* Lógica em Vanilla JS para gerenciar estado da lista em `sessionStorage` (soma de quantidades, validação de 1-9999 itens).
- `[BACKEND-P0]` **UC14: Salvar Lista / Persistir (RF08)**  
  *Descrição:* Transação MySQL explícita (`BEGIN`/`COMMIT`) para inserir `listas` e `itens_lista` atomicamente. Validar se categorias foram pré-selecionadas (UC03).
- `[FRONTEND-P0]` **UC17: Promover Lista Efêmera (RF08)**  
  *Descrição:* Modal disparado no login se `sessionStorage` tiver dados. Opção de migrar para o DB ou manter efêmera.
- `[BACKEND-P0]` **UC15: Listar Minhas Listas (RF09)**  
  *Descrição:* Endpoint com paginação (20/página), ordenação por `criado_em DESC` e filtro por nome. Ignorar registros com `deletado_em`.
- `[BACKEND-P1]` **UC13: Editar e Excluir Lista (RF10, RF11)**  
  *Descrição:* Update de nome/itens. Exclusão lógica (soft delete) com confirmação de digitação do nome da lista.

#### 🔄 Sprint 3: Pré-filtro e Comparação (Dias 13-18)
- `[FRONTEND-P0]` **UC03: Selecionar Categorias (Pré-filtro) (RF12)**  
  *Descrição:* Tela inicial com checkboxes das 11 categorias. Filtra dinamicamente a lista de fornecedores disponíveis via API.
- `[FRONTEND-P0]` **UC04: Selecionar Fornecedores (RF13)**  
  *Descrição:* Checkboxes com nome e % de disponibilidade. Bloquear cálculo se < 2 fornecedores selecionados.
- `[FRONTEND-P1]` **UC05: Filtrar por Disponibilidade (RF14)**  
  *Descrição:* Slider 0-100% no frontend. Atualização em tempo real da lista de fornecedores, mantendo seleções válidas.
- `[BACKEND-P0]` **UC06: Calcular Orçamento (RF15)**  
  *Descrição:* Endpoint que recebe lista + fornecedores. Retorna tabela flat (disponíveis, ausentes, preço total). Implementar cache de 5min. Timeout de 10s.
- `[FRONTEND-P0]` **UC07: Visualizar Resultados (RF16)**  
  *Descrição:* Tabela HTML ordenada por preço ASC. Destaque verde (`bg-green-50`) na melhor oferta. Tooltips para itens ausentes ("N/D").

#### 📤 Sprint 4: Exportação, Perfil e Polish (Dias 19-24)
- `[BACKEND-P0]` **UC08/UC29: Exportar Lista em PDF (RF17)**  
  *Descrição:* Endpoint `POST /api/export/pdf` usando ReportLab. Gera PDF A4 server-side. Funciona para visitantes e autenticados. Nome: `lista_YYYYMMDD.pdf`.
- `[FRONTEND-P1]` **UC09: Otimização para Impressão (RF18)**  
  *Descrição:* CSS `@media print`. Ocultar menus/navegação, garantir quebras de página limpas e header repetido em tabelas longas.
- `[BACKEND-P1]` **UC18: Visualizar Perfil (RF05)**  
  *Descrição:* Endpoint e tela exibindo dados (nome de usuário read-only, email, nome, data de criação).
- `[BACKEND-P1]` **UC16: Gerenciar Perfil (RF06)**  
  *Descrição:* Formulário para alterar email, nome e senha (exigir senha atual). Transação ACID para atualizações simultâneas.
- `[FRONTEND-P1]` **UI/UX: Feedback Visual Global (RNF05)**  
  *Descrição:* Implementar componente de Toast (sucesso/erro), estados de loading (skeletons) e modais de confirmação.

#### 🛡️ Sprint 5: Buffer, QA e Demo (Dias 25-30)
- `[TEST-P0]` **Cobertura de Testes Unitários ≥80% (RNF06)**  
  *Descrição:* Testes com `pytest` e `pytest-cov` focados em Domain Rules e UseCases (regras de cálculo, validações de auth).
- `[INFRA-P1]` **Pipeline CI/CD GitHub Actions (RNF07)**  
  *Descrição:* Workflow executando `ruff` (lint), `pytest --cov` e build em <5 minutos.
- `[DOCS-P1]` **Refinar README.md e OpenAPI (RNF02)**  
  *Descrição:* Validar Swagger (`/docs`) gerado pelo FastAPI. Preencher README com instruções de `docker compose up` e arquitetura.
- `[CHORE-P0]` **Preparação da Apresentação Final**  
  *Descrição:* Definir roteiro de 30-35 minutos, dividir falas igualmente entre os 5 integrantes e ensaiar o fluxo "cadastro → comparação → exportação PDF".

---

### 4. Definição de Pronto (Definition of Done - DoD)
*Adicione este checklist no template de Pull Request do repositório:*
- [ ] Código segue Clean Architecture (4 camadas) e não vaza dependências de framework para o Domain.
- [ ] Todas as queries no backend usam *parameterized queries* (proteção contra SQLi).
- [ ] Nomenclatura do banco de dados e variáveis está em PT-BR conforme DER v3.2.
- [ ] Testes unitários foram escritos e a cobertura não diminuiu.
- [ ] O contrato OpenAPI (`/docs`) foi atualizado (SDD).
- [ ] Funciona corretamente via `docker compose up` sem configuração manual extra.

### 5. Próximos Passos Imediatos para o Grupo (Hoje, 15/09)
1. **Leonardo (ou Tech Lead):** Criar o repositório no GitHub, configurar as 5 colunas, os Labels e os 5 Milestones listados acima.
2. **Todos os integrantes:** Criar as Issues listadas na **Sprint 1**, atribuindo o Milestone "S1" e distribuindo os responsáveis (Assignees) entre os 5 membros.
3. **Foco Absoluto até 18/09:** O card `[DOCS-P0]` deve ser movido para `In Progress` imediatamente. Usem o modelo de documento ABNT que forneci na resposta anterior para preencher e gerar o PDF.

Precisa que eu detalhe o checklist de algum card específico (ex: o script de Seed ou a configuração do Docker Compose) para acelerar o trabalho da equipe?