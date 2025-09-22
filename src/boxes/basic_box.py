"""
basic_box.py
------------
Prosta implementacja siatki pudełka (glue, side, front, back).
"""

from src.config import BoxDims, TechParams

class BasicBox:
    def __init__(self, dims: BoxDims, tech: TechParams):
        self.dims = dims
        self.tech = tech

    def build_geometry(self):
        """
        Zwraca: (cut_lines, crease_lines)
        """
        cut = []
        crease = []

        w, h, d = self.dims.width, self.dims.height, self.dims.depth
        g = self.tech.glue_width

        # Prosty prototyp: prostokąt (bez patki kurzowej/klejowej)
        cut.append((0, 0, w, 0))
        cut.append((w, 0, w, h))
        cut.append((w, h, 0, h))
        cut.append((0, h, 0, 0))

        # Biga w środku (prosty przykład)
        crease.append((0, h/2, w, h/2))

        return cut, crease
