---
id: ai-specs-tap
title: TAP COBECO — linha de base v3 (congelada)
type: spec
version: 1.0.0
status: ratificado
owner: agent-project-analyst
ratified_by: gh-sig:owner:leonardosetti:14863508
ratified_at: '2026-11-16T04:58:00-03:00'
derived-from:
- .ai/specs/tap.md (adequado à norma em 2026-11-05)
last-revised: '2026-11-16'
lgpd-class: n/a
tags:
- specs
- docs
- adequado-a-norma
- ratificado-ccb-001
---

# TAP COBECO — Linha de Base Congelada (espelho do plano-integral)

## 1. Regime (congelamento e emenda controlada)

- **Status ontológico:** o TAP v3 (autorizado em 18/09/2026) está em regime de *freeze* desde o início do planejamento: "não é revisado, reversionado ou corrigido ao longo do ciclo", por força da Premissa P9 (plano-integral:10, 23/ADR-005-freeze.md). O TAP autoriza o projeto, não integra a EAP e não é objeto de ciclos PDCA (plano-integral:10; plano-integral:116 — P9).
- **Precedência intra-TAP:** em divergência entre seções do TAP, "a seção §6 Marcos é canônica para matéria temporal e de marcos" (ADR-005-freeze.md:28; eco em plano-integral:89).
- **Emenda controlada:** a ADR-013 instituiu o Regime de Emenda Controlada (ADR-013:24-28) e foi posteriormente incorporada integralmente na **ADR-005 v1.1.0** (ADR-013:5; ADR-005-regime-tap.md:54). Núcleo blindado, intocável sem Emenda MAJOR + CCB: "Objeto, objetivos SMART, justificativa, orçamento-teto (R$ 0,00) e a estrutura macro da EAP (12 fases / 37 pacotes)" (ADR-005-regime-tap.md:27). Toda emenda pontual registra-se em `docs/tap/delta-v3.1.md` (delta-v3.1.md:3-10; ADR-005-regime-tap.md:31-36).
- **Natureza deste artefato:** este arquivo é **ESPELHO** (transcrição P-08 rígido), não fonte. **Fonte viva única = plano-integral-tap-1-2-3-4-5.md** (KB-INDEX:32 — "fonte canônica: plano-integral-tap-1-2-3-4-5.md"; KB-INDEX:51 — "TAP integral vivo reside no plano-integral"). `docs/tap/TAP.md` é stub (KB-INDEX:32) e `docs/tap/TAP.docx` é export derivado (kb-taxonomy.md:51,67).
- **Resolução de divergência:** em caso de divergência entre este espelho e o plano-integral, **o plano-integral vence** e aqui registra-se `UNKNOWN - verify`. Divergências contra o regime de emendas (delta-v3.1) seguem o Delta Log como leitura operacional vigente, sem alteração textual da baseline (delta-v3.1.md:3).
- **Imutabilidade pós-escrita:** `docs/decisoes/ADR-011-Ecossistema-SDDAI.md:56` classifica `.ai/specs/*.md` como "Specs imutáveis... Once written, never modified without new version file" (transcrito em MANIFEST.md §5.2). Alterações futuras neste arquivo = novo arquivo de versão, não edição in-place.
- **LGPD:** este espelho transcreve apenas nomes/papéis de governança já públicos no TAP acadêmico (plano-integral:4, 16-28); nenhuma agenda de dados pessoais é especificada aqui.
- **Nota de execução (2026-11-03):** o MANIFEST:101 registrava `tap.md` (0 B); no momento desta task o arquivo inexistia no diretório `.ai/specs/` (nem como 0 B). TA-0063 cria-o no caminho pinned, sem rename (MANIFEST:101, §5.1).

## 2. Contexto e origem

