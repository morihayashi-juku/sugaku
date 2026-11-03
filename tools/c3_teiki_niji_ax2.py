"""中3 定期テスト対策（二次方程式・関数 y＝ax²）問題2ページ＋こたえ2ページ

  cd tools && python3 c3_teiki_niji_ax2.py

- 先生がくださった定期テスト（手書き）と同じ形・同じ順で、数字だけ変えた類題。
  1ページ目＝［1］二次方程式を解く7問・［2］文章題など3問
  2ページ目＝［3］y＝ax²（式を求める・グラフ2つ・放物線・変域3問）
- 出力：pdf/c3_teiki_niji_ax2_A.pdf と c3_teiki_niji_ax2_A_ans.pdf
- 答えは SymPy で確かめる（check）。
"""
import re
from fractions import Fraction as F

import sympy as sp

from mathlib import CSS, head, write_pdfs

TITLE = "定期テスト対策"
SUB = "二次方程式・関数 <i>y</i>＝<i>ax</i>²"
FILE = "c3_teiki_niji_ax2_A"


def m(s):
    """式を HTML に。{上|下}＝分数、x y a＝斜体、^2＝2乗、-＝−、<=＝≦"""
    def frac(mt):
        return f"<span class=fr><span class=nu>{mt[1]}</span><span class=de>{mt[2]}</span></span>"
    s = s.replace("<=", "≦").replace("<", "＜").replace("^2", "²").replace("=", "＝").replace("-", "−")
    s = re.sub(r"([xya])", r"<i>\1</i>", s)
    s = re.sub(r"(?<=[0-9²)>])−", "<span class=op>−</span>", s)   # 符号の − には余白をつけない
    s = re.sub(r"([+＝≦＜])", r"<span class=op>\1</span>", s)
    s = re.sub(r"\{([^|}]*)\|([^}]*)\}", frac, s)
    return f"<span class=mx>{s}</span>"


# ---------- 問題のデータ ----------
# (式, 途中の式, 解) ※解は check で SymPy と照らし合わせる
EQS = [
    ("x^2+7x+10=0", ["(x+2)(x+5)=0"], [-2, -5]),
    ("x^2-5x-14=0", ["(x+2)(x-7)=0"], [-2, 7]),
    ("x^2-10x+25=0", ["(x-5)^2=0"], [5]),
    ("3x^2+12x=0", ["3x(x+4)=0"], [0, -4]),
    ("x^2=5x", ["x^2-5x=0", "x(x-5)=0"], [0, 5]),
    ("3x^2+6x-24=0", ["x^2+2x-8=0", "(x+4)(x-2)=0"], [-4, 2]),
    ("x^2-5x+9=3(x-1)", ["x^2-5x+9=3x-3", "x^2-8x+12=0", "(x-2)(x-6)=0"], [2, 6]),
]

Q2 = [
    "連続した3つの正の整数があります。小さい方の2つの数の積が、3つの数の和より12大きいとき、これら3つの整数を求めなさい。",
    "長さ44cmのひもで長方形をつくり、その面積が112cm²になるようにします。このときの長方形のたてとよこの長さを求めなさい。",
    f"二次方程式 {m('x^2-ax+12=0')} の解の1つが3であるとき、{m('a')} の値と、他の解を求めなさい。",
]

# グラフ：(a, 変域 or None, 式の表示, 変域の表示)
G2 = [(F(2), None, "y=2x^2", ""), (F(1, 4), (-4, 2), "y={1|4}x^2", "-4<=x<=2")]
G3 = [(F(-3), None, "y=-3x^2", ""), (F(-1, 2), (-2, 4), "y=-{1|2}x^2", "-2<=x<=4")]
GRID2 = dict(ymin=-3, ymax=12, xlab=(-4, -2, 2, 4), ylab=(2, 4, 6, 8, 10))
GRID3 = dict(ymin=-16, ymax=1, xlab=(-5, 5), ylab=(-5, -10, -15))

# 変域：(a, xの範囲, 式, 答え)
RANGES = [
    (F(4), (1, 3), "y=4x^2", "1<=x<=3", (4, 36)),
    (F(-2), (-3, 2), "y=-2x^2", "-3<=x<=2", (-18, 0)),
    (F(1, 3), (-3, 6), "y={1|3}x^2", "-3<=x<=6", (0, 12)),
]


