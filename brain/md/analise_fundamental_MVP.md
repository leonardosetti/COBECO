# 📊 ANÁLISE FUNDAMENTAL DO MVP COBECO v2.1

## _Documento Fonte da Verdade — Single Source of Truth (SSOT)_

**Versão:** 2.1 (Refinamento de Requisitos)  
**Data:** 01 de Setembro de 2026  
**Status:** ✅ **APROVADO — Fonte Primária de Verdade**  
**Classificação:** Artefato de Governança de Produto  
**Próxima Revisão:** Após validação do protótipo de alta fidelidade

---

## 🎯 1. PROPÓSITO DO DOCUMENTO

Este documento consolida **todas as decisões estratégicas, arquiteturais e de produto** do MVP COBECO (Comparador de Compras), servindo como **única fonte autoritativa** para:

- ✅ Equipe de desenvolvimento (frontend, backend, QA)
- ✅ Stakeholders e Product Owner
- ✅ Novos integrantes do time (onboarding)
- ✅ Auditorias técnicas e de produto
- ✅ Resolução de conflitos entre artefatos

### 📌 Princípio Fundamental

> **"Em caso de divergência entre qualquer artefato do projeto e este documento, este prevalece. Qualquer alteração deve passar por governança formal registrada aqui."**

---

## 🏛️ 2. HIERARQUIA DE FONTES DE VERDADE

### 2.1. Pirâmide de Autoridade

| Nível          | Artefato                                      | Autoridade                | Uso                                             |
| -------------- | --------------------------------------------- | ------------------------- | ----------------------------------------------- |
| **🥇 Nível 1** | **Este documento (Análise Fundamental v2.1)** | **SSOT — Fonte Primária** | Decisões estratégicas, princípios, governança   |
| **🥈 Nível 2** | `Report_Espec_MVP.md` (v2.1)                  | Fonte Especificativa      | Requisitos funcionais/não funcionais detalhados |
| **🥉 Nível 3** | `Analise_de_Consistencia_UCD.md` (v2.1)       | Fonte Complementar        | Casos de uso, atores, relações UML              |
| **🏅 Nível 4** | `casos_de_uso_v0.2.xml`                       | Fonte Visual              | Diagrama UML (representação gráfica)            |
| **📎 Nível 5** | Protótipos, wireframes, PRs                   | Fonte Implementativa      | Execução técnica                                |

### 2.2. Regra de Resolução de Conflitos

```
Se [artefato X] contradiz [artefato Y]:
  → Consultar Nível hierárquico
  → Nível menor prevalece
  → Se mesmo nível: este documento (Nível 1) decide
  → Registrar alteração via PR com link para esta seção
```

---

## 📜 3. EVOLUÇÃO HISTÓRICA DAS DECISÕES

### 3.1. Mudanças Estruturais Consolidadas

| Fase                             | Decisão Original (v1.0)                     | Decisão Final (v2.1)                             | Impacto                                              | Status           |
| -------------------------------- | ------------------------------------------- | ------------------------------------------------ | ---------------------------------------------------- | ---------------- |
| **Autenticação**                 | ❌ Sem cadastro/login (dados efêmeros)      | ✅ Cadastro, login, logout, recuperação de senha | +5 dias dev · Essencial para usabilidade             | ✅ Consolidado   |
| **Persistência**                 | ❌ LocalStorage apenas                      | ✅ PostgreSQL com ACID + histórico               | +3 dias · Alto valor para usuário                    | ✅ Consolidado   |
| **Motor de Paridade**            | Agrupamento complexo por cobertura idêntica | ✅ Tabela flat simplificada                      | -3 dias · Mantém 80% do valor                        | ✅ Consolidado   |
| **Exportação**                   | CSV, JSON, PDF                              | ✅ Apenas CSV + impressão via navegador          | -2 dias · Elimina dependência                        | ✅ Consolidado   |
| **Testes**                       | BDD + E2E + Unitários                       | ✅ Apenas unitários críticos + CI básico         | -3 dias · Foco em qualidade essencial                | ✅ Consolidado   |
| **Validação de Email**           | Envio de link real via Resend (cadastro)    | ✅ Validação de formato apenas no cadastro       | -2 dias · Recuperação de senha ainda usa email       | ✅ Consolidado   |
| **Seleção de Fornecedores** ⭐   | ❌ Comparação automática de todos           | ✅ Usuário seleciona mínimo 2 fornecedores       | +0.5 dia · Princípio Nielsen #3 (controle/liberdade) | ✅ **NOVO v2.1** |
| **Filtro de Disponibilidade** ⭐ | ❌ Ausente                                  | ✅ Slider 0-100% para filtrar fornecedores       | +0.5 dia · UX aprimorada                             | ✅ **NOVO v2.1** |

