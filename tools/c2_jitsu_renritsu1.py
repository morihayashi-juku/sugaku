"""中2 実力テスト対策①（11/26 木）連立方程式の利用：4ページ＋こたえ4ページ（赤で書きこみ）

  cd tools && python3 c2_jitsu_renritsu1.py

1ページ1テーマ・全幅・計算スペース広め。各ページ「ポイント」→「例題（解き方つき）」→「練習」。
  ① 代金・個数  ② 速さ（道のり・時間・池のまわり）  ③ 割合（増減・割引・食塩水）  ④ 数・過不足・実力テスト形式
- 答えは SymPy で連立方程式を解いて確かめる（SOL）。
- 出力：pdf/c2_jitsu_renritsu1.pdf と c2_jitsu_renritsu1_ans.pdf
"""
import sympy as sp

from texlib import doc, tex as T, write_pdfs
from c2_kakuritsu_nyumon import CSS as BASE_CSS, point, example

FILE = "c2_jitsu_renritsu1"
ANS = False
x, y = sp.symbols("x y")


def solve(e1, e2):
    s = sp.solve([e1, e2], [x, y], dict=True)[0]
    return s[x], s[y]


# ---------- 答えの確かめ ----------
SOL = {
    "ex1": solve(sp.Eq(x + y, 12), sp.Eq(120 * x + 50 * y, 880)),
    "p1": solve(sp.Eq(x + y, 10), sp.Eq(80 * x + 150 * y, 1220)),
    "p2": solve(sp.Eq(2 * x + 3 * y, 2600), sp.Eq(x + 4 * y, 2300)),
    "p3": solve(sp.Eq(x + y, 15), sp.Eq(50 * x + 84 * y, 954)),
    "ex2": solve(sp.Eq(x + y, 1800), sp.Eq(x / 60 + y / 150, 24)),
    "s1": solve(sp.Eq(x + y, 12), sp.Eq(x / 3 + y / 5, sp.Rational(10, 3))),
    "s2": solve(sp.Eq(x + y, 3), sp.Eq(15 * x + 3 * y, 33)),
    "s3": solve(sp.Eq(12 * (x + y), 2400), sp.Eq(60 * (x - y), 2400)),
    "ex3": solve(sp.Eq(x + y, 500), sp.Eq(sp.Rational(10, 100) * x - sp.Rational(5, 100) * y, 5)),
    "w1": solve(sp.Eq(x + y, 1500), sp.Eq(sp.Rational(8, 10) * x + sp.Rational(9, 10) * y, 1260)),
    "w2": solve(sp.Eq(x + y, 360), sp.Eq(sp.Rational(20, 100) * x - sp.Rational(10, 100) * y, 12)),
    "w3": solve(sp.Eq(x + y, 500), sp.Eq(sp.Rational(8, 100) * x + sp.Rational(3, 100) * y, 25)),
    "n1": solve(sp.Eq(x + y, 11), sp.Eq((10 * y + x) - (10 * x + y), 27)),
    "n2": solve(sp.Eq(y, 3 * x + 8), sp.Eq(y, 4 * x - 7)),
    "n3": solve(sp.Eq(x + y, 1300), sp.Eq(3 * x + 5 * y, 5100)),
}
EXP = {"ex1": (4, 8), "p1": (4, 6), "p2": (700, 400), "p3": (9, 6), "ex2": (1200, 600), "s1": (7, 5), "s2": (2, 1),
       "s3": (120, 80), "ex3": (200, 300), "w1": (900, 600), "w2": (160, 200), "w3": (200, 300), "n1": (4, 7),
       "n2": (15, 53), "n3": (700, 600)}
assert {k: tuple(v) for k, v in SOL.items()} == EXP, SOL
assert sp.Rational(8, 10) * (4 * 700 + 18 * 600) == 10880        # ④(3)③ 団体割引


# ---------- 部品 ----------
def b(w, v=""):
    if ANS:
        return f"<span class='ul fill' style='width:{w}mm'>{v}</span>"
    return f"<span class=ul style='width:{w}mm'></span>"


def eqs(e1, e2, ans_html):
    """連立方程式のらん（大かっこ＋2行）と答え"""
    return (f"<div class=eqrow><span class=lb>連立方程式</span><span class=brace>{{</span>"
            f"<span class=stack>{b(58, T(e1))}{b(58, T(e2))}</span>"
            f"<span class=lb style='margin-left:6mm'>答</span>{ans_html}</div>")


