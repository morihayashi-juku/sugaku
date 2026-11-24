"""高1 数学A 図形の性質 定期考査対策 第1回（学校の「2学期期末考査対策プリント＜後段＞」大問27〜35 の類題）。
A3 横・3列・2ページ（両面印刷で1枚）。問題 pdf/k1_zukei_teiki_1.pdf と、赤で答え・途中式を書きこんだ pdf/k1_zukei_teiki_1_ans.pdf。
  cd tools && python3 k1_zukei_teiki_1.py
図は座標から計算して描き、答えはその座標でも確かめる（check）。
［1］平行線と線分の比 ［2］内分・外分 ［3］［4］角の二等分線と比 ［5］外角の二等分線
［6］外心 ［7］内心 ［8］［9］重心
"""
import math, re
from fractions import Fraction as Fr
from pathlib import Path
from playwright.sync_api import sync_playwright
from texlib import tex, doc as texdoc

OUT = Path(__file__).resolve().parent.parent / "pdf"
NAME = "k1_zukei_teiki_1"
TITLE = "数学A 図形の性質　定期考査対策 第1回"

# ---------------- 幾何の道具 ----------------
def P(x, y): return (float(x), float(y))
def add(a, b): return (a[0]+b[0], a[1]+b[1])
def sub(a, b): return (a[0]-b[0], a[1]-b[1])
def mul(a, k): return (a[0]*k, a[1]*k)
def lerp(a, b, t): return (a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t)
def dist(a, b): return math.hypot(a[0]-b[0], a[1]-b[1])
def unit(v):
    l = math.hypot(*v); return (v[0]/l, v[1]/l)
def ang(v): return math.atan2(v[1], v[0])
def angle_at(V, A, B):
    a, b = unit(sub(A, V)), unit(sub(B, V))
    return math.degrees(math.acos(max(-1, min(1, a[0]*b[0]+a[1]*b[1]))))
def tri_sides(a, b, c):
    """BC=a, CA=b, AB=c。B=(0,0), C=(a,0)、A は上。"""
    x = (c*c + a*a - b*b) / (2*a); y = math.sqrt(c*c - x*x)
    return P(x, y), P(0, 0), P(a, 0)
def tri_angles(A, B):
    """角 A, B（度）の三角形。BC=1 で B=(0,0), C=(1,0)。"""
    C = 180 - A - B
    c = math.sin(math.radians(C)) / math.sin(math.radians(A))
    return P(c*math.cos(math.radians(B)), c*math.sin(math.radians(B))), P(0, 0), P(1, 0)
