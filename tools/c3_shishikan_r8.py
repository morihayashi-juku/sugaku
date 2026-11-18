"""尚志館高等学校 入学試験問題（令和8年度 本試験）数学を、大問ごとの PDF にする。
問題（pdf/c3_shishikan_r8_*.pdf）と、問題に赤字で答え・解説（途中式・考え方）を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
サイトでは「尚志館入試過去問」のタブ（common.json の nyushi[] の id＝shishikan）に入れる。test の id は shi-r8。

  大問1  計算                         c3_shishikan_r8_d1      → 小問集合（大問1・2）
  大問2  小問集合（8問）               c3_shishikan_r8_d2      → 小問集合（大問1・2）
  大問3  関数 y＝ax² と図形            c3_shishikan_r8_kansu   → 関数 y＝ax²
  大問4  円と相似（会話文）            c3_shishikan_r8_en      → 平面図形（円・相似）
  大問5  正四角錐（最短距離・体積）    c3_shishikan_r8_kuukan  → 空間図形

実行：cd tools && python3 c3_shishikan_r8.py
"""
from fractions import Fraction as F
from itertools import combinations
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build  # noqa: E402
from c3_jitsu3_test import T, L, right_mark  # noqa: E402

# ================= 答えの確認 =================
assert 2026 + 2 ** 3 * 126 == 3034 and F(2, 3) - F(1, 6) == F(1, 2)
for a in range(1, 4):
    for b in range(1, 4):
        assert F(a) - F(b, 2) - F(a - 2 * b, 4) == F(3 * a, 4)
        assert F((-2 * a * a * b) ** 3, (-a * b) ** 2) * F(1, 2) * a * b == -4 * a ** 5 * b ** 2
