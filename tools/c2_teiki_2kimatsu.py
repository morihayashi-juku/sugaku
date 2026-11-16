"""中2 定期テスト対策（2学期期末）11/16（月）用：4ページ（1ページ＝1テーマ・全幅）＋こたえ4ページ（赤で書きこみ）

  cd tools && python3 c2_teiki_2kimatsu.py

テスト範囲：一次関数の利用（速さ・動点・グラフと面積）、図形の用語・性質、角度（対頂角・錯角・同位角・内角・外角）、証明の進め方
  ① 一次関数の利用   ② 図形の用語・性質   ③ 角度を求める（10問）   ④ 証明の進め方
- 図は実際の角度・長さで描き、図から角度を測りなおして問題の数字と合っているか確かめる（check_angles）。
- 出力：pdf/c2_teiki_2kimatsu.pdf と c2_teiki_2kimatsu_ans.pdf
"""
import math
from fractions import Fraction as F

import sympy as sp

from texlib import doc, tex as T, write_pdfs
from c2_teiki_ichiji_riyou_thu import Plane, dot_pattern, rect_fig, dot_solutions, piece_of
from c2_teiki_ichiji_riyou_mon import coord_svg, RED, BLUE

FILE = "c2_teiki_2kimatsu"
X, Y = T("x"), T("y")
ANS = False                 # こたえを作るときだけ True
IT = 'font-family="KaTeX_Math" font-style="italic"'


def b(w, v):
    """答えのらん（こたえでは赤で書きこむ）"""
    if ANS:
        return f"<span class='ul fill' style='width:{w}mm'>{v}</span>"
    return f"<span class=ul style='width:{w}mm'></span>"


def q(no, text, ans="", work="", grow=1, extra="", inline=False):
    if inline:      # 答えのらんを問題文と同じ行に（入らなければ次の行の右）
        return (f"<div class=sqi style='flex:{grow} 1 0'><div class=qt><span class=no>({no})</span><div>{text}</div>"
                f"<span class='ans in'>{ans}</span></div><div class=work>{work if ANS else ''}</div>{extra}</div>")
    return (f"<div class=sqi style='flex:{grow} 1 0'><div class=qt><span class=no>({no})</span><div>{text}</div></div>"
            f"<div class=work>{work if ANS else ''}</div>{extra}{f'<div class=ans>{ans}</div>' if ans else ''}</div>")


def head(n, title):
    right = ("<span class=kotae>こたえ</span>" if ANS else
             "<span class=cl>（　）組（　）番　名前 <span class=u style='width:34mm'></span></span>")
    return (f"<div class=head><b>中2数学 定期テスト対策</b><span class=sub>2学期期末 {'①②③④'[n - 1]} {title}</span>{right}</div>")


def big(n, text, pill=""):
    return (f"<div class=big><span class=box>{n}</span>{text}"
            f"{f'<span class=pill>{pill}</span>' if pill else ''}</div>")


# ---------- 図をかく道具（座標は mm・y は上向き） ----------
def u(d):
    return (math.cos(math.radians(d)), math.sin(math.radians(d)))


def add(p, v, t=1):
    return (p[0] + v[0] * t, p[1] + v[1] * t)


def inter(p, d1, q_, d2):
    (a, b_), (c, d) = u(d1), u(d2)
    det = a * (-d) - (-c) * b_
    t = ((q_[0] - p[0]) * (-d) - (-c) * (q_[1] - p[1])) / det
    return add(p, (a, b_), t)


def ang(V, P, Q):
    a1 = math.atan2(P[1] - V[1], P[0] - V[0])
    a2 = math.atan2(Q[1] - V[1], Q[0] - V[0])
    d = abs(math.degrees(a2 - a1)) % 360
    return min(d, 360 - d)


