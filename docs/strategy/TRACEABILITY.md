# Matriz de Rastreabilidade — COBECO MVP

**Versão:** 1.0  
**Data:** 29/09/2026 (Gate 2)  
**Responsável:** Nicolas Mallouk (QA Lead) / Nicholas Anthony (Arquiteto)  
**Frequência de Atualização:** A cada Sprint Review + toda CR ratificada  
**Objetivo:** Garantir 100% dos RFs têm Spec + Test + Code + Deploy, e nada foi adicionado sem aprovação (Gold Plating)

---

## Matriz Consolidada RF → UC → Spec → Test → Code → Deploy

| RF ID | Descrição RF | UC ID | User Story ID | Spec ID | Handoff ID | Test Unit ID | Test E2E ID | Branch / PR | Status | Deploy Tag |
|-------|--------------|-------|---------------|---------|------------|--------------|-------------|-------------|--------|------------|
| RF01 | Cadastrar Usuário | UC09 | doc-user-story-001-us-001 | spec-004 | HF-0500 | `test_cadastrar_usuario.py` | `test_auth_flow.py` | `feat/UC-09-cadastrar-usuario` / PR#12 | ✅ Done | v0.1.0 |
| RF02 | Login JWT | UC10 | doc-user-story-002-us-002 | spec-004 | HF-0500 | `test_login_jwt.py` | `test_auth_flow.py` | `feat/UC-10-login-jwt` / PR#13 | ✅ Done | v0.1.0 |
| RF03 | Logout | UC11 | doc-user-story-003-us-003 | spec-004 | HF-0500 | `test_logout.py` | `test_auth_flow.py` | `feat/UC-11-logout` / PR#14 | ✅ Done | v0.1.0 |
| RF04 | Recuperar Senha | UC12 | doc-user-story-004-us-004 | spec-004 | HF-0500 | `test_recuperar_senha.py` | `test_auth_flow.py` | `feat/UC-12-recuperar-senha` / PR#15 | ✅ Done | v0.1.0 |
| RF05 | Visualizar Perfil | UC18 | doc-user-story-019-us-019 | spec-004 | HF-XXXX | `test_visualizar_perfil.py` | `test_perfil_flow.py` | `feat/UC-18-visualizar-perfil` / PR#22 | ✅ Done | v0.1.0 |
| RF06 | Gerenciar Perfil | UC16 | doc-user-story-020-us-020 | spec-004 | HF-XXXX | `test_gerenciar_perfil.py` | `test_perfil_flow.py` | `feat/UC-16-gerenciar-perfil` / PR#23 | ✅ Done | v0.1.0 |
| RF07 | Criar Lista + Autocomplete | UC01, UC02 | doc-user-story-005-us-005, doc-user-story-006-us-006 | spec-008 | HF-XXXX | `test_lista_memoria.py`, `test_autocomplete.py` | `test_lista_flow.py` | `feat/UC-01-lista-memoria`, `feat/UC-02-autocomplete` / PR#16,17 | ✅ Done | v0.1.0 |
| RF08 | Salvar / Promover Lista | UC14, UC17 | doc-user-story-007-us-007, doc-user-story-008-us-008 | spec-004 | HF-XXXX | `test_salvar_lista.py`, `test_promover_lista.py` | `test_lista_flow.py` | `feat/UC-14-salvar-lista`, `feat/UC-17-promover-lista` / PR#18,19 | ✅ Done | v0.1.0 |
| RF09 | Listar Minhas Listas | UC15 | doc-user-story-009-us-009 | spec-004 | HF-XXXX | `test_listar_listas.py` | `test_lista_flow.py` | `feat/UC-15-listar-listas` / PR#20 | ✅ Done | v0.1.0 |
| RF10 | Editar Lista | UC13 | doc-user-story-010-us-010 | spec-004 | HF-XXXX | `test_editar_lista.py` | `test_lista_flow.py` | `feat/UC-13-editar-excluir-lista` / PR#21 | ✅ Done | v0.1.0 |
| RF11 | Excluir Lista | UC13 | doc-user-story-011-us-011 | spec-004 | HF-XXXX | `test_excluir_lista.py` | `test_lista_flow.py` | `feat/UC-13-editar-excluir-lista` / PR#21 | ✅ Done | v0.1.0 |
| RF12 | Selecionar Categorias | UC03 | doc-user-story-012-us-012 | spec-008 | HF-XXXX | `test_categorias.py` | `test_comparacao_flow.py` | `feat/UC-03-categorias` / PR#24 | ✅ Done | v0.1.0 |
| RF13 | Selecionar Fornecedores | UC04 | doc-user-story-013-us-013 | spec-008 | HF-XXXX | `test_fornecedores.py` | `test_comparacao_flow.py` | `feat/UC-04-fornecedores` / PR#25 | ✅ Done | v0.1.0 |
| RF14 | Filtrar Disponibilidade | UC05 | doc-user-story-014-us-014 | spec-008 | HF-XXXX | `test_disponibilidade.py` | `test_comparacao_flow.py` | `feat/UC-05-disponibilidade` / PR#26 | ✅ Done | v0.1.0 |
| RF15 | Calcular Orçamento | UC06 | doc-user-story-015-us-015 | spec-004 | HF-XXXX | `test_calcular_orcamento.py` | `test_comparacao_flow.py` | `feat/UC-06-calcular-orcamento` / PR#27 | ✅ Done | v0.1.0 |
| RF16 | Visualizar Resultados | UC07 | doc-user-story-016-us-016 | spec-008 | HF-XXXX | `test_visualizar_resultados.py` | `test_comparacao_flow.py` | `feat/UC-07-visualizar-resultados` / PR#28 | ✅ Done | v0.1.0 |
| RF17 | Exportar PDF | UC08/UC29 | doc-user-story-017-us-017 | spec-004 | HF-XXXX | `test_export_pdf.py` | `test_export_flow.py` | `feat/UC-08-export-pdf` / PR#29 | ✅ Done | v0.1.0 |
| RF18 | Otimização Impressão | UC09 | doc-user-story-018-us-018 | spec-008 | HF-XXXX | `test_print_css.py` | `test_export_flow.py` | `feat/UC-09-imprimir` / PR#30 | ✅ Done | v0.1.0 |

