from dataclasses import dataclass

@dataclass
class BoxDims:
    """Podstawowe wymiary pudełka (mm)."""
    width: float   # szerokość (front/back)
    height: float  # wysokość
    depth: float   # głębokość (boki)

@dataclass
class TechParams:
    """Parametry technologiczne (mm/°)."""
    glue_width: float = 10.0       # szerokość patki klejowej
    dust_flap: float = 8.0         # wysokość patki kurzowej (prosty wariant V3.1.1)

    # Offsety i tolerancje
    front_offset: float = 1.0      # o ile BACK jest węższy od FRONT (back = W - front_offset)
    front_crease_offset: float = 1.0  # big frontu podniesiony/opuszczony (± w Y)

    # Patka klejowa
    glue_angle: float = 15.0       # kąt skosu górnej/dolnej krawędzi (°)

    # Zatrzask klapki dolnej (front)
    bottom_triangle_h: float = 15.0  # wysokość trójkąta zatrzasku
    bottom_triangle_w: float = 24.0  # szerokość podstawy trójkąta zatrzasku

    # (rezerwa na przyszłe warianty patek/klapek)
    flap_variant: str = "rect"     # "rect" (na razie)
    dust_variant: str = "rect"     # "rect" (docelowo: "angled", "rounded", ...)
