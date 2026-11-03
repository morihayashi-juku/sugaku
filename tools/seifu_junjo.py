"""計算の順序（正の数だけ・×÷が先）（A4・問題2ページ＋こたえ1ページ）

  python3 tools/seifu_junjo.py        # 全パターン
  python3 tools/seifu_junjo.py C      # パターンCだけ

ねらい：符号の計算とは切りはなして「何から計算するか」だけを練習する（K 用に作成）。
- その1：×が1つ＋たし算・ひき算。×のところに下線を引いてから、そこを先に計算する（下線と途中式の欄つき）
- その2：÷、×が2つ、3つの項、かっこ
- 式："*" は ×、"/" は ÷。途中式も書く。答えが0以上の整数で、途中もマイナスにならないか確かめる。
- 出力：pdf/seifu_junjo_{パターン}.pdf と _ans.pdf
"""
import sys

from mathlib import answer_doc, fm, problem_doc, write_pdfs, CIRC

PATTERNS = {
    "A": [
        ("3+2*4", ["3+8"]), ("5*3+4", ["15+4"]), ("20-3*4", ["20-12"]), ("6*2-5", ["12-5"]),
        ("9+4*5", ["9+20"]), ("4*7-10", ["28-10"]), ("35-5*6", ["35-30"]), ("2+6*3", ["2+18"]),
        ("18/3+4", ["6+4"]), ("20-12/4", ["20-3"]), ("2*3+4*5", ["6+20"]), ("30-4*6+2", ["30-24+2", "6+2"]),
        ("24/6+3*2", ["4+6"]), ("40-6*5-3", ["40-30-3", "10-3"]), ("(3+5)*2", ["8*2"]), ("4*(9-6)", ["4*3"]),
    ],
    "B": [
        ("4+3*5", ["4+15"]), ("6*4+2", ["24+2"]), ("25-4*5", ["25-20"]), ("7*3-8", ["21-8"]),
        ("8+2*6", ["8+12"]), ("5*6-12", ["30-12"]), ("41-7*5", ["41-35"]), ("1+8*3", ["1+24"]),
        ("21/7+5", ["3+5"]), ("30-18/6", ["30-3"]), ("3*4+2*6", ["12+12"]), ("50-6*7+3", ["50-42+3", "8+3"]),
        ("36/9+4*3", ["4+12"]), ("45-8*5-2", ["45-40-2", "5-2"]), ("(4+6)*3", ["10*3"]), ("5*(11-7)", ["5*4"]),
    ],
}
TITLE = "計算の順序"
EX = {"A": "3＋<u>2×4</u> ＝ 3＋8 ＝ 11", "B": "4＋<u>3×5</u> ＝ 4＋15 ＝ 19"}

SCAF = "<div class=scaf><span class=ln>＝</span><span class=ln>＝</span></div>"


def check(key, probs):
    out = []
    for q, steps in probs:
        v = eval(q)
        assert v == int(v) and v >= 0, (key, q, v)
        for s in steps:
            assert eval(s) == v, (key, q, s, eval(s), v)
        # 左から順に計算したときと答えがちがうか（順序を考えないと間ちがえる問題か）は表示しない・参考
        out.append(int(v))
    return out


def build(key):
    probs = PATTERNS[key]
    ans = check(key, probs)
    title = f"{TITLE} {key}"
    prob = problem_doc(title, [
        {"label": "その1", "sub": "×が1つ（正の数だけ）", "scaffold": SCAF, "probs": [q for q, _ in probs[:8]],
         "tip": f"ポイント：<b>×のところに下線を引いて、そこを先に</b>計算しよう。たし算・ひき算はそのあと。　例）<span class=ex>{EX[key]}</span>"},
        {"label": "その2", "sub": "÷・×が2つ・かっこ", "scaffold": SCAF, "probs": [q for q, _ in probs[8:]],
         "tip": "ポイント：<b>÷も×と同じで先に</b>計算しよう。×・÷が2つあったら、両方とも先に。<b>( ) があれば、そこがいちばん先。</b>"},
    ])
    rows = []
    for i, (q, steps) in enumerate(probs):
        mid = "".join(f"<span class=st>＝ {fm(s)}</span>　" for s in steps)
        rows.append(f"<div class=a>{CIRC[i]}　{fm(q)}<br>{mid}＝ <span class=res>{ans[i]}</span></div>")
    ansh = answer_doc(title, [{"label": "その1　×が1つ", "rows": rows[:8]}, {"label": "その2　÷・×が2つ・かっこ", "rows": rows[8:]}])
    return [(prob, f"seifu_junjo_{key}.pdf"), (ansh, f"seifu_junjo_{key}_ans.pdf")], ans


if __name__ == "__main__":
    docs = []
    for k in sys.argv[1:] or list(PATTERNS):
        d, a = build(k)
        print(k, "こたえ:", a)
        docs += d
    write_pdfs(docs)
