"""尚志館高等学校 入学試験問題（令和5年度 本試験）数学を、大問ごとの PDF にする。
問題（pdf/c3_shishikan_r5_*.pdf）と、問題に赤字で答え・解説を書き込んだ「解答・解説」（_ans.pdf）を同じレイアウトで出す。
サイトでは「尚志館入試過去問」のタブ（common.json の nyushi[] の id＝shishikan）。test の id は shi-r5。

  大問1  計算                          c3_shishikan_r5_d1      → 小問集合（大問1・大問2）
  大問2  小問集合（8問）                c3_shishikan_r5_d2      → 小問集合（大問1・大問2）
  大問3  関数 y＝ax² と正六角形         c3_shishikan_r5_kansu   → 関数 y＝ax²
  大問4  円と相似の証明（会話文）       c3_shishikan_r5_en      → 平面図形（円・相似）
  大問5  三角すいの体積（会話文）       c3_shishikan_r5_kuukan  → 空間図形

実行：cd tools && python3 c3_shishikan_r5.py
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
assert 17 ** 2 * 7 - 124 * 5 == 1403 and F(1, 3) + F(5, 6) - F(1, 2) == F(2, 3)
for a in range(1, 4):
    for b in range(1, 4):
        assert F(2 * a - b, 4) - F(a + b, 2) == F(-3 * b, 4)
        assert F((2 * a) ** 2, -3 * a * a * b ** 4) * 9 * b ** 5 == -12 * b
assert 6 - 4 - 4 == -2                                          # 6√2−4√2−4√2
assert all((x + 4) ** 2 - (x - 2) * (x + 10) == 36 for x in range(-3, 4))
assert len([x for x in range(1, 100) if 25 < x < 36]) == 10
assert 2023 ** 2 - 2022 ** 2 == 4045
assert [n for n in range(1, 101) if n % 9 == 4 and n % 15 == 4] == [4, 49, 94]
assert F(5 * 91, 13) == 35 and 136 // 2 == 68
assert 160 * 24 + 150 * 16 == 156 * 40
dat = [2, 6, 6, 8, 9, 11, 12, 13, 14, 16, 16, 16, 20]
med = lambda v: F(v[len(v) // 2]) if len(v) % 2 else F(v[len(v) // 2 - 1] + v[len(v) // 2], 2)
assert (med(dat[:6]), med(dat), med(dat[7:])) == (7, 12, 16)
hands = list(product(range(3), repeat=3))
assert F(sum(len(set(h)) in (1, 3) for h in hands), len(hands)) == F(1, 3)
s3 = math.sqrt(3)
a3 = F(1, 3)                                                   # 12a＝3a＋3
assert 12 * a3 == 3 * a3 + 3
HEX = {"A": (-s3, 1), "B": (s3, 1), "C": (2 * s3, 4), "D": (s3, 7), "E": (-s3, 7), "F": (-2 * s3, 4)}
assert all(abs(math.dist(HEX[p], HEX[q]) - 2 * s3) < 1e-9 for p, q in ["AB", "BC", "CD", "DE", "EF", "FA"])
assert all(abs(HEX[k][1] - HEX[k][0] ** 2 / 3) < 1e-9 for k in "ABCF")


def shoelace(ps):
    return abs(sum(ps[i][0] * ps[(i + 1) % len(ps)][1] - ps[(i + 1) % len(ps)][0] * ps[i][1] for i in range(len(ps)))) / 2


assert abs(shoelace([HEX[k] for k in "ABCDEF"]) - 18 * s3) < 1e-9
Mx = ((HEX["A"][0] + HEX["F"][0]) / 2, (HEX["A"][1] + HEX["F"][1]) / 2)
assert abs(shoelace([HEX["C"], HEX["B"], HEX["A"], Mx]) - 6 * s3) < 1e-9
slope = (HEX["C"][1] - Mx[1]) / (HEX["C"][0] - Mx[0])
assert abs(slope - s3 / 7) < 1e-12 and abs(HEX["C"][1] - slope * HEX["C"][0] - 22 / 7) < 1e-12
# 大問4：O(0,0) 半径1、PQ は y＝h の弦、A(0,ya)
h4, ya = 0.7, 3.0
P4, Q4, A4 = (-math.sqrt(1 - h4 * h4), h4), (math.sqrt(1 - h4 * h4), h4), (0, ya)
d = (P4[0] - A4[0], P4[1] - A4[1])
tt = [t for t in [(-2 * (A4[0] * d[0] + A4[1] * d[1]) + s * math.sqrt(4 * (A4[0] * d[0] + A4[1] * d[1]) ** 2 - 4 * (d[0] ** 2 + d[1] ** 2) * (A4[0] ** 2 + A4[1] ** 2 - 1))) / (2 * (d[0] ** 2 + d[1] ** 2)) for s in (1, -1)]]
B4 = (A4[0] + max(tt) * d[0], A4[1] + max(tt) * d[1])
ang = lambda p, v, q: math.degrees(math.acos(((p[0] - v[0]) * (q[0] - v[0]) + (p[1] - v[1]) * (q[1] - v[1])) / math.dist(p, v) / math.dist(q, v)))
R4y = Q4[1] + (B4[1] - Q4[1]) * (0 - Q4[0]) / (B4[0] - Q4[0])
R4 = (0, R4y)
assert abs(ang(A4, (0, 0), Q4) - ang(A4, B4, Q4)) < 1e-9          # ∠AOQ＝∠ABQ
assert abs(ang((0, 0), A4, Q4) - ang((0, 0), Q4, R4)) < 1e-9      # ∠OAQ＝∠OQR
# 大問5
assert 6 ** 2 + 8 ** 2 == 10 ** 2 and 6 + 8 == 14 and F(1, 2) * 14 * 6 == 42
R5 = 10 * 6 * math.sqrt(2) * 14 / (4 * 42)
assert abs(R5 - 5 * math.sqrt(2)) < 1e-9 and 225 - 50 == 175 and abs(F(1, 3) * 42 - 14) == 0   # AH＝5√7、体積 14×5√7

TAG = "尚志館　令和5年度　本試験"


def header(title, page=None):
    return _header(title, page).replace("令和8年度", "令和5年度")


def ch(*ws):
    return '<div class="ch" style="border:1px solid #444;display:inline-block;padding:1mm 4mm;margin:1mm 0 1mm 6mm">' + "　　".join(ws) + "</div>"


# ================= 図 =================
def tri_svg():
    k = 92
    O_ = (150, 92)
    P = lambda deg: (O_[0] + k * math.cos(math.radians(deg)), O_[1] - k * math.sin(math.radians(deg)))
    A_, B_, C_ = P(202), P(96), P(-22)
    s = f'<polygon points="{A_[0]:.1f},{A_[1]:.1f} {B_[0]:.1f},{B_[1]:.1f} {C_[0]:.1f},{C_[1]:.1f}" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += L(O_, A_) + L(O_, B_) + L(O_, C_)
    def tick(p, q, n=2):
        m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        ux, uy = (q[0] - p[0]) / math.dist(p, q), (q[1] - p[1]) / math.dist(p, q)
        return "".join(L((m[0] - 4 * uy + (i - 0.5) * 3 * ux, m[1] + 4 * ux + (i - 0.5) * 3 * uy), (m[0] + 4 * uy + (i - 0.5) * 3 * ux, m[1] - 4 * ux + (i - 0.5) * 3 * uy), 0.9) for i in range(n))
    s += tick(O_, A_) + tick(O_, B_) + tick(O_, C_)
    s += _arc(O_, 12, -22, -158) + T(O_[0], O_[1] + 26, "136°", "sm")
    s += T(A_[0] - 8, A_[1] + 6, "A") + T(B_[0], B_[1] - 5, "B") + T(C_[0] + 8, C_[1] + 6, "C")
    c = f'<circle cx="{O_[0]}" cy="{O_[1]}" r="{k}" fill="none" stroke="#c00" stroke-dasharray="3 3" stroke-width="0.9"/>' + T(O_[0] + 10, O_[1] - 4, "O")
    return svg(300, 196, s + f'<g class="cons">{c}</g>')


def hex_svg():
    k = 21
    ox, oy = 112, 196
    P = lambda p: (ox + p[0] * k, oy - p[1] * k)
    s = L((P((-5, 0))[0], oy), (P((5, 0))[0], oy), 1) + L((ox, oy + 12), (ox, oy - 8.8 * k), 1)
    s += T(P((5, 0))[0] + 7, oy + 4, '<tspan class="ax">x</tspan>', "pl") + T(ox + 4, oy - 8.8 * k + 2, '<tspan class="ax">y</tspan>', "pl", "start") + T(ox - 7, oy + 12, "O", "sm")
    xs = [i / 20 for i in range(-104, 105)]
    s += '<polyline points="' + " ".join(f"{P((x, x * x / 3))[0]:.1f},{P((x, x * x / 3))[1]:.1f}" for x in xs if x * x / 3 <= 8.3) + '" fill="none" stroke="#000" stroke-width="1.1"/>'
    s += T(P((4.6, 8))[0], P((4.6, 8))[1], '<tspan class="ax">y</tspan>＝<tspan class="ax">ax</tspan>²', "sm")
    hp = [P(HEX[k_]) for k_ in "ABCDEF"]
    s += '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in hp) + '" fill="none" stroke="#000" stroke-width="1.3"/>'
    s += L(P(HEX["E"]), P(HEX["A"]), 0.7, True) + L(P(HEX["D"]), P(HEX["B"]), 0.7, True)
    off = {"A": (-7, 12), "B": (7, 12), "C": (11, 4), "D": (6, -5), "E": (-6, -5), "F": (-11, 4)}
    s += "".join(T(P(HEX[n])[0] + dx, P(HEX[n])[1] + dy, n) for n, (dx, dy) in off.items())
    c = L(P(HEX["C"]), P((-2.4 * s3, 4 - slope * 4.4 * s3)), 1.2, False, "#c00") + dot(P(Mx), 2.4, "#c00") + T(P(Mx)[0] - 12, P(Mx)[1] + 10, "M") + T(P((-2.3 * s3, 1.0))[0] - 2, P((-2.3 * s3, 1.0))[1], "ℓ")
    c += L(P(HEX["C"]), P(HEX["A"]), 0.8, True, "#c00") + L(P(HEX["C"]), P(HEX["F"]), 0.8, True, "#c00")
    return svg(240, 214, s + f'<g class="cons">{c}</g>')


def circ4_svg():
    k = 60
    P = lambda p: (100 + p[0] * k, 196 - p[1] * k)
    O_, Pp, Qp, Ap, Bp, Rp = P((0, 0)), P(P4), P(Q4), P(A4), P(B4), P(R4)
    s = f'<circle cx="{O_[0]}" cy="{O_[1]}" r="{k}" fill="none" stroke="#000" stroke-width="1"/>'
    s += L(Ap, Bp) + L(Ap, Qp) + L(Pp, Qp) + L(Ap, O_) + L(Bp, Qp) + L(O_, Qp)
    s += right_mark(P((0, h4)), (1, 0), (0, -1), 6)
    s += T(Ap[0], Ap[1] - 5, "A") + T(Pp[0] - 9, Pp[1] + 2, "P") + T(Qp[0] + 9, Qp[1] + 3, "Q") + T(Bp[0] - 8, Bp[1] + 6, "B") + T(O_[0], O_[1] + 14, "O") + T(Rp[0] - 9, Rp[1] - 2, "R")
    oc = (A4[1] / 2)                                                # 4点O・Q・A・Bを通る円：中心は OA の垂直二等分線上
    cx = ((Q4[0] ** 2 + Q4[1] ** 2) - 2 * Q4[1] * oc) / (2 * Q4[0])
    rr = math.hypot(cx, oc)
    C_ = P((cx, oc))
    c = L(O_, Bp, 0.9, False, "#c00") + f'<circle cx="{C_[0]:.1f}" cy="{C_[1]:.1f}" r="{rr * k:.1f}" fill="none" stroke="#c00" stroke-dasharray="3 3" stroke-width="0.9"/>'
    return svg(276, 276, s + f'<g class="cons">{c}</g>', -6, -6)


def tet_svg():
    A_, B_, C_, D_ = (130, 12), (14, 120), (140, 196), (232, 132)
    s = L(A_, B_) + L(A_, C_) + L(A_, D_) + L(B_, C_) + L(C_, D_) + L(B_, D_, 0.8, True)
    s += T(A_[0], A_[1] - 3, "A") + T(B_[0] - 8, B_[1] + 4, "B") + T(C_[0] + 2, C_[1] + 13, "C") + T(D_[0] + 9, D_[1] + 4, "D")
    return svg(250, 214, s, 0, -4)


def bcd_svg():
    k = 13
    P = lambda x, y: (16 + x * k, 104 - y * k)
    B_, D_, E_, C_ = P(0, 0), P(14, 0), P(8, 0), P(8, 6)
    s = f'<polygon points="{B_[0]},{B_[1]} {C_[0]},{C_[1]} {D_[0]},{D_[1]}" fill="none" stroke="#000" stroke-width="1.2"/>' + L(C_, E_) + right_mark(E_, (1, 0), (0, -1), 6)
    s += T(B_[0] - 8, B_[1] + 4, "B") + T(D_[0] + 8, D_[1] + 4, "D") + T(C_[0], C_[1] - 5, "C") + T(E_[0] - 2, E_[1] + 13, "E")
    s += T((B_[0] + C_[0]) / 2 - 10, (B_[1] + C_[1]) / 2 - 6, "10", "sm") + T((C_[0] + D_[0]) / 2 + 12, (C_[1] + D_[1]) / 2 - 6, "6√2", "sm") + T((B_[0] + D_[0]) / 2 - 20, B_[1] + 13, "14", "sm")
    c = T((E_[0] + D_[0]) / 2, E_[1] + 13, "6", "sm") + T((B_[0] + E_[0]) / 2, E_[1] + 13, "8", "sm") + T(C_[0] + 8, (C_[1] + E_[1]) / 2 + 4, "6", "sm")
    return svg(220, 122, s + f'<g class="cons">{c}</g>')


# ================= 大問1 =================
def d1():
    c = [Q("(1)", r"$17^2\times7-124\times5$", W(r"$289\times7-620=2023-620$"), A("1403"), 10),
         Q("(2)", r"$\dfrac13+\dfrac56-\dfrac12$", W(r"分母を6にそろえる　$\dfrac26+\dfrac56-\dfrac36=\dfrac46$"), A(r"$\dfrac23$"), 10),
         Q("(3)", r"$\dfrac{2a-b}4-\dfrac{a+b}2$", W(r"$\dfrac{2a-b-2(a+b)}{4}=\dfrac{2a-b-2a-2b}{4}$<br>（ひく分数はかっこをつけて分配）"), A(r"$-\dfrac{3b}{4}$"), 10),
         Q("(4)", r"$(2a)^2\div(-3a^2b^4)\times9b^5$", W(r"$4a^2\times\left(-\dfrac{1}{3a^2b^4}\right)\times9b^5=-\dfrac{36a^2b^5}{3a^2b^4}$"), A(r"$-12b$"), 10),
         Q("(5)", r"$6\sqrt2-\sqrt{32}-\dfrac8{\sqrt2}$", W(r"$\sqrt{32}=4\sqrt2$、$\dfrac8{\sqrt2}=\dfrac{8\sqrt2}{2}=4\sqrt2$<br>$6\sqrt2-4\sqrt2-4\sqrt2$"), A(r"$-2\sqrt2$"), 10),
         Q("(6)", r"$(x+4)^2-(x-2)(x+10)$", W(r"$(x^2+8x+16)-(x^2+8x-20)$<br>$=16+20$"), A("36"), 10)]
    return f"""<section class="page">{header("大問1　計算")}
