"""K 用　計算の順序　かけ算・わり算の混じった計算（正の数だけ）（11/26〜。先生の希望「負なし・計算の順番の練習」）

  python3 junjo_jojo.py        # tools/ で実行

- 授業・自習：A4・4ページ32問＋こたえ4ページ（木 11/26＝A、月 11/30 の自習＝B）
  その1 ×÷が2つ（左から順に）／その2 ×÷が3つ／その3 ＋−もまざる（×÷が先、×÷どうしは左から）／その4 ( ) つき
- 宿題（11/27 金〜12/2 水の6日分）：1日1ページ8問・プリントに直接書く（宿題1・2と同じ形）。左＝×÷だけ、右＝＋−・( ) もまざる。
- 問題は乱数（種を固定）で作る。途中の数もぜんぶ正の整数（わり算は割り切れる）になるものだけ使う。
- こたえは途中式を1つずつ（1回の計算ごとに1行）赤で書きこむ。
- 出力：pdf/junjo_jojo_{A,B}.pdf・_ans、pdf/junjo_jojo_hw1.pdf・_ans
"""
import random
import re

from mathlib import ANS_RED, CIRC, CSS, calc_docs, fm, head, tex, write_pdfs
from seifu_hw_k import EXTRA as HW_EXTRA

SCAF = "<div class=scaf>" + f"<span class=ln>{tex('=')}</span>" * 3 + "</div>"


def tok(s):
    return re.findall(r"\d+|[-+*/()]", s)


def one(ts):
    """いちばん先に計算するところを1つだけ計算する。できなければ None"""
    # いちばん内側の ( )
    if "(" in ts:
        r = ts.index(")")
        l = max(i for i in range(r) if ts[i] == "(")
        inner = ts[l + 1:r]
        if len(inner) == 1:
            return ts[:l] + inner + ts[r + 1:]
        new = one(inner)
        if new is None:
            return None
        if len(new) == 1:
            return ts[:l] + new + ts[r + 1:]
        return ts[:l + 1] + new + ts[r:]
    for ops in (("*", "/"), ("+", "-")):
        for i, x in enumerate(ts):
            if x in ops:
                a, b = int(ts[i - 1]), int(ts[i + 1])
                if x == "*":
                    v = a * b
                elif x == "/":
                    if b == 0 or a % b:
                        return None
                    v = a // b
                elif x == "+":
                    v = a + b
                else:
                    v = a - b
                if v <= 1 or v > 200:
                    return None
                return ts[:i - 1] + [str(v)] + ts[i + 2:]
    return None


def steps(expr):
    """[途中式…]、答え。途中で負・0・割り切れないものがあれば None"""
    ts, out = tok(expr), []
    while len(ts) > 1:
        ts = one(ts)
        if ts is None:
            return None
        out.append("".join(ts))
    return out[:-1], int(ts[0])


def fill(tmpl, rng):
    s = tmpl
    for ch in "abcd":
        if ch in s:
            if ch == "a" and ("a/" in s or "a*b/" in s):
                v = rng.choice([12, 14, 15, 16, 18, 20, 21, 24, 27, 28, 30, 32, 35, 36, 40, 42, 45, 48, 54, 56, 60, 63, 64, 72])
            else:
                v = rng.randint(2, 9)
            s = s.replace(ch, str(v), 1)
    return s


def gen(rng, tmpls, seen):
    out = []
    for tm in tmpls:
        for _ in range(20000):
            q = fill(tm, rng)
            r = steps(q)
            if r and r[1] <= 100 and q not in seen:
                seen.add(q)
                out.append((q, r[0]))
                break
        else:
            raise RuntimeError(tm)
    return out


T1 = ["a/b*c"] * 4 + ["a*b/c"] * 2 + ["a/b/c"] * 2
T2 = ["a/b*c*d", "a*b/c*d", "a/b*c/d", "a*b/c/d", "a/b/c*d", "a*b*c/d", "a/b*c*d", "a*b/c/d"]
T3 = ["a+b/c*d", "a-b*c/d", "a/b*c+d", "a*b/c-d", "a+b*c/d", "a/b*c-d", "a-b/c*d", "a*b/c+d"]
T4 = ["(a+b)/c*d", "a/(b*c)", "(a-b)*c/d", "a*(b+c)/d", "a/(b-c)*d", "(a+b)*c/d", "a/b*(c+d)", "(a-b)/c*d"]

SECS = [
    ("その1", "×と÷が2つ（左から順に）", f"ポイント：×と÷だけの式は、<b>左から順に</b>計算する（×が先ではない）。　例）{tex(r'12\div 3\times 2=4\times 2=8')}"),
    ("その2", "×と÷が3つ", "ポイント：×÷が3つでも、<b>左から順に1つずつ</b>。計算するところに下線を引いてから、1回ずつ式を書く。"),
    ("その3", "＋・−もまざる", f"ポイント：＋−がまざったら、<b>×÷が先</b>。×÷どうしは左から順に。　例）{tex(r'20-12\div 4\times 2=20-3\times 2=20-6=14')}"),
    ("その4", "( ) のある計算", "ポイント：( ) があれば、<b>( ) の中がいちばん先</b>。そのあと×÷を左から、最後に＋−。"),
]

