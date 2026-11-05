"""中3 相似比と長さ（問題4ページ＋こたえ2ページ）

  cd tools && python3 c3_souji_nagasa.py

  その1＝相似比・比例式・向きが同じ相似　その2＝向きが違う・図なし・四角形
  その3＝重なった図形（相似な三角形を見つける）　その4＝利用（テストの形）
- 図は長さどおりに座標から描く。図に書く長さは座標と照らし合わせて確かめる（Fig.side）。
- 式は KaTeX（texlib）。文字式の文字は KaTeX の数式用イタリック。
- 出力：pdf/c3_souji_nagasa_A.pdf と c3_souji_nagasa_A_ans.pdf
"""
import math
from fractions import Fraction as Fr

from texlib import doc, tex as T, write_pdfs

FILE = "c3_souji_nagasa_A"
SUB = "相似比と長さ"


def S(name):
    return T(r"\mathrm{%s}" % name)


def seg(name, v, unit="cm"):
    return f"{T(r'\mathrm{%s}=%s' % (name, v))}{unit}"


def TR(name):
    return T(r"\triangle\mathrm{%s}" % name)


def SIM(a, b):
    return T(r"\triangle\mathrm{%s}\backsim\triangle\mathrm{%s}" % (a, b))


# ---------- 図 ----------
class Fig:
    """頂点は長さの単位（cm）で持ち、mm に直して SVG にする。y は上向き"""

    def __init__(self, pts, scale):
        self.p, self.s = {k: (float(x), float(y)) for k, (x, y) in pts.items()}, scale
        self.lines, self.sides, self.marks, self.dots = [], [], [], []
        self.vlabels = {}

    def poly(self, names, close=True):
        ns = list(names)
        for a, b in zip(ns, ns[1:] + (ns[:1] if close else [])):
            self.lines.append((a, b))
        return self

    def line(self, a, b, dash=False):
        self.lines.append((a, b, dash))
        return self

    def dist(self, a, b):
        (x1, y1), (x2, y2) = self.p[a], self.p[b]
        return math.hypot(x1 - x2, y1 - y2)

    def side(self, a, b, text, val=None, sign=1, off=3.1, unit="cm", at=None):
        """a–b の長さを図に書く。val があれば座標の長さと確かめる。sign=−1 で中心側へ"""
        if val is not None:
            assert abs(self.dist(a, b) - float(val)) < 1e-6, (a, b, val, self.dist(a, b))
        self.sides.append((a, b, str(text), sign, off, unit, at))
        return self

    def par(self, a, b, n=1):
        self.marks.append(("par", a, b, n))
        return self

    def right(self, a, v, b):
        self.marks.append(("right", a, v, b))
        return self

    def angle(self, a, v, b, n=1):
        self.marks.append(("ang", a, v, b, n))
        return self

    def label(self, **kw):
        """頂点の文字の位置を手で決める（mm の向き dx, dy）"""
        self.vlabels.update(kw)
        return self

    def svg(self, color=None):
        s = self.s
        xs = [q[0] for q in self.p.values()]
        ys = [q[1] for q in self.p.values()]
        pad = 10.5
        x0, y1 = min(xs) * s - pad, max(ys) * s + pad
        w, h = (max(xs) - min(xs)) * s + 2 * pad, (max(ys) - min(ys)) * s + 2 * pad
        X = lambda q: q[0] * s - x0
        Y = lambda q: y1 - q[1] * s
        cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
        o = [f'<svg class=fig width="{w:.1f}mm" height="{h:.1f}mm" viewBox="0 0 {w:.1f} {h:.1f}">']
        for ln in self.lines:
            a, b = ln[:2]
            dash = len(ln) > 2 and ln[2]
            o.append(f'<line x1="{X(self.p[a]):.2f}" y1="{Y(self.p[a]):.2f}" x2="{X(self.p[b]):.2f}" y2="{Y(self.p[b]):.2f}" '
                     f'stroke="#111" stroke-width=".35" stroke-linecap="round"{" stroke-dasharray=\"1.2 1\"" if dash else ""}/>')
        for mk in self.marks:
            if mk[0] == "par":
                _, a, b, n = mk
                ax, ay, bx, by = X(self.p[a]), Y(self.p[a]), X(self.p[b]), Y(self.p[b])
                L = math.hypot(bx - ax, by - ay)
                ux, uy = (bx - ax) / L, (by - ay) / L
                for i in range(n):
                    mx, my = (ax + bx) / 2 + ux * (i * 1.4 + 3.5), (ay + by) / 2 + uy * (i * 1.4 + 3.5)
                    o.append(f'<polyline points="{mx - ux * 1.2 - uy * .9:.2f},{my - uy * 1.2 + ux * .9:.2f} {mx:.2f},{my:.2f} '
                             f'{mx - ux * 1.2 + uy * .9:.2f},{my - uy * 1.2 - ux * .9:.2f}" fill="none" stroke="#111" stroke-width=".3"/>')
            elif mk[0] == "right":
                _, a, v, b = mk
                vx, vy = X(self.p[v]), Y(self.p[v])
                def u(t):
                    dx, dy = X(self.p[t]) - vx, Y(self.p[t]) - vy
                    L = math.hypot(dx, dy)
                    return dx / L * 2.2, dy / L * 2.2
                (ax, ay), (bx, by) = u(a), u(b)
                o.append(f'<polyline points="{vx + ax:.2f},{vy + ay:.2f} {vx + ax + bx:.2f},{vy + ay + by:.2f} {vx + bx:.2f},{vy + by:.2f}" '
                         f'fill="none" stroke="#111" stroke-width=".25"/>')
            else:
                _, a, v, b, n = mk
                vx, vy = X(self.p[v]), Y(self.p[v])
                t1 = math.atan2(Y(self.p[a]) - vy, X(self.p[a]) - vx)
                t2 = math.atan2(Y(self.p[b]) - vy, X(self.p[b]) - vx)
                d = (t2 - t1 + math.pi) % (2 * math.pi) - math.pi
                for i in range(n):
                    r = 3.6 + i * .8
                    o.append(f'<path d="M{vx + r * math.cos(t1):.2f},{vy + r * math.sin(t1):.2f} '
                             f'A{r},{r} 0 0 {1 if d > 0 else 0} {vx + r * math.cos(t2):.2f},{vy + r * math.sin(t2):.2f}" '
                             f'fill="none" stroke="#111" stroke-width=".25"/>')
        # 頂点の文字
        for k, q in self.p.items():
            if k in self.vlabels:
                dx, dy = self.vlabels[k]
            else:
                dx, dy = q[0] - cx, -(q[1] - cy)
                L = math.hypot(dx, dy) or 1
                dx, dy = dx / L * 3.4, dy / L * 3.4
            o.append(f'<text x="{X(q) + dx:.2f}" y="{Y(q) + dy + 1.2:.2f}" text-anchor="middle" font-size="3.8" '
                     f'font-family="KaTeX_Main">{k}</text>')
        # 長さ
        for a, b, text, sign, off, unit, at in self.sides:
            ax, ay, bx, by = X(self.p[a]), Y(self.p[a]), X(self.p[b]), Y(self.p[b])
            mx, my = (ax + bx) / 2, (ay + by) / 2
            nx, ny = -(by - ay), bx - ax
            L = math.hypot(nx, ny)
            nx, ny = nx / L, ny / L
            if (mx + nx - (cx * s - x0)) ** 2 + (my + ny - (y1 - cy * s)) ** 2 < (mx - (cx * s - x0)) ** 2 + (my - (y1 - cy * s)) ** 2:
                nx, ny = -nx, -ny
            hw = (len(text) + len(unit) + (.3 if text in ("x", "y") else 0)) * .95    # 文字の幅の半分くらい
            d = off + abs(nx) * hw
            tx, ty = mx + nx * d * sign, my + ny * d * sign + 1.1
            if at:
                tx, ty = mx + at[0], my + at[1] + 1.1
            if text in ("x", "y"):
                body = f'<tspan font-family="KaTeX_Math" font-style="italic">{text}</tspan>'
            else:
                body = text
            o.append(f'<text x="{tx:.2f}" y="{ty:.2f}" text-anchor="middle" font-size="3.4" font-family="KaTeX_Main" '
                     f'stroke="#fff" stroke-width=".8" paint-order="stroke">{body}<tspan dx=".35">{unit}</tspan></text>')
        o.append("</svg>")
        return "".join(o)