<div class="lead">次の(1)〜(6)の計算をしなさい。</div>
<div class="grid2">{"".join(c)}</div>
</section>"""


# ================= 大問2 =================
def d2():
    q = [Q("(1)", r"$5\lt\sqrt x\lt 6$ となるような自然数 $x$ の個数を求めなさい。",
           W(r"それぞれ2乗して　$25\lt x\lt 36$　→　$x=26,\ 27,\ \cdots,\ 35$"), A("10個"), 10),
         Q("(2)", r"$x=2023$、$y=2022$ のとき、$x^2-y^2$ の値を求めなさい。",
           W(r"$x^2-y^2=(x+y)(x-y)=4045\times1$"), A("4045"), 10),
         Q("(3)", "9で割っても15で割っても4余る自然数のうち100以下の自然数の個数を求めなさい。",
           W(r"4をひくと9でも15でも割り切れる → 9と15の最小公倍数45の倍数（0もふくむ）に4を足した数<br>"
             r"$0+4=4$、$45+4=49$、$90+4=94$（4も9・15で割ると商0・余り4）"), A("3個"), 12),
         Q("(4)", r"比例式 $5:13=x:91$ を解きなさい。", W(r"外側の積＝内側の積　$13x=5\times91$　$x=\dfrac{455}{13}$"), A(r"$x=35$"), 10),
         '<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(5)</span>次の図で∠ABCの大きさを求めなさい。（図の同じ印の線分の長さは等しい）</div>'
         + W("図の中の点をOとすると OA＝OB＝OC なので、A・B・Cは Oを中心とする円の周上にある（右の図の赤い円）。<br>"
             r"∠ABCは弧ACに対する円周角、136°は同じ弧に対する中心角なので　$136^\circ\div2$")
         + f'<div class="al">答　{A("68°")}</div></div><div class="fig">{tri_svg()}</div></div></div>']
    q2 = [Q("(6)", "あるクラスで生徒の身長を測ったところ、全生徒40人についての平均が156cm、男子生徒の平均が160cm、女子生徒の平均が150cmであった。このクラスの男子生徒の数は何人か求めなさい。",
            W(r"男子を $x$ 人とすると、女子は $(40-x)$ 人。身長の合計で式をつくる<br>"
              r"$160x+150(40-x)=156\times40$　$10x+6000=6240$　$10x=240$"), A("24人"), 14),
          Q("(7)", "次のデータは2022サッカーワールドカップに出場した欧州13チームの出場回数である。このデータについて次の問いに答えなさい。"
            '<div class="frame" style="display:inline-block;margin:1.5mm 0 1mm 6mm;padding:1mm 4mm">2、6、6、8、9、11、12、13、14、16、16、16、20</div>'
            "<br>1）四分位数を求めなさい。　2）四分位範囲を求めなさい。",
            W(r"13個なので、第2四分位数（中央値）は7番目の12<br>"
              r"第1四分位数は前半6個（2、6、6、8、9、11）の中央値 $\dfrac{6+8}2=7$、第3四分位数は後半6個（13、14、16、16、16、20）の中央値 $\dfrac{16+16}2=16$<br>"
              r"四分位範囲＝第3四分位数−第1四分位数＝$16-7$"),
            "1）第1" + A("7", "w20") + " 第2" + A("12", "w20") + " 第3" + A("16", "w20") + "　2）" + A("9", "w20"), 14),
          Q("(8)", "A、B、C 3人でじゃんけんをするとき、3人があいこになる確率を求めなさい。",
            W(r"手の出し方は全部で $3\times3\times3=27$（通り）<br>"
              r"あいこは、3人とも同じ手（3通り）か、3人の手がすべてちがう（$3\times2\times1=6$ 通り）とき　$\dfrac{3+6}{27}=\dfrac9{27}$"),
            A(r"$\dfrac13$"), 12)]
    return f"""<section class="page">{header("大問2　小問集合", "1")}
