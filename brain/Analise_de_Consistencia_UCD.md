# Análise de Consistência e Novo Diagrama de Casos de Uso

## 📋 Validação dos Requisitos Funcionais

### Mudanças Fundamentais Identificadas

| Aspecto          | Documento Original                    | Novo Documento (MVP)                             | Status      |
| ---------------- | ------------------------------------- | ------------------------------------------------ | ----------- |
| **Autenticação** | ❌ Sem cadastro/login                 | ✅ Cadastro, login, logout, recuperação de senha | ✅ Coerente |
| **Persistência** | ❌ Dados efêmeros (local)             | ✅ PostgreSQL com ACID                           | ✅ Coerente |
| **Listas**       | ❌ Não persistidas                    | ✅ CRUD completo com histórico                   | ✅ Coerente |
| **Comparação**   | ❌ Agrupamento complexo por cobertura | ✅ Tabela flat simplificada                      | ✅ Coerente |
| **Exportação**   | ❌ CSV, JSON, PDF                     | ✅ Apenas CSV + impressão                        | ✅ Coerente |

### Análise de Consistência dos RFs

**✅ Requisitos Coerentes com o MVP:**

- **RF01-05 (Autenticação)**: Completos e bem definidos com guard-rails apropriados
- **RF06-10 (Gestão de Listas)**: CRUD completo com validações e soft delete
- **RF11-12 (Comparação)**: Simplificados para tabela flat (adequado ao MVP)
- **RF13-14 (Exportação)**: Reduzidos a CSV + impressão (pragmático)

**⚠️ Pontos de Atenção:**

1. **RF11 (Calcular Orçamento)**: A simplificação para "tabela flat" elimina o agrupamento por cobertura descrito no documento original. Isso é uma **redução significativa de escopo**, mas está alinhado com a decisão de MVP simplificado.

2. **RF12 (Visualizar Resultados)**: Não menciona mais "itens faltantes com valor de referência" - isso foi removido na simplificação.

3. **Ausência de RF para "Limpar Sessão"**: No documento original havia UC14 (Limpar Sessão Local), mas no novo MVP isso não faz sentido pois os dados são persistidos no banco.

**Conclusão da Validação:** ✅ Requisitos coerentes com a proposta de MVP simplificado.

---

## 🎯 Novo Diagrama de Casos de Uso

Com base nas mudanças de escopo, criei um novo diagrama que reflete:

