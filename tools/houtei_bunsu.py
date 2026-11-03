"""分数のある方程式（A4・問題2ページ＋こたえ1ページ）と、宿題6日分（N 用）

  python3 tools/houtei_bunsu.py          # A・B・宿題 ぜんぶ
  python3 tools/houtei_bunsu.py A        # パターンAだけ
  python3 tools/houtei_bunsu.py hw       # 宿題だけ

- その1：分母が1つ。その2：分母が2つ以上（最小公倍数をかける・かっこ・ひく分数）。
- 各問に「両辺に □ をかけると」を書かせる（何をかけるか判断してから解く）。
- 問題は (式, かける数, [途中式...], 答え)。式の書き方は mathlib.fm（{上|下} が分数）。
  SymPy で「答えが合っているか」「1つ目の途中式＝元の式×かける数 になっているか」「どの途中式も同じ答えか」を確かめる。
- 宿題：木曜のあと金〜水の6日分・1日4問。A4 1枚に2日分×3枚。答えは自学ノートに途中式も書く。こたえは本人に渡して毎日丸つけ。
- 出力：pdf/houtei_bunsu_{A,B}.pdf・_ans.pdf、pdf/houtei_bunsu_hw1.pdf・houtei_bunsu_hw1_ans.pdf
"""
import re
import sys

import sympy as sp
from sympy.parsing.sympy_parser import (implicit_multiplication_application, parse_expr,
                                        standard_transformations)

from mathlib import CIRC, CSS, answer_doc, fm, head, problem_doc, write_pdfs

X = sp.Symbol("x")
TR = standard_transformations + (implicit_multiplication_application,)

PATTERNS = {
    "A": [
        ("{x|3}+2=5", 3, ["x+6=15"], 9),
        ("{x|2}-4=1", 2, ["x-8=2"], 10),
        ("{3x|4}=6", 4, ["3x=24"], 8),
        ("{x|5}=x-12", 5, ["x=5x-60", "-4x=-60"], 15),
        ("{x+2|3}=4", 3, ["x+2=12"], 10),
        ("{x|4}-1=2", 4, ["x-4=8"], 12),
        ("{x-1|2}=3", 2, ["x-1=6"], 7),
        ("{x|3}+1=x-5", 3, ["x+3=3x-15", "-2x=-18"], 9),
        ("{x|2}+{x|3}=5", 6, ["3x+2x=30", "5x=30"], 6),
        ("{x|3}-{x|4}=1", 12, ["4x-3x=12"], 12),
        ("{x|2}-1={x|3}", 6, ["3x-6=2x"], 6),
        ("{x+1|3}={x-1|2}", 6, ["2(x+1)=3(x-1)", "2x+2=3x-3", "-x=-5"], 5),
        ("{x|4}+{1|2}=2", 4, ["x+2=8"], 6),
        ("{x-2|3}={x|5}", 15, ["5(x-2)=3x", "5x-10=3x", "2x=10"], 5),
        ("{2x-1|3}={x+3|2}", 6, ["2(2x-1)=3(x+3)", "4x-2=3x+9"], 11),
        ("{x|6}-{x-4|4}=0", 12, ["2x-3(x-4)=0", "2x-3x+12=0", "-x=-12"], 12),
    ],
    "B": [
        ("{x|4}+3=5", 4, ["x+12=20"], 8),
        ("{x|3}-2=1", 3, ["x-6=3"], 9),
        ("{2x|5}=4", 5, ["2x=20"], 10),
        ("{x|3}=x-6", 3, ["x=3x-18", "-2x=-18"], 9),
        ("{x+3|2}=5", 2, ["x+3=10"], 7),
        ("{x|5}+2=4", 5, ["x+10=20"], 10),
        ("{x-4|3}=3", 3, ["x-4=9"], 13),
        ("{x|2}+3=x-1", 2, ["x+6=2x-2", "-x=-8"], 8),
        ("{x|3}+{x|6}=3", 6, ["2x+x=18", "3x=18"], 6),
        ("{x|2}-{x|5}=3", 10, ["5x-2x=30", "3x=30"], 10),
        ("{x|4}+2={x|2}", 4, ["x+8=2x", "-x=-8"], 8),
        ("{x+2|4}={x-1|3}", 12, ["3(x+2)=4(x-1)", "3x+6=4x-4", "-x=-10"], 10),
        ("{x|6}+{1|3}=1", 6, ["x+2=6"], 4),
        ("{x+1|2}={x|3}", 6, ["3(x+1)=2x", "3x+3=2x"], -3),
        ("{3x-1|4}={x+3|2}", 4, ["3x-1=2(x+3)", "3x-1=2x+6"], 7),
        ("{x|4}-{x-6|6}=2", 12, ["3x-2(x-6)=24", "3x-2x+12=24"], 12),
    ],
}

