"""実力テスト 令和6年度 3年・9月（大問1〜5）を、大問1／単元別の PDF にする。
問題（pdf/c3_jitsu_r609_*.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
部品・CSS は c3_jitsu_test.py などと共通。common.json の jitsu.tests の id は r6-3-09。

  大問1 小問集合（平方根・確率・中点の作図）         c3_jitsu_r609_d1
  大問2 空間図形（立方体・展開図・三角錐）           c3_jitsu_r609_kuukan
  大問3 データの活用（箱ひげ図・ヒストグラム）       c3_jitsu_r609_data（2ページ）
  大問4 平面図形（合同・角・長さ・面積）             c3_jitsu_r609_zukei
  大問5 一次関数（2直線と正方形）                     c3_jitsu_r609_ichiji

実行：cd tools && python3 c3_jitsu_r609.py
"""
from fractions import Fraction as F
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build, _arc  # noqa: E402
from c3_jitsu3_test import T, L, right_mark  # noqa: E402

# ================= 答えの確認 =================
assert -7 + 2 == -5 and F(-8) / F(-4, 5) == 10 and (9 * -2 + 7, 5 * -2 - 1) == (-11, -11)
assert all(a * a + a - 56 == (a + 8) * (a - 7) for a in range(-5, 6))
assert 5 * 3 + 3 * -4 == 3 and 2 * 3 - -4 == 10
assert F(sum(1 for a in range(1, 7) for b in range(1, 7) if a * b % 9 == 0), 36) == F(1, 9)
assert F(1, 3) * F(1, 2) * 6 * 6 * 6 == 36 and 6 * 6 * 6 - 3 * 18 * 2 == 108
BOX1, BOX2, BOX3 = (2, 12, 22, 26, 33), (0, 5, 14, 20, 30), (2, 6, 11, 21, 29)   # 図から読んだ値
assert BOX1[4] - BOX1[0] == 31 and BOX1[3] - BOX1[1] == 14 and BOX2[4] - BOX2[0] == 30 and BOX2[3] - BOX2[1] == 15
HIST = [7, 8, 4, 5, 3, 4]                                                          # 3組（0時間から5時間ごと）
assert sum(HIST) == 31
cls = lambda k: next(i for i in range(6) if sum(HIST[:i + 1]) >= k) * 5          # k 番目（小さいほうから）の階級の下限
assert cls(8) == 5 and cls(16) == 10 and cls(24) == 15 and not (15 <= BOX3[3] < 20)   # 第3四分位数（上から8番目）がおかしい
assert 180 - (90 - 35) - 45 == 80 and 6 + 3 - 4 == 5 and F(1, 2) * 4 * (6 - 4) == 4
assert (-10 + 16, F(10, 2) + 1) == (6, 6) and (-4 + 16) - (2 + 1) == 9
assert (-6 + 16) - (3 + 1) == 6

TAG = "令和6年度　3年・9月"


def header(title, page=None):
    p = f"（{page}）" if page else ""
    return (f'<div class="hd"><div class="ht"><span class="tag">{TAG}</span>{title}{p}<span class="key">解答</span></div>'
            '<div class="nm">　月　　日　名前（　　　　　　　　　）</div></div>')


def arc_at(c, r, p, w=10):
    ang = math.degrees(math.atan2(-(p[1] - c[1]), p[0] - c[0]))
    return _arc(c, r, ang + w, ang - w)


