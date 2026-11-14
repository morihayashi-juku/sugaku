"""中3 実力テスト④（高校入試形式・大問1〜5）を、大問1／単元別の PDF にする。
問題（pdf/c3_jitsu4_*.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
部品・CSS は c3_jitsu_test.py（①）・c3_jitsu2_test.py（②）・c3_jitsu3_test.py（③）と共通。

  大問1 小問集合（確率・作図つき）          c3_jitsu4_d1
  大問2-1 データの活用（箱ひげ図）          c3_jitsu4_data
  大問2-2 文字式の利用（色紙の規則性）      c3_jitsu4_moji
  大問3 一次関数（料金プラン）              c3_jitsu4_ichiji
  大問4 図形（平行四辺形・合同・面積）      c3_jitsu4_zukei
  大問5 空間図形（直方体・六角錐）          c3_jitsu4_kuukan

実行：cd tools && python3 c3_jitsu4_test.py
"""
from fractions import Fraction as F
from itertools import combinations
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build  # noqa: E402
from c3_jitsu3_test import T, L, right_mark  # noqa: E402

# ================= 答えの確認 =================
assert -4 - (-12) == 8 and 40 / -8 == -5
assert (lambda x: 4 * x + (5 * x + 7))(-2) == -11 and 5 * -2 + 7 == -3
CARDS = list(combinations([2, 3, 4, 5], 2))
assert F(sum(a % 2 == 0 and b % 2 == 0 for a, b in CARDS), len(CARDS)) == F(1, 6)
BOX1 = (14, 23, 28, 31, 37)          # 並び方①（図から読んだ値）
BOX2 = (12, 19, 28, 33, 42)          # 並び方②
HIST = {"ア": [4, 8, 7, 6, 3, 2], "イ": [2, 5, 9, 7, 5, 2], "ウ": [3, 4, 5, 6, 8, 4]}   # 10点から5点ごと
assert all(sum(h) == 30 for h in HIST.values())
assert BOX1[2] == BOX2[2] and BOX1[3] - BOX1[1] < BOX2[3] - BOX2[1]        # (3) エ
assert 22 % 3 == 1 and 7 * 10 + 3 == 73
PA, PB, PC = (lambda x: 50 * x + 600), (lambda x: 25 * x + 1500), (lambda x: 2850)
assert PA(40) == 2600 and PB(40) < PA(40) and min(PA(30), PB(30), PC(30)) == PA(30)
assert PB(36) == PA(36) and PB(54) == PC(54)
assert 180 - 2 * 38 == 104 and F(F(36, 5) / 2, F(12, 2) / 2) == F(6, 5)
assert 2 * (6 * 4 + 6 * 5 + 4 * 5) == 148 and F(1, 3) * (24 - 3 - 3) * 5 == 30

TAG = "中3　実力テスト④"


def header(title, page=None):
    p = f"（{page}）" if page else ""
    return (f'<div class="hd"><div class="ht"><span class="tag">{TAG}</span>{title}{p}<span class="key">解答</span></div>'
            '<div class="nm">　月　　日　名前（　　　　　　　　　）</div></div>')


# ================= 図 =================
def cards_svg():
    s = "".join(f'<rect x="{6 + i * 44}" y="6" width="38" height="54" fill="#fff" stroke="#000" stroke-width="1.1"/>' + T(25 + i * 44, 40, n, "b2")
                for i, n in enumerate("2345"))
    return f'<svg width="186" height="66" viewBox="0 0 186 66">{s}</svg>'