### 3.2. Linha do Tempo de Versões

```
v1.0 (25/08/2026) → Documento original com 14 RFs
  ↓
v2.0 (31/08/2026) → Adição de autenticação + persistência (14 RFs mantidos)
  ↓
v2.1 (01/09/2026) → Refinamento crítico: seleção de fornecedores (16 RFs)
  ↓
v3.0 (previsto)   → Pós-MVP com LLMs, scraping, mobile
```

---

## 🔍 4. INCONSISTÊNCIAS IDENTIFICADAS E RESOLVIDAS

### 4.1. Matriz de Correções Aplicadas

| Documento Legado                   | Inconsistência                              | Correção Aplicada                                | Status       |
| ---------------------------------- | ------------------------------------------- | ------------------------------------------------ | ------------ |
| `_old_Projeto Cotação...`          | RF21: "Não reter dados do usuário"          | ❌ **DESCARTADO** — MVP atual persiste listas    | ✅ Resolvido |
| `_old_objetivos.md`                | RNF20: "Alpine.js ou Vue.js"                | ⚠️ **SUBSTITUÍDO** — React + TypeScript definido | ✅ Resolvido |
| `Analise_de_Consistencia_UCD` (v1) | UC14 "Limpar Sessão Local" removido         | ✅ **CORRETO** — dados persistidos no DB         | ✅ Resolvido |
| `README.md` (antigo)               | Menciona "BDD + E2E" completos              | ❌ **ATUALIZAR** — MVP usa apenas unitários      | ✅ Resolvido |
| `Report_Espec_MVP.md` (v2.0)       | Ausência de RF para seleção de fornecedores | ✅ **ADICIONADO** — RF11 e RF12 em v2.1          | ✅ Resolvido |
| `casos_de_uso_v0.2.xml`            | UC13 sem pré-requisito de seleção           | ✅ **ATUALIZAR** — UC25/UC26 como pré-requisito  | ⏳ Pendente  |

### 4.2. Princípio de Resolução

> **Todo artefato legado que contradiz a v2.1 deve ser considerado obsoleto.**  
> A equipe deve abrir PR de atualização referenciando este documento.

---

## 🎯 5. DECISÕES ESTRATÉGICAS FINAIS (SSOT)

### 5.1. Fonte Primária: `Report_Espec_MVP.md` (v2.1)

| Domínio                          | Decisão Consolidada                    | Justificativa                                  |
| -------------------------------- | -------------------------------------- | ---------------------------------------------- |
| **Motor de Paridade**            | Tabela flat simplificada               | Complexidade reduzida, 80% do valor mantido    |
| **Validação de Email**           | Formato apenas no cadastro             | Elimina dependência externa no onboarding      |
| **Recuperação de Senha**         | Email real via Resend                  | Essencial para segurança do usuário            |
| **Exportação**                   | CSV + impressão (sem PDF)              | Pragmático, elimina dependência de bibliotecas |
| **Testes**                       | Unitários críticos + CI básico         | Foco em qualidade essencial, sem BDD/E2E       |
| **Seleção de Fornecedores** ⭐   | Mínimo 2, máximo 10, sessão temporária | Princípio Nielsen #3 (controle e liberdade)    |
| **Filtro de Disponibilidade** ⭐ | Slider 0-100%, tempo real              | UX aprimorada, sem persistência                |

### 5.2. Fonte Complementar: `Analise_de_Consistencia_UCD.md` (v2.1)

| Aspecto                    | Definição Consolidada                                              |
| -------------------------- | ------------------------------------------------------------------ |
| **Total de Casos de Uso**  | 26 (18 principais + 8 internos)                                    |
| **Atores**                 | 4: Usuário Não Autenticado, Usuário Autenticado, Sistema, API Mock |
| **Relações `<<include>>`** | 9 relações mapeadas                                                |
| **Relações `<<extend>>`**  | 5 relações mapeadas                                                |
| **Novos UCs v2.1**         | UC25 (Selecionar Fornecedores), UC26 (Filtrar por Disponibilidade) |

