# 📋 Definição de Casos de Uso e Fluxos do MVP COBECO v2.1

Com base nos documentos SSOT (`analise_fundamental_MVP.md`), especificação (`Report_Espec_MVP.md`) e análise de consistência (`Analise_de_Consistencia_UCD.md`), apresento abaixo a definição formal dos casos de uso e 5 fluxos detalhados com happy paths e exceções.

---

## 🎯 1. CATÁLOGO DE CASOS DE USO (26 UCs)

### 1.1 Casos de Uso Principais (18)

| ID       | Caso de Uso                           | Ator                    | RF Relacionado | Descrição Resumida                             |
| -------- | ------------------------------------- | ----------------------- | -------------- | ---------------------------------------------- |
| **UC01** | Cadastrar-se                          | Usuário Não Autenticado | RF01           | Criar nova conta com username, email e senha   |
| **UC02** | Realizar Login                        | Usuário Não Autenticado | RF02           | Autenticar via email/username + senha          |
| **UC03** | Recuperar Senha                       | Usuário Não Autenticado | RF04           | Solicitar reset de senha via email (Resend)    |
| **UC04** | Realizar Logout                       | Usuário Autenticado     | RF03           | Encerrar sessão ativa                          |
| **UC05** | Visualizar Perfil                     | Usuário Autenticado     | RF05           | Ver dados pessoais                             |
| **UC06** | Editar Perfil                         | Usuário Autenticado     | RF05           | Alterar nome/email/senha                       |
| **UC07** | Excluir Conta                         | Usuário Autenticado     | RF05           | Soft delete com confirmação "EXCLUIR"          |
| **UC08** | Criar Lista de Compras                | Usuário Autenticado     | RF06           | Nova lista com nome + itens (produto + qtd)    |
| **UC09** | Listar Minhas Listas                  | Usuário Autenticado     | RF07           | Exibir listas paginadas (20/página)            |
| **UC10** | Editar Lista                          | Usuário Autenticado     | RF08           | Alterar itens, quantidades, nome (draft 30s)   |
| **UC11** | Excluir Lista                         | Usuário Autenticado     | RF09           | Soft delete com confirmação por nome           |
| **UC12** | Buscar Produtos (Autocomplete)        | Usuário Autenticado     | RF10           | Sugestões ao digitar (debounce 300ms)          |
| **UC13** | Calcular Orçamento (Tabela Flat)      | Usuário Autenticado     | RF13           | Gerar comparação dos fornecedores selecionados |
| **UC14** | Visualizar Resultados                 | Usuário Autenticado     | RF14           | Tabela comparativa com melhor oferta destacada |
| **UC15** | Destacar Melhor Oferta                | Usuário Autenticado     | RF14           | Evidenciar linha de menor preço (verde)        |
| **UC16** | Visualizar Itens Disponíveis/Ausentes | Usuário Autenticado     | RF14           | Tooltip com % de disponibilidade               |
| **UC17** | Exportar CSV                          | Usuário Autenticado     | RF15           | Download UTF-8 + BOM, delimitador `;`          |
| **UC18** | Imprimir                              | Usuário Autenticado     | RF16           | `window.print()` com CSS `@media print`        |
| **UC25** | Selecionar Fornecedores ⭐            | Usuário Autenticado     | RF11           | Escolher 2-10 fornecedores (sessão temporária) |
| **UC26** | Filtrar por Disponibilidade ⭐        | Usuário Autenticado     | RF12           | Slider 0-100% para filtrar fornecedores        |

### 1.2 Casos de Uso Internos/Auxiliares (8)

| ID       | Caso de Uso                    | Ator     | Descrição                                     |
| -------- | ------------------------------ | -------- | --------------------------------------------- |
| **UC19** | Validar Dados                  | Sistema  | Validação cross-cutting (Zod/class-validator) |
| **UC20** | Hash de Senha (bcrypt)         | Sistema  | Salt=12 para armazenamento seguro             |
| **UC21** | Gerar Token JWT                | Sistema  | Access (1h) + Refresh (7d httpOnly)           |
| **UC22** | Fornecer Catálogo de Produtos  | API Mock | Seed com 50 produtos                          |
| **UC23** | Fornecer Lista de Fornecedores | API Mock | Seed com 10 fornecedores + % disponibilidade  |
| **UC24** | Fornecer Preços                | API Mock | Preços com variação ±20%                      |
| **UC27** | Aplicar Rate Limiting          | Sistema  | 5 req/15min (auth) · 100 req/min (API)        |
| **UC28** | Invalidar Refresh Token        | Sistema  | Logout e rotação de tokens                    |

