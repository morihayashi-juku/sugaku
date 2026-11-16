"""実力テスト 令和3年度 3年・10月（大問1〜5）を、大問1／単元別の PDF にする。
問題（pdf/c3_jitsu_r310_*.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
部品・CSS は c3_jitsu_test.py などと共通。common.json の jitsu.tests の id は r3-3-10。

  大問1   小問集合（度数分布表・円の中心の作図）           c3_jitsu_r310_d1
  大問2-1 確率（玉の取り出し・積が6の倍数）               c3_jitsu_r310_kakuritsu
  大問2-2 方程式の利用（ダンスコンテストの交代時間）       c3_jitsu_r310_renritsu
  大問3-1 比例と反比例（反比例の性質）                     c3_jitsu_r310_hirei
  大問3-2 一次関数（直線と三角形の面積・等積変形）         c3_jitsu_r310_ichiji
  大問4   平面図形（角の二等分線・合同・長さ・面積比）     c3_jitsu_r310_zukei
  大問5   空間図形（正四角錐）                             c3_jitsu_r310_kuukan

実行：cd tools && python3 c3_jitsu_r310.py
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

# ================= 答えの確認 =================
assert -2 + 7 == 5 and (-1) ** 3 * 4 == -4
assert all(3 * (-3 * x + y) + 5 * (2 * x - y) == x - 2 * y for x in range(3) for y in range(3))
assert all((x + 4) * (x - 4) - x * x == -16 for x in range(5))
assert 4 + 3 == 7                                             # 20/√5＝4√5、√45＝3√5
assert all(x * x - 7 * x + 6 == 0 for x in (1, 6)) and (2 * -1 - 5, 2 * 4 - 5) == (-7, 3)
FREQ = [7, 5, 2, 3, 2, 1]
cum = [sum(FREQ[:i + 1]) for i in range(6)]
assert cum[0] < 10 and cum[1] >= 11 and F(cum[2], 20) == F(7, 10)       # 中央値は28〜32の階級、イの累積相対度数0.7
BA, BB = [2, 3, 4, 5, 6], [6, 7, 8, 9]
pa = list(combinations(BA, 2))
assert len(pa) == 10 and F(sum(a + b >= 8 for a, b in pa), 10) == F(3, 5)
pA = F(sum(a * b % 6 == 0 for a, b in pa), 10)
pB = F(sum(a * b % 6 == 0 for a, b in combinations(BB, 2)), 6)
assert (pA, pB) == (F(3, 5), F(2, 3)) and pB > pA
assert 6 * 6 + 5 * 4 == 56 and 15 * 7 + 14 * 5 == (12 * 60 + 25) - (9 * 60 + 30)
assert (6 + 3, -2 + 3) == (9, 1) and F(1, 2) * 3 * (6 + 2) == 12
assert F(6 - 9, 0 - (-6)) == F(-1, 2) and F(1, 2) * (6 - 3) * 8 == 12
assert 180 - 65 - 37 == 78 and 78 // 2 == 39
assert 15 * 3 // 5 == 9
S_ABD, S_ACD = 2, 3                                           # BD：DC＝2：3
S_BED = S_ACD - S_ABD
assert F(S_BED * 3, 2) / S_ABD == F(3, 4)
assert F(1, 3) * 12 * 3 == 12 and 12 + 4 * F(1, 2) * 12 == 36   # 1辺 2√3、側面1つ ½×2√3×2√3＝6
assert 3 ** 2 + 3 == 12                                       # 高さ² ＋ (半分の辺)² ＝ (2√3)²

TAG = "令和3年度　3年・10月"


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
def circ_svg():
    """∠ABC と点P。作図（Pを通るBCの垂線、∠ABCの二等分線 → 交点O）は .cons"""
    B_, C_, P_ = (20, 170), (275, 170), (190, 170)
    ang = 54
    A_ = (B_[0] + 210 * math.cos(math.radians(ang)), B_[1] - 210 * math.sin(math.radians(ang)))
    s = L(B_, A_, 1.3) + L(B_, C_, 1.3) + f'<circle cx="{P_[0]}" cy="{P_[1]}" r="2.2"/>'
    s += T(A_[0] + 8, A_[1] + 2, "A") + T(B_[0] - 8, B_[1] + 4, "B") + T(C_[0] + 9, C_[1] + 4, "C") + T(P_[0], P_[1] + 15, "P")
    r = 30
    c = _arc(P_, r, 175, 140) + _arc(P_, r, 40, 5)
    X1, X2 = (P_[0] - r, P_[1]), (P_[0] + r, P_[1])
    up = (P_[0], P_[1] - 40)
    c += arc_at(X1, 50, up, 10) + arc_at(X2, 50, up, 10)
    c += L((P_[0], P_[1] + 4), (P_[0], 10), 0.9, True)
    # 角の二等分線
    rb = 45
    c += _arc(B_, rb, ang + 6, -6)
    Y1, Y2 = (B_[0] + rb, B_[1]), (B_[0] + rb * math.cos(math.radians(ang)), B_[1] - rb * math.sin(math.radians(ang)))
    h = ang / 2
    t = (B_[0] + 80 * math.cos(math.radians(h)), B_[1] - 80 * math.sin(math.radians(h)))
    c += arc_at(Y1, 45, t, 9) + arc_at(Y2, 45, t, 9)
    O = (P_[0], B_[1] - (P_[0] - B_[0]) * math.tan(math.radians(h)))
    c += L(B_, (B_[0] + (O[0] - B_[0]) * 1.2, B_[1] + (O[1] - B_[1]) * 1.2), 0.9, True)
    c += f'<circle cx="{O[0]:.1f}" cy="{O[1]:.1f}" r="2.8" fill="#c00"/>' + T(O[0] + 10, O[1] - 4, "O")
    c += f'<circle cx="{O[0]:.1f}" cy="{O[1]:.1f}" r="{B_[1] - O[1]:.1f}" fill="none" stroke-dasharray="2 3" stroke-width="0.8"/>'
    return svg(300, 185, s + f'<g class="cons">{c}</g>', 0, 0)


def balls_svg():
    def box(x, y, w, h, lab, balls):
        s = f'<path d="M{x + 6} {y} H{x} V{y + h} H{x + w} V{y} H{x + w - 6}" fill="none" stroke="#000" stroke-width="1.1"/>'
        s += T(x - 2, y - 4, lab, "", "start")
        for (bx, by, n) in balls:
            s += f'<circle cx="{x + bx}" cy="{y + by}" r="10" fill="#fff" stroke="#000" stroke-width="1"/>' + T(x + bx, y + by + 5, str(n))
        return s
    s = box(4, 18, 76, 62, "A", [(16, 18, 2), (38, 18, 3), (60, 28, 6), (20, 42, 4), (42, 42, 5)])
    s += box(4, 108, 76, 62, "B", [(18, 20, 6), (48, 18, 7), (26, 44, 8), (54, 42, 9)])
    return svg(90, 176, s)


def black(x, y, n, r=7.5):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#000"/><text x="{x}" y="{y + 3.6}" text-anchor="middle" font-size="{9 if n < 10 else 7.5}" fill="#fff" font-weight="700">{n}</text>'


def flow_svg(cells, left="", right="", gap_after=None):
    """発表・交代時間の帯。cells は ('発', n) か ('交',)。gap_after の後ろに「……」をはさむ"""
    cw, ch, x, y0 = 24, 108, 4, 16
    s = ""
    for i, c in enumerate(cells):
        s += f'<rect x="{x}" y="{y0}" width="{cw}" height="{ch}" fill="#fff" stroke="#000" stroke-width="1"/>'
        if c[0] == "発":
            s += T(x + cw / 2, y0 + 22, "発", "sm") + T(x + cw / 2, y0 + 40, "表", "sm") + black(x + cw / 2, y0 + 58, c[1])
        else:
            s += "".join(T(x + cw / 2, y0 + 22 + 17 * k, ch_, "sm") for k, ch_ in enumerate("交代時間"))
        x += cw
        if gap_after is not None and i == gap_after:
            s += T(x + 14, y0 + ch / 2, "……", "sm")
            x += 28
    if left:
        s += T(4, y0 - 4, left, "sm", "start")
    if right:
        s += T(x, y0 - 4, right, "sm", "end")
    return svg(x + 6, y0 + ch + 4, s)


def line_svg():
    sc = 15
    ox, oy = 8 + 8 * sc, 11 * sc
    X = lambda x: ox + x * sc
    Y = lambda y: oy - y * sc
    s = L((X(-8), Y(0)), (X(5), Y(0)), 1) + L((X(0), Y(-2)), (X(0), Y(10.5)), 1)
    s += T(X(5) + 6, Y(0) + 4, '<tspan class="ax">x</tspan>', "pl") + T(X(0) + 2, Y(10.5) - 2, '<tspan class="ax">y</tspan>', "pl", "start")
    s += T(X(0) - 7, Y(0) + 12, "O", "sm") + T(X(-6), Y(0) + 13, "−6", "sm") + T(X(2), Y(0) + 13, "2", "sm")
    s += L((X(-7), Y(10)), (X(4.6), Y(-1.6)), 1.2)
    s += L((X(-6), Y(9)), (X(-6), Y(0)), 0.7, True) + L((X(2), Y(1)), (X(2), Y(0)), 0.7, True)
    s += f'<circle cx="{X(-6)}" cy="{Y(9)}" r="2.2"/><circle cx="{X(2)}" cy="{Y(1)}" r="2.2"/>'
    s += T(X(-6), Y(9) - 6, "A") + T(X(2) - 2, Y(1) - 7, "B")
    c = L((X(-6), Y(9)), (X(1.5), Y(5.25)), 1.1) + L((X(0), Y(0)), (X(-6), Y(9)), 0.8, True) + L((X(0), Y(0)), (X(2), Y(1)), 0.8, True)
    c += L((X(0), Y(6)), (X(2), Y(1)), 0.8, True) + f'<circle cx="{X(0)}" cy="{Y(6)}" r="2.6" fill="#c00"/>' + T(X(0) + 12, Y(6) - 2, "P")
    return svg(X(5) + 18, Y(-2) + 4, s + f'<g class="cons">{c}</g>')


def bis_svg():
    k = 17
    P = lambda x, y: (40 + x * k, 12 + (8.6 - y) * k)
    A_, B_, C_, D_, E_ = P(4, 8.25), P(0, 0), P(15, 0), P(6, 0), P(-2, -4.125)
    s = f'<polygon points="{A_[0]},{A_[1]} {B_[0]},{B_[1]} {C_[0]},{C_[1]}" fill="none" stroke="#000" stroke-width="1.2"/>'
    s += L(A_, D_) + L(B_, E_) + L(E_, D_) + L(E_, C_)
    s += T(A_[0], A_[1] - 4, "A") + T(B_[0] - 9, B_[1] + 2, "B") + T(C_[0] + 9, C_[1] + 3, "C") + T(D_[0] + 2, D_[1] + 14, "D") + T(E_[0] - 6, E_[1] + 12, "E")
    return svg(int(C_[0]) + 22, int(E_[1]) + 18, s)


def pyr_svg():
    A_, B_, C_, D_, E_ = (120, 14), (14, 182), (172, 182), (226, 126), (68, 126)
    Oc = ((B_[0] + D_[0]) / 2, (B_[1] + D_[1]) / 2)
    Mcd = ((C_[0] + D_[0]) / 2, (C_[1] + D_[1]) / 2)
    s = "".join(L(p, q, 1.2) for p, q in [(A_, B_), (A_, C_), (A_, D_), (B_, C_), (C_, D_)])
    s += "".join(L(p, q, 0.8, True) for p, q in [(A_, E_), (B_, E_), (E_, D_), (B_, D_), (C_, E_), (A_, Oc), (A_, Mcd)])
    s += right_mark(Oc, (1, 0), (0, -1), 5) + right_mark(Mcd, (-0.72, -0.69), (-0.69, 0.72), 5)
    s += T(A_[0], A_[1] - 4, "A") + T(B_[0] - 8, B_[1] + 4, "B") + T(C_[0] + 2, C_[1] + 14, "C") + T(D_[0] + 9, D_[1] + 3, "D") + T(E_[0] - 6, E_[1] - 3, "E")
    s += T(Oc[0] - 18, (A_[1] + Oc[1]) / 2 + 10, "3cm", "sm") + T(Mcd[0] + 6, (A_[1] + Mcd[1]) / 2 - 6, "2√3cm", "sm", "start")
    return svg(262, 196, s)


# ================= 大問1 =================
def d1():
    c = [Q("(1)", r"$-2+7$ を計算しなさい。", "", A("5"), 1),
         Q("(2)", r"$(-1)^3\times4$ を計算しなさい。", W(r"$(-1)\times4$"), A("$-4$"), 1),
         Q("(3)", r"$3(-3x+y)+5(2x-y)$ を計算しなさい。", W(r"$-9x+3y+10x-5y$"), A(r"$x-2y$"), 1),
         Q("(4)", r"$(x+4)(x-4)-x^2$ を計算しなさい。", W(r"$x^2-16-x^2$"), A("$-16$"), 1),
         Q("(5)", r"$\dfrac{20}{\sqrt5}+\sqrt{45}$ を計算しなさい。", W(r"$\dfrac{20\sqrt5}{5}+3\sqrt5=4\sqrt5+3\sqrt5$"), A(r"$7\sqrt5$"), 1),
         Q("(6)", r"二次方程式 $x^2-7x+6=0$ を解きなさい。", W(r"$(x-1)(x-6)=0$"), A(r"$x=1,\ 6$"), 1)]
    c7 = Q("(7)", r"一次関数 $y=2x-5$ について、$x$ の変域が $-1\leqq x\leqq4$ のときの $y$ の変域を求めなさい。",
           W(r"$x=-1$ のとき $y=-7$、$x=4$ のとき $y=3$（傾きが正なので増加）"), A(r"$-7\leqq y\leqq3$"), 1)
    rows = [("24 〜 28", 7, "0.35"), ("28 〜 32", 5, "0.25"), ("32 〜 36", 2, "0.10"), ("36 〜 40", 3, "0.15"), ("40 〜 44", 2, "0.10"), ("44 〜 48", 1, "0.05")]
    tb = ('<table class="tb" style="font-size:8.6pt"><tr><th>年齢(歳)</th><th>度数(人)</th><th>相対度数</th></tr><tr><td>以上　未満</td><td></td><td></td></tr>'
          + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{r}</td></tr>" for a, b, r in rows)
          + '<tr><td>計</td><td>20</td><td>1.00</td></tr></table>')
    c8 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(8)</span>右の表は、あるソフトボールチームに所属する選手20人の年齢について、度数および相対度数をまとめたものである。'
          'この表から、<b>かならずいえること</b>として適切なものを、次のア〜エから1つ選び、記号で答えなさい。'
          '<div class="ch">ア　選手の年齢の中央値は36歳である。<br>イ　32歳以上36歳未満の階級の累積相対度数は0.7である。<br>'
          'ウ　選手の年齢の最小値は24歳である。<br>エ　選手の年齢の最頻値は46歳である。</div></div>'
          + W("ア：10番目・11番目はどちらも28〜32の階級　イ：0.35＋0.25＋0.10＝0.70 ○<br>ウ：24歳以上というだけで、24歳の人がいるとはかぎらない　エ：最頻値は26歳（24〜28の階級値）")
          + f'<div class="al">答　{A("イ", "w20")}</div></div><div class="fig">{tb}</div></div></div>')
    c9 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(9)</span>右の図のように、∠ABCがあり、線分BC上に点Pがある。'
          '点Pで線分BCに接し、線分ABにも接する円の中心Oを、コンパスと定規を使って作図しなさい。作図に用いた線は消さずに残しておくこと。</div>'
          + W("円の中心は、接点Pを通るBCの垂線の上にあり、2辺AB・BCから等しい距離にあるので∠ABCの二等分線の上にもある。<br>"
              "①点Pを通る線分BCの垂線をひく。<br>②∠ABCの二等分線をひく。<br>③①と②の交点がO。")
          + f'</div><div class="fig">{circ_svg()}</div></div></div>')
    return f"""<section class="page tight">{header("大問1　小問集合")}