def circumcenter(A, B, C):
    ax, ay = A; bx, by = B; cx, cy = C
    d = 2*(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
    ux = ((ax*ax+ay*ay)*(by-cy) + (bx*bx+by*by)*(cy-ay) + (cx*cx+cy*cy)*(ay-by)) / d
    uy = ((ax*ax+ay*ay)*(cx-bx) + (bx*bx+by*by)*(ax-cx) + (cx*cx+cy*cy)*(bx-ax)) / d
    return P(ux, uy)
def incenter(A, B, C):
    a, b, c = dist(B, C), dist(C, A), dist(A, B); s = a+b+c
    return P((a*A[0]+b*B[0]+c*C[0])/s, (a*A[1]+b*B[1]+c*C[1])/s)

class Fig:
    """数学の座標（y が上）で描いて、SVG にする。"""
    def __init__(self, scale=40):
        self.s = scale; self.el = []; self.pts = []; self.ctr = None
    def X(self, p): self.pts.append(p); return f"{p[0]*self.s:.1f},{-p[1]*self.s:.1f}"
    def seg(self, a, b, w=1.6, dash=False, red=False):
        self.el.append(f'<line x1="{a[0]*self.s:.1f}" y1="{-a[1]*self.s:.1f}" x2="{b[0]*self.s:.1f}" y2="{-b[1]*self.s:.1f}" stroke="{"#d40000" if red else "#000"}" stroke-width="{w}"' + (' stroke-dasharray="4 3"' if dash else '') + '/>')
        self.pts += [a, b]
    def poly(self, *ps, w=1.8):
        if len(ps) == 3: self.ctr = (sum(p[0] for p in ps)/3, sum(p[1] for p in ps)/3)
        for i in range(len(ps)): self.seg(ps[i], ps[(i+1) % len(ps)], w)
    def text(self, p, s, size=15, it=False, red=False, anchor="middle"):
        self.pts.append(p)
        fam = "KaTeX_Math, 'Times New Roman', serif" if it else "KaTeX_Main, 'Times New Roman', serif"
        st = ' font-style="italic"' if it else ''
        self.el.append(f'<text x="{p[0]*self.s:.1f}" y="{-p[1]*self.s+size*0.35:.1f}" font-size="{size}" font-family="{fam}"{st} text-anchor="{anchor}" fill="{"#d40000" if red else "#000"}">{s}</text>')
    def name(self, p, s, d):
        """頂点の名前。d は外向きの向き（数学座標のベクトル）。"""
        u = unit(d); self.text(add(p, mul(u, 0.42*40/self.s)), s, 15)
    def val(self, s):  # 数字か x
        return (s, True) if s in ("x",) else (s, False)
    def _side(self, a, b, side):
        """三角形の図では、いつも外側（重心から遠い側）に置く。"""
        if self.ctr is None: return side
        m = lerp(a, b, .5); n = (-(b[1]-a[1]), b[0]-a[0])
        return 1 if n[0]*(m[0]-self.ctr[0]) + n[1]*(m[1]-self.ctr[1]) > 0 else -1
    def lab(self, a, b, s, side=1, off=0.32):
        """線分 ab の横に長さ。side=+1 は a→b の左。"""
        side = self._side(a, b, side)
        m = lerp(a, b, .5); n = unit((-(b[1]-a[1]), b[0]-a[0])); t, it = self.val(s)
        self.text(add(m, mul(n, side*off*40/self.s)), t, 15, it)
    def arc(self, a, b, s, side=1, bulge=0.35):
        """a から b までの長さを点線の弧で示す（教科書の形）。"""
        side = self._side(a, b, side)
        m = lerp(a, b, .5); n = unit((-(b[1]-a[1]), b[0]-a[0])); k = bulge*40/self.s
        c = add(m, mul(n, side*k*2))
        self.el.append(f'<path d="M{self.X(a)} Q{self.X(c)} {self.X(b)}" fill="none" stroke="#000" stroke-width="1" stroke-dasharray="3 3"/>')
        t, it = self.val(s)
        self.text(add(m, mul(n, side*(k+0.3*40/self.s))), t, 15, it)
    def par(self, a, b, t=0.55, n=1):
        """平行の矢印（a→b の向き）。"""
        u = unit(sub(b, a)); k = 0.16*40/self.s
        for i in range(n):
            c = lerp(a, b, t); c = add(c, mul(u, i*k*0.9))
            w1 = add(sub(c, mul(u, k)), mul((-u[1], u[0]), k*0.8)); w2 = add(sub(c, mul(u, k)), mul((u[1], -u[0]), k*0.8))
            self.el.append(f'<polyline points="{self.X(w1)} {self.X(c)} {self.X(w2)}" fill="none" stroke="#000" stroke-width="1.4"/>')
    def angmark(self, V, A, B, s=None, r=0.4, lr=None, double=False):
        """∠AVB の弧と（あれば）ラベル。"""
        r = r*40/self.s; a1, a2 = ang(sub(A, V)), ang(sub(B, V))
        d = (a2 - a1) % (2*math.pi)
        if d > math.pi: a1, a2 = a2, a1; d = 2*math.pi - d
        p1 = add(V, (r*math.cos(a1), r*math.sin(a1))); p2 = add(V, (r*math.cos(a2), r*math.sin(a2)))
        self.el.append(f'<path d="M{self.X(p1)} A{r*self.s:.1f},{r*self.s:.1f} 0 0 0 {self.X(p2)}" fill="none" stroke="#000" stroke-width="1"/>')
        if s is not None:
            m = a1 + d/2
            lr = r + (0.3 + min(0.55, 0.1/math.sin(d/2)))*40/self.s if lr is None else lr*40/self.s
            t, it = self.val(s)
            self.text(add(V, (lr*math.cos(m), lr*math.sin(m))), t, 13, it)
    def dots(self, V, A, B, r=0.42, n=1):
        """∠AVB を二等分する印（それぞれの半分に●）。B は二等分線上の点。"""
        r = r*40/self.s
        for X_ in (A, B):
            pass
    def bis_dots(self, V, A, D, B, r=0.5):
        """V から D への二等分線で分けた ∠AVD・∠DVB に ● を1つずつ。"""
        r = r*40/self.s
        for X1, X2 in ((A, D), (D, B)):
            a1, a2 = ang(sub(X1, V)), ang(sub(X2, V))
            d = (a2 - a1 + math.pi) % (2*math.pi) - math.pi; m = a1 + d/2
            c = add(V, (r*math.cos(m), r*math.sin(m))); self.pts.append(c)
            self.el.append(f'<circle cx="{c[0]*self.s:.1f}" cy="{-c[1]*self.s:.1f}" r="2.3" fill="#000"/>')
    def dot(self, p, red=False, r=2.6):
        self.pts.append(p); self.el.append(f'<circle cx="{p[0]*self.s:.1f}" cy="{-p[1]*self.s:.1f}" r="{r}" fill="{"#d40000" if red else "#000"}"/>')
    def svg(self, maxw=None, maxh=None):
        xs = [p[0]*self.s for p in self.pts]; ys = [-p[1]*self.s for p in self.pts]
        x0, x1, y0, y1 = min(xs)-12, max(xs)+12, min(ys)-14, max(ys)+10
        w, h = x1-x0, y1-y0
        st = []
        if maxw: st.append(f"max-width:{maxw}")
        if maxh: st.append(f"max-height:{maxh}")
        return (f'<svg viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}" style="width:{w*0.2646:.1f}mm;max-width:100%;height:auto" '
                f'xmlns="http://www.w3.org/2000/svg">' + "".join(self.el) + '</svg>')

CHK = []   # 図の座標で答えを確かめる
def ok(name, got, want, tol=1e-6):
    CHK.append(name); assert abs(got - want) < tol, (name, got, want)

# ---------------- 問題 ----------------
def q1():
    figs, sols = [], []
    # (1) AP=10, PB=x(=5), AQ=8, QC=4
    A, B, C = P(1.7, 3.9), P(0, 0), P(4.4, 0); t = 10/15
    Pp, Q = lerp(A, B, t), lerp(A, C, t)
    ok("1(1)", dist(A, Pp)/dist(Pp, B)*4, 8)  # AP:PB=AQ:QC → 10:5=8:4
    f = Fig(36); f.poly(A, B, C); f.seg(Pp, Q, 1.6); f.par(Pp, Q); f.par(B, C)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.6)); f.name(C, "C", (1, -.6)); f.name(Pp, "P", (-1, .3)); f.name(Q, "Q", (1, .3))
    f.arc(A, Pp, "10", 1, .25); f.arc(Pp, B, "x", 1, .22); f.arc(Q, A, "8", 1, .25); f.arc(C, Q, "4", 1, .22)
    figs.append(f.svg(maxh="44mm"))
    sols.append([r"$\mathrm{AP}:\mathrm{PB}=\mathrm{AQ}:\mathrm{QC}$", r"$10:x=8:4$", r"$8x=40$", r"$x=\boldsymbol{5}$"])
    # (2) AQ=6, QC=4, BC=15, PQ=x(=9)
    A, B, C = P(2.4, 4.6), P(0, 0), P(3.4, 0); t = .6
    Pp, Q = lerp(A, B, t), lerp(A, C, t)
    ok("1(2)", dist(Pp, Q)/dist(B, C)*15, 9)
    f = Fig(36); f.poly(A, B, C); f.seg(Pp, Q); f.par(Pp, Q); f.par(B, C)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.6)); f.name(C, "C", (1, -.6)); f.name(Pp, "P", (-1, .2)); f.name(Q, "Q", (1, .2))
    f.arc(A, Q, "6", -1, .22); f.arc(Q, C, "4", -1, .22); f.arc(C, B, "15", -1, .3); f.lab(Pp, Q, "x", -1, .3)
    figs.append(f.svg(maxh="44mm"))
    sols.append([r"$\mathrm{AQ}:\mathrm{AC}=\mathrm{PQ}:\mathrm{BC}$", r"$6:10=x:15$", r"$10x=90$", r"$x=\boldsymbol{9}$"])
    # (3) 交わる形：AQ=6, AC=4, BC=10, QP=x(=15)
    A = P(0, 0); B, C = P(-1.6, -1.0), P(1.6, -1.0); Q, Pp = mul(C, -1.5), mul(B, -1.5)
    ok("1(3)", dist(Q, Pp)/dist(B, C)*10, 15)
    f = Fig(36); f.seg(Q, C); f.seg(Pp, B); f.seg(Q, Pp); f.seg(B, C); f.par(Q, Pp); f.par(B, C)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.4)); f.name(C, "C", (1, -.4)); f.name(Q, "Q", (-1, .3)); f.name(Pp, "P", (1, .3))
    f.arc(Q, A, "6", -1, .25); f.arc(A, C, "4", -1, .2); f.arc(C, B, "10", 1, .3); f.arc(Pp, Q, "x", -1, .3)
    figs.append(f.svg(maxh="44mm"))
    sols.append([r"$\mathrm{AQ}:\mathrm{AC}=\mathrm{QP}:\mathrm{CB}$", r"$6:4=x:10$", r"$4x=60$", r"$x=\boldsymbol{15}$"])
    return figs, sols

