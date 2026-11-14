"""実力テスト 令和4年度 3年・6月（大問1〜5）を、大問1／単元別の PDF にする。
問題（pdf/c3_jitsu_r406_*.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
部品・CSS は c3_jitsu_test.py などと共通。common.json の jitsu.tests の id は r4-3-06。

  大問1 小問集合（度数分布表・作図つき）     c3_jitsu_r406_d1
  大問2-1 確率（玉を戻して2回取り出す）      c3_jitsu_r406_kakuritsu
  大問2-2 方程式の利用（ハンバーグ）         c3_jitsu_r406_houtei
  大問3-1 比例と反比例（表）                 c3_jitsu_r406_hirei
  大問3-2 一次関数（直線と正方形）           c3_jitsu_r406_ichiji
  大問4 平面図形（合同・平行四辺形・面積）   c3_jitsu_r406_zukei
  大問5 空間図形（三角錐・展開図）           c3_jitsu_r406_kuukan

実行：cd tools && python3 c3_jitsu_r406.py
"""
from fractions import Fraction as F
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from c3_jitsu_test import A, W, BX, Q, lines, OUT  # noqa: E402
from c3_jitsu2_test import build  # noqa: E402
from c3_jitsu3_test import T, L, right_mark  # noqa: E402
from c3_jitsu5_test import _bis  # noqa: E402

# ================= 答えの確認 =================
assert -11 + 4 == -7 and -3 * 2 - 5 == -11 and F(-3, 2) / F(1, 4) == -6 and F(1, 2) - F(2, 5) == F(1, 10)
assert 3 * 2 + 4 * -1 == 2 and 2 * 2 - 5 * -1 == 9
C1, C2 = [2, 4, 17, 9, 8], [0, 5, 13, 12, 8]                   # 握力の度数分布表（15kg から 5kg ごと）
assert sum(C1) == 40 and sum(C2) == 38 and C1.index(max(C1)) == C2.index(max(C2)) == 2    # 最頻値が同じ → ウ
assert F(8, 40) != F(8, 38)
assert 3 * 3 + 2 * 2 == 13 and 3 * 2 * 2 == 12 and 5 * 5 == 25 and 5 * 4 // 2 == 10
assert 35 * 120 // 100 == 42 and F(12, 10) * 120 + F(13, 10) * 80 == 248
assert 2 * 18 / 6 == 6
assert F(7 - 4, 2) == F(3, 2) and -2 + 4 == 2 and F(4 + 5, 2) * 2 == 9
assert 180 - 55 - 45 == 80 and 2 * (4 + 9) == 26 and 2 + 5 + 2 == 9
assert F(1, 3) * 18 * 12 == 72 and 144 - 36 - 18 - 36 == 54 and F(72 * 3, 54) == 4

TAG = "令和4年度　3年・6月"


def header(title, page=None):
    p = f"（{page}）" if page else ""
    return (f'<div class="hd"><div class="ht"><span class="tag">{TAG}</span>{title}{p}<span class="key">解答</span></div>'
            '<div class="nm">　月　　日　名前（　　　　　　　　　）</div></div>')


