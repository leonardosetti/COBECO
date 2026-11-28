# SPECS — COBECO: Jornada Efêmera, Navbar de Início, Retenção Opcional e Pré-filtro de Grandes Áreas

**Projeto:** COBECO — Comparador de Bens de Consumo  
**Versão:** 3.4 (adendo ao SPECS v3.3 — SSOT mantido)  
**Status:** Para implementação  
**Base:** observações de uso pós-MVP v3.3 + frontend `frontend/src/app.js` + backend `src/adapters/api/catalogo.py`  
**Stack:** Frontend Vanilla JS + Tailwind (sessionStorage), Backend FastAPI + MySQL, Desktop ≥1024px (RNF04)

---

## 1. PROBLEMA (5 observações do usuário)

| # | Problema | Impacto |
|---|----------|---------|
| P1 | Após gerar lista efêmera e comparar, o usuário fica "preso" na última tela; não há renovação de sessão para iniciar a próxima lista. | Jornada trava; usuário não consegue começar nova comparação sem recarregar a página. |
| P2 | Não há navbar/link visível para voltar à página de início da jornada (Home). | Não há ponto de partida claro após concluir uma lista. |
| P3 | Ao voltar ao início com uma lista em andamento, não há opção de esquecê-la ou mantê-la. | Perda acidental de rascunho ou impossibilidade de começar do zero preservando o rascunho. |
| P4 | Busca semântica de categorias substitui a lista visível; categorias já selecionadas ficam "invisíveis e marcadas" fora do filtro. | Usuário não percebe o que está selecionado ao navegar por buscas diferentes. |
| P5 | Com muitas categorias macro, não há pré-filtro por grandes áreas (Supermercado, Informática, Automóveis, Lojas de departamento…). | Lista de categorias longa e de difícil varredura; sem multi-seleção de áreas. |

---

## 2. ESCOPO E PRINCÍPIOS

- Alterações apenas no **frontend** (`app.js`, `index.html`) e um **novo endpoint de catálogo** no backend.
- Persistência continua em `sessionStorage` (sobrevive a recarregar aba; morre ao fechar browser/limpar sessão) — atende "espaço próprio até encerramento do browser".
- Não grava nada novo no MySQL para listas efêmeras (mantém Autenticação Tardia da SPECS §6).
- Mudança mínima: reaproveita `state`, `persistEph`, `loadEph`, `navHTML`, `vCategorias` existentes.

---

## 3. MODELO DE PERSISTÊNCIA (sessionStorage)

Nova chave `cobeco_jornada` (objeto) substituindo/ampliando `cobeco_eph`:

```ts
sessionStorage.cobeco_jornada = {
  rascunho: { lista: { nome, itens[] }, categorias: id[], areas: id[] }, // em andamento
  gerada:   { lista, categorias, areas, resultado, exportadoEm }, // última lista concluída (espaço próprio)
  historico: [ { lista, categorias, areas, exportadoEm } ] // listas geradas da sessão (até fechar browser)
};
```

- `rascunho`: lista que o usuário está montando (não concluída).
- `gerada`: a última lista já comparada/exportada — fica visível no "espaço próprio" até o browser fechar.
- `historico`: todas as listas concluídas da sessão.

---

## 4. REQUISITOS FUNCIONAIS (novos)

| ID | Requisito | Descrição | Prioridade |
|----|-----------|-----------|------------|
| **RF22** | Retornar ao início após concluir lista efêmera | Ao exportar/imprimir a Lista Vencedora (ou clicar "Nova lista"), o rascunho atual vira `gerada`+`historico`, o `rascunho` é limpo e o usuário volta à página inicial para iniciar a próxima lista. | P0 |
| **RF23** | Espaço próprio de listas geradas | Listas concluídas ficam retidas em espaço próprio (`gerada`/`historico` no sessionStorage) até fechar o browser ou limpar cookies/sessão. Disponíveis para reabrir/reexportar durante a sessão. | P0 |
| **RF24** | Navbar fixa com link Início | Navbar sempre visível no topo com link "Início" (página home/jornada), "Nova lista" (reiniciar), "Minhas listas"/"Perfil" (logado) e "Sair"/"Entrar". | P0 |
| **RF25** | Retenção opcional ao esquecer rascunho | Ao navegar para Início/Nova lista com `rascunho` não vazio, abrir modal: "Esquecer lista em andamento? Sim / Não". Sim → limpa rascunho e começa nova. Não → mantém rascunho e permanece na tela atual (ou volta ao início mantendo o rascunho). | P0 |
| **RF26** | Categorias selecionadas sempre visíveis | Na busca semântica de categorias (RF20), categorias já selecionadas permanecem visíveis e marcadas mesmo quando não batem no termo de busca. Filtro de busca nunca esconde uma seleção ativa. | P0 |
| **RF27** | Pré-filtro de grandes áreas (multi-seleção) | Barra acima das categorias macro com grandes áreas (ex.: Supermercado, Informática, Automóveis, Lojas de departamento, Construção e Ferragens, Casa e Jardim, Livros e Papelaria). Multi-seleção via checkboxes; mostra apenas categorias pertencentes a ≥1 área selecionada. Nenhuma área selecionada = mostra todas as categorias. | P0 |
| **RF28** | Mapeamento categoria macro → grande área | Cada categoria macro pertence a ≥1 grande área. Mapeamento mantido no backend (análogo a `CATEGORIA_GATILHOS`) e exposto via endpoint. | P0 |