def tri(ab, bc, ca, names="ABC", flip=False, rot=0, scale=1.0):
    """AB, BC, CA の長さの三角形（B が左下、C が右下）。flip で左右反転、rot（度）で回転"""
    assert ab + bc > ca and bc + ca > ab and ca + ab > bc, (ab, bc, ca)
    ax = (ab**2 + bc**2 - ca**2) / (2 * bc)
    ay = math.sqrt(ab**2 - ax**2)
    a, b, c = names
    pts = {a: (ax, ay), b: (0.0, 0.0), c: (float(bc), 0.0)}
    out = {}
    t = math.radians(rot)
    for k, (x, y) in pts.items():
        if flip:
            x = -x
        out[k] = (x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t))
    return out


def sim_pair(abc, k, show1, show2, scale=2.6, flip=False, rot=0, names=("ABC", "DEF")):
    """相似な2つの三角形の図。show は {('A','B'): 文字 or None}（None は長さをそのまま）"""
    ab, bc, ca = abc
    n1, n2 = names
    f1 = Fig(tri(ab, bc, ca, n1), scale).poly(n1)
    f2 = Fig(tri(ab * k, bc * k, ca * k, n2, flip=flip, rot=rot), scale).poly(n2)
    for fig, nm, show, m in ((f1, n1, show1, 1), (f2, n2, show2, k)):
        lens = {(nm[0], nm[1]): ab * m, (nm[1], nm[2]): bc * m, (nm[2], nm[0]): ca * m}
        for (p, q), lab in show.items():
            v = lens[(p, q)]
            assert float(v).is_integer(), (p, q, v)
            fig.side(p, q, lab if lab else int(v), v)
    return f1.svg() + f2.svg()


