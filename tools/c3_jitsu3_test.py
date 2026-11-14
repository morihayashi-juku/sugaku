"""中3 実力テスト③（高校入試形式・大問1〜5）を、大問1／単元別の PDF にする。
問題（pdf/c3_jitsu3_*.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
部品・CSS は c3_jitsu_test.py（①）・c3_jitsu2_test.py（②）と共通。

  大問1 小問集合（箱ひげ図・作図つき）  c3_jitsu3_d1
  大問2-1 確率（約数）                  c3_jitsu3_kakuritsu
  大問2-2 方程式の利用（割合）          c3_jitsu3_houtei
  大問3 一次関数（動点と面積）          c3_jitsu3_ichiji
  大問4 図形（合同・面積）              c3_jitsu3_zukei
  大問5 空間図形（円錐）                c3_jitsu3_kuukan

実行：cd tools && python3 c3_jitsu3_test.py
"""
from fractions import Fraction as F
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build, _pt, _arc  # noqa: E402

# ================= 答えの確認 =================
assert 3 - (-7) == 10 and F(-10, 3) / F(-5, 9) == 6
assert -18 / -3 == 6 and F(-3 * -6, 2) == 9                       # y=18/x
assert (lambda x: (x, 10 - x))(3) == (3, 7) and 3 - 7 == -4
assert 360 / 12 == 30
BOX1 = (144, 152, 157, 163, 177)        # 1組（図から読んだ値）
BOX2 = (147, 154, 162, 169, 174)        # 2組
assert BOX2[0] >= 145 and BOX1[1] <= 155 and BOX2[1] <= 155 and BOX1[2] < 160 and BOX2[4] <= 175   # 答えはイ
BA, BB = [2, 6, 15, 24], [3, 4, 12, 30]
AB_ = [(a, b) for a in BA for b in BB if b % a == 0]
BA_ = [(a, b) for a in BA for b in BB if a % b == 0]
assert len(BA) * len(BB) == 16 and len(AB_) == 6 and len(BA_) == 5
X = F(240 + 30 + 60, 1 - F(25, 100) - F(20, 100))
assert X == 600
assert 4 * 3 == 12 and 16 - 4 * 0 == 16 and 64 - 4 * 14 == 8
assert F(1, 2) * 6 * 3 == 9 and F(18) * F(2, 3) == 12
assert F(1, 3) * 36 * 8 == 96 and 360 * 6 // 12 == 180 and 12 * 6 + 36 == 108

TAG = "中3　実力テスト③"


def header(title, page=None):
    p = f"（{page}）" if page else ""
    return (f'<div class="hd"><div class="ht"><span class="tag">{TAG}</span>{title}{p}<span class="key">解答</span></div>'
            '<div class="nm">　月　　日　名前（　　　　　　　　　）</div></div>')


def T(x, y, s, cls="pl", anc="middle"):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anc}">{s}</text>'


def L(p, q, w=1.2, dash=False, col="#000"):
    d = ' stroke-dasharray="3,2"' if dash else ""
    return f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{col}" stroke-width="{w}"{d}/>'


def right_mark(p, u1, u2, k=8):
    q = [(p[0] + k * u1[0], p[1] + k * u1[1]), (p[0] + k * (u1[0] + u2[0]), p[1] + k * (u1[1] + u2[1])), (p[0] + k * u2[0], p[1] + k * u2[1])]
    return '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in q) + '" fill="none" stroke="#000" stroke-width="1"/>'