assert 4 + 2 * 2 - 2 == 6                                       # √32＋2√8−4/√2 ＝ 4√2＋4√2−2√2
assert all((x + 2) * (x - 4) - (x - 1) ** 2 == -9 for x in range(-3, 4))
assert all((x + 1) ** 2 - (2 * x + 1) ** 2 == 0 for x in (F(0), F(-2, 3)))
x5 = math.sqrt(5) - 2
assert abs(x5 ** 2 + 4 * x5 + 5 - 6) < 1e-9
assert 400 * 60 // 100 * 5 // 12 == 100
data = [3, 4, 4, 5, 5, 6, 8, 11, 15, 19]
assert sum(data) == 80 and data == sorted(data) and (sorted(data)[7] - sorted(data)[2]) == 7    # a＝8、b＝11
lots = list(combinations(range(6), 2))                          # 0・1 が当たり
assert F(sum(0 in c or 1 in c for c in lots), len(lots)) == F(3, 5)
P_, Q_, D_ = (2, 0), (5, 2), (0, 3)                             # A(0,0) B(5,0) C(5,3) D(0,3)
v1, v2 = (P_[0] - Q_[0], P_[1] - Q_[1]), (D_[0] - Q_[0], D_[1] - Q_[1])
assert abs(math.degrees(math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / math.hypot(*v1) / math.hypot(*v2))) - 45) < 1e-9
assert 830 * F(21 + 11, 40) == 664
assert [6 * p for p in (2, 3, 5, 7, 11, 13)] == [n for n in range(10, 100) if n % 6 == 0 and all((n // 6) % k for k in range(2, n // 6)) and n // 6 > 1]
a3 = F(-2, -3 + 2)                                              # 傾き a(−3＋2)＝−2
assert a3 == 2
Ay, By = 2 * 9, 2 * 4
assert (Ay, By) == (18, 8) and F(1, 2) * 12 * 5 == 30 and F(1, 2) * (12 - 4) * 5 == 20
assert all(2 * x * x == -2 * x + 4 for x in (-2, 1))
pts = [(-3, 18), (-2, 8), (1, 2), (2, 8)]
area = abs(sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1] for i in range(4))) / 2
assert area == 32
cx, cy = (F(-3 + 2, 2) + F(-2 + 1, 2)) / 2, (F(18 + 8, 2) + F(8 + 2, 2)) / 2
assert (cx, cy) == (F(-1, 2), 9) and cy / cx == -18
# 大問4：H(0,0) A(−2√3,0) B(√3,0) C(0,2)
s3 = math.sqrt(3)
Ac, Bc, Cc = (-2 * s3, 0), (s3, 0), (0, 2)
assert abs(math.dist(Ac, Bc) - 3 * s3) < 1e-9 and abs(math.dist(Ac, Cc) - 4) < 1e-9 and abs(math.dist(Bc, Cc) - math.sqrt(7)) < 1e-9
Oc = (-s3 / 2, -0.5)
assert all(abs(math.dist(Oc, p) - math.sqrt(7)) < 1e-9 for p in (Ac, Bc, Cc))
ang = lambda p, v, q: math.degrees(math.acos(((p[0] - v[0]) * (q[0] - v[0]) + (p[1] - v[1]) * (q[1] - v[1])) / math.dist(p, v) / math.dist(q, v)))
beta = ang(Ac, Bc, Cc)
assert abs(ang(Cc, Ac, Bc) - 30) < 1e-9


def on_ab(deg_from_cb):
    lo, hi = Ac[0], Bc[0]
    for _ in range(200):
        m = (lo + hi) / 2
        if ang((m, 0), Cc, Bc) > deg_from_cb:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


Dx = on_ab(30 + beta)                                           # ∠BCD ＝ ∠ACB の外角 ＝ ∠A＋∠B
Ex = on_ab(30 + beta + (ang(Ac, Cc, (Dx, 0))) / 2)
assert abs(ang((Ex, 0), Cc, Bc) - 90) < 1e-6 and abs(math.dist((Ex, 0), Cc) - 2 * math.sqrt(21) / 3) < 1e-6
assert Ac[0] < Ex < Dx < Bc[0]
# 大問5
assert abs(F(3, 1) / 4 - F(3, 4)) == 0                          # OQ：QB＝OP：AB＝3：4
h5 = 2 * math.sqrt(2)
assert abs(math.sqrt(16 - 8) - h5) < 1e-12
assert abs(F(1, 3) * 16 * F(4, 7) * h5 - 128 * math.sqrt(2) / 21) < 1e-9
Qx, Qy = F(3, 7) * 2, 2 - F(6, 7)                              # R(0,0) B(2√2,0) O(0,2√2) を √2 でわったもの
assert abs(math.sqrt(2) * math.hypot(Qx, Qy) - 10 * math.sqrt(2) / 7) < 1e-12

TAG = "尚志館　令和8年度　本試験"


def header(title, page=None):
    p = f"（{page}）" if page else ""
    return (f'<div class="hd"><div class="ht"><span class="tag">{TAG}</span>{title}{p}<span class="key">解答・解説</span></div>'
            '<div class="nm">　月　　日　名前（　　　　　　　　　）</div></div>')


def svg(w, h, s, x0=0, y0=0):
    return f'<svg width="{w}" height="{h}" viewBox="{x0} {y0} {w} {h}">{s}</svg>'


def dot(p, r=2.3, col="#000"):
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{col}"/>'


# ================= 図 =================
def rect_svg():
    """大問2(6)：こたえだけに出す図（長方形と合同な直角三角形）"""
    k = 26
    P = lambda x, y: (14 + x * k, 12 + (3 - y) * k)
    A_, B_, C_, D_ = P(0, 0), P(5, 0), P(5, 3), P(0, 3)
    Pp, Qp = P(2, 0), P(5, 2)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]} {D_[0]},{D_[1]}" fill="none" stroke="#000" stroke-width="1"/>'
    s += L(Pp, Qp) + L(Qp, D_) + L(D_, Pp)
    s += T(A_[0] - 6, A_[1] + 12, "A", "sm") + T(B_[0] + 6, B_[1] + 12, "B", "sm") + T(C_[0] + 7, C_[1] - 2, "C", "sm") + T(D_[0] - 6, D_[1] - 2, "D", "sm")
    s += T(Pp[0], Pp[1] + 12, "P", "sm") + T(Qp[0] + 8, Qp[1] + 4, "Q", "sm")
    s += T((A_[0] + Pp[0]) / 2, A_[1] + 12, "2", "sm") + T((Pp[0] + B_[0]) / 2, B_[1] + 12, "3", "sm") + T(B_[0] + 7, (B_[1] + Qp[1]) / 2 + 4, "2", "sm") + T(D_[0] - 7, (A_[1] + D_[1]) / 2 + 4, "3", "sm")
    s += right_mark(Pp, ((D_[0] - Pp[0]) / math.dist(D_, Pp), (D_[1] - Pp[1]) / math.dist(D_, Pp)), ((Qp[0] - Pp[0]) / math.dist(Qp, Pp), (Qp[1] - Pp[1]) / math.dist(Qp, Pp)), 7)
    return svg(170, 106, f'<g class="cons">{s}</g>')


