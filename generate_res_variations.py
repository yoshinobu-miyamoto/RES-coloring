from __future__ import annotations

import math
from pathlib import Path
from typing import Callable, Iterable, Tuple

W, H = 1536, 1024
OUTPUT = Path("outputs")
OUTPUT.mkdir(exist_ok=True)

Color = Tuple[int, int, int]


def rgb(c: Color) -> str:
    return f"rgb({c[0]},{c[1]},{c[2]})"


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def blend(c1: Color, c2: Color, t: float) -> Color:
    return (lerp(c1[0], c2[0], t), lerp(c1[1], c2[1], t), lerp(c1[2], c2[2], t))


def tri_grid(side: int = 78):
    tri_h = int(side * math.sqrt(3) / 2)
    for row, y in enumerate(range(-tri_h, H + tri_h, tri_h)):
        offset = 0 if row % 2 == 0 else side // 2
        for col, x in enumerate(range(-side, W + side, side)):
            p1 = (x + offset, y)
            p2 = (x + offset + side // 2, y + tri_h)
            p3 = (x + offset - side // 2, y + tri_h)
            cx = int((p1[0] + p2[0] + p3[0]) / 3)
            cy = int((p1[1] + p2[1] + p3[1]) / 3)
            yield row, col, (p1, p2, p3), cx, cy


def polygon(points: Iterable[tuple[int, int]]) -> str:
    return " ".join(f"{x},{y}" for x, y in points)


def svg_header(extra_defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
        "<defs>\n"
        f"{extra_defs}\n"
        "</defs>\n"
    )


def svg_footer() -> str:
    return "</svg>\n"


def save(name: str, body: str) -> None:
    out = OUTPUT / name
    out.write_text(body, encoding="utf-8")
    print(f"saved: {out}")


def make_a() -> None:
    palette = [(239, 71, 111), (255, 209, 102), (6, 214, 160), (17, 138, 178), (131, 56, 236), (255, 102, 0)]
    lines = [svg_header(), '<rect width="100%" height="100%" fill="rgb(248,248,252)"/>']
    for row, col, pts, _cx, _cy in tri_grid():
        c = palette[(row * 3 + col) % len(palette)]
        lines.append(f'<polygon points="{polygon(pts)}" fill="{rgb(c)}" stroke="rgb(35,35,35)" stroke-width="1"/>')
    lines.append('<text x="36" y="44" font-size="30" fill="rgb(10,10,10)">Variation A: Element-wise multicolor</text>')
    lines.append(svg_footer())
    save("res_variation_a_element_multicolor.svg", "\n".join(lines))


def make_b() -> None:
    defs = '<linearGradient id="g1" x1="0%" y1="0%" x2="0%" y2="100%">\n'
    for i in range(11):
        t = i / 10
        c = blend((255, 94, 98), (72, 52, 212), t)
        defs += f'<stop offset="{int(t*100)}%" stop-color="{rgb(c)}"/>\n'
    defs += "</linearGradient>"
    lines = [svg_header(defs), '<rect width="100%" height="100%" fill="rgb(250,250,255)"/>']
    for row, col, pts, _cx, _cy in tri_grid():
        lines.append(f'<polygon points="{polygon(pts)}" fill="url(#g1)" fill-opacity="0.94" stroke="rgb(35,35,35)" stroke-width="1"/>')
    lines.append('<text x="36" y="44" font-size="30" fill="rgb(10,10,10)">Variation B: Global gradient</text>')
    lines.append(svg_footer())
    save("res_variation_b_gradient.svg", "\n".join(lines))


def make_c() -> None:
    defs = """
<pattern id="stripe" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(25)">
  <rect width="16" height="16" fill="rgba(0,0,0,0)"/>
  <rect width="5" height="16" fill="rgba(20,20,20,0.45)"/>
</pattern>
<pattern id="dot" width="20" height="20" patternUnits="userSpaceOnUse">
  <circle cx="5" cy="5" r="3" fill="rgba(20,20,20,0.5)"/>
</pattern>
<pattern id="line" width="24" height="24" patternUnits="userSpaceOnUse">
  <path d="M0 0 H24" stroke="rgba(20,20,20,0.45)" stroke-width="3"/>
</pattern>
""".strip()
    palette = [(255, 183, 3), (251, 133, 0), (33, 158, 188), (142, 202, 230)]
    patterns = ["stripe", "dot", "line"]
    lines = [svg_header(defs), '<rect width="100%" height="100%" fill="rgb(247,251,255)"/>']

    for row, col, pts, _cx, _cy in tri_grid(88):
        base = palette[(row + col) % len(palette)]
        pat = patterns[(row * 2 + col) % len(patterns)]
        p = polygon(pts)
        lines.append(f'<polygon points="{p}" fill="{rgb(base)}" stroke="rgb(30,30,30)" stroke-width="1"/>')
        lines.append(f'<polygon points="{p}" fill="url(#{pat})"/>')

    lines.append('<text x="36" y="44" font-size="30" fill="rgb(10,10,10)">Variation C: Printed patterns</text>')
    lines.append(svg_footer())
    save("res_variation_c_pattern.svg", "\n".join(lines))


def make_d() -> None:
    lines = [svg_header(), '<rect width="100%" height="100%" fill="rgb(255,255,255)"/>']
    for _row, _col, pts, cx, cy in tri_grid():
        t = min(max(cy / H, 0), 1)
        if cx < W // 2:
            c = blend((255, 0, 110), (0, 187, 249), t)
        else:
            c = blend((235, 235, 235), (90, 90, 90), t)
        lines.append(
            f'<polygon points="{polygon(pts)}" fill="{rgb(c)}" fill-opacity="0.95" stroke="rgb(20,20,20)" stroke-width="1"/>'
        )
    lines.append(f'<line x1="{W//2}" y1="0" x2="{W//2}" y2="{H}" stroke="rgb(0,0,0)" stroke-opacity="0.7" stroke-width="4"/>')
    lines.append('<text x="36" y="44" font-size="30" fill="rgb(10,10,10)">Variation D: Front/Back-inspired hybrid</text>')
    lines.append(svg_footer())
    save("res_variation_d_hybrid_front_back.svg", "\n".join(lines))


def main() -> None:
    make_a()
    make_b()
    make_c()
    make_d()


if __name__ == "__main__":
    main()
