"""中3 定期テスト対策「学習のまとめ(2)」の類題（2ページ＝A3 2枚）＋こたえ（問題に赤で書き込んだ形）

  cd tools && python3 c3_teiki_matome2.py

- 先生が見せてくれた学校の「第3回定期テストに向けて 学習のまとめ(2)」と同じ並び・同じ形で、数字と図を変えた類題。
  1ページ目：［1］解の1つから a と他の解／［2］2乗と2倍をまちがえた／［3］差と積／［4］y＝ax² の式と値
             ［5］変域・変化の割合／［6］相似条件を3つ
  2ページ目：［7］放物線と直線・三角形の面積／［8］相似比・長さ・角／［9］相似の証明／［10］平行線と線分の比
- A3 に拡大して印刷する想定。ファイルは A4・左右2列。
- 1つの HTML から、赤字（.a）を消した問題と、赤字を出したこたえを作る。
- 出力：pdf/c3_teiki_matome2.pdf と c3_teiki_matome2_ans.pdf
"""
import math
import re
from fractions import Fraction as F

import sympy as sp

from c3_souji_nagasa import Fig, tri
from texlib import doc, tex as T, write_pdfs

FILE = "c3_teiki_matome2"
X_, Y_ = T("x"), T("y")


def S(name):
    return T(r"\mathrm{%s}" % name)


def SIM(a, b):
    return T(r"\triangle\mathrm{%s}\backsim\triangle\mathrm{%s}" % (a, b))


def A(s):
    return f"<span class=a>{s}</span>"


def st(*lines):
    return "".join(f"<span class=st>{A(l)}</span>" for l in lines)


def ln(body="", w=45, label=""):
    return f"<div class=ln style='width:{w}mm'>{label}{A(body)}</div>"


# ---------- 図 ----------
class Fig2(Fig):
    """頂点の文字を消せる・好きな所に文字を置ける Fig"""

    def __init__(self, pts, scale, hide=(), pad=7):
        super().__init__(pts, scale)
        self.pad, self.hide, self.texts = pad, set(hide), []

    def text(self, at, dx, dy, t, size=3.4, extra=""):
        self.texts.append((at, dx, dy, t, size, extra))
        return self

    def svg(self, color=None):
        s = super().svg()
        for k in self.hide:
            s = re.sub(r'<text[^>]*>' + re.escape(k) + '</text>', '', s)
        xs = [q[0] for q in self.p.values()]
        ys = [q[1] for q in self.p.values()]
        x0, y1 = min(xs) * self.s - self.pad, max(ys) * self.s + self.pad
        add = ""
        for at, dx, dy, t, size, extra in self.texts:
            q = self.p[at] if isinstance(at, str) else at
            add += (f'<text x="{q[0] * self.s - x0 + dx:.2f}" y="{y1 - q[1] * self.s + dy + 1.1:.2f}" text-anchor="middle" '
                    f'font-size="{size}" font-family="KaTeX_Main" {extra}>{t}</text>')
        return s.replace("</svg>", add + "</svg>")


def on(P, Q, r):
    return (P[0] + (Q[0] - P[0]) * r, P[1] + (Q[1] - P[1]) * r)


def tri_angles(a_deg, c_deg, ab, names, scale, flip=False):
    """∠A, ∠C と AB から三角形（B 左下・C 右下）"""
    a, b, c = names
    B_ = math.radians(180 - a_deg - c_deg)
    A_ = (ab * math.cos(B_), ab * math.sin(B_))
    bc = ab * math.sin(math.radians(a_deg)) / math.sin(math.radians(c_deg))
    pts = {a: A_, b: (0.0, 0.0), c: (bc, 0.0)}
    if flip:
        pts = {k: (-x, y) for k, (x, y) in pts.items()}
    return Fig2(pts, scale).poly(names)


