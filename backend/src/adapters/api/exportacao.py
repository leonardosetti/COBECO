# COBECO Backend — Exportação Router (FastAPI)
# Endpoints: POST /v1/export/pdf (RF17) - ReportLab server-side

import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.api.auth import get_current_user, get_current_user_optional
from src.adapters.db.database import get_db
from src.adapters.db.models import ItemListaModel, ListaModel, ProdutoModel
from src.domain.repositories import ExportacaoRepository

router = APIRouter(tags=["Exportação"])


# ============================================================
# Repository Implementations
# ============================================================
class ExportacaoRepositoryImpl(ExportacaoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def gerar_pdf_lista(self, lista_id: int) -> bytes:
        """Gera PDF da lista salva (ReportLab server-side)"""
        from reportlab.lib.colors import HexColor, grey, white  # type: ignore[import-untyped]
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT  # type: ignore[import-untyped]
        from reportlab.lib.pagesizes import A4  # type: ignore[import-untyped]
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # type: ignore[import-untyped]
        from reportlab.lib.units import cm  # type: ignore[import-untyped]
        from reportlab.platypus import (  # type: ignore[import-untyped]
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )

        # Busca dados da lista
        resultado = await self.session.execute(select(ListaModel).where(ListaModel.id == lista_id))
        lista = resultado.scalar_one_or_none()
        if not lista:
            raise HTTPException(status_code=404, detail="Lista não encontrada")

        itens_result = await self.session.execute(
            select(ItemListaModel).where(ItemListaModel.lista_id == lista_id)
        )
        itens = list(itens_result.scalars().all())

        if not itens:
            raise HTTPException(status_code=400, detail="Lista vazia")

        produto_ids = [item.produto_id for item in itens]
        produtos_result = await self.session.execute(
            select(ProdutoModel).where(ProdutoModel.id.in_(produto_ids))
        )
        produtos_map = {p.id: p for p in produtos_result.scalars().all()}

        # Busca fornecedores e preços para comparação completa (opcional)
        orcamento = None
        try:
            from src.adapters.api.comparacao import ComparacaoRepositoryImpl
            from src.adapters.db.models import FornecedorModel

            comp_repo = ComparacaoRepositoryImpl(self.session)
            # Buscar todos os fornecedores ativos para comparação
            fornecedores_result = await self.session.execute(
                select(FornecedorModel).where(FornecedorModel.ativo)
            )
            fornecedor_ids = [f.id for f in fornecedores_result.scalars().all()]
            if len(fornecedor_ids) >= 2:
                orcamento = await comp_repo.calcular_orcamento(lista_id, fornecedor_ids, 0.0)
        except Exception:
            orcamento = None  # Sem comparação se falhar

        # ============================================================
        # Gera PDF com ReportLab
        # ============================================================
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=styles["Title"],
                fontSize=18,
                spaceAfter=6,
                alignment=TA_CENTER,
                textColor=HexColor("#1a1a2e"),
            )
        )
        styles.add(
            ParagraphStyle(
                name="CustomSubtitle",
                parent=styles["Normal"],
                fontSize=11,
                spaceAfter=12,
                alignment=TA_CENTER,
                textColor=HexColor("#444"),
            )
        )
        styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=styles["Heading2"],
                fontSize=13,
                spaceBefore=16,
                spaceAfter=8,
                textColor=HexColor("#1a1a2e"),
                borderWidth=0,
                borderPadding=0,
            )
        )
        styles.add(
            ParagraphStyle(
                name="TableHeader",
                parent=styles["Normal"],
                fontSize=9,
                textColor=white,
                alignment=TA_CENTER,
            )
        )
        styles.add(
            ParagraphStyle(
                name="TableCell",
                parent=styles["Normal"],
                fontSize=8,
                alignment=TA_LEFT,
            )
        )
        styles.add(
            ParagraphStyle(
                name="TableCellCenter",
                parent=styles["Normal"],
                fontSize=8,
                alignment=TA_CENTER,
            )
        )
        styles.add(
            ParagraphStyle(
                name="TableCellRight",
                parent=styles["Normal"],
                fontSize=8,
                alignment=TA_RIGHT,
            )
        )

        story = []

        # --- Header ---
        story.append(Paragraph("COBECO — Cotação de Bens de Consumo", styles["CustomTitle"]))
        story.append(Paragraph(f"Lista: {lista.nome}", styles["CustomSubtitle"]))
        story.append(
            Paragraph(
                f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                styles["CustomSubtitle"],
            )
        )
        story.append(Spacer(1, 12))

        # --- Tabela de Itens da Lista ---
        story.append(Paragraph("Itens da Lista", styles["SectionHeader"]))

        # Cabeçalho
        headers = ["Produto", "Un.", "Qtd."]
        col_widths = [11 * cm, 2 * cm, 2 * cm]

        table_data = [headers]
        for item in itens:
            produto = produtos_map.get(item.produto_id)
            table_data.append(
                [
                    Paragraph(produto.nome if produto else "Desconhecido", styles["TableCell"]),
                    Paragraph(produto.unidade if produto else "un", styles["TableCellCenter"]),
                    Paragraph(str(item.quantidade), styles["TableCellCenter"]),
                ]
            )

        tabela_itens = Table(table_data, colWidths=col_widths, repeatRows=1)
        tabela_itens.setStyle(
            TableStyle(
                [
                    # Header
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    ("TOPPADDING", (0, 0), (-1, 0), 8),
                    # Body
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                    ("TOPPADDING", (0, 1), (-1, -1), 6),
                    # Grid
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#ddd")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    # Alternating rows
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f9f9f9")]),
                ]
            )
        )
        story.append(tabela_itens)

        # --- Total consolidado (preços do fornecedor vencedor, se houver comparação) ---
        if orcamento and orcamento.fornecedores:
            vencedor = next((f for f in orcamento.fornecedores if f.eh_melhor), None)
            if vencedor is None:
                vencedor = orcamento.fornecedores[0]
            total_txt = (
                f"R$ {vencedor.preco_total:,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )
            total_box = Table(
                [
                    [
                        Paragraph(
                            f"Total consolidado da compra "
                            f"({vencedor.itens_disponiveis} itens · {sum(i.quantidade for i in vencedor.itens)} unidades)",
                            ParagraphStyle(
                                "TotalLabel",
                                parent=styles["Normal"],
                                fontSize=10,
                                alignment=TA_LEFT,
                                textColor=white,
                            ),
                        ),
                        Paragraph(
                            total_txt,
                            ParagraphStyle(
                                "TotalValue",
                                parent=styles["Normal"],
                                fontSize=16,
                                alignment=TA_RIGHT,
                                textColor=white,
                            ),
                        ),
                    ]
                ],
                colWidths=[11 * cm, 5 * cm],
            )
            total_box.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#1E7D32")),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                        ("TOPPADDING", (0, 0), (-1, -1), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                        ("LEFTPADDING", (0, 0), (-1, -1), 14),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                    ]
                )
            )
            story.append(Spacer(1, 16))
            story.append(total_box)

        # --- Footer ---
        story.append(Spacer(1, 24))
        story.append(
            Paragraph(
                "COBECO MVP — FATEC Taquaritinga — Análise e Desenvolvimento de Sistemas",
                ParagraphStyle(
                    "Footer",
                    parent=styles["Normal"],
                    fontSize=7,
                    alignment=TA_CENTER,
                    textColor=grey,
                ),
            )
        )
        story.append(
            Paragraph(
                "Dados mockados para fins acadêmicos — Não representa preços reais de mercado",
                ParagraphStyle(
                    "Footer2",
                    parent=styles["Normal"],
                    fontSize=7,
                    alignment=TA_CENTER,
                    textColor=grey,
                ),
            )
        )

        # Build
        doc.build(story)
        buffer.seek(0)
        return buffer.read()

    async def gerar_pdf_vencedora(self, orcamento) -> bytes:
        """RF17: PDF da LISTA VENCEDORA — apenas itens precificados do fornecedor
        campeão (maior cobertura; empate → menor total). Nunca a tabela comparativa."""
        from reportlab.lib.colors import HexColor, grey, white  # type: ignore[import-untyped]
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT  # type: ignore[import-untyped]
        from reportlab.lib.pagesizes import A4  # type: ignore[import-untyped]
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # type: ignore[import-untyped]
        from reportlab.lib.units import cm  # type: ignore[import-untyped]
        from reportlab.platypus import (  # type: ignore[import-untyped]
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )

        vencedor = next((f for f in orcamento.fornecedores if f.eh_melhor), None)
        if vencedor is None and orcamento.fornecedores:
            vencedor = orcamento.fornecedores[0]
        if vencedor is None:
            raise HTTPException(status_code=400, detail="Nenhum fornecedor na comparação")

        cnpj_txt = "—"
        try:
            from src.adapters.db.models import FornecedorModel

            res = await self.session.execute(
                select(FornecedorModel.cnpj).where(FornecedorModel.id == vencedor.fornecedor_id)
            )
            cnpj_txt = res.scalar_one_or_none() or "—"
        except Exception:
            cnpj_txt = "—"

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=styles["Title"],
                fontSize=18,
                spaceAfter=6,
                alignment=TA_CENTER,
                textColor=HexColor("#1a1a2e"),
            )
        )
        styles.add(
            ParagraphStyle(
                name="CustomSubtitle",
                parent=styles["Normal"],
                fontSize=11,
                spaceAfter=4,
                alignment=TA_CENTER,
                textColor=HexColor("#444"),
            )
        )
        styles.add(
            ParagraphStyle(
                name="TableCell",
                parent=styles["Normal"],
                fontSize=9,
                alignment=TA_LEFT,
            )
        )
        styles.add(
            ParagraphStyle(
                name="TableCellCenter",
                parent=styles["Normal"],
                fontSize=9,
                alignment=TA_CENTER,
            )
        )
        styles.add(
            ParagraphStyle(
                name="TableCellRight",
                parent=styles["Normal"],
                fontSize=9,
                alignment=TA_RIGHT,
            )
        )

        story = []

        # --- Header ---
        story.append(Paragraph("COBECO — LISTA VENCEDORA — COTAÇÃO", styles["CustomTitle"]))
        story.append(Paragraph(f"Lista: {orcamento.lista_nome}", styles["CustomSubtitle"]))
        story.append(
            Paragraph(
                f"Melhor oferta: {vencedor.fornecedor_nome} — CNPJ {cnpj_txt}",
                styles["CustomSubtitle"],
            )
        )
        story.append(
            Paragraph(
                f"Cobertura: {vencedor.percentual_disponibilidade:.1f}% · "
                f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                styles["CustomSubtitle"],
            )
        )
        story.append(Spacer(1, 10))

        # --- Tabela de Itens Precificados ---
        headers = ["#", "Produto", "Un.", "Qtd", "Preço unit.", "Subtotal"]
        col_widths = [1 * cm, 6.5 * cm, 1.5 * cm, 1.5 * cm, 2.75 * cm, 2.75 * cm]

        table_data = [headers]
        ausentes = []
        for idx, item in enumerate(vencedor.itens, start=1):
            if item.disponivel:
                preco_unit = (
                    f"R$ {item.preco_unitario:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
                subtotal = (
                    f"R$ {item.preco_total:,.2f}".replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                )
            else:
                preco_unit = "N/D"
                subtotal = "N/D"
                ausentes.append(item.produto_nome)
            table_data.append(
                [
                    Paragraph(str(idx), styles["TableCellCenter"]),
                    Paragraph(item.produto_nome, styles["TableCell"]),
                    Paragraph(item.unidade, styles["TableCellCenter"]),
                    Paragraph(str(item.quantidade), styles["TableCellCenter"]),
                    Paragraph(preco_unit, styles["TableCellRight"]),
                    Paragraph(subtotal, styles["TableCellRight"]),
                ]
            )

        tabela = Table(table_data, colWidths=col_widths, repeatRows=1)
        tabela.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    ("TOPPADDING", (0, 0), (-1, 0), 8),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                    ("TOPPADDING", (0, 1), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#ddd")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, HexColor("#f9f9f9")]),
                ]
            )
        )
        story.append(tabela)
        story.append(Spacer(1, 12))

        if ausentes:
            story.append(
                Paragraph(
                    "⚠ Itens indisponíveis neste fornecedor: " + ", ".join(ausentes),
                    ParagraphStyle(
                        "Ausentes",
                        parent=styles["Normal"],
                        fontSize=8,
                        textColor=HexColor("#F57F17"),
                    ),
                )
            )
            story.append(Spacer(1, 8))

        # --- Total consolidado ---
        total_unidades = sum(i.quantidade for i in vencedor.itens)
        total_txt = (
            f"R$ {vencedor.preco_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        total_box = Table(
            [
                [
                    Paragraph(
                        f"Total consolidado da compra "
                        f"({vencedor.itens_disponiveis} itens · {total_unidades} unidades)",
                        ParagraphStyle(
                            "TotalLabel",
                            parent=styles["Normal"],
                            fontSize=10,
                            alignment=TA_LEFT,
                            textColor=white,
                        ),
                    ),
                    Paragraph(
                        total_txt,
                        ParagraphStyle(
                            "TotalValue",
                            parent=styles["Normal"],
                            fontSize=16,
                            alignment=TA_RIGHT,
                            textColor=white,
                        ),
                    ),
                ]
            ],
            colWidths=[11 * cm, 5 * cm],
        )
        total_box.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), HexColor("#1E7D32")),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("LEFTPADDING", (0, 0), (-1, -1), 14),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ]
            )
        )
        story.append(total_box)

        # --- Footer ---
        story.append(Spacer(1, 24))
        story.append(
            Paragraph(
                "Documento gerado por COBECO — sem valor fiscal",
                ParagraphStyle(
                    "Footer",
                    parent=styles["Normal"],
                    fontSize=7,
                    alignment=TA_CENTER,
                    textColor=grey,
                ),
            )
        )
        story.append(
            Paragraph(
                "Dados mockados para fins acadêmicos — Não representa preços reais de mercado",
                ParagraphStyle(
                    "Footer2",
                    parent=styles["Normal"],
                    fontSize=7,
                    alignment=TA_CENTER,
                    textColor=grey,
                ),
            )
        )

        # Build
        doc.build(story)
        buffer.seek(0)
        return buffer.read()


