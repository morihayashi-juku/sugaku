"""正負の数　四則の混じった計算（A4・問題2ページ＋こたえ1ページ）

  python3 tools/seifu_shisoku.py        # 全パターンを pdf/ に出力
  python3 tools/seifu_shisoku.py C      # パターンCだけ

- 1ページ目「その1」＝かけ算1つ＋たし算・ひき算、2ページ目「その2」＝かけ算が2つ以上。
- 1ページに左右2列 × 4問 ＝ 8問。
- 新しいパターンは PATTERNS に (問題, 途中式) を16個足す。答えが整数で、問題と途中式の値が同じか自動で確かめる。
  式の書き方："*" は ×、"-" は −（先頭・かっこの直後は符号、それ以外はひき算）。
- 出力：pdf/seifu_shisoku_{パターン}.pdf と pdf/seifu_shisoku_{パターン}_ans.pdf
  （data/library.json にも足すこと）
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "pdf"

PATTERNS = {
    "A": {
        "example": "例）(−3)×4＋5 ＝ −12＋5 ＝ −7",
        "probs": [
            ("(-3)*4+5", "-12+5"),
            ("7+2*(-6)", "7-12"),
            ("8-(-2)*3", "8+6"),
            ("(-5)*(-3)-20", "15-20"),
            ("-9+(-4)*(-2)", "-9+8"),
            ("3*(-7)-(-10)", "-21+10"),
            ("12-5*(-2)", "12+10"),
            ("(-6)*2+(-8)", "-12-8"),
            ("(-2)*5+3*(-4)", "-10-12"),
            ("4*(-3)-(-6)*2", "-12+12"),
            ("(-7)*(-2)+(-5)*3", "14-15"),
            ("-8-(-3)*(-4)", "-8-12"),
            ("6*(-2)-5+(-3)*(-3)", "-12-5+9"),
            ("10+(-4)*(-5)-(-2)*7", "10+20+14"),
            ("(-3)*(-2)*(-5)+12", "-30+12"),
            ("-15-(-3)*4+(-1)*(-6)", "-15+12+6"),
        ],
    },
    "B": {
        "example": "例）6＋(−2)×5 ＝ 6−10 ＝ −4",
        "probs": [
            ("4*(-5)+9", "-20+9"),
            ("-6+3*(-4)", "-6-12"),
            ("10-(-4)*2", "10+8"),
            ("(-6)*(-2)-15", "12-15"),
            ("-7-(-2)*(-5)", "-7-10"),
            ("(-8)*3+30", "-24+30"),
            ("5+(-9)*(-1)", "5+9"),
            ("2*(-8)-(-7)", "-16+7"),
            ("(-4)*3+(-2)*(-5)", "-12+10"),
            ("5*(-2)-(-3)*(-2)", "-10-6"),
            ("(-6)*(-3)-4*7", "18-28"),
            ("-11+(-2)*(-3)*(-2)", "-11-12"),
            ("8-(-4)*3+(-5)*2", "8+12-10"),
            ("(-9)*2+7-(-2)*(-4)", "-18+7-8"),
            ("2*(-3)*4-(-20)", "-24+20"),
            ("-12-(-5)*(-2)+(-7)*(-3)", "-12-10+21"),
        ],
    },
}

TITLE = "正負の数　四則の混じった計算"
SEC = ["その1　かけ算＋たし算・ひき算", "その2　かけ算が2つ以上"]
CIRC = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯"


def fmt(e):
    out = []
    for i, ch in enumerate(e):
        prev = e[i - 1] if i else ""
        if ch == "*":
            out.append("<span class=op>×</span>")
        elif ch == "+":
            out.append("<span class=op>+</span>")
        elif ch == "-":
            out.append("−" if prev in ("", "(") else "<span class=op>−</span>")
        else:
            out.append(ch)
    return "".join(out)


def num(v):
    return str(v).replace("-", "−")


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; }
.page { width: 210mm; height: 297mm; padding: 14mm 15mm 12mm; page-break-after: always;
        display: flex; flex-direction: column; }
.page:last-child { page-break-after: auto; }
.head { display: flex; justify-content: space-between; align-items: flex-end;
        border-bottom: 1.6pt solid #111; padding-bottom: 2.5mm; }
.title { white-space: nowrap; font-size: 17pt; font-weight: 700; letter-spacing: .02em; }
.title small { display: block; font-size: 11pt; font-weight: 400; margin-top: 1mm; }
.name { font-size: 11pt; display: flex; gap: 4mm; white-space: nowrap; }
.name span { display: inline-block; border-bottom: .8pt solid #111; }
.name .n { width: 42mm; } .name .s { width: 22mm; text-align: right; }
.tip { margin-top: 3mm; font-size: 10.5pt; background: #f1f1f1; border-radius: 2mm; padding: 2mm 4mm; }
.grid { flex: 1; display: grid; grid-template-columns: 1fr 1fr; margin-top: 4mm; }
.col { display: grid; grid-template-rows: repeat(4, 1fr); }
.col:first-child { border-right: .8pt dashed #999; padding-right: 6mm; }
.col:last-child { padding-left: 6mm; }
.q { border-bottom: .6pt solid #ccc; padding-top: 3mm; position: relative; }
.col .q:last-child { border-bottom: none; }
.expr { font-size: 15pt; font-family: 'Noto Serif CJK JP', serif; }
.no { font-family: 'Noto Sans CJK JP'; font-size: 14pt; margin-right: 2.5mm; }
.op { margin: 0 .9mm; }
.ansbox { position: absolute; right: 0; bottom: 3mm; font-size: 10.5pt; }
.ansbox span { display: inline-block; width: 28mm; border-bottom: .8pt solid #111; }
.agrid { margin-top: 6mm; display: grid; grid-template-columns: 1fr 1fr; column-gap: 10mm; }
.sec { grid-column: 1 / -1; font-weight: 700; font-size: 12pt; margin: 4mm 0 1mm;
       border-left: 3pt solid #111; padding-left: 2mm; }
.a { font-family: 'Noto Serif CJK JP', serif; font-size: 12.5pt; padding: 2.6mm 0;
     border-bottom: .5pt solid #ddd; line-height: 1.7; }
.a .res { font-weight: 700; }
.a .st { color: #555; }
"""


