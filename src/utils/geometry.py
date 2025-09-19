"""
geometry.py (V3.1.1)
--------------------
Prosta deduplikacja bez scalania paneli:
- usuwa duplikaty 1:1 (z tolerancją),
- jeśli ta sama linia występuje jako CUT i CREASE → zostaje CREASE.
"""

from typing import List, Tuple

Line = Tuple[float, float, float, float]

def _eq(a: float, b: float, tol: float) -> bool:
    return abs(a - b) <= tol

def _same_line(l1: Line, l2: Line, tol: float) -> bool:
    x1, y1, x2, y2 = l1
    a1, b1, a2, b2 = l2
    # ta sama orientacja i te same końce (lub odwrócone)
    same_dir = _eq(x1, a1, tol) and _eq(y1, b1, tol) and _eq(x2, a2, tol) and _eq(y2, b2, tol)
    rev_dir  = _eq(x1, a2, tol) and _eq(y1, b2, tol) and _eq(x2, a1, tol) and _eq(y2, b1, tol)
    return same_dir or rev_dir

def uniq(lines: List[Line], tol: float = 0.05) -> List[Line]:
    out: List[Line] = []
    for l in lines:
        if not any(_same_line(l, o, tol) for o in out):
            out.append(l)
    return out

def reconcile_layers(cut_lines: List[Line], crease_lines: List[Line], tol: float = 0.05):
    """Usuwa z CUT linie, które dokładnie pokrywają się z CREASE."""
    crease_u = uniq(crease_lines, tol)
    cut_u: List[Line] = []
    for l in cut_lines:
        if not any(_same_line(l, c, tol) for c in crease_u):
            cut_u.append(l)
    # na końcu usuń duplikaty RESZTY CUT
    cut_u = uniq(cut_u, tol)
    return cut_u, crease_u
