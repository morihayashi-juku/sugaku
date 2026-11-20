"""高2 数学Ⅱ 図形と方程式「円の方程式」定期テスト対策（11/20 金）
学校のプリント（最新数学Ⅱ 第3章 No.13・No.14）の類題。A3 両面＝1パターン2ページ（1ページの中は左右2列）。
No.1 ＝ 中心と半径 ⇄ 方程式、通る点・接する円、直径の両端（No.13・練習20 の類題）
No.2 ＝ x²+y²+lx+my+n=0 の表す図形（平方完成・点・図形なし）、円を表す k の範囲（No.14 の類題）
問題（pdf/k2_en_teiki_1.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
答えは SymPy で確認。実行：cd tools && python3 k2_en_teiki.py
"""
import math
import pathlib
import sys

import sympy as sp

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from texlib import _dist  # noqa: E402

X, Y = sp.symbols("x y")
OUT = pathlib.Path(__file__).resolve().parent.parent / "pdf"
NAME = "k2_en_teiki_1"


# ---------- 式の書き方 ----------
def sq(r2):
    """r^2 → r を簡単にした TeX"""
    k = 1
    for i in range(math.isqrt(r2), 0, -1):
        if r2 % (i * i) == 0:
            k = i
            break
    m = r2 // (k * k)
    if m == 1:
        return str(k)
    return f"{k}\\sqrt{{{m}}}" if k > 1 else f"\\sqrt{{{m}}}"


def lin(v, a):
    """(v-a)^2 の TeX。a=0 なら v^2"""
    if a == 0:
        return f"{v}^2"
    return f"({v}{'-' if a > 0 else '+'}{abs(a)})^2"


def std(a, b, r2):
    return f"{lin('x', a)}+{lin('y', b)}={r2}"


def poly(terms):
    """[(係数, 'x^2'), ...] → TeX（係数0は省く）"""
    out = ""
    for c, t in terms:
        if c == 0:
            continue
        sgn = "-" if c < 0 else "+"
        mag = abs(c)
        body = (t if mag == 1 and t else f"{mag}{t}")
        out += (("-" if c < 0 else "") if out == "" else sgn) + body
    return out or "0"


def gen(l, m, n):
    return poly([(1, "x^2"), (1, "y^2"), (l, "x"), (m, "y"), (n, "")]) + "=0"


def check_std_gen(a, b, r2, l, m, n):
    lhs = sp.expand((X - a) ** 2 + (Y - b) ** 2 - r2)
    assert lhs == sp.expand(X**2 + Y**2 + l * X + m * Y + n), (a, b, r2, l, m, n)


def pt(a, b):
    return f"({a},\\,{b})"


def M(s):
    return f"${s}$"


def ans(s, w=38):
    return f'<span class="ans" style="--w:{w}mm">{s}</span>'


def work(s):
    return f'<div class="work">{s}</div>'


def it(no, prob, body, h=None):
    """問題 → （計算スペース。こたえでは途中式）→ いちばん下に答えのらん"""
    i = body.find('<div class="work">')
    a_part, w_part = (body[:i], body[i:]) if i >= 0 else (body, "")
    if a_part.startswith("<br>"):
        a_part = a_part[4:]
    return (f'<div class="it"><div class="q"><span class="no">({no})</span>{prob}</div>'
            f'{w_part}<div class="a">{a_part}</div></div>')


def grid(cls, items, rows, weight=None):
    """rows＝行の数。列の高さの余りを weight（なければ rows）の割合で分ける"""
    return f'<div class="{cls}" style="--g:{weight or rows}">{"".join(items)}</div>'


def sec(n, title):
    return f'<h3><span class="sn">{n}</span>{title}</h3>'


