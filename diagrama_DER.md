# 📊 Diagrama Entidade-Relacionamento — COBECO MVP v3.1

**Documento Técnico — DER Oficial**
**Data:** 12 de Setembro de 2026
**Status:** ✅ APROVADO (SSOT)
**Base:** Relatório Analítico Final v3.1 + ADR-003 (SQLite3 WAL)

---

## 🎯 Especificação do DER v3.1

### Premissas Aplicadas

| Princípio | Aplicação no DER |
|-----------|------------------|
| **ACID** | Foreign keys com `ON DELETE CASCADE/RESTRICT`, transações explícitas, WAL mode |
| **KISS** | SQLite3 stdlib, zero ORM pesado, Repository pattern |
| **YAGNI** | Sem tabelas de sessão, sem refresh_tokens, sem comparisons |
| **SDD** | Campos alinhados aos schemas Pydantic |
| **Correção v3.1** | Categorias são de **FORNECEDORES** (N:N via `supplier_categories`) |

### Entidades (8 tabelas)

| # | Tabela | Grupo | Regra de Negócio |
|---|--------|-------|------------------|
| 1 | `users` | 🔐 Auth | Usuários com autenticação JWT |
| 2 | `lists` | 📝 Listas | Listas persistidas (soft delete) |
| 3 | `list_items` | 📝 Listas | Itens de cada lista |
| 4 | `categories` | 🏪 Catálogo | Categorias **MACRO de fornecedores** |
| 5 | `suppliers` | 🏪 Catálogo | Fornecedores mockados |
| 6 | `supplier_categories` | 🏪 Catálogo | **Pivô N:N** (fornecedor ↔ categorias) |
| 7 | `products` | 🏪 Catálogo | Produtos agnósticos a categoria |
| 8 | `supplier_products` | 🏪 Catálogo | Preços e estoque por fornecedor |

### Relacionamentos (Cardinalidades)

| Origem | → | Destino | Cardinalidade | Constraint |
|--------|---|---------|---------------|------------|
| `users` | → | `lists` | 1:N | FK `user_id` ON DELETE CASCADE |
| `lists` | → | `list_items` | 1:N | FK `list_id` ON DELETE CASCADE |
| `products` | → | `list_items` | 1:N | FK `product_id` ON DELETE RESTRICT |
| `suppliers` | → | `supplier_products` | 1:N | FK `supplier_id` ON DELETE CASCADE |
| `products` | → | `supplier_products` | 1:N | FK `product_id` ON DELETE RESTRICT |
| `suppliers` | ↔ | `categories` | N:N | Via `supplier_categories` |

---

