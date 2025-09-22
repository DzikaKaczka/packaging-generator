"""
svg_helpers.py
--------------
Eksport do SVG.
"""

def save_svg(filename, cut_lines, crease_lines):
    with open(filename, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">\n')

        # Cut (czarne linie)
        f.write('<g id="Cut" stroke="black" stroke-width="0.2" fill="none">\n')
        for (x1, y1, x2, y2) in cut_lines:
            f.write(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />\n')
        f.write('</g>\n')

        # Crease (czerwone linie)
        f.write('<g id="Crease" stroke="red" stroke-width="0.2" fill="none">\n')
        for (x1, y1, x2, y2) in crease_lines:
            f.write(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />\n')
        f.write('</g>\n')

        f.write('</svg>\n')

    print(f"[OK] SVG zapisane: {filename}")
