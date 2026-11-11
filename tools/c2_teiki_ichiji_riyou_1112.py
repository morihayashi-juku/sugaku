"""中2 定期テスト対策（一次関数の利用）11/12（木）用：1ページ＝1テーマ×3ページ＋こたえ3ページ（赤で書きこみ）

  cd tools && python3 c2_teiki_ichiji_riyou_1112.py

- 形は 11/9（月）の c2_teiki_ichiji_riyou_mon.py と同じ（全幅・大問1問・計算スペース広め）。数値と場面を変えた。
  ①速さ（途中で速さが変わる・追いかけ）②動点（長方形・△ABP・グラフをかく）③グラフと面積（交点・2等分線・点P）
- ③の図はマス目なし。座標・式は問題文に書く。
- 出力：pdf/c2_teiki_ichiji_riyou_1112.pdf（3ページ）と c2_teiki_ichiji_riyou_1112_ans.pdf（3ページ）
"""
from fractions import Fraction as F

import sympy as sp

from texlib import doc, tex as T, write_pdfs
from c2_teiki_ichiji_riyou_thu import Plane, line2, pt_tex, dot_pattern, rect_fig, dot_solutions, piece_of
from c2_teiki_ichiji_riyou_mon import CSS, page, blank, coord_svg, X, Y, RED, BLUE

FILE = "c2_teiki_ichiji_riyou_1112"


# ---------- ① 速さ ----------
AA = [(0, 0), (10, 600), (22, 2400)]          # Aさん：歩く → 走る
FA = [(11, 0), (19, 2400)]                    # 父：自転車


def speed_answers():
    x = sp.symbols("x")
    v1 = F(600, 10)
    v2 = F(2400 - 600, 22 - 10)
    a_run = sp.expand(600 + v2 * (x - 10))
    vf = F(2400, 19 - 11)
    f = sp.expand(vf * (x - 11))
    t = sp.solve(sp.Eq(a_run, f), x)[0]
    rem = 2400 - a_run.subs(x, 19)
    r = (v1, v2, str(a_run), vf, str(f), t, a_run.subs(x, t), rem)
    assert r == (60, 150, "150*x - 900", 300, "300*x - 3300", 16, 1500, 450), r
    assert 10 <= t <= 22 and 11 <= t <= 19
    return r


def page_speed(a=False):
    speed_answers()
    b = lambda w, v: blank(w, v, a)
    story = (f"Aさんは、家から2400m離れた駅に向かった。はじめは歩いていたが、途中から走って駅に向かった。"
             f"Aさんが家を出発してから11分後に、父が家を出発し、同じ道を自転車でAさんを追いかけた。<br>"
             f"右のグラフは、Aさんが家を出発してから {X} 分後の家からの道のりを {Y} m として、2人のようすを表したものである。"
             f"歩く速さ、走る速さ、父の速さは、それぞれ一定とする。")
    P = Plane((0, 24), (0, 2600), 104 / 24, 74 / 2600, (1, 5), (100, 200), xu="（分）", yu="（m）", mr=17, ml=11)
    P.poly(AA, RED, .75)
    P.text(22, 2400, "Aさん", 1.4, 1.4, "start", 4.2, f'style="fill:{RED};font-weight:700"')
    P.poly(FA, BLUE, .75)
    P.text(19, 2400, "父", -1.4, -1.6, "end", 4.4, f'style="fill:{BLUE};font-weight:700"')
    qs = [
        ("Aさんが歩いた速さは分速何mですか。", f"答　分速{b(22, '60')}m", 1,
         f"10分で600m進んでいるから　{T('600\\div10=60')}"),
        (f"Aさんが走っているときの {X} と {Y} の関係を式で表しなさい。また、{X} の変域も答えなさい。",
         f"答　式{b(50, T('y=150x-900'))}　変域{b(36, T('10\\leqq x\\leqq 22'))}", 1.25,
         f"走る速さは {T('(2400-600)\\div(22-10)=150')}（分速150m）。"
         f"{T('y=150x+b')} に {T('(10,\\ 600)')} を代入して {T('600=1500+b')}、{T('b=-900')}"),
        (f"父が家を出発してから駅に着くまでの {X} と {Y} の関係を式で表しなさい。また、{X} の変域も答えなさい。",
         f"答　式{b(50, T('y=300x-3300'))}　変域{b(36, T('11\\leqq x\\leqq 19'))}", 1.25,
         f"父の速さは {T('2400\\div(19-11)=300')}（分速300m）。"
         f"{T('y=300x+b')} に {T('(11,\\ 0)')} を代入して {T('0=3300+b')}、{T('b=-3300')}"),
        ("父がAさんに追いつくのは、Aさんが家を出発してから何分後ですか。また、それは家から何mの地点ですか。",
         f"答　{b(18, '16')}分後、家から{b(20, '1500')}m", 1.25,
         f"グラフより、追いつくのはAさんが走っているとき。<br>{T('150x-900=300x-3300')}　{T('-150x=-2400')}　{T('x=16')}<br>"
         f"{T('y=150\\times16-900=1500')}"),
        ("父が駅に着いたとき、Aさんは駅まであと何mのところにいますか。", f"答　{b(22, '450')}m", 1.1,
         f"父が着くのは {T('x=19')}。Aさんは {T('y=150\\times19-900=1950')}　{T('2400-1950=450')}"),
    ]
    return page(1, "速さ（ダイヤグラム）", story, P.svg(), qs, a)