def para_svg():
    sx, sy = 26, 7.4
    ox, oy = 16 + 3.6 * sx, 10 + 19.5 * sy
    X = lambda x: ox + x * sx
    Y = lambda y: oy - y * sy
    s = L((X(-3.6), Y(0)), (X(3.2), Y(0)), 1) + L((X(0), Y(-0.8)), (X(0), Y(20)), 1)
    s += T(X(3.2) + 7, Y(0) + 4, '<tspan class="ax">x</tspan>', "pl") + T(X(0) + 3, Y(20) + 2, '<tspan class="ax">y</tspan>', "pl", "start")
    s += T(X(0) - 6, Y(0) + 12, "O", "sm") + T(X(-3), Y(0) + 13, "−3", "sm") + T(X(2), Y(0) + 13, "2", "sm")
    xs = [i / 20 for i in range(-62, 58)]
    s += '<polyline points="' + " ".join(f"{X(x):.1f},{Y(2 * x * x):.1f}" for x in xs if 2 * x * x <= 20) + '" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += L((X(-3.6), Y(19.2)), (X(3), Y(-2 * 3 + 12)), 1.1)
    s += L((X(-3), Y(18)), (X(-3), Y(0)), 0.7, True) + L((X(2), Y(8)), (X(2), Y(0)), 0.7, True)
    s += L((X(0), Y(0)), (X(-3), Y(18)), 0.9) + L((X(0), Y(0)), (X(2), Y(8)), 0.9)
    s += dot((X(-3), Y(18))) + dot((X(2), Y(8))) + T(X(-3) - 9, Y(18) + 2, "A") + T(X(2) + 9, Y(8) - 2, "B")
    c = L((X(-2), Y(8)), (X(1), Y(2)), 1.1, False, "#c00") + L((X(-2), Y(8)), (X(-3), Y(18)), 0.9, True, "#c00") + L((X(1), Y(2)), (X(2), Y(8)), 0.9, True, "#c00")
    c += L((X(0), Y(0)), (X(-0.75), Y(13.5)), 1.1, False, "#c00") + dot((X(-0.5), Y(9)), 2.4, "#c00")
    c += dot((X(-2), Y(8)), 2.4, "#c00") + dot((X(1), Y(2)), 2.4, "#c00")
    c += T(X(-2) - 12, Y(8) + 3, "P′") + T(X(1) + 12, Y(2) + 2, "P″")
    return svg(X(3.2) + 18, Y(-0.8) + 6, s + f'<g class="cons">{c}</g>')


def circle_svg():
    k = 46
    P = lambda p: (180 + p[0] * k, 130 - p[1] * k)
    R = math.sqrt(7) * k
    O_, A_, B_, C_, D_, E_, H_ = P(Oc), P(Ac), P(Bc), P(Cc), P((Dx, 0)), P((Ex, 0)), P((0, 0))
    s = f'<circle cx="{O_[0]:.1f}" cy="{O_[1]:.1f}" r="{R:.1f}" fill="none" stroke="#000" stroke-width="1"/>'
    s += L(A_, B_) + L(A_, C_) + L(B_, C_) + L(C_, D_) + L(C_, E_) + L(O_, B_)
    s += dot(O_, 1.8) + dot(D_, 1.8) + dot(E_, 1.8)
    s += T(A_[0] - 9, A_[1] + 2, "A") + T(B_[0] + 9, B_[1] + 4, "B") + T(C_[0] + 4, C_[1] - 6, "C") + T(O_[0], O_[1] + 14, "O")
    s += T(D_[0] + 1, D_[1] + 14, "D") + T(E_[0] - 2, E_[1] + 14, "E")
    c = L(C_, H_, 0.9, True, "#c00") + right_mark(H_, (1, 0), (0, -1), 6) + T(H_[0] + 7, H_[1] + 13, "H")
    c += L(O_, C_, 0.8, True, "#c00")
    return svg(316, 282, s + f'<g class="cons">{c}</g>')


