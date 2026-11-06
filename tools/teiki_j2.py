"""中1 定期テスト対策　授業②（月 11/9 の授業用・U と K の2人で同じプリント）比例と反比例（A4・4ページ32問＋こたえ2ページ）

  python3 teiki_j2.py        # tools/ で実行

先生の決定（11/6）：月 11/9 は U・K の2人に比例・反比例を授業で教える（N は月曜に来ない）。2人とも同じ内容。
- 前半（その1・その2）は正の数中心の基本 → 2人とも全部。
- 後半（その3・その4）は負の数・グラフ・利用。☆の問題は「チャレンジ」（U は全部、K は☆なしだけでもよい）。
- 各ページのポイント欄に例題と解き方（先生が説明に使う）。問題は対策②・宿題とは別。
- 出力：pdf/teiki_j2.pdf・pdf/teiki_j2_ans.pdf
"""
from fractions import Fraction as Fr

from teiki_2 import EXTRA, hanpi_shiki, hirei_shiki
from teiki_lib import table, tvals
from teiki_j1 import ex
from teiki_lib import coords, graph, t, worksheet
from mathlib import write_pdfs

STAR = "<b>☆</b>"


def hr(x, y, star=False):
    a = Fr(y, x)
    return {"q": f"{STAR if star else ''}{t('y')} は {t('x')} に比例し、{t(f'x={x}')} のとき {t(f'y={y}')} です。{t('y')} を {t('x')} の式で表しなさい。",
            "albl": t("y="), "fa": t(hirei_shiki(a)[2:]), "a": f"{t('a')}＝{t(str(y))}÷{t('(' + str(x) + ')' if x < 0 else str(x))}＝{t(str(a))}　→　<b>{t(hirei_shiki(a))}</b>",
            "checks": [a.denominator == 1]}


def hn(x, y, star=False):
    a = x * y
    return {"q": f"{STAR if star else ''}{t('y')} は {t('x')} に反比例し、{t(f'x={x}')} のとき {t(f'y={y}')} です。{t('y')} を {t('x')} の式で表しなさい。",
            "albl": t("y="), "fa": t(hanpi_shiki(a)[2:]), "a": f"{t('a')}＝{t(str(x))}×{t('(' + str(y) + ')' if y < 0 else str(y))}＝{t(str(a))}　→　<b>{t(hanpi_shiki(a))}</b>"}


def tb(f, xs, fn, star=False):
    return {"q": f"{STAR if star else ''}{t(f)} で、表のあいているところをうめなさい。" + table(xs, fn), "noa": True, "albl": "",
            "a": "<b>" + tvals(fn, xs) + "</b>"}


def use(q, shiki, val_a, checks=(), star=False):
    return {"q": (STAR if star else "") + q, "albl": "", "a": f"<b>{t(shiki)}</b>、<b>{val_a}</b>", "checks": list(checks)}