- Origem: task TA-0063 / handoff hf-exec-0619 (action: spec), item A.2 de `docs/analise/LISTA-SPECS-PENDENTES-2026-11-02.md:26` — "Restaurar `.ai/specs/tap.md` (0 B) como baseline de escopo TAP da camada 5, transcrevendo o TAP v3 em regime de congelamento que sobrevive em `plano-integral-tap-1-2-3-4-5.md` e no PDF... Entregável: espelho não vazio da linha de base congelada."
- O TAP original (artefato autorizativo) perdeu-se como arquivo editável (G-08; OKB-C-08 — LISTA:25-26); seu conteúdo sobrevive reproduzido "de maneira integral e não subnumerada" na Introdução do plano-integral (plano-integral:10) e em `docs/tap/TAP.docx` (binário, 18/09/2026 — docs/tap/). Esta rodada transcreve exclusivamente do plano-integral (fonte viva única, hf-exec-0619:17,23); o DOCX binário não é transcrita aqui.
- Cobertura declarada da reprodução TAP no plano-integral: "identificação, objetivos, justificativa, EAP com 12 fases e 37 pacotes, 15 requisitos, 4 marcos + milestone auxiliar, 9 premissas e 7 categorias de restrição" (plano-integral:660).

## 3. Resolução de conflitos (divergências registradas)

| # | Tema | Leitura A (baseline congelada) | Leitura B (regime vigente) | Fonte vencedora | Registro |
|---|---|---|---|---|---|
| 1 | Data-alvo do marco M2 | 30/09/2026 (plano-integral:96, 194, 272, 442) | 15/11/2026 — emenda CR-001 + ADR-015, registrada no Delta Log (delta-v3.1.md:10; ADR-005-regime-tap.md:36,55) | Delta Log para leitura operacional; baseline textual permanece 30/09 (plano-integral ainda não reflete a emenda na Tabela 4) | `UNKNOWN - verify` — consolidação da Tabela 4 do plano-integral pós-emenda é matéria de custódia PM |
| 2 | REQ-07 (cache de cotações) | SQLite (plano-integral:77, 325) | PostgreSQL 15+ — emenda ADR-010, registrada no Delta Log (delta-v3.1.md:9; ADR-013:36; ADR-005-regime-tap.md:35) | Delta Log para leitura operacional; baseline textual permanece SQLite | `UNKNOWN - verify` — idem |
| 3 | Status da ADR-013-a | KB-INDEX:62 lista ADR-013-a como "ratified... supersedes ADR-005 parcialmente" | ADR-013 declara-se "SUPERSSEDIDA... incorporada integralmente na ADR-005 v1.1.0" (ADR-013:5; ADR-005-regime-tap.md:54) | ADR-005-regime-tap.md (v1.1.0, ratificada — ADR-005-regime-tap.md:6,46) | `UNKNOWN - verify` — atualização do KB-INDEX é matéria do CCB (também colisão de ID OKB-C-26, KB-INDEX:20,62-63) |
| 4 | Regime ADR-005 citado pelo KB-INDEX | KB-INDEX:48 aponta ADR-005 = `ADR-005-freeze.md` v1.0.0 (freeze absoluto) | Versão vigente é ADR-005 v1.1.0 = `ADR-005-regime-tap.md` (freeze + emenda controlada) | ADR-005-regime-tap.md:74-75 (histórico v1.0.0 → v1.1.0) | `UNKNOWN - verify` — idem CCB |
| 5 | Estado de `docs/tap/TAP.md` | KB-INDEX:32 declara "stub-ponteiro (não-0B, CCB F-06 TA-0016)" | Arquivo com 0 B no disco (verificação 2026-11-03, `wc -c`) | Observação direta do disco | `UNKNOWN - verify` — correção do caveat é matéria do owner agent-pm / CCB |
| 6 | Caminho do plano-integral | KB-INDEX:33 cita `docs/planos/plano-integral-tap-1-2-3-4-5.md` | Arquivo real em `docs/planos/plano-granular/plano-integral-tap-1-2-3-4-5.md` (o caminho sem `plano-granular/` não existe no disco) | Observação direta do disco | `UNKNOWN - verify` — relocalização humana unstaged já registrada em MANIFEST §7 |
| 7 | Data da decisão ADR-005 | 21/09/2026 (ADR-005-freeze.md:7,16) | 18/09/2026 "decisão original" (ADR-005-regime-tap.md:7); ADR-013 frontmatter 2026-11-01 vs instrumento 31/10 (OKB-C-28, KB-INDEX:62) | `UNKNOWN - verify` — data efetiva depende de ratificação CCB (ADR-005-freeze.md:6) | `UNKNOWN - verify` |

