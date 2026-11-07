"""中2 定期テスト対策（一次関数の利用）月曜用：1ページ＝大問1問（全幅・計算スペース広め）×4ページ＋こたえ4ページ（問題に赤で答えを書きこんだ形）

  cd tools && python3 c2_teiki_ichiji_riyou_mon.py

- 先生の希望（11/7）：左右に分けない。1ページに大問1問。計算するところを広く。
  グラフと面積の問題は、グラフにマス目をつけず、問題文に点の座標や直線の式など「解くための材料」を書く。
- ①速さ（行き帰りのある追いかけ・出会い）②動点（長方形・グラフをかく）③グラフと面積（2点から式）④グラフと面積（式から交点）
- 出力：pdf/c2_teiki_ichiji_riyou_mon.pdf（4ページ）と c2_teiki_ichiji_riyou_mon_ans.pdf（4ページ・問題と同じページに赤で答えと途中式）
"""
from fractions import Fraction as F

import sympy as sp

from texlib import doc, tex as T, write_pdfs
from c2_teiki_ichiji_riyou_thu import Plane, fr, lin, line2, UL, pt_tex, dot_pattern, rect_fig, dot_solutions, piece_of

FILE = "c2_teiki_ichiji_riyou_mon"
RED, BLUE = "#b4232c", "#1f5fbf"
X, Y = T("x"), T("y")
IT = 'font-family="KaTeX_Math" font-style="italic"'


def frac_t(a):
    return T(fr(a))


# ---------- 図（マス目なし） ----------
def arrow_axes(w, h, ox, oy, xt="x", yt="y", xu="", yu="", o_pos=(-1.4, 4.6, "end")):
    """原点 (ox, oy)（mm）を通る x 軸・y 軸（幅 w・高さ h の図）"""
    return (f'<line x1="0" y1="{oy}" x2="{w + 2}" y2="{oy}" stroke="#111" stroke-width=".45"/>'
            f'<polygon points="{w + 3.6},{oy} {w + 1.2},{oy - 1} {w + 1.2},{oy + 1}" fill="#111"/>'
            f'<line x1="{ox}" y1="{h}" x2="{ox}" y2="-2" stroke="#111" stroke-width=".45"/>'
            f'<polygon points="{ox},-3.6 {ox - 1},-1.2 {ox + 1},-1.2" fill="#111"/>'
            f'<text x="{w + 4.6}" y="{oy + 1.4}" font-size="4.4" {IT}>{xt}<tspan font-family="Noto Sans CJK JP" font-style="normal" font-size="3.6">{xu}</tspan></text>'
            f'<text x="{ox + 2}" y="-1.6" font-size="4.4" {IT}>{yt}<tspan font-family="Noto Sans CJK JP" font-style="normal" font-size="3.6">{yu}</tspan></text>'
            f'<text x="{ox + o_pos[0]}" y="{oy + o_pos[1]}" font-size="4" text-anchor="{o_pos[2]}">O</text>')


def speed_svg(ppl, xmax, ymax, xlabels, ylabels, guides, w=96, h=60):
    Xm = lambda v: v / xmax * w
    Ym = lambda v: h - v / ymax * h
    o = []
    for (gx, gy) in guides:                     # 目もりへの点線
        o.append(f'<polyline points="{Xm(gx):.2f},{h} {Xm(gx):.2f},{Ym(gy):.2f} 0,{Ym(gy):.2f}" fill="none" stroke="#777" stroke-width=".3" stroke-dasharray="1.2 1"/>')
    for v in xlabels:
        o.append(f'<text x="{Xm(v):.2f}" y="{h + 4.8}" font-size="3.9" text-anchor="middle">{v}</text>')
    for v in ylabels:
        o.append(f'<text x="-1.6" y="{Ym(v) + 1.4:.2f}" font-size="3.9" text-anchor="end">{v}</text>')
    for name, col, pts, (lx, ly, dx, dy, an) in ppl:
        o.append(f'<polyline points="{" ".join(f"{Xm(a):.2f},{Ym(b):.2f}" for a, b in pts)}" fill="none" stroke="{col}" stroke-width=".7" stroke-linejoin="round"/>')
        o.append(f'<text x="{Xm(lx) + dx:.2f}" y="{Ym(ly) + dy:.2f}" font-size="4.4" font-weight="700" text-anchor="{an}" fill="{col}">{name}</text>')
    o.append(arrow_axes(w, h, 0, h, xu="（分）", yu="（m）"))
    ml, mt, mr, mb = 12, 7, 16, 8
    W, H = w + ml + mr, h + mt + mb
    return f'<svg class=fig width="{W}mm" height="{H}mm" viewBox="{-ml} {-mt} {W} {H}">{"".join(o)}</svg>'