def tri_svg():
    """△ABC。作図（BCの垂直二等分線 → 中点M → 直線AM）は .cons＝こたえだけ"""
    B_, C_, A_ = (24, 160), (264, 160), (92, 22)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="#000" stroke-width="1.3"/>'
    s += T(A_[0], A_[1] - 6, "A") + T(B_[0] - 10, B_[1] + 5, "B") + T(C_[0] + 10, C_[1] + 5, "C")
    M = ((B_[0] + C_[0]) / 2, B_[1])
    r = 150
    h = (r * r - ((C_[0] - B_[0]) / 2) ** 2) ** 0.5
    top, bot = (M[0], M[1] - h), (M[0], M[1] + h)
    c = ""
    for cx in (B_[0], C_[0]):
        for py in (top[1], bot[1]):
            # 交点のまわりに短い弧
            import math
            ang = math.degrees(math.atan2(-(py - B_[1]), M[0] - cx))
            p1 = (cx + r * math.cos(math.radians(ang + 9)), B_[1] - r * math.sin(math.radians(ang + 9)))
            p2 = (cx + r * math.cos(math.radians(ang - 9)), B_[1] - r * math.sin(math.radians(ang - 9)))
            c += f'<path d="M{p1[0]:.1f} {p1[1]:.1f} A{r} {r} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="#000" stroke-width="1"/>'
    c += L((M[0], top[1] + 8), (M[0], bot[1] - 8), 0.9, True)
    # 直線 AM を少し延ばす
    dx, dy = M[0] - A_[0], M[1] - A_[1]
    c += L((A_[0] - 0.15 * dx, A_[1] - 0.15 * dy), (M[0] + 0.15 * dx, M[1] + 0.15 * dy), 1.4)
    c += f'<circle cx="{M[0]}" cy="{M[1]}" r="2.4" fill="#c00"/>' + T(M[0] + 8, M[1] + 14, "M", "sm")
    c += T(M[0] + 0.15 * dx + 8, M[1] + 0.15 * dy + 4, '<tspan class="ax">ℓ</tspan>', "pl", "start")
    y0 = int(min(A_[1], top[1])) - 16
    hh = int(bot[1]) + 8 - y0
    return f'<svg width="290" height="{hh}" viewBox="0 {y0} 290 {hh}">{s}<g class="cons">{c}</g></svg>'


def box2_svg():
    Lx, Wd = 64, 560
    xs = lambda v: Lx + v / 50 * Wd
    s = f'<rect x="{Lx}" y="4" width="{Wd}" height="118" fill="none" stroke="#000" stroke-width="1"/>'
    for v in range(1, 50):
        s += L((xs(v), 4), (xs(v), 122), 0.4 if v % 5 else 0.8, v % 5 != 0, "#888" if v % 5 else "#555")
    for y0, bx, lab in [(40, BOX1, "並び方①"), (86, BOX2, "並び方②")]:
        mn, q1, md, q3, mx = bx
        s += T(Lx - 6, y0 + 4, lab, "sm", "end")
        s += L((xs(mn), y0), (xs(q1), y0)) + L((xs(q3), y0), (xs(mx), y0))
        s += L((xs(mn), y0 - 8), (xs(mn), y0 + 8)) + L((xs(mx), y0 - 8), (xs(mx), y0 + 8))
        s += f'<rect x="{xs(q1):.1f}" y="{y0 - 14}" width="{xs(q3) - xs(q1):.1f}" height="28" fill="#fff" stroke="#000" stroke-width="1.2"/>'
        s += L((xs(md), y0 - 14), (xs(md), y0 + 14))
    for v in range(0, 51, 10):
        s += T(xs(v), 136, str(v), "sm")
    s += T(xs(50) + 10, 136, "(点)", "sm", "start")
    return f'<svg width="{Lx + Wd + 36}" height="142" viewBox="0 0 {Lx + Wd + 36} 142">{s}</svg>'


def hist_svg(counts):
    Lx, Tp, Wd, Hh = 22, 16, 150, 92
    xs = lambda v: Lx + v / 50 * Wd
    ys = lambda v: Tp + Hh - v / 10 * Hh
    s = T(4, 10, "(回)", "sm", "start") + f'<rect x="{Lx}" y="{Tp}" width="{Wd}" height="{Hh}" fill="none" stroke="#000" stroke-width="1"/>'
    for v in range(5, 50, 5):
        s += L((xs(v), Tp), (xs(v), Tp + Hh), 0.4, True, "#888")
    for i, c in enumerate(counts):
        x0 = 10 + 5 * i
        s += f'<rect x="{xs(x0):.1f}" y="{ys(c):.1f}" width="{xs(5) - xs(0):.1f}" height="{Hh * c / 10:.1f}" fill="#fff" stroke="#000" stroke-width="1.1"/>'
    for v in (0, 5, 10):
        s += T(Lx - 3, ys(v) + 3, str(v), "sm", "end")
    for v in range(0, 51, 10):
        s += T(xs(v), Tp + Hh + 11, str(v), "sm")
    s += T(xs(50) + 3, Tp + Hh + 11, "(点)", "sm", "start")
    return f'<svg width="200" height="{Tp + Hh + 16}" viewBox="0 0 200 {Tp + Hh + 16}">{s}</svg>'


