"""数学プリントの共通部品（A4・1ページ左右2列×4問＝8問の形と、こたえページ）
授業・自習のプリントは4ページ（その1〜その4・32問）、こたえは2ページが基本。

  from mathlib import fm, problem_doc, answer_doc, write_pdfs

式の書き方（fm）：KaTeX で組む（11/3〜 文字式の文字は KaTeX の数式用イタリック＝先生の希望の書体）
  *  → ×　　/ → ÷　　{a|b} → 分数 a/b（中も同じ書き方）　　ほかは TeX のまま（x、(、= など）
  ポイント欄など、ふつうの文の中の式も tex("2x+3") や fm(...) で書く（Noto の斜体にしない）
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

from texlib import KATEX_CSS, _KATEX_JS, _RENDER, tex

OUT = Path(__file__).resolve().parent.parent / "pdf"
CIRC = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟"


def to_tex(e):
    """式の文字列を TeX にする（* → \\times、/ → \\div、{上|下} → \\dfrac）"""
    out, j = [], 0
    while j < len(e):
        ch = e[j]
        if ch == "{":
            depth, k = 1, j + 1
            while depth:
                depth += {"{": 1, "}": -1}.get(e[k], 0)
                k += 1
            inner = e[j + 1:k - 1]
            d, bar = 0, None
            for n, c in enumerate(inner):
                d += {"{": 1, "}": -1}.get(c, 0)
                if c == "|" and d == 0:
                    bar = n
                    break
            out.append(r"\dfrac{" + to_tex(inner[:bar]) + "}{" + to_tex(inner[bar + 1:]) + "}")
            j = k
            continue
        out.append({"*": r"\times ", "/": r"\div ", " ": ""}.get(ch, ch))
        j += 1
    return "".join(out)


def fm(e):
    """式を KaTeX で組む（文字式の文字は先生の希望の書体＝KaTeX の数式用イタリック）"""
    return tex(to_tex(e))


def fmb(e):
    """太字の式（こたえの答えの部分）"""
    return tex(r"\boldsymbol{" + to_tex(e) + "}")


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
.katex { font-size: 1.08em; }
.tip .katex, .scaf .katex { font-size: 1.02em; }
.a .katex { font-size: 1em; }
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
.ansbox .blank { display: inline-block; width: 26mm; border-bottom: .8pt solid #111; }
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
                         f"<div class=ansbox>{ans_label} <span class=blank></span></div></div>")
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
            html = html.replace("<head>", f"<head><style>{KATEX_CSS}</style><script>{_KATEX_JS}</script>", 1)
            html = html.replace("</body>", _RENDER + "</body>", 1)
            if not html.lstrip().lower().startswith("<!doctype"):
                html = "<!doctype html>" + html          # KaTeX は標準モードでないと動かない
            pg.set_content(html)
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
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


def calc_docs(title, secs, probs, fname, scaffold="", nonneg=False):
    """計算プリント（四則混合・計算の順序など）の問題とこたえを作る。
    secs：[(その1, 小見出し, ポイント), …]（1つ＝1ページ・8問）
    probs：secs と同じ数のリスト。中身は (式, [途中式…])。式は Python で計算できる書き方（* と /）。
    答えが整数か、途中式も同じ値か（nonneg=True なら途中も0以上か）を確かめる。"""
    flat, ans = [], []
    for sec in probs:
        assert len(sec) == 8, f"{title}: 1ページ8問（{len(sec)}問）"
        for q, steps in sec:
            v = eval(q)
            assert v == int(v), (title, q, v)
            for s in steps:
                assert eval(s) == v, (title, q, s, eval(s), v)
            if nonneg:
                assert v >= 0 and all(eval(s) >= 0 for s in steps), (title, q)
            flat.append((q, steps))
            ans.append(int(v))
    prob = problem_doc(title, [{"label": l, "sub": sub, "tip": tip, "scaffold": scaffold, "probs": [q for q, _ in sec]}
                               for (l, sub, tip), sec in zip(secs, probs)])
    rows = []
    for i, (q, steps) in enumerate(flat):
        mid = "".join(f"<span class=st>{fm('=' + s)}</span>　" for s in steps)
        rows.append(f"<div class=a>{CIRC[i]}　{fm(q)}<br>{mid}<span class=res>{fmb("=" + str(ans[i]))}</span></div>")
    asecs = [{"label": f"{l}　{sub}", "rows": rows[k * 8:(k + 1) * 8]} for k, (l, sub, _) in enumerate(secs)]
    ansh = answer_doc(title, asecs, pages=[len(secs) // 2] if len(secs) > 2 else None)
    return [(prob, f"{fname}.pdf"), (ansh, f"{fname}_ans.pdf")], ans


def num(v):
    return str(v).replace("-", "−")
