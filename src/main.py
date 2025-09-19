from src.boxes.basic_box import BasicBox
from src.config import BoxDims, TechParams
from src.utils.svg_helpers import save_svg, save_pdf

def main():
    # przykładowe wymiary (mm)
    dims = BoxDims(width=90, height=60, depth=20)
    tech = TechParams(
        glue_width=10,
        glue_angle=15,
        triangle_h=15,
        triangle_w=24,
        closures_on="front",           # 'front' | 'back' | 'both'
        dust_flap=8,
        front_crease_offset=1.0,      # bigi frontu podniesione/opuszczone
        back_width_delta=-1.0         # back węższy o 1 mm
    )

    box = BasicBox(dims, tech)
    cut, crease = box.build_geometry()

    save_svg("basic_box_v3.2_clean.svg", cut, crease)
    save_pdf("basic_box_v3.2_clean.pdf", cut, crease)  # działa, jeśli masz reportlab
    print(f"[INFO] CUT: {len(cut)} | CREASE: {len(crease)}")

if __name__ == "__main__":
    main()
