"""尚志館高等学校 入学試験問題（令和6年度 本試験）数学を、大問ごとの PDF にする。
問題（pdf/c3_shishikan_r6_*.pdf）と、問題に赤字で答え・解説を書き込んだ「解答・解説」（_ans.pdf）を同じレイアウトで出す。
サイトでは「尚志館入試過去問」のタブ（common.json の nyushi[] の id＝shishikan）。test の id は shi-r6。

  大問1  計算                          c3_shishikan_r6_d1      → 小問集合（大問1・大問2）
  大問2  小問集合（8問）                c3_shishikan_r6_d2      → 小問集合（大問1・大問2）
  大問3  関数 y＝ax²（最短距離）         c3_shishikan_r6_kansu   → 関数 y＝ax²
  大問4  垂心と合同の証明（会話文）     c3_shishikan_r6_zukei   → 平面図形
  大問5  直角三角すいと切断            c3_shishikan_r6_kuukan  → 空間図形

実行：cd tools && python3 c3_shishikan_r6.py
"""
from fractions import Fraction as F
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build, _arc  # noqa: E402
from c3_jitsu3_test import T, L, right_mark  # noqa: E402
from c3_shishikan_r8 import header as _header, svg, dot  # noqa: E402

# ================= 答えの確認 =================
assert 2024 - 123 * 6 == 1286 and F(4, 3) + F(5, 6) - F(3, 2) == F(2, 3)
for a in range(1, 4):
    for b in range(1, 4):
        assert F(3 * a + b, 6) - F(a - b, 2) == F(2 * b, 3)
        assert F((-a) ** 2, 2 * a * b ** 4) * 4 * b ** 5 == 2 * a * b
assert 4 - 3 + 2 == 3                                           # 4√2−3√2＋2√2
assert all((x + 3) ** 2 - (x + 7) * (x - 1) == 16 for x in range(-3, 4))
assert 24 < 25 and 100 * F(100, 4) == 2500 and F(62.5) + F(30, 25) == F(637, 10)
days = (1 - F(4, 12)) / (F(1, 12) + F(1, 10))
assert days == F(40, 11)
cube = {(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)}
mids = []                                                       # x−y＋z＝1/2 と辺の交点（立方体の辺の中点6つ）
for p in cube:
    for q in cube:
        if p < q and sum(abs(i - j) for i, j in zip(p, q)) == 1:
            m = tuple(F(i + j, 2) for i, j in zip(p, q))
            if m[0] - m[1] + m[2] == F(1, 2):
                mids.append(m)
assert len(mids) == 6
assert 2 * math.factorial(3) == 12                              # 窓側の席は2つ、残り3人は3!
assert (61 - 37) / 2 == 12
assert 2024 == 2 ** 3 * 11 * 23
a3 = F(18, 9)
assert a3 == 2
Ab, Bb = (-1, 2), (3, 18)
assert F(Bb[1] - Ab[1], Bb[0] - Ab[0]) == 4 and F(-6, 4) == F(-3, 2)
assert F(1, 2) * F(3, 2) * 2 / (F(1, 2) * 6 * 4) == F(1, 8)
assert F(18 - (-2), 3 - (-1)) == 5 and F(-3, 5) * 5 + 3 == 0
# 大問4：D(0,0) E(a,0) F(0,b)
for aa, bb in [(3, 2), (5, 4), (2, 7)]:
    E_, F_, I_, J_, L_, K_ = (aa, 0), (0, bb), (0, -aa), (aa, -aa), (-bb, 0), (-bb, bb)
    G_ = (E_[0] + F_[0] - K_[0], E_[1] + F_[1] - K_[1])
    assert G_ == (aa + bb, 0)
    vIG, vJF = (G_[0] - I_[0], G_[1] - I_[1]), (F_[0] - J_[0], F_[1] - J_[1])
    assert vIG[0] * vJF[0] + vIG[1] * vJF[1] == 0                # IG⊥JF
    # M：JF と DE（x軸）、N：EK と DF（y軸）
    Mx = J_[0] + (F_[0] - J_[0]) * F(0 - J_[1], F_[1] - J_[1])
    Ny = E_[1] + (K_[1] - E_[1]) * F(0 - E_[0], K_[0] - E_[0])
    assert Mx == Ny                                              # DM＝DN
# 大問5
assert F(1, 6) * 4 * 4 * 3 == 8
assert 25 - 8 == 17                                             # AB＝4√2、AC＝BC＝5、高さ√17 → 2√34
h5 = 3 * 8 / (2 * math.sqrt(34))
assert abs(h5 - 6 * math.sqrt(34) / 17) < 1e-12
assert F(1, 3) * F(1, 2) * F(8, 3) * F(8, 3) * 3 + F(1, 3) * F(64, 9) == F(160, 27)
assert 3 * (F(8, 3) ** 2 / 2 - F(8, 3) ** 3 / 12) == F(160, 27)  # 積分での確認

