"""尚志館高等学校 入学試験問題（令和4年度 本試験）数学を、大問ごとの PDF にする。
問題（pdf/c3_shishikan_r4_*.pdf）と、問題に赤字で答え・解説を書き込んだ「解答・解説」（_ans.pdf）を同じレイアウトで出す。
サイトでは「尚志館入試過去問」のタブ（common.json の nyushi[] の id＝shishikan）。test の id は shi-r4。

  大問1  計算                          c3_shishikan_r4_d1      → 小問集合（大問1・大問2）
  大問2  小問集合（8問）                c3_shishikan_r4_d2      → 小問集合（大問1・大問2）
  大問3  関数 y＝ax²（回転体）          c3_shishikan_r4_kansu   → 関数 y＝ax²
  大問4  立方体と三角すい（会話文）     c3_shishikan_r4_kuukan  → 空間図形
  大問5  円と相似（トレミーの定理）     c3_shishikan_r4_zukei   → 平面図形

実行：cd tools && python3 c3_shishikan_r4.py
"""
from fractions import Fraction as F
from itertools import product
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build, _arc  # noqa: E402
from c3_jitsu3_test import T, L, right_mark  # noqa: E402
from c3_shishikan_r8 import header as _header, svg, dot  # noqa: E402

# ================= 答えの確認 =================
assert 2022 - 4 * 124 == 1526 and F(1, 2) + F(1, 3) + F(1, 6) == 1
for a in range(1, 4):
    for b in range(1, 4):
        assert F(2 * a + b, 3) - F(a + 2 * b, 6) == F(a, 2)
        assert F(2 * a * a * b ** 3, (a * b * b) ** 2) * b == 2