# 宿題：(曜日, ポイント, 4問)
HW = [
    ("金", "分母が1つ。<b>すべての項に</b>分母の数をかける。", [
        ("{x|2}+1=4", 2, ["x+2=8"], 6), ("{x|3}-1=2", 3, ["x-3=6"], 9),
        ("{3x|2}=9", 2, ["3x=18"], 6), ("{x+1|4}=2", 4, ["x+1=8"], 7)]),
    ("土", "分母が1つ。右辺に x があったら、移項して左辺に集める。", [
        ("{x|4}-2=1", 4, ["x-8=4"], 12), ("{x-3|2}=4", 2, ["x-3=8"], 11),
        ("{x|2}=x-3", 2, ["x=2x-6", "-x=-6"], 6), ("{2x|3}+1=5", 3, ["2x+3=15", "2x=12"], 6)]),
    ("日", "分母が2つ。<b>両方の分母でわれる数（最小公倍数）</b>をかける。", [
        ("{x|2}+{x|4}=3", 4, ["2x+x=12", "3x=12"], 4), ("{x|3}+{x|2}=10", 6, ["2x+3x=60", "5x=60"], 12),
        ("{x|2}-{x|3}=2", 6, ["3x-2x=12"], 12), ("{x|3}+2={x|2}", 6, ["2x+12=3x", "-x=-12"], 12)]),
    ("月", "分子が x＋1 のような式のときは、<b>かっこをつけて</b>かける。", [
        ("{x+1|2}={x+4|3}", 6, ["3(x+1)=2(x+4)", "3x+3=2x+8"], 5), ("{x-1|3}={x|4}", 12, ["4(x-1)=3x", "4x-4=3x"], 4),
        ("{x|6}+{1|2}=2", 6, ["x+3=12"], 9), ("{x+2|3}={x+6|5}", 15, ["5(x+2)=3(x+6)", "5x+10=3x+18", "2x=8"], 4)]),
    ("火", "<b>ひく分数</b>に注意。−2(x−1) は −2x<b>＋</b>2 になる。", [
        ("{x|2}-{x-1|3}=1", 6, ["3x-2(x-1)=6", "3x-2x+2=6"], 4), ("{2x+1|3}={x+5|2}", 6, ["2(2x+1)=3(x+5)", "4x+2=3x+15"], 13),
        ("{x|3}-{x-2|4}=1", 12, ["4x-3(x-2)=12", "4x-3x+6=12"], 6), ("{x-3|2}-{x-5|4}=2", 4, ["2(x-3)-(x-5)=8", "2x-6-x+5=8"], 9)]),
    ("水", "まとめ。かける数を決めてから解こう。", [
        ("{x|3}+4=6", 3, ["x+12=18"], 6), ("{x|2}+{x|5}=7", 10, ["5x+2x=70", "7x=70"], 10),
        ("{x+5|4}={x+1|2}", 4, ["x+5=2(x+1)", "x+5=2x+2", "-x=-3"], 3), ("{x|4}-{x-2|6}=1", 12, ["3x-2(x-2)=12", "3x-2x+4=12"], 8)]),
]


def to_sym(s):
    s = re.sub(r"\{", "((", s)
    s = s.replace("|", ")/(").replace("}", "))")
    L, R = s.split("=")
    return parse_expr(L, transformations=TR), parse_expr(R, transformations=TR)


def check(tag, probs):
    for eq, m, steps, a in probs:
        L, R = to_sym(eq)
        sol = sp.solve(sp.Eq(L, R), X)
        assert sol == [a], (tag, eq, sol, a)
        L0, R0 = to_sym(steps[0])
        assert sp.expand(L0 - R0 - m * (L - R)) == 0, (tag, eq, "1つ目の途中式が「元の式×かける数」になっていません", steps[0])
        for s in steps:
            Ls, Rs = to_sym(s)
            assert sp.solve(sp.Eq(Ls, Rs), X) == [a], (tag, eq, s)
        # 分母を全部はらえているか（途中式に分数が残っていないか）
        for s in steps:
            assert "{" not in s, (tag, s)


def ans_row(i, eq, m, steps, a, label=None):
    mid = "".join(f"<span class=st>→ {fm(s)}</span>　" for s in steps)
    no = label if label is not None else CIRC[i]
    return (f"<div class=a><div class=row>{no}　{fm(eq)}</div>"
            f"<div class=row><span class=hint>両辺に×{m}</span>{mid}<span class=res>→ {fm('x=' + str(a))}</span></div></div>")


SCAF = "<div class=scaf>両辺に<span class=box></span>をかけると</div>"
EXTRA = ".q .expr{min-height:12mm}"


