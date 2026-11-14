# Matriz de Rastreabilidade — <NOME DO PROJETO>

**Versão:** 1.0  
**Data:** DD/MM/AAAA  
**Responsável:** QA Lead / Arquiteto  
**Frequência de Atualização:** A cada Sprint Review + toda CR ratificada  
**Objetivo:** Garantir que 100% dos RFs têm Spec + Test + Code + Deploy, e nada foi adicionado sem aprovação (Gold Plating)

---

## Matriz Consolidada RF → UC → Spec → Test → Code → Deploy

| RF ID | Descrição RF | UC ID | User Story ID | Spec ID | Handoff ID | Test Unit ID | Test E2E ID | Branch / PR | Status | Deploy Tag |
|-------|--------------|-------|---------------|---------|------------|--------------|-------------|-------------|--------|------------|
| RF01 | Cadastrar Usuário | UC09 | doc-user-story-0001-us-001 | spec-004 | hf-exec-0500 | test_cadastrar_usuario.py | test_auth_flow.py | `feat/UC-09-cadastrar-usuario` | ☐ | v0.1.0 |
| RF02 | Login JWT | UC10 | doc-user-story-0002-us-002 | spec-004 | hf-exec-0500 | test_login_jwt.py | test_auth_flow.py | `feat/UC-10-login-jwt` | ☐ | v0.1.0 |
| RF03 | Logout | UC11 | doc-user-story-0003-us-003 | spec-004 | hf-exec-0500 | test_logout.py | test_auth_flow.py | `feat/UC-11-logout` | ☐ | v0.1.0 |
| RF04 | Recuperar Senha | UC12 | doc-user-story-0004-us-004 | spec-004 | hf-exec-0500 | test_recuperar_senha.py | test_auth_flow.py | `feat/UC-12-recuperar-senha` | ☐ | v0.1.0 |
| RF05 | Visualizar Perfil | UC18 | doc-user-story-0005-us-005 | spec-004 | HF-XXXX | test_visualizar_perfil.py | test_perfil_flow.py | `feat/UC-18-visualizar-perfil` | ☐ | v0.1.0 |
| RF06 | Gerenciar Perfil | UC16 | doc-user-story-0006-us-006 | spec-004 | HF-XXXX | test_gerenciar_perfil.py | test_perfil_flow.py | `feat/UC-16-gerenciar-perfil` | ☐ | v0.1.0 |
| RF07 | Criar Lista + Autocomplete | UC01, UC02 | doc-user-story-0007-us-007, doc-user-story-0008-us-008 | spec-008 | HF-XXXX | test_autocomplete.py, test_lista_memoria.py | test_lista_flow.py | `feat/UC-01-lista-memoria`, `feat/UC-02-autocomplete` | ☐ | v0.1.0 |
| RF08 | Salvar / Promover Lista | UC14, UC17 | doc-user-story-0009-us-009, doc-user-story-0010-us-010 | spec-004 | HF-XXXX | test_salvar_lista.py, test_promover_lista.py | test_lista_flow.py | `feat/UC-14-salvar-lista`, `feat/UC-17-promover-lista` | ☐ | v0.1.0 |
| RF09 | Listar Minhas Listas | UC15 | doc-user-story-0011-us-011 | spec-004 | HF-XXXX | test_listar_listas.py | test_lista_flow.py | `feat/UC-15-listar-listas` | ☐ | v0.1.0 |
| RF10 | Editar Lista | UC13 | doc-user-story-0012-us-012 | spec-004 | HF-XXXX | test_editar_lista.py | test_lista_flow.py | `feat/UC-13-editar-excluir-lista` | ☐ | v0.1.0 |
| RF11 | Excluir Lista | UC13 | doc-user-story-0013-us-013 | spec-004 | HF-XXXX | test_excluir_lista.py | test_lista_flow.py | `feat/UC-13-editar-excluir-lista` | ☐ | v0.1.0 |
| RF12 | Selecionar Categorias | UC03 | doc-user-story-0014-us-014 | spec-008 | HF-XXXX | test_categorias.py | test_comparacao_flow.py | `feat/UC-03-categorias` | ☐ | v0.1.0 |
| RF13 | Selecionar Fornecedores | UC04 | doc-user-story-0015-us-015 | spec-008 | HF-XXXX | test_fornecedores.py | test_comparacao_flow.py | `feat/UC-04-fornecedores` | ☐ | v0.1.0 |
| RF14 | Filtrar Disponibilidade | UC05 | doc-user-story-0016-us-016 | spec-008 | HF-XXXX | test_disponibilidade.py | test_comparacao_flow.py | `feat/UC-05-disponibilidade` | ☐ | v0.1.0 |
| RF15 | Calcular Orçamento | UC06 | doc-user-story-0017-us-017 | spec-004 | HF-XXXX | test_calcular_orcamento.py | test_comparacao_flow.py | `feat/UC-06-calcular-orcamento` | ☐ | v0.1.0 |
| RF16 | Visualizar Resultados | UC07 | doc-user-story-0018-us-018 | spec-008 | HF-XXXX | test_visualizar_resultados.py | test_comparacao_flow.py | `feat/UC-07-visualizar-resultados` | ☐ | v0.1.0 |
| RF17 | Exportar PDF | UC08/UC29 | doc-user-story-0019-us-019 | spec-004 | HF-XXXX | test_export_pdf.py | test_export_flow.py | `feat/UC-08-export-pdf` | ☐ | v0.1.0 |
| RF18 | Otimização Impressão | UC09 | doc-user-story-0020-us-020 | spec-008 | HF-XXXX | test_print_css.py | test_export_flow.py | `feat/UC-09-imprimir` | ☐ | v0.1.0 |

