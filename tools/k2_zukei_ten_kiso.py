"""高2 数学Ⅱ 図形と方程式「点の座標」4ページ（11/6 金曜の授業）
① 象限・対称な点／② 2点間の距離／③ 内分点・外分点／④ 中点・重心の利用
問題（pdf/k2_zukei_ten_kiso.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
答えは Fraction で計算・assert で確認。実行：cd tools && python3 k2_zukei_ten_kiso.py
"""
from fractions import Fraction as F
import math, pathlib

# ---------- helpers ----------
def n(v):
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = "-" if v < 0 else ""
    return f"{s}\\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"

def p(v):  # with parentheses for negatives
    s = n(v)
    return f"({s})" if F(v) < 0 else s

def pt(name, x, y):
    return f"{name}({n(x)},\\,{n(y)})"

def sqrt_simplify(m):
    k = 1
    for i in range(int(math.isqrt(m)), 0, -1):
        if m % (i * i) == 0:
            k = i
            break
    r = m // (k * k)
    if r == 1:
        return str(k)
    return (f"{k}\\sqrt{{{r}}}" if k > 1 else f"\\sqrt{{{r}}}")

def quadrant(x, y):
    if x == 0 and y == 0:
        return "原点（どの象限にも属さない）"
    if x == 0:
        return "どの象限にも属さない（$y$軸上）"
    if y == 0:
        return "どの象限にも属さない（$x$軸上）"
    if x > 0 and y > 0: return "第1象限"
    if x < 0 and y > 0: return "第2象限"
    if x < 0 and y < 0: return "第3象限"
    return "第4象限"

def M(s):
    return f"${s}$"

def ans(s):
    return f'<span class="ans">{s}</span>'

def work(s):
    return f'<div class="work">{s}</div>'

# ---------- page 1 ----------
def page1():
    q1 = [(3, 5), (-2, 4), (-1, -6), (4, -3), (0, 3), (-5, 0)]
    items = "".join(
        f'<div class="it"><span class="no">({i+1})</span>{M(pt("", x, y))}　→　{ans(quadrant(x, y))}</div>'
        for i, (x, y) in enumerate(q1))
    # a>0, b<0
    a, b = 1, -1
    q2 = [("(a,\\,b)", (a, b)), ("(-a,\\,b)", (-a, b)), ("(a,\\,-b)", (a, -b)), ("(b,\\,a)", (b, a))]
    why = {"(a,\\,b)": "x>0,\\ y<0", "(-a,\\,b)": "x<0,\\ y<0", "(a,\\,-b)": "x>0,\\ y>0", "(b,\\,a)": "x<0,\\ y>0"}
    items2 = "".join(
        f'<div class="it"><span class="no">({i+1})</span>{M(lbl)}　→　{ans(quadrant(*v))}{work(M(why[lbl]))}</div>'
        for i, (lbl, v) in enumerate(q2))
    pts = [(4, 1), (-2, 5), (-3, -6), (0, 4)]
    rows = "".join(
        f"<tr><td>{M(pt('', x, y))}</td><td>{ans(M(pt('', x, -y)))}</td>"
        f"<td>{ans(M(pt('', -x, y)))}</td><td>{ans(M(pt('', -x, -y)))}</td></tr>"
        for (x, y) in pts)
    return f"""
<section class="page p1">
{header("①", "点の座標と象限・対称な点")}
<div class="box">
<div class="boxt">ポイント</div>
<div class="pointflex">
<div>
座標平面は $x$軸・$y$軸によって4つの部分に分けられる。これを<b>象限</b>という。<br>
<table class="qt"><tr><th>象限</th><th>第1</th><th>第2</th><th>第3</th><th>第4</th></tr>
<tr><td>$x$座標</td><td>＋</td><td>－</td><td>－</td><td>＋</td></tr>
<tr><td>$y$座標</td><td>＋</td><td>＋</td><td>－</td><td>－</td></tr></table>
※ 座標軸上の点は、どの象限にも属さない。<br>
<div style="margin-top:2mm">点 $(a,\\,b)$ と対称な点</div>
・$x$軸に関して対称 → $(a,\\,-b)$<br>
・$y$軸に関して対称 → $(-a,\\,b)$<br>
・原点に関して対称 → $(-a,\\,-b)$
</div>
<div>{grid_svg()}</div>
</div>
</div>

<h3><span class="sn">1</span>次の点は第何象限の点か答えよ。</h3>
<div class="grid2">{items}</div>

<h3><span class="sn">2</span>$a>0,\\ b<0$ のとき、次の点は第何象限の点か答えよ。</h3>
<div class="grid2">{items2}</div>

<h3><span class="sn">3</span>次の点と、$x$軸・$y$軸・原点に関して対称な点の座標をそれぞれ求めよ。</h3>
<table class="sym"><tr><th>点</th><th>$x$軸に関して対称</th><th>$y$軸に関して対称</th><th>原点に関して対称</th></tr>
{rows}</table>
</section>"""

