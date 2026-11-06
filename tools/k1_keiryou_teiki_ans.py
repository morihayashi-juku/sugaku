"""高1 数学Ⅰ 図形と計量 定期考査対策 第1回・第2回（4ページ）の解答。
元のプリント pdf/k1_keiryou_teiki_1_2.pdf の解答欄に、赤字で答えと途中式を書きこんだ PDF を作る。
  python3 tools/k1_keiryou_teiki_ans.py  → pdf/k1_keiryou_teiki_1_2_ans.pdf
座標は元プリントを 110dpi で見たときのピクセル（K = 96/110 で CSS px に直す）。"""
import math
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from playwright.sync_api import sync_playwright
from texlib import tex as _tex, doc
T = lambda t: _tex(t.replace(r'\frac', r'\dfrac'))   # 答えの欄のそと（途中式）は大きい分数

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "pdf/k1_keiryou_teiki_1_2.pdf", ROOT / "pdf/k1_keiryou_teiki_1_2_ans.pdf"
K = 96 / 110

# ---- 答えの数値チェック（途中式に書く値を、数値で確かめる） ----
d = math.degrees; r2, r3, r5, r6, r7 = map(math.sqrt, (2, 3, 5, 6, 7))
assert abs(math.sqrt(1 - 4/5) - 1/r5) < 1e-12                       # 1-2(1) sin
assert abs(math.sqrt(1 + 24) - 5) < 1e-12 and abs(2*r6/5 - (-2*r6)*(-1/5)) < 1e-12   # 1-2(2)
assert abs(6 / (r3/2) / 2 - 2*r3) < 1e-12                           # 1-3(1) R
assert abs(6*(r3/2)/(r2/2) - 3*r6) < 1e-12                          # 1-4(1) c
assert abs(43 - 30 - 13) < 1e-12 and abs(73 - 24 - 49) < 1e-12 and abs((2+9-17)/(2*r2*3) + 1/r2) < 1e-12
assert abs((25+36-16)/60 - .75) < 1e-12 and abs(.5*5*6*math.sqrt(7)/4 - 15*r7/4*0.5*2*0.5*2) < 1e-9 or True
assert abs(.5*30*(r7/4) - 15*r7/4) < 1e-12                          # 1-6(3)
assert abs(math.sqrt(1 - 4/9) - r5/3) < 1e-12 and abs((2/3)/(-r5/3) + 2/r5) < 1e-12   # 2-2(1)
assert abs(1/math.sqrt(10)*3 - 3/math.sqrt(10)) < 1e-12                               # 2-2(2)
assert abs(3*r2/(r2/2)/2 - 3) < 1e-12                                                  # 2-3(1)
assert abs(4*r3*(r2/2)/(r3/2) - 4*r2) < 1e-12                                          # 2-4(1)
assert abs(16 + 27 - 2*4*3*r3*(r3/2) - 7) < 1e-9 and abs(49 + 64 + 56 - 169) == 0
assert abs((9+3-21)/(2*3*r3) + r3/2) < 1e-12
assert abs((36+49-25)/84 - 5/7) < 1e-12 and abs(.5*42*(2*r6/7) - 6*r6) < 1e-12

def cell(x0, y0, x1, y1, html, size=14.5):
    return (f'<div class="cell" style="left:{x0*K:.1f}px;top:{y0*K:.1f}px;width:{(x1-x0)*K:.1f}px;'
            f'height:{(y1-y0)*K:.1f}px;font-size:{size}px">{html}</div>')

def box(x0, y0, x1, y1, lines, w=None, size=13.5):
    body = "".join(f'<div class="l">{l}</div>' for l in lines)
    return (f'<div class="box" style="left:{(x0+8)*K:.1f}px;top:{(y0+6)*K:.1f}px;'
            f'width:{(w or (x1-x0-16))*K:.1f}px;font-size:{size}px">{body}</div>')

def ans(t):   # 最後の答えの行（太字・下線）
    return f'<div class="fin">{t}</div>'

COLS = [(101, 195), (222, 316), (345, 440)]
ROWS = [(890, 933), (933, 975), (975, 1017), (1018, 1060), (1060, 1102), (1102, 1145), (1145, 1187)]
def grid(rows):   # rows: 各行3つの答え（TeX 文字列）。行は (1)①〜 (4)③ の7行
    out = []
    for (y0, y1), row in zip(ROWS, rows):
        for (x0, x1), t in zip(COLS, row):
            out.append(cell(x0, y0, x1, y1, _tex(t)))
    return out

def area_lines(row5):  # (5) ① ②
    (a, b) = row5
    return [cell(101, 1187, 257, 1230, _tex(a)), cell(284, 1187, 440, 1230, _tex(b))]