def strip_svg():
    k = 10
    x, s = 28, ""
    fill = {"青": "#999", "白": "#fff", "黄": "#ddd"}
    wid = {"青": 3, "白": 2, "黄": 5}
    for c in ["青", "白", "黄", "青", "白", "黄", "青"]:
        w = wid[c] * k
        s += f'<rect x="{x}" y="8" width="{w}" height="{6 * k}" fill="{fill[c]}" stroke="#000" stroke-width="1"/>' + T(x + w / 2, 8 + 3 * k + 4, c, "sm")
        x += w
    s += T(x + 8, 42, "…", "sm", "start")
    s += T(11, 42, "6cm", "sm") + T(26 + 15, 84, "3cm", "sm") + T(26 + 30 + 10, 84, "2cm", "sm") + T(26 + 50 + 25, 84, "5cm", "sm")
    return f'<svg width="{x + 26}" height="90" viewBox="0 0 {x + 26} 90">{s}</svg>'


def plan_svg():
    Lx, Tp, sx, sy = 44, 18, 3.4, 0.05      # 1分＝3.4px、1円＝0.05px
    X = lambda x: Lx + x * sx
    Y = lambda y: Tp + (4000 - y) * sy
    s = ""
    for x in range(0, 61, 10):
        s += L((X(x), Y(0)), (X(x), Y(4000)), 0.5, False, "#999") + T(X(x), Y(0) + 12, str(x) if x else "O", "sm")
    for y in range(0, 4001, 500):
        s += L((X(0), Y(y)), (X(60), Y(y)), 0.5, False, "#999")
        if y:
            s += T(X(0) - 4, Y(y) + 3, str(y), "sm", "end")
    s += L((X(0), Y(0)), (X(60), Y(0)), 1.2) + L((X(0), Y(0)), (X(0), Y(4000)), 1.2)
    s += T(X(0) - 18, Tp - 6, "(円)", "sm") + T(X(0) + 6, Tp - 6, '<tspan class="ax">y</tspan>', "sm") + T(X(60) + 8, Y(0) + 4, '<tspan class="ax">x</tspan>(分)', "sm", "start")
    s += L((X(0), Y(PA(0))), (X(60), Y(PA(60))), 1.3) + L((X(0), Y(PB(0))), (X(60), Y(PB(60))), 1.3)
    s += T(X(60) + 4, Y(PA(60)) + 4, "プランA", "sm", "start") + T(X(60) + 4, Y(PB(60)) + 4, "プランB", "sm", "start")
    c = L((X(0), Y(2850)), (X(60), Y(2850)), 1.3) + T(X(60) + 4, Y(2850) + 14, "プランC", "sm", "start")
    c += L((X(36), Y(0)), (X(36), Y(PA(36))), 0.9, True) + L((X(54), Y(0)), (X(54), Y(2850)), 0.9, True)
    return f'<svg width="{X(60) + 56:.0f}" height="{Y(0) + 18:.0f}" viewBox="0 0 {X(60) + 56:.0f} {Y(0) + 18:.0f}">{s}<g class="cons">{c}</g></svg>'


def para_svg():
    k = 16
    B_, C_ = (14, 150), (14 + 12 * k, 150)
    A_ = (B_[0] + 3 * k, 150 - 5.2 * k)
    D_ = (A_[0] + 12 * k, A_[1])
    E_ = ((A_[0] + D_[0]) / 2, A_[1])
    F_ = (2 * D_[0] - C_[0], 2 * D_[1] - C_[1])        # DF＝CD
    oy = 6 - F_[1]
    sh = lambda p: (p[0], p[1] + oy)
    A_, B_, C_, D_, E_, F_ = map(sh, (A_, B_, C_, D_, E_, F_))
    s = (f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]} {D_[0]},{D_[1]}" fill="none" stroke="#000" stroke-width="1.2"/>'
         + L(B_, F_) + L(D_, F_))
    s += T(A_[0] - 4, A_[1] - 6, "A") + T(E_[0] - 2, E_[1] - 6, "E") + T(D_[0] + 9, D_[1] + 2, "D") + T(B_[0] - 2, B_[1] + 14, "B") + T(C_[0] + 6, C_[1] + 14, "C") + T(F_[0] + 6, F_[1] + 6, "F")
    return f'<svg width="{F_[0] + 20:.0f}" height="{B_[1] + 20:.0f}" viewBox="0 0 {F_[0] + 20:.0f} {B_[1] + 20:.0f}">{s}</svg>'