def grid_svg():
    s = 17  # px per unit
    R = 5
    W = 2 * R * s + 40
    o = W / 2
    g = []
    for i in range(-R, R + 1):
        c = "#ddd" if i else "#000"
        g.append(f'<line x1="{o+i*s}" y1="{o-R*s}" x2="{o+i*s}" y2="{o+R*s}" stroke="{c}" stroke-width="{1.2 if i==0 else 0.6}"/>')
        g.append(f'<line x1="{o-R*s}" y1="{o+i*s}" x2="{o+R*s}" y2="{o+i*s}" stroke="{c}" stroke-width="{1.2 if i==0 else 0.6}"/>')
    g.append(f'<text x="{o+R*s+4}" y="{o+4}" class="ax">x</text>')
    g.append(f'<text x="{o-4}" y="{o-R*s-4}" class="ax">y</text>')
    g.append(f'<text x="{o-11}" y="{o+11}" class="sm">O</text>')
    for lab, (qx, qy) in {"第1象限": (3, 4.3), "第2象限": (-3, 4.3), "第3象限": (-3, -4.6), "第4象限": (3, -4.6)}.items():
        g.append(f'<text x="{o+qx*s}" y="{o-qy*s}" class="ql" text-anchor="middle">{lab}</text>')
    P = (3, 2)
    pts = [("P(a, b)", P, "#000"), ("(a, −b)", (3, -2), "#c00"), ("(−a, b)", (-3, 2), "#c00"), ("(−a, −b)", (-3, -2), "#c00")]
    g.append(f'<line x1="{o+3*s}" y1="{o-2*s}" x2="{o-3*s}" y2="{o+2*s}" stroke="#c00" stroke-dasharray="3,2"/>')
    g.append(f'<line x1="{o+3*s}" y1="{o-2*s}" x2="{o+3*s}" y2="{o+2*s}" stroke="#c00" stroke-dasharray="3,2"/>')
    g.append(f'<line x1="{o+3*s}" y1="{o-2*s}" x2="{o-3*s}" y2="{o-2*s}" stroke="#c00" stroke-dasharray="3,2"/>')
    for lab, (x, y), c in pts:
        g.append(f'<circle cx="{o+x*s}" cy="{o-y*s}" r="2.8" fill="{c}"/>')
        dx = 5 if x > 0 else -5
        anc = "start" if x > 0 else "end"
        dy = -5 if y > 0 else 13
        g.append(f'<text x="{o+x*s+dx}" y="{o-y*s+dy}" class="pl" text-anchor="{anc}" fill="{c}">{lab}</text>')
    return f'<svg width="{W}" height="{W}" viewBox="0 0 {W} {W}">{"".join(g)}</svg>'

# ---------- page 2 ----------
def dist_line(a, b):
    return abs(b - a)

