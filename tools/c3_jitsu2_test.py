"""中3 実力テスト②（高校入試形式・大問1〜5）を、大問1／単元別の PDF にする。
問題（pdf/c3_jitsu2_*.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
部品・CSS は c3_jitsu_test.py（実力テスト①）と共通。

  大問1 小問集合（作図つき）   c3_jitsu2_d1
  大問2-1 確率                 c3_jitsu2_kakuritsu
  大問2-2 連立方程式の利用     c3_jitsu2_renritsu
  大問3 データの活用           c3_jitsu2_data（2ページ）
  大問4 図形（合同・面積）     c3_jitsu2_zukei（2ページ）
  大問5 一次関数               c3_jitsu2_ichiji

実行：cd tools && python3 c3_jitsu2_test.py
"""
from fractions import Fraction as F
import itertools
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import c3_jitsu_test as base  # noqa: E402
from c3_jitsu_test import A, W, BX, Q, lines, build as _build, CSS as BASE_CSS, KATEX, OUT  # noqa: E402

# ================= 答えの確認 =================
assert 3 - (-4) == 7 and F(-5, 6) / 10 == F(-1, 12)
assert 3 * (-2) + 4 == -(-2) - 4
assert math.isclose(2 * math.sqrt(3) + math.sqrt(27), 5 * math.sqrt(3))
COINS = [500, 100, 50, 10]
SUBS = list(itertools.product([0, 1], repeat=4))
assert sum(1 for s in SUBS if sum(c * b for c, b in zip(COINS, s)) <= 100) == 5
assert 17 + 14 == 31 and 3 * 17 + 5 * 14 == 121
H1 = [1, 5, 6, 5, 8, 7, 3]
assert sum(H1) == 35 and sum(H1[:3]) == 12 and H1[0] + H1[1] == 1 + 5 and H1[1] + H1[2] == 11 and H1[3] + H1[4] == 13 and H1[5] + H1[6] == 10
assert math.hypot(3, 4) == 5 and F(1, 3) * 9 * 4 == 12
assert 15 - 2 * F(1, 2) * 3 * 4 == 3 and (180 - 30) / 2 == 75
assert F(3 + 5, -4) == -2 and F(1, 2) * 14 * 4 == 28
ADB = abs((-6 + 4) * (-5 - 3) - (0 - 3) * (0 + 4)) / 2
assert ADB == 14 and -5 - ADB / 2 == -12

TAG = "令和8年度　3年・10月"


def header(title, page=None):
    p = f"（{page}）" if page else ""
    return (f'<div class="hd"><div class="ht"><span class="tag">{TAG}</span>{title}{p}<span class="key">解答</span></div>'
            '<div class="nm">　月　　日　名前（　　　　　　　　　）</div></div>')


EXTRA = r"""
.cons, .cons * { }
.mondai .cons { display:none; }
.kaitou .cons line, .kaitou .cons path, .kaitou .cons circle { stroke:#c00; }
.kaitou .cons text { fill:#c00; font-weight:700; }
.tb { border-collapse:collapse; margin:0 auto; font-size:9.5pt; }
.tb th, .tb td { border:1px solid #333; padding:1mm 4mm; text-align:center; font-weight:400; }
.tb .ph { font-size:7pt; display:block; line-height:1; text-align:left; }
.pt16 { display:grid; grid-template-columns: repeat(4, 1fr); gap:1mm 3mm; margin:1mm 0 1mm 4mm; font-size:9pt; }
.pt16 span { border:1px solid #c88; padding:0 2mm; border-radius:2px; text-align:center; }
.pt16 .hit { background:#fde; font-weight:700; }
.ul { text-decoration:underline; }
.spc { height:6mm; }
"""
CSS = BASE_CSS + EXTRA


def build(body, mode):
    return _build(body, mode).replace(BASE_CSS, CSS)


# ================= 図 =================
def _pt(c, r, deg):
    a = math.radians(deg)
    return (c[0] + r * math.cos(a), c[1] - r * math.sin(a))


def _arc(c, r, a1, a2):
    p1, p2 = _pt(c, r, a1), _pt(c, r, a2)
    sweep = 1 if a2 < a1 else 0
    return f'<path d="M{p1[0]:.1f} {p1[1]:.1f} A{r} {r} 0 0 {sweep} {p2[0]:.1f} {p2[1]:.1f}" fill="none" stroke="#000" stroke-width="1"/>'


