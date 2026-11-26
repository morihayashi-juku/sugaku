"""中3 円周角の定理（角度を求める）4ページ＋こたえ（問題に赤で書き込んだ形）

  cd tools && python3 c3_en_shuukaku.py

- 1回1テーマでじっくり（中3前半・先生の希望）。証明・利用は別の回。
  その1＝中心角と円周角・同じ弧の円周角
  その2＝直径と円周角・三角形と組み合わせる
  その3＝弧と円周角（等しい弧・弧の長さに比例・等分）
  その4＝練習（☆＝チャレンジ）
- 図は円周上の点の位置（度）から描き、答えと図に書いた角度を座標で確かめる（check）。
- 出力：pdf/c3_en_shuukaku_A.pdf と c3_en_shuukaku_A_ans.pdf
"""
import math

from texlib import doc, tex as T, write_pdfs

FILE = "c3_en_shuukaku_A"
X_, Y_ = T("x"), T("y")


def S(n):
    return T(r"\mathrm{%s}" % n)


def ANG(n):
    return T(r"\angle\mathrm{%s}" % n)


def A(s):
    return f"<span class=a>{s}</span>"


def st(*lines):
    return "".join(f"<span class=st>{A(l)}</span>" for l in lines)


def ln(body, w=26, label=""):
    return f"<div class=ln style='width:{w}mm'>{label}{A(body)}</div>"


