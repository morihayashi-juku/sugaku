"""中2 確率（はじめて習う人用）4ページ＋こたえ4ページ（赤で書きこみ）

  cd tools && python3 c2_kakuritsu_nyumon.py

まだ習っていない単元なので、各ページに「ポイント」→「例題（解き方つき）」→「練習」の順。
  ① 確率の意味（a/n、0〜1、起こらない確率）  ② 樹形図で数える（硬貨・並び方・くじ）
  ③ 2つのさいころ（表で数える）  ④ 同時に取り出す・2けたの整数・少なくとも
- 答えはすべて itertools で全部の場合を数えて確かめる（check）。分数は約分した形。
- 出力：pdf/c2_kakuritsu_nyumon.pdf と c2_kakuritsu_nyumon_ans.pdf
"""
from fractions import Fraction as F
from itertools import combinations, permutations, product

from texlib import doc, tex as T, write_pdfs

FILE = "c2_kakuritsu_nyumon"
ANS = False


def fr(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"\\dfrac{{{v.numerator}}}{{{v.denominator}}}"


def b(w, v=""):
    if ANS:
        return f"<span class='ul fill' style='width:{w}mm'>{v}</span>"
    return f"<span class=ul style='width:{w}mm'></span>"


def bp(v):
    """確率の答えのらん（分数が入るので少し高め）"""
    return b(26, T(fr(v)))


def q(no, text, ans="", work="", grow=1, extra=""):
    return (f"<div class=sqi style='flex:{grow} 1 0'><div class=qt><span class=no>({no})</span><div>{text}</div>"
            f"<span class='ans in'>{ans}</span></div><div class=work>{work if ANS else ''}</div>{extra}</div>")


def head(n, title):
    right = ("<span class=kotae>こたえ</span>" if ANS else
             "<span class=cl>（　）組（　）番　名前 <span class=u style='width:34mm'></span></span>")
    return f"<div class=head><b>中2数学 確率</b><span class=sub>{'①②③④'[n - 1]} {title}</span>{right}</div>"


def point(html):
    return f"<div class=point><span class=tag>ポイント</span><div>{html}</div></div>"


def example(prob, sol, fig=""):
    return (f"<div class=ex><div class=exl><div><span class=tag2>例題</span>{prob}</div>"
            f"<div class=sol><b>解き方</b>　{sol}</div></div>{fig}</div>")


def page(n, title, pt, ex, qs):
    return (f"<div class=page>{head(n, title)}{pt}{ex}"
            f"<div class=big><span class=box>練習</span>次の確率や、場合の数を求めなさい。</div>"
            f"<div class=qs>{''.join(qs)}</div></div>")


def P(good, allc):
    good, allc = list(good), list(allc)
    return F(len(good), len(allc))


# ---------- 全部の場合を数えて確かめる ----------
DIE = range(1, 7)
D2 = list(product(DIE, DIE))
C3 = list(product("表裏", repeat=3))
ABC = list(permutations("ABC"))
KUJI = list(permutations(["当1", "当2", "は"], 2))
BALLS = list(combinations(["赤1", "赤2", "白1", "白2"], 2))
CARD2 = list(permutations([1, 2, 3, 4], 2))
KUJI5 = list(combinations(["当1", "当2", "は1", "は2", "は3"], 2))
R = dict(
    even=P([d for d in DIE if d % 2 == 0], DIE), ge5=P([d for d in DIE if d >= 5], DIE), seven=P([d for d in DIE if d == 7], DIE),
    red=F(3, 5), mul4=P([k for k in range(1, 11) if k % 4 == 0], range(1, 11)),
    prime=P([k for k in range(1, 11) if k in (2, 3, 5, 7)], range(1, 11)),
    c3=len(C3), c3all=P([c for c in C3 if c == ("表",) * 3], C3), c3two=P([c for c in C3 if c.count("表") == 2], C3),
    abc=len(ABC), afirst=P([p for p in ABC if p[0] == "A"], ABC), kuji=P([k for k in KUJI if all("当" in s for s in k)], KUJI),
    s7=P([d for d in D2 if sum(d) == 7], D2), s10=P([d for d in D2 if sum(d) >= 10], D2),
    odd=P([d for d in D2 if d[0] * d[1] % 2 == 1], D2), big=P([d for d in D2 if d[0] > d[1]], D2),
    six=P([d for d in D2 if 6 in d], D2),
    balls=len(BALLS), rr=P([x for x in BALLS if all("赤" in s for s in x)], BALLS),
    rw=P([x for x in BALLS if sum("赤" in s for s in x) == 1], BALLS),
    card=len(CARD2), ceven=P([c for c in CARD2 if c[1] % 2 == 0], CARD2), c40=P([c for c in CARD2 if c[0] * 10 + c[1] >= 40], CARD2),
    atari=P([k for k in KUJI5 if any("当" in s for s in k)], KUJI5),
)
EXPECT = dict(even=F(1, 2), ge5=F(1, 3), seven=0, red=F(3, 5), mul4=F(1, 5), prime=F(2, 5), c3=8, c3all=F(1, 8), c3two=F(3, 8),
              abc=6, afirst=F(1, 3), kuji=F(1, 3), s7=F(1, 6), s10=F(1, 6), odd=F(1, 4), big=F(5, 12), six=F(11, 36),
              balls=6, rr=F(1, 6), rw=F(2, 3), card=12, ceven=F(1, 2), c40=F(1, 4), atari=F(7, 10))
assert R == EXPECT, {k: (R[k], EXPECT[k]) for k in R if R[k] != EXPECT[k]}


# ---------- 図 ----------
def tree_svg(levels, w=64, gap=6.0, col=19, root=""):
    """樹形図。levels＝各段のえだ（例：[['表','裏'],['表','裏']]）"""
    leaves = 1
    for lv in levels:
        leaves *= len(lv)
    h = leaves * gap + 4
    o = []

    def draw(depth, x, y0, y1, px, py):
        n = len(levels[depth])
        for i, lab in enumerate(levels[depth]):
            a, c = y0 + (y1 - y0) * i / n, y0 + (y1 - y0) * (i + 1) / n
            y = (a + c) / 2
            nx = x + col
            if px is not None:
                o.append(f'<line x1="{px + 3.2:.1f}" y1="{py:.1f}" x2="{nx - 3.4:.1f}" y2="{y:.1f}" stroke="#333" stroke-width=".35"/>')
            o.append(f'<text x="{nx:.1f}" y="{y + 1.3:.1f}" font-size="3.8" text-anchor="middle">{lab}</text>')
            if depth + 1 < len(levels):
                draw(depth + 1, nx, a, c, nx, y)

    draw(0, -col + 6, 2, h - 2, None, None)
    return f'<svg class=fig width="{w}mm" height="{h:.1f}mm" viewBox="0 0 {w} {h:.1f}">{"".join(o)}</svg>'


def dice_table():
    rows = "<tr><th class=corner>大＼小</th>" + "".join(f"<th>{j}</th>" for j in DIE) + "</tr>"
    for i in DIE:
        rows += f"<tr><th>{i}</th>" + "".join(f"<td>{(i + j) if ANS else ''}</td>" for j in DIE) + "</tr>"
    return f"<table class=dice>{rows}</table>"


# ---------- ページ ----------
def page1():
    pt = point("どの場合が起こることも同じ程度に期待できるとき、「<b>同様に確からしい</b>」という。<br>"
               f"起こりうる場合が全部で {T('n')} 通りあり、そのうち、ことがらAの起こる場合が {T('a')} 通りのとき、"
               f"<b>Aの起こる確率</b>は　{T('p=\\dfrac{a}{n}')}<br>"
               f"・確率 {T('p')} の範囲は {T('0\\leqq p\\leqq 1')}（必ず起こる＝1、決して起こらない＝0）"
               f"　・<b>Aの起こらない確率</b>＝{T('1-p')}")
    ex = example("1つのさいころを投げるとき、3の倍数の目が出る確率を求めなさい。",
                 f"目の出方は1〜6の全部で <b>6通り</b>。3の倍数は 3、6 の <b>2通り</b>。"
                 f"だから　{T('\\dfrac{2}{6}=\\dfrac{1}{3}')}（約分する）")
    qs = [
        q(1, "1つのさいころを投げるとき、偶数の目が出る確率", f"答　{bp(R['even'])}", f"偶数は2、4、6の3通り　{T('\\dfrac36=\\dfrac12')}"),
        q(2, "1つのさいころを投げるとき、5以上の目が出る確率", f"答　{bp(R['ge5'])}", f"5、6の2通り　{T('\\dfrac26=\\dfrac13')}"),
        q(3, "1つのさいころを投げるとき、7の目が出る確率", f"答　{bp(0)}", "7の目はないので、決して起こらない"),
        q(4, "赤玉3個と白玉2個が入った袋から玉を1個取り出すとき、赤玉が出る確率", f"答　{bp(R['red'])}",
          f"玉は全部で5個（5通り）、赤玉は3通り　{T('\\dfrac35')}"),
        q(5, "1から10までの数が1つずつ書かれた10枚のカードから1枚引くとき、4の倍数が出る確率", f"答　{bp(R['mul4'])}",
          f"4の倍数は4、8の2通り　{T('\\dfrac{2}{10}=\\dfrac15')}"),
        q(6, "(5)で、4の倍数が出ない確率", f"答　{bp(1 - R['mul4'])}", f"起こらない確率＝1－（起こる確率）　{T('1-\\dfrac15=\\dfrac45')}"),
        q(7, "(5)のカードから1枚引くとき、素数（1とその数のほかに約数がない数）が出る確率", f"答　{bp(R['prime'])}",
          f"素数は2、3、5、7の4通り（1は素数ではない）　{T('\\dfrac{4}{10}=\\dfrac25')}"),
    ]
    return page(1, "確率の意味と求め方", pt, ex, qs)


def page2():
    pt = point("起こりうる場合を、もれや重なりがないように数えるには、<b>樹形図</b>（えだ分かれの図）をかくとよい。")
    ex = example("2枚の硬貨A、Bを同時に投げるとき、1枚が表で1枚が裏になる確率を求めなさい。",
                 f"右の樹形図より、出方は全部で <b>4通り</b>。1枚が表で1枚が裏になるのは（表、裏）（裏、表）の <b>2通り</b>。"
                 f"だから　{T('\\dfrac24=\\dfrac12')}",
                 f"<div class=treebox><div class=tlab><span>A</span><span>B</span></div>{tree_svg([['表', '裏'], ['表', '裏']], w=40, gap=6.4)}</div>")
    tree3 = f"<div class='anstree'>{tree_svg([['表', '裏']] * 3, w=62, gap=5.0)}</div>" if ANS else ""
    tree_abc = (f"<div class='anstree'>{tree_svg([['A', 'B', 'C'], ['B', 'C'], ['C']], w=58, gap=5)}</div>"
                if False else "")
    qs = [
        q(1, "3枚の硬貨A、B、Cを同時に投げるとき、表と裏の出方は全部で何通りありますか。樹形図をかいて数えなさい。",
          f"答　{b(20, '8')}通り", "1枚ごとに表・裏の2通り　2×2×2＝8", 1.6, tree3),
        q(2, "(1)で、3枚とも表になる確率", f"答　{bp(R['c3all'])}", f"（表、表、表）の1通り　{T('\\dfrac18')}"),
        q(3, "(1)で、2枚が表、1枚が裏になる確率", f"答　{bp(R['c3two'])}",
          f"（表表裏）（表裏表）（裏表表）の3通り　{T('\\dfrac38')}"),
        q(4, "A、B、Cの3人が1列に並ぶとき、並び方は全部で何通りありますか。", f"答　{b(20, '6')}通り",
          "ABC、ACB、BAC、BCA、CAB、CBA の6通り（先頭3通り×2番目2通り×最後1通り）"),
        q(5, "(4)で、Aが先頭になる確率", f"答　{bp(R['afirst'])}", f"ABC、ACB の2通り　{T('\\dfrac26=\\dfrac13')}"),
        q(6, "当たり2本、はずれ1本の3本のくじがある。まずaさんが1本引き、もどさずにbさんが1本引く。2人とも当たる確率",
          f"答　{bp(R['kuji'])}",
          f"当たりを①②、はずれを×とすると、（a，b）は（①②）（①×）（②①）（②×）（×①）（×②）の6通り。<br>"
          f"2人とも当たりは（①②）（②①）の2通り　{T('\\dfrac26=\\dfrac13')}", 1.4),
    ]
    return page(2, "樹形図で数える", pt, ex, qs)


def page3():
    pt = point("大小2つのさいころを投げるとき、目の出方は　6×6＝<b>36通り</b>。<b>表</b>にまとめると数えやすい。")
    ex = example("大小2つのさいころを投げるとき、出る目の和が5になる確率を求めなさい。",
                 f"和が5になるのは（大，小）＝（1，4）（2，3）（3，2）（4，1）の <b>4通り</b>。"
                 f"だから　{T('\\dfrac{4}{36}=\\dfrac19')}")
    qs = [
        q(1, "下の表は、大きいさいころの目を縦に、小さいさいころの目を横にとったものです。2つの目の和を、表の空らんに書き入れなさい。",
          "", "", 0, f"<div class=tw>{dice_table()}</div>"),
        q(2, "出る目の和が7になる確率", f"答　{bp(R['s7'])}", f"表の右上から左下へのななめの6通り　{T('\\dfrac{6}{36}=\\dfrac16')}"),
        q(3, "出る目の和が10以上になる確率", f"答　{bp(R['s10'])}",
          f"和が10・11・12は（4，6）（5，5）（6，4）（5，6）（6，5）（6，6）の6通り　{T('\\dfrac{6}{36}=\\dfrac16')}"),
        q(4, "出る目の積（かけ算の答え）が奇数になる確率", f"答　{bp(R['odd'])}",
          f"どちらも奇数（1、3、5）のとき。3×3＝9通り　{T('\\dfrac{9}{36}=\\dfrac14')}"),
        q(5, "大きいさいころの目が、小さいさいころの目より大きくなる確率", f"答　{bp(R['big'])}",
          f"表の左下の部分。1＋2＋3＋4＋5＝15通り　{T('\\dfrac{15}{36}=\\dfrac{5}{12}')}"),
        q(6, "少なくとも1つは6の目が出る確率", f"答　{bp(R['six'])}",
          f"どちらも6でない出方は 5×5＝25通り。{T('1-\\dfrac{25}{36}=\\dfrac{11}{36}')}"),
    ]
    return page(3, "2つのさいころ", pt, ex, qs)


def page4():
    pt = point("「<b>同時に</b>2個取り出す」「2人を選ぶ」ときは、<b>順番を考えない</b>（AとBを選ぶ＝BとAを選ぶ）。<br>"
               "「並べる」「1番目・2番目」のときは、順番を考える。<br>"
               f"「<b>少なくとも</b>1つ」は、{T('1-')}（1つも起こらない確率）で求めると楽になる。")
    ex = example("A、B、C、Dの4人から、くじで2人の当番を選ぶとき、Aが選ばれる確率を求めなさい。",
                 f"選び方は　AB、AC、AD、BC、BD、CD　の <b>6通り</b>（BAはABと同じ）。Aが入っているのは <b>3通り</b>。"
                 f"だから　{T('\\dfrac36=\\dfrac12')}")
    qs = [
        q(1, "赤玉2個と白玉2個が入った袋から、同時に2個取り出すとき、取り出し方は全部で何通りありますか。", f"答　{b(20, '6')}通り",
          "赤①、赤②、白①、白②とすると　赤①赤②、赤①白①、赤①白②、赤②白①、赤②白②、白①白② の6通り"),
        q(2, "(1)で、2個とも赤玉である確率", f"答　{bp(R['rr'])}", f"赤①赤②の1通り　{T('\\dfrac16')}"),
        q(3, "(1)で、赤玉と白玉が1個ずつである確率", f"答　{bp(R['rw'])}", f"4通り　{T('\\dfrac46=\\dfrac23')}"),
        q(4, "1、2、3、4の4枚のカードから2枚を続けて取り出し、取り出した順に左から並べて2けたの整数をつくる。できる整数は全部で何通りですか。",
          f"答　{b(20, '12')}通り", "十の位が4通り、一の位は残りの3通り　4×3＝12", 1.15),
        q(5, "(4)で、できた整数が偶数になる確率", f"答　{bp(R['ceven'])}",
          f"一の位が2か4。12、32、42、14、24、34 の6通り　{T('\\dfrac{6}{12}=\\dfrac12')}"),
        q(6, "(4)で、できた整数が40以上になる確率", f"答　{bp(R['c40'])}", f"41、42、43 の3通り　{T('\\dfrac{3}{12}=\\dfrac14')}"),
        q(7, "当たりが2本入った5本のくじから、同時に2本引くとき、少なくとも1本は当たる確率", f"答　{bp(R['atari'])}",
          f"引き方は全部で10通り。2本ともはずれは3通り（はずれ3本から2本）。{T('1-\\dfrac{3}{10}=\\dfrac{7}{10}')}", 1.15),
    ]
    return page(4, "取り出し方・いろいろな確率", pt, ex, qs)


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; font-size: 10pt; }
.page { width: 210mm; height: 297mm; padding: 9mm 12mm 9mm; page-break-after: always;
        display: flex; flex-direction: column; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.katex { font-size: 1.07em; }
.head { display: flex; align-items: baseline; white-space: nowrap; border-bottom: 1pt solid #111; padding-bottom: 1.6mm; }
.head b { font-size: 12.5pt; }
.head .sub { font-size: 10pt; margin-left: 2mm; }
.head .cl { margin-left: auto; font-size: 9.5pt; }
.head .u { display: inline-block; border-bottom: .7pt solid #111; }
.head .kotae { margin-left: auto; font-weight: 700; color: #b4232c; font-size: 12pt; }
.point { margin-top: 2.4mm; border: 1pt solid #1f5fbf; border-radius: 2.5mm; padding: 2mm 3mm; display: flex; gap: 3mm;
         line-height: 1.8; background: #f3f7fd; }
.tag, .tag2 { flex: none; font-weight: 700; font-size: 9pt; color: #fff; background: #1f5fbf; border-radius: 1.5mm;
              padding: .3mm 2mm; height: fit-content; margin-top: .6mm; }
.tag2 { background: #2f7d32; margin-right: 2mm; display: inline-block; }
.ex { margin-top: 2mm; border: .9pt solid #2f7d32; border-radius: 2.5mm; padding: 2mm 3mm; display: flex; gap: 3mm; line-height: 1.75; }
.exl { flex: 1; }
.sol { margin-top: 1mm; padding-top: 1mm; border-top: .5pt dashed #999; }
.treebox { display: flex; flex-direction: column; align-items: center; flex: none; }
.tlab { display: flex; gap: 10mm; font-size: 9pt; margin-left: 6mm; }
.big { margin-top: 2.6mm; font-weight: 700; font-size: 10.5pt; display: flex; align-items: center; gap: 2mm; }
.big .box { display: inline-flex; padding: 0 1.6mm; height: 5.6mm; border: .9pt solid #111; align-items: center; justify-content: center; font-size: 9.5pt; }
.qs { flex: 1; min-height: 0; display: flex; flex-direction: column; margin-top: 1mm; }
.sqi { display: flex; flex-direction: column; border-top: .4pt solid #bbb; padding: 1.4mm 0 1mm; }
.qt { display: flex; flex-wrap: wrap; line-height: 1.6; }
.qt > div { flex: 1 1 90mm; }
.qt .no { flex: none; width: 7.5mm; font-size: 9pt; }
.ans.in { margin-left: auto; align-self: flex-end; white-space: nowrap; padding-left: 3mm; }
.work { flex: 1; margin: .6mm 0 0 7.5mm; line-height: 1.75; font-size: 9.5pt; color: #c0141e; }
.ul { display: inline-block; border-bottom: .8pt solid #111; height: 7mm; vertical-align: bottom; }
.ul.fill { color: #c0141e; font-weight: 700; text-align: center; height: auto; line-height: 1.3; }
.fig text { font-family: 'Noto Sans CJK JP'; }
.anstree { display: flex; justify-content: flex-start; margin-left: 10mm; }
.anstree text { fill: #c0141e; }
.tw { display: flex; justify-content: center; margin: 1mm 0; }
table.dice { border-collapse: collapse; }
table.dice th, table.dice td { border: .7pt solid #333; width: 13mm; height: 7.2mm; text-align: center; font-size: 10.5pt; }
table.dice th { background: #eee; font-weight: 700; }
table.dice th.corner { font-size: 8pt; }
table.dice td { color: #c0141e; font-weight: 700; }
"""


def build(ans):
    global ANS
    ANS = ans
    return page1() + page2() + page3() + page4()


if __name__ == "__main__":
    print("確認OK：すべての場合を数えた確率と答えが一致", len(R), "問")
    write_pdfs([
        (doc(CSS, build(False)), f"{FILE}.pdf"),
        (doc(CSS, build(True)), f"{FILE}_ans.pdf"),
    ])