def page2():
    q1 = [(3, 8), (-2, 5), (-7, -1), (4, -6)]
    it1 = "".join(
        f'<div class="it"><span class="no">({i+1})</span>$\\mathrm{{A}}({n(a)}),\\ \\mathrm{{B}}({n(b)})$　→　'
        f'{ans(M(f"\\mathrm{{AB}}={dist_line(a,b)}"))}{work(M(f"|{n(b)}-{p(a)}|={dist_line(a,b)}"))}</div>'
        for i, (a, b) in enumerate(q1))
    q2 = [((0, 0), (3, 4), "O"), ((1, 2), (4, 6), "A"), ((-2, 3), (4, -5), "A"), ((2, -1), (5, 1), "A"),
          ((-3, -4), (1, 0), "A"), ((0, 5), (-6, -3), "A"), ((2, 3), (-1, 3), "A"), ((-1, -2), (3, 4), "A")]
    it2 = []
    for i, ((x1, y1), (x2, y2), nm) in enumerate(q2):
        d2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
        n1 = "O" if nm == "O" else "A"
        n2 = "A" if nm == "O" else "B"
        lab = f"\\mathrm{{{n1}{n2}}}"
        prob = (f"$\\mathrm{{O}}(0,\\,0),\\ \\mathrm{{A}}({n(x2)},\\,{n(y2)})$" if nm == "O"
                else f"$\\mathrm{{A}}({n(x1)},\\,{n(y1)}),\\ \\mathrm{{B}}({n(x2)},\\,{n(y2)})$")
        dx, dy = x2 - x1, y2 - y1
        w = f"\\sqrt{{{p(dx)}^2+{p(dy)}^2}}=\\sqrt{{{d2}}}"
        res = sqrt_simplify(d2)
        if res != f"\\sqrt{{{d2}}}":
            w += f"={res}"
        it2.append(f'<div class="it"><span class="no">({i+1})</span>{prob}<br>{ans(M(f"{lab}={res}"))}{work(M(w))}</div>')
    it2 = "".join(it2)

    # 3: equidistant points  A(1,3), B(5,1)
    Ax, Ay, Bx, By = 1, 3, 5, 1
    # x-axis P(x,0): (x-Ax)^2+Ay^2=(x-Bx)^2+By^2 -> x = (Bx^2+By^2-Ax^2-Ay^2)/(2(Bx-Ax))
    px = F(Bx**2 + By**2 - Ax**2 - Ay**2, 2 * (Bx - Ax))
    qy = F(Bx**2 + By**2 - Ax**2 - Ay**2, 2 * (By - Ay))
    assert (px - Ax) ** 2 + Ay**2 == (px - Bx) ** 2 + By**2
    assert Ax**2 + (qy - Ay) ** 2 == Bx**2 + (qy - By) ** 2

    # 4: triangle shapes
    def tri(A, B, C):
        d = lambda P, Q: (P[0] - Q[0]) ** 2 + (P[1] - Q[1]) ** 2
        return d(A, B), d(B, C), d(C, A)
    t1 = tri((1, 1), (4, 2), (2, 4))
    t2 = tri((0, 0), (4, 1), (3, 5))
    assert t1 == (10, 8, 10) and t2 == (17, 17, 34)

    return f"""
<section class="page">
{header("②", "2点間の距離")}
<div class="box">
<div class="boxt">ポイント</div>
・数直線上の2点 $\\mathrm{{A}}(a),\\ \\mathrm{{B}}(b)$ 間の距離　$\\mathrm{{AB}}=|b-a|$<br>
・座標平面上の2点 $\\mathrm{{A}}(x_1,\\,y_1),\\ \\mathrm{{B}}(x_2,\\,y_2)$ 間の距離
　$\\mathrm{{AB}}=\\sqrt{{(x_2-x_1)^2+(y_2-y_1)^2}}$<br>
・とくに、原点 O と点 $\\mathrm{{A}}(x,\\,y)$ の距離は　$\\mathrm{{OA}}=\\sqrt{{x^2+y^2}}$
</div>

<h3><span class="sn">1</span>数直線上の次の2点間の距離を求めよ。</h3>
<div class="grid2">{it1}</div>

<h3><span class="sn">2</span>座標平面上の次の2点間の距離を求めよ。</h3>
<div class="grid2">{it2}</div>

<h3><span class="sn">3</span>2点 $\\mathrm{{A}}(1,\\,3),\\ \\mathrm{{B}}(5,\\,1)$ から等距離にある、次の点の座標を求めよ。</h3>
<div class="grid2">
<div class="it"><span class="no">(1)</span>$x$軸上の点 P<br>{ans(M(f"\\mathrm{{P}}({n(px)},\\,0)"))}
{work("P$(x,\\,0)$ とおくと $\\mathrm{AP}^2=\\mathrm{BP}^2$ より<br>$(x-1)^2+3^2=(x-5)^2+1^2$<br>$-2x+10=-10x+26$　$8x=16$　$x=2$")}</div>
<div class="it"><span class="no">(2)</span>$y$軸上の点 Q<br>{ans(M(f"\\mathrm{{Q}}(0,\\,{n(qy)})"))}
{work("Q$(0,\\,y)$ とおくと $\\mathrm{AQ}^2=\\mathrm{BQ}^2$ より<br>$1^2+(y-3)^2=5^2+(y-1)^2$<br>$-6y+10=-2y+26$　$-4y=16$　$y=-4$")}</div>
</div>

<h3><span class="sn">4</span>次の3点を頂点とする △ABC はどのような三角形か答えよ。</h3>
<div class="grid2">
<div class="it"><span class="no">(1)</span>$\\mathrm{{A}}(1,\\,1),\\ \\mathrm{{B}}(4,\\,2),\\ \\mathrm{{C}}(2,\\,4)$<br>{ans("AB＝AC の二等辺三角形")}
{work("$\\mathrm{AB}^2=3^2+1^2=10$<br>$\\mathrm{BC}^2=(-2)^2+2^2=8$<br>$\\mathrm{CA}^2=(-1)^2+(-3)^2=10$")}</div>
<div class="it"><span class="no">(2)</span>$\\mathrm{{A}}(0,\\,0),\\ \\mathrm{{B}}(4,\\,1),\\ \\mathrm{{C}}(3,\\,5)$<br>{ans("∠B＝90° の直角二等辺三角形")}
{work("$\\mathrm{AB}^2=4^2+1^2=17$<br>$\\mathrm{BC}^2=(-1)^2+4^2=17$<br>$\\mathrm{CA}^2=(-3)^2+(-5)^2=34$<br>AB＝BC かつ $\\mathrm{AB}^2+\\mathrm{BC}^2=\\mathrm{CA}^2$")}</div>
</div>
</section>"""