def coord_svg(xr, yr, s, lines, points, o_pos=(-1.4, 4.6, "end")):
    """マス目なしの座標平面。lines=[(a,b,名前,色,(ラベルのx, dx, dy, anchor))]、points=[(名前,(x,y),dx,dy,anchor)]"""
    (xl, xh), (yl, yh) = xr, yr
    w, h = (xh - xl) * s, (yh - yl) * s
    Xm = lambda v: (float(v) - xl) * s
    Ym = lambda v: (yh - float(v)) * s
    o = []
    for a, b, nm, col, (lx, dx, dy, an) in lines:
        lo, hi = xl, xh
        if a != 0:
            u, v = (yl - b) / a, (yh - b) / a
            lo, hi = max(lo, min(u, v)), min(hi, max(u, v))
        o.append(f'<line x1="{Xm(lo):.2f}" y1="{Ym(a * F(lo) + b):.2f}" x2="{Xm(hi):.2f}" y2="{Ym(a * F(hi) + b):.2f}" stroke="{col}" stroke-width=".65"/>')
        o.append(f'<text x="{Xm(lx) + dx:.2f}" y="{Ym(a * F(lx) + b) + dy:.2f}" font-size="5" font-weight="700" text-anchor="{an}" fill="{col}" {IT}>{nm}</text>')
    o.append(arrow_axes(w, h, Xm(0), Ym(0), o_pos=o_pos))
    for nm, (px, py), dx, dy, an in points:
        o.append(f'<circle cx="{Xm(px):.2f}" cy="{Ym(py):.2f}" r=".9" fill="#111"/>')
        o.append(f'<text x="{Xm(px) + dx:.2f}" y="{Ym(py) + dy:.2f}" font-size="4.6" text-anchor="{an}">{nm}</text>')
    ml, mt, mr, mb = 6, 7, 10, 7
    W, H = w + ml + mr, h + mt + mb
    return f'<svg class=fig width="{W:.1f}mm" height="{H:.1f}mm" viewBox="{-ml} {-mt} {W:.1f} {H:.1f}">{"".join(o)}</svg>'




def blank(w, val, ans):
    """答えのらん。こたえのプリントでは赤で書きこむ"""
    if ans:
        return f"<span class='ul fill' style='width:{w}mm'>{val}</span>"
    return UL(w)


# ---------- ① 速さ ----------
ANE = [(0, 0), (30, 1800)]
IMO = [(10, 0), (20, 1800), (22, 1800), (32, 0)]


def speed_answers():
    x = sp.symbols("x")
    v_ane = F(1800, 30)
    v_imo = F(1800, 20 - 10)
    go = sp.expand(v_imo * (x - 10))                 # 行き
    back = sp.expand(1800 - v_imo * (x - 22))        # 帰り
    t1 = sp.solve(sp.Eq(v_ane * x, go), x)[0]
    t2 = sp.solve(sp.Eq(v_ane * x, back), x)[0]
    r = dict(v_ane=v_ane, v_imo=v_imo, go=go, back=back, t1=t1, y1=v_ane * t1, t2=t2, y2=v_ane * t2, home=22 + 1800 / v_imo)
    assert (r["v_ane"], r["v_imo"], str(go), str(back), t1, r["y1"], t2, r["y2"], r["home"]) == \
        (60, 180, "180*x - 1800", "5760 - 180*x", 15, 900, 24, 1440, 32), r
    return r