# ================= 図 =================
def tri_svg():
    """△ABC。作図（辺BCの垂直二等分線 → 中点P → 線分AP）は .cons＝こたえだけ"""
    B_, C_, A_ = (20, 150), (250, 150), (82, 30)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="#000" stroke-width="1.3"/>'
    s += T(A_[0], A_[1] - 6, "A") + T(B_[0] - 8, B_[1] + 12, "B") + T(C_[0] + 8, C_[1] + 12, "C")
    M = ((B_[0] + C_[0]) / 2, B_[1])
    r = 140
    h = math.sqrt(r * r - ((C_[0] - B_[0]) / 2) ** 2)
    top, bot = (M[0], M[1] - h), (M[0], M[1] + h)
    c = arc_at(B_, r, top, 8) + arc_at(B_, r, bot, 8) + arc_at(C_, r, top, 8) + arc_at(C_, r, bot, 8)
    c += L((M[0], top[1] + 6), (M[0], bot[1] - 6), 0.9, True) + L(A_, M, 1.4)
    c += f'<circle cx="{M[0]}" cy="{M[1]}" r="2.4" fill="#c00"/>' + T(M[0] + 9, M[1] + 13, "P")
    y0 = int(min(top[1], A_[1] - 10)) - 8
    hh = int(bot[1]) + 8 - y0
    return f'<svg width="275" height="{hh}" viewBox="0 {y0} 275 {hh}">{s}<g class="cons">{c}</g></svg>'


def cube_svg(fig2=False):
    sc = 0.6
    P = lambda x, y: ((x - 1200) * sc, (y - 240) * sc)
    A_, B_, F_, E_ = P(1235, 320), P(1410, 320), P(1410, 500), P(1235, 500)
    D_, C_, G_, H_ = P(1310, 265), P(1485, 265), P(1485, 440), P(1310, 440)
    s = "".join(L(p, q) for p, q in [(A_, B_), (B_, F_), (F_, E_), (E_, A_), (A_, D_), (D_, C_), (C_, B_), (C_, G_), (G_, F_)])
    s += "".join(L(p, q, 1, True) for p, q in [(D_, H_), (H_, E_), (H_, G_)])
    if fig2:
        s += L(A_, C_) + L(A_, F_) + L(F_, C_)
    lab = [("A", A_, -9, 2), ("B", B_, 9, 12), ("F", F_, 0, 14), ("E", E_, -6, 14), ("D", D_, 0, -6), ("C", C_, 6, -5), ("G", G_, 9, 6), ("H", H_, -10, -2)]
    s += "".join(T(p[0] + dx, p[1] + dy, n) for n, p, dx, dy in lab)
    return f'<svg width="195" height="178" viewBox="-6 2 195 178">{s}</svg>'


NETS = {"ア": [((1, 1), (2, 0)), ((0, 1), (1, 2)), ((1, 1), (2, 2))],
        "イ": [((1, 1), (2, 0)), ((1, 1), (2, 2)), ((2, 2), (3, 1))],
        "ウ": [((1, 1), (2, 0)), ((0, 1), (1, 2)), ((2, 2), (3, 1))],
        "エ": [((1, 1), (2, 0)), ((1, 1), (2, 2)), ((3, 1), (4, 2))]}


def net_svg(diags, mark):
    s_ = 26
    o = (6, 14)
    P = lambda x, y: (o[0] + x * s_, o[1] + y * s_)
    out = [(1, 0), (2, 0), (2, 1), (4, 1), (4, 2), (2, 2), (2, 3), (1, 3), (1, 2), (0, 2), (0, 1), (1, 1)]
    s = '<polygon points="' + " ".join(f"{P(*p)[0]},{P(*p)[1]}" for p in out) + '" fill="#fff" stroke="#000" stroke-width="1.1"/>'
    for p, q in [((1, 1), (2, 1)), ((1, 2), (2, 2)), ((1, 1), (1, 2)), ((2, 1), (2, 2)), ((3, 1), (3, 2))]:
        s += L(P(*p), P(*q), 0.8, True)
    s += "".join(L(P(*p), P(*q), 1.2) for p, q in diags)
    lab = [("D", (1, 0), -6, -2), ("C", (2, 0), 6, -2), ("A", (1, 1), -6, -3), ("B", (2, 1), 6, -3),
           ("E", (1, 2), -6, 11), ("F", (2, 2), 6, 11), ("H", (1, 3), -6, 8), ("G", (2, 3), 6, 8)]
    s += "".join(T(P(*p)[0] + dx, P(*p)[1] + dy, n, "sm") for n, p, dx, dy in lab)
    s += T(2, 10, mark, "b2", "start")
    return f'<svg width="{4 * s_ + 14}" height="{3 * s_ + 26}" viewBox="0 0 {4 * s_ + 14} {3 * s_ + 26}">{s}</svg>'