# ---------- page 3 ----------
def div1(a, b, m, k, ext):
    if ext:
        return F(-k * a + m * b, m - k)
    return F(k * a + m * b, m + k)

def page3():
    a, b = -2, 10
    q1 = [(1, 2, False), (3, 1, False), None, (3, 1, True), (1, 3, True), (5, 2, True)]
    it1 = []
    for i, q in enumerate(q1):
        if q is None:
            v = F(a + b, 2)
            it1.append(f'<div class="it"><span class="no">({i+1})</span>線分 AB の中点 M<br>{ans(M(f"\\mathrm{{M}}({n(v)})"))}'
                       f'{work(M(f"\\dfrac{{{n(a)}+{n(b)}}}{{2}}={n(v)}"))}</div>')
            continue
        m, k, ext = q
        v = div1(a, b, m, k, ext)
        if ext:
            w = f"\\dfrac{{-{k}\\cdot{p(a)}+{m}\\cdot{p(b)}}}{{{m}-{k}}}={n(v)}"
            name, kind = "Q", "外分"
        else:
            w = f"\\dfrac{{{k}\\cdot{p(a)}+{m}\\cdot{p(b)}}}{{{m}+{k}}}={n(v)}"
            name, kind = "P", "内分"
        it1.append(f'<div class="it"><span class="no">({i+1})</span>{m}:{k} に{kind}する点 {name}<br>{ans(M(f"\\mathrm{{{name}}}({n(v)})"))}{work(M(w))}</div>')
    it1 = "".join(it1)

    A, B = (-1, 4), (5, -2)
    q2 = [(2, 1, False), (1, 5, False), None, (3, 1, True), (1, 3, True), (3, 2, True)]
    it2 = []
    for i, q in enumerate(q2):
        if q is None:
            vx, vy = F(A[0] + B[0], 2), F(A[1] + B[1], 2)
            w = (f"x=\\dfrac{{{n(A[0])}+{n(B[0])}}}{{2}}={n(vx)},\\ "
                 f"y=\\dfrac{{{n(A[1])}+{p(B[1])}}}{{2}}={n(vy)}")
            it2.append(f'<div class="it"><span class="no">({i+1})</span>線分 AB の中点 M<br>{ans(M(pt("\\mathrm{M}", vx, vy)))}{work(M(w))}</div>')
            continue
        m, k, ext = q
        vx = div1(A[0], B[0], m, k, ext)
        vy = div1(A[1], B[1], m, k, ext)
        if ext:
            wx = f"\\dfrac{{-{k}\\cdot{p(A[0])}+{m}\\cdot{p(B[0])}}}{{{m}-{k}}}={n(vx)}"
            wy = f"\\dfrac{{-{k}\\cdot{p(A[1])}+{m}\\cdot{p(B[1])}}}{{{m}-{k}}}={n(vy)}"
            name, kind = "Q", "外分"
        else:
            wx = f"\\dfrac{{{k}\\cdot{p(A[0])}+{m}\\cdot{p(B[0])}}}{{{m}+{k}}}={n(vx)}"
            wy = f"\\dfrac{{{k}\\cdot{p(A[1])}+{m}\\cdot{p(B[1])}}}{{{m}+{k}}}={n(vy)}"
            name, kind = "P", "内分"
        it2.append(f'<div class="it"><span class="no">({i+1})</span>{m}:{k} に{kind}する点 {name}<br>{ans(M(pt(f"\\mathrm{{{name}}}", vx, vy)))}'
                   f'{work(M("x=" + wx) + "<br>" + M("y=" + wy))}</div>')
    it2 = "".join(it2)

    return f"""
<section class="page p3">
{header("③", "内分点・外分点")}
<div class="box">
<div class="boxt">ポイント</div>
2点 $\\mathrm{{A}}(x_1,\\,y_1),\\ \\mathrm{{B}}(x_2,\\,y_2)$ を結ぶ線分 AB を<br>
<div class="fl">
<div>・$m:n$ に<b>内分</b>する点　$\\left(\\dfrac{{nx_1+mx_2}}{{m+n}},\\ \\dfrac{{ny_1+my_2}}{{m+n}}\\right)$</div>
<div>・$m:n$ に<b>外分</b>する点　$\\left(\\dfrac{{-nx_1+mx_2}}{{m-n}},\\ \\dfrac{{-ny_1+my_2}}{{m-n}}\\right)$</div>
<div>・<b>中点</b>　$\\left(\\dfrac{{x_1+x_2}}{{2}},\\ \\dfrac{{y_1+y_2}}{{2}}\\right)$</div>
</div>
※ 数直線上の2点 $\\mathrm{{A}}(a),\\ \\mathrm{{B}}(b)$ では、$x$座標の式だけを使う。外分は「内分の式の $n$ を $-n$ にかえたもの」と覚えるとよい。
{division_svg()}
</div>

<h3><span class="sn">1</span>数直線上の2点 $\\mathrm{{A}}(-2),\\ \\mathrm{{B}}(10)$ について、線分 AB を次のように分ける点の座標を求めよ。</h3>
<div class="grid3">{it1}</div>

<h3><span class="sn">2</span>2点 $\\mathrm{{A}}(-1,\\,4),\\ \\mathrm{{B}}(5,\\,-2)$ について、線分 AB を次のように分ける点の座標を求めよ。</h3>
<div class="grid2">{it2}</div>
</section>"""