def build(key):
    probs = PATTERNS[key]
    check(key, probs)
    title = f"分数のある方程式 {key}"
    prob = problem_doc(title, [
        {"label": "その1", "sub": "分母が1つ", "scaffold": SCAF, "probs": [p[0] for p in probs[:8]],
         "tip": "ポイント：両辺に<b>分母の数</b>をかけて分数をなくそう。<b>分数でない項にもかける</b>のを忘れずに。　例）"
                f"<span class=ex>{fm('{x|3}+2=5')} → ×3 → {fm('x+6=15')} → {fm('x=9')}</span>"},
        {"label": "その2", "sub": "分母が2つ以上", "scaffold": SCAF, "probs": [p[0] for p in probs[8:]],
         "tip": "ポイント：<b>どの分母でもわれる数（最小公倍数）</b>をかけよう。分子が式のときは<b>かっこ</b>をつける。"
                f"　例）<span class=ex>{fm('{x+1|3}={x-1|2}')} → ×6 → {fm('2(x+1)=3(x-1)')}</span>"},
    ], ans_label="<i>x</i> ＝")
    rows = [ans_row(i, *p) for i, p in enumerate(probs)]
    ansh = answer_doc(title, [{"label": "その1　分母が1つ", "rows": rows[:8]}, {"label": "その2　分母が2つ以上", "rows": rows[8:]}])
    return [(prob, f"houtei_bunsu_{key}.pdf"), (ansh, f"houtei_bunsu_{key}_ans.pdf")]


HW_CSS = """
.day { flex: 1; display: flex; flex-direction: column; margin-top: 4mm; }
.day + .day { border-top: 1pt dashed #999; padding-top: 4mm; }
.band { display: flex; align-items: center; gap: 4mm; background: #fbefdc; color: #7a4508; border-radius: 2mm;
        padding: 2mm 4mm; font-weight: 700; font-size: 12.5pt; }
.band .sp { margin-left: auto; white-space: nowrap; font-weight: 400; font-size: 10.5pt; color: #111; display: flex; gap: 5mm; }
.band .sp span { display: inline-block; border-bottom: .8pt solid #111; width: 14mm; }
.band .ck::before { content: ""; display: inline-block; width: 4.5mm; height: 4.5mm; border: .8pt solid #111; margin-right: 1.5mm; vertical-align: -1mm; }
.point { font-size: 10.5pt; margin: 2.5mm 1mm 0; }
.hq { flex: 1; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 0 8mm; margin-top: 2mm; }
.hq .expr { font-size: 16pt; padding-top: 3mm; }
.rule { margin-top: 3mm; font-size: 10pt; border: .8pt solid #111; border-radius: 2mm; padding: 2mm 4mm; line-height: 1.6; }
"""


def build_hw():
    pages = []
    for d in range(0, 6, 2):
        days = ""
        for k in (d, d + 1):
            youbi, point, probs = HW[k]
            check(f"宿題{k + 1}日目", probs)
            cells = "".join(f"<div class=expr><span class=no>{CIRC[j]}</span>{fm(p[0])}</div>" for j, p in enumerate(probs))
            days += (f"<div class=day><div class=band>{k + 1}日目（{youbi}）<span class=sp>"
                     f"<span class=ck>丸つけした</span></span></div>"
                     f"<p class=point>ポイント：{point}</p><div class=hq>{cells}</div></div>")
        rule = ("<div class=rule>やり方：自学ノートに日付と問題番号を書き、<b>「両辺に○をかける」→ 途中式 → 答え</b>の順に書く。"
                "終わったら<b>こたえを見て自分で丸つけ</b>。まちがえたら、正しい途中式をもう一度ノートに書く。</div>") if d == 0 else ""
        pages.append(f"<div class=page>{head('分数のある方程式　宿題', f'{d + 1}日目・{d + 2}日目（1日4問）', name=True)}{rule}{days}</div>")
    prob = f"<html><head><meta charset=utf-8><style>{CSS}{HW_CSS}</style></head><body>{''.join(pages)}</body></html>"
    secs = []
    for k, (youbi, _, probs) in enumerate(HW):
        secs.append({"label": f"{k + 1}日目（{youbi}）", "rows": [ans_row(j, *p) for j, p in enumerate(probs)]})
    ansh = answer_doc("分数のある方程式　宿題", secs, order="row", pages=[3])
    ansh = ansh.replace("</style>", ".agrid{margin-top:2mm}.sec{margin:2mm 0 .5mm}.a{padding:1.2mm 0;font-size:11pt}</style>", 1)
    return [(prob, "houtei_bunsu_hw1.pdf"), (ansh, "houtei_bunsu_hw1_ans.pdf")]


if __name__ == "__main__":
    keys = sys.argv[1:] or [*PATTERNS, "hw"]
    docs = []
    for k in keys:
        docs += build_hw() if k == "hw" else build(k)
    print("SymPy の確認 OK")
    write_pdfs(docs, extra_css=EXTRA)