def boxes_svg(rows, wid=420):
    Lx, Wd = 40, wid - 80
    xs = lambda v: Lx + v / 37 * Wd
    H = 18 + 46 * len(rows)
    s = f'<rect x="{xs(-1):.1f}" y="4" width="{xs(37) - xs(-1):.1f}" height="{H - 8}" fill="none" stroke="#000" stroke-width="1"/>'
    for v in range(0, 37):
        s += L((xs(v), 4), (xs(v), H - 4), 0.4, True, "#888")
    for i, (lab, bx) in enumerate(rows):
        y0 = 30 + 46 * i
        mn, q1, md, q3, mx = bx
        s += T(Lx - 10, y0 + 4, lab, "sm", "end")
        s += L((xs(mn), y0), (xs(q1), y0), 1.3) + L((xs(q3), y0), (xs(mx), y0), 1.3)
        s += L((xs(mn), y0 - 8), (xs(mn), y0 + 8), 1.3) + L((xs(mx), y0 - 8), (xs(mx), y0 + 8), 1.3)
        s += f'<rect x="{xs(q1):.1f}" y="{y0 - 15}" width="{xs(q3) - xs(q1):.1f}" height="30" fill="#fff" stroke="#000" stroke-width="1.3"/>'
        s += L((xs(md), y0 - 15), (xs(md), y0 + 15), 1.3)
    for v in range(0, 36, 5):
        s += T(xs(v), H + 10, str(v), "sm")
    s += T(xs(35) + 12, H + 10, "(時間)", "sm", "start")
    return f'<svg width="{wid}" height="{H + 16}" viewBox="0 0 {wid} {H + 16}">{s}</svg>'


def hist_svg():
    Lx, Tp, Wd, Hh = 26, 16, 230, 135
    xs = lambda v: Lx + (v + 2) / 37 * Wd
    ys = lambda v: Tp + Hh - v / 9 * Hh
    s = T(4, 10, "(人)", "sm", "start")
    for v in range(0, 10):
        s += L((Lx, ys(v)), (Lx + Wd, ys(v)), 0.5, v > 0, "#888") + T(Lx - 4, ys(v) + 3, str(v), "sm", "end")
    for i, c in enumerate(HIST):
        s += f'<rect x="{xs(5 * i):.1f}" y="{ys(c):.1f}" width="{xs(5) - xs(0):.1f}" height="{Hh * c / 9:.1f}" fill="#ccc" stroke="#000" stroke-width="1"/>'
    for v in range(0, 31, 5):
        s += T(xs(v), Tp + Hh + 12, str(v), "sm")
    s += T(Lx + Wd - 4, Tp + Hh + 12, "(時間)", "sm", "start")
    return f'<svg width="{Lx + Wd + 32}" height="{Tp + Hh + 18}" viewBox="0 0 {Lx + Wd + 32} {Tp + Hh + 18}">{s}</svg>'


def rect_svg(fig2=False):
    k = 20
    S = lambda x, y: (16 + x * k, 14 + (10 - y) * k)
    A_, B_, C_, D_, E_, G_, F_ = S(0, 6), S(0, 0), S(9, 0), S(9, 6), S(4, 0), S(6, 6), S(6, 10)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]} {D_[0]},{D_[1]}" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += L(A_, F_) + L(A_, E_) + L(E_, F_) + L(F_, G_) + right_mark(G_, (-1, 0), (0, -1), 6)
    if fig2:
        s += L(G_, E_)
    s += T(A_[0] - 9, A_[1] + 2, "A") + T(B_[0] - 8, B_[1] + 10, "B") + T(C_[0] + 8, C_[1] + 10, "C") + T(D_[0] + 8, D_[1] + 2, "D")
    s += T(E_[0], E_[1] + 14, "E") + T(G_[0] + 4, G_[1] + 13, "G") + T(F_[0], F_[1] - 5, "F")
    return f'<svg width="{C_[0] + 24}" height="{B_[1] + 20}" viewBox="0 0 {C_[0] + 24} {B_[1] + 20}">{s}</svg>'