def q(no, text, ans_row, work="", grow=1):
    return (f"<div class=sqi style='flex:{grow} 1 0'><div class=qt><span class=no>{f'({no})' if no else ''}</span><div>{text}</div></div>"
            f"<div class=work>{work if ANS else ''}</div>{ans_row}</div>")


def head(n, title):
    right = ("<span class=kotae>こたえ</span>" if ANS else
             "<span class=cl>（　）組（　）番　名前 <span class=u style='width:34mm'></span></span>")
    return (f"<div class=head><b>中2数学 実力テスト対策① 連立方程式の利用</b>"
            f"<span class=sub>{'①②③④'[n - 1]} {title}</span>{right}</div>")


def page(n, title, pt, ex, qs, lead="次の問いに答えなさい。連立方程式をつくって解き、答えを書きなさい。"):
    return (f"<div class=page>{head(n, title)}{pt}{ex}"
            f"<div class=big><span class=box>練習</span>{lead}</div>"
            f"<div class=qs>{''.join(qs)}</div></div>")


STEPS = ("<b>解き方の手順</b>　①何を " + T("x") + "、" + T("y") + " にするか決める　②等しい関係を2つ見つけて、連立方程式をつくる"
         "　③解く　④答えが問題に合っているか確かめて、単位をつけて答える")


# ---------- ページ ----------
def page1():
    pt = point(STEPS + "<br>代金の問題は「<b>個数の関係</b>」と「<b>代金の関係</b>」の2つで式をつくる。")
    ex = example("1個120円のりんごと1個50円のみかんを合わせて12個買ったら、代金は880円でした。りんごとみかんをそれぞれ何個買いましたか。",
                 f"りんごを {T('x')} 個、みかんを {T('y')} 個とすると　{T('\\begin{cases} x+y=12 \\\\ 120x+50y=880 \\end{cases}')}"
                 f"　これを解いて {T('x=4,\\ y=8')}　　答　りんご4個、みかん8個")
    qs = [
        q(1, "1個80円のパンと1個150円のおにぎりを合わせて10個買ったら、代金は1220円でした。パンとおにぎりをそれぞれ何個買いましたか。",
          eqs("x+y=10", "80x+150y=1220", f"パン{b(14, '4')}個、おにぎり{b(14, '6')}個"),
          f"パン {T('x')} 個、おにぎり {T('y')} 個。{T('y=10-x')} を代入して {T('80x+1500-150x=1220')}　{T('-70x=-280')}　{T('x=4')}、{T('y=6')}"),
        q(2, "ある博物館の入館料は、大人2人と子ども3人で2600円、大人1人と子ども4人で2300円です。大人1人、子ども1人の入館料はそれぞれ何円ですか。",
          eqs("2x+3y=2600", "x+4y=2300", f"大人{b(16, '700')}円、子ども{b(16, '400')}円"),
          f"大人 {T('x')} 円、子ども {T('y')} 円。下の式を2倍してひくと {T('-5y=-2000')}　{T('y=400')}、{T('x=2300-1600=700')}"),
        q(3, "50円切手と84円切手を合わせて15枚買ったら、代金は954円でした。それぞれ何枚買いましたか。",
          eqs("x+y=15", "50x+84y=954", f"50円{b(14, '9')}枚、84円{b(14, '6')}枚"),
          f"50円切手 {T('x')} 枚、84円切手 {T('y')} 枚。上の式を50倍してひくと {T('34y=204')}　{T('y=6')}、{T('x=9')}"),
    ]
    return page(1, "代金・個数", pt, ex, qs)