def check():
    x, a = sp.symbols("x a")

    def parse(s):
        s = s.replace("^2", "**2")
        s = re.sub(r"(\d)x", r"\1*x", s)
        s = re.sub(r"x\(", "x*(", s)
        s = re.sub(r"(\d)\(", r"\1*(", s)
        s = s.replace(")(", ")*(")
        left, right = s.split("=")
        return sp.sympify(left) - sp.sympify(right)

    for eq, steps, sols in EQS:
        e = parse(eq)
        assert set(sp.solve(e, x)) == set(sols), eq
        for st in steps:                       # 途中の式も、解が同じ
            assert set(sp.solve(parse(st), x)) == set(sols), (eq, st)
    # ［2］(1)
    sol = sp.solve(x * (x + 1) - (x + x + 1 + x + 2 + 12), x)
    assert set(sol) == {5, -3}
    assert 5 * 6 == 5 + 6 + 7 + 12
    # ［2］(2)
    assert set(sp.solve(x * (22 - x) - 112, x)) == {8, 14}
    assert 2 * (8 + 14) == 44 and 8 * 14 == 112
    # ［2］(3)
    assert sp.solve(9 - 3 * a + 12, a) == [7]
    assert set(sp.solve(x**2 - 7 * x + 12, x)) == {3, 4}
    # ［3］(1)
    assert F(48, (-4) ** 2) == 3
    # 変域
    for k, (lo, hi), _, _, ans in RANGES:
        vals = [k * lo**2, k * hi**2] + ([0] if lo <= 0 <= hi else [])
        assert (min(vals), max(vals)) == ans, (k, lo, hi)
    # グラフ：変域のはしと、印をつける点が方眼に入り、目もりの上にある
    for curves, g in ((G2, GRID2), (G3, GRID3)):
        for k, dom, _, _ in curves:
            for px in dots(k, dom, g):
                assert (k * px**2).denominator == 1, (k, px)
                assert g["ymin"] <= k * px**2 <= g["ymax"], (k, px)
    print("確認OK：解・途中の式・変域・グラフの点")


# ---------- グラフ ----------
def dots(k, dom, g):
    """印をつける点（x, y とも整数で方眼の中）"""
    lo, hi = dom or (-5, 5)
    return [px for px in range(lo, hi + 1)
            if (k * px**2).denominator == 1 and g["ymin"] <= k * px**2 <= g["ymax"]]