# ---------- No.1 ----------
def page1():
    # [1] 中心・半径 → 方程式
    q1 = [((3, 2), 16, "4"), ((-1, 4), 6, "\\sqrt{6}"), ((2, -5), 1, "1"),
          ((0, -3), 8, "2\\sqrt{2}"), ((0, 0), 25, "5"), ((-4, 0), 3, "\\sqrt{3}")]
    s1 = []
    for i, ((a, b), r2, rs) in enumerate(q1):
        assert sq(r2) == rs
        cen = "原点" if (a, b) == (0, 0) else M(pt(a, b))
        s1.append(it(i + 1, f"中心 {cen}、半径 {M(rs)}",
                     "<br>" + ans(M(std(a, b, r2)), 56)
                     + work(M(f"{lin('x', a)}+{lin('y', b)}=({rs})^2" if not rs.isdigit() else f"{lin('x', a)}+{lin('y', b)}={rs}^2")), 30))

    # [2] 方程式 → 中心・半径
    q2 = [(2, 7, 9), (-5, 1, 16), (0, -6, 12), (-1, -3, 7), (0, 0, 50), (3, 0, 20)]
    s2 = []
    for i, (a, b, r2) in enumerate(q2):
        rs = sq(r2)
        w = f"r^2={r2}\\ より\\ r=" + (f"\\sqrt{{{r2}}}={rs}" if rs != f"\\sqrt{{{r2}}}" and not rs.isdigit() else rs)
        s2.append(it(i + 1, M(std(a, b, r2)),
                     "<br>中心 " + ans(M(pt(a, b)), 20) + "　半径 " + ans(M(rs), 14) + work(M(w).replace("より", "\\text{より}")), 30))

    # [3] 通る点・接する
    a, b, px, py = 2, 1, 5, 5
    r2a = (px - a) ** 2 + (py - b) ** 2
    a2, b2 = -3, 2
    r2b = a2**2 + b2**2
    a3, b3 = 4, -3
    a4, b4 = -2, 5
    assert (r2a, r2b) == (25, 13)
    s3 = [
        it(1, f"中心が点 {M(pt(a, b))} で、点 {M(pt(px, py))} を通る円",
           "<br>" + ans(M(std(a, b, r2a)), 50)
           + work(f"半径は中心と点 {M(pt(px, py))} の距離<br>" + M(f"r^2=({px}-{a})^2+({py}-{b})^2=9+16=25")), 30),
        it(2, f"中心が点 {M(pt(a2, b2))} で、原点を通る円",
           "<br>" + ans(M(std(a2, b2, r2b)), 50)
           + work(M(f"r^2=(-3-0)^2+(2-0)^2=9+4=13")), 30),
        it(3, f"中心が点 {M(pt(a3, b3))} で、{M('x')}軸に接する円",
           "<br>" + ans(M(std(a3, b3, b3 * b3)), 50)
           + work(f"{M('x')}軸に接する → 半径＝中心から {M('x')}軸までの距離＝{M(f'|{b3}|')}＝{M(abs(b3))}"), 30),
        it(4, f"中心が点 {M(pt(a4, b4))} で、{M('y')}軸に接する円",
           "<br>" + ans(M(std(a4, b4, a4 * a4)), 50)
           + work(f"{M('y')}軸に接する → 半径＝中心から {M('y')}軸までの距離＝{M(f'|{a4}|')}＝{M(abs(a4))}"), 30),
    ]

    # [4] 直径の両端
    D = [((1, 2), (5, 6)), ((-3, 1), (1, -5)), ((-2, -1), (4, 3))]
    s4 = []
    for i, ((x1, y1), (x2, y2)) in enumerate(D):
        cx, cy = sp.Rational(x1 + x2, 2), sp.Rational(y1 + y2, 2)
        assert cx.is_integer and cy.is_integer
        cx, cy = int(cx), int(cy)
        r2 = (x1 - cx) ** 2 + (y1 - cy) ** 2
        assert r2 == (x2 - cx) ** 2 + (y2 - cy) ** 2
        rs = sq(r2)
        wk = (M(f"\\left(\\dfrac{{{x1}+{'(' + str(x2) + ')' if x2 < 0 else x2}}}{{2}},\\ \\dfrac{{{y1}+{'(' + str(y2) + ')' if y2 < 0 else y2}}}{{2}}\\right)={pt(cx, cy)}")
              + "<br>" + M(f"r=\\mathrm{{CA}}=\\sqrt{{({x1}{'-' if cx >= 0 else '+'}{abs(cx)})^2+({y1}{'-' if cy >= 0 else '+'}{abs(cy)})^2}}=\\sqrt{{{r2}}}" + ("" if rs == f"\\sqrt{{{r2}}}" else f"={rs}")))
        s4.append(it(i + 1, f"$\\mathrm{{A}}{pt(x1, y1)},\\ \\mathrm{{B}}{pt(x2, y2)}$",
                     "<br>中心 " + ans(M(pt(cx, cy)), 24) + "　半径 " + ans(M(rs), 20)
                     + "<br>方程式 " + ans(M(std(cx, cy, r2)), 56) + work(wk), 40))

    return f"""
<section class="page">
{header("No.1", "円の方程式")}
<div class="cols">
<div class="col">
<div class="box">
<div class="boxt">ポイント</div>
・中心 $(a,\\,b)$、半径 $r$ の円　→　$(x-a)^2+(y-b)^2=r^2$<br>
・原点が中心、半径 $r$ の円　→　$x^2+y^2=r^2$<br>
・$(x-a)^2+(y-b)^2=r^2$ の中心は $(a,\\,b)$　<span class="note">（かっこの中と符号が逆になる）</span><br>
・2点 A, B を直径の両端とする円 → 中心は <b>AB の中点</b>、半径は <b>中心と A の距離</b><br>
・$x$軸に接する円の半径＝中心の $y$座標の絶対値<br>・$y$軸に接する円の半径＝中心の $x$座標の絶対値
</div>
{sec(1, "次のような円の方程式を求めよ。")}
{grid("grid2", s1, 3)}
{sec(2, "次の方程式が表す円の中心の座標と半径を求めよ。")}
{grid("grid2", s2, 3)}
</div>
<div class="col">
{sec(3, "次のような円の方程式を求めよ。")}
{grid("grid2", s3, 2)}
{sec(4, "次の2点 A, B を結ぶ線分を直径とする円について、中心の座標と半径を求めよ。また、その方程式を求めよ。")}
<div class="fig">{diam_svg()}</div>
{grid("grid1", s4, 3, 3.6)}
</div>
</div>
</section>"""