def numberline(ans):
    """A を 0、B を 6 目もり。−5〜12。"""
    s = 22; x0 = -5; x1 = 12; W = (x1-x0)*s + 40; y = 30
    X = lambda v: 20 + (v-x0)*s
    el = [f'<line x1="{X(x0)-8}" y1="{y}" x2="{X(x1)+8}" y2="{y}" stroke="#000" stroke-width="1.5"/>']
    for v in range(x0, x1+1):
        el.append(f'<line x1="{X(v)}" y1="{y-6}" x2="{X(v)}" y2="{y+6}" stroke="#000" stroke-width="1.2"/>')
    for v, n in ((0, "A"), (6, "B")):
        el.append(f'<text x="{X(v)}" y="{y+24}" font-size="15" text-anchor="middle" font-family="KaTeX_Main, serif">{n}</text>')
    if ans:
        for v, n in ((2, "P"), (10, "Q"), (-3, "R")):
            el.append(f'<circle cx="{X(v)}" cy="{y}" r="4" fill="#d40000"/><text x="{X(v)}" y="{y-12}" font-size="15" text-anchor="middle" fill="#d40000" font-family="KaTeX_Main, serif">{n}</text>')
    return f'<svg viewBox="0 0 {W} 60" style="width:100%;height:auto" xmlns="http://www.w3.org/2000/svg">' + "".join(el) + '</svg>'