### 1.3 Matriz de Relações UML

**Relações `<<include>>` (obrigatórias):**

- UC01 → UC19, UC20 (Cadastro valida + hasheia senha)
- UC02 → UC21, UC27 (Login gera JWT + rate limit)
- UC03 → UC27 (Recuperação sujeita a rate limit)
- UC06 → UC19 (Edição de perfil valida dados)
- UC08, UC10 → UC19 (Listas validam FK de produto)
- UC12 → UC22 (Busca consome catálogo)
- UC13 → UC19, UC23, UC24 (Cálculo valida + busca fornecedores/preços)
- **UC25 → UC23** ⭐ (Seleção consome lista de fornecedores)
- **UC26 → UC25** ⭐ (Filtro opera sobre seleção)

**Relações `<<extend>>` (opcionais):**

- UC15 → UC14 (Destaque é extensão da visualização)
- UC17, UC18 → UC14 (Exportação/Impressão extendem resultados)
- UC06 → UC05 (Edição parte da visualização)
- **UC26 → UC25** ⭐ (Filtro é extensão opcional da seleção)

---

## 🔄 2. CINCO FLUXOS DETALHADOS (Happy Path + Exceções)

### 📌 FLUXO 1 — Cadastro e Login de Usuário

**Cobertura:** UC01, UC02, UC03 | **RFs:** RF01, RF02, RF04 | **RNFs:** RNF11, RNF12, RNF13

#### ✅ Happy Path

```
1. Usuário acessa /register
2. Preenche: username="joao_silva", nome="João Silva",
   email="joao@email.com", senha="Senha@123"
3. Frontend valida (Zod) → onSubmit
4. Backend → UC19 (valida formato) → UC20 (bcrypt salt=12)
5. Prisma INSERT em `users` (constraint UNIQUE username/email)
6. Retorna 201 Created
7. Usuário é redirecionado para /login
8. Faz login → UC21 gera JWT (1h) + refresh httpOnly (7d)
9. Redirecionado para /dashboard
```

#### ⚠️ Exceções Previstas

| #   | Exceção                     | Guard-Rail (RF/RNF)                          | Resposta do Sistema                                                     |
| --- | --------------------------- | -------------------------------------------- | ----------------------------------------------------------------------- |
| E1  | Username já existe          | RF01 + RNF03 (constraint DB)                 | Mensagem genérica: _"Credenciais inválidas"_ (não revela qual campo)    |
| E2  | Senha fraca                 | RF01 (mín 8, 1 maiúsc, 1 número, 1 especial) | Erro inline no campo no `onBlur` (RNF06)                                |
| E3  | 6ª tentativa de login falha | RF02 + RNF13 (5 req/15min por IP)            | HTTP 429 + bloqueio temporário + toast _"Tente novamente em X minutos"_ |
| E4  | Email inválido no cadastro  | RF01 (regex) + RNF06                         | Validação frontend impede submit                                        |

---

### 📌 FLUXO 2 — Criação e Edição de Lista de Compras

**Cobertura:** UC08, UC10, UC12 | **RFs:** RF06, RF08, RF10 | **RNFs:** RNF03, RNF06

#### ✅ Happy Path

```
1. Usuário autenticado clica "Nova Lista"
2. Digita nome="Compras do Mês"
3. Adiciona item via autocomplete (UC12):
   - Digita "arr" → debounce 300ms → cache 5min
   - Seleciona "Arroz Tipo 1 5kg" (UC22 consome catálogo)
   - Define quantidade=2
4. Frontend calcula subtotal em tempo real (qtd × preço)
5. Salva → Backend valida FK do produto (RNF03 ACID)
6. Draft automático a cada 30s (RF08)
7. Toast verde: *"Lista salva com sucesso"*
```

#### ⚠️ Exceções Previstas

