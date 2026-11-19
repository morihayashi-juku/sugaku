"""中1 比例の基本（U・N 用・テスト後に基本からやり直し）（11/19〜）

  python3 hirei_kihon.py        # tools/ で実行

- 授業・自習：A4・4ページ32問＋こたえ4ページ（木＝A、月の自習＝B。同じ形で数がちがう）
  その1 比例の表と式／その2 比例の式を求める（a＝y÷x）／その3 式を使って値を求める／その4 座標と比例のグラフ
- 宿題（N 用・木曜に渡して金〜水の6日分）：1日4問・A4 1枚に2日分・答えは自学ノート
- 値は Fraction で計算して確かめる。こたえは問題のプリントに赤で書きこんだ形。
- 出力：pdf/hirei_kihon_{A,B}.pdf・_ans、pdf/hirei_kihon_hw1.pdf・_ans
- 次は「反比例の基本」→「グラフ」の順（先生の希望・11/19「基本からやり直し」）。
"""
from fractions import Fraction as Fr

from teiki_2 import EXTRA, hirei_shiki
from teiki_lib import coords, fs, graph, hw_notebook, t, table, tvals, worksheet
from mathlib import write_pdfs


def paren(v):
    v = Fr(v)
    return t(f"({fs(v)})") if v < 0 else t(fs(v))


def gtable(xs, ys):
    """値がぜんぶ書いてある表"""
    h = "".join(f"<td>{t(str(v))}</td>" for v in xs)
    b = "".join(f"<td>{t(fs(v))}</td>" for v in ys)
    return f"<table class=tb><tr><th>{t('x')}</th>{h}</tr><tr><th>{t('y')}</th>{b}</tr></table>"


def p_table(a, xs):
    a = Fr(a)
    return {"q": f"比例 {t(hirei_shiki(a))} で、表のあいているところをうめなさい。" + table(xs, lambda x: a * x), "noa": True, "albl": "", "a": ""}


def p_given(a, xs):
    a = Fr(a)
    return {"q": f"下の表は、{t('y')} が {t('x')} に比例するようすです。比例定数を答え、{t('y')} を {t('x')} の式で表しなさい。" + gtable(xs, [a * x for x in xs]),
            "albl": "", "a": f"{t('a')}＝{paren(a * xs[1])}÷{paren(xs[1])}＝<b>{t(fs(a))}</b>　<b>{t(hirei_shiki(a))}</b>"}


def p_word(q, a):
    return {"q": f"{q}。{t('y')} を {t('x')} の式で表し、比例定数を答えなさい。", "albl": "",
            "a": f"<b>{t(hirei_shiki(a))}</b>　比例定数 <b>{t(fs(Fr(a)))}</b>"}


def p_shiki(x, y):
    a = Fr(y, x)
    return {"q": f"{t('y')} は {t('x')} に比例し、{t(f'x={x}')} のとき {t(f'y={y}')} です。{t('y')} を {t('x')} の式で表しなさい。",
            "fa": t(hirei_shiki(a)), "a": f"{t('a')}＝{paren(y)}÷{paren(x)}＝{t(fs(a))}"}


def p_y(a, x):
    a = Fr(a)
    return {"q": f"比例 {t(hirei_shiki(a))} で、{t(f'x={x}')} のときの {t('y')} の値を求めなさい。", "fa": t(f"y={fs(a * x)}"),
            "a": f"{t('y')}＝{t(fs(a))}×{paren(x)}", "checks": [(a * x).denominator == 1]}


def p_x(a, y):
    a = Fr(a)
    return {"q": f"比例 {t(hirei_shiki(a))} で、{t(f'y={y}')} のときの {t('x')} の値を求めなさい。", "fa": t(f"x={fs(y / a)}"),
            "a": f"{paren(y)}＝{t(fs(a))}{t('x')}　{t('x')}＝{paren(y)}÷{paren(a)}", "checks": [(y / a).denominator == 1]}