def tri_svg():
    """∠BAC=90°, ∠ACB=40° の直角三角形（作図の線は .cons＝こたえだけ）"""
    L = 260
    B = (24, 190)
    C = (B[0] + L, B[1])
    ab = L * math.sin(math.radians(40))
    A_ = _pt(B, ab, 50)
    s = f'<polygon points="{B[0]},{B[1]} {C[0]},{C[1]} {A_[0]:.1f},{A_[1]:.1f}" fill="none" stroke="#000" stroke-width="1.3"/>'
    # 直角の印（A）
    u1 = ((B[0] - A_[0]) / ab, (B[1] - A_[1]) / ab)
    ac = L * math.cos(math.radians(40))
    u2 = ((C[0] - A_[0]) / ac, (C[1] - A_[1]) / ac)
    k = 9
    q = [(A_[0] + k * u1[0], A_[1] + k * u1[1]), (A_[0] + k * (u1[0] + u2[0]), A_[1] + k * (u1[1] + u2[1])), (A_[0] + k * u2[0], A_[1] + k * u2[1])]
    s += f'<polyline points="{q[0][0]:.1f},{q[0][1]:.1f} {q[1][0]:.1f},{q[1][1]:.1f} {q[2][0]:.1f},{q[2][1]:.1f}" fill="none" stroke="#000" stroke-width="1"/>'
    s += f'<text x="{A_[0]-4:.1f}" y="{A_[1]-8:.1f}" class="pl">A</text><text x="{B[0]-14}" y="{B[1]+14}" class="pl">B</text><text x="{C[0]+6}" y="{C[1]+14}" class="pl">C</text>'
    s += f'<text x="{C[0]-52}" y="{C[1]-6}" class="sm">40°</text>'
    # ---- 作図（こたえ） ----
    r1, rr = 80, 62
    M = _pt(B, r1, 50)
    N = _pt(B, r1, 0)
    mid = _pt(B, r1 * math.cos(math.radians(25)), 25)
    half = r1 * math.sin(math.radians(25))
    d = math.sqrt(rr * rr - half * half)
    Q_ = _pt(B, r1 * math.cos(math.radians(25)) + d, 25)
    # P = 直線BQ と 辺AC の交点
    dx, dy = math.cos(math.radians(25)), -math.sin(math.radians(25))
    ex, ey = C[0] - A_[0], C[1] - A_[1]
    det = dx * (-ey) - dy * (-ex)
    t = ((A_[0] - B[0]) * (-ey) - (A_[1] - B[1]) * (-ex)) / det
    P = (B[0] + t * dx, B[1] + t * dy)
    # 角度の確認：∠PBA=25°
    assert abs(math.degrees(math.atan2(-(P[1] - B[1]), P[0] - B[0])) - 25) < 1e-6
    # M・N を中心とする円の、Q のまわり
    thM = math.degrees(math.atan2(-(Q_[1] - M[1]), Q_[0] - M[0]))
    thN = math.degrees(math.atan2(-(Q_[1] - N[1]), Q_[0] - N[0]))
    c = _arc(B, r1, 58, -6) + _arc(M, rr, thM + 14, thM - 14) + _arc(N, rr, thN + 14, thN - 14)
    c += f'<line x1="{B[0]}" y1="{B[1]}" x2="{P[0]:.1f}" y2="{P[1]:.1f}" stroke="#000" stroke-width="1.4"/>'
    c += "".join(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="2.2" fill="#c00"/>' for p in (M, N, Q_, P))
    c += f'<text x="{P[0]+5:.1f}" y="{P[1]-3:.1f}" class="pl">P</text>'
    c += f'<text x="{M[0]-12:.1f}" y="{M[1]+4:.1f}" class="sm">M</text><text x="{N[0]+3:.1f}" y="{N[1]-4:.1f}" class="sm">N</text><text x="{Q_[0]+4:.1f}" y="{Q_[1]-3:.1f}" class="sm">Q</text>'
    return f'<svg width="320" height="215" viewBox="0 0 320 215">{s}<g class="cons">{c}</g></svg>'


def hist_svg():
    L, T, Wd, Hh = 28, 18, 232, 112
    xs = lambda v: L + (v - 5) / 7 * Wd
    ys = lambda v: T + Hh - v / 8 * Hh
    s = '<text x="2" y="12" class="sm">(人)</text>'
    for v in range(0, 9):
        s += f'<line x1="{L}" y1="{ys(v)}" x2="{L+Wd}" y2="{ys(v)}" stroke="#777" stroke-width="0.5" stroke-dasharray="2,2"/>'
        if v % 2 == 0:
            s += f'<text x="{L-5}" y="{ys(v)+3}" class="sm" text-anchor="end">{v}</text>'
    s += f'<rect x="{L}" y="{T}" width="{Wd}" height="{Hh}" fill="none" stroke="#000" stroke-width="1"/>'
    for i, c in enumerate(H1):
        s += f'<rect x="{xs(5+i):.1f}" y="{ys(c):.1f}" width="{Wd/7:.1f}" height="{Hh*c/8:.1f}" fill="#666" stroke="#000" stroke-width="1"/>'
    for v in range(5, 13):
        s += f'<text x="{xs(v):.1f}" y="{T+Hh+13}" class="sm" text-anchor="middle">{v}</text>'
    s += f'<text x="{L+Wd+6}" y="{T+Hh+13}" class="sm">(kg)</text>'
    return f'<svg width="{L+Wd+36}" height="{T+Hh+20}" viewBox="0 0 {L+Wd+36} {T+Hh+20}">{s}</svg>'


def box_svg():
    L, Wd = 14, 270
    xs = lambda v: L + (v - 5) / 7 * Wd
    s = f'<rect x="{L}" y="8" width="{Wd}" height="54" fill="none" stroke="#000" stroke-width="1"/>'
    v = 5.5
    while v < 12:
        s += f'<line x1="{xs(v):.1f}" y1="8" x2="{xs(v):.1f}" y2="62" stroke="#777" stroke-width="0.5" stroke-dasharray="2,2"/>'
        v += 0.5
    mn, q1, md, q3, mx = 5.5, 7.5, 9, 10.5, 11.5
    y0 = 35
    s += f'<line x1="{xs(mn):.1f}" y1="{y0}" x2="{xs(q1):.1f}" y2="{y0}" stroke="#000" stroke-width="1.3"/><line x1="{xs(q3):.1f}" y1="{y0}" x2="{xs(mx):.1f}" y2="{y0}" stroke="#000" stroke-width="1.3"/>'
    s += f'<line x1="{xs(mn):.1f}" y1="{y0-9}" x2="{xs(mn):.1f}" y2="{y0+9}" stroke="#000" stroke-width="1.3"/><line x1="{xs(mx):.1f}" y1="{y0-9}" x2="{xs(mx):.1f}" y2="{y0+9}" stroke="#000" stroke-width="1.3"/>'
    s += f'<rect x="{xs(q1):.1f}" y="{y0-15}" width="{xs(q3)-xs(q1):.1f}" height="30" fill="#fff" stroke="#000" stroke-width="1.3"/><line x1="{xs(md):.1f}" y1="{y0-15}" x2="{xs(md):.1f}" y2="{y0+15}" stroke="#000" stroke-width="1.3"/>'
    for t in range(5, 13):
        s += f'<text x="{xs(t):.1f}" y="76" class="sm" text-anchor="middle">{t}</text>'
    s += f'<text x="{L+Wd+4}" y="76" class="sm">(kg)</text>'
    return f'<svg width="{L+Wd+40}" height="84" viewBox="0 0 {L+Wd+40} 84">{s}</svg>'


def rect_svg():
    k = 52
    Bp, Cp, Ap, Dp = (0, 3 * k), (5 * k, 3 * k), (0, 0), (5 * k, 0)
    Ep = (4 * k, 0)
    e = (0.8, -0.6)
    dot = (Cp[0] - Bp[0]) * e[0] + (Cp[1] - Bp[1]) * e[1]
    Hp = (Bp[0] + dot * e[0], Bp[1] + dot * e[1])
    ox, oy = 16, 22
    P = lambda p: (p[0] + ox, p[1] + oy)
    ln = lambda a, b: f'<line x1="{P(a)[0]:.1f}" y1="{P(a)[1]:.1f}" x2="{P(b)[0]:.1f}" y2="{P(b)[1]:.1f}" stroke="#000" stroke-width="1.2"/>'
    s = ln(Ap, Dp) + ln(Dp, Cp) + ln(Cp, Bp) + ln(Bp, Ap) + ln(Bp, Ep) + ln(Hp, Cp)
    u1, u2 = (-0.8, 0.6), (0.6, 0.8)
    m = 8
    q = [(Hp[0] + m * u1[0], Hp[1] + m * u1[1]), (Hp[0] + m * (u1[0] + u2[0]), Hp[1] + m * (u1[1] + u2[1])), (Hp[0] + m * u2[0], Hp[1] + m * u2[1])]
    s += '<polyline points="' + " ".join(f"{P(p)[0]:.1f},{P(p)[1]:.1f}" for p in q) + '" fill="none" stroke="#000" stroke-width="1"/>'
    lab = lambda t, p, dx, dy: f'<text x="{P(p)[0]+dx:.1f}" y="{P(p)[1]+dy:.1f}" class="pl">{t}</text>'
    s += lab("A", Ap, -4, -6) + lab("E", Ep, -3, -6) + lab("D", Dp, 2, -6) + lab("H", Hp, -14, -3) + lab("B", Bp, -6, 15) + lab("C", Cp, 2, 15)
    return f'<svg width="{5*k+40}" height="{3*k+48}" viewBox="0 0 {5*k+40} {3*k+48}">{s}</svg>'


def rtri_svg():
    k = 40
    Bp, Hp, Cp = (3 * k, 0), (3 * k, 4 * k), (0, 4 * k)
    ox, oy = 22, 22
    P = lambda p: (p[0] + ox, p[1] + oy)
    s = '<polygon points="' + " ".join(f"{P(p)[0]},{P(p)[1]}" for p in (Bp, Cp, Hp)) + '" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += f'<polyline points="{P(Hp)[0]-8},{P(Hp)[1]} {P(Hp)[0]-8},{P(Hp)[1]-8} {P(Hp)[0]},{P(Hp)[1]-8}" fill="none" stroke="#000" stroke-width="1"/>'
    s += f'<text x="{P(Bp)[0]-4}" y="{P(Bp)[1]-7}" class="pl">B</text><text x="{P(Cp)[0]-14}" y="{P(Cp)[1]+13}" class="pl">C</text><text x="{P(Hp)[0]+2}" y="{P(Hp)[1]+14}" class="pl">H</text>'
    return f'<svg width="{3*k+50}" height="{4*k+46}" viewBox="0 0 {3*k+50} {4*k+46}">{s}</svg>'


def graph_svg(with_d=False):
    sc = 12
    ox, oy = 9 * sc + 12, int(11.5 * sc) + 10
    X = lambda x: ox + x * sc
    Y = lambda y: oy - y * sc
    s = f'<line x1="{X(-9)}" y1="{Y(0)}" x2="{X(5)}" y2="{Y(0)}" stroke="#000"/><line x1="{X(0)}" y1="{Y(-9.5)}" x2="{X(0)}" y2="{Y(11.5)}" stroke="#000"/>'
    s += f'<text x="{X(5)+3}" y="{Y(0)+4}" class="ax">x</text><text x="{X(0)-12}" y="{Y(11.5)+3}" class="ax">y</text>'
    s += f'<line x1="{X(-8)}" y1="{Y(11)}" x2="{X(2)}" y2="{Y(-9)}" stroke="#000" stroke-width="1.2"/>'
    s += f'<line x1="{X(-9)}" y1="{Y(-4.5)}" x2="{X(1)}" y2="{Y(10.5)}" stroke="#000" stroke-width="1.2"/>'
    s += f'<text x="{X(-8)-9}" y="{Y(11)+2}" class="pl">①</text><text x="{X(1)+2}" y="{Y(10.5)+1}" class="pl">②</text>'
    s += f'<text x="{X(-4)-12}" y="{Y(3)+4}" class="pl">A</text><text x="{X(0)+4}" y="{Y(-5)+8}" class="pl">B</text><text x="{X(0)+5}" y="{Y(9)+3}" class="pl">C</text><text x="{X(0)+4}" y="{Y(0)+12}" class="pl">O</text>'
    if with_d:
        s += f'<line x1="{X(-6)}" y1="{Y(0)}" x2="{X(0)}" y2="{Y(-5)}" stroke="#000" stroke-width="1.2"/><text x="{X(-6)-12}" y="{Y(0)-4}" class="pl">D</text>'
    w, h = 14 * sc + 44, int(21 * sc) + 26
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{s}</svg>'


# ================= 大問1 =================
def d1():
    c1 = Q("(1)", r"$3-(-4)$ を計算しなさい。", W(r"$3+4=7$"), A("7"), 9)
    c2 = Q("(2)", r"$-\dfrac{5}{6}\div10$ を計算しなさい。", W(r"$-\dfrac{5}{6}\times\dfrac{1}{10}=-\dfrac{1}{12}$"), A(r"$-\dfrac{1}{12}$"), 9)
    c3 = Q("(3)", r"方程式 $3x+4=-x-4$ を解きなさい。", W(r"$3x+x=-4-4$　$4x=-8$"), A(r"$x=-2$"), 9)
    c4 = Q("(4)", r"$2\sqrt{3}+\sqrt{27}$ を計算しなさい。", W(r"$\sqrt{27}=3\sqrt3$ だから　$2\sqrt3+3\sqrt3$"), A(r"$5\sqrt{3}$"), 9)
    c5 = Q("(5)", r"方程式 $(x-3)^2=25$ を解きなさい。", W(r"$x-3=\pm5$　$x=3\pm5$"), A(r"$x=8,\ -2$"), 9)
    c6 = Q("(6)", "頂点の数が4の角錐の名称を答えなさい。", W(r"$n$ 角錐の頂点の数は、底面の頂点 $n$ 個＋頂点1個＝$n+1$（個）。$n+1=4$ より $n=3$"), A("三角錐", "w30"), 9)
    c7 = ('<div class="q"><div class="qt"><span class="no">(7)</span>次のことがらのうち、$y$ が $x$ の関数<b>でない</b>ものを、ア〜エから1つ選び、記号で答えなさい。</div>'
          '<div class="ch">ア　分速60mで $x$ 分歩くときの進んだ道のり $y$ m<br>イ　縦5cm、横 $x$ cmの長方形の面積 $y$ cm²<br>ウ　水槽に毎分3Lずつ水を入れるときの $x$ 分後の水の量 $y$ L<br>エ　1日の最低気温が $x$ ℃のときの最高気温 $y$ ℃</div>'
          + W(r"ア $y=60x$、イ $y=5x$、ウ $y=3x$ は $x$ の値が決まると $y$ が1つに決まる。<br>エは最低気温が決まっても最高気温は1つに決まらない。") +
          f'<div class="al">答　{A("エ", "w20")}</div></div>')
    c8 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(8)</span>右の図のような、$\\angle\\mathrm{BAC}=90^\\circ$、$\\angle\\mathrm{ACB}=40^\\circ$ の直角三角形ABCにおいて、'
          '$\\angle\\mathrm{PBA}=25^\\circ$ となる辺AC上の点Pを、コンパスと定規を使って作図しなさい。作図に用いた線は消さずに残しておくこと。</div>'
          + W(r"$\angle\mathrm{ABC}=180^\circ-90^\circ-40^\circ=50^\circ$　$25^\circ=50^\circ\div2$ だから、BPは $\angle\mathrm{ABC}$ の二等分線。<br>"
              "①Bを中心とする円をかき、辺BA・BCとの交点をM・Nとする。<br>②M・Nを中心に同じ半径の円をかき、その交点をQとする。<br>③直線BQと辺ACとの交点がP。")
          + '</div><div class="fig"><b>図</b><br>' + tri_svg() + '</div></div></div>')
    return f"""<section class="page">{header("大問1　小問集合")}
<div class="lead">次の(1)〜(8)の問いに答えなさい。</div>
<div class="grid2">{c1}{c2}{c3}{c4}{c5}{c6}</div>
{c7}
{c8}
</section>"""


