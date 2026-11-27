"""高2 数学Ⅱ 図形と方程式「円の方程式」練習プリント（11/27 作成・A4 4ページ）
k2_en_teiki_1（定期テスト対策）の大問1・2・3を練習するための類題。
その1 ＝ 中心と半径 → 方程式（大問1の類題・12問）
その2 ＝ 方程式 → 中心と半径（大問2の類題・12問）
その3 ＝ 中心と通る点 → 方程式（大問3(1)(2)の類題・8問）
その4 ＝ 軸に接する円（大問3(3)(4)の類題・6問）＋まとめ（4問）
問題（pdf/k2_en_renshu_1.pdf）と、問題に赤字で答え・途中式を書き込んだこたえ（_ans.pdf）を同じレイアウトで出す。
答えは SymPy で確認。実行：cd tools && python3 k2_en_renshu.py
"""
import math
import pathlib
import sys

import sympy as sp

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from texlib import _dist  # noqa: E402

X, Y = sp.symbols("x y")
OUT = pathlib.Path(__file__).resolve().parent.parent / "pdf"
NAME = "k2_en_renshu_1"


# ---------- 式の書き方 ----------
def sq(r2):
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
    if a == 0:
        return f"{v}^2"
    return f"({v}{'-' if a > 0 else '+'}{abs(a)})^2"


def std(a, b, r2):
    return f"{lin('x', a)}+{lin('y', b)}={r2}"


def pt(a, b):
    return f"({a},\\,{b})"


def p(v):
    return f"({v})" if v < 0 else str(v)


def M(s):
    return f"${s}$"


def ans(s, w=38):
    return f'<span class="ans" style="--w:{w}mm">{s}</span>'


def work(s):
    return f'<div class="work">{s}</div>'


def it(no, prob, a_part, w_part=""):
    return (f'<div class="it"><div class="q"><span class="no">({no})</span>{prob}</div>'
            f'{work(w_part) if w_part else ""}<div class="a">{a_part}</div></div>')


def check(a, b, r2, eq_tex=None):
    """円 (x-a)^2+(y-b)^2=r2 の中心・半径を SymPy で確かめる"""
    e = sp.expand((X - a) ** 2 + (Y - b) ** 2 - r2)
    cx = -sp.Poly(e, X).coeffs()[1] / 2 if a else 0
    assert sp.simplify(cx - a) == 0
    assert r2 > 0 and sp.sqrt(r2) ** 2 == r2


def sq_work(r2):
    """r^2 = r2 から r を出す途中式"""
    rs = sq(r2)
    if rs.isdigit():
        return f"r^2={r2}\\ \\text{{より}}\\ r={rs}"
    if rs == f"\\sqrt{{{r2}}}":
        return f"r^2={r2}\\ \\text{{より}}\\ r={rs}"
    return f"r^2={r2}\\ \\text{{より}}\\ r=\\sqrt{{{r2}}}={rs}"


def rad_tex(r2):
    rs = sq(r2)
    return rs


def eq_work(a, b, r2):
    rs = sq(r2)
    rhs = f"{rs}^2" if rs.isdigit() else f"({rs})^2"
    return f"{lin('x', a)}+{lin('y', b)}={rhs}"


def header(no, title):
    return f"""<div class="hd"><div class="ht"><span class="tag">数学Ⅱ 円の方程式 練習 その{no}</span>{title}<span class="key">解答</span></div>
<div class="nm">名前（　　　　　　　　）</div></div>"""


def grid(cls, items, rows):
    return f'<div class="{cls}" style="--g:{rows}">{"".join(items)}</div>'


def sec(n, title):
    return f'<h3><span class="sn">{n}</span>{title}</h3>'


# ---------- その1 中心と半径 → 方程式 ----------
P1 = [((2, 5), 9), ((-3, 1), 25), ((4, -2), 4), ((-1, -6), 16),
      ((0, 2), 9), ((5, 0), 1), ((0, 0), 49), ((1, -3), 5),
      ((-2, 4), 10), ((3, 3), 12), ((-5, -1), 18), ((0, 0), 20)]


def page1():
    items = []
    for i, ((a, b), r2) in enumerate(P1):
        check(a, b, r2)
        cen = "原点" if (a, b) == (0, 0) else M(pt(a, b))
        items.append(it(i + 1, f"中心 {cen}、半径 {M(sq(r2))}", ans(M(std(a, b, r2)), 54), M(eq_work(a, b, r2))))
    return f"""<section class="page">
{header(1, "中心と半径から円の方程式を求める")}
<div class="box"><b>ポイント</b>　中心 $(a,\\,b)$、半径 $r$ の円　→　$(x-a)^2+(y-b)^2=r^2$
<span class="note">（右辺は半径の<b>2乗</b>。$(\\sqrt{{5}})^2=5$、$(2\\sqrt{{3}})^2=12$）</span><br>
<span class="note">中心の座標が負なら、かっこの中は $+$ になる。例：中心 $(-3,\\,1)$ → $(x+3)^2+(y-1)^2$。中心が原点なら $x^2+y^2=r^2$</span></div>
{sec(1, "次のような円の方程式を求めよ。")}
{grid("grid2", items, 6)}
</section>"""