# ================= 図 =================
def boxes_svg():
    Lx, Wd = 34, 240
    xs = lambda v: Lx + (v - 140) / 40 * Wd
    s = f'<rect x="{Lx}" y="4" width="{Wd}" height="104" fill="none" stroke="#000" stroke-width="1"/>'
    for v in range(145, 180, 5):
        s += L((xs(v), 4), (xs(v), 108), 0.5, True, "#777")
    for row, (y0, bx) in enumerate([(32, BOX1), (80, BOX2)]):
        mn, q1, md, q3, mx = bx
        s += T(Lx - 6, y0 + 4, f"{row + 1}組", "sm", "end")
        s += L((xs(mn), y0), (xs(q1), y0)) + L((xs(q3), y0), (xs(mx), y0))
        s += L((xs(mn), y0 - 8), (xs(mn), y0 + 8)) + L((xs(mx), y0 - 8), (xs(mx), y0 + 8))
        s += f'<rect x="{xs(q1):.1f}" y="{y0 - 13}" width="{xs(q3) - xs(q1):.1f}" height="26" fill="#fff" stroke="#000" stroke-width="1.2"/>'
        s += L((xs(md), y0 - 13), (xs(md), y0 + 13))
    for v in range(140, 181, 10):
        s += T(xs(v), 122, str(v), "sm")
    s += T(xs(180) + 8, 122, "(cm)", "sm", "start")
    return f'<svg width="{Lx + Wd + 36}" height="128" viewBox="0 0 {Lx + Wd + 36} 128">{s}</svg>'


