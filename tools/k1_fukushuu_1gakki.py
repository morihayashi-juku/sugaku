"""高1 数学Ⅰ 1学期の復習（やさしめ）。期末考査のあとの軽い授業用（11/27 金）。
A4 縦・4ページ（その1〜その4・各8問・計32問）。各ページの上に「ポイント」。
問題 pdf/k1_fukushuu_1gakki.pdf と、赤で答え・途中式を書きこんだ pdf/k1_fukushuu_1gakki_ans.pdf。
  cd tools && python3 k1_fukushuu_1gakki.py      （答えは SymPy で確かめる）
その1 式の展開と因数分解／その2 平方根の計算／その3 1次不等式と2次関数の頂点／その4 2次関数の最大・最小と2次方程式・2次不等式
"""
import re
from pathlib import Path
from sympy import (symbols, expand, factor, sqrt, simplify, radsimp, solve, solveset, S, Interval, Union,
                   Rational, Abs, nsimplify)
from playwright.sync_api import sync_playwright
from texlib import tex, doc as texdoc

OUT = Path(__file__).resolve().parent.parent / "pdf"
NAME = "k1_fukushuu_1gakki"
x = symbols("x", real=True)

# 各問：(問題の式・文, 答え(TeX), 途中式(TeX の行), 検算)
PAGES = [
 dict(title="その1　式の展開と因数分解",
  point=r"<span class=nw>$(x+a)(x+b)=x^2+(a+b)x+ab$</span>　<span class=nw>$(a+b)^2=a^2+2ab+b^2$</span><br><span class=nw>$(a-b)^2=a^2-2ab+b^2$</span>　<span class=nw>$(a+b)(a-b)=a^2-b^2$</span><br>因数分解は展開の逆。まず「たして□・かけて□」になる2つの数をさがす。",
  lead=["(1)〜(4) は展開し，(5)〜(8) は因数分解せよ。"],
  qs=[
   (r"$(x+3)(x+5)$", r"x^2+8x+15", [r"$=x^2+(3+5)x+3\times5$"], lambda: expand((x+3)*(x+5)) == x**2+8*x+15),
   (r"$(2x-1)^2$", r"4x^2-4x+1", [r"$=(2x)^2-2\cdot2x\cdot1+1^2$"], lambda: expand((2*x-1)**2) == 4*x**2-4*x+1),
   (r"$(x+4)(x-4)$", r"x^2-16", [r"$=x^2-4^2$"], lambda: expand((x+4)*(x-4)) == x**2-16),
   (r"$(3x+2)(x-1)$", r"3x^2-x-2", [r"$=3x^2-3x+2x-2$"], lambda: expand((3*x+2)*(x-1)) == 3*x**2-x-2),
   (r"$x^2+7x+12$", r"(x+3)(x+4)", [r"たして $7$，かけて $12$ → $3$ と $4$"], lambda: expand((x+3)*(x+4)) == x**2+7*x+12),
   (r"$x^2-9$", r"(x+3)(x-3)", [r"$=x^2-3^2$"], lambda: expand((x+3)*(x-3)) == x**2-9),
   (r"$x^2-6x+9$", r"(x-3)^2", [r"たして $-6$，かけて $9$ → $-3$ と $-3$"], lambda: expand((x-3)**2) == x**2-6*x+9),
   (r"$2x^2+5x+3$", r"(x+1)(2x+3)", [r"たすきがけ：$x\times 3+1\times 2x=5x$", r"→ $(x+1)(2x+3)$"], lambda: expand((x+1)*(2*x+3)) == 2*x**2+5*x+3),
  ]),
 dict(title="その2　平方根の計算",
  point=r"$\sqrt{a^2b}=a\sqrt{b}$（中の数を小さくする）　$\sqrt{a}\times\sqrt{b}=\sqrt{ab}$<br>分母の有理化：分母と分子に同じものをかける。$\sqrt{a}-\sqrt{b}$ には $\sqrt{a}+\sqrt{b}$ をかける。",
  lead=["次の計算をせよ。(5)・(6) は分母を有理化せよ。"],
  qs=[
   (r"$\sqrt{12}+\sqrt{27}$", r"5\sqrt{3}", [r"$=2\sqrt{3}+3\sqrt{3}$"], lambda: simplify(sqrt(12)+sqrt(27)-5*sqrt(3)) == 0),
   (r"$\sqrt{18}-\sqrt{2}$", r"2\sqrt{2}", [r"$=3\sqrt{2}-\sqrt{2}$"], lambda: simplify(sqrt(18)-sqrt(2)-2*sqrt(2)) == 0),
   (r"$\sqrt{2}\times\sqrt{8}$", r"4", [r"$=\sqrt{16}$"], lambda: simplify(sqrt(2)*sqrt(8)) == 4),
   (r"$(\sqrt{3}+1)^2$", r"4+2\sqrt{3}", [r"$=3+2\sqrt{3}+1$"], lambda: simplify(expand((sqrt(3)+1)**2)-(4+2*sqrt(3))) == 0),
   (r"$\dfrac{6}{\sqrt{3}}$", r"2\sqrt{3}", [r"$=\dfrac{6\sqrt{3}}{3}$"], lambda: simplify(6/sqrt(3)-2*sqrt(3)) == 0),
   (r"$\dfrac{1}{\sqrt{3}-1}$", r"\dfrac{\sqrt{3}+1}{2}", [r"$=\dfrac{\sqrt{3}+1}{(\sqrt{3}-1)(\sqrt{3}+1)}=\dfrac{\sqrt{3}+1}{3-1}$"], lambda: simplify(1/(sqrt(3)-1)-(sqrt(3)+1)/2) == 0),
   (r"$(\sqrt{5}+\sqrt{2})(\sqrt{5}-\sqrt{2})$", r"3", [r"$=(\sqrt{5})^2-(\sqrt{2})^2=5-2$"], lambda: simplify(expand((sqrt(5)+sqrt(2))*(sqrt(5)-sqrt(2)))) == 3),
   (r"$|-5|+|3|$", r"8", [r"$=5+3$"], lambda: Abs(-5)+Abs(3) == 8),
  ]),
 dict(title="その3　1次不等式と2次関数の頂点",
  point=r"不等式は方程式と同じように解く。ただし<b>両辺に負の数をかける・わるときは不等号の向きが逆</b>。<br>$y=a(x-p)^2+q$ の頂点は $(p,\ q)$。$y=x^2+bx+c$ は平方完成して $y=(x-p)^2+q$ の形にする。",
  lead=["(1)〜(4) は不等式を解け。(5)〜(8) は2次関数のグラフの頂点を求めよ。"],
  qs=[
   (r"$3x-2>7$", r"x>3", [r"$3x>9$"], lambda: solveset(3*x-2 > 7, x, S.Reals) == Interval.open(3, S.Infinity)),
   (r"$-2x+5\leqq 1$", r"x\geqq 2", [r"$-2x\leqq -4$（$-2$ でわると向きが逆）"], lambda: solveset(-2*x+5 <= 1, x, S.Reals) == Interval(2, S.Infinity)),
   (r"$2(x-1)<x+3$", r"x<5", [r"$2x-2<x+3$"], lambda: solveset(2*(x-1) < x+3, x, S.Reals) == Interval.open(-S.Infinity, 5)),
   (r"$\begin{cases}x+1>3\\2x-1<9\end{cases}$", r"2<x<5", [r"$x>2$ と $x<5$ の共通部分"], lambda: solveset(x+1 > 3, x, S.Reals).intersect(solveset(2*x-1 < 9, x, S.Reals)) == Interval.open(2, 5)),
   (r"$y=(x-2)^2+3$", r"(2,\ 3)", [r"$p=2,\ q=3$"], lambda: True),
   (r"$y=-(x+1)^2+4$", r"(-1,\ 4)", [r"$x+1=x-(-1)$ だから $p=-1$"], lambda: True),
   (r"$y=x^2-4x+1$", r"(2,\ -3)", [r"$=(x-2)^2-4+1=(x-2)^2-3$"], lambda: expand((x-2)**2-3) == x**2-4*x+1),
   (r"$y=2x^2+8x+5$", r"(-2,\ -3)", [r"$=2(x^2+4x)+5=2(x+2)^2-8+5$"], lambda: expand(2*(x+2)**2-3) == 2*x**2+8*x+5),
  ]),
 dict(title="その4　2次関数の最大・最小と2次方程式",
  point=r"下に凸（$a>0$）なら頂点で最小，上に凸（$a<0$）なら頂点で最大。範囲があるときはグラフをかいて両はしも見る。<br>2次方程式は因数分解か解の公式 $x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$。2次不等式は方程式の解を使う。",
  lead=["(1)〜(3) は最大値・最小値を求めよ。(4)〜(6) は方程式，(7)・(8) は不等式を解け。"],
  qs=[
   (r"$y=(x-1)^2+2$ の最小値", r"x=1\ \text{で最小値}\ 2", [r"下に凸。頂点 $(1,\ 2)$"], lambda: True),
   (r"$y=-x^2+6x-4$ の最大値", r"x=3\ \text{で最大値}\ 5", [r"$=-(x-3)^2+9-4=-(x-3)^2+5$"], lambda: expand(-(x-3)**2+5) == -x**2+6*x-4),
   (r"$y=x^2\ \ (-1\leqq x\leqq 2)$", r"\begin{gathered}x=2\ \text{で最大値}\ 4\\x=0\ \text{で最小値}\ 0\end{gathered}", [r"頂点 $(0,0)$ は範囲の中。$x=-1$ で $1$，$x=2$ で $4$"], lambda: max((-1)**2, 2**2) == 4),
   (r"$x^2-5x+6=0$", r"x=2,\ 3", [r"$(x-2)(x-3)=0$"], lambda: set(solve(x**2-5*x+6, x)) == {2, 3}),
   (r"$x^2-2x-4=0$", r"x=1\pm\sqrt{5}", [r"$x=\dfrac{2\pm\sqrt{4+16}}{2}=\dfrac{2\pm2\sqrt{5}}{2}$"], lambda: set(solve(x**2-2*x-4, x)) == {1+sqrt(5), 1-sqrt(5)}),
   (r"$2x^2+x-1=0$", r"x=\dfrac{1}{2},\ -1", [r"$(2x-1)(x+1)=0$"], lambda: set(solve(2*x**2+x-1, x)) == {Rational(1, 2), -1}),
   (r"$x^2-3x+2<0$", r"1<x<2", [r"$(x-1)(x-2)<0$　解の間"], lambda: solveset(x**2-3*x+2 < 0, x, S.Reals) == Interval.open(1, 2)),
   (r"$x^2-4\geqq 0$", r"x\leqq -2,\ 2\leqq x", [r"$(x+2)(x-2)\geqq 0$　解の外側"], lambda: solveset(x**2-4 >= 0, x, S.Reals) == Union(Interval(-S.Infinity, -2), Interval(2, S.Infinity))),
  ]),
]