# ================= 図 =================
def quad_svg():
    """四角形ABCD。作図（∠ABC の二等分線＝折り目 ℓ）は .cons＝こたえだけ"""
    k = 0.5
    B_ = (20, 160)
    P = lambda x, y: (B_[0] + x * k, B_[1] - y * k)
    A_, C_, D_ = P(50, 270), P(300, 5), P(280, 245)
    s = f'<polygon points="{A_[0]:.1f},{A_[1]:.1f} {B_[0]},{B_[1]} {C_[0]:.1f},{C_[1]:.1f} {D_[0]:.1f},{D_[1]:.1f}" fill="none" stroke="#000" stroke-width="1.3"/>'
    s += T(A_[0] - 2, A_[1] - 6, "A") + T(B_[0] - 8, B_[1] + 8, "B") + T(C_[0] + 8, C_[1] + 8, "C") + T(D_[0] + 6, D_[1] - 4, "D")
    a1 = math.degrees(math.atan2(270, 50))
    a2 = math.degrees(math.atan2(5, 300))
    c, am = _bis(B_, a1, a2, 34, 30)
    end = (B_[0] + 205 * math.cos(math.radians(am)), B_[1] - 205 * math.sin(math.radians(am)))
    c += L(B_, end, 1.4) + T(end[0] + 6, end[1] + 2, '<tspan class="ax">ℓ</tspan>', "pl", "start")
    return f'<svg width="{C_[0] + 30:.0f}" height="{B_[1] + 14}" viewBox="0 0 {C_[0] + 30:.0f} {B_[1] + 14}">{s}<g class="cons">{c}</g></svg>'


def bag_svg():
    s = ('<path d="M42 12 Q60 4 78 12 Q72 24 74 34 Q108 52 104 92 Q100 128 60 128 Q20 128 16 92 Q12 52 46 34 Q48 24 42 12 Z" fill="#fff" stroke="#000" stroke-width="1.2"/>')
    for (x, y, red) in [(44, 62, 1), (84, 60, 0), (64, 84, 1), (38, 100, 1), (82, 106, 0)]:
        s += f'<circle cx="{x}" cy="{y}" r="11" fill="{"#aaa" if red else "#fff"}" stroke="#000" stroke-width="1"/>'
    return f'<svg width="120" height="134" viewBox="0 0 120 134">{s}</svg>'


def graph_svg():
    sc = 20
    ox, oy = 4 * sc + 10, 9 * sc + 10
    X = lambda x: ox + x * sc
    Y = lambda y: oy - y * sc
    s = L((X(-4), Y(0)), (X(9.5), Y(0)), 1) + L((X(0), Y(-2.2)), (X(0), Y(9.3)), 1)
    s += T(X(9.5) + 6, Y(0) + 4, '<tspan class="ax">x</tspan>', "pl") + T(X(0) + 2, Y(9.3) - 4, '<tspan class="ax">y</tspan>', "pl") + T(X(0) - 8, Y(0) + 14, "O", "sm")
    s += L((X(-3.8), Y(7.8)), (X(6), Y(-2))) + L((X(-4), Y(-2)), (X(3.4), Y(9.1)))
    s += T(X(-3.8) - 4, Y(7.8) - 6, '<tspan class="ax">y</tspan>＝−<tspan class="ax">x</tspan>＋4', "sm", "start") + T(X(3.4) + 6, Y(9.1) + 4, '<tspan class="ax">ℓ</tspan>', "pl", "start")
    s += f'<polygon points="{X(2)},{Y(7)} {X(2)},{Y(2)} {X(7)},{Y(2)} {X(7)},{Y(7)}" fill="none" stroke="#000" stroke-width="1.1"/>'
    s += L((X(0), Y(0)), (X(2), Y(2)), 1) + L((X(4), Y(0)), (X(7), Y(2)), 1)
    s += T(X(2) - 10, Y(7) - 4, "P") + T(X(7) + 8, Y(7) - 2, "S") + T(X(2) - 12, Y(2) + 4, "Q") + T(X(7) + 9, Y(2) + 4, "R") + T(X(0) - 10, Y(4) + 4, "A") + T(X(4) + 2, Y(0) + 14, "B")
    return f'<svg width="{X(9.5) + 20}" height="{Y(-2.2) + 4}" viewBox="0 0 {X(9.5) + 20} {Y(-2.2) + 4}">{s}</svg>'