# ---------- 部品 ----------
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; font-size: 10.5pt; }
.page { width: 210mm; height: 297mm; padding: 10mm 13mm 10mm; page-break-after: always;
        display: flex; flex-direction: column; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.katex { font-size: 1.1em; }
.head { display: flex; align-items: baseline; white-space: nowrap; border-bottom: 1.2pt solid #111; padding-bottom: 1.5mm; flex: none; }
.head b { font-size: 14pt; }
.head .sub { font-size: 10pt; margin-left: 3mm; }
.head .nm { margin-left: auto; font-size: 9.5pt; }
.head .u { display: inline-block; border-bottom: .7pt solid #111; width: 42mm; }
.head .kotae { margin-left: auto; font-weight: 700; color: #b4232c; font-size: 12pt; }
.big { font-weight: 700; margin-top: 3mm; display: flex; align-items: center; gap: 1.8mm; flex: none; }
.big .box { display: inline-flex; width: 5.4mm; height: 5.4mm; border: .9pt solid #111; align-items: center; justify-content: center; }
.big span.t { line-height: 1.45; }
.tip { flex: none; margin-top: 2.5mm; border: .8pt solid #666; border-radius: 1.5mm; padding: 1.8mm 3mm; font-size: 9.8pt; line-height: 1.7; background: #f6f6f6; }
.no { flex: none; width: 7mm; font-size: 9pt; padding-top: .6mm; }
.row2 { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); column-gap: 5mm; flex: 1; min-height: 0; margin-top: 1.5mm; }
.row1 { flex: 1; min-height: 0; margin-top: 1.5mm; display: flex; flex-direction: column; }
.q { display: flex; flex-direction: column; min-height: 0; }
.q .tx { display: flex; line-height: 1.6; }
.figs { display: flex; justify-content: center; align-items: flex-end; gap: 6mm; margin-top: .5mm; flex: none; }
.space { flex: 1; min-height: 3mm; }
.ansl { text-align: right; white-space: nowrap; margin-bottom: 1mm; }
.ansl .u { display: inline-block; border-bottom: .8pt solid #111; width: 25mm; margin-left: 1mm; }
.sim { white-space: nowrap; margin: .8mm 0 0 7mm; font-size: 10pt; }
.sim .u { display: inline-block; border-bottom: .7pt solid #111; width: 17mm; height: 4mm; }
.sub3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: 3mm; margin-top: 1mm; flex: 1; min-height: 0; }
.sub3 > div { display: flex; flex-direction: column; min-height: 25mm; line-height: 1.5; }
.fourq { display: grid; grid-template-columns: repeat(4, 1fr); flex: none; height: 25mm; margin-top: 1.5mm; }
.fourq > div { display: flex; }
.fig text { fill: #111; }
/* こたえ */
.ansp { font-size: 9.6pt; line-height: 1.6; }
.acols { columns: 2; column-gap: 7mm; flex: 1; min-height: 0; margin-top: 1mm; column-fill: auto; }
.ah { font-weight: 700; margin-top: 2.5mm; break-after: avoid; border-left: 1.2mm solid #333; padding-left: 1.5mm; }
.ar { display: flex; padding: .7mm 0; border-bottom: .4pt solid #ddd; break-inside: avoid; }
.ar .no { padding-top: .2mm; font-size: 8.8pt; }
.ar .st { display: block; color: #333; }
.res { font-weight: 700; color: #b4232c; }
"""


def head(no, ans=None):
    left = f"<b>中3数学 {SUB}</b><span class=sub>{'その' + str(no) if no else ''}</span>"
    if ans:
        return f"<div class=head>{left}<span class=kotae>こたえ（{ans}）</span></div>"
    return f"<div class=head>{left}<span class=nm>名前 <span class=u></span></span></div>"


def big(n, text):
    return f"<div class=big><span class=box>{n}</span><span class=t>{text}</span></div>"


def ansl(*labels):
    return "<div class=ansl>" + "　".join(f"{l}<span class=u></span>" for l in labels) + "</div>"


X_, Y_ = T("x"), T("y")
BLANK_SIM = "相似な三角形：△<span class=u></span>∽△<span class=u></span>"


def sim3(a, b, c):
    def one(i, t, unit=""):
        return f"<div><span>({i}) {t}</span><div class=space></div>{ansl(unit)}</div>"
    return f"<div class=sub3>{one(1, f'相似比（{TR(a)}：{TR(b)}）を求めなさい。', '')}{one(2, f'{X_} の値を求めなさい。', X_ + '＝')}{one(3, f'{Y_} の値を求めなさい。', Y_ + '＝')}</div>"


# ---------- その1〜その4 ----------
def page1():
    pq = [("x:6=2:3", 4), ("4:x=2:5", 10), ("3:4=x:20", 15), ("5:8=15:x", 24)]
    four = "".join(f"<div><span class=no>({i + 1})</span>{T(q)}</div>" for i, (q, _) in enumerate(pq))
    p1 = sim_pair((6, 8, 4), Fr(3, 2), {("A", "B"): None, ("B", "C"): None, ("C", "A"): "y"},
                  {("D", "E"): None, ("E", "F"): "x", ("F", "D"): None}, scale=3.5)
    p2 = sim_pair((8, 12, 16), Fr(3, 4), {("A", "B"): None, ("B", "C"): None, ("C", "A"): "y"},
                  {("D", "E"): None, ("E", "F"): "x", ("F", "D"): None}, scale=2.7)
    return f"""<div class=page>{head(1)}
<div class=tip><b>相似比</b>＝対応する辺の長さの比（いちばん簡単な整数の比にする）。相似な図形では、<b>対応する辺の比はどこも相似比と同じ</b>。<br>
<b>比例式の解き方</b>　{T('a:b=c:d')} ならば {T('ad=bc')}（外側どうしの積＝内側どうしの積）</div>
{big(1, f"次の式を満たす {X_} の値を求めなさい。")}
<div class=fourq>{four}</div>
{big(2, f"次の図で {SIM('ABC', 'DEF')} のとき，次の問いに答えなさい。（長さの単位は cm）")}
<div class=row1><div class=figs>{p1}</div>{sim3('ABC', 'DEF', '')}</div>
{big(3, f"次の図で {SIM('ABC', 'DEF')} のとき，次の問いに答えなさい。（長さの単位は cm）")}
<div class=row1><div class=figs>{p2}</div>{sim3('ABC', 'DEF', '')}</div>
</div>"""


def quad():
    # 右の辺・左の辺が平行な台形（18, 12, 9, 15 と 12, 8, 6, 10）
    def q(names, m):
        a, b, c, d = names
        return Fig({a: (0, 18 * m), b: (0, 0), c: (12 * m, 0), d: (12 * m, 9 * m)}, 2.15).poly(names)
    f1 = q("ABCD", 1).side("A", "B", 18, 18).side("B", "C", 12, 12).side("D", "A", 15, 15).side("C", "D", "y", 9)
    f2 = q("EFGH", Fr(2, 3)).side("E", "F", 12, 12).side("F", "G", "x", 8).side("G", "H", 6, 6).side("H", "E", 10, 10)
    return f1.svg() + f2.svg()


def page2():
    p1 = sim_pair((10, 14, 12), Fr(3, 2), {("A", "B"): None, ("B", "C"): None, ("C", "A"): "y"},
                  {("D", "E"): None, ("E", "F"): "x", ("F", "D"): None}, scale=1.6, flip=True)
    p2 = sim_pair((9, 12, 6), Fr(5, 3), {("A", "B"): None, ("B", "C"): None, ("C", "A"): "y"},
                  {("D", "E"): None, ("E", "F"): "x", ("F", "D"): None}, scale=1.5, rot=125)
    def two(no, figs):
        return (f"<div class=q><div class=tx><span class=no>({no})</span><div>{SIM('ABC', 'DEF')}</div></div>"
                f"<div class=figs style='gap:2mm'>{figs}</div><div class=space></div>{ansl(X_ + '＝', Y_ + '＝')}</div>")
    qs = [
        (f"{SIM('ABC', 'PQR')}，{seg('AB', 6)}，{seg('PQ', 9)}，{seg('BC', 8)} のとき，{S('QR')} の長さ"),
        (f"{SIM('ABC', 'DEF')}，{seg('BC', 12)}，{seg('EF', 8)}，{seg('AC', 15)} のとき，{S('DF')} の長さ"),
        (f"{SIM('ABC', 'FED')}，{seg('AB', 10)}，{seg('FE', 6)}，{seg('AC', 15)} のとき，{S('FD')} の長さ"),
        (f"{SIM('ABC', 'DEF')}，{seg('AB', 6)}，{seg('DE', 4)}，{seg('CA', 5)} のとき，{S('FD')} の長さ（分数で）"),
    ]
    qh = "".join(f"<div class=q><div class=tx><span class=no>({i + 1})</span><div>{t}</div></div><div class=space></div>{ansl('')}</div>"
                 for i, t in enumerate(qs))
    return f"""<div class=page>{head(2)}
{big(1, f"向きがちがっても，<b>対応する頂点の順</b>に注意して，{X_}，{Y_} の値を求めなさい。（単位は cm）")}
<div class=row2 style="flex:0 0 74mm">{two(1, p1)}{two(2, p2)}</div>
{big(2, "図をかかずに，<b>△の文字の順</b>から対応する辺を見つけて求めなさい。")}
<div class=row2 style="grid-template-rows:1fr 1fr">{qh}</div>
{big(3, f"四角形 {S('ABCD')} ∽ 四角形 {S('EFGH')} のとき，{X_}，{Y_} の値を求めなさい。（単位は cm）")}
<div class=row1 style="flex:0 0 66mm"><div class=figs>{quad()}</div><div class=space></div>{ansl(X_ + '＝', Y_ + '＝')}</div>
</div>"""


def figs3():
    # (1) DE∥BC  AD=6 DB=3 DE=8 BC=12
    t = tri(9, 12, 10)
    A, B, C = t["A"], t["B"], t["C"]
    pts = {"A": A, "B": B, "C": C, "D": (A[0] + (B[0] - A[0]) * 2 / 3, A[1] + (B[1] - A[1]) * 2 / 3),
           "E": (A[0] + (C[0] - A[0]) * 2 / 3, A[1] + (C[1] - A[1]) * 2 / 3)}
    f1 = Fig(pts, 3.3).poly("ABC").line("D", "E").par("D", "E").par("B", "C")
    f1.label(D=(-3.6, -1.8)).side("A", "D", 6, 6).side("D", "B", 3, 3, at=(-8, -.3)).side("D", "E", 8, 8, at=(0, -2.2)).side("B", "C", "x", 12)
    # (2) DE∥BC  AD=4 DB=6 AE=6 EC=9
    t = tri(10, 15, 15)
    A, B, C = t["A"], t["B"], t["C"]
    r = 4 / 10
    pts = {"A": A, "B": B, "C": C, "D": (A[0] + (B[0] - A[0]) * r, A[1] + (B[1] - A[1]) * r),
           "E": (A[0] + (C[0] - A[0]) * r, A[1] + (C[1] - A[1]) * r)}
    f2 = Fig(pts, 2.4).poly("ABC").line("D", "E").par("D", "E").par("B", "C")
    f2.label(D=(-3.5, .3)).side("A", "D", 4, 4, at=(-6.5, -1)).side("D", "B", 6, 6).side("A", "E", 6, 6).side("E", "C", "x", 9)

    def butterfly(oa, ob, ab, k, sc):
        t = tri(oa, ab, ob, "OAB")          # O を上に作って，O を原点へ
        ox, oy = t["O"]
        A = (t["A"][0] - ox, t["A"][1] - oy)
        B = (t["B"][0] - ox, t["B"][1] - oy)
        # A，B を上に（AB が上の辺）
        A, B = (-A[0], -A[1]), (-B[0], -B[1])
        return {"O": (0, 0), "A": A, "B": B, "D": (-A[0] * k, -A[1] * k), "C": (-B[0] * k, -B[1] * k)}
    f3 = Fig(butterfly(6, 7, 8, 1.5, 2.3), 2.3).line("A", "B").line("C", "D").line("A", "D").line("B", "C").par("A", "B").par("C", "D")
    f3.label(O=(5, 0)).side("O", "A", 6, 6, at=(6.5, 1.5)).side("O", "D", 9, 9, at=(-6.5, -1)).side("A", "B", 8, 8).side("C", "D", "x", 12)
    f4 = Fig(butterfly(5, 6, 8, 1.5, 2.4), 2.4).line("A", "B").line("C", "D").line("A", "D").line("B", "C").par("A", "B").par("C", "D")
    f4.label(O=(5, 0)).side("O", "B", 6, 6, at=(-6.5, 1.5)).side("O", "C", 9, 9, at=(6.5, -1)).side("A", "B", "x", 8).side("C", "D", 12, 12)
    # (5) ∠ABC＝∠ACD  AB=9 AC=6 BC=12 AD=4 CD=8
    t = tri(9, 12, 6)
    A, B, C = t["A"], t["B"], t["C"]
    pts = {"A": A, "B": B, "C": C, "D": (A[0] + (B[0] - A[0]) * 4 / 9, A[1] + (B[1] - A[1]) * 4 / 9)}
    f5 = Fig(pts, 3.5).poly("ABC").line("C", "D").angle("A", "B", "C").angle("A", "C", "D")
    # ∠ABC＝∠ACD を確かめる
    def ang(F, p, v, q):
        (a, b), (c, d), (e, g) = F.p[p], F.p[v], F.p[q]
        return math.atan2(abs((a - c) * (g - d) - (b - d) * (e - c)), (a - c) * (e - c) + (b - d) * (g - d))
    assert abs(ang(f5, "A", "B", "C") - ang(f5, "A", "C", "D")) < 1e-9
    f5.side("A", "D", "x", 4).side("D", "B", 5, 5).side("A", "C", 6, 6).side("B", "C", 12, 12).side("C", "D", "y", 8, at=(.5, -2.8))
    # (6) 直角三角形  AB=15 AC=20 BC=25  BD=9 CD=16 AD=12
    pts = {"A": (9, 12), "B": (0, 0), "C": (25, 0), "D": (9, 0)}
    f6 = Fig(pts, 1.75).poly("ABC").line("A", "D").right("B", "A", "C").right("A", "D", "C")
    f6.side("A", "B", 15, 15).side("A", "C", 20, 20).side("B", "D", "x", 9).side("D", "A", "y", 12, at=(5, 0))
    assert abs(f6.dist("D", "C") - 16) < 1e-9 and abs(f6.dist("B", "C") - 25) < 1e-9
    return f1, f2, f3, f4, f5, f6


def page3():
    f1, f2, f3, f4, f5, f6 = figs3()
    def q(no, text, fig, ans, sim=True):
        return (f"<div class=q><div class=tx><span class=no>({no})</span><div>{text}</div></div>"
                f"<div class=figs>{fig.svg()}</div>"
                f"{f'<div class=sim>{BLANK_SIM}</div>' if sim else ''}<div class=space></div>{ansl(*ans)}</div>")
    return f"""<div class=page>{head(3)}
{big(1, "どの三角形とどの三角形が相似かを見つけて書き，文字の値を求めなさい。（単位は cm）")}
<div class=row2 style="margin-top:1.5mm">
{q(1, f"{S('DE')} ∥ {S('BC')}", f1, [X_ + '＝'])}
{q(2, f"{S('DE')} ∥ {S('BC')}", f2, [X_ + '＝'])}
</div>
<div class=row2>
{q(3, f"{S('AB')} ∥ {S('DC')}", f3, [X_ + '＝'])}
{q(4, f"{S('AB')} ∥ {S('DC')}", f4, [X_ + '＝'])}
</div>
<div class=row2>
{q(5, f"{T(r'\angle\mathrm{ABC}=\angle\mathrm{ACD}')}", f5, [X_ + '＝', Y_ + '＝'])}
{q(6, f"{T(r'\angle\mathrm{BAC}=90^\circ')}，{S('AD')} ⊥ {S('BC')}，{seg('BC', 25)}", f6, [X_ + '＝', Y_ + '＝'])}
</div></div>"""


def figs4():
    # (1) 台形 AD=6 BC=9 AO=4 OC=6
    A, D, B, C = (1, 6), (7, 6), (0, 0), (9, 0)
    O = (A[0] + (C[0] - A[0]) * .4, A[1] + (C[1] - A[1]) * .4)
    f1 = Fig({"A": A, "B": B, "C": C, "D": D, "O": O}, 3.4).poly("ABCD").line("A", "C").line("B", "D").par("A", "D").par("B", "C")
    f1.label(O=(0, -3)).side("A", "D", 6, 6).side("B", "C", 9, 9).side("A", "O", 4, 4, at=(-1.5, 3.6)).side("O", "C", "x", 6, at=(.7, -2.7))
    # (2) 平行四辺形 AD=12 CE:ED=1:2 CF=6
    A, B, C, D = (3, 8), (0, 0), (12, 0), (15, 8)
    E = (C[0] + (D[0] - C[0]) / 3, C[1] + (D[1] - C[1]) / 3)
    F = (18, 0)
    assert abs((E[1] - A[1]) * (F[0] - A[0]) - (F[1] - A[1]) * (E[0] - A[0])) < 1e-9
    f2 = Fig({"A": A, "B": B, "C": C, "D": D, "E": E, "F": F}, 2.2).poly("ABCD").line("A", "F").line("C", "F")
    f2.label(E=(3.2, -1.5), C=(-1, 3.4)).side("A", "D", 12, 12).side("C", "F", "x", 6)
    # (3) 影
    f3 = Fig({"A": (0, 1.5), "B": (0, 0), "C": (2, 0), "D": (5, 6), "E": (5, 0), "F": (13, 0)}, 3.3)
    f3.poly("ABC").poly("DEF").right("A", "B", "C").right("D", "E", "F").label(A=(-1.5, -3), B=(-1.5, 3.2), C=(0, 3.4), D=(-3, -.5), E=(0, 3.4), F=(1.5, 3.4))
    f3.side("A", "B", "1.5", 1.5, unit="m", off=1.2).side("B", "C", 2, 2, unit="m", off=7).side("D", "E", "x", 6, unit="m", off=4).side("E", "F", 8, 8, unit="m", off=7)
    # (5) 内接する正方形 BC=12 AH=6 1辺4
    A, B, C = (4, 6), (0, 0), (12, 0)
    P, S_ = (8 / 3, 4), (20 / 3, 4)
    Q, R = (8 / 3, 0), (20 / 3, 0)
    f5 = Fig({"A": A, "B": B, "C": C, "P": P, "S": S_, "Q": Q, "R": R, "H": (4, 0)}, 3)
    f5.poly("ABC").poly("PQRS").line("A", "H", dash=True).right("A", "H", "C").label(H=(1, 3.4), Q=(-1, 3.4), R=(1, 3.4), P=(-3, -1), S=(3, -1))
    f5.side("B", "C", 12, 12, at=(0, 7.5))
    return f1, f2, f3, f5


def page4():
    f1, f2, f3, f5 = figs4()
    def q(no, text, fig, ans):
        fg = f"<div class=figs>{fig.svg()}</div>" if fig else ""
        return (f"<div class=q><div class=tx><span class=no>[{no}]</span><div>{text}</div></div>{fg}"
                f"<div class=space></div>{ansl(*ans)}</div>")
    return f"""<div class=page>{head(4)}
<div class=row2 style="margin-top:3mm">
{q(1, f"台形 {S('ABCD')} で {S('AD')} ∥ {S('BC')}，{S('O')} は対角線の交点です。{X_} の値を求めなさい。（単位は cm）", f1, [X_ + '＝'])}
{q(2, f"平行四辺形 {S('ABCD')} の辺 {S('CD')} 上に {T(r'\mathrm{CE}:\mathrm{ED}=1:2')} となる点 {S('E')} をとり，{S('AE')} の延長と {S('BC')} の延長の交点を {S('F')} とします。{X_} の値を求めなさい。（単位は cm）", f2, [X_ + '＝'])}
</div>
<div class=row2>
{q(3, f"長さ 1.5m の棒の影が 2m のとき，同じ時刻に木の影は 8m でした。木の高さ {X_} m を求めなさい。", f3, [X_ + '＝'])}
{q(4, f"下の図で，{S('PQRS')} は正方形です。{seg('BC', 12)}，高さ {seg('AH', 6)} のとき，正方形の1辺の長さを求めなさい。", f5, ['1辺＝'])}
</div>
<div class=row2 style="flex:0 0 52mm">
{q(5, f"相似な2つの三角形があり，相似比は 3：5 です。小さい方の周の長さが 24cm のとき，大きい方の周の長さを求めなさい。", None, [''])}
{q(6, f"縮尺 {T(r'\dfrac{1}{25000}')} の地図で，2地点間の長さは 6cm でした。実際の距離は何 km ですか。", None, [''])}
</div></div>"""


# ---------- こたえ ----------
def ar(no, lines, res):
    mid = "".join(f"<span class=st>{l}</span>" for l in lines)
    return f"<div class=ar><span class=no>{no}</span><div>{mid}<span class=res>{res}</span></div></div>"


def ts(*eqs):
    return [T(e) for e in eqs]


def answers():
    p1 = (
        "<div class=ah>その1 ［1］</div>"
        + ar("(1)", ts("3x=12"), T("x=4")) + ar("(2)", ts("2x=20"), T("x=10"))
        + ar("(3)", ts("4x=60"), T("x=15")) + ar("(4)", ts("5x=120"), T("x=24"))
        + "<div class=ah>その1 ［2］</div>"
        + ar("(1)", [f"{S('AB')}：{S('DE')}＝6：9"], "2：3")
        + ar("(2)", ts("8:x=2:3", "2x=24"), T("x=12"))
        + ar("(3)", ts("y:6=2:3", "3y=12"), T("y=4"))
        + "<div class=ah>その1 ［3］</div>"
        + ar("(1)", [f"{S('AB')}：{S('DE')}＝8：6"], "4：3")
        + ar("(2)", ts("12:x=4:3", "4x=36"), T("x=9"))
        + ar("(3)", ts("y:12=4:3", "3y=48"), T("y=16"))
        + "<div class=ah>その2 ［1］</div>"
        + ar("(1)", [f"相似比 {S('AB')}：{S('DE')}＝10：15＝2：3"] + ts("14:x=2:3", "y:18=2:3"), f"{T('x=21')}，{T('y=12')}")
        + ar("(2)", [f"相似比 {S('AB')}：{S('DE')}＝9：15＝3：5"] + ts("12:x=3:5", "y:10=3:5"), f"{T('x=20')}，{T('y=6')}")
        + "<div class=ah>その2 ［2］</div>"
        + ar("(1)", [f"6：9＝2：3。8：{S('QR')}＝2：3"], "12cm")
        + ar("(2)", [f"12：8＝3：2。15：{S('DF')}＝3：2"], "10cm")
        + ar("(3)", [f"A→F，B→E，C→D が対応。{S('AC')} に対応するのは {S('FD')}", f"10：6＝5：3。15：{S('FD')}＝5：3"], "9cm")
        + ar("(4)", [f"6：4＝3：2。5：{S('FD')}＝3：2", T(r"3\times\mathrm{FD}=10")], T(r"\dfrac{10}{3}") + "cm")
        + "<div class=ah>その2 ［3］</div>"
        + ar("", [f"相似比 {S('AB')}：{S('EF')}＝18：12＝3：2"] + ts("12:x=3:2", "y:6=3:2"), f"{T('x=8')}，{T('y=9')}")
    )
    p2 = (
        "<div class=ah>その3</div>"
        + ar("(1)", [SIM("ADE", "ABC") + "（2組の角）", T(r"\mathrm{AD}:\mathrm{AB}=6:9=2:3"), T("8:x=2:3")], T("x=12"))
        + ar("(2)", [SIM("ADE", "ABC"), T(r"\mathrm{AD}:\mathrm{AB}=4:10=2:5"), T("6:(6+x)=2:5"), T("2(6+x)=30")], T("x=9"))
        + ar("(3)", [SIM("OAB", "ODC") + "（2組の角）", T("6:9=2:3"), T("8:x=2:3")], T("x=12"))
        + ar("(4)", [SIM("OAB", "ODC"), T("6:9=2:3"), T("x:12=2:3")], T("x=8"))
        + ar("(5)", [SIM("ABC", "ACD") + "（∠A が共通，∠ABC＝∠ACD）", T(r"\mathrm{AB}:\mathrm{AC}=9:6=3:2"),
                     T("6:x=3:2") + "，" + T("12:y=3:2")], f"{T('x=4')}，{T('y=8')}")
        + ar("(6)", [SIM("ABC", "DBA") + "（∠B が共通，直角）", T(r"\mathrm{BC}:\mathrm{BA}=25:15=5:3"),
                     T("15:x=5:3") + "，" + T("20:y=5:3")], f"{T('x=9')}，{T('y=12')}")
        + "<div class=ah>その4</div>"
        + ar("[1]", [SIM("AOD", "COB") + "（2組の角）", T(r"\mathrm{AD}:\mathrm{CB}=6:9=2:3"), T("4:x=2:3")], T("x=6"))
        + ar("[2]", [SIM("AED", "FEC") + "（2組の角）", T(r"\mathrm{ED}:\mathrm{EC}=2:1"), T("12:x=2:1")], T("x=6"))
        + ar("[3]", ["棒と影の三角形と，木と影の三角形は相似", T("1.5:x=2:8"), T("2x=12")], T("x=6") + "（6m）")
        + ar("[4]", [f"1辺を {X_} cm とする。{SIM('APS', 'ABC')}", "△APS の高さは " + T("(6-x)") + " cm", T("x:12=(6-x):6"), T("6x=12(6-x)"), T("18x=72")], "4cm")
        + ar("[5]", ["周の長さの比も相似比と同じ", T("24:x=3:5"), T("3x=120")], "40cm")
        + ar("[6]", [T(r"6\times 25000=150000") + "（cm）＝1500m"], "1.5km")
    )
    return (f"<div class='page ansp'>{head(0, '1/2')}<div class=acols>{p1}</div></div>"
            f"<div class='page ansp'>{head(0, '2/2')}<div class=acols>{p2}</div></div>")


def check():
    F = Fr
    # 比例式
    assert F(6 * 2, 3) == 4 and F(4 * 5, 2) == 10 and F(3 * 20, 4) == 15 and F(8 * 15, 5) == 24
    # 相似：x は対応する辺×比
    assert 8 * F(3, 2) == 12 and 6 * F(2, 3) == 4 and 12 * F(3, 4) == 9 and 12 / F(3, 4) == 16
    assert 14 * F(3, 2) == 21 and 18 * F(2, 3) == 12 and 12 * F(5, 3) == 20 and 10 * F(3, 5) == 6
    # 図なし
    assert 8 * F(9, 6) == 12 and 15 * F(8, 12) == 10 and 15 * F(6, 10) == 9 and 5 * F(4, 6) == F(10, 3)
    # 四角形
    assert 12 * F(2, 3) == 8 and 6 * F(3, 2) == 9
    # 重なり
    assert 8 * F(9, 6) == 12 and 6 * F(10, 4) - 6 == 9 and 8 * F(9, 6) == 12 and 12 * F(6, 9) == 8
    assert F(6 * 6, 9) == 4 and 12 * F(6, 9) == 8 and F(15 * 15, 25) == 9 and F(15 * 20, 25) == 12
    # 利用
    assert 4 * F(9, 6) == 6 and F(12, 2) == 6 and F(15, 10) * 4 == 6
    assert 4 * 12 == 12 * (6 - 4) * 2 and 24 * F(5, 3) == 40 and 6 * 25000 == 150000
    print("確認OK：答えと図の長さ")


if __name__ == "__main__":
    check()
    write_pdfs([
        (doc(CSS, page1() + page2() + page3() + page4()), f"{FILE}.pdf"),
        (doc(CSS, answers()), f"{FILE}_ans.pdf"),
    ])