def page_speed(a=False):
    speed_answers()
    b = lambda w, v: blank(w, v, a)
    story = (f"姉は、家を出発して、家から1800m離れた図書館まで歩いて向かった。姉が出発してから10分後に、妹が家を出発し、"
             f"同じ道を自転車で図書館に向かった。妹は図書館で2分間過ごしたあと、行きと同じ速さで同じ道を家に帰った。<br>"
             f"右のグラフは、姉が家を出発してから {X} 分後の家からの道のりを {Y} m として、2人のようすを表したものである。"
             f"2人とも、止まっているとき以外は一定の速さで進むものとする。")
    ppl = [("姉", RED, ANE, (30, 1800, 1.6, -1.6, "start")), ("妹", BLUE, IMO, (32, 0, 1.6, -4.5, "start"))]
    P = Plane((0, 34), (0, 2000), 104 / 34, 72 / 2000, (1, 5), (100, 200), xu="（分）", yu="（m）", mr=17, ml=11)
    for name, col, pts, (lx, ly, dx, dy, an) in ppl:
        P.poly(pts, col, .75)
        P.text(lx, ly, name, dx, dy, an, 4.4, f'style="fill:{col};font-weight:700"')
    svg = P.svg()
    qs = [
        ("姉の歩く速さは分速何mですか。", f"答　分速{b(22, '60')}m", 1,
         f"30分で1800m進むから　{T('1800\\div30=60')}"),
        (f"妹が家を出発してから図書館に着くまでの {X} と {Y} の関係を式で表しなさい。また、{X} の変域も答えなさい。",
         f"答　式{b(50, T('y=180x-1800'))}　変域{b(36, T('10\\leqq x\\leqq 20'))}", 1.25,
         f"妹の速さは {T('1800\\div(20-10)=180')}（分速180m）。{T('y=180x+b')} に {T('(10,\\ 0)')} を代入して {T('0=1800+b')}、{T('b=-1800')}"),
        ("妹が姉に追いつくのは、姉が家を出発してから何分後ですか。また、それは家から何mの地点ですか。",
         f"答　{b(18, '15')}分後、家から{b(20, '900')}m", 1.25,
         f"姉の式は {T('y=60x')}。{T('60x=180x-1800')}　{T('-120x=-1800')}　{T('x=15')}<br>"
         f"{T('y=60\\times15=900')}"),
        (f"妹が図書館を出発してから家に着くまでの {X} と {Y} の関係を式で表しなさい。また、{X} の変域も答えなさい。",
         f"答　式{b(50, T('y=-180x+5760'))}　変域{b(36, T('22\\leqq x\\leqq 32'))}", 1.25,
         f"出発は {T('x=20+2=22')}、家に着くのは {T('x=22+1800\\div180=32')}。傾きは {T('-180')}<br>"
         f"{T('y=-180x+b')} に {T('(22,\\ 1800)')} を代入して {T('1800=-3960+b')}、{T('b=5760')}"),
        ("家に帰る妹と、図書館に向かう姉が出会うのは、姉が家を出発してから何分後ですか。また、それは家から何mの地点ですか。",
         f"答　{b(18, '24')}分後、家から{b(20, '1440')}m", 1.25,
         f"{T('60x=-180x+5760')}　{T('240x=5760')}　{T('x=24')}<br>{T('y=60\\times24=1440')}"),
    ]
    return page(1, "速さ（ダイヤグラム）", story, svg, qs, a)


# ---------- ② 動点 ----------
DOTM = dot_pattern("ABCD", "APD", 10, 6, 1, 4, 15, (0, 2), ["", "", ""])


def dot_grid(answer=False):
    d = DOTM
    P = Plane((0, 22), (0, 35), 118 / 22, 52 / 35, (1, 2), (5, 5), xu="（秒）", yu="（cm²）", mr=17, ml=10)
    if answer:
        P.poly(list(zip(d["ts"], d["ys"])), RED, .8)
    return P.svg()