def graph(g, cell, curves=()):
    """方眼（x は −5〜5）。curves があれば答えのグラフを重ねる。単位は mm"""
    xmin, xmax, ymin, ymax = -5, 5, g["ymin"], g["ymax"]
    pad = 3.5
    w, h = (xmax - xmin) * cell + pad * 2, (ymax - ymin) * cell + pad * 2
    X = lambda v: pad + (float(v) - xmin) * cell
    Y = lambda v: pad + (ymax - float(v)) * cell
    o = [f'<svg class=gr width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">']
    for i in range(xmin, xmax + 1):
        o.append(f'<line x1="{X(i)}" y1="{Y(ymin)}" x2="{X(i)}" y2="{Y(ymax)}" stroke="#888" stroke-width=".18"/>')
    for j in range(ymin, ymax + 1):
        o.append(f'<line x1="{X(xmin)}" y1="{Y(j)}" x2="{X(xmax)}" y2="{Y(j)}" stroke="#888" stroke-width=".18"/>')
    o.append(f'<line x1="{X(xmin) - 2}" y1="{Y(0)}" x2="{X(xmax) + 2}" y2="{Y(0)}" stroke="#111" stroke-width=".4"/>')
    o.append(f'<line x1="{X(0)}" y1="{Y(ymin)}" x2="{X(0)}" y2="{Y(ymax) - 2}" stroke="#111" stroke-width=".4"/>')

    def label(px, py, t, anchor="middle", style="", size=2.9):
        # 文字のうしろを白く抜いて、方眼の線と重ならないようにする
        o.append(f'<text x="{px}" y="{py}" font-size="{size}" text-anchor="{anchor}" {style} '
                 f'stroke="#fff" stroke-width=".9" paint-order="stroke">{t}</text>')

    ser = 'font-family="Noto Serif CJK JP"'
    label(X(xmax) + 2.2, Y(0) - .9, "x", "end", ser + ' font-style="italic"', 3.2)
    label(X(0) + 1.1, Y(ymax) - .6, "y", "start", ser + ' font-style="italic"', 3.2)
    label(X(0) - 1, Y(0) + 3.2, "O", "end", ser)
    for v in g["xlab"]:
        label(X(v), Y(0) + 3.2, str(v).replace("-", "−"), style=ser)
    for v in g["ylab"]:
        label(X(0) - 1, Y(v) + 1, str(v).replace("-", "−"), "end", ser)

    colors = ("#b4232c", "#1f5fbf")
    for idx, (k, dom, _, _) in enumerate(curves):
        lo, hi = dom or (-5, 5)
        n, pts = 400, []
        for i in range(n + 1):
            vx = lo + (hi - lo) * i / n
            vy = float(k) * vx * vx
            if ymin <= vy <= ymax:
                pts.append(f"{X(vx):.2f},{Y(vy):.2f}")
        c = colors[idx]
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width=".55"/>')
        for px in dots(k, dom, g):
            o.append(f'<circle cx="{X(px)}" cy="{Y(k * px**2)}" r=".75" fill="{c}"/>')
        # 名札は、左はしの点のそば
        lx = dots(k, dom, g)[0]
        ly = k * lx**2
        label(X(lx) - 1.5, Y(ly) + (2.8 if k < 0 else -1), "①②"[idx], "end", f'fill="{c}" font-weight="700"', 3.6)
    o.append("</svg>")
    return "".join(o)


# ---------- ページ ----------
EXTRA = """
.mx { font-family: 'Noto Serif CJK JP', serif; white-space: nowrap; }
.mx .op { margin: 0 .7mm; }
.big { font-size: 12.5pt; font-weight: 700; display: flex; align-items: center; gap: 2mm; margin-top: 4mm; }
.big .box { display: inline-flex; width: 6.4mm; height: 6.4mm; border: 1pt solid #111; align-items: center;
            justify-content: center; font-size: 12pt; }
.big small { font-size: 10pt; font-weight: 400; }
.eqs { display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: 1fr; flex: 0 0 90mm; margin-top: 2mm; }
.e { font-size: 13.5pt; padding-top: 1mm; }
.no2 { font-family: 'Noto Sans CJK JP'; font-size: 11.5pt; margin-right: 2mm; }
.word { flex: 1; min-height: 0; display: flex; flex-direction: column; margin-top: 2mm; }
.wq { flex: 1; position: relative; font-size: 12pt; line-height: 1.6; display: flex; }
.wq .no2 { flex: none; }
.line { position: absolute; right: 0; bottom: 3mm; font-size: 11pt; }
.line .u { display: inline-block; border-bottom: .8pt solid #111; width: 62mm; }
.t3 { font-size: 11.5pt; line-height: 1.6; display: flex; }
.t3 .no2 { flex: none; }
.gq { display: flex; justify-content: space-between; margin-top: 1.5mm; }
.gtext { font-size: 11.5pt; line-height: 1.6; flex: 1; }
.gtext .eqn { margin: 2.5mm 0 0 3mm; font-size: 12.5pt; }
.gtext .dom { margin-left: 8mm; font-size: 11pt; }
.gtext .care { margin-top: 3mm; font-size: 10.5pt; }
.q3 { position: relative; flex: 1; min-height: 0; margin-top: 1mm; }
.blank { display: inline-block; width: 15mm; height: 6.5mm; border: .8pt solid #111; vertical-align: middle; }
.blank.w { width: 22mm; text-align: right; padding-right: 1mm; line-height: 6mm; }
/* こたえ */
.as { margin-top: 2mm; }
.ar { display: flex; font-size: 11pt; line-height: 1.75; padding: 1.1mm 0; border-bottom: .5pt solid #ddd; }
.ar .no2 { flex: none; font-size: 10.5pt; width: 9mm; }
.ar .res { font-weight: 700; color: #b4232c; }
.ar .st { color: #444; }
.tw { display: grid; grid-template-columns: 1fr 1fr; column-gap: 8mm; }
.gpair { display: flex; justify-content: space-between; margin-top: 2mm; }
.gpair > div { font-size: 10.5pt; line-height: 1.6; }
.gcap { margin-bottom: 1mm; }
"""