def tri_svg():
    """∠A=90° の直角三角形（A 左下・B 右下・C 上）。作図（∠CAP=30°）は .cons＝こたえだけ"""
    k = 34
    A_ = (30, 4 * k + 26)
    B_ = (A_[0] + 6 * k, A_[1])
    C_ = (A_[0], A_[1] - 4 * k)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="#000" stroke-width="1.3"/>'
    s += right_mark(A_, (1, 0), (0, -1))
    s += T(A_[0] - 10, A_[1] + 6, "A") + T(B_[0] + 9, B_[1] + 6, "B") + T(C_[0] - 2, C_[1] - 6, "C")
    # 作図：A を中心に円 → AB との交点 M → M を中心に同じ半径 → 交点 Q（∠MAQ=60°）→ 直線 AQ と BC の交点 P
    r = 60
    M = _pt(A_, r, 0)
    Qp = _pt(A_, r, 60)
    t = 1 / (math.cos(math.radians(60)) / (6 * k) + math.sin(math.radians(60)) / (4 * k))
    P = _pt(A_, t, 60)
    # P は BC 上、∠CAP=30°
    assert abs((P[0] - A_[0]) / (6 * k) + (A_[1] - P[1]) / (4 * k) - 1) < 1e-9
    c = _arc(A_, r, 80, -6) + _arc(M, r, 135, 100)
    c += L(A_, P, 1.4)
    c += "".join(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="2.2" fill="#c00"/>' for p in (M, Qp, P))
    c += T(P[0] + 9, P[1] - 3, "P") + T(M[0] + 3, M[1] + 12, "M", "sm") + T(Qp[0] - 9, Qp[1] - 2, "Q", "sm")
    p30 = _pt(A_, 34, 76)
    c += T(p30[0], p30[1], "30°", "sm", "start")
    return f'<svg width="{B_[0] + 30}" height="{A_[1] + 16}" viewBox="0 0 {B_[0] + 30} {A_[1] + 16}">{s}<g class="cons">{c}</g></svg>'


def balls_svg():
    def box(x0, nums, lab):
        s = (f'<path d="M{x0 + 30} 8 H{x0} V100 H{x0 + 110} V8 H{x0 + 80}" fill="none" stroke="#000" stroke-width="1.2"/>'
             + T(x0 + 55, 118, lab))
        pos = [(x0 + 28, 30), (x0 + 78, 36), (x0 + 26, 72), (x0 + 78, 76)]
        for (cx, cy), n in zip(pos, nums):
            s += f'<circle cx="{cx}" cy="{cy}" r="14" fill="#fff" stroke="#000" stroke-width="1"/>' + T(cx, cy + 5, n, "b2")
        return s
    return f'<svg width="260" height="124" viewBox="0 0 260 124">{box(5, ["2", "24", "15", "6"], "A")}{box(140, ["12", "4", "3", "30"], "B")}</svg>'


def pie_svg():
    cx, cy, r = 160, 128, 84
    parts = [("A", 144, "240人"), ("B", 90, ""), ("C", 72, ""), ("D", 18, ""), ("その他", 36, "60人")]
    s = '<rect x="2" y="2" width="296" height="226" fill="none" stroke="#000" stroke-width="1"/>' + T(160, 18, "ある中学校の通学区域調べ", "sm")
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#000" stroke-width="1.2"/>'
    ang = 0
    for name, deg, n in parts:
        a = math.radians(90 - ang)
        s += L((cx, cy), (cx + r * math.cos(a), cy - r * math.sin(a)), 1)
        mid = math.radians(90 - (ang + deg / 2))
        if name == "D":
            px, py = cx + r * math.cos(mid), cy - r * math.sin(mid)
            s += f'<path d="M{px:.1f} {py:.1f} Q{px - 6:.1f} {py - 30:.1f} {px - 30:.1f} {py - 32:.1f}" fill="none" stroke="#000" stroke-width="0.8"/>'
            s += T(px - 48, py - 44, "D", "b2") + T(px - 48, py - 28, "30人", "sm")
        else:
            rr = r * (0.62 if name != "その他" else 0.7)
            x, y = cx + rr * math.cos(mid), cy - rr * math.sin(mid)
            s += T(x, y - (4 if n else -4), name, "b2") + (T(x, y + 12, n, "sm") if n else "")
        ang += deg
    return f'<svg width="300" height="230" viewBox="0 0 300 230">{s}</svg>'


def rect_p_svg():
    k = 30
    A_, B_, C_, D_ = (40, 22), (40, 22 + 4 * k), (40 + 8 * k, 22 + 4 * k), (40 + 8 * k, 22)
    P = (40, 22 + 1.6 * k)
    s = (f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]} {D_[0]},{D_[1]}" fill="none" stroke="#000" stroke-width="1.2"/>'
         + L(P, D_) + f'<circle cx="{P[0]}" cy="{P[1]}" r="2.2" fill="#000"/>')
    s += T(A_[0] - 2, A_[1] - 6, "A") + T(D_[0] + 6, D_[1] - 4, "D") + T(B_[0] - 6, B_[1] + 14, "B") + T(C_[0] + 6, C_[1] + 14, "C") + T(P[0] - 10, P[1] + 3, "P")
    s += T(A_[0] + 100, A_[1] + 22, '<tspan class="ax">y</tspan> cm²', "sm")
    s += T(A_[0] - 24, B_[1] - 34, "4cm", "sm") + T(A_[0] + 4 * k, B_[1] + 16, "8cm", "sm")
    s += '<path d="M30 92 l0 20 m-3 -6 l3 6 l3 -6" fill="none" stroke="#000" stroke-width="0.9"/>'
    s += f'<path d="M{A_[0] + 50} {B_[1] - 8} l22 0 m-6 -3 l6 3 l-6 3" fill="none" stroke="#000" stroke-width="0.9"/>'
    s += f'<path d="M{D_[0] + 10} {D_[1] + 80} l0 -22 m-3 6 l3 -6 l3 6" fill="none" stroke="#000" stroke-width="0.9"/>'
    return f'<svg width="{D_[0] + 30}" height="{B_[1] + 24}" viewBox="0 0 {D_[0] + 30} {B_[1] + 24}">{s}</svg>'


def square_svg():
    k = 34
    o = (20, 18)
    P = lambda x, y: (o[0] + x * k, o[1] + y * k)      # A(0,0) 左上・D(6,0)・B(0,6)・C(6,6)、E(4,2)、F(6,3)
    A_, D_, B_, C_, E_, F_ = P(0, 0), P(6, 0), P(0, 6), P(6, 6), P(4, 2), P(6, 3)
    s = (f'<polygon points="{A_[0]},{A_[1]} {D_[0]},{D_[1]} {C_[0]},{C_[1]} {B_[0]},{B_[1]}" fill="none" stroke="#000" stroke-width="1.2"/>'
         + L(B_, D_) + L(A_, F_) + L(E_, C_))
    s += T(A_[0] - 8, A_[1] - 3, "A") + T(D_[0] + 8, D_[1] - 3, "D") + T(B_[0] - 8, B_[1] + 12, "B") + T(C_[0] + 8, C_[1] + 12, "C")
    s += T(E_[0] - 4, E_[1] - 7, "E") + T(F_[0] + 9, F_[1] + 4, "F")
    return f'<svg width="{6 * k + 46}" height="{6 * k + 36}" viewBox="0 0 {6 * k + 46} {6 * k + 36}">{s}</svg>'