def pyr_svg():
    s2, S = math.sqrt(2), 30
    P = lambda x, y, z: (110 + x * S, 112 - z * S - y * S * 0.45)
    V = lambda deg: P(2 * s2 * math.cos(math.radians(deg)), 2 * s2 * math.sin(math.radians(deg)), 0)
    O_, A_, B_, C_, D_ = P(0, 0, 2 * s2), V(200), V(290), V(20), V(110)
    R_ = P(0, 0, 0)
    Pp = (O_[0] + (C_[0] - O_[0]) * 0.75, O_[1] + (C_[1] - O_[1]) * 0.75)
    Qp = (O_[0] + (B_[0] - O_[0]) * 3 / 7, O_[1] + (B_[1] - O_[1]) * 3 / 7)
    s = "".join(L(p, q, 1.2) for p, q in [(O_, A_), (O_, B_), (O_, C_), (A_, B_), (B_, C_)])
    s += "".join(L(p, q, 0.8, True) for p, q in [(O_, D_), (A_, D_), (D_, C_), (A_, C_), (B_, D_)])
    s += L(A_, Qp, 0.9) + L(Qp, Pp, 0.9) + dot(Qp, 1.8) + dot(Pp, 1.8) + dot(R_, 1.6)
    s += T(O_[0], O_[1] - 5, "O") + T(A_[0] - 9, A_[1] + 4, "A") + T(B_[0] + 2, B_[1] + 13, "B") + T(C_[0] + 9, C_[1] + 4, "C") + T(D_[0] + 9, D_[1] - 4, "D")
    s += T(Qp[0] + 9, Qp[1] + 1, "Q", "sm") + T(Pp[0] + 8, Pp[1] - 3, "P", "sm") + T(R_[0] - 2, R_[1] + 12, "R", "sm")
    s += T((A_[0] + B_[0]) / 2 - 8, (A_[1] + B_[1]) / 2 + 13, "4cm", "sm") + T((O_[0] + A_[0]) / 2 - 22, (O_[1] + A_[1]) / 2 - 2, "4cm", "sm")
    s += T((Pp[0] + C_[0]) / 2 + 13, (Pp[1] + C_[1]) / 2 - 2, "1cm", "sm")
    c = L(O_, R_, 0.9, True, "#c00") + L(Qp, R_, 1.1, False, "#c00")
    return svg(232, 160, s + f'<g class="cons">{c}</g>')


def net_svg():
    """大問5(2)の考え方（こたえだけ）：面OABと面OBCを開いた図。ひし形OABC′の中で AP と OB の交点が Q"""
    # 正三角形 OAB・OBC（1辺4）：O(0,0) B(0,4) A(−2√3,2) C(2√3,2) を縦長に
    sc = 26
    Pt = lambda x, y: (110 + x * sc, 12 + y * sc)
    O_, B_, A_, C_ = Pt(0, 0), Pt(0, 4), Pt(-2 * math.sqrt(3), 2), Pt(2 * math.sqrt(3), 2)
    Pp = (O_[0] + (C_[0] - O_[0]) * 0.75, O_[1] + (C_[1] - O_[1]) * 0.75)
    Qp = (O_[0] + (B_[0] - O_[0]) * 3 / 7, O_[1] + (B_[1] - O_[1]) * 3 / 7)
    c = f'<polygon points="{O_[0]},{O_[1]} {A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="#c00" stroke-width="1"/>' + L(O_, B_, 1, False, "#c00")
    c += L(A_, Pp, 1.2, False, "#c00") + dot(Pp, 2, "#c00") + dot(Qp, 2, "#c00")
    c += T(O_[0], O_[1] - 3, "O", "sm") + T(A_[0] - 8, A_[1] + 4, "A", "sm") + T(B_[0], B_[1] + 12, "B", "sm") + T(C_[0] + 8, C_[1] + 4, "C", "sm")
    c += T(Pp[0] + 8, Pp[1] - 2, "P", "sm") + T(Qp[0] + 9, Qp[1] + 4, "Q", "sm") + T((O_[0] + Pp[0]) / 2 + 9, (O_[1] + Pp[1]) / 2 - 2, "3", "sm")
    c += T(110, B_[1] + 26, "面OAB・面OBCの展開図", "sm")
    return svg(220, B_[1] + 32, f'<g class="cons">{c}</g>')