# ---------- ② 動点 ----------
DOTM = dot_pattern("BCDA", "ABP", 12, 8, 2, 3, 32, (0, 2), ["", "", ""])


def dot_grid(answer=False):
    d = DOTM
    P = Plane((0, 16), (0, 56), 112 / 16, 56 / 56, (1, 2), (4, 8), xu="（秒）", yu="（cm²）", mr=17, ml=10)
    if answer:
        P.poly(list(zip(d["ts"], d["ys"])), RED, .8)
    return P.svg()


def page_dot(a=False):
    d = DOTM
    assert [(lo, hi, int(p), int(q)) for lo, hi, p, q in d["pieces"]] == [(0, 6, 8, 0), (6, 10, 0, 48), (10, 16, -8, 128)]
    assert piece_of(d, 3) == 24 and [int(s[0]) for s in dot_solutions(d)] == [4, 12]
    b = lambda w, v: blank(w, v, a)
    story = (f"右の図のような、AB＝8cm、BC＝12cm の長方形ABCDがある。点Pは、頂点Bを出発して、辺BC、CD、DA上を、"
             f"毎秒2cmの速さで頂点Aまで動く。点PがBを出発してから {X} 秒後の △ABP の面積を {Y} cm² とする。"
             f"ただし、点PがB、Aにあるときは {T('y=0')} とする。")
    qs = [
        (f"{T('x=3')} のときの {Y} の値を求めなさい。", f"答　{Y}＝{b(22, '24')}", 1,
         f"3秒後、点Pは辺BC上で BP＝{T('2\\times3=6')} cm。{T('y=\\dfrac12\\times8\\times6=24')}"),
        (f"点Pが辺BC上を動くとき（{T('0\\leqq x\\leqq 6')}）、{Y} を {X} の式で表しなさい。", f"答　{b(50, T('y=8x'))}", 1,
         f"BP＝{T('2x')} cm、底辺AB＝8cm だから　{T('y=\\dfrac12\\times8\\times2x=8x')}"),
        (f"点Pが辺DA上を動くとき（{T('10\\leqq x\\leqq 16')}）、{Y} を {X} の式で表しなさい。", f"答　{b(50, T('y=-8x+128'))}", 1.15,
         f"Pが D に着くのは {T('(12+8)\\div2=10')} 秒後。そこから AP＝{T('12-2(x-10)=-2x+32')} (cm)<br>"
         f"{T('y=\\dfrac12\\times8\\times(-2x+32)=-8x+128')}"),
        ("△ABPの面積が32cm² になるのは、点PがBを出発してから何秒後ですか。すべて答えなさい。",
         f"答　{b(20, '4')}秒後、{b(20, '12')}秒後", 1.15,
         f"辺BC上：{T('8x=32')}　{T('x=4')}　辺CD上：{T('y=\\dfrac12\\times8\\times12=48')} で一定なので32にならない<br>"
         f"辺DA上：{T('-8x+128=32')}　{T('x=12')}"),
        (f"{X} と {Y} の関係を表すグラフを、下の図にかきなさい（{T('0\\leqq x\\leqq 16')}）。", "", 0,
         f"点 {T('(0,\\ 0)')}、{T('(6,\\ 48)')}、{T('(10,\\ 48)')}、{T('(16,\\ 0)')} を順に線分で結ぶ",
         f"<div class=gw>{dot_grid(a)}</div>"),
    ]
    return page(2, "動点", story, rect_fig(d, s=4.0), qs, a)


# ---------- ③ グラフと面積 ----------
A3, D3 = (-4, 0), (0, 8)
M3 = (F(-1), F(5))                            # 直線 m：y＝−x＋5


