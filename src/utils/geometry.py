"""
geometry.py
-----------
Helpery geometryczne: linie, kąty, przesunięcia.
"""

import math

def line_eq(p1, p2):
    """Zwraca (a, b) dla równania y = ax + b"""
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2:
        return None  # pionowa linia
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b

def offset_point(x, y, dx, dy):
    """Przesunięcie punktu (x, y) o (dx, dy)."""
    return x + dx, y + dy

def rotate_point(x, y, angle_deg, origin=(0, 0)):
    """Obrót punktu wokół origin o angle_deg."""
    ox, oy = origin
    rad = math.radians(angle_deg)
    qx = ox + math.cos(rad) * (x - ox) - math.sin(rad) * (y - oy)
    qy = oy + math.sin(rad) * (x - ox) + math.cos(rad) * (y - oy)
    return qx, qy