def cuboid_svg(fig2=False):
    k = 26
    dx, dy = 0.55 * k, -0.45 * k                     # 奥行き 1cm あたり
    E_ = (24, 30 + 5 * k + 4 * -dy)
    pt = lambda x, d, z: (E_[0] + x * k + d * dx, E_[1] - z * k + d * dy)   # x＝AB方向、d＝AD方向、z＝高さ
    A_, B_, C_, D_ = pt(0, 0, 5), pt(6, 0, 5), pt(6, 4, 5), pt(0, 4, 5)
    E2, F_, G_, H_ = pt(0, 0, 0), pt(6, 0, 0), pt(6, 4, 0), pt(0, 4, 0)
    s = "".join(L(p, q) for p, q in [(A_, B_), (B_, C_), (C_, D_), (D_, A_), (A_, E2), (B_, F_), (C_, G_), (E2, F_), (F_, G_)])
    s += "".join(L(p, q, 1, True) for p, q in [(D_, H_), (H_, E2), (H_, G_)])
    lab = [("A", A_, -9, 2), ("B", B_, 8, 12), ("C", C_, 8, -2), ("D", D_, 0, -6), ("E", E2, -8, 12), ("F", F_, 2, 14), ("G", G_, 9, 4), ("H", H_, -10, -3)]
    s += "".join(T(p[0] + ox, p[1] + oy, n) for n, p, ox, oy in lab)
    if not fig2:
        s += T((A_[0] + B_[0]) / 2, A_[1] + 14, "6cm", "sm") + T(A_[0] - 16, (A_[1] + E2[1]) / 2, "5cm", "sm") + T((A_[0] + D_[0]) / 2 - 14, (A_[1] + D_[1]) / 2 - 4, "4cm", "sm")
    else:
        mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
        P = mid(A_, C_)
        Qp, R_, S_, Tp = mid(E2, F_), mid(F_, G_), mid(G_, H_), mid(H_, E2)
        s += L(A_, C_, 0.6) + L(D_, B_, 0.6)
        s += "".join(L(P, p, 1.6) for p in (F_, R_, Qp, Tp)) + "".join(L(P, p, 1.2, True) for p in (S_, H_))
        s += L(Tp, Qp, 1.6) + L(Qp, F_, 1.6) + L(F_, R_, 1.6) + L(R_, S_, 1.2, True) + L(S_, H_, 1.2, True) + L(H_, Tp, 1.2, True)
        s += T(P[0], P[1] - 6, "P") + T(Qp[0], Qp[1] + 14, "Q") + T(R_[0] + 9, R_[1] + 6, "R") + T(S_[0] + 2, S_[1] - 6, "S") + T(Tp[0] - 9, Tp[1] + 2, "T")
    w = pt(6, 4, 0)[0] + 24
    return f'<svg width="{w:.0f}" height="{E_[1] + 22:.0f}" viewBox="0 0 {w:.0f} {E_[1] + 22:.0f}">{s}</svg>'