def get_exportacao_repo(
    session: AsyncSession = Depends(get_db),
) -> ExportacaoRepository:
    return ExportacaoRepositoryImpl(session)


# ============================================================
# Endpoints
# ============================================================
@router.post(
    "/pdf",
    summary="UC08/RF17 - Exportar Lista Salva em PDF",
)
async def exportar_pdf(
    lista_id: int,
    current_user=Depends(get_current_user),
    export_repo: ExportacaoRepository = Depends(get_exportacao_repo),
):
    """PDF da lista salva (dado do usuário — requer auth e propriedade)."""
    # Segurança: lista só pode ser exportada pelo seu proprietário
    lista_result = await export_repo.session.execute(
        select(ListaModel).where(
            ListaModel.id == lista_id,
            ListaModel.usuario_id == current_user.id,
            ListaModel.deletado_em.is_(None),
        )
    )
    if lista_result.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="Lista não encontrada")

    try:
        pdf_bytes = await export_repo.gerar_pdf_lista(lista_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar PDF: {str(e)}")

    filename = f"lista_{datetime.now().strftime('%Y%m%d')}.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(len(pdf_bytes)),
        },
    )


@router.post(
    "/pdf/vencedora",
    summary="UC08/RF17 - Exportar Lista Vencedora em PDF (visitante ou autenticado)",
)
async def exportar_pdf_vencedora(
    request: dict,
    current_user=Depends(get_current_user_optional),
    export_repo: ExportacaoRepository = Depends(get_exportacao_repo),
):
    """RF17: funciona para TODOS (sem login) quando itens vêm inline (lista efêmera).
    Fluxo com lista salva exige auth — lista é dado do usuário."""
    lista_id_val = request.get("lista_id")
    if not request.get("itens") and current_user is None:
        raise HTTPException(status_code=401, detail="Autenticação necessária")
    if not request.get("itens") and lista_id_val is None:
        raise HTTPException(status_code=400, detail="lista_id é obrigatório")

    try:
        comp_repo = ComparacaoRepositoryImpl(export_repo.session)
        if request.get("itens"):
            orcamento = await comp_repo.calcular_orcamento_itens(
                request["itens"],
                request.get("fornecedor_ids", []),
                request.get("disponibilidade_minima", 0.0),
                lista_nome=request.get("lista_nome") or "Lista",
            )
        else:
            orcamento = await comp_repo.calcular_orcamento(
                int(lista_id_val),
                request.get("fornecedor_ids", []),
                request.get("disponibilidade_minima", 0.0),
            )
        pdf_bytes = await export_repo.gerar_pdf_vencedora(orcamento)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar PDF: {str(e)}")

    filename = f"lista_{datetime.now().strftime('%Y%m%d')}.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(len(pdf_bytes)),
        },
    )