def division_svg():
    W, H = 600, 66
    g = ['<line x1="20" y1="30" x2="580" y2="30" stroke="#000" stroke-width="1"/>']
    def dot(x, lab, c="#000"):
        g.append(f'<circle cx="{x}" cy="30" r="3" fill="{c}"/>')
        g.append(f'<text x="{x}" y="20" text-anchor="middle" class="pl" fill="{c}">{lab}</text>')
    A, B = 60, 300
    P = A + (B - A) * 2 / 3
    Q = A + (B - A) * 3 / 2
    dot(A, "A"); dot(B, "B"); dot(P, "P（内分点）", "#c00"); dot(Q, "Q（外分点）", "#06c")
    def brace(x1, x2, y, lab, c):
        g.append(f'<path d="M{x1},{y-4} L{x1},{y} L{x2},{y} L{x2},{y-4}" fill="none" stroke="{c}" stroke-width="1"/>')
        g.append(f'<text x="{(x1+x2)/2}" y="{y+11}" text-anchor="middle" class="ax" fill="{c}">{lab}</text>')
    brace(A, P - 2, 40, "m", "#c00"); brace(P + 2, B, 40, "n", "#c00")
    g.append(f'<text x="{(A+B)/2}" y="64" text-anchor="middle" class="sm" fill="#c00">AP : PB ＝ m : n（P は線分 AB 上）</text>')
    g.append(f'<text x="{(B+Q)/2+30}" y="64" text-anchor="middle" class="sm" fill="#06c">AQ : QB ＝ m : n（Q は線分 AB の延長上）</text>')
    return f'<div style="text-align:center;margin-top:1mm"><svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(g)}</svg></div>'

