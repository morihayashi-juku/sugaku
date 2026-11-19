"""K の宿題2（11/19 木に渡して 金11/20〜水11/25 の6日分）かけ算・わり算の混じった計算（A4・1日1ページ＝6ページ＋こたえ6ページ）

  python3 seifu_jojo_hw.py        # tools/ で実行

- 宿題1（seifu_hw_k.py）と同じ形：1日1ページ8問、プリントに直接書く（途中式の欄つき）、こたえを渡して毎日自分で丸つけ。
- 左の列＝符号の練習（2つの数のかけ算・わり算）4問、右の列＝かけ算・わり算の混じった計算 4問（授業の seifu_jojo と同じやり方）。
  右は 金・土＝×だけ → 日・月＝÷1つ＋×1つ → 火＝3つの計算 → 水＝まとめ（÷2つも）。
- 授業の A・B と同じ問題は出さない（seifu_jojo の種で作った問題をよけて作る）。
- 出力：pdf/seifu_hw2.pdf・pdf/seifu_hw2_ans.pdf
"""
import random

from mathlib import ANS_RED, CIRC, CSS, fm, head, write_pdfs
from seifu_hw_k import EXTRA, RULE, SCAF
from seifu_jojo import SHAPES, gen

HW_NO = 2
YOUBI = ["金", "土", "日", "月", "火", "水"]
RIGHT_SHAPES = [
    [("*", "*")] * 4,
    [("*", "*")] * 4,
    [("/", "*"), ("*", "/"), ("/", "*"), ("*", "/")],
    [("*", "/"), ("/", "*"), ("*", "/"), ("/", "*")],
    [("*", "*", "/"), ("/", "*", "*"), ("*", "/", "*"), ("/", "*", "*")],
    [("*", "*"), ("/", "*"), ("/", "/"), ("*", "/", "/")],
]
RIGHT_POINT = [
    "−の数を数えて、符号を先に書く（偶数こ → ＋、奇数こ → −）。",
    "符号を書いたら、数だけをかける。",
    "÷も×と同じ。符号を決めてから、数だけを左から順に。",
    "÷が先でも×が先でも、左から順に計算する。",
    "−の数を指でおさえて数える。それから数だけを左から順に。",
    "1週間のまとめ。まちがえたら、その曜日のポイントを見なおそう。",
]
LEFT_POINT = [
    f"同じ符号どうし → {fm('+')}、ちがう符号どうし → {fm('-')}。",
    f"わり算の符号も、かけ算と同じ。{fm('(-)/(-)')} は {fm('+')}。",
    "符号を先に書いてから、数だけを計算。",
    "符号を先に書いてから、数だけを計算。",
    "符号を先に書いてから、数だけを計算。",
    "まとめ。",
]


def two(rng, op, seen):
    while True:
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        if op == "/":
            a = a * b
        a = a if rng.random() < .5 else -a
        b = b if rng.random() < .5 else -b
        if a > 0 and b > 0:
            continue
        q = (f"({a})" if a < 0 else str(a)) + op + f"({b})" if b < 0 else (f"({a})" if a < 0 else str(a)) + op + str(b)
        if q not in seen:
            seen.add(q)
            return q, []


def make_days():
    seen = set()
    for seed in (1119, 1123):                     # 授業の A・B と同じ問題をよける
        r = random.Random(seed)
        for sh in SHAPES:
            gen(r, sh, seen)
    rng = random.Random(1120)
    left_ops = [["*"] * 4, ["/"] * 4, ["*", "/", "*", "/"], ["/", "*", "/", "*"], ["*", "/", "/", "*"], ["/", "*", "*", "/"]]
    days = []
    for d in range(6):
        left = [two(rng, op, seen) for op in left_ops[d]]
        right = gen(rng, RIGHT_SHAPES[d], seen)
        days.append((YOUBI[d], LEFT_POINT[d], left, RIGHT_POINT[d], right))
    return days


def cell(no, q, steps=None):
    if steps is None:
        return (f"<div class=q><div class=expr><span class=no>{CIRC[no]}</span>{fm(q)}</div>{SCAF}"
                f"<div class=ansbox>答え <span class=blank></span></div></div>")
    work = "<br>".join(fm("=" + s_) for s_ in steps)
    return (f"<div class=q><div class=expr><span class=no>{CIRC[no]}</span>{fm(q)}</div>"
            f"{('<div class=ra>' + work + '</div>') if work else ''}"
            f"<div class=ansbox>答え <span class=fill>{fm(str(int(eval(q))))}</span></div></div>")


def pages_html(days, answer):
    pages = []
    for d, (youbi, lp, left, rp, right) in enumerate(days):
        L = "".join(cell(j, q, st if answer else None) for j, (q, st) in enumerate(left))
        R = "".join(cell(4 + j, q, st if answer else None) for j, (q, st) in enumerate(right))
        title = f"正負の数　宿題 {HW_NO}"
        hd = (head(title + "<span class=ans-tag>こたえ</span>", f"{d + 1}日目（{youbi}）", name=False) if answer
              else head(title, f"{d + 1}日目（{youbi}）・1日8問", score=8, date=True))
        pages.append(f"""<div class=page>{hd}
{RULE if d == 0 else ''}
<div class=band>{d + 1}日目（{youbi}）<span class=sp><span class=ck>丸つけした</span></span></div>
<div class=grid>
 <div class=col><div class=ch><span class=t>符号の練習（2つの数）</span>ポイント：{lp}</div>{L}</div>
 <div class=col><div class=ch><span class=t>かけ算・わり算の混じった計算</span>ポイント：{rp}</div>{R}</div>
</div></div>""")
    css = CSS + EXTRA + (ANS_RED if answer else "")
    return f"<html><head><meta charset=utf-8><style>{css}</style></head><body>{''.join(pages)}</body></html>"


if __name__ == "__main__":
    days = make_days()
    for youbi, _, left, _, right in days:
        for q, st in left + right:
            v = eval(q)
            assert v == int(v), (youbi, q)
            assert all(eval(s) == v for s in st), (youbi, q)
        print(youbi, [q for q, _ in left + right])
    write_pdfs([(pages_html(days, False), f"seifu_hw{HW_NO}.pdf"), (pages_html(days, True), f"seifu_hw{HW_NO}_ans.pdf")])