# ================= 大問1 =================
def d1():
    c = [Q("(1)", r"$2026+2^3\times126$", W(r"$2026+8\times126=2026+1008$<br>（累乗 → かけ算 → たし算の順）"), A("3034"), 10),
         Q("(2)", r"$\dfrac23-\dfrac16$", W(r"通分して　$\dfrac46-\dfrac16=\dfrac36$　約分する"), A(r"$\dfrac12$"), 10),
         Q("(3)", r"$a-\dfrac b2-\dfrac{a-2b}4$", W(r"分母を4にそろえる<br>$\dfrac{4a-2b-(a-2b)}{4}=\dfrac{4a-2b-a+2b}{4}$<br>（ひく分数の分子はかっこをつけて符号に注意）"), A(r"$\dfrac{3a}{4}$"), 10),
         Q("(4)", r"$(-2a^2b)^3\div(-ab)^2\times\dfrac12ab$",
           W(r"$(-2a^2b)^3=-8a^6b^3$、$(-ab)^2=a^2b^2$<br>$-8a^6b^3\times\dfrac{1}{a^2b^2}\times\dfrac{ab}{2}=-\dfrac{8a^7b^4}{2a^2b^2}$"), A(r"$-4a^5b^2$"), 10),
         Q("(5)", r"$\sqrt{32}+2\sqrt8-\dfrac4{\sqrt2}$",
           W(r"$\sqrt{32}=4\sqrt2$、$2\sqrt8=4\sqrt2$、$\dfrac4{\sqrt2}=\dfrac{4\sqrt2}{2}=2\sqrt2$<br>$4\sqrt2+4\sqrt2-2\sqrt2$"), A(r"$6\sqrt2$"), 10),
         Q("(6)", r"$(x+2)(x-4)-(x-1)^2$",
           W(r"$(x^2-2x-8)-(x^2-2x+1)$<br>$=x^2-2x-8-x^2+2x-1$"), A("$-9$"), 10)]
    return f"""<section class="page">{header("大問1　計算")}
<div class="lead">次の(1)〜(6)の計算をしなさい。</div>
<div class="grid2">{"".join(c)}</div>
</section>"""