# ================= 大問2-1 確率 =================
def d2a():
    cells = []
    for s in SUBS:
        tot = sum(c * b for c, b in zip(COINS, s))
        mark = "".join("○" if b else "×" for b in s)
        cells.append(f'<span class="{"hit" if tot <= 100 else ""}">{mark}　{tot}円</span>')
    table = '<div class="pt16">' + "".join(cells) + "</div>"
    kai = ('<div class="frame"><b>【会話Ⅰ】</b>'
           '<p class="dl"><b>洋一：</b>表が出た硬貨の金額の合計が一番高くなるのは、すべて表が出たときだね。</p>'
           '<p class="dl"><b>静江：</b>そうだね。すべて表が出る確率は ' + BX("&emsp;&emsp;", r"$\dfrac{1}{16}$") + ' だよ。</p>'
           '<p class="dl"><b>洋一：</b>そのときの金額の合計は660円になるね。</p>'
           r'<p class="dl"><b>静江：</b>そうすると、100円以下になる確率は $\dfrac{1}{6}$ より小さいのかな。</p>'
           '<p class="dl"><b>洋一：</b>どうだろう。100円以下になる硬貨の表裏の出かたが何通りあるか調べて、その確率を求めてみよう。</p></div>')
    q1 = Q("(1)", "【会話Ⅰ】の " + BX("&emsp;&emsp;", r"$\dfrac{1}{16}$") + " に当てはまる数を答えなさい。",
           W(r"4枚の硬貨の表裏の出かたは全部で $2\times2\times2\times2=16$（通り）。すべて表になるのは1通り。"), A(r"$\dfrac{1}{16}$", "w20"), 22)
    q2 = Q("(2)", "表が出た硬貨の合計金額が100円以下になる確率を求めなさい。",
           W("表を○、裏を×として、（500円・100円・50円・10円）の表裏の出かたを全部調べる（ピンクが100円以下）。" + table +
             r"100円以下になるのは5通り（すべて裏＝0円、10円、50円、60円、100円）。500円が表だと500円以上になるので入らない。"), A(r"$\dfrac{5}{16}$", "w20"), 80)
    return f"""<section class="page">{header("大問2-1　確率")}
<div class="lead">500円硬貨、100円硬貨、50円硬貨、10円硬貨がそれぞれ1枚ずつある。4枚の硬貨を同時に1回投げる。【会話Ⅰ】は、表が出た硬貨の金額の合計がいくらになるか、洋一さんと静江さんが話し合っている場面である。<br>
このとき、下の(1)、(2)の問いに答えなさい。ただし、どの硬貨も表裏の出かたは同様に確からしいとする。</div>
{kai}{q1}{q2}
</section>"""