<div class="lead">次の(1)〜(9)の問いに答えなさい。</div>
<div class="grid2">{"".join(c)}</div>
{c7}{c8}{c9}
</section>"""


# ================= 大問2-1 確率 =================
def d2a():
    task = ('<b>【課題】</b><div class="frame"><div class="flex"><div class="grow">右の図のように、2、3、4、5、6の数字が、それぞれ書かれた玉が1個ずつはいっている箱Aと、'
            '6、7、8、9の数字が、それぞれ書かれた玉が1個ずつはいっている箱Bがある。<br>'
            '(Ⅰ)　箱Aの中から同時に2個の玉を取り出すとき、取り出した2個の玉に書かれた数の和が8以上になる確率を求めなさい。ただし、どの玉の取り出し方も同様に確からしいとする。<br>'
            '(Ⅱ)　箱A、Bそれぞれにおいて、箱から同時に2個の玉を取り出すとき、取り出した2個の玉に書かれた数の積が6の倍数になりやすいのはどちらか、答えなさい。ただし、どの玉の取り出し方も同様に確からしいとする。'
            f'</div><div class="fig">{balls_svg()}</div></div></div>')
    d = lambda who, t: f'<p class="dl"><b>{who}：</b>{t}</p>'
    kaiwa = ('<b>【会話】</b><div class="frame">'
             + d("そうた", "(Ⅰ)について、取り出す2個の玉の組み合わせは全部で " + BX("①", "10") + " 通り、求める確率は " + BX("②", r"$\dfrac35$") + " だと思うよ。")
             + d("すず", "そうだね。(Ⅱ)はどのように考えればよいのかな。")
             + d("そうた", "(Ⅰ)は樹形図を使って考えたよ。(Ⅱ)も同じ方法で考えたらいいと思うな。")
             + d("すず", "うーん、樹形図をかくのは面倒だし、工夫したら求められないかな。2個の玉に書かれた数の積を考えると、箱Aでは、2×3＝6、3×4＝12、4×5＝20、5×6＝30の4通りの中で、6の倍数は3つあるから…。")
             + d("そうた", "ちょっと待って！きちんと樹形図をかいて考えてみようよ。") + '</div>')
    q1 = Q("(1)", "【会話】の中の ①、② にあてはまる数の組み合わせとして適切なものを、次のア〜エから1つ選び、記号で答えなさい。"
           r'<div class="ch">ア　①4　②$\dfrac12$　　　イ　①4　②$\dfrac35$　　　ウ　①10　②$\dfrac12$　　　エ　①10　②$\dfrac35$</div>',
           W("組み合わせ：{2,3}{2,4}{2,5}{2,6}{3,4}{3,5}{3,6}{4,5}{4,6}{5,6} の10通り<br>"
             "和が8以上：{2,6}{3,5}{3,6}{4,5}{4,6}{5,6} の6通り　$\\dfrac{6}{10}=\\dfrac35$"),
           A("エ", "w20"), 2)
    q2 = Q("(2)", "【課題】(Ⅱ)について、取り出した2個の玉に書かれた数の積が6の倍数になりやすいのはどちらか、答えなさい。また、その理由を、確率を求めて説明しなさい。",
           '<div style="margin-bottom:1mm">（答）' + A("箱B", "w20") + "</div>"
           + lines(r"箱A：10通りのうち、積が6の倍数になるのは {2,3}{2,6}{3,4}{3,6}{4,6}{5,6} の6通りで、確率は $\dfrac{6}{10}=\dfrac35$<br>"
                   r"箱B：{6,7}{6,8}{6,9}{7,8}{7,9}{8,9} の6通りのうち、6の倍数は {6,7}{6,8}{6,9}{8,9} の4通りで、確率は $\dfrac46=\dfrac23$<br>"
                   r"$\dfrac35=\dfrac{9}{15}$、$\dfrac23=\dfrac{10}{15}$ で、$\dfrac23$ のほうが大きいから、箱Bのほうが6の倍数になりやすい。", 36),
           "", 0)
    return f"""<section class="page tight">{header("大問2-1　確率")}