# ---------- page 4 ----------
def page4():
    G = [((1, 4), (-3, 1), (5, -2)), ((2, -1), (6, 5), (-5, 2)), ((-4, 0), (0, 7), (1, -1))]
    itg = []
    for i, (A, B, C) in enumerate(G):
        gx, gy = F(A[0] + B[0] + C[0], 3), F(A[1] + B[1] + C[1], 3)
        w = (f"x=\\dfrac{{{n(A[0])}+{p(B[0])}+{p(C[0])}}}{{3}}={n(gx)},\\ "
             f"y=\\dfrac{{{n(A[1])}+{p(B[1])}+{p(C[1])}}}{{3}}={n(gy)}")
        itg.append(f'<div class="it"><span class="no">({i+1})</span>$\\mathrm{{A}}({n(A[0])},\\,{n(A[1])}),\\ \\mathrm{{B}}({n(B[0])},\\,{n(B[1])}),\\ \\mathrm{{C}}({n(C[0])},\\,{n(C[1])})$<br>'
                   f'{ans(M(pt("\\mathrm{G}", gx, gy)))}{work(M(w))}</div>')
    itg = "".join(itg)

    # 2 symmetric about a point
    S = [((2, 5), (4, 1)), ((-3, 2), (1, -1))]
    its = []
    for i, (A, P) in enumerate(S):
        Bx, By = 2 * P[0] - A[0], 2 * P[1] - A[1]
        assert F(A[0] + Bx, 2) == P[0] and F(A[1] + By, 2) == P[1]
        w = (f"\\mathrm{{B}}(x,\\,y)\\text{{ とおくと P は AB の中点}}<br>")
        its.append(f'<div class="it"><span class="no">({i+1})</span>点 $\\mathrm{{A}}({n(A[0])},\\,{n(A[1])})$ の、点 $\\mathrm{{P}}({n(P[0])},\\,{n(P[1])})$ に関して対称な点 B<br>'
                   f'{ans(M(pt("\\mathrm{B}", Bx, By)))}'
                   f'{work("B$(x,\\,y)$ とおくと、P は線分 AB の中点だから<br>" + M(f"\\dfrac{{{n(A[0])}+x}}{{2}}={n(P[0])},\\ \\dfrac{{{n(A[1])}+y}}{{2}}={n(P[1])}"))}</div>')
    its = "".join(its)

    # 3 midpoint given
    A, Mm = (1, 2), (3, -1)
    Bx, By = 2 * Mm[0] - A[0], 2 * Mm[1] - A[1]

    # 4 parallelogram
    PG = [((1, 1), (5, 2), (6, 5)), ((-2, 1), (3, -1), (4, 3))]
    itp = []
    for i, (A2, B2, C2) in enumerate(PG):
        Dx, Dy = A2[0] + C2[0] - B2[0], A2[1] + C2[1] - B2[1]
        mx, my = F(A2[0] + C2[0], 2), F(A2[1] + C2[1], 2)
        assert F(B2[0] + Dx, 2) == mx and F(B2[1] + Dy, 2) == my
        itp.append(f'<div class="it"><span class="no">({i+1})</span>$\\mathrm{{A}}({n(A2[0])},\\,{n(A2[1])}),\\ \\mathrm{{B}}({n(B2[0])},\\,{n(B2[1])}),\\ \\mathrm{{C}}({n(C2[0])},\\,{n(C2[1])})$<br>'
                   f'{ans(M(pt("\\mathrm{D}", Dx, Dy)))}'
                   f'{work("ACの中点 " + M(f"\\left({n(mx)},\\,{n(my)}\\right)") + " と BDの中点が一致する")}</div>')
    itp = "".join(itp)

    # 5 centroid given -> C
    A3, B3, G3 = (1, 4), (3, -2), (3, 1)
    Cx, Cy = 3 * G3[0] - A3[0] - B3[0], 3 * G3[1] - A3[1] - B3[1]
    assert F(A3[0] + B3[0] + Cx, 3) == G3[0] and F(A3[1] + B3[1] + Cy, 3) == G3[1]

    return f"""
<section class="page">
{header("④", "中点・重心の利用")}
<div class="box">
<div class="boxt">ポイント</div>
・3点 $\\mathrm{{A}}(x_1,\\,y_1),\\ \\mathrm{{B}}(x_2,\\,y_2),\\ \\mathrm{{C}}(x_3,\\,y_3)$ を頂点とする △ABC の<b>重心</b> G<br>　　$\\left(\\dfrac{{x_1+x_2+x_3}}{{3}},\\ \\dfrac{{y_1+y_2+y_3}}{{3}}\\right)$<br>
・点 P に関して点 A と対称な点 B → <b>P は線分 AB の中点</b><br>
・平行四辺形 ABCD → <b>対角線 AC と BD の中点が一致する</b>
</div>

<h3><span class="sn">1</span>次の3点を頂点とする △ABC の重心 G の座標を求めよ。</h3>
<div class="grid1">{itg}</div>

<h3><span class="sn">2</span>次の点の座標を求めよ。</h3>
<div class="grid2">{its}</div>

<h3><span class="sn">3</span>点 $\\mathrm{{A}}(1,\\,2)$ と点 B を結ぶ線分 AB の中点が $\\mathrm{{M}}(3,\\,-1)$ であるとき、点 B の座標を求めよ。</h3>
<div class="grid1"><div class="it">{ans(M(pt("\\mathrm{B}", Bx, By)))}
{work("B$(x,\\,y)$ とおくと　" + M("\\dfrac{1+x}{2}=3,\\ \\dfrac{2+y}{2}=-1") + "　より　" + M(f"x={Bx},\\ y={By}"))}</div></div>

<h3><span class="sn">4</span>次の3点 A, B, C に対して、四角形 ABCD が平行四辺形となるような点 D の座標を求めよ。</h3>
<div class="grid2">{itp}</div>

<h3><span class="sn">5</span>3点 $\\mathrm{{A}}(1,\\,4),\\ \\mathrm{{B}}(3,\\,-2)$, C を頂点とする △ABC の重心が $\\mathrm{{G}}(3,\\,1)$ のとき、点 C の座標を求めよ。</h3>
<div class="grid1"><div class="it">{ans(M(pt("\\mathrm{C}", Cx, Cy)))}
{work("C$(x,\\,y)$ とおくと　" + M("\\dfrac{1+3+x}{3}=3,\\ \\dfrac{4+(-2)+y}{3}=1") + "　より　" + M(f"x={Cx},\\ y={Cy}"))}</div></div>
</section>"""

