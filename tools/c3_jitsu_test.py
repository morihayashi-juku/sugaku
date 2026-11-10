"""中3 実力テスト（高校入試形式・大問1〜5）を、大問ごと（大問1／単元別）の PDF にする。
問題（pdf/c3_jitsu_*.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。

  大問1 小問集合                  c3_jitsu_d1
  大問2 連立方程式の利用・整数    c3_jitsu_renritsu
  大問3 データの活用              c3_jitsu_data（2ページ）
  大問4 合同・平行線と面積        c3_jitsu_zukei（2ページ）
  大問5 一次関数                  c3_jitsu_ichiji

答えは Fraction／数値で計算して assert で確認している。実行：cd tools && python3 c3_jitsu_test.py
"""
from fractions import Fraction as F
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from texlib import _dist  # noqa: E402

KATEX = _dist()
OUT = pathlib.Path(__file__).resolve().parent.parent / "pdf"


# ================= 答えの確認（数値） =================
# 大問1
assert -9 - (-5) == -4
assert F(6) / F(-4, 3) == F(-9, 2)
assert math.isclose(math.sqrt(2) * (math.sqrt(2) + math.sqrt(6)), 2 + 2 * math.sqrt(3))
assert 2 < math.sqrt(5) < 3 and (math.sqrt(5) - 2 + 2) ** 2 - 5 < 1e-9
# 大問2
assert 5 * 1 + 3 * 3 == 14
assert 4 * 12 + 8 * 3 == 72 and 12 + 3 * 3 == 21
sol4 = [(a, b) for a in range(1, 40) for b in range(1, 20) if 5 * a + 8 * b == 150]
assert sol4 == [(6, 15), (14, 10), (22, 5)]
# 大問3
h1 = [1, 6, 8, 7, 6, 4]                 # 資料II 0-150, 150-300, ...
h2 = [0, 1, 4, 5, 7, 6, 6, 4, 2]        # 資料III 0-100, 100-200, ... （最初の0は表示しない）
assert sum(h1) == 32 and sum(h2) == 35
assert round(sum(c * v for c, v in zip([75 + 150 * i for i in range(6)], h1)) / 32) == 483
assert round(sum(c * v for c, v in zip([50 + 100 * i for i in range(9)], h2)) / 35) == 513
assert round((6 + 4) / 32 * 100) == 31 and round((6 + 4 + 2) / 35 * 100) == 34
# 大問4：AD=6, BC=10, △AED=15 → 高さ10 → 台形80、BG=2
hh = F(15 * 2 * 2, 6)
assert hh == 10 and F(1, 2) * (6 + 10) * hh == 80
assert F(1, 2) * 16 * hh == 80 and (6 + 10) / 2 - 6 == 2
# 大問5
ax = F(12 - 6, 3)
assert (ax, ax + 6) == (2, 8)
assert F(1, 2) * (12 - 6) * 2 == 6
abd = F(1, 2) * 12 * 8
assert abd == 48 and F(1, 2) * 8 * 6 == abd / 2


# ================= 部品 =================
def A(s, w="w30"):
    return f'<span class="ans {w}">{s}</span>'


def W(s):
    return f'<div class="work">{s}</div>'


def BX(label, ans):
    return f'<span class="bx"><span class="ql">{label}</span><span class="qa">{ans}</span></span>'


def header(title, page=None):
    p = f"（{page}）" if page else ""
    return (f'<div class="hd"><div class="ht"><span class="tag">中3　実力テスト</span>{title}{p}<span class="key">解答</span></div>'
            f'<div class="nm">　月　　日　名前（　　　　　　　　　）</div></div>')


def Q(no, text, work="", ans="", sp=14, cls=""):
    al = f'<div class="al">答　{ans}</div>' if ans else ""
    return (f'<div class="q {cls}"><div class="qt"><span class="no">{no}</span>{text}</div>'
            f'<div class="sp" style="min-height:{sp}mm">{work}</div>{al}</div>')


def lines(text, h=30):
    """記述欄：問題では罫線だけ、こたえでは赤字"""
    return f'<div class="lines" style="min-height:{h}mm"><div class="lt">{text}</div></div>'


# ================= 図 =================
def cube_svg():
    o = [("A", 15, 45), ("B", 85, 45), ("F", 85, 115), ("E", 15, 115), ("D", 50, 15), ("C", 120, 15), ("G", 120, 85), ("H", 50, 85)]
    P = {n: (x, y) for n, x, y in o}

    def ln(a, b, dash=False):
        d = ' stroke-dasharray="4,3"' if dash else ""
        return f'<line x1="{P[a][0]}" y1="{P[a][1]}" x2="{P[b][0]}" y2="{P[b][1]}" stroke="#000" stroke-width="1.3"{d}/>'
    s = "".join(ln(a, b) for a, b in ["AB", "BF", "FE", "EA", "AD", "BC", "DC", "CG", "FG"])
    s += "".join(ln(a, b, True) for a, b in ["DH", "HE", "HG"])
    off = {"A": (-12, -3), "B": (5, 3), "F": (3, 14), "E": (-11, 13), "D": (-4, -5), "C": (3, -4), "G": (5, 6), "H": (-12, -2)}
    for n, (x, y) in P.items():
        s += f'<text x="{x+off[n][0]}" y="{y+off[n][1]}" class="pl">{n}</text>'
    return f'<svg width="168" height="135" viewBox="0 0 168 135">{s}</svg>'