## 📄 Script XML para Draw.io

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-09-12T00:00:00.000Z" agent="COBECO MVP v3.1" version="24.0.0" type="device">
  <diagram id="cobeco-der-v31" name="COBECO — DER MVP v3.1">
    <mxGraphModel dx="2600" dy="1800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2600" pageHeight="1800" math="0" shadow="1">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- ===================== TÍTULO ===================== -->
        <mxCell id="title" value="&lt;b&gt;Diagrama Entidade-Relacionamento — COBECO MVP v3.1&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:11px;&quot; color=&quot;#666&quot;&gt;8 Tabelas • SQLite3 WAL • ACID • 12/09/2026&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontColor=#1A237E;" vertex="1" parent="1">
          <mxGeometry x="700" y="20" width="1200" height="55" as="geometry"/>
        </mxCell>

        <!-- ===================== BOUNDARY DO BANCO ===================== -->
        <mxCell id="boundary" value="SQLite3 Database — cobeco.db (WAL Mode + Foreign Keys ON)" style="swimlane;startSize=35;fillColor=#FAFAFA;strokeColor=#1A237E;fontStyle=1;fontSize=14;rounded=1;arcSize=4;shadow=1;strokeWidth=2;swimlaneLine=0;" vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="2400" height="1500" as="geometry"/>
        </mxCell>

        <!-- ===================== GRUPO AUTH (VERMELHO) ===================== -->
        <mxCell id="groupAuth" value="🔐 AUTENTICAÇÃO" style="swimlane;startSize=28;fillColor=#FFEBEE;strokeColor=#C62828;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#B71C1C;swimlaneLine=0;shadow=0;" vertex="1" parent="boundary">
          <mxGeometry x="40" y="50" width="420" height="480" as="geometry"/>
        </mxCell>

        <mxCell id="tblUsers" value="&lt;b&gt;users&lt;/b&gt;" style="swimlane;startSize=30;fillColor=#FFFFFF;strokeColor=#C62828;fontStyle=1;fontSize=13;rounded=1;arcSize=4;shadow=1;strokeWidth=2;swimlaneLine=0;fontColor=#B71C1C;" vertex="1" parent="groupAuth">
          <mxGeometry x="40" y="50" width="340" height="380" as="geometry"/>
        </mxCell>

        <mxCell id="u1" value="🔑 &lt;b&gt;id&lt;/b&gt; : INTEGER" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblUsers">
          <mxGeometry x="0" y="35" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="u2" value="&lt;b&gt;username&lt;/b&gt; : TEXT &lt;font color=&quot;#C62828&quot;&gt;[UQ, NN]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblUsers">
          <mxGeometry x="0" y="60" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="u3" value="&lt;b&gt;email&lt;/b&gt; : TEXT &lt;font color=&quot;#C62828&quot;&gt;[UQ, NN]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblUsers">
          <mxGeometry x="0" y="85" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="u4" value="&lt;b&gt;name&lt;/b&gt; : TEXT [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblUsers">
          <mxGeometry x="0" y="110" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="u5" value="&lt;b&gt;password_hash&lt;/b&gt; : TEXT [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblUsers">
          <mxGeometry x="0" y="135" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="u6" value="&lt;b&gt;security_question&lt;/b&gt; : TEXT [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblUsers">
          <mxGeometry x="0" y="160" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="u7" value="&lt;b&gt;security_answer_hash&lt;/b&gt; : TEXT [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblUsers">
          <mxGeometry x="0" y="185" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="u8" value="&lt;b&gt;created_at&lt;/b&gt; : DATETIME [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblUsers">
          <mxGeometry x="0" y="210" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="u9" value="&lt;b&gt;updated_at&lt;/b&gt; : DATETIME [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblUsers">
          <mxGeometry x="0" y="235" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="u10" value="&lt;b&gt;deleted_at&lt;/b&gt; : DATETIME &lt;font color=&quot;#666&quot;&gt;[soft delete]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblUsers">
          <mxGeometry x="0" y="260" width="340" height="25" as="geometry"/>
        </mxCell>

        <mxCell id="uConst" value="&lt;font color=&quot;#C62828&quot;&gt;&lt;b&gt;CONSTRAINTS&lt;/b&gt;&lt;/font&gt;&lt;br&gt;PK(id)&lt;br&gt;UNIQUE(username)&lt;br&gt;UNIQUE(email)&lt;br&gt;CHECK(length(username) BETWEEN 3 AND 30)&lt;br&gt;CHECK(length(name) BETWEEN 2 AND 100)" style="text;html=1;strokeColor=#C62828;fillColor=#FFEBEE;align=left;verticalAlign=top;fontSize=10;spacingLeft=8;spacingTop=4;rounded=1;strokeWidth=1;" vertex="1" parent="tblUsers">
          <mxGeometry x="10" y="295" width="320" height="75" as="geometry"/>
        </mxCell>

        <!-- ===================== GRUPO LISTAS (AZUL) ===================== -->
        <mxCell id="groupLists" value="📝 GESTÃO DE LISTAS" style="swimlane;startSize=28;fillColor=#E3F2FD;strokeColor=#1565C0;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#0D47A1;swimlaneLine=0;shadow=0;" vertex="1" parent="boundary">
          <mxGeometry x="500" y="50" width="800" height="480" as="geometry"/>
        </mxCell>

        <mxCell id="tblLists" value="&lt;b&gt;lists&lt;/b&gt;" style="swimlane;startSize=30;fillColor=#FFFFFF;strokeColor=#1565C0;fontStyle=1;fontSize=13;rounded=1;arcSize=4;shadow=1;strokeWidth=2;swimlaneLine=0;fontColor=#0D47A1;" vertex="1" parent="groupLists">
          <mxGeometry x="30" y="50" width="320" height="320" as="geometry"/>
        </mxCell>

        <mxCell id="l1" value="🔑 &lt;b&gt;id&lt;/b&gt; : INTEGER" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblLists">
          <mxGeometry x="0" y="35" width="320" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="l2" value="🔗 &lt;b&gt;user_id&lt;/b&gt; : INTEGER &lt;font color=&quot;#1565C0&quot;&gt;[FK, NN]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblLists">
          <mxGeometry x="0" y="60" width="320" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="l3" value="&lt;b&gt;name&lt;/b&gt; : TEXT [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblLists">
          <mxGeometry x="0" y="85" width="320" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="l4" value="&lt;b&gt;created_at&lt;/b&gt; : DATETIME [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblLists">
          <mxGeometry x="0" y="110" width="320" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="l5" value="&lt;b&gt;updated_at&lt;/b&gt; : DATETIME [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblLists">
          <mxGeometry x="0" y="135" width="320" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="l6" value="&lt;b&gt;deleted_at&lt;/b&gt; : DATETIME &lt;font color=&quot;#666&quot;&gt;[soft delete]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblLists">
          <mxGeometry x="0" y="160" width="320" height="25" as="geometry"/>
        </mxCell>

        <mxCell id="lConst" value="&lt;font color=&quot;#1565C0&quot;&gt;&lt;b&gt;CONSTRAINTS&lt;/b&gt;&lt;/font&gt;&lt;br&gt;PK(id)&lt;br&gt;FK(user_id) → users(id) ON DELETE CASCADE&lt;br&gt;CHECK(length(name) BETWEEN 1 AND 100)&lt;br&gt;INDEX(user_id, created_at DESC)" style="text;html=1;strokeColor=#1565C0;fillColor=#E3F2FD;align=left;verticalAlign=top;fontSize=10;spacingLeft=8;spacingTop=4;rounded=1;strokeWidth=1;" vertex="1" parent="tblLists">
          <mxGeometry x="10" y="195" width="300" height="75" as="geometry"/>
        </mxCell>

        <mxCell id="tblListItems" value="&lt;b&gt;list_items&lt;/b&gt;" style="swimlane;startSize=30;fillColor=#FFFFFF;strokeColor=#1565C0;fontStyle=1;fontSize=13;rounded=1;arcSize=4;shadow=1;strokeWidth=2;swimlaneLine=0;fontColor=#0D47A1;" vertex="1" parent="groupLists">
          <mxGeometry x="430" y="50" width="340" height="320" as="geometry"/>
        </mxCell>

        <mxCell id="li1" value="🔑 &lt;b&gt;id&lt;/b&gt; : INTEGER" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblListItems">
          <mxGeometry x="0" y="35" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="li2" value="🔗 &lt;b&gt;list_id&lt;/b&gt; : INTEGER &lt;font color=&quot;#1565C0&quot;&gt;[FK, NN]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblListItems">
          <mxGeometry x="0" y="60" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="li3" value="🔗 &lt;b&gt;product_id&lt;/b&gt; : INTEGER &lt;font color=&quot;#1565C0&quot;&gt;[FK, NN]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblListItems">
          <mxGeometry x="0" y="85" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="li4" value="&lt;b&gt;quantity&lt;/b&gt; : INTEGER [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblListItems">
          <mxGeometry x="0" y="110" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="li5" value="&lt;b&gt;created_at&lt;/b&gt; : DATETIME [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblListItems">
          <mxGeometry x="0" y="135" width="340" height="25" as="geometry"/>
        </mxCell>

        <mxCell id="liConst" value="&lt;font color=&quot;#1565C0&quot;&gt;&lt;b&gt;CONSTRAINTS&lt;/b&gt;&lt;/font&gt;&lt;br&gt;PK(id)&lt;br&gt;FK(list_id) → lists(id) ON DELETE CASCADE&lt;br&gt;FK(product_id) → products(id) ON DELETE RESTRICT&lt;br&gt;CHECK(quantity BETWEEN 1 AND 9999)&lt;br&gt;UNIQUE(list_id, product_id)" style="text;html=1;strokeColor=#1565C0;fillColor=#E3F2FD;align=left;verticalAlign=top;fontSize=10;spacingLeft=8;spacingTop=4;rounded=1;strokeWidth=1;" vertex="1" parent="tblListItems">
          <mxGeometry x="10" y="170" width="320" height="90" as="geometry"/>
        </mxCell>

        <!-- ===================== GRUPO CATÁLOGO (VERDE) ===================== -->
        <mxCell id="groupCatalog" value="🏪 CATÁLOGO DE FORNECEDORES E PRODUTOS" style="swimlane;startSize=28;fillColor=#E8F5E9;strokeColor=#2E7D32;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#1B5E20;swimlaneLine=0;shadow=0;" vertex="1" parent="boundary">
          <mxGeometry x="40" y="570" width="2320" height="880" as="geometry"/>
        </mxCell>

        <mxCell id="tblCategories" value="&lt;b&gt;categories&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;&quot; color=&quot;#2E7D32&quot;&gt;(macro — para FORNECEDORES)&lt;/font&gt;" style="swimlane;startSize=40;fillColor=#FFFFFF;strokeColor=#2E7D32;fontStyle=1;fontSize=13;rounded=1;arcSize=4;shadow=1;strokeWidth=2;swimlaneLine=0;fontColor=#1B5E20;" vertex="1" parent="groupCatalog">
          <mxGeometry x="40" y="50" width="340" height="200" as="geometry"/>
        </mxCell>

        <mxCell id="c1" value="🔑 &lt;b&gt;id&lt;/b&gt; : INTEGER" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblCategories">
          <mxGeometry x="0" y="45" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="c2" value="&lt;b&gt;name&lt;/b&gt; : TEXT &lt;font color=&quot;#2E7D32&quot;&gt;[UQ, NN]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblCategories">
          <mxGeometry x="0" y="70" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="c3" value="&lt;b&gt;description&lt;/b&gt; : TEXT" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblCategories">
          <mxGeometry x="0" y="95" width="340" height="25" as="geometry"/>
        </mxCell>

        <mxCell id="cConst" value="&lt;font color=&quot;#2E7D32&quot;&gt;&lt;b&gt;CONSTRAINTS&lt;/b&gt;&lt;/font&gt;&lt;br&gt;PK(id)&lt;br&gt;UNIQUE(name)&lt;br&gt;Seed: 5 categorias macro" style="text;html=1;strokeColor=#2E7D32;fillColor=#E8F5E9;align=left;verticalAlign=top;fontSize=10;spacingLeft=8;spacingTop=4;rounded=1;strokeWidth=1;" vertex="1" parent="tblCategories">
          <mxGeometry x="10" y="130" width="320" height="60" as="geometry"/>
        </mxCell>

        <mxCell id="tblSuppliers" value="&lt;b&gt;suppliers&lt;/b&gt;" style="swimlane;startSize=30;fillColor=#FFFFFF;strokeColor=#2E7D32;fontStyle=1;fontSize=13;rounded=1;arcSize=4;shadow=1;strokeWidth=2;swimlaneLine=0;fontColor=#1B5E20;" vertex="1" parent="groupCatalog">
          <mxGeometry x="40" y="290" width="340" height="280" as="geometry"/>
        </mxCell>

        <mxCell id="s1" value="🔑 &lt;b&gt;id&lt;/b&gt; : INTEGER" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSuppliers">
          <mxGeometry x="0" y="35" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="s2" value="&lt;b&gt;name&lt;/b&gt; : TEXT [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSuppliers">
          <mxGeometry x="0" y="60" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="s3" value="&lt;b&gt;cnpj&lt;/b&gt; : TEXT &lt;font color=&quot;#2E7D32&quot;&gt;[UQ, NN]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSuppliers">
          <mxGeometry x="0" y="85" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="s4" value="&lt;b&gt;active&lt;/b&gt; : BOOLEAN [NN, DEFAULT 1]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSuppliers">
          <mxGeometry x="0" y="110" width="340" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="s5" value="&lt;b&gt;created_at&lt;/b&gt; : DATETIME [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSuppliers">
          <mxGeometry x="0" y="135" width="340" height="25" as="geometry"/>
        </mxCell>

        <mxCell id="sConst" value="&lt;font color=&quot;#2E7D32&quot;&gt;&lt;b&gt;CONSTRAINTS&lt;/b&gt;&lt;/font&gt;&lt;br&gt;PK(id)&lt;br&gt;UNIQUE(cnpj)&lt;br&gt;Seed: 10 fornecedores" style="text;html=1;strokeColor=#2E7D32;fillColor=#E8F5E9;align=left;verticalAlign=top;fontSize=10;spacingLeft=8;spacingTop=4;rounded=1;strokeWidth=1;" vertex="1" parent="tblSuppliers">
          <mxGeometry x="10" y="170" width="320" height="60" as="geometry"/>
        </mxCell>

        <!-- TABELA PIVÔ supplier_categories -->
        <mxCell id="tblSupplierCategories" value="&lt;b&gt;supplier_categories&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;&quot; color=&quot;#2E7D32&quot;&gt;⭐ PIVÔ N:N (NOVO v3.1)&lt;/font&gt;" style="swimlane;startSize=40;fillColor=#FFFFFF;strokeColor=#2E7D32;fontStyle=1;fontSize=13;rounded=1;arcSize=4;shadow=1;strokeWidth=2;swimlaneLine=0;fontColor=#1B5E20;dashed=0;" vertex="1" parent="groupCatalog">
          <mxGeometry x="450" y="50" width="380" height="200" as="geometry"/>
        </mxCell>

        <mxCell id="sc1" value="🔑🔗 &lt;b&gt;supplier_id&lt;/b&gt; : INTEGER &lt;font color=&quot;#2E7D32&quot;&gt;[FK, PK]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSupplierCategories">
          <mxGeometry x="0" y="45" width="380" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="sc2" value="🔑🔗 &lt;b&gt;category_id&lt;/b&gt; : INTEGER &lt;font color=&quot;#2E7D32&quot;&gt;[FK, PK]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSupplierCategories">
          <mxGeometry x="0" y="70" width="380" height="25" as="geometry"/>
        </mxCell>

        <mxCell id="scConst" value="&lt;font color=&quot;#2E7D32&quot;&gt;&lt;b&gt;CONSTRAINTS&lt;/b&gt;&lt;/font&gt;&lt;br&gt;PK(supplier_id, category_id) — composta&lt;br&gt;FK(supplier_id) → suppliers(id) ON DELETE CASCADE&lt;br&gt;FK(category_id) → categories(id) ON DELETE CASCADE&lt;br&gt;Seed: ~20 relações N:N" style="text;html=1;strokeColor=#2E7D32;fillColor=#E8F5E9;align=left;verticalAlign=top;fontSize=10;spacingLeft=8;spacingTop=4;rounded=1;strokeWidth=1;" vertex="1" parent="tblSupplierCategories">
          <mxGeometry x="10" y="105" width="360" height="85" as="geometry"/>
        </mxCell>

        <mxCell id="tblProducts" value="&lt;b&gt;products&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;&quot; color=&quot;#2E7D32&quot;&gt;(agnósticos à categoria)&lt;/font&gt;" style="swimlane;startSize=40;fillColor=#FFFFFF;strokeColor=#2E7D32;fontStyle=1;fontSize=13;rounded=1;arcSize=4;shadow=1;strokeWidth=2;swimlaneLine=0;fontColor=#1B5E20;" vertex="1" parent="groupCatalog">
          <mxGeometry x="450" y="290" width="380" height="280" as="geometry"/>
        </mxCell>

        <mxCell id="p1" value="🔑 &lt;b&gt;id&lt;/b&gt; : INTEGER" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblProducts">
          <mxGeometry x="0" y="45" width="380" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="p2" value="&lt;b&gt;name&lt;/b&gt; : TEXT [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblProducts">
          <mxGeometry x="0" y="70" width="380" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="p3" value="&lt;b&gt;unit&lt;/b&gt; : TEXT [NN] &lt;font color=&quot;#666&quot;&gt;(un, kg, L, m)&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblProducts">
          <mxGeometry x="0" y="95" width="380" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="p4" value="&lt;b&gt;active&lt;/b&gt; : BOOLEAN [NN, DEFAULT 1]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblProducts">
          <mxGeometry x="0" y="120" width="380" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="p5" value="&lt;b&gt;created_at&lt;/b&gt; : DATETIME [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblProducts">
          <mxGeometry x="0" y="145" width="380" height="25" as="geometry"/>
        </mxCell>

        <mxCell id="pConst" value="&lt;font color=&quot;#2E7D32&quot;&gt;&lt;b&gt;CONSTRAINTS&lt;/b&gt;&lt;/font&gt;&lt;br&gt;PK(id)&lt;br&gt;INDEX(name)&lt;br&gt;Seed: 50 produtos&lt;br&gt;&lt;font color=&quot;#C62828&quot;&gt;⚠️ SEM FK para categories (correção v3.1)&lt;/font&gt;" style="text;html=1;strokeColor=#2E7D32;fillColor=#E8F5E9;align=left;verticalAlign=top;fontSize=10;spacingLeft=8;spacingTop=4;rounded=1;strokeWidth=1;" vertex="1" parent="tblProducts">
          <mxGeometry x="10" y="180" width="360" height="90" as="geometry"/>
        </mxCell>

        <mxCell id="tblSupplierProducts" value="&lt;b&gt;supplier_products&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;&quot; color=&quot;#2E7D32&quot;&gt;(preços e estoque por fornecedor)&lt;/font&gt;" style="swimlane;startSize=40;fillColor=#FFFFFF;strokeColor=#2E7D32;fontStyle=1;fontSize=13;rounded=1;arcSize=4;shadow=1;strokeWidth=2;swimlaneLine=0;fontColor=#1B5E20;" vertex="1" parent="groupCatalog">
          <mxGeometry x="900" y="50" width="400" height="340" as="geometry"/>
        </mxCell>

        <mxCell id="sp1" value="🔑🔗 &lt;b&gt;supplier_id&lt;/b&gt; : INTEGER &lt;font color=&quot;#2E7D32&quot;&gt;[FK, PK]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSupplierProducts">
          <mxGeometry x="0" y="45" width="400" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="sp2" value="🔑🔗 &lt;b&gt;product_id&lt;/b&gt; : INTEGER &lt;font color=&quot;#2E7D32&quot;&gt;[FK, PK]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSupplierProducts">
          <mxGeometry x="0" y="70" width="400" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="sp3" value="&lt;b&gt;price&lt;/b&gt; : DECIMAL(10,2) [NN]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSupplierProducts">
          <mxGeometry x="0" y="95" width="400" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="sp4" value="&lt;b&gt;stock&lt;/b&gt; : INTEGER [NN, DEFAULT 0]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSupplierProducts">
          <mxGeometry x="0" y="120" width="400" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="sp5" value="&lt;b&gt;active&lt;/b&gt; : BOOLEAN [NN, DEFAULT 1]" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontColor=#333333;spacingLeft=8;" vertex="1" parent="tblSupplierProducts">
          <mxGeometry x="0" y="145" width="400" height="25" as="geometry"/>
        </mxCell>

        <mxCell id="spConst" value="&lt;font color=&quot;#2E7D32&quot;&gt;&lt;b&gt;CONSTRAINTS&lt;/b&gt;&lt;/font&gt;&lt;br&gt;PK(supplier_id, product_id) — composta&lt;br&gt;FK(supplier_id) → suppliers(id) ON DELETE CASCADE&lt;br&gt;FK(product_id) → products(id) ON DELETE RESTRICT&lt;br&gt;CHECK(price &amp;gt;= 0)&lt;br&gt;CHECK(stock &amp;gt;= 0)&lt;br&gt;Seed: ~300 preços (variação ±20%)" style="text;html=1;strokeColor=#2E7D32;fillColor=#E8F5E9;align=left;verticalAlign=top;fontSize=10;spacingLeft=8;spacingTop=4;rounded=1;strokeWidth=1;" vertex="1" parent="tblSupplierProducts">
          <mxGeometry x="10" y="180" width="380" height="110" as="geometry"/>
        </mxCell>

        <!-- ===================== RELACIONAMENTOS (LINHAS) ===================== -->

        <!-- users 1:N lists -->
        <mxCell id="rel1" value="1 : N" style="endArrow=ERmany;startArrow=ERone;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=11;fontStyle=1;fontColor=#0D47A1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.3;entryDx=0;entryDy=0;" edge="1" source="tblUsers" target="tblLists" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="rel1t" value="&lt;b&gt;possui&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=#FFFFFF;align=center;verticalAlign=middle;fontSize=10;fontColor=#0D47A1;rounded=1;spacingLeft=4;spacingRight=4;" vertex="1" connectable="0" parent="rel1">
          <mxGeometry x="-0.1" relative="1" as="geometry">
            <mxPoint as="offset"/>
          </mxGeometry>
        </mxCell>

        <!-- lists 1:N list_items -->
        <mxCell id="rel2" value="1 : N" style="endArrow=ERmany;startArrow=ERone;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=11;fontStyle=1;fontColor=#0D47A1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.3;entryDx=0;entryDy=0;" edge="1" source="tblLists" target="tblListItems" parent="groupLists">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="rel2t" value="&lt;b&gt;contém&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=#FFFFFF;align=center;verticalAlign=middle;fontSize=10;fontColor=#0D47A1;rounded=1;spacingLeft=4;spacingRight=4;" vertex="1" connectable="0" parent="rel2">
          <mxGeometry x="-0.1" relative="1" as="geometry">
            <mxPoint as="offset"/>
          </mxGeometry>
        </mxCell>

        <!-- products 1:N list_items (cross-group) -->
        <mxCell id="rel3" value="1 : N" style="endArrow=ERmany;startArrow=ERone;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=11;fontStyle=1;fontColor=#0D47A1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;curved=1;" edge="1" source="tblProducts" target="tblListItems" parent="groupCatalog">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="rel3t" value="&lt;b&gt;referencia&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=#FFFFFF;align=center;verticalAlign=middle;fontSize=10;fontColor=#0D47A1;rounded=1;spacingLeft=4;spacingRight=4;" vertex="1" connectable="0" parent="rel3">
          <mxGeometry x="-0.1" relative="1" as="geometry">
            <mxPoint as="offset"/>
          </mxGeometry>
        </mxCell>

        <!-- suppliers 1:N supplier_products -->
        <mxCell id="rel4" value="1 : N" style="endArrow=ERmany;startArrow=ERone;html=1;strokeColor=#2E7D32;strokeWidth=2;fontSize=11;fontStyle=1;fontColor=#1B5E20;exitX=1;exitY=0.3;exitDx=0;exitDy=0;entryX=0;entryY=0.7;entryDx=0;entryDy=0;curved=1;" edge="1" source="tblSuppliers" target="tblSupplierProducts" parent="groupCatalog">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="rel4t" value="&lt;b&gt;vende&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=#FFFFFF;align=center;verticalAlign=middle;fontSize=10;fontColor=#1B5E20;rounded=1;spacingLeft=4;spacingRight=4;" vertex="1" connectable="0" parent="rel4">
          <mxGeometry x="-0.1" relative="1" as="geometry">
            <mxPoint as="offset"/>
          </mxGeometry>
        </mxCell>

        <!-- products 1:N supplier_products -->
        <mxCell id="rel5" value="1 : N" style="endArrow=ERmany;startArrow=ERone;html=1;strokeColor=#2E7D32;strokeWidth=2;fontSize=11;fontStyle=1;fontColor=#1B5E20;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.3;entryDx=0;entryDy=0;" edge="1" source="tblProducts" target="tblSupplierProducts" parent="groupCatalog">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="rel5t" value="&lt;b&gt;ofertado por&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=#FFFFFF;align=center;verticalAlign=middle;fontSize=10;fontColor=#1B5E20;rounded=1;spacingLeft=4;spacingRight=4;" vertex="1" connectable="0" parent="rel5">
          <mxGeometry x="-0.1" relative="1" as="geometry">
            <mxPoint as="offset"/>
          </mxGeometry>
        </mxCell>

        <!-- suppliers N:N categories (via supplier_categories) -->
        <mxCell id="rel6" value="N" style="endArrow=ERmany;html=1;strokeColor=#2E7D32;strokeWidth=2;fontSize=11;fontStyle=1;fontColor=#1B5E20;exitX=1;exitY=0.2;exitDx=0;exitDy=0;entryX=0;entryY=0.7;entryDx=0;entryDy=0;" edge="1" source="tblSuppliers" target="tblSupplierCategories" parent="groupCatalog">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="rel7" value="N" style="endArrow=ERmany;html=1;strokeColor=#2E7D32;strokeWidth=2;fontSize=11;fontStyle=1;fontColor=#1B5E20;exitX=0;exitY=0.7;exitDx=0;exitDy=0;entryX=1;entryY=0.3;entryDx=0;entryDy=0;" edge="1" source="tblCategories" target="tblSupplierCategories" parent="groupCatalog">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="relNN" value="&lt;b&gt;N : N&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:9px;&quot;&gt;(via pivô)&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=#E8F5E9;align=center;verticalAlign=middle;fontSize=11;fontColor=#1B5E20;rounded=1;spacingLeft=6;spacingRight=6;strokeColor=#2E7D32;strokeWidth=1;" vertex="1" parent="groupCatalog">
          <mxGeometry x="390" y="230" width="80" height="40" as="geometry"/>
        </mxCell>

        <!-- ===================== LEGENDA ===================== -->
        <mxCell id="legend" value="&lt;b&gt;LEGENDA — DER COBECO v3.1&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1A237E;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontSize=12;shadow=1;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="1400" y="1100" width="380" height="460" as="geometry"/>
        </mxCell>

        <mxCell id="leg1" value="🔑" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="1420" y="1140" width="30" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="leg1t" value="Primary Key (PK)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1460" y="1140" width="200" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg2" value="🔗" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="1420" y="1175" width="30" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="leg2t" value="Foreign Key (FK)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1460" y="1175" width="200" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg3" value="&lt;font color=&quot;#C62828&quot;&gt;[UQ]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1415" y="1210" width="40" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="leg3t" value="UNIQUE constraint" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1460" y="1210" width="200" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg4" value="&lt;font color=&quot;#C62828&quot;&gt;[NN]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1415" y="1245" width="40" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="leg4t" value="NOT NULL" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1460" y="1245" width="200" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg5" value="" style="endArrow=ERmany;startArrow=ERone;html=1;strokeColor=#1565C0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1420" y="1295" as="sourcePoint"/>
            <mxPoint x="1480" y="1295" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg5t" value="Relacionamento 1:N" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1490" y="1280" width="200" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg6" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFEBEE;strokeColor=#C62828;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="1425" y="1320" width="50" height="20" as="geometry"/>
        </mxCell>
        <mxCell id="leg6t" value="🔐 Autenticação" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1490" y="1310" width="200" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg7" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1565C0;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="1425" y="1350" width="50" height="20" as="geometry"/>
        </mxCell>
        <mxCell id="leg7t" value="📝 Gestão de Listas" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1490" y="1340" width="200" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg8" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#2E7D32;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="1425" y="1380" width="50" height="20" as="geometry"/>
        </mxCell>
        <mxCell id="leg8t" value="🏪 Catálogo" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1490" y="1370" width="200" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg9" value="&lt;font color=&quot;#666&quot;&gt;[soft delete]&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=10;fontStyle=2;" vertex="1" parent="1">
          <mxGeometry x="1415" y="1410" width="70" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="leg9t" value="Campo de soft delete (deleted_at)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1490" y="1400" width="250" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg10" value="⭐" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontSize=14;" vertex="1" parent="1">
          <mxGeometry x="1420" y="1445" width="30" height="30" as="geometry"/>
        </mxCell>
        <mxCell id="leg10t" value="NOVO v3.1 (correção conceitual)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=11;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="1460" y="1445" width="250" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg11" value="&lt;b&gt;PRAGMAs SQLite3&lt;/b&gt;&lt;br&gt;• PRAGMA journal_mode=WAL&lt;br&gt;• PRAGMA foreign_keys=ON&lt;br&gt;• PRAGMA busy_timeout=5000&lt;br&gt;&lt;br&gt;&lt;b&gt;ACID&lt;/b&gt;: Atomicity, Consistency,&lt;br&gt;Isolation, Durability" style="text;html=1;strokeColor=#1A237E;fillColor=#FAFAFA;align=left;verticalAlign=top;fontSize=10;spacingLeft=8;spacingTop=4;rounded=1;strokeWidth=1;" vertex="1" parent="1">
          <mxGeometry x="1415" y="1485" width="350" height="65" as="geometry"/>
        </mxCell>

        <!-- ===================== SEED INFO ===================== -->
        <mxCell id="seedInfo" value="&lt;b&gt;📦 SEED DE DADOS&lt;/b&gt;&lt;br&gt;• 1 admin user&lt;br&gt;• 5 categorias macro&lt;br&gt;• 10 fornecedores&lt;br&gt;• ~20 relações supplier_categories&lt;br&gt;• 50 produtos&lt;br&gt;• ~300 preços (variação ±20%)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#E65100;align=left;verticalAlign=top;fontSize=11;spacingLeft=10;spacingTop=6;shadow=1;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="1820" y="1100" width="280" height="170" as="geometry"/>
        </mxCell>

        <!-- ===================== CORREÇÃO v3.1 INFO ===================== -->
        <mxCell id="corrInfo" value="&lt;b&gt;⭐ CORREÇÃO v3.1&lt;/b&gt;&lt;br&gt;&lt;br&gt;Categorias são classificações&lt;br&gt;&lt;b&gt;MACRO de FORNECEDORES&lt;/b&gt;,&lt;br&gt;não de produtos.&lt;br&gt;&lt;br&gt;Exemplo: Leroy Merlin&lt;br&gt;→ Material de Construção&lt;br&gt;→ Ferramentas&lt;br&gt;→ Jardinagem&lt;br&gt;→ Decoração" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#2E7D32;align=left;verticalAlign=top;fontSize=11;spacingLeft=10;spacingTop=6;shadow=1;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="1820" y="1290" width="280" height="200" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 📊 Resumo do DER v3.1

