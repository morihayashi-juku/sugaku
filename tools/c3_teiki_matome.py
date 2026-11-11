"""中3 定期テスト対策 まとめ（二次方程式・関数 y＝ax²・相似）2パターン＋こたえ（問題に赤で書き込んだ形）

  cd tools && python3 c3_teiki_matome.py

- A3 に拡大して印刷する想定。ファイルは A4 で、1ページに左右2列・1ページ＝1パターン（①②）。
  左＝［1］二次方程式4問（×3）・［2］二次方程式の利用2問（×4）・［3］y＝ax²（式・グラフ・変域2問、×3）
  右＝［4］相似と長さ4問（×4）・［5］相似の証明の穴うめ3か所（×4）　計60点
- 1つの HTML から、赤字（.a）を消した問題と、赤字を出したこたえを作る（こたえは問題と同じ並び）。
- 出力：pdf/c3_teiki_matome.pdf と c3_teiki_matome_ans.pdf
- 答えは SymPy と図の座標で確かめる（check）。
"""
import math
from fractions import Fraction as F

import sympy as sp

from c3_souji_nagasa import Fig, tri
from c3_teiki_niji_ax2 import coef, dom_tex, dots, graph
from texlib import doc, tex as T, write_pdfs

FILE = "c3_teiki_matome"
NO = "①②"
X_, Y_ = T("x"), T("y")


def S(name):
    return T(r"\mathrm{%s}" % name)


def TR(name):
    return T(r"\triangle\mathrm{%s}" % name)


def SIM(a, b):
    return T(r"\triangle\mathrm{%s}\backsim\triangle\mathrm{%s}" % (a, b))


def A(s):
    """こたえの赤字（問題では見えない・場所はとったまま）"""
    return f"<span class=a>{s}</span>"


# ---------- 図（相似） ----------
def on(P, Q, r):
    return (P[0] + (Q[0] - P[0]) * r, P[1] + (Q[1] - P[1]) * r)


def butterfly(oa, ob, ab, k):
    """O を中心に、上に B（左）・A（右）、下に −kA・−kB。AB と下の辺は平行"""
    t = tri(oa, ab, ob, "OAB")              # OA, AB, BO
    ox, oy = t["O"]
    a = (ox - t["A"][0], oy - t["A"][1])
    b = (ox - t["B"][0], oy - t["B"][1])
    return (0.0, 0.0), a, b, (-a[0] * k, -a[1] * k), (-b[0] * k, -b[1] * k)


def fig_par(ab, bc, ca, r, s, labels):
    """DE∥BC（D は AB 上、E は AC 上、AD：AB＝r）"""
    t = tri(ab, bc, ca)
    A_, B_, C_ = t["A"], t["B"], t["C"]
    f = Fig({"A": A_, "B": B_, "C": C_, "D": on(A_, B_, r), "E": on(A_, C_, r)}, s)
    f.pad = 7
    f.poly("ABC").line("D", "E").par("D", "E").par("B", "C").label(D=(-3.2, -2.4), E=(3.4, -.6))
    for a, b, text, val, kw in labels:
        f.side(a, b, text, val, **kw)
    return f


def fig_bf(oa, ob, ab, k, s, names, labels, lab=None):
    """ちょうちょ形。names＝(O, 上右, 上左, 下左, 下右)"""
    o, a, b, c, d = butterfly(oa, ob, ab, k)
    n = dict(zip(names, (o, a, b, c, d)))
    f = Fig(n, s)
    f.pad = 7
    no, na, nb, nc, nd = names
    f.line(na, nb).line(nc, nd).line(na, nc).line(nb, nd)
    f.label(**{no: (4.2, .8)}, **(lab or {}))
    for a_, b_, text, val, kw in labels:
        f.side(a_, b_, text, val, **kw)
    return f


def fig_angle(ab, bc, ca, s, labels, lab=None):
    """∠ABC＝∠ACD（D は AB 上、AD＝AC²／AB）"""
    t = tri(ab, bc, ca)
    A_, B_, C_ = t["A"], t["B"], t["C"]
    D_ = on(A_, B_, ca * ca / ab / ab)
    f = Fig({"A": A_, "B": B_, "C": C_, "D": D_}, s)
    f.pad = 7
    f.poly("ABC").line("C", "D").angle("A", "B", "C").angle("A", "C", "D").label(**(lab or {}))
    assert abs(ang(f, "A", "B", "C") - ang(f, "A", "C", "D")) < 1e-9
    for a, b, text, val, kw in labels:
        f.side(a, b, text, val, **kw)
    return f