CSS = r"""
@page{size:A4;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:'Noto Sans CJK JP';font-size:11pt;line-height:1.45;color:#000;-webkit-print-color-adjust:exact}
.page{width:210mm;height:297mm;padding:10mm 11mm 8mm;display:flex;flex-direction:column;page-break-after:always;overflow:hidden}
.hd{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.5pt solid #000;padding-bottom:1.5mm}
.hd .t{font-size:12.5pt;font-weight:600;white-space:nowrap}.nw{white-space:nowrap}.hd .n{font-size:10.5pt;white-space:nowrap}
.pt{border:1pt solid #666;border-radius:2mm;background:#f2f2f2;padding:2mm 3mm;margin:3mm 0 2mm;font-size:10pt;line-height:1.6}
.pt b{font-weight:600}.pt .lb{font-weight:600;margin-right:2mm}
.lead{margin:1mm 0 2mm;font-size:10.5pt}
.grid{flex:1;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(4,1fr);border-top:.8pt solid #000;border-left:.8pt solid #000;min-height:0}
.cell{border-right:.8pt solid #000;border-bottom:.8pt solid #000;padding:2mm 3mm;display:flex;flex-direction:column;min-height:0}
.q{font-size:11.5pt}.q .no{font-weight:600;margin-right:2mm}
.sol{color:#d40000;font-size:10.5pt;margin-top:2mm;line-height:1.6}.sol .katex,.ans .v .katex{color:#d40000}
.ans{margin-top:auto;align-self:flex-end;white-space:nowrap;font-size:11pt}
.ans .v{display:inline-block;min-width:40mm;border-bottom:1pt solid #000;text-align:center;padding:0 1mm;color:#d40000}
.foot{text-align:center;font-size:9pt;margin-top:1.5mm}
"""
ANS = False
def page(i, P):
    cells = ""
    for k, (q, a, steps, _) in enumerate(P["qs"]):
        sol = ('<div class="sol">' + "".join(f"<div>{s}</div>" for s in steps) + '</div>') if ANS else ''
        cells += (f'<div class="cell"><div class="q"><span class="no">({k+1})</span>{q}</div>{sol}'
                  f'<div class="ans">答　<span class="v">{"$"+a+"$" if ANS else ""}</span></div></div>')
    t = f'数学Ⅰ 1学期の復習（やさしめ） {P["title"]}'
    nm = '<span style="color:#d40000;font-weight:600">【解答】</span>' if ANS else ('1年(　)組(　)番 名前(　　　　　　)' if i == 0 else '名前(　　　　　　)')
    return (f'<div class="page"><div class="hd"><div class="t">{t}</div><div class="n">{nm}</div></div>'
            f'<div class="pt"><span class="lb">ポイント</span>{P["point"]}</div>'
            f'<div class="lead">{"".join(P["lead"])}</div><div class="grid">{cells}</div><div class="foot">-{i+1}-</div></div>')

def doc(): return texdoc(CSS, re.sub(r"\$(.+?)\$", lambda m: tex(m.group(1)), "".join(page(i, P) for i, P in enumerate(PAGES))))

if __name__ == "__main__":
    n = 0
    for P in PAGES:
        for q, a, _, chk in P["qs"]:
            assert chk(), (P["title"], q); n += 1
    print("検算", n, "問OK")
    bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page()
        for ans, name in [(False, NAME), (True, NAME + "_ans")]:
            ANS = ans
            pg.set_content(doc()); pg.wait_for_timeout(300); pg.evaluate("document.fonts.ready")
            over = pg.evaluate("""()=>[...document.querySelectorAll('.cell,.page')].filter(e=>e.scrollHeight>e.clientHeight+1).map(e=>e.textContent.slice(0,25))""")
            if over: bad += 1; print("!! はみ出し", name, over)
            pg.pdf(path=str(OUT / f"{name}.pdf"), prefer_css_page_size=True, print_background=True)
            print(name + ".pdf")
        br.close()
    if bad: raise SystemExit("はみ出しあり")
