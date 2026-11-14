"""実力テスト 令和2年度 3年・9月（大問1〜5）を、大問1／単元別の PDF にする。
問題（pdf/c3_jitsu_r209_*.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
部品・CSS は c3_jitsu_test.py などと共通。common.json の jitsu.tests の id は r2-3-09。

  大問1   小問集合（確率・30°の作図）                     c3_jitsu_r209_d1
  大問2-1 データの活用（漢字テストの度数・代表値）         c3_jitsu_r209_data
  大問2-2 方程式・連立方程式の利用（碁石の正方形・正三角形） c3_jitsu_r209_renritsu
  大問3   一次関数（図形の移動と重なる面積）               c3_jitsu_r209_ichiji
  大問4   平面図形（平行四辺形の証明・面積・角）           c3_jitsu_r209_zukei
  大問5   空間図形（立方体・切断）                         c3_jitsu_r209_kuukan

実行：cd tools && python3 c3_jitsu_r209.py
"""
from fractions import Fraction as F
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build, _arc  # noqa: E402
from c3_jitsu3_test import T, L  # noqa: E402

# ================= 答えの確認 =================
assert 8 - (-3) == 11 and F(-5, 6) + F(3, 8) == F(-11, 24) and -2 ** 2 + (-5) ** 2 == 21
assert all(3 * (3 * a - 2 * b) - (4 * a - 5 * b) == 5 * a - b for a in range(3) for b in range(3))
assert 2 - 5 - 3 == -6                                        # √8−√50−√18 ＝ (2−5−3)√2
assert -3 * -7 + 4 == -4 * -7 - 3                             # a＝−4
assert F(3 * 6, -2) == -9
HIKARU, AYUMU = [1, 2, 3, 4], [2, 2, 3, 3]
assert F(sum(h > a for h in HIKARU for a in AYUMU), 16) == F(3, 8)
CNT = {0: 1, 1: 2, 2: 3, 3: 4, 4: 7, 5: 3}                     # ①＝4、②＝7
data = sorted(k for k, v in CNT.items() for _ in range(v))
assert len(data) == 20 and F(data[9] + data[10], 2) == F(7, 2)
assert F(sum(k * v for k, v in CNT.items()), 20) == F(63, 20) and 22 * 3 - 63 == 3 and 1 + 2 == 3
assert 1 + 2 + 3 == 6 and F(6, 20) == F(3, 10) and max(CNT, key=CNT.get) == 4      # ア○ イ× ウ× エ○
x_, y_ = 5, 10
assert (4 * x_ - 4) + (3 * y_ - 3) == 43 and y_ == 2 * x_


def overlap(t):
    """図形あ（左端 A−6、[A−6,A−2] は高さ4、[A−2,A] は高さ2）と長方形 [0,8] の重なり。A の位置＝t"""
    seg = lambda a, b: max(0, min(b, 8) - max(a, 0))
    return 4 * seg(t - 6, t - 2) + 2 * seg(t - 2, t)


assert overlap(1) == 2 and overlap(2) == 4
assert all(overlap(t) == 4 * t - 4 for t in range(2, 7)) and all(overlap(t) == 20 for t in range(6, 9))
assert all(overlap(t) == -2 * t + 36 for t in range(8, 11)) and all(overlap(t) == -4 * t + 56 for t in range(10, 15))
assert [t for t in [x / 2 for x in range(29)] if overlap(t) == F(3, 5) * 20] == [4, 11]
assert 14 * 4 + 14 * 4 // 2 == 84 and 180 - 90 - 35 == 55
assert 6 * 1 == 6                                              # 表面積 6a²
J, K, A3, G3 = (0, 0, 1), (3, 3, 2), (0, 3, 3), (3, 0, 0)
sub = lambda p, q: tuple(a - b for a, b in zip(p, q))
d2_ = lambda v: sum(a * a for a in v)
assert sub(J, A3) == sub(G3, K) and d2_(sub(J, A3)) != d2_(sub(K, A3)) and d2_(sub(G3, A3)) != d2_(sub(K, J))   # 平行四辺形
assert F(1, 3) * F(9, 2) * 2 * 9 == 27                                        # 3：27＝1：9
assert 12 + 3 == 9 + 6 == 15 and 12 * 12 * F(15, 2) == 1080