def cone_tri_svg():
    k = 18
    C_ = (30 + 6 * k, 20 + 8 * k)
    B_ = (30, C_[1])
    A_ = (C_[0], 20)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += right_mark(C_, (-1, 0), (0, -1))
    s += T(A_[0], A_[1] - 6, "A") + T(B_[0] - 9, B_[1] + 4, "B") + T(C_[0] + 9, C_[1] + 4, "C")
    s += T((A_[0] + B_[0]) / 2 - 18, (A_[1] + B_[1]) / 2, '<tspan class="ax">a</tspan>cm', "sm")
    s += T(A_[0] + 8, (A_[1] + C_[1]) / 2, '<tspan class="ax">b</tspan>cm', "sm", "start") + T((B_[0] + C_[0]) / 2, C_[1] + 15, "6cm", "sm")
    return f'<svg width="{C_[0] + 50}" height="{C_[1] + 22}" viewBox="0 0 {C_[0] + 50} {C_[1] + 22}">{s}</svg>'


def sectors_svg():
    def sector(cx, cy, r, deg, up=True):
        """中心角 deg のおうぎ形（up＝中心が上、弧が下）"""
        a1, a2 = -90 - deg / 2, -90 + deg / 2
        if not up:
            a1, a2 = 90 - deg / 2 + 180, 90 + deg / 2 + 180
        p1, p2 = _pt((cx, cy), r, a1), _pt((cx, cy), r, a2)
        large = 1 if deg > 180 else 0
        return (f'<path d="M{cx} {cy} L{p1[0]:.1f} {p1[1]:.1f} A{r} {r} 0 {large} 0 {p2[0]:.1f} {p2[1]:.1f} Z" fill="#fff" stroke="#000" stroke-width="1.1"/>')
    s = sector(45, 20, 52, 90) + T(12, 14, "ア", "b2")
    s += sector(150, 20, 52, 120) + T(105, 14, "イ", "b2")
    s += f'<path d="M210 26 h96 a48 48 0 0 1 -96 0 z" fill="#fff" stroke="#000" stroke-width="1.1"/>' + T(212, 14, "ウ", "b2")
    cx, cy, r = 372, 58, 42
    p1, p2 = _pt((cx, cy), r, 135), _pt((cx, cy), r, 45)
    s += f'<path d="M{cx} {cy} L{p1[0]:.1f} {p1[1]:.1f} A{r} {r} 0 1 0 {p2[0]:.1f} {p2[1]:.1f} Z" fill="#fff" stroke="#000" stroke-width="1.1"/>' + T(326, 14, "エ", "b2")
    return f'<svg width="430" height="110" viewBox="0 0 430 110">{s}</svg>'