def parabola_fig(k, xa, xb, ans):
    """y＝kx² と A，B（x 座標 xa, xb）、直線 AB、△AOB。単位は mm"""
    s = 4.6
    xmin, xmax, ymin, ymax = -3.6, 5.2, -1.2, 5.8
    W, H = (xmax - xmin) * s, (ymax - ymin) * s
    X = lambda v: (v - xmin) * s
    Y = lambda v: (ymax - v) * s
    ya, yb = k * xa * xa, k * xb * xb
    m = (yb - ya) / (xb - xa)
    n = ya - m * xa
    o = [f'<svg class=fig width="{W:.1f}mm" height="{H:.1f}mm" viewBox="0 0 {W:.1f} {H:.1f}">']
    o.append(f'<polygon points="{X(xa)},{Y(ya)} {X(0)},{Y(0)} {X(xb)},{Y(yb)}" fill="#e6e6e6"/>')
    ar = 'stroke="#111" stroke-width=".35"'
    o.append(f'<line x1="0" y1="{Y(0)}" x2="{W - 1}" y2="{Y(0)}" {ar}/><line x1="{X(0)}" y1="{H}" x2="{X(0)}" y2="1" {ar}/>')
    o.append(f'<polygon points="{W},{Y(0)} {W - 2},{Y(0) - .8} {W - 2},{Y(0) + .8}" fill="#111"/>')
    o.append(f'<polygon points="{X(0)},0 {X(0) - .8},2 {X(0) + .8},2" fill="#111"/>')
    pts = []
    for i in range(301):
        v = xmin + (xmax - xmin) * i / 300
        w = k * v * v
        if w <= ymax:
            pts.append(f"{X(v):.2f},{Y(w):.2f}")
    o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#111" stroke-width=".45"/>')
    lx0, lx1 = -3.4, 5.0
    o.append(f'<line x1="{X(lx0)}" y1="{Y(m * lx0 + n)}" x2="{X(lx1)}" y2="{Y(m * lx1 + n)}" stroke="#111" stroke-width=".4"/>')
    for p, q in ((xa, ya), (xb, yb)):
        o.append(f'<line x1="{X(p)}" y1="{Y(q)}" x2="{X(p)}" y2="{Y(0)}" stroke="#111" stroke-width=".25" stroke-dasharray="1 .8"/>')
        o.append(f'<line x1="{X(0)}" y1="{Y(q)}" x2="{X(p)}" y2="{Y(q)}" stroke="#111" stroke-width=".25" stroke-dasharray="1 .8"/>')
        o.append(f'<line x1="{X(0)}" y1="{Y(0)}" x2="{X(p)}" y2="{Y(q)}" stroke="#111" stroke-width=".4"/>')
        o.append(f'<circle cx="{X(p)}" cy="{Y(q)}" r=".7" fill="#111"/>')

    def t(x, y, s_, anchor="middle", extra=""):
        o.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="3.3" text-anchor="{anchor}" font-family="KaTeX_Main" {extra}>{s_}</text>')

    it = 'font-family="KaTeX_Math" font-style="italic"'
    t(X(xa) - 2, Y(ya) - 1.2, "A")
    t(X(xb) + 2.2, Y(yb) + .5, "B")
    t(X(0) - 1.6, Y(0) + 3.4, "O")
    t(W - 1, Y(0) - 1.4, "x", extra=it)
    t(X(0) + 2, 3, "y", extra=it)
    t(X(xa), Y(0) + 3.6, str(xa).replace("-", "−"))
    t(X(xb), Y(0) + 3.6, str(xb))
    if ans:
        red = 'fill="#c8102e"'
        t(X(0) - 1.2, Y(ya) + 1.1, f"{ya:g}", "end", red)
        t(X(0) - 1.2, Y(yb) + 1.1, f"{yb:g}", "end", red)
        t(X(0) - 1.2, Y(n) - .6, f"{n:g}", "end", red)
    o.append("</svg>")
    return "".join(o)


def fig8():
    f1 = tri_angles(75, 55, 15, "ABC", 2.25)
    f1.side("A", "B", "15", None).side("B", "C", "x", None)
    f1.angle("B", "A", "C").angle("A", "C", "B")
    f1.text("A", 1.2, 7, "75°", 3).text("C", -6, -1.5, "55°", 3)
    f2 = tri_angles(75, 55, 10, "DEF", 2.25)
    f2.side("D", "E", "10", None).side("E", "F", "12", None)
    f2.angle("D", "F", "E")
    f2.text("F", -6, -1.5, "55°", 3)
    return f1.svg() + f2.svg()