def graph_svg(ax):
    sc = 12
    ox, oy = 14, 17 * sc + 6
    X = lambda x: ox + x * sc
    Y = lambda y: oy - y * sc
    s = L((X(-1), Y(0)), (X(17), Y(0)), 1) + L((X(0), Y(-1)), (X(0), Y(17)), 1)
    s += T(X(17) + 6, Y(0) + 4, '<tspan class="ax">x</tspan>', "pl") + T(X(0) - 8, Y(17) + 2, '<tspan class="ax">y</tspan>', "pl") + T(X(0) - 8, Y(0) + 12, "O", "sm")
    s += L((X(0), Y(16)), (X(16.6), Y(-0.6)), 1.1) + L((X(-1), Y(0.5)), (X(17), Y(9.5)), 1.1)
    s += T(X(0) + 10, Y(16) + 2, "①", "sm", "start") + T(X(17) + 2, Y(9.5), "②", "sm", "start")
    ya, yb = -ax + 16, ax / 2 + 1
    s += L((X(ax), Y(ya)), (X(ax), Y(yb)), 1.1) + f'<circle cx="{X(ax)}" cy="{Y(ya)}" r="2"/><circle cx="{X(ax)}" cy="{Y(yb)}" r="2"/>'
    s += T(X(ax) + 7, Y(ya) - 3, "A") + T(X(ax) + 2, Y(yb) + 14, "B") + T(X(10) + 2, Y(6) - 7, "P")
    if ax == 6:
        s += L((X(0), Y(ya)), (X(ax), Y(ya)), 1.1) + L((X(0), Y(yb)), (X(ax), Y(yb)), 1.1) + T(X(0) - 8, Y(ya) + 4, "C") + T(X(0) - 8, Y(yb) + 4, "D")
    return f'<svg width="{X(17) + 22}" height="{Y(-1) + 8}" viewBox="0 0 {X(17) + 22} {Y(-1) + 8}">{s}</svg>'


# ================= 大問1 =================
def d1():
    c = [Q("(1)", r"$(-7)+2$ を計算しなさい。", W(r"$-(7-2)$"), A("$-5$"), 1),
         Q("(2)", r"$(-8)\div\left(-\dfrac45\right)$ を計算しなさい。", W(r"$(-8)\times\left(-\dfrac54\right)$"), A("10"), 1),
         Q("(3)", r"方程式 $9x+7=5x-1$ を解きなさい。", W(r"$9x-5x=-1-7$　$4x=-8$"), A(r"$x=-2$"), 1),
         Q("(4)", r"$a^2+a-56$ を因数分解しなさい。", W(r"かけて $-56$、たして $1$ → $8$ と $-7$"), A(r"$(a+8)(a-7)$"), 1),
         Q("(5)", r"連立方程式 $\begin{cases}5x+3y=3\\2x-y=10\end{cases}$ を解きなさい。",
           W(r"下×3 $6x-3y=30$ をたして $11x=33$　$x=3$<br>$2\times3-y=10$　$y=-4$"), A(r"$x=3,\ y=-4$"), 1),
         Q("(6)", "大小2つのさいころを同時に投げるとき、出た目の数の積が9の倍数になる確率を求めなさい。ただし、さいころの目の出かたは、同様に確からしいとする。",
           W("積が9の倍数：(3,3)(3,6)(6,3)(6,6) の4通り。全部で36通り"), A(r"$\dfrac19$"), 1)]
    c7 = Q("(7)", "平方根について述べたことがらのうち、正しいものを、次のア〜エから1つ選び、記号で答えなさい。"
           r'<div class="ch">ア　$\sqrt8+\sqrt2$ は $\sqrt{10}$ である。<br>イ　$(-\sqrt5)^2$ は $-5$ である。<br>ウ　$\sqrt3\times\sqrt7$ は $\sqrt{21}$ である。<br>エ　$\sqrt{49}$ は $\pm7$ である。</div>',
           W(r"ア $2\sqrt2+\sqrt2=3\sqrt2$　イ $5$　エ $7$（$\sqrt{49}$ は正の数）"), A("ウ", "w20"), 1)
    c8 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(8)</span>右の図のような△ABCがある。辺BC上に点Pをとって、△ABCの面積を2等分する線分APを、コンパスと定規を使って作図しなさい。'
          '作図に用いた線は消さずに濃くはっきりと残しておくこと。</div>'
          + W("Pを辺BCの中点にすると、△ABPと△ACPは底辺も高さも等しい。<br>"
              "①B・Cを中心に同じ半径の円をかき、2つの交点を結ぶ（辺BCの垂直二等分線）。<br>②辺BCとの交点がP。③AとPを結ぶ。")
          + f'</div><div class="fig">{tri_svg()}</div></div></div>')
    return f"""<section class="page tight">{header("大問1　小問集合")}
<div class="lead">次の(1)〜(8)の問いに答えなさい。</div>
<div class="grid2">{"".join(c)}</div>
{c7}{c8}
</section>"""