<div class="lead"><b>1</b>　そうたさんとすずさんは、次の【課題】について考えた。下の【会話】は、2人が話し合っている場面の一部である。このとき、下の(1)、(2)の問いに答えなさい。</div>
{task}{kaiwa}{q1}{q2}
</section>"""


# ================= 大問2-2 方程式の利用 =================
def d2b():
    last = [("発", i // 2 + 1) if i % 2 == 0 else ("交",) for i in range(11)]
    fig1 = flow_svg(last, "10：00")
    fig2 = flow_svg([("発", 1), ("交",), ("発", 2), ("交",), ("発", 14), ("交",), ("発", 15)], "9：30", "12：25", gap_after=3)
    memo = ('<div class="frame" style="font-size:8.6pt;line-height:1.8;white-space:nowrap"><b>【メモ】</b><br>□　参加は15グループ<br>□　発表時間は一定で、それぞれ7分ずつ<br>'
            '□　最初のグループの発表が始まる時刻は9時30分<br>□　最後のグループの発表が終わる時刻は12時25分<br>□　交代時間も一定とする。</div>')
    q1 = Q("(1)", "昨年のダンスコンテストで、最後のグループの発表が終わった時刻は何時何分か、答えなさい。",
           W(r"発表6回で $6\times6=36$（分）、交代時間は5回で $4\times5=20$（分）。合わせて56分なので、10時の56分後"), A("10時56分", "w20"), 10)
    q2 = Q("(2)", "実行委員会では、今年のダンスコンテストについて話し合い、下の【メモ】のような内容が決定している。このとき、1回の交代時間を何分にすればよいか、方程式を使って求めなさい。"
           "ただし、答えを求める過程がわかるように、式と計算、説明も書きなさい。"
           f'<div class="flex" style="align-items:flex-start;margin-top:1.5mm"><div class="grow">{fig2}</div><div style="width:82mm">{memo}</div></div>',
           lines(r"1回の交代時間を $x$ 分とする。9時30分から12時25分までは175分。<br>"
                 r"発表は15回で $7\times15=105$（分）、交代時間は14回あるので<br>"
                 r"$105+14x=175$　$14x=70$　$x=5$<br>（5分は問題に合っている）", 34),
           A("5分", "w20"), 0)
    return f"""<section class="page">{header("大問2-2　方程式の利用")}