class Fig:
    def __init__(s, w, h):
        s.w, s.h, s.o, s.checks = w, h, [], []

    def m(s, p):
        return (p[0], s.h - p[1])

    def line(s, p, q_, w=.5, col="#111"):
        a, c = s.m(p), s.m(q_)
        s.o.append(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{c[0]:.2f}" y2="{c[1]:.2f}" stroke="{col}" '
                   f'stroke-width="{w}" stroke-linecap="round"/>')

    def poly(s, pts):
        for i in range(len(pts)):
            s.line(pts[i], pts[(i + 1) % len(pts)])

    def text(s, p, t, dx=0, dy=0, anchor="middle", size=3.9, italic=False, col="#111"):
        a = s.m(p)
        st = IT if italic else ""
        s.o.append(f'<text x="{a[0] + dx:.2f}" y="{a[1] + dy:.2f}" font-size="{size}" text-anchor="{anchor}" fill="{col}" {st}>{t}</text>')

    def dot(s, p):
        a = s.m(p)
        s.o.append(f'<circle cx="{a[0]:.2f}" cy="{a[1]:.2f}" r=".7" fill="#111"/>')

    def angle(s, V, P, Q, label, r=5.0, lr=3.6, value=None, italic=False):
        """V で VP と VQ がつくる角（小さいほう）に弧と文字。value があれば図から測って確かめる"""
        a1 = math.atan2(P[1] - V[1], P[0] - V[0])
        a2 = math.atan2(Q[1] - V[1], Q[0] - V[0])
        d = (a2 - a1) % (2 * math.pi)
        if d > math.pi:
            a1, d = a2, 2 * math.pi - d
        p1 = s.m(add(V, (math.cos(a1), math.sin(a1)), r))
        p2 = s.m(add(V, (math.cos(a1 + d), math.sin(a1 + d)), r))
        s.o.append(f'<path d="M{p1[0]:.2f},{p1[1]:.2f} A{r},{r} 0 0 0 {p2[0]:.2f},{p2[1]:.2f}" fill="none" stroke="#111" stroke-width=".35"/>')
        mid = a1 + d / 2
        lp = add(V, (math.cos(mid), math.sin(mid)), r + lr)
        s.text(lp, label, 0, 1.3, "middle", 3.6 if not italic else 4.4, italic)
        if value is not None:
            s.checks.append((round(math.degrees(d), 3), value, label))

    def par(s, p, d=0):
        """平行の印（＞）"""
        for k in (-1, 1):
            tip = add(p, u(d), 1.2 + k * 0)
            s.line(add(tip, u(d + 150), 2.2), tip, .4)
            s.line(add(tip, u(d - 150), 2.2), tip, .4)
            p = add(p, u(d), 1.6)

    def svg(s):
        for got, want, lab in s.checks:
            assert abs(got - want) < 1e-6, (lab, got, want)
        return (f'<svg class=fig width="{s.w}mm" height="{s.h}mm" viewBox="0 0 {s.w} {s.h}">'
                f'{"".join(s.o)}</svg>')