assert 3 - 2 + 1 == 2                                           # 3√3−2√3＋√3
assert all((x + 8) * (x - 2) - (x + 4) * (x - 4) == 6 * x for x in range(-3, 4))
assert 4 * 6 ** 2 == 144 and F(4, 3) * 6 ** 3 == 288
assert F(sum(sum(c) >= 2 for c in product((0, 1), repeat=3)), 8) == F(1, 2)
assert all((x - 1) ** 2 + 3 * (x - 1) == 10 for x in (-4, 3))
assert [n for n in range(1, 50) if (20 * n) % 3 == 0 and math.isqrt(20 * n // 3) ** 2 == 20 * n // 3][0] == 15
C5 = 48
assert (C5 + 16) + (C5 + 23) + C5 + (C5 + 13) == 61 * 4 and C5 + 16 == 64
assert 3 - 2 * 1 == 1 and 2 * 1 * 1 + 3 * -2 == -4               # a＝3、b＝1
assert 180 - (360 - (180 - 70)) / 2 == 55
assert 48 + 1 == 49                                             # AD＝√(48＋1)＝7
assert F(2, 4) == F(1, 2) and F(1, 2) * 16 == 8 and F(8 - 2, 4 + 2) == 1
assert F(1, 2) * 4 * 2 == 4 and F(1, 2) * 4 * (2 + 4) == 12
VCBO = F(64, 3) + 64
VCAO = F(8, 3) + F(8, 3)
assert VCBO - VCAO == 80                                        # 80π
# 大問4：A(0,0,0) B(7,0,0) C(7,7,0) D(0,7,0) G(7,7,7)、BP：PC＝2：1、CQ：QD＝2：1
Pc, Qc, Gc, Ac = (7, F(14, 3), 0), (F(7, 3), 7, 0), (7, 7, 7), (0, 0, 0)
d2 = lambda p, q: sum((i - j) ** 2 for i, j in zip(p, q))
assert d2(Gc, Qc) == d2(Ac, Pc) and d2(Gc, Pc) == d2(Ac, Qc)       # GQ＝AP、GP＝AQ
sCPQ = F(1, 2) * F(7, 3) * F(14, 3)
sAQP = 49 - F(49, 3) - F(49, 6) - sCPQ
assert sCPQ / sAQP == F(2, 7) and F(49, 6) + F(49, 3) + sCPQ + sAQP == 49
assert 7 * F(2, 7) == 2
# 大問5：トレミー（数値で確認）
pt = lambda deg: (math.cos(math.radians(deg)), math.sin(math.radians(deg)))
Ap, Bp, Cp, Dp = pt(95), pt(205), pt(300), pt(20)
dd = math.dist
assert abs(dd(Ap, Bp) * dd(Cp, Dp) + dd(Ap, Dp) * dd(Bp, Cp) - dd(Ap, Cp) * dd(Bp, Dp)) < 1e-9

TAG = "尚志館　令和4年度　本試験"


def header(title, page=None):
    return _header(title, page).replace("令和8年度", "令和4年度")


def ch(*ws):
    return '<div class="ch" style="border:1px solid #444;display:inline-block;padding:0.6mm 4mm;margin:0.6mm 0 0.6mm 4mm;line-height:1.8">' + "　".join(ws) + "</div>"


def dl(who, t):
    return f'<p class="dl"><b>{who}</b>「{t}」</p>'


def un(p, q):
    d = math.dist(p, q)
    return ((q[0] - p[0]) / d, (q[1] - p[1]) / d)


def inter(p1, p2, p3, p4):
    d1, d2_ = (p2[0] - p1[0], p2[1] - p1[1]), (p4[0] - p3[0], p4[1] - p3[1])
    den = d1[0] * d2_[1] - d1[1] * d2_[0]
    t = ((p3[0] - p1[0]) * d2_[1] - (p3[1] - p1[1]) * d2_[0]) / den
    return (p1[0] + t * d1[0], p1[1] + t * d1[1])


# ================= 図 =================
def bis_svg():
    Ap = (120, 10)
    lft = (Ap[0] - 200 * math.sin(math.radians(28)), Ap[1] + 200 * math.cos(math.radians(28)))
    rgt = (Ap[0] + 200 * math.sin(math.radians(42)), Ap[1] + 200 * math.cos(math.radians(42)))
    P_ = (Ap[0] + (lft[0] - Ap[0]) * 0.38, Ap[1] + (lft[1] - Ap[1]) * 0.38)
    Qy = P_[1]
    t = (Qy - Ap[1]) / (rgt[1] - Ap[1])
    Q_ = (Ap[0] + (rgt[0] - Ap[0]) * t, Qy)
    # 外角の二等分線
    def bis(V, a_dir, b_dir):
        u1, u2 = un(V, a_dir), un(V, b_dir)
        return (u1[0] + u2[0], u1[1] + u2[1])
    b1 = bis(P_, Q_, lft)
    b2 = bis(Q_, P_, rgt)
    X_ = inter(P_, (P_[0] + b1[0], P_[1] + b1[1]), Q_, (Q_[0] + b2[0], Q_[1] + b2[1]))
    s = L(Ap, lft) + L(Ap, rgt) + L(P_, Q_) + L(P_, X_) + L(Q_, X_)
    s += T(Ap[0] + 2, Ap[1] + 26, "70°", "sm") + _arc(Ap, 14, 270 - 42, 270 + 28)
    s += T(X_[0], X_[1] - 10, '<tspan class="ax">x</tspan>', "sm")
    def mark(V, d1, d2_, sym):
        m1 = un(V, d1)
        m2 = un(V, d2_)
        mid = (m1[0] + m2[0] * 0.0, 0)
        p1 = (V[0] + 14 * (m1[0] * 0.8 + m2[0] * 0.2) / 1, V[1] + 14 * (m1[1] * 0.8 + m2[1] * 0.2))
        return T(p1[0], p1[1] + 3, sym, "sm")
    s += mark(P_, Q_, X_, "•") + mark(P_, lft, X_, "•") + mark(Q_, P_, X_, "×") + mark(Q_, rgt, X_, "×")
    return svg(250, 200, s, 0, 0)


def tri8_svg():
    k = 18
    P = lambda x, y: (16 + x * k, 156 - y * k)
    B_, C_, A_, D_ = P(0, 0), P(8, 0), P(4, 4 * math.sqrt(3)), P(3, 0)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="#000" stroke-width="1.2"/>' + L(A_, D_)
    s += T(A_[0], A_[1] - 4, "A") + T(B_[0] - 8, B_[1] + 4, "B") + T(C_[0] + 8, C_[1] + 4, "C") + T(D_[0], D_[1] + 13, "D")
    s += T((A_[0] + B_[0]) / 2 - 16, (A_[1] + B_[1]) / 2, "8cm", "sm") + T((B_[0] + D_[0]) / 2, B_[1] + 13, "3cm", "sm")
    M_ = P(4, 0)
    c = L(A_, M_, 0.9, True, "#c00") + right_mark(M_, (1, 0), (0, -1), 5) + T(M_[0] + 4, M_[1] + 13, "M", "sm") + T(M_[0] + 18, (A_[1] + M_[1]) / 2, "4√3", "sm")
    return svg(180, 172, s + f'<g class="cons">{c}</g>', 0, 0)


def para_svg():
    sx, sy = 22, 11
    ox, oy = 16 + 4.6 * sx, 12 + 8.8 * sy
    X = lambda x: ox + x * sx
    Y = lambda y: oy - y * sy
    s = L((X(-4.6), Y(0)), (X(5.2), Y(0)), 1) + L((X(0), Y(-1.4)), (X(0), Y(9.2)), 1)
    s += T(X(5.2) + 6, Y(0) + 4, '<tspan class="ax">x</tspan>', "pl") + T(X(0) + 3, Y(9.2) + 2, '<tspan class="ax">y</tspan>', "pl", "start") + T(X(0) - 7, Y(0) + 13, "O", "sm")
    xs = [i / 20 for i in range(-86, 86)]
    s += '<polyline points="' + " ".join(f"{X(x):.1f},{Y(x * x / 2):.1f}" for x in xs if x * x / 2 <= 9.2) + '" fill="none" stroke="#000" stroke-width="1.1"/>'
    s += L((X(-4.6), Y(-0.6)), (X(4.8), Y(8.8)), 1.1) + L((X(4), Y(8)), (X(4), Y(0)), 0.7, True)
    s += dot((X(-2), Y(2))) + dot((X(4), Y(8))) + T(X(-2) - 9, Y(2) - 2, "A") + T(X(4) + 9, Y(8) + 6, "B") + T(X(-4) - 2, Y(0) - 6, "C") + T(X(4), Y(0) + 13, "4", "sm")
    c = f'<polygon points="{X(0)},{Y(0)} {X(-2)},{Y(2)} {X(4)},{Y(8)}" fill="rgba(204,0,0,0.12)" stroke="#c00" stroke-width="1"/>'
    return svg(X(5.2) + 16, Y(-1.4) + 4, s + f'<g class="cons">{c}</g>')


def cube_svg():
    S = 120
    P = lambda x, y, z: (24 + x * S + y * S * 0.45, 20 + (1 - z) * S + (1 - y) * S * 0.32 - S * 0.0)
    V = {"A": (0, 0, 0), "B": (1, 0, 0), "C": (1, 1, 0), "D": (0, 1, 0), "E": (0, 0, 1), "F": (1, 0, 1), "G": (1, 1, 1), "H": (0, 1, 1)}
    # 手前は A・B・F・E（y＝0）。図の向きに合わせて少し回す
    p = {n: P(*v) for n, v in V.items()}
    s = "".join(L(p[a], p[b], 1.2) for a, b in ["AB", "BC", "CG", "GF", "FB", "FE", "EA", "EH", "HG"])
    s += "".join(L(p[a], p[b], 0.8, True) for a, b in ["AD", "DC", "DH"])
    Pp, Qp = P(1, 2 / 3, 0), P(1 / 3, 1, 0)
    s += L(p["G"], Pp, 1.1) + L(p["G"], Qp, 0.8, True) + L(Pp, Qp, 0.8, True) + dot(Pp, 1.8) + dot(Qp, 1.8)
    off = {"A": (-9, 4), "B": (0, 14), "C": (9, 4), "D": (-2, -5), "E": (-9, 2), "F": (-2, -5), "G": (9, 2), "H": (0, -5)}
    s += "".join(T(p[n][0] + dx, p[n][1] + dy, n, "sm") for n, (dx, dy) in off.items())
    s += T(Pp[0] + 2, Pp[1] + 13, "P", "sm") + T(Qp[0] - 2, Qp[1] + 13, "Q", "sm")
    c = L(p["A"], Pp, 0.9, True, "#c00") + L(p["A"], Qp, 0.9, True, "#c00")
    return svg(S * 1.45 + 48, S * 1.32 + 40, s + f'<g class="cons">{c}</g>')


def ptol_svg():
    k = 70
    O_ = (90, 82)
    P = lambda deg: (O_[0] + k * math.cos(math.radians(deg)), O_[1] - k * math.sin(math.radians(deg)))
    A_, B_, C_, D_ = P(95), P(205), P(300), P(20)
    # E：BD上で ∠BAE＝∠CAD
    def angle(p, v, q):
        a1 = math.atan2(p[1] - v[1], p[0] - v[0])
        a2 = math.atan2(q[1] - v[1], q[0] - v[0])
        return abs(math.degrees(a1 - a2))
    target = angle(C_, A_, D_)
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        E_ = (B_[0] + (D_[0] - B_[0]) * m, B_[1] + (D_[1] - B_[1]) * m)
        if angle(B_, A_, E_) < target:
            lo = m
        else:
            hi = m
    s = f'<circle cx="{O_[0]}" cy="{O_[1]}" r="{k}" fill="none" stroke="#000" stroke-width="1"/>'
    s += L(A_, B_) + L(A_, C_) + L(A_, D_) + L(A_, E_) + L(B_, D_) + L(B_, C_) + L(C_, D_) + dot(E_, 1.6)
    s += T(A_[0], A_[1] - 4, "A") + T(B_[0] - 8, B_[1] + 4, "B") + T(C_[0] + 6, C_[1] + 10, "C") + T(D_[0] + 8, D_[1] - 2, "D") + T(E_[0] + 2, E_[1] + 13, "E")
    return svg(186, 168, s, 0, 0)


# ================= 大問1 =================
def d1():
    c = [Q("(1)", r"$2022-4\times124$", W(r"かけ算が先　$2022-496$"), A("1526"), 10),
         Q("(2)", r"$\dfrac12+\dfrac13+\dfrac16$", W(r"$\dfrac36+\dfrac26+\dfrac16=\dfrac66$"), A("1"), 10),
         Q("(3)", r"$\dfrac{2a+b}3-\dfrac{a+2b}6$", W(r"$\dfrac{2(2a+b)-(a+2b)}{6}=\dfrac{4a+2b-a-2b}{6}=\dfrac{3a}6$"), A(r"$\dfrac a2$"), 10),
         Q("(4)", r"$\sqrt{27}-\dfrac6{\sqrt3}+\sqrt3$", W(r"$\sqrt{27}=3\sqrt3$、$\dfrac6{\sqrt3}=\dfrac{6\sqrt3}3=2\sqrt3$<br>$3\sqrt3-2\sqrt3+\sqrt3$"), A(r"$2\sqrt3$"), 10),
         Q("(5)", r"$2a^2b^3\div(-ab^2)^2\times b$", W(r"$(-ab^2)^2=a^2b^4$　$\dfrac{2a^2b^3\times b}{a^2b^4}$"), A("2"), 10),
         Q("(6)", r"$(x+8)(x-2)-(x+4)(x-4)$", W(r"$(x^2+6x-16)-(x^2-16)$"), A(r"$6x$"), 10)]
    return f"""<section class="page">{header("大問1　計算")}
<div class="lead">次の(1)〜(6)の計算をしなさい。</div>
<div class="grid2">{"".join(c)}</div>
</section>"""


# ================= 大問2 =================
def d2():
    q = [Q("(1)", r"表面積が $144\pi$ cm² の球の体積を求めなさい。",
           W(r"半径を $r$ とすると　$4\pi r^2=144\pi$　$r^2=36$　$r=6$<br>体積　$\dfrac43\pi\times6^3=\dfrac43\pi\times216$"), A(r"$288\pi$ cm³"), 10),
         Q("(2)", "3枚の硬貨を同時に投げるとき、2枚以上表が出る確率を求めなさい。",
           W(r"表裏の出方は $2\times2\times2=8$（通り）。表が2枚：3通り、表が3枚：1通り　$\dfrac{4}8$"), A(r"$\dfrac12$"), 8),
         Q("(3)", r"2次方程式 $(x-1)^2+3(x-1)=10$ を解きなさい。",
           W(r"$x-1=t$ とおくと　$t^2+3t-10=0$　$(t+5)(t-2)=0$　$t=-5,\ 2$<br>$x-1=-5$ より $x=-4$、$x-1=2$ より $x=3$"), A(r"$x=-4,\ 3$"), 10),
         Q("(4)", r"$\sqrt{\dfrac{20n}3}$ が整数になるとき、最も小さい自然数 $n$ の値を求めなさい。",
           W(r"$\dfrac{20n}3=\dfrac{2^2\times5\times n}{3}$ が（整数の）2乗になればよい。$n=3\times5=15$ のとき $\dfrac{20\times15}3=100=10^2$"), A(r"$n=15$"), 10),
         Q("(5)", "A、B、C、Dの4人に数学のテストをしたところ、Aの得点はBの得点より7点低く、Cの得点よりも16点高かった。また、Cの得点とDの得点の差は13点で、Cの得点が最低点であった。4人の平均点が61点であったとき、Aの得点を求めなさい。",
           W(r"Cの得点を $x$ 点とすると　A＝$x+16$、B＝$x+23$、D＝$x+13$（Cが最低点なのでDはCより高い）<br>"
             r"合計 $4x+52=61\times4=244$　$4x=192$　$x=48$　A＝$48+16$"), A("64点"), 12)]
    q2 = [Q("(6)", r"連立方程式 $\begin{cases}ax+by=1\\2bx+ay=-4\end{cases}$ の解が $x=1$、$y=-2$ であるとき、$a$、$b$ の値を求めなさい。",
            W(r"代入すると $\begin{cases}a-2b=1\\2b-2a=-4\end{cases}$　2つの式をたすと $-a=-3$　$a=3$、$3-2b=1$ より $b=1$"),
            A(r"$a=3,\ b=1$"), 10),
          '<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(7)</span>右図において∠<span class="ax">x</span> の大きさを求めなさい。（同じ印の角は等しい）</div>'
          + W(r"上の三角形で、下の2つの内角を $p$、$q$ とすると $p+q=180^\circ-70^\circ=110^\circ$<br>"
              r"●は外角 $(180^\circ-p)$ の半分、×は外角 $(180^\circ-q)$ の半分。下の三角形で<br>"
              r"$x=180^\circ-\dfrac{(180^\circ-p)+(180^\circ-q)}{2}=180^\circ-\dfrac{360^\circ-110^\circ}2=180^\circ-125^\circ$")
          + f'<div class="al">答　{A("55°")}</div></div><div class="fig">{bis_svg()}</div></div></div>',
          '<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(8)</span>右図のように、1辺の長さが8cmの正三角形ABCの辺BC上にBD＝3cmとなるような点Dをとる。このとき、線分ADの長さを求めなさい。</div>'
          + W(r"AからBCに垂線AMをひくと、MはBCの中点で BM＝4、AM＝$8\times\dfrac{\sqrt3}2=4\sqrt3$、DM＝$4-3=1$<br>"
              r"△ADMで三平方の定理　AD＝$\sqrt{(4\sqrt3)^2+1^2}=\sqrt{49}$")
          + f'<div class="al">答　{A("7cm")}</div></div><div class="fig">{tri8_svg()}</div></div></div>']
    return f"""<section class="page">{header("大問2　小問集合", "1")}
<div class="lead">次の(1)〜(8)の各問いに答えなさい。</div>
{"".join(q)}
</section>
<section class="page">{header("大問2　小問集合", "2")}
{"".join(q2)}
</section>"""


# ================= 大問3 =================
def d3():
    q = [Q("(1)", r"$a$ の値と点Bの $y$ 座標を求めなさい。", W(r"A$(-2,\ 2)$ を代入　$2=4a$　$a=\dfrac12$　Bの $y$ 座標は $\dfrac12\times4^2$"),
           r"$a=$" + A(r"$\dfrac12$", "w20") + "　Bの<span class='ax'>y</span>座標" + A("8", "w20"), 6),
         Q("(2)", r"$x$ の変域が $-2\leqq x\leqq4$ のとき、$y$ の変域を求めなさい。", W(r"$x=0$ をふくむので最小値は0、最大値は $x=4$ のときの8"), A(r"$0\leqq y\leqq8$", "w30"), 4),
         Q("(3)", r"$x$ が $-2$ から4まで増加するときの変化の割合を求めなさい。", W(r"$\dfrac{8-2}{4-(-2)}=\dfrac66$"), A("1", "w20"), 4),
         Q("(4)", r"直線ABの式を求め、直線ABと $x$ 軸との交点の座標も求めなさい。",
           W(r"傾き1、$y=x+b$ に A を代入　$2=-2+b$　$b=4$　→ $y=x+4$。$y=0$ のとき $x=-4$"),
           A(r"$y=x+4$", "w20") + "　交点" + A(r"$(-4,\ 0)$", "w20"), 6),
         Q("(5)", "(4)で求めた $x$ 軸との交点をCとします。△OACと△OABの面積の比を最も簡単な整数比で答えなさい。",
           W(r"△OAC＝$\dfrac12\times4\times2=4$。△OAB は $y$ 軸との交点(0, 4)で分けて　$\dfrac12\times4\times\{4-(-2)\}=12$　$4:12$"),
           A("1：3", "w20"), 8),
         Q("(6)", r"△OABを $x$ 軸のまわりに1回転させたときにできる図形の体積を求めなさい。",
           W(r"Aは線分CB上にあるので、△OAB＝△CBO−△CAO。回転体の体積も（△CBOの回転体）−（△CAOの回転体）<br>"
             r"△CBO：Bから $x$ 軸に垂線BH（H(4, 0)）をひくと、円すい（底面の半径8、高さCH＝8）−円すい（半径8、高さOH＝4）<br>"
             r"　$\dfrac13\pi\times8^2\times8-\dfrac13\pi\times8^2\times4=\dfrac{256}3\pi$<br>"
             r"△CAO：半径2（Aの $y$ 座標）、高さの合計 CO＝4 の2つの円すい　$\dfrac13\pi\times2^2\times4=\dfrac{16}3\pi$<br>"
             r"$\dfrac{256}3\pi-\dfrac{16}3\pi=\dfrac{240}3\pi$"),
           A(r"$80\pi$", "w20"), 22)]
    return f"""<section class="page">{header("大問3　関数 y＝ax²")}
<div class="flex"><div class="grow"><div class="lead">右図のように、関数 $y=ax^2\\ (a\\gt0)$ ……①のグラフ上に2点A、Bがあります。点A$(-2,\\ 2)$ で点Bの $x$ 座標が4である。次の(1)〜(6)の各問いに答えなさい。</div>{q[0]}{q[1]}{q[2]}</div>
<div class="fig">{para_svg()}</div></div>
{q[3]}{q[4]}{q[5]}
</section>"""


# ================= 大問4 =================
def d4():
    talk = ('<div style="line-height:1.85;font-size:9.4pt">'
            + dl("尚子", "何を考えているの？") + dl("志郎", "点Cから、3点G、P、Qを含む平面に下ろした垂線の長さを考えているんだ。")
            + dl("尚子", "体積を求めてから？")
            + dl("志郎", "うん。三角すいの体積は、" + BX("(a)", r"$\dfrac13$") + "×" + BX("(ア)", "底面積") + "×" + BX("(イ)", "高さ") + " で求められるから…。")
            + dl("尚子", "だったら、わざわざ求めなくてもいいじゃない！") + dl("志郎", "どういうこと？")
            + dl("尚子", "△CPQと△" + BX("(ウ)", "GPQ") + " の面積の比を考えればいいじゃない？")
            + dl("志郎", "そうだよね。でも、どうすれば簡単に求められるかな？")
            + dl("尚子", "だって、GQの長さと " + BX("(エ)", "AP") + " の長さは等しいでしょう。")
            + dl("志郎", "そうか！だったらGPの長さと " + BX("(オ)", "AQ") + " の長さも等しいから△" + BX("(ウ)", "GPQ") + " と△" + BX("(カ)", "AQP") + " は合同だね。だったら、もう1つの問いも簡単に答えられたのだ！")
            + dl("尚子", "『もう1つの問い』って？") + dl("志郎", "三角すいG−PCQの表面積なんだ。") + dl("尚子", "即答できるわね。")
            + dl("志郎", "確かに！三角すいG−PCQの表面積は、" + BX("(b)", "49") + " だね。")
            + dl("尚子", "そして、△CPQと△" + BX("(ウ)", "GPQ") + " の面積比は簡単な整数比で表すと、" + BX("(c)", "2") + "：" + BX("(d)", "7") + " と分かるわね。")
            + dl("志郎", "ということは、△CPQと△" + BX("(ウ)", "GPQ") + " をそれぞれ底面としたときの高さの比を考えて計算すると点Cから、3点G、P、Qを含む平面に下ろした垂線の長さは " + BX("(e)", "2") + " になるね。")
            + "</div>")
    q = Q("問", "(a) 〜 (e) には、正しい数値を入れなさい。また、(ア) 〜 (イ) には語群Ⅰから、(ウ) 〜 (カ) は語群Ⅱの中から選んで答えなさい。<br>"
          + "語群Ⅰ" + ch("1辺", "縦", "横", "底辺", "底面積", "側面積", "高さ", "斜め") + "<br>"
          + "語群Ⅱ" + ch("ABP", "ADQ", "APQ", "AQP", "CPQ", "GCP", "GCQ", "GPQ", "<br>AB", "AD", "AP", "AQ", "CG", "CP", "CQ", "PQ"),
          W(r"CP＝$7\times\dfrac13=\dfrac73$（BP：PC＝2：1）、CQ＝$7\times\dfrac23=\dfrac{14}3$、DQ＝$\dfrac73$（CQ：QD＝2：1）<br>"
            r"エ・オ：GQ²＝$7^2+\left(\dfrac{14}3\right)^2$＝AB²＋BP²＝AP²、GP²＝$7^2+\left(\dfrac73\right)^2$＝AD²＋DQ²＝AQ²　→ △GPQ≡△AQP（3組の辺、PQ共通）<br>"
            r"(b)：△GCP≡△ADQ、△GCQ≡△ABP、△GPQ≡△AQP なので、表面積＝△ADQ＋△ABP＋△AQP＋△CPQ＝正方形ABCD＝$7\times7=49$<br>"
            r"(c)(d)：△CPQ＝$\dfrac12\times\dfrac73\times\dfrac{14}3=\dfrac{49}9$、△AQP＝$49-\dfrac{49}3-\dfrac{49}6-\dfrac{49}9=\dfrac{343}{18}$　$\dfrac{49}9:\dfrac{343}{18}=98:343=2:7$<br>"
            r"(e)：体積は同じなので、高さの比は面積の逆比。CG＝7 が底面△CPQのときの高さなので　$7\times\dfrac27=2$"),
          "(a)" + A(r"$\dfrac13$", "w20") + " (b)" + A("49", "w20") + " (c)" + A("2", "w20") + " (d)" + A("7", "w20") + " (e)" + A("2", "w20")
          + "<br>(ア)" + A("底面積", "w20") + " (イ)" + A("高さ", "w20") + " (ウ)" + A("GPQ", "w20") + " (エ)" + A("AP", "w20") + " (オ)" + A("AQ", "w20") + " (カ)" + A("AQP", "w20"), 4)
    return f"""<section class="page">{header("大問4　空間図形", "1")}
<div class="flex"><div class="grow"><div class="lead">1辺の長さが7である立方体ABCD−EFGHがあります。辺BCを2：1に分ける点をP、辺CDを2：1に分ける点をQとします。三角すいG−PCQについて考えている志郎君と尚子さんの会話を読んで、問いに答えなさい。</div></div>
<div class="fig">{cube_svg()}</div></div>
{talk}
</section>
<section class="page">{header("大問4　空間図形", "2")}
{q}
</section>"""


# ================= 大問5 =================
def d5():
    proof = ('<div class="frame" style="line-height:2">（証明）△BAEと△CADにおいて<br>仮定より　∠BAE＝∠' + BX("(ア)", "CAD") + "…①<br>"
             r"$\overset{\frown}{\mathrm{AD}}$ に対する円周角であるから　∠ABE＝∠" + BX("(イ)", "ACD") + "…②<br>①、②より　"
             + BX("(ウ)", "2組の角がそれぞれ等しい") + " から　△BAE∽△CAD</div>")
    q1 = Q("(1)", "△BAE∽△CADを次のように証明した。□にあてはまるものを答えなさい。ただし (ウ) には、三角形の相似条件が入ります。" + proof, "", "", 0)
    q2 = Q("(2)", "AB：BE＝ (i) ：(ii) の (i)、(ii) にあてはまる線分を答えなさい。",
           W("△BAE∽△CAD で、対応する辺は AB↔AC、BE↔CD なので AB：AC＝BE：CD、つまり AB：BE＝AC：CD"),
           "(i)" + A("AC", "w20") + "　(ii)" + A("CD", "w20"), 4)
    q3 = Q("(3)", "△ABC∽△AEDであることを証明しなさい。",
           lines(r"△ABCと△AEDにおいて<br>∠BAC＝∠BAE＋∠EAC、∠EAD＝∠EAC＋∠CAD で、仮定より ∠BAE＝∠CAD なので　∠BAC＝∠EAD……①<br>"
                 r"弧ABに対する円周角であるから　∠ACB＝∠ADB＝∠ADE……②<br>"
                 r"①、②より、2組の角がそれぞれ等しいから　△ABC∽△AED", 26), "", 0)
    q4 = Q("(4)", "AB×CD＋AD×BC＝AC×BDが成り立つことを証明しなさい。",
           lines(r"(2)より AB：BE＝AC：CD なので　AB×CD＝AC×BE……①<br>"
                 r"(3)の △ABC∽△AED より BC：ED＝AC：AD なので　AD×BC＝AC×ED……②<br>"
                 r"①＋②より　AB×CD＋AD×BC＝AC×BE＋AC×ED＝AC×(BE＋ED)<br>"
                 r"EはBD上の点なので BE＋ED＝BD　よって　AB×CD＋AD×BC＝AC×BD", 26), "", 0)
    return f"""<section class="page">{header("大問5　平面図形")}
<div class="flex"><div class="grow"><div class="lead">円周上に4点A、B、C、Dがあり、点Eは∠CAD＝∠BAEを満たす線分BD上の点である。このとき、△BAE∽△CAD、△ABC∽△AEDを利用して AB×CD＋AD×BC＝AC×BD が成り立つことを証明したい。次の(1)〜(4)の各問いに答えなさい。</div>{q1}</div>
<div class="fig">{ptol_svg()}</div></div>
{q2}{q3}{q4}
</section>"""


JOBS = [("c3_shishikan_r4_d1", d1), ("c3_shishikan_r4_d2", d2), ("c3_shishikan_r4_kansu", d3),
        ("c3_shishikan_r4_kuukan", d4), ("c3_shishikan_r4_zukei", d5)]

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