TAG = "尚志館　令和6年度　本試験"


def header(title, page=None):
    return _header(title, page).replace("令和8年度", "令和6年度")


def ch(*ws):
    return '<div class="ch" style="border:1px solid #444;display:inline-block;padding:1mm 4mm;margin:1mm 0 1mm 6mm;line-height:1.8">' + "　　".join(ws) + "</div>"


def dl(who, t):
    return f'<p class="dl"><b>{who}</b>「{t}」</p>'


# ================= 図 =================
def cube_svg():
    S = 92
    P = lambda x, y, z: (14 + x * S + y * S * 0.55, 34 + (1 - z) * S - y * S * 0.32)
    V = {"A": (0, 0, 1), "B": (1, 0, 1), "C": (1, 1, 1), "D": (0, 1, 1), "E": (0, 0, 0), "F": (1, 0, 0), "G": (1, 1, 0), "H": (0, 1, 0)}
    p = {n: P(*v) for n, v in V.items()}
    s = "".join(L(p[a], p[b], 1.2) for a, b in ["AB", "BC", "CD", "DA", "AE", "EF", "FB", "FG", "GC"])
    s += "".join(L(p[a], p[b], 0.8, True) for a, b in ["DH", "HE", "HG"])
    off = {"A": (-9, 3), "B": (9, 10), "C": (9, -3), "D": (0, -5), "E": (-9, 6), "F": (6, 13), "G": (10, 4), "H": (8, -4)}
    s += "".join(T(p[n][0] + dx, p[n][1] + dy, n, "sm") for n, (dx, dy) in off.items())
    Pp, Qp, Rp = P(0, 0.5, 1), P(0, 0, 0.5), P(0.5, 0, 0)
    s += dot(Pp, 1.8) + dot(Qp, 1.8) + dot(Rp, 1.8) + T(Pp[0] - 6, Pp[1] - 5, "P", "sm") + T(Qp[0] - 9, Qp[1] + 4, "Q", "sm") + T(Rp[0], Rp[1] + 13, "R", "sm")
    hexa = [P(0, 0.5, 1), P(0, 0, 0.5), P(0.5, 0, 0), P(1, 0.5, 0), P(1, 1, 0.5), P(0.5, 1, 1)]
    c = '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in hexa) + '" fill="rgba(204,0,0,0.12)" stroke="#c00" stroke-width="1.2"/>'
    return svg(S * 1.55 + 40, S * 1.32 + 52, s + f'<g class="cons">{c}</g>')


def circ_svg():
    k = 70
    O_ = (88, 86)
    P = lambda deg: (O_[0] + k * math.cos(math.radians(deg)), O_[1] - k * math.sin(math.radians(deg)))
    A_, B_, C_, D_ = P(128), P(226), P(336), P(360)

    def inter(p1, p2, p3, p4):
        d1, d2 = (p2[0] - p1[0], p2[1] - p1[1]), (p4[0] - p3[0], p4[1] - p3[1])
        den = d1[0] * d2[1] - d1[1] * d2[0]
        t = ((p3[0] - p1[0]) * d2[1] - (p3[1] - p1[1]) * d2[0]) / den
        return (p1[0] + t * d1[0], p1[1] + t * d1[1])
    E_ = inter(A_, D_, B_, C_)
    X_ = inter(A_, C_, B_, D_)
    s = f'<circle cx="{O_[0]}" cy="{O_[1]}" r="{k}" fill="none" stroke="#000" stroke-width="1"/>'
    s += L(A_, C_) + L(B_, D_) + L(A_, E_) + L(B_, E_)
    s += T(A_[0] - 7, A_[1] - 3, "A") + T(B_[0] - 8, B_[1] + 6, "B") + T(C_[0] + 4, C_[1] + 13, "C") + T(D_[0] + 9, D_[1] - 3, "D")
    s += T(X_[0] - 24, X_[1] + 2, "61°", "sm") + T(E_[0] - 30, E_[1] - 1, "37°", "sm") + T(A_[0] + 22, A_[1] + 18, '<tspan class="ax">x</tspan>', "sm")
    ang = lambda p, q: math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0]))
    s += _arc(X_, 10, ang(X_, A_), ang(X_, B_) + 360 if ang(X_, B_) < ang(X_, A_) else ang(X_, B_))
    s += _arc(E_, 16, ang(E_, A_), ang(E_, B_)) + _arc(A_, 18, ang(A_, D_), ang(A_, C_))
    return svg(int(E_[0]) + 12, 178, s)