PJ2 = [(2, 4, "A"), (-3, 1, "B"), (-1, -4, "C"), (5, -3, "D")]
SECS = [
    ("その1", "比例の式と表", ex(f"{t('y=3x')} の表を作る。{t('x=2')} のときは？",
                             [f"{t('x')} に3を<b>かける</b>", t("y=3*2=6"), f"表では {t('y')}÷{t('x')} がいつも3（比例定数）", f"式は <b>{t('y=ax')}</b>"]), [
        tb("y=2x", [1, 2, 3, 4, 5], lambda x: 2 * x),
        tb("y=4x", [0, 1, 2, 3, 4], lambda x: 4 * x),
        hr(3, 15), hr(4, 24),
        {"q": f"{t('y=3x')} で、{t('x=7')} のときの {t('y')} の値を求めなさい。", "albl": t("y="), "a": f"<b>{t('21')}</b>", "checks": [3 * 7 == 21]},
        {"q": f"{t('y=8x')} で、{t('y=40')} のときの {t('x')} の値を求めなさい。", "albl": t("x="), "a": f"{t('40=8x')}　→　<b>{t('5')}</b>", "checks": [Fr(40, 8) == 5]},
        {"q": f"1本70円のペンを {t('x')} 本買ったときの代金を {t('y')} 円とします。{t('y')} を {t('x')} の式で表しなさい。", "albl": t("y="), "a": f"<b>{t('y=70x')}</b>（比例）"},
        {"q": f"時速40kmで {t('x')} 時間走ったときの道のりを {t('y')} kmとします。{t('y')} を {t('x')} の式で表しなさい。", "albl": t("y="), "a": f"<b>{t('y=40x')}</b>（比例）"},
    ]),
    ("その2", "反比例の式と表", ex(f"{t('y={12|x}')} の表を作る。{t('x=3')} のときは？",
                               [f"12を {t('x')} で<b>わる</b>", t("y=12/3=4"), f"表では {t('x')}×{t('y')} がいつも12（比例定数）", f"式は <b>{t('y={a|x}')}</b>"]), [
        tb("y={24|x}", [1, 2, 3, 4, 6], lambda x: Fr(24, x)),
        tb("y={36|x}", [1, 2, 3, 4, 6], lambda x: Fr(36, x)),
        hn(2, 9), hn(5, 6),
        {"q": f"{t('y={20|x}')} で、{t('x=4')} のときの {t('y')} の値を求めなさい。", "albl": t("y="), "a": f"<b>{t('5')}</b>", "checks": [Fr(20, 4) == 5]},
        {"q": f"{t('y={48|x}')} で、{t('y=8')} のときの {t('x')} の値を求めなさい。", "albl": t("x="), "a": f"{t('8={48|x}')}　→　<b>{t('6')}</b>", "checks": [Fr(48, 8) == 6]},
        {"q": f"30個のあめを {t('x')} 人で同じ数ずつ分けると、1人 {t('y')} 個になります。{t('y')} を {t('x')} の式で表しなさい。", "albl": t("y="), "a": f"<b>{t('y={30|x}')}</b>（反比例）"},
        {"q": f"面積が16cm²の長方形の縦を {t('x')} cm、横を {t('y')} cmとします。{t('y')} を {t('x')} の式で表しなさい。", "albl": t("y="), "a": f"<b>{t('y={16|x}')}</b>（反比例）"},
    ]),
    ("その3", "座標とグラフ（☆はチャレンジ）", ex("点 (3, −2) の場所は？",
                                         [f"原点から {t('x')} 座標の3 → <b>右へ3</b>", f"{t('y')} 座標の −2 → <b>下へ2</b>",
                                          f"比例のグラフは<b>原点を通る直線</b>、反比例は<b>双曲線</b>"]), [
        {"q": "図の点 A〜D の座標を書きなさい。<br>" + coords(PJ2), "fig": graph(pts=PJ2, size=38), "albl": "", "noa": True,
         "a": "<b>A(2, 4)、B(−3, 1)、C(−1, −4)、D(5, −3)</b>"},
        {"q": "次の点を、図にかき入れなさい。<br>E(−2, 4)　F(3, −3)　G(−4, 0)", "fig": graph(size=38, ans_pts=[(-2, 4, "E"), (3, -3, "F"), (-4, 0, "G")]), "albl": "", "noa": True,
         "a": "E は左へ2・上へ4、F は右へ3・下へ3、G は左へ4（" + t("x") + " 軸の上）"},
        {"q": "図の直線は比例のグラフです。式を求めなさい。", "fig": graph(line=3, pts=[(1, 3, "")], size=34), "albl": t("y="),
         "fa": t('3x'), "noa": True, "a": f"(1, 3) を通る　<b>{t('y=3x')}</b>"},
        {"q": "図の直線は比例のグラフです。式を求めなさい。", "fig": graph(line=Fr(1, 2), pts=[(2, 1, "")], size=34), "albl": t("y="),
         "fa": t('{1|2}x'), "noa": True, "a": f"(2, 1) を通る　<b>{t('y={1|2}x')}</b>"},
        {"q": f"{STAR}図の直線は比例のグラフです。式を求めなさい。", "fig": graph(line=-1, pts=[(2, -2, "")], size=34), "albl": t("y="),
         "fa": t('-x'), "noa": True, "a": f"(2, −2) を通る　<b>{t('y=-x')}</b>"},
        {"q": "図の曲線は反比例のグラフです。式を求めなさい。", "fig": graph(hyper=12, pts=[(3, 4, "")], size=34), "albl": t("y="),
         "fa": t('{12|x}'), "noa": True, "a": f"(3, 4) を通る　<b>{t('y={12|x}')}</b>"},
        {"q": f"{STAR}図の曲線は反比例のグラフです。式を求めなさい。", "fig": graph(hyper=-4, pts=[(2, -2, "")], size=34), "albl": t("y="),
         "fa": t('-{4|x}'), "noa": True, "a": f"(2, −2) を通る　<b>{t('y=-{4|x}')}</b>"},
        {"q": f"比例 {t('y=2x')} のグラフをかきなさい。", "fig": graph(size=34, ans_line=2, ans_pts=[(1, 2, ""), (-1, -2, "")]), "albl": "", "noa": True, "a": "原点と (1, 2) を通る直線（(−1, −2) も通る）"},
    ]),
    ("その4", "負の数・利用（☆はチャレンジ）", ex(f"{t('y=-2x')} で、{t('x=-3')} のときの {t('y')} は？",
                                          [f"{t('-2*(-3)')}", "（−）×（−）は（＋）", "<b>" + t("y=6") + "</b>"]), [
        tb("y=-2x", [-2, -1, 0, 1, 2], lambda x: -2 * x, star=True),
        hr(-2, 8, star=True), hn(-3, 4, star=True),
        {"q": f"{STAR}{t('y=-{18|x}')} で、{t('x=6')} のときの {t('y')} の値を求めなさい。", "albl": t("y="), "a": f"<b>{t('-3')}</b>", "checks": [Fr(-18, 6) == -3]},
        use(f"同じ紙20枚の重さは60gです。紙 {t('x')} 枚の重さを {t('y')} gとして、{t('y')} を {t('x')} の式で表しなさい。また、30枚の重さを求めなさい。", "y=3x", "90g", [Fr(60, 20) == 3, 3 * 30 == 90]),
        use(f"40Lの水そうに毎分 {t('x')} Lずつ水を入れると、{t('y')} 分でいっぱいになります。{t('y')} を {t('x')} の式で表しなさい。また、毎分5Lずつ入れると何分でいっぱいになりますか。", "y={40|x}", "8分", [Fr(40, 5) == 8]),
        use(f"同じ針金4mの重さは100gです。針金 {t('x')} mの重さを {t('y')} gとして、{t('y')} を {t('x')} の式で表しなさい。また、350gの針金は何mですか。", "y=25x", "14m", [Fr(100, 4) == 25, Fr(350, 25) == 14], star=True),
        use(f"歯の数が36の歯車Aが毎分5回転しています。Aとかみ合う歯の数 {t('x')} の歯車Bは毎分 {t('y')} 回転します。{t('y')} を {t('x')} の式で表しなさい。また、Bの歯の数が30のとき、毎分何回転しますか。", "y={180|x}", "6回転", [36 * 5 == 180, Fr(180, 30) == 6], star=True),
    ]),
]

if __name__ == "__main__":
    prob, ans = worksheet("授業 比例と反比例", SECS)
    write_pdfs([(prob, "teiki_j2.pdf"), (ans, "teiki_j2_ans.pdf")], extra_css=EXTRA)