# ---------- 円の図 ----------
class CF:
    """円周上の点は角度（度・0＝右、反時計回り）、ほかは (x, y)（半径1の単位）。"""

    def __init__(self, pts, R=18.0):
        self.R = R
        self.p = {}
        self.on = set()
        for k, v in pts.items():
            if isinstance(v, (int, float)):
                t = math.radians(v)
                self.p[k] = (math.cos(t), math.sin(t))
                self.on.add(k)
            else:
                self.p[k] = v
        self.segs, self.marks, self.lab = [], [], {}
        self.hide = set()

    def inter(self, name, a, b, c, d):
        """直線 ab と cd の交点"""
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = self.p[a], self.p[b], self.p[c], self.p[d]
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        self.p[name] = (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        return self

    def seg(self, *pairs):
        for s_ in pairs:
            self.segs.append((s_[0], s_[1]))
        return self

    def angle(self, v, a, b):
        (vx, vy), (ax, ay), (bx, by) = self.p[v], self.p[a], self.p[b]
        u1, u2 = (ax - vx, ay - vy), (bx - vx, by - vy)
        c = (u1[0] * u2[0] + u1[1] * u2[1]) / (math.hypot(*u1) * math.hypot(*u2))
        return math.degrees(math.acos(max(-1, min(1, c))))

    def mark(self, v, a, b, text, r=4.0, d=None, val=None):
        """∠avb に弧と文字。val を書くと角度を確かめる"""
        ang = self.angle(v, a, b)
        if val is not None:
            assert abs(ang - val) < 1e-6, (v, a, b, ang, val)
        self.marks.append((v, a, b, text, r, d))
        return self

    def svg(self, ans_text=None):
        R, pad = self.R, 6.5
        W = 2 * R + 2 * pad
        X = lambda q: pad + R + q[0] * R
        Y = lambda q: pad + R - q[1] * R
        o = [f'<svg class=fig width="{W:.1f}mm" height="{W:.1f}mm" viewBox="0 0 {W:.1f} {W:.1f}">',
             f'<circle cx="{pad + R}" cy="{pad + R}" r="{R}" fill="none" stroke="#111" stroke-width=".4"/>']
        for a, b in self.segs:
            o.append(f'<line x1="{X(self.p[a]):.2f}" y1="{Y(self.p[a]):.2f}" x2="{X(self.p[b]):.2f}" y2="{Y(self.p[b]):.2f}" '
                     f'stroke="#111" stroke-width=".35" stroke-linecap="round"/>')
        for v, a, b, text, r, d in self.marks:
            vx, vy = X(self.p[v]), Y(self.p[v])
            t1 = math.atan2(Y(self.p[a]) - vy, X(self.p[a]) - vx)
            t2 = math.atan2(Y(self.p[b]) - vy, X(self.p[b]) - vx)
            dd = (t2 - t1 + math.pi) % (2 * math.pi) - math.pi
            o.append(f'<path d="M{vx + r * math.cos(t1):.2f},{vy + r * math.sin(t1):.2f} A{r},{r} 0 0 {1 if dd > 0 else 0} '
                     f'{vx + r * math.cos(t1 + dd):.2f},{vy + r * math.sin(t1 + dd):.2f}" fill="none" stroke="#111" stroke-width=".25"/>')
            tm = t1 + dd / 2
            dist = d if d is not None else r + 3.6
            tx, ty = vx + dist * math.cos(tm), vy + dist * math.sin(tm) + 1.1
            if text in ("x", "y"):
                o.append(f'<text x="{tx:.2f}" y="{ty:.2f}" text-anchor="middle" font-size="3.6" font-family="KaTeX_Math" font-style="italic">{text}</text>')
            else:
                o.append(f'<text x="{tx:.2f}" y="{ty:.2f}" text-anchor="middle" font-size="3.1" font-family="KaTeX_Main">{text}</text>')
        for k, q in self.p.items():
            if k in self.hide:
                continue
            o.append(f'<circle cx="{X(q):.2f}" cy="{Y(q):.2f}" r=".55" fill="#111"/>')
            if k in self.lab:
                dx, dy = self.lab[k]
            elif k in self.on:
                dx, dy = q[0] * 3.6, -q[1] * 3.6
            else:
                # 角の印があれば、その反対がわに置く
                vs = []
                for v, a, b, *_ in self.marks:
                    if v != k:
                        continue
                    for t in (a, b):
                        ux, uy = X(self.p[t]) - X(q), Y(self.p[t]) - Y(q)
                        L = math.hypot(ux, uy)
                        vs.append((ux / L, uy / L))
                if vs:
                    mx, my = sum(v[0] for v in vs), sum(v[1] for v in vs)
                    L = math.hypot(mx, my) or 1
                    dx, dy = -mx / L * 3.4, -my / L * 3.4
                else:
                    dx, dy = -2.2, 3.2
            o.append(f'<text x="{X(q) + dx:.2f}" y="{Y(q) + dy + 1.2:.2f}" text-anchor="middle" font-size="3.5" font-family="KaTeX_Main">{k}</text>')
        o.append("</svg>")
        return "".join(o)


O = (0.0, 0.0)


def central(a, b, p):
    """中心角 ∠AOB と、P からの円周角 ∠APB の基本の図"""
    return CF({"O": O, "A": a, "B": b, "P": p}).seg("OA", "OB", "PA", "PB")


# ---------- 問題（図・問題文・答え・こたえの説明） ----------
def p1():
    q = []
    f = central(215, 325, 95).mark("O", "A", "B", "110°", val=110).mark("P", "A", "B", "x", r=5, val=55)
    q.append((f, "", [("x", 55)], ["円周角は中心角の半分", "110°÷2"]))
    f = central(200, 280, 60).mark("P", "A", "B", "40°", r=5, val=40).mark("O", "A", "B", "x", val=80)
    q.append((f, "", [("x", 80)], ["中心角は円周角の2倍", "40°×2"]))
    f = central(20, 144, 262).mark("O", "A", "B", "124°", val=124).mark("P", "A", "B", "x", r=5, val=62)
    q.append((f, "", [("x", 62)], ["弧 AB に対する円周角", "124°÷2"]))
    f = CF({"A": 222, "B": 318, "P": 70, "Q": 125}).seg("PA", "PB", "QA", "QB")
    f.mark("P", "A", "B", "48°", r=5, val=48).mark("Q", "A", "B", "x", r=5, val=48)
    q.append((f, "", [("x", 48)], ["同じ弧 AB に対する円周角は等しい"]))
    f = CF({"O": O, "A": 210, "B": 330, "C": 60, "D": 130}).seg("OA", "OB", "CA", "CB", "DA", "DB")
    f.mark("O", "A", "B", "120°", val=120).mark("C", "A", "B", "x", r=5, val=60).mark("D", "A", "B", "y", r=5, val=60)
    q.append((f, "", [("x", 60), ("y", 60)], ["どちらも弧 AB に対する円周角", "120°÷2"]))
    f = central(200, 340, 270).mark("O", "A", "B", "140°", r=3.5, d=6.2, val=140).mark("P", "A", "B", "x", r=3, d=5.6, val=110)
    q.append((f, "☆ 点 P は短いほうの弧の上", [("x", 110)], ["P が見ているのは長いほうの弧", "その中心角は 360°－140°＝220°", "220°÷2"]))
    return q


def p2():
    q = []
    f = CF({"O": O, "A": 180, "B": 0, "C": 120}).seg("AB", "AC", "BC")
    f.mark("B", "A", "C", "30°", r=6, val=30).mark("A", "B", "C", "x", r=6, val=60)
    q.append((f, f"{S('AB')} は直径", [("x", 60)], [f"直径に対する円周角だから {ANG('ACB')}＝90°", "x＝180°－90°－30°"]))
    f = CF({"O": O, "A": 180, "B": 0, "C": 250, "D": 100}).seg("AB", "AC", "BC", "AD", "DC")
    f.mark("D", "A", "C", "35°", r=6, val=35).mark("A", "C", "B", "x", r=6, val=55)
    q.append((f, f"{S('AB')} は直径", [("x", 55)],
              [f"弧 AC に対する円周角だから {ANG('ABC')}＝{ANG('ADC')}＝35°", f"{ANG('ACB')}＝90°（直径）", "x＝180°－90°－35°"]))
    f = CF({"O": O, "A": 210, "B": 330, "C": 90}).seg("OA", "OB", "AB", "CA", "CB")
    f.mark("A", "O", "B", "30°", r=7, val=30).mark("C", "A", "B", "x", r=5, val=60)
    q.append((f, "O は円の中心", [("x", 60)], [f"OA＝OB だから {ANG('OBA')}＝30°", f"{ANG('AOB')}＝180°－30°×2＝120°", "x＝120°÷2"]))
    f = CF({"A": 160, "B": 230, "C": 310, "D": 100}).seg("AC", "BD", "AB", "CD").inter("E", "A", "C", "B", "D")
    f.mark("D", "B", "C", "40°", r=6, val=40).mark("C", "A", "D", "30°", r=6, val=30).mark("E", "A", "B", "x", r=3.5, d=6.5, val=110)
    q.append((f, f"{S('E')} は {S('AC')} と {S('BD')} の交点", [("x", 110)],
              [f"弧 BC → {ANG('BAC')}＝{ANG('BDC')}＝40°", f"弧 AD → {ANG('ABD')}＝{ANG('ACD')}＝30°", "△ABE で x＝180°－40°－30°"]))
    return q


def p3():
    q = []
    f = CF({"A": 140, "B": 190, "C": 240, "D": 20}).seg("DA", "DB", "DC")
    f.mark("D", "A", "B", "25°", r=10, d=14, val=25).mark("D", "A", "C", "x", r=5, val=50)
    q.append((f, "弧 AB＝弧 BC", [("x", 50)], [f"等しい弧に対する円周角は等しい → {ANG('BDC')}＝25°", "x＝25°＋25°"]))
    pts = {chr(65 + k): 90 - 40 * k for k in range(9)}
    f = CF(pts).seg("AC", "AF", "FC")
    f.mark("A", "C", "F", "x", r=5, val=60).mark("F", "A", "C", "y", r=6, val=40)
    q.append((f, "円周を9等分した点", [("x", 60), ("y", 40)],
              ["弧1つ分の中心角は 360°÷9＝40° → 円周角は 20°", "x：弧 CF は3つ分 → 20°×3", "y：弧 AC は2つ分 → 20°×2"]))
    f = CF({"A": 150, "B": 210, "C": 300, "D": 40}).seg("DA", "DB", "DC")
    f.mark("D", "A", "B", "30°", r=11, d=15, val=30).mark("D", "B", "C", "x", r=6, val=45)
    q.append((f, "弧 AB：弧 BC＝2：3", [("x", 45)], ["円周角は弧の長さに比例する", T("2:3=30:x") + "　" + T("2x=90")]))
    f = CF({"O": O, "A": 250, "B": 322, "C": 100}).seg("CA", "CB", "OA", "OB")
    f.mark("C", "A", "B", "36°", r=6, val=36)
    q.append((f, f"{ANG('ACB')}＝36° のとき，弧 AB の長さは円周の何分のいくつ？", [("", "1/5")],
              [f"中心角 {ANG('AOB')}＝36°×2＝72°", T(r"\dfrac{72}{360}=\dfrac{1}{5}")]))
    return q


def p4():
    q = []
    f = central(195, 345, 90).mark("O", "A", "B", "150°", val=150).mark("P", "A", "B", "x", r=5, val=75)
    q.append((f, "", [("x", 75)], ["150°÷2"]))
    f = CF({"O": O, "A": 180, "B": 0, "C": 56, "D": 280}).seg("AB", "AC", "BC", "AD", "DC")
    f.mark("A", "B", "C", "28°", r=8, val=28).mark("D", "A", "C", "x", r=5, val=62)
    q.append((f, f"{S('AB')} は直径", [("x", 62)], [f"{ANG('ACB')}＝90° → {ANG('ABC')}＝62°", f"弧 AC → x＝{ANG('ABC')}"]))
    f = CF({"O": O, "A": 220, "B": 320, "C": 90}).seg("OA", "OB", "AB", "CA", "CB")
    f.mark("C", "A", "B", "50°", r=5, val=50).mark("A", "O", "B", "x", r=7, val=40)
    q.append((f, "O は円の中心", [("x", 40)], [f"{ANG('AOB')}＝50°×2＝100°", "OA＝OB → x＝(180°－100°)÷2"]))
    f = CF({"A": 160, "B": 230, "C": 300, "D": 70}).seg("AC", "BD", "AB", "CD").inter("E", "A", "C", "B", "D")
    f.mark("A", "B", "C", "35°", r=6, val=35).mark("C", "A", "D", "45°", r=6, val=45).mark("E", "B", "C", "x", r=3.5, d=6.5, val=80)
    q.append((f, f"{S('E')} は {S('AC')} と {S('BD')} の交点", [("x", 80)],
              [f"弧 BC → {ANG('BDC')}＝35°", f"△ECD で {ANG('DEC')}＝180°－35°－45°＝100°", "x＝180°－100°"]))
    f = central(215, 325, 270).mark("P", "A", "B", "125°", r=3, d=6.2, val=125).mark("O", "A", "B", "x", r=3.5, d=6, val=110)
    q.append((f, "☆ 点 P は短いほうの弧の上", [("x", 110)], ["長いほうの弧の中心角は 125°×2＝250°", "x＝360°－250°"]))
    pts = {chr(65 + k): 90 - 72 * k for k in range(5)}
    f = CF(pts).seg("AB", "BC", "CD", "DE", "EA", "AC", "AD")
    f.mark("A", "C", "D", "x", r=7, val=36)
    q.append((f, "円周を5等分した点", [("x", 36)], ["弧 CD は円周の ⅕ → 中心角 72°", "x＝72°÷2"]))
    return q


def cells(qs, cols, ans):
    out = ""
    for i, (f, cond, asks, why) in enumerate(qs):
        lines = ""
        for name, val in asks:
            body = (T(r"\dfrac{1}{5}") if val == "1/5" else f"{val}°")
            label = f"{T(name)}＝" if name else ""
            lines += ln(body, 24, label)
        out += (f"<div class=cell><div class=tx><span class=no>({i + 1})</span><div>{cond}</div></div>"
                f"<div class=fg>{f.svg()}</div><div class=wk>{st(*why)}</div><div class=lns>{lines}</div></div>")
    return f"<div class='grid c{cols}'>{out}</div>"


def check():
    for qs in (p1(), p2(), p3(), p4()):       # 図を作るときに mark(val=…) で角度を確かめている
        assert qs
    assert abs(72 / 360 - 1 / 5) < 1e-12
    print("確認OK：図の角度と答え（座標で確認）")


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; font-size: 10.2pt; }
.page { width: 210mm; height: 297mm; padding: 10mm 13mm 9mm; page-break-after: always; display: flex; flex-direction: column; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.katex { font-size: 1.08em; }
.a, .a .katex { color: #c8102e; }
.hide .a { visibility: hidden; }
.head { display: flex; align-items: baseline; white-space: nowrap; border-bottom: 1.2pt solid #111; padding-bottom: 1.5mm; flex: none; }
.head b { font-size: 14pt; }
.head .sub { margin-left: 3mm; font-size: 10.5pt; }
.head .kai { color: #c8102e; font-weight: 700; margin-left: 2mm; }
.head .nm { margin-left: auto; font-size: 9.5pt; }
.head .u { display: inline-block; border-bottom: .7pt solid #111; width: 42mm; }
.tip { flex: none; margin-top: 2.5mm; border: .8pt solid #666; border-radius: 1.5mm; padding: 2mm 3.5mm; font-size: 9.8pt; line-height: 1.75; background: #f5f5f5; display: flex; gap: 4mm; align-items: center; }
.big { flex: none; font-weight: 700; margin-top: 3mm; line-height: 1.5; }
.grid { flex: 1; min-height: 0; display: grid; column-gap: 5mm; row-gap: 3mm; margin-top: 2mm; }
.c3 { grid-template-columns: repeat(3, minmax(0, 1fr)); grid-template-rows: 1fr 1fr; }
.c2 { grid-template-columns: repeat(2, minmax(0, 1fr)); grid-template-rows: 1fr 1fr; }
.cell { display: flex; flex-direction: column; min-height: 0; border-top: .4pt solid #ccc; padding-top: 1mm; }
.cell .tx { display: flex; line-height: 1.55; font-size: 9.6pt; min-height: 5mm; }
.no { flex: none; width: 7mm; font-size: 9pt; padding-top: .3mm; }
.fg { display: flex; justify-content: center; flex: none; }
.fig { flex: none; }
.fig text { fill: #111; }
.wk { flex: 1 0 auto; }
.st { display: block; font-size: 9pt; line-height: 1.5; }
.ln { border-bottom: .9pt solid #111; height: 7mm; flex: none; display: flex; align-items: flex-end; justify-content: center; padding-bottom: .5mm; white-space: nowrap; }
.lns { display: flex; justify-content: flex-end; gap: 3mm; flex: none; }
"""


def head(no, title, ans):
    kai = "<span class=kai>【解答】</span>" if ans else ""
    return (f"<div class=head><b>中3数学 円周角の定理 その{no}</b><span class=sub>{title}</span>{kai}"
            f"<span class=nm>名前 <span class=u></span></span></div>")


def tipfig(kind):
    if kind == 1:
        f = CF({"O": O, "A": 215, "B": 325, "P": 95, "Q": 140}, R=11).seg("OA", "OB", "PA", "PB", "QA", "QB")
        f.mark("O", "A", "B", "2●", r=3, d=6).mark("P", "A", "B", "●", r=3.5, d=6).mark("Q", "A", "B", "●", r=3.5, d=6)
    else:
        f = CF({"O": O, "A": 180, "B": 0, "P": 115}, R=11).seg("AB", "PA", "PB")
        f.mark("P", "A", "B", "90°", r=3, d=6.5)
    return f.svg()


def page(no, title, tip, qs, cols, ans, tk=1):
    return (f"<div class='page{'' if ans else ' hide'}'>{head(no, title, ans)}"
            f"<div class=tip><div>{tip}</div>{tipfig(tk) if tk else ''}</div>"
            f"<div class=big>次の図で，{X_}（{Y_}）の値を求めなさい。</div>{cells(qs, cols, ans)}</div>")


def pages(ans):
    t1 = ("<b>円周角の定理</b><br>① 1つの弧に対する<b>円周角は，中心角の半分</b>（中心角は円周角の2倍）。<br>"
          "② <b>同じ弧に対する円周角は，どこでも等しい</b>。<br>"
          "<span style='font-size:8.8pt'>どの弧を見ている角かを，まず指でなぞって確かめよう。</span>")
    t2 = ("<b>直径と円周角</b>　半円の弧（直径）に対する円周角は <b>90°</b>。<br>"
          "円周角で角を移したら，<b>三角形の内角の和 180°</b> や <b>二等辺三角形（OA＝OB）</b> と組み合わせる。")
    t3 = ("<b>弧と円周角</b><br>・<b>等しい弧</b>に対する円周角は等しい。<br>"
          "・円周角の大きさは<b>弧の長さに比例</b>する（弧が2倍なら円周角も2倍）。<br>"
          "・円周を <i>n</i> 等分 → 弧1つ分の中心角は 360°÷<i>n</i>，円周角はその半分。")
    return (page(1, "中心角と円周角", t1, p1(), 3, ans)
            + page(2, "直径・三角形と組み合わせる", t2, p2(), 2, ans, tk=2)
            + page(3, "弧と円周角", t3, p3(), 2, ans, tk=0)
            + f"<div class='page{'' if ans else ' hide'}'>{head(4, '練習', ans)}"
              f"<div class=big>次の図で，{X_} の値を求めなさい。（☆＝チャレンジ）</div>{cells(p4(), 3, ans)}</div>")


if __name__ == "__main__":
    check()
    write_pdfs([(doc(CSS, pages(False)), f"{FILE}.pdf"), (doc(CSS, pages(True)), f"{FILE}_ans.pdf")])
