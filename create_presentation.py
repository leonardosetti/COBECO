#!/usr/bin/env python3
"""
COBECO MVP - Presentation Generator
Creates a professional PowerPoint presentation for the project.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import os

# ─── Color Palette ───
COLOR_PRIMARY = RGBColor(0x1E, 0x40, 0xAF)    # Blue-600
COLOR_SECONDARY = RGBColor(0x05, 0x96, 0x69)  # Emerald-600
COLOR_ACCENT = RGBColor(0xDC, 0x26, 0x26)     # Red-600
COLOR_BG = RGBColor(0xF8, 0xFA, 0xFC)         # Gray-50
COLOR_CARD = RGBColor(0xFF, 0xFF, 0xFF)       # White
COLOR_TEXT = RGBColor(0x1E, 0x29, 0x3B)       # Slate-800
COLOR_TEXT_LIGHT = RGBColor(0x64, 0x74, 0x8B) # Slate-500
COLOR_BORDER = RGBColor(0xE2, 0xE8, 0xF0)     # Slate-200

# ─── Helper Functions ───
def add_background(slide, color=COLOR_BG):
    """Set slide background color."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_shape_bg(slide, left, top, width, height, color=COLOR_CARD, border_color=None, border_width=None):
    """Add a rounded rectangle shape as background card."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = border_width or Pt(1)
    else:
        shape.line.fill.background()
    return shape

def add_text_box(slide, left, top, width, height, text, font_size=18, bold=False, color=COLOR_TEXT, alignment=PP_ALIGN.LEFT, font_name='Calibri'):
    """Add a text box with formatted text."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_bullet_list(slide, left, top, width, height, items, font_size=16, color=COLOR_TEXT, bullet_color=None, spacing=Pt(6), font_name='Calibri'):
    """Add a bullet point list."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = font_name
        p.space_after = spacing
        p.level = 0
        # Add bullet character
        pPr = p._p.get_or_add_pPr()
        buChar = pPr.makeelement(qn('a:buChar'), {'char': '•'})
        pPr.append(buChar)
        if bullet_color:
            buClr = pPr.makeelement(qn('a:buClr'), {})
            srgbClr = buClr.makeelement(qn('a:srgbClr'), {'val': '%02X%02X%02X' % (bullet_color[0], bullet_color[1], bullet_color[2])})
            buClr.append(srgbClr)
            pPr.append(buClr)
    return txBox

def add_icon_circle(slide, left, top, size, icon_text, bg_color=COLOR_PRIMARY, font_color=RGBColor(0xFF, 0xFF, 0xFF), font_size=24):
    """Add a circle with icon/text inside."""
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = icon_text
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = font_color
    p.alignment = PP_ALIGN.CENTER
    tf.paragraphs[0].space_before = Pt(0)
    tf.paragraphs[0].space_after = Pt(0)
    return shape

def add_step_card(slide, left, top, width, height, step_num, title, description, color=COLOR_PRIMARY):
    """Add a step card with number, title, description."""
    # Card background
    card = add_shape_bg(slide, left, top, width, height, COLOR_CARD, COLOR_BORDER, Pt(1))
    
    # Step number circle
    circle_size = Inches(0.5)
    circle_left = left + Inches(0.3)
    circle_top = top + Inches(0.3)
    add_icon_circle(slide, circle_left, circle_top, circle_size, str(step_num), color, font_size=18)
    
    # Title
    add_text_box(slide, circle_left + circle_size + Inches(0.15), circle_top - Inches(0.05), width - Inches(1), Inches(0.4),
                 title, font_size=16, bold=True, color=COLOR_TEXT)
    
    # Description
    add_text_box(slide, circle_left + circle_size + Inches(0.15), circle_top + Inches(0.35), width - Inches(1), height - Inches(0.8),
                 description, font_size=13, color=COLOR_TEXT_LIGHT)
    
    return card

# ─── Create Presentation ───
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ─── SLIDE 1: TITLE SLIDE ───
slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
add_background(slide, COLOR_PRIMARY)

# Decorative line
line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(2.8), Inches(10.3), Pt(3))
line.fill.solid()
line.fill.fore_color.rgb = COLOR_SECONDARY
line.line.fill.background()

# Title
add_text_box(slide, Inches(1.5), Inches(1.2), Inches(10.3), Inches(1.5),
             "COBECO", font_size=56, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), alignment=PP_ALIGN.CENTER, font_name='Calibri')

# Subtitle
add_text_box(slide, Inches(1.5), Inches(3.1), Inches(10.3), Inches(0.8),
             "Comparação de Bens de Consumo — MVP", font_size=28, color=RGBColor(0xD1, 0xD5, 0xDB), alignment=PP_ALIGN.CENTER)

# Details
details = [
    "FATEC Taquaritinga — Análise e Desenvolvimento de Sistemas",
    "Orientadora: Profa. Thais Cristina Casagrande",
    "Equipe: Leonardo Setti, Fabrício Cabral, Nicholas Anthony, Eduardo Passarelli, Nicolas Mallouk",
    "2026"
]
y = Inches(4.2)
for d in details:
    add_text_box(slide, Inches(1.5), y, Inches(10.3), Inches(0.4),
                 d, font_size=16, color=RGBColor(0x94, 0xA3, 0xB8), alignment=PP_ALIGN.CENTER)
    y += Inches(0.35)

# ─── SLIDE 2: AGENDA ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)

add_text_box(slide, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.7),
             "AGENDA", font_size=36, bold=True, color=COLOR_PRIMARY)

agenda_items = [
    ("01", "Visão Geral & Problema", "Contexto, persona e proposta de valor"),
    ("02", "Arquitetura & Stack", "Clean Architecture, tecnologias e decisões técnicas"),
    ("03", "Fluxo do Usuário", "5 passos + autenticação tardia + dashboard"),
    ("04", "Funcionalidades-Chave", "18 RFs, 12 RNFs, regras de negócio críticas"),
    ("05", "Modelo de Dados", "DER, seed determinístico, relacionamentos"),
    ("06", "Qualidade & Entregáveis", "Testes, CI/CD, Docker, cobertura, replicabilidade"),
    ("07", "Próximos Passos", "Backlog pós-MVP e evolução do produto"),
]

y_start = Inches(1.4)
card_height = Inches(0.7)
gap = Inches(0.1)

for i, (num, title, desc) in enumerate(agenda_items):
    y = y_start + i * (card_height + gap)
    # Number circle
    add_icon_circle(slide, Inches(0.8), y + Inches(0.1), Inches(0.5), num, COLOR_PRIMARY, font_size=16)
    # Title
    add_text_box(slide, Inches(1.5), y + Inches(0.05), Inches(4), Inches(0.35),
                 title, font_size=18, bold=True, color=COLOR_TEXT)
    # Description
    add_text_box(slide, Inches(5.5), y + Inches(0.05), Inches(7), Inches(0.35),
                 desc, font_size=15, color=COLOR_TEXT_LIGHT)
    # Divider line
    if i < len(agenda_items) - 1:
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.5), y + card_height - Pt(1), Inches(10.5), Pt(1))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_BORDER
        line.line.fill.background()

# ─── SLIDE 3: PROBLEM & SOLUTION ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)

add_text_box(slide, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.7),
             "PROBLEMA & SOLUÇÃO", font_size=36, bold=True, color=COLOR_PRIMARY)

# Problem card
add_shape_bg(slide, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.2), COLOR_CARD, COLOR_ACCENT, Pt(2))
add_text_box(slide, Inches(1.1), Inches(1.7), Inches(5.2), Inches(0.5),
             "❌  PROBLEMA", font_size=22, bold=True, color=COLOR_ACCENT)
problems = [
    "Comerciantes e consumidores perdem tempo comparando preços manualmente em múltiplos fornecedores",
    "Não existe ferramenta unificada que agregue catálogos mockados e permita comparação lado a lado",
    "Processo de decisão de compra é ineficiente, propenso a erros e sem registro histórico",
    "Pequenos negócios (ex: restaurantes) compram semanalmente em 3+ mercados sem otimização",
]
add_bullet_list(slide, Inches(1.1), Inches(2.3), Inches(5.2), Inches(4), problems, font_size=15, color=COLOR_TEXT, bullet_color=(0xDC, 0x26, 0x26))

# Solution card
add_shape_bg(slide, Inches(7.0), Inches(1.5), Inches(5.8), Inches(5.2), COLOR_CARD, COLOR_SECONDARY, Pt(2))
add_text_box(slide, Inches(7.3), Inches(1.7), Inches(5.2), Inches(0.5),
             "✅  SOLUÇÃO — COBECO", font_size=22, bold=True, color=COLOR_SECONDARY)
solutions = [
    "MVP desktop-first para comparação inteligente de preços de listas de compras",
    "Fluxo de 5 passos: Categorias → Lista → Fornecedores → Comparação → Lista Vencedora/PDF",
    "Autenticação tardia: visitante percorre todo fluxo sem login; auth só para salvar",
    "Motor de comparação: tabela flat, slider de disponibilidade (0-100%), destaque da melhor oferta",
    "Exportação PDF server-side (ReportLab) apenas da lista vencedora — nunca tabela comparativa",
    "Stack minimalista: Vanilla JS + Tailwind + FastAPI + MySQL 8.0 (InnoDB) + Docker",
]
add_bullet_list(slide, Inches(7.3), Inches(2.3), Inches(5.2), Inches(4.5), solutions, font_size=15, color=COLOR_TEXT, bullet_color=(0x05, 0x96, 0x69))

# Persona
add_text_box(slide, Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.5),
             "👤 Persona: Mariana Duarte, 34 — dona do restaurante \"Tempero da Mari\" (Taquaritinga/SP). Compra semanal de insumos em 3 mercados.",
             font_size=14, color=COLOR_TEXT_LIGHT, alignment=PP_ALIGN.CENTER)

# ─── SLIDE 4: ARCHITECTURE ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)

add_text_box(slide, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.7),
             "ARQUITETURA & STACK TECNOLÓGICA", font_size=36, bold=True, color=COLOR_PRIMARY)

# Architecture diagram (text-based)
arch_text = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                              COBECO MVP                                      │
├────────────────────────────────────┬────────────────────────────────────────┤
│  FRONTEND (Vanilla JS + Tailwind)  │  BACKEND (FastAPI - Clean Architecture)│
│  http://localhost:8380             │  http://localhost:8000                 │
│  • SPA Router (hash-based)         │  • Domain / UseCase / Adapter / Frame  │
│  • Tailwind CSS via CDN            │  • SQLAlchemy 2.0 + Pydantic 2.10      │
│  • Playwright E2E Tests            │  • JWT HS256 + bcrypt (salt=12)        │
│  • Desktop-only (≥1024px)          │  • ReportLab (PDF server-side)         │
└─────────────────────────────┬──────┴────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   MySQL 8.0       │
                    │   (InnoDB)        │
                    │   utf8mb4         │
                    │   ACID compliant  │
                    └───────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │    nginx Proxy    │
                    │  TLS ready        │
                    │  :8380 → :8000    │
                    └───────────────────┘
"""
txBox = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(4.5))
tf = txBox.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = arch_text
p.font.size = Pt(14)
p.font.name = 'Consolas'
p.font.color.rgb = COLOR_TEXT
p.space_after = Pt(0)
for para in tf.paragraphs[1:]:
    para.font.size = Pt(14)
    para.font.name = 'Consolas'
    para.font.color.rgb = COLOR_TEXT