def para_svg():
    sx, sy = 30, 7
    ox, oy = 20 + 2.6 * sx, 12 + 20 * sy
    X = lambda x: ox + x * sx
    Y = lambda y: oy - y * sy
    s = L((X(-2.6), Y(0)), (X(3.6), Y(0)), 1) + L((X(0), Y(-4)), (X(0), Y(21)), 1)
    s += T(X(3.6) + 7, Y(0) + 4, '<tspan class="ax">x</tspan>', "pl") + T(X(0) + 3, Y(21) + 3, '<tspan class="ax">y</tspan>', "pl", "start") + T(X(0) + 8, Y(0) + 12, "O", "sm")
    xs = [i / 20 for i in range(-64, 66)]
    s += '<polyline points="' + " ".join(f"{X(x):.1f},{Y(2 * x * x):.1f}" for x in xs if 2 * x * x <= 20.5) + '" fill="none" stroke="#000" stroke-width="1.1"/>'
    s += L((X(-2.4), Y(4 * -2.4 + 6)), (X(3.6), Y(4 * 3.6 + 6) if 4 * 3.6 + 6 < 21 else Y(21)), 1.1)
    s += dot((X(-1), Y(2))) + dot((X(3), Y(18))) + T(X(-1) - 9, Y(2) - 2, "A") + T(X(3) + 9, Y(18), "B")
    c = dot((X(-1.5), Y(0)), 2.2, "#c00") + T(X(-1.5) - 4, Y(0) + 13, "C")
    c += L((X(-1), Y(2)), (X(-1), Y(-2)), 0.8, True, "#c00") + dot((X(-1), Y(-2)), 2.2, "#c00") + T(X(-1) - 12, Y(-2) + 4, "A′")
    c += L((X(-1), Y(-2)), (X(3), Y(18)), 1.1, False, "#c00") + dot((X(-0.6), Y(0)), 2.6, "#c00") + T(X(-0.6) + 10, Y(0) + 12, "P")
    return svg(X(3.6) + 18, Y(-4) + 4, s + f'<g class="cons">{c}</g>')


def ortho_svg():
    A_, B_, C_ = (90, 10), (14, 150), (156, 150)
    def foot(p, a, b):
        d = (b[0] - a[0], b[1] - a[1])
        t = ((p[0] - a[0]) * d[0] + (p[1] - a[1]) * d[1]) / (d[0] ** 2 + d[1] ** 2)
        return (a[0] + t * d[0], a[1] + t * d[1])
    Qf, Rf, Pf = foot(B_, A_, C_), foot(C_, A_, B_), foot(A_, B_, C_)
    Hy = B_[1] + (Qf[1] - B_[1]) * (Pf[0] - B_[0]) / (Qf[0] - B_[0])
    H_ = (Pf[0], Hy)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += L(B_, Qf) + L(C_, Rf) + L(A_, Pf)
    u = lambda p, q: ((q[0] - p[0]) / math.dist(p, q), (q[1] - p[1]) / math.dist(p, q))
    s += right_mark(Qf, u(Qf, C_), u(Qf, B_), 5) + right_mark(Rf, u(Rf, B_), u(Rf, C_), 5)
    s += T(A_[0], A_[1] - 3, "A") + T(B_[0] - 8, B_[1] + 4, "B") + T(C_[0] + 8, C_[1] + 4, "C") + T(Pf[0], Pf[1] + 13, "P") + T(Qf[0] + 9, Qf[1], "Q") + T(Rf[0] - 9, Rf[1], "R") + T(H_[0] + 8, H_[1] - 3, "H", "sm")
    return svg(172, 170, s, 0, -6)


def sq_pts():
    D_ = (150.0, 96.0)
    u, v = (-0.80, 0.60), (0.60, 0.80)                         # DE 方向・DF 方向（画面の座標）
    a, b = 120, 100
    E_ = (D_[0] + a * u[0], D_[1] + a * u[1])
    F_ = (D_[0] + b * v[0], D_[1] + b * v[1])
    I_ = (D_[0] - a * v[0], D_[1] - a * v[1])
    J_ = (I_[0] + E_[0] - D_[0], I_[1] + E_[1] - D_[1])
    L_ = (D_[0] - b * u[0], D_[1] - b * u[1])
    K_ = (L_[0] + F_[0] - D_[0], L_[1] + F_[1] - D_[1])
    G_ = (E_[0] + F_[0] - K_[0], E_[1] + F_[1] - K_[1])

    def inter(p1, p2, p3, p4):
        d1, d2 = (p2[0] - p1[0], p2[1] - p1[1]), (p4[0] - p3[0], p4[1] - p3[1])
        den = d1[0] * d2[1] - d1[1] * d2[0]
        t = ((p3[0] - p1[0]) * d2[1] - (p3[1] - p1[1]) * d2[0]) / den
        return (p1[0] + t * d1[0], p1[1] + t * d1[1])
    M_ = inter(D_, E_, J_, F_)
    N_ = inter(E_, K_, D_, F_)
    return dict(D=D_, E=E_, F=F_, I=I_, J=J_, L=L_, K=K_, G=G_, M=M_, N=N_)