<div class="lead"><b>2</b>　かすみさんの中学校では、毎年ダンスコンテストを実施している。かすみさんは、その実行委員を務めることになった。昨年は、下の図にあるような【昨年の発表の流れ】で行われたが、今年は発表するグループの数が変わったため、発表の流れを見直すことになった。このとき、次の(1)、(2)の問いに答えなさい。</div>
<div class="frame"><b>【昨年の発表の流れ】</b><div style="text-align:center">{fig1}</div>
※　発表は6グループが行い、発表時間は一定でそれぞれ6分とする。<br>※　交代時間は一定で、それぞれ4分とする。<br>※　最初のグループの発表が始まる時刻は10時とする。</div>
{q1}{q2}
</section>"""


# ================= 大問3-1 反比例 =================
def d3a():
    q = Q("1", r"反比例 $y=\dfrac6x$ の $x$ の値とそれに対応する $y$ の値について、正しく説明している文を、次のア〜エから1つ選び、記号で答えなさい。"
          r'<div class="ch">ア　$x$ の値と $y$ の値の和は、いつも6である。<br>イ　$y$ の値から $x$ の値をひいた差は、いつも6である。<br>'
          r'ウ　$x$ の値と $y$ の値の積は、いつも6である。<br>エ　$y$ の値を $x$ の値でわった商は、いつも6である。</div>',
          W(r"$y=\dfrac6x$ の両辺に $x$ をかけると $xy=6$（反比例では、$x$ と $y$ の積が一定で比例定数に等しい）<br>"
            r"たとえば $x=1$ のとき $y=6$、$x=2$ のとき $y=3$ で、和・差・商は一定ではない"),
          A("ウ", "w20"), 10)
    return f"""<section class="page">{header("大問3-1　比例と反比例")}
{q}
</section>"""


# ================= 大問3-2 一次関数 =================
def d3b():
    q1 = Q("(1)", r"点Aの $y$ 座標を求めなさい。", W(r"$y=-(-6)+3$"), A("9", "w20"), 8)
    q2 = Q("(2)", "3点O、A、Bを結んでできる△OABの面積を求めなさい。",
           W(r"直線と $y$ 軸の交点を C$(0,\ 3)$ とする。△OAB＝△OAC＋△OBC<br>$\dfrac12\times3\times6+\dfrac12\times3\times2=9+3$"),
           A("12", "w20"), 14)
    q3 = Q("(3)", r"$y$ 軸上に、点Oと異なる点Pをとる。△PABの面積と△OABの面積が等しくなるとき、2点A、Pを通る直線の式を求めなさい。",
           W(r"△PAB＝$\dfrac12\times\mathrm{PC}\times(6+2)=12$ より PC＝3。Pは点Oと異なるので P$(0,\ 6)$<br>"
             r"A$(-6,\ 9)$、P$(0,\ 6)$ を通るので　傾き $\dfrac{6-9}{0-(-6)}=-\dfrac12$、切片6"),
           A(r"$y=-\dfrac12x+6$", "w30"), 16)
    return f"""<section class="page">{header("大問3-2　一次関数")}