def fig_right(bd, dc, s, labels, lab=None):
    """∠BAC＝90°、AD⊥BC（BD・DC から A の高さを決める）"""
    h = math.sqrt(bd * dc)
    f = Fig({"A": (bd, h), "B": (0, 0), "C": (bd + dc, 0), "D": (bd, 0)}, s)
    f.pad = 7
    f.poly("ABC").line("A", "D").right("B", "A", "C").right("A", "D", "C").label(**(lab or {}))
    assert abs(ang(f, "B", "A", "C") - math.pi / 2) < 1e-9
    for a, b, text, val, kw in labels:
        f.side(a, b, text, val, **kw)
    return f


def ang(f, p, v, q):
    (a, b), (c, d), (e, g) = f.p[p], f.p[v], f.p[q]
    return math.atan2(abs((a - c) * (g - d) - (b - d) * (e - c)), (a - c) * (e - c) + (b - d) * (g - d))


def fig_proof_angle():
    """△ADE∽△ACB（∠ADE＝∠ACB）AB＝10，AC＝8，AD＝4，AE＝5"""
    t = tri(10, 9, 8)
    A_, B_, C_ = t["A"], t["B"], t["C"]
    f = Fig({"A": A_, "B": B_, "C": C_, "D": on(A_, B_, .4), "E": on(A_, C_, 5 / 8)}, 3.4)
    f.pad = 6
    f.poly("ABC").line("D", "E").angle("A", "D", "E").angle("A", "C", "B").label(D=(-3.4, -.4), E=(3.4, -.4))
    assert abs(ang(f, "A", "D", "E") - ang(f, "A", "C", "B")) < 1e-9
    return f


def fig_proof_sas():
    """OA＝4，OC＝6，OB＝6，OD＝9"""
    o, a, b, c, d = butterfly(4, 6, 7, 1.5)
    f = Fig({"O": o, "A": a, "B": b, "C": c, "D": d}, 2.6)
    f.pad = 6
    f.line("A", "B").line("C", "D").line("A", "C").line("B", "D").label(O=(4.2, .8))
    f.side("O", "A", 4, 4, at=(2.8, 2.6)).side("O", "C", 6, 6, at=(-3.6, -2.4))
    f.side("O", "B", 6, 6, at=(-3.6, 2.6)).side("O", "D", 9, 9, at=(3.8, -2.4))
    return f


# ---------- 問題のデータ ----------
def sol(*s):
    return "，".join(T(f"x={v}") for v in s)


