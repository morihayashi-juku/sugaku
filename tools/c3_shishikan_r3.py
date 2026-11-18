"""尚志館高等学校 入学試験問題（令和3年度 本試験）数学を、大問ごとの PDF にする。
問題（pdf/c3_shishikan_r3_*.pdf）と、問題に赤字で答え・解説を書き込んだ「解答・解説」（_ans.pdf）を同じレイアウトで出す。
サイトでは「尚志館入試過去問」のタブ（common.json の nyushi[] の id＝shishikan）。test の id は shi-r3。

  大問1  計算                          c3_shishikan_r3_d1      → 小問集合（大問1・大問2）
  大問2  小問集合（7問）                c3_shishikan_r3_d2      → 小問集合（大問1・大問2）
  大問3  関数 y＝1/2x²                  c3_shishikan_r3_kansu   → 関数 y＝ax²
  大問4  四角すいの体積（会話文）       c3_shishikan_r3_kuukan  → 空間図形
  大問5  シムソン線（会話文・証明）     c3_shishikan_r3_zukei   → 平面図形

実行：cd tools && python3 c3_shishikan_r3.py
"""
from fractions import Fraction as F
from itertools import combinations
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build, _arc  # noqa: E402
from c3_jitsu3_test import T, L, right_mark  # noqa: E402
from c3_shishikan_r8 import header as _header, svg, dot  # noqa: E402

# ================= 答えの確認 =================
assert 2021 - 3 * 125 == 1646 and F(1, 6) + F(1, 2) == F(2, 3)
for a in range(1, 4):
    for b in range(1, 4):
        assert F(a + b, 2) - F(2 * a - b, 4) == F(3 * b, 4)
        assert F(4 * a * a * b, 6 * a) * (-3 * b) ** 2 == 6 * a * b ** 3
assert 3 - 4 + 2 == 1                                           # 3√3−4√3＋2√3
assert all((x + 2) ** 2 - (x + 5) * (x - 1) == 9 for x in range(-3, 4))
assert 3 * (40 - 15) == 5 * 15
assert F(2 * 6 * 150, 360) == 5 and F(36 * 150, 360) == 15        # 5π、15π
assert 4 - 2 * -4 + 3 * -4 == 0 and (-6) ** 2 + 4 * -6 - 12 == 0
boys = 200
assert -F(9, 100) * boys + F(8, 100) * (850 - boys) == F(4, 100) * 850 and (850 - boys) * F(108, 100) == 702
assert F(sum(a * b % 4 == 0 for a, b in combinations(range(1, 10), 2)), 36) == F(4, 9)
WINS = [15, 14, 12, 14, 12, 13, 14, 14, 15, 13, 15, 14, 14, 13, 15, 14, 11, 14, 14, 13, 14, 13, 15, 13, 13, 15, 12, 14, 12, 14]
sw = sorted(WINS)
assert len(WINS) == 30 and (sw[14] + sw[15]) / 2 == 14 and max(set(WINS), key=WINS.count) == 14 and sum(WINS) / 30 == 13.6
assert F(4 * 6, 4 + 6) == F(12, 5)
ya = lambda x: F(x * x, 2)
assert (ya(6), ya(2)) == (18, 2) and F(18 - 2, 6 - -2) == 2 and 2 - 2 * -2 == 6
for p in (F(1), F(3), F(7)):
    assert F(ya(8) - ya(p), 8 + p) == (8 - p) / 2                # BD の傾き（p→8 で小さくなる）
    assert F(ya(p) - ya(8), p + 8) == (p - 8) / 2                # AC の傾き（p→8 で大きくなる）
p = F(1)
abcd = (4 * p + 2 * p) / 2 * (ya(2 * p) - ya(p))
cpqd = (ya(p) + ya(2 * p)) / 2 * p
assert abcd / cpqd == F(18, 5)
s3, s6 = math.sqrt(3), math.sqrt(6)
Ap = (0, s3, 2 * s6)
for q in [(-3, 0, 0), (3, 0, 0)]:
    assert abs(math.dist(Ap, q) - 6) < 1e-9
assert abs(math.dist(Ap, (-2, s3, 0)) - 2 * math.sqrt(7)) < 1e-9 and 36 + 4 - 12 == 28 and 28 - 4 == 24
assert 27 == 24 + 3                                             # AM²＝AN²＋MN² → AN が高さ
assert abs((6 + 4) / 2 * s3 * 2 * s6 / 3 - 10 * math.sqrt(2)) < 1e-9

TAG = "尚志館　令和3年度　本試験"