# ================= 大問2-2 連立方程式 =================
def d2b():
    kai = ('<div class="frame"><b>【会話Ⅱ】</b>'
           '<p class="dl"><b>洋一：</b>参加賞のボールペンは全部で121本用意したんだったね。</p>'
           '<p class="dl"><b>静江：</b>子ども会には小学生と中学生が参加して、参加者の人数は合わせて31人だったよ。</p>'
           '<p class="dl"><b>洋一：</b><span class="ul">①小学生には1人3本、中学生には1人5本ずつ配ったら</span>、参加者全員にちょうど配ることができたんだ。</p>'
           '<p class="dl"><b>静江：</b><span class="ul">②小学生と中学生は、それぞれ何人ずつ参加したのかな。</span></p></div>')
    q1 = Q("(1)", r"下線部①について、子ども会に参加した小学生を $x$ 人、中学生を $y$ 人とし、配ったボールペンの本数を、$x,\ y$ を用いた最も簡単な式で表しなさい。",
           W(r"小学生：$3\times x=3x$（本）　中学生：$5\times y=5y$（本）"), A(r"$(3x+5y)$ 本", "w30"), 24)
    q2 = Q("(2)", r"下線部②について、子ども会に参加した小学生と中学生の人数を、連立方程式を使ってそれぞれ求めなさい。ただし、子ども会に参加した小学生を $x$ 人、中学生を $y$ 人とし、答えを求める過程がわかるように、式と計算も書きなさい。",
           W(r"人数：$x+y=31$　ボールペン：$3x+5y=121$<br>"
             r"$\begin{cases}x+y=31\\3x+5y=121\end{cases}$　上の式を3倍すると $3x+3y=93$<br>"
             r"$3x+5y=121$ から $3x+3y=93$ をひくと　$2y=28$　$y=14$<br>$x+y=31$ に代入して　$x=17$<br>（3×17＋5×14＝121 で問題に合う）"),
           "小学生：" + A("17人", "w20") + "　中学生：" + A("14人", "w20"), 90)
    return f"""<section class="page">{header("大問2-2　連立方程式の利用")}
<div class="lead">洋一さんと静江さんは、地域の子ども会に参加した。【会話Ⅱ】は、2人がそのときに配られた参加賞のボールペンの本数について話し合っている場面である。<br>このとき、下の(1)、(2)の問いに答えなさい。</div>
{kai}{q1}{q2}
</section>"""


