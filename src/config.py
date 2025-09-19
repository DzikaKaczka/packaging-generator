from dataclasses import dataclass

@dataclass
class BoxDims:
    width: float    # szerokość FRONT/BACK (mm)
    height: float   # wysokość (mm)
    depth: float    # głębokość (boki) (mm)

@dataclass
class TechParams:
    # klejowa
    glue_width: float = 10.0     # mm
    glue_angle: float = 15.0     # stopnie (nachylenie górnej/dolnej krawędzi klejowej)

    # klapki zamykające (trapez na prostokącie)
    triangle_h: float = 15.0     # wysokość trapezu (mm)
    triangle_w: float = 24.0     # szerokość podstawy trapezu (mm)
    closures_on: str = "front"    # 'front' | 'back' | 'both'

    # patki kurzowe
    dust_flap: float = 8.0       # prostokątna patka kurzowa (mm)

    # offsety
    front_crease_offset: float = 1.0  # mm, przesunięcie poziomych big na froncie
    back_width_delta: float = -1.0    # mm, korekta szerokości BACK (np. -1.0 → BACK węższy o 1 mm)