# ================= 大問1 =================
def d1():
    c1 = Q("(1)", r"$3-(-7)$ を計算しなさい。", W(r"$3+7=10$"), A("10"), 3)
    c2 = Q("(2)", r"$-\dfrac{10}{3}\div\left(-\dfrac{5}{9}\right)$ を計算しなさい。", W(r"$+\dfrac{10}{3}\times\dfrac{9}{5}=6$"), A("6"), 3)
    c3 = Q("(3)", r"$(4x-2y)-(6x-4y)$ を計算しなさい。", W(r"$4x-2y-6x+4y$"), A(r"$-2x+2y$"), 3)
    c4 = Q("(4)", r"$y$ は $x$ に反比例し、$x=-3$ のとき $y=-6$ である。$x=2$ のとき、$y$ の値を求めなさい。",
           W(r"$y=\dfrac{a}{x}$ に代入して $a=(-3)\times(-6)=18$　$y=\dfrac{18}{2}$"), A(r"$y=9$"), 3)
    c5 = Q("(5)", r"連立方程式 $\begin{cases}y=10-x\\x-y=-4\end{cases}$ を解きなさい。",
           W(r"下の式に代入して　$x-(10-x)=-4$　$2x=6$　$x=3$<br>$y=10-3=7$"), A(r"$x=3,\ y=7$"), 3)
    c6 = Q("(6)", "正十二角形の1つの外角の大きさを求めなさい。", W(r"外角の和は $360^\circ$ だから　$360^\circ\div12$"), A(r"$30^\circ$"), 3)
    c7 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(7)</span>右の図は、ある中学校の3年1組と3年2組、それぞれ40人の身長のデータを箱ひげ図に表したものである。'
          'この箱ひげ図からわかることについて述べた文として適切なものを、次のア〜エから1つ選び、記号で答えなさい。</div>'
          '<div class="ch">ア　145cmより低い生徒は、どちらのクラスにもいる。<br>イ　155cm以下の生徒は、どちらのクラスにも10人以上いる。<br>'
          'ウ　160cm以上の生徒は、どちらのクラスにも20人以上いる。<br>エ　175cmより高い生徒は、どちらのクラスにもいる。</div>'
          + W("ア：2組の最小値は145cmより大きい。エ：2組の最大値は175cmより小さい。<br>"
              "ウ：1組の中央値が160cmより小さい。イ：第1四分位数（10・11番目の平均）がどちらも155cm以下なので、低いほうから10人は155cm以下。")
          + f'</div><div class="fig">{boxes_svg()}</div></div><div class="al">答　{A("イ", "w20")}</div></div>')
    c8 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(8)</span>右の図の $\\angle\\mathrm{A}=90^\\circ$ の直角三角形ABCで、辺BC上にあり、'
          '$\\angle\\mathrm{CAP}=30^\\circ$ となる点Pを、コンパスと定規を使って作図しなさい。作図に用いた線は消さずに残しておくこと。</div>'
          + W(r"$\angle\mathrm{CAP}=30^\circ$ ⇔ $\angle\mathrm{BAP}=90^\circ-30^\circ=60^\circ$。正三角形の角 $60^\circ$ を使う。<br>"
              "①Aを中心とする円をかき、辺ABとの交点をMとする。<br>②Mを中心に同じ半径の円をかき、①の円との交点をQとする（△AMQは正三角形）。<br>③直線AQと辺BCとの交点がP。")
          + f'</div><div class="fig">{tri_svg()}</div></div></div>')
    return f"""<section class="page">{header("大問1　小問集合")}
<div class="lead">次の(1)〜(8)の問いに答えなさい。</div>
<div class="grid2">{c1}{c2}{c3}{c4}{c5}{c6}</div>
{c7}
{c8}
</section>"""


# ================= 大問2-1 確率 =================
def d2a():
    def tbl(pairs, head):
        cells = "".join(f"<td>{a}</td>" for a in BA)
        rows = "".join("<tr><th>" + str(b) + "</th>" + "".join(f'<td>{"○" if (a, b) in pairs else ""}</td>' for a in BA) + "</tr>" for b in BB)
        return f'<table class="mini" style="display:inline-table;margin-right:6mm"><tr><th>{head}</th>{cells}</tr>{rows}</table>'
    q1 = Q("(1)", "玉の取り出し方は全部で何通りあるか、求めなさい。", W(r"Aの箱が4通り、それぞれにBの箱が4通りあるので　$4\times4=16$（通り）"), A("16通り", "w20"), 16)
    q2 = Q("(2)", r"$a$ が $b$ の約数になる場合と、$b$ が $a$ の約数になる場合とでは、どちらのことがらの方が起こりやすいか、確率をそれぞれ示して説明しなさい。",
           W("表の上が $a$（Aの箱）、左が $b$（Bの箱）。" + "<br>" + tbl(AB_, "<i>a</i>が<i>b</i>の約数") + tbl(BA_, "<i>b</i>が<i>a</i>の約数"))
           + lines(r"$a$ が $b$ の約数になるのは、$(a,b)=(2,4),(2,12),(2,30),(6,12),(6,30),(15,30)$ の6通りで、確率は $\dfrac{6}{16}=\dfrac{3}{8}$。<br>"
                   r"$b$ が $a$ の約数になるのは、$(a,b)=(6,3),(15,3),(24,3),(24,4),(24,12)$ の5通りで、確率は $\dfrac{5}{16}$。<br>"
                   r"$\dfrac{3}{8}=\dfrac{6}{16}>\dfrac{5}{16}$ なので、<b>$a$ が $b$ の約数になる場合</b>の方が起こりやすい。", 34), "", 26)
    return f"""<section class="page">{header("大問2-1　確率")}
<div class="flex"><div class="grow"><div class="lead">右の図のように、Aの箱には2、6、15、24の数を1つずつ書いた4個の玉が入っており、Bの箱には3、4、12、30の数を1つずつ書いた4個の玉が入っている。
Aの箱から玉を1個取り出して、その数を $a$ とし、Bの箱から玉を1個取り出して、その数を $b$ とする。ただし、どの玉を取り出すことも同様に確からしいとする。<br>このとき、次の(1)、(2)の問いに答えなさい。</div></div>
<div class="fig">{balls_svg()}</div></div>
{q1}{q2}
</section>"""