def tri4_svg():
    k = 26
    bc = 10
    ab = bc * math.sin(math.radians(45)) / math.sin(math.radians(80))
    B_ = (0.0, 0.0)
    C_ = (bc, 0.0)
    A_ = (ab * math.cos(math.radians(55)), ab * math.sin(math.radians(55)))
    vab = (A_[0] - B_[0], A_[1] - B_[1])
    D_ = (C_[0] + 0.4 * vab[0], C_[1] + 0.4 * vab[1])
    F_ = (A_[0] + 0.4 * vab[0], A_[1] + 0.4 * vab[1])
    E_ = ((A_[0] + D_[0]) / 2, (A_[1] + D_[1]) / 2)
    top = F_[1]
    S = lambda p: (24 + p[0] * k, 20 + (top - p[1]) * k)
    a, b, c, d, e, f = map(S, (A_, B_, C_, D_, E_, F_))
    s = L(f, b) + L(b, c) + L(c, d) + L(d, a) + L(a, c) + L(f, c) + L(f, d)
    s += T(a[0] - 10, a[1] + 2, "A") + T(b[0] - 8, b[1] + 12, "B") + T(c[0] + 6, c[1] + 12, "C") + T(d[0] + 9, d[1] + 4, "D") + T(e[0] + 4, e[1] - 6, "E") + T(f[0], f[1] - 6, "F")
    W_ = max(c[0], d[0]) + 26
    return f'<svg width="{W_:.0f}" height="{b[1] + 18:.0f}" viewBox="0 0 {W_:.0f} {b[1] + 18:.0f}">{s}</svg>'


def tetra_svg():
    A_, B_, C_, D_ = (24, 110), (136, 110), (82, 22), (24, 330)
    s = L(A_, B_) + L(A_, C_) + L(C_, B_) + L(A_, D_) + L(B_, D_) + L(C_, D_, 1, True)
    s += right_mark(A_, (1, 0), (0, 1), 7)
    s += T(A_[0] - 10, A_[1] + 4, "A") + T(B_[0] + 9, B_[1] + 4, "B") + T(C_[0], C_[1] - 6, "C") + T(D_[0], D_[1] + 14, "D")
    return f'<svg width="160" height="350" viewBox="0 0 160 350">{s}</svg>'


def net_svg():
    k = 15
    o = (16, 18)
    P = lambda x, y: (o[0] + x * k, o[1] + y * k)
    s = f'<rect x="{o[0]}" y="{o[1]}" width="{12 * k}" height="{12 * k}" fill="none" stroke="#000" stroke-width="1.2"/>'
    C_, B_, D_ = P(6, 0), P(12, 6), P(0, 12)
    s += L(D_, C_) + L(C_, B_) + L(B_, D_)
    s += T(o[0] - 4, o[1] - 5, "A") + T(C_[0], C_[1] - 5, "C") + T(P(12, 0)[0] + 4, o[1] - 5, "A") + T(B_[0] + 9, B_[1] + 4, "B") + T(P(12, 12)[0] + 8, P(12, 12)[1] + 10, "A") + T(D_[0] - 6, D_[1] + 12, "D")
    return f'<svg width="{12 * k + 44}" height="{12 * k + 40}" viewBox="0 0 {12 * k + 44} {12 * k + 40}">{s}</svg>'