Nenhuma divergência acima foi "resolvida" por reescrita do espelho: a transcrição das §§4-15 segue o plano-integral (fonte viva única) e as emendas do Delta Log aparecem somente nesta tabela e na §10, como leitura operacional (delta-v3.1.md:3).

## 4. Identificação do projeto (TAP — Tabela 1 da fonte)

Transcrição integral de plano-integral:16-28 ("Tabela 1 — Identificação do projeto"):

| Campo | Descrição |
| --- | --- |
| Projeto | COBECO — Conversor de Ganhos em Moeda Estrangeira |
| Instituição | Fatec Taquaritinga — Curso Superior de Tecnologia em Análise e Desenvolvimento de Sistemas |
| Disciplina | Gerência de Projetos |
| Gerente de Projeto | Leonardo David Silva Setti |
| Equipe | Leonardo David Silva Setti, Fabricio de Lima Cabral, Edson Luis Silva |
| Stakeholder-Avaliador | Prof. Dr. Nivaldo Carleto |
| Data de autorização do TAP | 18/09/2026 (versão 3 — regime de *freeze*) |

Fonte: plano-integral:20-26 (tabela), :28 ("Elaborado pelos autores (2026)"), :4 (cabeçalho institdoc-arch-0006-uc-v1ional integral).

## 5. Objeto e autorização

Transcrição de trechos do parágrafo de autorização (plano-integral:12; parágrafo integral na fonte):

- "O projeto COBECO — Conversor de Ganhos em Moeda Estrangeira — é autorizado formalmente por este termo, conferindo-lhe existência oficial perante a instituição de ensino (Fatec Taquaritinga) e perante o professor orientador da disciplina de Gerência de Projetos, Prof. Dr. Nivaldo Carleto." (plano-integral:12)
- "Concede-se autoridade formal ao aluno Leonardo David Silva Setti, no papel de gerente do projeto, para aplicar os recursos organizacionais, planejar as atividades, tomar decisões e mobilizar os recursos necessários à execução do projeto" (plano-integral:12)
- "Definem-se, ainda, os limites preliminares do projeto, incluindo escopo de alto nível, premissas, restrições, riscos iniciais, cronograma de marcos e orçamento preliminar; identificam-se as principais partes interessadas e seus papéis; e institui-se este termo como documento de referência ao longo de todo o ciclo de vida do projeto." (plano-integral:12)
- Governança declarada no TAP §1.c: PMBOK® 7ª (primária), PMBOK® 6ª (dicionário complementar), Kanban via GitHub Projects (execução) (plano-integral:4, 144; Tabela 7 em plano-integral:146-154).
- CCB: o GP é "decisor operacional único e Change Control Board (CCB) de membro único", autoridade delegada pelo TAP (§1.b, §9 P7) (plano-integral:165, 246).

## 6. Justificativa (TAP)

Transcrição de trechos do parágrafo de justificativa (plano-integral:14; parágrafo integral na fonte):

- Contexto: profissionais PJ/freelancer no Brasil prestam serviço a mercados que remuneram em moeda estrangeira (predominantemente USD e EUR), e "a gestão financeira desses ganhos apresenta uma complexidade que as ferramentas atualmente disponíveis no mercado não resolvem de maneira integrada" (plano-integral:14).
- Lacuna: "não há, até o momento, solução única, gratuita e de código aberto que reúna, em um mesmo ambiente, a simulação cambial completa, a comparação entre diferentes regimes de cálculo e a emissão de documentos fiscais e financeiros associados." (plano-integral:14)
- Fundamento FOSS: "A determinação de utilizar exclusivamente tecnologias abertas (*open source*) é valor fundante do projeto, sustentada pelos pilares de transparência e auditabilidade, gratuidade e acessibilidade, sustentabilidade e comunidade, e alinhamento institdoc-arch-0006-uc-v1ional com a eddoc-arch-0006-uc-v1ação pública." (plano-integral:14)

## 7. Objetivos (TAP §3) — lacuna declarada

