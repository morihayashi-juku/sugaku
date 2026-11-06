"""中2 定期テスト対策（一次関数の利用：速さ・動点・グラフと面積）4パターン（1ページ＝1パターン）＋こたえ4ページ

  cd tools && python3 c2_teiki_ichiji_riyou_thu.py

- A3 に拡大して印刷する想定。ファイルは A4 で、1ページに左右2列（ほかの定期テスト対策プリントと同じ形）。
  左＝［1］速さ（ダイヤグラム）・［2］動点（長方形の辺上を動く点P）／右＝［3］グラフと面積（2直線と三角形）
- 式は KaTeX（texlib）。文字式の文字は KaTeX の数式用イタリック。
- 出力：pdf/c2_teiki_ichiji_riyou_thu.pdf と c2_teiki_ichiji_riyou_thu_ans.pdf
- 答えは SymPy・座標計算で確かめる（check）。
"""
import math
from fractions import Fraction as F

import sympy as sp

from texlib import doc, tex as T, write_pdfs

FILE = "c2_teiki_ichiji_riyou_thu"
NO = "①②③④"
RED, BLUE, GRAY = "#b4232c", "#1f5fbf", "#555"


# ---------- 小さな道具 ----------
def fr(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{'-' if v < 0 else ''}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def lin(a, b):
    a, b = F(a), F(b)
    s = ""
    if a != 0:
        s = "x" if a == 1 else "-x" if a == -1 else f"{fr(a)}x"
    if b != 0:
        s = s + ("+" if b > 0 else "-") + fr(abs(b)) if s else fr(b)
    return "y=" + (s or "0")


def line2(p, q):
    (x1, y1), (x2, y2) = p, q
    a = F(y2 - y1) / F(x2 - x1)
    return a, F(y1) - a * x1


def UL(w):
    return f"<span class=ul style='width:{w}mm'></span>"


def pt_tex(p):
    return T(f"({fr(p[0])},\\ {fr(p[1])})")


# ---------- 方眼・座標平面（SVG。単位は mm） ----------
class Plane:
    def __init__(s, xr, yr, cx, cy, xs, ys, cross=False, xt="x", yt="y", xu="", yu="", ml=9.5, mb=6, mt=5.5, mr=9):
        s.xmin, s.xmax = xr
        s.ymin, s.ymax = yr
        s.cx, s.cy, s.xs, s.ys, s.cross = cx, cy, xs, ys, cross
        s.xt, s.yt, s.xu, s.yu = xt, yt, xu, yu
        s.ml, s.mb, s.mt, s.mr = ml, mb, mt, mr
        s.w, s.h = (s.xmax - s.xmin) * cx, (s.ymax - s.ymin) * cy
        s.o = []

    def X(s, v):
        return (float(v) - s.xmin) * s.cx

    def Y(s, v):
        return (s.ymax - float(v)) * s.cy

    def text(s, x, y, t, dx=0, dy=0, anchor="middle", size=2.8, extra=""):
        s.o.append(f'<text x="{s.X(x) + dx:.2f}" y="{s.Y(y) + dy:.2f}" font-size="{size}" text-anchor="{anchor}" {extra}>{t}</text>')

    def line(s, a, b, color, width=.55):
        lo, hi = float(s.xmin), float(s.xmax)
        if a != 0:
            u, v = (s.ymin - b) / a, (s.ymax - b) / a
            lo, hi = max(lo, float(min(u, v))), min(hi, float(max(u, v)))
        elif not (s.ymin <= b <= s.ymax):
            return
        if lo > hi:
            return
        s.o.append(f'<line x1="{s.X(lo):.2f}" y1="{s.Y(a * F(lo).limit_denominator(10**6) + b):.2f}" '
                   f'x2="{s.X(hi):.2f}" y2="{s.Y(a * F(hi).limit_denominator(10**6) + b):.2f}" '
                   f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')

    def poly(s, pts, color, width=.55, dots=True, r=.7):
        s.o.append(f'<polyline points="{" ".join(f"{s.X(x):.2f},{s.Y(y):.2f}" for x, y in pts)}" fill="none" '
                   f'stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>')
        if dots:
            for x, y in pts:
                s.o.append(f'<circle cx="{s.X(x):.2f}" cy="{s.Y(y):.2f}" r="{r}" fill="{color}"/>')

    def dot(s, x, y, color="#111", r=.75):
        s.o.append(f'<circle cx="{s.X(x):.2f}" cy="{s.Y(y):.2f}" r="{r}" fill="{color}"/>')

    def svg(s):
        w, h = s.w, s.h
        ax = 0 if (s.cross and s.xmin <= 0 <= s.xmax) else s.xmin       # y 軸の位置（x 座標）
        ay = 0 if (s.cross and s.ymin <= 0 <= s.ymax) else s.ymin       # x 軸の位置（y 座標）
        g = []
        for axis in "xy":
            lo, hi, st, cl = (s.xmin, s.xmax, s.xs, s.X) if axis == "x" else (s.ymin, s.ymax, s.ys, s.Y)
            v = math.ceil(lo / st[0]) * st[0]
            while v <= hi:
                major = v % st[1] == 0
                c, wd = ("#888", .2) if major else ("#c9c9c9", .12)
                if axis == "x":
                    g.append(f'<line x1="{cl(v):.2f}" y1="0" x2="{cl(v):.2f}" y2="{h}" stroke="{c}" stroke-width="{wd}"/>')
                else:
                    g.append(f'<line x1="0" y1="{cl(v):.2f}" x2="{w}" y2="{cl(v):.2f}" stroke="{c}" stroke-width="{wd}"/>')
                v += st[0]
        X0, Y0 = s.X(ax), s.Y(ay)
        g.append(f'<line x1="0" y1="{Y0}" x2="{w + 2.2}" y2="{Y0}" stroke="#111" stroke-width=".4"/>')
        g.append(f'<line x1="{X0}" y1="{h}" x2="{X0}" y2="-2.2" stroke="#111" stroke-width=".4"/>')
        g.append(f'<polygon points="{w + 3.4},{Y0} {w + 1.4},{Y0 - .8} {w + 1.4},{Y0 + .8}" fill="#111"/>')
        g.append(f'<polygon points="{X0},-3.4 {X0 - .8},-1.4 {X0 + .8},-1.4" fill="#111"/>')
        lab = []

        def L(x, y, t, anchor="middle"):
            lab.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="3.4" text-anchor="{anchor}">{t}</text>')

        mi = lambda v: str(v).replace("-", "−")
        kx = 1
        while s.cx * s.xs[1] * kx < 7:
            kx += 1
        ky = 1
        while s.cy * s.ys[1] * ky < 5.6:
            ky += 1
        v = math.ceil(s.xmin / (s.xs[1] * kx)) * s.xs[1] * kx
        while v <= s.xmax:
            if v != 0:
                L(s.X(v), Y0 + 3.9, mi(v))
            v += s.xs[1] * kx
        v = math.ceil(s.ymin / (s.ys[1] * ky)) * s.ys[1] * ky
        while v <= s.ymax:
            if v != 0:
                L(X0 - 1.0, s.Y(v) + 1.2, mi(v), "end")
            v += s.ys[1] * ky
        L(X0 - 1.0, Y0 + 3.9, "O", "end")
        it = 'font-family="KaTeX_Math" font-style="italic"'
        lab.append(f'<text x="{w + 4.4:.2f}" y="{Y0 + 1:.2f}" font-size="4" {it}>{s.xt}<tspan font-family="Noto Sans CJK JP" font-style="normal" font-size="3.3">{s.xu}</tspan></text>')
        lab.append(f'<text x="{X0 + 1.8:.2f}" y="-1.6" font-size="4" text-anchor="start" {it}>{s.yt}<tspan font-family="Noto Sans CJK JP" font-style="normal" font-size="3.3">{s.yu}</tspan></text>')
        W, H = w + s.ml + s.mr, h + s.mt + s.mb
        return (f'<svg class=gr width="{W:.1f}mm" height="{H:.1f}mm" viewBox="{-s.ml} {-s.mt} {W:.1f} {H:.1f}">'
                f'{"".join(g)}{"".join(s.o)}{"".join(lab)}</svg>')


# ---------- ［1］速さ（ダイヤグラム） ----------
def seg(pts, i):
    (t0, d0), (t1, d1) = pts[i], pts[i + 1]
    a = F(d1 - d0, t1 - t0)
    return a, F(d0) - a * t0, (t0, t1)


def at(pts, t):
    for i in range(len(pts) - 1):
        a, b, (t0, t1) = seg(pts, i)
        if t0 <= t <= t1:
            return a * t + b
    raise ValueError(t)


def meet(s1, s2):
    (a1, b1, r1), (a2, b2, r2) = s1, s2
    x = (b2 - b1) / (a1 - a2)
    assert max(r1[0], r2[0]) <= x <= min(r1[1], r2[1]), (s1, s2, x)
    return x, a1 * x + b1


def eqx(lo, hi):
    return T(f"{lo}\\leqq x\\leqq {hi}")


def speed_pattern(k):
    X, Y = T("x"), T("y")
    unit = f"{X} 分、家からの道のりを {Y} m"
    if k == 0:
        g = dict(xr=(0, 20), yr=(0, 1200), xs=(1, 5), ys=(100, 200))
        ppl = [("弟", RED, [(0, 0), (20, 1200)], (20, 1200, -2, 3.6, "end")),
               ("兄", BLUE, [(5, 0), (15, 1200)], (15, 1200, -1.5, -1.6, "end"))]
        story = (f"弟は、家を出発して駅まで歩いた。5分後に、兄が家を出発して、同じ道を自転車で追いかけた。"
                 f"右のグラフは、弟が出発してからの時間を {unit} として、2人のようすを表したものである。"
                 f"2人とも一定の速さで進むものとする。")
        ot, nt = ppl[0][2], ppl[1][2]
        a_o, b_o, _ = seg(ot, 0)
        a_n, b_n, rn = seg(nt, 0)
        mx, my = meet(seg(ot, 0), seg(nt, 0))
        end_t = nt[-1][0]
        rem = nt[-1][1] - at(ot, end_t)
        assert (a_n, b_n, mx, my, rem) == (120, -600, 10, 600, 300)
        qs = [
            ("兄の自転車の速さは分速何mですか。", f"答　分速{UL(16)}m",
             f"{T('1200\\div(15-5)=120')}", "分速120m"),
            (f"兄が家を出発してから駅に着くまでの {X} と {Y} の関係を、式で表しなさい。{X} の変域もかくこと。", f"答　{UL(46)}",
             f"傾きは兄の速さ120。点{pt_tex((5, 0))}を通るから {T('0=120\\times5+b')}、{T('b=-600')}",
             f"{T('y=120x-600')}　{eqx(5, 15)}"),
            ("兄が弟に追いつくのは、弟が家を出発してから何分後ですか。また、それは家から何mの地点ですか。",
             f"答　{UL(12)}分後、家から{UL(12)}m",
             f"弟は {T('y=60x')}。{T('60x=120x-600')} を解いて {T('x=10')}、{T('y=60\\times10=600')}", "10分後、家から600m"),
            ("兄が駅に着いたとき、弟は駅の何m手前にいますか。", f"答　{UL(16)}m",
             f"兄が駅に着くのは {T('x=15')} のとき。弟は {T('y=60\\times15=900')} の地点だから、{T('1200-900=300')}", "300m"),
        ]
    elif k == 1:
        g = dict(xr=(0, 30), yr=(0, 2400), xs=(1, 5), ys=(200, 400))
        ppl = [("Aさん", RED, [(0, 0), (30, 2400)], (30, 2400, -1.2, -1.8, "end")),
               ("Bさん", BLUE, [(5, 2400), (25, 0)], (5, 2400, 1.8, 3.4, "start"))]
        story = (f"P町とQ町は2400m離れている。Aさんは、P町からQ町へ歩いた。5分後に、BさんがQ町からP町へ、"
                 f"同じ道を自転車で向かった。右のグラフは、Aさんが出発してからの時間を {X} 分、P町からの道のりを {Y} m として、"
                 f"2人のようすを表したものである。2人とも一定の速さで進むものとする。")
        at_, bt_ = ppl[0][2], ppl[1][2]
        a_b, b_b, _ = seg(bt_, 0)
        mx, my = meet(seg(at_, 0), seg(bt_, 0))
        rem = 2400 - at(at_, 25)
        assert (a_b, b_b, mx, my, rem) == (-120, 3000, 15, 1200, 400)
        qs = [
            ("Aさんの歩く速さは分速何mですか。", f"答　分速{UL(16)}m", f"{T('2400\\div30=80')}", "分速80m"),
            (f"Bさんが出発してからP町に着くまでの {X} と {Y} の関係を、式で表しなさい。{X} の変域もかくこと。", f"答　{UL(46)}",
             f"Bさんの速さは {T('2400\\div(25-5)=120')}。グラフは右下がりだから傾きは {T('-120')}。"
             f"点{pt_tex((25, 0))}を通るから {T('0=-120\\times25+b')}、{T('b=3000')}",
             f"{T('y=-120x+3000')}　{eqx(5, 25)}"),
            ("2人が出会うのは、Aさんが出発してから何分後ですか。また、それはP町から何mの地点ですか。",
             f"答　{UL(12)}分後、P町から{UL(12)}m",
             f"Aさんは {T('y=80x')}。{T('80x=-120x+3000')} を解いて {T('x=15')}、{T('y=80\\times15=1200')}", "15分後、P町から1200m"),
            ("Bさんが P町に着いたとき、Aさんは Q町まであと何mのところにいますか。", f"答　{UL(16)}m",
             f"Bさんが着くのは {T('x=25')} のとき。Aさんは {T('y=80\\times25=2000')} の地点だから、{T('2400-2000=400')}", "400m"),
        ]
    elif k == 2:
        g = dict(xr=(0, 40), yr=(0, 2400), xs=(2, 10), ys=(200, 400))
        ppl = [("姉", RED, [(0, 0), (10, 800), (20, 800), (40, 2400)], (40, 2400, -1.2, -1.8, "end")),
               ("父", BLUE, [(18, 0), (28, 2400)], (28, 2400, -2, -1.2, "end"))]
        story = (f"姉は、家から展望台まで歩いた。途中で休けいしたが、休けいの前後で歩く速さは同じである。"
                 f"姉が出発した18分後に、父が自転車で同じ道を追いかけた。右のグラフは、姉が出発してからの時間を {unit} として、"
                 f"2人のようすを表したものである。休けい以外は、一定の速さで進むものとする。")
        am, fa = ppl[0][2], ppl[1][2]
        a2, b2, _ = seg(am, 2)
        mx, my = meet(seg(am, 2), seg(fa, 0))
        rem = 2400 - at(am, 28)
        assert (a2, b2, mx, my, rem) == (80, -800, 22, 960, 960)
        qs = [
            ("姉は、途中で何分間休けいしましたか。", f"答　{UL(16)}分間", f"グラフが横になっているのは {T('x=10')} から {T('x=20')} まで", "10分間"),
            (f"姉が休けいしたあと、展望台に着くまでの {X} と {Y} の関係を、式で表しなさい。{X} の変域もかくこと。", f"答　{UL(46)}",
             f"姉の速さは {T('800\\div10=80')}。傾きは80、点{pt_tex((20, 800))}を通るから {T('800=80\\times20+b')}、{T('b=-800')}",
             f"{T('y=80x-800')}　{eqx(20, 40)}"),
            ("父が姉に追いつくのは、姉が家を出発してから何分後ですか。また、それは家から何mの地点ですか。",
             f"答　{UL(12)}分後、家から{UL(12)}m",
             f"父は {T('2400\\div(28-18)=240')} より {T('y=240x-4320')}（点{pt_tex((18, 0))}を通る）。"
             f"{T('240x-4320=80x-800')} を解いて {T('x=22')}、{T('y=80\\times22-800=960')}", "22分後、家から960m"),
            ("父が展望台に着いたとき、姉は展望台まであと何mのところにいますか。", f"答　{UL(16)}m",
             f"父が着くのは {T('x=28')} のとき。姉は {T('y=80\\times28-800=1440')} の地点だから、{T('2400-1440=960')}", "960m"),
        ]
    else:
        g = dict(xr=(0, 30), yr=(0, 1400), xs=(1, 5), ys=(100, 200))
        ppl = [("兄", RED, [(0, 0), (12, 1200), (16, 1200), (28, 0)], (28, 0, 1.2, -2.4, "start")),
               ("弟", BLUE, [(17, 0), (27, 1200)], (27, 1200, 1.8, 2.2, "start"))]
        story = (f"兄は、家から公園まで歩き、公園で休んだあと、同じ道を歩いて帰った。"
                 f"兄が出発した17分後に、弟が家から公園まで走った。"
                 f"右のグラフは、兄が出発してからの時間を {unit} として、2人のようすを表したものである。"
                 f"休けい以外は、一定の速さで進むものとする。")
        br, ot = ppl[0][2], ppl[1][2]
        a3, b3, _ = seg(br, 2)
        mx, my = meet(seg(br, 2), seg(ot, 0))
        rem = at(br, 27)
        assert (a3, b3, mx, my, rem) == (-100, 2800, 22, 600, 100)
        qs = [
            ("兄が家から公園まで歩いた速さは分速何mですか。", f"答　分速{UL(16)}m", f"{T('1200\\div12=100')}", "分速100m"),
            (f"兄が公園を出発してから家に着くまでの {X} と {Y} の関係を、式で表しなさい。{X} の変域もかくこと。", f"答　{UL(46)}",
             f"グラフは右下がりで、{T('1200\\div(28-16)=100')} より傾きは {T('-100')}。点{pt_tex((28, 0))}を通るから "
             f"{T('0=-100\\times28+b')}、{T('b=2800')}", f"{T('y=-100x+2800')}　{eqx(16, 28)}"),
            ("兄と弟が道の途中で出会うのは、兄が家を出発してから何分後ですか。また、それは家から何mの地点ですか。",
             f"答　{UL(12)}分後、家から{UL(12)}m",
             f"弟は {T('1200\\div(27-17)=120')} より {T('y=120x-2040')}（点{pt_tex((17, 0))}を通る）。"
             f"{T('-100x+2800=120x-2040')} を解いて {T('x=22')}、{T('y=-100\\times22+2800=600')}", "22分後、家から600m"),
            ("弟が公園に着いたとき、兄は家まであと何mのところにいますか。", f"答　{UL(16)}m",
             f"弟が着くのは {T('x=27')} のとき。兄は {T('y=-100\\times27+2800=100')} の地点にいる", "100m"),
        ]

    def plane(wmm=62, hmm=21):
        P = Plane(g["xr"], g["yr"], wmm / (g["xr"][1] - g["xr"][0]), hmm / (g["yr"][1] - g["yr"][0]),
                  g["xs"], g["ys"], xu="（分）", yu="（m）", mr=17)
        for name, col, pts, (lx, ly, dx, dy, an) in ppl:
            P.poly(pts, col)
            P.text(lx, ly, name, dx, dy, an, 3.9, f'style="fill:{col};font-weight:700"')
        return P

    return dict(story=story, plane=plane, g=g, qs=qs, ppl=ppl)


# ---------- ［2］動点 ----------
def tri_area(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])) / F(2)