# ================= 大問1 =================
def d1():
    c1 = Q("(1)", r"$-4-(-12)$ を計算しなさい。", W(r"$-4+12=8$"), A("8"), 3)
    c2 = Q("(2)", r"$40\div(-8)$ を計算しなさい。", W(r"$-(40\div8)=-5$"), A("$-5$"), 3)
    c3 = Q("(3)", r"$15a^2b\div3ab$ を計算しなさい。", W(r"$\dfrac{15\times a\times a\times b}{3\times a\times b}$"), A("$5a$"), 3)
    c4 = Q("(4)", r"$\dfrac12x-\dfrac{x-y}{4}$ を計算しなさい。", W(r"$\dfrac{2x}{4}-\dfrac{x-y}{4}=\dfrac{2x-x+y}{4}$"), A(r"$\dfrac{x+y}{4}$"), 3)
    c5 = Q("(5)", r"連立方程式 $\begin{cases}4x+y=-11\\y=5x+7\end{cases}$ を解きなさい。",
           W(r"上の式に代入して　$4x+5x+7=-11$　$9x=-18$　$x=-2$<br>$y=5\times(-2)+7=-3$"), A(r"$x=-2,\ y=-3$"), 3)
    c6 = Q("(6)", r"A地点からB地点まで、毎分80mの速さで歩くと20分かかった。毎分 $x$ mの速さで歩くと $y$ 分かかるとして、$y$ を $x$ の式で表しなさい。",
           W(r"道のりは $80\times20=1600$（m）。（時間）＝（道のり）÷（速さ）"), A(r"$y=\dfrac{1600}{x}$"), 3)
    c7 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(7)</span>右のような4枚のカードがある。これをよくきって、同時に2枚のカードを取り出すとき、'
          '2枚とも偶数のカードが出る確率を求めなさい。ただし、どのカードが取り出されることも同様に確からしいとする。</div>'
          + W("取り出し方は {2,3} {2,4} {2,5} {3,4} {3,5} {4,5} の6通り。2枚とも偶数は {2,4} の1通り。")
          + f'</div><div class="fig">{cards_svg()}</div></div><div class="al">答　{A(r"$\dfrac{1}{6}$", "w20")}</div></div>')
    c8 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(8)</span>右の図の△ABCで、頂点Aを通り、△ABCの面積を二等分する直線 $\\ell$ を、'
          'コンパスと定規を使って作図しなさい。作図に用いた線は消さずに残しておくこと。</div>'
          + W("底辺BCの中点をMとすると、△ABMと△ACMは底辺も高さも等しい。<br>"
              "①B・Cを中心に同じ半径の円をかき、2つの交点を結ぶ（辺BCの垂直二等分線）。<br>②辺BCとの交点がM。③直線AMが $\\ell$。")
          + f'</div><div class="fig">{tri_svg()}</div></div></div>')
    return f"""<section class="page">{header("大問1　小問集合")}
<div class="lead">次の(1)〜(8)の問いに答えなさい。</div>
<div class="grid2">{c1}{c2}{c3}{c4}{c5}{c6}</div>
{c7}
{c8}
</section>"""


# ================= 大問2-1 データの活用 =================
def d2a():
    q1 = Q("(1)", "並び方①の得点分布の範囲を求めなさい。", W(r"（範囲）＝（最大値）−（最小値）＝$37-14=23$"), A("23点", "w20"), 8)
    hs = "".join(f'<div style="text-align:center"><b>{n}</b><br>{hist_svg(h)}</div>' for n, h in HIST.items())
    q2 = Q("(2)", "並び方①の箱ひげ図について、同じデータを使って作成したヒストグラムとして適切なものを、次のア〜ウから1つ選び、記号で答えなさい。"
           f'<div class="hists">{hs}</div>',
           W("並び方①：最小値14・第1四分位数23・中央値28・第3四分位数31・最大値37（30回）。<br>"
             "中央値（15・16番目）は25点以上30点未満、第3四分位数（23番目）は30点以上35点未満の階級に入るのはウだけ。"), A("ウ", "w20"), 6)
    q3 = Q("(3)", "箱ひげ図から読み取れることとして適切なものを、次のア〜エから1つ選び、記号で答えなさい。"
           '<div class="ch">ア　並び方①と並び方②の平均値は等しいが、並び方①の四分位範囲のほうが大きく、散らばりが大きいと考えられる。<br>'
           'イ　並び方①と並び方②の平均値は等しいが、並び方①の四分位範囲のほうが小さく、散らばりが小さいと考えられる。<br>'
           'ウ　並び方①と並び方②の中央値は等しいが、並び方①の四分位範囲のほうが大きく、散らばりが大きいと考えられる。<br>'
           'エ　並び方①と並び方②の中央値は等しいが、並び方①の四分位範囲のほうが小さく、散らばりが小さいと考えられる。</div>',
           W("箱ひげ図から平均値はわからない。中央値はどちらも28点。四分位範囲は ①$31-23=8$、②$33-19=14$ で①のほうが小さい。"), A("エ", "w20"), 4)
    return f"""<section class="page">{header("大問2-1　データの活用（箱ひげ図）")}
<div class="lead">のあさんの中学校では、クラス対抗大縄跳び大会が毎年行われている。跳んだ回数がそのまま得点となるため、のあさんのクラスでは、並び方①と並び方②のどちらにするか話し合っている。
下の図は、並び方①と並び方②のそれぞれで、30回ずつ練習したときの得点のデータを箱ひげ図に表したものである。このとき、下の(1)〜(3)の問いに答えなさい。</div>
<div style="text-align:center">{box2_svg()}</div>
{q1}{q2}{q3}
</section>"""