# ---------- ① 一次関数の利用 ----------
def page1():
    x = sp.symbols("x")
    # 速さ
    A_ = [(0, 0), (20, 1600)]
    AN = [(6, 1600), (14, 0)]
    va = F(1600, 20)
    an = sp.expand(1600 - F(1600, 8) * (x - 6))
    t = sp.solve(sp.Eq(va * x, an), x)[0]
    assert (va, str(an), t, va * t) == (80, "2800 - 200*x", 10, 800)
    P = Plane((0, 20), (0, 1600), 52 / 20, 38 / 1600, (1, 5), (100, 200), xu="（分）", yu="（m）", mr=18, ml=11)
    P.poly(A_, RED, .75)
    P.text(20, 1600, "Aさん", 1.2, 1.2, "start", 3.9, f'style="fill:{RED};font-weight:700"')
    P.poly(AN, BLUE, .75)
    P.text(6, 1600, "兄", -2.6, 4.2, "end", 4.2, f'style="fill:{BLUE};font-weight:700"')
    s1 = (f"Aさんは、家から1600m離れた図書館へ歩いた。兄は、その6分後に図書館を出て、同じ道を自転車で家に向かった。"
          f"グラフは、Aさんが出発してから {X} 分後の家からの道のりを {Y} m として、2人のようすを表したものである。")
    q1 = (q(1, "Aさんの速さは分速何mですか。", f"答　分速{b(18, '80')}m", f"{T('1600\\div20=80')}", inline=True)
          + q(2, f"兄が図書館を出発してから家に着くまでの {X} と {Y} の関係を式で表しなさい。{X} の変域も答えなさい。",
              f"答　式{b(34, T('y=-200x+2800'))}　変域{b(24, T('6\\leqq x\\leqq 14'))}",
              f"傾き {T('-1600\\div8=-200')}、{T('0=-200\\times14+b')}、{T('b=2800')}", 1.3)
          + q(3, "2人が出会うのは、Aさんが家を出発してから何分後ですか。また、家から何mの地点ですか。",
              f"答　{b(14, '10')}分後、家から{b(16, '800')}m",
              f"{T('80x=-200x+2800')}、{T('x=10')}、{T('y=800')}", 1.2))
    blk1 = (f"<div class=blk style='flex:1.26 1 0'>{big(1, '速さ')}<div class=row><div class=lft><div class=story>{s1}</div>"
            f"<div class=qs>{q1}</div></div><div class=rgt>{P.svg()}</div></div></div>")
    # 動点
    d = dot_pattern("BCD", "APD", 8, 6, 1, 4, 12, (0, 1), ["", ""])
    assert [(lo, hi, int(p_), int(q_)) for lo, hi, p_, q_ in d["pieces"]] == [(0, 8, 0, 24), (8, 14, -4, 56)]
    assert [int(s_[0]) for s_ in dot_solutions(d)] == [11]
    s2 = (f"AB＝6cm、BC＝8cm の長方形ABCDがある。点Pは、頂点Bを出発して、辺BC、CD上を毎秒1cmの速さで頂点Dまで動く。"
          f"点PがBを出発してから {X} 秒後の △APD の面積を {Y} cm² とする。")
    q2 = (q(1, "点Pが辺BC上にあるとき、△APDの面積は何cm²ですか。", f"答　{b(18, '24')}cm²",
            f"{T('\\frac12\\times8\\times6=24')}（BC上では一定）", inline=True)
          + q(2, f"{T('8\\leqq x\\leqq 14')} のとき、{Y} を {X} の式で表しなさい。", f"答　{b(40, T('y=-4x+56'))}",
              f"DP＝{T('14-x')}、{T('y=\\frac12\\times8\\times(14-x)=-4x+56')}", 1.1)
          + q(3, "△APDの面積が12cm² になるのは、点PがBを出発してから何秒後ですか。", f"答　{b(18, '11')}秒後",
              f"{T('-4x+56=12')}、{T('x=11')}", inline=True))
    blk2 = (f"<div class=blk style='flex:1.08 1 0'>{big(2, '動点')}<div class=row><div class=lft><div class=story>{s2}</div>"
            f"<div class=qs>{q2}</div></div><div class=rgt>{rect_fig(d, s=4.4)}</div></div></div>")
    # グラフと面積
    l, m = (F(1), F(3)), (F(-2), F(12))
    A, B = (-l[1] / l[0], 0), (-m[1] / m[0], 0)
    cx = sp.solve(sp.Eq(x + 3, -2 * x + 12), x)[0]
    C = (int(cx), int(cx) + 3)
    S = F(abs(B[0] - A[0]) * C[1], 2)
    Mx = (A[0] + B[0]) / 2
    slope = F(C[1], C[0] - Mx)
    assert (A, B, C, S, Mx, slope, -slope * Mx) == ((-3, 0), (6, 0), (3, 6), 27, F(3, 2), 4, -6)
    s3 = (f"直線 {T('\\ell')}：{T('y=x+3')} と直線 {T('m')}：{T('y=-2x+12')} がある。{T('\\ell')}、{T('m')} と {X} 軸との交点を"
          f"それぞれA、Bとし、{T('\\ell')} と {T('m')} の交点をCとする。座標の1目もりを1cmとする。")
    svg3 = coord_svg((-5, 8), (-1.2, 10), 4.4,
                     [(l[0], l[1], "ℓ", RED, (6.6, 1.2, 0, "start")), (m[0], m[1], "m", BLUE, (1.2, 1.6, 0, "start"))],
                     [("A", A, -1.4, -1.8, "end"), ("B", B, 1.4, -1.8, "start"), ("C", C, 2.2, 1.6, "start")])
    q3 = (q(1, "点Cの座標を求めなさい。", f"答　C{b(28, T('(3,\\ 6)'))}",
            f"{T('x+3=-2x+12')}、{T('x=3')}、{T('y=6')}", inline=True)
          + q(2, "△ABCの面積を求めなさい。", f"答　{b(18, '27')}cm²",
              f"AB＝{T('6-(-3)=9')}、{T('\\frac12\\times9\\times6=27')}", inline=True)
          + q(3, "点Cを通り、△ABCの面積を2等分する直線の式を求めなさい。", f"答　{b(40, T('y=4x-6'))}",
              f"ABの中点 M{T('(1.5,\\ 0)')} を通る。傾き {T('6\\div1.5=4')}、{T('b=-6')}", 1.2))
    blk3 = (f"<div class=blk>{big(3, 'グラフと面積')}<div class=row><div class=lft><div class=story>{s3}</div>"
            f"<div class=qs>{q3}</div></div><div class=rgt>{svg3}</div></div></div>")
    return f"<div class=page>{head(1, '一次関数の利用')}{blk1}{blk2}{blk3}</div>"