def hist_svg(title, bw, nb, start_idx, counts, tick_step, ymax=8):
    """ヒストグラム。x軸は0〜900。bw＝階級の幅、start_idx＝最初の棒が何番目の階級か"""
    L, T, Wd, Hh = 26, 22, 188, 150
    xs = lambda v: L + v / 900 * Wd
    ys = lambda v: T + Hh - v / ymax * Hh
    s = f'<text x="{L+Wd/2}" y="12" class="ht2" text-anchor="middle">{title}</text><text x="2" y="{T-6}" class="sm">(人)</text>'
    for v in range(0, ymax + 1):
        s += f'<line x1="{L}" y1="{ys(v)}" x2="{L+Wd}" y2="{ys(v)}" stroke="#777" stroke-width="0.5" stroke-dasharray="2,2"/>'
        s += f'<text x="{L-4}" y="{ys(v)+3}" class="sm" text-anchor="end">{v}</text>'
    for i, c in enumerate(counts):
        if c:
            x0 = (start_idx + i) * bw
            s += f'<rect x="{xs(x0)}" y="{ys(c)}" width="{Wd*bw/900}" height="{Hh*c/ymax}" fill="#555" stroke="#000" stroke-width="1"/>'
    for v in range(0, 901, tick_step):
        s += f'<text x="{xs(v)}" y="{T+Hh+12}" class="sm" text-anchor="middle">{v}</text>'
    s += f'<text x="{L+Wd+2}" y="{T+Hh+12}" class="sm">(cm)</text>'
    return f'<svg width="240" height="{T+Hh+20}" viewBox="0 0 240 {T+Hh+20}">{s}</svg>'


def box_svg():
    L, Wd = 72, 360
    xs = lambda v: L + v / 900 * Wd
    s = '<text x="2" y="42" class="b2">3年2組</text>'
    for v in range(0, 901, 50):
        s += f'<line x1="{xs(v)}" y1="14" x2="{xs(v)}" y2="62" stroke="#888" stroke-width="0.5" stroke-dasharray="2,2"/>'
    mn, q1, md, q3, mx = 173, 331, 502, 659, 860
    s += f'<line x1="{xs(mn)}" y1="38" x2="{xs(q1)}" y2="38" stroke="#000" stroke-width="1.4"/><line x1="{xs(q3)}" y1="38" x2="{xs(mx)}" y2="38" stroke="#000" stroke-width="1.4"/>'
    s += f'<line x1="{xs(mn)}" y1="28" x2="{xs(mn)}" y2="48" stroke="#000" stroke-width="1.4"/><line x1="{xs(mx)}" y1="28" x2="{xs(mx)}" y2="48" stroke="#000" stroke-width="1.4"/>'
    s += f'<rect x="{xs(q1)}" y="22" width="{xs(q3)-xs(q1)}" height="32" fill="#fff" stroke="#000" stroke-width="1.4"/><line x1="{xs(md)}" y1="22" x2="{xs(md)}" y2="54" stroke="#000" stroke-width="1.4"/>'
    for v in range(0, 901, 100):
        s += f'<text x="{xs(v)}" y="74" class="sm" text-anchor="middle">{v}</text>'
    s += f'<text x="{xs(900)+14}" y="74" class="sm">(cm)</text>'
    for v in (mn, q1, md, q3, mx):
        s += f'<line x1="{xs(v)}" y1="96" x2="{xs(v)}" y2="80" stroke="#000" stroke-width="1"/><path d="M{xs(v)} 78 l-3.5 7 l7 0 z" fill="#000"/>'
        s += f'<text x="{xs(v)}" y="108" class="sm" text-anchor="middle">{v}</text>'
    return f'<svg width="{L+Wd+40}" height="116" viewBox="0 0 {L+Wd+40} 116">{s}</svg>'


def trap(fig, scale=1.0):
    """台形 ABCD（AD∥BC）。fig = 1,2,3,4。AD=6, BC=10, 高さ10 を 13 px/cm で"""
    k = 13 * scale
    A_, D_, B_, C_ = (2 * k, 0), (8 * k, 0), (0, 10 * k), (10 * k, 10 * k)
    # 辺AB の中点 E、BF = AD となる F
    E_ = ((A_[0] + B_[0]) / 2, (A_[1] + B_[1]) / 2)
    F_ = (B_[0] - 6 * k, B_[1])
    G_ = (E_[0] + 2 * k, B_[1])                      # EG∥DC
    ox = 6 * k + 18 if fig >= 3 else 18
    oy = 16

    def P(p):
        return (p[0] + ox, p[1] + oy)

    def ln(a, b, dash=False, w=1.2):
        (x1, y1), (x2, y2) = P(a), P(b)
        d = ' stroke-dasharray="3,2"' if dash else ""
        return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#000" stroke-width="{w}"{d}/>'

    def lab(t, p, dx, dy, anc="middle"):
        x, y = P(p)
        return f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" class="pl" text-anchor="{anc}">{t}</text>'
    s = ln(A_, D_) + ln(D_, C_) + ln(C_, B_) + ln(B_, A_)
    if fig >= 2:
        s += ln(E_, D_) + ln(E_, C_)
    if fig >= 3:
        s += ln(F_, B_) + ln(E_, F_)
    if fig == 4:
        s += ln(E_, G_)
    s += lab("A", A_, -4, -6) + lab("D", D_, 4, -6) + lab("B", B_, -6, 14) + lab("C", C_, 7, 14)
    if fig >= 1:
        s += f'<circle cx="{P(E_)[0]:.1f}" cy="{P(E_)[1]:.1f}" r="2" fill="#000"/>' + lab("E", E_, -9, 4 if fig == 1 else -2)
    if fig >= 3:
        s += lab("F", F_, -4, 14)
    if fig == 4:
        s += lab("G", G_, 4, 14)
    w = (16 * k if fig >= 3 else 10 * k) + 40
    h = 10 * k + 36
    return f'<svg width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}">{s}</svg>'


