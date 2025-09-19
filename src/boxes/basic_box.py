"""
BasicBox – czysta, stabilna baza V3.2-clean
Zasady:
- układ: [glue]|[side1=depth]|[front=width]|[side2=depth]|[back=width+delta]
- pionowe wewnętrzne = Crease
- poziome: side1/side2 = Crease; front = Crease na y=-offset oraz y=H+offset; back = Cut (y=0 i y=H)
- patka klejowa = trapez (top/bottom pod kątem glue_angle)
- klapki zamykające: prostokąt (wys.=depth) + trapez (triangle_h/triangle_w) na panelu closures_on
- patki kurzowe: prostokątne na side1/side2 (góra i dół)
"""
from typing import List, Tuple
import math
from src.config import BoxDims, TechParams
from src.utils.geometry import add_line_safe, reconcile_layers

Line = Tuple[float, float, float, float]

class BasicBox:
    def __init__(self, dims: BoxDims, tech: TechParams):
        self.dims = dims
        self.tech = tech

        # aliasy mm
        self.W = float(dims.width)
        self.H = float(dims.height)
        self.D = float(dims.depth)

        self.GW = float(tech.glue_width)
        self.GA = float(tech.glue_angle)
        self.DF = float(tech.dust_flap)
        self.TH = float(tech.triangle_h)
        self.TW = float(tech.triangle_w)
        self.CO = tech.closures_on.lower().strip()
        self.FO = float(tech.front_crease_offset)
        self.BD = float(tech.back_width_delta)

    # ---------- helpers rysujące ----------
    def _add_rect_flap(self, cut: List[Line], xL: float, xR: float, base_y: float, out_mm: float, up: bool):
        """Prostokątna patka (dust flap): od krawędzi panelu 'base_y' na zewnątrz o 'out_mm'."""
        y2 = base_y - out_mm if up else base_y + out_mm
        add_line_safe((xL, base_y, xL, y2), cut)
        add_line_safe((xR, base_y, xR, y2), cut)
        add_line_safe((xL, y2,   xR, y2),   cut)

    def _add_closure(self, cut: List[Line], crease: List[Line], xL: float, xR: float, top: bool):
        """
        Klapka zamykająca: prostokąt (wys.=D) + trapez (TH,TW).
        Umiejscowienie: top (nad panelem) lub bottom (pod panelem).
        """
        mid = (xL + xR) / 2.0
        rect_edge_y = 0.0 if top else self.H
        out_rect_y  = (-self.D) if top else (self.H + self.D)

        # prostokąt
        add_line_safe((xL, rect_edge_y, xL, out_rect_y), cut)
        add_line_safe((xR, rect_edge_y, xR, out_rect_y), cut)
        add_line_safe((xL, out_rect_y,  xR, out_rect_y), cut)
        # biga krawędzi prostokąta (na linii panelu)
        add_line_safe((xL, rect_edge_y, xR, rect_edge_y), crease)

        # trapez
        apex_y = out_rect_y - self.TH if top else out_rect_y + self.TH
        left_base  = mid - self.TW/2.0
        right_base = mid + self.TW/2.0
        add_line_safe((left_base,  apex_y, mid,       apex_y), cut)  # górna/dolna krawędź trapezu (krótka)
        add_line_safe((mid,        apex_y, right_base,apex_y), cut)
        add_line_safe((xL, out_rect_y, left_base,  apex_y), cut)
        add_line_safe((xR, out_rect_y, right_base, apex_y), cut)

    # ---------- główna geometria ----------
    def build_geometry(self):
        cut: List[Line] = []
        crease: List[Line] = []

        # pozycje X paneli (od 0)
        x = 0.0
        x_glue_L = x
        x_glue_R = x + self.GW

        x_side1_L = x_glue_R
        x_side1_R = x_side1_L + self.D

        x_front_L = x_side1_R
        x_front_R = x_front_L + self.W

        x_side2_L = x_front_R
        x_side2_R = x_side2_L + self.D

        back_w = max(self.W + self.BD, 0.0)
        x_back_L = x_side2_R
        x_back_R = x_back_L + back_w

        # --- patka klejowa (trapez: górna i dolna krawędź pod kątem GA) ---
        dy = math.tan(math.radians(self.GA)) * self.GW
        # lewa krawędź (pion)
        add_line_safe((x_glue_L, 0.0, x_glue_L, self.H), cut)
        # prawa krawędź (pion, ale skrócona do wierzchołków skosów)
        add_line_safe((x_glue_R, -dy, x_glue_R, self.H + dy), cut)
        # górny skos
        add_line_safe((x_glue_L, 0.0, x_glue_R, -dy), cut)
        # dolny skos
        add_line_safe((x_glue_L, self.H, x_glue_R, self.H + dy), cut)

        # --- pionowe WEWNĘTRZNE bigi (między panelami) ---
        for x_v in (x_side1_L, x_side1_R, x_front_L, x_front_R, x_side2_L, x_side2_R, x_back_L):
            # tylko te, które należą do podziału między panelami (pomiń x_glue_L i x_back_R)
            if x_v in (x_glue_L, x_back_R):
                continue
            add_line_safe((x_v, 0.0, x_v, self.H), crease)

        # --- zewnętrzna prawa krawędź całości (Cut) ---
        add_line_safe((x_back_R, 0.0, x_back_R, self.H), cut)

        # --- POZIOME: side1/side2 = Crease; front = Crease z offsetem; back = Cut ---
        # side1
        add_line_safe((x_side1_L, 0.0, x_side1_R, 0.0), crease)
        add_line_safe((x_side1_L, self.H, x_side1_R, self.H), crease)
        # side2
        add_line_safe((x_side2_L, 0.0, x_side2_R, 0.0), crease)
        add_line_safe((x_side2_L, self.H, x_side2_R, self.H), crease)
        # front (offsetowana biga)
        if self.FO != 0.0:
            add_line_safe((x_front_L, -self.FO, x_front_R, -self.FO), crease)
            add_line_safe((x_front_L, self.H + self.FO, x_front_R, self.H + self.FO), crease)
        else:
            add_line_safe((x_front_L, 0.0, x_front_R, 0.0), crease)
            add_line_safe((x_front_L, self.H, x_front_R, self.H), crease)
        # back (cięcia)
        add_line_safe((x_back_L, 0.0, x_back_R, 0.0), cut)
        add_line_safe((x_back_L, self.H, x_back_R, self.H), cut)

        # --- KLAPKI ZAMYKAJĄCE (na closures_on) ---
        def want(panel: str) -> bool:
            return self.CO in ("both", panel)

        if want("front"):
            self._add_closure(cut, crease, x_front_L, x_front_R, top=True)
            self._add_closure(cut, crease, x_front_L, x_front_R, top=False)
        if want("back"):
            self._add_closure(cut, crease, x_back_L, x_back_R, top=True)
            self._add_closure(cut, crease, x_back_L, x_back_R, top=False)

        # --- PATKI KURZOWE (side1/side2, góra i dół) ---
        # top (na zewnątrz w górę)
        self._add_rect_flap(cut, x_side1_L, x_side1_R, base_y=0.0,  out_mm=self.DF, up=True)
        self._add_rect_flap(cut, x_side2_L, x_side2_R, base_y=0.0,  out_mm=self.DF, up=True)
        # bottom (na zewnątrz w dół)
        self._add_rect_flap(cut, x_side1_L, x_side1_R, base_y=self.H, out_mm=self.DF, up=False)
        self._add_rect_flap(cut, x_side2_L, x_side2_R, base_y=self.H, out_mm=self.DF, up=False)

        # porządki: deduplikacja + reguła "Crease > Cut"
        cut, crease = reconcile_layers(cut, crease)
        return cut, crease