def square_svg():
    p = sq_pts()
    s = "".join(L(p[a], p[b], 1.1) for a, b in ["DI", "IJ", "JE", "DE", "DF", "EF", "FK", "KL", "LD", "JF", "EK", "GE", "GF", "IG", "IF"])
    s += right_mark(p["D"], (0.60, 0.80), (-0.80, 0.60), 6)
    off = {"D": (4, -6), "E": (-9, 4), "F": (5, 13), "I": (0, -5), "J": (-9, 3), "K": (9, 3), "L": (5, -5), "G": (-8, 10), "M": (0, -6), "N": (9, 8)}
    s += "".join(T(p[n][0] + dx, p[n][1] + dy, n, "sm") for n, (dx, dy) in off.items())
    xs = [q[0] for q in p.values()]
    ys = [q[1] for q in p.values()]
    x0, y0 = min(xs) - 16, min(ys) - 14
    c = L(p["I"], p["M"], 1.0, True, "#c00") + L(p["M"], (p["M"][0] + (p["M"][0] - p["I"][0]) * 0.6, p["M"][1] + (p["M"][1] - p["I"][1]) * 0.6), 1.0, True, "#c00")
    return svg(max(xs) - x0 + 18, max(ys) - y0 + 18, s + f'<g class="cons">{c}</g>', x0, y0)


def tet_svg():
    O_, A_, B_, C_ = (128, 150), (130, 14), (14, 210), (220, 186)
    s = L(A_, B_) + L(A_, C_) + L(B_, C_) + L(O_, A_, 0.8, True) + L(O_, B_, 0.8, True) + L(O_, C_, 0.8, True)
    s += T(A_[0], A_[1] - 4, "A") + T(B_[0] - 8, B_[1] + 4, "B") + T(C_[0] + 9, C_[1] + 4, "C") + T(O_[0] + 2, O_[1] + 16, "O")
    s += f'<polygon points="{O_[0]},{O_[1]} {O_[0]},{O_[1] - 7} {O_[0] - 6},{O_[1] - 4} {O_[0] - 6},{O_[1] + 3}" fill="none" stroke="#000" stroke-width="0.6"/>'
    lp = lambda p, q, t: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    Pp, Qp, Rp, Sp = lp(O_, A_, 2 / 3), lp(O_, B_, 2 / 3), lp(B_, C_, 1 / 3), lp(A_, C_, 1 / 3)
    c = f'<polygon points="{Pp[0]:.1f},{Pp[1]:.1f} {Qp[0]:.1f},{Qp[1]:.1f} {Rp[0]:.1f},{Rp[1]:.1f} {Sp[0]:.1f},{Sp[1]:.1f}" fill="rgba(204,0,0,0.12)" stroke="#c00" stroke-width="1.1"/>'
    c += T(Pp[0] - 9, Pp[1] + 2, "P", "sm") + T(Qp[0] - 2, Qp[1] - 6, "Q", "sm") + T(Rp[0], Rp[1] + 13, "R", "sm") + T(Sp[0] + 9, Sp[1], "S", "sm")
    return svg(240, 226, s + f'<g class="cons">{c}</g>', 0, -4)