---

## 5. REQUISITOS NÃO FUNCIONAIS

| ID | Requisito | Métrica |
|----|-----------|---------|
| **RNF13** | Sem novos dados no MySQL para efêmeras | Listas efêmeras/geradas vivem apenas em sessionStorage. |
| **RNF14** | Desktop-only ≥1024px | Navbar e pré-filtro respeitam breakpoint único (RNF04). |
| **RNF15** | Feedback <100ms | Troca de área/filtro e busca atualizam categorias visíveis em <100ms. |
| **RNF16** | Persistência de sessão | `sessionStorage` sobrevive a recarregar aba; perdido ao fechar browser/limpar sessão (sem cookies novos). |

---

## 6. ESPECIFICAÇÃO DE UI / TELAS

### 6.1 Navbar (RF24) — `navHTML()` em `app.js`
Fixada no topo, visível em todas as views:

```
[🛒 COBECO]  [Início] [Nova lista]  (logado: [Minhas listas] [Perfil])  (não logado: [Entrar] [Criar conta]) [Sair]
```

- "Início" → `go('home')`.
- "Nova lista" → dispara RF25 (modal se houver rascunho).

### 6.2 Passo 1 — Categorias com pré-filtro de áreas (RF27/RF28)
Novo toolbar acima das categorias macro:

```
Grandes áreas: [☐ Supermercado] [☐ Informática] [☐ Automóveis] [☐ Lojas de departamento] [☐ Construção e Ferragens] [☐ Casa e Jardim] [☐ Livros e Papelaria]  [Limpar áreas]
Buscar categoria (semântica): [input]
```

- Cada grande área = checkbox multi-seleção (`state.areasSelecionadas`).
- `categoriasVisiveis` = categorias que pertencem a ≥1 área selecionada (ou todas se nenhuma área selecionada) ∪ categorias já selecionadas (RF26).
- Chip contador mantém: "N categoria(s) selecionada(s)".

### 6.3 Modal "Esquecer lista em andamento?" (RF25)
Disparado por "Início" ou "Nova lista" quando `state.lista.itens.length > 0` (rascunho não vazio):

```
Esquecer lista em andamento?
Itens: X · Categorias: Y
[Não — manter rascunho]   [Sim — começar nova lista]
```

- Não → cancela navegação, mantém tela e rascunho.
- Sim → limpa `rascunho` (lista, categorias, áreas), vai para `home` ou `categorias` zerado.

### 6.4 Após conclusão (RF22/RF23)
Na tela Vencedora/Resultados, após Exportar PDF ou Imprimir:
- Move `rascunho` → `gerada` + `historico`.
- Limpa `rascunho`.
- `go('home')`.
- Toast: "Lista concluída. Inicie uma nova lista."

---

## 7. ESPECIFICAÇÃO DE PERSISTÊNCIA (código frontend)

Substituir `persistEph`/`loadEph` por:

```js
function persistJornada() {
  try {
    sessionStorage.setItem('cobeco_jornada', JSON.stringify({
      rascunho: { lista: state.lista, categorias: state.categorias, areas: state.areasSelecionadas },
      gerada: state.listaGerada,
      historico: state.historicoSessao
    }));
  } catch (e) {}
}
function loadJornada() {
  const raw = sessionStorage.getItem('cobeco_jornada');
  if (!raw) return;
  const d = JSON.parse(raw);
  if (d.rascunho?.lista?.itens?.length) { state.lista = d.rascunho.lista; state.categorias = d.rascunho.categorias || []; state.areasSelecionadas = d.rascunho.areas || []; }
  state.listaGerada = d.gerada; state.historicoSessao = d.historico || [];
}
```

`state` ganha: `areasSelecionadas: []`, `listaGerada: null`, `historicoSessao: []`.

---

## 8. ESPECIFICAÇÃO DE BACKEND (mínimo)

### Novo endpoint — `GET /catalogo/areas-grandes`
Retorna grandes áreas com as categorias macro que pertencem a cada uma:

```ts
class AreaGrandeResponse {
  id: int; nome: str; categorias: list[CategoriaResponse];
}
```

Mapeamento sugerido (análogo a `CATEGORIA_GATILHOS`, hardcoded ou coluna futura):

| Grande área | Categorias macro |
|-------------|------------------|
| Supermercado | Mercado |
| Informática | Informática |
| Automóveis | Automotivos |
| Lojas de departamento | Vestuário, Móveis, Decoração, Eletrodomésticos |
| Construção e Ferragens | Materiais de Construção e Ferragens, Ferramentas |
| Casa e Jardim | Jardinagem, Decoração |
| Livros e Papelaria | Livros |