def g_answers():
    x = sp.symbols("x")
    l = line2(A3, D3)
    B = (-M3[1] / M3[0], F(0))
    cx = sp.solve(sp.Eq(2 * x + 8, -x + 5), x)[0]
    C = (F(int(cx)), l[0] * int(cx) + l[1])
    S = abs(B[0] - A3[0]) * C[1] / 2
    M = ((A3[0] + B[0]) / 2, F(0))
    half = line2(C, M)
    tri = lambda P, Q, R: abs((Q[0] - P[0]) * (R[1] - P[1]) - (R[0] - P[0]) * (Q[1] - P[1])) / F(2)
    assert tri(A3, M, C) == tri(M, B, C) == S / 2
    bp = (S / 3) * 2 / C[1]                     # △BPC＝△ABC×1/3（高さは C の y 座標）
    Pp = (B[0] + bp, F(0))
    assert tri(B, Pp, C) == S / 3
    r = (l, B, C, S, M, half, Pp)
    assert r == ((2, 8), (5, 0), (-1, 6), 27, (F(1, 2), 0), (-4, 2), (8, 0)), r
    return dict(l=l, B=B, C=C, S=S, M=M, half=half, P=Pp)


def page_g(a=False):
    r = g_answers()
    b = lambda w, v: blank(w, v, a)
    story = (f"右の図で、直線 {T('\\ell')} は2点 A{pt_tex(A3)}、D{pt_tex(D3)} を通り、直線 {T('m')} の式は {T('y=-x+5')} である。"
             f"直線 {T('m')} と {X} 軸との交点をB、直線 {T('\\ell')} と {T('m')} の交点をCとする。"
             f"座標の1目もりを1cmとする。")
    svg = coord_svg((-6, 9), (-1.2, 10), 5.0,
                    [(F(2), F(8), "ℓ", RED, (0.8, 1.6, 0, "start")), (M3[0], M3[1], "m", BLUE, (-4.6, -1.6, 0, "end"))],
                    [("A", A3, -1.6, -1.6, "end"), ("B", r["B"], 1.2, -1.8, "start"), ("C", r["C"], -2, -1.2, "end"),
                     ("D", D3, 1.6, 1.4, "start")])
    qs = [
        (f"直線 {T('\\ell')} の式を求めなさい。", f"答　{b(50, T('y=2x+8'))}", 1,
         f"切片は D の {Y} 座標で8。傾き {T('\\dfrac{8-0}{0-(-4)}=2')}"),
        ("点Bの座標を求めなさい。", f"答　B{b(36, pt_tex((5, 0)))}", 0.9,
         f"{T('y=-x+5')} に {T('y=0')} を代入して {T('0=-x+5')}、{T('x=5')}"),
        ("点Cの座標を求めなさい。", f"答　C{b(36, pt_tex((-1, 6)))}", 1.1,
         f"{T('2x+8=-x+5')}　{T('3x=-3')}　{T('x=-1')}　{T('y=-(-1)+5=6')}"),
        ("△ABCの面積を求めなさい。", f"答　{b(26, '27')}cm²", 1,
         f"底辺AB＝{T('5-(-4)=9')}、高さは点Cの {Y} 座標で6。{T('\\dfrac12\\times9\\times6=27')}"),
        ("点Cを通り、△ABCの面積を2等分する直線の式を求めなさい。", f"答　{b(50, T('y=-4x+2'))}", 1.2,
         f"辺ABの真ん中の点M を通ればよい。{T('\\dfrac{-4+5}{2}=\\dfrac12')} より M{T('\\left(\\dfrac12,\\ 0\\right)')}<br>"
         f"傾き {T('\\dfrac{6-0}{-1-\\frac12}=6\\div\\left(-\\dfrac32\\right)=-4')}。{T('0=-4\\times\\dfrac12+b')}、{T('b=2')}"),
        (f"{X} 軸上で点Bより右に点Pをとる。△BPCの面積が△ABCの面積の {T('\\dfrac13')} になるとき、点Pの座標を求めなさい。",
         f"答　P{b(36, pt_tex((8, 0)))}", 1.1,
         f"△BPC＝{T('27\\times\\dfrac13=9')}。高さは点Cの {Y} 座標で6だから {T('\\dfrac12\\times\\mathrm{BP}\\times6=9')}、BP＝3<br>"
         f"Pの {X} 座標は {T('5+3=8')}"),
    ]
    return page(3, "グラフと面積", story, svg, qs, a)


def build(ans):
    return page_speed(ans) + page_dot(ans) + page_g(ans)


if __name__ == "__main__":
    speed_answers(); g_answers()
    print("確認OK：答え（SymPy・面積の計算）")
    write_pdfs([
        (doc(CSS, build(False)), f"{FILE}.pdf"),
        (doc(CSS, build(True)), f"{FILE}_ans.pdf"),
    ])
