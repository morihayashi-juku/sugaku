"""中3 定期テスト対策（二次方程式・関数 y＝ax²）2パターン（1ページ＝1パターン）＋こたえ2ページ

  cd tools && python3 c3_teiki_niji_ax2.py

- A3 に拡大して印刷する想定。ファイルは A4 で、1ページに左右2列（ほかの定期テスト対策プリントと同じ形）。
  左＝［1］二次方程式7問・［2］文章題など3問／右＝［3］y＝ax²（式・グラフ2つ・穴うめ・変域3問）
- 式は KaTeX（texlib）。文字式の文字は KaTeX の数式用イタリック。
- 出力：pdf/c3_teiki_niji_ax2.pdf と c3_teiki_niji_ax2_ans.pdf
- 答えは SymPy で確かめる（check）。
"""
import re
from fractions import Fraction as F

import sympy as sp

from texlib import doc, tex as T, write_pdfs

FILE = "c3_teiki_niji_ax2"
NO = "①②"

# ---------- 問題のデータ（1パターン＝1つの dict） ----------
PATTERNS = [
    {
        "eqs": [
            ("x^2+7x+10=0", ["(x+2)(x+5)=0"], [-2, -5]),
            ("x^2-5x-14=0", ["(x+2)(x-7)=0"], [-2, 7]),
            ("x^2-14x+49=0", ["(x-7)^2=0"], [7]),
            ("3x^2+12x=0", ["3x(x+4)=0"], [0, -4]),
            ("x^2=5x", ["x^2-5x=0", "x(x-5)=0"], [0, 5]),
            ("2x^2+6x-20=0", ["x^2+3x-10=0", "(x+5)(x-2)=0"], [-5, 2]),
            ("x^2-5x+9=3(x-1)", ["x^2-5x+9=3x-3", "x^2-8x+12=0", "(x-2)(x-6)=0"], [2, 6]),
        ],
        "words": [
            "連続した3つの正の整数があります。小さい方の2つの数の積が，3つの数の和より12大きいとき，これら3つの整数を求めなさい。",
            "長さ44cmのひもで長方形をつくり，その面積が112cm²になるようにします。このときの長方形のたてとよこの長さを求めなさい。",
            f"二次方程式 {T('x^2-ax+12=0')} の解の1つが3であるとき，{T('a')} の値と，他の解を求めなさい。",
        ],
        "word_ans": [
            (f"連続した3つの正の整数を {T('x,\\ x+1,\\ x+2')} とする。",
             ["x(x+1)=x+(x+1)+(x+2)+12", "x^2-2x-15=0", "(x+3)(x-5)=0"],
             f"{T('x')} は正の整数だから {T('x=5')}（{T('x=-3')} は合わない）", "5，6，7"),
            (f"たてを {T('x')} cm とすると，よこは {T('(22-x)')} cm。",
             ["x(22-x)=112", "x^2-22x+112=0", "(x-8)(x-14)=0"],
             f"{T('x=8,\\ 14')}（どちらも {T('0<x<22')} に合う）", "8cmと14cm"),
            (f"{T('x=3')} を代入する。",
             ["9-3a+12=0", "a=7", "x^2-7x+12=0", "(x-3)(x-4)=0"], "", f"{T('a=7')}，他の解 {T('x=4')}"),
        ],
        "p1": (-4, 48, 3),
        "g2": [(F(3), None), (F(1, 4), (-2, 4))],
        "g3": [(F(-1), None), (F(-1, 2), (-4, 2))],
        "fill": (f"関数 {T('y=ax^2')} のグラフは <span class='blank w'></span> とよばれる曲線で，"
                 f"<span class=blank></span> 軸について対称である。□をうめなさい。<small>（完答）</small>"),
        "fill_ans": "放物線，" + T("y") + "（軸）",
        "ranges": [(F(4), (1, 3), (4, 36)), (F(-2), (-3, 2), (-18, 0)), (F(1, 3), (-3, 6), (0, 12))],
    },
    {
        "eqs": [
            ("x^2-x-20=0", ["(x+4)(x-5)=0"], [-4, 5]),
            ("x^2+10x+21=0", ["(x+3)(x+7)=0"], [-3, -7]),
            ("x^2+12x+36=0", ["(x+6)^2=0"], [-6]),
            ("4x^2-20x=0", ["4x(x-5)=0"], [0, 5]),
            ("x^2=-7x", ["x^2+7x=0", "x(x+7)=0"], [0, -7]),
            ("2x^2-8x-24=0", ["x^2-4x-12=0", "(x+2)(x-6)=0"], [-2, 6]),
            ("x^2+3x-2=2(2x+5)", ["x^2+3x-2=4x+10", "x^2-x-12=0", "(x+3)(x-4)=0"], [-3, 4]),
        ],
        "words": [
            "連続した3つの正の整数があります。いちばん小さい数の2乗が，残りの2つの数の和より5大きいとき，これら3つの整数を求めなさい。",
            "正方形の土地があります。この土地のたてを3m長くし，よこを2m短くした長方形の面積は50m²になりました。もとの正方形の1辺の長さを求めなさい。",
            f"二次方程式 {T('x^2-6x+a=0')} の解の1つが {T('-2')} であるとき，{T('a')} の値と，他の解を求めなさい。",
        ],
        "word_ans": [
            (f"連続した3つの正の整数を {T('x,\\ x+1,\\ x+2')} とする。",
             ["x^2=(x+1)+(x+2)+5", "x^2-2x-8=0", "(x+2)(x-4)=0"],
             f"{T('x')} は正の整数だから {T('x=4')}（{T('x=-2')} は合わない）", "4，5，6"),
            (f"もとの1辺を {T('x')} m とする（{T('x>2')}）。",
             ["(x+3)(x-2)=50", "x^2+x-56=0", "(x+8)(x-7)=0"],
             f"{T('x>2')} だから {T('x=7')}（{T('x=-8')} は合わない）", "7m"),
            (f"{T('x=-2')} を代入する。",
             ["4+12+a=0", "a=-16", "x^2-6x-16=0", "(x+2)(x-8)=0"], "", f"{T('a=-16')}，他の解 {T('x=8')}"),
        ],
        "p1": (3, -18, -2),
        "g2": [(F(1, 2), None), (F(2), (-1, 2))],
        "g3": [(F(-3), None), (F(-1, 4), (-2, 4))],
        "fill": (f"関数 {T('y=ax^2')} のグラフは，{T('a>0')} のとき <span class=blank></span> に開き，"
                 f"{T('a<0')} のとき <span class=blank></span> に開く。□をうめなさい。<small>（完答）</small>"),
        "fill_ans": "上，下",
        "ranges": [(F(2), (2, 4), (8, 32)), (F(-3), (-2, 1), (-12, 0)), (F(1, 4), (-4, 2), (0, 4))],
    },
]