# ================= 大問2-2 方程式の利用 =================
def d2b():
    q1 = Q("(1)", r"この中学校の全校生徒の人数を $x$ 人とするとき、B地区の生徒の人数を $x$ を使って表しなさい。",
           W(r"25％ $=\dfrac{25}{100}=\dfrac14$ だから　$x\times\dfrac14$"), A(r"$\dfrac{1}{4}x$ 人", "w30"), 20)
    q2 = Q("(2)", r"この中学校の全校生徒の人数を方程式を使って求めなさい。ただし、この中学校の全校生徒の人数を $x$ 人とし、答えを求める過程がわかるように、式と計算も書きなさい。",
           W(r"C地区は $\dfrac{20}{100}x=\dfrac15x$ 人。全部の地区をたすと全校生徒になるので<br>"
             r"$240+\dfrac14x+\dfrac15x+30+60=x$<br>両辺に20をかけて　$4800+5x+4x+600+1200=20x$<br>"
             r"$6600=11x$　$x=600$<br>（B地区 150人、C地区 120人。240＋150＋120＋30＋60＝600 で問題に合う）"), A("600人", "w20"), 70)
    return f"""<section class="page">{header("大問2-2　方程式の利用（割合）")}
<div class="lead">ある中学校の全校生徒について、通学区域を調べ、次のグラフのようにまとめた。このうち、全校生徒に対するB地区、C地区の生徒の割合は、それぞれ25％、20％であった。<br>このとき、次の(1)、(2)の問いに答えなさい。</div>
<div style="text-align:center">{pie_svg()}</div>
{q1}{q2}
</section>"""