# ================= 大問2 空間図形 =================
def d2():
    q1 = Q("1", "図Ⅰにおいて、辺を直線、面を平面とみたとき、平面AEHDと平行な直線は何本あるか答えなさい。",
           W("平面AEHDと向かい合う面BFGCの4本の辺 BF・FG・GC・CB"), A("4本", "w20"), 6)
    opts = "".join(f'<div style="display:inline-block;margin-right:3mm">{net_svg(d, m)}</div>' for m, d in NETS.items())
    t1 = Q("(1)", "対角線を立方体の展開図に表したものとして正しいものを、次のア〜エから1つ選び、記号で答えなさい。"
           f'<div style="margin:1mm 0 0 7mm">{opts}</div>',
           W("面ABCDにAC、面AEFBにAF、面BFGC（面AEFBの右どなり）にFC。この3本がそろうのはイ。"), A("イ", "w20"), 2)
    t2 = Q("(2)", "A、B、C、Fを頂点とする三角錐ABCFの体積を求めなさい。",
           W(r"底面△ABC＝$\dfrac12\times6\times6=18$、高さBF＝6　$\dfrac13\times18\times6=36$"), A("36cm³", "w20"), 10)
    t3 = Q("(3)", "立方体から三角錐ABCFを取り除いた立体ACDEFGHの表面積は、三角錐ABCFの表面積より何cm²大きいか求めなさい。",
           W(r"どちらも△ACFをふくむので、△ACF以外を比べる。立体ACDEFGH：立方体の表面 $36\times6=216$ から直角二等辺三角形3つ（$18\times3=54$）をひいて 162<br>"
             r"三角錐ABCF：直角二等辺三角形3つで 54　　$162-54=108$"), A("108cm²", "w20"), 16)
    return f"""<section class="page">{header("大問2　空間図形")}
<div class="flex"><div class="grow"><div class="lead">右の図Ⅰのような、1辺の長さが6cmの立方体ABCDEFGHがある。このとき、次の1、2の問いに答えなさい。</div>{q1}
<div class="q"><div class="qt"><span class="no">2</span>図Ⅱは、図Ⅰにおいて、面ABCD、AEFB、BFGCの3つの面に対角線AC、AF、FCをひいたものである。このとき、次の(1)〜(3)の問いに答えなさい。</div></div></div>
<div class="fig"><b>図Ⅰ</b><br>{cube_svg()}</div><div class="fig"><b>図Ⅱ</b><br>{cube_svg(True)}</div></div>
{t1}{t2}{t3}
</section>"""