# ================= 大問1 =================
def d1():
    c = [Q("(1)", r"$2024-123\times6$", W(r"かけ算が先　$2024-738$"), A("1286"), 10),
         Q("(2)", r"$\dfrac43+\dfrac56-\dfrac32$", W(r"分母を6にそろえる　$\dfrac86+\dfrac56-\dfrac96=\dfrac46$"), A(r"$\dfrac23$"), 10),
         Q("(3)", r"$\dfrac{3a+b}6-\dfrac{a-b}2$", W(r"$\dfrac{3a+b-3(a-b)}{6}=\dfrac{3a+b-3a+3b}{6}=\dfrac{4b}6$"), A(r"$\dfrac{2b}{3}$"), 10),
         Q("(4)", r"$(-a)^2\div2ab^4\times4b^5$", W(r"$a^2\times\dfrac1{2ab^4}\times4b^5=\dfrac{4a^2b^5}{2ab^4}$"), A(r"$2ab$"), 10),
         Q("(5)", r"$\sqrt{32}-3\sqrt2+\dfrac4{\sqrt2}$", W(r"$\sqrt{32}=4\sqrt2$、$\dfrac4{\sqrt2}=\dfrac{4\sqrt2}2=2\sqrt2$<br>$4\sqrt2-3\sqrt2+2\sqrt2$"), A(r"$3\sqrt2$"), 10),
         Q("(6)", r"$(x+3)^2-(x+7)(x-1)$", W(r"$(x^2+6x+9)-(x^2+6x-7)$<br>$=9+7$"), A("16"), 10)]
    return f"""<section class="page">{header("大問1　計算")}
<div class="lead">次の(1)〜(6)の計算をしなさい。</div>
<div class="grid2">{"".join(c)}</div>
</section>"""


# ================= 大問2 =================
def d2():
    q = [Q("(1)", r"$2\sqrt6$ と5のうち、大きい数はどちらか答えなさい。",
           W(r"$2\sqrt6=\sqrt{4\times6}=\sqrt{24}$、$5=\sqrt{25}$。$24\lt25$ なので $\sqrt{24}\lt\sqrt{25}$"), A("5"), 8),
         Q("(2)", "池にいるコイの数を調べるため、池から100匹のコイを捕まえて、印を付けた後、コイを池に戻した。翌日、池から再び100匹のコイを捕まえたところ、4匹だけに印が付いていた。池には、およそ何匹のコイがいると考えられるか。",
           W(r"池全体を $x$ 匹とすると、印の付いたコイの割合は同じと考えて　$x:100=100:4$　$4x=10000$"), A("およそ2500匹"), 10),
         Q("(3)", "25人のクラスで数学のテストがあった。最初は平均点が62.5点と発表されたが、採点ミスがあり、合計点が30点あがった。修正後の平均点を求めなさい。",
           W(r"合計が30点ふえると、平均は $30\div25=1.2$（点）ふえる　$62.5+1.2$"), A("63.7点"), 8),
         Q("(4)", "ある仕事を終わらせるのに、Aさんは12日間、Bさんは10日間かかる。同じ仕事をAさんが4日間行った後、残りはA、Bの2人で仕事をした。このとき、二人で仕事をしたのは何日間か求めなさい。",
           W(r"仕事全体を1とすると、1日にAは $\dfrac1{12}$、Bは $\dfrac1{10}$。Aの4日で $\dfrac4{12}=\dfrac13$、残りは $\dfrac23$<br>"
             r"2人で1日に $\dfrac1{12}+\dfrac1{10}=\dfrac{11}{60}$　$\dfrac23\div\dfrac{11}{60}=\dfrac23\times\dfrac{60}{11}=\dfrac{40}{11}$（$3\dfrac7{11}$ 日）"),
           A(r"$\dfrac{40}{11}$ 日間"), 12),
         '<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(5)</span>右図のような立方体ABCD−EFGHにおいて、AD、AE、EFの中点P、Q、Rを通るようにこの立方体を切断するとき、切断面はどのような形になるか。</div>'
         + W("切り口は、P、Q、Rのほかに、FG・GC・CDの中点も通る（向かい合う面の切り口は平行になる）。<br>6つの辺の中点を結ぶので、6辺の長さがすべて等しく（面の対角線の半分）、角もすべて等しい")
         + f'<div class="al">答　{A("正六角形")}</div></div><div class="fig">{cube_svg()}</div></div></div>']
    q2 = [Q("(6)", "遠足のバスでA、B、C、Dの4人が後部座席に座ることになった。Aが窓側の席になるような座り方は何通りあるか求めなさい。",
            W(r"後部座席は4人が横1列にならび、窓側は両はしの2席。Aの席の選び方が2通り、残りの3席にB、C、Dが座る並び方が $3\times2\times1=6$（通り）<br>$2\times6$"),
            A("12通り"), 10),
          '<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(7)</span>右の図で、<span class="ax">x</span> の値を求めなさい。</div>'
          + W(r"ACとBDの交点をX、直線ADとBCの交点をYとする。∠DAC＝∠DBC＝$x$（弧DCに対する円周角）<br>61°は△AXDの外角なので　$61^\circ=x+\angle\mathrm{ADB}$<br>"
              r"∠ADBは△DBYの外角なので　∠ADB＝∠DBY＋∠DYB＝$x+37^\circ$<br>"
              r"$61^\circ=x+x+37^\circ$　$2x=24^\circ$")
          + f'<div class="al">答　{A(r"$x=12$")}</div></div><div class="fig">{circ_svg()}</div></div></div>',
          Q("(8)", "2024の約数のうち、最も大きい素数を求めなさい。",
            W(r"素因数分解する　$2024=2^3\times253=2^3\times11\times23$"), A("23"), 8)]
    return f"""<section class="page">{header("大問2　小問集合", "1")}
<div class="lead">次の問いに答えなさい。</div>
{"".join(q)}
</section>
<section class="page">{header("大問2　小問集合", "2")}
{"".join(q2)}
</section>"""