def fig9():
    pts = {"A": (2, 5), "D": (6.5, 5), "B": (0, 0), "C": (9.5, 0)}
    ax, ay = pts["A"]
    cx, cy = pts["C"]
    bx, by = pts["B"]
    dx, dy = pts["D"]
    t = ((bx - ax) * (dy - by) - (by - ay) * (dx - bx)) / ((cx - ax) * (dy - by) - (cy - ay) * (dx - bx))
    pts["O"] = (ax + (cx - ax) * t, ay + (cy - ay) * t)
    f = Fig2(pts, 2.9, pad=6).poly("ABCD").line("A", "C").line("B", "D").par("A", "D").par("B", "C")
    f.label(O=(0, 4), A=(-2, -2.6), D=(2, -2.6))
    return f.svg()


def fig10_1():
    t = tri(12, 14, 15)
    A_, B_, C_ = t["A"], t["B"], t["C"]
    f = Fig2({"A": A_, "B": B_, "C": C_, "D": on(A_, B_, 8 / 12), "E": on(A_, C_, 8 / 12)}, 2.4)
    f.poly("ABC").line("D", "E").par("D", "E").par("B", "C").label(D=(-3.4, -.6), E=(3.4, -.6))
    f.side("A", "D", 8, 8).side("D", "B", 4, 4).side("A", "E", 10, 10).side("E", "C", "x", 5, at=(4.2, -.5))
    return f.svg()


def fig10_2():
    # A＝交点、上に B（左）・C（右）、下に E（左）・D（右）。AC＝6，BC＝9，AE＝8，ED＝12
    t = tri(6, 9, 7, "OCB")                     # OC＝6，CB＝9，BO＝7
    ox, oy = t["O"]
    c = (ox - t["C"][0], oy - t["C"][1])
    b = (ox - t["B"][0], oy - t["B"][1])
    k = F(4, 3)
    pts = {"A": (0, 0), "C": c, "B": b, "E": (-c[0] * float(k), -c[1] * float(k)), "D": (-b[0] * float(k), -b[1] * float(k))}
    f = Fig2(pts, 2.6).line("B", "C").line("E", "D").line("B", "D").line("C", "E").par("B", "C").par("E", "D")
    f.label(A=(4.2, .8))
    f.side("B", "C", 9, 9).side("E", "D", 12, 12).side("A", "C", 6, 6, at=(3.2, 2.2)).side("A", "E", "x", 8, at=(-3.6, -2.2))
    return f.svg()


def fig10_3():
    s6, c6 = .6, .8                              # 左の線：長さ6 の間に高さ 3.6
    s4 = .9
    c4 = math.sqrt(1 - s4 * s4)                  # 右の線：長さ4 の間に高さ 3.6
    p = {"l0": (-1.5, 9), "l1": (15.5, 9), "m0": (-1.5, 5.4), "m1": (15.5, 5.4), "n0": (-1.5, 0), "n1": (15.5, 0)}
    p["a0"] = (0.6, 9 + .8 * 1.5)
    p["a1"] = (0.6 + .8 * 1.5, 9)
    p["a2"] = (p["a1"][0] + c6 * 6, 5.4)
    p["a3"] = (p["a2"][0] + c6 * 9, 0)
    p["b1"] = (9, 9)
    p["b2"] = (9 + c4 * 4, 5.4)
    p["b3"] = (p["b2"][0] + c4 * 6, 0)
    p["b0"] = (9 - c4 * 1.2, 9 + s4 * 1.2)
    p["a4"] = (p["a3"][0] + c6 * 1.5, -1.5 * s6)
    p["b4"] = (p["b3"][0] + c4 * 1.2, -1.2 * s4)
    f = Fig2(p, 2.1, hide=p.keys(), pad=4)
    f.line("l0", "l1").line("m0", "m1").line("n0", "n1").line("a0", "a4").line("b0", "b4")
    f.side("a1", "a2", 6, 6, at=(-5.5, 0)).side("a2", "a3", 9, 9, at=(-5.5, 0))
    f.side("b1", "b2", 4, 4, at=(5, 0)).side("b2", "b3", "x", 6, at=(5.5, 0))
    it = 'font-family="KaTeX_Math" font-style="italic"'
    for nm, lab in (("l0", "ℓ"), ("m0", "m"), ("n0", "n")):
        f.text(nm, -2.5, .2, lab, 3.6, it)
    return f.svg()