# ================= 大問1 =================
def d1():
    c = [Q("(1)", r"$-11+4$ を計算しなさい。", W(r"$-(11-4)$"), A("$-7$"), 1),
         Q("(2)", r"$(-3)\times2-5$ を計算しなさい。", W(r"$-6-5$"), A("$-11$"), 1),
         Q("(3)", r"$-\dfrac32\div\dfrac14$ を計算しなさい。", W(r"$-\dfrac32\times4$"), A("$-6$"), 1),
         Q("(4)", r"$\dfrac12a-\dfrac25a$ を計算しなさい。", W(r"$\dfrac{5}{10}a-\dfrac{4}{10}a$"), A(r"$\dfrac{1}{10}a$"), 1),
         Q("(5)", r"$7x-4+2(1-x)$ を計算しなさい。", W(r"$7x-4+2-2x$"), A(r"$5x-2$"), 1),
         Q("(6)", r"連立方程式 $\begin{cases}3x+4y=2\\2x-5y=9\end{cases}$ を解きなさい。",
           W(r"上×2 $6x+8y=4$、下×3 $6x-15y=27$<br>ひいて $23y=-23$　$y=-1$　$x=2$"), A(r"$x=2,\ y=-1$"), 1)]
    c7 = Q("(7)", r"$y$ は $x$ に比例し、$x=3$ のとき $y=-6$ である。$y$ を $x$ の式で表しなさい。", W(r"$y=ax$ に代入して $-6=3a$　$a=-2$"), A(r"$y=-2x$"), 1)
    rows = "".join(f"<tr><td>{15 + 5 * i}〜{20 + 5 * i}</td><td>{a}</td><td>{b}</td></tr>" for i, (a, b) in enumerate(zip(C1, C2)))
    tbl = ('<table class="tb"><tr><th rowspan="2">記録(kg)</th><th>1組</th><th>2組</th></tr><tr><th>度数(人)</th><th>度数(人)</th></tr>'
           f'{rows}<tr><td>合計</td><td>40</td><td>38</td></tr></table><div style="font-size:7.5pt;text-align:center">（以上〜未満）</div>')
    c8 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(8)</span>右の表は、ある中学校3年生の、1組40人と2組38人の生徒の握力の記録を、度数分布表に整理したものである。'
          'この度数分布表からわかることについて述べた文として<b>適切なもの</b>を、次のア〜エから1つ選び、記号で答えなさい。</div>'
          '<div class="ch">ア　1組と2組それぞれの記録において、最小値は同じである。<br>イ　1組と2組それぞれの記録において、中央値をふくむ階級は同じである。<br>'
          'ウ　1組と2組それぞれの記録において、最頻値は同じである。<br>エ　1組と2組それぞれの記録において、35kg以上40kg未満の階級における相対度数は同じである。</div>'
          + W(r"ア：最小値の階級は1組15〜20kg、2組20〜25kg。イ：中央値の階級は1組25〜30kg、2組30〜35kg。<br>"
              r"ウ：最頻値はどちらも 27.5kg（25〜30kg）。エ：8÷40＝0.2、8÷38＝0.21…")
          + f'</div><div class="fig">{tbl}</div></div><div class="al">答　{A("ウ", "w20")}</div></div>')
    c9 = ('<div class="q"><div class="flex"><div class="grow"><div class="qt"><span class="no">(9)</span>右の図のような四角形ABCDの紙を、辺ABが辺BCと重なるように折ったとき、折り目となる直線 $\\ell$ をコンパスと定規を使って作図しなさい。作図に用いた線は消さずに残しておくこと。</div>'
          + W(r"辺ABと辺BCが重なる折り目は、$\angle\mathrm{ABC}$ の二等分線。<br>Bを中心に円をかき、BA・BCとの交点を中心に同じ半径の円をかいて、その交点とBを結ぶ。")
          + f'</div><div class="fig">{quad_svg()}</div></div></div>')
    return f"""<section class="page tight">{header("大問1　小問集合")}
<div class="lead">次の(1)〜(9)の問いに答えなさい。</div>
<div class="grid2">{"".join(c)}{c7}</div>
{c8}{c9}
</section>"""