# ---------- ② 図形の用語・性質 ----------
def lines_fig():
    Fg = Fig(78, 46)
    P, Q = (30, 32), None
    Q = inter(P, 245, (0, 10), 0)
    Fg.line((3, 32), (64, 32))
    Fg.line((3, 10), (64, 10))
    Fg.line(add(P, u(65), 10), add(Q, u(245), 9))
    Fg.text((64, 32), "ℓ", 1.6, 1.4, "start", 4.4, True)
    Fg.text((64, 10), "m", 1.6, 1.4, "start", 4.4, True)
    Fg.text(add(P, u(65), 10), "n", 1.6, 2, "start", 4.4, True)
    for V, lets in ((P, "abcd"), (Q, "efgh")):
        for k, d in enumerate((32, 122, 212, 302)):
            mid = d if k % 2 == 0 else d
            Fg.text(add(V, u([32.5, 122.5, 212.5, 302.5][k]), 5.2), lets[k], 0, 1.4, "middle", 4.2, True)
    return Fg.svg()


def page2():
    a = lambda t: T(f"\\angle {t}")
    blk1 = (f"<div class=blk style='flex:0.9 1 0'>{big(1, '右の図のように、2直線 ' + T('\\ell') + '、' + T('m') + ' に直線 ' + T('n') + ' が交わっている。')}"
            f"<div class=row><div class=lft><div class=qs>"
            + q(1, f"{a('a')} の対頂角はどれですか。", f"答　{b(18, a('c'))}", "", .7)
            + q(2, f"{a('c')} の同位角はどれですか。", f"答　{b(18, a('g'))}", "", .7)
            + q(3, f"{a('d')} の錯角はどれですか。", f"答　{b(18, a('f'))}", "", .7)
            + q(4, f"{T('\\ell\\parallel m')}、{a('a')}＝65° のとき、{a('g')} と {a('h')} の大きさを求めなさい。",
                f"答　{a('g')}＝{b(14, '65')}°　{a('h')}＝{b(14, '115')}°",
                f"同位角 {a('e')}＝{a('a')}＝65°、対頂角 {a('g')}＝{a('e')}＝65°。{a('h')}＝180°－65°＝115°", 1.3)
            + f"</div></div><div class=rgt>{lines_fig()}</div></div></div>")
    items = [
        f"2直線に1つの直線が交わるとき、2直線が平行ならば、同位角・錯角は {b(22, '等しい')}。",
        f"三角形の3つの内角の和は {b(18, '180')}°である。",
        f"三角形の1つの外角は、それととなり合わない2つの {b(30, '内角の和')} に等しい。",
        f"{T('n')} 角形の内角の和は {b(36, T('180^\\circ\\times(n-2)'))} である。",
        f"多角形の外角の和は {b(18, '360')}°である。",
        f"0°より大きく90°より小さい角を {b(20, '鋭角')}、90°より大きく180°より小さい角を {b(20, '鈍角')} という。",
        f"三角形の合同条件：{b(46, '3組の辺')} がそれぞれ等しい／{b(46, '2組の辺とその間の角')} がそれぞれ等しい／"
        f"{b(46, '1組の辺とその両端の角')} がそれぞれ等しい",
        f"「○○ならば△△」の形のことがらで、○○の部分を {b(20, '仮定')}、△△の部分を {b(20, '結論')} という。",
        f"ことばの意味をはっきりと述べたものを {b(20, '定義')}、証明されたことがらのうち大切なものを {b(20, '定理')} という。",
    ]
    blk2 = (f"<div class=blk style='flex:1.25 1 0'>{big(2, '次の文の空らんに当てはまることばや数・式を書きなさい。')}"
            f"<ol class=fill>{''.join(f'<li>{it}</li>' for it in items)}</ol></div>")
    blk3 = (f"<div class=blk>{big(3, '次の問いに答えなさい。')}<div class=qs>"
            + q(1, "八角形の内角の和は何度ですか。", f"答　{b(18, '1080')}°", f"{T('180\\times(8-2)=1080')}")
            + q(2, "正八角形の1つの内角は何度ですか。", f"答　{b(18, '135')}°", f"{T('1080\\div8=135')}（外角 {T('360\\div8=45')}、{T('180-45=135')} でもよい）")
            + q(3, "内角の和が1440°になる多角形は何角形ですか。", f"答　{b(22, '十')}角形",
                f"{T('180\\times(n-2)=1440')}　{T('n-2=8')}　{T('n=10')}")
            + q(4, "1つの外角が24°である正多角形は正何角形ですか。", f"答　正{b(22, '十五')}角形", f"{T('360\\div24=15')}")
            + "</div></div>")
    return f"<div class=page>{head(2, '図形の用語・性質')}{blk1}{blk2}{blk3}</div>"


# ---------- ③ 角度 ----------
W3, H3 = 76, 40


def fit(pts, w=W3, h=H3, mg=6):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    k = min((w - 2 * mg) / (max(xs) - min(xs)), (h - 2 * mg) / (max(ys) - min(ys)))
    ox = (w - k * (max(xs) - min(xs))) / 2 - k * min(xs)
    oy = (h - k * (max(ys) - min(ys))) / 2 - k * min(ys)
    return [(ox + k * p[0], oy + k * p[1]) for p in pts]