# ================= 大問3 データの活用 =================
def d3():
    d = lambda who, t: f'<p class="dl"><b>{who}：</b>{t}</p>'
    kai1 = ('<div class="frame"><b>【会話Ⅰ】</b>'
            + d("太郎", "ぼくは1組の生徒30人にアンケートをとって、読書時間を調べたよ。")
            + d("花子", "わたしは2組の生徒30人にアンケートをとったよ。")
            + d("太郎", "アンケート結果をもとに、1組と2組の読書時間を、それぞれ箱ひげ図に表してみよう。")
            + f'<div style="text-align:center;font-size:9pt"><b>図Ⅰ</b><br>{boxes_svg([("1組", BOX1), ("2組", BOX2)])}</div>'
            + d("花子", "1組と2組の読書時間をそれぞれ箱ひげ図に表すと、図Ⅰのようになったよ。")
            + d("太郎", "箱ひげ図に表してみると、データの散らばりぐあいがわかりやすいね。")
            + d("花子", "うん。たとえば、範囲は1組が " + BX("①", "31") + " 時間、2組が30時間だから、1組のほうが大きいけど、四分位範囲は1組が14時間、2組が " + BX("②", "15") + " 時間だから、2組のほうが大きいことがわかるよ。")
            + d("太郎", 'そうだね。このほかに、<span class="ul">上の箱ひげ図から読み取れること</span>はないかな。') + '</div>')
    r1 = Q("(1)", "【会話Ⅰ】の " + BX("①", "31") + "、" + BX("②", "15") + " にあてはまる数を答えなさい。",
           W(r"1組の範囲 $33-2=31$　2組の四分位範囲 $20-5=15$"), "①" + A("31", "w20") + "　②" + A("15", "w20"), 6)
    r2 = Q("(2)", "【会話Ⅰ】の波線部のように、「上の箱ひげ図から読み取れること」として正しくないものを、次のア〜エから1つ選び、記号で答えなさい。"
           '<div class="ch">ア　1組のほうが2組より最大値が大きいこと。<br>イ　1組で、読書時間が26時間であった生徒が少なくとも1人はいること。<br>'
           'ウ　2組で、読書時間が5時間以下であった生徒が8人以上いること。<br>エ　2組の生徒の読書時間の平均値が14時間であること。</div>',
           W("イ：30人の第3四分位数は大きいほうから8番目の1人の値なので、26時間の人がいる。ウ：第1四分位数（8番目）が5時間。<br>エ：14時間は中央値。平均値は箱ひげ図からはわからない。"),
           A("エ", "w20"), 4)
    p1 = f"""<section class="page">{header("大問3　データの活用", "1/2")}
<div class="lead">ある中学校の3年1組の太郎さんと3年2組の花子さんは、ともに図書委員である。2人は、自分たちの中学校の3年生の1か月間の読書時間を調べることにした。このとき、後の1、2の問いに答えなさい。ただし、データの値はすべて整数とする。</div>
<div class="lead"><b>1</b>　次の【会話Ⅰ】は、2人が3年1組と2組の1か月間の読書時間について話し合っている場面である。後の(1)、(2)の問いに答えなさい。</div>
{kai1}{r1}{r2}
</section>"""
    kai2 = ('<div class="frame"><b>【会話Ⅱ】</b>'
            + d("太郎", "3組の図書委員からもらったデータを、1組、2組と同じように箱ひげ図に表してみたら、図Ⅲのようになったよ。")
            + f'<div style="text-align:center;font-size:9pt"><b>図Ⅲ</b><br>{boxes_svg([("3組", BOX3)])}</div>'
            + d("花子", 'あれ？　ヒストグラムとこの箱ひげ図には、<span class="ul">対応していないところ</span>があるよ。') + '</div>')
    box4 = '<span class="bx" style="min-width:60mm"><span class="ql">④</span><span class="qa">15時間以上20時間未満の階級にふくまれる</span></span>'
    expl = ('<div class="frame">箱ひげ図によると、' + BX("①", "ウ") + ' は ' + BX("②", "21") + ' 時間となっている。<br>'
            + BX("①", "ウ") + ' は読書時間が長いほうから ' + BX("③", "8") + ' 番目のデータであり、ヒストグラムによると、そのデータは ' + box4 + ' から。</div>'
            '<div class="ch">ア　第1四分位数　　イ　第2四分位数　　ウ　第3四分位数</div>')
    s2 = Q("", "【会話Ⅱ】の波線部のように、3組の箱ひげ図には明らかに誤っているところが1か所ある。次の文章は、なぜ誤っているのかを説明したものである。"
           + BX("①", "ウ") + " にはどこが誤っているのかを、あとのア〜ウの中から1つ選び、記号で答えなさい。また、" + BX("②", "21") + "、" + BX("③", "8")
           + " にはあてはまる数を、④にはあてはまる説明を、①がふくまれている階級が何時間以上何時間未満であるかを具体的に示して、それぞれ答えなさい。" + expl,
           W("31人のとき、第1四分位数は小さいほうから8番目、中央値は16番目、第3四分位数は大きいほうから8番目。<br>"
             "ヒストグラムで大きいほうから 4人（25〜30）、3人（20〜25）で7人なので、8番目は15時間以上20時間未満。箱ひげ図の21時間とは合わない。<br>"
             "（第1四分位数6時間は5〜10、中央値11時間は10〜15の階級で、合っている）"),
           "①" + A("ウ", "w20") + "　②" + A("21", "w20") + "　③" + A("8", "w20"), 4)
    p2 = f"""<section class="page">{header("大問3　データの活用", "2/2")}
<div class="flex"><div class="grow"><div class="lead"><b>2</b>　図Ⅱは、後日、太郎さんと花子さんが、3年3組の図書委員からもらったデータをもとに、3組の生徒31人の1か月間の読書時間についてアンケート結果をヒストグラムにまとめたものである。図Ⅱでは、各階級を0時間以上5時間未満、5時間以上10時間未満、…、25時間以上30時間未満としている。【会話Ⅱ】は、2人が3年3組の1か月間の読書時間について話し合っている場面である。</div></div>
<div class="fig"><b>図Ⅱ</b><br>{hist_svg()}</div></div>
{kai2}{s2}
</section>"""
    return p1 + p2