# Stack table
add_text_box(slide, Inches(0.8), Inches(5.6), Inches(11.7), Inches(0.5),
             "STACK TECNOLÓGICO", font_size=20, bold=True, color=COLOR_PRIMARY)

stack_data = [
    ("Camada", "Tecnologia", "Versão/Detalhe"),
    ("Frontend", "Vanilla JS ES6+", "Tailwind CSS CDN, Playwright E2E"),
    ("Backend", "FastAPI", "0.115, Clean Architecture, OpenAPI 3.0"),
    ("Database", "MySQL", "8.0 InnoDB, aiomysql/pymysql, utf8mb4"),
    ("Auth", "JWT + bcrypt", "HS256, Access 15min (mem), Refresh 7d (httpOnly)"),
    ("PDF", "ReportLab", "Server-side, A4, <5s para ≤100 itens"),
    ("Proxy", "nginx", "Reverse proxy, rate limiting, TLS ready"),
    ("CI/CD", "GitHub Actions", "ruff + pytest + coverage ≥80% + Docker build"),
    ("Container", "Docker Compose", "MySQL + migrations + seed + backend + frontend + proxy"),
]

table = slide.shapes.add_table(len(stack_data), 3, Inches(0.8), Inches(6.1), Inches(11.7), Inches(1.2)).table
table.columns[0].width = Inches(1.8)
table.columns[1].width = Inches(2.5)
table.columns[2].width = Inches(7.4)