# ================= 大問3 =================
def d3():
    q = [Q("(1)", r"$a$ の値を求めなさい。", W(r"B$(3,\ 18)$ を代入　$18=a\times3^2$　$9a=18$"), A(r"$a=2$", "w20"), 6),
         Q("(2)", r"この放物線において、$x$ の変域が $-1\leqq x\leqq3$ のとき、$y$ の変域を求めなさい。",
           W(r"$x=0$ をふくむので、最小値は $x=0$ のときの0。最大値は $x$ の絶対値が大きい $x=3$ のときの18"), A(r"$0\leqq y\leqq18$", "w30"), 6),
         Q("(3)", "2点A、Bを通る直線と $x$ 軸との交点をCとする。△OACと△OABの面積比を求めなさい。",
           W(r"A$(-1,\ 2)$。直線ABの傾きは $\dfrac{18-2}{3-(-1)}=4$、$y=4x+b$ に A を代入して $b=6$ → $y=4x+6$<br>"
             r"C は $0=4x+6$ より $x=-\dfrac32$。△OAC＝$\dfrac12\times\dfrac32\times2=\dfrac32$<br>"
             r"△OAB＝$\dfrac12\times6\times\{3-(-1)\}=12$（$y$ 軸で2つに分ける）　$\dfrac32:12=3:24$"),
           A("1：8", "w20"), 12),
         Q("(4)", r"$x$ 軸上に点Pをとり、AP＋PBが最小となるときの点Pの座標を求めなさい。",
           W(r"Aを $x$ 軸について対称に移した点を A′$(-1,\ -2)$ とすると AP＝A′P。AP＋PB＝A′P＋PB が最小になるのは A′、P、B が一直線のとき<br>"
             r"直線A′Bの傾きは $\dfrac{18-(-2)}{3-(-1)}=5$、$y=5x+b$ に A′ を代入して $b=3$ → $y=5x+3$。$y=0$ のとき $x=-\dfrac35$"),
           A(r"$\left(-\dfrac35,\ 0\right)$", "w30"), 14)]
    return f"""<section class="page">{header("大問3　関数 y＝ax²")}
<div class="flex"><div class="grow"><div class="lead">右図のような放物線 $y=ax^2$ 上に $x$ 座標が $-1$ である点Aと B$(3,\\ 18)$ がある。次の問いに答えなさい。</div>{q[0]}{q[1]}</div>
<div class="fig">{para_svg()}</div></div>
{q[2]}{q[3]}
</section>"""