def p_two(x, y, kind, v):
    """式を求めてから値を求める（kind='x' なら x=v のときの y、'y' なら y=v のときの x）"""
    a = Fr(y, x)
    if kind == "x":
        ask, ans = f"{t(f'x={v}')} のときの {t('y')} の値", t(f"y={fs(a * v)}")
        ok = (a * v).denominator == 1
    else:
        ask, ans = f"{t(f'y={v}')} のときの {t('x')} の値", t(f"x={fs(v / a)}")
        ok = (v / a).denominator == 1
    return {"q": f"{t('y')} は {t('x')} に比例し、{t(f'x={x}')} のとき {t(f'y={y}')} です。{ask}を求めなさい。", "fa": ans,
            "a": f"まず式　{t(hirei_shiki(a))}", "checks": [ok]}


def p_gshiki(a, pt):
    a = Fr(a)
    return {"q": f"図の直線は比例のグラフです。{t('y')} を {t('x')} の式で表しなさい。", "fig": graph(line=a, pts=[(pt[0], pt[1], "")], size=32),
            "fa": t(hirei_shiki(a)), "a": f"({pt[0]}, {pt[1]}) を通る".replace("-", "−"), "checks": [a * pt[0] == pt[1]]}


def p_draw(a, pts):
    a = Fr(a)
    return {"q": f"比例 {t(hirei_shiki(a))} のグラフをかきなさい。", "fig": graph(size=32, ans_line=a, ans_pts=[(x, y, "") for x, y in pts]),
            "albl": "", "noa": True, "a": "", "checks": [all(a * x == y for x, y in pts)]}


def make(P):
    return [
        ("その1", "比例の表と式", f"ポイント：比例は {t('y=ax')}（{t('a')} が<b>比例定数</b>）。表は、{t('x')} の数に {t('a')} を<b>かける</b>と {t('y')}。　例）{t('y=-2x')} で {t('x=3')} → {t('y=-2*3=-6')}", [
            *[p_table(a, xs) for a, xs in P["tables"]],
            *[p_given(a, xs) for a, xs in P["given"]],
            *[p_word(q, a) for q, a in P["words"]],
        ]),
        ("その2", "比例の式を求める", f"ポイント：比例定数 {t('a')}＝<b>{t('y')}÷{t('x')}</b>。符号に注意して計算し、{t('y=ax')} の {t('a')} に入れる。　例）{t('x=2')} のとき {t('y=-6')} → {t('a=(-6)/2=-3')} → {t('y=-3x')}", [
            p_shiki(x, y) for x, y in P["pairs"]]),
        ("その3", "式を使って値を求める", f"ポイント：{t('x')} の値がわかっているときは<b>かける</b>。{t('y')} の値がわかっているときは、式に入れて<b>方程式</b>を解く。　例）{t('y=3x')} で {t('y=12')} → {t('12=3x')} → {t('x=4')}", [
            *[p_y(a, x) for a, x in P["ys"]],
            *[p_x(a, y) for a, y in P["xs"]],
            *[p_two(*z) for z in P["two"]],
        ]),
        ("その4", "座標と比例のグラフ", f"ポイント：座標は ({t('x')}, {t('y')}) の順。比例のグラフは<b>原点を通る直線</b>。式は、通る点（マス目の交わるところ）を読んで {t('a')}＝{t('y')}÷{t('x')}。", [
            {"q": "図の点 A〜D の座標を書きなさい。<br>" + coords(P["pts"]), "fig": graph(pts=P["pts"], size=32), "albl": "", "noa": True, "a": ""},
            {"q": "次の点を、図にかき入れなさい。<br>" + "　".join(f"{n}({x}, {y})".replace("-", "−") for x, y, n in P["plot"]),
             "fig": graph(size=32, ans_pts=P["plot"]), "albl": "", "noa": True, "a": ""},
            *[p_gshiki(a, pt) for a, pt in P["gshiki"]],
            *[p_draw(a, pts) for a, pts in P["draw"]],
            {"q": f"比例 {t(hirei_shiki(P['pass'][0]))} のグラフは、点 ({P['pass'][1]}, □) を通ります。□に入る数を書きなさい。".replace("(-", "(−"), "albl": "□＝",
             "fa": t(fs(Fr(P['pass'][0]) * P['pass'][1])), "a": f"{t('y')}＝{t(fs(Fr(P['pass'][0])))}×{paren(P['pass'][1])}"},
            {"q": f"次の比例のグラフは、右上がり・右下がりのどちらですか。<br>（1）{t(hirei_shiki(P['dir'][0]))}　（2）{t(hirei_shiki(P['dir'][1]))}", "albl": "",
             "a": f"<b>（1）{'右上がり' if P['dir'][0] > 0 else '右下がり'}　（2）{'右上がり' if P['dir'][1] > 0 else '右下がり'}</b>（{t('a')} が正 → 右上がり、負 → 右下がり）"},
        ]),
    ]


