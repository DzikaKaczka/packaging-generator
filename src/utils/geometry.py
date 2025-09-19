"""
geometry helpers (V3.2-clean)
"""
from typing import List, Tuple

Line = Tuple[float, float, float, float]

def _round(v: float, nd=4) -> float:
    return round(float(v), nd)

def _norm(line: Line, nd=4) -> Line:
    x1,y1,x2,y2 = map(lambda v: _round(v, nd), line)
    # niezależnie od kierunku: (A,B) == (B,A)
    if (x1,y1,x2,y2) > (x2,y2,x1,y1):
        return (x2,y2,x1,y1)
    return (x1,y1,x2,y2)

def add_line_safe(line: Line, pool: List[Line], tol: float = 0.05) -> None:
    """Dodaj linię, jeśli nie ma duplikatu w 'pool' (z tolerancją mm)."""
    x1,y1,x2,y2 = line
    for (a1,b1,a2,b2) in pool:
        if abs(x1-a1)<=tol and abs(y1-b1)<=tol and abs(x2-a2)<=tol and abs(y2-b2)<=tol:
            return
        if abs(x1-a2)<=tol and abs(y1-b2)<=tol and abs(x2-a1)<=tol and abs(y2-b1)<=tol:
            return
    pool.append((x1,y1,x2,y2))

def reconcile_layers(cut: List[Line], crease: List[Line], tol: float = 0.05):
    """
    Usuwa duplikaty i kolizje CUT vs CREASE.
    Zasada: jeśli linia występuje jako CUT i CREASE (z tolerancją), zostaje CREASE.
    """
    # znormalizowane słowniki dla deduplikacji
    cut_map   = {}
    crease_map= {}

    for l in cut:
        cut_map[_norm(l)] = l
    for l in crease:
        crease_map[_norm(l)] = l

    # jeśli ta sama (w normie) istnieje w obu → usuń z CUT
    for key in list(crease_map.keys()):
        if key in cut_map:
            cut_map.pop(key, None)

    # wynik bez duplikatów
    new_cut   = list(cut_map.values())
    new_creas = list(crease_map.values())
    return new_cut, new_creas

def bbox(lines: List[Line]):
    if not lines:
        return (0,0,0,0)
    xs = []
    ys = []
    for (x1,y1,x2,y2) in lines:
        xs += [x1,x2]
        ys += [y1,y2]
    return (min(xs), min(ys), max(xs), max(ys))