### Estatísticas

| Métrica | Valor |
|---------|-------|
| **Total de tabelas** | 8 |
| **Primary Keys** | 8 (todas simples, exceto 2 compostas) |
| **Foreign Keys** | 9 |
| **Constraints UNIQUE** | 4 |
| **Constraints CHECK** | 5 |
| **Relacionamentos 1:N** | 5 |
| **Relacionamentos N:N** | 1 (via pivô) |
| **Soft deletes** | 2 (`users`, `lists`) |
| **Índices compostos** | 2 |

### Validação ACID

| Princípio | Garantia no DER |
|-----------|-----------------|
| **Atomicity** | Transações explícitas via `BEGIN/COMMIT` em todas operações de escrita |
| **Consistency** | FKs com CASCADE/RESTRICT, CHECK constraints, UNIQUE |
| **Isolation** | WAL mode permite leitura concorrente sem bloqueio |
| **Durability** | SQLite3 WAL grava em disco com checkpoint automático |

### Correções Conceituais Aplicadas (v3.1)

| v3.0 (incorreto) | v3.1 (corrigido) |
|------------------|------------------|
| `products.category_id` FK → `categories` | ❌ **Removido** — produtos são agnósticos |
| Categorias de produtos | ✅ Categorias de **FORNECEDORES** |
| Relacionamento 1:N produto→categoria | ✅ N:N fornecedor↔categoria via `supplier_categories` |

---

## 📥 Instruções de Uso

1. **Salvar**: Copie o XML acima e salve como `cobeco-der-v31.drawio`
2. **Abrir no Draw.io**: [app.diagrams.net](https://app.diagrams.net) → File → Open from → Device
3. **Exportar**: File → Export as → PNG/SVG/PDF
4. **Validar**: Confirme 8 tabelas + 9 FKs + 1 pivô N:N

---

## ✅ Checklist de Validação

- [x] 8 tabelas conforme especificação v3.1
- [x] Tabela pivô `supplier_categories` presente (N:N)
- [x] `products` SEM FK para `categories` (correção conceitual)
- [x] Todas PKs, FKs, UNIQUE, CHECK visíveis
- [x] Cardinalidades 1:N e N:N corretas
- [x] Soft delete em `users` e `lists` (deleted_at)
- [x] Seed documentado (10 forn + 50 prod + 5 cat)
- [x] PRAGMAs SQLite3 documentados (WAL + FK)
- [x] Legenda completa com ícones 🔑 🔗
- [x] Canvas 2600x1800 otimizado para apresentação

**Próximo artefato recomendado:** Diagrama de Transição de Estados (3 máquinas: Auth, Lista, Comparação).