def graph_svg(with_f=False):
    sc = 14
    ox, oy = 8 * sc + 6, 15 * sc
    X = lambda x: ox + x * sc
    Y = lambda y: oy - y * sc
    s = f'<line x1="{X(-8)}" y1="{Y(0)}" x2="{X(9)}" y2="{Y(0)}" stroke="#000" stroke-width="1"/><line x1="{X(0)}" y1="{Y(-1.2)}" x2="{X(0)}" y2="{Y(14.3)}" stroke="#000" stroke-width="1"/>'
    s += f'<text x="{X(9)+3}" y="{Y(0)+4}" class="ax">x</text><text x="{X(0)+6}" y="{Y(14.3)+4}" class="ax">y</text>'
    # ℓ: y=-2x+12 / m: y=x+6
    s += f'<line x1="{X(-1.2)}" y1="{Y(14.4)}" x2="{X(6.6)}" y2="{Y(-1.2)}" stroke="#000" stroke-width="1.2"/>'
    s += f'<line x1="{X(-7.2)}" y1="{Y(-1.2)}" x2="{X(7.6)}" y2="{Y(13.6)}" stroke="#000" stroke-width="1.2"/>'
    s += f'<text x="{X(-1.2)-12}" y="{Y(14.4)+2}" class="ax">ℓ</text><text x="{X(7.6)+4}" y="{Y(13.6)}" class="ax">m</text>'
    pts = {"A": ((2, 8), (6, -3)), "B": ((-6, 0), (-3, 12)), "C": ((0, 6), (-11, 3)), "D": ((6, 0), (4, 13)), "E": ((0, 12), (-12, 2))}
    for n, ((x, y), (dx, dy)) in pts.items():
        s += f'<text x="{X(x)+dx}" y="{Y(y)+dy}" class="pl">{n}</text>'
    s += f'<text x="{X(0)-11}" y="{Y(0)+12}" class="pl">O</text>'
    if with_f:
        s += f'<line x1="{X(0)}" y1="{Y(6)}" x2="{X(2)}" y2="{Y(0)}" stroke="#000" stroke-width="1.2"/><text x="{X(2)-3}" y="{Y(0)+13}" class="pl">F</text>'
    w, h = 17 * sc + 22, 15 * sc + 18
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{s}</svg>'


# ================= 大問1 =================
def d1():
    c1 = Q("(1)", r"$(-9)-(-5)$ を計算しなさい。", W(r"$(-9)+5=-4$"), A(r"$-4$"), 11)
    c2 = Q("(2)", r"$6\div\left(-\dfrac{4}{3}\right)$ を計算しなさい。", W(r"$6\times\left(-\dfrac{3}{4}\right)=-\dfrac{9}{2}$"), A(r"$-\dfrac{9}{2}$"), 11)
    c3 = Q("(3)", r"$\sqrt{2}(\sqrt{2}+\sqrt{6})$ を計算しなさい。", W(r"$\sqrt2\times\sqrt2+\sqrt2\times\sqrt6=2+\sqrt{12}=2+2\sqrt3$"), A(r"$2+2\sqrt{3}$"), 11)
    c4 = Q("(4)", r"$(3x+1)(3x-1)$ を計算しなさい。", W(r"$(3x)^2-1^2$"), A(r"$9x^2-1$"), 11)
    c5 = Q("(5)", r"分速 $a$ m で15分間歩くと、進む道のりは $b$ m以上になる。このときの数量の関係を不等式に表しなさい。",
           W(r"（道のり）＝（速さ）×（時間）より　$a\times15=15a$"), A(r"$15a\geqq b$"), 11)
    c6 = Q("(6)", r"3枚の硬貨を同時に投げるとき、表が2枚出る確率を求めなさい。ただし、硬貨の表裏の出かたは、同様に確からしいとする。",
           W(r"表を○、裏を×とすると、全部で8通り。<br>表が2枚になるのは（○○×）（○×○）（×○○）の3通り"), A(r"$\dfrac{3}{8}$"), 11)
    c7 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(7)</span>右の図の立方体の辺や面の位置関係について、'
          '<b>正しくない</b>ものを、次のア〜エから1つ選び、記号で答えなさい。</div>'
          '<div class="ch">ア　辺ADと辺BCは平行である。<br>イ　辺AEと面EFGHは垂直である。<br>ウ　面AEHDと辺CGは平行である。<br>エ　辺ABと辺HGはねじれの位置にある。</div>'
          + W(r"エ：辺ABと辺HGはどちらも横向きの辺で、平行である。（ねじれの位置ではない）") +
          '</div><div class="fig">' + cube_svg() + '</div></div>'
          f'<div class="al">答　{A("エ", "w20")}</div></div>')
    c8 = ('<div class="q"><div class="qt"><span class="no">(8)</span>啓太さんは、$\\sqrt5$ の小数部分を $a$ とするとき、$a^2+4a+4$ の値を次のように求めた。このとき、'
          + BX("①", "2") + "、" + BX("③", "5") + " に当てはまる数と、" + BX("②", "$a+2$") + " に当てはまる式を答えなさい。ただし、同じ番号の□には共通するものがはいる。</div>"
          '<div class="frame">'
          r'$\sqrt4<\sqrt5<\sqrt9$ より、$2<\sqrt5<3$ だから、$\sqrt5$ の整数部分は ' + BX("①", "2") + ' になる。<br>'
          r'よって、$\sqrt5$ の小数部分 $a$ は、$a=\sqrt5-$' + BX("①", "2") + r' と表される。<br>'
          r'一方、$a^2+4a+4$ を因数分解すると、$a^2+4a+4=($' + BX("②", "$a+2$") + r'$)^2$<br>'
          r'$($' + BX("②", "$a+2$") + r'$)^2$ に $a=\sqrt5-$' + BX("①", "2") + r' を代入して計算すると、$a^2+4a+4$ の値は ' + BX("③", "5") + ' である。'
          '</div>' + W(r"$(a+2)^2=(\sqrt5-2+2)^2=(\sqrt5)^2=5$") +
          f'<div class="al">答　①{A("2", "w20")}　②{A("$a+2$", "w20")}　③{A("5", "w20")}</div></div>')
    return f"""<section class="page">{header("大問1　小問集合")}
<div class="lead">次の(1)〜(8)の問いに答えなさい。</div>
<div class="grid2">{c1}{c2}{c3}{c4}</div>
<div class="grid2">{c5}{c6}</div>
{c7}
{c8}
</section>"""