# ================= 大問4 平面図形 =================
def d4():
    q1 = Q("1", "△ABE≡△AGFであることを証明しなさい。",
           lines(r"△ABEと△AGFで、<br>仮定より　AE＝AF　……①<br>"
                 r"長方形の角と、FG⊥AD より　$\angle\mathrm{ABE}=\angle\mathrm{AGF}=90^\circ$　……②<br>"
                 r"仮定より $\angle\mathrm{BAE}=\angle\mathrm{DAF}$ で、点Gは辺AD上にあるから　$\angle\mathrm{BAE}=\angle\mathrm{GAF}$　……③<br>"
                 r"①、②、③より、直角三角形の斜辺と1つの鋭角がそれぞれ等しいから、△ABE≡△AGF", 40), "", 0)
    q2 = Q("2", r"$\angle\mathrm{GAE}=55^\circ$ のとき、$\angle\mathrm{FEC}$ の大きさを求めなさい。",
           W(r"$\angle\mathrm{BAE}=90^\circ-55^\circ=35^\circ=\angle\mathrm{DAF}$ より $\angle\mathrm{EAF}=55^\circ+35^\circ=90^\circ$。AE＝AF なので $\angle\mathrm{AEF}=45^\circ$<br>"
             r"△ABEで $\angle\mathrm{AEB}=180^\circ-90^\circ-35^\circ=55^\circ$　$\angle\mathrm{FEC}=180^\circ-55^\circ-45^\circ=80^\circ$"),
           A(r"$80^\circ$", "w20"), 16)
    t1 = Q("(1)", "線分ECの長さを求めなさい。",
           W(r"1より AG＝AB＝6cm、BE＝GF＝4cm。BC＝AD＝AG＋GD＝6＋3＝9（cm）　EC＝9−4＝5"), A("5cm", "w20"), 10)
    t2 = Q("(2)", "△FEGの面積を求めなさい。",
           W(r"FGを底辺（4cm）とすると、高さは点Eから直線FGまでの距離。BE＝4、BからFGまでは AG＝6 なので、高さは $6-4=2$<br>$\dfrac12\times4\times2=4$"),
           A("4cm²", "w20"), 16)
    return f"""<section class="page">{header("大問4　平面図形（合同・角・面積）")}
<div class="flex"><div class="grow"><div class="lead">図Ⅰのように、長方形ABCDの辺BC上に点Eをとり、長方形ABCDの外側に、AE＝AF、∠BAE＝∠DAFとなるような点Fをとる。点Fから辺ADに垂線をひき、交点をGとする。さらに、点Eと点Fを線分で結ぶ。このとき、次の1〜3の問いに答えなさい。</div>{q1}</div>
<div class="fig"><b>図Ⅰ</b><br>{rect_svg()}</div></div>
{q2}
<div class="flex"><div class="grow"><div class="q"><div class="qt"><span class="no">3</span>図Ⅱは、図Ⅰにおいて、点Gと点Eを線分で結んだものである。AB＝6cm、FG＝4cm、GD＝3cmのとき、次の(1)、(2)の問いに答えなさい。</div></div>{t1}{t2}</div>
<div class="fig"><b>図Ⅱ</b><br>{rect_svg(True)}</div></div>
</section>"""