PATTERNS = [
    {
        "eqs": [
            ("x^2-3x-28=0", ["(x-7)(x+4)=0"], sol(7, -4)),
            ("3x^2-48=0", ["x^2=16"], T(r"x=\pm 4")),
            ("x^2+5x+3=0", [r"x=\dfrac{-5\pm\sqrt{5^2-4\times1\times3}}{2}"], T(r"x=\dfrac{-5\pm\sqrt{13}}{2}")),
            ("(x+2)(x-5)=8", ["x^2-3x-10=8", "x^2-3x-18=0", "(x-6)(x+3)=0"], sol(6, -3)),
        ],
        "words": [
            ("連続する2つの正の偶数があります。この2つの数の積が168のとき，2つの偶数を求めなさい。",
             [f"小さい方を {X_} とすると，大きい方は {T('x+2')}", T("x(x+2)=168"), T("x^2+2x-168=0"),
              T("(x+14)(x-12)=0") + "　" + T("x=-14,\\ 12"), f"{X_} は正の偶数だから {T('x=12')}"], "12，14"),
            ("たての長さがよこの長さより4cm長い長方形があり，面積は60cm²です。よこの長さを求めなさい。",
             [f"よこを {X_} cm とすると，たては {T('(x+4)')} cm", T("x(x+4)=60"), T("x^2+4x-60=0"),
              T("(x+10)(x-6)=0") + "　" + T("x=-10,\\ 6"), f"{T('x>0')} だから {T('x=6')}"], "6cm"),
        ],
        "p1": (3, -18, -2),
        "graph": [(F(1, 2), None), (F(-1), (-2, 3))],
        "ranges": [(F(3), (-1, 2), (0, 12)), (F(-1, 2), (2, 4), (-8, -2))],
        "sim": [
            ("par", f"{S('DE')} ∥ {S('BC')}", "ADE", "ABC", ["4:6=x:9"], 6),
            ("bf", f"{S('AB')} ∥ {S('DC')}", "OAB", "ODC", ["4:6=6:x"], 9),
            ("ang", f"{T(r'\angle\mathrm{ABC}=\angle\mathrm{ACD}')}<br>{T(r'\mathrm{AB}=9')}cm", "ACD", "ABC", ["6:9=x:6"], 4),
            ("right", f"{T(r'\angle\mathrm{BAC}=90^\circ')}，{S('AD')} ⊥ {S('BC')}", "ABD", "CAD", ["4:x=x:9", "x^2=36"], 6),
        ],
        "proof": "angle",
    },
    {
        "eqs": [
            ("x^2+2x-35=0", ["(x+7)(x-5)=0"], sol(-7, 5)),
            ("(x-3)^2=25", [r"x-3=\pm 5"], sol(8, -2)),
            ("2x^2-3x-1=0", [r"x=\dfrac{3\pm\sqrt{9+8}}{4}"], T(r"x=\dfrac{3\pm\sqrt{17}}{4}")),
            ("x(x+4)=3(x+2)", ["x^2+4x=3x+6", "x^2+x-6=0", "(x+3)(x-2)=0"], sol(-3, 2)),
        ],
        "words": [
            ("ある正の数の2乗を3倍した数は，もとの数を15倍した数と等しくなります。この正の数を求めなさい。",
             [f"ある正の数を {X_} とすると", T("3x^2=15x"), T("3x^2-15x=0"),
              T("3x(x-5)=0") + "　" + T("x=0,\\ 5"), f"{X_} は正の数だから {T('x=5')}"], "5"),
            (f"1辺 {X_} cm の正方形の厚紙の4すみから1辺2cmの正方形を切り取り，ふたのない箱をつくると，容積は72cm³になりました。{X_} の値を求めなさい。",
             [f"底面の1辺は {T('(x-4)')} cm，高さは2cm", T("2(x-4)^2=72"), T("(x-4)^2=36"),
              T(r"x-4=\pm 6") + "　" + T("x=10,\\ -2"), f"{T('x>4')} だから {T('x=10')}"], T("x=10")),
        ],
        "p1": (-2, 12, 3),
        "graph": [(F(-1, 4), None), (F(2), (-1, 2))],
        "ranges": [(F(-3), (-2, 1), (-12, 0)), (F(1, 4), (-6, -2), (1, 9))],
        "sim": [
            ("par", f"{S('DE')} ∥ {S('BC')}", "ADE", "ABC", ["6:10=x:15"], 9),
            ("bf", f"{S('AB')} ∥ {S('DC')}", "OAB", "OCD", ["4:6=x:9"], 6),
            ("ang", f"{T(r'\angle\mathrm{ABC}=\angle\mathrm{ACD}')}<br>{T(r'\mathrm{AB}=12')}cm", "ACD", "ABC", ["6:12=x:14"], 7),
            ("right", f"{T(r'\angle\mathrm{BAC}=90^\circ')}，{S('AD')} ⊥ {S('BC')}<br>{T(r'\mathrm{BC}=9')}cm", "ABC", "DBA", ["6:x=9:6", "9x=36"], 4),
        ],
        "proof": "sas",
    },
]

GRID = dict(ymin=-9, ymax=9, xlab=(-4, -2, 2, 4), ylab=(-8, -4, 4, 8))