# ================= 大問2 =================
def d2():
    q1 = Q("1", "ノートAの4冊入りが5セット、8冊入りが3セット売れたとき、おまけとして渡した鉛筆の本数を求めなさい。",
           W(r"4冊入り：$1\times5=5$（本）　8冊入り：$3\times3=9$（本）<br>$5+9=14$（本）"), A("14本"), 14)
    q2 = Q("2", r"ある日のノートAの売り上げ冊数の合計は72冊で、おまけとして渡した鉛筆の本数は21本だった。この日、ノートAの4冊入りが $x$ セット、8冊入りが $y$ セット売れたとして、連立方程式をつくり、この日売れたノートAの4冊入りと8冊入りのセット数をそれぞれ求めなさい。",
           W(r"冊数：$4x+8y=72$　　鉛筆：$x+3y=21$<br>$\begin{cases}4x+8y=72\\x+3y=21\end{cases}$　上の式を4でわると $x+2y=18$<br>"
             r"$x+3y=21$ から $x+2y=18$ をひくと　$y=3$　これを $x+3y=21$ に代入して　$x=12$<br>（4×12＋8×3＝72、12＋3×3＝21 で問題に合う）"),
           "4冊入り：" + A("12セット", "w20") + "　8冊入り：" + A("3セット", "w20"), 36)
    q3 = Q("3", r"別の日に、この文房具店は、ノートAを150冊仕入れて、4冊入りと8冊入りのセットをつくっていったが、4冊入りと8冊入りのセットをどのように組み合わせても、ノートAを余りなく使いきることができなかった。4冊入りのセットを $a$ セット、8冊入りのセットを $b$ セットつくるとして、ノートAを余りなく使いきることができない理由を、「倍数」の語句を用いて説明しなさい。",
           lines(r"使うノートの冊数は $4a+8b$（冊）と表され、$4a+8b=4(a+2b)$ となる。$a+2b$ は整数だから、$4a+8b$ は<b>4の倍数</b>である。"
                 r"ところが、150は4の倍数ではない（$150=4\times37+2$）ので、$4a+8b=150$ になることはない。よって、余りなく使いきることができない。", 36), "", 0)
    q4 = Q("4", "この文房具店は、ノートBについてもセットにして販売している。ノートBは、5冊入りと8冊入りの2種類のセットにしているが、150冊仕入れてセットをつくっていくと、余りなく使いきることができる。"
           "ノートBを150冊仕入れて、2種類のセットをつくるとき、5冊入りのセットと8冊入りのセットの組み合わせは、全部で何通りできるか、求めなさい。ただし、どちらのセットも1セット以上つくるものとする。",
           W(r"5冊入りを $a$ セット、8冊入りを $b$ セットとすると　$5a+8b=150$（$a,\ b$ は1以上の整数）<br>"
             r"$5a=150-8b$ で、$5a$ と150は5の倍数だから、$8b$ も5の倍数。8と5は共通の約数をもたないので、$b$ は5の倍数。<br>"
             r"$8b<150$ より　$b=5,\ 10,\ 15$　　$b=5$ のとき $a=22$、$b=10$ のとき $a=14$、$b=15$ のとき $a=6$"
             r"<table class='mini'><tr><th>8冊入り $b$</th><td>5</td><td>10</td><td>15</td></tr><tr><th>5冊入り $a$</th><td>22</td><td>14</td><td>6</td></tr></table>"),
           A("3通り", "w20"), 38)
    intro = ('<div class="lead">ある文房具店では、ノートAを、4冊入りと8冊入りの2種類のセットにして販売しており、4冊入りの場合は1セットにつき1本、'
             '8冊入りの場合は1セットにつき3本の鉛筆をおまけとして渡している。<br>このとき、下の1〜4の問いに答えなさい。</div>')
    return f'<section class="page">{header("大問2　連立方程式の利用・整数")}{intro}{q1}{q2}{q3}{q4}</section>'