GRID2 = dict(ymin=-1, ymax=11, xlab=(-4, -2, 2, 4), ylab=(2, 4, 6, 8, 10))
GRID3 = dict(ymin=-13, ymax=1, xlab=(-4, -2, 2, 4), ylab=(-5, -10))


def coef(k):
    """y = kx² の TeX"""
    if k.denominator == 1:
        c = {1: "", -1: "-"}.get(k.numerator, str(k.numerator))
    else:
        c = ("-" if k < 0 else "") + f"\\dfrac{{{abs(k.numerator)}}}{{{k.denominator}}}"
    return f"y={c}x^2"


def dom_tex(d, v="x"):
    return f"{d[0]}\\leqq {v}\\leqq {d[1]}"


def dots(k, dom, g):
    lo, hi = dom or (-5, 5)
    return [p for p in range(lo, hi + 1) if (k * p**2).denominator == 1 and g["ymin"] <= k * p**2 <= g["ymax"]]


def check():
    x, a = sp.symbols("x a")

    def parse(s):
        s = s.replace("^2", "**2")
        s = re.sub(r"(\d)([xa(])", r"\1*\2", s)
        s = re.sub(r"x\(", "x*(", s).replace(")(", ")*(")
        left, right = s.split("=")
        return sp.sympify(left) - sp.sympify(right)

    for pt in PATTERNS:
        for eq, steps, sols in pt["eqs"]:
            assert set(sp.solve(parse(eq), x)) == set(sols), eq
            for st in steps:
                assert set(sp.solve(parse(st), x)) == set(sols), (eq, st)
        px, py, k = pt["p1"]
        assert k * px**2 == py
        for k, (lo, hi), ans in pt["ranges"]:
            vals = [k * lo**2, k * hi**2] + ([F(0)] if lo <= 0 <= hi else [])
            assert (min(vals), max(vals)) == ans, (k, lo, hi)
        for curves, g in ((pt["g2"], GRID2), (pt["g3"], GRID3)):
            for k, dom in curves:
                ps = dots(k, dom, g)
                assert len(ps) >= 3, (k, dom)
                if dom:                         # 変域のはしが整数の点で方眼に入る
                    assert dom[0] in ps and dom[1] in ps, (k, dom)
    # 文章題
    p1, p2 = PATTERNS
    assert set(sp.solve(x * (x + 1) - (3 * x + 3 + 12), x)) == {5, -3} and 5 * 6 == 5 + 6 + 7 + 12
    assert set(sp.solve(x * (22 - x) - 112, x)) == {8, 14} and 2 * (8 + 14) == 44
    assert sp.solve(9 - 3 * a + 12, a) == [7] and set(sp.solve(x**2 - 7 * x + 12, x)) == {3, 4}
    assert set(sp.solve(x**2 - (2 * x + 3 + 5), x)) == {4, -2} and 4**2 == 5 + 6 + 5
    assert set(sp.solve((x + 3) * (x - 2) - 50, x)) == {7, -8} and 10 * 5 == 50
    assert sp.solve(4 + 12 + a, a) == [-16] and set(sp.solve(x**2 - 6 * x - 16, x)) == {-2, 8}
    # 2つのパターンで同じ問題がないか
    assert not {q for q, _, _ in p1["eqs"]} & {q for q, _, _ in p2["eqs"]}
    print("確認OK：解・途中の式・文章題・変域・グラフの点")