# ================= 大問2-2 文字式の利用 =================
def d2b():
    d = lambda who, t: f'<p class="dl"><b>{who}：</b>{t}</p>'
    kadai = ('<div class="frame"><b>【課題】</b><div class="flex"><div class="grow">青、白、黄の3種類の長方形の色紙がある。3種類の色紙の縦の長さはすべて6cmで、'
             '横の長さは青が3cm、白が2cm、黄が5cmである。</div><div class="fig">' + strip_svg() + '</div></div>'
             'これらの色紙を、右の図のように青、白、黄、青、白、黄、青、…の順番で、横一列にすき間なく並べ、そのときにできる長方形の面積について考えてみよう。</div>')
    kaiwa = ('<div class="frame"><b>【会話】</b>'
             + d("たつや", "色紙を17枚並べたとき、一番右端の色紙は何色かな？")
             + d("みなみ", "色は青、白、黄を3枚ごとにくり返すから、17÷3＝5余り2で、3の倍数である「15枚目の色紙」が黄とわかるね。ということは、「16枚目の色紙」は青、「17枚目の色紙」は白になるね。")
             + d("たつや", "なるほど。じゃあ、色紙を22枚並べたとき一番右端の色紙の色は " + BX("①", "青") + " だね。")
             + d("みなみ", "このときにできる長方形の横の長さは " + BX("②", "73") + " cmになるよ。横の長さがわかれば、長方形の面積を求めることもできるね。")
             + d("たつや", r"次に、一番右端が青の色紙になるように並べて作った長方形で、使った青の色紙の総数が $n$ 枚である場合について考えてみよう。")
             + d("みなみ", r"使った青の色紙の総数が $n$ 枚ということは、右端の青の色紙が「$n$ 枚目の青」で、そのすぐ左側にある黄の色紙は「$(n-1)$ 枚目の黄」ということになるね。つまり、白の色紙の総数と黄の色紙の総数は、それぞれ $(n-1)$ 枚ということがわかるよ。")
             + d("たつや", r'ということは、<span class="ul">一番右端が青の色紙になるように並べて作った長方形で、使った青の色紙が $n$ 枚である</span>ときの長方形の面積も $n$ を使った式で表すことができるね。')
             + '</div>')
    q1 = Q("(1)", "【会話】の中の " + BX("①", "青") + " には青、白、黄のどれが当てはまるか、答えなさい。また、" + BX("②", "73") + " には当てはまる数を、答えなさい。",
           W(r"$22\div3=7$ 余り1 → 21枚目が黄で、22枚目は青。<br>横の長さ：青・白・黄の1組で $3+2+5=10$（cm）。7組と青1枚で　$10\times7+3=73$"),
           "①" + A("青", "w20") + "　②" + A("73", "w20"), 16)
    q2 = Q("(2)", r"【会話】の中の下線部について、長方形の面積を、$n$ を用いて表しなさい。",
           W(r"横の長さ：青 $3n$ cm、白 $2(n-1)$ cm、黄 $5(n-1)$ cm<br>$3n+2(n-1)+5(n-1)=10n-7$（cm）<br>面積：$6\times(10n-7)=60n-42$"),
           A(r"$(60n-42)$ cm²", "w30"), 22)
    return f"""<section class="page">{header("大問2-2　文字式の利用（規則性）")}
<div class="lead">たつやさんとみなみさんは、次のような【課題】について考えた。下の【会話】は、2人が話し合っている場面の一部である。このとき、下の(1)、(2)の問いに答えなさい。</div>
{kadai}{kaiwa}{q1}{q2}
</section>"""