<div class="lead">次の(1)〜(8)の各問いに答えなさい。</div>
{"".join(q)}
</section>
<section class="page">{header("大問2　小問集合", "2")}
{"".join(q2)}
</section>"""


# ================= 大問3 =================
def d3():
    q = [Q("(1)", r"$a$ の値を求めなさい。",
           W(r"ABは $x$ 軸に平行なので、A$(-\sqrt3,\ 3a)$、B$(\sqrt3,\ 3a)$。正六角形の1つの内角は120°なので、BからCへは<br>"
             r"右に $2\sqrt3\times\dfrac12=\sqrt3$、上に $2\sqrt3\times\dfrac{\sqrt3}2=3$ 進む → C$(2\sqrt3,\ 3a+3)$<br>"
             r"Cは $y=ax^2$ 上にあるので　$a\times(2\sqrt3)^2=3a+3$　$12a=3a+3$　$9a=3$"),
           A(r"$a=\dfrac13$", "w20"), 12),
         Q("(2)", "点Cの座標を答えなさい。", W(r"$3a+3=3\times\dfrac13+3=4$"), A(r"$(2\sqrt3,\ 4)$", "w20"), 6),
         Q("(3)", "正六角形ABCDEFの面積を求めなさい。",
           W(r"1辺 $2\sqrt3$ の正三角形6つ分。正三角形1つは $\dfrac12\times2\sqrt3\times3=3\sqrt3$（高さは $2\sqrt3\times\dfrac{\sqrt3}2=3$）<br>$3\sqrt3\times6$"),
           A(r"$18\sqrt3$", "w20"), 10),
         Q("(4)", "点Cを通り、正六角形ABCDEFの面積を3等分する直線のうち、傾きが正である直線を ℓ とする。ℓ の方程式を求めなさい。",
           W(r"1つ分の面積は $18\sqrt3\div3=6\sqrt3$。△CBA は $3\sqrt3$（$\dfrac12\times2\sqrt3\times3$）で足りず、△CAF は $6\sqrt3$<br>"
             r"→ ℓ は辺AFと交わり、その点をMとすると △CAM＝$6\sqrt3-3\sqrt3=3\sqrt3$＝$\dfrac12$△CAF なので、MはAFの中点<br>"
             r"A$(-\sqrt3,\ 1)$、F$(-2\sqrt3,\ 4)$ より M$\left(-\dfrac{3\sqrt3}2,\ \dfrac52\right)$。傾きは $\dfrac{4-\frac52}{2\sqrt3+\frac{3\sqrt3}2}=\dfrac{\frac32}{\frac{7\sqrt3}2}=\dfrac{3}{7\sqrt3}=\dfrac{\sqrt3}7$<br>"
             r"C$(2\sqrt3,\ 4)$ を通るので　$4=\dfrac{\sqrt3}7\times2\sqrt3+b$　$b=4-\dfrac67=\dfrac{22}7$"),
           A(r"$y=\dfrac{\sqrt3}{7}x+\dfrac{22}{7}$", "w30"), 22)]
    return f"""<section class="page">{header("大問3　関数 y＝ax²")}