- O plano-integral reproduz o TAP "integral e não subnumerada" (plano-integral:10, 660): **os cinco Objetivos SMART do TAP §3 não constam como lista numerada no arquivo-fonte**.
- Referências existentes na fonte (sem o texto integral dos objetivos): a verificação dos "cinco Objetivos SMART do TAP §3" integra o encerramento formal do projeto (plano-integral:272); o objetivo SMART de Cronograma (TAP §3, item ii) é discutido na NC-01 (plano-integral:466); critérios de aceite do TAP §3.2 (ex.: coverage ≥ 80%, UAT sem defeitos críticos) regem a qualidade (plano-integral:564); "Critério de Inovação Controlada do TAP §3.2.e" citado (plano-integral:377); condição de fracasso TAP §3.3.e (dependências incompatíveis com FOSS > 30%) citada (plano-integral:535).
- Texto integral e subnumerado dos Objetivos SMART: `UNKNOWN - verify` (única fonte sobrevivente potencial: `docs/tap/TAP.docx`, binário — fora do escopo desta rodada).

## 8. Produtos e entregas — requisitos principais (TAP §5 / §3)

Transcrição integral de plano-integral:67-87 ("Tabela 3 — Requisitos principais das entregas (REQ-01 a REQ-15)"), base de verificação do escopo e da qualidade (plano-integral:65):

| ID | Requisito | Critério de Aceite | Rastreabilidade |
| --- | --- | --- | --- |
| REQ-01 | Simulação de conversão cambial em tempo real (USD/EUR → BRL) | Cotação obtida via API externa com latência ≤ 2s | TAP §3 (Produto) + N5.2 |
| REQ-02 | Suporte a 5 regimes de contratação (hora, dia, semana, mês, valor fixo) | 100% dos regimes operacionais em UAT | TAP §3 (Produto) + N5.1 |
| REQ-03 | Aplicação de encargos financeiros simulados (spread + IOF) | Cálculo auditável com precisão de 2 casas decimais | TAP §3 (Produto) + N5.1 |
| REQ-04 | Emissão de invoice em formato PDF | Geração via WeasyPrint em ≤ 3s por documento | TAP §3 (Produto) + N5.4 |
| REQ-05 | Tempo de resposta da aplicação | ≤ 3s em 95% das requisições (ambiente homologação) | TAP §3 (Produto) + N5.1 |
| REQ-06 | Interface web responsiva (FOSS) | Compatível com Chrome/Firefox/Edge (últimas 2 versões) | TAP §3 (Inovação) + N5.3 |
| REQ-07 | Cache de cotações (SQLite) | Redução de ≥ 50% das chamadas à API externa | Decisão arquitetural documentada + N5.2 |
| REQ-08 | Cobertura de testes automatizados | ≥ 80% do código (unitários + integração via pytest + coverage.py) | TAP §3 (Qualidade) + N6.1 |
| REQ-09 | Testes de aceitação (UAT) | 100% dos fluxos críticos passando, zero defeitos críticos/bloqueantes | TAP §3 (Qualidade) + N6.2 |
| REQ-10 | Aplicação de ferramentas da qualidade (PDCA + Ishikawa 6M) | 12 PDCAs consolidados + diagrama de causa e efeito documentado | TAP §3 (Qualidade) + N6.3 |
| REQ-11 | Pipeline CI funcional | Lint + testes rodando em ≤ 5 min por push | Padrão de integração contínua + N7.1 |
| REQ-12 | ADRs para decisões arquiteturais críticas | Mínimo 3 ADRs registrados (stack, Kanban, métricas) | Política de documentação técnica + N9.1 |
| REQ-13 | Rastreabilidade de prompts SDD | 100% dos prompts catalogados em .ai/handoffs/ | Política de rastreabilidade de prompts + N9.3 |
| REQ-14 | Documentação técnica consolidada | Arquitetura + APIs (OpenAPI) revisadas e aprovadas | TAP §3 (Produto) + N11.1 |
| REQ-15 | Licenciamento 100% FOSS | Todas as dependências com licenças OSI-approved | TAP §3 (Inovação) + N1.5 + N4.4 |

Fonte: plano-integral:71-85 (linhas da tabela), :87 ("conforme TAP §5").

- Divergência ativa sobre REQ-07 (SQLite → PostgreSQL 15+): ver §3 item 2 (delta-v3.1.md:9).
- Fronteira IN/OUT do escopo (derivada no Plano de Escopo §2.3 "com base no TAP §3 e §8", plano-integral:316-331, Tabela 13) não é reproduzida aqui: pertence à custódia do plano de escopo; consulta direta em plano-integral:318-329.

