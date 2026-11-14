# User Story — US-<NNN>

**Título:** <Nome da história>  
**ID Único:** US-<NNN> (ex: doc-user-story-0001-us-001)  
**Status:** Backlog | Sprint Backlog | In Progress | Review | Done  
**Sprint:** S<X> | **Milestone:** <nome>  
**Prioridade:** P0 | P1 | P2  
**Story Points:** <1|2|3|5|8|13> (Fibonacci)  
**Autor:** <Nome> (PO)  
**Data Criação:** DD/MM/AAAA  
**Data Atualização:** DD/MM/AAAA  
**Rastreabilidade:** RF-XX, UC-YY, Spec-<NNN>

---

## 1. História (Formato Padrão)

Como **<tipo de usuário>**,  
eu quero **<objetivo/ação>**,  
para **<benefício/valor de negócio>**.

> **Exemplo:**  
> Como **usuário autenticado**,  
> eu quero **criar uma lista de compras com autocomplete de produtos**,  
> para **economizar tempo e evitar erros de digitação**.

---

## 2. Critérios de Aceite — Formato Gherkin (Dado/Quando/Então)

> **Regra:** Todo critério deve ser testável, automático quando possível, e escrito em Gherkin.

### Cenário 1: <Nome do cenário principal>
```gherkin
Dado que <pré-condição / estado inicial>
Quando <ação do usuário / evento>
Então <resultado esperado / validação>
E <resultado adicional se houver>
```

### Cenário 2: <Cenário alternativo / erro>
```gherkin
Dado que <pré-condição>
Quando <ação inválida / caso de borda>
Então <mensagem de erro / comportamento esperado>
E <estado do sistema inalterado>
```

### Cenário 3: <Cenário de integração / borda>
```gherkin
Dado que <condição complexa>
Quando <fluxo completo>
Então <resultado final validado>
```

---

## 3. Critérios de Aceite — Tabela Resumo (para Checklist Rápido)

| # | Critério (Resumo) | Tipo (Func/Non-Func) | Automatizável? | Teste Relacionado | Status |
|---|-------------------|---------------------|----------------|-------------------|--------|
| AC-01 | <Resumo do critério 1> | Funcional | Sim | `test_<nome>.py` | ☐ |
| AC-02 | <Resumo do critério 2> | Funcional | Sim | `test_<nome>.py` | ☐ |
| AC-03 | <Resumo do critério 3> | Não-funcional (perf) | Não | Benchmark manual | ☐ |

---

## 4. Tarefas Técnicas (Tasks) — Decomposição para Sprint

| Task ID | Descrição Técnica | Camada | Estimativa (h) | Responsável | Status | Branch |
|---------|-------------------|--------|----------------|-------------|--------|--------|
| TA-<NNN> | <Ex.: Criar endpoint POST /v1/usuarios com validação Pydantic> | Backend | 4 | Dev Back 1 | ☐ Todo | `feat/UC-09-cadastrar-usuario` |
| TA-<NNN> | <Ex.: Implementar bcrypt hash + unicidade email/usuario> | Backend | 2 | Dev Back 1 | ☐ Todo | `feat/UC-09-cadastrar-usuario` |
| TA-<NNN> | <Ex.: Criar página Cadastro com Vanilla JS + Tailwind> | Frontend | 6 | Dev Front | ☐ Todo | `feat/UC-09-cadastrar-usuario` |

---

## 5. Definição de Pronto (DoD) — Obrigatório para "Done"

- [ ] **Código:** Clean Architecture (4 camadas), sem vazamento de framework para Domain
- [ ] **Segurança:** Queries parameterizadas (SQLi protection), validação Pydantic
- [ ] **Padronização:** Nomenclatura PT-BR (DB, variáveis, comentários, erros)
- [ ] **Testes:** Unitários escritos + cobertura ≥ 80% nos módulos tocados (`pytest --cov`)
- [ ] **Contrato:** OpenAPI (`/docs`) atualizado (SDD — spec → handoff → impl)
- [ ] **Infra:** Funciona via `docker compose up` sem config manual extra
- [ ] **Revisão:** Code review aprovado (rubrica R-01..R-07) + CI verde
- [ ] **Governança:** Aprovação humana (CCB) + merge em `main` → kanban "Done"
- [ ] **Documentação:** Spec/ADR/RFC atualizados se houver decisão arquitetural

---

## 6. Rastreabilidade Bidirecional

| Direção | Artefato | ID / Localização |
|---------|----------|------------------|
| **Origem (Negócio)** | req-func-0001-requisitos-funcionais-canon.md | RF-XX |
| **Origem (Caso de Uso)** | req-use-case-0001-casos-de-uso-canon.md | UC-YY |
| **Especificação (SDD)** | `.ai/specs/spec-<NNN>.spec.md` | Spec ID |
| **Handoff (Execução)** | `.ai/handoffs/HF-<NNNN>.md` | Handoff ID |
| **Implementação** | Branch Git | `feat/UC-XX-descricao` |
| **Testes** | `backend/tests/` + `frontend/tests/e2e/` | Test IDs |
| **Deploy** | Release / Tag | `v<semver>` |

---

## 7. Notas Técnicas / Decisões (Opcional)

<Registre aqui decisões técnicas tomadas durante a implementação que não cabem em ADR/RFC mas são úteis para manutenção futura.>

---

## 8. Controle de Versões da User Story

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | DD/MM/AAAA | PO | Criação inicial | — |
| 1.1 | DD/MM/AAAA | PO | Ajuste critérios após refinamento | Tech Lead |

---

**Fim da User Story US-<NNN>**  
*Uma User Story por arquivo em `docs/strategy/user-stories/US-<NNN>.md` + Issue correspondente no GitHub Projects.*