- **Autenticação completa** (3 novos casos de uso)
- **Gestão de listas persistida** (CRUD completo)
- **Comparação simplificada** (tabela flat)
- **Exportação reduzida** (CSV + impressão)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-08-31T00:00:00.000Z" agent="MVP Comparador de Compras" version="24.0.0" type="device">
  <diagram id="mvp-use-case-v2" name="Diagrama de Caso de Uso — MVP v2.0">
    <mxGraphModel dx="2400" dy="1600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2400" pageHeight="1600" math="0" shadow="1">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>

        <!-- ===================== TÍTULO ===================== -->
        <mxCell id="title" value="&lt;b&gt;Diagrama de Caso de Uso — Sistema Comparador de Compras (MVP v2.0)&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:11px;&quot; color=&quot;#666&quot;&gt;Versão com autenticação e persistência • 31/08/2026&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=18;fontColor=#1A237E;" vertex="1" parent="1">
          <mxGeometry x="600" y="20" width="1200" height="50" as="geometry"/>
        </mxCell>

        <!-- ===================== BOUNDARY DO SISTEMA ===================== -->
        <mxCell id="boundary" value="Sistema Comparador de Compras (MVP v2.0)" style="swimlane;startSize=35;fillColor=#FAFAFA;strokeColor=#1A237E;fontStyle=1;fontSize=15;rounded=1;arcSize=4;shadow=1;strokeWidth=2;swimlaneLine=0;" vertex="1" parent="1">
          <mxGeometry x="400" y="90" width="1600" height="1400" as="geometry"/>
        </mxCell>

        <!-- ===================== ATORES ===================== -->
        <mxCell id="actorUnauthenticated" value="Usuário Não&#xa;Autenticado" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontSize=14;fontStyle=1;fillColor=#FFEBEE;strokeColor=#C62828;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="120" y="200" width="50" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="actorAuthenticated" value="Usuário&#xa;Autenticado" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontSize=14;fontStyle=1;fillColor=#E8F5E9;strokeColor=#2E7D32;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="120" y="700" width="50" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="actorSystem" value="Sistema" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontSize=14;fontStyle=1;fillColor=#FFF3E0;strokeColor=#E65100;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="2150" y="200" width="50" height="100" as="geometry"/>
        </mxCell>

        <mxCell id="actorAPI" value="API Mock&#xa;de Fornecedores" style="shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fontSize=13;fontStyle=1;fillColor=#E3F2FD;strokeColor=#1565C0;strokeWidth=2;" vertex="1" parent="1">
          <mxGeometry x="2150" y="900" width="50" height="100" as="geometry"/>
        </mxCell>

        <!-- ===================== ÁREA 1 — AUTENTICAÇÃO ===================== -->
        <mxCell id="area1" value="AUTENTICAÇÃO" style="swimlane;startSize=28;fillColor=#FFEBEE;strokeColor=#C62828;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#B71C1C;swimlaneLine=0;shadow=0;" vertex="1" parent="boundary">
          <mxGeometry x="40" y="50" width="720" height="280" as="geometry"/>
        </mxCell>

        <mxCell id="UC01" value="UC01&#xa;Cadastrar-se" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C62828;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area1">
          <mxGeometry x="40" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC02" value="UC02&#xa;Realizar Login" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C62828;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area1">
          <mxGeometry x="270" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC03" value="UC03&#xa;Recuperar Senha" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C62828;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area1">
          <mxGeometry x="500" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC04" value="UC04&#xa;Realizar Logout" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#C62828;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area1">
          <mxGeometry x="270" y="170" width="180" height="70" as="geometry"/>
        </mxCell>

        <!-- ===================== ÁREA 2 — GESTÃO DE LISTAS ===================== -->
        <mxCell id="area2" value="GESTÃO DE LISTAS DE COMPRAS" style="swimlane;startSize=28;fillColor=#E3F2FD;strokeColor=#1565C0;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#0D47A1;swimlaneLine=0;shadow=0;" vertex="1" parent="boundary">
          <mxGeometry x="40" y="360" width="720" height="380" as="geometry"/>
        </mxCell>

        <mxCell id="UC05" value="UC05&#xa;Visualizar Perfil" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="40" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC06" value="UC06&#xa;Editar Perfil" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="40" y="170" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC07" value="UC07&#xa;Excluir Conta" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="40" y="280" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC08" value="UC08&#xa;Criar Lista de Compras" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="270" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC09" value="UC09&#xa;Listar Minhas Listas" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="270" y="170" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC10" value="UC10&#xa;Editar Lista" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="500" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC11" value="UC11&#xa;Excluir Lista" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="500" y="170" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC12" value="UC12&#xa;Buscar Produtos&#xa;(Autocomplete)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1565C0;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area2">
          <mxGeometry x="270" y="280" width="180" height="70" as="geometry"/>
        </mxCell>

        <!-- ===================== ÁREA 3 — COMPARAÇÃO E RESULTADOS ===================== -->
        <mxCell id="area3" value="COMPARAÇÃO E RESULTADOS" style="swimlane;startSize=28;fillColor=#E8F5E9;strokeColor=#2E7D32;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#1B5E20;swimlaneLine=0;shadow=0;" vertex="1" parent="boundary">
          <mxGeometry x="800" y="50" width="760" height="380" as="geometry"/>
        </mxCell>

        <mxCell id="UC13" value="UC13&#xa;Calcular Orçamento&#xa;(Tabela Flat)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#2E7D32;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area3">
          <mxGeometry x="40" y="60" width="200" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="UC14" value="UC14&#xa;Visualizar Resultados&#xa;(Tabela Comparativa)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#2E7D32;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area3">
          <mxGeometry x="280" y="60" width="200" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="UC15" value="UC15&#xa;Destacar Melhor Oferta" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#2E7D32;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area3">
          <mxGeometry x="520" y="60" width="200" height="80" as="geometry"/>
        </mxCell>

        <mxCell id="UC16" value="UC16&#xa;Visualizar Itens&#xa;Disponíveis/Ausentes" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#2E7D32;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area3">
          <mxGeometry x="280" y="180" width="200" height="80" as="geometry"/>
        </mxCell>

        <!-- ===================== ÁREA 4 — EXPORTAÇÃO ===================== -->
        <mxCell id="area4" value="EXPORTAÇÃO E IMPRESSÃO" style="swimlane;startSize=28;fillColor=#F3E5F5;strokeColor=#6A1B9A;rounded=1;arcSize=6;fontStyle=1;fontSize=13;fontColor=#4A148C;swimlaneLine=0;shadow=0;" vertex="1" parent="boundary">
          <mxGeometry x="800" y="460" width="760" height="280" as="geometry"/>
        </mxCell>

        <mxCell id="UC17" value="UC17&#xa;Exportar CSV" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6A1B9A;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area4">
          <mxGeometry x="80" y="80" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC18" value="UC18&#xa;Imprimir" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#6A1B9A;fontSize=12;fontStyle=1;shadow=1;strokeWidth=1.5;" vertex="1" parent="area4">
          <mxGeometry x="290" y="80" width="180" height="70" as="geometry"/>
        </mxCell>

        <!-- ===================== CASOS INTERNOS (AUXILIARES) ===================== -->
        <mxCell id="areaInternal" value="Casos de Uso Internos (Auxiliares de Domínio)" style="swimlane;startSize=28;fillColor=#F5F5F5;strokeColor=#616161;rounded=1;arcSize=6;fontStyle=1;fontSize=12;fontColor=#424242;swimlaneLine=0;shadow=0;dashed=1;dashPattern=8 4;" vertex="1" parent="boundary">
          <mxGeometry x="40" y="770" width="1520" height="280" as="geometry"/>
        </mxCell>

        <mxCell id="UC19" value="UC19&#xa;Validar Dados" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="80" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC20" value="UC20&#xa;Hash de Senha&#xa;(bcrypt)" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="300" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC21" value="UC21&#xa;Gerar Token JWT" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="520" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC22" value="UC22&#xa;Fornecer Catálogo&#xa;de Produtos" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="740" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC23" value="UC23&#xa;Fornecer Lista&#xa;de Fornecedores" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="960" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <mxCell id="UC24" value="UC24&#xa;Fornecer Preços" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;fontSize=11;fontStyle=2;shadow=0;strokeWidth=1.5;dashed=1;dashPattern=4 3;" vertex="1" parent="areaInternal">
          <mxGeometry x="1180" y="60" width="180" height="70" as="geometry"/>
        </mxCell>

        <!-- ===================== ASSOCIAÇÕES — USUÁRIO NÃO AUTENTICADO ===================== -->
        <mxCell id="a1" style="endArrow=none;html=1;strokeColor=#C62828;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorUnauthenticated" target="UC01" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a2" style="endArrow=none;html=1;strokeColor=#C62828;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorUnauthenticated" target="UC02" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a3" style="endArrow=none;html=1;strokeColor=#C62828;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorUnauthenticated" target="UC03" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== ASSOCIAÇÕES — USUÁRIO AUTENTICADO ===================== -->
        <mxCell id="a4" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.3;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC04" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a5" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC05" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a6" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC06" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a7" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC07" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a8" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC08" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a9" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC09" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a10" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC10" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a11" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC11" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a12" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC12" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a13" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC13" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a14" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC14" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a15" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC15" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a16" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC16" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a17" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC17" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="a18" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAuthenticated" target="UC18" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== ASSOCIAÇÕES — SISTEMA ===================== -->
        <mxCell id="b1" style="endArrow=none;html=1;strokeColor=#E65100;strokeWidth=1.5;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorSystem" target="UC19" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="b2" style="endArrow=none;html=1;strokeColor=#E65100;strokeWidth=1.5;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorSystem" target="UC20" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="b3" style="endArrow=none;html=1;strokeColor=#E65100;strokeWidth=1.5;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorSystem" target="UC21" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== ASSOCIAÇÕES — API MOCK ===================== -->
        <mxCell id="c1" style="endArrow=none;html=1;strokeColor=#1565C0;strokeWidth=1.5;exitX=0;exitY=0.3;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAPI" target="UC22" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="c2" style="endArrow=none;html=1;strokeColor=#1565C0;strokeWidth=1.5;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAPI" target="UC23" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="c3" style="endArrow=none;html=1;strokeColor=#1565C0;strokeWidth=1.5;exitX=0;exitY=0.7;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="actorAPI" target="UC24" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== RELAÇÕES <<include>> ===================== -->
        <mxCell id="inc1" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC01" target="UC19" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="inc2" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.3;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC01" target="UC20" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="inc3" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC02" target="UC21" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="inc4" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#BF360C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC13" target="UC19" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="inc5" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#0D47A1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC12" target="UC22" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="inc6" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#0D47A1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC13" target="UC23" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="inc7" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#1565C0;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#0D47A1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC13" target="UC24" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== RELAÇÕES <<extend>> ===================== -->
        <mxCell id="ext1" value="&lt;&lt;extend&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#6A1B9A;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#4A148C;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="UC15" target="UC14" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="ext2" value="&lt;&lt;extend&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#6A1B9A;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#4A148C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC17" target="UC14" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="ext3" value="&lt;&lt;extend&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#6A1B9A;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#4A148C;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.7;entryY=0;entryDx=0;entryDy=0;" edge="1" source="UC18" target="UC14" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <mxCell id="ext4" value="&lt;&lt;extend&gt;&gt;" style="endArrow=open;endSize=12;dashed=1;html=1;strokeColor=#6A1B9A;strokeWidth=2;fontSize=10;fontStyle=1;fontColor=#4A148C;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="UC06" target="UC05" parent="1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>

        <!-- ===================== LEGENDA ===================== -->
        <mxCell id="legend" value="&lt;b&gt;Legenda&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#1A237E;align=left;verticalAlign=top;spacingLeft=12;spacingTop=8;fontSize=12;shadow=1;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="120" y="1100" width="240" height="360" as="geometry"/>
        </mxCell>

        <mxCell id="leg1" value="" style="endArrow=none;html=1;strokeColor=#C62828;strokeWidth=2;exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="140" y="1150" as="sourcePoint"/>
            <mxPoint x="200" y="1150" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg1t" value="Associação — Usuário Não Autenticado" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="210" y="1135" width="150" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg2" value="" style="endArrow=none;html=1;strokeColor=#2E7D32;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="140" y="1190" as="sourcePoint"/>
            <mxPoint x="200" y="1190" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg2t" value="Associação — Usuário Autenticado" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="210" y="1175" width="150" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg3" value="" style="endArrow=none;html=1;strokeColor=#E65100;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="140" y="1230" as="sourcePoint"/>
            <mxPoint x="200" y="1230" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg3t" value="Associação — Sistema" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="210" y="1215" width="150" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg4" value="" style="endArrow=none;html=1;strokeColor=#1565C0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="140" y="1270" as="sourcePoint"/>
            <mxPoint x="200" y="1270" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg4t" value="Associação — API Mock" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="210" y="1255" width="150" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg5" value="&lt;&lt;include&gt;&gt;" style="endArrow=open;endSize=10;dashed=1;html=1;strokeColor=#E65100;strokeWidth=2;fontSize=9;fontStyle=1;fontColor=#BF360C;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="140" y="1310" as="sourcePoint"/>
            <mxPoint x="200" y="1310" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg5t" value="Inclusão (obrigatória)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="210" y="1295" width="150" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg6" value="&lt;&lt;extend&gt;&gt;" style="endArrow=open;endSize=10;dashed=1;html=1;strokeColor=#6A1B9A;strokeWidth=2;fontSize=9;fontStyle=1;fontColor=#4A148C;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="140" y="1350" as="sourcePoint"/>
            <mxPoint x="200" y="1350" as="targetPoint"/>
          </mxGeometry>
        </mxCell>
        <mxCell id="leg6t" value="Extensão (opcional)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="210" y="1335" width="150" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg7" value="" style="ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#616161;dashed=1;dashPattern=4 3;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="150" y="1390" width="40" height="25" as="geometry"/>
        </mxCell>
        <mxCell id="leg7t" value="Caso Interno (auxiliar)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="210" y="1385" width="150" height="30" as="geometry"/>
        </mxCell>

        <mxCell id="leg8" value="" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#FFEBEE;strokeColor=#C62828;strokeWidth=1.5;" vertex="1" parent="1">
          <mxGeometry x="150" y="1430" width="40" height="20" as="geometry"/>
        </mxCell>
        <mxCell id="leg8t" value="Área: Autenticação" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;fontSize=10;" vertex="1" parent="1">
          <mxGeometry x="210" y="1425" width="150" height="30" as="geometry"/>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