# ================= 大問3 データの活用 =================
def d3():
    kai1 = ('<div class="frame"><b>【会話Ⅰ】</b>'
            '<p class="dl"><b>由佳：</b>私たちのクラスの生徒35人を対象に、通学に使用しているカバンの重さを調査した結果をヒストグラムで表したよ。</p>'
            '<p class="dl"><b>康平：</b>このヒストグラムから、カバンの重さが8kg未満の人が ' + BX("①", "12") + ' 人いることがわかるね。</p>'
            '<p class="dl"><b>由佳：</b>このヒストグラムから、カバンの重さの最頻値を求めると ' + BX("②", "9.5") + ' kgだね。</p>'
            '<p class="dl"><b>康平：</b>同じデータを、<span class="ul">度数分布表</span>にまとめるとどうなるかな。</p></div>')
    tb = ('<table class="tb"><tr><th colspan="2">表</th></tr><tr><th>重さ(kg)</th><th>人数(人)</th></tr>'
          '<tr><td>2〜4</td><td>0</td></tr><tr><td>4〜6</td><td><i>a</i></td></tr><tr><td>6〜8</td><td>11</td></tr>'
          '<tr><td>8〜10</td><td>13</td></tr><tr><td>10〜12</td><td><i>b</i></td></tr><tr><td>合計</td><td>35</td></tr></table>'
          '<div style="font-size:8pt;text-align:center">（以上〜未満）</div>')
    r1 = Q("(1)", "【会話Ⅰ】の " + BX("①", "12") + " に当てはまる数を答えなさい。",
           W(r"8kg未満の階級（5〜6、6〜7、7〜8）の人数をたす。$1+5+6=12$"), A("12", "w20"), 8)
    r2 = Q("(2)", "【会話Ⅰ】の " + BX("②", "ウ") + " に当てはまる数として適切なものを、次のア〜エから1つ選び、記号で答えなさい。"
           '<div class="ch row">ア　7.5　　　イ　8　　　ウ　9.5　　　エ　12</div>',
           W(r"最頻値は、度数がもっとも多い階級（9kg以上10kg未満・8人）の階級値。$(9+10)\div2=9.5$"), A("ウ", "w20"), 8)
    r3 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(3)</span>右の表は、【会話Ⅰ】の下線部について、康平さんが同じデータを使って度数分布表にまとめたものである。'
          '$a,\\ b$ に当てはまる数の組み合わせとして正しいものを、次のア〜エの中から1つ選び、その記号を書きなさい。</div>'
          '<div class="ch">ア　$a$　0　　$b$　7<br>イ　$a$　0　　$b$　10<br>ウ　$a$　1　　$b$　7<br>エ　$a$　1　　$b$　10</div>'
          + W(r"$a$（4kg以上6kg未満）＝5〜6kgの1人　$b$（10kg以上12kg未満）＝$7+3=10$（人）") +
          f'</div><div class="fig">{tb}</div></div><div class="al">答　{A("エ", "w20")}</div></div>')
    p1 = f"""<section class="page">{header("大問3　データの活用", "1/2")}
<div class="lead">由佳さんと康平さんは、クラスの生徒35人について、通学に使用しているカバンの重さを調べることにした。<br>このとき、後の1、2の問いに答えなさい。</div>
<div class="lead"><b>1</b>　図Ⅰは、カバンの重さをヒストグラムにまとめたものである。例えば、カバンの重さが5kg以上6kg未満の生徒は1人いたことがわかる。次の【会話Ⅰ】は、2人がヒストグラムについて話し合っている場面である。下の(1)〜(3)の問いに答えなさい。</div>
<div style="text-align:center;font-size:9pt"><b>図Ⅰ</b><br>{hist_svg()}</div>
{kai1}{r1}{r2}{r3}
</section>"""
    kai2 = ('<div class="frame"><b>【会話Ⅱ】</b>'
            '<p class="dl"><b>由佳：</b>箱ひげ図にすると、<span class="ul">①中央値</span>がはっきりするね。</p>'
            '<p class="dl"><b>康平：</b>うん。他にも最大値や最小値を示せるメリットがあるよ。</p>'
            '<p class="dl"><b>由佳：</b><span class="ul">②四分位範囲</span>から、散らばり具合もよくわかるね。</p>'
            '<p class="dl"><b>康平：</b>同じデータでも、表し方によってわかることが違うのはおもしろいね。</p></div>')
    s1 = Q("(1)", "【会話Ⅱ】の下線部①について、適切な値を求めなさい。",
           W(r"箱の中の線（中央値）の位置は9kg。（35人の18番目の値で、ヒストグラムでも9kg以上10kg未満の階級にある）"), A("9 kg", "w20"), 22)
    s2 = Q("(2)", "【会話Ⅱ】の下線部②について、四分位範囲を求めなさい。ただし、第1四分位数と第3四分位数を示して、式と計算も書きなさい。",
           W(r"第1四分位数は 7.5 kg、第3四分位数は 10.5 kg。<br>（四分位範囲）＝（第3四分位数）−（第1四分位数）＝$10.5-7.5=3$"), A("3 kg", "w20"), 60)
    p2 = f"""<section class="page">{header("大問3　データの活用", "2/2")}
<div class="lead"><b>2</b>　由佳さんは、カバンの重さについて、1と同じデータを使って、図Ⅱのように箱ひげ図に表した。【会話Ⅱ】は、図Ⅱを見ながら2人が話し合っている場面である。<br>このとき、下の(1)、(2)の問いに答えなさい。ただし、カバンの重さは0.5kg単位で量ったものとする。</div>
<div style="text-align:center;font-size:9pt"><b>図Ⅱ</b><br>{box_svg()}</div>
{kai2}{s1}{s2}
</section>"""
    return p1 + p2