# ================= 大問3 =================
def d3():
    t1 = ('<table class="dt"><tr><th>生徒</th><td>A</td><td>B</td><td>C</td><td>D</td><td class="cut">…</td></tr>'
          '<tr><th>記録(cm)</th><td>286</td><td>709</td><td>637</td><td>566</td><td class="cut"></td></tr></table>')
    t2 = ('<table class="dt"><tr><th>生徒</th><td>A</td><td>B</td><td>C</td><td>D</td><td class="cut">…</td></tr>'
          '<tr><th>記録(cm)</th><td>330</td><td>422</td><td>860</td><td>471</td><td class="cut"></td></tr></table>')
    d = lambda who, t: f'<p class="dl"><b>{who}：</b>{t}</p>'
    top = (d("悠人", "資料Ⅰは、3年1組と3年2組の記録について、クラスごとにまとめたものだね。")
           + d("陽菜", "資料Ⅰから、3年1組と3年2組の平均値をそれぞれ計算してみると、3年1組は約511cm、3年2組は約514cmだったよ。")
           + d("悠人", "資料Ⅰから、3年1組と3年2組の最頻値をそれぞれ調べてみたんだけど、どちらのクラスも、同じ記録の人はいなかったよ。"))
    mid = (d("陽菜", "ところで、資料Ⅰはそれぞれの記録についてはわかるけど、全体的な分布のようすはよくわからないね。")
           + d("悠人", "では、クラスごとにヒストグラムにまとめてみようか。")
           + d("陽菜", "私は3年1組の記録をまとめるから、3年2組の記録は悠人さんにお願いするね。"))
    after = (d("陽菜", "資料Ⅱが3年1組の32人の記録、資料Ⅲが3年2組の35人の記録をまとめたものだね。")
             + d("悠人", "資料Ⅱと資料Ⅲからわかることを考えてみよう。")
             + d("陽菜", "まず、最頻値を求めてみよう。度数がもっとも多い階級の階級値は、資料Ⅱでは " + BX("①", "375") + " cm で、資料Ⅲでは " + BX("②", "450") + " cm だね。")
             + d("悠人", "次に、記録が600cm以上の人をよい記録として、どちらのクラスのほうがよい記録を残したか調べてみよう。記録が600cm以上の人数の割合は、小数第1位を四捨五入すると、3年1組は約 "
                 + BX("③", "31") + " %、3年2組は約 " + BX("④", "34") + " %なので、3年 " + BX("⑤", "2") + " 組のほうがよい記録といえるね。"))
    p1 = f"""<section class="page">{header("大問3　データの活用", "1/2")}
<div class="lead">3年1組と3年2組の生徒がそれぞれ紙飛行機を1人1回ずつ飛ばして、その飛行距離を記録した。次の【会話】は、悠人さんと陽菜さんがその記録について話し合っている場面である。このとき、後の1〜4の問いに答えなさい。</div>
<div class="frame conv"><div class="ctitle">【会話】</div>
<div class="flex"><div class="grow">{top}</div><div class="sidet"><b>資料Ⅰ　紙飛行機の飛行距離</b><div>【3年1組】</div>{t1}<div>【3年2組】</div>{t2}</div></div>
{mid}
<div class="hists"><div><b>資料Ⅱ</b><br>{hist_svg("3年1組の記録", 150, 6, 0, h1, 150)}</div><div><b>資料Ⅲ</b><br>{hist_svg("3年2組の記録", 100, 9, 0, h2, 100)}</div></div>
{after}
</div></section>"""
    last = (d("陽菜", "最後に、平均値を計算してみよう。") + d("悠人", "資料Ⅱでは約483cm、資料Ⅲでは約513cmになったよ。")
            + d("陽菜", "これらの数値と、資料Ⅰから計算した数値は、3年2組については近い値だけど、3年1組については大きく異なっているね。どうしてだろう？")
            + d("悠人", "それは、資料Ⅲよりも資料Ⅱのほうが " + BX("⑥", "階級の幅") + " が大きいからだよ。"))
    r1 = Q("1", BX("①", "375") + "、" + BX("②", "450") + " に当てはまる数をそれぞれ求めなさい。",
           W(r"最頻値＝度数がもっとも多い階級の階級値。資料Ⅱは300cm以上450cm未満（8人）、資料Ⅲは400cm以上500cm未満（7人）<br>"
             r"資料Ⅱ：$(300+450)\div2=375$　　資料Ⅲ：$(400+500)\div2=450$"),
           "①" + A("375", "w20") + "　②" + A("450", "w20"), 16)
    r2 = Q("2", BX("③", "31") + "〜" + BX("⑤", "2") + " に当てはまる数をそれぞれ求めなさい。",
           W(r"600cm以上の人数　資料Ⅱ：$6+4=10$（人）→ $10\div32\times100=31.25\cdots$ より約31％<br>"
             r"資料Ⅲ：$6+4+2=12$（人）→ $12\div35\times100=34.28\cdots$ より約34％<br>31％＜34％ なので、よい記録といえるのは3年2組"),
           "③" + A("31", "w20") + "　④" + A("34", "w20") + "　⑤" + A("2", "w20"), 22)
    r3 = Q("3", BX("⑥", "ウ") + " に当てはまるもっとも適切な語句を、次のア〜エから1つ選び、記号で答えなさい。"
           '<div class="ch row">ア　範囲　　　イ　四分位範囲　　　ウ　階級の幅　　　エ　累積度数</div>',
           W(r"資料Ⅱの階級の幅は150cm、資料Ⅲは100cm。階級の幅が大きいほど、階級値と実際の記録のずれが大きくなり、平均値が大きくずれる。"),
           A("ウ", "w20"), 12)
    r4 = (Q("4", "資料Ⅳは、資料Ⅰをもとにして、3年2組の記録を箱ひげ図にまとめたものである。3年2組に所属する陽菜さんの記録は671cmだったので、自分の記録が3年2組の上位8人に必ず入っていると考えた。"
            "陽菜さんの考えが正しいかどうか、適切なほうを○で囲みなさい。また、その理由を、「第1四分位数」「第2四分位数」「第3四分位数」の中から、もっとも適切な語句を1つ選び、その選んだ語句の値を用いて説明しなさい。"
            '<div class="choice">（　<span class="c1">正しい</span>　・　正しくない　）</div>',
            lines(r"<b>第3四分位数</b>が659cmで、35人を記録の大きい順に並べると、659cmは大きいほうから9番目の記録である。"
                  r"陽菜さんの記録は671cmで659cmより大きいので、上位8人に必ず入る。", 24), "", 0)
          + f'<div class="hist4"><b>資料Ⅳ</b><br>{box_svg()}</div>')
    p2 = f"""<section class="page">{header("大問3　データの活用", "2/2")}
<div class="frame conv">{last}</div>
{r1}{r2}{r3}{r4}
</section>"""
    return p1 + p2