| #   | Exceção                               | Guard-Rail                   | Resposta do Sistema                                                   |
| --- | ------------------------------------- | ---------------------------- | --------------------------------------------------------------------- |
| E1  | Lista sem itens                       | RF06 (mínimo 1 item)         | Botão "Salvar" desabilitado + mensagem _"Adicione ao menos 1 item"_   |
| E2  | Quantidade = 0 ou negativa            | RF06 (1-9999)                | Validação inline rejeita; ícone de erro no campo                      |
| E3  | Produto foi descontinuado no catálogo | RF06 (FK constraint) + RNF03 | Toast vermelho: _"Produto indisponível, remova da lista"_             |
| E4  | Nome da lista >100 chars              | RF06                         | Contador visual "X/100" + bloqueio de digitação                       |
| E5  | Perda de conexão durante draft        | RNF05 (feedback visual)      | Toast _"Salvamento falhou. Tentando novamente..."_ + retry automático |

---

### 📌 FLUXO 3 — Seleção e Filtragem de Fornecedores ⭐ (NOVO v2.1)

**Cobertura:** UC25, UC26 | **RFs:** RF11, RF12 | **RNFs:** RNF04, RNF05, RNF06

#### ✅ Happy Path

```
1. Usuário clica "Comparar Fornecedores" em uma lista salva
2. Sistema abre tela de seleção (UC25)
3. Lista exibe 10 fornecedores com checkboxes + % disponibilidade
   Ex: "Mercado Bom Preço — 9/10 itens (90%)"
4. Usuário aplica filtro (UC26): slider em 70%
   → Lista reduz para 6 fornecedores que atendem ≥70%
5. Usuário seleciona 3 fornecedores via checkboxes
6. Contador visual: "3 fornecedores selecionados" ✅
7. Botão "Calcular Orçamento" habilitado (mínimo 2 atendido)
8. Seleção mantida em memória (sessão temporária — não persiste no DB)
```

#### ⚠️ Exceções Previstas

| #   | Exceção                                              | Guard-Rail                      | Resposta do Sistema                                                            |
| --- | ---------------------------------------------------- | ------------------------------- | ------------------------------------------------------------------------------ |
| E1  | Usuário seleciona apenas 1 fornecedor                | RF11 (mínimo 2 obrigatórios)    | Botão "Calcular" desabilitado + mensagem _"Selecione ao menos 2 fornecedores"_ |
| E2  | Filtro 100% elimina todos                            | RF12                            | Mensagem _"Nenhum fornecedor atende ao filtro"_ + sugestão de reduzir %        |
| E3  | Filtro desmarca fornecedor já selecionado            | RF12 (manter seleção se válida) | Sistema mantém checkbox ativo SE fornecedor ainda passar no filtro             |
| E4  | Usuário clica "Selecionar Todos" com 10 fornecedores | RF11 (máximo 10)                | Permitido (dentro do limite)                                                   |
| E5  | Usuário recarrega a página                           | Apêndice A (sessão temporária)  | Seleção é perdida (comportamento documentado) — toast informativo              |

---

### 📌 FLUXO 4 — Cálculo e Visualização de Resultados

**Cobertura:** UC13, UC14, UC15, UC16 | **RFs:** RF13, RF14 | **RNFs:** RNF10

#### ✅ Happy Path

```
1. Usuário clica "Calcular Orçamento"
2. Backend valida: lista pertence ao usuário + ≥2 fornecedores (RF13)
3. UC23 + UC24: busca fornecedores selecionados + preços
4. Calcula para cada fornecedor:
   - Itens disponíveis
   - Itens ausentes
   - Preço total (qtd × preço unitário)
5. Ordena por preço total (menor → maior)
6. Cache de resultados por 5min (RF13)
7. Frontend renderiza tabela flat (RNF04 desktop-first ≥1024px)
8. UC15 destaca linha do "Mercado Bom Preço" em verde
9. UC16: tooltip mostra "Faltam: Leite integral, Sabão em pó"
10. Botões "Exportar" e "Imprimir" sempre visíveis
```

#### ⚠️ Exceções Previstas

| #   | Exceção                                 | Guard-Rail                      | Resposta do Sistema                                              |
| --- | --------------------------------------- | ------------------------------- | ---------------------------------------------------------------- |
| E1  | Cálculo demora >10s                     | RF13 (timeout)                  | Toast _"Tempo esgotado. Tente menos fornecedores"_ + botão retry |
| E2  | Lista foi excluída em outra aba         | RF13 (validação de propriedade) | Redireciona para /dashboard + toast _"Lista não encontrada"_     |
| E3  | Fornecedor sem preço para algum produto | RF14                            | Ícone de alerta ⚠️ + valor "N/D" na célula                       |
| E4  | Usuário altera seleção e recalcula      | RF13 (invalidar cache)          | Cache é descartado, novo cálculo disparado                       |
| E5  | API lenta (>500ms p95)                  | RNF10                           | Skeleton loading exibido após 300ms (RNF05)                      |