def big(n, text, small=""):
    return (f"<div class=big><span class=box>{n}</span><span>{text}</span>"
            f"{f'<small>{small}</small>' if small else ''}</div>")


def problems():
    eqs = "".join(f"<div class=e><span class=no2>({i + 1})</span>{m(q)}</div>" for i, (q, _, _) in enumerate(EQS))
    lines = ["3つの整数", "たて・よこ", f"{m('a')}＝<span class=u style='width:22mm'></span>，他の解"]
    words = "".join(
        f"<div class=wq><span class=no2>({i + 1})</span><div>{q}</div>"
        f"<div class=line>{lines[i]} <span class=u style='width:{40 if i == 2 else 62}mm'></span></div></div>" for i, q in enumerate(Q2))
    p1 = f"""<div class=page>{head(TITLE, SUB)}
{big(1, "次の二次方程式を解きなさい。", "（×3点）")}
<div class=eqs>{eqs}</div>
{big(2, "次の問に答えなさい。", "（×4点）※途中の式等もきちんと書くこと。")}
<div class=word>{words}</div></div>"""

    def gq(no, curves, g):
        items = ""
        for i, (_, _, eq, dom) in enumerate(curves):
            items += f"<div class=eqn>{'①②'[i]}　{m(eq)}</div>"
            if dom:
                items += f"<div class=dom>（{m(dom)}）</div>"
        return (f"<div class=gq><div class=gtext><div class=t3><span class=no2>({no})</span>"
                f"<div>次のグラフを右の<br>座標平面にかきなさい。</div></div>{items}"
                f"<div class=care>（※ていねいにかくこと。）</div></div>{graph(g, 4.35)}</div>")

    rng = ""
    for i, (_, _, eq, dom, _) in enumerate(RANGES):
        rng += (f"<div class=q3><div class=t3><span class=no2>({i + 5})</span>"
                f"<div>{m(eq)} で、{m(dom)} のときの {m('y')} の変域を求めなさい。</div></div>"
                f"<div class=line style='bottom:1mm'><span class=u></span></div></div>")
    p2 = f"""<div class=page>{head(TITLE, SUB)}
{big(3, "次の問に答えなさい。", "（×3点）")}
<div class=q3 style="flex:0 0 19mm"><div class=t3><span class=no2>(1)</span>
<div>{m('y')} は {m('x')} の2乗に比例し、{m('x=-4')} のとき {m('y=48')} である。{m('y')} を {m('x')} の式で表しなさい。</div></div>
<div class=line style="bottom:0"><span class=u></span></div></div>
{gq(2, G2, GRID2)}{gq(3, G3, GRID3)}
<div class=q3 style="flex:0 0 15mm"><div class=t3><span class=no2>(4)</span>
<div>関数 {m('y=ax^2')} の (2)，(3) のようなグラフのことを <span class="blank w">線</span> という。<span class=blank style="width:9mm;height:5mm"></span> をうめなさい。</div></div></div>
{rng}</div>"""
    return f"<html><head><meta charset=utf-8><style>{CSS}{EXTRA}</style></head><body>{p1}{p2}</body></html>"


def sols(v):
    return "，".join(m(f"x={s}") for s in v)