# ================= 大問4 =================
def d4():
    ans1 = Q("1", "辺ABの中点Eは、ある直線と辺ABとの交点として、コンパスと定規を使った作図によって求めることができる。どのような直線と辺ABとの交点として求めることができるか、次のア〜エから1つ選び、記号で答えなさい。"
             '<div class="ch">ア　∠ADCの二等分線と辺ABとの交点<br>イ　∠BCDの二等分線と辺ABとの交点<br>ウ　線分ABの垂直二等分線と辺ABとの交点<br>エ　線分CDの垂直二等分線と辺ABとの交点</div>',
             W("線分の中点は、その線分の垂直二等分線との交点として作図できる。"), A("ウ", "w20"), 8)
    q2 = ('<div class="q"><div class="qt"><span class="no">2</span>図Ⅱは、図Ⅰにおいて、点Dと点E、点Cと点Eをそれぞれ線分で結んだものである。和人さんと咲良さんは、図Ⅱを見て、次のことを予想した。</div></div>')
    yosou = '<div class="frame"><b>【予想】</b><div class="rb">△DECの面積は、台形ABCDの面積の $\\dfrac12$ である。</div></div>'
    kaiwa = ('<p>次の【会話】は、この【予想】が成り立つことを説明するために、2人が話し合っている場面である。</p>'
             '<div class="frame"><b>【会話】</b>'
             '<p class="dl"><b>和人：</b>点Eは辺ABの中点だから、これを何とか利用できないかな。</p>'
             '<p class="dl"><b>咲良：</b>線分DEを延長してみたらどうだろう。</p>'
             '<p class="dl"><b>和人：</b>線分DEの延長と辺CBの延長との交点をFとして△BEFをつくると、△AED≡△BEFがいえそうだよ。</p>'
             '<p class="dl"><b>咲良：</b>なるほど。そうすると、合同な図形の性質を利用して台形ABCDを変形することで、△DEC＝$\\dfrac12$×（台形ABCD）が説明できそうだね。</p></div>'
             '<p>このとき、次の(1)、(2)の問いに答えなさい。</p>')
    p1 = f"""<section class="page">{header("大問4　合同・平行線と面積", "1/2")}
<div class="flex"><div class="grow"><div class="lead">図Ⅰで、四角形ABCDはAD∥BCの台形、Eは辺ABの中点である。このとき、下の1〜3の問いに答えなさい。</div></div><div class="fig"><b>図Ⅰ</b><br>{trap(1)}</div></div>
{ans1}
<div class="flex"><div class="grow">{q2}</div><div class="fig"><b>図Ⅱ</b><br>{trap(2)}</div></div>
{yosou}
{kaiwa}
</section>"""
    proof = ('<div class="frame proof"><div>△AEDと△BEFで、</div>'
             '<div class="pbody">'
             '<div class="lt">仮定より、AE＝BE　……①<br>対頂角は等しいから、∠AED＝∠BEF　……②<br>AD∥BC より AD∥FB で、平行線の錯角は等しいから、∠DAE＝∠EBF　……③<br>'
             '①、②、③より、1組の辺とその両端の角がそれぞれ等しいから、</div></div>'
             '<div>△AED≡△BEF</div></div>')
    s1 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(1)</span>2人はまず、【会話】にあるように、図Ⅱから、線分DEの延長と辺CBの延長との交点をFとして、図Ⅲをかき、次のようにして、'
          '△AED≡△BEFを証明した。<span class="dotbox"></span>をうめて、【証明】を完成させなさい。</div></div>'
          f'<div class="fig"><b>図Ⅲ</b><br>{trap(3, 0.9)}</div></div>{proof}</div>')
    s2 = ('<div class="q"><div class="qt"><span class="no">(2)</span>その後、2人は、△AED≡△BEFの結果を利用して、【予想】が成り立つことを次のように説明した。'
          + BX("あ", "FCD") + "、" + BX("い", "EF") + " に当てはまる記号を答えなさい。ただし、同じひらがなの□には共通するものがはいる。</div>"
          '<div class="frame"><b>【説明】</b><div class="rb">△AED≡△BEF より、△AED＝△BEF がいえるから、これを利用すると、<br>'
          '台形ABCDの面積は、△' + BX("あ", "FCD") + ' の面積と等しくなる。<br>'
          '一方、△AED≡△BEF より、ED＝' + BX("い", "EF") + ' だから、Eは線分DFの中点。<br>'
          'したがって、△DEC＝$\\dfrac12$△' + BX("あ", "FCD") + '＝$\\dfrac12$×（台形ABCD）より、△DECの面積は、台形ABCDの面積の $\\dfrac12$ になる。</div></div>'
          + W("台形ABCD＝△AED＋四角形EBCD＝△BEF＋四角形EBCD＝△FCD")
          + f'<div class="al">答　あ{A("FCD", "w20")}　い{A("EF", "w20")}</div></div>')
    t1 = Q("(1)", "台形ABCDの面積を求めなさい。",
           W(r"△AED≡△BEF より FB＝AD＝6cm。台形の高さを $h$ cm とすると、Eは辺ABの中点だから、EからADまでの高さは $\dfrac{h}{2}$ cm。<br>"
             r"△AED＝$\dfrac12\times6\times\dfrac{h}{2}=15$ より $h=10$<br>台形ABCD＝$\dfrac12\times(6+10)\times10=80$（cm²）"),
           A("80 cm²", "w20"), 21)
    t2 = Q("(2)", "線分BGの長さを求めなさい。",
           W(r"Eは線分DFの中点で、EG∥DC だから、Gは線分FCの中点（中点連結定理）。<br>"
             r"FC＝FB＋BC＝6＋10＝16（cm）より FG＝8cm<br>BG＝FG−FB＝8−6＝2（cm）"),
           A("2 cm", "w20"), 15)
    s3 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">3</span>図Ⅳは、図Ⅲにおいて、点Eを通って辺DCに平行な直線と辺BCとの交点をGとしたものである。'
          'AD＝6cm、BC＝10cmで、△AEDの面積が15cm²のとき、次の(1)、(2)の問いに答えなさい。</div>'
          f'{t1}{t2}</div><div class="fig"><b>図Ⅳ</b><br>{trap(4, 0.9)}</div></div></div>')
    p2 = f"""<section class="page tight">{header("大問4　合同・平行線と面積", "2/2")}
{s1}{s2}{s3}
</section>"""
    return p1 + p2