def dot_pattern(path, tri, W, H, v, x1, yk, asked, reasons):
    pts = {"A": (0, H), "B": (0, 0), "C": (W, 0), "D": (W, H)}
    seq = list(path)
    ts = [F(0)]
    for i in range(len(seq) - 1):
        p, q = pts[seq[i]], pts[seq[i + 1]]
        ts.append(ts[-1] + F(abs(p[0] - q[0]) + abs(p[1] - q[1]), v))
    fixed = [pts[c] for c in tri if c != "P"]

    def pos(x):
        for i in range(len(seq) - 1):
            if ts[i] <= x <= ts[i + 1]:
                p, q = pts[seq[i]], pts[seq[i + 1]]
                r = (x - ts[i]) / (ts[i + 1] - ts[i])
                return (p[0] + (q[0] - p[0]) * r, p[1] + (q[1] - p[1]) * r)

    area = lambda x: tri_area(pos(x), *fixed)
    ys = [area(t) for t in ts]
    pieces = []
    for i in range(len(seq) - 1):
        a = (ys[i + 1] - ys[i]) / (ts[i + 1] - ts[i])
        b = ys[i] - a * ts[i]
        for t in (ts[i] + (ts[i + 1] - ts[i]) / 3, ts[i] + (ts[i + 1] - ts[i]) * F(2, 3)):
            assert area(t) == a * t + b, (path, tri, i)         # 幾何で面積を直接はかって一致を確かめる
        pieces.append((int(ts[i]), int(ts[i + 1]), a, b))
    assert all(t.denominator == 1 for t in ts)
    return dict(path=seq, tri=tri, W=W, H=H, v=v, x1=x1, yk=yk, asked=asked, reasons=reasons,
                ts=[int(t) for t in ts], pieces=pieces, ys=[int(y) for y in ys])