# ================= 大問2-1 確率 =================
def d2a():
    d = lambda who, t: f'<p class="dl"><b>{who}：</b>{t}</p>'
    kadai = ('<div class="frame"><b>【課題】</b><div class="flex"><div class="grow">袋の中に赤玉が3個、白玉が2個、あわせて5個の玉が入っている。この袋から玉を1個取り出して色を調べ、それを袋に戻してから、また玉を1個取り出して色を調べる。'
             'このとき、1回目と2回目に取り出した玉の色が同じである場合と、異なる場合では、どちらのほうが起こりやすいか、答えなさい。ただし、どの玉の取り出し方も同様に確からしいとする。</div>'
             f'<div class="fig">{bag_svg()}</div></div></div>')
    kaiwa = ('<div class="frame"><b>【会話】</b>'
             + d("こうた", "同時に2個の玉を取り出すのではなくて、1個の玉を取り出して色を調べたら袋に戻すというのがポイントだね。")
             + d("もね", "なるほど。同時に2個の玉を取り出す場合の玉の取り出し方は、全部で " + BX("①", "10") + " 通りだよね。でも、この【課題】の玉の取り出し方は、全部で " + BX("②", "25") + " 通りかな。")
             + d("こうた", "そのとおりだね。ぼくは、1回目と2回目に取り出した玉の色が同じである場合のほうが起こりやすいと思うな。")
             + d("もね", "私は、1回目と2回目に取り出した玉の色が異なる場合のほうが起こりやすい気がするよ。")
             + d("こうた", '<span class="ul">では、それぞれの確率を求めて、どちらの場合のほうが起こりやすいか調べてみよう。</span>') + '</div>')
    q1 = Q("(1)", "【会話】の中の " + BX("①", "10") + "、" + BX("②", "25") + " にあてはまる数の組み合わせとして適切なものを、次のア〜エから1つ選び、記号で答えなさい。"
           '<div class="ch">ア　①10　②20　　　イ　①10　②25　　　ウ　①20　②20　　　エ　①20　②25</div>',
           W(r"同時に2個：5個から2個の組み合わせ $\dfrac{5\times4}{2}=10$（通り）　戻して2回：$5\times5=25$（通り）"), A("イ", "w20"), 6)
    q2 = Q("(2)", "【会話】の中の下線部について、どちらの場合のほうが起こりやすいか、それぞれの確率を求めて説明しなさい。",
           lines(r"赤玉を①②③、白玉を④⑤とすると、取り出し方は全部で25通り。<br>"
                 r"色が同じ：赤→赤 $3\times3=9$ 通り、白→白 $2\times2=4$ 通りで 13通り。確率は $\dfrac{13}{25}$<br>"
                 r"色が異なる：赤→白 $3\times2=6$ 通り、白→赤 $2\times3=6$ 通りで 12通り。確率は $\dfrac{12}{25}$<br>"
                 r"$\dfrac{13}{25}>\dfrac{12}{25}$ なので、<b>色が同じである場合</b>のほうが起こりやすい。", 40), "", 0)
    return f"""<section class="page">{header("大問2-1　確率")}
<div class="lead">こうたさんともねさんは、次の【課題】について考えた。下の【会話】は、2人が話し合っている場面の一部である。このとき、下の(1)、(2)の問いに答えなさい。</div>
{kadai}{kaiwa}{q1}{q2}
</section>"""