for row_idx, row_data in enumerate(stack_data):
    for col_idx, cell_text in enumerate(row_data):
        cell = table.cell(row_idx, col_idx)
        cell.text = cell_text
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(12)
            paragraph.font.name = 'Calibri'
            if row_idx == 0:
                paragraph.font.bold = True
                paragraph.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                paragraph.font.color.rgb = COLOR_TEXT
        if row_idx == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_PRIMARY
        elif row_idx % 2 == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0xF1, 0xF5, 0xF9)

# ─── SLIDE 5: USER FLOW ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)

add_text_box(slide, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.7),
             "FLUXO DO USUÁRIO — 5 PASSOS + AUTENTICAÇÃO TARDIA", font_size=32, bold=True, color=COLOR_PRIMARY)

# Flow steps
steps = [
    ("1", "CATEGORIAS\n(Pré-filtro)", "11 categorias macro\nCheckboxes múltipla escolha\nMínimo 1 categoria\nFornecedores filtrados dinamicamente", "RF12"),
    ("2", "LISTA\n(Em memória)", "Nome + itens (produto + qtd)\nAutocomplete de 50 produtos\nValidação existência\nsessionStorage (efêmera)", "RF07"),
    ("3", "FORNECEDORES\n(Seleção)", "Filtrados por categorias\n10 fornecedores reais\n% disponibilidade por item\nSlider 0-100% + checkboxes\nMínimo 2 fornecedores", "RF13", "RF14"),
    ("4", "COMPARAÇÃO\n(Tabela flat)", "Itens disponíveis/ausentes\nPreço total ordenado ASC\nMelhor oferta: maior cobertura\nEmpate → menor custo total\nTooltip itens ausentes", "RF15", "RF16"),
    ("5", "VENCEDORA/PDF\n(Exportação)", "Apenas lista do campeão\nItens precificados + total\nPDF server-side ReportLab\nFunciona sem login (visitante)\n@media print otimizado", "RF17", "RF18"),
]