XS5 = [-2, -1, 0, 1, 2]
PA = {
    "tables": [(2, [1, 2, 3, 4, 5]), (3, [0, 1, 2, 3, 4]), (-2, XS5), (-4, XS5)],
    "given": [(5, [1, 2, 3, 4]), (-3, [1, 2, 3, 4])],
    "words": [(f"1個80円のパンを {t('x')} 個買ったときの代金を {t('y')} 円とします", 80), (f"分速60mで {t('x')} 分歩いた道のりを {t('y')} mとします", 60)],
    "pairs": [(2, 8), (3, 15), (4, -12), (-2, 10), (-3, -18), (5, -20), (6, 4), (-4, 6)],
    "ys": [(4, 3), (-5, 2), (-3, -4)],
    "xs": [(6, -18), (-2, 14)],
    "two": [(2, -6, "x", 5), (-4, -8, "x", 3), (3, 12, "y", -8)],
    "pts": [(3, 2, "A"), (-4, 1, "B"), (-2, -3, "C"), (1, -5, "D")],
    "plot": [(2, 4, "E"), (-3, -2, "F"), (0, 3, "G")],
    "gshiki": [(-2, (1, -2)), (Fr(2, 3), (3, 2))],
    "draw": [(2, [(1, 2), (2, 4), (-1, -2), (-2, -4)]), (Fr(-1, 3), [(3, -1), (-3, 1)])],
    "pass": (-3, 2),
    "dir": (4, -2),
}
PB = {
    "tables": [(4, [1, 2, 3, 4, 5]), (5, [0, 1, 2, 3, 4]), (-3, XS5), (-5, XS5)],
    "given": [(6, [1, 2, 3, 4]), (-2, [1, 2, 3, 4])],
    "words": [(f"1本120円のジュースを {t('x')} 本買ったときの代金を {t('y')} 円とします", 120), (f"時速40kmで {t('x')} 時間走った道のりを {t('y')} kmとします", 40)],
    "pairs": [(3, 12), (2, 14), (5, -15), (-3, 21), (-4, -20), (6, -24), (9, 6), (-6, 9)],
    "ys": [(6, 4), (-4, 3), (-2, -7)],
    "xs": [(5, -20), (-3, 18)],
    "two": [(3, -9, "x", 4), (-5, -10, "x", -3), (4, 20, "y", -15)],
    "pts": [(4, 3, "A"), (-3, 2, "B"), (-1, -4, "C"), (2, -2, "D")],
    "plot": [(3, 5, "E"), (-4, -1, "F"), (-2, 0, "G")],
    "gshiki": [(-3, (1, -3)), (Fr(3, 2), (2, 3))],
    "draw": [(3, [(1, 3), (-1, -3)]), (Fr(-1, 2), [(2, -1), (4, -2), (-2, 1), (-4, 2)])],
    "pass": (-4, 2),
    "dir": (-3, 5),
}