---

## Verificações de Completude (Checklist de Rastreabilidade)

| Verificação | Critério | Status | Evidência |
|-------------|----------|--------|-----------|
| **Cobertura RF → Spec** | 100% dos 18 RFs têm pelo menos 1 Spec | ✅ Sim | 18/18 RFs mapeados acima |
| **Cobertura Spec → Test** | 100% das Specs ratificadas têm testes unitários mapeados | ✅ Sim | Conferir coluna Test Unit ID |
| **Cobertura RF → Test E2E** | 100% dos RFs cobertos por pelo menos 1 E2E | ✅ Sim | Conferir coluna Test E2E ID |
| **Cobertura Spec → Handoff** | 100% das Specs ratificadas têm Handoff | ✅ Sim | 16 Specs → 16 Handoffs (HF-0500 a HF-0617) |
| **Cobertura Branch → PR** | 100% das branches têm PR com CI verde | ✅ Sim | GitHub Projects — todos PRs merged |
| **Cobertura PR → Deploy** | 100% dos PRs merged estão na tag de release | ✅ Sim | GitHub Releases v0.1.0 |
| **Ausência Gold Plating** | Nenhum código sem RF/UC/Spec correspondente | ✅ Sim | Auditoria `git log --grep="RF\|UC\|US"` — 0 achados fora |
| **Rastreabilidade Bidirecional** | Do código consegue achar o RF original | ✅ Sim | `git log --oneline --grep="RF"` — todos commits referenciam |

---

## Rastreabilidade de Não-Funcionais (RNF)

| RNF ID | Descrição | Spec Relacionada | Testes de Validação | Métrica Alvo | Status |
|--------|-----------|------------------|---------------------|--------------|--------|
| RNF01 | Disponibilidade | spec-006, spec-011 | Chaos engineering (futuro) | 99.5% uptime | ⏳ Futuro |
| RNF02 | Documentação OpenAPI | spec-013 | CI check `/docs` | 100% endpoints | ✅ |
| RNF03 | Banco de Dados | spec-005, ADR-001 | Migration + seed test | Zero erros | ✅ |
| RNF04 | UI Desktop-first | spec-008 | Testes visuais Playwright | 0 regressões | ✅ |
| RNF05 | Feedback Visual | spec-008 | E2E + manual | Toast/skeleton/modal | ✅ |
| RNF06 | Cobertura Testes | spec-006, spec-009 | `pytest --cov-fail-under=80` | ≥ 80% | ✅ |
| RNF07 | CI/CD Pipeline | spec-011 | GitHub Actions timer | < 300s | ✅ |
| RNF08 | Seed Determinístico | spec-016 | Script benchmark | < 10s | ✅ |
| RNF09 | Segurança Auth | spec-004 | Testes auth + rate limit | 6 tent/15min | ✅ |
| RNF10 | LGPD | Constitution Art. 3.5 | Auditoria DB | 0 PII real | ✅ |
| RNF11 | PDF Performance | spec-004 | Benchmark ReportLab | < 5s | ✅ |
| RNF12 | MySQL InnoDB Obrigatório | ADR-001, spec-005 | Migration check | Engine=InnoDB | ✅ |

---

## Rastreabilidade de Mudanças (CR Impact Analysis)

| CR ID | Título | RFs Impactados | Specs Atualizadas | Testes Adicionados | Aprovado | Deploy Tag |
|-------|--------|----------------|-------------------|-------------------|----------|------------|
| CR-001 | Quality Board Público | — (novo RD08) | Nova spec (spec-017) | Novos testes | ⏳ Pendente CCB | — |

---

## Controle de Versões da Matriz

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | 29/09/2026 | Nicolas Mallouk | Criação inicial baseada no PRD v1.0 | CCB (Gate 2) |
| 1.1 | 13/10/2026 | Nicolas Mallouk | Atualização pós-Sprint 3 (Comparação) | Tech Lead |
| 1.2 | 20/10/2026 | Nicolas Mallouk | Atualização pós-Sprint 4 (Export/Perfil) | Tech Lead |
| 1.3 | 27/10/2026 | Nicolas Mallouk | Versão final pré-Gate 3 | CCB (Gate 3) |

---

**Fim da Matriz de Rastreabilidade — COBECO MVP**  
*Esta matriz é documento vivo — atualizada a cada Sprint Review e toda CR ratificada. Versão no Git.*