def page2():
    pt = point(f"（道のり）＝（速さ）×（時間）　（時間）＝{T('\\dfrac{道のり}{速さ}')}<br>"
               f"「<b>道のりの関係</b>」と「<b>時間の関係</b>」で式をつくる。単位（m と km、分と時間）をそろえる。")
    ex = example("家から1800m離れた駅まで、はじめは分速60mで歩き、途中から分速150mで走ったら、全部で24分かかりました。歩いた道のりと走った道のりを求めなさい。",
                 f"歩いた道のり {T('x')} m、走った道のり {T('y')} m とすると　"
                 f"{T('\\begin{cases} x+y=1800 \\\\ \\dfrac{x}{60}+\\dfrac{y}{150}=24 \\end{cases}')}"
                 f"　下の式を300倍して {T('5x+2y=7200')}　解いて {T('x=1200,\\ y=600')}　答　歩いた道のり1200m、走った道のり600m")
    qs = [
        q(1, "A地点から峠をこえてB地点まで、全部で12kmの道のりを歩きました。上りは時速3km、下りは時速5kmで歩き、全部で3時間20分かかりました。上りと下りの道のりを求めなさい。",
          eqs("x+y=12", "\\dfrac{x}{3}+\\dfrac{y}{5}=\\dfrac{10}{3}", f"上り{b(14, '7')}km、下り{b(14, '5')}km"),
          f"上り {T('x')} km、下り {T('y')} km。3時間20分＝{T('\\dfrac{10}{3}')} 時間。下の式を15倍して {T('5x+3y=50')}<br>"
          f"{T('5x+3(12-x)=50')}　{T('2x=14')}　{T('x=7')}、{T('y=5')}", 1.25),
        q(2, "家から33km離れた町まで、はじめは自転車で時速15km、途中からは歩いて時速3kmで進んだら、全部で3時間かかりました。自転車で進んだ時間と歩いた時間を求めなさい。",
          eqs("x+y=3", "15x+3y=33", f"自転車{b(14, '2')}時間、歩き{b(14, '1')}時間"),
          f"自転車 {T('x')} 時間、歩き {T('y')} 時間。道のりの式から上の式を3倍してひくと {T('12x=24')}　{T('x=2')}、{T('y=1')}"),
        q(3, "1周2400mの池のまわりを、AさんとBさんが同じ地点から同時に出発します。反対の向きに進むと12分後に出会い、同じ向きに進むと60分後にAさんがBさんにちょうど1周差をつけて追いつきます。2人の速さはそれぞれ分速何mですか。",
          eqs("12x+12y=2400", "60x-60y=2400", f"A 分速{b(14, '120')}m、B 分速{b(14, '80')}m"),
          f"Aを分速 {T('x')} m、Bを分速 {T('y')} m。反対向き＝2人の道のりの和が1周、同じ向き＝道のりの差が1周<br>"
          f"{T('x+y=200')}、{T('x-y=40')} を解いて {T('x=120')}、{T('y=80')}", 1.25),
    ]
    return page(2, "速さ", pt, ex, qs)


def page3():
    pt = point(f"{T('a')}％ → {T('\\dfrac{a}{100}')}　　{T('b')}割引 → 定価の {T('\\dfrac{10-b}{10}')}　　食塩の重さ＝食塩水の重さ×濃度<br>"
               "<b>もとの量</b>を " + T("x") + "、" + T("y") + " にすると式がつくりやすい。答えるものが「今年の人数」などのときは、最後に計算しなおす。")
    ex = example("ある中学校の昨年の生徒数は500人でした。今年は、男子が10％増え、女子が5％減ったので、全体で5人増えました。今年の男子と女子の人数を求めなさい。",
                 f"昨年の男子 {T('x')} 人、女子 {T('y')} 人とすると　"
                 f"{T('\\begin{cases} x+y=500 \\\\ \\dfrac{10}{100}x-\\dfrac{5}{100}y=5 \\end{cases}')}"
                 f"　解いて {T('x=200,\\ y=300')}<br>今年の男子は {T('200\\times1.1=220')}、女子は {T('300\\times0.95=285')}　答　男子220人、女子285人")
    qs = [
        q(1, "商品Aと商品Bを1個ずつ定価で買うと、合わせて1500円です。Aを定価の2割引、Bを定価の1割引で1個ずつ買ったら、代金は1260円でした。AとBの定価をそれぞれ求めなさい。",
          eqs("x+y=1500", "\\dfrac{8}{10}x+\\dfrac{9}{10}y=1260", f"A{b(16, '900')}円、B{b(16, '600')}円"),
          f"Aの定価 {T('x')} 円、Bの定価 {T('y')} 円。下の式を10倍して {T('8x+9y=12600')}<br>"
          f"上の式を8倍してひくと {T('y=600')}、{T('x=900')}"),
        q(2, "ある店で、先月の商品Aと商品Bの売れた個数は合わせて360個でした。今月は、先月と比べてAが20％増え、Bが10％減ったので、合わせて12個増えました。今月のAとBの売れた個数をそれぞれ求めなさい。",
          eqs("x+y=360", "\\dfrac{20}{100}x-\\dfrac{10}{100}y=12", f"A{b(16, '192')}個、B{b(16, '180')}個"),
          f"先月のA {T('x')} 個、B {T('y')} 個。下の式を10倍して {T('2x-y=120')}　上の式とたして {T('3x=480')}　{T('x=160')}、{T('y=200')}<br>"
          f"今月のAは {T('160\\times1.2=192')}、Bは {T('200\\times0.9=180')}", 1.2),
        q(3, "8％の食塩水と3％の食塩水を混ぜて、5％の食塩水を500gつくります。それぞれ何g混ぜればよいですか。",
          eqs("x+y=500", "\\dfrac{8}{100}x+\\dfrac{3}{100}y=500\\times\\dfrac{5}{100}", f"8％を{b(16, '200')}g、3％を{b(16, '300')}g"),
          f"8％を {T('x')} g、3％を {T('y')} g。食塩の重さ：{T('0.08x+0.03y=25')}　100倍して {T('8x+3y=2500')}<br>"
          f"上の式を3倍してひくと {T('5x=1000')}　{T('x=200')}、{T('y=300')}", 1.15),
    ]
    return page(3, "割合", pt, ex, qs)