# ================= 大問5 一次関数 =================
def d5():
    q1 = Q("1", "関数①と②のどちらにもあてはまらない特徴を述べた文として正しいものを、次のア〜エから1つ選び、記号で答えなさい。"
           r'<div class="ch">ア　グラフの切片は $\dfrac12$ である。<br>イ　変化の割合は一定である。<br>ウ　$x$ の変域が $-6\leqq x\leqq8$ のとき、$y$ の変域は $-2\leqq y\leqq5$ である。<br>エ　$x$ の値が増加すると、$y$ の値は減少する。</div>',
           W(r"切片は①16、②1。イ：どちらも一次関数。ウ：②は $x=-6$ で $-2$、$x=8$ で $5$。エ：①は傾きが負。"), A("ア", "w20"), 2)
    q2 = Q("2", "点Pの座標を求めなさい。", W(r"$-x+16=\dfrac12x+1$　$-\dfrac32x=-15$　$x=10$　$y=-10+16=6$"), A("P$(10,\\ 6)$", "w20"), 8)
    q3 = Q("3", r"点Aの $x$ 座標が4のとき、線分ABの長さを求めなさい。", W(r"A$(4,\ 12)$、B$(4,\ 3)$　AB＝$12-3$"), A("9", "w20"), 8)
    q4 = Q("4", r"図Ⅱは、図Ⅰにおいて、点A、Bから $y$ 軸に垂線をひき、交点をそれぞれC、Dとしたものである。四角形ABDCが正方形になるとき、点Aの座標を求めなさい。ただし、点Aの $y$ 座標は点Bの $y$ 座標より大きいものとする。",
           W(r"Aの $x$ 座標を $t$ とすると AC＝$t$、AB＝$(-t+16)-\left(\dfrac12t+1\right)=15-\dfrac32t$<br>"
             r"AB＝AC より $15-\dfrac32t=t$　$\dfrac52t=15$　$t=6$　A$(6,\ 10)$（AB＝$10-4=6$ で合う）"), A("A$(6,\\ 10)$", "w20"), 22)
    return f"""<section class="page">{header("大問5　一次関数")}
<div class="flex"><div class="grow"><div class="lead">図Ⅰのように、2つの関数　$y=-x+16$ …①、$y=\\dfrac12x+1$ …②　のグラフが点Pで交わっている。また、点Aは関数①のグラフ上の点、点Bは関数②のグラフ上の点で、線分ABは $y$ 軸に平行である。このとき、次の1〜4の問いに答えなさい。</div>{q1}</div>
<div class="fig"><b>図Ⅰ</b><br>{graph_svg(4)}</div></div>
{q2}{q3}
<div class="flex"><div class="grow">{q4}</div><div class="fig"><b>図Ⅱ</b><br>{graph_svg(6)}</div></div>
</section>"""


JOBS = [("c3_jitsu_r609_d1", d1), ("c3_jitsu_r609_kuukan", d2), ("c3_jitsu_r609_data", d3),
        ("c3_jitsu_r609_zukei", d4), ("c3_jitsu_r609_ichiji", d5)]

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