def diam_svg():
    W, H = 260, 120
    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<circle cx="105" cy="60" r="46" fill="none" stroke="#000" stroke-width="1.3"/>
<line x1="68" y1="33" x2="142" y2="87" stroke="#000" stroke-width="1"/>
<circle cx="68" cy="33" r="2.5"/><circle cx="142" cy="87" r="2.5"/><circle cx="105" cy="60" r="2.5"/>
<text x="56" y="28" class="pl">A</text><text x="148" y="98" class="pl">B</text>
<text x="96" y="76" class="pl">C</text>
<text x="160" y="40" class="sm">C は AB の中点</text>
<text x="160" y="56" class="sm">半径 r＝CA</text>
</svg>"""


# ---------- No.2 ----------
def complete(l, m, n):
    a, b = sp.Rational(-l, 2), sp.Rational(-m, 2)
    assert a.is_integer and b.is_integer
    a, b = int(a), int(b)
    rhs = a * a + b * b - n
    return a, b, rhs


def cs_work(l, m, n):
    """平方完成の途中式（2行）"""
    a, b, rhs = complete(l, m, n)
    gx = poly([(1, "x^2"), (l, "x")])
    gy = poly([(1, "y^2"), (m, "y")])
    left1 = (f"({gx})" if l else "x^2") + "+" + (f"({gy})" if m else "y^2")
    line1 = f"{left1}={-n}"
    px = f"{lin('x', a)}-{a * a}" if a else "x^2"
    py = f"{lin('y', b)}-{b * b}" if b else "y^2"
    line2 = f"{px}+{py}={-n}"
    line3 = f"{lin('x', a)}+{lin('y', b)}={rhs}"
    return a, b, rhs, [line1, line2, line3]


def page2():
    # [5] 一般形 → 中心・半径
    q5 = [(-4, 6, -3), (2, -8, 8), (-10, 0, 0), (0, 6, -1), (-2, 4, -15), (8, -2, 9)]
    s5 = []
    for i, (l, m, n) in enumerate(q5):
        a, b, rhs, lines = cs_work(l, m, n)
        assert rhs > 0
        check_std_gen(a, b, rhs, l, m, n)
        s5.append(it(i + 1, M(gen(l, m, n)),
                     "<br>中心 " + ans(M(pt(a, b)), 20) + "　半径 " + ans(M(sq(rhs)), 14)
                     + work("<br>".join(M(s) for s in lines)), 36))

    # [6] 標準形 → 一般形
    q6 = [(-3, 1, 4), (2, 5, 10)]
    s6 = []
    for i, (a, b, r2) in enumerate(q6):
        l, m, n = -2 * a, -2 * b, a * a + b * b - r2
        check_std_gen(a, b, r2, l, m, n)
        ex = poly([(1, "x^2"), (l, "x"), (a * a, "")]) + "+" + poly([(1, "y^2"), (m, "y"), (b * b, "")]) + f"={r2}"
        s6.append(it(i + 1, M(std(a, b, r2)), "<br>" + ans(M(gen(l, m, n)), 62) + work("展開すると　" + M(ex)), 20))

    # [7] どのような図形か（円・点・なし）
    q7 = [(-6, 2, 10), (4, -2, 9), (-8, 4, 11), (2, 6, 10)]
    s7 = []
    for i, (l, m, n) in enumerate(q7):
        a, b, rhs, lines = cs_work(l, m, n)
        if rhs > 0:
            res = f"中心 {M(pt(a, b))}、半径 {M(sq(rhs))} の円"
            why = ""
        elif rhs == 0:
            res = f"点 {M(pt(a, b))}"
            why = "<br>" + M(f"{lin('x', a)}\\geqq 0,\\ {lin('y', b)}\\geqq 0") + " だから<br>" + M(f"x{'-' if a > 0 else '+'}{abs(a)}=0,\\ y{'-' if b > 0 else '+'}{abs(b)}=0")
        else:
            res = "表す図形はない"
            why = "<br>（左辺）" + M("\\geqq 0") + " なので、右辺が " + M(f"{rhs}") + " に<br>なる点 " + M("(x,\\,y)") + " はない"
        s7.append(it(i + 1, M(gen(l, m, n)), "<br>" + ans(res, 52) + work("<br>".join(M(s) for s in lines) + why), 36))
    kinds = [complete(*q)[2] for q in q7]
    assert [k > 0 for k in kinds].count(True) == 1 and kinds.count(0) == 2 and [k < 0 for k in kinds].count(True) == 1

    # [8] k の範囲・半径
    l, m = -4, 2
    a, b = 2, -1
    lim = a * a + b * b  # 5 - k > 0
    k_r2 = lim - 4
    assert sp.solve(sp.Eq(lim - sp.Symbol("k"), 4)) == [k_r2]
    s8 = [
        it(1, "円を表すような定数 $k$ の値の範囲を求めよ。",
           "<br>" + ans(M(f"k<{lim}"), 30)
           + work(M("(x-2)^2-4+(y+1)^2-1=-k") + "<br>" + M(f"(x-2)^2+(y+1)^2={lim}-k") + "<br>円を表すのは　" + M(f"{lim}-k>0") + "　のとき"), 30),
        it(2, "半径が $2$ の円を表すような定数 $k$ の値を求めよ。また、そのときの円の中心の座標を求めよ。",
           "<br>" + "$k=$ " + ans(M(k_r2), 18) + "　中心 " + ans(M(pt(a, b)), 24)
           + work(M(f"{lim}-k=2^2") + "　より　" + M(f"k={k_r2}")), 26),
    ]

    return f"""
