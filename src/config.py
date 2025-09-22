"""
config.py
---------
Definicje parametrów wejściowych dla pudełek.
"""

from dataclasses import dataclass

@dataclass
class BoxDims:
    width: float    # szerokość (front/back)
    height: float   # wysokość
    depth: float    # głębokość (side)

@dataclass
class TechParams:
    glue_width: float = 10.0         # szerokość patki klejowej
    dust_flap: float = 8.0           # wysokość patki kurzowej
    top_triangle_h: float = 15.0     # wysokość trapezu górnego
    top_triangle_w: float = 24.0     # szerokość trapezu górnego
    bottom_triangle_h: float = 15.0  # wysokość trapezu dolnego
    bottom_triangle_w: float = 24.0  # szerokość trapezu dolnego
    crease_offset: float = 1.0       # domyślne przesunięcie bigi
    glue_angle: float = 15.0         # kąt patki klejowej (°)