def page_dot(a=False):
    d = DOTM
    assert [(lo, hi, int(p), int(q)) for lo, hi, p, q in d["pieces"]] == [(0, 6, 5, 0), (6, 16, 0, 30), (16, 22, -5, 110)]
    assert piece_of(d, 4) == 20 and [int(s[0]) for s in dot_solutions(d)] == [3, 19]
    b = lambda w, v: blank(w, v, a)
    story = (f"右の図のような、AB＝6cm、BC＝10cm の長方形ABCDがある。点Pは、頂点Aを出発して、辺AB、BC、CD上を、"
             f"毎秒1cmの速さで頂点Dまで動く。点PがAを出発してから {X} 秒後の △APD の面積を {Y} cm² とする。"
             f"ただし、点PがA、Dにあるときは {T('y=0')} とする。")
    qs = [
        (f"{T('x=4')} のときの {Y} の値を求めなさい。", f"答　{Y}＝{b(22, '20')}", 1,
         f"4秒後、点Pは辺AB上で AP＝4cm。{T('y=\\dfrac12\\times10\\times4=20')}"),
        (f"点Pが辺AB上を動くとき（{T('0\\leqq x\\leqq 6')}）、{Y} を {X} の式で表しなさい。", f"答　{b(50, T('y=5x'))}", 1,
         f"AP＝{X} cm、底辺AD＝10cm だから　{T('y=\\dfrac12\\times10\\times x=5x')}"),
        (f"点Pが辺CD上を動くとき（{T('16\\leqq x\\leqq 22')}）、{Y} を {X} の式で表しなさい。", f"答　{b(50, T('y=-5x+110'))}", 1.15,
         f"Pが C に着くのは {T('6+10=16')} 秒後。そこから DP＝{T('6-(x-16)=-x+22')} (cm)<br>"
         f"{T('y=\\dfrac12\\times10\\times(-x+22)=-5x+110')}"),
        ("△APDの面積が15cm² になるのは、点PがAを出発してから何秒後ですか。すべて答えなさい。",
         f"答　{b(20, '3')}秒後、{b(20, '19')}秒後", 1.15,
         f"辺AB上：{T('5x=15')}　{T('x=3')}　辺BC上：{T('y=30')} で一定なので15にならない<br>"
         f"辺CD上：{T('-5x+110=15')}　{T('x=19')}"),
        (f"{X} と {Y} の関係を表すグラフを、下の図にかきなさい（{T('0\\leqq x\\leqq 22')}）。", "", 0,
         f"点 {T('(0,\\ 0)')}、{T('(6,\\ 30)')}、{T('(16,\\ 30)')}、{T('(22,\\ 0)')} を順に線分で結ぶ",
         f"<div class=gw>{dot_grid(a)}</div>"),
    ]
    return page(2, "動点", story, rect_fig(d, s=4.6), qs, a)


# ---------- ③ グラフと面積（2点から式） ----------
G3 = dict(A=(-4, 0), B=(6, 0), D=(0, 4), E=(0, 9))


def g3_answers():
    A, B, D, E = G3["A"], G3["B"], G3["D"], G3["E"]
    l, m = line2(A, D), line2(B, E)
    x = sp.symbols("x")
    cx = sp.solve(sp.Eq(sp.Rational(l[0].numerator, l[0].denominator) * x + int(l[1]),
                        sp.Rational(m[0].numerator, m[0].denominator) * x + int(m[1])), x)[0]
    C = (F(int(cx)), l[0] * int(cx) + l[1])
    S = F(abs(B[0] - A[0]) * C[1], 2)
    tri = lambda P, Q, R: abs((Q[0] - P[0]) * (R[1] - P[1]) - (R[0] - P[0]) * (Q[1] - P[1])) / F(2)
    assert tri(A, B, C) == S
    M = (F(A[0] + B[0], 2), F(0))
    half = line2(C, M)
    assert tri(A, M, C) == tri(M, B, C) == S / 2
    p = 2 * S / abs(B[0] - A[0])                     # △PAB＝△ABC → 高さが同じ
    r = dict(l=l, m=m, C=C, S=S, M=M, half=half, P=(0, p))
    assert (l, m, C, S, half, p) == ((1, 4), (F(-3, 2), 9), (2, 6), 30, (6, -6), 6), r
    return r