<section class="page">
{header("No.2", "$x^2+y^2+lx+my+n=0$ の表す図形")}
<div class="cols">
<div class="col">
<div class="box">
<div class="boxt">ポイント</div>
・円の方程式は　$x^2+y^2+lx+my+n=0$　の形にも表される（$l,\\,m,\\,n$ は定数）。<br>
・$x$ と $y$ でそれぞれ<b>平方完成</b>して、$(x-a)^2+(y-b)^2=k$ の形にする。
<div class="cs">
$(x^2+4x)+(y^2-6y)=12$<br>
$(x+2)^2-2^2+(y-3)^2-3^2=12$　<br><span class="note">↑ $x$・$y$ の係数の<b>半分</b>を使ってかっこの2乗にし、その<b>2乗</b>を引く</span><br>
$(x+2)^2+(y-3)^2=25$
</div>
・右辺 $k$ が　<b>正</b> → 中心 $(a,\\,b)$、半径 $\\sqrt{{k}}$ の円　／　<b>0</b> → 点 $(a,\\,b)$　／　<b>負</b> → 表す図形はない
</div>
{sec(5, "次の方程式はどのような円を表すか。中心の座標と半径を求めよ。")}
{grid("grid2 tight", s5, 3)}
</div>
<div class="col">
{sec(6, "次の円の方程式を、$x^2+y^2+lx+my+n=0$ の形で表せ。")}
{grid("grid1", s6, 2, 1.2)}
{sec(7, "次の方程式はどのような図形を表すか。")}
{grid("grid2 tight", s7, 2, 2.6)}
{sec(8, "方程式 $x^2+y^2-4x+2y+k=0$ について、次の問いに答えよ。")}
{grid("grid1", s8, 2)}
</div>
</div>
</section>"""


def header(no, title):
    return f"""<div class="hd"><div class="ht"><span class="tag">数学Ⅱ 図形と方程式 定期テスト対策 {no}</span>{title}<span class="key">解答</span></div>