---

## 📊 Resumo das Mudanças no Diagrama

### ✅ Novos Casos de Uso Adicionados

| ID   | Caso de Uso       | Justificativa       |
| ---- | ----------------- | ------------------- |
| UC01 | Cadastrar-se      | Novo requisito RF01 |
| UC02 | Realizar Login    | Novo requisito RF02 |
| UC03 | Recuperar Senha   | Novo requisito RF04 |
| UC04 | Realizar Logout   | Novo requisito RF03 |
| UC05 | Visualizar Perfil | Novo requisito RF05 |
| UC06 | Editar Perfil     | Novo requisito RF05 |
| UC07 | Excluir Conta     | Novo requisito RF05 |

### ❌ Casos de Uso Removidos/Simplificados

| Caso Original                      | Status      | Justificativa                            |
| ---------------------------------- | ----------- | ---------------------------------------- |
| UC07 (Gerar Agrupamentos)          | ❌ Removido | Substituído por tabela flat simplificada |
| UC15 (Identificar Itens Faltantes) | ❌ Removido | Simplificado na visualização             |
| UC16 (Calcular Total Estimado)     | ❌ Removido | Não aplicável no MVP simplificado        |
| UC14 (Limpar Sessão Local)         | ❌ Removido | Dados agora são persistidos              |

### 🔄 Novos Atores

| Ator                    | Tipo       | Justificativa                              |
| ----------------------- | ---------- | ------------------------------------------ |
| Usuário Não Autenticado | Primário   | Separação clara de estados de autenticação |
| Usuário Autenticado     | Primário   | Acesso a funcionalidades protegidas        |
| Sistema                 | Secundário | Executa validações e operações automáticas |

### 🔗 Novas Relações

**<<include>> (7 relações):**

- UC01 → UC19 (Validar Dados)
- UC01 → UC20 (Hash de Senha)
- UC02 → UC21 (Gerar Token JWT)
- UC13 → UC19 (Validar Dados)
- UC12 → UC22 (Fornecer Catálogo)
- UC13 → UC23 (Fornecer Fornecedores)
- UC13 → UC24 (Fornecer Preços)

**<<extend>> (4 relações):**

- UC15 → UC14 (Destacar Melhor Oferta)
- UC17 → UC14 (Exportar CSV)
- UC18 → UC14 (Imprimir)
- UC06 → UC05 (Editar Perfil)

---

**Última atualização:** 31 de Agosto de 2026
