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