# ================= 大問2 =================
def d2():
    q = [Q("(1)", r"2次方程式 $(x+1)^2-(2x+1)^2=0$ を解きなさい。",
           W(r"$A^2-B^2=(A-B)(A+B)$ を使う<br>$\{(x+1)-(2x+1)\}\{(x+1)+(2x+1)\}=0$<br>$-x(3x+2)=0$"), A(r"$x=0,\ -\dfrac23$"), 12),
         Q("(2)", r"$x=\sqrt5-2$ のとき、$x^2+4x+5$ の値を求めなさい。",
           W(r"$x^2+4x+5=(x+2)^2+1$ と変形する。$x+2=\sqrt5$ なので<br>$(\sqrt5)^2+1=5+1$"), A("6"), 12),
         Q("(3)", "ある中学校の2年生と3年生の人数の比は、5：7で、1年生の人数は、全校生徒数の40％である。全校生徒数が400人のとき、2年生の人数を求めなさい。",
           W(r"1年生は $400\times0.4=160$（人）、2・3年生は $400-160=240$（人）<br>2年生は $240\times\dfrac{5}{5+7}=240\times\dfrac5{12}$"), A("100人"), 12),
         Q("(4)", r"次の10個のデータは、左から小さい順に並んでいる。平均値が8、四分位範囲が7のとき、$a$、$b$ の値をそれぞれ求めなさい。<br>　3、4、4、5、5、6、$a$、$b$、15、19",
           W(r"合計は $8\times10=80$ なので　$a+b=80-61=19$<br>"
             r"第1四分位数は前半5個（3、4、4、5、5）の中央値で4、第3四分位数は後半5個（6、$a$、$b$、15、19）の中央値で $b$<br>"
             r"四分位範囲 $b-4=7$ より $b=11$、$a=19-11=8$（6≦8≦11≦15 で小さい順になっている）"), A(r"$a=8,\ b=11$"), 16)]
    q2 = [Q("(5)", "当たりくじを2本含む6本のくじの中から、同時に2本のくじを引くとき、少なくとも1本は当たりくじを引く確率を求めなさい。ただし、どのくじを引くことも同様に確からしいものとする。",
            W(r"当たりを①②、はずれを③④⑤⑥とする。2本の引き方は全部で15通り<br>"
              r"2本ともはずれ：{③④}{③⑤}{③⑥}{④⑤}{④⑥}{⑤⑥} の6通り<br>"
              r"「少なくとも1本は当たり」＝ 1−（2本ともはずれ）　$1-\dfrac6{15}=\dfrac9{15}$"), A(r"$\dfrac35$"), 14),
          '<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(6)</span>AB＝5、AD＝3である長方形ABCDにおいて、辺AB上にAP＝2、辺BC上にBQ＝2を満たす、点P、Qをとる。このとき、∠PQDの大きさを求めなさい。</div>'
          + W(r"△DAPと△PBQで、DA＝PB＝3、AP＝BQ＝2、∠DAP＝∠PBQ＝90°なので △DAP≡△PBQ（2組の辺とその間の角）<br>"
              r"よって DP＝PQ、∠ADP＝∠BPQ。∠APD＋∠BPQ＝∠APD＋∠ADP＝90° なので ∠DPQ＝90°<br>"
              r"△DPQは直角二等辺三角形だから　∠PQD＝45°")
          + f'<div class="al">答　{A("45°")}</div></div><div class="fig">{rect_svg()}</div></div></div>',
          Q("(7)", "志布志市の中学生830人の中から無作為に抽出した40人に対してアンケートを行ったところ、運動部への加入者は21人、文化部への加入者は11人だった。志布志市の中学生の全体の部活動加入者（運動部と文化部をあわせた）は約何人と推定できるか。",
            W(r"標本40人のうち加入者は $21+11=32$（人）で、割合は $\dfrac{32}{40}=\dfrac45$<br>母集団でも同じ割合と考えて　$830\times\dfrac45$"), A("約664人"), 12),
          Q("(8)", r"$n$ を2桁の自然数とするとき、$\dfrac n6$ が素数となるような $n$ の個数を求めなさい。",
            W(r"$\dfrac n6=p$（素数）とすると $n=6p$。$10\leqq6p\leqq99$ より $2\leqq p\leqq16$<br>"
              r"この範囲の素数は 2、3、5、7、11、13 → $n=$12、18、30、42、66、78"), A("6個"), 12)]
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
           W(r"A$(-3,\ 9a)$、B$(2,\ 4a)$。傾きは $\dfrac{4a-9a}{2-(-3)}=\dfrac{-5a}{5}=-a$<br>$-a=-2$ より"), A(r"$a=2$", "w20"), 10),
         Q("(2)", "△OABの面積を求めなさい。",
           W(r"A$(-3,\ 18)$、B$(2,\ 8)$。直線ABは $y=-2x+b$ に B を代入して $8=-4+b$、$b=12$ → $y=-2x+12$<br>"
             r"$y$ 軸との交点を C$(0,\ 12)$ とすると　△OAB＝△OAC＋△OBC＝$\dfrac12\times12\times3+\dfrac12\times12\times2=18+12$"),
           A("30", "w20"), 12),
         Q("(3)", r"①のグラフ上の2点A、Bの間に点Pをとる。$\triangle\mathrm{PAB}=\dfrac23\triangle\mathrm{OAB}$ となる点Pは2つ存在する。このときの $x$ 座標の小さい方をP′、大きい方をP″とする。P′、P″の座標をそれぞれ求めなさい。",
           W(r"$\triangle\mathrm{PAB}=30\times\dfrac23=20$。Pを通りABに平行な直線を $y=-2x+k$ とすると、△PAB＝$\dfrac12\times(12-k)\times\{2-(-3)\}=20$ より $k=4$<br>"
             r"（平行線を使った等積変形：Pを直線上で動かしても△PABの面積は変わらない）<br>"
             r"$2x^2=-2x+4$　$x^2+x-2=0$　$(x+2)(x-1)=0$　$x=-2,\ 1$"),
           "P′" + A(r"$(-2,\ 8)$", "w20") + "　P″" + A(r"$(1,\ 2)$", "w20"), 18),
         Q("(4)", "(3)のとき、四角形AP′P″Bの面積を原点を通る直線で2等分する。この直線の傾きを求めなさい。",
           W(r"P′P″の傾きは $\dfrac{2-8}{1-(-2)}=-2$ で AB∥P′P″ なので、四角形AP′P″Bは台形<br>"
             r"台形は、平行な2辺の中点を結んだ線分の中点 M を通り、平行な2辺と交わる直線で2等分される<br>"
             r"ABの中点 $\left(-\dfrac12,\ 13\right)$、P′P″の中点 $\left(-\dfrac12,\ 5\right)$ → M$\left(-\dfrac12,\ 9\right)$<br>"
             r"原点とMを通る直線の傾きは　$9\div\left(-\dfrac12\right)=-18$（$y=-18x$ はABと $x=-\dfrac34$、P′P″と $x=-\dfrac14$ で交わる）"),
           A("$-18$", "w20"), 22)]
    return f"""<section class="page">{header("大問3　関数 y＝ax²")}
<div class="flex"><div class="grow"><div class="lead">図のように、関数 $y=ax^2$ ……①のグラフ上に2点A、Bがあり、それぞれの $x$ 座標は $-3$、2である。また、2点を通る直線の傾きは $-2$ である。次の(1)〜(4)の各問いに答えなさい。</div>{q[0]}{q[1]}</div>
<div class="fig">{para_svg()}</div></div>
{q[2]}{q[3]}
</section>"""