## 9. EAP — linha de base estrutural (TAP §4) — referência compacta

- Linha de base canônica: "nível 0 (raiz), doze fases de nível 1 e trinta e sete pacotes de trabalho de nível 2, agrupados em três macro-fases temporais (MF1 — Fundação, MF2 — Construção, MF3 — Consolidação)" (plano-integral:30); "Total: 12 fases de nível 1 + 37 pacotes de nível 2", conforme TAP §4 (plano-integral:49).
- Macro-fases com contagens da fonte: MF1 — Fundação (6 fases, 20 pacotes), MF2 — Construção (4 fases, 12 pacotes), MF3 — Consolidação (2 fases, 5 pacotes) (plano-integral:62).
- Estrutura por fase (transcrita de plano-integral:36-47, Tabela 2): N1. Iniciação e Planejamento (5 pacotes, MF1); N2. Levantamento de Requisitos (3, MF1); N3. Modelagem e Prototipação (3, MF1); N4. Configuração de Ambiente (4, MF1); N5. Desenvolvimento do Sistema (5, MF2); N6. Garantia da Qualidade (3, MF2); N7. DevOps e CI/CD (1, MF2); N8. Comunicação (2, MF1); N9. Base de Conhecimento (3, MF1); N10. Gestão de Mudanças (3, MF2); N11. Documentação do Projeto (2, MF3); N12. Encerramento (3, MF3). Decomposição completa dos 37 pacotes: plano-integral:36-47.
- Regra de congelamento estrutural: "nenhum pacote de trabalho pode ser adicionado, removido ou renomeado sem aprovação formal via change-request" (plano-integral:362); contagens divergentes (13/48) são voláteis e não canônicas (plano-integral:360, 635 NC-Q4).
- Transcrição integral da EAP (todos os pacotes com rastreabilidade) = custódia de `.ai/specs/eap.md` (EAP-001, item A.3 — LISTA:27); este espelho mantém apenas a referência compacta acima.

## 10. Marcos (TAP §6)

Transcrição integral de plano-integral:91-100 ("Tabela 4 — Marcos do projeto"); em matéria temporal, §6 é canônico intra-TAP (ADR-005-freeze.md:28; plano-integral:89):

| ID | Macro-Fase (EAP) | Descrição do Marco (Entrega de Valor) | Data Alvo | Critério de Aceite |
| --- | --- | --- | --- | --- |
| M1 | MF1: Fundação | Entrega Parcial Documental: aprovação do TAP + Planos de Gerenciamento das Áreas 1 a 5 (Integração, Escopo, Cronograma, Custos, Qualidade) + 12 PDCAs consolidados + Diagrama de Ishikawa | 22/09/2026 | Documentação submetida via GitHub e validada pelo Prof. Dr. Nivaldo Carleto sem achados críticos |
| M2 | MF1: Fundação | Ambiente e Modelagem Concluídos: stack FOSS definida e validada, ambiente local/CI configurado, DER e Protótipo UX/UI aprovados | 30/09/2026 | Pipeline CI "verde" e artefatos de modelagem versionados no repositório |
| M3 | MF2: Construção | MVP Funcional (Beta): código-fonte full-stack operacional (Backend, Frontend, PDF, SDD com IA), com cobertura de testes ≥ 80% e validado em UAT local | 15/11/2026 | Zero defeitos críticos/bloqueantes; métricas de fluxo dentro da baseline |
| M4 | MF3: Consolidação | Encerramento e Aceite Final: documentação técnica consolidada, lições aprendidas, verificação dos critérios SMART e apresentação final com aceite formal | 15/12/2026 | Validação acadêmica pelo Prof. Dr. Nivaldo Carleto no marco M4 e repositório com tag de release final |

Fonte: plano-integral:95-98 (linhas da tabela), :100 ("conforme TAP §6").

- Milestone auxiliar: "Calibração (03/10, auxiliar)" entre M2 e M3; período de calibração 23/09–03/10/2026, "sem substituir o M2" (plano-integral:194, 242).
- **Divergência ativa sobre M2:** emenda de repactuação M2 30/09 → 15/11/2026 (CR-001 + ADR-015; delta-v3.1.md:10) — ver §3 item 1. A tabela acima transcreve a baseline congelada da fonte.