def header(title, page=None):
    return _header(title, page).replace("令和8年度", "令和3年度")


def ch(*ws):
    return '<div class="ch" style="border:1px solid #444;display:inline-block;padding:0.6mm 4mm;margin:0.6mm 0 0.6mm 4mm;line-height:1.8">' + "　".join(ws) + "</div>"


def dl(who, t):
    return f'<p class="dl"><b>{who}</b>：{t}</p>'


def u(p, q):
    d = math.dist(p, q)
    return ((q[0] - p[0]) / d, (q[1] - p[1]) / d)


# ================= 図 =================
def para_lines_svg():
    k = 24
    P = lambda x, y: (14 + x * k, 160 - y * k)
    v = (0.22, 0.975)
    B_, D_ = P(0, 0), P(10, 0)
    A_ = (B_[0] + 4 * k * v[0], B_[1] - 4 * k * v[1])
    C_ = (D_[0] + 6 * k * v[0], D_[1] - 6 * k * v[1])
    E_ = (B_[0] + (C_[0] - B_[0]) * 0.4, B_[1] + (C_[1] - B_[1]) * 0.4)
    F_ = (B_[0] + (D_[0] - B_[0]) * 0.4, B_[1])
    s = L(A_, B_) + L(C_, D_) + L(B_, D_) + L(A_, D_) + L(B_, C_) + L(E_, F_)
    s += T(A_[0] - 6, A_[1] - 3, "A") + T(B_[0] - 8, B_[1] + 4, "B") + T(C_[0] + 8, C_[1] - 2, "C") + T(D_[0] + 6, D_[1] + 12, "D") + T(E_[0], E_[1] - 7, "E") + T(F_[0], F_[1] + 13, "F")
    s += T((A_[0] + B_[0]) / 2 - 8, (A_[1] + B_[1]) / 2, "4", "sm") + T((C_[0] + D_[0]) / 2 + 9, (C_[1] + D_[1]) / 2, "6", "sm") + T(E_[0] + 9, (E_[1] + F_[1]) / 2 + 4, '<tspan class="ax">x</tspan>', "sm")
    return svg(int(C_[0]) + 22, 168, s, 0, 6)


def parab_svg():
    k = 26
    ox, oy = 18 + 4.5 * k, 12 + 9 * k
    X = lambda x: ox + x * k
    Y = lambda y: oy - y * k * 0.9
    pp, qq = 1.6, 4.0
    s = L((X(-4.6), Y(0)), (X(4.8), Y(0)), 1) + L((X(0), Y(-0.8)), (X(0), Y(10.2)), 1)
    s += T(X(4.8) + 6, Y(0) + 4, '<tspan class="ax">x</tspan>', "pl") + T(X(0) + 3, Y(10.2) + 2, '<tspan class="ax">y</tspan>', "pl", "start") + T(X(0) - 7, Y(0) + 13, "O", "sm")
    xs = [i / 20 for i in range(-90, 91)]
    s += '<polyline points="' + " ".join(f"{X(x):.1f},{Y(x * x / 2):.1f}" for x in xs if x * x / 2 <= 10.2) + '" fill="none" stroke="#000" stroke-width="1.1"/>'
    for x0, lab in [(pp, "P"), (qq, "Q")]:
        s += L((X(x0), Y(0)), (X(x0), Y(x0 * x0 / 2)), 0.9) + T(X(x0), Y(0) + 13, lab, "sm")
    s += L((X(-pp), Y(pp * pp / 2)), (X(pp), Y(pp * pp / 2)), 0.9) + L((X(-qq), Y(qq * qq / 2)), (X(qq), Y(qq * qq / 2)), 0.9)
    s += T(X(pp) + 2, Y(pp * pp / 2) - 6, "C", "sm") + T(X(-pp) - 8, Y(pp * pp / 2) - 2, "B", "sm") + T(X(qq) + 8, Y(qq * qq / 2) + 2, "D", "sm") + T(X(-qq) - 8, Y(qq * qq / 2) - 2, "A", "sm")
    s += T(X(3.6), Y(10) - 2, '<tspan class="ax">y</tspan>＝½<tspan class="ax">x</tspan>²', "sm")
    return svg(X(4.8) + 16, Y(-0.8) + 4, s)