# ================= 大問4 =================
def d4():
    talk1 = ('<div style="line-height:1.9;font-size:9.5pt">'
             + dl("志郎", "三角形の各頂点から対辺に垂線を下ろすと、1点で交わるように見えるのだけれども…")
             + dl("尚子", "鋭角三角形で図を描いてみると、確かに見えるわね。じゃあ、確かめてみましょう。点Bから辺ACに垂線BQ、点Cから辺ABに垂線CRを下ろして、BQとCRの交点をH、そして、直線AHと辺BCの交点をPとおいてAP⊥BCとなるか、考えてみましょう。")
             + dl("志郎", "∠BRC＝∠BQCだから " + BX("ア", "円周角の定理の逆") + " から4点B、C、Q、Rは同じ円周上の点だね。ということは " + BX("イ", "円周角の定理") + " から∠CBQ＝∠" + BX("エ", "HRQ") + " がわかるね。")
             + dl("尚子", "∠ARHと∠AQHは90°だから、RとQはAHを " + BX("ウ", "直径") + " とする円周上にあるわよ。")
             + dl("志郎", "ということは、∠" + BX("エ", "HRQ") + "＝∠" + BX("オ", "PAC") + " がいえる。")
             + dl("尚子", "そうなると∠CBQ＋∠BCQ＝90°だから∠" + BX("オ", "PAC") + "＋∠BCQ＝90°となってAP⊥BCがわかるわね。")
             + dl("先生", "2人とも、よく気付きましたね。この点Hは垂心といいます。では、次の問題を考えてみましょう。次のページの図を見て下さい。<br>"
                  "　△DEFは∠EDF＝90°の直角三角形です。四角形DIJEと四角形DFKLは正方形です。DEとJFの交点をM、EKとDFの交点をNとします。DM＝DNとなることを示して下さい。")
             + "</div>")
    talk2 = ('<div style="line-height:1.9;font-size:9.5pt">'
             + dl("志郎", "いまの、垂心と関係あるのですか？") + dl("先生", "さあ、どうでしょう？")
             + dl("尚子", "多分、あるわよ！少しヒント下さい。") + dl("先生", "では、平行四辺形EGFKを作ってみて下さい。")
             + dl("志郎", "EG＝KFだよね。ということは　DG＝" + BX("カ", "IF") + " だね。更にID＝" + BX("キ", "IJ") + " ということは、△DIG≡△" + BX("ク", "IJF") + " はいえるね。")
             + dl("尚子", "じゃあ、IG⊥JFはいえるわよね。ということは、Mは△" + BX("ケ", "IGF") + " の垂心になるんだ。")
             + dl("志郎", "つまり、GFと直線 " + BX("コ", "IM") + " は垂直なんだ。でもGF∥" + BX("サ", "EK") + " だから、" + BX("サ", "EK") + " と直線 " + BX("コ", "IM") + " も垂直なんだ。")
             + dl("尚子", "わかったわ。△IDM≡△EDNとなります。") + "</div>")
    q1 = Q("(1)", "ア 〜 ウ にあてはまる語句を下から選びなさい。<br>" + ch("ピタゴラスの定理", "中点連結の定理", "円周角の定理", "<br>ピタゴラスの定理の逆", "中点連結の定理の逆", "円周角の定理の逆", "<br>中心", "半径", "直径"),
           W("ア：∠BRC＝∠BQC＝90°で、R、Qが直線BCについて同じ側 → 4点は同じ円周上（円周角の定理の逆）<br>"
             "イ：同じ弧CQに対する円周角は等しい（円周角の定理）　ウ：直角をはさむ円周角は直径に対する角（半円の弧に対する円周角は90°）"),
           "ア" + A("円周角の定理の逆", "w30") + "　イ" + A("円周角の定理", "w30") + "　ウ" + A("直径", "w20"), 2)
    q2 = Q("(2)", "エ 〜 サ にあてはまるものを下から選びなさい。<br>" + ch("ABQ　ACR　HRQ　DGF　EGF　IGF", "<br>IJF　JEF　LEK　PAC　EK　EL", "<br>IF　IJ　IM　JF"),
           W("エ：∠CBQ と同じ弧CQに対する円周角は∠CRQ（＝∠HRQ、HはCR上）　オ：AHを直径とする円で、弧HQに対する円周角 ∠HRQ＝∠HAQ＝∠PAC<br>"
             "カ：EG＝KF＝DF で、GはDEの延長上なので DG＝DE＋DF。I、D、Fは一直線で IF＝ID＋DF＝DE＋DF<br>"
             "キ・ク：ID＝IJ（正方形の辺）、DG＝IF、∠IDG＝∠JIF＝90° → △DIG≡△IJF（2組の辺とその間の角）<br>"
             "ケ：GD⊥IF、FJ⊥IG なので、2本の垂線の交点Mは△IGFの垂心　コ：垂心を通る3本目の垂線 IM⊥GF　サ：平行四辺形EGFKで GF∥EK"),
           "エ" + A("HRQ", "w20") + " オ" + A("PAC", "w20") + " カ" + A("IF", "w20") + " キ" + A("IJ", "w20") + "<br>ク" + A("IJF", "w20") + " ケ" + A("IGF", "w20") + " コ" + A("IM", "w20") + " サ" + A("EK", "w20"), 4)
    q3 = Q("(3)", "IG⊥JFとなることを簡単に説明しなさい。",
           lines(r"△DIGと△IJFで、DI＝IJ（正方形の辺）、DG＝DE＋EG＝DE＋DF＝IF、∠IDG＝∠JIF＝90°<br>"
                 r"2組の辺とその間の角がそれぞれ等しいので　△DIG≡△IJF　よって　∠DIG＝∠IJF<br>"
                 r"IGとJFの交点をXとすると、△IJXで　∠XIJ＋∠IJX＝(90°−∠DIG)＋∠IJF＝90°<br>"
                 r"したがって ∠IXJ＝90° となり、IG⊥JF", 28), "", 0)
    q4 = Q("(4)", "△IDM≡△EDNを示しなさい。",
           lines(r"△IDMと△EDNで、正方形DIJEの辺なので　ID＝ED……①<br>"
                 r"∠IDM＝∠EDN＝90°……②（∠IDE＝90°、∠EDF＝90°）<br>"
                 r"Mは△IGFの垂心なので IM⊥GF、GF∥EK より IM⊥EK。直線IMとEKの交点をTとすると<br>"
                 r"∠DIM＝90°−∠DMI、∠MET＝90°−∠EMT で、∠DMI＝∠EMT（対頂角）なので　∠DIM＝∠DEN……③<br>"
                 r"①、②、③より、1組の辺とその両端の角がそれぞれ等しいから　△IDM≡△EDN（よって DM＝DN）", 34), "", 0)
    return f"""<section class="page">{header("大問4　平面図形", "1")}
<div class="lead">先生、志郎君、尚子さんの会話を読んで(1)〜(4)の各問いに答えなさい。</div>
<div class="flex"><div class="grow">{talk1}</div><div class="fig">{ortho_svg()}</div></div>
</section>
<section class="page">{header("大問4　平面図形", "2")}
<div style="text-align:center">{square_svg()}</div>
{talk2}
{q1}
</section>
<section class="page">{header("大問4　平面図形", "3")}
{q2}{q3}{q4}
</section>"""