def page_g3(a=False):
    A, B, D, E = G3["A"], G3["B"], G3["D"], G3["E"]
    r = g3_answers()
    C = r["C"]
    b = lambda w, v: blank(w, v, a)
    story = (f"右の図で、直線 {T('\\ell')} は2点 A{pt_tex(A)}、D{pt_tex(D)} を通り、"
             f"直線 {T('m')} は2点 B{pt_tex(B)}、E{pt_tex(E)} を通る。直線 {T('\\ell')} と {T('m')} の交点をCとする。"
             f"座標の1目もりを1cmとする。")
    svg = coord_svg((-6, 8), (-1.2, 10), 5.4,
                    [(F(1), F(4), "ℓ", RED, (5.4, 1.6, 1.6, "start")), (F(-3, 2), F(9), "m", BLUE, (6.6, 1.6, 1.6, "start"))],
                    [("A", A, -1.4, -1.8, "end"), ("B", B, -1.2, 5, "end"), ("C", C, 2.2, 2.0, "start"),
                     ("D", D, -1.6, -1, "end"), ("E", E, -1.6, 1.2, "end")])
    qs = [
        (f"直線 {T('\\ell')} の式を求めなさい。", f"答　{b(50, T('y=x+4'))}", 1,
         f"切片は D の {Y} 座標で4。傾き {T('\\dfrac{4-0}{0-(-4)}=1')}"),
        (f"直線 {T('m')} の式を求めなさい。", f"答　{b(50, T('y=-\\dfrac32x+9'))}", 1,
         f"切片は E の {Y} 座標で9。傾き {T('\\dfrac{9-0}{0-6}=-\\dfrac32')}"),
        ("点Cの座標を求めなさい。", f"答　C{b(36, pt_tex((2, 6)))}", 1.15,
         f"{T('x+4=-\\dfrac32x+9')}　両辺を2倍して {T('2x+8=-3x+18')}　{T('5x=10')}　{T('x=2')}<br>"
         f"{T('y=2+4=6')}"),
        ("△ABCの面積を求めなさい。", f"答　{b(26, '30')}cm²", 1,
         f"底辺AB＝{T('6-(-4)=10')}、高さは点Cの {Y} 座標で6。{T('\\dfrac12\\times10\\times6=30')}"),
        ("点Cを通り、△ABCの面積を2等分する直線の式を求めなさい。", f"答　{b(50, T('y=6x-6'))}", 1.15,
         f"辺ABの真ん中の点M{pt_tex((1, 0))} を通ればよい（{T('\\dfrac{-4+6}{2}=1')}）。<br>"
         f"C{pt_tex((2, 6))}、M を通るから 傾き {T('\\dfrac{6-0}{2-1}=6')}。{T('0=6\\times1+b')}、{T('b=-6')}"),
        (f"{Y} 軸上の {Y} 座標が正の部分に点Pをとる。△PABの面積が△ABCの面積と等しくなるとき、点Pの座標を求めなさい。",
         f"答　P{b(36, pt_tex((0, 6)))}", 1,
         f"底辺ABが同じだから、高さ（点Pの {Y} 座標）が点Cと同じ6になればよい"),
    ]
    return page(3, "グラフと面積①", story, svg, qs, a)


# ---------- ④ グラフと面積（式から交点） ----------
L4, M4 = (F(-2), F(12)), (F(1), F(0))