card_width = Inches(2.3)
card_height = Inches(4.5)
start_x = Inches(0.5)
start_y = Inches(1.4)
gap_x = Inches(0.25)

for i, step_data in enumerate(steps):
    x = start_x + i * (card_width + gap_x)
    step_num, title, desc, *rf_ids = step_data
    color = COLOR_PRIMARY if i < 4 else COLOR_SECONDARY
    
    # Card
    card = add_shape_bg(slide, x, start_y, card_width, card_height, COLOR_CARD, COLOR_BORDER, Pt(1))
    
    # Step number
    circle_size = Inches(0.6)
    add_icon_circle(slide, x + (card_width - circle_size) / 2, start_y + Inches(0.2), circle_size, step_num, color, font_size=22)
    
    # Title
    add_text_box(slide, x + Inches(0.15), start_y + Inches(0.95), card_width - Inches(0.3), Inches(0.7),
                 title, font_size=16, bold=True, color=COLOR_TEXT, alignment=PP_ALIGN.CENTER)
    
    # Description
    add_text_box(slide, x + Inches(0.15), start_y + Inches(1.7), card_width - Inches(0.3), Inches(2.5),
                 desc, font_size=12, color=COLOR_TEXT_LIGHT, alignment=PP_ALIGN.LEFT)
    
    # RF badges
    badge_y = start_y + Inches(4.1)
    for j, rf in enumerate(rf_ids):
        badge_x = x + Inches(0.15) + j * Inches(1.05)
        badge = add_shape_bg(slide, badge_x, badge_y, Inches(0.95), Inches(0.3), color)
        tf = badge.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = rf
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.alignment = PP_ALIGN.CENTER

# Auth tardia note
add_shape_bg(slide, Inches(0.5), Inches(6.1), Inches(12.3), Inches(0.8), RGBColor(0xFF, 0xF3, 0xE0), RGBColor(0xF5, 0x9E, 0x0B), Pt(1))
add_text_box(slide, Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.7),
             "🔓 AUTENTICAÇÃO TARDIA: Visitante percorre Passos 1→5 sem login. Login exigido APENAS para Salvar Lista (RF08) → Promove lista efêmera para persistida.",
             font_size=14, bold=False, color=RGBColor(0x9A, 0x67, 0x00), alignment=PP_ALIGN.LEFT)

# ─── SLIDE 6: KEY FEATURES ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)

add_text_box(slide, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.7),
             "FUNCIONALIDADES-CHAVE — 18 RFs & 12 RNFs", font_size=32, bold=True, color=COLOR_PRIMARY)

# RF Table
rf_data = [
    ("ID", "Requisito Funcional", "Prio"),
    ("RF01", "Cadastrar Usuário (nome, email, senha, pergunta segurança)", "P0"),
    ("RF02", "Login JWT + Refresh + Lockout 6 tentativas/15min", "P0"),
    ("RF03", "Logout (invalida tokens)", "P0"),
    ("RF04", "Recuperar Senha (pergunta segurança)", "P1"),
    ("RF05", "Visualizar Perfil", "P1"),
    ("RF06", "Editar Perfil (senha antiga obrigatória)", "P1"),
    ("RF07", "Criar Lista em Memória (autocomplete + qtd)", "P0"),
    ("RF08", "Salvar Lista Persistida (requer auth + categorias)", "P0"),
    ("RF09", "Listar Minhas Listas (paginação 20, DESC, soft delete)", "P0"),
    ("RF10", "Editar Lista Salva (valida propriedade)", "P1"),
    ("RF11", "Excluir Lista (soft delete + confirmação nome)", "P1"),
    ("RF12", "Selecionar Categorias (pré-filtro fornecedores)", "P0"),
    ("RF13", "Selecionar Fornecedores (≥2, filtrados por categoria)", "P0"),
    ("RF14", "Filtrar Disponibilidade (slider 0-100% tempo real)", "P1"),
    ("RF15", "Calcular Orçamento (tabela flat, ordena preço ASC)", "P0"),
    ("RF16", "Visualizar Resultados (melhor oferta: cobertura > custo)", "P0"),
    ("RF17", "Exportar PDF (lista vencedora, server-side, sem login)", "P0"),
    ("RF18", "Impressão @media print (oculta navegação, A4)", "P1"),
]

table = slide.shapes.add_table(len(rf_data), 3, Inches(0.3), Inches(1.2), Inches(12.7), Inches(5.8)).table
table.columns[0].width = Inches(0.8)
table.columns[1].width = Inches(10.5)
table.columns[2].width = Inches(1.4)