# ---------- チェック ----------
def check():
    x, a = sp.symbols("x a")
    assert sp.solve(16 - 4 * a + 8, a) == [6] and set(sp.solve(x**2 - 6 * x + 8, x)) == {2, 4}
    assert set(sp.solve(x**2 - 3 * x - 40, x)) == {-5, 8}
    assert set(sp.solve(x * (x - 3) - 54, x)) == {9, -6} and 9 - 6 == 3 and 9 * 6 == 54
    assert F(12, 16) == F(3, 4) and F(3, 4) * 36 == 27
    # ［5］
    assert (min(0, 2, 18), max(2, 18)) == (0, 18) and (2 * 1, 2 * 9) == (2, 18)
    assert F(-2 * 9 - (-2 * 1), 3 - 1) == -8 and F(-2 * 4 - (-2 * 16), 2 - (-4)) == 4
    # ［7］
    k = F(1, 4)
    ya, yb = k * 4, k * 16
    assert (ya, yb) == (1, 4)
    m = (yb - ya) / (4 - (-2))
    n = ya - m * (-2)
    assert (m, n) == (F(1, 2), 2) and F(1, 2) * n * (2 + 4) == 6
    # ［8］
    assert F(15, 10) == F(3, 2) and 12 * F(3, 2) == 18 and 180 - 75 - 55 == 50
    # ［10］
    assert F(10 * 4, 8) == 5 and F(6 * 12, 9) == 8 and F(4 * 9, 6) == 6
    print("確認OK")