DOT = [
    dot_pattern("ABCD", "APD", 8, 6, 2, 2, 8, (0, 2),
                [f"点Pは辺AB上。AP＝{T('2x')} cm、底辺AD＝8cm だから {T('y=\\dfrac12\\times8\\times2x=8x')}",
                 f"点Pは辺BC上。底辺AD＝8cm、高さAB＝6cm で一定。{T('y=\\dfrac12\\times8\\times6=24')}",
                 f"点Pは辺CD上。DP＝{T('6-2(x-7)=-2x+20')} cm だから {T('y=\\dfrac12\\times8\\times(-2x+20)=-8x+80')}"]),
    dot_pattern("BCD", "APC", 6, 4, 1, 2, 6, (0, 1),
                [f"点Pは辺BC上。PC＝{T('6-x')} cm、高さAB＝4cm だから {T('y=\\dfrac12\\times(6-x)\\times4=-2x+12')}",
                 f"点Pは辺CD上。CP＝{T('x-6')} cm、高さBC＝6cm だから {T('y=\\dfrac12\\times(x-6)\\times6=3x-18')}"]),
    dot_pattern("BCDA", "ABP", 8, 6, 2, 3, 12, (0, 2),
                [f"点Pは辺BC上。BP＝{T('2x')} cm、底辺AB＝6cm だから {T('y=\\dfrac12\\times6\\times2x=6x')}",
                 f"点Pは辺CD上。底辺AB＝6cm、高さBC＝8cm で一定。{T('y=\\dfrac12\\times6\\times8=24')}",
                 f"点Pは辺DA上。AP＝{T('8-2(x-7)=-2x+22')} cm、底辺AB＝6cm だから {T('y=\\dfrac12\\times6\\times(-2x+22)=-6x+66')}"]),
    dot_pattern("ABC", "APC", 8, 6, 1, 2, 12, (0, 1),
                [f"点Pは辺AB上。AP＝{T('x')} cm、高さBC＝8cm だから {T('y=\\dfrac12\\times x\\times8=4x')}",
                 f"点Pは辺BC上。PC＝{T('8-(x-6)=-x+14')} cm、高さAB＝6cm だから {T('y=\\dfrac12\\times(-x+14)\\times6=-3x+42')}"]),
]