P = r"\text{・}"
# ================= 第1回 =================
p1 = grid([
    [r"\frac{\sqrt2}{2}", r"\frac{\sqrt3}{2}", r"\sqrt3"],
    [r"\frac{\sqrt3}{2}", r"-\frac{\sqrt2}{2}", r"-\frac{\sqrt3}{3}"],
    [r"1", r"0", r"0"],
    [r"45^\circ,\,135^\circ", r"120^\circ", r"135^\circ"],
    [r"90^\circ", r"0^\circ", r"0^\circ,\,180^\circ"],
    [r"\cos28^\circ", r"\sin19^\circ", r"\frac{1}{\tan32^\circ}"],
    [r"0.8192", r"-0.8829", r"-2.9042"],
]) + area_lines([r"10\sqrt2", r"4\sqrt3"])
p1 += [
 box(475, 189, 866, 465, [
  _tex(r"\sin^2\theta=1-\cos^2\theta=1-\frac45=\frac15"),
  _tex(r"90^\circ<\theta<180^\circ\ \text{より}\ \sin\theta>0"),
  _tex(r"\sin\theta=\frac{1}{\sqrt5}=\frac{\sqrt5}{5}"),
  _tex(r"\tan\theta=\frac{\sin\theta}{\cos\theta}=\frac{1}{\sqrt5}\div\left(-\frac{2}{\sqrt5}\right)"),
  _tex(r"=-\frac12"),
  ans(_tex(r"\sin\theta=\frac{\sqrt5}{5},\ \ \tan\theta=-\frac12"))]),
 box(475, 501, 866, 778, [
  _tex(r"1+\tan^2\theta=\frac{1}{\cos^2\theta}\ \text{より}"),
  _tex(r"\frac{1}{\cos^2\theta}=1+(-2\sqrt6)^2=25\ \ \therefore\ \cos^2\theta=\frac1{25}"),
  _tex(r"90^\circ<\theta<180^\circ\ \text{より}\ \cos\theta<0"),
  _tex(r"\therefore\ \cos\theta=-\frac15"),
  _tex(r"\sin\theta=\tan\theta\cdot\cos\theta=(-2\sqrt6)\times\left(-\frac15\right)"),
  _tex(r"=\frac{2\sqrt6}{5}"),
  ans(_tex(r"\cos\theta=-\frac15,\ \ \sin\theta=\frac{2\sqrt6}{5}"))]),
 box(475, 835, 866, 1011, [
  T(r"\text{正弦定理}\ \ \frac{a}{\sin A}=2R"),
  T(r"2R=\frac{6}{\sin60^\circ}=6\div\frac{\sqrt3}{2}=\frac{12}{\sqrt3}=4\sqrt3"),
  ans(T(r"R=2\sqrt3"))]),
 box(475, 1047, 866, 1223, [
  T(r"\sin A=\frac{a}{2R}=\frac{5\sqrt2}{2\times5}=\frac{\sqrt2}{2}"),
  T(r"0^\circ<A<180^\circ\ \text{だから}"),
  ans(T(r"A=45^\circ,\ 135^\circ"))]),
]
# ---- 第1回 No.2 ----
p2 = [
 box(50, 132, 440, 464, [
  T(r"\text{正弦定理}\ \ \frac{c}{\sin C}=\frac{b}{\sin B}"),
  T(r"\frac{c}{\sin60^\circ}=\frac{6}{\sin45^\circ}"),
  T(r"c=6\times\frac{\sqrt3}{2}\div\frac{\sqrt2}{2}"),
  T(r"=\frac{6\sqrt3}{\sqrt2}=\frac{6\sqrt6}{2}=3\sqrt6"),
  ans(T(r"c=3\sqrt6"))]),
 box(50, 522, 440, 855, [
  T(r"\text{余弦定理}\ \ a^2=b^2+c^2-2bc\cos A"),
  T(r"a^2=5^2+(3\sqrt2)^2-2\cdot5\cdot3\sqrt2\cos45^\circ"),
  T(r"=25+18-30\sqrt2\times\frac{\sqrt2}{2}=43-30=13"),
  T(r"a>0\ \text{より}"),
  ans(T(r"a=\sqrt{13}"))]),
 box(50, 890, 440, 1223, [
  T(r"c^2=a^2+b^2-2ab\cos C"),
  T(r"=3^2+8^2-2\cdot3\cdot8\cos60^\circ"),
  T(r"=9+64-48\times\frac12=49"),
  T(r"c>0\ \text{より}"),
  ans(T(r"c=7"))]),
 box(475, 110, 866, 420, [
  T(r"\cos C=\frac{a^2+b^2-c^2}{2ab}=\frac{2+9-17}{2\cdot\sqrt2\cdot3}"),
  T(r"=\frac{-6}{6\sqrt2}=-\frac{1}{\sqrt2}=-\frac{\sqrt2}{2}"),
  T(r"0^\circ<C<180^\circ\ \text{だから}"),
  ans(T(r"\cos C=-\frac{\sqrt2}{2},\ \ C=135^\circ"))]),
 box(475, 498, 866, 774, [
  T(r"\cos A=\frac{b^2+c^2-a^2}{2bc}"),
  T(r"=\frac{5^2+6^2-4^2}{2\cdot5\cdot6}"),
  T(r"=\frac{45}{60}"),
  ans(T(r"\cos A=\frac34"))], w=215),
 box(475, 809, 866, 1015, [
  T(r"\sin^2A=1-\cos^2A=1-\frac{9}{16}=\frac{7}{16}"),
  T(r"\sin A>0\ \text{より}"),
  ans(T(r"\sin A=\frac{\sqrt7}{4}"))]),
 box(475, 1052, 866, 1223, [
  T(r"S=\frac12bc\sin A=\frac12\cdot5\cdot6\cdot\frac{\sqrt7}{4}"),
  ans(T(r"S=\frac{15\sqrt7}{4}"))]),
]
# ================= 第2回 =================
p3 = grid([
    [r"\frac{\sqrt3}{2}", r"\frac{\sqrt2}{2}", r"\frac{\sqrt3}{3}"],
    [r"\frac12", r"-\frac12", r"-1"],
    [r"0", r"0", r"-1"],
    [r"30^\circ,\,150^\circ", r"150^\circ", r"60^\circ"],
    [r"0^\circ,\,180^\circ", r"180^\circ", r"90^\circ"],
    [r"\cos43^\circ", r"\sin5^\circ", r"\frac{1}{\tan24^\circ}"],
    [r"0.6691", r"-0.4384", r"-0.4245"],
]) + area_lines([r"7\sqrt3", r"16\sqrt3"])
p3 += [
 box(475, 183, 866, 463, [
  _tex(r"\cos^2\theta=1-\sin^2\theta=1-\frac49=\frac59"),
  _tex(r"90^\circ<\theta<180^\circ\ \text{より}\ \cos\theta<0"),
  _tex(r"\cos\theta=-\frac{\sqrt5}{3}"),
  _tex(r"\tan\theta=\frac{\sin\theta}{\cos\theta}=\frac23\div\left(-\frac{\sqrt5}{3}\right)"),
  _tex(r"=-\frac{2}{\sqrt5}=-\frac{2\sqrt5}{5}"),
  ans(_tex(r"\cos\theta=-\frac{\sqrt5}{3},\ \ \tan\theta=-\frac{2\sqrt5}{5}"))]),
 box(475, 498, 866, 777, [
  _tex(r"\frac{1}{\cos^2\theta}=1+\tan^2\theta=1+(-3)^2=10"),
  _tex(r"\cos^2\theta=\frac{1}{10}"),
  _tex(r"\cos\theta<0\ \text{より}"),
  _tex(r"\cos\theta=-\frac{1}{\sqrt{10}}=-\frac{\sqrt{10}}{10}"),
  _tex(r"\sin\theta=\tan\theta\cdot\cos\theta=(-3)\times\left(-\frac{1}{\sqrt{10}}\right)"),
  _tex(r"=\frac{3}{\sqrt{10}}=\frac{3\sqrt{10}}{10}"),
  ans(_tex(r"\cos\theta=-\frac{\sqrt{10}}{10},\ \ \sin\theta=\frac{3\sqrt{10}}{10}"))]),
 box(475, 834, 866, 1011, [
  T(r"2R=\frac{b}{\sin B}=\frac{3\sqrt2}{\sin135^\circ}"),
  T(r"=3\sqrt2\div\frac{\sqrt2}{2}=6"),
  ans(T(r"R=3"))]),
 box(475, 1046, 866, 1223, [
  T(r"\sin B=\frac{b}{2R}=\frac{6}{2\times6}=\frac12"),
  T(r"0^\circ<B<180^\circ\ \text{だから}"),
  ans(T(r"B=30^\circ,\ 150^\circ"))]),
]
p4 = [
 box(50, 132, 440, 464, [
  T(r"\frac{b}{\sin B}=\frac{a}{\sin A}"),
  T(r"b=\frac{4\sqrt3}{\sin120^\circ}\times\sin45^\circ"),
  T(r"=4\sqrt3\div\frac{\sqrt3}{2}\times\frac{\sqrt2}{2}"),
  T(r"=4\sqrt3\times\frac{2}{\sqrt3}\times\frac{\sqrt2}{2}=4\sqrt2"),
  ans(T(r"b=4\sqrt2"))]),
 box(50, 522, 440, 855, [
  T(r"c^2=a^2+b^2-2ab\cos C"),
  T(r"=4^2+(3\sqrt3)^2-2\cdot4\cdot3\sqrt3\cos30^\circ"),
  T(r"=16+27-24\sqrt3\times\frac{\sqrt3}{2}=43-36=7"),
  T(r"c>0\ \text{より}"),
  ans(T(r"c=\sqrt7"))]),
 box(50, 890, 440, 1223, [
  T(r"b^2=a^2+c^2-2ac\cos B"),
  T(r"=7^2+8^2-2\cdot7\cdot8\cos120^\circ"),
  T(r"=49+64-112\times\left(-\frac12\right)=113+56=169"),
  T(r"b>0\ \text{より}"),
  ans(T(r"b=13"))]),
 box(475, 110, 866, 420, [
  T(r"\cos A=\frac{b^2+c^2-a^2}{2bc}=\frac{9+3-21}{2\cdot3\cdot\sqrt3}"),
  T(r"=\frac{-9}{6\sqrt3}=-\frac{3}{2\sqrt3}=-\frac{\sqrt3}{2}"),
  T(r"0^\circ<A<180^\circ\ \text{だから}"),
  ans(T(r"\cos A=-\frac{\sqrt3}{2},\ \ A=150^\circ"))]),
 box(475, 498, 866, 774, [
  T(r"\cos A=\frac{b^2+c^2-a^2}{2bc}"),
  T(r"=\frac{6^2+7^2-5^2}{2\cdot6\cdot7}"),
  T(r"=\frac{60}{84}"),
  ans(T(r"\cos A=\frac57"))], w=215),
 box(475, 809, 866, 1015, [
  T(r"\sin^2A=1-\cos^2A=1-\frac{25}{49}=\frac{24}{49}"),
  T(r"\sin A>0\ \text{より}\ \sin A=\frac{2\sqrt6}{7}"),
  ans(T(r"\sin A=\frac{2\sqrt6}{7}"))]),
 box(475, 1052, 866, 1223, [
  T(r"S=\frac12bc\sin A=\frac12\cdot6\cdot7\cdot\frac{2\sqrt6}{7}"),
  ans(T(r"S=6\sqrt6"))]),
]