# ---------- グラフ ----------
def graph(g, cell, curves=()):
    """方眼（x は −5〜5）。単位は mm。curves があれば答えのグラフを重ねる"""
    xmin, xmax, ymin, ymax = -5, 5, g["ymin"], g["ymax"]
    w, h = (xmax - xmin) * cell, (ymax - ymin) * cell
    X = lambda v: (float(v) - xmin) * cell
    Y = lambda v: (ymax - float(v)) * cell
    o = [f'<svg class=gr width="{w + .4}mm" height="{h + .4}mm" viewBox="-.2 -.2 {w + .4} {h + .4}">']
    for i in range(xmin, xmax + 1):
        o.append(f'<line x1="{X(i)}" y1="0" x2="{X(i)}" y2="{h}" stroke="#777" stroke-width=".14"/>')
    for j in range(ymin, ymax + 1):
        o.append(f'<line x1="0" y1="{Y(j)}" x2="{w}" y2="{Y(j)}" stroke="#777" stroke-width=".14"/>')
    o.append(f'<line x1="0" y1="{Y(0)}" x2="{w}" y2="{Y(0)}" stroke="#111" stroke-width=".42"/>')
    o.append(f'<line x1="{X(0)}" y1="0" x2="{X(0)}" y2="{h}" stroke="#111" stroke-width=".42"/>')

    def label(px, py, t, anchor="middle", size=2.6, extra=""):
        o.append(f'<text x="{px}" y="{py}" font-size="{size}" text-anchor="{anchor}" {extra} '
                 f'stroke="#fff" stroke-width=".7" paint-order="stroke">{t}</text>')

    math = 'font-family="KaTeX_Math" font-style="italic"'
    label(w - .6, Y(0) - .9, "x", "end", 3, math)
    label(X(0) + .9, 3, "y", "start", 3, math)
    # 0 の下に数字を置く。y の数字は y 軸の左
    label(X(0) - 1, Y(0) + 3.1, "O")
    for v in g["xlab"]:
        label(X(v), Y(0) + 3.1, str(v).replace("-", "−"))
    for v in g["ylab"]:
        label(X(0) - .8, Y(v) + .9, str(v).replace("-", "−"), "end")

    colors = ("#b4232c", "#1f5fbf")
    for idx, (k, dom) in enumerate(curves):
        lo, hi = dom or (-5, 5)
        pts = []
        for i in range(501):
            vx = lo + (hi - lo) * i / 500
            vy = float(k) * vx * vx
            if ymin <= vy <= ymax:
                pts.append(f"{X(vx):.2f},{Y(vy):.2f}")
        c = colors[idx]
        o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{c}" stroke-width=".5"/>')
        ds = dots(k, dom, g)
        for p in ds:
            o.append(f'<circle cx="{X(p)}" cy="{Y(k * p**2)}" r=".65" fill="{c}"/>')
        # 名札：①は左はしの点、②は右はしの点のそば（方眼からはみ出さないように内側へ）
        lx = ds[0] if idx == 0 else ds[-1]
        inside = abs(lx) >= 3
        right = (lx < 0) == inside              # 点の右に置くか
        label(X(lx) + (1.1 if right else -1.1), Y(k * lx**2) + (3 if k < 0 else 1.2), NO[idx], "start" if right else "end", 3.2,
              f'style="fill:{c};font-weight:700"')
    o.append("</svg>")
    return "".join(o)


