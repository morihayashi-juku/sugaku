"""数学プリントの共通部品（A4・1ページ左右2列×4問＝8問の形と、こたえページ）

  from mathlib import fm, problem_doc, answer_doc, write_pdfs

式の書き方（fm）：
  *  → ×　　/ → ÷　　- → −（先頭・「(」「=」「{」「|」の直後は符号）　= → ＝
  {a|b} → 分数 a/b（中も同じ書き方）　　x → 斜体の x
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "pdf"
CIRC = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"


def fm(e):
    """式の文字列を HTML にする"""
    out, i = [], 0

    def sign_ok(prev):
        return prev in ("", "(", "=", "{", "|")

    def walk(s):
        res, j, prev = [], 0, ""
        while j < len(s):
            ch = s[j]
            if ch == "{":                       # 分数 {上|下}
                depth, k = 1, j + 1
                while depth:
                    depth += {"{": 1, "}": -1}.get(s[k], 0)
                    k += 1
                inner = s[j + 1:k - 1]
                d, bar = 0, None
                for n, c in enumerate(inner):
                    d += {"{": 1, "}": -1}.get(c, 0)
                    if c == "|" and d == 0:
                        bar = n
                        break
                res.append(f"<span class=fr><span class=nu>{walk(inner[:bar])}</span>"
                           f"<span class=de>{walk(inner[bar + 1:])}</span></span>")
                j, prev = k, "}"
                continue
            if ch == "*":
                res.append("<span class=op>×</span>")
            elif ch == "/":
                res.append("<span class=op>÷</span>")
            elif ch == "+":
                res.append("<span class=op>+</span>")
            elif ch == "=":
                res.append("<span class=eq>＝</span>")
            elif ch == "-":
                res.append("−" if sign_ok(prev) else "<span class=op>−</span>")
            elif ch == "x":
                res.append("<i>x</i>")
            elif ch == " ":
                j += 1
                continue
            else:
                res.append(ch)
            prev = ch
            j += 1
        return "".join(res)

    return walk(e)


CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans CJK JP', sans-serif; color: #111; }
.page { width: 210mm; height: 297mm; padding: 14mm 15mm 12mm; page-break-after: always;
        display: flex; flex-direction: column; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.head { display: flex; justify-content: space-between; align-items: flex-end;
        border-bottom: 1.6pt solid #111; padding-bottom: 2.5mm; }
.title { white-space: nowrap; font-size: 17pt; font-weight: 700; letter-spacing: .02em; }
.title small { display: block; font-size: 11pt; font-weight: 400; margin-top: 1mm; }
.name { font-size: 11pt; display: flex; gap: 4mm; white-space: nowrap; }
.name span { display: inline-block; border-bottom: .8pt solid #111; }
.name .d { width: 20mm; } .name .n { width: 38mm; } .name .s { width: 20mm; text-align: right; }
.tip { margin-top: 3mm; font-size: 10.5pt; background: #f1f1f1; border-radius: 2mm; padding: 2mm 4mm; line-height: 1.6; }
.tip .ex { font-family: 'Noto Serif CJK JP', serif; white-space: nowrap; }
.grid { flex: 1; display: grid; grid-template-columns: 1fr 1fr; margin-top: 3mm; min-height: 0; }
.col { display: grid; grid-template-rows: repeat(4, 1fr); min-height: 0; }
.col:first-child { border-right: .8pt dashed #999; padding-right: 6mm; }
.col:last-child { padding-left: 6mm; }
.q { border-bottom: .6pt solid #ccc; padding-top: 3mm; position: relative; overflow: hidden; }
.col .q:last-child { border-bottom: none; }
.expr { font-size: 15pt; font-family: 'Noto Serif CJK JP', serif; display: flex; align-items: center; flex-wrap: wrap; }
.no { font-family: 'Noto Sans CJK JP'; font-size: 14pt; margin-right: 2.5mm; }
.op { margin: 0 .9mm; } .eq { margin: 0 1.6mm; }
i { font-style: italic; font-family: 'Noto Serif CJK JP', serif; padding: 0 .3mm; }
.fr { display: inline-flex; flex-direction: column; align-items: center; vertical-align: middle;
      margin: 0 .6mm; line-height: 1.05; font-size: .9em; }
.fr .nu { padding: 0 1mm .5mm; border-bottom: .8pt solid #111; }
.fr .de { padding: .5mm 1mm 0; }
.scaf { margin-top: 2mm; font-size: 10.5pt; color: #333; line-height: 2.3; }
.scaf .box { display: inline-block; width: 13mm; height: 7mm; border: .8pt solid #555; border-radius: 1mm;
             vertical-align: middle; margin: 0 1mm; }
.scaf .ln { display: block; font-family: 'Noto Serif CJK JP', serif; font-size: 13pt; }
.scaf .ln::after { content: ""; display: inline-block; width: 52mm; border-bottom: .6pt solid #999; margin-left: 1mm; }
.ansbox { position: absolute; right: 0; bottom: 3mm; font-size: 10.5pt; background: #fff; padding-left: 2mm; }
.ansbox span { display: inline-block; width: 26mm; border-bottom: .8pt solid #111; }
.ansbox i { font-size: 12pt; }
/* こたえ */
.agrid { margin-top: 5mm; display: grid; grid-template-columns: 1fr 1fr; column-gap: 8mm; }
.sec { grid-column: 1 / -1; font-weight: 700; font-size: 12pt; margin: 3mm 0 1mm;
       border-left: 3pt solid #111; padding-left: 2mm; }
.a { font-family: 'Noto Serif CJK JP', serif; font-size: 11.5pt; padding: 2mm 0;
     border-bottom: .5pt solid #ddd; line-height: 1.55; }
.a .row { display: flex; flex-wrap: wrap; align-items: center; }
.a .res { font-weight: 700; }
.a .st { color: #555; white-space: nowrap; }
.a .res { white-space: nowrap; }
.a .hint { font-family: 'Noto Sans CJK JP'; font-size: 9pt; color: #b4232c; margin: 0 1mm; }
.a .fr { font-size: .85em; }
"""