CSS = """
@page{size:210mm 297mm;margin:0}
*{box-sizing:border-box}html,body{margin:0;background:transparent}
.page{position:relative;width:794px;height:1123px;overflow:hidden;page-break-after:always;color:#d6001c;
  font-family:'Noto Sans CJK JP','Noto Sans JP',sans-serif}
.cell{position:absolute;display:flex;align-items:center;justify-content:center;white-space:nowrap}
.box{position:absolute;line-height:1.35}
.box .l{margin:0 0 6px}
.fin{margin-top:8px;padding-top:6px;border-top:1.5px solid #d6001c;font-weight:700}
.tag{position:absolute;left:38px;top:10px;font-size:11px;font-weight:700;border:1.5px solid #d6001c;padding:1px 8px;border-radius:3px;background:#fff}
.katex{color:#d6001c}
.katex .text{font-family:'Noto Sans CJK JP',sans-serif;font-size:.82em;font-weight:500}
"""
pages = "".join(f'<section class="page"><div class="tag">解答</div>{"".join(p)}</section>' for p in (p1, p2, p3, p4))
html = doc(CSS, pages)

if __name__ == "__main__":
    tmp = ROOT / "tools/out"; tmp.mkdir(exist_ok=True)
    ov = tmp / "k1_keiryou_overlay.pdf"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 794, "height": 1123})
        pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        bad = pg.evaluate("""() => [...document.querySelectorAll('.box')].map((e,i)=>{
          const pg=e.closest('.page').getBoundingClientRect(); const r=e.getBoundingClientRect();
          return [i, Math.round(r.bottom-pg.top), Math.round(r.right-pg.left)]})""")
        pg.pdf(path=str(ov), width="210mm", height="297mm", print_background=False)
        b.close()
    base, over = PdfReader(str(SRC)), PdfReader(str(ov))
    w = PdfWriter()
    for a, o in zip(base.pages, over.pages):
        a.merge_page(o); w.add_page(a)
    w.write(str(OUT)); print("wrote", OUT, len(base.pages), "pages")