TAG = "令和2年度　3年・9月"


def header(title, page=None):
    p = f"（{page}）" if page else ""
    return (f'<div class="hd"><div class="ht"><span class="tag">{TAG}</span>{title}{p}<span class="key">解答</span></div>'
            '<div class="nm">　月　　日　名前（　　　　　　　　　）</div></div>')


def arc_at(c, r, p, w=10):
    ang = math.degrees(math.atan2(-(p[1] - c[1]), p[0] - c[0]))
    return _arc(c, r, ang + w, ang - w)


def svg(w, h, s, x0=0, y0=0):
    return f'<svg width="{w}" height="{h}" viewBox="{x0} {y0} {w} {h}">{s}</svg>'


# ================= 図 =================
def angle30_svg():
    """線分AB。作図（正三角形で60° → 二等分して30°）は .cons＝こたえだけ"""
    A_, B_ = (24, 150), (290, 150)
    s = L(A_, B_, 1.3) + T(A_[0] - 10, A_[1] + 4, "A") + T(B_[0] + 10, B_[1] + 4, "B")
    r = 110
    X = (A_[0] + r, A_[1])
    Qp = (A_[0] + r * 0.5, A_[1] - r * math.sqrt(3) / 2)
    rr = 80
    # R：X と Q から半径 rr の円の交点（30°の線の上）
    d = r * math.cos(math.radians(30)) + math.sqrt(rr * rr - (r * math.sin(math.radians(30))) ** 2)
    R = (A_[0] + d * math.cos(math.radians(30)), A_[1] - d * math.sin(math.radians(30)))
    end = (A_[0] + 290 * math.cos(math.radians(30)), A_[1] - 290 * math.sin(math.radians(30)))
    c = _arc(A_, r, 68, -6) + arc_at(X, r, Qp, 12) + arc_at(X, rr, R, 9) + arc_at(Qp, rr, R, 9)
    c += L(A_, end, 1.4) + L(A_, Qp, 0.8, True)
    c += T(X[0] + 2, X[1] + 13, "X", "sm") + T(Qp[0] - 8, Qp[1] - 2, "Q", "sm") + T(end[0] + 4, end[1] + 4, "P", "", "start")
    c += T(A_[0] + 38, A_[1] - 6, "30°", "sm")
    return svg(320, 165, s + f'<g class="cons">{c}</g>', 0, 0)