# ================= 大問4 図形 =================
def d4():
    proof = lines(r"△ABEと△HCBで、<br>仮定より　BE＝CB　……①<br>長方形の角だから $\angle\mathrm{BAE}=90^\circ$、CH⊥BE だから $\angle\mathrm{CHB}=90^\circ$　よって $\angle\mathrm{BAE}=\angle\mathrm{CHB}=90^\circ$　……②<br>"
                  r"AD∥BC で、平行線の錯角は等しいから　$\angle\mathrm{AEB}=\angle\mathrm{HBC}$　……③<br>①、②、③より、直角三角形の斜辺と1つの鋭角がそれぞれ等しいから、△ABE≡△HCB", 62)
    q1 = Q("1", "△ABE≡△HCBであることを証明しなさい。", proof, "", 0)
    q2 = Q("2", r"点CとEを結ぶ。$\angle\mathrm{ABE}=60^\circ$ のとき、$\angle\mathrm{CEH}$ の大きさを求めなさい。",
           W(r"$\angle\mathrm{EBC}=90^\circ-60^\circ=30^\circ$。BE＝BC より △BCE は二等辺三角形だから<br>"
             r"$\angle\mathrm{BEC}=(180^\circ-30^\circ)\div2=75^\circ$。点Hは線分BE上にあるので $\angle\mathrm{CEH}=\angle\mathrm{BEC}=75^\circ$"),
           A(r"$75^\circ$", "w20"), 28)
    p1 = f"""<section class="page">{header("大問4　図形（合同・面積）", "1/2")}
<div class="flex"><div class="grow"><div class="lead">図Ⅰは、長方形ABCDにおいて、辺AD上にBE＝BCとなる点Eをとったものである。また、点Cから線分BEにひいた垂線と線分BEとの交点をHとする。<br>このとき、後の1〜3の問いに答えなさい。</div></div>
<div class="fig"><b>図Ⅰ</b><br>{rect_svg()}</div></div>
{q1}{q2}
</section>"""
    t1 = Q("(1)", "四角形EHCDの面積は、長方形ABCDの面積の何倍か求めなさい。",
           W(r"AB＝3cm、AE＝4cm、AE：BC＝4：5 より BC＝5cm。長方形ABCD＝$3\times5=15$（cm²）<br>"
             r"△ABE＝$\dfrac12\times3\times4=6$（cm²）。△ABE≡△HCB より △HCB＝6cm²<br>"
             r"四角形EHCD＝$15-6-6=3$（cm²）　$3\div15=\dfrac15$"), A(r"$\dfrac{1}{5}$ 倍", "w20"), 52)
    t2 = Q("(2)", r"図Ⅱは、図Ⅰから△BCHを取り出したものである。△BCHを、直線BHを軸として1回転させてできる立体の体積を求めなさい。ただし、円周率は $\pi$ とする。",
           W(r"△ABE≡△HCB より HC＝AB＝3cm、BH＝AE＝4cm（BE＝BC＝5cm）<br>"
             r"底面の半径がCH＝3cm、高さがBH＝4cm の円錐ができる。<br>$\dfrac13\times\pi\times3^2\times4=12\pi$"), A(r"$12\pi$ cm³", "w20"), 40)
    p2 = f"""<section class="page">{header("大問4　図形（合同・面積）", "2/2")}
<div class="q"><div class="qt"><span class="no">3</span>AE：BC＝4：5、AB＝3cm、AE＝4cmであるとき、次の(1)、(2)の問いに答えなさい。</div></div>
{t1}
<div class="flex"><div class="grow">{t2}</div><div class="fig"><b>図Ⅱ</b><br>{rtri_svg()}</div></div>
</section>"""
    return p1 + p2


