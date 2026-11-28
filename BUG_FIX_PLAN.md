# Plano de Correção de Bugs - COBECO MVP

## Status Atual

### ✅ Já Corrigidos (parcial ou totalmente)

| Bug | Status | O que foi feito |
|-----|--------|-----------------|
| **BUG-001** Cadastro usuário | 🟡 Parcial | Frontend: handleCadastro com toast + auto-login + promover rascunho. Backend: endpoint já retorna TokenResponse. |
| **BUG-002** Salvar lista | 🟡 Parcial | Frontend: handleSalvarLista + handler no dispatch + fluxo modal para não-logados. Backend: endpoints /listas e /listas/promover-efemera existem. |
| **BUG-003** Foco busca categorias | 🟡 Parcial | `recalcularVisiveis` agora chama `atualizarCategoriasVisiveis` (partial DOM update). `buscarCategoriasUI` usa partial update. |
| **BUG-004** Fulltext search | 🟡 Parcial | `CATEGORIA_GATILHOS` expandido significativamente. Falta: triggers para 14 categorias novas + popular `produto_classes` no seed. |
| **BUG-005** Apresentação categorias | 🔴 Pendente | Precisa: CSS Grid responsivo, sorting (alfabético/área/frequência), multi-seleção visual (checkboxes/cards), áreas como accordions/tabs, contador. |
| **BUG-006** Grandes áreas incompletas | 🟡 Parcial | `AREAS_GRANDES` atualizado mas ainda mapeia apenas 11 categorias do seed protótipo. Seed realístico tem 25 categorias. Precisa alinhar. |
| **BUG-007** Produtos irrelevantes | 🟢 Resolvido | `listar_por_categorias` agora filtra por `produtos.categoria_id` + disponibilidade em fornecedores ativos. Não mais JOIN por fornecedor. |
| **BUG-008** Quantidade × valor | 🟡 Parcial | `exportacao.py` agora mostra preço unitário e subtotal (quantidade × unitário). `comparacao.py` já multiplica corretamente (linha 225). Falta: verificar PDF vencedor. |

---

## 🎯 Ações Restantes por Bug

### BUG-001: Cadastro Usuário
- [ ] Verificar se backend `cadastrar_usuario` retorna `TokenResponse` corretamente (já faz)
- [ ] Testar fluxo completo: cadastro → login automático → toast → redirect → promover rascunho

### BUG-002: Salvar Lista
- [ ] Testar fluxo logado: salvar → toast → limpar rascunho → home
- [ ] Testar fluxo não-logado: modal → cadastro/login → promover rascunho → home
- [ ] Verificar se `promoverListaSeHouverRascunho` lê sessionStorage corretamente

### BUG-003: Foco Busca Categorias
- [ ] Testar: digitar no campo `#busca-cat` não deve perder foco
- [ ] Verificar se `atualizarCategoriasVisiveis` preserva foco no input
- [ ] Adicionar `focus()` programático no input após update se necessário

### BUG-004: Busca Inteligente / Fulltext
**FALTANDO triggers para 14 categorias do seed realístico:**
- Padaria
- Frios e Laticínios
- Açougue
- Hortifruti
- Eletrônicos
- Informática (já tem)
- Eletrodomésticos
- Móveis
- Livros (já tem)
- Papelaria
- Ferramentas (já tem)
- Materiais Construção
- Jardinagem (já tem)
- Iluminação
- Pet Alimentos
- Pet Acessórios
- Peças Automotivas
- Pneus e Rodas
- Vestuário Masculino
- Vestuário Feminino
- Calçados

**AÇÃO:** Adicionar entradas no `CATEGORIA_GATILHOS` para cada categoria acima.

**FALTANDO:** Popular tabela `produto_classes` no seed
- Script `script-seed-0004-realistic-seed-data.py` não popula `produto_classes`
- Precisa criar script ou adicionar ao seed existente

### BUG-005: Apresentação Categorias (UI/UX)
**AÇÕES FRONTEND (app.js + CSS):**
1. **CSS Grid responsivo** em `.cat-grid` - colunas auto-fit
2. **Sorting options**: dropdown com "Alfabético", "Por área grande", "Por frequência"
3. **Multi-seleção visual**: cards com estado `sel`, contador visível
4. **Áreas grandes como accordions/tabs**: agrupar categorias por área
5. **Contador de selecionadas** já existe (`cat-count`), melhorar visibilidade

**CSS (input.css):**
```css
.cat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}
.cat-card.sel { border-color: var(--pri); background: var(--pri-bg); }
.area-accordion { border: 1px solid var(--border); border-radius: 8px; margin-bottom: 8px; }
.area-accordion summary { padding: 12px; cursor: pointer; font-weight: 600; }
.area-accordion .cat-grid { padding: 0 12px 12px; }
```

### BUG-006: Grandes Áreas Incompletas
**Seed realístico (25 categorias) vs AREAS_GRANDES atual (11 categorias):**

| Grande Área | Categorias do Seed Realístico |
|-------------|-------------------------------|
| Supermercado | Mercearia, Bebidas, Limpeza, Higiene, Padaria, Frios e Laticínios, Açougue, Hortifruti |
| Departamento / Eletrônicos | Eletrônicos, Informática, Eletrodomésticos, Móveis |
| Livros e Papelaria | Livros, Papelaria |
| Hardware / Construção | Ferramentas, Materiais Construção, Jardinagem, Iluminação |
| Pet | Pet Alimentos, Pet Acessórios |
| Automotivo | Peças Automotivas, Pneus e Rodas |
| Moda | Vestuário Masculino, Vestuário Feminino, Calçados |

**AÇÃO:** Reescrever `AREAS_GRANDES` para mapear TODAS as 25 categorias.

### BUG-007: Produtos Irrelevantes
✅ **RESOLVIDO** - `listar_por_categorias` filtra por `produto.categoria_id` + disponibilidade.

### BUG-008: Quantidade × Valor
- [x] `comparacao.py` linha 225: `preco_item = preco_unit * item_lista.quantidade` ✅
- [x] `exportacao.py` `gerar_pdf_lista`: mostra preço unitário e subtotal ✅
- [ ] `exportacao.py` `gerar_pdf_vencedora`: verificar se usa quantidade (linha 462: `str(item.quantidade)` - OK, mas preço total usa `item.preco_total` que já inclui quantidade)
- [ ] Testar PDF exportado com item quantidade > 1

---

## 📋 Ordem de Execução Recomendada

1. **BUG-006** (AREAS_GRANDES) - base para BUG-004 e BUG-005
2. **BUG-004** (CATEGORIA_GATILHOS + produto_classes seed)
3. **BUG-005** (CSS Grid + Sorting + Accordions)
4. **BUG-003** (Testar e ajustar foco)
5. **BUG-001** (Teste completo cadastro)
6. **BUG-002** (Teste completo salvar lista)
7. **BUG-008** (Verificar PDF vencedor)

---

## 🔧 Comandos Úteis

```bash
# Rodar backend
cd backend && uvicorn src.main:app --reload

# Rodar frontend (servir estático)
cd frontend && python -m http.server 8080

# Popular banco com seed realístico
cd backend && python -m scripts.script-seed-0004-realistic-seed-data

# Rodar testes
cd backend && pytest tests/ -v
cd frontend && npx playwright test
```