def pyr_svg():
    S = 22
    P = lambda x, y, z: (120 + x * S - y * S * 0.2, 80 - z * S + y * S * 0.75)
    A_, B_, E_, C_, D_ = P(0, s3, 2 * s6), P(-3, 0, 0), P(3, 0, 0), P(-2, s3, 0), P(2, s3, 0)
    s = L(A_, B_) + L(A_, C_) + L(A_, D_) + L(A_, E_) + L(B_, C_) + L(C_, D_) + L(D_, E_) + L(B_, E_, 0.8, True)
    s += T(A_[0], A_[1] - 4, "A") + T(B_[0] - 8, B_[1] + 4, "B") + T(C_[0], C_[1] + 13, "C") + T(D_[0] + 8, D_[1] + 8, "D") + T(E_[0] + 9, E_[1] + 2, "E")
    M_, N_ = P(0, 0, 0), P(0, s3, 0)
    c = L(M_, N_, 0.9, True, "#c00") + L(A_, M_, 0.9, True, "#c00") + L(A_, N_, 1.0, False, "#c00") + T(M_[0] - 2, M_[1] - 4, "M", "sm") + T(N_[0] + 2, N_[1] + 12, "N", "sm")
    return svg(220, 140, s + f'<g class="cons">{c}</g>', 0, -16)


def abc_svg():
    k = 15
    P = lambda x, y: (14 + x * k, 100 - y * k)
    B_, C_, A_, H_ = P(0, 0), P(2, 0), P(3, 3 * s3), P(3, 0)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="#000" stroke-width="1.1"/>'
    s += L(C_, H_, 0.7, True) + L(A_, H_, 0.7, True) + right_mark(H_, (-1, 0), (0, -1), 4)
    s += _arc(B_, 14, 0, 60) + T(B_[0] + 22, B_[1] - 5, "60°", "sm")
    s += T(A_[0] + 6, A_[1] - 2, "A") + T(B_[0] - 8, B_[1] + 4, "B") + T(C_[0] + 2, C_[1] + 13, "C") + T((A_[0] + B_[0]) / 2 - 8, (A_[1] + B_[1]) / 2, "6", "sm") + T((B_[0] + C_[0]) / 2, B_[1] + 13, "2", "sm")
    c = T(H_[0] + 4, H_[1] + 13, "H", "sm") + T(A_[0] + 10, (A_[1] + H_[1]) / 2, "3√3", "sm", "start") + T((C_[0] + H_[0]) / 2, H_[1] + 13, "1", "sm")
    return svg(110, 116, s + f'<g class="cons">{c}</g>', 0, 4)


def foot(p, a, b):
    d = (b[0] - a[0], b[1] - a[1])
    t = ((p[0] - a[0]) * d[0] + (p[1] - a[1]) * d[1]) / (d[0] ** 2 + d[1] ** 2)
    return (a[0] + t * d[0], a[1] + t * d[1])