for row_idx, row_data in enumerate(rf_data):
    for col_idx, cell_text in enumerate(row_data):
        cell = table.cell(row_idx, col_idx)
        cell.text = cell_text
        for paragraph in cell.text_frame.paragraphs:
            paragraph.font.size = Pt(11)
            paragraph.font.name = 'Calibri'
            if row_idx == 0:
                paragraph.font.bold = True
                paragraph.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                paragraph.alignment = PP_ALIGN.CENTER
            else:
                paragraph.font.color.rgb = COLOR_TEXT
                if col_idx == 2:
                    paragraph.alignment = PP_ALIGN.CENTER
        if row_idx == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_PRIMARY
        elif row_idx % 2 == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0xF1, 0xF5, 0xF9)
        # Color priority
        if row_idx > 0 and col_idx == 2:
            if cell_text == "P0":
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xDC, 0xF2, 0xE7)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xFF, 0xF3, 0xE0)

# RNF summary at bottom
add_text_box(slide, Inches(0.5), Inches(7.05), Inches(12.3), Inches(0.4),
             "RNFs: Clean Arch (RNF01) | SDD OpenAPI (RNF02) | ACID InnoDB (RNF03,12) | Desktop-only ≥1024px (RNF04) | Feedback <100ms (RNF05) | Coverage ≥80% (RNF06) | CI/CD Docker <5min (RNF07) | Seed <10s (RNF08) | p95 <500ms (RNF09) | Segurança rate-limit/brute-force (RNF10) | PDF <5s (RNF11)",
             font_size=10, color=COLOR_TEXT_LIGHT)

# ─── SLIDE 7: BUSINESS RULES ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)

add_text_box(slide, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.7),
             "REGRAS DE NEGÓCIO CRÍTICAS", font_size=36, bold=True, color=COLOR_PRIMARY)

rules = [
    ("🏆 Melhor Oferta", "Maior % cobertura da lista; empate → menor custo total. Aplicada em RF16, UC07, Passos 4/5.", COLOR_PRIMARY),
    ("📄 Lista Vencedora no PDF", "PDF exporta APENAS a lista do fornecedor campeão (itens precificados + total consolidado). NUNCA a tabela comparativa. RF17, UC08, Passo 5.", COLOR_SECONDARY),
    ("🔓 Autenticação Tardia", "Visitante percorre todo fluxo (Passos 1-5) sem login. Auth só exigida para SALVAR (RF08/UC14/UC17).", COLOR_ACCENT),
    ("⚡ Lista Efêmera", "Armazenada em sessionStorage (memória JS). Recuperada ao reabrir aba. Perdida ao fechar aba/limpar storage. RF07, UC01, UC17.", RGBColor(0x7C, 0x3A, 0xED)),
    ("🗑️ Soft Delete", "Listas excluídas: deletado_em preenchido. Não aparecem no dashboard. RF11, UC13.", RGBColor(0xEA, 0x58, 0x0C)),
    ("💰 Preço Parcial", "Se fornecedor não tem item → preço total calculado apenas sobre disponíveis. Badge \"parcial\" + aviso no banner. RF15, RF16.", RGBColor(0x08, 0x91, 0xB2)),
    ("🛡️ Rate Limiting Híbrido", "Por IP + por username (após login). 6 req/15min. RF02, UC10, UC27.", RGBColor(0xBE, 0x18, 0x5D)),
    ("✅ Validação Categorias no Save", "Salvar lista (RF08) exige ≥1 categoria selecionada (UC03). RF08, UC14.", RGBColor(0x65, 0xA3, 0x0D)),
]

y_start = Inches(1.3)
card_h = Inches(0.7)
gap = Inches(0.1)

for i, (title, desc, color) in enumerate(rules):
    y = y_start + i * (card_h + gap)
    # Color indicator bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.12), card_h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    # Card
    add_shape_bg(slide, Inches(0.92), y, Inches(11.6), card_h, COLOR_CARD, COLOR_BORDER, Pt(1))
    # Title
    add_text_box(slide, Inches(1.1), y + Inches(0.05), Inches(3), card_h - Inches(0.1),
                 title, font_size=16, bold=True, color=color)
    # Description
    add_text_box(slide, Inches(4.1), y + Inches(0.05), Inches(8.3), card_h - Inches(0.1),
                 desc, font_size=13, color=COLOR_TEXT)

# ─── SLIDE 8: DATA MODEL ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)

add_text_box(slide, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.7),
             "MODELO DE DADOS — DER & SEED DETERMINÍSTICO", font_size=32, bold=True, color=COLOR_PRIMARY)