# ================= 大問2-2 方程式の利用 =================
def d2b():
    t1 = ('<div><b>【表Ⅰ】ハンバーグ本体</b><table class="tb" style="margin:1mm 0"><tr><th colspan="2">●ハンバーグ1個分の分量</th></tr><tr><th>材料</th><th>分量(g)</th></tr>'
          + "".join(f"<tr><td>{n}</td><td>{g}</td></tr>" for n, g in [("豚ひき肉", 100), ("玉ねぎ", 35), ("バター", 3), ("卵", 17), ("パン粉", 4), ("牛乳", 15), ("こしょう", 1), ("サラダ油", 4)])
          + '</table></div>')
    t2 = ('<div><b>【表Ⅱ】ハンバーグソース</b><table class="tb" style="margin:1mm 0"><tr><th colspan="2">●材料1mLあたりのカロリー</th></tr><tr><th>材料</th><th>カロリー(kcal)</th></tr>'
          '<tr><td>ケチャップ</td><td>1.2</td></tr><tr><td>とんかつソース</td><td>1.3</td></tr></table></div>')
    q1 = Q("(1)", "ひかるさんの家には、豚ひき肉が120gある。この豚ひき肉を全部使って、調理実習でつくった分量と同じ割合のハンバーグをつくるとき、玉ねぎは何g必要か、求めなさい。",
           W(r"玉ねぎを $x$ g とすると　$100:35=120:x$　$100x=4200$　$x=42$"), A("42g", "w20"), 24)
    q2 = Q("(2)", r"ハンバーグソースを200mLつくるとき、ハンバーグソースのカロリーは248kcalになった。このとき、ケチャップととんかつソースをそれぞれ何mL使ったか、使ったケチャップの量を $x$ mLとして、方程式を使って求めなさい。ただし、答えを求める過程がわかるように、式と計算も書きなさい。",
           W(r"とんかつソースは $(200-x)$ mL。カロリーの合計から　$1.2x+1.3(200-x)=248$<br>"
             r"両辺を10倍して　$12x+13(200-x)=2480$　$12x+2600-13x=2480$　$-x=-120$　$x=120$<br>とんかつソースは $200-120=80$（mL）"),
           "ケチャップ：" + A("120mL", "w20") + "　とんかつソース：" + A("80mL", "w20"), 46)
    return f"""<section class="page">{header("大問2-2　方程式の利用")}
<div class="lead">ひかるさんは、学校の調理実習でつくった分量と同じ割合のハンバーグを、家にある材料でつくることにした。下の【表Ⅰ】は、ハンバーグ本体1個分の材料とその分量を、【表Ⅱ】はハンバーグソースに使うケチャップととんかつソースの、1mLあたりのカロリーを調べてまとめたものである。
このとき、下の(1)、(2)の問いに答えなさい。</div>
<div class="flex" style="justify-content:space-around;align-items:flex-start">{t1}{t2}</div>
{q1}{q2}
</section>"""


# ================= 大問3-1 比例と反比例 =================
def ex_box(title, ys, text):
    xs = ["…", "0", "…", "2", "…", "6", "…"]
    cells_x = "".join(f"<td>{v}</td>" for v in xs)
    cells_y = "".join(f"<td>{v}</td>" for v in ys)
    return (f'<div style="margin:2mm 0 0 7mm"><b>{title}</b><div class="frame" style="margin-top:1mm"><div class="flex" style="align-items:center">'
            f'<table class="extbl"><tr><th><i>x</i></th>{cells_x}</tr><tr><th><i>y</i></th>{cells_y}</tr></table><div class="grow" style="padding-left:3mm">{text}</div></div></div></div>')


def d3a():
    box = '<span style="display:inline-block;width:9mm;height:5mm;border:1px solid #333;vertical-align:middle"></span>'
    e1 = ex_box("【例1】", ["…", "0", "…", "18", "…", box, "…"], "$y$ は $x$ に比例するから、<br>表の空欄にあてはまる値は54である。")
    e2 = ex_box("【例2】", ["…", "×", "…", "18", "…", box, "…"], "$y$ は $x$ に反比例するから、<br>表の空欄にあてはまる値は " + BX("ア", "6") + " である。")
    q = Q("1", "次の【例1】は、$y$ が $x$ に比例する例を、【例2】は、$y$ が $x$ に反比例する例を表に示している。【例1】を参考にして、下の【例2】について、" + BX("ア", "6") + " にあてはまる数を求めなさい。"
          + e1 + e2,
          W(r"反比例は $xy$ の値が一定。$x=2$ のとき $y=18$ だから $xy=36$（$y=\dfrac{36}{x}$）<br>$x=6$ のとき　$y=36\div6=6$"), A("6", "w20"), 18)
    return f"""<section class="page">{header("大問3-1　比例と反比例")}
{q}
</section>"""


