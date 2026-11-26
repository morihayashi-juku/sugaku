"""K 用　かけ算・わり算の混じった計算 パターン C・D と宿題3（11/26〜。先生の希望「かけ算・わり算をもう1回」）

  python3 seifu_jojo2.py        # tools/ で実行

- 形は seifu_jojo.py（A・B）・seifu_jojo_hw.py（宿題2）と同じ。木 11/26＝C、月曜の自習＝D。
- 宿題3：11/27 金〜12/2 水の6日分（1日1ページ8問・プリントに直接書く）。
- A・B・宿題2 と同じ問題は出さない（それぞれの種で作った問題をよけて作る）。
- 出力：pdf/seifu_jojo_{C,D}.pdf・_ans、pdf/seifu_hw3.pdf・_ans
"""
import random

import seifu_jojo_hw as hw
from mathlib import calc_docs, write_pdfs
from seifu_jojo import SCAF, SECS, SHAPES, gen


def used():
    """A・B・宿題2 で使った問題"""
    seen = set()
    for seed in (1119, 1123):
        r = random.Random(seed)
        for sh in SHAPES:
            gen(r, sh, seen)
    for _, _, left, _, right in hw.make_days():
        seen |= {q for q, _ in left + right}
    return seen


def hw_days(seed, seen):
    rng = random.Random(seed)
    left_ops = [["*"] * 4, ["/"] * 4, ["*", "/", "*", "/"], ["/", "*", "/", "*"], ["*", "/", "/", "*"], ["/", "*", "*", "/"]]
    return [(hw.YOUBI[d], hw.LEFT_POINT[d], [hw.two(rng, op, seen) for op in left_ops[d]], hw.RIGHT_POINT[d], gen(rng, hw.RIGHT_SHAPES[d], seen))
            for d in range(6)]


if __name__ == "__main__":
    seen = used()
    docs = []
    for key, seed in (("C", 1126), ("D", 1130)):
        rng = random.Random(seed)
        probs = [gen(rng, sh, seen) for sh in SHAPES]
        d, a = calc_docs(f"正負の数　かけ算・わり算 {key}", SECS, probs, f"seifu_jojo_{key}", scaffold=SCAF)
        print(key, a)
        docs += d
    days = hw_days(1127, seen)
    for youbi, _, left, _, right in days:
        for q, st in left + right:
            v = eval(q)
            assert v == int(v) and all(eval(s) == v for s in st), (youbi, q)
        print(youbi, [q for q, _ in left + right])
    hw.HW_NO = 3
    docs += [(hw.pages_html(days, False), "seifu_hw3.pdf"), (hw.pages_html(days, True), "seifu_hw3_ans.pdf")]
    write_pdfs(docs)