# ------------------------------------------------------------ 宿題（1日1ページ8問・直接書く）
HW_DAYS = [
    ("金", ["a/b*c"] * 4, ["a+b/c*d", "a-b*c/d", "a+b*c/d", "a/b*c+d"]),
    ("土", ["a*b/c", "a/b*c", "a/b/c", "a/b*c"], ["a*b/c-d", "a+b/c*d", "a-b/c*d", "a*b/c+d"]),
    ("日", ["a/b*c*d", "a*b/c*d", "a/b/c*d", "a/b*c/d"], ["a/b*c-d", "a+b*c/d", "a-b*c/d", "a/b*c+d"]),
    ("月", ["a*b/c/d", "a/b*c*d", "a*b*c/d", "a/b*c/d"], ["(a+b)/c*d", "(a-b)*c/d", "a/(b*c)", "a*(b+c)/d"]),
    ("火", ["a/b*c", "a/b/c", "a*b/c*d", "a/b*c*d"], ["(a+b)*c/d", "a/b*(c+d)", "(a-b)/c*d", "a/(b-c)*d"]),
    ("水", ["a/b*c", "a/b/c*d", "a*b/c", "a/b*c/d"], ["a-b/c*d", "(a+b)/c*d", "a*b/c+d", "a/(b*c)"]),
]
HW_POINT = [
    ("×と÷だけは、左から順に。", "＋−があったら、×÷が先。"),
    ("÷が先に書いてあったら、÷から。", "×÷が2つ続いたら、その中は左から。"),
    ("3つでも左から1つずつ。", "×÷が先、＋−はあと。"),
    ("下線を引いてから計算。", "( ) の中がいちばん先。"),
    ("左から順に。", "( ) → ×÷（左から）→ ＋−。"),
    ("まとめ。", "まとめ。まちがえたら、その曜日のポイントを見なおそう。"),
]
RULE = ("<div class=rule>やり方：1日1ページ。<b>計算するところに下線を引いて、1回ずつ式を書いて</b>答えを出す。"
        "終わったら<b>こたえを見て自分で丸つけ</b>して、まちがえたら正しい答えを横に書く。</div>")
HW_CSS = HW_EXTRA + ".scaf .ln::after { width: 50mm; }"


def cell(no, q, st=None):
    if st is None:
        return (f"<div class=q><div class=expr><span class=no>{CIRC[no]}</span>{fm(q)}</div>{SCAF}"
                f"<div class=ansbox>答え <span class=blank></span></div></div>")
    work = "<br>".join(fm("=" + s_) for s_ in st)
    return (f"<div class=q><div class=expr><span class=no>{CIRC[no]}</span>{fm(q)}</div>"
            f"{('<div class=ra>' + work + '</div>') if work else ''}"
            f"<div class=ansbox>答え <span class=fill>{fm(str(steps(q)[1]))}</span></div></div>")


def hw_html(days, answer):
    pages = []
    for d, (youbi, left, right) in enumerate(days):
        lp, rp = HW_POINT[d]
        L = "".join(cell(j, q, st if answer else None) for j, (q, st) in enumerate(left))
        R = "".join(cell(4 + j, q, st if answer else None) for j, (q, st) in enumerate(right))
        title = "計算の順序　×÷の宿題"
        hd = (head(title + "<span class=ans-tag>こたえ</span>", f"{d + 1}日目（{youbi}）", name=False) if answer
              else head(title, f"{d + 1}日目（{youbi}）・1日8問", score=8, date=True))
        pages.append(f"""<div class=page>{hd}
{RULE if d == 0 else ''}
<div class=band>{d + 1}日目（{youbi}）<span class=sp><span class=ck>丸つけした</span></span></div>
<div class=grid>
 <div class=col><div class=ch><span class=t>×と÷だけ（左から順に）</span>ポイント：{lp}</div>{L}</div>
 <div class=col><div class=ch><span class=t>＋−・( ) もまざる</span>ポイント：{rp}</div>{R}</div>
</div></div>""")
    css = CSS + HW_CSS + (ANS_RED if answer else "")
    return f"<html><head><meta charset=utf-8><style>{css}</style></head><body>{''.join(pages)}</body></html>"


if __name__ == "__main__":
    seen, docs = set(), []
    for key, seed in (("A", 1126), ("B", 1130)):
        rng = random.Random(seed)
        probs = [gen(rng, T, seen) for T in (T1, T2, T3, T4)]
        for sec in probs:
            for q, st in sec:
                assert eval(q) == steps(q)[1], q
        d, a = calc_docs(f"計算の順序　かけ算・わり算 {key}", SECS, probs, f"junjo_jojo_{key}", scaffold=SCAF, nonneg=True)
        print(key, a)
        docs += d
    rng = random.Random(1127)
    days = [(y, gen(rng, l, seen), gen(rng, r, seen)) for y, l, r in HW_DAYS]
    for y, l, r in days:
        print(y, [q for q, _ in l + r])
    docs += [(hw_html(days, False), "junjo_jojo_hw1.pdf"), (hw_html(days, True), "junjo_jojo_hw1_ans.pdf")]
    write_pdfs(docs)