def pent(interiors, lens):
    """内角を順にもつ五角形。最後の2辺の長さは閉じるように決める"""
    hs = [0]
    for a_ in interiors[1:]:
        hs.append(hs[-1] + 180 - a_)
    (u3x, u3y), (u4x, u4y) = u(hs[3]), u(hs[4])
    sx = sum(L * u(hs[i])[0] for i, L in enumerate(lens))
    sy = sum(L * u(hs[i])[1] for i, L in enumerate(lens))
    L3, L4 = sp.symbols("L3 L4")
    so = sp.solve([sx + L3 * u3x + L4 * u4x, sy + L3 * u3y + L4 * u4y], [L3, L4])
    Ls = list(lens) + [float(so[L3]), float(so[L4])]
    assert min(Ls) > 0
    pts = [(0.0, 0.0)]
    for i in range(4):
        pts.append(add(pts[-1], u(hs[i]), Ls[i]))
    return pts, hs


def fig_angles():
    """10問：(図, 図の上の説明, 答え, 途中式)"""
    out = []
    # 1 3本の直線
    Fg = Fig(W3, H3)
    O = (38, 20)
    for d_, L in ((0, 34), (40, 22), (105, 19)):
        Fg.line(add(O, u(d_ + 180), L), add(O, u(d_), L))
    Fg.angle(O, add(O, u(0)), add(O, u(40)), "40°", 6, 4, 40)
    Fg.angle(O, add(O, u(40)), add(O, u(105)), "65°", 5, 4, 65)
    Fg.angle(O, add(O, u(285)), add(O, u(360)), "x", 6, 3.6, 75, True)
    out.append((Fg.svg(), "3本の直線が1点で交わっている。", 75,
                f"対頂角と一直線：{T('180-(40+65)=75')}"))
    # 2 平行線と同位角
    Fg = Fig(W3, H3)
    A = (32, 32)
    B = inter(A, 252, (0, 8), 0)
    Fg.line((4, 32), (68, 32)); Fg.line((4, 8), (68, 8))
    Fg.line(add(A, u(72), 7), add(B, u(252), 6))
    Fg.par((56, 32)); Fg.par((56, 8))
    Fg.text((69, 32), "ℓ", 1, 1.4, "start", 4.4, True); Fg.text((69, 8), "m", 1, 1.4, "start", 4.4, True)
    Fg.angle(A, add(A, u(0)), add(A, u(72)), "72°", 5, 4, 72)
    Fg.angle(B, add(B, u(180)), add(B, u(72)), "x", 5, 3.4, 108, True)
    out.append((Fg.svg(), f"{T('\\ell\\parallel m')}", 108, f"同位角で72°、{T('x=180-72=108')}"))
    # 3 くの字
    Fg = Fig(W3, H3)
    A = (10, 34)
    Pp = add(A, u(-35), 15 / math.sin(math.radians(35)))
    B = inter(Pp, 230, (0, 6), 0)
    Fg.line((4, 34), (64, 34)); Fg.line((4, 6), (64, 6))
    Fg.line(A, Pp); Fg.line(Pp, B)
    Fg.par((54, 34)); Fg.par((54, 6))
    Fg.text((65, 34), "ℓ", 1, 1.4, "start", 4.4, True); Fg.text((65, 6), "m", 1, 1.4, "start", 4.4, True)
    Fg.angle(A, add(A, u(0)), Pp, "35°", 7, 4.2, 35)
    Fg.angle(B, add(B, u(0)), Pp, "50°", 6, 4.2, 50)
    Fg.angle(Pp, A, B, "x", 4, 3.4, 85, True)
    out.append((Fg.svg(), f"{T('\\ell\\parallel m')}", 85,
                f"平行線をひいて錯角：{T('x=35+50=85')}"))
    # 4 三角形の内角
    Fg = Fig(W3, H3)
    B, C = (14, 4), (60, 4)
    A = inter(B, 55, C, 112)
    Fg.poly([A, B, C])
    Fg.angle(B, C, A, "55°", 5, 4, 55); Fg.angle(C, B, A, "68°", 5, 4, 68); Fg.angle(A, B, C, "x", 4, 3.4, 57, True)
    out.append((Fg.svg(), "", 57, f"{T('180-(55+68)=57')}"))
    # 5 外角
    Fg = Fig(W3, H3)
    B, C, D = (6, 4), (44, 4), (72, 4)
    A = inter(B, 62, C, 110)
    Fg.poly([A, B, C]); Fg.line(C, D)
    Fg.angle(B, C, A, "62°", 5, 4, 62); Fg.angle(A, B, C, "48°", 5, 4, 48); Fg.angle(C, D, A, "x", 5, 3.4, 110, True)
    out.append((Fg.svg(), "", 110, f"外角＝となりの内角の和：{T('x=48+62=110')}"))
    # 6 外角から内角
    Fg = Fig(W3, H3)
    B, C, D = (6, 4), (44, 4), (72, 4)
    A = inter(B, 55, C, 130)
    Fg.poly([A, B, C]); Fg.line(C, D)
    Fg.angle(A, B, C, "75°", 5, 4, 75); Fg.angle(C, D, A, "130°", 5, 5, 130); Fg.angle(B, C, A, "x", 5, 3.4, 55, True)
    out.append((Fg.svg(), "", 55, f"{T('x+75=130')} より {T('x=55')}"))
    # 7 五角形の内角
    ints = [100, 110, 95, 120, 115]
    pts, _ = pent(ints, [40, 26, 30])
    pts = fit(pts)
    Fg = Fig(W3, H3)
    Fg.poly(pts)
    for i, a_ in enumerate(ints):
        lab, it = (f"{a_}°", False) if i < 4 else ("x", True)
        Fg.angle(pts[i], pts[i - 1], pts[(i + 1) % 5], lab, 4, 4.2 if not it else 3.2, a_, it)
    out.append((Fg.svg(), "五角形", 115, f"{T('180\\times3=540')}、{T('540-425=115')}"))
    # 8 五角形の外角
    exts = [80, 65, 75, 60, 80]
    ints = [180 - e for e in exts]
    pts, hs = pent(ints, [36, 30, 28])
    ext_pts = []
    for i in range(5):                         # 各頂点で、前の辺をのばした先
        ext_pts.append(add(pts[i], u(hs[i - 1] if i else hs[4]), 9))
    allp = fit(pts + ext_pts, mg=4)
    pts, ext_pts = allp[:5], allp[5:]
    Fg = Fig(W3, H3)
    Fg.poly(pts)
    for i in range(5):
        Fg.line(pts[i], ext_pts[i], .45)
        lab, it = (f"{exts[i]}°", False) if i < 4 else ("x", True)
        Fg.angle(pts[i], ext_pts[i], pts[(i + 1) % 5], lab, 3.4, 3.8 if not it else 3, exts[i], it)
    out.append((Fg.svg(), "五角形の外角", 80, f"外角の和360°：{T('360-280=80')}"))
    # 9 くぼんだ四角形
    Fg = Fig(W3, H3)
    B, C = (10, 4), (66, 4)
    A = inter(B, 70, C, 110)
    D = inter(B, 40, C, 135)
    sc = 36 / (A[1] - 4)
    A, D = (38 + (A[0] - 38) * sc, 4 + (A[1] - 4) * sc), (38 + (D[0] - 38) * sc, 4 + (D[1] - 4) * sc)
    B, C = (38 + (B[0] - 38) * sc, 4), (38 + (C[0] - 38) * sc, 4)
    Fg.line(A, B); Fg.line(B, D); Fg.line(D, C); Fg.line(C, A)
    Fg.angle(A, B, C, "40°", 6, 4, 40); Fg.angle(B, A, D, "30°", 7, 4.2, 30); Fg.angle(C, A, D, "25°", 8, 4.2, 25)
    Fg.angle(D, B, C, "x", 4, 3.2, 95, True)
    out.append((Fg.svg(), "", 95, f"{T('x=40+30+25=95')}"))
    # 10 平行線と三角形
    Fg = Fig(W3, H3)
    A = (34, 34)
    B = inter(A, 228, (0, 6), 0)
    C = inter(A, 290, (0, 6), 0)
    Fg.line((4, 34), (68, 34)); Fg.line((4, 6), (68, 6))
    Fg.line(A, B); Fg.line(A, C)
    Fg.par((58, 34)); Fg.par((58, 6))
    Fg.text((69, 34), "ℓ", 1, 1.4, "start", 4.4, True); Fg.text((69, 6), "m", 1, 1.4, "start", 4.4, True)
    Fg.angle(A, add(A, u(180)), B, "48°", 6, 4.4, 48)
    Fg.angle(C, B, A, "70°", 5, 4.2, 70)
    Fg.angle(A, B, C, "x", 4, 3.2, 62, True)
    out.append((Fg.svg(), f"{T('\\ell\\parallel m')}", 62,
                f"錯角で48°、{T('x=180-(48+70)=62')}"))
    return out


