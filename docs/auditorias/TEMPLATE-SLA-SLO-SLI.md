# SLA / SLO / SLI — COBECO MVP

**Documento:** Acordos de Nível de Serviço  
**Versão:** 1.0  
**Status:** Ativo | Arquivado  
**Data:** DD/MM/AAAA  
**Autor:** <Nome>  
**Contexto:** MVP acadêmico (FATEC Taquaritinga) — não ambiente de produção comercial

---

## 1. SLI (Service Level Indicators)

| Indicador | Definição | Ferramenta de medição |
|---|---|---|
| Disponibilidade | % de tempo com backend respondendo `/health` | Docker + curl |
| Latência p95 | Tempo de resposta da API em 95º percentil | `curl + time` |
| Taxa de erro | % de requisições com código 5xx | Logs do backend |
| Cobertura de testes | % de código coberto por testes | `pytest --cov` |

---

## 2. SLO (Service Level Objectives)

| Objetivo | Alvo | Janela de medição |
|---|---|---|
| Disponibilidade | ≥ 99% (ambiente de desenvolvimento) | Por sprint |
| Latência p95 | < 500 ms (RNF09) | Por requisição |
| Geração de PDF | < 5 s para até 100 itens (RNF11) | Por geração |
| Cobertura de testes | ≥ 80% nos módulos tocados (RNF06) | Por CI run |
| Seed de dados | < 10 s (RNF08) | Por `make seed` |

---

## 3. SLA (Service Level Agreement)

Não aplicável comercialmente (MVP acadêmico, zero cloud, desktop-only). Compromissos internos entre time e CCB:

| Compromisso | Alvo |
|---|---|
| Resposta a incidente | < 4 horas (dias úteis) |
| Correção de bug P0 | < 24 horas |
| Deploy de nova versão | Conforme milestone S1–S5 |

---

## 4. Rastreabilidade

- **REQUISITOS.md:** RNF06, RNF08, RNF09, RNF11
- **Constitution:** Art. 16.3 (SLA / SLO / SLI)
- **CI:** `.github/workflows/ci.yml`

---

**Fim do SLA / SLO / SLI**