# ================= 大問3 一次関数 =================
def d3():
    shiryo = ('<div class="frame" style="width:78mm"><b>【資料】</b><br><b>1か月の利用料金</b><br>'
              'プランA：基本料金600円<br>　　　＋　通話料金　1分につき50円<br>プランB：基本料金1500円<br>　　　＋　通話料金　1分につき25円<br>'
              'プランC：何分かけても定額2850円</div>')
    q1 = Q("1", "プランAで、1か月の通話時間が40分のときの利用料金を求めなさい。", W(r"$600+50\times40=2600$"), A("2600円", "w20"), 6)
    q2 = Q("2", "通話時間を決めたときの利用料金について述べた文として正しいものを、次のア〜エから1つ選び、記号で答えなさい。"
           '<div class="ch">ア　通話時間が30分のとき、利用料金がもっとも安くなるのはプランBである。<br>イ　通話時間が40分のとき、プランAよりプランBの利用料金のほうが安い。<br>'
           'ウ　通話時間が50分のとき、利用料金がもっとも安くなるのはプランCである。<br>エ　通話時間が60分のとき、プランCよりプランBの利用料金のほうが安い。</div>',
           W("30分：A 2100円・B 2250円・C 2850円　40分：A 2600円・B 2500円<br>50分：A 3100円・B 2750円・C 2850円　60分：B 3000円・C 2850円"), A("イ", "w20"), 4)
    q3 = Q("3", r"$x$ と $y$ の関係について、次の①、②にあてはまる式を書きなさい。"
           '<div class="frame" style="margin-left:7mm">プランA　$y=$' + BX("①", r"$50x+600$") + '<br>プランB　$y=$' + BX("②", r"$25x+1500$")
           + '<br>プランC　$y=2850$</div>',
           W("（料金）＝（1分の通話料金）×（分）＋（基本料金）"), "①" + A(r"$50x+600$", "w30") + "　②" + A(r"$25x+1500$", "w30"), 3)
    q4 = Q("4", "3つの料金プランの中で、プランBの利用料金がもっとも安くなるのは、通話時間が何分以上何分以下のときか、求めなさい。ただし、もっとも安い料金プランが2つある場合もふくむものとする。",
           W(r"BがA以下：$25x+1500\leqq50x+600$　$900\leqq25x$　$x\geqq36$<br>"
             r"BがC以下：$25x+1500\leqq2850$　$25x\leqq1350$　$x\leqq54$（グラフの赤い線）"), A("36分以上54分以下", "w30"), 14)
    return f"""<section class="page">{header("大問3　一次関数（料金プラン）")}
<div class="lead">ある携帯電話会社では、1か月の利用料金について、3つの料金プランが用意されている。次の【資料】は、3つの料金プランを調べて、まとめたものである。また、下の図は、1か月の通話時間を $x$ 分、利用料金を $y$ 円として、プランA、プランBについて、$x$ と $y$ の関係をグラフに表したものである。このとき、次の1〜4の問いに答えなさい。</div>
<div class="flex" style="align-items:center;justify-content:space-around">{shiryo}<div class="fig">{plan_svg()}</div></div>
{q1}{q2}{q3}{q4}
</section>"""