## 11. Premissas (TAP §9)

Transcrição integral de plano-integral:104-118 ("Tabela 5 — Premissas do projeto (TAP §9)"):

| ID | Premissa | Justificativa de Alto Nível |
| --- | --- | --- |
| P1 | Governança híbrida: PMBOK 7ª como base de princípios e domínios, PMBOK 6ª como dicionário complementar, Kanban como método de execução | Alinhamento com as diretrizes acadêmicas da disciplina |
| P2 | Projeto desenvolvido exclusivamente com tecnologias FOSS | Premissa pedagógica e de valor social |
| P3 | Uso de IA Generativa (LLMs) como apoio ao desenvolvimento (SDD) autorizado, com rastreabilidade e revisão humana | Diretrizes acadêmicas atuais de uso ético de IA |
| P4 | Código-fonte funcional (MVP full-stack) constitui deliverable formal | Natureza prática do curso de ADS |
| P5 | Equipe manterá disponibilidade média de até 20 horas semanais por membro | Capacidade realística para projeto acadêmico noturno |
| P6 | Hardware local adequado e suficiente para desenvolvimento, modelagem, testes e execução do MVP | Condição base para desenvolvimento sem nuvem paga |
| P7 | Professor Orientador atua como stakeholder-avaliador único nos marcos (M1 a M4), sem ingerência operacional; CCB delegada ao GP | Simplificação pedagógica e autonomia do GP |
| P8 | Áreas de "Aquisições" e "Gerenciamento das Partes Interessadas" tratadas com simplificação pedagógica | Foco nas 8 áreas restantes |
| P9 | Separação ontológica TAP ≠ EAP ≠ PDCA: o TAP autoriza, não integra a EAP nem é objeto de ciclos PDCA | Preservação do status autorizativo do TAP |

Fonte: plano-integral:108-116 (linhas da tabela), :118 ("conforme TAP §9").

## 12. Restrições (TAP §8 e §11)

Transcrição integral de plano-integral:120-132 ("Tabela 6 — Restrições consolidadas (TAP §8 e §11)"):

| Categoria PMBOK | Restrições Aplicáveis |
| --- | --- |
| Escopo | MVP acadêmico; desenvolvimento do zero |
| Cronograma | 2 bimestres (com ≈ 25% já decorrido); marco 22/09/2026; curso noturno |
| Custo | Orçamento zero; proibição de ferramentas pagas |
| Recursos | Equipe de 3 pessoas (múltiplos papéis); hardware modesto; dependência externa |
| Qualidade | Testes com tempo limitado; ambiente de validação restrito |
| Riscos | Sem plano de contingência formal; APIs gratuitas instáveis |
| Tecnológicas | FOSS/gratuito obrigatório; SDD experimental; licença open source final |

Fonte: plano-integral:124-130 (linhas da tabela), :132 ("conforme TAP §8 e §11").

- Orçamento-teto (TAP §11): "TOTAL R$ 0,00 (linha de base imutável sem CCB)" (plano-integral:512); rubricas RH/Software/Infraestrutura/Reservas todas R$ 0,00 (plano-integral:512). Orçamento-teto é núcleo blindado (ADR-005-regime-tap.md:27).
- Exclusões YAGNI da fronteira (fundadas na restrição TAP §8.1): plano-integral:314.

## 13. Partes interessadas (TAP §7) — lacuna declarada

- Registrados na fonte (reprodução do TAP): Stakeholder-Avaliador Prof. Dr. Nivaldo Carleto (plano-integral:25); Gerente de Projeto e Equipe (plano-integral:23-24); autoridade do GP e vínculo do projeto com o avaliador (plano-integral:12).
- Papéis operacionais de governança (derivação do Plano de Integração §1.2, não do TAP): GP (decisor único/CCB), Desenvolvedores (execução técnica, revisão em pares), Stakeholder-Avaliador (avaliação acadêmica M1–M4, sem ingerência operacional) (plano-integral:165).
- Registro dedicado de partes interessadas do TAP §7 (tabela própria, estratégias de engajamento): **não reproduzido no plano-integral** → `UNKNOWN - verify` (coerente com a simplificação pedagógica da P8, plano-integral:115).

