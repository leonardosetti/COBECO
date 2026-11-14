# Test Plan — <Nome da Funcionalidade / Release>

**Documento:** Test Plan / QA Sign-off  
**Versão:** 1.0  
**Status:** Draft | Aprovado | Arquivado  
**Data:** DD/MM/AAAA  
**Autor:** <Nome> (QA / SDET)  
**Release:** <versão> | **Sprint:** S<X>

---

## 1. Objetivo

Validar que os requisitos funcionais e não funcionais atendem aos critérios de aceite antes do deploy.

---

## 2. Estratégia de testes

| Tipo | Ferramenta | Cobertura alvo | Ambiente |
|---|---|---|---|
| Unitário | pytest | ≥ 80% nos módulos tocados | Local / CI |
| Integração | pytest + MySQL | Cenários críticos | Local / CI |
| E2E | Playwright | Fluxo demo (cadastro → comparação → PDF) | Local |

---

## 3. Cenários de teste

| ID | Requisito (RF) | Cenário | Resultado esperado | Status |
|---|---|---|---|---|
| TC-01 | RF01 | Cadastrar usuário com senha válida | Usuário criado, JWT emitido |  |
| TC-02 | RF02 | Login com credenciais corretas | Access token (15m) + refresh cookie |  |
| TC-03 | RF15 | Calcular orçamento com 2+ fornecedores | Tabela flat, preço total |  |
| TC-04 | RF17 | Exportar PDF | `lista_YYYYMMDD.pdf` válido, A4 |  |

---

## 4. Critérios de aceitação (DoD)

- [ ] Testes unitários escritos; cobertura não diminuiu
- [ ] CI verde (`ruff` + `pytest --cov` + `mypy`)
- [ ] E2E verde em `docker compose up`
- [ ] Code review rubrica R-01..R-07 aprovado
- [ ] Aprovação humana do CCB

---

## 5. Rastreabilidade

- **REQUISITOS.md:** RF-XX
- **CASOSDEUSO.md:** UC-YY
- **SPEC:** `.ai/specs/spec-<NNN>.spec.md`
- **Handoff:** `.ai/handoffs/HF-<NNNN>.md`

---

## 6. QA Sign-off

| Papel | Nome | Decisão | Data | Assinatura |
|---|---|---|---|---|
| QA / SDET |  |  |  |  |
| Tech Lead |  |  |  |  |

---

**Fim do Test Plan**