# ---------- その2 方程式 → 中心と半径 ----------
P2 = [(4, 1, 25), (-2, 3, 36), (1, -5, 4), (-6, -2, 1),
      (0, 4, 9), (-3, 0, 49), (0, 0, 16), (2, -1, 11),
      (-4, 5, 18), (3, -3, 24), (0, -2, 27), (0, 0, 32)]


def page2():
    items = []
    for i, (a, b, r2) in enumerate(P2):
        check(a, b, r2)
        items.append(it(i + 1, M(std(a, b, r2)),
                        "中心 " + ans(M(pt(a, b)), 24) + "　半径 " + ans(M(sq(r2)), 16),
                        M(sq_work(r2))))
    return f"""<section class="page">
{header(2, "円の方程式から中心と半径を読む")}
<div class="box"><b>ポイント</b>　$(x-a)^2+(y-b)^2=r^2$ の円は　中心 $(a,\\,b)$、半径 $r$
<span class="note">（中心は<b>かっこの中と符号が逆</b>。$(x+2)^2$ → $x$座標は $-2$）</span><br>
<span class="note">半径は右辺の<b>正の平方根</b>。根号の中はできるだけ小さくする：$\\sqrt{{18}}=3\\sqrt{{2}}$、$\\sqrt{{24}}=2\\sqrt{{6}}$</span></div>
{sec(2, "次の方程式が表す円の中心の座標と半径を求めよ。")}
{grid("grid2", items, 6)}
</section>"""


# ---------- その3 中心と通る点 ----------
P3 = [((1, 3), (4, 7)), ((-2, 1), (3, 13)), ((3, -2), (5, 1)), ((-1, -4), (2, -1)),
      ((0, 2), (4, 0)), ((4, 1), (0, 0)), ((-3, -5), (0, 0)), ((2, -3), (2, 4))]


def thru_work(a, b, px, py):
    r2 = (px - a) ** 2 + (py - b) ** 2
    return r2, (f"r^2=({px}-{p(a)})^2+({py}-{p(b)})^2" + f"={(px - a) ** 2}+{(py - b) ** 2}={r2}")


def page3():
    items = []
    for i, ((a, b), (px, py)) in enumerate(P3):
        r2, w = thru_work(a, b, px, py)
        check(a, b, r2)
        assert sp.expand((px - a) ** 2 + (py - b) ** 2 - r2) == 0
        through = "原点" if (px, py) == (0, 0) else f"点 {M(pt(px, py))}"
        items.append(it(i + 1, f"中心が点 {M(pt(a, b))} で、{through} を通る円",
                        ans(M(std(a, b, r2)), 54), M(w)))
    return f"""<section class="page">
{header(3, "中心と通る点から円の方程式を求める")}
<div class="box"><b>ポイント</b>　半径＝<b>中心と通る点の距離</b>。方程式の右辺は $r^2$ なので、<b>$r^2$ をそのまま使えば根号はいらない</b>。<br>
<span class="note">例：中心 $(2,\\,1)$ で点 $(5,\\,5)$ を通る → $r^2=(5-2)^2+(5-1)^2=9+16=25$ → $(x-2)^2+(y-1)^2=25$</span></div>
{sec(3, "次のような円の方程式を求めよ。")}
{grid("grid2", items, 4)}
</section>"""


# ---------- その4 接する円＋まとめ ----------
P4x = [(2, 5), (-3, -4), (5, -1)]
P4y = [(-6, 2), (3, -7), (-1, 4)]