def page3():
    figs = fig_angles()
    cells = []
    for i, (svg, cap, val, work) in enumerate(figs, 1):
        cells.append(f"<div class=cell><div class=ct><span class=no>({i})</span>{cap}</div>"
                     f"<div class=cfig>{svg}</div><div class=crow><div class=work>{work if ANS else ''}</div>"
                     f"<div class=ans>答　{T('\\angle x')}＝{b(16, str(val))}°</div></div></div>")
    return (f"<div class=page>{head(3, '角度を求める')}"
            f"{big(1, '次の図で、' + T('\\angle x') + ' の大きさを求めなさい。', '同じ印のついた直線は平行')}"
            f"<div class=grid>{''.join(cells)}</div></div>")


# ---------- ④ 証明の進め方 ----------
def proof_fig1():
    Fg = Fig(52, 40)
    O = (26, 20)
    A, B = (6, 36), (10, 4)
    D, C = (2 * O[0] - A[0], 2 * O[1] - A[1]), (2 * O[0] - B[0], 2 * O[1] - B[1])
    Fg.line(A, D); Fg.line(B, C); Fg.line(A, B); Fg.line(C, D)
    for p, t, dx, dy, an in ((A, "A", -1.4, -1, "end"), (B, "B", -1.4, 3.6, "end"), (C, "C", 1.4, -1, "start"),
                             (D, "D", 1.4, 3.6, "start"), (O, "O", 0, 5.4, "middle")):
        Fg.text(p, t, dx, dy, an, 4)
    return Fg.svg()