## 14. Riscos de alto nível (TAP §10) — lacuna declarada

- Lista subnumerada R1–R8 do TAP §10 **não consta no plano-integral**; a fonte traz apenas referências fragmentadas:
  - Restrição de riscos: "Sem plano de contingência formal; APIs gratuitas instáveis" (plano-integral:129).
  - R3 do TAP §10 — burnout/WIP (referenciado): plano-integral:192.
  - R2 do TAP §10 — stack FOSS "definida e validada por protótipo" (referenciado): plano-integral:442, 472 (NC-04).
  - Guardrail "R1–R8 do guardrail" monitorados (referência histórica OKB §3): plano-integral:687.
- Texto integral dos riscos R1–R8: `UNKNOWN - verify` (fonte potencial: `docs/tap/TAP.docx`, binário; e plano de riscos das Áreas 6-8, diferido ao M2 — plano-integral:270).

## 15. Critérios de sdoc-arch-0006-uc-v1esso (TAP §3.2) — lacuna declarada

- A lista §3.2 do TAP não é reproduzida de forma subnumerada no plano-integral. Critérios de sdoc-arch-0006-uc-v1esso declarados nos trechos transcritos da fonte:
  - Aceite do escopo: requisitos Must operacionais em UAT; cobertura ≥ 80% validada em CI; zero defeitos críticos/bloqueantes; 100% das dependências com licença OSI-approved; validação acadêmica no M4 (plano-integral:333).
  - Critérios de aceite por marco M1–M4 (Tabela 4): plano-integral:95-98.
  - Verificação dos cinco Objetivos SMART no encerramento (plano-integral:272); critério §3.2.g citado na NC-01 (plano-integral:466); critérios §3.2 regem a hierarquia da qualidade (plano-integral:564).
- Enumeração integral e subnumerada do TAP §3.2: `UNKNOWN - verify`.

## 16. Critérios de aceite e testes (deste artefato)

Derivados de hf-exec-0619:17 e LISTA:26 (nada aqui é critério do TAP):

- [ ] Arquivo não vazio (não-0B) no caminho pinned `.ai/specs/tap.md`, sem rename (MANIFEST:101, §5.1; DoR kb-taxonomy.md:43).
- [ ] Toda seção transcrita (§§4-15) possui citação `arquivo:linha` do plano-integral ou da ADR citada.
- [ ] Zero conteúdo novo: nenhum requisito, valor, data ou métrica que não exista na fonte; lacunas declaradas como `UNKNOWN - verify` (§§7, 13, 14, 15 e §3).
- [ ] Regime de congelamento + fonte viva única declarados no cabeçalho (§1), conforme hf-exec-0619:17.
- [ ] Divergências fonte × regime registradas na §3 (7 itens), sem reescrita da baseline.
- [ ] Nenhum outro arquivo editado nesta task (plano-integral, ADRs, KB-INDEX, delta-v3.1 intocados).
- Validação: agent-reviewer / agent-gatekeeper. DoD desta task: parcela JSON `{"task_id":"TA-0063",...}` com artifacts e todos os checkboxes acima verificáveis (hf-exec-0619:27-29).

## 17. Rastreabilidade