# ================= 大問3 一次関数（動点） =================
def d3():
    def fix(no, text, work, ans):
        return Q(no, text, W(work), "答　" + A(ans, "w20") if False else A(ans, "w20"), 14)
    p1 = fix("(1)", r"$x=3$ のとき、$y=\underline{24}$ である。", r"辺AB上（$0\leqq x\leqq4$）では AP＝$x$ cm、底辺AD＝8cm だから $y=\dfrac12\times8\times x=4x$<br>$x=3$ のとき $y=4\times3=12$", "12")
    p2 = fix("(2)", r"点Pが辺AB上を動くとき、$x$ の変域は、$0\leqq x\leqq\underline{8}$ である。", r"AB＝4cm なので、Bに着くのは $x=4$ のとき", "4")
    p3 = fix("(3)", r"点Pが辺BC上を動くとき、常に $y=\underline{16}$ である。", r"高さはいつもAB＝4cm だから　$y=\dfrac12\times8\times4=16$（正しい）", "○")
    s1 = Q("(1)", r"点Pが辺CD上を動くとき、$y$ を $x$ の式で表しなさい。",
           W(r"Cに着くのは $x=4+8=12$、Dに着くのは $x=16$。辺CD上（$12\leqq x\leqq16$）では PD＝$16-x$ cm<br>"
             r"$y=\dfrac12\times8\times(16-x)=64-4x$"), A(r"$y=-4x+64$", "w30"), 24)
    s2 = Q("(2)", "点Pが辺CD上を動くとき、△APDの面積が8cm²となるのは、点PがAから何cm動いたときか、答えなさい。",
           W(r"$-4x+64=8$　$-4x=-56$　$x=14$（$12\leqq x\leqq16$ に入っている）"), A("14 cm", "w20"), 24)
    return f"""<section class="page">{header("大問3　一次関数（動点と面積）")}
<div class="flex"><div class="grow"><div class="lead">右の図のような、AB＝4cm、BC＝8cmの長方形で、点PはAを出発して、この長方形の辺上をB、Cを通ってDまで動く。
点PがAから $x$ cm動いたときの△APDの面積を $y$ cm²とするとき、次の1、2の問いに答えなさい。</div></div>
<div class="fig">{rect_p_svg()}</div></div>
<div class="q"><div class="qt"><span class="no">1</span>次の(1)〜(3)は、点Pが辺AB、BC上を動くときの $x,\\ y$ の変化のようすについて述べたものである。それぞれの文中の下線部が正しければ○を書き、誤っていれば、下線部の誤りをなおして正しくしなさい。</div></div>
{p1}{p2}{p3}
<div class="q"><div class="qt"><span class="no">2</span>点Pが辺CD上を動くときについて、次の(1)、(2)の問いに答えなさい。</div></div>
{s1}{s2}
</section>"""


# ================= 大問4 図形 =================
def d4():
    q1 = Q("1", "△ABE≡△CBEであることを証明しなさい。",
           lines(r"△ABEと△CBEで、<br>正方形の辺だから　AB＝CB　……①<br>共通な辺だから　BE＝BE　……②<br>"
                 r"正方形の対角線BDは $\angle\mathrm{ABC}$ を2等分するから　$\angle\mathrm{ABE}=\angle\mathrm{CBE}=45^\circ$　……③<br>"
                 r"①、②、③より、2組の辺とその間の角がそれぞれ等しいから、△ABE≡△CBE", 50), "", 0)
    q2 = Q("2", r"$\angle\mathrm{BCE}=a^\circ$ のとき、$\angle\mathrm{AED}$ の大きさを、$a$ を使った最も簡単な式で表しなさい。",
           W(r"△ABE≡△CBE より $\angle\mathrm{BAE}=\angle\mathrm{BCE}=a^\circ$<br>"
             r"$\angle\mathrm{AED}$ は△ABEの頂点Eの外角だから　$\angle\mathrm{AED}=\angle\mathrm{BAE}+\angle\mathrm{ABE}=a^\circ+45^\circ$"),
           A(r"$(a+45)^\circ$", "w30"), 22)
    q3 = '<div class="q"><div class="qt"><span class="no">3</span>△ADF＝9cm²のとき、次の(1)、(2)の問いに答えなさい。</div></div>'
    t1 = Q("(1)", "線分DFの長さを求めなさい。", W(r"$\angle\mathrm{ADF}=90^\circ$、AD＝6cm だから　$\dfrac12\times6\times\mathrm{DF}=9$　DF＝3"), A("3 cm", "w20"), 18)
    t2 = Q("(2)", "△ABEの面積を求めなさい。",
           W(r"AB∥DF より △ABE∽△FDE で、相似比は AB：FD＝6：3＝2：1。よって BE：ED＝2：1<br>"
             r"△ABD＝$\dfrac12\times6\times6=18$ で、△ABEと△ABDは高さが同じだから　△ABE＝$18\times\dfrac23=12$"), A("12 cm²", "w20"), 28)
    return f"""<section class="page">{header("大問4　図形（合同・面積）")}
<div class="flex"><div class="grow"><div class="lead">下の図で、四角形ABCDは1辺の長さが6cmの正方形である。対角線BD上に点Eをとり、線分AEの延長が辺CDと交わる点をFとする。また、点Eと点Cを結ぶ。<br>このとき、次の1〜3の問いに答えなさい。</div></div>
<div class="fig">{square_svg()}</div></div>
{q1}{q2}{q3}{t1}{t2}
</section>"""