<div class="flex"><div class="grow"><div class="lead"><b>2</b>　図のように、一次関数 $y=-x+3$ のグラフ上に2点A、Bがあり、$x$ 座標はそれぞれ $-6$、2である。このとき、次の(1)〜(3)の問いに答えなさい。</div>{q1}{q2}</div>
<div class="fig">{line_svg()}</div></div>
{q3}
</section>"""


# ================= 大問4 平面図形 =================
def d4():
    q1 = Q("1", r"$\angle\mathrm{ABC}=65^\circ$、$\angle\mathrm{ACB}=37^\circ$ のとき、$\angle\mathrm{BAD}$ の大きさを求めなさい。",
           W(r"$\angle\mathrm{BAC}=180^\circ-65^\circ-37^\circ=78^\circ$　ADは∠BACの二等分線なので　$78^\circ\div2$"), A(r"$39^\circ$", "w20"), 8)
    q2 = Q("2", "△AED≡△ACDであることを証明しなさい。",
           lines(r"△AEDと△ACDで、<br>ADは共通　……①<br>ADは∠BACの二等分線だから　$\angle\mathrm{EAD}=\angle\mathrm{CAD}$　……②<br>"
                 r"仮定より　$\angle\mathrm{ADE}=\angle\mathrm{ADC}$　……③<br>①、②、③より、1組の辺とその両端の角がそれぞれ等しいから、△AED≡△ACD", 36), "", 0)
    t1 = Q("(1)", "BC＝15cmであるとき、DEの長さを求めなさい。",
           W(r"DC＝$15\times\dfrac35=9$（cm）。2より △AED≡△ACD なので DE＝DC"), A("9cm", "w20"), 10)
    t2 = Q("(2)", "△CDEの面積は△ABDの面積の何倍か、求めなさい。",
           W(r"△ABD：△ADC＝BD：DC＝2：3 なので、△ABD＝2S、△ADC＝3S とする。△AED＝△ACD＝3S より　△BED＝3S−2S＝S<br>"
             r"△BED：△CDE＝BD：DC＝2：3 なので　△CDE＝$\dfrac32$S　　$\dfrac32\mathrm S\div2\mathrm S=\dfrac34$"),
           A(r"$\dfrac34$ 倍", "w20"), 16)
    return f"""<section class="page">{header("大問4　平面図形（合同・面積）")}
