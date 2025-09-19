"""
BasicBox (V3.1.1)
-----------------
Poprawki:
- big offset na FRONT (front_crease_offset),
- back = W - front_offset,
- patka klejowa z krawędziami pod kątem glue_angle,
- klapki frontu: prostokąt (wys.=depth) + trójkątny zatrzask (powrót),
- osobne odcinki bigu per panel,
- deduplikacja bez scalania paneli.
"""

from dataclasses import dataclass
from math import tan, radians
from typing import List, Tuple
from src.config import BoxDims, TechParams
from src.utils.geometry import reconcile_layers

Line = Tuple[float, float, float, float]  # bez typu: typy trzymamy per-lista


@dataclass
class BasicBox:
    dims: BoxDims
    tech: TechParams

    def build_geometry(self):
        """
        Zwraca: (cut_lines, crease_lines)
        """
        W = float(self.dims.width)
        H = float(self.dims.height)
        D = float(self.dims.depth)

        p = self.tech
        G = float(p.glue_width)

        # front/back szerokości (uwaga: back zwężony o front_offset)
        W_front = W
        W_back  = max(W - float(p.front_offset), 0.1)

        x0, y0 = 0.0, 0.0
        panels = [
            ("glue",  G),
            ("side1", D),
            ("front", W_front),
            ("side2", D),
            ("back",  W_back),
        ]

        cut:   List[Line] = []
        crease:List[Line] = []

        # --- piony: tylko skrajne CUT, wewnętrzne CREASE ---
        x = x0
        # lewa krawędź całości (CUT)
        cut.append((x, y0, x, y0 + H))
        for name, w in panels:
            # granica między panelami (po lewej stronie aktualnego panelu)
            if name != "glue":
                crease.append((x, y0, x, y0 + H))
            x += w
        # prawa krawędź całości (CUT)
        cut.append((x, y0, x, y0 + H))

        # --- poziome bigi: osobno dla każdego panelu ---
        for name, xs, w in self._scan_positions(x0, panels):
            if name == "front":
                # offset bigów frontu w górę/dół (domyślnie +1 mm)
                off = float(p.front_crease_offset)
                crease.append((xs, y0 - off, xs + w, y0 - off))
                crease.append((xs, y0 + H + off, xs + w, y0 + H + off))
            else:
                crease.append((xs, y0, xs + w, y0))
                crease.append((xs, y0 + H, xs + w, y0 + H))

        # --- patki kurzowe (tu: proste prostokąty, identyczne góra/dół) ---
        df = float(p.dust_flap)
        for name, xs, w in self._scan_positions(x0, panels):
            if name.startswith("side"):
                # TOP
                cut.append((xs, y0, xs, y0 - df))
                cut.append((xs + w, y0, xs + w, y0 - df))
                cut.append((xs, y0 - df, xs + w, y0 - df))
                crease.append((xs, y0, xs + w, y0))
                # BOTTOM
                yb = y0 + H
                cut.append((xs, yb, xs, yb + df))
                cut.append((xs + w, yb, xs + w, yb + df))
                cut.append((xs, yb + df, xs + w, yb + df))
                crease.append((xs, yb, xs + w, yb))

        # --- patka klejowa: krawędzie górna/dolna pod kątem glue_angle ---
        # lewa pionowa
        cut.append((x0, y0, x0, y0 + H))
        # prawa pionowa
        cut.append((x0 + G, y0, x0 + G, y0 + H))
        # górna skośna: od (x0,y0) do (x0+G, y0 - dy)
        dy = tan(radians(float(p.glue_angle))) * G
        cut.append((x0, y0, x0 + G, y0 - dy))
        # dolna skośna: od (x0,y0+H) do (x0+G, y0+H - dy)
        cut.append((x0, y0 + H, x0 + G, y0 + H - dy))

        # --- klapki frontu ---
        # TOP: prostokąt wys.=D
        x_front = self._x_of("front", x0, panels)
        w_front = W_front
        cut.append((x_front, y0, x_front, y0 - D))
        cut.append((x_front + w_front, y0, x_front + w_front, y0 - D))
        cut.append((x_front, y0 - D, x_front + w_front, y0 - D))
        crease.append((x_front, y0, x_front + w_front, y0))  # zawias

        # BOTTOM: prostokąt wys.=D + zatrzask (trójkąt)
        yb = y0 + H
        cut.append((x_front, yb, x_front, yb + D))
        cut.append((x_front + w_front, yb, x_front + w_front, yb + D))
        cut.append((x_front, yb + D, x_front + w_front, yb + D))
        crease.append((x_front, yb, x_front + w_front, yb))  # zawias

        # zatrzask – trójkąt na środku dolnej klapki
        mid = x_front + w_front / 2.0
        latch_w = float(p.bottom_triangle_w)
        latch_h = float(p.bottom_triangle_h)
        base_y = yb + D
        cut.append((mid - latch_w / 2.0, base_y, mid, base_y + latch_h))
        cut.append((mid, base_y + latch_h, mid + latch_w / 2.0, base_y))

        # --- reconcile (usuń duplikaty, Cut < Crease) ---
        cut, crease = reconcile_layers(cut, crease, tol=0.05)
        return cut, crease

    # -------- pomocnicze --------
    @staticmethod
    def _scan_positions(x0: float, panels: List[Tuple[str, float]]):
        x = x0
        for name, w in panels:
            yield (name, x, w)
            x += w

    @staticmethod
    def _x_of(name_wanted: str, x0: float, panels: List[Tuple[str, float]]) -> float:
        x = x0
        for name, w in panels:
            if name == name_wanted:
                return x
            x += w
        raise ValueError(f"Panel '{name_wanted}' nie istnieje")