### Ajuste — `GET /categorias`
Aceita query opcional `?areas=1,2,3` para filtrar categorias pelas áreas selecionadas (multi-seleção). Sem parâmetro = todas.

### Sem alterações no MySQL
Mapeamento área→categoria mantido em código (parecido com `CATEGORIA_GATILHOS`). Sem nova migração.

---

## 9. FLUXO ATUALIZADO (jornada do visitante)

```
Home → (áreas +) Categorias → Lista → Fornecedores → Comparação → Vencedora
                                                                ↓
                                                        Exportar PDF / Imprimir
                                                                ↓
                                                        rascunho → gerada/historico
                                                                ↓
                                                        volta ao Home (nova lista)
```

---

## 10. DEFINIÇÃO DE PRONTO (DoD) v3.4

- [ ] Navbar fixa com link "Início" visível em todas as views (RF24).
- [ ] Pré-filtro de grandes áreas multi-seleção no Passo 1 (RF27/RF28).
- [ ] Busca de categorias nunca esconde categorias já selecionadas (RF26).
- [ ] Modal "Esquecer lista em andamento? Sim/Não" ao voltar ao início com rascunho (RF25).
- [ ] Após concluir lista, rascunho vira `gerada`/`historico`, limpa e volta ao Home (RF22/RF23).
- `gerada`/`historico` persistem em sessionStorage até fechar browser/limpar sessão (RNF13/RNF16).
- [ ] Endpoint `GET /catalogo/areas-grandes` e filtro `?areas=` em `/categorias` (RF28).
- [ ] E2E Playwright: fluxo completo conclui → retorna ao início; busca mantém selecionada visível; pré-filtro áreas multi-seleção funciona; modal Sim/Não limpa ou mantém rascunho.
- [ ] Testes unitários de persistência `cobeco_jornada` (≥80% cobertura regras negócio, RNF06).

---

## 11. NOTAS DE IMPLEMENTAÇÃO (ponytail — mínimo necessário)

- Reutilizar `cat-grid`, `count-chip`, `stepperHTML`, `persistEph`/`loadEph` existentes; não criar componentes novos.
- `state.areasSelecionadas` é um array de ids (multi-seleção).
- Na busca de categorias (`buscarCategoriasUI`), depois de filtrar, adicionar de volta as `state.categorias` que não apareceram no resultado para que fiquem visíveis/marcadas (RF26).
- Não adicionar dependências npm novas.

---
**Fim do documento SPECS v3.4 (adendo ao SPECS v3.3).**

## 12. IMPLEMENTAÇÃO REALIZADA

### Arquivos alterados

| Arquivo | O que mudou |
|---------|-------------|
| `frontend/src/app.js` | `state` (+areasSelecionadas, areasGrandes, listaGerada, historicoSessao); `ApiClient.listarAreasGrandes`; `carregarAreasGrandes`; `navHTML()` injetado no `topbar` via `render()` (RF24); `vCategorias` com barra de áreas multi-seleção + `areasParaCategorias`/`recalcularVisiveis` (RF27/RF28); `buscarCategoriasUI` mantém selecionadas visíveis (RF26); `persistEph`/`loadEph` → `persistJornada`/`loadJornada` (chave `cobeco_jornada`, rascunho+gerada+historico) (RF23); modal "Esquecer lista em andamento? Sim/Não" via `irParaInicioComModal` (RF25); `concluirJornada` chamado após export-pdf (RF22); boot recarrega áreas e reaplica filtro persistido. |
| `frontend/src/styles/prototype.css` | Estilos de `.areas-bar`, `.area-cb`, `.cat-grid`, `.cat-card` (RF27). |
| `backend/src/adapters/api/catalogo.py` | Constante `AREAS_GRANDES` (mapeamento área→categorias); schema `AreaGrandeResponse`; `GET /catalogo/areas-grandes` (RF28); `GET /categorias` aceita `?areas=1,2,3` (filtro multi-seleção backend) (RF27/RF28). Sem nova migração MySQL. |

### Arquivos não alterados (intencional)
- `SPECS.md` v3.3 (SSOT mantido; este é um adendo).
- `frontend/src/index.html` (já possui `<header class="top">` com `#topbar`; injetado via JS).
- MySQL / migrações (listas efêmeras continuam apenas em `sessionStorage`).

### Como verificar (DoD v3.4)
- Navbar com "Início" visível em todas as views (fixa no topo).
- Pré-filtro de grandes áreas com multi-seleção no Passo 1.
- Busca de categorias nunca esconde categorias já selecionadas.
- Modal Sim/Não ao voltar ao início com rascunho.
- Após exportar PDF, rascunho vira `gerada`/`historico`, limpa e volta ao Início.
- `sessionStorage.cobeco_jornada` persiste até fechar o browser.