# ------------------------------------------------------------ 宿題（N 用・6日分・ノート）
HW_RULE = ("<div class=rule>やり方：自学ノートに日付と問題番号を書き、<b>式 → 答え</b>の順に書く（{a}＝{y}÷{x} などの途中も書く）。"
           "終わったら<b>こたえを見て自分で丸つけ</b>。まちがえたら、正しい式をもう一度ノートに書く。</div>").format(a=t("a"), y=t("y"), x=t("x"))


def h(p):
    """授業プリントの形の問題を、宿題（ノート）の形に（答えはこたえの赤字に）"""
    q = dict(p)
    if p.get("fa"):
        q["a"] = (p["a"] + "　" if p.get("a") else "") + f"答え <b>{p['fa']}</b>"
    q.pop("fa", None)
    q.pop("albl", None)
    return q


def hval(a, xs):
    a = Fr(a)
    return {"q": f"比例 {t(hirei_shiki(a))} で、{'、'.join(t(f'x={x}') for x in xs)} のときの {t('y')} の値をそれぞれ求めなさい。",
            "a": "<b>" + tvals(lambda x: a * x, xs) + "</b>"}


HW = [
    ("金", f"比例は {t('y=ax')}。{t('x')} の数に {t('a')} をかけると {t('y')}。", [
        hval(3, [2, -1, -4]), hval(-4, [3, -2, 0]),
        h(p_word(f"1冊150円のノートを {t('x')} 冊買ったときの代金を {t('y')} 円とします", 150)),
        h(p_word(f"毎分3Lずつ水を入れるとき、{t('x')} 分後の水の量を {t('y')} Lとします", 3)),
    ]),
    ("土", f"比例定数 {t('a')}＝{t('y')}÷{t('x')}。符号に注意。", [h(p_shiki(x, y)) for x, y in [(4, 20), (3, -21), (-5, 15), (-2, -16)]]),
    ("日", f"{t('y')} の値がわかっているときは、式に入れて方程式を解く。", [
        h(p_x(7, -28)), h(p_x(-6, 30)), h(p_y(-5, -3)), h(p_x(-4, -36)),
    ]),
    ("月", "まず式を求めてから、値を求める。", [h(p_two(*z)) for z in [(2, 10, "x", -3), (-3, 12, "x", 2), (4, -8, "y", 6), (-6, -18, "y", -12)]]),
    ("火", f"分数の比例定数もある。{t('a')}＝{t('y')}÷{t('x')} を分数で書く。", [
        h(p_shiki(4, 6)), h(p_shiki(-6, 4)), h(p_y(Fr(2, 3), 9)), h(p_x(Fr(-3, 4), 6)),
    ]),
    ("水", "グラフが通るマス目の点を読んで、式を作る。", [
        {**h(p_gshiki(3, (1, 3))), "fig": graph(line=3, pts=[(1, 3, "")], size=30)},
        {**h(p_gshiki(Fr(-1, 2), (2, -1))), "fig": graph(line=Fr(-1, 2), pts=[(2, -1, "")], size=30)},
        h(p_two(-2, 6, "x", 4)),
        {"q": f"比例 {t('y=-2x')} のグラフは、点 (3, □) を通ります。□に入る数を求めなさい。", "a": f"{t('y=-2*3')}　<b>−6</b>"},
    ]),
]
TITLE_HW = "比例の基本 宿題（6日分）"

if __name__ == "__main__":
    docs = []
    for k, P in (("A", PA), ("B", PB)):
        p, a = worksheet(f"比例の基本 {k}", make(P))
        docs += [(p, f"hirei_kihon_{k}.pdf"), (a, f"hirei_kihon_{k}_ans.pdf")]
    docs += [(hw_notebook(TITLE_HW, HW, HW_RULE), "hirei_kihon_hw1.pdf"), (hw_notebook(TITLE_HW, HW, HW_RULE, answer=True), "hirei_kihon_hw1_ans.pdf")]
    write_pdfs(docs, extra_css=EXTRA)