# DER Description (text-based)
der_text = """
ENTIDADES (8 tabelas normalizadas PT-BR, InnoDB, ACID):

┌─────────────┐       ┌─────────────┐       ┌──────────────────┐
│  USUARIOS   │ 1:N   │   LISTAS    │ 1:N   │   ITENS_LISTA    │
├─────────────┤───────┤├─────────────┤───────┤├──────────────────┤
│ id (PK)     │       │ id (PK)     │       │ id (PK)          │
│ nome_usuario│       │ usuario_id  │       │ lista_id (FK)    │
│ email       │       │ nome        │       │ produto_id (FK)  │
│ senha_hash  │       │ categorias  │       │ quantidade (1-9999)│
│ pergunta_seg│       │ deletado_em │       │ criado_em        │
└─────────────┘       └─────────────┘       └──────────────────┘
        │                     │                      │
        │                     │                      │ N:1
        │                     │                      ▼
        │                     │              ┌─────────────┐
        │                     │              │  PRODUTOS   │
        │                     │              ├─────────────┤
        │                     │              │ id (PK)     │
        │                     │              │ nome        │
        │                     │              │ unidade     │
        │                     │              │ ativo       │
        │                     │              └─────────────┘
        │                     │                      │
        │                     │                      │ 1:N
        │                     │                      ▼
        │                     │              ┌──────────────────────┐
        │                     │              │FORNECEDORES_PRODUTOS │
        │                     │              ├──────────────────────┤
        │                     │              │ fornecedor_id (PK)   │
        │                     │              │ produto_id (PK)      │
        │                     │              │ preco (decimal 10,2) │
        │                     │              │ estoque (int ≥ 0)    │
        │                     │              │ ativo                │
        │                     │              └──────────────────────┘
        │                     │                      ▲
        │                     │                      │ N:1
        │                     │              ┌───────┴───────┐
        │                     │              │  FORNECEDORES │
        │                     │              ├───────────────┤
        │                     │              │ id (PK)       │
        │                     │              │ nome          │
        │                     │              │ cnpj (UNIQUE) │
        │                     │              │ ativo         │
        │                     │              └───────────────┘
        │                     │                      ▲
        │                     │                      │ N:N (pivô)
        │                     │              ┌───────┴───────┐
        │                     │              │FORNECEDORES_CATEGORIAS│
        │                     │              ├───────────────┤
        │                     │              │ fornecedor_id │
        │                     │              │ categoria_id  │
        │                     │              └───────────────┘
        │                     │                      ▲
        │                     │                      │ N:1
        │                     │              ┌───────┴───────┐
        │                     └──────────────┤  CATEGORIAS   │
        │                                    ├───────────────┤
        └───────────────────────────────────►│ id (PK)       │
                                             │ nome (11 fixas)│
                                             │ descricao     │
                                             └───────────────┘

TABELA ADICIONAL: sessoes (refresh tokens, user_agent, IP, expiração, revogação)
"""
txBox = slide.shapes.add_textbox(Inches(0.3), Inches(1.2), Inches(12.7), Inches(4.5))
tf = txBox.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = der_text
p.font.size = Pt(10)
p.font.name = 'Consolas'
p.font.color.rgb = COLOR_TEXT
for para in tf.paragraphs[1:]:
    para.font.size = Pt(10)
    para.font.name = 'Consolas'
    para.font.color.rgb = COLOR_TEXT

# Seed info
add_text_box(slide, Inches(0.5), Inches(5.8), Inches(12.3), Inches(0.4),
             "SEED DETERMINÍSTICO (make seed < 10s):", font_size=18, bold=True, color=COLOR_PRIMARY)

seed_items = [
    "11 Categorias macro fixas (Mercado, Vestuário, Automotivos, Informática, Decoração, Móveis, Materiais de Construção, Ferramentas, Livros, Jardinagem, Eletrodomésticos)",
    "10 Fornecedores reais: Carrefour, Extra, Pão de Açúcar, Magazine Luiza, Casas Bahia, Leroy Merlin, Etna, C&A, Renner, Hering",
    "50 Produtos (mix: mercado, ferramentas, informática, vestuário, decoração, jardinagem, eletrodomésticos)",
    "~300 Preços (mapping fornecedor→produto com preço e estoque)",
    "25 Relações N:N fornecedor↔categoria",
]
add_bullet_list(slide, Inches(0.8), Inches(6.3), Inches(11.7), Inches(1.2), seed_items, font_size=13, color=COLOR_TEXT, bullet_color=(0x05, 0x96, 0x69), spacing=Pt(4))

# ─── SLIDE 9: QUALITY & DELIVERABLES ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)

add_text_box(slide, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.7),
             "QUALIDADE, TESTES & ENTREGÁVEIS", font_size=36, bold=True, color=COLOR_PRIMARY)

# Metrics cards
metrics = [
    ("Cobertura\nTestes", "≥ 80%", "RNF06\npytest-cov", COLOR_PRIMARY),
    ("CI/CD\nPipeline", "< 5 min", "RNF07\nGitHub Actions", COLOR_SECONDARY),
    ("API\nLatência p95", "< 500 ms", "RNF09\nFastAPI async", RGBColor(0x7C, 0x3A, 0xED)),
    ("PDF\nGeração", "< 5 s", "RNF11\nReportLab ≤100 itens", RGBColor(0xEA, 0x58, 0x0C)),
    ("Seed\nDados", "< 10 s", "RNF08\n10 forn + 50 prod", RGBColor(0x08, 0x91, 0xB2)),
    ("Segurança\nRate Limit", "6/15 min", "RNF10\nIP + username", RGBColor(0xBE, 0x18, 0x5D)),
]