# ================= 大問3-2 一次関数 =================
def d3b():
    q1 = Q("(1)", "点Aの $y$ 座標を求めなさい。", W(r"Aは $y=-x+4$ と $y$ 軸の交点なので、$x=0$ を代入"), A("4", "w20"), 10)
    q2 = Q("(2)", r"直線 $\ell$ の式を求めなさい。", W(r"$\ell$ は A$(0,\ 4)$ と P$(2,\ 7)$ を通る。傾き $\dfrac{7-4}{2-0}=\dfrac32$、切片4"), A(r"$y=\dfrac32x+4$", "w30"), 14)
    q3 = Q("(3)", "四角形OBRQの面積を求めなさい。",
           W(r"Qは $x=2$ で $y=-2+4=2$ → Q$(2,\ 2)$。PQ＝$7-2=5$ なので R$(7,\ 2)$。B$(4,\ 0)$<br>"
             r"OB と QR はどちらも $x$ 軸に平行な台形。OB＝4、QR＝5、高さ2<br>$\dfrac12\times(4+5)\times2=9$"), A("9", "w20"), 26)
    return f"""<section class="page">{header("大問3-2　一次関数")}
<div class="lead"><b>2</b>　図のように、直線 $\\ell$ と直線 $y=-x+4$ が、$y$ 軸上の点Aで交わっており、点Bは直線 $y=-x+4$ と $x$ 軸の交点である。直線 $\\ell$ 上に点P$(2,\\ 7)$ をとり、線分PQが $y$ 軸に平行になるように、直線 $y=-x+4$ 上に点Qをとる。また、四角形PQRSが正方形となるように、点R、Sをとる。ただし、点Rの $x$ 座標は、点Qの $x$ 座標より大きいものとする。
このとき、次の(1)〜(3)の問いに答えなさい。</div>
<div class="flex"><div class="grow">{q1}{q2}{q3}</div><div class="fig">{graph_svg()}</div></div>
</section>"""


# ================= 大問4 平面図形 =================
def d4():
    q1 = Q("1", r"$\angle\mathrm{ABC}=55^\circ$、$\angle\mathrm{ACB}=45^\circ$ のとき、$\angle\mathrm{ACD}$ の大きさを求めなさい。",
           W(r"$\angle\mathrm{BAC}=180^\circ-55^\circ-45^\circ=80^\circ$。AB∥DC より錯角は等しいから $\angle\mathrm{ACD}=\angle\mathrm{BAC}$"), A(r"$80^\circ$", "w20"), 10)
    q2 = Q("2", "△AEF≡△DECであることを証明しなさい。",
           lines(r"△AEFと△DECで、<br>仮定より　AE＝DE　……①<br>対頂角は等しいから　$\angle\mathrm{AEF}=\angle\mathrm{DEC}$　……②<br>"
                 r"AB∥DC より AF∥DC で、平行線の錯角は等しいから　$\angle\mathrm{FAE}=\angle\mathrm{CDE}$　……③<br>"
                 r"①、②、③より、1組の辺とその両端の角がそれぞれ等しいから、△AEF≡△DEC", 40), "", 0)
    q3 = '<div class="q"><div class="qt"><span class="no">3</span>BA：AF＝5：2であるとき、次の(1)、(2)の問いに答えなさい。</div></div>'
    t1 = Q("(1)", "BA＝10cm、CA＝9cmのとき、四角形ACDFの周の長さを求めなさい。",
           W(r"AF＝$10\times\dfrac25=4$（cm）。△AEF≡△DEC より AE＝DE、FE＝CE なので、対角線がそれぞれの中点で交わり、四角形ACDFは平行四辺形。<br>"
             r"DC＝AF＝4cm、DF＝CA＝9cm　周の長さ $2\times(4+9)=26$"), A("26cm", "w20"), 12)
    t2 = Q("(2)", "四角形FBCDの面積は△AEFの面積の何倍か、求めなさい。",
           W(r"△AEF＝$S$ とする。平行四辺形ACDFは対角線で4つの面積の等しい三角形に分かれるので、△ACF＝$2S$、△FCD＝$2S$<br>"
             r"△ABCと△ACFは高さが同じで、底辺の比 BA：AF＝5：2 だから　△ABC＝$5S$<br>四角形FBCD＝△ABC＋△ACF＋△FCD＝$5S+2S+2S=9S$"), A("9倍", "w20"), 18)
    return f"""<section class="page">{header("大問4　平面図形（合同・面積）")}
<div class="flex"><div class="grow"><div class="lead">下の図のように、AB∥DCである四角形ABCDがあり、辺ADの中点をE、CEの延長とBAの延長との交点をFとする。点AとC、点DとFをそれぞれ結ぶ。<br>このとき、下の1〜3の問いに答えなさい。</div></div>
<div class="fig">{tri4_svg()}</div></div>
{q1}{q2}{q3}{t1}{t2}
</section>"""