def sim_figs(i):
    """パターン i の［4］の図（4つ）"""
    if i == 0:
        return [
            fig_par(6, 9, 8, 4 / 6, 3.3, [("A", "D", 4, 4, {}), ("D", "B", 2, 2, dict(at=(-5.5, 1.2))),
                                          ("D", "E", "x", 6, dict(at=(-5, -1.6))), ("B", "C", 9, 9, {})]),
            fig_bf(4, 5, 6, 1.5, 2.55, ("O", "A", "B", "D", "C"),
                   [("O", "A", 4, 4, dict(at=(3.2, 2.4))), ("O", "D", 6, 6, dict(at=(-4, -2))),
                    ("A", "B", 6, 6, {}), ("D", "C", "x", 9, {})]),
            fig_angle(9, 10, 6, 3.2, [("A", "D", "x", 4, {}), ("A", "C", 6, 6, {}),
                                      ("B", "C", 10, 10, {})], lab=dict(D=(-3, -2))),
            fig_right(4, 9, 2.6, [("B", "D", 4, 4, {}), ("D", "C", 9, 9, {}),
                                  ("A", "D", "x", 6, dict(at=(-4, 0)))], lab=dict(D=(0, 3.6))),
        ]
    return [
        fig_par(10, 15, 12, .6, 2.15, [("A", "D", 6, 6, {}), ("D", "B", 4, 4, {}),
                                       ("D", "E", "x", 9, dict(at=(0, -2.2))), ("B", "C", 15, 15, {})]),
        fig_bf(5, 4, 6, 1.5, 2.7, ("O", "A", "B", "D", "C"),
               [("O", "B", 4, 4, dict(at=(-4, 1))), ("O", "C", 6, 6, dict(at=(4.5, -1))),
                ("A", "B", "x", 6, {}), ("D", "C", 9, 9, {})]),
        fig_angle(12, 14, 6, 2.3, [("A", "C", 6, 6, {}), ("B", "C", 14, 14, {}),
                                    ("C", "D", "x", 7, dict(at=(-1, 3.4)))], lab=dict(D=(-3, -2))),
        fig_right(4, 5, 3.0, [("A", "B", 6, 6, {}), ("B", "D", "x", 4, {})], lab=dict(D=(2.2, 3.6))),
    ]


# ---------- チェック ----------
def check():
    x, a = sp.symbols("x a")

    def P(s):
        s = s.replace("^", "**").replace(r"\pm", "")
        import re
        s = re.sub(r"(\d)([x(])", r"\1*\2", s).replace(")(", ")*(").replace("x(", "x*(")
        l, r = s.split("=")
        return sp.sympify(l) - sp.sympify(r)

    want = [[{7, -4}, {4, -4}, set(sp.solve(x**2 + 5 * x + 3, x)), {6, -3}],
            [{-7, 5}, {8, -2}, set(sp.solve(2 * x**2 - 3 * x - 1, x)), {-3, 2}]]
    for pt, w in zip(PATTERNS, want):
        for (q, steps, _), ws in zip(pt["eqs"], w):
            assert set(sp.solve(P(q), x)) == ws, q
            for st in steps:
                if "pm" not in st and "dfrac" not in st:
                    assert set(sp.solve(P(st), x)) == ws, (q, st)
    assert set(sp.solve(x**2 + 5 * x + 3, x)) == {(-5 + sp.sqrt(13)) / 2, (-5 - sp.sqrt(13)) / 2}
    assert set(sp.solve(2 * x**2 - 3 * x - 1, x)) == {(3 + sp.sqrt(17)) / 4, (3 - sp.sqrt(17)) / 4}
    # 文章題
    assert 12 * 14 == 168 and set(sp.solve(x * (x + 2) - 168, x)) == {12, -14}
    assert set(sp.solve(x * (x + 4) - 60, x)) == {6, -10}
    assert set(sp.solve(3 * x**2 - 15 * x, x)) == {0, 5}
    assert set(sp.solve(2 * (x - 4)**2 - 72, x)) == {10, -2} and 2 * 6 * 6 == 72
    # y=ax²
    for pt in PATTERNS:
        px, py, k = pt["p1"]
        assert k * px**2 == py
        for k, (lo, hi), ans in pt["ranges"]:
            v = [k * lo**2, k * hi**2] + ([F(0)] if lo <= 0 <= hi else [])
            assert (min(v), max(v)) == ans, (k, lo, hi)
        for k, dom in pt["graph"]:
            ds = dots(k, dom, GRID)
            assert len(ds) >= 3 and (not dom or (dom[0] in ds and dom[1] in ds)), (k, dom)
    # 相似（図の長さは Fig.side が座標と照らし合わせる）
    assert F(4, 6) * 9 == 6 and F(6, 4) * 6 == 9 and F(6 * 6, 9) == 4 and 4 * 9 == 36
    assert F(6, 10) * 15 == 9 and F(4, 6) * 9 == 6 and F(6, 12) * 14 == 7 and F(36, 9) == 4
    for i in range(2):
        sim_figs(i)
    fig_proof_angle()
    fig_proof_sas()
    print("確認OK：方程式・文章題・y＝ax²・相似の長さと図")