def rect_fig(d, s=2.9):
    W, H = d["W"], d["H"]
    w, h = W * s, H * s
    pts = {"A": (0, 0), "B": (0, h), "C": (w, h), "D": (w, 0)}
    o = [f'<svg class=fig width="{w + 22}mm" height="{h + 13}mm" viewBox="-14 -6 {w + 22} {h + 13}">',
         f'<rect x="0" y="0" width="{w}" height="{h}" fill="none" stroke="#111" stroke-width=".5"/>']
    seq = d["path"]
    for i in range(len(seq) - 1):                       # 進む向きの矢印（辺の真ん中）
        p, q = pts[seq[i]], pts[seq[i + 1]]
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        ux, uy = (q[0] - p[0]), (q[1] - p[1])
        n = math.hypot(ux, uy)
        ux, uy = ux / n, uy / n
        tip = (mx + ux * 1.6, my + uy * 1.6)
        l1 = (mx - ux * 1.2 - uy * 1.2, my - uy * 1.2 + ux * 1.2)
        l2 = (mx - ux * 1.2 + uy * 1.2, my - uy * 1.2 - ux * 1.2)
        o.append(f'<polygon points="{tip[0]:.2f},{tip[1]:.2f} {l1[0]:.2f},{l1[1]:.2f} {l2[0]:.2f},{l2[1]:.2f}" fill="{GRAY}"/>')
    sx, sy = pts[seq[0]]
    o.append(f'<circle cx="{sx}" cy="{sy}" r="1.1" fill="#111"/>')
    lab = {"A": (-1.6, -1.4, "end"), "B": (-1.6, 3.6, "end"), "C": (1.6, 3.6, "start"), "D": (1.6, -1.4, "start")}
    for c, (dx, dy, an) in lab.items():
        o.append(f'<text x="{pts[c][0] + dx}" y="{pts[c][1] + dy}" font-size="4.2" text-anchor="{an}">{c}</text>')
    o.append(f'<text x="-2.2" y="{h / 2 + 1}" font-size="3.7" text-anchor="end">{H}cm</text>')
    o.append(f'<text x="{w / 2}" y="{h + 5.6}" font-size="3.7" text-anchor="middle">{W}cm</text>')
    o.append("</svg>")
    return "".join(o)