# ================= 大問4 =================
def d4():
    k = lambda who, t: f'<p class="dl"><b>{who}</b>「{t}」</p>'
    talk = ('<div class="frame" style="line-height:2">'
            + k("志郎", "どこから手を着ければいいのかなあ")
            + k("尚子", "まず、わかるところから、求めていきましょう。たとえば、円の半径とか。")
            + k("志郎", "それって、OBだよね。まあ、BCでもいいけど。△OBCって " + BX("(ア)", "正三角形") + " だよね。")
            + k("尚子", "ということは、∠CAB＝" + BX("(イ)", "30") + "°だよ。だから、CからABに垂線CHを下ろすと")
            + k("志郎", "CHの長さは " + BX("(ウ)", "2") + " だね。ということは半径は " + BX("(エ)", r"$\sqrt7$") + " だ。")
            + k("尚子", "あと、∠BCDが∠ACBの外角と等しくて、CEが∠ACDの二等分線だから…")
            + k("志郎", "∠ECB＝" + BX("(オ)", "90") + "°だ。ということは、△EBCと△" + BX("(カ)", "CBH") + " は相似か。")
            + k("尚子", "だったら、解けたわね。") + "</div>")
    q1 = Q("(1)", "(ア)に入る語句を、次の中から選びなさい。<div class=\"ch\">［　直角三角形　　正三角形　　直角二等辺三角形　］</div>",
           W("OB・OCは半径なので OB＝OC。これと OB＝BC から OB＝OC＝BC"), A("正三角形", "w30"), 4)
    q2 = Q("(2)", "(イ)〜(オ)に入る数値を答えなさい。",
           W(r"(イ)　∠BOC＝60°（正三角形）。∠CABは弧BCに対する円周角なので　$60^\circ\div2=30^\circ$<br>"
             r"(ウ)　△ACHは30°・60°・90°の直角三角形で AC＝4 なので　CH＝$4\times\dfrac12=2$、AH＝$2\sqrt3$<br>"
             r"(エ)　HB＝$3\sqrt3-2\sqrt3=\sqrt3$。△CHBで三平方の定理より　BC＝$\sqrt{2^2+(\sqrt3)^2}=\sqrt7$。半径＝BC＝$\sqrt7$<br>"
             r"(オ)　∠CAB＝$a$、∠ABC＝$b$ とすると ∠ACBの外角は $a+b$ なので ∠BCD＝$a+b$。∠ACD＝∠ACB−∠BCD＝$(180^\circ-a-b)-(a+b)$<br>"
             r"　∠ECB＝$\dfrac12$∠ACD＋∠BCD＝$90^\circ-(a+b)+(a+b)=90^\circ$"),
           "(イ)" + A("30", "w20") + "　(ウ)" + A("2", "w20") + "　(エ)" + A(r"$\sqrt7$", "w20") + "　(オ)" + A("90", "w20"), 8)
    q3 = Q("(3)", "(カ)に入るものを、次の中から選びなさい。<div class=\"ch\">［　ECH　　CHE　　CBH　　BHC　　ABC　　BAC　］</div>",
           W("∠ECB＝∠CHB＝90°で、∠Bが共通。対応する頂点の順（E↔C、B↔B、C↔H）に書く"), A("CBH", "w20"), 4)
    q4 = Q("(4)", "△EBCと△(カ)が相似である理由を記しなさい。",
           lines("△EBCと△CBHで、<br>∠ECB＝∠CHB＝90°……①<br>∠EBC＝∠CBH（共通）……②<br>①、②より、2組の角がそれぞれ等しいから、△EBC∽△CBH", 26), "", 0)
    q5 = Q("(5)", "CEの長さを求めなさい。",
           W(r"△EBC∽△CBH より　EC：CH＝BC：BH　→　EC：2＝$\sqrt7$：$\sqrt3$<br>"
             r"EC＝$\dfrac{2\sqrt7}{\sqrt3}=\dfrac{2\sqrt{21}}{3}$"),
           A(r"$\dfrac{2\sqrt{21}}{3}$", "w20"), 12)
    return f"""<section class="page">{header("大問4　円と相似", "1")}
<div class="lead">点Oを中心とする円周上に、2点B、CをOB＝BCとなるように、点AはAB＝$3\\sqrt3$、AC＝4となるようにとります。また、点Dを辺AB上に∠BCDが、△ABCの∠ACBの外角と等しくなるようにとり、更に、∠ACDの二等分線とABの交点をEとします。このときCEの長さを求めなさい。</div>
<div class="lead">この問題を考えている尚子さんと志郎君の会話を読み、(1)〜(5)の各問いに答えなさい。</div>
{talk}
<div style="text-align:center;margin-top:2mm">{circle_svg()}</div>
</section>
<section class="page">{header("大問4　円と相似", "2")}
{q1}{q2}{q3}{q4}{q5}
</section>"""


