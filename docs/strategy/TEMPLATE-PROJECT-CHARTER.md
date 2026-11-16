# Project Charter — <NOME DO PROJETO>

**Versão:** 1.0  
**Status:** Rascunho | Aprovado | Arquivado  
**Data de Criação:** DD/MM/AAAA  
**Data de Aprovação:** DD/MM/AAAA  
**Autor:** <Nome> (Product Owner)  
**Aprovadores:** CCB (Change Control Board)

---

## 1. Identificação do Projeto

| Campo | Valor |
|-------|-------|
| **Nome do Projeto** | <Nome> |
| **Código / ID** | <Código único> |
| **Patrocinador** | <Nome / Órgão> |
| **Product Owner** | <Nome> |
| **Tech Lead** | <Nome> |
| **Data de Início Prevista** | DD/MM/AAAA |
| **Data de Término Prevista** | DD/MM/AAAA |
| **Metodologia** | Híbrido (PMBOK 7 + SDD + Scrum) |
| **Constituição Vigente** | `constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-0001-constitution-0001-constitution-canon-0001-constitution-0001-constitution-canon-canon-canon-canon.md` v2.0 |

---

## 2. Justificativa e Objetivos (Business Case Resumido)

### 2.1 Problema / Oportunidade
<Descreva o problema de negócio ou oportunidade que o projeto resolve.>

### 2.2 Objetivos do Projeto (SMART)
| # | Objetivo | Métrica de Sucesso |
|---|----------|-------------------|
| 1 | <Objetivo 1> | <KPI mensurável> |
| 2 | <Objetivo 2> | <KPI mensurável> |
| 3 | <Objetivo 3> | <KPI mensurável> |

### 2.3 Benefícios Esperados
- **Tangíveis:** <ex.: redução de tempo, aumento de receita>
- **Intangíveis:** <ex.: satisfação do usuário, aprendizado da equipe>

---

## 3. Escopo

### 3.1 Dentro do Escopo (In Scope)
- <Entrega 1>
- <Entrega 2>
- <Entrega 3>

### 3.2 Fora do Escopo (Out of Scope)
- <Item explicitamente NÃO incluído>
- <Item explicitamente NÃO incluído>

### 3.3 Requisitos de Alto Nível (RFs Principais)
| ID | Requisito Funcional | Prioridade |
|----|---------------------|------------|
| RF01 | <Descrição> | P0 |
| RF02 | <Descrição> | P0 |

---

## 4. Premissas e Restrições

### 4.1 Premissas (Assumptions)
| # | Premissa | Impacto se Falsa |
|---|----------|------------------|
| A1 | <Premissa> | <Impacto> |
| A2 | <Premissa> | <Impacto> |

### 4.2 Restrições (Constraints)
| # | Restrição | Tipo (Tempo/Custo/Escopo/Qualidade/Recurso) |
|---|-----------|---------------------------------------------|
| C1 | Prazo fixo: 30 dias (5 sprints) | Tempo |
| C2 | Equipe de 5 integrantes | Recurso |
| C3 | Orçamento zero (recursos próprios) | Custo |
| C4 | Stack definida em ADR-001 (FastAPI, MySQL, Vanilla JS) | Tecnologia |
| C5 | Constitution v2.0 como lei suprema | Governança |

---

## 5. Riscos Principais (Top 5)

| ID | Risco | Prob. | Impacto | Exposição | Mitigação |
|----|-------|-------|---------|-----------|-----------|
| R1 | <Risco> | Alta/Média/Baixa | Alto/Médio/Baixo | <Score> | <Ação> |
| R2 | <Risco> | | | | |

---

## 6. Stakeholders Principais

| Nome | Papel | Interesse | Poder | Engajamento Necessário |
|------|-------|-----------|-------|------------------------|
| <Nome> | Product Owner | Alto | Alto | Liderar |
| <Nome> | Tech Lead | Alto | Alto | Decidir técnico |
| <Nome> | Orientador Acadêmico | Alto | Alto | Aprovar marcos |
| <Nome> | Banca Avaliadora | Alto | Alto | Avaliar entrega final |
| <Nome> | Dev Backend | Médio | Baixo | Executar |
| <Nome> | Dev Frontend | Médio | Baixo | Executar |

