#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draws the figures for the explainer page, as SVG, from data/terms.json.

    python src/make_figures.py

Standard library only. SVG on purpose: sharp at any zoom, prints well, reads in
light and dark themes, and every number in it can be checked against the data,
which is what verify.py does.

Output: docs/figures/*.svg
"""
import json
import math
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "docs", "figures")

INK = "#1f2933"
MUTED = "#6b7785"
LINE = "#9aa5b1"
BLUE = "#2f6fb5"
GREEN = "#2e7d52"
AMBER = "#c8871a"
PURPLE = "#7a4fa3"
FONT = ("-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,"
        "'Helvetica Neue',Arial,sans-serif")


def head(w, h, title, desc):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'width="100%%" role="img" aria-labelledby="t d">\n'
        '<title id="t">%s</title><desc id="d">%s</desc>\n'
        '<style>\n'
        '  text{font-family:%s;fill:%s}\n'
        '  .m{fill:%s}.s{font-size:13px}.xs{font-size:11px}\n'
        '  .lbl{font-size:15px;font-weight:600}\n'
        '  .big{font-size:20px;font-weight:700}\n'
        '  .mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}\n'
        '  @media (prefers-color-scheme:dark){\n'
        '    text{fill:#e4e7eb}.m{fill:#9aa5b1}.stroke{stroke:#7b8794}\n'
        '  }\n'
        '</style>\n' % (w, h, title, desc, FONT, INK, MUTED))


def arrowdefs(name, color):
    return ('<defs><marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/></marker></defs>'
            % (name, color))


def write(name, body):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(body)
    print("  docs/figures/" + name)


def _ring(o, nodes, cx, cy, r, color, start=-90.0):
    """Coloca los vertices en circulo y devuelve sus posiciones."""
    pos = {}
    n = len(nodes)
    for i, v in enumerate(nodes):
        a = math.radians(start + 360.0 * i / n)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        pos[v] = (x, y)
        o.append('<circle cx="%.1f" cy="%.1f" r="25" fill="none" stroke="%s" '
                 'stroke-width="2.5" class="stroke"/>' % (x, y, color))
        o.append('<text class="lbl" x="%.1f" y="%.1f" text-anchor="middle">'
                 '%s</text>' % (x, y + 5, v))
    return pos


def _arc(o, p, q, color, marker="a"):
    (x1, y1), (x2, y2) = p, q
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy) or 1
    ux, uy = dx / d, dy / d
    sx, sy = x1 + 27 * ux, y1 + 27 * uy
    ex, ey = x2 - 29 * ux, y2 - 29 * uy
    mx, my = (sx + ex) / 2 - 0.16 * (ey - sy), (sy + ey) / 2 + 0.16 * (ex - sx)
    o.append('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f" stroke="%s" '
             'stroke-width="2" fill="none" marker-end="url(#%s)" '
             'class="stroke"/>' % (sx, sy, mx, my, ex, ey, color, marker))


# --------------------------------------------------------------------------
def fig_graph(es=False):
    """El digrafo de 234, con las cuentas al costado."""
    w, h = 700, 330
    T = {
        "title": ("El dibujo de 234" if es else "The drawing of 234"),
        "desc": ("234 = 2 x 3^2 x 13. Cada primo apunta a los primos de la suma "
                 "de divisores de su potencia, y queda un triangulo."
                 if es else
                 "234 = 2 x 3^2 x 13. Each prime points at the primes of the "
                 "sum of divisors of its power, forming a triangle."),
        "n": "234 = 2 × 3² × 13",
        "c1": "σ(2) = 1+2 = 3",
        "c2": "σ(3²) = 1+3+9 = 13",
        "c3": "σ(13) = 1+13 = 14 = 2 × 7",
        "r1": ("el 3 aparece → flecha 2 → 3" if es else "3 appears → arrow 2 → 3"),
        "r2": ("el 13 aparece → flecha 3 → 13" if es else "13 appears → arrow 3 → 13"),
        "r3": ("el 2 aparece → flecha 13 → 2" if es else "2 appears → arrow 13 → 2"),
        "out": ("Se cierra un triángulo: la CINTURA de 234 es 3"
                if es else "A triangle closes: the GIRTH of 234 is 3"),
    }
    o = [head(w, h, T["title"], T["desc"])]
    o.append('<text class="big" x="150" y="44" text-anchor="middle">%s</text>'
             % T["n"])
    pos = _ring(o, ["2", "3", "13"], 150, 180, 78, BLUE)
    for a, b in (("2", "3"), ("3", "13"), ("13", "2")):
        _arc(o, pos[a], pos[b], BLUE)
    o.append('<text class="s" x="150" y="300" text-anchor="middle" fill="%s" '
             'font-weight="600">%s</text>' % (GREEN, T["out"]))
    x0 = 330
    for i, (c, r) in enumerate((("c1", "r1"), ("c2", "r2"), ("c3", "r3"))):
        y = 92 + i * 62
        o.append('<text class="s mono" x="%d" y="%d">%s</text>' % (x0, y, T[c]))
        o.append('<text class="xs m" x="%d" y="%d">%s</text>'
                 % (x0, y + 20, T[r]))
    o.append(arrowdefs("a", LINE))
    o.append("</svg>\n")
    return "\n".join(o)


def fig_girth(es=False):
    """Que es la cintura: el ciclo mas corto."""
    w, h = 700, 300
    T = {
        "title": ("La cintura es el ciclo más corto" if es
                  else "Girth is the shortest cycle"),
        "desc": ("El 6 cierra un ciclo de dos flechas y el 234 uno de tres: sus "
                 "cinturas son 2 y 3." if es else
                 "6 closes a two-arrow cycle and 234 a three-arrow one: their "
                 "girths are 2 and 3."),
        "a": "6 = 2 × 3", "b": "234 = 2 × 3² × 13",
        "ka": ("cintura 2" if es else "girth 2"),
        "kb": ("cintura 3" if es else "girth 3"),
        "foot": ("La pregunta del trabajo: para cada k, ¿cuál es el número MÁS "
                 "CHICO de cintura k?" if es else
                 "The question of this work: for each k, what is the SMALLEST "
                 "number of girth k?"),
    }
    o = [head(w, h, T["title"], T["desc"])]
    o.append('<text class="s" x="170" y="44" text-anchor="middle" '
             'font-weight="600">%s</text>' % T["a"])
    pa = _ring(o, ["2", "3"], 170, 150, 62, GREEN, start=180)
    _arc(o, pa["2"], pa["3"], GREEN)
    _arc(o, pa["3"], pa["2"], GREEN)
    o.append('<text class="s" x="170" y="248" text-anchor="middle" fill="%s">'
             '%s</text>' % (GREEN, T["ka"]))
    o.append('<text class="s" x="500" y="44" text-anchor="middle" '
             'font-weight="600">%s</text>' % T["b"])
    pb = _ring(o, ["2", "3", "13"], 500, 150, 66, AMBER)
    for a, b in (("2", "3"), ("3", "13"), ("13", "2")):
        _arc(o, pb[a], pb[b], AMBER)
    o.append('<text class="s" x="500" y="248" text-anchor="middle" fill="%s">'
             '%s</text>' % (AMBER, T["kb"]))
    o.append('<text class="xs m" x="350" y="284" text-anchor="middle">%s</text>'
             % T["foot"])
    o.append(arrowdefs("a", LINE))
    o.append("</svg>\n")
    return "\n".join(o)


def fig_terms(terms, es=False):
    """El tamano de los menores testigos, en escala logaritmica."""
    w, h = 760, 400
    pad_l, pad_r, pad_t, pad_b = 62, 22, 40, 92
    gw, gh = w - pad_l - pad_r, h - pad_t - pad_b
    series = [("sigma", BLUE, "σ"), ("sigma*", AMBER, "σ*"),
              ("phi*", PURPLE, "φ*")]
    ks = list(range(2, 10))
    mx = 0
    for name, _, _ in series:
        for e in terms[name]:
            mx = max(mx, math.log10(e["n"]))
    T = {
        "title": ("Cuánto crece el número más chico de cada cintura" if es
                  else "How the smallest number of each girth grows"),
        "desc": ("En escala logaritmica: cada escalon hacia arriba es multiplicar "
                 "por diez." if es else
                 "On a logarithmic scale: each step up multiplies by ten."),
        "y": ("cantidad de cifras del número" if es
              else "number of digits"),
        "x": ("cintura k" if es else "girth k"),
        "foot": ("Los puntos rellenos son los que este trabajo calculó por "
                 "primera vez." if es else
                 "Filled dots are the ones this work computed first."),
    }
    o = [head(w, h, T["title"], T["desc"])]
    o.append('<text class="xs m" x="14" y="%d" text-anchor="middle" '
             'transform="rotate(-90 14 %d)">%s</text>'
             % (pad_t + gh // 2, pad_t + gh // 2, T["y"]))
    o.append('<text class="xs m" x="%d" y="%d" text-anchor="middle">%s</text>'
             % (pad_l + gw // 2, h - 52, T["x"]))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" '
             'stroke-width="1.5" class="stroke"/>'
             % (pad_l, pad_t + gh, pad_l + gw, pad_t + gh, LINE))
    for d in range(0, int(mx) + 3, 3):
        yy = pad_t + gh - gh * d / (mx + 1)
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                 'stroke-width="1" stroke-dasharray="3 4" opacity="0.45" '
                 'class="stroke"/>' % (pad_l, yy, pad_l + gw, yy, LINE))
        o.append('<text class="xs m" x="%d" y="%.1f" text-anchor="end">%d</text>'
                 % (pad_l - 8, yy + 4, d))
    step = gw / (len(ks) - 1)
    for i, k in enumerate(ks):
        x = pad_l + i * step
        o.append('<text class="xs m" x="%.1f" y="%d" text-anchor="middle">%d'
                 '</text>' % (x, pad_t + gh + 18, k))
    for name, col, lab in series:
        pts = []
        for e in terms[name]:
            i = e["girth"] - 2
            x = pad_l + i * step
            y = pad_t + gh - gh * math.log10(e["n"]) / (mx + 1)
            pts.append((x, y, e.get("first_computed_here", False)))
        if len(pts) > 1:
            o.append('<polyline points="%s" fill="none" stroke="%s" '
                     'stroke-width="2" opacity="0.75"/>'
                     % (" ".join("%.1f,%.1f" % (p[0], p[1]) for p in pts), col))
        for x, y, nuevo in pts:
            o.append('<circle cx="%.1f" cy="%.1f" r="5.5" fill="%s" '
                     'stroke="%s" stroke-width="2"/>'
                     % (x, y, col if nuevo else "none", col))
        lx, ly = pts[-1][0], pts[-1][1]
        o.append('<text class="s" x="%.1f" y="%.1f" fill="%s" '
                 'font-weight="700">%s</text>' % (lx + 12, ly + 5, col, lab))
    o.append('<text class="xs m" x="%d" y="%d">%s</text>'
             % (pad_l, h - 22, T["foot"]))
    o.append("</svg>\n")
    return "\n".join(o)


def fig_cutoff(es=False):
    """De 'el mas chico que vimos' a 'el mas chico'."""
    w, h = 720, 290
    T = {
        "title": ("De «el más chico que vimos» a «el más chico»" if es
                  else "From 'the smallest we saw' to 'the smallest'"),
        "desc": ("El lema de corte acota el mayor primo posible, y entonces la "
                 "busqueda se vuelve finita." if es else
                 "The cutoff lemma bounds the largest possible prime, so the "
                 "search becomes finite."),
        "a1": ("ANTES: se probaban primos hasta donde alguien miró"
               if es else "BEFORE: primes were tried as far as somebody looked"),
        "a2": ("…y siempre quedaba la duda de si más allá había uno mejor"
               if es else "…and it was never clear whether a better one lay beyond"),
        "b1": ("AHORA: se demuestra que ningún primo por encima del corte sirve"
               if es else "NOW: no prime above the cutoff can work, and that is proved"),
        "b2": ("…así que revisar hasta ahí es revisar TODO"
               if es else "…so checking up to there is checking EVERYTHING"),
        "cut": ("corte demostrado" if es else "proved cutoff"),
        "inf": "∞",
    }
    o = [head(w, h, T["title"], T["desc"])]
    o.append('<text class="xs" x="34" y="46" fill="%s" font-weight="700">%s</text>'
             % (MUTED, T["a1"]))
    o.append('<line x1="34" y1="74" x2="640" y2="74" stroke="%s" '
             'stroke-width="2" class="stroke" stroke-dasharray="6 5"/>' % LINE)
    o.append('<rect x="34" y="62" width="300" height="24" rx="6" fill="%s" '
             'opacity="0.22"/>' % LINE)
    o.append('<text class="xs m" x="660" y="79">%s</text>' % T["inf"])
    o.append('<text class="xs m" x="34" y="106">%s</text>' % T["a2"])
    o.append('<text class="xs" x="34" y="168" fill="%s" font-weight="700">%s</text>'
             % (GREEN, T["b1"]))
    o.append('<line x1="34" y1="196" x2="640" y2="196" stroke="%s" '
             'stroke-width="2" class="stroke" stroke-dasharray="6 5"/>' % LINE)
    o.append('<rect x="34" y="184" width="300" height="24" rx="6" fill="%s" '
             'opacity="0.3"/>' % GREEN)
    o.append('<line x1="334" y1="168" x2="334" y2="224" stroke="%s" '
             'stroke-width="3"/>' % GREEN)
    o.append('<text class="xs" x="342" y="222" fill="%s" font-weight="600">%s'
             '</text>' % (GREEN, T["cut"]))
    o.append('<text class="xs m" x="660" y="201">%s</text>' % T["inf"])
    o.append('<text class="xs m" x="34" y="256">%s</text>' % T["b2"])
    o.append("</svg>\n")
    return "\n".join(o)


def main():
    with open(os.path.join(HERE, "data", "terms.json"), encoding="utf-8") as fh:
        terms = json.load(fh)["functions"]
    print("figures:")
    for es, suf in ((False, ""), (True, ".es")):
        write("graph%s.svg" % suf, fig_graph(es=es))
        write("girth%s.svg" % suf, fig_girth(es=es))
        write("terms%s.svg" % suf, fig_terms(terms, es=es))
        write("cutoff%s.svg" % suf, fig_cutoff(es=es))


if __name__ == "__main__":
    main()