def header(no, title):
    return f"""<div class="hd"><div class="ht"><span class="tag">数学Ⅱ　図形と方程式 {no}</span>{title}<span class="key">解答</span></div>
<div class="nm">　月　　日　名前（　　　　　　　　　）</div></div>"""

import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from texlib import _dist
KATEX = _dist()
OUT = pathlib.Path(__file__).resolve().parent.parent / "pdf"
html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="file://{KATEX}/katex.min.css">
<script src="file://{KATEX}/katex.min.js"></script>
<script src="file://{KATEX}/contrib/auto-render.min.js"></script>
<style>
@page {{ size: A4; margin: 0; }}
body {{ margin:0; font-family: "Noto Sans CJK JP", sans-serif; font-size: 10.5pt; color:#111; }}
.page {{ width:210mm; height:297mm; box-sizing:border-box; padding:11mm 13mm; page-break-after: always; overflow:hidden; }}
.hd {{ border-bottom: 2px solid #333; padding-bottom: 2mm; margin-bottom: 3mm; display:flex; justify-content:space-between; align-items:flex-end; }}
.ht {{ font-size: 15pt; font-weight: 700; white-space:nowrap; }}
.tag {{ display:inline-block; font-size:9pt; background:#333; color:#fff; padding:1px 7px; margin-right:6px; border-radius:3px; vertical-align:middle; }}
.key {{ display:inline-block; font-size:9pt; border:1.5px solid #c00; color:#c00; padding:0 6px; margin-left:8px; border-radius:3px; vertical-align:middle; }}
.nm {{ font-size: 10pt; white-space:nowrap; }}
.box {{ border: 1.3px solid #555; border-radius: 4px; padding: 2.5mm 4mm; margin-bottom: 3mm; background:#f7f7f7; line-height:1.75; }}
.boxt {{ font-weight:700; font-size:10pt; margin-bottom:1mm; }}
.pointflex {{ display:flex; justify-content:space-between; align-items:center; }}
.fl div {{ margin: 0.5mm 0 0.5mm 2mm; }}
h3 {{ font-size: 11pt; margin: 4mm 0 2mm; font-weight:700; }}
.sn {{ display:inline-block; width:6mm; height:6mm; line-height:6mm; text-align:center; background:#333; color:#fff; border-radius:3px; margin-right:2mm; font-size:10pt; }}
.grid1, .grid2, .grid3 {{ display:grid; gap: 2.5mm 6mm; margin-left: 3mm; }}
.grid2 {{ grid-template-columns: 1fr 1fr; }}
.grid3 {{ grid-template-columns: 1fr 1fr 1fr; }}
.it {{ line-height: 1.8; }}
.no {{ margin-right: 2mm; }}
.ans {{ color:#c00; font-weight:700; border-bottom: 1px solid #c00; padding: 0 2px; }}
.ans .katex {{ color:#c00; }}
.work {{ color:#c33; font-size: 8.8pt; line-height:1.7; margin: 0.5mm 0 0 4mm; }}
.work .katex {{ font-size: 1.0em; }}
.p3 .work {{ line-height: 2.5; }}
.p1 .grid2 {{ row-gap: 4mm; }}
table.qt {{ border-collapse: collapse; margin: 1mm 0; font-size:9.5pt; }}
table.qt td, table.qt th {{ border: 1px solid #777; padding: 0 3mm; text-align:center; background:#fff; }}
table.sym {{ border-collapse: collapse; width: 96%; margin-left:3mm; }}
table.sym td, table.sym th {{ border: 1px solid #777; padding: 3.2mm 2mm; text-align:center; }}
table.sym th {{ background:#eee; font-size:9.5pt; }}
svg text {{ font-family: "Noto Sans CJK JP", sans-serif; }}
.ax {{ font-style: italic; font-family: "KaTeX_Math", serif !important; font-size: 12px; }}
.sm {{ font-size: 10px; }}
.ql {{ font-size: 9px; fill:#666; }}
.pl {{ font-size: 10px; }}
.mondai .ans, .mondai .ans .katex {{ color: transparent !important; border-bottom-color:#333; }}
.mondai .work {{ visibility: hidden; }}
.mondai .ans {{ display:inline-block; width:38mm; height:1.3em; overflow:hidden; white-space:nowrap; vertical-align:bottom; }}
.mondai table.sym .ans {{ width:26mm; }}
.mondai .key {{ display:none; }}
</style></head><body class="__MODE__">
{page1()}{page2()}{page3()}{page4()}
<script>
renderMathInElement(document.body, {{delimiters:[{{left:"$", right:"$", display:false}}], throwOnError:true}});
document.body.setAttribute("data-done","1");
</script>
</body></html>"""

from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for mode, fname in [("mondai", "k2_zukei_ten_kiso.pdf"), ("kaitou", "k2_zukei_ten_kiso_ans.pdf")]:
        hp = pathlib.Path(f"/tmp/k2_zukei_{mode}.html")
        hp.write_text(html.replace("__MODE__", mode), encoding="utf-8")
        pg = br.new_page()
        pg.goto(f"file://{hp.resolve()}")
        pg.wait_for_selector("body[data-done]")
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(OUT / fname), format="A4", print_background=True, prefer_css_page_size=True)
        pg.close()
    br.close()
