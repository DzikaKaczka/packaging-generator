"""
main.py (V3.1.1)
Uruchom:  python3 -m src.main
"""

from src.boxes.basic_box import BasicBox
from src.config import BoxDims, TechParams
from src.utils.svg_helpers import save_svg, save_pdf

def main():
    dims = BoxDims(width=90, height=60, depth=20)
    tech = TechParams(
        glue_width=10,
        dust_flap=8,
        front_offset=1.0,          # back = W - 1
        front_crease_offset=1.0,   # big frontu: ±1 mm
        glue_angle=15.0,
        bottom_triangle_h=15.0,
        bottom_triangle_w=24.0,
    )

    box = BasicBox(dims, tech)
    cut_lines, crease_lines = box.build_geometry()

    # Podgląd (SVG = wszystko w jednym)
    save_svg("basic_box_v3.svg", cut_lines + crease_lines)
    # Produkcja (PDF = warstwy)
    save_pdf("basic_box_v3.pdf", cut_lines, crease_lines)

    print(f"[INFO] CUT: {len(cut_lines)} linii, CREASE: {len(crease_lines)} linii")
    print("== DONE ==")

if __name__ == "__main__":
    main()
