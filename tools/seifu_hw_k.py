"""K の宿題 1週間分（木曜に渡して 金〜水 の6日分）（A4・1日1ページ＝6ページ＋こたえ2ページ）

  python3 seifu_hw_k.py        # tools/ で実行

ねらい：授業の「計算の順序」と、まだ定着していない「符号」を、分けて毎日少しずつ。
- 1日1ページ。左の列＝計算の順序（正の数だけ・×÷が先）4問、右の列＝正負の数（符号）4問。
- プリントに直接書く（途中式の欄つき）。こたえを本人に渡し、毎日自分で丸つけ。
- 符号は：たし算・ひき算 → ひく負の数 → かけ算・わり算の符号 → 3つ以上の数（同じ符号を集める）→ 符号のついた ×＋ → まとめ。
- (式, [途中式]) は Python で計算できる書き方（* と /）。答え・途中式を確かめる。左の列は途中もマイナスにならないか確かめる。
- 出力：pdf/seifu_hw1.pdf・pdf/seifu_hw1_ans.pdf（次の週は HW_NO と DAYS を書きかえて seifu_hw2）
"""
from mathlib import ANS_RED, CIRC, CSS, fm, head, tex, write_pdfs

HW_NO = 1
# (曜日, 左のポイント, 左4問, 右の見出し, 右のポイント, 右4問)
DAYS = [
    ("金", "×のところに下線を引いて、先に計算。",
     [("6+3*5", ["6+15"]), ("4*6-9", ["24-9"]), ("30-2*8", ["30-16"]), ("7*3+5", ["21+5"])],
     "たし算・ひき算", "符号がちがうときは、大きいほうから小さいほうをひいて、大きいほうの符号。",
     [("-3+5", []), ("-4-2", []), ("6-9", []), ("-7+3", [])]),
    ("土", "×のところに下線を引いて、先に計算。",
     [("9+2*7", ["9+14"]), ("5*5-8", ["25-8"]), ("40-6*5", ["40-30"]), ("3+8*4", ["3+32"])],
     "ひく負の数", f"{fm('-(-3)')} は {fm('+3')}、{fm('+(-3)')} は {fm('-3')} になおしてから計算。",
     [("5-(-3)", ["5+3"]), ("-2-(-6)", ["-2+6"]), ("-8-(-1)", ["-8+1"]), ("4+(-9)", ["4-9"])]),
    ("日", "÷も×と同じで先に計算。",
     [("24/4+3", ["6+3"]), ("20-15/5", ["20-3"]), ("8+30/6", ["8+5"]), ("45/9-2", ["5-2"])],
     "かけ算・わり算の符号", f"同じ符号どうし → {fm('+')}、ちがう符号どうし → {fm('-')}。",
     [("(-4)*3", []), ("(-5)*(-2)", []), ("(-18)/3", []), ("(-24)/(-4)", [])]),
    ("月", "×・÷が2つあったら、両方とも先に。",
     [("6*3-12/4", ["18-3"]), ("16/2+5*3", ["8+15"]), ("50-7*6", ["50-42"]), ("9+36/9", ["9+4"])],
     "3つ以上の数", "並べかえて、<b>＋の数どうし・−の数どうし</b>を集めてから計算。",
     [("-3+7-5", ["7-3-5", "7-8"]), ("4-6+9-2", ["4+9-6-2", "13-8"]), ("-5-4+6", ["6-5-4", "6-9"]), ("8-3-7+1", ["8+1-3-7", "9-10"])]),
    ("火", "( ) があれば、そこがいちばん先。",
     [("(2+5)*3", ["7*3"]), ("6*(10-4)", ["6*6"]), ("2*4+3*5", ["8+15"]), ("40-3*5-6", ["40-15-6", "25-6"])],
     "×が先・符号つき", "かけ算を先に計算してから、たし算・ひき算（符号に注意）。",
     [("-2+3*4", ["-2+12"]), ("(-3)*2+5", ["-6+5"]), ("10-4*3", ["10-12"]), ("(-2)*(-4)-3", ["8-3"])]),
    ("水", "まとめ。何から計算するか、下線を引いてから。",
     [("7+6*8", ["7+48"]), ("56/8-3", ["7-3"]), ("(9-4)*6", ["5*6"]), ("4*7-18/3", ["28-6"])],
     "まとめ", "1週間のまとめ。まちがえたら、その曜日のポイントを見なおそう。",
     [("7-(-2)", ["7+2"]), ("(-6)*(-3)", []), ("-4+9-8", ["9-4-8", "9-12"]), ("3+(-5)*2", ["3-10"])]),
]