# ================= 大問5 空間図形 =================
def d5():
    q1 = Q("1", "図Ⅰにおいて、面ADBと垂直な辺はどれか、答えなさい。", W("辺ACは、面ADB上の2本の辺AB・ADの両方に垂直（∠BAC＝∠CAD＝90°）。"), A("辺AC", "w20"), 8)
    q2 = Q("2", "この三角錐DABCの体積を求めなさい。", W(r"底面△ABC＝$\dfrac12\times6\times6=18$、高さAD＝12　$\dfrac13\times18\times12=72$"), A("72cm³", "w20"), 12)
    q3 = Q("3", "図Ⅱは、図Ⅰの三角錐DABCの展開図である。△BCDの面積を求めなさい。",
           W(r"展開図は1辺12cmの正方形。正方形から、まわりの3つの直角三角形をひく。<br>"
             r"$144-\dfrac12\times12\times6-\dfrac12\times6\times6-\dfrac12\times12\times6=144-36-18-36=54$"), A("54cm²", "w20"), 16)
    q4 = Q("4", "△BCDを底面としたとき、三角錐DABCの高さを求めなさい。",
           W(r"体積は72cm³で同じ。高さを $h$ とすると　$\dfrac13\times54\times h=72$　$18h=72$　$h=4$"), A("4cm", "w20"), 16)
    return f"""<section class="page">{header("大問5　空間図形")}
<div class="flex"><div class="grow"><div class="lead">図Ⅰの三角錐DABCで、面ABC、ADB、ADCはそれぞれ $\\angle\\mathrm{{BAC}}=\\angle\\mathrm{{BAD}}=\\angle\\mathrm{{CAD}}=90^\\circ$ の直角三角形である。AB＝AC＝6cm、AD＝12cmであるとき、次の1〜4の問いに答えなさい。</div>
{q1}{q2}</div><div class="fig"><b>図Ⅰ</b><br>{tetra_svg()}</div></div>
<div class="flex"><div class="grow">{q3}{q4}</div><div class="fig"><b>図Ⅱ</b><br>{net_svg()}</div></div>
</section>"""


EXTRA = r"""
.tb td, .tb th { padding:0.6mm 3mm !important; }
.extbl { border-collapse:collapse; font-size:9.5pt; }
.extbl th, .extbl td { padding:1mm 2.6mm; text-align:center; font-weight:400; }
.extbl tr:first-child th, .extbl tr:first-child td { border-bottom:1px solid #333; }
.extbl th { border-right:1px solid #333; font-family:"KaTeX_Math", serif; }
"""


def build2(body, mode):
    return build(body, mode).replace("</style>", EXTRA + "</style>", 1)


JOBS = [("c3_jitsu_r406_d1", d1), ("c3_jitsu_r406_kakuritsu", d2a), ("c3_jitsu_r406_houtei", d2b),
        ("c3_jitsu_r406_hirei", d3a), ("c3_jitsu_r406_ichiji", d3b), ("c3_jitsu_r406_zukei", d4), ("c3_jitsu_r406_kuukan", d5)]

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
                hp.write_text(build2(body, mode), encoding="utf-8")
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
