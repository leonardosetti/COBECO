# COBECO Backend — Exportação Router (FastAPI)
# Endpoints: POST /v1/export/pdf (RF17) - ReportLab server-side

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
import io

from src.domain.repositories import ExportacaoRepository, ListaRepository, ComparacaoRepository
from src.adapters.db.models import (
    ListaModel, ItemListaModel, FornecedorModel, ProdutoModel,
    FornecedorProdutoModel, UsuarioModel
)
from src.adapters.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.adapters.api.auth import get_current_user, UsuarioRepositoryImpl

router = APIRouter(tags=["Exportação"])


# ============================================================
# Repository Implementations
# ============================================================
class ListaRepositoryImpl(ListaRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def buscar_por_id(self, lista_id: int, usuario_id: Optional[int] = None):
        query = select(ListaModel).where(ListaModel.id == lista_id, ListaModel.deletado_em.is_(None))
        if usuario_id:
            query = query.where(ListaModel.usuario_id == usuario_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


class ExportacaoRepositoryImpl(ExportacaoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def gerar_pdf_lista(self, lista_id: int) -> bytes:
        """Gera PDF da lista (RF17) - ReportLab server-side"""
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
        from reportlab.lib.colors import HexColor, white, black, grey
        from reportlab.lib import colors

        # Busca dados da lista
        lista = await self.session.execute(
            select(ListaModel).where(ListaModel.id == lista_id)
        )
        lista = lista.scalar_one_or_none()
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

        # Busca fornecedores e preços para comparação completa
        from src.adapters.api.comparacao import ComparacaoRepositoryImpl
        comp_repo = ComparacaoRepositoryImpl(self.session)
        orcamento = await comp_repo.calcular_orcamento(lista_id, [], 0.0)  # Sem filtro de fornecedores

        # ============================================================
        # Gera PDF com ReportLab
        # ============================================================
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm,
        )

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontSize=18,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=HexColor('#1a1a2e'),
        ))
        styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=HexColor('#444'),
        ))
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontSize=13,
            spaceBefore=16,
            spaceAfter=8,
            textColor=HexColor('#1a1a2e'),
            borderWidth=0,
            borderPadding=0,
        ))
        styles.add(ParagraphStyle(
            name='TableHeader',
            parent=styles['Normal'],
            fontSize=9,
            textColor=white,
            alignment=TA_CENTER,
        ))
        styles.add(ParagraphStyle(
            name='TableCell',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_LEFT,
        ))
        styles.add(ParagraphStyle(
            name='TableCellCenter',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
        ))
        styles.add(ParagraphStyle(
            name='TableCellRight',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_RIGHT,
        ))

        story = []

        # --- Header ---
        story.append(Paragraph("COBECO — Cotação de Bens de Consumo", styles['CustomTitle']))
        story.append(Paragraph(f"Lista: {lista.nome}", styles['CustomSubtitle']))
        story.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['CustomSubtitle']))
        story.append(Spacer(1, 12))

        # --- Tabela de Itens da Lista ---
        story.append(Paragraph("Itens da Lista", styles['SectionHeader']))

        # Cabeçalho
        headers = ['Produto', 'Un.', 'Qtd.']
        col_widths = [11*cm, 2*cm, 2*cm]

        table_data = [headers]
        for item in itens:
            produto = produtos_map.get(item.produto_id)
            table_data.append([
                Paragraph(produto.nome if produto else "Desconhecido", styles['TableCell']),
                Paragraph(produto.unidade if produto else "un", styles['TableCellCenter']),
                Paragraph(str(item.quantidade), styles['TableCellCenter']),
            ])

        tabela_itens = Table(table_data, colWidths=col_widths, repeatRows=1)
        tabela_itens.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a1a2e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            # Body
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#ddd')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # Alternating rows
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f9f9f9')]),
        ]))
        story.append(tabela_itens)
        story.append(Spacer(1, 16))

        # --- Tabela de Comparação (se houver fornecedores) ---
        if orcamento.fornecedores:
            story.append(Paragraph("Comparação de Fornecedores", styles['SectionHeader']))

            headers_comp = ['Fornecedor', 'Disponíveis', 'Ausentes', '% Disp.', 'Total (R$)']
            col_widths_comp = [6*cm, 2.5*cm, 2.5*cm, 2*cm, 3.5*cm]

            table_data_comp = [headers_comp]
            for f in orcamento.fornecedores:
                destaque = " ⭐ MELHOR" if f.eh_melhor else ""
                table_data_comp.append([
                    Paragraph(f"{f.fornecedor_nome}{destaque}", styles['TableCell']),
                    Paragraph(str(f.itens_disponiveis), styles['TableCellCenter']),
                    Paragraph(str(f.itens_ausentes), styles['TableCellCenter']),
                    Paragraph(f"{f.percentual_disponibilidade:.1f}%", styles['TableCellCenter']),
                    Paragraph(f"R$ {f.preco_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), styles['TableCellRight']),
                ])

            tabela_comp = Table(table_data_comp, colWidths=col_widths_comp, repeatRows=1)
            tabela_comp.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d5a27')),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('TOPPADDING', (0, 0), (-1, 0), 8),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#ddd')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f0f8f0')]),
                # Highlight best
                ('BACKGROUND', (0, 1), (-1, 1), HexColor('#e8f5e9') if orcamento.fornecedores[0].eh_melhor else HexColor('#f0f8f0')),
            ]))
            story.append(tabela_comp)

        # --- Footer ---
        story.append(Spacer(1, 24))
        story.append(Paragraph(
            "COBECO MVP — FATEC Taquaritinga — Análise e Desenvolvimento de Sistemas",
            ParagraphStyle('Footer', parent=styles['Normal'], fontSize=7, alignment=TA_CENTER, textColor=grey)
        ))
        story.append(Paragraph(
            "Dados mockados para fins acadêmicos — Não representa preços reais de mercado",
            ParagraphStyle('Footer2', parent=styles['Normal'], fontSize=7, alignment=TA_CENTER, textColor=grey)
        ))

        # Build
        doc.build(story)
        buffer.seek(0)
        return buffer.read()


def get_lista_repo(session: AsyncSession = Depends(get_db)) -> ListaRepository:
    return ListaRepositoryImpl(session)


def get_exportacao_repo(session: AsyncSession = Depends(get_db)) -> ExportacaoRepository:
    return ExportacaoRepositoryImpl(session)


# ============================================================
# Endpoints
# ============================================================
@router.post(
    "/pdf",
    summary="UC08/RF17 - Exportar Lista em PDF",
)
async def exportar_pdf(
    lista_id: int,
    current_user = Depends(get_current_user),
    export_repo: ExportacaoRepository = Depends(get_exportacao_repo),
):
    """Gera PDF da lista (funciona para visitantes - sem auth obrigatório)"""
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
        }
    )