<div class="nm">名前（　　　　　　　　　）</div></div>"""


KATEX = _dist()
CSS = """
@page { size: A3; margin: 0; }
body { margin:0; font-family: "Noto Sans CJK JP", sans-serif; font-size: 11.5pt; color:#111; }
.page { width:297mm; height:420mm; box-sizing:border-box; padding:13mm 14mm; page-break-after: always; overflow:hidden; }
.hd { border-bottom: 2px solid #333; padding-bottom: 2mm; margin-bottom: 4mm; display:flex; justify-content:space-between; align-items:flex-end; }
.ht { font-size: 16pt; font-weight: 700; white-space:nowrap; }
.tag { display:inline-block; font-size:10pt; background:#333; color:#fff; padding:1px 8px; margin-right:8px; border-radius:3px; vertical-align:middle; }
.key { display:inline-block; font-size:10pt; border:1.5px solid #c00; color:#c00; padding:0 6px; margin-left:8px; border-radius:3px; vertical-align:middle; }
.nm { font-size: 11pt; white-space:nowrap; }
.page { display:flex; flex-direction:column; }
.cols { flex:1; min-height:0; display:grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); gap: 0 9mm; }
.col { display:flex; flex-direction:column; min-height:0; }
.col .grid1, .col .grid2 { flex: var(--g) 1 0; grid-auto-rows: 1fr; }
.it { display:flex; flex-direction:column; border-bottom: 1px dotted #bbb; padding-bottom: 1.5mm; }
.it .a { margin-top:auto; padding-top: 1mm; }
.tight .q { white-space: nowrap; }
.tight .q .katex { font-size: 1.04em; }
.tight .work { margin-left: 1mm; font-size: 9pt; }
.tight .work .katex { font-size: 1.0em; }
.col + .col { border-left: 1px solid #999; padding-left: 9mm; }
.box { border: 1.3px solid #555; border-radius: 4px; padding: 2.5mm 4mm; margin-bottom: 3mm; background:#f7f7f7; line-height:1.85; font-size:10.5pt; }
.boxt { font-weight:700; margin-bottom:1mm; }
.note { font-size: 9pt; color:#555; }
.cs { margin: 1.5mm 0 1.5mm 6mm; padding: 1.5mm 3mm; border-left: 3px solid #999; background:#fff; }
h3 { font-size: 11.5pt; margin: 4mm 0 2mm; font-weight:700; line-height:1.6; }
.sn { display:inline-block; width:6.5mm; height:6.5mm; line-height:6.5mm; text-align:center; background:#333; color:#fff; border-radius:3px; margin-right:2mm; font-size:10.5pt; }
.grid1, .grid2 { display:grid; gap: 2.5mm 6mm; margin-left: 2mm; }
.grid2 { grid-template-columns: minmax(0,1fr) minmax(0,1fr); }
.it { line-height: 1.9; }
.no { margin-right: 2mm; }
.ans { color:#c00; font-weight:700; border-bottom: 1px solid #c00; padding: 0 2px; }
.ans .katex { color:#c00; }
.work { color:#c33; font-size: 9.5pt; line-height:1.9; margin: 0.5mm 0 0 3mm; }
.fig { text-align:center; margin: -1mm 0 1mm; }
svg text { font-family: "Noto Sans CJK JP", sans-serif; }
.pl { font-size: 12px; } .sm { font-size: 10px; }
.mondai .ans, .mondai .ans .katex { color: transparent !important; border-bottom-color:#333; }
.mondai .ans { display:inline-block; width:var(--w,38mm); height:1.35em; overflow:hidden; white-space:nowrap; vertical-align:bottom; }
.mondai .work { visibility: hidden; }
.mondai .key { display:none; }
"""

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="file://{KATEX}/katex.min.css">
<script src="file://{KATEX}/katex.min.js"></script>
<script src="file://{KATEX}/contrib/auto-render.min.js"></script>
<style>{CSS}</style></head><body class="__MODE__">
{page1()}{page2()}
<script>
renderMathInElement(document.body, {{delimiters:[{{left:"$", right:"$", display:false}}], throwOnError:true}});
document.body.setAttribute("data-done","1");
</script>
</body></html>"""

from playwright.sync_api import sync_playwright  # noqa: E402

with sync_playwright() as pw:
    br = pw.chromium.launch()
    for mode, fname in [("mondai", f"{NAME}.pdf"), ("kaitou", f"{NAME}_ans.pdf")]:
        hp = pathlib.Path(f"/tmp/{NAME}_{mode}.html")
        hp.write_text(html.replace("__MODE__", mode), encoding="utf-8")
        pg = br.new_page()
        pg.goto(f"file://{hp.resolve()}")
        pg.wait_for_selector("body[data-done]")
        pg.evaluate("document.fonts.ready")
        info = pg.evaluate("""(()=>{const its=[...document.querySelectorAll('.it')];
          const over=its.filter(e=>e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1).map(e=>e.querySelector('.q').innerText.slice(0,12));
          const free=its.map(e=>{const q=e.querySelector('.q').getBoundingClientRect(),a=e.querySelector('.a').getBoundingClientRect();return Math.round((a.top-q.bottom)/3.78)});
          const cols=[...document.querySelectorAll('.col')].map(c=>c.scrollHeight>c.clientHeight+1);
          return {over, free, cols};})()""")
        print(mode, "はみ出し:", info["over"], "列あふれ:", info["cols"])
        print("  計算スペース(mm):", info["free"])
        pg.pdf(path=str(OUT / fname), format="A3", print_background=True, prefer_css_page_size=True)
        pg.close()
    br.close()