---

## 🏗️ 6. PRINCÍPIOS ARQUITETURAIS INEGOCIÁVEIS

### 6.1. Princípios de Produto

| #      | Princípio                                        | Aplicação Prática                                        |
| ------ | ------------------------------------------------ | -------------------------------------------------------- |
| **P1** | **Desktop-First**                                | Layout exclusivo para ≥1024px, sem responsividade mobile |
| **P2** | **Controle e Liberdade do Usuário** (Nielsen #3) | Seleção de fornecedores, filtros, undo/redo              |
| **P3** | **Simplicidade Pragmática** (KISS)               | Tabela flat > agrupamento complexo                       |
| **P4** | **Persistência Confiável**                       | PostgreSQL ACID, nunca LocalStorage                      |
| **P5** | **Segurança por Padrão**                         | bcrypt, JWT, rate limiting, CSP headers                  |

### 6.2. Princípios Técnicos

| #      | Princípio                              | Guard-Rail                                 |
| ------ | -------------------------------------- | ------------------------------------------ |
| **T1** | Clean Architecture                     | Domain → UseCase → Adapter → Framework     |
| **T2** | Specification-Driven Development (SDD) | OpenAPI antes de implementar               |
| **T3** | Type-Safety End-to-End                 | TypeScript strict em frontend + backend    |
| **T4** | Testabilidade                          | Cobertura mínima 80% em casos críticos     |
| **T5** | Observabilidade                        | Logs estruturados, métricas de performance |

---

## 🚧 7. RESTRIÇÕES E LIMITAÇÕES (FORA DO ESCOPO MVP)

### 7.1. Explicitamente Excluído

| Item                             | Justificativa                    | Quando Será Considerado |
| -------------------------------- | -------------------------------- | ----------------------- |
| 📱 Apps móveis (iOS/Android/PWA) | Foco em desktop-first            | v3.0 (pós-MVP)          |
| 🤖 Integração com LLMs           | Complexidade alta, valor incerto | v3.0                    |
| 🕷️ Web scraping em tempo real    | Dependência externa frágil       | v3.0                    |
| 💳 Processamento de pagamentos   | Fora do core do produto          | v4.0+                   |
| 🗺️ Roteirização logística        | Não essencial para comparação    | v3.0                    |
| 📄 Geração de PDF nativo         | Impressão via navegador basta    | v3.0                    |
| 🧪 BDD/E2E tests                 | Overkill para MVP                | v3.0                    |
| 🌐 Multi-idioma (i18n)           | Português brasileiro apenas      | v3.0                    |

### 7.2. Restrições Técnicas

| Restrição                   | Limite           | Motivo           |
| --------------------------- | ---------------- | ---------------- |
| Fornecedores por comparação | 2-10             | Performance + UX |
| Itens por lista             | 1-9999 por item  | Limite prático   |
| Tempo de resposta API       | <500ms (p95)     | UX aceitável     |
| Bundle size frontend        | <500KB gzipped   | Performance      |
| Emails Resend/mês           | 3000 (free tier) | Custo zero       |

---

## 🔐 8. GOVERNANÇA DE MUDANÇAS

### 8.1. Processo de Alteração deste Documento

```
1. Identificação de necessidade de mudança
   ↓
2. Abertura de PR no repositório oficial
   ↓
3. Análise de impacto (técnico + produto)
   ↓
4. Aprovação: Product Owner + Tech Lead
   ↓
5. Merge + atualização de versão
   ↓
6. Comunicação à equipe (Slack/Daily)
```

### 8.2. Critérios de Aceitação para Mudanças

- ✅ Alinhamento com objetivo do MVP (validação de proposta de valor)
- ✅ Impacto temporal justificável (<5 dias de dev)
- ✅ Não viola princípios inegociáveis (Seção 6)
- ✅ Rastreabilidade completa (RF → RNF → UC)
- ✅ Testabilidade garantida

### 8.3. Registro de Mudanças (Change Log)

| Versão   | Data           | Mudança                              | Autor      | PR       |
| -------- | -------------- | ------------------------------------ | ---------- | -------- |
| v1.0     | 25/08/2026     | Documento inicial (14 RFs)           | Equipe     | #001     |
| v2.0     | 31/08/2026     | Adição autenticação + persistência   | Equipe     | #015     |
| **v2.1** | **01/09/2026** | **RF11-12: Seleção de fornecedores** | **Equipe** | **#023** |

---

## 📚 9. GLOSSÁRIO DE TERMOS-CHAVE

| Termo                    | Definição Oficial                                                            |
| ------------------------ | ---------------------------------------------------------------------------- |
| **COBECO**               | Nome do produto: **CO**mparador de **BE**nefícios de **CO**mpras             |
| **MVP**                  | Minimum Viable Product — versão mínima para validar proposta de valor        |
| **SSOT**                 | Single Source of Truth — fonte única de verdade                              |
| **SDD**                  | Specification-Driven Development — desenvolvimento orientado a especificação |
| **ACID**                 | Atomicity, Consistency, Isolation, Durability — propriedades transacionais   |
| **Guard-Rails**          | Limites de segurança que previnem erros do usuário/sistema                   |
| **Tabela Flat**          | Estrutura comparativa simples (fornecedor × métricas), sem agrupamentos      |
| **Sessão de Comparação** | Período temporário onde seleção de fornecedores é mantida (não persistida)   |
| **Seed**                 | Script de popularização inicial do banco com dados de teste                  |

---

## ✅ 10. CHECKLIST DE VALIDAÇÃO DO MVP

### 10.1. Critérios de Sucesso (Go/No-Go)

| #   | Critério               | Métrica                                         | Status Atual               |
| --- | ---------------------- | ----------------------------------------------- | -------------------------- |
| 1   | Funcionalidade Core    | Usuário cria lista → compara → vê melhor oferta | ✅ Definido (RF06-14)      |
| 2   | Usabilidade            | Fluxo completo <5 minutos                       | ✅ Definido (RNF04-06)     |
| 3   | Performance            | API <500ms p95                                  | ✅ Definido (RNF10)        |
| 4   | Qualidade              | Cobertura testes >80%                           | ✅ Definido (RNF07)        |
| 5   | Segurança              | Zero vulnerabilidades OWASP Top 10              | ✅ Definido (RNF11-13)     |
| 6   | Controle do Usuário ⭐ | Seleção de fornecedores funcional               | ✅ **NOVO v2.1** (RF11-12) |

### 10.2. Definição de "Pronto" (DoD)

Uma feature está **PRONTA** quando:

- ✅ Código revisado e aprovado (PR mergeado)
- ✅ Testes unitários passando (>80% cobertura)
- ✅ Documentação atualizada (este documento se aplicável)
- ✅ Deploy em staging validado
- ✅ Feedback do Product Owner coletado
- ✅ Sem bugs críticos ou bloqueantes

---

## 📎 11. ARTEFATOS RELACIONADOS

| Artefato                               | Versão | Localização            | Status                    |
| -------------------------------------- | ------ | ---------------------- | ------------------------- |
| `Report_Espec_MVP.md`                  | v2.1   | `/docs/especificacao/` | ✅ Aprovado               |
| `Analise_de_Consistencia_UCD.md`       | v2.1   | `/docs/uml/`           | ✅ Aprovado               |
| `casos_de_uso_v0.2.xml`                | v2.1   | `/docs/diagrams/`      | ⏳ Atualizar UC25/26      |
| Protótipo Baixa Fidelidade             | v2.1   | `/design/wireframes/`  | ⏳ Atualizar tela seleção |
| DER (Diagrama Entidade-Relacionamento) | v1.0   | `/docs/db/`            | ✅ Aprovado               |
| OpenAPI Spec                           | v2.1   | `/api/docs/`           | ⏳ Gerar com RF11-12      |

---

## 🚀 12. PRÓXIMOS PASSOS IMEDIATOS

### Prioridade P0 (Esta Semana)

1. ✅ **Aprovação deste documento** como SSOT
2. ⏳ **Atualizar `casos_de_uso_v0.2.xml`** com UC25 e UC26
3. ⏳ **Atualizar protótipo de baixa fidelidade** com tela de seleção de fornecedores
4. ⏳ **Implementar RF11-12** (seleção + filtro de fornecedores)

### Prioridade P1 (Próximas 2 Semanas)

5. ⏳ **Desenvolver motor de comparação** (RF13-14) usando seleção
6. ⏳ **Implementar exportação** (RF15-16)
7. ⏳ **Testes unitários** dos novos requisitos

### Prioridade P2 (Pós-MVP)

8. ⏳ **Planejar v3.0** com LLMs, scraping, mobile
9. ⏳ **Coletar feedback** de usuários reais
10. ⏳ **Métricas de produto** (retenção, conversão, NPS)

---

## 📝 13. CONTATO E GOVERNANÇA

| Papel                        | Responsável               | Canal                      |
| ---------------------------- | ------------------------- | -------------------------- |
| **Product Owner**            | [A definir]               | Slack: `#cobeco-product`   |
| **Tech Lead**                | [A definir]               | Slack: `#cobeco-tech`      |
| **Arquiteto de Software**    | [A define]                | Slack: `#cobeco-arch`      |
| **Guardião deste Documento** | Tech Lead + PO (conjunto) | PRs no repositório oficial |

**Repositório Oficial:** [github.com/leonardosetti/COBECO](https://github.com/leonardosetti/COBECO)  
**Canal de Decisões:** WhatsApp `#COBECO-MVP`  
**Documentação:** Branch `main` do repositório

---

## 🏁 DECLARAÇÃO FINAL

> **Este documento representa a verdade consolidada sobre o MVP COBECO em 01 de Setembro de 2026.**  
> **Todas as decisões estratégicas, arquiteturais e de produto estão aqui registradas.**  
> **Qualquer divergência deve ser resolvida consultando esta fonte primária.**  
> **Mudanças futuras devem seguir o processo de governança definido na Seção 8.**

---

**Fim do Documento**  
**Versão:** 2.1 · **Data:** 01/09/2026 · **Status:** ✅ APROVADO  
**Próxima Revisão Programada:** Após validação do protótipo de alta fidelidade

---

# Seção Histórico

## 📊 ANÁLISE DA FUNDAMENTAÇÃO DO MVP

### **Evolução Histórica das Decisões**

| Fase                   | Decisão Original                            | Decisão Final                                    | Impacto                                           |
| ---------------------- | ------------------------------------------- | ------------------------------------------------ | ------------------------------------------------- |
| **Autenticação**       | ❌ Sem cadastro/login (dados efêmeros)      | ✅ Cadastro, login, logout, recuperação de senha | +5 dias de dev, mas essencial para usabilidade    |
| **Persistência**       | ❌ LocalStorage apenas                      | ✅ PostgreSQL com ACID + histórico               | +3 dias, valor alto para usuário                  |
| **Motor de Paridade**  | Agrupamento complexo por cobertura idêntica | Tabela flat simplificada                         | -3 dias, mantém 80% do valor                      |
| **Exportação**         | CSV, JSON, PDF                              | Apenas CSV + impressão via navegador             | -2 dias, elimina dependência                      |
| **Testes**             | BDD + E2E + Unitários                       | Apenas unitários críticos + CI básico            | -3 dias, foco em qualidade essencial              |
| **Validação de Email** | Envio de link real via Resend               | Validação de formato apenas (MVP)                | -2 dias, mas recuperação de senha ainda usa email |

### **Inconsistências Identificadas**

| Documento                     | Inconsistência                      | Correção Aplicada                                |
| ----------------------------- | ----------------------------------- | ------------------------------------------------ |
| `_old_Projeto Cotação...`     | RF21: "Não reter dados do usuário"  | ❌ Conflitante com MVP atual que persiste listas |
| `_old_objetivos.md`           | RNF20: "Alpine.js ou Vue.js"        | ⚠️ Report_Espec define React + TypeScript        |
| `Analise_de_Consistencia_UCD` | UC14 "Limpar Sessão Local" removido | ✅ Correto, dados agora são persistidos          |
| `README.md`                   | Menciona "BDD + E2E" completos      | ❌ MVP simplificado usa apenas unitários         |

### **Decisões Estratégicas Finais (Fontes de Verdade)**

**✅ Report_Espec_MVP.md (v2.0) - Fonte Primária:**

- Motor de paridade simplificado (tabela flat)
- Validação de email por formato (sem envio de link no cadastro)
- Recuperação de senha via email (Resend)
- Exportação: CSV + impressão (sem PDF)
- Testes: unitários críticos + CI básico (sem BDD/E2E)

**✅ Analise_de_Consistencia_UCD.md - Fonte Complementar:**

- 24 casos de uso definidos (18 principais + 6 internos)
- 4 atores: Usuário Não Autenticado, Usuário Autenticado, Sistema, API Mock
- Relações <<include>> e <<extend>> mapeadas

---

**Última atualização:** 31 de Agosto de 2026