card_w = Inches(2.0)
card_h = Inches(1.5)
start_x = Inches(0.5)
start_y = Inches(1.4)
gap_x = Inches(0.2)
gap_y = Inches(0.25)

for i, (title, value, desc, color) in enumerate(metrics):
    row = i // 3
    col = i % 3
    x = start_x + col * (card_w + gap_x)
    y = start_y + row * (card_h + gap_y)
    
    card = add_shape_bg(slide, x, y, card_w, card_h, COLOR_CARD, color, Pt(2))
    
    # Title
    add_text_box(slide, x + Inches(0.15), y + Inches(0.1), card_w - Inches(0.3), Inches(0.4),
                 title, font_size=14, bold=True, color=COLOR_TEXT, alignment=PP_ALIGN.CENTER)
    # Value
    add_text_box(slide, x + Inches(0.15), y + Inches(0.5), card_w - Inches(0.3), Inches(0.5),
                 value, font_size=28, bold=True, color=color, alignment=PP_ALIGN.CENTER)
    # Description
    add_text_box(slide, x + Inches(0.15), y + Inches(1.0), card_w - Inches(0.3), Inches(0.4),
                 desc, font_size=11, color=COLOR_TEXT_LIGHT, alignment=PP_ALIGN.CENTER)

# Test Strategy
add_text_box(slide, Inches(0.5), Inches(4.6), Inches(6), Inches(0.4),
             "ESTRATÉGIA DE TESTES", font_size=20, bold=True, color=COLOR_PRIMARY)

test_items = [
    "Backend: Unit (domain/use-case) + Integration (DB real) + Contract (OpenAPI) + Security",
    "Frontend: E2E Playwright (Chromium) — fluxo completo 5 passos + auth + PDF",
    "Cobertura mínima 80% regras de negócio (domain/use-case) — gate no CI",
    "Seed determinístico garante reprodutibilidade de testes de integração",
    "Linting: ruff (Python) — formatação + import sorting + type hints",
]
add_bullet_list(slide, Inches(0.8), Inches(5.1), Inches(6), Inches(2), test_items, font_size=13, color=COLOR_TEXT, bullet_color=(0x1E, 0x40, 0xAF), spacing=Pt(4))

# Replicability
add_text_box(slide, Inches(7.0), Inches(4.6), Inches(6), Inches(0.4),
             "REPLICABILIDADE (Docker Compose)", font_size=20, bold=True, color=COLOR_SECONDARY)

replica_items = [
    "docker compose -f config-docker-0001-docker-compose-v1.0.yml up -d --build",
    "Orquestra: MySQL + migrações Alembic + seed + backend + frontend + nginx proxy",
    ".env.example trackado; cada dev cria seu .env local (SECRET_KEY, senhas)",
    "Portas: 8380 (proxy/frontend), 8000 (backend direto), 3306 (MySQL)",
    "Volume db_data persiste dados; down -v limpa tudo para recomeçar",
]
add_bullet_list(slide, Inches(7.3), Inches(5.1), Inches(5.5), Inches(2), replica_items, font_size=13, color=COLOR_TEXT, bullet_color=(0x05, 0x96, 0x69), spacing=Pt(4))

# Deliverables
add_text_box(slide, Inches(0.5), Inches(6.8), Inches(12.3), Inches(0.4),
             "ENTREGÁVEIS: Código fonte (GitHub) | Docker Compose funcional | Documentação (SPECS.md, README, ADRs) | Testes passando | CI verde | PDF exportável",
             font_size=12, bold=True, color=COLOR_TEXT, alignment=PP_ALIGN.CENTER)

# ─── SLIDE 10: NEXT STEPS ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide)

add_text_box(slide, Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.7),
             "PRÓXIMOS PASSOS — BACKLOG PÓS-MVP", font_size=36, bold=True, color=COLOR_PRIMARY)

# Backlog items
backlog = [
    ("RD01", "Histórico persistente de comparações", "Armazenar resultados de comparação para consulta futura", "Alta"),
    ("RD02", "Importação de listas via CSV", "Upload de arquivo para criar lista de compras em massa", "Média"),
    ("RD03", "Alertas de queda de preço", "Notificações quando produtos monitorados baixam de preço", "Média"),
    ("RD04", "Link público de compartilhamento", "Gerar link público para listas de compras (sem auth)", "Média"),
    ("RD05", "Versão responsiva / PWA", "Adaptar layout para mobile + service worker offline", "Baixa"),
]