# ---------- ページ ----------
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; font-size: 9.4pt; }
.page { width: 210mm; height: 297mm; padding: 9mm 11mm 9mm; page-break-after: always;
        display: flex; flex-direction: column; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.katex { font-size: 1.1em; }
.a { color: #c8102e; }
.q .a .katex, .a .katex { color: #c8102e; }
.hide .a { visibility: hidden; }
.head { display: flex; align-items: baseline; white-space: nowrap; border-bottom: 1pt solid #111; padding-bottom: 1.5mm; flex: none; }
.head b { font-size: 12.5pt; }
.head .kai { color: #c8102e; }
.head .sub { font-size: 8.6pt; margin-left: 2mm; }
.head .cl { font-size: 8.6pt; margin-left: auto; }
.head .u { display: inline-block; border-bottom: .7pt solid #111; }
.head .pts { margin-left: 3mm; font-size: 9pt; }
.cols { flex: 1; min-height: 0; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); margin-top: 2mm; }
.col { display: flex; flex-direction: column; min-height: 0; }
.col:first-child { padding-right: 4mm; border-right: .7pt solid #111; }
.col:last-child { padding-left: 4mm; }
.big { font-weight: 700; display: flex; align-items: center; gap: 1.5mm; white-space: nowrap; flex: none; margin-top: 2mm; }
.big:first-child { margin-top: 0; }
.big .box { display: inline-flex; width: 5mm; height: 5mm; border: .8pt solid #111; align-items: center; justify-content: center; font-size: 9.5pt; }
.big small { font-size: 7.8pt; font-weight: 400; }
.big .pill { font-size: 6.8pt; font-weight: 400; border: .7pt solid #111; border-radius: 3mm; padding: .1mm 1.5mm; }
.no { font-size: 7.6pt; flex: none; width: 6mm; padding-top: .6mm; }
.st { display: block; font-size: 8.8pt; line-height: 1.55; }
.ln { border-bottom: .9pt solid #111; width: 40mm; margin-left: auto; height: 6mm; text-align: center; flex: none;
      display: flex; align-items: flex-end; justify-content: center; padding-bottom: .4mm; }
/* ［1］ */
.eqs { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); grid-template-rows: 1fr 1fr; flex: 0 0 47mm; margin-top: 1mm; }
.e { display: flex; }
.e .q { font-size: 10pt; white-space: nowrap; }
.e .st { margin-top: .3mm; font-size: 8.4pt; line-height: 1.35; }
/* ［2］ */
.words { display: flex; flex-direction: column; gap: 1.5mm; flex: none; margin-top: 1mm; }
.w { display: flex; flex-direction: column; }
.w .tx { display: flex; line-height: 1.6; }
.w .wk { min-height: 22mm; padding-left: 6mm; }
.w .wk .st { line-height: 1.38; font-size: 8.5pt; }
.w .ln { margin-top: -1mm; }
.w .ln { width: 30mm; }
/* ［3］ */
.r { display: flex; line-height: 1.6; margin-top: 1mm; }
.gq { display: flex; justify-content: space-between; margin-top: 1.5mm; flex: none; }
.gtext { line-height: 1.6; }
.gtext .eq { margin-top: 2.5mm; margin-left: 2mm; font-size: 10pt; white-space: nowrap; }
.gtext .dm { margin-left: 5.5mm; white-space: nowrap; }
.gtext .care { margin-top: 2.5mm; font-size: 7.6pt; }
.gr text { font-family: 'Noto Sans CJK JP'; }
.rng { flex: 1; min-height: 0; display: grid; grid-template-rows: 1fr 1fr; }
.rng > div { display: flex; flex-direction: column; justify-content: space-between; }
/* ［4］ */
.sims { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); grid-template-rows: 1fr 1fr; column-gap: 2mm; flex: 0 0 158mm; margin-top: 1mm; }
.sm { display: flex; flex-direction: column; min-height: 0; }
.sm .tx { display: flex; line-height: 1.5; font-size: 8.8pt; }
.sm .fg { display: flex; justify-content: center; flex: none; }
.sm .wk { flex: 1; padding-left: 1mm; }
.sm .ln { width: 27mm; }
.fig text { fill: #111; }
.fig, .gr { flex: none; }
/* ［5］ */
.pf { flex: 1; min-height: 0; display: flex; flex-direction: column; margin-top: 1mm; }
.pf .top { display: flex; justify-content: space-between; align-items: flex-start; }
.pf .top .tx { line-height: 1.6; padding-top: 1mm; padding-right: 2mm; }
.pbox { border: .8pt solid #111; padding: 2mm 2.5mm; line-height: 2.25; margin-top: 1mm; }
.bl { display: inline-block; border: .8pt solid #111; min-width: 22mm; height: 6.4mm; line-height: 6mm; text-align: center;
      vertical-align: middle; padding: 0 1mm; position: relative; }
.bl .k { position: absolute; left: .6mm; top: -.2mm; font-size: 6.5pt; line-height: 1; color: #111; }
.bl.wide { display: block; width: 100%; margin: .8mm 0; }
"""


def head(i, ans):
    kai = "<span class=kai>【解答】</span>" if ans else ""
    return (f"<div class=head><b>中3数学 定期テスト対策 {NO[i]}{kai}</b>"
            f"<span class=sub>二次方程式・関数 {T('y=ax^2')}・相似</span>"
            f"<span class=cl>名前 <span class=u style='width:32mm'></span></span>"
            f"<span class=pts><span class=u style='width:9mm'></span>／60点</span></div>")


def big(n, text, small="", pill=""):
    return (f"<div class=big><span class=box>{n}</span>{text}"
            f"{f'<small>{small}</small>' if small else ''}{f'<span class=pill>{pill}</span>' if pill else ''}</div>")


def bl(k, text, wide=False):
    return f"<span class='bl{' wide' if wide else ''}'><span class=k>{k}</span>{A(text)}</span>"


def proof(kind):
    if kind == "angle":
        f = fig_proof_angle()
        top = (f"右の図で，{T(r'\angle\mathrm{ADE}=\angle\mathrm{ACB}')} のとき，"
               f"{SIM('ADE', 'ACB')} であることを次のように証明しました。□をうめなさい。")
        body = (f"{TR('ADE')} と {TR('ACB')} において<br>"
                f"仮定より　{T(r'\angle\mathrm{ADE}=')} {bl('ア', T(r'\angle\mathrm{ACB}'))}　……①<br>"
                f"{bl('イ', '共通')} な角だから　{T(r'\angle\mathrm{DAE}=\angle\mathrm{CAB}')}　……②<br>"
                f"①，②より，{bl('ウ', '2組の角がそれぞれ等しい', True)}"
                f"から　{SIM('ADE', 'ACB')}")
    else:
        f = fig_proof_sas()
        top = (f"右の図で，線分 {S('AC')} と {S('BD')} の交点を {S('O')} とします。"
               f"{SIM('OAB', 'OCD')} であることを次のように証明しました。□をうめなさい。")
        body = (f"{TR('OAB')} と {TR('OCD')} において<br>"
                f"{T(r'\mathrm{OA}:\mathrm{OC}=4:6=2:3')}　……①<br>"
                f"{T(r'\mathrm{OB}:\mathrm{OD}=6:9=')} {bl('ア', T('2:3'))}　……②<br>"
                f"{bl('イ', '対頂角')} は等しいから　{T(r'\angle\mathrm{AOB}=\angle\mathrm{COD}')} …③<br>"
                f"①〜③より，{bl('ウ', '2組の辺の比とその間の角がそれぞれ等しい', True)}"
                f"から　{SIM('OAB', 'OCD')}")
    return (f"<div class=pf><div class=top><div class=tx>{top}</div>{f.svg()}</div>"
            f"<div class=pbox>{body}</div></div>")


def page(i, pt, ans):
    eqs = ""
    for n, (q, steps, res) in enumerate(pt["eqs"]):
        mid = "".join(f"<span class=st>{A(T(s))}</span>" for s in steps)
        eqs += (f"<div class=e><span class=no>({n + 1})</span><div><span class=q>{T(q)}</span>"
                f"{mid}<span class=st>{A('<b>' + res + '</b>')}</span></div></div>")
    words = ""
    for n, (q, steps, res) in enumerate(pt["words"]):
        wk = "".join(f"<span class=st>{A(s)}</span>" for s in steps)
        words += (f"<div class=w><div class=tx><span class=no>({n + 1})</span><div>{q}</div></div>"
                  f"<div class=wk>{wk}</div><div class=ln>答　{A(res)}</div></div>")
    px, py, k1 = pt["p1"]
    gtext = ""
    for j, (k, dom) in enumerate(pt["graph"]):
        gtext += f"<div class=eq>{NO[j]} {T(coef(k))}</div>"
        if dom:
            gtext += f"<div class=dm>{T('(' + dom_tex(dom) + ')')}</div>"
    gsvg = graph(GRID, 2.85, pt["graph"] if ans else ())
    rng = ""
    for j, (k, d, (lo, hi)) in enumerate(pt["ranges"]):
        rng += (f"<div><div class=r><span class=no>({j + 3})</span><div>{T(coef(k))} で，{T(dom_tex(d))} のときの "
                f"{Y_} の変域を求めなさい。</div></div><div class=ln>{A(T(f'{lo}' + chr(92) + 'leqq y' + chr(92) + f'leqq {hi}'))}</div></div>")
    sims = ""
    for n, ((kind, cond, t1, t2, wk, res), f) in enumerate(zip(pt["sim"], sim_figs(i))):
        w = f"<span class=st>{A(SIM(t1, t2))}</span>" + "".join(f"<span class=st>{A(T(s))}</span>" for s in wk)
        sims += (f"<div class=sm><div class=tx><span class=no>({n + 1})</span><div>{cond}</div></div>"
                 f"<div class=fg>{f.svg()}</div><div class=wk>{w}</div>"
                 f"<div class=ln>{X_}＝{A(T(str(res)))}</div></div>")
    return f"""<div class="page{'' if ans else ' hide'}">{head(i, ans)}<div class=cols>
<div class=col>
{big(1, "次の二次方程式を解きなさい。", "（×3点）")}<div class=eqs>{eqs}</div>
{big(2, "次の問いに答えなさい。", "（×4点）", "※途中の式も書くこと")}<div class=words>{words}</div>
{big(3, "次の問いに答えなさい。", "（×3点）")}
<div class=r><span class=no>(1)</span><div>{Y_} は {X_} の2乗に比例し，{T(f'x={px}')} のとき {T(f'y={py}')} です。{Y_} を {X_} の式で表しなさい。</div></div>
<div class=ln>{A(T(coef(F(k1))))}</div>
<div class=gq><div class=gtext><div class=r style="margin-top:0"><span class=no>(2)</span><div>次のグラフを右の<br>座標平面にかきなさい。</div></div>{gtext}
<div class=care>（※ていねいにかくこと。）</div></div>{gsvg}</div>
<div class=rng>{rng}</div>
</div>
<div class=col>
{big(4, f"次の図で，{X_} の値を求めなさい。", "（×4点・単位は cm）")}<div class=sims>{sims}</div>
{big(5, "相似の証明", "（×4点）")}{proof(pt["proof"])}
</div></div></div>"""


if __name__ == "__main__":
    check()
    write_pdfs([
        (doc(CSS, "".join(page(i, p, False) for i, p in enumerate(PATTERNS))), f"{FILE}.pdf"),
        (doc(CSS, "".join(page(i, p, True) for i, p in enumerate(PATTERNS))), f"{FILE}_ans.pdf"),
    ])