def dot_plane(d, cell_x=None):
    ts, ys = d["ts"], d["ys"]
    xmax, ymax = ts[-1], max(ys)
    ytop = (ymax // 4 + 1) * 4
    return Plane((0, xmax), (0, ytop), 62 / xmax, 21 / ytop, (1, 2), (2, 4), xu="（秒）", yu="（cm²）", mr=17)


def dot_text(d):
    seq, v = d["path"], d["v"]
    sides = "、".join(seq[i] + seq[i + 1] for i in range(len(seq) - 1))
    return (f"右の図のような長方形ABCDがある。点Pは、{seq[0]}を出発して、辺{sides}上を、毎秒{v}cmの速さで{seq[-1]}まで動く。"
            f"点Pが{seq[0]}を出発してから {T('x')} 秒後の △{d['tri']} の面積を {T('y')} cm² とする。"
            f"点Pが頂点と重なるときは {T('y=0')} とする。")


def piece_of(d, x):
    for (lo, hi, a, b) in d["pieces"]:
        if lo <= x <= hi:
            return a * x + b
    raise ValueError


def dot_solutions(d):
    out = []
    for (lo, hi, a, b) in d["pieces"]:
        if a == 0:
            continue
        x = (d["yk"] - b) / a
        if lo <= x <= hi:
            out.append((x, a, b))
    return out


# ---------- ［3］グラフと面積 ----------
def graph_pattern(l, m, kind, win, mtext, q5, lab):
    """l, m=(傾き, 切片)。kind: 'X'＝A,B が x 軸上、'Y'＝A,B が y 軸上"""
    (al, bl), (am, bm) = l, m
    cx_ = (bm - bl) / (al - am)
    C = (cx_, al * cx_ + bl)
    if kind == "X":
        A, B = (-bl / al, F(0)), (-bm / am, F(0))
        base, height = abs(B[0] - A[0]), C[1]
    else:
        A, B = (F(0), bl), (F(0), bm)
        base, height = abs(A[1] - B[1]), C[0]
    S = base * height / 2
    d = dict(l=l, m=m, kind=kind, win=win, mtext=mtext, A=A, B=B, C=C, S=S, base=base, height=height, q5=q5, lab=lab)
    if q5 == "midAB":
        M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
        d["q5res"] = (M, line2(C, M))
    elif q5 == "midBC":
        M = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
        d["q5res"] = (M, line2(A, M))
    else:                                           # 'P'：y軸上の点 P（△PAB＝△ABC の2倍）
        d["q5res"] = (F(4) * S / base,)
    # 整数・読みとれる点であることの確認
    for p in (A, B, C):
        assert all(F(c).denominator == 1 for c in p), p
    return d


GR = [
    graph_pattern((F(1, 2), F(3)), (F(-1), F(6)), "X", dict(xr=(-8, 8), yr=(-1, 8)), None, "midAB",
                  dict(l=(3.6, 6.2, 1.2, 4.2, "start"), m=(-1.6, 7.6, -1.2, 0, "end"),
                       A=(-1.3, -2.8), B=(1.0, -2.8), C=(1.3, -1.0, "start"))),
    graph_pattern((F(2), F(4)), (F(-1), F(10)), "X", dict(xr=(-4, 12), yr=(-2, 10)),
                  "直線 m は、点B(10, 0) を通り、傾きが −1 の直線である。", "midBC",
                  dict(l=(-1.1, 1.8, -1.0, 0, "end"), m=(8.2, 1.8, 1.2, -1.0, "start"),
                       A=(-1.2, -2.6), B=(.4, -2.8), C=(1.3, -1.0, "start"))),
    graph_pattern((F(-2), F(10)), (F(1), F(4)), "Y", dict(xr=(-3, 9), yr=(-1, 11)), None, "midAB",
                  dict(l=(3.7, 2.6, 1.2, -.5, "start"), m=(6.8, 10.8, 1.2, 0, "start"),
                       A=(1.7, -1.6, "start"), B=(1.7, 3.2, "start"), C=(1.7, -1.6, "start"))),
    graph_pattern((F(1, 2), F(2)), (F(-2), F(12)), "X", dict(xr=(-6, 9), yr=(-1, 9)),
                  "直線 m は、点B(6, 0) を通り、傾きが −2 の直線である。", "P",
                  dict(l=(6.6, 5.3, 1.2, 0, "start"), m=(.9, 9.1, 1.2, -.3, "start"),
                       A=(-1.2, -2.6), B=(.4, -2.8), C=(1.3, -1.0, "start"))),
]


def g_plane(d):
    (xl, xh), (yl, yh) = d["win"]["xr"], d["win"]["yr"]
    cell = min(5.6, 68 / (xh - xl), 84 / (yh - yl))
    P = Plane((xl, xh), (yl, yh), cell, cell, (1, 2), (1, 2), cross=True)
    return P


def g_draw(d, P, answer=False):
    (al, bl), (am, bm) = d["l"], d["m"]
    P.line(al, bl, RED)
    P.line(am, bm, BLUE)
    it = 'font-family="KaTeX_Math" font-style="italic"'
    lx, ly, dx, dy, an = d["lab"]["l"]
    P.text(lx, ly, "ℓ", dx, dy, an, 4.4, f'{it} style="fill:{RED};font-weight:700"')
    lx, ly, dx, dy, an = d["lab"]["m"]
    P.text(lx, ly, "m", dx, dy, an, 4.4, f'{it} style="fill:{BLUE};font-weight:700"')
    for nm in "ABC":
        p = d[nm]
        P.dot(p[0], p[1])
        lb = d["lab"][nm]
        P.text(p[0], p[1], nm, lb[0], lb[1], lb[2] if len(lb) > 2 else "middle", 4.2)


def par(v):
    return f"({v})" if v < 0 else str(v)


def lattice_pts(a, b, win):
    """方眼の交点を通る点を2つ（y切片があればそれと、もう1つ）"""
    (xl, xh), (yl, yh) = win["xr"], win["yr"]
    ps = [(x, a * x + b) for x in range(xl, xh + 1) if (a * x + b).denominator == 1 and yl <= a * x + b <= yh]
    ps.sort(key=lambda p: abs(p[0]))
    return ps[:2] if ps[0][0] == 0 else ps[:2]


# ---------- 確かめ ----------
def check():
    x = sp.symbols("x")
    # 速さ
    for k in range(4):
        spd = speed_pattern(k)           # 組み立て中に assert で答えを確かめている
        assert len(spd["qs"]) == 4
    # 速さの交点を SymPy でも
    assert sp.solve(sp.Eq(60 * x, 120 * x - 600), x) == [10]
    assert sp.solve(sp.Eq(80 * x, -120 * x + 3000), x) == [15]
    assert sp.solve(sp.Eq(80 * x - 800, 240 * x - 4320), x) == [22]
    assert sp.solve(sp.Eq(-100 * x + 2800, 120 * x - 2040), x) == [22]
    # 動点（dot_pattern の中で幾何と照合済み）
    exp = {0: [(0, 3, 8, 0), (3, 7, 0, 24), (7, 10, -8, 80)], 1: [(0, 6, -2, 12), (6, 10, 3, -18)],
           2: [(0, 4, 6, 0), (4, 7, 0, 24), (7, 11, -6, 66)], 3: [(0, 6, 4, 0), (6, 14, -3, 42)]}
    for i, d in enumerate(DOT):
        assert [(lo, hi, int(a), int(b)) for lo, hi, a, b in d["pieces"]] == exp[i], i
        assert piece_of(d, d["x1"]) == [8 * 2, None, None, None][i] if i == 0 else True
        sol = dot_solutions(d)
        assert len(sol) == 2 and all(F(s[0]).denominator == 1 for s in sol), (i, sol)
    assert [int(s[0]) for s in dot_solutions(DOT[0])] == [1, 9]
    assert [int(s[0]) for s in dot_solutions(DOT[1])] == [3, 8]
    assert [int(s[0]) for s in dot_solutions(DOT[2])] == [2, 9]
    assert [int(s[0]) for s in dot_solutions(DOT[3])] == [3, 10]
    assert [piece_of(d, d["x1"]) for d in DOT] == [16, 8, 18, 8]
    # グラフと面積
    exp_g = [dict(C=(2, 4), S=24, q5=("0,0", (2, 0))), dict(C=(2, 8), S=48), dict(C=(2, 6), S=6), dict(C=(4, 4), S=20)]
    for d, e in zip(GR, exp_g):
        assert d["C"] == e["C"] and d["S"] == e["S"], (d["C"], d["S"])
        sol = sp.solve([sp.Symbol("y") - (sp.Rational(d["l"][0].numerator, d["l"][0].denominator) * x + sp.Rational(d["l"][1].numerator, d["l"][1].denominator))], sp.Symbol("y"))
    assert GR[0]["q5res"][1] == (2, 0) and GR[1]["q5res"][1] == (F(1, 2), 1)
    assert GR[2]["q5res"][1] == (F(-1, 2), 7) and GR[3]["q5res"] == (8,)
    # 2等分線は本当に面積を半分にする（頂点と対辺の中点を結ぶ）
    for d in GR[:3]:
        a, b = d["q5res"][1]
        assert a * (d["C"][0] if d["q5"] == "midAB" else d["A"][0]) + b == (d["C"][1] if d["q5"] == "midAB" else d["A"][1])
    print("確認OK：速さ・動点・グラフと面積の答え")


# ---------- ページ ----------
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; font-size: 8.8pt; }
.page { width: 210mm; height: 297mm; padding: 9mm 12mm 10mm; page-break-after: always;
        display: flex; flex-direction: column; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.katex { font-size: 1.1em; }
.head { display: flex; align-items: baseline; white-space: nowrap; border-bottom: 1pt solid #111; padding-bottom: 1.6mm; }
.head b { font-size: 12.5pt; }
.head .sub { font-size: 8.8pt; margin-left: 2mm; color: #222; }
.head .cl { font-size: 8.8pt; margin-left: 2.5mm; }
.head .u { display: inline-block; border-bottom: .7pt solid #111; }
.head .pts { margin-left: auto; font-size: 9pt; }
.head .kotae { margin-left: auto; font-weight: 700; color: #b4232c; font-size: 11pt; }
.cols { flex: 1; min-height: 0; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); margin-top: 2.5mm; }
.col { display: flex; flex-direction: column; min-height: 0; }
.col:first-child { padding-right: 4.5mm; border-right: .7pt solid #111; }
.col:last-child { padding-left: 4.5mm; }
.blk { flex: 1 1 0; min-height: 0; display: flex; flex-direction: column; }
.col:first-child .blk:first-child { flex: 0 0 auto; }
.col:first-child .blk:last-child { flex: 1 1 auto; }
.blk + .blk { margin-top: 2mm; padding-top: 2.2mm; border-top: .5pt dashed #777; }
.big { font-weight: 700; display: flex; align-items: center; gap: 1.6mm; white-space: nowrap; }
.big .box { display: inline-flex; width: 5mm; height: 5mm; border: .8pt solid #111; align-items: center;
            justify-content: center; font-size: 9.5pt; }
.big small { font-size: 8pt; font-weight: 400; }
.big .pill { font-size: 7pt; font-weight: 400; border: .7pt solid #111; border-radius: 3mm; padding: .1mm 1.6mm; margin-left: 1mm; }
.no { font-size: 7.6pt; flex: none; width: 6.5mm; padding-top: .7mm; text-align: center; }
.story { line-height: 1.52; margin-top: 1.6mm; }
.gw { display: flex; justify-content: center; margin-top: .6mm; }
.gr, .fig { flex: none; }
.gr text, .fig text { font-family: 'Noto Sans CJK JP'; }
.sq { flex: 1; min-height: 0; display: grid; margin-top: .8mm; }
.sq > .sqi:last-child { flex: 1 1 auto; }
.sq.auto { flex: none; }
.sqi { flex: none; display: flex; flex-direction: column; justify-content: space-between; padding-bottom: 1.2mm; }
.qt { display: flex; flex-wrap: wrap; line-height: 1.6; }
.qt > div { flex: 1 1 38mm; }
.ans.in { margin: 0 0 0 auto; align-self: flex-end; }
.ans { align-self: flex-end; white-space: nowrap; margin-top: 1mm; }
.ul { display: inline-block; border-bottom: .8pt solid #111; height: 4.6mm; vertical-align: baseline; }
.dtop { display: flex; gap: 2mm; align-items: flex-start; }
.dtop .story { flex: 1; }
.dtop .fig { margin-top: 2mm; }
.gtop .story { margin-top: 1.6mm; }
.gtop2 { margin-top: .6mm; }
/* こたえ */
.ansp { font-size: 8.7pt; line-height: 1.5; }
.ansp .katex { font-size: 1.06em; }
.res { font-weight: 700; color: #b4232c; display: block; }
.st { display: block; color: #333; }
.ar { display: flex; padding: .9mm 0; border-bottom: .4pt solid #ddd; }
.ar > div:last-child { min-width: 0; flex: 1; }
.agr { display: flex; justify-content: center; margin: 1mm 0 .5mm; }
"""


def head(i, ans=False):
    left = f"<b>中2数学 定期テスト対策 {NO[i]}</b><span class=sub>一次関数の利用</span>"
    if ans:
        return f"<div class=head>{left}<span class=kotae>こたえ</span></div>"
    return (f"<div class=head>{left}<span class=cl>（　）組（　）番　名前 <span class=u style='width:26mm'></span></span>"
            f"<span class=pts><span class=u style='width:9mm'></span>／60点</span></div>")


def big(n, text, small="", pill=""):
    return (f"<div class=big><span class=box>{n}</span>{text}"
            f"{f'<small>{small}</small>' if small else ''}{f'<span class=pill>{pill}</span>' if pill else ''}</div>")


def sqi(no, qhtml, ans="", extra="", mh=0, inline=False):
    """mh＝この小問の最低の高さ（mm。計算の場所）。inline＝答えの欄を問題文と同じ行（入らなければ次の行）に置く"""
    if inline:
        return (f"<div class=sqi style='min-height:{mh}mm'><div class=qt><span class=no>({no})</span><div>{qhtml}</div>"
                f"<span class='ans in'>{ans}</span></div>{extra}</div>")
    return (f"<div class=sqi style='min-height:{mh}mm'><div class=qt><span class=no>({no})</span><div>{qhtml}</div></div>{extra}"
            f"{f'<div class=ans>{ans}</div>' if ans else ''}</div>")


def block_speed(k):
    s = speed_pattern(k)
    P = s["plane"]()
    mh, il = (0, 13, 13, 0), (True, False, False, True)
    body = "".join(sqi(n + 1, q, a, mh=mh[n], inline=il[n]) for n, (q, a, _, _) in enumerate(s["qs"]))
    return (f"<div class=blk>{big(1, '次の問いに答えなさい。', '（×5点）', '※式や計算も書くこと')}"
            f"<div class=story>{s['story']}</div><div class=gw>{P.svg()}</div>"
            f"<div class='sq auto'>{body}</div></div>")


def rng(d, i):
    lo, hi, _, _ = d["pieces"][i]
    return T(f"{lo}\\leqq x\\leqq {hi}")


def block_dot(k):
    d = DOT[k]
    P = dot_plane(d)
    tri = d["tri"]
    qs = [
        sqi(1, f"{T(f'x={d['x1']}')} のときの {T('y')} の値を求めなさい。", f"答　{UL(14)}cm²", inline=True),
        sqi(2, f"{rng(d, d['asked'][0])} のとき、{T('y')} を {T('x')} の式で表しなさい。", f"答　{UL(28)}", mh=9, inline=True),
        sqi(3, f"{rng(d, d['asked'][1])} のとき、{T('y')} を {T('x')} の式で表しなさい。", f"答　{UL(28)}", mh=9, inline=True),
        sqi(4, f"△{tri} の面積が {d['yk']}cm² になるのは、点Pが出発してから何秒後ですか。すべて答えなさい。",
            f"答　{UL(12)}秒後、{UL(12)}秒後", mh=12),
        sqi(5, f"{T('x')} と {T('y')} の関係を表すグラフを、下の方眼にかきなさい。", "", f"<div class=gw>{P.svg()}</div>"),
    ]
    return (f"<div class=blk>{big(2, '次の問いに答えなさい。', '（×4点）', '※式や計算も書くこと')}"
            f"<div class=dtop><div class=story>{dot_text(d)}</div>{rect_fig(d)}</div>"
            f"<div class=sq style='display:flex;flex-direction:column'>{''.join(qs)}</div></div>")


def ell():
    return T("\\ell")


def block_graph(k):
    d = GR[k]
    P = g_plane(d)
    g_draw(d, P)
    kind = d["kind"]
    ax = "x軸" if kind == "X" else "y軸"
    story = (f"右の図のように、2直線 {ell()}、{T('m')} がある。{ell()} は{ax}と点Aで、{T('m')} は{ax}と点Bで交わり、"
             f"{ell()} と {T('m')} は点Cで交わっている。座標軸の1目盛りを1cmとする。")
    if d["mtext"]:
        story += d["mtext"].replace(" m ", f" {T('m')} ").replace("直線 m", f"直線 {T('m')}")
    q2 = f"直線 {T('m')} の式を求めなさい。"
    q5 = {"midAB": f"点Cを通り、△ABCの面積を2等分する直線の式を求めなさい。",
          "midBC": f"点Aを通り、△ABCの面積を2等分する直線の式を求めなさい。",
          "P": f"y軸上に点Pをとり、△PABの面積が△ABCの面積の2倍になるようにする。ただし、点Pの{T('y')}座標は正とする。点Pの座標を求めなさい。"}[d["q5"]]
    a5 = f"答　{UL(46)}" if d["q5"] != "P" else f"答　P{UL(30)}"
    qs = [
        sqi(1, f"直線 {ell()} の式を求めなさい。", f"答　{UL(46)}"),
        sqi(2, q2, f"答　{UL(46)}"),
        sqi(3, "点Cの座標を求めなさい。", f"答　C{UL(30)}"),
        sqi(4, "△ABCの面積を求めなさい。", f"答　{UL(16)}cm²"),
        sqi(5, q5, a5),
    ]
    return (f"<div class=blk>{big(3, '次の問いに答えなさい。', '（×4点）', '※式や計算も書くこと')}"
            f"<div class=story>{story}</div><div class=gw>{P.svg()}</div>"
            f"<div class=sq style='grid-template-rows:repeat(5,1fr)'>{''.join(qs)}</div></div>")


def page_q(i):
    return (f"<div class=page>{head(i)}<div class=cols>"
            f"<div class=col>{block_speed(i)}{block_dot(i)}</div><div class=col>{block_graph(i)}</div></div></div>")


# ---------- こたえ ----------
def ar(no, *rows, res=""):
    mid = "".join(f"<span class=st>{r}</span>" for r in rows)
    return f"<div class=ar><span class=no>({no})</span><div>{mid}<span class=res>{res}</span></div></div>"


def ans_speed(k):
    s = speed_pattern(k)
    rows = "".join(ar(n + 1, expl, res=res) for n, (_, _, expl, res) in enumerate(s["qs"]))
    return f"<div class=blk>{big(1, '速さ')}{rows}</div>"


def ans_dot(k):
    d = DOT[k]
    rows = ""
    x1 = d["x1"]
    ia = next(i for i, (lo, hi, _, _) in enumerate(d["pieces"]) if lo <= x1 <= hi)
    a, b = d["pieces"][ia][2:]
    rows += ar(1, d["reasons"][ia], f"{T(f'x={x1}')} を代入して {T(f'y={piece_of(d, x1)}')}", res=f"{piece_of(d, x1)}cm²")
    for n, idx in enumerate(d["asked"]):
        lo, hi, a, b = d["pieces"][idx]
        rows += ar(2 + n, f"{rng(d, idx)} のとき　" + d["reasons"][idx], res=f"{T(lin(a, b))}")
    sols = dot_solutions(d)
    exp = "　／　".join(f"{T(str(d['yk']) + '=' + lin(a, b)[2:])} より {T(f'x={fr(x)}')}" for x, a, b in sols)
    rows += ar(4, exp, res="、".join(f"{int(x)}秒後" for x, _, _ in sols))
    P = dot_plane(d)
    P.poly(list(zip(d["ts"], d["ys"])), RED, .6)
    vt = "，".join(f"({t},\\ {y})" for t, y in zip(d["ts"], d["ys"]))
    rows += ar(5, "点Pが頂点にくる時刻の点を直線で結ぶ。" + T(vt), res="下のグラフ") + f"<div class=agr>{P.svg()}</div>"
    return f"<div class=blk>{big(2, '動点')}{rows}</div>"


def ans_graph(k):
    d = GR[k]
    (al, bl), (am, bm) = d["l"], d["m"]
    A, B, C = d["A"], d["B"], d["C"]
    p1, p2 = lattice_pts(al, bl, d["win"])
    r = ar(1, f"グラフは 2点{pt_tex(p1)}、{pt_tex(p2)} を通る。傾き " +
           T(f"\\dfrac{{{p2[1]}-{par(p1[1])}}}{{{p2[0]}-{par(p1[0])}}}={fr(al)}") +
           f"、切片 {T(fr(bl))}", res=T(lin(al, bl)))
    if d["mtext"]:
        p0 = (int(B[0]), int(B[1]))
        r += ar(2, f"傾き {T(fr(am))} だから {T('y=' + fr(am) + 'x+b')} とおく。点B{pt_tex(p0)}を通るから "
                   f"{T('0=' + fr(am) + '\\times' + ('(' + str(p0[0]) + ')') + '+b')}、{T('b=' + fr(bm))}", res=T(lin(am, bm)))
    else:
        q1, q2 = lattice_pts(am, bm, d["win"])
        r += ar(2, f"グラフは 2点{pt_tex(q1)}、{pt_tex(q2)} を通る。傾き " +
                T(f"\\dfrac{{{q2[1]}-{par(q1[1])}}}{{{q2[0]}-{par(q1[0])}}}={fr(am)}") +
                f"、切片 {T(fr(bm))}", res=T(lin(am, bm)))
    r += ar(3, f"{T(lin(al, bl))}、{T(lin(am, bm))} を連立方程式として解く。{T(lin(al, bl)[2:] + '=' + lin(am, bm)[2:])}" + f" より {T('x=' + fr(C[0]))}、{T('y=' + fr(C[1]))}", res=f"C{pt_tex(C)}")
    if d["kind"] == "X":
        tx = f"A{pt_tex(A)}、B{pt_tex(B)} だから AB＝{int(d['base'])}cm、底辺をABとすると高さは点Cの {T('y')} 座標 {int(C[1])}cm。"
        r += ar(4, tx + T(f"\\dfrac{{1}}{{2}}\\times{int(d['base'])}\\times{int(C[1])}={int(d['S'])}"), res=f"{int(d['S'])}cm²")
    else:
        tx = f"A{pt_tex(A)}、B{pt_tex(B)} だから AB＝{int(d['base'])}cm、底辺をABとすると高さは点Cの {T('x')} 座標 {int(C[0])}cm。"
        r += ar(4, tx + T(f"\\dfrac{{1}}{{2}}\\times{int(d['base'])}\\times{int(C[0])}={int(d['S'])}"), res=f"{int(d['S'])}cm²")
    if d["q5"] == "P":
        pv = int(d["q5res"][0])
        r += ar(5, f"△ABC＝{int(d['S'])}cm² だから △PAB＝{int(2 * d['S'])}cm²。AB＝{int(d['base'])}cm なので、点Pの {T('y')} 座標を {T('p')} とすると "
                   + T(f"\\dfrac{{1}}{{2}}\\times{int(d['base'])}\\times p={int(2 * d['S'])}") + f"、{T(f'p={pv}')}", res=f"P(0, {pv})")
    else:
        M, (a5, b5) = d["q5res"]
        own, nm = (C, "C") if d["q5"] == "midAB" else (A, "A")
        seg_nm = "AB" if d["q5"] == "midAB" else "BC"
        r += ar(5, f"頂点{nm}と、向かい合う辺{seg_nm}の真ん中の点Mを通る直線が面積を2等分する。M{pt_tex(M)}。"
                   f"{nm}{pt_tex(own)}とMを通るから 傾き {T(fr(a5))}、" +
                f"{'切片 ' + T(fr(b5))}", res=T(lin(a5, b5)))
    return f"<div class=blk>{big(3, 'グラフと面積')}{r}</div>"


def page_a(i):
    return (f"<div class='page ansp'>{head(i, True)}<div class=cols>"
            f"<div class=col>{ans_speed(i)}{ans_dot(i)}</div><div class=col>{ans_graph(i)}</div></div></div>")


if __name__ == "__main__":
    check()
    write_pdfs([
        (doc(CSS, "".join(page_q(i) for i in range(4))), f"{FILE}.pdf"),
        (doc(CSS, "".join(page_a(i) for i in range(4))), f"{FILE}_ans.pdf"),
    ])