EXTRA = """
.band { display: flex; align-items: center; gap: 4mm; background: #fbefdc; color: #7a4508; border-radius: 2mm;
        padding: 2mm 4mm; font-weight: 700; font-size: 12.5pt; margin-top: 3mm; }
.band .sp { margin-left: auto; white-space: nowrap; font-weight: 400; font-size: 10.5pt; color: #111; }
.band .ck::before { content: ""; display: inline-block; width: 4.5mm; height: 4.5mm; border: .8pt solid #111; margin-right: 1.5mm; vertical-align: -1mm; }
.rule { margin-top: 2.5mm; font-size: 10pt; border: .8pt solid #111; border-radius: 2mm; padding: 1.8mm 4mm; line-height: 1.55; }
.ch { font-size: 10pt; line-height: 1.5; padding: 1.5mm 0 1mm; border-bottom: .8pt solid #111; min-height: 15mm; }
.ch .t { font-size: 11pt; font-weight: 700; display: block; }
.grid { margin-top: 2mm; }
.col { grid-template-rows: auto repeat(4, 1fr); }
.scaf .ln::after { width: 50mm; }
"""
SCAF = f"<div class=scaf><span class=ln>{tex('=')}</span><span class=ln>{tex('=')}</span></div>"
RULE = ("<div class=rule>やり方：1日1ページ。<b>途中式も書いて</b>答えを出す。終わったら<b>こたえを見て自分で丸つけ</b>して、"
        "まちがえたら正しい答えを横に書く。わからないときは、ポイントを読んでからもう一度。</div>")


def check():
    for youbi, _, left, _, _, right in DAYS:
        assert len(left) == 4 and len(right) == 4, youbi
        for q, steps in left + right:
            v = eval(q)
            assert v == int(v), (youbi, q, v)
            for s in steps:
                assert eval(s) == v, (youbi, q, s)
        for q, steps in left:
            assert eval(q) >= 0 and all(eval(s) >= 0 for s in steps), (youbi, "左の列は正の数だけ", q)


def cell(no, q, steps=None):
    """steps を渡すと「こたえ」：途中式と答えを赤で書きこむ"""
    if steps is None:
        return (f"<div class=q><div class=expr><span class=no>{CIRC[no]}</span>{fm(q)}</div>{SCAF}"
                f"<div class=ansbox>答え <span class=blank></span></div></div>")
    work = "<br>".join(fm("=" + s_) for s_ in steps)
    return (f"<div class=q><div class=expr><span class=no>{CIRC[no]}</span>{fm(q)}</div>"
            f"{('<div class=ra>' + work + '</div>') if work else ''}"
            f"<div class=ansbox>答え <span class=fill>{fm(str(int(eval(q))))}</span></div></div>")


def pages_html(answer):
    pages = []
    for d, (youbi, lp, left, rt, rp, right) in enumerate(DAYS):
        L = "".join(cell(j, q, steps if answer else None) for j, (q, steps) in enumerate(left))
        R = "".join(cell(4 + j, q, steps if answer else None) for j, (q, steps) in enumerate(right))
        title = f'正負の数　宿題 {HW_NO}'
        hd = (head(title + "<span class=ans-tag>こたえ</span>", f'{d + 1}日目（{youbi}）', name=False) if answer
              else head(title, f'{d + 1}日目（{youbi}）・1日8問', score=8, date=True))
        pages.append(f"""<div class=page>{hd}
{RULE if d == 0 else ''}
<div class=band>{d + 1}日目（{youbi}）<span class=sp><span class=ck>丸つけした</span></span></div>
<div class=grid>
 <div class=col><div class=ch><span class=t>計算の順序（×÷が先）</span>ポイント：{lp}</div>{L}</div>
 <div class=col><div class=ch><span class=t>正負の数　{rt}</span>ポイント：{rp}</div>{R}</div>
</div></div>""")
    css = CSS + EXTRA + (ANS_RED if answer else "")
    return f"<html><head><meta charset=utf-8><style>{css}</style></head><body>{''.join(pages)}</body></html>"


def build():
    """問題と、こたえ（問題と同じ形に赤で書きこむ・11/6〜）"""
    check()
    return [(pages_html(False), f"seifu_hw{HW_NO}.pdf"), (pages_html(True), f"seifu_hw{HW_NO}_ans.pdf")]


if __name__ == "__main__":
    write_pdfs(build())