<div class="lead">下の図のように、△ABCがあり、∠BACの二等分線と辺BCとの交点をDとする。辺ABの延長上に∠ADE＝∠ADCとなるように点Eをとり、点EとCを結ぶ。このとき、次の1〜3の問いに答えなさい。</div>
<div style="text-align:center">{bis_svg()}</div>
{q1}{q2}
<div class="q"><div class="qt"><span class="no">3</span>BD：DC＝2：3のとき、次の(1)、(2)の問いに答えなさい。</div></div>
{t1}{t2}
</section>"""


# ================= 大問5 空間図形 =================
def d5():
    q1 = Q("1", "辺ACとねじれの位置にある辺は何本か、答えなさい。",
           W("ACと交わる辺（AB・AD・AE・BC・CD）をのぞくと、残りは辺DE・辺EB。どちらもACと平行でもない"), A("2本", "w20"), 8)
    q2 = Q("2", "底面の正方形の1辺の長さとして適切なものを、次のア〜エから1つ選び、記号で答えなさい。"
           r'<div class="ch">ア　$\sqrt3$ cm　　イ　$\sqrt6$ cm　　ウ　$2\sqrt3$ cm　　エ　$2\sqrt6$ cm</div>',
           W(r"1辺を $a$ cm とすると $a^2=12$　$a=\sqrt{12}=2\sqrt3$"), A("ウ", "w20"), 4)
    q3 = Q("3", "この正四角錐の体積を求めなさい。", W(r"$\dfrac13\times12\times3$"), A("12cm³", "w20"), 10)
    q4 = Q("4", "この正四角錐の表面積を求めなさい。",
           W(r"側面1つ：$\dfrac12\times2\sqrt3\times2\sqrt3=6$　側面4つで24<br>底面12とあわせて　$12+24=36$"), A("36cm²", "w20"), 14)
    return f"""<section class="page">{header("大問5　空間図形（正四角錐）")}
<div class="flex"><div class="grow"><div class="lead">右の図は、高さが3cmの正四角錐である。この正四角錐の底面積は12cm²であり、側面の二等辺三角形の高さは $2\\sqrt3$ cmである。このとき、次の1〜4の問いに答えなさい。</div>{q1}</div>
<div class="fig">{pyr_svg()}</div></div>
{q2}{q3}{q4}
</section>"""


JOBS = [("c3_jitsu_r310_d1", d1), ("c3_jitsu_r310_kakuritsu", d2a), ("c3_jitsu_r310_renritsu", d2b),
        ("c3_jitsu_r310_hirei", d3a), ("c3_jitsu_r310_ichiji", d3b), ("c3_jitsu_r310_zukei", d4), ("c3_jitsu_r310_kuukan", d5)]

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