def answers():
    def row(no, body):
        return f"<div class=ar><span class=no2>({no})</span><div>{body}</div></div>"

    eq_rows = ""
    for i, (q, steps, s) in enumerate(EQS):
        mid = "".join(f"<span class=st>{m(t)}</span><br>" for t in steps)
        eq_rows += row(i + 1, f"{m(q)}<br>{mid}<span class=res>{sols(s)}</span>")
    w = [
        f"連続した3つの正の整数を {m('x')}，{m('x+1')}，{m('x+2')} とする。<br>"
        f"<span class=st>{m('x(x+1)=x+(x+1)+(x+2)+12')}<br>{m('x^2+x=3x+15')}<br>{m('x^2-2x-15=0')}<br>"
        f"{m('(x+3)(x-5)=0')}　より　{m('x=-3')}，{m('x=5')}</span><br>"
        f"{m('x')} は正の整数だから {m('x=5')}（{m('x=-3')} は問題に合わない）<br>"
        f"<span class=res>5，6，7</span>",
        f"たてを {m('x')} cm とすると、たて＋よこ＝22cm だから、よこは {m('(22-x)')} cm。<br>"
        f"<span class=st>{m('x(22-x)=112')}<br>{m('x^2-22x+112=0')}<br>"
        f"{m('(x-8)(x-14)=0')}　より　{m('x=8')}，{m('x=14')}</span><br>"
        f"どちらも {m('0<x<22')} に合う。<br>"
        f"<span class=res>たて8cm，よこ14cm（または たて14cm，よこ8cm）</span>",
        f"{m('x=3')} を代入する。<span class=st>{m('9-3a+12=0')}　より　{m('a=7')}</span><br>"
        f"もとの式は <span class=st>{m('x^2-7x+12=0')}，{m('(x-3)(x-4)=0')}</span><br>"
        f"<span class=res>{m('a=7')}，他の解 {m('x=4')}</span>",
    ]
    p1 = f"""<div class=page>{head(TITLE, SUB + "　こたえ（1/2）", name=False)}
{big(1, "二次方程式")}<div class="as tw">{eq_rows}</div>
{big(2, "文章題など")}<div class=as>{''.join(row(i + 1, t) for i, t in enumerate(w))}</div></div>"""

    def cap(no, curves):
        pts = []
        for i, (k, dom, eq, d) in enumerate(curves):
            pts.append(f"{'①②'[i]} {m(eq)}" + (f"（{m(d)}）" if d else ""))
        return f"<div class=gcap>({no})　{'　'.join(pts)}</div>"

    def pts(curves, g):
        out = []
        for i, (k, dom, _, _) in enumerate(curves):
            s = "，".join(f"({str(px).replace('-', '−')}, {str(k * px**2).replace('-', '−')})" for px in dots(k, dom, g))
            out.append(f"{'①②'[i]} 通る点：{s}")
        return "<br>".join(out)

    rng = ""
    for i, (k, (lo, hi), eq, dom, (a, b)) in enumerate(RANGES):
        if lo <= 0 <= hi:
            why = f"{m('x=0')} をふくむので、{'最大' if k < 0 else '最小'}は {m('y=0')}。" \
                  f"もう一方は 0 から遠い {m('x=' + str(lo if abs(lo) > abs(hi) else hi))} のとき。"
        else:
            why = f"{m('x=' + str(lo))} のとき {m('y=' + str(a))}，{m('x=' + str(hi))} のとき {m('y=' + str(b))}。"
        rng += row(i + 5, f"{m(eq)}（{m(dom)}）　<span class=st>{why}</span><br><span class=res>{m(f'{a}<=y<={b}')}</span>")
    p2 = f"""<div class=page>{head(TITLE, SUB + "　こたえ（2/2）", name=False)}
{big(3, "関数 <i>y</i>＝<i>ax</i>²")}
<div class=as>{row(1, f"{m('y=ax^2')} に {m('x=-4')}，{m('y=48')} を代入。<span class=st>{m('48=16a')}　より　{m('a=3')}</span>　<span class=res>{m('y=3x^2')}</span>")}</div>
<div class=gpair><div>{cap(2, G2)}{graph(GRID2, 3.9, G2)}<br>{pts(G2, GRID2)}</div>
<div>{cap(3, G3)}{graph(GRID3, 3.9, G3)}<br>{pts(G3, GRID3)}</div></div>
<div class=as>{row(4, "<span class=res>放物</span>（線）")}{rng}</div></div>"""
    return f"<html><head><meta charset=utf-8><style>{CSS}{EXTRA}</style></head><body>{p1}{p2}</body></html>"


if __name__ == "__main__":
    check()
    write_pdfs([(problems(), f"{FILE}.pdf"), (answers(), f"{FILE}_ans.pdf")])