def page4():
    pt = point(f"2けたの自然数は、十の位を {T('x')}、一の位を {T('y')} とすると {T('10x+y')}（入れかえた数は {T('10y+x')}）。<br>"
               "過不足の問題は、「配る数」を2通りの式で表して等しいとおく。")
    ex = example("2けたの自然数があります。十の位の数と一の位の数の和は11で、十の位と一の位を入れかえた数は、もとの数より27大きくなります。もとの自然数を求めなさい。",
                 f"十の位を {T('x')}、一の位を {T('y')} とすると　"
                 f"{T('\\begin{cases} x+y=11 \\\\ (10y+x)-(10x+y)=27 \\end{cases}')}"
                 f"　下の式を整理して {T('-9x+9y=27')}、{T('-x+y=3')}　解いて {T('x=4,\\ y=7')}　答　47")
    qs = [
        q(1, "何人かの生徒にノートを配ります。1人に3冊ずつ配ると8冊余り、1人に4冊ずつ配ると7冊たりません。生徒の人数とノートの冊数を求めなさい。",
          eqs("y=3x+8", "y=4x-7", f"生徒{b(14, '15')}人、ノート{b(14, '53')}冊"),
          f"生徒 {T('x')} 人、ノート {T('y')} 冊。{T('3x+8=4x-7')}　{T('x=15')}、{T('y=3\\times15+8=53')}"),
        q(2, "ある美術館の入館料は、大人1人と中学生1人で合わせて1300円、大人3人と中学生5人で5100円です。<br>"
             "① 大人1人の入館料を " + T("x") + " 円、中学生1人の入館料を " + T("y") + " 円として、連立方程式をつくって解きなさい。",
          eqs("x+y=1300", "3x+5y=5100", f"大人{b(16, '700')}円、中学生{b(16, '600')}円"),
          f"上の式を3倍してひくと {T('2y=1200')}　{T('y=600')}、{T('x=700')}"),
        q("", "② この美術館では、20人以上の団体は全員の入館料が2割引になります。大人4人と中学生18人の団体で入館したときの入館料の合計を求めなさい。",
          f"<div class=eqrow><span class=lb style='margin-left:auto'>答</span>{b(30, '10880')}円</div>",
          f"22人なので2割引。{T('(700\\times4+600\\times18)\\times\\dfrac{8}{10}=13600\\times0.8=10880')}", .8),
    ]
    return page(4, "数・過不足・実力テストの形", pt, ex, qs)


CSS = BASE_CSS + """
.eqrow { display: flex; align-items: center; justify-content: flex-end; gap: 1.5mm; margin-top: .5mm; white-space: nowrap; }
.eqrow .lb { font-size: 9.5pt; font-weight: 700; }
.brace { font-size: 26pt; line-height: 1; font-weight: 200; margin-left: 1mm; }
.stack { display: inline-flex; flex-direction: column; gap: 1.6mm; }
.stack .ul { height: 7.5mm; display: flex; align-items: flex-end; justify-content: center; }
.stack .ul.fill { height: auto; min-height: 7.5mm; padding-bottom: .4mm; }
.sol .katex-display, .ex .katex { font-size: 1.05em; }
"""


def build(ans):
    global ANS
    ANS = ans
    return page1() + page2() + page3() + page4()


if __name__ == "__main__":
    print("確認OK：15問の連立方程式の答え（SymPy）")
    write_pdfs([
        (doc(CSS, build(False)), f"{FILE}.pdf"),
        (doc(CSS, build(True)), f"{FILE}_ans.pdf"),
    ])