# ================= 大問5 空間図形 =================
def d5():
    q1a = Q("(1)", "円錐Pの母線の長さを答えなさい。", W("辺ACを軸にして回転させるので、辺ABが母線になる。"), A("10 cm", "w20"), 18)
    q1b = Q("(2)", "円錐Pの体積を求めなさい。", W(r"底面の半径は BC＝6cm、高さは AC＝8cm<br>$\dfrac13\times\pi\times6^2\times8=96\pi$"), A(r"$96\pi$ cm³", "w30"), 24)
    q2a = Q("(1)", "円錐Pの展開図をかくとき、側面の形として適切なものを、次のア〜エから1つ選び、記号で答えなさい。"
            f'<div style="margin:1mm 0 0 7mm">{sectors_svg()}</div>',
            W(r"側面のおうぎ形は、半径が母線12cm、弧の長さが底面の円周 $2\pi\times6$。<br>"
              r"中心角は $360^\circ\times\dfrac{6}{12}=180^\circ$（半円）"), A("ウ", "w20"), 12)
    q2b = Q("(2)", "円錐Pの表面積を求めなさい。",
            W(r"側面積＝$\pi\times12^2\times\dfrac{180}{360}=72\pi$（または $\pi\times12\times6$）　底面積＝$\pi\times6^2=36\pi$<br>$72\pi+36\pi=108\pi$"),
            A(r"$108\pi$ cm²", "w30"), 22)
    return f"""<section class="page">{header("大問5　空間図形（円錐）")}
<div class="flex"><div class="grow"><div class="lead">右の図のように、AB＝$a$ cm、BC＝6cm、CA＝$b$ cm、$\\angle\\mathrm{{C}}=90^\\circ$ の直角三角形ABCがある。この三角形を、辺ACを軸にして1回転させてできる円錐Pについて、次の1、2の問いに答えなさい。ただし、円周率は $\\pi$ とする。</div>
<div class="q"><div class="qt"><span class="no">1</span>$a=10,\\ b=8$ のとき、次の(1)、(2)の問いに答えなさい。</div></div>{q1a}</div>
<div class="fig">{cone_tri_svg()}</div></div>
{q1b}
<div class="q"><div class="qt"><span class="no">2</span>$a=12$ のとき、次の(1)、(2)の問いに答えなさい。</div></div>
{q2a}{q2b}
</section>"""


JOBS = [("c3_jitsu3_d1", d1), ("c3_jitsu3_kakuritsu", d2a), ("c3_jitsu3_houtei", d2b),
        ("c3_jitsu3_ichiji", d3), ("c3_jitsu3_zukei", d4), ("c3_jitsu3_kuukan", d5)]

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    only = sys.argv[1:]
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for name, fn in JOBS:
            if only and name not in only:
                continue
            body = fn()
            for mode, suffix in [("mondai", ""), ("kaitou", "_ans")]:
                hp = pathlib.Path(f"/tmp/{name}_{mode}.html")
                hp.write_text(build(body, mode), encoding="utf-8")
                pg = br.new_page(viewport={"width": 794, "height": 1123})
                pg.goto(f"file://{hp}")
                pg.wait_for_selector("body[data-done]")
                pg.evaluate("document.fonts.ready")
                bad = pg.evaluate("""() => { const r = []; document.querySelectorAll('.page').forEach((p, i) => {
                    if (p.scrollHeight > p.clientHeight + 1) r.push('ページ' + (i + 1) + ' はみ出し ' + (p.scrollHeight - p.clientHeight) + 'px'); }); return r; }""")
                if bad:
                    print("!!", name + suffix, bad)
                pg.pdf(path=str(OUT / f"{name}{suffix}.pdf"), format="A4", print_background=True, prefer_css_page_size=True)
                pg.close()
                print("書き出し:", f"{name}{suffix}.pdf")
        br.close()