def page4():
    s4 = []
    n = 0
    for (a, b) in P4x:
        n += 1
        r = abs(b)
        check(a, b, r * r)
        s4.append(it(n, f"中心が点 {M(pt(a, b))} で、$x$軸に接する円", ans(M(std(a, b, r * r)), 54),
                     f"半径＝中心の $y$座標の絶対値＝{M(f'|{b}|={r}')}"))
    for (a, b) in P4y:
        n += 1
        r = abs(a)
        check(a, b, r * r)
        s4.append(it(n, f"中心が点 {M(pt(a, b))} で、$y$軸に接する円", ans(M(std(a, b, r * r)), 54),
                     f"半径＝中心の $x$座標の絶対値＝{M(f'|{a}|={r}')}"))

    # まとめ（大問1・2・3を1問ずつ＋接する円）
    m = []
    a, b, r2 = -2, 6, 8
    check(a, b, r2)
    m.append(it(1, f"中心 {M(pt(a, b))}、半径 {M(sq(r2))} の円の方程式を求めよ。", ans(M(std(a, b, r2)), 54), M(eq_work(a, b, r2))))
    a, b, r2 = -5, 3, 45
    check(a, b, r2)
    m.append(it(2, f"円 {M(std(a, b, r2))} の中心の座標と半径を求めよ。",
                "中心 " + ans(M(pt(a, b)), 24) + "　半径 " + ans(M(sq(r2)), 16), M(sq_work(r2))))
    a, b, px, py = 4, -1, -2, 7
    r2, w = thru_work(a, b, px, py)
    assert r2 == 100
    m.append(it(3, f"中心が点 {M(pt(a, b))} で、点 {M(pt(px, py))} を通る円の方程式を求めよ。", ans(M(std(a, b, r2)), 54), M(w)))
    a, b = -5, 2
    m.append(it(4, f"中心が点 {M(pt(a, b))} で、$x$軸に接する円の方程式を求めよ。", ans(M(std(a, b, b * b)), 54),
                f"半径＝中心の $y$座標の絶対値＝{M(f'|{b}|={abs(b)}')}"))
    return f"""<section class="page">
{header(4, "軸に接する円・まとめ")}
<div class="box"><b>ポイント</b>　$x$軸に接する円 → 半径＝中心の <b>$y$座標</b>の絶対値　／　$y$軸に接する円 → 半径＝中心の <b>$x$座標</b>の絶対値<br>
<span class="note">例：中心 $(4,\\,-3)$ で $x$軸に接する → 半径 $3$ → $(x-4)^2+(y+3)^2=9$（$x$軸・$y$軸を取りちがえないように図をかいて確かめる）</span></div>
{sec(4, "次のような円の方程式を求めよ。")}
{grid("grid2", s4, 3)}
{sec(5, "まとめ　次の問いに答えよ。")}
{grid("grid2", m, 2)}
</section>"""


KATEX = _dist()
CSS = """
@page { size: A4; margin: 0; }
body { margin:0; font-family: "Noto Sans CJK JP", sans-serif; font-size: 10.5pt; color:#111; }
.page { width:210mm; height:297mm; box-sizing:border-box; padding:10mm 12mm; page-break-after: always; overflow:hidden; display:flex; flex-direction:column; }
.hd { border-bottom: 2px solid #333; padding-bottom: 2mm; margin-bottom: 3mm; display:flex; justify-content:space-between; align-items:flex-end; }
.ht { font-size: 13.5pt; font-weight: 700; white-space:nowrap; }
.tag { display:inline-block; font-size:9pt; background:#333; color:#fff; padding:1px 7px; margin-right:6px; border-radius:3px; vertical-align:middle; }
.key { display:inline-block; font-size:9pt; border:1.5px solid #c00; color:#c00; padding:0 6px; margin-left:8px; border-radius:3px; vertical-align:middle; }
.nm { font-size: 10pt; white-space:nowrap; }
.box { border: 1.3px solid #555; border-radius: 4px; padding: 2mm 4mm; margin-bottom: 1mm; background:#f7f7f7; line-height:1.8; }
.note { font-size: 9pt; color:#444; }
h3 { font-size: 11pt; margin: 3mm 0 2mm; font-weight:700; }
.sn { display:inline-block; width:6mm; height:6mm; line-height:6mm; text-align:center; background:#333; color:#fff; border-radius:3px; margin-right:2mm; font-size:10pt; }
.grid1, .grid2 { display:grid; gap: 2mm 7mm; margin-left: 2mm; flex: var(--g) 1 0; grid-auto-rows: 1fr; min-height:0; }
.grid2 { grid-template-columns: minmax(0,1fr) minmax(0,1fr); }
.it { display:flex; flex-direction:column; border-bottom: 1px dotted #bbb; padding-bottom: 1.5mm; line-height:1.8; min-width:0; }
.it .a { margin-top:auto; padding-top: 1mm; white-space:nowrap; }
.no { margin-right: 2mm; }
.ans { color:#c00; font-weight:700; border-bottom: 1px solid #c00; padding: 0 2px; }
.ans .katex { color:#c00; }
.work { color:#c33; font-size: 9.3pt; line-height:1.8; margin: 0.5mm 0 0 3mm; }
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
{page1()}{page2()}{page3()}{page4()}
<script>
renderMathInElement(document.body, {{delimiters:[{{left:"$", right:"$", display:false}}], throwOnError:true}});
document.body.setAttribute("data-done","1");
</script>
</body></html>"""

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

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
              const over=its.filter(e=>e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1).map(e=>e.querySelector('.q').innerText.slice(0,14));
              const free=its.map(e=>{const q=e.querySelector('.q').getBoundingClientRect(),a=e.querySelector('.a').getBoundingClientRect();return Math.round((a.top-q.bottom)/3.78)});
              const pages=[...document.querySelectorAll('.page')].map(p=>p.scrollHeight>p.clientHeight+1);
              return {over, free, pages};})()""")
            print(mode, "はみ出し:", info["over"], "ページあふれ:", info["pages"])
            print("  計算スペース(mm):", info["free"])
            pg.pdf(path=str(OUT / fname), format="A4", print_background=True, prefer_css_page_size=True)
            pg.close()
        br.close()