def q3():
    A, B, C = tri_sides(15, 12, 8)          # BC=15, CA=12, AB=8
    D = P(6, 0)
    ok("3 角の二等分", angle_at(A, B, D), angle_at(A, D, C))
    f = Fig(17); f.poly(A, B, C); f.seg(A, D); f.bis_dots(A, B, D, C, .6)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.name(D, "D", (0, -1))
    f.arc(B, A, "8", -1, .3); f.arc(A, C, "12", -1, .3); f.arc(C, B, "15", -1, .62); f.arc(B, D, "x", 1, .2)
    return f.svg(maxh="48mm"), [r"$\mathrm{BD}:\mathrm{DC}=\mathrm{AB}:\mathrm{AC}=8:12=2:3$", r"$x=15\times\dfrac{2}{5}=\boldsymbol{6}$"]

def q4():
    figs, sols = [], []
    # (1) AB=14, AC=8, BC=11, BD=x(=7), DC=4
    A, B, C = tri_sides(11, 8, 14); D = P(7, 0)
    ok("4(1)", angle_at(A, B, D), angle_at(A, D, C))
    f = Fig(13); f.poly(A, B, C); f.seg(A, D); f.bis_dots(A, B, D, C, .6)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.name(D, "D", (0, -1))
    f.arc(B, A, "14", -1, .3); f.arc(A, C, "8", -1, .3); f.arc(D, B, "x", -1, .3); f.arc(C, D, "4", -1, .3)
    figs.append(f.svg(maxh="40mm"))
    sols.append([r"$\mathrm{BD}:\mathrm{DC}=\mathrm{AB}:\mathrm{AC}$", r"$x:4=14:8$", r"$8x=56$", r"$x=\boldsymbol{7}$"])
    # (2) ∠B の二等分線、AB=9, BC=6, AC=10, AD=x(=6)
    A, B, C = tri_sides(6, 10, 9); D = lerp(A, C, 6/10)
    ok("4(2)", angle_at(B, A, D), angle_at(B, D, C))
    f = Fig(16); f.poly(A, B, C); f.seg(B, D); f.bis_dots(B, A, D, C, .6)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.name(D, "D", (1, .4))
    f.arc(B, A, "9", -1, .3); f.arc(A, C, "10", -1, .62); f.arc(C, B, "6", -1, .3); f.arc(A, D, "x", 1, .2)
    figs.append(f.svg(maxh="40mm"))
    sols.append([r"$\mathrm{AD}:\mathrm{DC}=\mathrm{BA}:\mathrm{BC}$", r"$=9:6=3:2$", r"$x=10\times\dfrac{3}{5}=\boldsymbol{6}$"])
    # (3) ∠C の二等分線、AB=12, AC=5, BC=10, BD=x(=8)
    A, B, C = tri_sides(10, 5, 12); D = lerp(B, A, 8/12)
    ok("4(3)", angle_at(C, B, D), angle_at(C, D, A))
    f = Fig(14); f.poly(A, B, C); f.seg(C, D); f.bis_dots(C, A, D, B, .6)
    f.name(A, "A", (.3, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.name(D, "D", (-.6, 1))
    f.arc(B, A, "12", -1, .62); f.arc(A, C, "5", -1, .3); f.arc(C, B, "10", -1, .3); f.arc(B, D, "x", 1, .2)
    figs.append(f.svg(maxh="40mm"))
    sols.append([r"$\mathrm{BD}:\mathrm{DA}=\mathrm{CB}:\mathrm{CA}$", r"$=10:5=2:1$", r"$x=12\times\dfrac{2}{3}=\boldsymbol{8}$"])
    return figs, sols

def q5():
    figs, sols = [], []
    # (1) AB=10, AC=6, BC=8, CD=x(=12)
    A, B, C = tri_sides(8, 6, 10); D = P(20, 0); E = add(A, mul(unit(sub(A, B)), 4))
    ok("5(1)", angle_at(A, E, D), angle_at(A, D, C))
    f = Fig(11); f.poly(A, B, C); f.seg(C, D); f.seg(A, D); f.seg(A, E, 1.2)
    f.bis_dots(A, E, D, C, .6)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (0, -1)); f.name(D, "D", (1, -.5))
    f.arc(B, A, "10", -1, .3); c0 = f.ctr; f.ctr = None; f.lab(A, C, "6", -1, .3); f.ctr = c0; f.arc(C, B, "8", -1, .3); f.arc(D, C, "x", -1, .3)
    figs.append(f.svg(maxh="34mm"))
    sols.append([r"$\mathrm{BD}:\mathrm{DC}=\mathrm{AB}:\mathrm{AC}=5:3$", r"$(8+x):x=5:3$", r"$5x=3(8+x)$", r"$2x=24$　$x=\boldsymbol{12}$"])
    # (2) AB=4, AC=7, BC=6, DB=x(=8)
    A, B, C = tri_sides(6, 7, 4); D = P(-8, 0); E = add(A, mul(unit(sub(A, C)), 2.5))
    ok("5(2)", angle_at(A, E, D), angle_at(A, D, B))
    f = Fig(11); f.poly(A, B, C); f.seg(D, B); f.seg(A, D); f.seg(A, E, 1.2)
    f.bis_dots(A, E, D, B, .6)
    f.name(A, "A", (0, 1)); f.name(B, "B", (0, -1)); f.name(C, "C", (1, -.5)); f.name(D, "D", (-1, -.5))
    c0 = f.ctr; f.ctr = None; f.lab(A, B, "4", 1, .3); f.ctr = c0; f.arc(A, C, "7", -1, .3); f.arc(C, B, "6", -1, .3); f.arc(B, D, "x", -1, .3)
    figs.append(f.svg(maxh="34mm"))
    sols.append([r"$\mathrm{DC}:\mathrm{DB}=\mathrm{AC}:\mathrm{AB}=7:4$", r"$(x+6):x=7:4$", r"$7x=4(x+6)$", r"$3x=24$　$x=\boldsymbol{8}$"])
    return figs, sols

def q6():
    figs, sols = [], []
    # (1) ∠OBC=25°, ∠OCA=40°, x=∠OAB(=25°)
    A, B, C = tri_angles(65, 50); O = circumcenter(A, B, C)
    ok("6(1) OBC", angle_at(B, O, C), 25); ok("6(1) OCA", angle_at(C, O, A), 40); ok("6(1) x", angle_at(A, B, O), 25)
    f = Fig(150); f.poly(A, B, C); f.seg(O, A, 1.2); f.seg(O, B, 1.2); f.seg(O, C, 1.2); f.dot(O, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.text(add(O, (0, -16/f.s)), "O", 14)
    f.angmark(B, O, C, "25°"); f.angmark(C, O, A, "40°"); f.angmark(A, B, O, "x")
    figs.append(f.svg(maxh="40mm"))
    sols.append([r"$\mathrm{OA}=\mathrm{OB}=\mathrm{OC}$ より", r"$\angle\mathrm{OBA}=x,\ \angle\mathrm{OCB}=25^\circ$", r"$\angle\mathrm{OAC}=40^\circ$", r"$2(x+25^\circ+40^\circ)=180^\circ$", r"$x=\boldsymbol{25^\circ}$"])
    # (2) ∠A=90°, O は BC の中点, ∠ABC=35°, x=∠OAC(=55°)
    A, B, C = tri_angles(90, 35); O = circumcenter(A, B, C)
    ok("6(2) O on BC", O[1], 0); ok("6(2) x", angle_at(A, O, C), 55)
    f = Fig(150); f.poly(A, B, C); f.seg(A, O, 1.2); f.dot(O, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.name(O, "O", (0, -1))
    f.angmark(B, C, A, "35°"); f.angmark(A, O, C, "x")
    figs.append(f.svg(maxh="40mm"))
    sols.append([r"O は斜辺 BC の中点で", r"$\mathrm{OA}=\mathrm{OB}$ より $\angle\mathrm{OAB}=35^\circ$", r"$\angle\mathrm{BAC}=90^\circ$ だから", r"$x=90^\circ-35^\circ=\boldsymbol{55^\circ}$"])
    # (3) O が外側。∠OBC=15°, ∠ACB=40°, x=∠ABC(=35°)
    A, B, C = tri_angles(105, 35); O = circumcenter(A, B, C)
    ok("6(3) O below", O[1] < 0, True); ok("6(3) OBC", angle_at(B, O, C), 15); ok("6(3) x", angle_at(B, A, C), 35)
    f = Fig(150); f.poly(A, B, C); f.seg(O, B, 1.2); f.seg(O, C, 1.2); f.dot(O, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, .2)); f.name(C, "C", (1, .2)); f.name(O, "O", (0, -1))
    f.angmark(B, C, A, "x"); f.angmark(B, O, C, "15°"); f.angmark(C, B, A, "40°")
    figs.append(f.svg(maxh="40mm"))
    sols.append([r"$\angle\mathrm{OCB}=15^\circ$", r"$\angle\mathrm{OAC}=\angle\mathrm{OCA}=55^\circ$", r"$\angle\mathrm{OAB}=\angle\mathrm{OBA}=x+15^\circ$", r"$x+40^\circ+(x+15^\circ)+55^\circ=180^\circ$", r"$x=\boldsymbol{35^\circ}$"])
    return figs, sols

def q7():
    figs, sols = [], []
    # (1) ∠IBC=32°, ∠ICB=28°, x=∠IAB(=30°)
    A, B, C = tri_angles(60, 64); I = incenter(A, B, C)
    ok("7(1)", angle_at(A, B, I), 30)
    f = Fig(150); f.poly(A, B, C); f.seg(I, A, 1.2); f.seg(I, B, 1.2); f.seg(I, C, 1.2); f.dot(I, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.text(add(I, (10/f.s, 12/f.s)), "I", 14)
    f.angmark(B, I, C, "32°"); f.angmark(C, B, I, "28°"); f.angmark(A, B, I, "x")
    figs.append(f.svg(maxh="40mm"))
    sols.append([r"$\angle\mathrm{IBA}=32^\circ,\ \angle\mathrm{ICA}=28^\circ$", r"$\angle\mathrm{IAC}=x$", r"$2(x+32^\circ+28^\circ)=180^\circ$", r"$x=\boldsymbol{30^\circ}$"])
    # (2) ∠BAC=50°, ∠IBC=40°, x=∠ICA(=25°)
    A, B, C = tri_angles(50, 80); I = incenter(A, B, C)
    ok("7(2)", angle_at(C, I, A), 25)
    f = Fig(150); f.poly(A, B, C); f.seg(I, B, 1.2); f.seg(I, C, 1.2); f.dot(I, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.text(add(I, (10/f.s, 12/f.s)), "I", 14)
    f.angmark(A, B, C, "50°"); f.angmark(B, I, C, "40°"); f.angmark(C, I, A, "x")
    figs.append(f.svg(maxh="40mm"))
    sols.append([r"$\angle\mathrm{B}=2\times 40^\circ=80^\circ$", r"$\angle\mathrm{C}=180^\circ-50^\circ-80^\circ=50^\circ$", r"$x=50^\circ\div 2=\boldsymbol{25^\circ}$"])
    # (3) ∠BIC=125°, x=∠BAC(=70°)
    A, B, C = tri_angles(70, 60); I = incenter(A, B, C)
    ok("7(3)", angle_at(I, B, C), 125)
    f = Fig(150); f.poly(A, B, C); f.seg(I, B, 1.2); f.seg(I, C, 1.2); f.dot(I, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.text(add(I, (10/f.s, 12/f.s)), "I", 14)
    f.angmark(I, C, B, "125°"); f.angmark(A, B, C, "x")
    figs.append(f.svg(maxh="40mm"))
    sols.append([r"$\angle\mathrm{IBC}+\angle\mathrm{ICB}$", r"$=180^\circ-125^\circ=55^\circ$", r"$\angle\mathrm{B}+\angle\mathrm{C}=110^\circ$", r"$x=180^\circ-110^\circ=\boldsymbol{70^\circ}$"])
    return figs, sols

def centroid_fig(bc_label=None, scale=30):
    A, B, C = P(2.1, 5), P(0, 0), P(6, 0); D = lerp(B, C, .5); G = lerp(A, D, 2/3)
    E = lerp(A, B, 2/3); F = lerp(A, C, 2/3)
    ok("8 EF//BC", E[1], G[1]); ok("8 EG:BD", dist(E, G)/dist(B, D), 2/3)
    f = Fig(scale); f.poly(A, B, C); f.seg(A, D, 1.3); f.seg(E, F, 1.3); f.par(E, F, .25); f.par(B, C, .25); f.dot(G, r=2)
    f.name(A, "A", (0, 1)); f.name(B, "B", (-1, -.5)); f.name(C, "C", (1, -.5)); f.name(D, "D", (0, -1))
    f.name(E, "E", (-1, .2)); f.name(F, "F", (1, .2)); f.text(add(G, (10/f.s, 12/f.s)), "G", 14)
    if bc_label: f.arc(C, B, bc_label, 1, .8)
    return f.svg()

# ---------------- 紙面 ----------------
CSS = r"""
@page{size:420mm 297mm;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:'Noto Sans CJK JP';font-size:12pt;line-height:1.45;color:#000;-webkit-print-color-adjust:exact}
.page{width:420mm;height:297mm;padding:9mm 12mm 7mm;display:flex;flex-direction:column;page-break-after:always;overflow:hidden}
.hd{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.6pt solid #000;padding-bottom:1.5mm}
.hd .t{font-size:15pt;font-weight:600;white-space:nowrap}.hd .n{font-size:12.5pt;white-space:nowrap}
.cols{flex:1;display:flex;min-height:0;margin-top:2.5mm}
.col{flex:1 1 0;min-width:0;display:flex;flex-direction:column;padding:0 4.5mm;border-left:.9pt solid #000}
.col:first-child{border-left:none;padding-left:0}.col:last-child{padding-right:0}
.foot{text-align:center;font-size:10pt;margin-top:1.5mm}
.blk{display:flex;flex-direction:column;flex:1 1 0;min-height:0;margin-bottom:2mm}
.q{display:flex;gap:1.8mm;align-items:flex-start;font-weight:500;margin-bottom:1.5mm}
.q .no{border:1.2pt solid #000;min-width:6.5mm;height:6.5mm;display:inline-flex;align-items:center;justify-content:center;font-size:11pt;flex:none;margin-top:.3mm}
.row{display:flex;gap:3mm;flex:1;min-height:0}
.cell{flex:1 1 0;min-width:0;display:flex;flex-direction:column}
.cell .sl{font-size:11pt;margin-bottom:.5mm}
.fig{display:flex;justify-content:center;align-items:flex-start}
.sol{color:#d40000;font-size:10.5pt;line-height:1.55;margin-top:1.5mm}.sol .katex{color:#d40000;font-size:1em}
.sol>div{margin-bottom:.3mm}
.ansl{margin-top:auto;align-self:flex-end;font-size:11.5pt;white-space:nowrap;padding-top:1mm}
.ansl .bx{display:inline-block;min-width:24mm;border-bottom:1pt solid #000;text-align:center;color:#d40000}
.sub{margin:0 0 1mm 2mm}
"""
ANS = False
def sol(lines):
    return ('<div class="sol">' + "".join(f"<div>{l}</div>" for l in lines) + '</div>') if ANS else ''
def ansline(v, pre="$x=$"):
    return f'<div class="ansl">{pre}<span class="bx">{v if ANS else ""}</span></div>'
def q(no, text): return f'<div class="q"><span class="no">{no}</span><span>{text}</span></div>'
def cells(figs, sols, finals, labels=True, grow=1):
    out = ""
    for i, (fg, sl, fn) in enumerate(zip(figs, sols, finals)):
        out += (f'<div class="cell">' + (f'<div class="sl">({i+1})</div>' if labels else '') + f'<div class="fig">{fg}</div>'
                + sol(sl) + ansline(fn) + '</div>')
    return f'<div class="row">{out}</div>'
def blk(inner, grow=1): return f'<div class="blk" style="flex-grow:{grow}">{inner}</div>'

def pages():
    f1, s1 = q1(); f3, s3 = q3(); f4, s4 = q4(); f5, s5 = q5(); f6, s6 = q6(); f7, s7 = q7()
    c1 = blk(q(1, '長さが図のように与えられていて，$\\mathrm{PQ}\\parallel\\mathrm{BC}$ のとき，$x$ を求めよ。')
             + cells(f1, s1, ["$5$", "$9$", "$15$"]))
    nl = (q(2, '線分 AB を $1:2$ に内分する点 P，線分 AB を $5:2$ に外分する点 Q，線分 AB を $1:3$ に外分する点 R を，それぞれ下の図にしるせ。')
          + f'<div style="margin:1mm 2mm 0">{numberline(ANS)}</div>'
          + sol([r"P：$\mathrm{AB}$ は 6 目もり。$\mathrm{AP}=6\times\dfrac{1}{3}=2$ 目もり",
                 r"Q：$\mathrm{AQ}:\mathrm{QB}=5:2$ → B の外側。$\mathrm{AQ}=6\times\dfrac{5}{3}=10$ 目もり",
                 r"R：$\mathrm{AR}:\mathrm{RB}=1:3$ → A の外側。$\mathrm{AR}=6\times\dfrac{1}{2}=3$ 目もり"]))
    c2 = blk(nl, .8) + blk(q(3, '右の図において，AD は $\\angle\\mathrm{A}$ の二等分線である。$x$ を求めよ。')
                         + f'<div class="row"><div class="cell"><div class="fig">{f3}</div>{sol(s3)}{ansline("$6$")}</div></div>', 1.2)
    c3 = blk(q(4, '下の図において，点 D は角の二等分線と辺の交点である。$x$ を求めよ。') + cells(f4, s4, ["$7$", "$6$", "$8$"]))
    d1 = (blk(q(5, '下の図において，AD は $\\triangle\\mathrm{ABC}$ の $\\angle\\mathrm{A}$ の外角の二等分線である。$x$ を求めよ。') + cells(f5, s5, ["$12$", "$8$"]))
          + blk(q(6, '下の図において，点 O は $\\triangle\\mathrm{ABC}$ の外心である。$x$ を求めよ。') + cells(f6, s6, ["$25^\\circ$", "$55^\\circ$", "$35^\\circ$"])))
    q8 = (q(8, '右の図において，点 G は $\\triangle\\mathrm{ABC}$ の重心であり，$\\mathrm{EF}\\parallel\\mathrm{BC}$ である。$\\mathrm{BC}=18$ のとき，次のものを求めよ。<br>(1) $\\mathrm{EG}:\\mathrm{BD}$　(2) 線分 EG の長さ　(3) 線分 EF の長さ')
          + f'<div class="row"><div class="cell"><div class="fig" style="justify-content:flex-end">{centroid_fig("18", 22)}</div>'
          + sol([r"(1) $\mathrm{AG}:\mathrm{GD}=2:1$，$\mathrm{EG}\parallel\mathrm{BD}$ より", r"$\mathrm{EG}:\mathrm{BD}=\mathrm{AG}:\mathrm{AD}=\boldsymbol{2:3}$",
                 r"(2) D は BC の中点で $\mathrm{BD}=9$", r"$\mathrm{EG}=9\times\dfrac{2}{3}=\boldsymbol{6}$",
                 r"(3) 同じように $\mathrm{GF}=\mathrm{DC}\times\dfrac{2}{3}=6$", r"$\mathrm{EF}=6+6=\boldsymbol{12}$"])
          + f'<div class="ansl">(1)<span class="bx">{"$2:3$" if ANS else ""}</span>　(2)<span class="bx">{"$6$" if ANS else ""}</span>　(3)<span class="bx">{"$12$" if ANS else ""}</span></div></div></div>')
    d2 = (blk(q(7, '下の図において，点 I は $\\triangle\\mathrm{ABC}$ の内心である。$x$ を求めよ。') + cells(f7, s7, ["$30^\\circ$", "$25^\\circ$", "$70^\\circ$"]))
          + blk(q8))
    q9 = (q(9, '右の図において，点 G は $\\triangle\\mathrm{ABC}$ の重心であり，$\\mathrm{EF}\\parallel\\mathrm{BC}$ である。$\\mathrm{AG}=8$，$\\mathrm{EG}=5$ のとき，線分 GD と線分 BC の長さを求めよ。')
          + f'<div class="row"><div class="cell"><div class="fig" style="justify-content:flex-end">{centroid_fig()}</div>'
          + sol([r"重心は中線を $2:1$ に分けるから", r"$\mathrm{GD}=8\div 2=\boldsymbol{4}$",
                 r"$\mathrm{EG}\parallel\mathrm{BD}$ より $\mathrm{EG}:\mathrm{BD}=\mathrm{AG}:\mathrm{AD}=2:3$", r"$\mathrm{BD}=5\times\dfrac{3}{2}=\dfrac{15}{2}$",
                 r"D は BC の中点だから $\mathrm{BC}=\dfrac{15}{2}\times 2=\boldsymbol{15}$"])
          + f'<div class="ansl">GD<span class="bx">{"$4$" if ANS else ""}</span>　BC<span class="bx">{"$15$" if ANS else ""}</span></div></div></div>')
    d3 = blk(q9)
    t = lambda n: f'{TITLE} &lt;No.{n}&gt;' + ('　<span style="color:#d40000">【解答】</span>' if ANS else '')
    nm = '1年(　　)組(　　)番　氏名(　　　　　　　　　　)'
    pg = lambda n, cs: (f'<div class="page"><div class="hd"><div class="t">{t(n)}</div><div class="n">{nm}</div></div>'
                        f'<div class="cols">' + "".join(f'<div class="col">{c}</div>' for c in cs) + f'</div><div class="foot">-{n}-</div></div>')
    return pg(1, [c1, c2, c3]) + pg(2, [d1, d2, d3])

def doc(body): return texdoc(CSS, re.sub(r"\$(.+?)\$", lambda m: tex(m.group(1)), body))

if __name__ == "__main__":
    bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page()
        for ANS, name in [(False, NAME), (True, NAME + "_ans")]:
            CHK.clear()
            pg.set_content(doc(pages())); pg.wait_for_timeout(400); pg.evaluate("document.fonts.ready")
            over = pg.evaluate("""()=>[...document.querySelectorAll('.col,.cell,.blk')].filter(e=>e.scrollHeight>e.clientHeight+1).map(e=>e.className+':'+e.textContent.slice(0,20))""")
            if over: bad += 1; print("!! はみ出し", name, over)
            pg.pdf(path=str(OUT / f"{name}.pdf"), prefer_css_page_size=True, print_background=True)
            print(name + ".pdf", "検算", len(CHK), "件OK")
        br.close()
    if bad: raise SystemExit("はみ出しあり")