---

## Verificações de Completude (Checklist de Rastreabilidade)

| Verificação | Critério | Status | Evidência |
|-------------|----------|--------|-----------|
| **Cobertura RF → Spec** | 100% dos 18 RFs têm pelo menos 1 Spec | ☐ Sim ☐ Não | Contar linhas acima |
| **Cobertura Spec → Test** | 100% das Specs têm testes unitários mapeados | ☐ Sim ☐ Não | Conferir coluna Test Unit ID |
| **Cobertura RF → Test E2E** | 100% dos RFs cobertos por pelo menos 1 E2E | ☐ Sim ☐ Não | Conferir coluna Test E2E ID |
| **Cobertura Spec → Handoff** | 100% das Specs ratificadas têm Handoff | ☐ Sim ☐ Não | Conferir coluna Handoff ID |
| **Cobertura Branch → PR** | 100% das branches têm PR com CI verde | ☐ Sim ☐ Não | GitHub Projects |
| **Cobertura PR → Deploy** | 100% dos PRs merged estão na tag de release | ☐ Sim ☐ Não | GitHub Releases |
| **Ausência Gold Plating** | Nenhum código sem RF/UC/Spec correspondente | ☐ Sim ☐ Não | Auditoria `git log --grep` |
| **Rastreabilidade Bidirecional** | Do código consegue achar o RF original | ☐ Sim ☐ Não | `git log --oneline --grep="RF"` |

---

## Rastreabilidade de Não-Funcionais (RNF)

| RNF ID | Descrição | Spec Relacionada | Testes de Validação | Métrica Alvo | Status |
|--------|-----------|------------------|---------------------|--------------|--------|
| RNF01 | Disponibilidade 99,5% | spec-006, spec-011 | Chaos engineering (futuro) | Uptime | ☐ |
| RNF02 | OpenAPI atualizado | spec-013 | CI check `/docs` | 100% endpoints | ☐ |
| RNF03 | MySQL InnoDB ACID | spec-005, ADR-001 | Migration + seed test | Zero erros | ☐ |
| RNF04 | Desktop-first ≥1024px | spec-008 | Testes visuais Playwright | 0 regressões | ☐ |
| RNF05 | Feedback Visual | spec-008 | E2E + manual | Toast/skeleton/modal | ☐ |
| RNF06 | Cobertura ≥ 80% | spec-006, spec-009 | `pytest --cov-fail-under=80` | ≥ 80% | ☐ |
| RNF07 | CI < 5 min | spec-011 | GitHub Actions timer | < 300s | ☐ |
| RNF08 | Seed < 10s | spec-016 | Script benchmark | < 10s | ☐ |
| RNF09 | Segurança Auth | spec-004 | Testes auth + rate limit | 6 tent/15min | ☐ |
| RNF10 | LGPD (dados sintéticos) | Constitution Art. 3.5 | Auditoria DB | 0 PII real | ☐ |
| RNF11 | PDF < 5s (100 itens) | spec-004 | Benchmark ReportLab | < 5s | ☐ |
| RNF12 | MySQL InnoDB obrigatório | ADR-001, spec-005 | Migration check | Engine=InnoDB | ☐ |

---

## Rastreabilidade de Mudanças (CR Impact Analysis)

| CR ID | Título | RFs Impactados | Specs Atualizadas | Testes Adicionados | Aprovado | Deploy Tag |
|-------|--------|----------------|-------------------|-------------------|----------|------------|
| CR-001 | Quality Board Público | — (novo RD) | Nova spec | Novos testes | ☐ Pendente | — |

---

## Controle de Versões da Matriz

| Versão | Data | Autor | Mudança | Aprovado por |
|--------|------|-------|---------|--------------|
| 1.0 | DD/MM/AAAA | QA Lead | Criação inicial baseada no PRD v1.0 | CCB (Gate 2) |
| 1.1 | DD/MM/AAAA | QA Lead | Atualização pós-Sprint 2 | Tech Lead |

---

**Fim da Matriz de Rastreabilidade**  
*Esta matriz é documento vivo — atualizada a cada Sprint Review e toda CR ratificada. Versão no Git.*