---

### 📌 FLUXO 5 — Exportação CSV e Impressão

**Cobertura:** UC17, UC18 | **RFs:** RF15, RF16 | **RNFs:** RNF04, RNF05

#### ✅ Happy Path

```
1. Usuário visualiza resultados da comparação
2. Clica "Exportar CSV" (UC17):
   - Frontend gera arquivo: "compras_do_mes_20260901.csv"
   - Encoding UTF-8 com BOM (compatível Excel PT-BR)
   - Delimitador ";" (padrão brasileiro)
   - Cabeçalho: Fornecedor;Itens Disp.;Itens Ausentes;Preço Total
   - Caracteres especiais escapados (aspas, vírgulas)
3. Download inicia + toast verde *"Download concluído"*
4. Usuário clica "Imprimir" (UC18):
   - CSS @media print oculta sidebar, botões, menu
   - Tabela formatada para A4 com quebras automáticas
   - Cores preservadas (melhor oferta em verde)
   - Data/hora da impressão no rodapé
5. window.print() abre diálogo nativo do navegador
```

#### ⚠️ Exceções Previstas

| #   | Exceção                                           | Guard-Rail            | Resposta do Sistema                                 |
| --- | ------------------------------------------------- | --------------------- | --------------------------------------------------- |
| E1  | Arquivo CSV >1MB                                  | RF15 (limite)         | Toast _"Arquivo muito grande. Reduza a comparação"_ |
| E2  | Nome da lista tem caracteres especiais (`,`, `"`) | RF15 (escaping)       | Sistema escapa automaticamente com aspas duplas     |
| E3  | Usuário tenta imprimir em tela <1024px            | RNF04 (desktop-first) | Aviso _"Impressão otimizada para telas ≥1024px"_    |
| E4  | Usuário cancela diálogo de impressão              | RF16                  | Nenhum erro; estado preservado                      |
| E5  | Download falha (sem espaço em disco)              | RNF05 (feedback)      | Toast vermelho _"Falha ao salvar arquivo"_          |

---

## 📊 3. MATRIZ DE COBERTURA DOS FLUXOS

| Fluxo          | RFs Cobertos     | RNFs Exercitados    | Princípios Nielsen                    |
| -------------- | ---------------- | ------------------- | ------------------------------------- |
| 1 — Auth       | RF01, RF02, RF04 | RNF11, RNF12, RNF13 | Segurança por padrão (P5)             |
| 2 — Listas     | RF06, RF08, RF10 | RNF03, RNF06        | Validação em tempo real               |
| 3 — Seleção ⭐ | RF11, RF12       | RNF04, RNF05, RNF06 | **Controle e Liberdade (Nielsen #3)** |
| 4 — Comparação | RF13, RF14       | RNF10               | Simplicidade Pragmática (P3)          |
| 5 — Exportação | RF15, RF16       | RNF04, RNF05        | KISS (P3)                             |

---

## ✅ 4. CONSIDERAÇÕES FINAIS DE CONSISTÊNCIA

### Alinhamento com o SSOT (`analise_fundamental_MVP.md`)

- ✅ Todos os 16 RFs da v2.1 estão mapeados em casos de uso
- ✅ UC25 e UC26 (novos v2.1) devidamente incorporados
- ✅ Princípio P2 (Controle e Liberdade) refletido no Fluxo 3
- ✅ Princípio P4 (Persistência Confiável) respeitado — seleção é temporária em memória, dados críticos em PostgreSQL ACID

### Regras de Governança Respeitadas

- ✅ Hierarquia de fontes: SSOT (Nível 1) > Especificação (Nível 2) > UCD (Nível 3)
- ✅ Guard-rails de cada RF aplicados nas exceções
- ✅ Rastreabilidade completa: RF → RNF → UC → Fluxo

### Próximos Passos Recomendados (conforme Seção 12 do SSOT)

1. ⏳ Atualizar `casos_de_uso_v0.2.xml` → `v2.1` incluindo UC25 e UC26
2. ⏳ Validar Fluxo 3 (seleção) com protótipo de alta fidelidade
3. ⏳ Implementar testes unitários cobrindo as exceções mapeadas (RNF07 — 80% cobertura)

---

**Documento gerado em:** 01/09/2026 · **Versão:** 1.0 · **Status:** ✅ Alinhado ao SSOT v2.1
