"""
main.py
-------
Punkt startowy do testów BasicBox.
"""

from src.config import BoxDims, TechParams
from src.boxes.basic_box import BasicBox
from src.utils.svg_helpers import save_svg

def main():
    dims = BoxDims(width=100, height=60, depth=40)
    tech = TechParams(glue_width=10)

    box = BasicBox(dims, tech)
    cut, crease = box.build_geometry()

    save_svg("basic_box_v4.svg", cut, crease)

if __name__ == "__main__":
    main()