def proof_fig2():
    Fg = Fig(52, 44)
    A, B, C = (26, 37), (4, 4), (48, 4)
    D, E = add(A, ((B[0] - A[0]) * .55, (B[1] - A[1]) * .55)), add(A, ((C[0] - A[0]) * .55, (C[1] - A[1]) * .55))
    Fg.poly([A, B, C]); Fg.line(B, E); Fg.line(C, D)
    for p, t, dx, dy, an in ((A, "A", 0, -1.6, "middle"), (B, "B", -1.4, 3.6, "end"), (C, "C", 1.4, 3.6, "start"),
                             (D, "D", -1.6, 0, "end"), (E, "E", 1.6, 0, "start")):
        Fg.text(p, t, dx, dy, an, 4)
    return Fg.svg()


def page4():
    k = lambda t: f"<span class=kk>{t}</span>"
    blk1 = (f"<div class=blk style='flex:.8 1 0'>{big(1, '次のことがらの仮定と結論を答えなさい。')}<div class=qs>"
            + q(1, f"{X} が6の倍数ならば、{X} は3の倍数である。",
                f"仮定{b(42, X + ' が6の倍数')}　結論{b(42, X + ' は3の倍数')}", "", .8)
            + q(2, "△ABC≡△DEF ならば、∠A＝∠D である。", f"仮定{b(42, '△ABC≡△DEF')}　結論{b(42, '∠A＝∠D')}", "", .8)
            + q(3, "2直線が平行ならば、錯角は等しい。", f"仮定{b(42, '2直線が平行')}　結論{b(42, '錯角は等しい')}", "", .8)
            + "</div></div>")
    proof = (f"（証明）△ABOと△DCOにおいて<br>"
             f"仮定から　AO＝{b(14, 'DO')}　…①<br>"
             f"{b(22, '対頂角')} は等しいから　∠AOB＝∠{b(14, 'DOC')}　…②<br>"
             f"AB∥CD より、平行線の {b(16, '錯角')} は等しいから<br>∠OAB＝∠{b(14, 'ODC')}　…③<br>"
             f"①、②、③より、{b(58, '1組の辺とその両端の角')} が<br>それぞれ等しいから　"
             f"△ABO≡△DCO")
    blk2 = (f"<div class=blk style='flex:1.75 1 0'>{big(2, '下の図で、線分ADとBCは点Oで交わり、AO＝DO、AB∥CD です。')}"
            f"<div class=row><div class=lft><div class=pt>(1)　このとき、△ABO≡△DCO であることを次のように証明した。"
            f"空らんに当てはまることばや記号を書きなさい。</div><div class=proof>{proof}</div>"
            f"<div class=qs>"
            + q(2, "この証明から、AB＝DC であることがいえます。その理由を書きなさい。",
                f"{b(110, '合同な図形の対応する辺は等しいから')}", "", .7)
            + f"</div></div><div class=rgt>{proof_fig1()}</div></div></div>")
    ans3 = ("（証明）△ABEと△ACDにおいて<br>仮定から　AB＝AC　…①<br>　　　　　AE＝AD　…②<br>"
            "共通な角だから　∠BAE＝∠CAD　…③<br>①、②、③より、2組の辺とその間の角がそれぞれ等しいから<br>"
            "　　△ABE≡△ACD")
    blk3 = (f"<div class=blk style='flex:1.25 1 0'>{big(3, '下の図で、AB＝AC、AD＝AE です。')}"
            f"<div class=row><div class=lft><div class=pt>このとき、△ABE≡△ACD であることを証明しなさい。</div>"
            f"<div class=frm>{ans3 if ANS else ''}</div></div><div class=rgt>{proof_fig2()}</div></div></div>")
    return f"<div class=page>{head(4, '証明の進め方')}{blk1}{blk2}{blk3}</div>"


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; font-size: 10pt; }
.page { width: 210mm; height: 297mm; padding: 9mm 12mm 9mm; page-break-after: always;
        display: flex; flex-direction: column; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.katex { font-size: 1.07em; }
.head { display: flex; align-items: baseline; white-space: nowrap; border-bottom: 1pt solid #111; padding-bottom: 1.6mm; }
.head b { font-size: 12.5pt; }
.head .sub { font-size: 9.5pt; margin-left: 2mm; }
.head .cl { margin-left: auto; font-size: 9.5pt; }
.head .u { display: inline-block; border-bottom: .7pt solid #111; }
.head .kotae { margin-left: auto; font-weight: 700; color: #b4232c; font-size: 12pt; }
.big { margin-top: 2.2mm; font-weight: 700; font-size: 10.5pt; display: flex; align-items: center; gap: 2mm; flex-wrap: wrap; }
.big .box { display: inline-flex; width: 5.6mm; height: 5.6mm; border: .9pt solid #111; align-items: center; justify-content: center; }
.big .pill { font-size: 8pt; font-weight: 400; border: .7pt solid #111; border-radius: 3mm; padding: .2mm 2mm; }
.blk { flex: 1 1 0; min-height: 0; display: flex; flex-direction: column; }
.blk + .blk { border-top: .8pt solid #111; margin-top: 1.5mm; }
.row { flex: 1; min-height: 0; display: flex; gap: 4mm; margin-top: 1.2mm; }
.lft { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.rgt { flex: none; display: flex; align-items: flex-start; justify-content: center; }
.story, .pt { line-height: 1.65; }
.qs { flex: 1; min-height: 0; display: flex; flex-direction: column; margin-top: 1mm; }
.sqi { display: flex; flex-direction: column; border-top: .4pt solid #bbb; padding: 1.2mm 0 1mm; }
.qt { display: flex; flex-wrap: wrap; line-height: 1.6; }
.qt > div { flex: 1 1 50mm; }
.ans.in { margin-left: auto; align-self: flex-end; }
.qt .no, .ct .no { flex: none; width: 7.5mm; font-size: 9pt; }
.work { flex: 1; margin: .6mm 0 0 7.5mm; line-height: 1.75; font-size: 9.5pt; color: #c0141e; }
.ans { align-self: flex-end; white-space: nowrap; }
.ul { display: inline-block; border-bottom: .8pt solid #111; height: 5.4mm; vertical-align: baseline; }
.ul.fill { color: #c0141e; font-weight: 700; text-align: center; height: auto; line-height: 1.3; }
.fig { flex: none; }
.fig text, .gr text { font-family: 'Noto Sans CJK JP'; }
ol.fill { margin: 1.2mm 0 0 7mm; flex: 1; display: flex; flex-direction: column; justify-content: space-around; line-height: 2.05; }
.grid { flex: 1; min-height: 0; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(5, 1fr); gap: 0 6mm; margin-top: 1.5mm; }
.cell { display: flex; flex-direction: column; border-top: .4pt solid #bbb; padding-top: 1mm; min-height: 0; }
.ct { display: flex; align-items: baseline; font-size: 9.5pt; }
.cfig { display: flex; justify-content: center; }
.crow { display: flex; align-items: flex-end; gap: 2mm; }
.crow .work { flex: 1; }
.cell .work { margin-left: 0; font-size: 8.4pt; line-height: 1.4; flex: none; }
.proof { margin-top: 1.5mm; line-height: 2.25; border: .8pt solid #444; border-radius: 2mm; padding: 1mm 3mm; }
.frm { flex: 1; margin-top: 1.5mm; border: .9pt solid #444; border-radius: 2.5mm; padding: 2mm 3mm; line-height: 2; color: #c0141e; }
"""


def build(ans):
    global ANS
    ANS = ans
    return page1() + page2() + page3() + page4()


if __name__ == "__main__":
    build(False)
    print("確認OK：答え・図の角度")
    write_pdfs([
        (doc(CSS, build(False)), f"{FILE}.pdf"),
        (doc(CSS, build(True)), f"{FILE}_ans.pdf"),
    ])
