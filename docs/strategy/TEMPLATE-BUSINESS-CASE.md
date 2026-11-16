# Business Case — <NOME DO PROJETO> (Versão Acadêmica)

**Versão:** 1.0  
**Status:** Rascunho | Aprovado | Arquivado  
**Data:** DD/MM/AAAA  
**Autor:** <Nome> (Product Owner)  
**Relacionado:** `docs/strategy/PROJECT-CHARTER.md`

---

## 1. Sumário Executivo

<Descreva em 2-3 parágrafos: o problema, a solução proposta, os benefícios principais e o investimento necessário.>

---

## 2. Contexto e Problema

### 2.1 Situação Atual
<Como as coisas funcionam hoje? Quais as dores, gaps, ineficiências?>

### 2.2 Oportunidade de Melhoria
<O que pode ser ganho resolvendo este problema?>

### 2.3 Consequências de Não Fazer
<O que acontece se o projeto não for realizado? Riscos de status quo.>

---

## 3. Análise de Alternativas

| Alternativa | Descrição | Prós | Contras | Custo Estimado | Tempo | Recomendação |
|-------------|-----------|------|---------|----------------|-------|--------------|
| A - <Nome> | <Descrição> | | | | | ☐ Escolhida |
| B - <Nome> | <Descrição> | | | | | ☐ |
| C - Status Quo | Manter como está | | | R$ 0 | 0 | ☐ |

**Alternativa Escolhida:** <A/B/C> — <Justificativa>

---

## 4. Benefícios Esperados

### 4.1 Benefícios Quantificáveis (Tangíveis)
| Benefício | Métrica | Valor Atual | Valor Alvo | Ganho | Como Medir |
|-----------|---------|-------------|------------|-------|------------|
| <Ex.: Tempo de comparação de preços> | Minutos | 30 min | 5 min | -83% | Cronômetro em teste de usabilidade |

### 4.2 Benefícios Qualitativos (Intangíveis)
| Benefício | Descrição | Stakeholder Impactado |
|-----------|-----------|----------------------|
| <Ex.: Aprendizado de Clean Architecture> | Equipe aplica padrões profissionais | Devs |
| <Ex.: Portfólio acadêmico> | Projeto real para currículo | Alunos |

---

## 5. Investimento Necessário

### 5.1 Recursos Humanos
| Papel | Qtd | Dedicação | Custo (Horas) | Observação |
|-------|-----|-----------|---------------|------------|
| Product Owner | 1 | 20% | ~60h | Aluno |
| Tech Lead | 1 | 50% | ~150h | Aluno |
| Dev Backend | 2 | 100% | ~600h | Alunos |
| Dev Frontend | 1 | 100% | ~300h | Aluno |
| QA | 1 (compartilhado) | 30% | ~90h | Aluno |

**Total Horas Estimadas:** ~1.200h (equipe de 5, 30 dias)

### 5.2 Infraestrutura e Ferramentas
| Item | Custo | Modelo |
|------|-------|--------|
| GitHub (repo + Actions + Projects) | Gratuito | Free tier |
| Docker Hub (imagens) | Gratuito | Free tier |
| MySQL (local/container) | Gratuito | FOSS |
| Domínio/SSL | Gratuito | Não necessário (localhost) |

**Investimento Financeiro Total: R$ 0,00**

---

## 6. Análise Financeira (Simplificada - Acadêmica)

| Métrica | Valor | Observação |
|---------|-------|------------|
| **ROI Financeiro** | N/A | Projeto sem receita direta |
| **Payback** | N/A | Não aplicável |
| **Valor Agregado (EVM)** | Acompanhar via Sprint Review | Velocity, Burndown |
| **Custo por Sprint** | ~240h / sprint | 5 pessoas × 6 dias × 8h |

> **Nota:** Por ser projeto acadêmico sem fins lucrativos, a análise foca em **valor educacional**, **entrega no prazo** e **qualidade técnica** como proxies de retorno.

---

## 7. Riscos Financeiros e de Cronograma

| Risco | Impacto no Cronograma | Impacto no "Orçamento" (Horas) | Mitigação |
|-------|----------------------|--------------------------------|-----------|
| Atraso na Sprint 1 (Setup) | +3 a 5 dias | +120h | Parallelizar setup + docs |
| Baixa cobertura de testes | Rework na Sprint 5 | +80h | TDD desde Sprint 1 |
| Integração Front↔Back falha | +2 dias | +40h | Contrato OpenAPI primeiro (SDD) |
| Membro da equipe indisponível | +5 a 10 dias | +200h | Pair programming, bus factor 2 |

---

## 8. Cronograma de Realização de Benefícios

| Benefício | Quando Começa a Ser Realizado | Como Validar |
|-----------|-------------------------------|--------------|
| Aprendizado técnico | Sprint 1 (Setup) | Code review, retro |
| Software funcionando | Sprint 3 (Comparação) | Demo interna |
| Demo para banca | Sprint 5 (Final) | Apresentação oficial |
| Portfólio público | Pós-projeto | GitHub público + doc-readme-0001-readme-canon |

---

## 9. Aprovação

| Papel | Nome | Assinatura | Data | Decisão |
|-------|------|------------|------|---------|
| CCB Chair / PO | | | | ☐ Aprovar ☐ Rejeitar |
| Tech Lead | | | | ☐ Aprovar ☐ Rejeitar |
| Orientador Acadêmico | | | | ☐ Aprovar ☐ Rejeitar |

---

## 10. Controle de Versões

| Versão | Data | Autor | Mudança |
|--------|------|-------|---------|
| 1.0 | DD/MM/AAAA | <Nome> | Criação inicial |

---

**Fim do Business Case**  
*Versão acadêmica simplificada — foco em valor educacional e entrega técnica.*