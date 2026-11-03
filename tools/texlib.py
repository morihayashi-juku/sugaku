"""KaTeX で式を組む PDF の共通部品（文字式の文字を、先生の希望の書体＝KaTeX の数式用イタリックにする）

  from texlib import tex, doc, write_pdfs, KATEX_CSS

- tex("x^2+7x+10=0") … 本文の中に置く式（TeX の書き方。分数は \\dfrac{1}{2}、≦ は \\leqq）
- doc(css, body) … 1つの PDF になる HTML を作る
- write_pdfs([(html, "ファイル名.pdf")]) … pdf/ に出力（A4。はみ出しがあれば「!! はみ出し」と出す）

KaTeX は pdf/ に入れず、作業環境のものを使う（/opt/npm-tools か、npm install katex した node_modules）。
"""
import base64
import html as _html
import re
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / "pdf"


def _dist():
    cands = [Path("/opt/npm-tools/node_modules/katex/dist"), Path.cwd() / "node_modules/katex/dist"]
    try:
        root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
        if root:
            cands.append(Path(root) / "katex/dist")
    except FileNotFoundError:
        pass
    for c in cands:
        if (c / "katex.min.js").exists():
            return c
    raise SystemExit("KaTeX が見つかりません。 npm install katex をしてから実行してください")


def _assets():
    d = _dist()

    def embed(mt):
        data = base64.b64encode((d / "fonts" / mt[1]).read_bytes()).decode()
        return f"url(data:font/woff2;base64,{data})"

    css = re.sub(r"url\(fonts/([\w-]+\.woff2)\)", embed, (d / "katex.min.css").read_text(encoding="utf-8"))
    return css, (d / "katex.min.js").read_text(encoding="utf-8")


KATEX_CSS, _KATEX_JS = _assets()

_RENDER = """<script>document.querySelectorAll('.tex').forEach(e =>
  katex.render(e.dataset.t, e, {throwOnError: true, strict: false}));</script>"""


def tex(t):
    return f'<span class=tex data-t="{_html.escape(t, quote=True)}"></span>'


def doc(css, body):
    return (f"<!doctype html><html><head><meta charset=utf-8><style>{KATEX_CSS}{css}</style>"
            f"<script>{_KATEX_JS}</script></head><body>{body}{_RENDER}</body></html>")


def write_pdfs(docs):
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 794, "height": 1123})
        for html, name in docs:
            pg.set_content(html)
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(300)
            bad = pg.evaluate("""() => {
              const r = [];
              document.querySelectorAll('.page').forEach((p, i) => {
                if (p.scrollHeight > p.clientHeight + 1) r.push('ページ' + (i + 1));
                p.querySelectorAll('.col').forEach((c, j) => {
                  if (c.scrollHeight > c.clientHeight + 1) r.push('ページ' + (i + 1) + ' 列' + (j + 1));
                });
              });
              return r;
            }""")
            if bad:
                print(f"!! はみ出し {name}: {bad}")
            pg.pdf(path=str(OUT / name), format="A4", print_background=True)
            print("書き出し:", name)
        b.close()
