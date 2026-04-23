"""
Geração de relatórios PDF com fpdf2 — Layout agrupado por categoria.
"""
import pandas as pd
from fpdf import FPDF
from datetime import datetime


# ─── Color Palettes ────────────────────────────────────────────────────────────

def _category_rgb(categoria: str) -> tuple[int, int, int]:
    cat = str(categoria).upper()
    if 'AJAX' in cat:           return (180, 120, 10)
    if 'NATURAL' in cat or 'SUAVE' in cat: return (30, 130, 70)
    if 'PROTEX' in cat:         return (10, 130, 120)
    if any(k in cat for k in ['CD ','CR D','DENTAL','SORRISO','COLGATE','LUMINOUS','TRIPLA','ANTICARIE','CARVAO']):
        return (30, 90, 180)
    if any(k in cat for k in ['ESC','ED ','ESCOVA','ZIG ZAG','SLIM','CLASSIC']):
        return (90, 50, 180)
    if 'PINHO' in cat or 'DESINF' in cat: return (180, 90, 20)
    if 'OLA' in cat:            return (180, 50, 100)
    if 'ENXAG' in cat:          return (10, 130, 160)
    return (100, 115, 140)

FAIXA_COLORS: dict[str, tuple[int, int, int]] = {
    'FX1-2': (29,  78, 216),  # blue
    'FX3':   (109, 40, 217),  # purple
    'FX4':   (194, 65,  12),  # orange
    'FX5':   (  4,120,  87),  # green
}


class ColgatePDF(FPDF):
    def __init__(self, filtros: dict):
        super().__init__(orientation="L")
        self.filtros = filtros
        self.set_left_margin(12)
        self.set_right_margin(12)
        self.set_top_margin(8)

    def header(self):
        # Red brand bar
        self.set_fill_color(227, 0, 27)
        self.rect(0, 0, 297, 6, 'F')

        self.ln(8)
        self.set_font("helvetica", "B", 16)
        self.set_text_color(227, 0, 27)
        self.cell(0, 8, "COLGATE FOCO", align="L", ln=0)

        self.set_font("helvetica", "", 9)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}", align="R", ln=1)

        # Filter summary line
        faixas = ', '.join(self.filtros.get('faixas', [])) or 'Todas'
        crit = '  |  Somente Prioritários' if self.filtros.get('only_critical') else ''
        self.set_font("helvetica", "I", 8)
        self.set_text_color(110, 110, 110)
        self.cell(0, 5, f"Faixas: {faixas}{crit}", align="L", ln=1)

        # Divider
        self.set_draw_color(220, 220, 220)
        self.line(12, self.get_y() + 1, 285, self.get_y() + 1)
        self.ln(4)

    def footer(self):
        self.set_y(-13)
        self.set_font("helvetica", "I", 7.5)
        self.set_text_color(160, 160, 160)
        self.set_fill_color(248, 248, 248)
        self.rect(0, self.get_y() - 2, 297, 15, 'F')
        self.cell(0, 10, f"Uso Interno Confidencial  -  Pág. {self.page_no()}/{{nb}}", align="C")


def _clean(text: str) -> str:
    return str(text).encode('latin-1', 'replace').decode('latin-1')


def _draw_faixa_badge(pdf: FPDF, faixa: str, x: float, y: float):
    """Draws a compact colored faixa pill at position (x, y). Returns new x."""
    r, g, b = FAIXA_COLORS.get(faixa, (100, 115, 140))
    w = 14
    h = 4.5
    # Background pill
    pdf.set_fill_color(r, g, b)
    pdf.set_draw_color(r, g, b)
    pdf.rect(x, y, w, h, 'F')
    # Label
    pdf.set_font("helvetica", "B", 6.5)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(x, y + 0.2)
    pdf.cell(w, h, faixa, align="C")
    return x + w + 2