---

## 7. Estrutura de Governança

### 7.1 Change Control Board (CCB)
| Papel | Nome | Autoridade |
|-------|------|------------|
| Chair / PO | <Nome> | Decisão final de escopo, prazo, orçamento |
| Tech Lead | <Nome> | Viabilidade técnica, arquitetura |
| Arquiteto | <Nome> | Qualidade, NFRs, ADRs |
| QA Lead | <Nome> | Testes, cobertura, release gate |

### 7.2 Gates de Aprovação (Stage Gates)
| Gate | Momento | Critério | Aprovadores |
|------|---------|----------|-------------|
| Gate 1 | Início (Kick-off) | Charter + RACI + ADR-001 ratificados | CCB |
| Gate 2 | Fim Sprint 1 | PRD + User Stories + C4 + NFRs + Test Plan + RAID | CCB |
| Gate 3 | Fim Sprint 5 (Go-Live) | Cobertura ≥80% + Runbooks + Release Notes + Demo | CCB + Orientador |
| Gate 4 | Encerramento | Termo de Encerramento + Lições + Post-Mortem | CCB + Banca |

---

## 8. Orçamento e Recursos

| Recurso | Quantidade | Custo Unitário | Total | Observação |
|---------|------------|----------------|-------|------------|
| Desenvolvedores | 5 | R$ 0,00 | R$ 0,00 | Equipe acadêmica |
| Infraestrutura (GitHub, Docker Hub) | - | Gratuito | R$ 0,00 | Free tier |
| Ferramentas (IDE, DB, CI) | - | Gratuito | R$ 0,00 | FOSS |

**Orçamento Total: R$ 0,00** (Projeto acadêmico sem custo financeiro)

---

## 9. Cronograma Macro (Milestones)

| Milestone | Descrição | Data Prevista | Gate |
|-----------|-----------|---------------|------|
| M1 | Kick-off + Charter + RACI + ADR-001 | DD/MM/AAAA | Gate 1 |
| M2 | Sprint 1: Setup, Docs, Auth | DD/MM/AAAA | — |
| M3 | Sprint 2: Listas e Catálogo | DD/MM/AAAA | — |
| M4 | Sprint 3: Pré-filtro e Comparação | DD/MM/AAAA | — |
| M5 | Sprint 4: Export, Perfil, Polish | DD/MM/AAAA | — |
| M6 | Sprint 5: Buffer, QA, Demo | DD/MM/AAAA | Gate 3 |
| M7 | Apresentação + Encerramento | DD/MM/AAAA | Gate 4 |

---

## 10. Critérios de Sucesso do Projeto

| Critério | Meta | Como Medir |
|----------|------|------------|
| Entrega de todos RFs (18) | 100% | GitHub Projects "Done" + Demo |
| Cobertura de testes | ≥ 80% | `pytest --cov-fail-under=80` |
| Documentação ABNT | Aprovada | Orientador + Banca |
| Deploy funcional | `docker compose up` | Smoke test em staging |
| Apresentação final | Nota ≥ 8,0 | Banca avaliadora |

---

## 11. Aprovação Formal (CCB)

| Papel | Nome | Assinatura | Data | Voto |
|-------|------|------------|------|------|
| **CCB Chair / PO** | | | | ☐ Aprovar ☐ Rejeitar |
| **Tech Lead** | | | | ☐ Aprovar ☐ Rejeitar |
| **Arquiteto** | | | | ☐ Aprovar ☐ Rejeitar |
| **QA Lead** | | | | ☐ Aprovar ☐ Rejeitar |

---

## 12. Controle de Versões

| Versão | Data | Autor | Descrição da Mudança |
|--------|------|-------|----------------------|
| 1.0 | DD/MM/AAAA | <Nome> | Criação inicial |

---

**Fim do Project Charter**  
*Este documento deve ser versionado no Git junto ao código (Docs-as-Code).*