def build(key, pat):
    P = pat["probs"]
    assert len(P) == 16, f"{key}: 問題は16個（{len(P)}個あります）"
    ans = []
    for q, s in P:
        a, b = eval(q), eval(s)
        assert a == b and a == int(a), (key, q, s, a, b)
        ans.append(int(a))

    def qhtml(i):
        return (f"<div class=q><div class=expr><span class=no>{CIRC[i]}</span>{fmt(P[i][0])}</div>"
                f"<div class=ansbox>答え <span></span></div></div>")

    def page(k, tip):
        left = "".join(qhtml(k * 8 + j) for j in range(4))
        right = "".join(qhtml(k * 8 + 4 + j) for j in range(4))
        label, sub = SEC[k].split("　")
        return f"""<div class=page>
<div class=head><div class=title>{TITLE} {key} {label}<small>{sub}</small></div>
<div class=name>名前<span class=n></span><span class=s>/ 8</span></div></div>
<div class=tip>{tip}</div>
<div class=grid><div class=col>{left}</div><div class=col>{right}</div></div></div>"""

    prob = f"""<html><head><meta charset=utf-8><style>{CSS}</style></head><body>
{page(0, "ポイント：<b>かけ算を先に</b>計算してから、たし算・ひき算をしよう。　" + pat["example"])}
{page(1, "ポイント：かけ算をぜんぶ先に計算して、<b>たし算・ひき算だけの式</b>にしてから答えを出そう。")}
</body></html>"""

    rows = [f"<div class=a>{CIRC[i]}　{fmt(q)}<br><span class=st>＝ {fmt(s)}</span>"
            f"　＝ <span class=res>{num(ans[i])}</span></div>" for i, (q, s) in enumerate(P)]

    def two_cols(lst):  # 左列に前半4問、右列に後半4問
        return "".join(a + b for a, b in zip(lst[:4], lst[4:]))

    ansh = f"""<html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class=page>
<div class=head><div class=title>{TITLE} {key} <small>こたえ</small></div></div>
<div class=agrid><div class=sec>{SEC[0]}</div>{two_cols(rows[:8])}<div class=sec>{SEC[1]}</div>{two_cols(rows[8:])}</div>
</div></body></html>"""
    return prob, ansh, ans


def main(keys):
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        for key in keys:
            prob, ansh, ans = build(key, PATTERNS[key])
            for html, name in [(prob, f"seifu_shisoku_{key}.pdf"), (ansh, f"seifu_shisoku_{key}_ans.pdf")]:
                pg.set_content(html)
                pg.wait_for_timeout(200)
                pg.pdf(path=str(OUT / name), format="A4", print_background=True)
            print(key, "こたえ:", ans)
        b.close()


if __name__ == "__main__":
    main(sys.argv[1:] or list(PATTERNS))