def g4_answers():
    x = sp.symbols("x")
    A = (-L4[1] / L4[0], 0)
    B = (0, L4[1])
    cx = sp.solve(sp.Eq(-2 * x + 12, x), x)[0]
    C = (F(int(cx)), F(int(cx)))
    S_oac = F(A[0] * C[1], 2)
    S_obc = F(B[1] * C[0], 2)
    Mab = (A[0] / 2, B[1] / 2)
    half = line2((0, 0), Mab)
    yp = C[1] / 2                                    # △OAP は △OAC と底辺OAが同じ → 高さが半分
    xp = (yp - L4[1]) / L4[0]
    r = dict(A=A, B=B, C=C, S_oac=S_oac, S_obc=S_obc, M=Mab, half=half, P=(xp, yp))
    assert (A, B, C, S_oac, S_obc, half, (xp, yp)) == ((6, 0), (0, 12), (4, 4), 12, 24, (2, 0), (5, 2)), r
    assert C[0] <= xp <= A[0] and S_oac + S_obc == F(6 * 12, 2)
    return r


def page_g4(a=False):
    r = g4_answers()
    b = lambda w, v: blank(w, v, a)
    story = (f"右の図で、直線 {T('\\ell')} の式は {T('y=-2x+12')}、直線 {T('m')} の式は {T('y=x')} である。"
             f"直線 {T('\\ell')} と {X} 軸、{Y} 軸との交点をそれぞれA、Bとし、直線 {T('\\ell')} と {T('m')} の交点をCとする。"
             f"Oは原点で、座標の1目もりを1cmとする。")
    svg = coord_svg((-1.5, 9), (-1.2, 13.5), 4.6,
                    [(L4[0], L4[1], "ℓ", RED, (6.9, 1.4, 1.4, "start")), (M4[0], M4[1], "m", BLUE, (8.8, -1.6, 0, "end"))],
                    [("A", r["A"], 1.4, -1.8, "start"), ("B", r["B"], -1.6, 1.4, "end"), ("C", r["C"], 2.4, 1.8, "start")],
                    o_pos=(1.2, 4.6, "start"))
    qs = [
        ("点A、点Bの座標をそれぞれ求めなさい。", f"答　A{b(30, pt_tex((6, 0)))}　B{b(30, pt_tex((0, 12)))}", 1,
         f"A：{T('y=0')} を代入して {T('0=-2x+12')}、{T('x=6')}　B：{T('x=0')} を代入して {T('y=12')}（切片）"),
        ("点Cの座標を求めなさい。", f"答　C{b(36, pt_tex((4, 4)))}", 1,
         f"{T('-2x+12=x')}　{T('-3x=-12')}　{T('x=4')}　{T('y=4')}"),
        ("△OACの面積を求めなさい。", f"答　{b(26, '12')}cm²", 1,
         f"底辺OA＝6、高さは点Cの {Y} 座標で4。{T('\\dfrac12\\times6\\times4=12')}"),
        ("△OBCの面積を求めなさい。", f"答　{b(26, '24')}cm²", 1,
         f"底辺OB＝12、高さは点Cの {X} 座標で4。{T('\\dfrac12\\times12\\times4=24')}"),
        ("点Oを通り、△OABの面積を2等分する直線の式を求めなさい。", f"答　{b(50, T('y=2x'))}", 1,
         f"辺ABの真ん中の点M{pt_tex((3, 6))} を通ればよい（{T('\\dfrac{6+0}{2}=3')}、{T('\\dfrac{0+12}{2}=6')}）。"
         f"原点とMを通るから 傾き {T('6\\div3=2')}"),
        ("線分AC上に点Pをとる。△OAPの面積が△OACの面積の半分になるとき、点Pの座標を求めなさい。", f"答　P{b(36, pt_tex((5, 2)))}", 1,
         f"底辺OAが同じだから、高さ（点Pの {Y} 座標）が点Cの半分の2になればよい。{T('2=-2x+12')}　{T('x=5')}"),
    ]
    return page(4, "グラフと面積②", story, svg, qs, a)