# Table
table = slide.shapes.add_table(len(backlog) + 1, 4, Inches(0.8), Inches(1.4), Inches(11.7), Inches(3.5)).table
table.columns[0].width = Inches(1.0)
table.columns[1].width = Inches(3.5)
table.columns[2].width = Inches(5.5)
table.columns[3].width = Inches(1.7)

headers = ["ID", "Feature", "Descrição", "Prioridade"]
for col_idx, h in enumerate(headers):
    cell = table.cell(0, col_idx)
    cell.text = h
    for p in cell.text_frame.paragraphs:
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        p.font.name = 'Calibri'
        p.alignment = PP_ALIGN.CENTER
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_PRIMARY

for row_idx, (id_, feature, desc, prio) in enumerate(backlog):
    for col_idx, val in enumerate([id_, feature, desc, prio]):
        cell = table.cell(row_idx + 1, col_idx)
        cell.text = val
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(13)
            p.font.name = 'Calibri'
            p.font.color.rgb = COLOR_TEXT
            if col_idx == 3:
                p.alignment = PP_ALIGN.CENTER
        if row_idx % 2 == 0:
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0xF1, 0xF5, 0xF9)
        if col_idx == 3:
            if val == "Alta":
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xFE, 0xCD, 0xD3)
            elif val == "Média":
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xFF, 0xF3, 0xE0)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xDC, 0xF2, 0xE7)

# Technical evolution
add_text_box(slide, Inches(0.8), Inches(5.2), Inches(11.7), Inches(0.4),
             "EVOLUÇÃO TÉCNICA PLANEJADA", font_size=20, bold=True, color=COLOR_PRIMARY)

tech_items = [
    "Migração gradual para TypeScript no frontend (manter Vanilla JS, adicionar tipos)",
    "Substituir seed SQL por factories Python (Faker) para dados mais realistas em testes",
    "Implementar cache Redis para consultas frequentes de catálogo/preços",
    "Adicionar observabilidade: OpenTelemetry + Prometheus + Grafana",
    "Migrar autenticação para OAuth2/OIDC (Keycloak/Auth0) para SSO enterprise",
    "Implementar web scraping real (Scrapy/Playwright) para fornecedores reais — substitui mock",
]
add_bullet_list(slide, Inches(1.0), Inches(5.7), Inches(11.3), Inches(1.8), tech_items, font_size=14, color=COLOR_TEXT, bullet_color=(0x1E, 0x40, 0xAF), spacing=Pt(5))

# ─── SLIDE 11: TEAM & CLOSING ───
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide, COLOR_PRIMARY)

# Decorative line
line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(2.5), Inches(10.3), Pt(3))
line.fill.solid()
line.fill.fore_color.rgb = COLOR_SECONDARY
line.line.fill.background()

add_text_box(slide, Inches(1.5), Inches(0.8), Inches(10.3), Inches(1.0),
             "COBECO MVP", font_size=48, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), alignment=PP_ALIGN.CENTER)

add_text_box(slide, Inches(1.5), Inches(1.7), Inches(10.3), Inches(0.7),
             "Comparação de Bens de Consumo — Entrega Acadêmica", font_size=24, color=RGBColor(0xD1, 0xD5, 0xDB), alignment=PP_ALIGN.CENTER)

# Team
add_text_box(slide, Inches(1.5), Inches(3.0), Inches(10.3), Inches(0.5),
             "EQUIPE", font_size=22, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), alignment=PP_ALIGN.CENTER)

team = [
    "Leonardo Setti — Tech Lead / Arquiteto",
    "Fabrício Cabral — Backend / Database",
    "Nicholas Anthony — Frontend / UX",
    "Eduardo Passarelli — Testes / Qualidade",
    "Nicolas Mallouk — DevOps / Documentação",
]
y = Inches(3.6)
for member in team:
    add_text_box(slide, Inches(1.5), y, Inches(10.3), Inches(0.4),
                 member, font_size=18, color=RGBColor(0xD1, 0xD5, 0xDB), alignment=PP_ALIGN.CENTER)
    y += Inches(0.35)

add_text_box(slide, Inches(1.5), Inches(5.6), Inches(10.3), Inches(0.5),
             "Orientadora: Profa. Thais Cristina Casagrande", font_size=16, color=RGBColor(0x94, 0xA3, 0xB8), alignment=PP_ALIGN.CENTER)

add_text_box(slide, Inches(1.5), Inches(6.2), Inches(10.3), Inches(0.5),
             "FATEC Taquaritinga — ADS 2026", font_size=16, color=RGBColor(0x94, 0xA3, 0xB8), alignment=PP_ALIGN.CENTER)

# ─── Save ───
output_path = "/lab/FATEC/202602/lab_eng_software/COBECO/COBECO_MVP_Apresentacao.pptx"
prs.save(output_path)
print(f"✅ Presentation saved to: {output_path}")
print(f"   Slides: {len(prs.slides)}")