# ================= 大問5 =================
def d5():
    intro = (r'<div class="lead">図Ⅰで、直線 $\ell$ は関数 $y=-2x+12$、直線 $m$ は関数 $y=x+6$ のグラフである。Aは直線 $\ell$ と直線 $m$ との交点、B、Cはそれぞれ直線 $m$ と $x$ 軸、$y$ 軸との交点、'
             r'D、Eはそれぞれ直線 $\ell$ と $x$ 軸、$y$ 軸との交点である。<br>このとき、次の1〜4の問いに答えなさい。</div>')
    q1 = Q("1", r"関数 $y=-2x+12$ について、$x$ の増加量が4のときの $y$ の増加量を求めなさい。",
           W(r"変化の割合は $-2$ だから　$y$ の増加量＝$-2\times4=-8$"), A("$-8$", "w20"), 22)
    q2 = Q("2", "点Aの座標を求めなさい。",
           W(r"$y=-2x+12$ と $y=x+6$ を連立方程式として解く。<br>$-2x+12=x+6$　より　$-3x=-6$　$x=2$　　$y=2+6=8$"), A("(2, 8)", "w20"), 30)
    q3 = Q("3", "△ACEの面積を求めなさい。",
           W(r"C(0, 6)、E(0, 12) より CE＝12−6＝6。CEを底辺とすると、高さは点Aの $x$ 座標の2<br>$\dfrac12\times6\times2=6$"), A("6", "w20"), 28)
    q4 = Q("4", "図Ⅱは、図Ⅰにおいて、線分BD上に点Fを、△CBFと四角形ACFDの面積が等しくなるようにとったものである。このとき、直線CFの式を求めなさい。",
           W(r"B(−6, 0)、D(6, 0) より BD＝12。△ABD＝$\dfrac12\times12\times8=48$<br>"
             r"△CBF＝四角形ACFD＝$48\div2=24$ だから　$\dfrac12\times\mathrm{BF}\times6=24$　より BF＝8<br>"
             r"F の $x$ 座標は $-6+8=2$ だから F(2, 0)。直線CFは C(0, 6)、F(2, 0) を通るので、傾き $\dfrac{0-6}{2-0}=-3$、切片6"),
           A("$y=-3x+6$", "w30"), 40)
    return f"""<section class="page">{header("大問5　一次関数")}
<div class="flex"><div class="grow">{intro}{q1}{q2}</div><div class="fig"><b>図Ⅰ</b><br>{graph_svg()}</div></div>
{q3}
<div class="flex"><div class="grow">{q4}</div><div class="fig"><b>図Ⅱ</b><br>{graph_svg(True)}</div></div>
</section>"""