def head(title, sub="", score=None, date=False, name=True):
    nm = "月　日<span class=d></span>" if date else ""
    nm += "名前<span class=n></span>" if name else ""
    if score:
        nm += f"<span class=s>/ {score}</span>"
    return (f"<div class=head><div class=title>{title}{f'<small>{sub}</small>' if sub else ''}</div>"
            f"<div class=name>{nm}</div></div>")


def problem_doc(title, sections, ans_label="答え"):
    """sections: [{label, sub, tip, probs:[式], scaffold: html か None}]（1つ＝1ページ・8問）"""
    pages, n = [], 0
    for sec in sections:
        cells = []
        for p in sec["probs"]:
            cells.append(f"<div class=q><div class=expr><span class=no>{CIRC[n]}</span>{fm(p)}</div>"
                         f"{sec.get('scaffold') or ''}"
                         f"<div class=ansbox>{ans_label} <span></span></div></div>")
            n += 1
        assert len(cells) == 8, f"{sec['label']}: 問題は8個（{len(cells)}個）"
        pages.append(f"""<div class=page>{head(title + ' ' + sec['label'], sec.get('sub', ''), score=8)}
<div class=tip>{sec['tip']}</div>
<div class=grid><div class=col>{''.join(cells[:4])}</div><div class=col>{''.join(cells[4:])}</div></div></div>""")
    return f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"


def answer_doc(title, sections, order="col", pages=None):
    """sections: [{label, rows:[html]}]。
    order="col"：左の列に前半・右の列に後半（問題ページの左右2列と同じ並び）／"row"：左→右の順（2×2の並び）
    pages：ページの区切り（例 [3] なら 1〜3つ目の section で1ページ、残りで2ページ目）"""
    cuts = [0, *(pages or []), len(sections)]
    out = []
    for a, b in zip(cuts, cuts[1:]):
        body = ""
        for sec in sections[a:b]:
            rows = sec["rows"]
            body += f"<div class=sec>{sec['label']}</div>"
            if order == "row":
                body += "".join(rows) + ("<div></div>" if len(rows) % 2 else "")
                continue
            h = (len(rows) + 1) // 2
            left, right = rows[:h], rows[h:]
            for k in range(h):
                body += left[k] + (right[k] if k < len(right) else "<div></div>")
        sub = "こたえ" + (f"（{len(out) + 1}/{len(cuts) - 1}）" if len(cuts) > 2 else "")
        out.append(f"<div class=page>{head(title, sub, name=False)}<div class=agrid>{body}</div></div>")
    return f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(out)}</body></html>"


def write_pdfs(docs, extra_css=""):
    """docs: [(html, ファイル名)]。はみ出しがあれば「!! はみ出し」と出す"""
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 794, "height": 1123})
        for html, name in docs:
            if extra_css:
                html = html.replace("</style>", extra_css + "</style>", 1)
            pg.set_content(html)
            pg.wait_for_timeout(200)
            bad = pg.evaluate("""() => {
              const r = [];
              document.querySelectorAll('.page').forEach((p, i) => {
                if (p.scrollHeight > p.clientHeight + 1) r.push('ページ' + (i + 1));
                p.querySelectorAll('.q').forEach((q, j) => { if (q.scrollHeight > q.clientHeight + 1) r.push('ページ' + (i + 1) + ' 問' + (j + 1)); });
              });
              return r;
            }""")
            if bad:
                print(f"!! はみ出し {name}: {bad}")
            pg.pdf(path=str(OUT / name), format="A4", print_background=True)
            print("書き出し:", name)
        b.close()