<div class="flex"><div class="grow"><div class="lead">$a>0$ とする。関数 $y=ax^2$ のグラフ上に、AB＝$2\\sqrt3$ となるように、点A、Bをとり、またABを1辺とする正六角形ABCDEFを考える。点C、Fも $y=ax^2$ のグラフ上にあるとき、次の各問いに答えよ。</div>{q[0]}</div>
<div class="fig">{hex_svg()}</div></div>
{q[1]}{q[2]}{q[3]}
</section>"""


# ================= 大問4 =================
def d4():
    k = lambda who, t: f'<p class="dl"><b>{who}</b>「{t}」</p>'
    talk = ('<div style="line-height:1.95;font-size:9.6pt">'
            + k("志郎", "簡単じゃない？だって、∠AOQ＝∠QORはわかっているから、残っている2組のうち、1組が等しいことを示せばいいはず。")
            + k("尚子", "確かにそうだけど…どうやって？") + k("志郎", "う〜む…？")
            + k("尚子", "じゃあ、∠OAQ＝∠OQRがいえないか、考えてみましょうよ。")
            + k("志郎", "PQは円の弦でPQ⊥OAだからOAは線分PQの " + BX("ア", "垂直2等分線") + " だから、AQ＝" + BX("イ", "AP") + " がいえるので∠OAQ＝∠" + BX("ウ", "OAP") + " となるのか。")
            + k("尚子", "ということは∠OQR＝∠" + BX("ウ", "OAP") + " を示せばいいということね。")
            + k("志郎", "だったら、∠OQR＝∠OQBのことだし、∠" + BX("ウ", "OAP") + "＝∠" + BX("エ", "OAB") + " のことだから、4点O、Q、A、Bが同一円周上にあることが言えれば…")
            + k("尚子", "そうなれば、" + BX("オ", "円周角の定理の逆") + " から示せるわ。それに、4点O、Q、A、Bが同一円周上にあれば∠AOQ＝∠" + BX("カ", "ABQ") + " のはずよね。")
            + k("志郎", "うん！わかったよ!!") + "</div>")
    q1 = Q("(1)", "ア に入る最も適当な語を下から選びなさい。<br>" + ch("平行線", "2等分線", "平行2等分線", "垂線", "垂直2等分線"),
           W("OP＝OQ（半径）の二等辺三角形OPQで、頂点Oから底辺PQにひいた垂線は底辺を2等分する"), A("垂直2等分線", "w30"), 2)
    q2 = Q("(2)", "イ 〜 エ、カ に入る最も適当なものを選びなさい。<br>" + ch("AB　AR　AP　AQ　BQ　OA　OAP　OAQ　OAB　OQR", "<br>ORB　APQ　AQP　ARP　ARQ　AOQ　ABQ"),
           W("イ：OAはPQの垂直2等分線なので、OA上の点Aから P・Q までの距離は等しい（AP＝AQ）<br>"
             "ウ：△APQは二等辺三角形で、OAは頂角∠PAQの二等分線　エ：B は直線AP上（Pの先）にあるので ∠OAP＝∠OAB<br>"
             "カ：4点が同一円周上なら、弦AQに対する円周角は等しいので ∠AOQ＝∠ABQ"),
           "イ" + A("AP", "w20") + "　ウ" + A("OAP", "w20") + "　エ" + A("OAB", "w20") + "　カ" + A("ABQ", "w20"), 6)
    q3 = Q("(3)", "オ に入る語を下から選びなさい。<br>" + ch("ピタゴラスの定理", "円周角の定理", "中点連結の定理", "<br>ピタゴラスの定理の逆", "円周角の定理の逆", "中点連結の定理の逆"),
           W("∠AOQ＝∠ABQ（2点O、Bが直線AQについて同じ側）がいえれば、4点O、Q、A、Bは同一円周上にある"), A("円周角の定理の逆", "w30"), 2)
    q4 = Q("(4)", "証明を完成させなさい。（△OAQ∽△OQRであることを示す）",
           lines(r"△OAQと△OQRで、∠AOQ＝∠QOR（共通）……①<br>"
                 r"OAは弦PQの垂直2等分線なので AP＝AQ で、OAは∠PAQを2等分する。Bは直線AP上にあるので　∠OAQ＝∠OAP＝∠OAB……②<br>"
                 r"また、OAは∠POQも2等分するので ∠AOQ＝$\dfrac12$∠POQ。円周角の定理より ∠PBQ＝$\dfrac12$∠POQ なので　∠AOQ＝∠ABQ<br>"
                 r"2点O、Bは直線AQについて同じ側にあるので、円周角の定理の逆より、4点O、Q、A、Bは同一円周上にある。<br>"
                 r"弧OBに対する円周角なので　∠OAB＝∠OQB＝∠OQR……③<br>"
                 r"②、③より ∠OAQ＝∠OQR……④　①、④より、2組の角がそれぞれ等しいから　△OAQ∽△OQR", 52), "", 0)
    return f"""<section class="page">{header("大問4　円と相似", "1")}