# ================= 大問5 =================
def d5():
    q = [Q("(1)", "三角すいOABCの体積を求めなさい。",
           W(r"△OABを底面（直角三角形）、OCを高さとみる　$\dfrac13\times\dfrac12\times4\times4\times3$"), A("8", "w20"), 8),
         Q("(2)", "△ABCの面積を求めなさい。",
           W(r"AB＝$4\sqrt2$（直角二等辺三角形OAB）、AC＝BC＝$\sqrt{4^2+3^2}=5$。△ABCは二等辺三角形<br>"
             r"Cから AB の中点Mへの垂線 CM＝$\sqrt{5^2-(2\sqrt2)^2}=\sqrt{17}$　面積＝$\dfrac12\times4\sqrt2\times\sqrt{17}=2\sqrt{34}$"),
           A(r"$2\sqrt{34}$", "w20"), 12),
         Q("(3)", "点Oから3点A、B、Cを含む平面に下ろした垂線の長さを求めなさい。",
           W(r"△ABCを底面とみると、垂線の長さ $h$ が高さ。体積は8なので　$\dfrac13\times2\sqrt{34}\times h=8$<br>"
             r"$h=\dfrac{12}{\sqrt{34}}=\dfrac{12\sqrt{34}}{34}=\dfrac{6\sqrt{34}}{17}$"),
           A(r"$\dfrac{6\sqrt{34}}{17}$", "w20"), 12),
         Q("(4)", "OAを2：1に分ける点をP、OBを2：1に分ける点をQ、BCを1：2に分ける点をR、ACを1：2に分ける点をSとする。三角すいOABCを、4点P、Q、R、Sを通る平面で切断したとき、点Oを含む立体の体積を求めなさい。",
           W(r"△AOCで AP：AO＝AS：AC＝1：3 なので PS∥OC、PS＝$3\times\dfrac13=1$。同じように QR∥OC、QR＝1。PQ∥AB で、切り口PQRSは長方形<br>"
             r"点Oをふくむ立体を、三角すい C−OPQ と四角すい C−PQRS に分ける<br>"
             r"C−OPQ：$\dfrac13\times\dfrac12\times\dfrac83\times\dfrac83\times3=\dfrac{32}9$<br>"
             r"C−PQRS：底面 PQ×PS＝$\dfrac{8\sqrt2}3\times1$。切り口は OC に平行なので、高さは O から直線PQ までの距離 $\dfrac83\div\sqrt2=\dfrac{4\sqrt2}3$<br>"
             r"$\dfrac13\times\dfrac{8\sqrt2}3\times\dfrac{4\sqrt2}3=\dfrac{64}{27}$　　合計 $\dfrac{32}9+\dfrac{64}{27}=\dfrac{96+64}{27}$"),
           A(r"$\dfrac{160}{27}$", "w20"), 22)]
    return f"""<section class="page">{header("大問5　空間図形")}
<div class="flex"><div class="grow"><div class="lead">三角すいOABCがあります。OA＝OB＝4、OC＝3、∠AOB＝∠BOC＝∠COA＝90°です。次の(1)〜(4)の各問いに答えなさい。</div>{q[0]}{q[1]}</div>
<div class="fig">{tet_svg()}</div></div>
{q[2]}{q[3]}
</section>"""


JOBS = [("c3_shishikan_r6_d1", d1), ("c3_shishikan_r6_d2", d2), ("c3_shishikan_r6_kansu", d3),
        ("c3_shishikan_r6_zukei", d4), ("c3_shishikan_r6_kuukan", d5)]

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