# ================= 大問4 図形 =================
def d4():
    q1 = Q("1", "△ABE≡△DFEであることを証明しなさい。",
           lines(r"△ABEと△DFEで、<br>仮定より　AE＝DE　……①<br>対頂角は等しいから　$\angle\mathrm{AEB}=\angle\mathrm{DEF}$　……②<br>"
                 r"AB∥DC より AB∥CF で、平行線の錯角は等しいから　$\angle\mathrm{BAE}=\angle\mathrm{FDE}$　……③<br>"
                 r"①、②、③より、1組の辺とその両端の角がそれぞれ等しいから、△ABE≡△DFE", 44), "", 0)
    q2 = '<div class="q"><div class="qt"><span class="no">2</span>AB＝6cm、BC＝12cmのとき、次の(1)〜(3)の問いに答えなさい。</div></div>'
    t1 = Q("(1)", "FCの長さを求めなさい。", W("△ABE≡△DFE より DF＝AB＝6cm。平行四辺形の対辺だから CD＝AB＝6cm<br>FC＝FD＋DC＝6＋6＝12"), A("12 cm", "w20"), 14)
    t2 = Q("(2)", r"$\angle\mathrm{EBC}=38^\circ$ のとき、$\angle\mathrm{BAE}$ の大きさを求めなさい。",
           W(r"AD＝BC＝12cm で、Eは辺ADの中点だから AE＝6cm＝AB。△ABEは二等辺三角形で $\angle\mathrm{ABE}=\angle\mathrm{AEB}$<br>"
             r"AD∥BC の錯角で $\angle\mathrm{AEB}=\angle\mathrm{EBC}=38^\circ$　よって　$\angle\mathrm{BAE}=180^\circ-38^\circ\times2=104^\circ$"), A(r"$104^\circ$", "w20"), 16)
    t3 = Q("(3)", "辺BC上にBG：GC＝3：2となるような点Gをとるとき、△BEGの面積は△DEFの面積の何倍か、求めなさい。",
           W(r"平行四辺形の高さを $h$ とする。BG＝$12\times\dfrac35=\dfrac{36}{5}$（cm）<br>"
             r"△BEG＝$\dfrac12\times\dfrac{36}{5}\times h=\dfrac{18}{5}h$　△DEF＝△ABE＝$\dfrac12\times6\times h=3h$<br>"
             r"$\dfrac{18}{5}h\div3h=\dfrac65$"), A(r"$\dfrac{6}{5}$ 倍", "w20"), 22)
    return f"""<section class="page">{header("大問4　図形（合同・面積）")}
<div class="flex"><div class="grow"><div class="lead">右の図のような平行四辺形ABCDがある。辺AD上にAE＝EDとなる点Eをとり、BEの延長とCDの延長とが交わる点をFとする。<br>このとき、次の1、2の問いに答えなさい。</div></div>
<div class="fig">{para_svg()}</div></div>
{q1}{q2}{t1}{t2}{t3}
</section>"""


# ================= 大問5 空間図形 =================
def d5():
    q1 = Q("1", "図Ⅰにおいて、辺ABと平行である面を、次のア〜オの中からすべて選び、記号で答えなさい。"
           '<div class="ch">ア　面ABCD　　イ　面EFGH　　ウ　面AEFB<br>エ　面CDHG　　オ　面BFGC</div>',
           W("面ABCD・面AEFBは辺ABをふくむ。面BFGCは辺ABと点Bで交わる（垂直）。"), A("イ、エ", "w30"), 4)
    q2 = Q("2", "図Ⅰの直方体の表面積を求めなさい。", W(r"$2\times(6\times4+6\times5+4\times5)=2\times74=148$"), A("148 cm²", "w20"), 10)
    q3 = Q("3", "図Ⅱは、図Ⅰの直方体の線分ACとDBの交点をPとし、辺EF、FG、GH、HEの中点をそれぞれQ、R、S、Tとしたものである。点Pを頂点とし、面FRSHTQを底面とする立体の名称を答えなさい。",
           W("底面FRSHTQは頂点が6つの六角形。"), A("六角錐", "w20"), 6)
    q4 = Q("4", "3の立体の体積を求めなさい。",
           W(r"底面積＝長方形EFGH $6\times4=24$ から、△EQT（$\dfrac12\times3\times2=3$）と△GSR（$3$）をひいて　$24-3-3=18$<br>"
             r"高さはAE＝5cm　　$\dfrac13\times18\times5=30$"), A("30 cm³", "w20"), 16)
    return f"""<section class="page">{header("大問5　空間図形（直方体・角錐）")}
<div class="lead">図ⅠのようなAB＝6cm、AD＝4cm、AE＝5cmの直方体がある。このとき、次の1〜4の問いに答えなさい。</div>
<div class="flex"><div class="grow">{q1}{q2}</div><div class="fig"><b>図Ⅰ</b><br>{cuboid_svg()}</div></div>
<div class="flex"><div class="grow">{q3}{q4}</div><div class="fig"><b>図Ⅱ</b><br>{cuboid_svg(True)}</div></div>
</section>"""


JOBS = [("c3_jitsu4_d1", d1), ("c3_jitsu4_data", d2a), ("c3_jitsu4_moji", d2b),
        ("c3_jitsu4_ichiji", d3), ("c3_jitsu4_zukei", d4), ("c3_jitsu4_kuukan", d5)]

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