# ================= 大問5 一次関数 =================
def d5():
    intro = (r'<div class="lead">図Ⅰのように、2つの関数 $y=ax-5\ (a<0)$ …①、$y=\dfrac32x+9$ …②のグラフが点A$(-4,\ 3)$ で交わっている。①のグラフと $y$ 軸との交点をBとし、②のグラフと $y$ 軸との交点をCとする。<br>このとき、次の1〜3の問いに答えなさい。</div>')
    q1 = Q("1", r"$a$ の値を求めなさい。", W(r"①は点A$(-4,\ 3)$ を通るから　$3=a\times(-4)-5$　$-4a=8$"), A(r"$a=-2$", "w20"), 28)
    q2 = Q("2", "△ABCの面積を求めなさい。",
           W(r"B$(0,\ -5)$、C$(0,\ 9)$ より BC＝$9-(-5)=14$。BCを底辺とすると、高さは点Aの $x$ 座標の絶対値4<br>$\dfrac12\times14\times4=28$"), A("28", "w20"), 40)
    q3a = Q("(1)", "点Dの座標を求めなさい。",
            W(r"②は $y=\dfrac32x+9$。$x$ 軸との交点だから $y=0$ を代入して　$0=\dfrac32x+9$　$x=-6$"), A("D$(-6,\\ 0)$", "w20"), 30)
    q3b = Q("(2)", r"$y$ 軸の負の部分に点Eを、△ADBの面積と△AEBの面積が等しくなるようにとる。このとき、点Eの $y$ 座標を求めなさい。",
            W(r"△ADB：A$(-4,3)$、D$(-6,0)$、B$(0,-5)$ の面積は14。（BDを結ぶ直線やAを通る長方形で囲んで求めてもよい）<br>"
              r"△AEB は BE を底辺とすると高さは4だから $\dfrac12\times\mathrm{BE}\times4=14$　BE＝7<br>"
              r"EはBより下にあるので（$y$ 軸の負の部分）　$y=-5-7=-12$"), A("$-12$", "w20"), 40)
    q3 = ('<div class="q"><div class="qt"><span class="no">3</span>図Ⅱは、図Ⅰにおいて、②のグラフと $x$ 軸との交点をDとし、点BとDを結んだものである。<br>このとき、次の(1)、(2)の問いに答えなさい。</div></div>')
    return f"""<section class="page">{header("大問5　一次関数")}
<div class="flex"><div class="grow">{intro}{q1}{q2}</div><div class="fig"><b>図Ⅰ</b><br>{graph_svg()}</div></div>
<div class="flex"><div class="grow">{q3}{q3a}{q3b}</div><div class="fig"><b>図Ⅱ</b><br>{graph_svg(True)}</div></div>
</section>"""


JOBS = [("c3_jitsu2_d1", d1), ("c3_jitsu2_kakuritsu", d2a), ("c3_jitsu2_renritsu", d2b),
        ("c3_jitsu2_data", d3), ("c3_jitsu2_zukei", d4), ("c3_jitsu2_ichiji", d5)]

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