# ---------- ページ ----------
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; font-size: 9.6pt; }
.page { width: 210mm; height: 297mm; padding: 9mm 11mm 9mm; page-break-after: always;
        display: flex; flex-direction: column; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.katex { font-size: 1.1em; }
.a, .a .katex { color: #c8102e; }
.hide .a { visibility: hidden; }
.head { display: flex; align-items: baseline; white-space: nowrap; border-bottom: 1pt solid #111; padding-bottom: 1.5mm; flex: none; }
.head b { font-size: 12pt; }
.head .kai { color: #c8102e; font-weight: 700; margin-left: 1mm; }
.head .cl { margin-left: auto; font-size: 9pt; }
.head .u { display: inline-block; border-bottom: .7pt solid #111; width: 38mm; }
.cols { flex: 1; min-height: 0; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); margin-top: 2mm; }
.col { display: flex; flex-direction: column; min-height: 0; }
.col:first-child { padding-right: 4mm; border-right: .7pt solid #111; }
.col:last-child { padding-left: 4mm; }
.q { display: flex; flex-direction: column; min-height: 0; }
.q + .q { margin-top: 2mm; }
.qt { display: flex; line-height: 1.6; }
.box { flex: none; display: inline-flex; width: 5mm; height: 5mm; border: .8pt solid #111; align-items: center;
       justify-content: center; font-weight: 700; font-size: 9.5pt; margin-right: 1.5mm; margin-top: .3mm; }
.sub { display: flex; line-height: 1.6; margin-top: 1.5mm; }
.no { flex: none; width: 6mm; font-size: 8pt; padding-top: .5mm; }
.wk { flex: 1 0 auto; padding-left: 6mm; }
.st { display: block; font-size: 9pt; line-height: 1.5; }
.ln { border-bottom: .9pt solid #111; margin-left: auto; height: 6.5mm; flex: none; text-align: center;
      display: flex; align-items: flex-end; justify-content: center; padding-bottom: .4mm; white-space: nowrap; }
.lns { display: flex; justify-content: flex-end; gap: 4mm; flex: none; }
.lns .ln { margin-left: 0; }
.fig { flex: none; }
.fig text { fill: #111; }
.row { display: flex; justify-content: space-between; align-items: flex-start; }
.tbl { border-collapse: collapse; margin: 1.5mm 0 0 6mm; font-size: 9.5pt; }
.tbl td { padding: .6mm 2.5mm; text-align: center; min-width: 11mm; height: 6.5mm; }
.tbl td:first-child { border-right: .8pt solid #111; min-width: 6mm; }
.tbl tr:first-child td { border-bottom: .8pt solid #111; }
.cond .ln { width: 100% !important; justify-content: flex-start; padding-left: 1mm; height: 8.5mm; }
.cond { display: flex; flex-direction: column; gap: 2mm; margin-top: 2mm; }
.pf { flex: 1; min-height: 0; padding: 0 0 0 6mm; border: .8pt solid #111; margin-top: 1mm; padding: 1.5mm 2mm; }
.pf .st { line-height: 1.75; }
"""


def head(page, ans):
    kai = "<span class=kai>【解答】</span>" if ans else ""
    return (f"<div class=head><b>中3数学 定期テスト対策　学習のまとめ(2) 類題（{page}/2）{kai}</b>"
            f"<span class=cl>（　）組（　）番　名前 <span class=u></span></span></div>")


def q(no, text, body, flex=None):
    stl = f" style='flex:{flex}'" if flex else ""
    return f"<div class=q{stl}><div class=qt><span class=box>{no}</span><div>{text}</div></div>{body}</div>"


def sub(no, text):
    num = f"({no})" if no != "" else ""
    return f"<div class=sub><span class=no>{num}</span><div>{text}</div></div>"


def table(xs, ys, ans):
    yy = [A(T(str(v))) for v in ys]
    return (f"<table class=tbl><tr><td>{X_}</td><td>{T(str(xs[0]))}</td><td>→</td><td>{T(str(xs[1]))}</td></tr>"
            f"<tr><td>{Y_}</td><td>{yy[0]}</td><td>→</td><td>{yy[1]}</td></tr></table>")


def page1(ans):
    q1 = q(1, f"二次方程式 {T('x^2-ax+8=0')} の解の1つが4であるとき，{T('a')} の値を求めなさい。また，もう1つの解を求めなさい。",
           "<div class=wk>" + st(f"{T('x=4')} を代入すると", T("16-4a+8=0"), T("-4a=-24") + "　" + T("a=6"),
                                  T("x^2-6x+8=0"), T("(x-2)(x-4)=0") + "　" + T("x=2,\\ 4")) + "</div>"
           + f"<div class=lns>{ln(T('6'), 26, T('a') + '＝')}{ln(T('x=2'), 38, 'もう1つの解 ')}</div>", "1.15 1 0")
    q2 = q(2, f"ある数 {X_} を，2乗しなければならないところを，まちがえて3倍したため，計算の結果は40だけ小さくなりました。この数 {X_} を求めなさい。",
           "<div class=wk>" + st("（式）" + T("x^2-3x=40"), T("x^2-3x-40=0"), T("(x+5)(x-8)=0"),
                                  T("x=-5,\\ 8") + "　（どちらも問題に合っている）") + "</div>"
           + ln("−5，8", 40, f"ある数 {X_} は "), "1 1 0")
    q3 = q(3, "大小2つの自然数があります。その差は3で，積は54です。この2つの数を求めなさい。",
           "<div class=wk>" + st(f"大きい方を {X_}，小さい方を {T('x-3')} とおくと", "（式）" + T("x(x-3)=54"), T("x^2-3x-54=0"),
                                  T("(x+6)(x-9)=0") + "　" + T("x=-6,\\ 9"), f"{T('x>0')} より {T('x=9')}（これがないとダメ）") + "</div>"
           + ln("9，6", 32), "1.15 1 0")
    q4 = q(4, f"{Y_} は {X_} の2乗に比例し，{T('x=4')} のとき {T('y=12')} です。",
           sub(1, f"{Y_} を {X_} の式で表しなさい。") + "<div class=wk>" + st(T("y=ax^2") + " に代入　" + T("12=16a") + "　" + T("a=\\dfrac{3}{4}")) + "</div>"
           + ln(T("y=\\dfrac{3}{4}x^2"), 36)
           + sub(2, f"{T('x=-6')} のときの {Y_} の値を求めなさい。") + "<div class=wk>" + st(T("y=\\dfrac{3}{4}\\times(-6)^2=\\dfrac{3}{4}\\times36")) + "</div>"
           + ln(T("y=27"), 36), "1.25 1 0")
    q5 = q(5, "次の各問いに答えなさい。",
           sub(1, f"関数 {T('y=2x^2')} について，{X_} の変域が次のとき，{Y_} の変域を求めなさい。")
           + sub("", f"① {T('-1\\leqq x\\leqq 3')}") + "<div class=wk>" + st(f"{T('x=0')} をふくむので，最小は {T('y=0')}", f"0 から遠い {T('x=3')} のとき 最大 {T('y=18')}") + "</div>"
           + ln(T("0\\leqq y\\leqq 18"), 42)
           + sub("", f"② {T('-3\\leqq x\\leqq -1')}") + "<div class=wk>" + st(f"{T('x=-1')} のとき {T('y=2')}，{T('x=-3')} のとき {T('y=18')}") + "</div>"
           + ln(T("2\\leqq y\\leqq 18"), 42)
           + sub(2, f"{T('y=-2x^2')} について，{X_} の値が次のように増加するときの変化の割合を求めなさい。")
           + sub("", "① 1から3まで") + table((1, 3), (-2, -18), ans) + "<div class=wk>" + st(T("\\dfrac{-18-(-2)}{3-1}=\\dfrac{-16}{2}")) + "</div>"
           + ln(T("-8"), 30)
           + sub("", "② −4から2まで") + table((-4, 2), (-32, -8), ans) + "<div class=wk>" + st(T("\\dfrac{-8-(-32)}{2-(-4)}=\\dfrac{24}{6}")) + "</div>"
           + ln(T("4"), 30), "3 1 0")
    q6 = q(6, "三角形の相似条件を3つ書きなさい。",
           "<div class=cond>" + "".join(ln(t, 80, "○ ") for t in
                                        ("3組の辺の比が，すべて等しい。", "2組の辺の比とその間の角が，それぞれ等しい。", "2組の角が，それぞれ等しい。")) + "</div>",
           "0 0 auto")
    return (f"<div class='page{'' if ans else ' hide'}'>{head(1, ans)}<div class=cols>"
            f"<div class=col>{q1}{q2}{q3}{q4}</div><div class=col>{q5}{q6}</div></div></div>")


def page2(ans):
    q7 = q(7, f"右の図のように，関数 {T('y=\\dfrac{1}{4}x^2')} のグラフ上に，2点 {S('A')}，{S('B')} があります。"
              f"{S('A')}，{S('B')} の {X_} 座標が，それぞれ {T('-2')}，4 であるとき，",
           f"<div class=row><div style='flex:1'>{sub(1, f'2点 {S(chr(65))}，{S(chr(66))} の座標を求めなさい。')}"
           + "<div class=wk>" + st(T("y=\\dfrac{1}{4}\\times(-2)^2=1"), T("y=\\dfrac{1}{4}\\times4^2=4")) + "</div>"
           + f"</div>{parabola_fig(F(1, 4), -2, 4, ans)}</div>"
           + f"<div class=lns>{ln(T('\\mathrm{A}(-2,\\ 1)'), 30)}{ln(T('\\mathrm{B}(4,\\ 4)'), 30)}</div>"
           + sub(2, f"2点 {S('A')}，{S('B')} を通る直線の式を求めなさい。")
           + "<div class=wk>" + st(T("y=ax+b") + "　" + T("a=\\dfrac{4-1}{4-(-2)}=\\dfrac{3}{6}=\\dfrac{1}{2}"),
                                    T("y=\\dfrac{1}{2}x+b") + " に B(4, 4) を代入", T("4=2+b") + "　" + T("b=2")) + "</div>"
           + ln(T("y=\\dfrac{1}{2}x+2"), 40)
           + sub(3, f"{T('\\triangle\\mathrm{AOB}')} の面積を求めなさい。")
           + "<div class=wk>" + st("直線と " + Y_ + " 軸の交点 (0, 2) で左右に分ける",
                                    "左側…" + T("2\\times2\\times\\dfrac{1}{2}=2") + "　右側…" + T("2\\times4\\times\\dfrac{1}{2}=4"),
                                    T("2+4=6")) + "</div>"
           + ln(T("6"), 30), "1.35 1 0")
    q8 = q(8, f"下の図で，{SIM('ABC', 'DEF')} のとき，次の各問いに答えなさい。（単位は cm）",
           f"<div class=row style='justify-content:space-around;align-items:flex-end;margin-top:1mm'>{fig8()}</div>"
           + sub(1, f"{T('\\triangle\\mathrm{ABC}')} と {T('\\triangle\\mathrm{DEF}')} の相似比をいいなさい。")
           + "<div class=wk>" + st(T("\\mathrm{AB}:\\mathrm{DE}=15:10=3:2")) + "</div>" + ln("3：2", 32)
           + sub(2, f"{S('BC')} の長さを求めなさい。")
           + "<div class=wk>" + st(f"{T('\\mathrm{BC}=x')} cm とすると", T("x:12=3:2"), T("2x=36") + "　" + T("x=18")) + "</div>"
           + ln(T("\\mathrm{BC}=18") + "（cm）", 40)
           + sub(3, f"{T('\\angle\\mathrm{C}')}，{T('\\angle\\mathrm{E}')} の大きさをそれぞれ求めなさい。")
           + "<div class=wk>" + st(T("\\angle\\mathrm{C}=\\angle\\mathrm{F}") + "，" + T("\\angle\\mathrm{E}=\\angle\\mathrm{B}=180^\\circ-75^\\circ-55^\\circ")) + "</div>"
           + f"<div class=lns>{ln(T('\\angle\\mathrm{C}=55^\\circ'), 30)}{ln(T('\\angle\\mathrm{E}=50^\\circ'), 30)}</div>", "1.25 1 0")
    proof = st(f"{T('\\triangle\\mathrm{AOD}')} と {T('\\triangle\\mathrm{COB}')} において",
               f"{T('\\mathrm{AD}')} ∥ {T('\\mathrm{BC}')} より",
               "　" + T("\\angle\\mathrm{OAD}=\\angle\\mathrm{OCB}") + "（錯角）……①",
               "　" + T("\\angle\\mathrm{ODA}=\\angle\\mathrm{OBC}") + "（錯角）……②",
               "①，②より",
               "　2組の角がそれぞれ等しいので",
               "　　" + SIM("AOD", "COB"),
               "（②のかわりに " + T("\\angle\\mathrm{AOD}=\\angle\\mathrm{COB}") + "（対頂角）を使ってもよい）")
    q9 = (f"<div class=q style='flex:1 1 0'><div class=row><div class=qt><span class=box>9</span><div>右の図で，{S('AD')} ∥ {S('BC')}，"
          f"{S('O')} は {S('AC')} と {S('BD')} の交点です。{SIM('AOD', 'COB')} であることを証明しなさい。</div></div>{fig9()}</div>"
          f"<div class=pf>{proof}</div></div>")
    q10 = q(10, f"下の図で，{S('DE')} ∥ {S('BC')} のとき，{X_} の値を求めなさい。（(3)は ℓ ∥ m ∥ n，単位は cm）",
            sub(1, "") + f"<div class=row><div class=wk>{st(T('\\mathrm{AD}:\\mathrm{DB}=\\mathrm{AE}:\\mathrm{EC}'), T('8:4=10:x'), T('8x=40'))}</div>{fig10_1()}</div>"
            + ln(T("x=5"), 30)
            + sub(2, f"（{S('BC')} ∥ {S('ED')}）") + f"<div class=row><div class=wk>{st(SIM('ABC', 'ADE'), T('\\mathrm{BC}:\\mathrm{DE}=9:12=3:4'), T('6:x=3:4'), T('3x=24'))}</div>{fig10_2()}</div>"
            + ln(T("x=8"), 30)
            + sub(3, "") + f"<div class=row><div class=wk>{st(T('6:9=4:x'), T('6x=36'))}</div>{fig10_3()}</div>"
            + ln(T("x=6"), 30), "0 0 auto")
    return (f"<div class='page{'' if ans else ' hide'}'>{head(2, ans)}<div class=cols>"
            f"<div class=col>{q7}{q8}</div><div class=col>{q9}{q10}</div></div></div>")


if __name__ == "__main__":
    check()
    write_pdfs([
        (doc(CSS, page1(False) + page2(False)), f"{FILE}.pdf"),
        (doc(CSS, page1(True) + page2(True)), f"{FILE}_ans.pdf"),
    ])