# ---------- ページの形 ----------
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; font-size: 10.5pt; }
.page { width: 210mm; height: 297mm; padding: 10mm 13mm 10mm; page-break-after: always;
        display: flex; flex-direction: column; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.katex { font-size: 1.08em; }
.head { display: flex; align-items: baseline; white-space: nowrap; border-bottom: 1pt solid #111; padding-bottom: 1.8mm; }
.head b { font-size: 13pt; }
.head .sub { font-size: 9.5pt; margin-left: 2mm; }
.head .cl { margin-left: auto; font-size: 9.5pt; }
.head .u { display: inline-block; border-bottom: .7pt solid #111; }
.head .kotae { margin-left: auto; font-weight: 700; color: #b4232c; font-size: 12pt; }
.big { margin-top: 3mm; font-weight: 700; font-size: 11pt; display: flex; align-items: center; gap: 2mm; }
.big .box { display: inline-flex; width: 6mm; height: 6mm; border: .9pt solid #111; align-items: center; justify-content: center; }
.big .pill { font-size: 8pt; font-weight: 400; border: .7pt solid #111; border-radius: 3mm; padding: .2mm 2mm; margin-left: 2mm; }
.top { display: flex; gap: 4mm; align-items: flex-start; margin-top: 2mm; }
.story { flex: 1; line-height: 1.75; }
.fig { flex: none; }
.fig text, .gr text { font-family: 'Noto Sans CJK JP'; }
.qs { flex: 1; min-height: 0; display: flex; flex-direction: column; margin-top: 2mm; }
.sqi { display: flex; flex-direction: column; border-top: .4pt solid #bbb; padding: 1.6mm 0 1.4mm; min-height: auto; }
.qt { display: flex; line-height: 1.65; }
.qt .no { flex: none; width: 8mm; font-size: 9.5pt; }
.work { flex: 1; margin: 1mm 0 0 8mm; line-height: 1.85; }
.ans { align-self: flex-end; white-space: nowrap; }
.ul { display: inline-block; border-bottom: .8pt solid #111; height: 5.5mm; vertical-align: baseline; }
.ul.fill { color: #c0141e; font-weight: 700; text-align: center; height: auto; line-height: 1.3; }
.ansp .work { color: #c0141e; }
.gw { display: flex; justify-content: center; }
"""


def head(n, title, ans):
    right = ("<span class=kotae>こたえ</span>" if ans else
             "<span class=cl>（　）組（　）番　名前 <span class=u style='width:34mm'></span></span>")
    return (f"<div class=head><b>中2数学 定期テスト対策</b><span class=sub>一次関数の利用 {'①②③④'[n - 1]} {title}</span>"
            f"{right}</div>")


def page(n, title, story, svg, qs, ans=False):
    rows = []
    for k, q in enumerate(qs, 1):
        text, a_html, grow, work = q[:4]
        extra = q[4] if len(q) > 4 else ""
        st = f"flex:{grow} 1 0" if grow else "flex:none"
        wk = f"<div class=work>{work if ans else ''}</div>" if grow else (f"<div class=work>{work}</div>" if ans else "")
        rows.append(f"<div class=sqi style='{st}'><div class=qt><span class=no>({k})</span><div>{text}</div></div>{wk}{extra}"
                    f"{f'<div class=ans>{a_html}</div>' if a_html else ''}</div>")
    return (f"<div class='page{' ansp' if ans else ''}'>{head(n, title, ans)}"
            f"<div class=big><span class=box>{n}</span>次の問いに答えなさい。<span class=pill>式や計算も書くこと</span></div>"
            f"<div class=top><div class=story>{story}</div>{svg}</div>"
            f"<div class=qs>{''.join(rows)}</div></div>")


def build(ans):
    return page_speed(ans) + page_dot(ans) + page_g3(ans) + page_g4(ans)


if __name__ == "__main__":
    speed_answers(); g3_answers(); g4_answers()
    print("確認OK：答え（SymPy・面積の計算）")
    write_pdfs([
        (doc(CSS, build(False)), f"{FILE}.pdf"),
        (doc(CSS, build(True)), f"{FILE}_ans.pdf"),
    ])
