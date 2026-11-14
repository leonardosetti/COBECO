# Matriz RACI — <NOME DO PROJETO>

**Versão:** 1.0  
**Data:** DD/MM/AAAA  
**Responsável:** Proddoc-arch-0006-uc-v1t Owner  
**Aprovação:** CCB (Gate 1)  
**Frequência de Revisão:** A cada mudança de escopo ou equipe

---

## Legenda RACI

| Código | Significado | Descrição |
|--------|-------------|-----------|
| **R** | **Responsible** | Quem executa o trabalho ("mão na massa") |
| **A** | **Accountable** | Quem aprova e responde pelo resultado (apenas **UM** por linha) |
| **C** | **Consulted** | Quem dá input antes da decisão/ação (duas vias) |
| **I** | **Informed** | Quem é avisado depois da decisão/ação (uma via) |

---

## Matriz RACI por Entregável/Atividade

| Entregável / Atividade | PO | Tech Lead | Arquiteto | Dev Backend 1 | Dev Backend 2 | Dev Frontend | QA | Orientador |
|------------------------|:--:|:---------:|:---------:|:-------------:|:-------------:|:------------:|:--:|:----------:|
| **Estratégia & Início** |
| Project Charter | A | R | C | I | I | I | I | C |
| Business Case | A | R | C | I | I | I | I | C |
| Stakeholder Register | A | R | I | I | I | I | I | C |
| Matriz RACI (esta) | A | R | C | I | I | I | I | I |
| Roadmap / Milestones | A | R | C | C | C | C | C | I |
| **Planejamento** |
| WBS / EAP | A | R | C | C | C | C | C | I |
| Cronograma (Gantt) | A | R | C | I | I | I | I | I |
| Sprint Planning (cada sprint) | A | R | C | R | R | R | C | I |
| **Produto & Requisitos** |
| PRD | A | C | C | C | C | C | C | I |
| User Stories + Critérios Aceite | A | C | C | C | C | C | R | I |
| Specs (SDD) | I | A | R | R | R | R | C | I |
| Protótipos / Wireframes | A | I | C | I | I | R | C | I |
| Backlog Priorização | A | C | I | C | C | C | I | I |
| **Arquitetura & Engenharia** |
| ADRs | I | A | R | C | C | C | I | I |
| RFCs | I | A | R | C | C | C | I | I |
| Diagramas C4 | I | A | R | C | C | C | I | I |
| Contratos API (OpenAPI) | I | A | R | R | R | C | C | I |
| DER / Dicionário Dados | I | A | R | R | R | I | C | I |
| NFRs | I | A | R | C | C | C | C | I |
| **Controle & Mudanças** |
| CR (Change Request) | A | R | C | C | C | C | C | I |
| RAID Log | A | R | C | C | C | C | R | I |
| Plano de Testes / QA | I | C | C | C | C | C | A/R | I |
| Status Report | A | R | I | I | I | I | I | C |
| **Entrega & Operação** |
| Runbooks | I | A | C | R | R | C | C | I |
| Release Notes | A | R | I | C | C | C | C | I |
| Deploy / Go-Live | I | A | C | R | R | R | C | I |
| Post-Mortem | A | R | R | R | R | R | R | I |
| Termo de Encerramento | A | R | C | I | I | I | I | C |

---

## Regras de Ouro da Matriz

1. **Apenas UM "A" (Accountable)** por linha — quem tem a palavra final
2. **Pelo menos UM "R" (Responsible)** por linha — alguém precisa fazer
3. **Evitar muitos "C"** — consultar demais paralisa; limitar a 2-3 por linha
4. **"I" é ilimitado** — informar não custa caro
5. **Revisar a cada Sprint Planning** — papéis podem mudar

---

## Validação da Matriz

| Verificação | Status | Observação |
|-------------|--------|------------|
| Todas as linhas têm exatamente 1 "A" | ☐ Sim ☐ Não | |
| Todas as linhas têm pelo menos 1 "R" | ☐ Sim ☐ Não | |
| Nenhuma coluna está sobrecarregada (>60% R+A) | ☐ Sim ☐ Não | |
| Stakeholders externos (Orientador) só têm C/I | ☐ Sim ☐ Não | |

---

## Controle de Versões

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | DD/MM/AAAA | <Nome> | Criação inicial | CCB |

---

**Fim da Matriz RACI**  
*Esta matriz vive no repositório (Docs-as-Code) e é versão controlada via Git.*