<div class="lead">点Oを中心とする円に弦PQをとり、円の外にPQ⊥OAとなるように点Aをとります。直線APと円の交点をB、線分OAと線分BQの交点をRとします。△OAQと△OQRが相似であることを示しなさい。<br>この問題を考えている志郎君と尚子さんの会話を読んで、(1)〜(4)の各問いに答えなさい。</div>
<div class="flex"><div class="grow">{talk}</div><div class="fig">{circ4_svg()}</div></div>
</section>
<section class="page">{header("大問4　円と相似", "2")}
{q1}{q2}{q3}{q4}
</section>"""


# ================= 大問5 =================
def d5():
    k = lambda who, t: f'<p class="dl"><b>{who}</b>「{t}」</p>'
    talk = ('<div style="line-height:1.95;font-size:9.6pt">'
            + k("志郎", "じゃあ、底面積から考えよう。")
            + k("尚子", "△BCDの面積を考えてみましょう。CからBDに垂線CEを下ろしてみると")
            + f'<div style="text-align:center">{bcd_svg()}</div>'
            + k("志郎", "△CEDは直角二等辺三角形に見えるね。")
            + k("尚子", "もし、そうだったら、CE＝DE＝" + BX("ア", "6") + " となり、BE＝" + BX("イ", "8") + " だから△BECで " + BX("ウ", "ピタゴラスの定理") + " が成り立つから、間違いないわ。")
            + k("志郎", "ということは底面となる△BCDの面積は " + BX("エ", "42") + " だ。あとは高さか。Aから△BCDを含む平面に垂線AHを下ろすと。")
            + k("尚子", "△ABH、△ACH、△ADHは合同だわ。")
            + k("志郎", "なるほど。そうなると点Hは3点B、C、Dを通る円の中心ということか。")
            + k("尚子", "じゃあ、∠BHC＝" + BX("オ", "90") + "°となって、BH＝" + BX("カ", r"$5\sqrt2$") + " ということはAH＝" + BX("キ", r"$5\sqrt7$") + "。")
            + k("志郎", "つまり、三角すいABCDの体積は " + BX("ク", r"$70\sqrt7$") + " ということがわかったね。") + "</div>")
    q1 = Q("(1)", "ア 、イ に正しい数値を入れなさい。",
           W(r"直角二等辺三角形CEDの斜辺CD＝$6\sqrt2$ なので　CE＝DE＝$6\sqrt2\div\sqrt2=6$　BE＝$14-6=8$"),
           "ア" + A("6", "w20") + "　イ" + A("8", "w20"), 4)
    q2 = Q("(2)", "ウ に入る正しい語を下から選びなさい。<br>" + ch("ピタゴラスの定理", "円周角の定理", "中点連結の定理"),
           W(r"$\mathrm{BE}^2+\mathrm{CE}^2=8^2+6^2=100=10^2=\mathrm{BC}^2$ なので、△BECは∠E＝90°の直角三角形として矛盾しない"),
           A("ピタゴラスの定理", "w30"), 2)
    q3 = Q("(3)", "エ に正しい数値を入れなさい。", W(r"$\dfrac12\times\mathrm{BD}\times\mathrm{CE}=\dfrac12\times14\times6$"), A("42", "w20"), 4)
    q4 = Q("(4)", "△ABH、△ACH、△ADHが合同であることを説明しなさい。",
           lines("△ABH、△ACH、△ADHで、AHは平面BCDに垂直なので　∠AHB＝∠AHC＝∠AHD＝90°……①<br>"
                 "仮定より　AB＝AC＝AD＝15……②　　AHは共通……③<br>"
                 "①、②、③より、直角三角形の斜辺と他の1辺がそれぞれ等しいから、△ABH≡△ACH≡△ADH", 26), "", 0)
    q5 = Q("(5)", "オ 〜 ク に正しい数値を入れなさい。",
           W(r"オ：合同なので HB＝HC＝HD、Hは△BCDの3つの頂点を通る円の中心。∠BDC＝45°（△CEDは直角二等辺三角形）は弧BCに対する円周角なので、中心角 ∠BHC＝$45^\circ\times2=90^\circ$<br>"
             r"カ：△BHCは HB＝HC の直角二等辺三角形で斜辺BC＝10 なので　BH＝$10\div\sqrt2=5\sqrt2$<br>"
             r"キ：△ABHで三平方の定理　AH＝$\sqrt{15^2-(5\sqrt2)^2}=\sqrt{225-50}=\sqrt{175}=5\sqrt7$<br>"
             r"ク：$\dfrac13\times42\times5\sqrt7=70\sqrt7$"),
           "オ" + A("90", "w20") + "　カ" + A(r"$5\sqrt2$", "w20") + "　キ" + A(r"$5\sqrt7$", "w20") + "　ク" + A(r"$70\sqrt7$", "w20"), 8)
    return f"""<section class="page">{header("大問5　空間図形", "1")}
<div class="lead">AB＝AC＝AD＝15、BC＝10、CD＝$6\\sqrt2$、DB＝14である三角すいABCDの体積を求めなさい。<br>この問題を考えている志郎君と尚子さんの会話を読んで(1)〜(5)の各問いに答えなさい。</div>
<div class="flex"><div class="grow">{talk}</div><div class="fig">{tet_svg()}</div></div>
</section>
<section class="page">{header("大問5　空間図形", "2")}
{q1}{q2}{q3}{q4}{q5}
</section>"""


JOBS = [("c3_shishikan_r5_d1", d1), ("c3_shishikan_r5_d2", d2), ("c3_shishikan_r5_kansu", d3),
        ("c3_shishikan_r5_en", d4), ("c3_shishikan_r5_kuukan", d5)]

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