def generate_pdf(df: pd.DataFrame, filtros_aplicados: dict, modo: str) -> bytes:
    pdf = ColgatePDF(filtros=filtros_aplicados)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # Column layout
    PAGE_W = 273  # 297 - 2*12 margins
    COL_SKU   = 16
    COL_DESC  = 106 if modo == "vendas" else 76
    COL_EAN   = 0   if modo == "vendas" else 30
    COL_TIPO  = 0   if modo == "vendas" else 12
    COL_COB   = 16
    COL_FAIXAS = PAGE_W - COL_SKU - COL_DESC - COL_EAN - COL_TIPO - COL_COB  # remaining

    # Global table header
    pdf.set_fill_color(40, 40, 55)
    pdf.set_text_color(200, 210, 230)
    pdf.set_font("helvetica", "B", 8.5)
    header_y = pdf.get_y()
    pdf.set_x(12)
    pdf.cell(COL_SKU,   6.5, "CÓD.",   border=0, fill=True, align="C")
    pdf.cell(COL_DESC,  6.5, "PRODUTO", border=0, fill=True)
    if modo != "vendas":
        pdf.cell(COL_EAN,  6.5, "EAN",   border=0, fill=True)
        pdf.cell(COL_TIPO, 6.5, "TIPO",  border=0, fill=True, align="C")
    pdf.cell(COL_COB, 6.5, "COB.", border=0, fill=True, align="C")
    pdf.cell(COL_FAIXAS, 6.5, "FAIXAS", border=0, fill=True, align="C")
    pdf.ln(6.5)

    grouped = df.groupby('categoria', sort=True)
    row_n = 0

    for cat, group in grouped:
        if pdf.get_y() > 175:
            pdf.add_page()

        # Category header band
        cat_r, cat_g, cat_b = _category_rgb(cat)
        pdf.set_fill_color(cat_r, cat_g, cat_b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("helvetica", "B", 8.5)
        pdf.set_x(12)
        pdf.cell(PAGE_W, 6, f"  {_clean(cat).upper()}  ({len(group)} produtos)", fill=True, border=0, ln=1)

        for _, row in group.iterrows():
            if pdf.get_y() > 183:
                pdf.add_page()

            is_crit = bool(row.get('is_critical', False))
            is_fav  = bool(row.get('favorito',    False))

            # Row background
            if is_crit:
                pdf.set_fill_color(255, 240, 242)
            else:
                pdf.set_fill_color(255, 255, 255) if row_n % 2 == 0 else pdf.set_fill_color(248, 249, 252)

            row_y = pdf.get_y()
            row_h = 6.5

            # Subtle category left stripe
            pdf.set_fill_color(cat_r, cat_g, cat_b)
            pdf.rect(12, row_y, 2, row_h, 'F')

            # SKU
            pdf.set_font("helvetica", "B" if is_crit else "", 7.5)
            pdf.set_text_color(60, 60, 60) if not is_crit else pdf.set_text_color(180, 0, 0)
            pdf.set_x(14)

            if is_crit:
                pdf.set_fill_color(255, 240, 242)
            else:
                pdf.set_fill_color(255, 255, 255) if row_n % 2 == 0 else pdf.set_fill_color(248, 249, 252)

            pdf.cell(COL_SKU - 2, row_h, _clean(str(row.get('sku', ''))), fill=True, align="C")

            # Description — strip "CODE - " prefix if present
            desc = str(row.get('descricao', ''))
            sku_prefix = str(row.get('sku', '')) + ' - '
            if desc.startswith(sku_prefix):
                desc = desc[len(sku_prefix):]
            if is_fav:
                desc = "★ " + desc

            pdf.set_font("helvetica", "B" if is_crit else "", 7.5)
            pdf.cell(COL_DESC, row_h, _clean(desc[:50 if modo == "vendas" else 36]), fill=True)

            if modo != "vendas":
                pdf.set_font("helvetica", "", 7)
                pdf.cell(COL_EAN,  row_h, _clean(str(row.get('ean', ''))[:16]), fill=True)
                pdf.cell(COL_TIPO, row_h, "Pack" if row.get('is_pack', False) else "Unit", fill=True, align="C")

            num_faixas = len(row.get('faixas', []))
            pdf.set_font("helvetica", "B" if num_faixas == 4 else "", 7.5)
            if num_faixas == 4:
                pdf.set_text_color(40, 140, 60)
            else:
                pdf.set_text_color(120, 120, 120)
            pdf.cell(COL_COB, row_h, f"{num_faixas}/4", fill=True, align="C")
            
            # Reset text color for badges if changed
            pdf.set_text_color(255, 255, 255)

            # Faixa badges inline
            badge_x = pdf.get_x() + 1
            badge_y = row_y + 1
            for f in row.get('faixas', []):
                badge_x = _draw_faixa_badge(pdf, f, badge_x, badge_y)

            pdf.ln(row_h)
            row_n += 1

        # Small gap between categories
        pdf.ln(2)

    return bytes(pdf.output(dest="S"))