def simson_svg():
    k = 66
    O_ = (96, 84)
    P = lambda deg: (O_[0] + k * math.cos(math.radians(deg)), O_[1] - k * math.sin(math.radians(deg)))
    A_, B_, C_, P_ = P(102), P(196), P(338), P(268)
    D_, E_, F_ = foot(P_, A_, B_), foot(P_, B_, C_), foot(P_, A_, C_)
    s = f'<circle cx="{O_[0]}" cy="{O_[1]}" r="{k}" fill="none" stroke="#000" stroke-width="1"/>'
    s += L(A_, B_) + L(B_, D_, 0.9) + L(B_, C_) + L(C_, A_) + L(P_, D_) + L(P_, E_) + L(P_, F_)
    ext = lambda p, q, t: (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    s += L(ext(D_, F_, -0.15), ext(D_, F_, 1.25), 0.8, True)
    s += right_mark(D_, u(D_, A_), u(D_, P_), 5) + right_mark(E_, u(E_, C_), u(E_, P_), 5) + right_mark(F_, u(F_, C_), u(F_, P_), 5)
    s += T(A_[0], A_[1] - 4, "A") + T(B_[0] - 2, B_[1] - 6, "B") + T(C_[0] + 8, C_[1] + 6, "C") + T(P_[0], P_[1] + 13, "P") + T(D_[0] - 9, D_[1] + 4, "D") + T(E_[0], E_[1] - 6, "E") + T(F_[0] + 6, F_[1] - 6, "F")
    c = f'<circle cx="{(B_[0] + P_[0]) / 2:.1f}" cy="{(B_[1] + P_[1]) / 2:.1f}" r="{math.dist(B_, P_) / 2:.1f}" fill="none" stroke="#c00" stroke-dasharray="3 3" stroke-width="0.8"/>'
    c += f'<circle cx="{(C_[0] + P_[0]) / 2:.1f}" cy="{(C_[1] + P_[1]) / 2:.1f}" r="{math.dist(C_, P_) / 2:.1f}" fill="none" stroke="#c00" stroke-dasharray="3 3" stroke-width="0.8"/>'
    x0 = min(D_[0], 20) - 16
    return svg(200 - x0, 166, s + f'<g class="cons">{c}</g>', x0, 6)


def quad_svg():
    k = 62
    O_ = (80, 76)
    P = lambda deg: (O_[0] + k * math.cos(math.radians(deg)), O_[1] - k * math.sin(math.radians(deg)))
    A_, B_, C_, P_ = P(98), P(208), P(345), P(292)
    s = f'<circle cx="{O_[0]}" cy="{O_[1]}" r="{k}" fill="none" stroke="#000" stroke-width="1"/>'
    s += L(A_, B_) + L(B_, P_) + L(P_, C_) + L(C_, A_) + L(O_, A_, 0.9) + L(O_, P_, 0.9) + dot(O_, 1.6)
    s += _arc(O_, 8, 98, 292) + _arc(O_, 11, -68, 98)
    s += T(O_[0] - 18, O_[1] + 4, '<tspan class="ax">x</tspan>', "sm") + T(O_[0] + 18, O_[1] + 2, '<tspan class="ax">y</tspan>', "sm") + T(O_[0] - 2, O_[1] + 18, "O", "sm")
    s += T(A_[0], A_[1] - 4, "A") + T(B_[0] - 8, B_[1] + 4, "B") + T(C_[0] + 8, C_[1] + 4, "C") + T(P_[0] + 4, P_[1] + 13, "P")
    return svg(170, 158, s, 0, 2)


# ================= 大問1 =================
def d1():
    c = [Q("(1)", r"$2021-3\times125$", W(r"かけ算が先　$2021-375$"), A("1646"), 10),
         Q("(2)", r"$\dfrac16+0.5$", W(r"$0.5=\dfrac12=\dfrac36$　$\dfrac16+\dfrac36=\dfrac46$"), A(r"$\dfrac23$"), 10),
         Q("(3)", r"$\dfrac{x+y}2-\dfrac{2x-y}4$", W(r"$\dfrac{2(x+y)-(2x-y)}{4}=\dfrac{2x+2y-2x+y}{4}$"), A(r"$\dfrac{3y}{4}$"), 10),
         Q("(4)", r"$4a^2b\div6a\times(-3b)^2$", W(r"$(-3b)^2=9b^2$　$\dfrac{4a^2b\times9b^2}{6a}=\dfrac{36a^2b^3}{6a}$"), A(r"$6ab^3$"), 10),
         Q("(5)", r"$\sqrt{27}-4\sqrt3+\dfrac6{\sqrt3}$", W(r"$\sqrt{27}=3\sqrt3$、$\dfrac6{\sqrt3}=\dfrac{6\sqrt3}3=2\sqrt3$<br>$3\sqrt3-4\sqrt3+2\sqrt3$"), A(r"$\sqrt3$"), 10),
         Q("(6)", r"$(x+2)^2-(x+5)(x-1)$", W(r"$(x^2+4x+4)-(x^2+4x-5)$<br>$=4+5$"), A("9"), 10)]
    return f"""<section class="page">{header("大問1　計算")}
<div class="lead">次の(1)〜(6)の計算をしなさい。</div>
<div class="grid2">{"".join(c)}</div>
</section>"""


# ================= 大問2 =================
def d2():
    q = [Q("(1)", r"比例式 $3:5=x:(40-x)$ を満たす $x$ の値を求めなさい。",
           W(r"外側の積＝内側の積　$3(40-x)=5x$　$120-3x=5x$　$8x=120$"), A(r"$x=15$"), 8),
         Q("(2)", "半径が6cm、中心角が150°のおうぎ形の弧の長さと面積を求めなさい。",
           W(r"弧の長さ　$2\pi\times6\times\dfrac{150}{360}=5\pi$　　面積　$\pi\times6^2\times\dfrac{150}{360}=15\pi$"),
           "弧の長さ" + A(r"$5\pi$ cm", "w20") + "　面積" + A(r"$15\pi$ cm²", "w20"), 8),
         Q("(3)", r"2次方程式 $x^2-ax+3a=0$ の1つの解が2である。このとき、$a$ の値と他の解を求めなさい。",
           W(r"$x=2$ を代入　$4-2a+3a=0$　$a=-4$<br>もとの式は $x^2+4x-12=0$　$(x+6)(x-2)=0$　$x=-6,\ 2$"),
           r"$a=$" + A("$-4$", "w20") + "　他の解" + A(r"$x=-6$", "w20"), 10),
         Q("(4)", "ある学校の昨年の生徒数は850人であった。今年は、男子生徒が9％減少し、女子生徒が8％増加して全体として生徒数が4％増加したという。今年の女子生徒数を求めなさい。",
           W(r"昨年の男子を $x$ 人、女子を $(850-x)$ 人とする。増えた人数で式をつくる<br>"
             r"$-0.09x+0.08(850-x)=850\times0.04$　$-0.17x+68=34$　$x=200$<br>"
             r"昨年の女子は650人、今年は $650\times1.08=702$（人）"), A("702人"), 14),
         Q("(5)", "1〜9の数字が1つずつ書かれた9枚のカードから2枚とるとき、2枚のカードの数の積が4の倍数である確率を求めなさい。",
           W(r"2枚のとり方は $\dfrac{9\times8}{2}=36$（通り）<br>"
             r"4か8をふくむ：4と他の8枚（8通り）＋8と他の8枚（8通り）−{4,8}の重なり（1通り）＝15通り。4・8以外で積が4の倍数は{2,6}の1通り<br>"
             r"$\dfrac{16}{36}$"), A(r"$\dfrac49$"), 12)]
    rows = [WINS[i:i + 6] for i in range(0, 30, 6)]
    tb = '<table class="tb" style="font-size:9pt;margin:1mm auto">' + "".join("<tr>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>" for r in rows) + "</table>"
    q2 = [Q("(6)", "下の資料は、2015年〜2019年の大相撲幕内力士優勝者の勝ち数である。" + tb
            + "(a) 中央値を求めなさい。　(b) 最頻値を求めなさい。　(c) 平均値を小数第1位まで求めなさい。",
            W(r"度数を数える：11勝1、12勝4、13勝7、14勝12、15勝6（計30）<br>"
              r"(a) 15番目と16番目はどちらも14勝（13勝までで12人、14勝までで24人）　(b) いちばん多いのは14勝（12回）<br>"
              r"(c) $(11\times1+12\times4+13\times7+14\times12+15\times6)\div30=408\div30=13.6$"),
            "(a)" + A("14勝", "w20") + " (b)" + A("14勝", "w20") + " (c)" + A("13.6勝", "w20"), 12),
          '<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(7)</span>右図において AB∥CD∥EF である。<span class="ax">x</span> の値を求めなさい。</div>'
          + W(r"AB∥CD より △EAB∽△EDC で、BE：EC＝AB：DC＝4：6＝2：3<br>"
              r"EF∥CD より △BEF∽△BCD で、EF：CD＝BE：BC＝2：5　$x=6\times\dfrac25=\dfrac{12}5$")
          + f'<div class="al">答　{A(r"$x=\dfrac{12}{5}$")}</div></div><div class="fig">{para_lines_svg()}</div></div></div>']
    return f"""<section class="page">{header("大問2　小問集合", "1")}
<div class="lead">次の(1)〜(7)の各問いに答えなさい。</div>
{"".join(q)}
</section>
<section class="page">{header("大問2　小問集合", "2")}
{"".join(q2)}
</section>"""


# ================= 大問3 =================
def d3():
    q = [Q("(1)", r"$p=2$、$q=6$ のとき、点A、Bの座標を求めなさい。",
           W(r"C$(2,\ 2)$、D$(6,\ 18)$。B、Aは $y$ 軸について C、D と対称な点なので"),
           "A" + A(r"$(-6,\ 18)$", "w20") + "　B" + A(r"$(-2,\ 2)$", "w20"), 8),
         Q("(2)", "(1)のとき、直線BDの式を求めなさい。",
           W(r"B$(-2,\ 2)$、D$(6,\ 18)$　傾き $\dfrac{18-2}{6-(-2)}=2$。$y=2x+b$ に B を代入　$2=-4+b$　$b=6$"),
           A(r"$y=2x+6$", "w30"), 8),
         Q("(3)", r"$q=8$ とする。次の ①、② にあてはまるものを（ア）〜（ウ）から1つ選びなさい。<br>"
           r"点PをQに近づけるとき、直線BDの傾きの値は ①。また、直線ACの傾きの値は ②。<br>（ア）どんどん大きくなる。　（イ）変わらない。　（ウ）どんどん小さくなる。",
           W(r"B$\left(-p,\ \dfrac{p^2}2\right)$、D$(8,\ 32)$ より BDの傾きは $\dfrac{32-\frac{p^2}2}{8+p}=\dfrac{(8-p)(8+p)}{2(8+p)}=\dfrac{8-p}2$ → $p$ が8に近づくと小さくなる<br>"
             r"A$(-8,\ 32)$、C$\left(p,\ \dfrac{p^2}2\right)$ より ACの傾きは $\dfrac{p-8}2$（負の数で、0に近づく）→ 大きくなる"),
           "①" + A("（ウ）", "w20") + "　②" + A("（ア）", "w20"), 10),
         Q("(4)", "OP：OQ＝1：2のとき、四角形ABCDと、四角形CPQDの面積比を求めなさい。",
           W(r"$q=2p$ とすると　A$(-2p,\ 2p^2)$、D$(2p,\ 2p^2)$、B$\left(-p,\ \dfrac{p^2}2\right)$、C$\left(p,\ \dfrac{p^2}2\right)$<br>"
             r"ABCDは台形：AD＝$4p$、BC＝$2p$、高さ $2p^2-\dfrac{p^2}2=\dfrac{3p^2}2$　面積 $\dfrac12\times(4p+2p)\times\dfrac{3p^2}2=\dfrac{9p^3}2$<br>"
             r"CPQDは台形：CP＝$\dfrac{p^2}2$、DQ＝$2p^2$、PQ＝$p$　面積 $\dfrac12\times\left(\dfrac{p^2}2+2p^2\right)\times p=\dfrac{5p^3}4$<br>"
             r"$\dfrac{9p^3}2:\dfrac{5p^3}4=18:5$（$p$ の値に関係なく同じ）"),
           A("18：5", "w20"), 18)]
    return f"""<section class="page">{header("大問3　関数 y＝ax²")}
<div class="flex"><div class="grow"><div class="lead">右の図は、2次関数 $y=\\dfrac12x^2$ ……①のグラフで、$x$ 軸上（$x\\gt0$）に、2点P$(p,\\ 0)$、Q$(q,\\ 0)$ をとっている。ただし、$p\\lt q$ とする。また、P、Qを通り $y$ 軸に平行な直線と①の交点をそれぞれC、Dとし、C、Dを通り $x$ 軸に平行な直線と①の交点のうち、C、Dと異なる方をそれぞれB、Aとする。</div>{q[0]}</div>
<div class="fig">{parab_svg()}</div></div>
{q[1]}{q[2]}{q[3]}
</section>"""


# ================= 大問4 =================
def d4():
    talk = ('<div style="line-height:1.9;font-size:9.5pt">'
            + dl("志郎", "四角すいの体積は、" + BX("ア", r"$\dfrac13$") + "×（底面積）×（高さ）で求められるよね。")
            + dl("尚子", "四角形BCDEに頂点Aから下ろした垂線の長さ（高さ）を求めよう。")
            + dl("志郎", "四角形BCDEは台形で、CD＝" + BX("イ", "4") + " だから、面積は " + BX("ウ", r"$5\sqrt3$") + " だね。")
            + dl("尚子", "あとはこの台形の高さだね……。BEの中点をM、CDの中点をNとおくと、MN＝" + BX("エ", r"$\sqrt3$") + " でしょう。そしてMN⊥BE、MN⊥CD、AN⊥CDだよね。")
            + dl("志郎", "AM＝" + BX("オ", r"$3\sqrt3$") + " だね。ANの長さはいくらだろう。")
            + dl("尚子", "そのためには、ACの長さを求めないと。") + dl("志郎", "△ABCはどんな三角形？")
            + dl("尚子", "△ABCだけかいてみると…。") + dl("志郎", "これならよくわかるね。AC＝" + BX("カ", r"$2\sqrt7$") + " だ。だったら　AN＝" + BX("キ", r"$2\sqrt6$") + " となるよね。")
            + dl("尚子", "AM＝" + BX("オ", r"$3\sqrt3$") + " で、MN＝" + BX("エ", r"$\sqrt3$") + "、AN＝" + BX("キ", r"$2\sqrt6$") + " ということは……。")
            + dl("志郎・尚子", "できた!!　四角すいの体積は " + BX("ク", r"$10\sqrt2$") + " だ！") + "</div>")
    expl = W(r"イ・ウ・エ：台形BCDEで、C、DからBEに垂線をひくと、∠CBE＝60°、BC＝2 なので はしの部分は $2\times\dfrac12=1$、高さは $2\times\dfrac{\sqrt3}2=\sqrt3$<br>"
             r"　CD＝$6-1-1=4$　面積＝$\dfrac12\times(6+4)\times\sqrt3=5\sqrt3$　MN＝台形の高さ＝$\sqrt3$<br>"
             r"オ：AMは1辺6の正三角形ABEの高さ　$6\times\dfrac{\sqrt3}2=3\sqrt3$<br>"
             r"カ：△ABCで、AからBCの延長に垂線AHをひくと BH＝$6\times\dfrac12=3$、AH＝$3\sqrt3$、CH＝$3-2=1$　AC＝$\sqrt{1^2+(3\sqrt3)^2}=\sqrt{28}=2\sqrt7$<br>"
             r"キ：AN⊥CD、CN＝2 なので　AN＝$\sqrt{28-4}=\sqrt{24}=2\sqrt6$<br>"
             r"ク：$\mathrm{AN}^2+\mathrm{MN}^2=24+3=27=\mathrm{AM}^2$ なので ∠ANM＝90°。AN⊥CD でもあるので、ANは底面に垂直で高さになる<br>"
             r"　体積＝$\dfrac13\times5\sqrt3\times2\sqrt6=\dfrac{10\sqrt{18}}3=\dfrac{30\sqrt2}3=10\sqrt2$")
    return f"""<section class="page">{header("大問4　空間図形")}
<div class="flex"><div class="grow"><div class="lead">四角すいA−BCDEについて△ABEは、1辺の長さ6の正三角形です。∠ABC＝∠AED＝∠CBE＝∠DEB＝60°でBC＝DE＝2です。またBE∥CDです。四角すいA−BCDEの体積を考えている志郎君と尚子さんの会話を読んで ア 〜 ク に正しい数値を入れなさい。</div></div>
<div class="fig">{pyr_svg()}</div></div>
<div class="flex"><div class="grow">{talk}</div><div class="fig">{abc_svg()}</div></div>
<div class="q"><div class="qt"><span class="no">解説</span></div>{expl}</div>
</section>"""


# ================= 大問5 =================
def d5():
    box = ('<div class="frame">円に内接する△ABCに、円周上の点Pから直線AB、BC、CAに垂線を引き、その交点をそれぞれD、E、Fとする。<br>'
           'このとき、3点D、E、Fは同一直線上にあることを示しなさい。</div>')
    t1 = ('<div style="line-height:1.85;font-size:9.4pt">'
          + dl("志郎", "確かに図を描いてみると、3点D、E、Fは同一直線上にあるように見えるね。でも、何をいえばいいのかな？")
          + dl("尚子", BX("ア", "対頂角") + " の性質を使えばいいのじゃないのかな？")
          + dl("志郎", "そうか！　∠BED＝∠" + BX("①", "CEF") + " をいえばいいのか。でも、どうやって？")
          + dl("尚子", "直角があるし、円に関係した問題だから、他にも円がかけるのじゃないかな？")
          + dl("志郎", "∠BDP＝∠BEP＝90°だからBPを " + BX("イ", "直径") + " とする円がかけるよね。")
          + dl("尚子", "そうすると " + BX("ウ", "円周角の定理") + " から　∠BED＝∠" + BX("②", "BPD") + " がいえるよね。")
          + dl("志郎", "それならば　∠PEC＝∠PFC　だから " + BX("エ", "円周角の定理の逆") + " から、4点P、E、F、Cは同一円周上にあるね。そうすると " + BX("オ", "円周角の定理") + " から　∠" + BX("①", "CEF") + "＝∠" + BX("③", "CPF") + " がいえるね。")
          + dl("尚子", "ということは、∠" + BX("②", "BPD") + "＝∠" + BX("③", "CPF") + " がいえるといいのだね。")
          + dl("志郎", "確かに!!　でもどうやって？") + dl("尚子", "先生！　もう少し、ヒント下さい。")
          + "</div>")
    t2 = ('<div style="line-height:1.85;font-size:9.4pt">'
          + dl("先生", "わかりました。この図を見て下さい。点Oを中心とする円に内接する四角形ABPCがありますね。")
          + dl("尚子・志郎", "は〜い！") + dl("先生", "円周角と中心角の関係は知っていますね。")
          + dl("志郎", "同じ弧に対する中心角は円周角の " + BX("Ⅰ", "2") + " 倍です。")
          + dl("先生", "そうですね。ということは")
          + dl("尚子", "∠ABP＝" + BX("(a)", r"$\dfrac12y$") + "、∠ACP＝" + BX("(b)", r"$\dfrac12x$") + " です。")
          + dl("先生", "でも <span class='ax'>x</span>＋<span class='ax'>y</span>＝" + BX("Ⅱ", "360") + "°ですよね。")
          + dl("志郎", "ということは　∠ABP＋∠ACP＝" + BX("Ⅲ", "180") + "°だ")
          + dl("尚子", "あっ！　わかったよ！") + dl("先生", "わかりましたね。じゃあ続きを完成させて下さい。")
          + dl("尚子・志郎", "は〜い。") + dl("先生", "このD、E、Fを結ぶ直線を「シムソン線」と呼びます。") + "</div>")
    q1 = Q("(1)", "ア 〜 オ に、次の語句から正しいものを選びなさい。ただし、同じものを選んでもよい。<br>"
           + ch("同位角", "錯角", "対頂角", "半径", "直径", "<br>ピタゴラスの定理", "円周角の定理", "中点連結の定理", "円周角の定理の逆"),
           W("ア：D、E、Fが一直線なら ∠BED と ∠CEF は対頂角で等しい（逆に、等しいことがいえれば一直線）<br>"
             "イ：∠BDP＝∠BEP＝90°なので、D、EはBPを直径とする円の周上　ウ：弧BDに対する円周角 ∠BED＝∠BPD<br>"
             "エ：∠PEC＝∠PFC＝90°で、E、Fが直線PCについて同じ側 → 4点は同一円周上（円周角の定理の逆）　オ：弧CFに対する円周角 ∠CEF＝∠CPF"),
           "ア" + A("対頂角", "w20") + " イ" + A("直径", "w20") + " ウ" + A("円周角の定理", "w30") + "<br>エ" + A("円周角の定理の逆", "w30") + " オ" + A("円周角の定理", "w30"), 2)
    q2 = Q("(2)", "①〜③ に、次の中から正しいものを選びなさい。ただし、同じものを選んでもよい。<br>" + ch("DBE", "DPE", "CEF", "BPD", "BPE", "EFP", "CPF", "ECP"),
           "", "①" + A("CEF", "w20") + "　②" + A("BPD", "w20") + "　③" + A("CPF", "w20"), 2)
    q3 = Q("(3)", "Ⅰ 〜 Ⅲ に正しい数を入れなさい。",
           W("Ⅰ：中心角＝円周角×2　Ⅱ：点Oのまわりの角は360°　Ⅲ：$\\dfrac12y+\\dfrac12x=\\dfrac12\\times360^\\circ=180^\\circ$（円に内接する四角形の向かい合う角の和）"),
           "Ⅰ" + A("2", "w20") + "　Ⅱ" + A("360", "w20") + "　Ⅲ" + A("180", "w20"), 2)
    q4 = Q("(4)", "(a)、(b) に、次の中から正しいものを選びなさい。<br>" + ch(r"$\dfrac12x$", r"$x$", r"$2x$", r"$\dfrac12y$", r"$y$", r"$2y$"),
           W("∠ABPは弧ACP（Bをふくまない方）に対する円周角で、その中心角は $y$。∠ACPは弧ABPに対する円周角で、その中心角は $x$"),
           "(a)" + A(r"$\dfrac12y$", "w20") + "　(b)" + A(r"$\dfrac12x$", "w20"), 4)
    q5 = Q("(5)", "∠ ② ＝∠ ③ を証明しなさい。（∠BPD＝∠CPF）",
           lines(r"(3)より ∠ABP＋∠ACP＝180°。DはABの延長上にあるので ∠PBD＝180°−∠ABP＝∠ACP……①<br>"
                 r"△PBDで ∠PDB＝90° なので　∠BPD＝90°−∠PBD……②<br>"
                 r"△PCFで ∠PFC＝90° なので　∠CPF＝90°−∠PCF＝90°−∠ACP……③（FはAC上なので ∠PCF＝∠ACP）<br>"
                 r"①、②、③より　∠BPD＝∠CPF<br>"
                 r"（したがって ∠BED＝∠BPD＝∠CPF＝∠CEF となり、対頂角が等しいので3点D、E、Fは同一直線上にある）", 40), "", 0)
    return f"""<section class="page">{header("大問5　平面図形", "1")}
<div class="lead">志郎君と尚子さんは、先生に次の問題を宿題としてもらった。</div>
{box}
<div class="flex"><div class="grow">{t1}</div><div class="fig">{simson_svg()}</div></div>
</section>
<section class="page">{header("大問5　平面図形", "2")}
<div class="flex"><div class="grow">{t2}</div><div class="fig">{quad_svg()}</div></div>
{q1}{q2}
</section>
<section class="page">{header("大問5　平面図形", "3")}
{q3}{q4}{q5}
</section>"""


JOBS = [("c3_shishikan_r3_d1", d1), ("c3_shishikan_r3_d2", d2), ("c3_shishikan_r3_kansu", d3),
        ("c3_shishikan_r3_kuukan", d4), ("c3_shishikan_r3_zukei", d5)]

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
