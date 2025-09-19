"""
SVG/PDF export (V3.2-clean)
"""
from typing import List, Tuple
from .geometry import bbox

Line = Tuple[float, float, float, float]

def save_svg(filename: str, cut_lines: List[Line], crease_lines: List[Line], pad: float = 5.0):
    all_lines = (cut_lines or []) + (crease_lines or [])
    min_x, min_y, max_x, max_y = bbox(all_lines) if all_lines else (0,0,100,100)
    vb_x = min_x - pad
    vb_y = min_y - pad
    vb_w = (max_x - min_x) + 2*pad
    vb_h = (max_y - min_y) + 2*pad

    with open(filename, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x} {vb_y} {vb_w} {vb_h}">\n')

        f.write('  <g id="Cut" stroke="#000" stroke-width="0.2" fill="none">\n')
        for (x1,y1,x2,y2) in cut_lines:
            f.write(f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>\n')
        f.write('  </g>\n')

        f.write('  <g id="Crease" stroke="red" stroke-width="0.2" fill="none">\n')
        for (x1,y1,x2,y2) in crease_lines:
            f.write(f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>\n')
        f.write('  </g>\n')

        f.write('</svg>\n')
    print(f"[OK] SVG zapisane: {filename}")

# PDF (opcjonalnie — działa, jeśli masz reportlab)
def save_pdf(filename: str, cut_lines: List[Line], crease_lines: List[Line], pad: float = 5.0):
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.colors import CMYKColor
    except Exception as e:
        print(f"[WARN] PDF pominięty (brak reportlab): {e}")
        return

    _MM_TO_PT = 2.83465
    all_lines = (cut_lines or []) + (crease_lines or [])
    min_x, min_y, max_x, max_y = bbox(all_lines) if all_lines else (0,0,100,100)
    vb_x = min_x - pad
    vb_y = min_y - pad
    vb_w = (max_x - min_x) + 2*pad
    vb_h = (max_y - min_y) + 2*pad

    c = canvas.Canvas(filename, pagesize=(vb_w*_MM_TO_PT, vb_h*_MM_TO_PT))

    def draw(lines, color):
        c.setStrokeColor(color)
        c.setLineWidth(0.2)
        for (x1,y1,x2,y2) in lines:
            c.line((x1 - vb_x)*_MM_TO_PT, (y1 - vb_y)*_MM_TO_PT,
                   (x2 - vb_x)*_MM_TO_PT, (y2 - vb_y)*_MM_TO_PT)

    cut_color   = CMYKColor(0, 0, 0, 100, spotName="CutLine")
    crease_color= CMYKColor(0, 100, 100, 0, spotName="CreaseLine")

    draw(cut_lines,   cut_color)
    draw(crease_lines, crease_color)

    c.showPage()
    c.save()
    print(f"[OK] PDF zapisany: {filename}")