| Seção deste artefato | Fonte (arquivo:linha) |
|---|---|
| §1 Regime | ADR-005-freeze.md:27-30; ADR-005-regime-tap.md:21-36,54; ADR-013:5,24-28; delta-v3.1.md:3-10; KB-INDEX:32,51; MANIFEST §5.1/§5.2; ADR-011:56 (via MANIFEST) |
| §2 Contexto | hf-exec-0619:17,23; LISTA:26; plano-integral:10,660; kb-taxonomy.md:51,67 |
| §3 Conflitos | delta-v3.1.md:9-10; ADR-015 (via delta-v3.1.md:10); ADR-010 (via delta-v3.1.md:9); ADR-013:5,36; ADR-005-regime-tap.md:35-36,54-55,74-75; KB-INDEX:32-33,48,62-63; ADR-005-freeze.md:6-7,16; plano-integral:96,77,325 |
| §4 Identificação | plano-integral:4, 16-28 |
| §5 Objeto/autorização | plano-integral:12, 144-154, 165, 246 |
| §6 Justificativa | plano-integral:14 |
| §7 Objetivos | plano-integral:10,272,377,466,535,564,660 |
| §8 Requisitos | plano-integral:65-87, 318-329 (Tabela 13, ponteiro); delta-v3.1.md:9 |
| §9 EAP | plano-integral:30,36-47,49,62,360,362,635 |
| §10 Marcos | plano-integral:89,91-100,194,242,442; delta-v3.1.md:10 |
| §11 Premissas | plano-integral:104-118 |
| §12 Restrições | plano-integral:120-132, 314, 512; ADR-005-regime-tap.md:27 |
| §13 Partes interessadas | plano-integral:12,23-25,115,165 |
| §14 Riscos | plano-integral:129,192,442,472,687,270 |
| §15 Critérios de sdoc-arch-0006-uc-v1esso | plano-integral:95-98,272,333,466,564 |
| Frontmatter/ID | KB-INDEX:51 (TAP-001, draft, 1.0.0, agent-sdd-specialist); KB-INDEX:32 (canal SDD .ai/specs/tap.md) |

## 18. Fora de escopo (YAGNI)

- Transcrição integral da EAP 12/37 (37 pacotes) → `.ai/specs/eap.md` (EAP-001, A.3 — LISTA:27); aqui apenas referência compacta (§9).
- Transcrição de `docs/tap/TAP.docx` (binário, 389.628 B, 18/09/2026) → não realizada nesta rodada; potencial fonte dos trechos `UNKNOWN - verify` (§§7, 13, 14, 15).
- Criação de requisitos novos ou alteração de REQ-01..15 → `.ai/specs/requisitos.md` (REQ-SPEC-001 — KB-INDEX:53); o espelho não altera a baseline.
- Edição de plano-integral, ADRs, KB-INDEX, delta-v3.1 ou de imutáveis → vedado (MANIFEST §4.2; ADR-011:56).
- Definição de leitura operacional nova (NCs) → locus exclusivo dos planos (ADR-005-freeze.md:29); este espelho não cria NCs.

## 19. CHANGELOG

- **1.0.0 — 2026-11-03 — TA-0063 / hf-exec-0619** (sender: agent-nexus-prime-ultimate): repovoamento do arquivo pinned (ausente no disco; MANIFEST:101 registrou 0 B) como espelho da linha de base TAP v3 em regime de congelamento. Transcrição: identificação, objeto/autorização, justificativa, requisitos REQ-01..15, EAP compacta 12/37, marcos M1–M4 + Calibração, premissas P1–P9, restrições §8/§11, com citações arquivo:linha. Lacunas declaradas `UNKNOWN - verify`: objetivos SMART §3, registro §7 partes interessadas, riscos R1–R8, critérios §3.2 (fonte subnumerada inexistente no plano-integral). Divergências registradas: 7 (§3), destaque para emendas M2 15/11 e REQ-07 PostgreSQL do Delta Log vs baseline textual.

## 20. CAMADAS FUNDAMENTAIS — MAPA (TA-0031)

Adaptado a arquivo pinned (sem `spec_id spec-NNN`; MANIFEST §5.1 — tap.md sem rename):

| Camada | Seção neste artefato | Estado |
|---|---|---|
| (a) Cabeçalho (frontmatter) | frontmatter YAML (id TAP-001; template de documento conforme hf-exec-0619:17) | ✅ |
| (b) Contexto/origem | §2 Contexto e origem | ✅ |
| (c) Resolução de conflitos | §3 Resolução de conflitos (7 divergências; `UNKNOWN - verify` onde aplicável) | ✅ |
| (d) Corpo de decisões/contratos | §§4-15 (transcrição da baseline; lacunas declaradas `UNKNOWN - verify`) | ✅ (parcial por natureza da fonte) |
| (e) Critérios de aceite e testes | §16 Critérios de aceite e testes (deste artefato) | ✅ |
| (f) Rastreabilidade | §17 Rastreabilidade (`arquivo:linha` por seção) | ✅ |
| (g) Fora de escopo (YAGNI) | §18 Fora de escopo (YAGNI) | ✅ |
| (h) Changelog | §19 CHANGELOG | ✅ |