# ---------- ページ ----------
CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; font-size: 9.8pt; }
.page { width: 210mm; height: 297mm; padding: 9mm 12mm 11mm; page-break-after: always;
        display: flex; flex-direction: column; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.katex { font-size: 1.12em; }
.head { display: flex; align-items: baseline; white-space: nowrap; border-bottom: 1pt solid #111; padding-bottom: 1.6mm; }
.head b { font-size: 12.5pt; }
.head .sub { font-size: 8.8pt; margin-left: 2mm; color: #222; }
.head .cl { font-size: 8.8pt; margin-left: 2.5mm; }
.head .u { display: inline-block; border-bottom: .7pt solid #111; }
.head .pts { margin-left: auto; font-size: 9pt; }
.head .kotae { margin-left: auto; font-weight: 700; color: #b4232c; font-size: 11pt; }
.cols { flex: 1; min-height: 0; display: grid; grid-template-columns: 1fr 1fr; margin-top: 2.5mm; }
.col { display: flex; flex-direction: column; min-height: 0; }
.col:first-child { padding-right: 4.5mm; border-right: .7pt solid #111; }
.col:last-child { padding-left: 4.5mm; }
.big { font-weight: 700; display: flex; align-items: center; gap: 1.6mm; white-space: nowrap; }
.big .box { display: inline-flex; width: 5mm; height: 5mm; border: .8pt solid #111; align-items: center;
            justify-content: center; font-size: 9.5pt; }
.big small { font-size: 8pt; font-weight: 400; }
.big .pill { font-size: 7pt; font-weight: 400; border: .7pt solid #111; border-radius: 3mm; padding: .1mm 1.6mm; margin-left: 1mm; }
.no { font-size: 7.6pt; flex: none; width: 6.5mm; padding-top: .7mm; text-align: center; }
/* 左列 */
.eqs { display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: 1fr; flex: 0 0 90mm; margin-top: 1.5mm; }
.e { display: flex; align-items: flex-start; font-size: 10pt; white-space: nowrap; }
.sec2 { margin-top: 2mm; }
.word { flex: 1; min-height: 0; display: grid; grid-template-rows: repeat(3, 1fr); margin-top: 1.5mm; }
.wq { display: flex; line-height: 1.75; }
/* 右列 */
.r1 { display: flex; line-height: 1.75; }
.ln { border-bottom: .9pt solid #111; width: 42mm; margin-left: auto; height: 5.5mm; }
.gq { display: flex; justify-content: space-between; margin-top: 3mm; }
.gtext { width: 31mm; line-height: 1.75; }
.gtext .eq { margin-top: 2.2mm; display: flex; align-items: center; gap: .8mm; font-size: 10pt; white-space: nowrap; }
.gtext .dm { margin-left: 3.5mm; font-size: 10pt; white-space: nowrap; }
.gtext .care { margin-top: 3mm; font-size: 8pt; white-space: nowrap; }
.gr { flex: none; }
.gr text { font-family: 'Noto Sans CJK JP'; }
.fill { margin-top: 3mm; }
.fill small { font-size: 7pt; }
.blank { display: inline-block; width: 9mm; height: 5.6mm; border: .7pt solid #111; vertical-align: middle; }
.blank.w { width: 23mm; }
.rs { flex: 1; min-height: 0; display: grid; grid-template-rows: repeat(3, 1fr); margin-top: 1.5mm; }
.rq { display: flex; flex-direction: column; justify-content: space-between; padding-bottom: 3.5mm; }
.rq > div:first-child { display: flex; line-height: 1.75; }
/* こたえ */
.ansp { font-size: 8.8pt; line-height: 1.55; }
.ansp .katex { font-size: 1.08em; }
.res { font-weight: 700; color: #b4232c; }
.st { display: block; color: #333; }
.aeq { display: grid; grid-template-columns: 1fr 1fr; column-gap: 3mm; margin: 1.5mm 0 3mm; }
.ar { display: flex; padding: 1mm 0; border-bottom: .4pt solid #ddd; }
.ar .no { padding-top: .3mm; }
.ar > div:last-child { min-width: 0; flex: 1; }
.ag { display: flex; gap: 3mm; padding: 1.2mm 0; border-bottom: .4pt solid #ddd; align-items: flex-start; }
.ag .pts { font-size: 8pt; line-height: 1.5; margin-top: 1.5mm; }
"""


def head(i, ans=False):
    left = (f"<b>中3数学 定期テスト対策 {NO[i]}</b><span class=sub>二次方程式・関数 {T('y=ax^2')}</span>")
    if ans:
        return f"<div class=head>{left}<span class=kotae>こたえ</span></div>"
    return (f"<div class=head>{left}<span class=cl>（　）組（　）番　名前 <span class=u style='width:33mm'></span></span>"
            f"<span class=pts><span class=u style='width:9mm'></span>／60点</span></div>")


def big(n, text, small="", pill=""):
    return (f"<div class=big><span class=box>{n}</span>{text}"
            f"{f'<small>{small}</small>' if small else ''}{f'<span class=pill>{pill}</span>' if pill else ''}</div>")


def gq(no, curves, g):
    items = ""
    for i, (k, dom) in enumerate(curves):
        items += f"<div class=eq>{NO[i]}{T(coef(k))}</div>"
        if dom:
            items += f"<div class=dm>{T('(' + dom_tex(dom) + ')')}</div>"
    return (f"<div class=gq><div class=gtext><span class=no style='font-size:7.6pt;display:inline-block;width:5.5mm'>({no})</span>"
            f"次のグラフを右の座標平面にかきなさい。{items}"
            f"<div class=care>（※ていねいにかくこと。）</div></div>{graph(g, 4.5)}</div>")


def page_q(i, pt):
    eqs = "".join(f"<div class=e><span class=no>({n + 1})</span>{T(q)}</div>" for n, (q, _, _) in enumerate(pt["eqs"]))
    words = "".join(f"<div class=wq><span class=no>({n + 1})</span><div>{q}</div></div>" for n, q in enumerate(pt["words"]))
    px, py, _ = pt["p1"]
    rs = ""
    for n, (k, d, _) in enumerate(pt["ranges"]):
        rs += (f"<div class=rq><div><span class=no>({n + 5})</span>"
               f"<div>{T(coef(k))} で，{T(dom_tex(d))} のときの {T('y')} の変域を求めなさい。</div></div>"
               f"<div class=ln></div></div>")
    return f"""<div class=page>{head(i)}<div class=cols>
<div class=col>{big(1, "次の二次方程式を解きなさい。", "（×3点）")}<div class=eqs>{eqs}</div>
<div class=sec2>{big(2, "次の問いに答えなさい。", "（×4点）", "※途中の式も書くこと")}</div><div class=word>{words}</div></div>
<div class=col>{big(3, "次の問いに答えなさい。", "（×3点）")}
<div class=r1 style="margin-top:1.5mm"><span class=no>(1)</span><div>{T('y')} は {T('x')} の2乗に比例し，{T(f'x={px}')} のとき {T(f'y={py}')} である。{T('y')} を {T('x')} の式で表しなさい。</div></div><div class=ln></div>
{gq(2, pt["g2"], GRID2)}{gq(3, pt["g3"], GRID3)}
<div class="r1 fill"><span class=no>(4)</span><div>{pt["fill"]}</div></div>
<div class=rs>{rs}</div></div>
</div></div>"""


def sols(v):
    return "，".join(T(f"x={s}") for s in v)


def page_a(i, pt):
    rows = ""
    for n, (q, steps, s) in enumerate(pt["eqs"]):
        mid = "".join(f"<span class=st>{T(t)}</span>" for t in steps)
        rows += f"<div class=ar><span class=no>({n + 1})</span><div><span class=st>{T(q)}</span>{mid}<span class=res>{sols(s)}</span></div></div>"
    ws = ""
    for n, (lead, steps, tail, res) in enumerate(pt["word_ans"]):
        mid = "".join(f"<span class=st>{T(t)}</span>" for t in steps)
        ws += (f"<div class=ar><span class=no>({n + 1})</span><div>{lead}{mid}"
               f"{f'<span class=st>{tail}</span>' if tail else ''}<span class=res>{res}</span></div></div>")

    def ag(no, curves, g):
        eqs = "".join(f"<div>{NO[j]} {T(coef(k))}" + (f"（{T(dom_tex(dom))}）" if dom else "") + "</div>"
                      for j, (k, dom) in enumerate(curves))
        pts = ""
        for j, (k, dom) in enumerate(curves):
            s = "，".join(f"({str(p).replace('-', '−')}, {str(k * p**2).replace('-', '−')})" for p in dots(k, dom, g))
            pts += f"<div>{NO[j]} {s}</div>"
        return (f"<div class=ag>{graph(g, 3.5, curves)}<div><span class=no style='display:inline-block'>({no})</span>"
                f"{eqs}<div class=pts>通る点<br>{pts}</div></div></div>")

    rs = ""
    for n, (k, (lo, hi), (a, b)) in enumerate(pt["ranges"]):
        if lo <= 0 <= hi:
            far = lo if abs(lo) > abs(hi) else hi
            why = f"{T('x=0')} をふくむので {'最大' if k < 0 else '最小'}は {T('y=0')}。0 から遠い {T(f'x={far}')} のとき {T(f'y={k * far**2}')}。"
        else:
            why = f"{T(f'x={lo}')} のとき {T(f'y={a}')}，{T(f'x={hi}')} のとき {T(f'y={b}')}。"
        rs += (f"<div class=ar><span class=no>({n + 5})</span><div><span class=st>{T(coef(k))}（{T(dom_tex((lo, hi)))}）</span>"
               f"<span class=st>{why}</span><span class=res>{T(f'{a}' + chr(92) + f'leqq y' + chr(92) + f'leqq {b}')}</span></div></div>")
    px, py, k = pt["p1"]
    return f"""<div class="page ansp">{head(i, True)}<div class=cols>
<div class=col>{big(1, "次の二次方程式を解きなさい。")}<div class=aeq>{rows}</div>
{big(2, "次の問いに答えなさい。")}<div style="margin-top:1mm">{ws}</div></div>
<div class=col>{big(3, "次の問いに答えなさい。")}
<div class=ar style="margin-top:1mm"><span class=no>(1)</span><div>{T('y=ax^2')} に代入。<span class=st>{T(f'{py}=a\\times({px})^2')}　より　{T(f'a={k}')}</span><span class=res>{T(coef(F(k)))}</span></div></div>
{ag(2, pt["g2"], GRID2)}{ag(3, pt["g3"], GRID3)}
<div class=ar><span class=no>(4)</span><div class=res>{pt["fill_ans"]}</div></div>
{rs}</div></div></div>"""


if __name__ == "__main__":
    check()
    write_pdfs([
        (doc(CSS, "".join(page_q(i, p) for i, p in enumerate(PATTERNS))), f"{FILE}.pdf"),
        (doc(CSS, "".join(page_a(i, p) for i, p in enumerate(PATTERNS))), f"{FILE}_ans.pdf"),
    ])