CSS = r"""
@page { size: A4; margin: 0; }
body { margin:0; font-family: "Noto Sans CJK JP", sans-serif; font-size: 10.3pt; color:#111; }
.page { width:210mm; height:297mm; box-sizing:border-box; padding:10mm 13mm; page-break-after: always; overflow:hidden; position:relative; }
.hd { border-bottom: 2px solid #333; padding-bottom: 2mm; margin-bottom: 3mm; display:flex; justify-content:space-between; align-items:flex-end; }
.ht { font-size: 14pt; font-weight: 700; white-space:nowrap; }
.tag { display:inline-block; font-size:9pt; background:#333; color:#fff; padding:1px 7px; margin-right:6px; border-radius:3px; vertical-align:middle; }
.key { display:inline-block; font-size:9pt; border:1.5px solid #c00; color:#c00; padding:0 6px; margin-left:8px; border-radius:3px; vertical-align:middle; }
.nm { font-size: 10pt; white-space:nowrap; }
.lead { line-height:1.7; margin: 1mm 0 2mm; }
.flex { display:flex; gap:4mm; align-items:flex-start; }
.grow { flex:1; min-width:0; }
.fig { flex:none; text-align:center; font-size:9pt; }
.grid2 { display:grid; grid-template-columns: 1fr 1fr; gap: 0 7mm; }
.q { margin: 0 0 2.5mm; }
.grid2 .q { display:flex; flex-direction:column; }
.grid2 .sp { flex:1; }
.qt { line-height:1.75; }
.no { display:inline-block; min-width:7mm; font-weight:700; }
.sp { margin: 0.5mm 0 0 7mm; }
.al { text-align:right; margin-top:1mm; }
.ch { margin: 1mm 0 1mm 7mm; line-height:1.75; }
.ch.row { margin-left:7mm; }
.frame { border:1.3px solid #333; border-radius:3px; padding:2mm 4mm; margin:2mm 0; line-height:1.75; }
.conv .ctitle { font-weight:700; }
.dl { margin: 0.6mm 0 0.6mm 2mm; line-height:1.7; text-indent:-2mm; padding-left:2mm; }
.sidet { flex:none; width:62mm; font-size:9pt; line-height:1.5; padding-left:2mm; }
.dt { border-collapse:collapse; margin:0.5mm 0 1.5mm; }
.dt td, .dt th { border:1px solid #333; padding:0.3mm 2mm; text-align:center; font-weight:400; font-size:9pt; }
.dt .cut { border-right:1px dashed #333; width:5mm; }
.hists { display:flex; justify-content:space-around; margin:1mm 0; font-size:9pt; }
.hist4 { margin: 1mm 0 0 7mm; font-size:9pt; }
svg text { font-family: "Noto Sans CJK JP", sans-serif; }
.pl { font-size: 11px; font-family: "KaTeX_Main", "Noto Sans CJK JP", serif !important; font-weight:700; }
.sm { font-size: 9px; } .ht2 { font-size: 10px; } .b2 { font-size:11px; }
.ax { font-style:italic; font-family: "KaTeX_Math", serif !important; font-size: 12px; }
.rb { margin: 1mm 0 0 3mm; }
.bx { display:inline-block; min-width:11mm; border:1px solid #333; border-radius:2px; text-align:center; padding:0 1.5mm; line-height:1.5; margin:0 0.5mm; vertical-align:baseline; }
.dotbox { display:inline-block; width:14mm; height:5mm; border:1px dashed #333; vertical-align:middle; }
.tight { padding-top:8mm; font-size:9.8pt; }
.tight .frame { line-height:1.65; margin:1.2mm 0; }
.tight .q { margin-bottom:1.5mm; }
.proof { padding:2mm 4mm; margin-top:2mm; }
.pbody { min-height:27mm; margin:1mm 0; border:1px dashed #888; padding:1mm 3mm; }
.lines { margin: 1mm 0 0 7mm; border:1px solid #999; padding:1mm 3mm; background-image: repeating-linear-gradient(transparent 0, transparent 7.2mm, #bbb 7.2mm, #bbb 7.4mm); line-height:7.4mm; }
.choice { margin: 1mm 0 1mm 7mm; }
.c1 { padding:0 1mm; }
table.mini { border-collapse:collapse; margin:1mm 0 0 4mm; }
table.mini td, table.mini th { border:1px solid #c33; padding:0 4mm; text-align:center; font-weight:400; }
/* 問題（mondai）と こたえ（kaitou） */
.ans { display:inline-block; vertical-align:middle; min-height:1.4em; padding:0 2px; text-align:center; border-bottom:1px solid #333; }
.w20 { min-width:20mm; } .w30 { min-width:30mm; }
.work, .lt { color:#c00; font-size:9pt; line-height:1.85; }
.lt { font-size:9.5pt; }
.kaitou .ans, .kaitou .ans .katex { color:#c00; font-weight:700; border-bottom-color:#c00; }
.kaitou .qa, .kaitou .qa .katex { color:#c00; font-weight:700; }
.kaitou .c1 { border:1.5px solid #c00; border-radius:50%; color:#c00; font-weight:700; padding:0.5mm 2.5mm; }
.mondai .ans, .mondai .ans .katex { color:transparent !important; }
.mondai .ans { overflow:hidden; white-space:nowrap; max-width:60mm; }
.mondai .work, .mondai .lt { visibility:hidden; }
.mondai .key { display:none; }
.mondai .qa { display:none; }
.kaitou .ql { display:none; }
"""


def build(body, mode):
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" href="file://{KATEX}/katex.min.css">'
            f'<script src="file://{KATEX}/katex.min.js"></script><script src="file://{KATEX}/contrib/auto-render.min.js"></script>'
            f'<style>{CSS}</style></head><body class="{mode}">{body}'
            '<script>renderMathInElement(document.body, {delimiters:[{left:"$", right:"$", display:false}], throwOnError:true});'
            'document.body.setAttribute("data-done","1");</script></body></html>')


JOBS = [("c3_jitsu_d1", d1), ("c3_jitsu_renritsu", d2), ("c3_jitsu_data", d3), ("c3_jitsu_zukei", d4), ("c3_jitsu_ichiji", d5)]

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
