"""
svg_helpers.py
--------------
Helpery do rysowania linii i zapisu do SVG/PDF.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor
import os

# --- LINIE ---

def line_exists(new_line, line_list, tol=0.01):
    """Sprawdza, czy linia (x1,y1,x2,y2) już istnieje (z tolerancją)."""
    x1, y1, x2, y2 = new_line
    for (lx1, ly1, lx2, ly2) in line_list:
        if abs(x1 - lx1) < tol and abs(y1 - ly1) < tol and abs(x2 - lx2) < tol and abs(y2 - ly2) < tol:
            return True
        if abs(x1 - lx2) < tol and abs(y1 - ly2) < tol and abs(x2 - lx1) < tol and abs(y2 - ly1) < tol:
            return True
    return False

def add_line_safe(new_line, line_list, tol=0.01):
    """Dodaje linię tylko jeśli nie istnieje już w liście."""
    if not line_exists(new_line, line_list, tol):
        line_list.append(new_line)

# --- SVG EXPORT ---

def save_svg(filename, lines, stroke="black"):
    """Zapis prostych linii do pliku SVG."""
    if not lines:
        print("[WARN] Brak linii do zapisania")
        return
    min_x = min(min(x1, x2) for x1, y1, x2, y2 in lines)
    max_x = max(max(x1, x2) for x1, y1, x2, y2 in lines)
    min_y = min(min(y1, y2) for x1, y1, x2, y2 in lines)
    max_y = max(max(y1, y2) for x1, y1, x2, y2 in lines)

    width = max_x - min_x
    height = max_y - min_y

    with open(filename, "w") as f:
        f.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" '
            f'width="{width}mm" height="{height}mm" '
            f'viewBox="{min_x} {min_y} {width} {height}">\n'
        )
        f.write(f'<g stroke="{stroke}" stroke-width="0.2" fill="none">\n')
        for (x1, y1, x2, y2) in lines:
            f.write(f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>\n')
        f.write('</g>\n')
        f.write('</svg>\n')
    print(f"[OK] SVG zapisane: {filename}")

# --- PDF EXPORT ---

_MM_TO_PT = 2.83465  # konwersja mm → punkty

def save_pdf(filename, cut_lines, crease_lines):
    """Eksport do PDF z liniami Cut i Crease (osobne kolory spot)."""
    if not cut_lines and not crease_lines:
        print("[WARN] Brak linii do zapisania (PDF)")
        return

    all_lines = cut_lines + crease_lines
    min_x = min(min(x1, x2) for (x1, y1, x2, y2) in all_lines)
    max_x = max(max(x1, x2) for (x1, y1, x2, y2) in all_lines)
    min_y = min(min(y1, y2) for (x1, y1, x2, y2) in all_lines)
    max_y = max(max(y1, y2) for (x1, y1, x2, y2) in all_lines)

    width_pt = (max_x - min_x + 10) * _MM_TO_PT
    height_pt = (max_y - min_y + 10) * _MM_TO_PT

    c = canvas.Canvas(filename, pagesize=(width_pt, height_pt))

    # Spoty (symulowane CMYK)
    cut_color = CMYKColor(0, 0, 0, 100)     # czarny
    crease_color = CMYKColor(0, 100, 100, 0)  # czerwony

    def draw(lines, color):
        c.setStrokeColor(color)
        c.setLineWidth(0.2)
        for (x1, y1, x2, y2) in lines:
            c.line(
                (x1 - min_x + 5) * _MM_TO_PT,
                (y1 - min_y + 5) * _MM_TO_PT,
                (x2 - min_x + 5) * _MM_TO_PT,
                (y2 - min_y + 5) * _MM_TO_PT,
            )

    draw(cut_lines, cut_color)
    draw(crease_lines, crease_color)

    c.showPage()
    c.save()
    print(f"[OK] PDF zapisany: {filename}")
