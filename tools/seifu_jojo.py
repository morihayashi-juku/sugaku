"""正負の数　かけ算・わり算の混じった計算（K 用・A4・問題4ページ32問＋こたえ4ページ）（11/19〜）

  python3 seifu_jojo.py        # A・B とも（tools/ で実行）

- やり方：① 答えの<b>符号を先に決める</b>（− の数が偶数こ → ＋、奇数こ → −）② <b>数だけ</b>を左から順に計算する。
- その1：かけ算だけ（3つの数）／その2：わり算1つ＋かけ算1つ／その3：かけ算・わり算が3つ／その4：わり算2つもまざる（まとめ）
- 問題は乱数（パターンごとに種を固定）で作り、答え・途中（数だけの計算）が整数になるものだけを使う。
- こたえは、途中式の欄に「＝符号（数だけの式）」を赤で書きこむ。
- 出力：pdf/seifu_jojo_{A,B}.pdf と _ans.pdf
"""
import random

from mathlib import calc_docs, tex, write_pdfs

SCAF = f"<div class=scaf><span class=ln>{tex('=')}</span><span class=ln>{tex('=')}</span></div>"


def term(v, first):
    return f"({v})" if v < 0 else str(v)


def build(nums, ops):
    """nums：符号つきの数、ops：'*' か '/'。（式, [途中式]）を返す。左から順に整数で割り切れるものだけ"""
    acc = abs(nums[0])
    for o, n in zip(ops, nums[1:]):
        if o == "/":
            if acc % abs(n):
                return None
            acc //= abs(n)
        else:
            acc *= abs(n)
    if acc == 0 or acc > 100:
        return None
    neg = sum(1 for n in nums if n < 0)
    if neg == 0:
        return None
    sign = "-" if neg % 2 else "+"
    q = term(nums[0], True) + "".join(o + term(n, False) for o, n in zip(ops, nums[1:]))
    body = str(abs(nums[0])) + "".join(o + str(abs(n)) for o, n in zip(ops, nums[1:]))
    return q, [f"{sign}({body})"], (sign == "-" and -acc or acc)


def gen(rng, shapes, seen):
    out = []
    for ops in shapes:
        while True:
            k = len(ops) + 1
            nums = [rng.randint(2, 9) for _ in range(k)]
            # わり算の前は大きめの数（割り切れやすく）
            if ops[0] == "/":
                nums[0] = rng.choice([12, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 54, 56, 60, 63, 64, 72])
            nums = [n if rng.random() < .45 else -n for n in nums]
            r = build(nums, ops)
            if r and r[0] not in seen:
                seen.add(r[0])
                out.append((r[0], r[1]))
                break
    return out


SHAPES = [
    [("*", "*")] * 8,                                                     # その1 かけ算だけ
    [("/", "*")] * 4 + [("*", "/")] * 4,                                  # その2 ÷1つ＋×1つ
    [("*", "*", "/"), ("/", "*", "*"), ("*", "/", "*"), ("/", "*", "*"),
     ("*", "*", "/"), ("*", "/", "*"), ("/", "*", "*"), ("*", "*", "/")],  # その3 3つの計算
    [("/", "/"), ("/", "/"), ("*", "/", "/"), ("/", "/", "*"),
     ("/", "*", "/"), ("/", "/"), ("*", "/", "/"), ("/", "*", "/")],      # その4 わり算2つ
]

SECS = [
    ("その1", "かけ算だけ（3つの数）", f"ポイント：① <b>−の数を数えて符号を先に決める</b>（偶数こ → ＋、奇数こ → −）② 数だけをかける。　例）{tex(r'(-2)\times 3\times(-4)=+(2\times 3\times 4)=24')}"),
    ("その2", "わり算1つ＋かけ算1つ", f"ポイント：符号の決め方は、わり算もかけ算と同じ。数だけを<b>左から順に</b>計算する。　例）{tex(r'(-18)\div 3\times 2=-(18\div 3\times 2)=-12')}"),
    ("その3", "かけ算・わり算が3つ", "ポイント：−がいくつあるか、<b>指でおさえて数える</b>。符号を書いてから、数だけを左から順に計算する。"),
    ("その4", "わり算が2つ（まとめ）", "ポイント：わり算が2つあっても、<b>左から順に</b>。符号 → 数だけの計算 → 答え の順で、式を書いてから計算する。"),
]

if __name__ == "__main__":
    docs = []
    for key, seed in (("A", 1119), ("B", 1123)):
        rng = random.Random(seed)
        seen = set()
        probs = [gen(rng, sh, seen) for sh in SHAPES]
        d, a = calc_docs(f"正負の数　かけ算・わり算 {key}", SECS, probs, f"seifu_jojo_{key}", scaffold=SCAF)
        print(key, a)
        docs += d
    write_pdfs(docs)