# ================= 大問5 =================
def d5():
    q = [Q("(1)", "対角線ACの長さを求めなさい。",
           W(r"底面は1辺4cmの正方形。対角線は1辺の $\sqrt2$ 倍"), A(r"$4\sqrt2$ cm", "w20"), 8),
         Q("(2)", "OQ：QBを最も簡単な整数比で求めなさい。",
           W(r"面OABと面OBCを開くと（右の図）、AQ＋QPが最小になるのは A、Q、P が一直線になるとき<br>"
             r"開いた図の四角形OABCは1辺4のひし形なので AB∥OC。よって △QOP∽△QBA で　OQ：QB＝OP：BA＝3：4"),
           A("3：4", "w20"), 10),
         Q("(3)", "四角錐Q−ABCDの体積を求めなさい。",
           W(r"高さOR：△OBRで OB＝4、BR＝$\dfrac{4\sqrt2}{2}=2\sqrt2$ なので　OR＝$\sqrt{16-8}=2\sqrt2$<br>"
             r"QB：OB＝4：7 なので、Qの高さは $2\sqrt2\times\dfrac47=\dfrac{8\sqrt2}{7}$<br>"
             r"$\dfrac13\times4\times4\times\dfrac{8\sqrt2}{7}=\dfrac{128\sqrt2}{21}$"),
           A(r"$\dfrac{128\sqrt2}{21}$ cm³", "w30"), 14),
         Q("(4)", "線分QRの長さを求めなさい。",
           W(r"△OBRは OR＝BR＝$2\sqrt2$ の直角二等辺三角形。Qから OR に垂線 QI をひくと<br>"
             r"QI＝$2\sqrt2\times\dfrac37=\dfrac{6\sqrt2}{7}$、IR＝（Qの高さ）＝$\dfrac{8\sqrt2}{7}$<br>"
             r"QR＝$\sqrt{\left(\dfrac{6\sqrt2}7\right)^2+\left(\dfrac{8\sqrt2}7\right)^2}=\sqrt{\dfrac{72+128}{49}}=\dfrac{10\sqrt2}{7}$"),
           A(r"$\dfrac{10\sqrt2}{7}$ cm", "w20"), 14)]
    return f"""<section class="page">{header("大問5　空間図形")}
<div class="flex"><div class="grow"><div class="lead">図のような、1辺の長さが4cmの正四角錐O−ABCDがある。辺OC上に、点PをCP＝1cmとなるように、辺OB上に、点QをAQ＋QPが最小となるようにとる。また、対角線AC、BDの交点をRとするとき、次の(1)〜(4)の各問いに答えなさい。</div>{q[0]}</div>
<div class="fig">{pyr_svg()}</div></div>
<div class="flex"><div class="grow">{q[1]}</div><div class="fig">{net_svg()}</div></div>
{q[2]}{q[3]}
</section>"""


JOBS = [("c3_shishikan_r8_d1", d1), ("c3_shishikan_r8_d2", d2), ("c3_shishikan_r8_kansu", d3),
        ("c3_shishikan_r8_en", d4), ("c3_shishikan_r8_kuukan", d5)]

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