def stones_svg():
    s = ""
    dot = lambda p: f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="3.6" fill="#333"/>'
    # 正方形
    x0, y0, w = 10, 10, 78
    ts = [0, 0.14, 0.28, 0.42, 1]
    for t in ts:
        for p in [(x0 + w * t, y0), (x0 + w * t, y0 + w), (x0, y0 + w * t), (x0 + w, y0 + w * t)]:
            s += dot(p)
    s += T(x0 + w * 0.71, y0 + 3, "…", "sm") + T(x0 + w * 0.71, y0 + w + 3, "…", "sm")
    s += T(x0, y0 + w * 0.73, "⋮", "sm") + T(x0 + w, y0 + w * 0.73, "⋮", "sm")
    s += f'<path d="M{x0} {y0 + w + 8} q0 6 6 6 H{x0 + w / 2 - 6} q6 0 6 6 q0 -6 6 -6 H{x0 + w - 6} q6 0 6 -6" fill="none" stroke="#333" stroke-width="1"/>'
    s += T(x0 + w / 2, y0 + w + 32, '<tspan class="ax">x</tspan>個', "sm")
    # 正三角形
    bx, by, b = 118, y0 + w, 92
    apex = (bx + b / 2, by - b * math.sqrt(3) / 2)
    left, right = (bx, by), (bx + b, by)
    for t in ts:
        for p, q in [(left, right), (left, apex), (right, apex)]:
            s += dot((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    s += T(bx + b * 0.71, by + 3, "…", "sm")
    s += f'<path d="M{bx} {by + 8} q0 6 6 6 H{bx + b / 2 - 6} q6 0 6 6 q0 -6 6 -6 H{bx + b - 6} q6 0 6 -6" fill="none" stroke="#333" stroke-width="1"/>'
    s += T(bx + b / 2, by + 32, '<tspan class="ax">y</tspan>個', "sm")
    return svg(220, by + 40, s)


def move_svg():
    k = 20
    X = lambda x: 40 + x * k
    Y = lambda y: 26 + (4 - y) * k
    P_ = lambda x, y: (X(x), Y(y))
    s = L((X(-1), Y(0)), (X(18), Y(0)), 1.1) + T(X(-1) + 2, Y(0) - 4, '<tspan class="ax">ℓ</tspan>', "sm", "start")
    pts = [(0, 0), (6, 0), (6, 2), (4, 2), (4, 4), (0, 4)]
    s += '<polygon points="' + " ".join(f"{X(a)},{Y(b)}" for a, b in pts) + '" fill="none" stroke="#000" stroke-width="1.3"/>'
    s += L(P_(4, 0), P_(4, 2), 1)
    s += f'<rect x="{X(9)}" y="{Y(4)}" width="{8 * k}" height="{4 * k}" fill="none" stroke="#000" stroke-width="1.3"/>'
    lab = [("G", 0, 0, 0, 12), ("D", 4, 0, 0, 12), ("A", 6, 0, 0, 12), ("F", 0, 4, -6, -3), ("E", 4, 4, 6, -3),
           ("C", 4, 2, -7, -3), ("B", 6, 2, 6, -3), ("S", 9, 0, 0, 12), ("P", 17, 0, 0, 12), ("R", 9, 4, 0, -4), ("Q", 17, 4, 0, -4)]
    s += "".join(T(X(a) + dx, Y(b) + dy, n, "sm") for n, a, b, dx, dy in lab)
    s += T(X(2), Y(4) - 4, "4cm", "sm") + T(X(0) - 4, Y(2) + 3, "4cm", "sm", "end") + T(X(6) + 3, Y(1) + 3, "2cm", "sm", "start")
    s += T(X(3), Y(0) + 24, "6cm", "sm") + T(X(13), Y(0) + 24, "8cm", "sm") + T(X(17) + 3, Y(2) + 3, "4cm", "sm", "start")
    s += L((X(0), Y(0) + 16), (X(6), Y(0) + 16), 0.7, True) + L((X(9), Y(0) + 16), (X(17), Y(0) + 16), 0.7, True)
    s += f'<circle cx="{X(2)}" cy="{Y(2)}" r="7" fill="none" stroke="#000" stroke-width="0.8"/>' + T(X(2), Y(2) + 4, "あ", "sm")
    s += L((X(5), Y(4) - 2), (X(7.5), Y(4) - 2), 1.1) + f'<path d="M{X(7.5)} {Y(4) - 2} l-6 -3 v6 z"/>'
    return svg(X(18) + 30, Y(0) + 30, s)


def para_svg():
    k = 0.6
    P = lambda x, y: (12 + x * k, 14 + (300 - y) * k)
    B_, C_, D_, A_, E_ = P(0, 0), P(390, 0), P(195, 0), P(265, 300), P(460, 300)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += L(A_, E_) + L(A_, D_) + L(E_, C_) + L(D_, E_)
    s += T(A_[0], A_[1] - 5, "A") + T(E_[0] + 8, E_[1], "E") + T(B_[0] - 2, B_[1] + 13, "B") + T(D_[0], D_[1] + 13, "D") + T(C_[0] + 4, C_[1] + 13, "C")
    return svg(int(E_[0]) + 20, int(B_[1]) + 18, s)


def cube_svg(kind=0):
    S = 120
    def P(x, y, z):
        return (14 + x * S + y * S * 0.42, 18 + (1 - z) * S + (1 - y) * S * 0.36)
    V = {"B": (0, 0, 1), "C": (1, 0, 1), "A": (0, 1, 1), "D": (1, 1, 1), "F": (0, 0, 0), "G": (1, 0, 0), "E": (0, 1, 0), "H": (1, 1, 0)}
    p = {n: P(*v) for n, v in V.items()}
    s = "".join(L(p[a], p[b], 1.2) for a, b in ["AB", "BC", "CD", "DA", "BF", "FG", "GC", "GH", "HD"])
    s += "".join(L(p[a], p[b], 0.9, True) for a, b in ["AE", "EF", "EH"])
    off = {"A": (-4, -5), "D": (4, -5), "B": (-10, 2), "C": (8, 10), "E": (-9, -3), "H": (10, 3), "F": (-6, 12), "G": (6, 12)}
    s += "".join(T(p[n][0] + dx, p[n][1] + dy, n, "sm") for n, (dx, dy) in off.items())
    if kind == 2:
        J, K = P(0, 0, 1 / 3), P(1, 1, 2 / 3)
        s += L(p["A"], p["C"]) + L(p["C"], J) + L(J, p["G"]) + L(p["G"], K) + L(p["A"], J, 0.9, True) + L(p["A"], K, 0.9, True)
        s += T(J[0] - 8, J[1] + 4, "J", "sm") + T(K[0] + 9, K[1] + 2, "K", "sm")
    if kind == 3:
        Lp, M, N = P(0, 1, 3 / 4), P(1, 0, 1 / 2), P(1, 1, 1 / 4)
        s += L(p["B"], M) + L(M, N) + L(p["B"], Lp, 0.9, True) + L(Lp, N, 0.9, True)
        s += T(Lp[0] + 7, Lp[1] - 1, "L", "sm") + T(M[0] - 9, M[1] - 3, "M", "sm") + T(N[0] + 9, N[1] + 2, "N", "sm")
    return svg(int(S * 1.42) + 34, int(S * 1.36) + 34, s)


# ================= 大問1 =================
def d1():
    c = [Q("(1)", r"$8-(-3)$ を計算しなさい。", W(r"$8+3$"), A("11"), 1),
         Q("(2)", r"$-\dfrac56+\dfrac38$ を計算しなさい。", W(r"$-\dfrac{20}{24}+\dfrac9{24}$"), A(r"$-\dfrac{11}{24}$"), 1),
         Q("(3)", r"$-2^2+(-5)^2$ を計算しなさい。", W(r"$-4+25$"), A("21"), 1),
         Q("(4)", r"$3(3a-2b)-(4a-5b)$ を計算しなさい。", W(r"$9a-6b-4a+5b$"), A(r"$5a-b$"), 1),
         Q("(5)", r"$\sqrt8-\sqrt{50}-\sqrt{18}$ を計算しなさい。", W(r"$2\sqrt2-5\sqrt2-3\sqrt2$"), A(r"$-6\sqrt2$"), 1),
         Q("(6)", r"一次方程式 $-3x+4=ax-3$ の解が $x=-7$ であるとき、$a$ の値を求めなさい。",
           W(r"$x=-7$ を代入　$21+4=-7a-3$　$7a=-28$"), A(r"$a=-4$"), 1),
         Q("(7)", r"$y$ は $x$ に反比例し、$x=3$ のとき $y=6$ である。$x=-2$ のときの $y$ の値を求めなさい。",
           W(r"$xy=3\times6=18$　$y=\dfrac{18}{-2}$"), A(r"$y=-9$"), 1)]
    c8 = Q("(8)", "光（ひかる）さんは1、2、3、4の4枚のカード、歩（あゆむ）さんは2、2、3、3の4枚のカードを持っている。カードをよくかき混ぜて、光さんと歩さんは同時にカードを1枚ずつ1回出し、"
           "数の大きいカードを出したほうを勝ちとする。また、同じ数のカードを出したときは引き分けとする。このとき、光さんが勝つ確率を求めなさい。ただし、どのカードの出し方も、同様に確からしいとする。",
           W("出し方は全部で 4×4＝16通り。光さんの勝ち：3を出して歩さんの2（2枚）→2通り、4を出して4枚どれでも→4通り。計6通り　$\\dfrac{6}{16}$"),
           A(r"$\dfrac38$"), 1)
    c9 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(9)</span>右の図のように、線分ABがある。'
          r'$\angle\mathrm{BAP}=30^\circ$ となる半直線APを、線分ABよりも上側に、コンパスと定規を使って作図しなさい。作図に用いた線は濃くはっきりと、残しておくこと。</div>'
          + W("①Aを中心に円をかき、ABとの交点をXとする。<br>②Xを中心に同じ半径の円をかき、①の円との交点をQとする（△AXQは正三角形で ∠QAX＝60°）。<br>"
              "③X・Qを中心に同じ半径の円をかき、その交点とAを結ぶ（∠QAXの二等分線）。60°÷2＝30°")
          + f'</div><div class="fig">{angle30_svg()}</div></div></div>')
    return f"""<section class="page tight">{header("大問1　小問集合")}
<div class="lead">次の(1)〜(9)の問いに答えなさい。</div>
<div class="grid2">{"".join(c[:6])}</div>
{c[6]}{c8}{c9}
</section>"""


# ================= 大問2-1 データの活用 =================
def d2a():
    tb = ('<div style="text-align:center;font-size:9.5pt;margin:2mm 0">漢字テストの得点<table class="tb"><tr><th>得点(点)</th>'
          + "".join(f"<td>{k}</td>" for k in range(6)) + '</tr><tr><th>人数(人)</th><td>1</td><td>2</td><td>3</td>'
          f'<td>{BX("①", "4")}</td><td>{BX("②", "7")}</td><td>3</td></tr></table></div>')
    q1 = Q("(1)", "表の①、②に当てはまる数を求めなさい。",
           W(r"①＋②＝$20-(1+2+3+3)=11$。中央値3.5点は、小さいほうから10番目と11番目の平均なので、10番目が3点、11番目が4点。<br>"
             r"2点以下が6人なので　6＋①＝10　①＝4、②＝11−4＝7"),
           "①" + A("4", "w20") + "　②" + A("7", "w20"), 16)
    q2 = Q("(2)", "このテストの得点について、正しいものを、次のア〜エからすべて選び、記号で答えなさい。"
           '<div class="ch">ア　得点が2点以下の人数は全体の30%である。<br>イ　得点の範囲は6点である。<br>ウ　最頻値は3点である。<br>エ　平均値は3.15点である。</div>',
           W(r"ア　$\dfrac{6}{20}=0.3$ ○　イ　$5-0=5$（点）×　ウ　いちばん多いのは4点（7人）×<br>"
             r"エ　$(0\times1+1\times2+2\times3+3\times4+4\times7+5\times3)\div20=63\div20=3.15$ ○"),
           A("ア、エ", "w20"), 16)
    q3 = Q("(3)", "このあと、さらに2人がこの漢字テストを受けて、この2人もふくめた22人の平均値を求めたら3点になった。この2人の得点の差が1点のとき、2人の得点は何点と何点か求めなさい。答えを求めるまでの過程も書きなさい。",
           lines(r"22人の合計は　$22\times3=66$（点）。20人の合計は63点なので、2人の合計は　$66-63=3$（点）<br>"
                 r"小さいほうの得点を $a$ 点とすると、大きいほうは $(a+1)$ 点　$a+(a+1)=3$　$a=1$<br>"
                 "（0〜5点の中にあり、問題に合う）", 34),
           A("1点と2点", "w20"), 0)
    return f"""<section class="page">{header("大問2-1　データの活用")}
<div class="lead"><b>1</b>　下の表は、あるクラスの生徒20人が受けた5点満点の漢字テストの得点を整理したものである。中央値は3.5点であることがわかっている。このとき、次の(1)〜(3)の問いに答えなさい。</div>
{tb}{q1}{q2}{q3}
</section>"""


# ================= 大問2-2 方程式の利用 =================
def d2b():
    q1 = Q("(1)", r"正方形をつくるのに使った碁石の数を、$x$ を使った式で表しなさい。",
           W(r"1辺 $x$ 個が4辺で $4x$ 個。かどの4個を2回ずつ数えているので　$4x-4$"), A(r"$4x-4$（個）", "w30"), 16)
    q2 = Q("(2)", r"$x$、$y$ の値をそれぞれ求めなさい。",
           W(r"正三角形は　$3y-3$（個）<br>$\begin{cases}(4x-4)+(3y-3)=43\\y=2x\end{cases}$　→　$4x+3y=50$ に $y=2x$ を代入<br>"
             r"$4x+6x=50$　$10x=50$　$x=5$　$y=2\times5=10$"),
           A(r"$x=5,\ y=10$", "w30"), 34)
    return f"""<section class="page">{header("大問2-2　連立方程式の利用")}
<div class="flex"><div class="grow"><div class="lead"><b>2</b>　碁石を右の図のように並べて、1辺の碁石の数が $x$ 個の正方形と $y$ 個の正三角形をつくると、碁石を全部で43個使い、正三角形の1辺の碁石の数は正方形の1辺の碁石の数の2倍であった。このとき、(1)、(2)の問いに答えなさい。</div></div>
<div class="fig">{stones_svg()}</div></div>
{q1}{q2}
</section>"""


# ================= 大問3 一次関数（図形の移動） =================
def d3():
    q1 = Q("1", r"$x=1$ のとき、$y$ の値を求めなさい。",
           W(r"Aが1cm進むと、重なるのは縦2cm・横1cmの長方形　$y=2\times1$"), A(r"$y=2$", "w20"), 8)
    q2 = Q("2", r"$0\leqq x\leqq2$ における $x$ と $y$ の関係について、正しいものを、次のア〜エから1つ選び、記号で答えなさい。"
           r'<div class="ch">ア　$y$ は $x$ に比例し、$x=2$ のとき $y=2$ である。<br>イ　$y$ は $x$ に比例し、$x=2$ のとき $y=4$ である。<br>'
           r'ウ　$y$ は $x$ に反比例し、$x=2$ のとき $y=2$ である。<br>エ　$y$ は $x$ に反比例し、$x=2$ のとき $y=4$ である。</div>',
           W(r"重なるのは縦2cm・横 $x$ cm の長方形なので $y=2x$（比例）。$x=2$ のとき $y=4$"), A("イ", "w20"), 4)
    expl = ('<div class="frame">2つの図形が重なってできる図形の面積 $y$ cm² は $x$ の変域によって、次のように表される。<br>'
            '<div style="margin-left:8mm;line-height:2.1">'
            r'$2\leqq x\leqq6$　　のとき、$y=$ ' + BX("①", r"$4x-4$") + ' となり、<br>'
            r'$6\leqq x\leqq$ ' + BX("②", "8") + ' 　のとき、$y=$ ' + BX("③", "20") + ' で一定となり、<br>'
            + BX("②", "8") + r' $\leqq x\leqq10$　のとき、$y=$ ' + BX("④", r"$-2x+36$") + ' で、<br>'
            r'$10\leqq x\leqq14$　のとき、$y=$ ' + BX("⑤", r"$-4x+56$") + ' となる。</div></div>')
    q3 = Q("3", r"$2\leqq x\leqq14$ における $x$ と $y$ の関係について、次の①〜⑤に当てはまる数または式を書き、【説明】を完成させなさい。<br><b>【説明】</b>" + expl,
           W(r"$2\leqq x\leqq6$：正方形ABCD（4cm²）がすべて重なり、正方形DEFGが横 $(x-2)$ cm 重なる　$4+4(x-2)=4x-4$<br>"
             r"$x=6$ で全部重なり、点AがPに着く $x=8$ まで　$16+4=20$<br>"
             r"$8\leqq x\leqq10$：正方形ABCDが横 $(x-8)$ cm 出ていく　$20-2(x-8)=-2x+36$<br>"
             r"$10\leqq x\leqq14$：正方形DEFGの残りの横 $(14-x)$ cm　$4(14-x)=-4x+56$"), "", 4)
    q4 = Q("4", r"2つの図形が重なってできる図形の面積が、あの図形の面積の $\dfrac35$ となるとき、$x$ の値をすべて求めなさい。",
           W(r"あの面積は20cm²なので　$20\times\dfrac35=12$<br>"
             r"$4x-4=12$ → $x=4$（$2\leqq x\leqq6$ に合う）　$-4x+56=12$ → $x=11$（$10\leqq x\leqq14$ に合う）<br>"
             r"$2x=12$ → $x=6$、$-2x+36=12$ → $x=12$ は変域に合わない"),
           A(r"$x=4,\ 11$", "w20"), 8)
    return f"""<section class="page tight">{header("大問3　一次関数（図形の移動）")}
<div class="flex"><div class="grow"><div class="lead">下の図のように、正方形ABCDと正方形DEFGの2つの正方形を組み合わせてできたあの図形ABCEFGと長方形PQRSが直線 ℓ 上にある。長方形PQRSを固定し、あの図形を図の位置から矢印の方向に毎秒1cmの速さで直線 ℓ 上を移動させる。
2つの図形が重なり始めてから $x$ 秒後の2つの図形が重なってできる図形の面積を $y$ cm² とする。このとき、次の1〜4の問いに答えなさい。</div></div></div>
<div style="text-align:center">{move_svg()}</div>
{q1}{q2}{q3}{q4}
</section>"""


# ================= 大問4 平面図形 =================
def d4():
    proof = ('<div class="frame">AB∥ED、AE∥BDで、四角形ABDEは平行四辺形より、AE＝BD…①'
             + lines("点Dは辺BCの中点だから　BD＝DC…②<br>①、②より　AE＝DC…③<br>また、AE∥BC より　AE∥DC…④<br>"
                     "③、④より、1組の対辺が平行でその長さが等しいから、", 30)
             + '四角形ADCEは平行四辺形である。</div>')
    q1 = Q("1", "四角形ADCEは平行四辺形であることを次のように証明した。【証明】を完成させなさい。<br><b>【証明】</b>" + proof, "", "", 0)
    q2 = Q("2", "辺ACと線分DEの交点をFとする。△AFEの面積が14cm²のとき、四角形ABCEの面積を求めなさい。",
           W(r"四角形ADCEは平行四辺形なので、対角線AC・DEはたがいの中点Fで交わり、△AFEは平行四辺形ADCEの $\dfrac14$<br>"
             r"平行四辺形ADCE＝$14\times4=56$。△ABD＝△ADC（BD＝DCで高さが同じ）＝$56\div2=28$<br>"
             r"四角形ABCE＝△ABD＋平行四辺形ADCE＝$28+56=84$"),
           A("84cm²", "w20"), 22)
    q3 = Q("3", r"$\angle\mathrm{BAC}=90^\circ$、$\angle\mathrm{ABC}=35^\circ$ のとき、$\angle\mathrm{ACE}$ の大きさを求めなさい。",
           W(r"DE∥AB、AB⊥AC より DE⊥AC。対角線が垂直に交わる平行四辺形ADCEはひし形なので、ACは∠DCEを2等分し $\angle\mathrm{ACE}=\angle\mathrm{ACD}$<br>"
             r"△ABCで　$\angle\mathrm{ACB}=180^\circ-90^\circ-35^\circ=55^\circ$"),
           A(r"$55^\circ$", "w20"), 16)
    return f"""<section class="page">{header("大問4　平面図形（平行四辺形）")}
<div class="flex"><div class="grow"><div class="lead">右の図のように、△ABCがあり、辺BCの中点をD、点Dを通り辺BAに平行な直線と点Aを通り辺BCに平行な直線との交点をEとする。点Aと点D、点Cと点Eをそれぞれ線分で結ぶ。このとき、次の1〜3の問いに答えなさい。</div></div>
<div class="fig">{para_svg()}</div></div>
{q1}{q2}{q3}
</section>"""


# ================= 大問5 空間図形 =================
def d5():
    q1 = Q("1", r"図Ⅰの立方体の1辺の長さが $a$ cmのとき、この立方体の表面積を $a$ を使って表しなさい。",
           W(r"1つの面は $a^2$ cm²、面は6つ"), A(r"$6a^2$ cm²", "w20"), 6)
    t1 = Q("(1)", "四角形AJGKはどのような四角形か。最も適切なものを次のア〜エから1つ選び、記号で答えなさい。"
           '<div class="ch">ア　長方形　　イ　ひし形　　ウ　平行四辺形　　エ　正方形</div>',
           W(r"1辺を3とすると BJ＝2、JF＝1、DK＝1、KH＝2。△ABJ≡△GHK、△ADK≡△GFJ より AJ＝GK、AK＝GJ（2組の対辺が等しい）<br>"
             r"$\mathrm{AJ}^2=9+4=13$、$\mathrm{AK}^2=9+1=10$ でとなりの辺が等しくない。対角線も AG$^2=27$、JK$^2=19$ で等しくない"),
           A("ウ", "w20"), 4)
    t2 = Q("(2)", "立体ABCJと立方体ABCDEFGHとの体積の比を、最も簡単な整数の比で表しなさい。",
           W(r"1辺を3とする。三角錐ABCJは底面△ABC＝$\dfrac12\times3\times3=\dfrac92$、高さBJ＝2　$\dfrac13\times\dfrac92\times2=3$<br>立方体は $27$　$3:27$"),
           A("1：9", "w20"), 12)
    q3 = Q("3", "図Ⅲは、図Ⅰの立方体の辺AE上に点L、辺CG上に点Mをとったもので、AL：LE＝1：3、CM：MG＝1：1である。この立方体を3点B、L、Mを通る平面で切ったら、切り口の平面は辺DH上の点Nを通り、DN：NH＝3：1であった。"
           "AB＝12cmのとき、切り分けられた2つの立体のうち、頂点Fをふくむほうの立体の体積を求めなさい。",
           W(r"BF＝12、LE＝9、MG＝6、NH＝3（cm）。$12+3=9+6=15$<br>同じ立体をもう1つ逆さにして切り口どうしを合わせると、高さ15cmの直方体になる<br>"
             r"$12\times12\times15\div2=1080$"),
           A("1080cm³", "w20"), 14)
    return f"""<section class="page tight">{header("大問5　空間図形")}
<div class="flex"><div class="grow"><div class="lead">右の図の立体は立方体である。このとき、次の1〜3の問いに答えなさい。</div>{q1}
<div class="q"><div class="qt"><span class="no">2</span>図Ⅱは、図Ⅰの立方体の辺BF上に点J、辺DH上に点Kをとったもので、BJ：JF＝2：1、DK：KH＝1：2である。このとき、次の(1)、(2)の問いに答えなさい。</div></div></div>
<div class="fig"><b>図Ⅰ</b><br>{cube_svg()}</div><div class="fig"><b>図Ⅱ</b><br>{cube_svg(2)}</div></div>
{t1}{t2}
<div class="flex"><div class="grow">{q3}</div><div class="fig"><b>図Ⅲ</b><br>{cube_svg(3)}</div></div>
</section>"""


JOBS = [("c3_jitsu_r209_d1", d1), ("c3_jitsu_r209_data", d2a), ("c3_jitsu_r209_renritsu", d2b),
        ("c3_jitsu_r209_ichiji", d3), ("c3_jitsu_r209_zukei", d4), ("c3_jitsu_r209_kuukan", d5)]

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
